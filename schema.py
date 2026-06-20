"""
schema.py – GraphQL-Schema
───────────────────────────
Strawberry-Typen, Resolver und Schema-Instanz.
Datenzugriff ausschließlich über data_layer.
"""

from __future__ import annotations
from typing import Optional

import strawberry

from domain import Contact as DomainContact
from domain import Group as DomainGroup
from domain import RelatedContact as DomainRelatedContact
import services as svc


# ── Mapper Domain -> GraphQL ─────────────────────────────────────────────────

def _to_group(group: DomainGroup) -> Group:
    return Group(id=group.id, name=group.name)


def _to_related_contact(related_contact: DomainRelatedContact) -> RelatedContact:
    return RelatedContact(id=related_contact.id, relation=related_contact.relation)


def _to_contact(contact: DomainContact) -> Contact:
    return Contact(
        id=contact.id,
        name=contact.name,
        alias=contact.alias,
        species=contact.species,
        organization=contact.organization,
        relationship=contact.relationship,
        met_at=contact.met_at,
        met_when=contact.met_when,
        notes=contact.notes,
        known_preferences=contact.known_preferences,
        _domain=contact,
    )


# ── Typen ─────────────────────────────────────────────────────────────────────

@strawberry.type(description="Eine Gruppe / Kategorie von Kontakten")
class Group:
    id:   int
    name: str

    @strawberry.field(description="Alle Kontakte in dieser Gruppe")
    def contacts(self) -> list[Contact]:
        return [_to_contact(contact) for contact in svc.list_contacts_for_group(self.id)]


@strawberry.type(description="Ein Kontakt mit Beziehungstyp (Teil von relatedTo)")
class RelatedContact:
    id:       int
    relation: Optional[str]

    @strawberry.field(description="Der verknüpfte Kontakt – volle Traversierung")
    def contact(self) -> Optional[Contact]:
        contact = svc.get_contact(self.id)
        return _to_contact(contact) if contact else None


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

    _domain: strawberry.Private[DomainContact]

    @strawberry.field(description="Beziehungen zu anderen Kontakten (traversierbar)")
    def related_to(self) -> list[RelatedContact]:
        return [_to_related_contact(related_contact) for related_contact in self._domain.related_to]

    @strawberry.field(description="Gruppen, denen dieser Kontakt angehört")
    def groups(self) -> list[Group]:
        return [_to_group(group) for group in svc.list_groups_for_contact(self.id)]


# ── Query (Resolver) ──────────────────────────────────────────────────────────

@strawberry.type
class Query:

    @strawberry.field(description="Einen Kontakt per ID abrufen")
    def contact(self, id: int) -> Optional[Contact]:
        contact = svc.get_contact(id)
        return _to_contact(contact) if contact else None

    @strawberry.field(description="Alle Kontakte, optional gefiltert")
    def all_contacts(
        self,
        name_contains: Optional[str] = None,
        organization:  Optional[str] = None,
        species:       Optional[str] = None,
    ) -> list[Contact]:
        contacts = svc.list_contacts(
            name_contains=name_contains,
            organization=organization,
            species=species,
        )
        return [_to_contact(contact) for contact in contacts]

    @strawberry.field(description="Alle Gruppen")
    def all_groups(self) -> list[Group]:
        return [_to_group(group) for group in svc.list_groups()]

    @strawberry.field(description="Alle Kontakte einer Gruppe (per Name)")
    def contacts_in_group(self, group_name: str) -> list[Contact]:
        contacts = svc.list_contacts_in_group(group_name)
        return [_to_contact(contact) for contact in contacts]


# ── Schema-Instanz ────────────────────────────────────────────────────────────

schema = strawberry.Schema(
    query=Query,
    types=[Contact, Group, RelatedContact],
)
