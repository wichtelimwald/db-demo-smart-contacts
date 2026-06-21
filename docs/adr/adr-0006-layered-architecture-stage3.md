# ADR-0006: Schichtenarchitektur für Stufe 3

**Status:** accepted  
**Datum:** 2026-06-20  
**Kontext:** Stufe 3 wuchs über eine einzelne Datei hinaus. Schema-Definition, Domäneobjekte, Datenzugriff und Geschäftslogik lagen zunächst zusammen in `main.py`. Um Lehrpunkte wie „Separation of Concerns" und Testbarkeit demonstrieren zu können, wurde die Logik aufgeteilt.

## Entscheidung
Stufe 3 gliedert sich in fünf Module mit klar definierten Verantwortlichkeiten:

| Modul | Aufgabe |
|---|---|
| `data_layer.py` | Lädt `contacts.json`, stellt indizierte Dictionaries bereit |
| `domain.py` | Einfache, API-freie Datenobjekte (`@dataclass(frozen=True)`) |
| `mappers.py` | Wandelt rohe JSON-Dicts in Domänenobjekte um (raw → domain) |
| `services.py` | Kapselt Abfrage- und Filterlogik (domain → domain) |
| `schema.py` | Strawberry-Typen und Resolver; Mapper domain → GraphQL |
| `main.py` | FastAPI-App, bindet GraphQL-Router und REST-Endpunkte ein |

Datenfluss (Leserichtung):
```
contacts.json
    → data_layer   (rohe dicts)
    → mappers      (domain objects)
    → services     (Abfragelogik)
    → schema       (GraphQL-Typen)
    → main         (HTTP-Layer)
```

## Begründung
- Jedes Modul ist isoliert testbar: `test_services.py` importiert nur `services`.
- `domain.py` und `services.py` enthalten kein Strawberry, kein FastAPI – sie sind framework-unabhängig und leicht verständlich.
- `mappers.py` zentralisiert das Mapping an einer Stelle; Änderungen am JSON-Format berühren nur `mappers.py`.
- Die Schichtung selbst ist ein didaktischer Lehrpunkt: das gleiche Prinzip wie in produktiven Systemen (Repository Pattern, Domain Layer).

## Alternativen
- **Alles in `main.py`** – abgelehnt: wird schnell unübersichtlich, nicht testbar.
- **ORM (SQLAlchemy)** – abgelehnt: zu schwerer Setup, überlagert den Lehrpunkt.
- **Pydantic-Modelle statt Dataclasses** – abgelehnt: Pydantic bringt Validierungslogik mit, die für die Demo nicht benötigt wird und Komplexität erhöht.

## Konsequenzen
- Fünf statt einer Python-Datei für Stufe 3 – auf einen Blick lesbar.
- `services.py`-Tests laufen ohne FastAPI/Strawberry-Abhängigkeit.
- Neue Felder in `contacts.yaml` berühren: `mappers.py` (Mapping), `domain.py` (Dataclass), `schema.py` (GraphQL-Typ).

## Didaktische Auswirkung
Mittel: Die Schichtung ist erklärbar als Mini-Abbild produktiver Systeme – ohne die Komplexität eines echten DBMS.
