# Innovative Datenbank- und Informationssysteme
### Live-Demo · Vorlesung DHBW Karlsruhe

> **Leitthese:**  
> Daten zu speichern ist vergleichsweise leicht. Daten dauerhaft korrekt, verständlich, integrierbar, sicher und nutzbar zu halten – das ist der eigentliche Engpass moderner Informationssysteme.

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
- Eine produktive Persistenzarchitektur
- Die Persistenz ist bewusst vereinfacht (`contacts.yaml` und `contacts.json` als didaktische Stand-ins)
- In echten Systemen könnte darunter ein DBMS liegen, z. B. PostgreSQL,
  MongoDB, ein Graph Store oder eine Cloud-Datenbank

**Warum dieser Ansatz:**
Erst durch Datenmodell, Schema, Zugriff, Semantik und Traversierung wird aus
gespeicherten Daten ein Informationssystem. Das ist der didaktische Kern dieser Demo.

---

## Demo-Konzept: Vom Kontakt-Datensatz zum Informationssystem

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
Stufe 2 · json-graphql-server    automatisch erzeugte Demo-API mit implizitem Schema
              ↓                   → Grenze: selbstreferentielle Traversierung geht nicht
Stufe 3 · Strawberry + FastAPI   explizites Schema in Python, volle Kontrolle
                                  → Contact → relatedTo → Contact funktioniert
                                  → REST und GraphQL als zwei Zugriffsmuster
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
├── Dockerfile.stage2        ← Image für Stage 2 (npm ci beim Build)
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

## Offline-Hinweis

Die Demo ist offline lauffähig, nachdem Dev Container bzw. Docker-Images und
Dependencies einmal vorab gebaut/installiert wurden.

- Stage 2 installiert Node-Abhängigkeiten beim Image-Build mit `npm ci`.
- Beim Live-Start von Stage 2 erfolgt kein `npm install`.
- `package-lock.json` dient als reproduzierbare Grundlage.

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
docker compose up
```

| Server | URL |
|---|---|
| Stufe 2 · GraphiQL | http://localhost:3000 |
| Stufe 3 · GraphQL + GraphiQL | http://localhost:8000/graphql |
| Stufe 3 · REST + Swagger | http://localhost:8000/docs |

Nach Änderungen an `contacts.yaml`:
```bash
docker compose restart stage3
```

Stoppen:
```bash
docker compose down
```

---

## Option C – Lokal

```bash
# Python-Abhängigkeiten
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Stufe 2** – json-graphql-server (Demo-/Mocking-Werkzeug):
```bash
python3 yaml_to_json.py
npm ci
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

`json-graphql-server` ist hier bewusst ein Demo-Werkzeug: schnell nutzbar,
automatisch abfragbar, aber mit fachlichen Grenzen bei Semantik und Traversierung.

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

In echten Systemen können aus solchen rohen Referenzen Folgeabfragen entstehen
- bis hin zum N+1-Problem.

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

1. `contacts.yaml` öffnen.
2. Datenstruktur zeigen (menschenlesbar, noch keine Abfragesprache).
3. `yaml_to_json.py` als Mini-ETL erklären.
4. Stage 2 starten oder zeigen (`docker compose up stage2`).
5. Tatooine-Query aus `queries/02_tatooine_suche.graphql` ausführen.
6. Rohe IDs bei Han Solo mit `queries/03_han_rohe_ids.graphql` zeigen.
7. Stage 3 starten oder zeigen (`docker compose up stage3`).
8. Traversierung bei Han Solo mit `queries/04_han_traversierung.graphql` zeigen.
9. REST-/Swagger-Seite optional kurz zeigen (`/docs`).
10. Grenzen der Demo benennen (didaktischer Fokus statt Produktivbetrieb).

---

## Wenn die Zeit knapp wird

- Gruppen-Query (`queries/05_rebel_alliance_gruppe.graphql`) weglassen.
- REST-/Swagger-Seite nur erwähnen, nicht öffnen.
- Direkt von rohen IDs (Stufe 2) zur expliziten Traversierung (Stufe 3) wechseln.

---

## Fallback für Live-Demo

- Screenshots oder ein kurzes Video der Kernschritte vorab vorbereiten.
- Wichtigste Query-Ergebnisse lokal bereithalten.
- Bei Ausfall kann die Demo verbal entlang der Query-Dateien erklärt werden.

---

## Hinweise

- Beide Server können **gleichzeitig** laufen (Port 3000 und 8000).
- Alle Abfragen liegen als `.graphql`-Dateien in `queries/`
- Offline im Hörsaal: zuverlässig nach einmaligem Vorab-Build der Images/Dependencies.

---

## Lizenz

MIT – frei nutzbar für Lehr- und Bildungszwecke.
