"""
services.py - Kleine Service-Schicht
────────────────────────────────────
Kapselt Abfrage- und Filterlogik fuer Kontakte und Gruppen.
Kein FastAPI, kein Strawberry.
"""

from __future__ import annotations

from typing import Optional

import data_layer as dl
from domain import Contact, Group
from mappers import map_contact, map_group


CONTACTS = [map_contact(raw) for raw in dl.DATA["contacts"]]
CONTACTS_BY_ID = {contact.id: contact for contact in CONTACTS}
GROUPS = [map_group(raw) for raw in dl.DATA["groups"]]
GROUPS_BY_ID = {group.id: group for group in GROUPS}


def get_contact(contact_id: int) -> Optional[Contact]:
    return CONTACTS_BY_ID.get(contact_id)


def list_contacts(
    contact_id: Optional[int] = None,
    q: Optional[str] = None,
    name_contains: Optional[str] = None,
    organization: Optional[str] = None,
    species: Optional[str] = None,
) -> list[Contact]:
    results = list(CONTACTS)
    if contact_id is not None:
        results = [contact for contact in results if contact.id == contact_id]
    if q:
        needle = q.lower()
        results = [
            contact
            for contact in results
            if any(
                needle in value
                for value in [
                    contact.name.lower(),
                    (contact.alias or "").lower(),
                    contact.species_text.lower(),
                    contact.organization_text.lower(),
                    (contact.relationship or "").lower(),
                    (contact.met_at or "").lower(),
                    (contact.met_when or "").lower(),
                    (contact.notes or "").lower(),
                    " ".join(contact.known_preferences).lower(),
                ]
            )
        ]
    if name_contains:
        needle = name_contains.lower()
        results = [contact for contact in results if needle in contact.name.lower()]
    if organization:
        needle = organization.lower()
        results = [contact for contact in results if needle in contact.organization_text.lower()]
    if species:
        needle = species.lower()
        results = [contact for contact in results if needle in contact.species_text.lower()]
    return results


def list_groups() -> list[Group]:
    return list(GROUPS)


def find_group_by_name(group_name: str) -> Optional[Group]:
    group_name_lower = group_name.lower()
    return next((group for group in GROUPS if group.name.lower() == group_name_lower), None)


def list_contact_ids_for_group(group_id: int) -> list[int]:
    return [cg["contact_id"] for cg in dl.CONTACT_GROUPS if cg["group_id"] == group_id]


def list_group_ids_for_contact(contact_id: int) -> list[int]:
    return [cg["group_id"] for cg in dl.CONTACT_GROUPS if cg["contact_id"] == contact_id]


def list_contacts_for_group(group_id: int) -> list[Contact]:
    contact_ids = list_contact_ids_for_group(group_id)
    return [CONTACTS_BY_ID[cid] for cid in contact_ids if cid in CONTACTS_BY_ID]


def list_groups_for_contact(contact_id: int) -> list[Group]:
    group_ids = list_group_ids_for_contact(contact_id)
    return [GROUPS_BY_ID[gid] for gid in group_ids if gid in GROUPS_BY_ID]


def list_contacts_in_group(group_name: str) -> list[Contact]:
    group = find_group_by_name(group_name)
    if not group:
        return []
    return list_contacts_for_group(group.id)
