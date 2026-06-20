"""
main.py – App-Setup
────────────────────
FastAPI-App, GraphQL-Router und REST-Endpunkte.
Schema:       schema.py
Datenzugriff: data_layer.py

GraphQL + GraphiQL:  http://localhost:8000/graphql
REST + Swagger:      http://localhost:8000/docs

Start:
  python main.py
  uvicorn main:app --reload
"""

from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from strawberry.fastapi import GraphQLRouter

import services as svc
from schema import schema


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Star Wars Contacts API",
    description="Demo-API – DHBW Karlsruhe",
    version="1.0.0",
)

app.include_router(GraphQLRouter(schema, graphql_ide="graphiql"), prefix="/graphql")


# ── REST-Endpunkte ────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/graphql")


@app.get("/contacts", tags=["REST"])
def list_contacts(name: Optional[str] = None):
    return svc.list_contacts(name_contains=name)


@app.get("/contacts/{contact_id}", tags=["REST"])
def get_contact(contact_id: int):
    raw = svc.get_contact(contact_id)
    if not raw:
        raise HTTPException(status_code=404, detail="Kontakt nicht gefunden")
    return raw


@app.get("/groups", tags=["REST"])
def list_groups():
    return svc.list_groups()


# ── Start ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
