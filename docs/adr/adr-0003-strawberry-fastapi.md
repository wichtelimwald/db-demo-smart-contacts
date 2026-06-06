# ADR-0003: Strawberry + FastAPI für Stufe 3

**Status:** accepted  
**Datum:** 2025-06-01  
**Kontext:** Stufe 3 soll zeigen, was ein explizites Schema leistet: selbstreferentielle Traversierung, typsichere Resolver, REST parallel zu GraphQL. Python ist bereits im Projekt (yaml_to_json.py).

## Entscheidung
`strawberry-graphql` + `FastAPI` + `uvicorn` als Stufe-3-Server auf Port 8000.

## Begründung
- Python bereits im Projekt → kein zweiter Stack nötig.
- Schema direkt im Code lesbar (`@strawberry.type`) – guter Kontrast zu implizitem Schema.
- `strawberry.Private` ermöglicht interne Felder ohne Schema-Exposition.
- FastAPI liefert automatisch Swagger-Doku unter `/docs` – zweites Zugriffsmodell ohne Extra-Arbeit.
- Selbstreferenz (`Contact → relatedTo → Contact`) funktioniert out of the box.

## Alternativen
- **Hasura + PostgreSQL** – abgelehnt: zu schwerer Setup für Live-Demo, echte DB überlagert GraphQL-Lehrpunkt.
- **Ariadne** – abgelehnt: Schema als SDL-String, weniger Python-nativ als Strawberry.
- **Graphene** – abgelehnt: ältere API, weniger idiomatisch für moderne Python-Typen.

## Konsequenzen
- `_make_contact()` als Factory-Funktion notwendig (Strawberry-Einschränkung bei Selbstreferenz).
- Datenzugriff direkt aus `contacts.json` – keine echte DB, bewusste Vereinfachung.
- REST-Endpunkte (`/contacts`, `/groups`) zeigen: gleiche Daten, anderes Zugriffsmodell.

## Didaktische Auswirkung
Hoch: Die nebeneinander laufenden Ports 3000 und 8000 machen den Unterschied „implizit vs. explizit" live erlebbar.
