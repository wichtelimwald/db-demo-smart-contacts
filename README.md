# Innovative Datenbank- und Informationssysteme
### Live-Demo · Probevorlesung DHBW Karlsruhe

> **Leitthese:**  
> Daten zu speichern ist einfach. Daten dauerhaft korrekt, verständlich, integrierbar, sicher und nutzbar zu halten – das ist der eigentliche Engpass moderner Informationssysteme.

---

## Kontext

Live-Demo zur 30-minütigen Probevorlesung  
**„Innovative Datenbank- und Informations-Systeme – Herausforderungen und Potentiale"**  
Berufungsverfahren Professur Informatik · DHBW Karlsruhe

Zielgruppe: Studierende im 2. Semester ohne Datenbankvorkenntnisse.

---

## Demo-Konzept: Die progressive Kontakt-Datenbank

Ein einziges, vertrautes Szenario als roter Faden:

> _„Ich möchte festhalten, wen ich kenne – und das nutzbar machen."_

| # | Leitfrage | Konzept |
|---|-----------|---------|
| 1 | Wo habe ich wen kennengelernt? | Datenspeicherung, Struktur |
| 2 | Wer gehört zu welcher Gruppe? | Beziehungen, Modellierung |
| 3 | Wie halte ich die Daten aktuell? | Updates, Versionierung |
| 4 | Gibt es Orte, wo bestimmte Kontakte wichtig sind? | Kontext, Verlinkung |
| 5 | Wie übernehme ich Updates automatisch? | Integration, APIs |
| 6 | Wer hat Recht, wenn zwei Quellen widersprechen? | Konsistenz, Merge-Konflikte |
| 7 | Wer darf was sehen? | Zugriffskontrolle, Governance |

---

## Demo-Dramaturgie: Drei Stufen

```
Stufe 1 · contacts.yaml          menschenlesbar, jeder versteht es
              ↓                   → Grenze: keine Abfragen, keine Beziehungen
Stufe 2 · json-graphql-server    implizites Schema, GraphQL out of the box
              ↓                   → Grenze: selbstreferentielle Traversierung geht nicht
Stufe 3 · Strawberry + FastAPI   explizites Schema in Python, volle Kontrolle
                                  → Contact → relatedTo → Contact funktioniert
                                  → REST und GraphQL parallel
```

Jede Stufe zeigt, was die vorherige nicht kann.  
Das Datenbankproblem entsteht von selbst – ohne Buzzwords.

---

## Dateistruktur

```
dhbw-db-demo/
│
├── data/
│   ├── contacts.yaml        ← menschenlesbare Quelle (hier editieren)
│   └── contacts.json        ← generiert, nie manuell editieren
│
├── queries/
│   ├── 01_alle_kontakte.graphql
│   ├── 02_gruppe_mit_kontakten.graphql
│   ├── 03_suche.graphql
│   └── 04_grenzen.graphql
│
├── main.py                  ← FastAPI + Strawberry Server (Stufe 3)
├── requirements.txt         ← Python-Abhängigkeiten
├── yaml_to_json.py          ← Konvertierung YAML → JSON
└── README.md
```

---

## Voraussetzungen

```bash
node --version    # v18+ (für Stufe 2)
python3 --version # 3.10+ (für Stufe 3)
```

---

## Setup

### Einmalig

```bash
git clone https://github.com/<username>/dhbw-db-demo.git
cd dhbw-db-demo

# Python-Abhängigkeiten installieren
pip install -r requirements.txt

# JSON aus YAML generieren
python3 yaml_to_json.py
```

Nach Änderungen an `contacts.yaml` immer:
```bash
python3 yaml_to_json.py
```

---

## Stufe 2 – json-graphql-server

```bash
npx json-graphql-server data/contacts.json
# → GraphiQL: http://localhost:3000
```

**Implizites Schema** – wird automatisch aus der JSON-Struktur abgeleitet.  
Kein Code, kein Setup, sofort abfragbar.

---

## Stufe 3 – Strawberry + FastAPI

```bash
python3 main.py
# → GraphQL + GraphiQL:  http://localhost:8000/graphql
# → REST + Swagger Docs: http://localhost:8000/docs
```

**Explizites Schema** – in Python definiert, volle Kontrolle.

---

## Abfragen im Vergleich

### Alle Kontakte

**Stufe 2 · json-graphql-server**
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

**Stufe 3 · Strawberry**
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

### Gruppe mit allen Mitgliedern

**Stufe 2**
```graphql
{
  allGroups(filter: { name: "Rebel Alliance" }) {
    id
    name
    contactGroups {
      contact { name organization }
    }
  }
}
```

**Stufe 3**
```graphql
{
  contactsInGroup(groupName: "Rebel Alliance") {
    name
    organization
  }
}
```

### Selbstreferentielle Traversierung – der Lehrmoment

**Stufe 2 · funktioniert nicht:**
```graphql
{
  Contact(id: "6") {
    name
    relatedTo       # liefert nur rohe IDs – kein Objekt dahinter
  }
}
```

**Stufe 3 · funktioniert:**
```graphql
{
  contact(id: 6) {
    name
    relatedTo {
      relation
      contact {
        name
        organization
        groups { name }
      }
    }
  }
}
```

> _„Das ist der Unterschied zwischen Daten ablegen und einem Informationssystem bauen:  
> Explizites Schema, echte Resolver, traversierbare Beziehungen."_

### Suche und Filter

**Stufe 3**
```graphql
{
  allContacts(nameContains: "Solo") {
    name
    organization
    relatedTo {
      relation
      contact { name }
    }
  }
}

{
  allContacts(organization: "Rebel") {
    name
    metAt
  }
}
```

### REST parallel (nur Stufe 3)

```bash
# Alle Kontakte
curl http://localhost:8000/contacts

# Einzelner Kontakt
curl http://localhost:8000/contacts/6

# Suche per Query-Parameter
curl "http://localhost:8000/contacts?name=Solo"

# Alle Gruppen
curl http://localhost:8000/groups
```

> _„Gleiche Daten, zwei Zugriffsmodelle – REST und GraphQL aus einer Codebasis."_

---

## Bekannte Grenze (Demo-Punkt Stufe 2)

`relatedTo` liefert in Stufe 2 nur rohe Objekte `[{"id": 8}, {"id": 7}]` –  
keine traversierbaren Contact-Objekte.

Das ist kein Bug, sondern die **Grenze des Tools** – und der Übergang zu Stufe 3.

---

## Hinweise zur Live-Demo

- Beide Server können **gleichzeitig** laufen (Port 3000 und 8000).
- Der Wechsel im Browser von 3000 → 8000 ist der Live-Lehrmoment.
- Alle Abfragen liegen als `.graphql`-Dateien in `queries/` – Copy/Paste, kein Tippen live.
- `contacts.yaml` **nicht** live editieren (einrückungsempfindlich).
- Demo läuft vollständig **offline**, kein Internet nötig.

---

## Lizenz

MIT – frei nutzbar für Lehr- und Bildungszwecke.
