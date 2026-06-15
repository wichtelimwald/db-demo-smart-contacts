# ADR-0005: Offline-Strategie für Live-Demo-Abhängigkeiten

**Status:** accepted  
**Datum:** 2026-06-15  
**Kontext:** Die Demo wird in einer Präsentationsumgebung ohne garantierten Internetzugang ausgeführt. Der bisherige Ansatz (`npx -y json-graphql-server`) zieht das Paket zur Laufzeit aus dem npm-Registry – das schlägt fehl, sobald kein Netz vorhanden ist.

## Entscheidung
Alle npm-Abhängigkeiten werden lokal über `package.json` verwaltet.  
`npm install` läuft beim Container-Build (Dockerfile) und beim Dev-Container-Setup (`postCreateCommand`).  
Der Stufe-2-Service verwendet `npm run stage2` statt `npx -y json-graphql-server`.

## Begründung
- `npx` ohne gecachtes Paket erfordert Internetzugang – inakzeptabel für eine Live-Demo.
- `package.json` mit gepinnter Version (`json-graphql-server: 2.6.2`) macht den Build reproduzierbar.
- `node_modules` liegt nach dem ersten Build vollständig im Container – kein Netz mehr nötig.
- Npm-Scripts sind ein Standard-Pattern; kein neues Konzept für den Demo-Stack.

## Alternativen
- **`npx` mit `--prefer-offline`** – abgelehnt: erfordert dass das Paket bereits im npm-Cache liegt, ist nicht zuverlässig garantierbar.
- **Eigenes Docker-Image bauen** – abgelehnt: mehr Komplexität, kein zusätzlicher Lehrpunkt.
- **Lokale Tarball-Datei** – abgelehnt: unübersichtlich, schwer zu warten.

## Konsequenzen
- Der Container-Build dauert beim ersten Mal länger (npm install lädt `json-graphql-server`).
- Nach dem ersten Build ist die Demo vollständig offline-fähig.
- `node_modules/` muss in `.gitignore` eingetragen bleiben.
- Dev-Container: `postCreateCommand` führt `npm install` vor `yaml_to_json.py` aus.

## Didaktische Auswirkung
Neutral: Studierende sehen nur den laufenden Server. Die Paketierungsstrategie ist Infrastruktur, kein Lehrpunkt.
