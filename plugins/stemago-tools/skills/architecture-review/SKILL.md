---
name: architecture-review
description: "Architekturelle Reibungspunkte finden und Vertiefungs-Möglichkeiten vorschlagen — basierend auf dem Deep-Modules-Konzept (Ousterhout). Verwende wenn: die Codebase schwerer wartbar wird, Änderungen immer mehrere Dateien betreffen, Module zu viele Abhängigkeiten haben, oder ein strategischer Architektur-Check gewünscht ist. NICHT für normale Code-Reviews (dafür /review) oder Bug-Fixes (dafür /diagnose)."
argument-hint: "[pfad-oder-bereich]"
---

# Architecture Review — Deep Modules

Finde architekturelle Reibungspunkte und schlage Vertiefungs-Möglichkeiten vor.

## Schlüsselkonzepte

| Begriff | Bedeutung |
|---|---|
| **Tiefes Modul** | Viel Verhalten hinter einfacher Schnittstelle → hohe Leverage |
| **Flaches Modul** | Interface-Komplexität ≈ Implementierungs-Komplexität → Warnsignal |
| **Seam** | Stelle wo Verhalten ausgetauscht werden kann ohne Code zu ändern |
| **Lokalität** | Änderungen und Bugs bleiben in einem Modul konzentriert |

**Der Lösch-Test:** Wenn du ein verdächtiges Modul entfernst — konzentriert sich die Komplexität (es verdient seinen Platz) oder verteilt sie sich (es ist eine leere Schicht)?

## Phase 1: Explore — Reibungspunkte finden

Erkunde die Codebase (oder `$ARGUMENTS` falls angegeben):

```bash
# Häufig gemeinsam geänderte Dateien = fehlende Lokalität
git log --format=format: --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -20

# Dateien mit vielen Imports = potentiell flach
grep -r "^import" --include="*.ts" -l | xargs wc -l 2>/dev/null | sort -n | tail -20

# Zirkuläre Abhängigkeiten (falls madge installiert)
npx madge --circular --extensions ts src/ 2>/dev/null || true
```

**Warnsignale:**
- Dateien die bei jeder Änderung gemeinsam angefasst werden müssen
- Interfaces genauso komplex wie ihre Implementierung
- Viele kleine Wrapper-Module ohne eigene Logik
- Wissen verteilt über viele Dateien (fehlende Lokalität)
- Lange Argument-Listen die Implementierungsdetails durchreichen

## Phase 2: Kandidaten präsentieren

Liste 3-5 konkrete Vertiefungs-Kandidaten:

```markdown
### Kandidat: [Modul/Datei]
**Problem:** [Architekturelles Problem in einem Satz]
**Lösung:** [Wie würde ein tiefes Modul hier aussehen?]
**Gewinn:** [Leverage + Lokalität die entsteht]
**Aufwand:** klein | mittel | groß
```

Verwende CONTEXT.md-Terminologie falls vorhanden.
Schlage noch keine konkreten Interfaces vor — erst nach dem Grilling-Loop.

## Phase 3: Grilling-Loop

Für jeden vom User gewählten Kandidaten:

**Eine Frage nach der anderen** via **AskUserQuestion** — Designentscheidungen gemeinsam treffen:
- "Welche Caller würden sich durch das neue Interface ändern?"
- "Was passiert wenn [Edge Case] — wie verhält sich das tiefe Modul?"
- "Welcher Teil darf der Caller nicht wissen müssen?"

**Interface entwerfen:** Wie sieht die neue einfache Schnittstelle aus?

**Nach dem Grilling:**
- Neue Domain-Konzepte → in `CONTEXT.md` ergänzen
- Refactoring-Task in Beads anlegen:
  ```javascript
  mcp__beads__create({
    title: "Refactor: [Modul] vertiefen",
    description: "Problem: [...]\nLösung: [...]\nBetroffene Dateien: [...]",
    issue_type: "task",
    labels: ["architecture", "refactor"]
  })
  ```
- ADR anbieten wenn die Entscheidung Constraints enthält die spätere Reviews kennen sollten:
  `docs/adr/YYYY-MM-DD-<entscheidung>.md`
