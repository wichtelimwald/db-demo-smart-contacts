"""
schema.py – GraphQL-Schema
───────────────────────────
Strawberry-Typen, Resolver und Schema-Instanz.
Datenzugriff ausschließlich über services.
"""

from __future__ import annotations
from typing import Optional

import strawberry
from strawberry import ID
from strawberry.schema.config import StrawberryConfig

from domain import Contact as DomainContact
import services as svc


def _id_to_int(value: ID | int | str) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


@strawberry.input(description="Filter-Objekt fuer Kontakt-Suche")
class ContactFilterInput:
    id: Optional[ID] = None
    q: Optional[str] = None
    name: Optional[str] = None
    organization: Optional[str] = None
    species: Optional[str] = None


# ── Typen ─────────────────────────────────────────────────────────────────────

@strawberry.type(description="Eine Gruppe / Kategorie von Kontakten")
class Group:
    id: int
    name: str

    @strawberry.field(description="Alle Kontakte in dieser Gruppe")
    def contacts(self) -> list[Contact]:
        return _to_contacts(svc.list_contacts_for_group(self.id))


@strawberry.type(description="Eine Person aus Lukes Kontaktliste")
class Contact:
    id: int
    name: str
    alias: Optional[str]
    species: Optional[str]
    organization: Optional[str]
    relationship: Optional[str]
    met_at: Optional[str]
    met_when: Optional[str]
    notes: Optional[str]
    known_preferences: list[str]

    _domain: strawberry.Private[DomainContact]

    @strawberry.field(description="Kontakte, die diese Person kennt (traversierbar)")
    def related_to(self) -> list[Contact]:
        related_contacts = [svc.get_contact(contact_id) for contact_id in self._domain.related_to]
        return [_to_contact(contact) for contact in related_contacts if contact is not None]

    @strawberry.field(description="Gruppen, denen dieser Kontakt angehört")
    def groups(self) -> list[Group]:
        return [Group(id=group.id, name=group.name) for group in svc.list_groups_for_contact(self.id)]


# ── Mapper Domain -> GraphQL (Contact) ───────────────────────────────────────

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


def _to_contacts(contacts: list[DomainContact]) -> list[Contact]:
    return [_to_contact(contact) for contact in contacts]


# ── Query (Resolver) ──────────────────────────────────────────────────────────

@strawberry.type
class Query:

    @strawberry.field(name="Contact", description="Einen Kontakt per ID abrufen")
    def contact(self, id: ID) -> Optional[Contact]:
        contact_id = _id_to_int(id)
        if contact_id is None:
            return None
        contact = svc.get_contact(contact_id)
        return _to_contact(contact) if contact else None

    @strawberry.field(name="allContacts", description="Alle Kontakte, optional gefiltert")
    def all_contacts(
        self,
        filter: Optional[ContactFilterInput] = None,
        name_contains: Optional[str] = None,
        organization: Optional[str] = None,
        species: Optional[str] = None,
    ) -> list[Contact]:
        contact_id: Optional[int] = None
        q: Optional[str] = None

        if filter:
            if filter.id is not None:
                contact_id = _id_to_int(filter.id)
                if contact_id is None:
                    return []
            q = filter.q
            if name_contains is None:
                name_contains = filter.name
            if organization is None:
                organization = filter.organization
            if species is None:
                species = filter.species

        contacts = svc.list_contacts(
            contact_id=contact_id,
            q=q,
            name_contains=name_contains,
            organization=organization,
            species=species,
        )
        return _to_contacts(contacts)

    @strawberry.field(name="allGroups", description="Alle Gruppen")
    def all_groups(self) -> list[Group]:
        return [Group(id=group.id, name=group.name) for group in svc.list_groups()]

    @strawberry.field(name="contactsInGroup", description="Alle Kontakte einer Gruppe (per Name)")
    def contacts_in_group(self, group_name: str) -> list[Contact]:
        contacts = svc.list_contacts_in_group(group_name)
        return _to_contacts(contacts)


# ── Schema-Instanz ────────────────────────────────────────────────────────────

schema = strawberry.Schema(
    query=Query,
    config=StrawberryConfig(auto_camel_case=False),
)
