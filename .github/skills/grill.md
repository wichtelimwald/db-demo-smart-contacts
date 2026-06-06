# Skill: grill
Hinterfrage jeden Plan systematisch – eine Frage nach der anderen.

Inspiriert von mattpocock/skills grill-with-docs.

---

## Vorgehen
1. Lies `.github/memory/CONTEXT.md` – prüfe ob der Plan zur bestehenden Sprache passt.
2. Lies relevante ADRs in `docs/adr/` – prüfe ob der Plan Vorentscheidungen widerspricht.
3. Erkunde Codebase für Fragen, die der Code beantworten kann – nicht fragen was bereits bekannt ist.
4. Stelle Fragen **einzeln** – warte auf Antwort bevor du weitermachst.
5. Liefere zu jeder Frage eine eigene Empfehlung als Ausgangspunkt.

## Prüfdimensionen
- **Terminologie**: Nutzt der Plan bestehende Begriffe aus CONTEXT.md korrekt?
- **Konsistenz**: Widerspricht der Plan einem bestehenden ADR?
- **Didaktik**: Bleibt die Änderung für Studierende im 2. Semester nachvollziehbar?
- **Minimalität**: Gibt es eine einfachere Lösung mit gleichem Lehreffekt?
- **Risiko**: Was kann schiefgehen – insbesondere bei der Live-Demo?

## Abschluss
- Aktualisiere CONTEXT.md wenn neue Begriffe oder Muster entstanden sind.
- Erstelle ein ADR wenn eine signifikante Architekturentscheidung gefallen ist → `.github/skills/adr.md`.
