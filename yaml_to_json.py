#!/usr/bin/env python3
"""
yaml_to_json.py
───────────────
Konvertiert contacts.yaml → contacts.json für json-graphql-server.

Erzeugte Collections:
  contacts          Haupttabelle
  groups            Eindeutige Gruppen / Kategorien
  contactGroups     Kontakt ↔ Gruppe (n:m Junction, contact_id + group_id)
        Hinweis: related_to bleibt als Integer-ID-Array eingebettet.
  json-graphql-server kann selbstreferentielle Traversierung nicht auflösen.
  → Demo-Punkt: Grenze des Tools, Übergang zu echter DB.

Usage:
  python yaml_to_json.py
  python yaml_to_json.py --input data/contacts.yaml --output data/contacts.json
  python yaml_to_json.py --verbose
"""

import json
import argparse
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML fehlt.\nBitte installieren:  pip install pyyaml")


# ─── Hilfsfunktionen ────────────────────────────────────────────────────────

def clean_string(value) -> str | None:
    """Normalisiert mehrzeilige YAML-Block-Skalare auf eine Zeile."""
    if value is None:
        return None
    return " ".join(str(value).split())


def fail_with_validation_error(message: str) -> None:
    """Beendet das Skript mit einer klaren deutschen Fehlermeldung."""
    sys.exit(f"❌ Validierungsfehler: {message}")


FIELD_MAP = {
    "met_at": "met_at",
    "met_when": "met_when",
    "relationship": "relationship",
    "organization": "organization",
}

# Felder, die separat verarbeitet werden
SKIP_FIELDS = {"groups", "related_to", "known_preferences"}


def convert_contact(contact: dict) -> dict:
    """
    Konvertiert einen rohen YAML-Kontakt in ein JSON-freundliches Dict.
    - Felder in SKIP_FIELDS werden ausgelassen (separat behandelt)
    - known_preferences bleibt snake_case als String-Array
    - related_to bleibt snake_case als [id]-Array (eingebettet)
    - Mehrzeilige Strings werden normalisiert
    """
    result = {}

    for key, value in contact.items():
        if key in SKIP_FIELDS:
            continue
        out_key = FIELD_MAP.get(key, key)
        if isinstance(value, str):
            result[out_key] = clean_string(value)
        elif value is None:
            result[out_key] = None
        else:
            result[out_key] = value

    # known_preferences als sauberes String-Array
    prefs = contact.get("known_preferences") or []
    result["known_preferences"] = [clean_string(p) for p in prefs]


    # related_to → eingebettetes [id]-Array
    result["related_to"] = extract_related_ids(contact.get("related_to") or [])

    return result


# ─── Hauptlogik ──────────────────────────────────────────────────────────────

def build_groups(raw_contacts: list) -> tuple[list, dict]:
    """Extrahiert eindeutige Gruppen und gibt Collection + Lookup zurück."""
    name_to_id: dict[str, int] = {}
    groups: list[dict] = []
    gid = 1
    for contact in raw_contacts:
        for name in contact.get("groups") or []:
            if name not in name_to_id:
                name_to_id[name] = gid
                groups.append({"id": gid, "name": name})
                gid += 1
    return groups, name_to_id


def build_contact_groups(raw_contacts: list, name_to_id: dict) -> list:
    """n:m Junction-Tabelle: Kontakt ↔ Gruppe."""
    contact_groups = []
    cg_id = 1
    for contact in raw_contacts:
        contact_id = contact["id"]
        for group_name in contact.get("groups") or []:
            gid = name_to_id.get(group_name)
            if gid:
                contact_groups.append(
                    {"id": cg_id, "contact_id": contact_id, "group_id": gid}
                )
                cg_id += 1
    return contact_groups


def extract_related_ids(related_to: list) -> list:
    """Extrahiert nur Ziel-IDs aus related_to und ignoriert optionale relation-Texte."""
    ids = []
    for rel in related_to or []:
        if isinstance(rel, dict):
            to_id = rel.get("id")
        elif isinstance(rel, int):
            to_id = rel
        else:
            continue
        if to_id is not None:
            ids.append(to_id)
    return ids


