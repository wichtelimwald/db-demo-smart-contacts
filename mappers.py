"""
mappers.py - Zentrales Mapping raw -> Domain
────────────────────────────────────────────
Wandelt rohe JSON-Dictionaries in einfache Domainobjekte um.
"""

from __future__ import annotations

from domain import Contact, Group, RelatedContact


def map_related_contact(raw: dict | int) -> RelatedContact:
    if isinstance(raw, dict):
        return RelatedContact(id=raw["id"], relation=raw.get("relation"))
    return RelatedContact(id=raw)


def map_contact(raw: dict) -> Contact:
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
        related_to=[map_related_contact(entry) for entry in raw.get("relatedTo") or []],
    )


def map_group(raw: dict) -> Group:
    return Group(id=raw["id"], name=raw["name"])