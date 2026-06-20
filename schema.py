"""
schema.py – GraphQL-Schema
───────────────────────────
Strawberry-Typen, Resolver und Schema-Instanz.
Datenzugriff ausschließlich über data_layer.
"""

from __future__ import annotations
from typing import Optional

import strawberry

import data_layer as dl
import services as svc


# ── Factory ───────────────────────────────────────────────────────────────────

def _make_contact(raw: dict) -> Contact:
    return Contact(
        id                = raw["id"],
        name              = raw["name"],
        alias             = raw.get("alias"),
        species           = raw.get("species"),
        organization      = raw.get("organization"),
        relationship      = raw.get("relationship"),
        met_at            = raw.get("metAt"),
        met_when          = raw.get("metWhen"),
        notes             = raw.get("notes"),
        known_preferences = raw.get("knownPreferences") or [],
        _related_raw      = raw.get("relatedTo") or [],
    )


# ── Typen ─────────────────────────────────────────────────────────────────────

@strawberry.type(description="Eine Gruppe / Kategorie von Kontakten")
class Group:
    id:   int
    name: str

    @strawberry.field(description="Alle Kontakte in dieser Gruppe")
    def contacts(self) -> list[Contact]:
        ids = svc.list_contact_ids_for_group(self.id)
        return [_make_contact(dl.CONTACTS_BY_ID[cid]) for cid in ids if cid in dl.CONTACTS_BY_ID]


@strawberry.type(description="Ein Kontakt mit Beziehungstyp (Teil von relatedTo)")
class RelatedContact:
    id:       int
    relation: Optional[str]

    @strawberry.field(description="Der verknüpfte Kontakt – volle Traversierung")
    def contact(self) -> Optional[Contact]:
        raw = dl.CONTACTS_BY_ID.get(self.id)
        return _make_contact(raw) if raw else None


@strawberry.type(description="Eine Person aus Lukes Kontaktliste")
class Contact:
    id:                int
    name:              str
    alias:             Optional[str]
    species:           Optional[str]
    organization:      Optional[str]
    relationship:      Optional[str]
    met_at:            Optional[str]
    met_when:          Optional[str]
    notes:             Optional[str]
    known_preferences: list[str]

    _related_raw: strawberry.Private[list]

    @strawberry.field(description="Beziehungen zu anderen Kontakten (traversierbar)")
    def related_to(self) -> list[RelatedContact]:
        return [
            RelatedContact(
                id       = r["id"] if isinstance(r, dict) else r,
                relation = r.get("relation") if isinstance(r, dict) else None,
            )
            for r in self._related_raw
        ]

    @strawberry.field(description="Gruppen, denen dieser Kontakt angehört")
    def groups(self) -> list[Group]:
        group_ids = svc.list_group_ids_for_contact(self.id)
        return [Group(**dl.GROUPS_BY_ID[gid]) for gid in group_ids if gid in dl.GROUPS_BY_ID]


# ── Query (Resolver) ──────────────────────────────────────────────────────────

@strawberry.type
class Query:

    @strawberry.field(description="Einen Kontakt per ID abrufen")
    def contact(self, id: int) -> Optional[Contact]:
        raw = svc.get_contact(id)
        return _make_contact(raw) if raw else None

    @strawberry.field(description="Alle Kontakte, optional gefiltert")
    def all_contacts(
        self,
        name_contains: Optional[str] = None,
        organization:  Optional[str] = None,
        species:       Optional[str] = None,
    ) -> list[Contact]:
        results = svc.list_contacts(
            name_contains=name_contains,
            organization=organization,
            species=species,
        )
        return [_make_contact(c) for c in results]

    @strawberry.field(description="Alle Gruppen")
    def all_groups(self) -> list[Group]:
        return [Group(**g) for g in svc.list_groups()]

    @strawberry.field(description="Alle Kontakte einer Gruppe (per Name)")
    def contacts_in_group(self, group_name: str) -> list[Contact]:
        results = svc.list_contacts_in_group(group_name)
        return [_make_contact(c) for c in results]


# ── Schema-Instanz ────────────────────────────────────────────────────────────

schema = strawberry.Schema(
    query=Query,
    types=[Contact, Group, RelatedContact],
)
