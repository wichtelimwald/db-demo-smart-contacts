# ADR-0002: json-graphql-server für Stufe 2

**Status:** accepted  
**Datum:** 2025-06-01  
**Kontext:** Stufe 2 soll zeigen, wie aus einer JSON-Datei automatisch eine GraphQL-API entsteht – ohne Code, ohne Schema-Definition, ohne Build-Schritt. Gleichzeitig soll die Grenze dieses Ansatzes sichtbar werden.

## Entscheidung
`json-graphql-server` (Node.js) als Stufe-2-Server auf Port 3000.  
Gestartet via Docker: `npm run stage2` (lokal gepinnte Version via `package.json`).

## Begründung
- Kein eigener Code nötig – das ist der Demo-Punkt.
- GraphiQL automatisch enthalten, kein Extra-Setup.
- Implizites Schema aus JSON-Struktur – direkt erklärbares Konzept.
- Bekannte Grenze (selbstreferentielle Traversierung) ist bewusst Teil der Demo.

## Alternativen
- **Hasura + PostgreSQL** – abgelehnt: zu viel Setup (Docker, Postgres, Schema tracken), überwältigt Erstsemester.
- **Apollo Server** – abgelehnt: erfordert Resolver-Code → verwischt den Lehrpunkt „kein Code nötig".
- **PostgREST** – abgelehnt: kein GraphQL, anderes Konzept.

## Konsequenzen
- `contact_id`-Konvention in `contactGroups` → automatische Beziehungsauflösung in Stufe 2.
- `relatedTo` bleibt eingebettetes ID-Array – selbstreferentielle Traversierung nicht möglich.
- Diese Grenze ist expliziter Demo-Moment für den Übergang zu Stufe 3.

## Didaktische Auswirkung
Sehr hoch: Der Kontrast „kein Code → sofort GraphQL, aber limitiert" ist der stärkste Lehrpunkt der gesamten Demo.
