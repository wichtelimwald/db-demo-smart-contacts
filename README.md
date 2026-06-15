# Innovative Datenbank- und Informationssysteme
### Live-Demo · Vorlesung DHBW Karlsruhe

> **Leitthese:**  
> Daten zu speichern ist einfach. Daten dauerhaft korrekt, verständlich, integrierbar, sicher und nutzbar zu halten – das ist der eigentliche Engpass moderner Informationssysteme.

---

## Kontext

Live-Demo zur 30-minütigen Vorlesung  
**„Innovative Datenbank- und Informations-Systeme – Herausforderungen und Potentiale"**  
DHBW Karlsruhe

Zielgruppe: Studierende im 2. Semester ohne Datenbankvorkenntnisse.

---

## Was diese Demo zeigt – und was sie bewusst nicht zeigt

**Was sie zeigt:**
- Wie sich ein Informationssystem schrittweise aus einfachen Daten entwickelt
- Die Rolle von Datenmodell, Schema und Zugriff
- Den Unterschied zwischen automatischem und explizitem Schema
- Traversierbare Beziehungen als Ergebnis semantischer Modellierung

**Was sie bewusst nicht zeigt:**
- Eine produktive Datenbankimplementierung
- Die Persistenzschicht ist vereinfacht (JSON-Datei statt DBMS)
- In echten Systemen läge darunter PostgreSQL, MongoDB, ein Graph Store
  oder eine Cloud-Datenbank – je nach Anforderung

**Warum dieser Ansatz:**
Erst durch Datenmodell, Schema und Zugriff wird aus gespeicherten Daten
ein Informationssystem. Das ist der didaktische Kern dieser Demo.

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
Das Problem entsteht von selbst – ohne Buzzwords.

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
│   ├── 02_tatooine_suche.graphql
│   ├── 03_han_rohe_ids.graphql
│   ├── 04_han_traversierung.graphql
│   └── 05_rebel_alliance_gruppe.graphql
│
├── Dockerfile               ← Image für FastAPI + Strawberry
├── docker-compose.yml       ← startet Stufe 2 und Stufe 3 gemeinsam
├── main.py                  ← FastAPI + Strawberry Server (Stufe 3)
├── requirements.txt         ← Python-Abhängigkeiten
├── yaml_to_json.py          ← Konvertierung YAML → JSON
├── .gitignore
└── README.md
```

---

## Voraussetzungen

**Option A (empfohlen): Docker**
```bash
docker --version        # Docker Desktop oder Docker Engine
docker compose version
```

**Option B: Lokal**
```bash
node --version    # v18+ (für Stufe 2)
python3 --version # 3.10+ (für Stufe 3)
```

---

## Setup

```bash
git clone https://github.com/wichtelimwald/db-demo-smart-contacts
cd db-demo-smart-contacts
```

---

## Option A – Dev Container in VS Code (empfohlen)

Voraussetzung: Docker + Extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installiert.

```bash
code .
# → VS Code: „Reopen in Container" klicken
```

Danach beide Server starten per `Cmd+Shift+B` → **Demo: Alle Server starten**.

| Server | URL |
|---|---|
| Stufe 2 · GraphiQL | http://localhost:3000 |
| Stufe 3 · GraphQL + GraphiQL | http://localhost:8000/graphql |
| Stufe 3 · REST + Swagger | http://localhost:8000/docs |

---

## Option B – Docker ohne VS Code

Ein Befehl startet beide Server:

```bash
docker-compose up
```

| Server | URL |
|---|---|
| Stufe 2 · GraphiQL | http://localhost:3000 |
| Stufe 3 · GraphQL + GraphiQL | http://localhost:8000/graphql |
| Stufe 3 · REST + Swagger | http://localhost:8000/docs |

Nach Änderungen an `contacts.yaml`:
```bash
docker-compose restart fastapi
```

Stoppen:
```bash
docker-compose down
```

---

## Option C – Lokal

```bash
# Python-Abhängigkeiten
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Stufe 2** – json-graphql-server:
```bash
python3 yaml_to_json.py
npm install
npm run stage2
# → GraphiQL: http://localhost:3000
```

**Stufe 3** – Strawberry + FastAPI (neues Terminal):
```bash
python3 main.py
# → GraphQL + GraphiQL:  http://localhost:8000/graphql
# → REST + Swagger Docs: http://localhost:8000/docs
```

Nach Änderungen an `contacts.yaml`:
```bash
python3 yaml_to_json.py
```

**Implizites Schema** (Stufe 2) – automatisch aus der JSON-Struktur.  
**Explizites Schema** (Stufe 3) – in Python definiert, volle Kontrolle.

---

## GraphQL

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

### Referenzauflösung und Traversierung

**Stufe 2** – Das System liefert nur rohe Referenz-IDs.
```graphql
{
  Contact(id: "6") {
    name
    relatedTo       # nur rohe ID-Referenzen – keine Traversierung möglich
  }
}
```

**Stufe 3**
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
> Explizites Schema, explizite Resolver, traversierbare Beziehungen."_

### Suche und Filter (nur Stufe 3)

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

## Demo-Ablauf (Presenter Guide)

1. `contacts.yaml` öffnen – menschenlesbare Daten zeigen,
   kein Schema, keine Abfragesprache
2. `yaml_to_json.py` kurz zeigen – Mini-ETL-Pipeline
   (Extract → Transform → Load)
3. Stufe 2 starten: `docker compose up stage2`
   → `json-graphql-server` auf Port 3000
4. `queries/02_tatooine_suche.graphql` in GraphiQL ausführen
   → Suche funktioniert automatisch
5. `queries/03_han_rohe_ids.graphql` ausführen
   → `relatedTo` liefert nur rohe IDs, keine Namen
   → Grenze des automatischen Schemas sichtbar machen
6. Stufe 3 starten: `docker compose up stage3`
   → FastAPI + Strawberry auf Port 8000
7. `queries/04_han_traversierung.graphql` in GraphiQL ausführen
   → `relatedTo` traversiert zu vollständigen Kontaktobjekten
   → Semantik durch explizites Schema
8. Swagger-UI (`/docs`) kurz zeigen
   → REST und GraphQL parallel verfügbar

---

## Hinweise

- Beide Server können **gleichzeitig** laufen (Port 3000 und 8000).
- Alle Abfragen liegen als `.graphql`-Dateien in `queries/`
- Demo läuft vollständig **offline**, kein Internet nötig.

---

## Lizenz

MIT – frei nutzbar für Lehr- und Bildungszwecke.
