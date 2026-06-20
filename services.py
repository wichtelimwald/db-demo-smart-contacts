"""
services.py - Kleine Service-Schicht
────────────────────────────────────
Kapselt Abfrage- und Filterlogik fuer Kontakte und Gruppen.
Kein FastAPI, kein Strawberry.
"""

from __future__ import annotations

from typing import Optional

import data_layer as dl


def get_contact(contact_id: int) -> Optional[dict]:
    return dl.CONTACTS_BY_ID.get(contact_id)


def list_contacts(
    name_contains: Optional[str] = None,
    organization: Optional[str] = None,
    species: Optional[str] = None,
) -> list[dict]:
    results = list(dl.DATA["contacts"])
    if name_contains:
        needle = name_contains.lower()
        results = [c for c in results if needle in c["name"].lower()]
    if organization:
        needle = organization.lower()
        results = [c for c in results if needle in (c.get("organization") or "").lower()]
    if species:
        needle = species.lower()
        results = [c for c in results if needle in (c.get("species") or "").lower()]
    return results


def list_groups() -> list[dict]:
    return list(dl.DATA["groups"])


def find_group_by_name(group_name: str) -> Optional[dict]:
    group_name_lower = group_name.lower()
    return next((g for g in dl.DATA["groups"] if g["name"].lower() == group_name_lower), None)


def list_contact_ids_for_group(group_id: int) -> list[int]:
    return [cg["contact_id"] for cg in dl.CONTACT_GROUPS if cg["group_id"] == group_id]


def list_group_ids_for_contact(contact_id: int) -> list[int]:
    return [cg["group_id"] for cg in dl.CONTACT_GROUPS if cg["contact_id"] == contact_id]


def list_contacts_in_group(group_name: str) -> list[dict]:
    group = find_group_by_name(group_name)
    if not group:
        return []
    contact_ids = list_contact_ids_for_group(group["id"])
    return [dl.CONTACTS_BY_ID[cid] for cid in contact_ids if cid in dl.CONTACTS_BY_ID]