def validate_contacts(raw_contacts: list[dict]) -> None:
    """Prueft die wichtigsten Datenregeln vor der Konvertierung."""
    missing_fields: list[str] = []

    for index, contact in enumerate(raw_contacts, start=1):
        contact_id = contact.get("id")
        for field_name in ("id", "name"):
            value = contact.get(field_name)
            if value is None or (isinstance(value, str) and not value.strip()):
                label = f"Kontakt an Position {index}"
                if contact_id is not None:
                    label = f"Kontakt mit ID {contact_id}"
                missing_fields.append(f"{label}: Pflichtfeld '{field_name}' fehlt")

    if missing_fields:
        raise ValueError("; ".join(missing_fields))

    contact_ids = [contact["id"] for contact in raw_contacts]
    duplicate_ids = sorted(contact_id for contact_id, count in Counter(contact_ids).items() if count > 1)
    if duplicate_ids:
        duplicates = ", ".join(str(contact_id) for contact_id in duplicate_ids)
        raise ValueError(f"Doppelte Kontakt-IDs gefunden: {duplicates}")

    existing_ids = set(contact_ids)
    invalid_references: list[str] = []
    for contact in raw_contacts:
        source_id = contact["id"]
        for entry in contact.get("related_to") or []:
            if isinstance(entry, dict):
                target_id = entry.get("id")
            elif isinstance(entry, int):
                target_id = entry
            else:
                continue

            if target_id is not None and target_id not in existing_ids:
                invalid_references.append(
                    f"Kontakt {source_id}: related_to verweist auf nicht existente ID {target_id}"
                )

    if invalid_references:
        raise ValueError("; ".join(invalid_references))


def main(input_path: Path, output_path: Path, verbose: bool = False):

    if not input_path.exists():
        sys.exit(f"❌ Datei nicht gefunden: {input_path}")

    with open(input_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    raw_contacts = data.get("contacts", [])
    if not raw_contacts:
        sys.exit("❌ Keine Kontakte in der YAML-Datei gefunden.")

    try:
        validate_contacts(raw_contacts)
    except ValueError as error:
        fail_with_validation_error(str(error))

    groups, name_to_id  = build_groups(raw_contacts)
    contacts            = [convert_contact(c) for c in raw_contacts]
    contact_groups      = build_contact_groups(raw_contacts, name_to_id)

    output = {
        "contacts":         contacts,
        "groups":           groups,
        "contactGroups":    contact_groups,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✓  {len(contacts):>3} contacts")
    print(f"✓  {len(groups):>3} groups")
    print(f"✓  {len(contact_groups):>3} contactGroups    (n:m Junction)")
    print(f"→  {output_path}")

    if verbose:
        print("\n── Gruppen ──────────────────────────────────────────")
        for g in groups:
            members = [
                c["name"]
                for c, rc in zip(contacts, raw_contacts)
                if g["name"] in (rc.get("groups") or [])
            ]
            print(f"   [{g['id']:>2}] {g['name']:<30} ({len(members)} Kontakte)")

        print("\n── related_to Stichprobe (erste 5 Kontakte mit Beziehungen) ─")
        contact_by_id = {c["id"]: c["name"] for c in contacts}
        shown = 0
        for c in contacts:
            if c.get("related_to") and shown < 5:
                rels = [contact_by_id.get(r, "?") for r in c["related_to"] if isinstance(r, int)]
                print(f"   {c['name']:<25} {', '.join(rels)}")
                shown += 1

    print(f"\nStart mit: json-graphql-server {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Konvertiert contacts.yaml → contacts.json für json-graphql-server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input",   default="data/contacts.yaml", type=Path)
    parser.add_argument("--output",  default="data/contacts.json",  type=Path)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    main(args.input, args.output, args.verbose)
