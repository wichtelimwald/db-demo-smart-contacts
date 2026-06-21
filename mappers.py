"""
mappers.py - Zentrales Mapping raw -> Domain
────────────────────────────────────────────
Wandelt rohe JSON-Dictionaries in einfache Domainobjekte um.
"""

from __future__ import annotations

from domain import Contact, Group


def map_related_contact_id(raw: dict | int) -> int | None:
    if isinstance(raw, dict):
        return raw.get("id")
    if isinstance(raw, int):
        return raw
    return None


def map_contact(raw: dict) -> Contact:
    related_to = [
        contact_id
        for entry in (raw.get("relatedTo") or [])
        for contact_id in [map_related_contact_id(entry)]
        if contact_id is not None
    ]

    return Contact(
        id=raw["id"],
        name=raw["name"],
        alias=raw.get("alias"),
        species=raw.get("species"),
        organization=raw.get("organization"),
        relationship=raw.get("relationship"),
        met_at=raw.get("metAt"),
        met_when=raw.get("metWhen"),
        notes=raw.get("notes"),
        known_preferences=raw.get("knownPreferences") or [],
        related_to=related_to,
    )


def map_group(raw: dict) -> Group:
    return Group(id=raw["id"], name=raw["name"])