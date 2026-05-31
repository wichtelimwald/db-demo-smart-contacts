#!/usr/bin/env python3
"""
yaml_to_json.py
───────────────
Konvertiert contacts.yaml → contacts.json für json-graphql-server.

Erzeugte Collections:
  contacts       Haupttabelle aller Kontakte
  groups         Eindeutige Gruppen / Kategorien
  contactGroups  Kontakt ↔ Gruppe (n:m Junction-Tabelle)
  relationships  Kontakt ↔ Kontakt (related_to Verweise)

Didaktischer Hinweis:
  Die vier Collections zeigen live, warum eine flache JSON-Datei
  nicht ausreicht, sobald Beziehungen ins Spiel kommen.

Usage:
  python yaml_to_json.py
  python yaml_to_json.py --input data/contacts.yaml --output data/contacts.json
  python yaml_to_json.py --verbose
"""

import json
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML fehlt.\n"
        "Bitte installieren:  pip install pyyaml"
    )


# ─── Hilfsfunktionen ────────────────────────────────────────────────────────

def clean_string(value) -> str | None:
    """Normalisiert mehrzeilige YAML-Block-Skalare auf eine Zeile."""
    if value is None:
        return None
    return " ".join(str(value).split())


FIELD_MAP = {
    "met_at": "metAt",
    "met_when": "metWhen",
    "relationship": "relationship",
    "organization": "organization",
}

# Felder, die separat verarbeitet werden
SKIP_FIELDS = {"groups", "related_to", "known_preferences"}


def convert_contact(contact: dict) -> dict:
    """
    Konvertiert einen rohen YAML-Kontakt in ein JSON-freundliches Dict.
    - Felder in SKIP_FIELDS werden ausgelassen (separat behandelt)
    - known_preferences wird als sauberes Array angehängt
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
    result["knownPreferences"] = [clean_string(p) for p in prefs]

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
                    {"id": cg_id, "contactId": contact_id, "groupId": gid}
                )
                cg_id += 1

    return contact_groups


def build_relationships(raw_contacts: list) -> list:
    """Selbstreferentielle Beziehungen aus related_to-Feldern."""
    relationships = []
    rel_id = 1

    for contact in raw_contacts:
        from_id = contact["id"]
        for rel in contact.get("related_to") or []:
            # Robuste Extraktion: {id: X} oder direkt X
            if isinstance(rel, dict):
                to_id = rel.get("id")
            elif isinstance(rel, int):
                to_id = rel
            else:
                to_id = None

            if to_id is not None:
                relationships.append(
                    {
                        "id": rel_id,
                        "fromContactId": from_id,
                        "toContactId": to_id,
                    }
                )
                rel_id += 1

    return relationships


def main(input_path: Path, output_path: Path, verbose: bool = False):

    # ── YAML laden ──────────────────────────────────────────────────────────
    if not input_path.exists():
        sys.exit(f"❌ Datei nicht gefunden: {input_path}")

    with open(input_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    raw_contacts = data.get("contacts", [])
    if not raw_contacts:
        sys.exit("❌ Keine Kontakte in der YAML-Datei gefunden.")

    # ── Collections aufbauen ─────────────────────────────────────────────────
    groups, name_to_id       = build_groups(raw_contacts)
    contacts                 = [convert_contact(c) for c in raw_contacts]
    contact_groups           = build_contact_groups(raw_contacts, name_to_id)
    relationships            = build_relationships(raw_contacts)

    # ── JSON schreiben ───────────────────────────────────────────────────────
    output = {
        "contacts":      contacts,
        "groups":        groups,
        "contactGroups": contact_groups,
        "relationships": relationships,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    # ── Zusammenfassung ──────────────────────────────────────────────────────
    print(f"✓  {len(contacts):>3} contacts")
    print(f"✓  {len(groups):>3} groups")
    print(f"✓  {len(contact_groups):>3} contactGroups   (n:m Junction)")
    print(f"✓  {len(relationships):>3} relationships   (contact ↔ contact)")
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

        print("\n── Beziehungen (Stichprobe, erste 10) ───────────────")
        contact_by_id = {c["id"]: c["name"] for c in contacts}
        for rel in relationships[:10]:
            frm = contact_by_id.get(rel["fromContactId"], "?")
            to  = contact_by_id.get(rel["toContactId"],   "?")
            print(f"   {frm:<25} → {to}")
        if len(relationships) > 10:
            print(f"   ... und {len(relationships) - 10} weitere")

    print("\nStart mit: json-graphql-server", output_path)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Konvertiert contacts.yaml → contacts.json für json-graphql-server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--input", default="data/contacts.yaml", type=Path,
        help="YAML-Quelldatei  (default: data/contacts.yaml)",
    )
    parser.add_argument(
        "--output", default="data/contacts.json", type=Path,
        help="JSON-Zieldatei   (default: data/contacts.json)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Gibt Gruppen und Beziehungen als Übersicht aus",
    )
    args = parser.parse_args()
    main(args.input, args.output, args.verbose)
