# Skill: plan
Analysiere → Konzept → Plan → Review → Implementiere

Nutze diesen Workflow vor jeder nicht-trivialen Änderung.

---

## A – Analysiere
- Lies nur direkt relevante Dateien (nicht das gesamte Repo).
- Benenne: was existiert, was das Problem ist, was die Einschränkungen sind.
- Prüfe `.github/memory/CONTEXT.md` auf bestehende Begriffe und Muster.
- Prüfe `docs/adr/` auf relevante Vorentscheidungen.

## K – Konzept
- Schlage 2–3 mögliche Ansätze vor.
- Bewerte jeden kurz nach: Komplexität, Didaktik, Wartung.
- Empfehle einen Ansatz mit Begründung.

## P – Plan
- Liste konkrete Schritte in Reihenfolge.
- Benenne betroffene Dateien.
- Benenne Risiken und Abhängigkeiten.
- Schätze ab: ist ein neues ADR nötig? → `.github/skills/adr.md` laden.

## R – Review
- Stelle genau eine Rückfrage, falls etwas unklar ist.
- Erkunde Codebase zuerst – nur fragen, was nicht aus dem Code hervorgeht.
- Prüfe: Bleibt die Änderung für Studierende im 2. Semester verständlich?

## I – Implementiere
- Mache die kleinste sichere Änderung.
- Modifiziere keine nicht betroffenen Dateien.
- Abschlussmeldung: geprüfte Dateien · geänderte Dateien · offene Punkte.
