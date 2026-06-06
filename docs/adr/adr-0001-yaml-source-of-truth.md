# ADR-0001: YAML als einzige Quelle der Wahrheit

**Status:** accepted  
**Datum:** 2025-06-01  
**Kontext:** Die Demo braucht eine menschenlesbare Datenbasis, die live im Editor gezeigt werden kann. Gleichzeitig muss ein maschinell verarbeitbares Format für die API-Server existieren.

## Entscheidung
`contacts.yaml` ist die einzige manuell editierte Datei.  
`contacts.json` wird immer über `yaml_to_json.py` generiert und nie direkt bearbeitet.

## Begründung
- YAML ist ohne Erklärung für Erstsemester lesbar.
- Die Konvertierung `YAML → JSON` ist selbst ein Lehrpunkt: Menschen lesen YAML, Systeme sprechen JSON.
- Konsistenz: eine Quelle, keine Synchronisationsprobleme.

## Alternativen
- **Direkt JSON editieren** – abgelehnt: JSON ist für Menschen schlechter lesbar, Fehleranfälligkeit höher.
- **SQLite als Quelle** – abgelehnt: zu viel Setup, kein direkter Editormoment möglich.
- **Beide Formate manuell pflegen** – abgelehnt: führt zwingend zu Inkonsistenzen.

## Konsequenzen
- `contacts.json` steht in `.gitignore` – wird bei Start generiert.
- Nach jeder YAML-Änderung muss `yaml_to_json.py` ausgeführt werden (Docker: `restart fastapi`).
- Die Konvertierung schafft Platz für didaktische Punkte: Typen, Normalisierung, Validierung.

## Didaktische Auswirkung
Positiv: Der Übergang YAML → JSON → API ist selbst ein Lehrstück über Datentransformation und Persistenzschichten.
