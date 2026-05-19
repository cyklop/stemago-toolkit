# Transcript: usage-report --months 3

**Skill:** `stemago-tools:usage-report`
**Argument:** `--months 3`
**Date:** 2026-05-12
**Project:** `/Users/schne1s/Projekte/stemago-toolkit`

---

## Ausgeführte Schritte

### Schritt 0: SKILL.md gelesen
Pfad: `/Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools/skills/usage-report/SKILL.md`
Argumente geparst: `--months 3` → MONTHS=3, PROJECT_PATH=pwd

### Schritt 1: Rohdaten extrahiert

Befehl:
```bash
python3 /plugins/stemago-tools/skills/usage-report/scripts/extract_session_data.py \
  --project /Users/schne1s/Projekte/stemago-toolkit \
  --months 3
```

Ergebnis (Kurzfassung):
- 2 Sessions gefunden (2026-05-07 und 2026-05-12)
- Skill-Aufrufe: superpowers:brainstorming×2, skill-creator:skill-creator×2, superpowers:writing-plans×1, superpowers:subagent-driven-development×1
- Agent-Aufrufe: general-purpose×5, stemago-tools:research-agent×2
- Modelle: claude-opus-4-7×264, claude-sonnet-4-6×131, <synthetic>×1

### Schritt 2: Projekt-Konfiguration gelesen

Gefundene Skills (12):
- reflect-config, usage-report, db-inspect, reflect, docs-lookup, browser-test, setup, github-ops, interview, beads-ready, review, land-the-plane

Gefundene Agents (14):
- task-checker, tdd-validation-agent, completion-gate, functional-testing-agent, feature-implementation-agent, task-orchestrator, research-agent, enhanced-quality-gate, infrastructure-implementation-agent, component-implementation-agent, devops-agent, readiness-gate, quality-agent, task-executor

Plugin-Manifest: plugins/stemago-tools/.claude-plugin/plugin.json
Hooks: plugins/stemago-tools/hooks/hooks.json

### Schritt 3: Report generiert

Gap-Analyse durchgeführt:
- 0/12 stemago-tools Skills genutzt (alle extern: superpowers, skill-creator)
- 2/14 Agents genutzt (general-purpose, research-agent)
- Modell-Verteilung: 66% Opus → Optimierungspotenzial identifiziert

### Schritt 4: Report gespeichert

- Workspace-Output: `skills/usage-report-workspace/iteration-1/months-parameter/with_skill/outputs/report.md`
- Projekt-Report: `docs/reports/usage-2026-05.md`

---

## Kein Fehler aufgetreten

Das Extraktions-Skript gab kein `error`-Feld zurück. Alle Schritte erfolgreich.
