# Skill: adr
Erstelle ein Architectural Decision Record.

Speicherort: `docs/adr/adr-NNNN-[titel-slug].md`  
Nächste Nummer: höchste bestehende Nummer + 1 (aus `docs/adr/` auslesen).

---

## Wann ein ADR nötig ist
- Eine neue Technologie oder ein neues Tool wird eingeführt.
- Eine bestehende Lösung wird durch eine andere ersetzt.
- Ein Kompromiss zwischen zwei gleichwertigen Optionen wird getroffen.
- Eine Entscheidung hat Auswirkung auf die Didaktik der Demo.

## Template

```markdown
# ADR-NNNN: [Titel]

**Status:** proposed | accepted | deprecated | superseded by ADR-XXXX  
**Datum:** YYYY-MM-DD  
**Kontext:** [Was ist das Problem? Welche Einschränkungen gelten?]

## Entscheidung
[Was wurde entschieden?]

## Begründung
[Warum diese Option? Was spricht dafür?]

## Alternativen
- [Option A] – abgelehnt weil: ...
- [Option B] – abgelehnt weil: ...

## Konsequenzen
- [Was wird einfacher?]
- [Was wird schwieriger oder muss beachtet werden?]

## Didaktische Auswirkung
[Bleibt die Demo für Studierende im 2. Semester verständlich?]
```

## Nach dem Erstellen
- Referenz in `.github/memory/CONTEXT.md` unter „Schlüsselentscheidungen" eintragen.
- Bei Ablösung einer bestehenden Entscheidung: altes ADR auf `superseded by ADR-NNNN` setzen.
