# Innovative Datenbank- und Informationssysteme
### Live-Demo · 30min Vorlesung DHBW Karlsruhe

> **Leitfrage der Demo:**
> Daten zu speichern ist einfach. Daten dauerhaft korrekt, verständlich, integrierbar, sicher und nutzbar zu halten – das ist der eigentliche Engpass moderner Informationssysteme.

---

## Kontext

Dieses Repository enthält die Live-Demo zur 30-minütigen Vorlesung
**„Innovative Datenbank- und Informations-Systeme – Herausforderungen und Potentiale"**

Zielgruppe: Studierende im 2. Semester ohne Datenbankvorkenntnisse.

---

## Demo-Konzept: Die progressive Kontakt-Datenbank

Die gesamte Demo dreht sich um **ein einziges, vertrautes Szenario:**

> _„Ich möchte festhalten, wen ich kenne – und das nutzbar machen."_

Sieben Leitfragen bauen aufeinander auf und zeigen, wie ein scheinbar einfaches Problem Schicht für Schicht komplexer wird:

| # | Leitfrage | Konzept |
|---|-----------|---------|
| 1 | Wo habe ich wen kennengelernt? | Datenspeicherung, Struktur |
| 2 | Wer gehört zu welcher Gruppe? | Beziehungen, Modellierung |
| 3 | Wie halte ich die Daten aktuell? | Updates, Versionierung |
| 4 | Gibt es Orte, wo bestimmte Kontakte wichtig sind? | Kontext, Verlinkung |
| 5 | Wie übernehme ich Updates automatisch? | Integration, APIs |
| 6 | Wer hat Recht, wenn zwei Quellen widersprechen? | Konsistenz, Merge-Konflikte |
| 7 | Wer darf was sehen? | Zugriffskontrolle, Governance |

**Dramaturgie:** Start mit einer einfachen JSON-Datei – jeder versteht es sofort.  
Dann zeigen wir live, wo es zerfällt. Am Ende entsteht das Datenbankproblem von selbst.

---

## Tech-Stack

| Komponente | Tool | Warum |
|---|---|---|
| Datenbasis | `contacts.json` | Kein Setup, sofort verständlich |
| Lesbare Version | `contacts.yaml` | Erklärung für Menschen |
| API + GraphQL | `json-graphql-server` | Auto-generiertes GraphQL-Schema + GraphiQL eingebaut |
| Editor | VS Code | Schema live editieren |
| Browser | beliebig | GraphiQL auf `localhost:3000` |

**Kein Docker. Kein Build. Kein Internet notwendig.**

---

## Voraussetzungen

```bash
node --version   # v18 oder neuer empfohlen
npm --version
```

Falls Node.js fehlt: [nodejs.org/en/download](https://nodejs.org/en/download)

---

## Setup

```bash
# Repository klonen
git clone https://github.com/<dein-username>/dhbw-db-demo.git
cd dhbw-db-demo

# json-graphql-server installieren (einmalig, global)
npm install -g json-graphql-server

# Demo starten
json-graphql-server data/contacts.json

# → GraphiQL läuft auf: http://localhost:3000
```

Fertig. Der gesamte Start dauert unter 30 Sekunden.

---

## Dateistruktur

```
dhbw-db-demo/
│
├── data/
│   ├── contacts.json        ← Datenbasis (wird von json-graphql-server gelesen)
│   └── contacts.yaml        ← Lesbare Version zur Erklärung (VS Code)
│
├── queries/
│   ├── 01_alle_kontakte.graphql
│   ├── 02_kontakt_mit_gruppe.graphql
│   ├── 03_kontakte_nach_location.graphql
│   └── 04_merge_konflikt_beispiel.graphql
│
├── slides/                  ← (optional) Begleitfolien / Whiteboard-Skizzen
│
└── README.md
```

---

## Demo-Ablauf (Schritt für Schritt)

### Schritt 1 – „Fangen wir einfach an"

`contacts.yaml` in VS Code öffnen und zeigen:

```yaml
# contacts.yaml – lesbare Version
- id: 1
  name: Anna Bauer
  email: anna@example.com
  met_at: "re:publica Berlin 2024"
  group: "Konferenz-Kontakte"

- id: 2
  name: Jonas Weber
  email: jonas@example.com
  met_at: "Bosch Workshop Stuttgart"
  group: "Arbeit"
```

> _„Jeder kennt das. Vielleicht habt ihr sowas ähnliches in einer Notiz-App."_

---

### Schritt 2 – Beziehungen werden unübersichtlich

Zeigen: Was passiert, wenn Anna in **zwei Gruppen** ist?  
Was passiert, wenn eine Gruppe **50 Mitglieder** hat?

→ JSON wächst unkontrolliert, Redundanz entsteht, Suchen werden fragil.

> _„Genau hier fängt das Datenbankproblem an."_

---

### Schritt 3 – GraphQL-API live (json-graphql-server)

Browser öffnen: [http://localhost:3000](http://localhost:3000)

**Abfrage 1: Alle Kontakte**
```graphql
{
  allContacts {
    id
    name
    email
    metAt
  }
}
```

**Abfrage 2: Kontakt mit Gruppe**
```graphql
{
  allContacts {
    name
    group {
      name
      category
    }
  }
}
```

**Abfrage 3: Nur Kontakte aus einer bestimmten Stadt**
```graphql
{
  allContacts(filter: { city: "Berlin" }) {
    name
    email
    metAt
  }
}
```

→ Zeigen: **Gleiche Daten, anderes Zugriffsmodell.**  
SQL hätte das mit einem JOIN gelöst. GraphQL gibt verschachteltes JSON zurück.

---

### Schritt 4 – Merge-Konflikt live erzeugen

`contacts.json` direkt in VS Code editieren:  
Anna Bauers E-Mail in zwei „Geräten" (zwei VS-Code-Tabs) unterschiedlich setzen.

> _„Wer hat Recht? Das ist kein technisches Problem – das ist ein Architekturproblem."_

Konzept zeigen: **Last-Write-Wins vs. Konfliktauflösung vs. Versionierung.**

---

### Schritt 5 – Übergang zur Kernaussage

> _„Wir haben gerade in 5 Minuten die wichtigsten Fragen moderner Informationssysteme berührt:  
> Struktur, Beziehungen, Konsistenz, Zugriffsmuster, Zugriffsrechte.  
> Das war noch keine Datenbank – aber genau deshalb brauchen wir eine."_

---

## Konzeptuelle Erweiterungen (Whiteboard / Folie)

Folgende Fragen werden **nicht live demonstriert**, aber direkt aus dem Demo-Szenario abgeleitet:

- **Zugriffsrechte:** Wer darf Annas private E-Mail sehen? → Zugriffskontrolle, Row-Level Security
- **Automatische Updates:** Kontakt ändert Arbeitgeber auf LinkedIn → CDC / Event-Driven
- **Orte mit Kontext:** „Welche Kontakte sind in München relevant?" → Geo, Graph, Kontext
- **Suche:** „Zeig mir alle, die ich auf Konferenzen 2024 kennengelernt habe" → Volltext, Semantik

---

## Lizenz

MIT – frei nutzbar für Lehr- und Bildungszwecke.
