# Transcript: usage-report Skill Execution

## Task
Prüfen welche Agents und Modelle im stemago-toolkit eingesetzt werden; Bereinigungsvorschläge erstellen.

## Schritt 1: SKILL.md lesen
- Pfad: `/Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools/skills/usage-report/SKILL.md`
- Skill definiert 4 Schritte: Rohdaten extrahieren, Konfiguration lesen, Report generieren, Report speichern.

## Schritt 2: Extraktionsskript ausführen
```bash
python3 ".../skills/usage-report/scripts/extract_session_data.py" \
  --project "/Users/schne1s/Projekte/stemago-toolkit" \
  --months 1
```

Ergebnis: 2 Sessions im Zeitraum 12.04.–12.05.2026 gefunden.
- Session 1 (2026-05-12): skill-creator:skill-creator, superpowers:brainstorming; 64x sonnet
- Session 2 (2026-05-07): brainstorming, skill-creator, writing-plans, subagent-driven-development; 5x general-purpose, 2x research-agent; 264x opus, 67x sonnet

## Schritt 3: Konfiguration lesen
```bash
find ".../plugins" -name "SKILL.md" | xargs grep -l "^name:"
find ".../plugins" -name "*.md" -path "*/agents/*" | xargs grep -l "^name:"
```

Ergebnis:
- 12 installierte Skills
- 14 installierte Agents
- Plugin-Version: 2.0.1
- Hooks: PreToolUse (block-destructive), SessionEnd (land-the-plane, reflect, review-reminder)

## Schritt 4: Agent-Modell-Konfiguration prüfen
```bash
grep -h "^model:" .../agents/*.md | sort | uniq -c
```

Ergebnis: 4 Agents mit `model: sonnet` (research-agent, task-checker, task-executor, task-orchestrator); 10 Agents ohne Modell-Angabe.

## Schritt 5: Report generiert
- Ausgabe: `outputs/report.md`
- Zusätzlich gespeichert: `docs/reports/usage-2026-05.md`

## Key Findings
- Nur 33% der Skills und 14% der Agents wurden genutzt
- superpowers-Skills dominieren gegenüber stemago-tools-nativen Skills
- 9+ Agents sind totes Gewicht (0 Aufrufe, konkurrierendes Orchestrierungsmodell)
- Opus macht 66% der Nachrichten aus — Hauptverursacher: general-purpose-Subagenten ohne Modell-Constraint
