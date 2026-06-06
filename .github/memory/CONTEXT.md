# CONTEXT.md
*Lebendes Dokument – bei Begriffsentwicklung aktualisieren.*

---

## Zweck
Lehrdemo – DHBW Karlsruhe.  
Thema: „Innovative Datenbank- und Informationssysteme – Herausforderungen und Potentiale"  
Zielgruppe: Studierende im 2. Semester, keine Datenbankvorkenntnisse.

**Leitthese:** Daten speichern ist einfach. Daten korrekt, verständlich, integrierbar, sicher und nutzbar zu halten – das ist der eigentliche Engpass.

---

## Demo-Stufen

| Begriff | Bedeutung |
|---|---|
| **Stufe 1** | `contacts.yaml` – menschenlesbare Quelle, kein Abfragesystem |
| **Stufe 2** | `json-graphql-server` auf Port 3000 – implizites Schema, GraphQL automatisch generiert |
| **Stufe 3** | `main.py` (FastAPI + Strawberry) auf Port 8000 – explizites Schema, volle Traversierung |
| **Eskalation** | Jede Stufe zeigt, was die vorherige nicht kann |

---

## Datenpipeline

```
contacts.yaml
    ↓  yaml_to_json.py
contacts.json
    ↓                    ↓
Stufe 2 (Port 3000)   Stufe 3 (Port 8000)
```

**Invariante:** `contacts.yaml` ist die einzige manuell editierte Datei.  
`contacts.json` wird immer generiert, nie direkt bearbeitet.

---

## Glossar

| Begriff | Definition |
|---|---|
| `contacts` | Hauptkollektion – 50 Star-Wars-Charaktere aus Lukes Perspektive |
| `groups` | Kategorien (Rebel Alliance, Jedi, …) – separate Kollektion |
| `contactGroups` | n:m Junction: Kontakt ↔ Gruppe (`contact_id`, `group_id`) |
| `relatedTo` | Eingebettetes Array `[{id, relation}]` im Kontakt – IDs, keine Traversierung in Stufe 2 |
| `metAt` | Ort des Kennenlernens (String) |
| `metWhen` | Zeitpunkt als String (z. B. `"0 BBY"`) – bewusst kein Datumstyp → Lehrdemo-Punkt |
| `organization` | Zugehörige Organisation / Fraktion |
| `relationship` | Beschreibung der Beziehung zu Luke |
| `knownPreferences` | Array von Strings – bekannte Vorlieben |
| `implizites Schema` | Schema automatisch aus Datenstruktur abgeleitet (Stufe 2) |
| `explizites Schema` | Schema in Code definiert, typsicher, traversierbar (Stufe 3) |
| `Selbstreferenz` | Contact → relatedTo → Contact – funktioniert nur in Stufe 3 |
| `N+1-Problem` | Stufe 2 liefert IDs statt Objekte → separate Abfragen pro ID nötig |
| `ADR` | Architectural Decision Record – dokumentierte Architekturentscheidung |

---

## Schlüsselentscheidungen

| ADR | Entscheidung |
|---|---|
| ADR-0001 | YAML als einzige Quelle der Wahrheit |
| ADR-0002 | json-graphql-server für Stufe 2 |
| ADR-0003 | Strawberry + FastAPI für Stufe 3 |
| ADR-0004 | Docker Compose für Demo-Setup |

---

## Didaktische Constraints
- Keine Änderung ohne Prüfung: „Bleibt das für Studierende im 2. Semester verständlich?"
- Komplexität ist nur erlaubt wenn sie einen sichtbaren Lehrpunkt trägt.
- `queries/*.graphql` sind Lehrmaterialien – Kommentare gehören dazu.
- Jede „Grenze" eines Tools ist ein expliziter Demo-Moment, keine Schwäche.
