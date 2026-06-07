"""
main.py – Star Wars Contacts API
─────────────────────────────────
FastAPI + Strawberry GraphQL

GraphQL:  http://localhost:8000/graphql
REST:     http://localhost:8000/docs

Unterschied zu json-graphql-server:
  → Explizites Schema in Python (kein implizites Schema)
  → Selbstreferentielle Traversierung funktioniert (Contact → relatedTo → Contact)
  → REST und GraphQL parallel aus einer Codebasis

Start:
  python main.py
  # oder mit Auto-Reload:
  uvicorn main:app --reload
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import strawberry
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from strawberry.fastapi import GraphQLRouter
import uvicorn


# ── Daten laden ──────────────────────────────────────────────────────────────

def _load() -> dict:
    path = Path(__file__).parent / "data" / "contacts.json"
    return json.loads(path.read_text(encoding="utf-8"))


_DATA             = _load()
_CONTACTS_BY_ID   = {c["id"]: c for c in _DATA["contacts"]}
_GROUPS_BY_ID     = {g["id"]: g for g in _DATA["groups"]}
_CONTACT_GROUPS   = _DATA["contactGroups"]   # [{id, contact_id, group_id}]


# ── Hilfsfunktion (Forward-Declaration wegen Selbstreferenz) ─────────────────

def _make_contact(raw: dict) -> "Contact":
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


# ── Strawberry Types ──────────────────────────────────────────────────────────

@strawberry.type(description="Eine Gruppe / Kategorie von Kontakten")
class Group:
    id:   int
    name: str

    @strawberry.field(description="Alle Kontakte in dieser Gruppe")
    def contacts(self) -> list[Contact]:
        ids = [
            cg["contact_id"]
            for cg in _CONTACT_GROUPS
            if cg["group_id"] == self.id
        ]
        return [
            _make_contact(_CONTACTS_BY_ID[cid])
            for cid in ids
            if cid in _CONTACTS_BY_ID
        ]


@strawberry.type(description="Ein Kontakt mit Beziehungstyp (Teil von relatedTo)")
class RelatedContact:
    id:       int
    relation: Optional[str]

    @strawberry.field(description="Der verknüpfte Kontakt – volle Traversierung")
    def contact(self) -> Optional[Contact]:
        raw = _CONTACTS_BY_ID.get(self.id)
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

    # Internes Feld – nicht im Schema sichtbar
    _related_raw: strawberry.Private[list]

    @strawberry.field(description="Beziehungen zu anderen Kontakten (traversierbar)")
    def related_to(self) -> list[RelatedContact]:
        return [
            RelatedContact(
                id=r["id"] if isinstance(r, dict) else r,
                relation=r.get("relation") if isinstance(r, dict) else None,
            )
            for r in self._related_raw
        ]

    @strawberry.field(description="Gruppen, denen dieser Kontakt angehört")
    def groups(self) -> list[Group]:
        group_ids = [
            cg["group_id"]
            for cg in _CONTACT_GROUPS
            if cg["contact_id"] == self.id
        ]
        return [
            Group(**_GROUPS_BY_ID[gid])
            for gid in group_ids
            if gid in _GROUPS_BY_ID
        ]


# ── Query ─────────────────────────────────────────────────────────────────────

@strawberry.type
class Query:

    @strawberry.field(description="Einen Kontakt per ID abrufen")
    def contact(self, id: int) -> Optional[Contact]:
        raw = _CONTACTS_BY_ID.get(id)
        return _make_contact(raw) if raw else None

    @strawberry.field(description="Alle Kontakte, optional nach Name filtern")
    def all_contacts(
        self,
        name_contains:    Optional[str] = None,
        organization:     Optional[str] = None,
        species:          Optional[str] = None,
    ) -> list[Contact]:
        results = list(_DATA["contacts"])
        if name_contains:
            results = [c for c in results if name_contains.lower() in c["name"].lower()]
        if organization:
            results = [c for c in results if organization.lower() in (c.get("organization") or "").lower()]
        if species:
            results = [c for c in results if species.lower() in (c.get("species") or "").lower()]
        return [_make_contact(c) for c in results]

    @strawberry.field(description="Alle Gruppen")
    def all_groups(self) -> list[Group]:
        return [Group(**g) for g in _DATA["groups"]]

    @strawberry.field(description="Alle Kontakte einer Gruppe (per Name)")
    def contacts_in_group(self, group_name: str) -> list[Contact]:
        group = next(
            (g for g in _DATA["groups"] if g["name"].lower() == group_name.lower()),
            None,
        )
        if not group:
            return []
        ids = [cg["contact_id"] for cg in _CONTACT_GROUPS if cg["group_id"] == group["id"]]
        return [_make_contact(_CONTACTS_BY_ID[cid]) for cid in ids if cid in _CONTACTS_BY_ID]


# ── App ───────────────────────────────────────────────────────────────────────

schema = strawberry.Schema(
    query=Query,
    types=[Contact, Group, RelatedContact],
)

app = FastAPI(
    title="Star Wars Contacts API",
    description="Demo-API für die Probevorlesung DHBW Karlsruhe",
    version="1.0.0",
)

# GraphQL-Endpunkt
graphql_router = GraphQLRouter(schema, graphql_ide="graphiql")
app.include_router(graphql_router, prefix="/graphql")


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/graphql")


# REST-Endpunkte (zeigt: gleiche Daten, anderes Zugriffsmodell)
@app.get("/contacts", tags=["REST"])
def list_contacts(name: Optional[str] = None):
    results = _DATA["contacts"]
    if name:
        results = [c for c in results if name.lower() in c["name"].lower()]
    return results


@app.get("/contacts/{contact_id}", tags=["REST"])
def get_contact(contact_id: int):
    raw = _CONTACTS_BY_ID.get(contact_id)
    if not raw:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Kontakt nicht gefunden")
    return raw


@app.get("/groups", tags=["REST"])
def list_groups():
    return _DATA["groups"]


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
