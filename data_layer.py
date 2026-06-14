"""
data_layer.py – Datenzugriff
─────────────────────────────
Lädt contacts.json und stellt indizierte Strukturen bereit.
Kein Strawberry, kein FastAPI – reine Datenschicht.
"""

import json
from pathlib import Path


def load() -> dict:
    path = Path(__file__).parent / "data" / "contacts.json"
    return json.loads(path.read_text(encoding="utf-8"))


DATA            = load()
CONTACTS_BY_ID  = {c["id"]: c for c in DATA["contacts"]}
GROUPS_BY_ID    = {g["id"]: g for g in DATA["groups"]}
CONTACT_GROUPS  = DATA["contactGroups"]   # [{id, contact_id, group_id}]
