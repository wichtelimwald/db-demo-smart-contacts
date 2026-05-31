# Innovative Datenbank- und Informationssysteme
### Live-Demo - Vorlesung DHBW Karlsruhe

> **Leitthese:**  
> Daten zu speichern ist einfach. Daten dauerhaft korrekt, verständlich, integrierbar, sicher und nutzbar zu halten - das ist der eigentliche Engpass moderner Informationssysteme.

---

## Kontext

Live-Demo zur 30-minütigen Vorlesung  
**"Innovative Datenbank- und Informations-Systeme - Herausforderungen und Potentiale"**  
Informatik - DHBW Karlsruhe

Zielgruppe: Studierende im 2. Semester ohne Datenbankvorkenntnisse.

---

## Demo-Konzept: Die progressive Kontakt-Datenbank

Ein einziges, vertrautes Szenario als roter Faden:

> _"Ich möchte festhalten, wen ich kenne - und das nutzbar machen."_

| # | Leitfrage | Konzept |
|---|-----------|---------|
| 1 | Wo habe ich wen kennengelernt? | Datenspeicherung, Struktur |
| 2 | Wer gehört zu welcher Gruppe? | Beziehungen, Modellierung |
| 3 | Wie halte ich die Daten aktuell? | Updates, Versionierung |
| 4 | Gibt es Orte, wo bestimmte Kontakte wichtig sind? | Kontext, Verlinkung |
| 5 | Wie übernehme ich Updates automatisch? | Integration, APIs |
| 6 | Wer hat Recht, wenn zwei Quellen widersprechen? | Konsistenz, Merge-Konflikte |
| 7 | Wer darf was sehen? | Zugriffskontrolle, Governance |

**Dramaturgie:** Start mit einer einfachen YAML-Datei - jeder versteht es sofort. Dann zeigen, wo es zerfällt. Das Datenbankproblem entsteht von selbst.

---

## Datenbasis: 50 Star-Wars-Kontakte aus Lukes Perspektive

`data/contacts.yaml` ist die menschenlesbare Quelle. `data/contacts.json` wird daraus generiert und enthält vier Collections:

| Collection | Einträge | Beschreibung |
|---|---|---|
| `contacts` | 50 | Alle Charaktere mit `relatedTo` als eingebettetem ID-Array |
| `groups` | 19 | Rebel Alliance, Jedi, Jabba's Hof, ... |
| `contactGroups` | 92 | n:m Junction: Kontakt <-> Gruppe |

> **Bekannte Grenze (Demo-Punkt):** `relatedTo` ist als Integer-Array direkt im Kontakt eingebettet. `json-graphql-server` kann selbstreferentielle Traversierung (`Contact -> Contact`) nicht auflösen - d. h. aus einer ID kann kein verschachteltes Contact-Objekt abgefragt werden. Diese Grenze ist bewusst Teil der Demo: Sie zeigt, wo ein Prototyping-Tool endet und eine echte Datenbank beginnt.

---

## Tech-Stack

| Komponente | Tool | Warum |
|---|---|---|
| Datenbasis (lesbar) | `contacts.yaml` | Kein Setup, sofort verständlich |
| Datenbasis (technisch) | `contacts.json` | Generiert, für json-graphql-server |
| Konvertierung | `yaml_to_json.py` | Python, keine Abhängigkeiten außer PyYAML |
| API + GraphQL | `json-graphql-server` | Auto-generiertes Schema + GraphiQL eingebaut |
| Editor | VS Code | Schema live zeigen |
| Browser | beliebig | GraphiQL auf `localhost:3000` |

**Kein Docker. Kein Build. Kein Internet notwendig.**

---

## Dateistruktur

```
dhbw-db-demo/
│
├── data/
│   ├── contacts.yaml        <- menschenlesbare Quelle (hier editieren)
│   └── contacts.json        <- generiert, nie manuell editieren
│
├── queries/
│   ├── 01_alle_kontakte.graphql
│   ├── 02_gruppe_mit_kontakten.graphql
│   ├── 03_suche.graphql
│   └── 04_grenzen.graphql
│
├── yaml_to_json.py          ← Konvertierungsskript
└── README.md
```

---

## Voraussetzungen

```bash
node --version   # v18+
python3 --version
pip install pyyaml
```

---

## Setup

```bash
git clone https://github.com/<username>/dhbw-db-demo.git
cd dhbw-db-demo

# JSON aus YAML generieren
python3 yaml_to_json.py

# Server starten
npx json-graphql-server data/contacts.json

# -> GraphiQL: http://localhost:3000
```

Nach Änderungen an `contacts.yaml`:
```bash
python3 yaml_to_json.py && npx json-graphql-server data/contacts.json
```

---

## Demo-Abfragen

### Alle Kontakte
```graphql
{
  allContacts {
    id
    name
    metAt
    organization
  }
}
```

### Einen Kontakt abrufen
```graphql
{
  Contact(id: "6") {
    name
    relationship
    organization
    metAt
    metWhen
    knownPreferences
    relatedTo
  }
}
```

### Alle Kontakte einer Gruppe
```graphql
{
  allGroups(filter: { name: "Rebel Alliance" }) {
    id
    name
    contactGroups {
      contact {
        name
        organization
      }
    }
  }
}
```

### Suche (case-insensitiv, Substring)
```graphql
{
  allContacts(filter: { q: "kriminell" }) {
    name
    organization
  }
}
```

### Alle Gruppen eines Kontakts
```graphql
{
  allContactGroups(filter: { contact_id: 9 }) {
    group {
      name
    }
  }
}
```

---

## Die Grenze - Demo-Punkt

Diese Abfrage **funktioniert nicht**:
```graphql
{
  Contact(id: "6") {
    relatedTo {
      name        # <- geht nicht: relatedTo ist ein Integer-Array, kein Objekt
    }
  }
}
```

`relatedTo` liefert nur `[8, 7, 15, 11]` - IDs, keine Namen.

> _"Um aus einer ID einen Namen zu machen, brauchen wir eine echte Datenbank mit Fremdschlüsseln, Joins und einem sauberen Schema. Genau das ist der Unterschied zwischen einem Prototyping-Tool und einem Informationssystem."_

**Nächster Schritt:** PostgreSQL + Hasura -> verschachtelte GraphQL-Abfragen mit echten Joins out of the box.

---

## Lizenz

MIT - frei nutzbar für Lehr- und Bildungszwecke.
