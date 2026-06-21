# db-demo-smart-contacts

Lehrdemo – DHBW Karlsruhe.

## Stack
Python 3.12 · Node 20 · Docker Compose  
`contacts.yaml` → `yaml_to_json.py` → `contacts.json` → Stage 2 (Port 3000) + Stage 3 (Port 8000)

## Didaktische Leitlinie
Jede Änderung muss nachvollziehbar bleiben.
Komplexität, die keinen Lehrpunkt trägt, wird abgelehnt.

## Kontext laden
- Domain-Modell + Glossar: `.github/memory/CONTEXT.md`
- Architekturentscheidungen: `docs/adr/`

## Workflow (on-demand Skills)
- Vor jeder Änderung: `.github/skills/plan.md`
- Vor neuer Architekturentscheidung: `.github/skills/adr.md`
- Plan hinterfragen: `.github/skills/grill.md`

## Smart Context
1. Konkrete Aufgabe identifizieren.
2. Nur direkt relevante Dateien lesen – aktuelle Datei, Fehler, Importe, referenzierte Symbole.
3. Kontext nur erweitern wenn etwas Notwendiges fehlt – erst begründen, dann erweitern.
4. Kein vollständiges Repository-Scan ohne explizite Aufforderung.
5. Vor Bearbeitung nennen: relevante Dateien + warum + kleinste sichere Änderung.
6. Nach Bearbeitung nennen: geprüfte Dateien, geänderte Dateien, offene Unsicherheiten.
