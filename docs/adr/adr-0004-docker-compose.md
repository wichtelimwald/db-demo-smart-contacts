# ADR-0004: Docker Compose für Demo-Setup

**Status:** accepted  
**Datum:** 2025-06-01  
**Kontext:** Die Demo muss zuverlässig auf dem Vorlesungsrechner starten – unabhängig von lokaler Python-Version, Node-Version oder virtualenv-Zustand. Auf macOS mit Homebrew-Python schlägt `pip install` ohne `--break-system-packages` fehl.

## Entscheidung
`docker-compose.yml` mit zwei Services: `json-graphql` (Node 20 Alpine) und `fastapi` (Python 3.12 Slim).  
`docker-compose up` startet beide Server. Kein weiteres Setup nötig.

## Begründung
- Ein Befehl, zwei Server, reproduzierbar auf jedem Rechner mit Docker.
- Kein Venv-Management, kein `source .venv/bin/activate`.
- `contacts.yaml` bleibt als Volume gemountet → live editierbar ohne Rebuild.
- `yaml_to_json.py` läuft automatisch beim Containerstart (CMD in Dockerfile).

## Alternativen
- **Lokales Venv** – abgelehnt: auf macOS + Homebrew fehleranfällig (PEP 668), zu viele Setup-Schritte vor der Demo.
- **Nur Docker für FastAPI, Node lokal** – abgelehnt: halbgarer Mix erhöht Setup-Komplexität.
- **Dev Container** – abgelehnt: VS Code-spezifisch, überflüssig für diese Demo.

## Konsequenzen
- Docker muss auf dem Demo-Rechner installiert sein (Docker Desktop reicht).
- Erster `docker-compose up` lädt Images (~200 MB) – vorher testen.
- Nach YAML-Änderung: `docker-compose restart fastapi` (nicht `up` – vermeidet Image-Rebuild).

## Didaktische Auswirkung
Neutral: Docker ist für die Demo transparent – sichtbar sind nur die laufenden Server.  
Positiv als Nebenpunkt: „Ein Befehl startet eine ganze Infrastruktur" ist selbst ein moderner Software-Engineering-Punkt.
