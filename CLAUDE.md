# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**stemago-toolkit** is a Claude Code plugin providing development workflows, specialized agents, and safety hooks. Version 3.3.0.

The plugin lives in `plugins/stemago-tools/` (skills, agents, hooks). The format conventions are visible in the existing files there. What the plugin expects from the projects that use it (for example the `CONTEXT.md` glossary) is documented in `README.md`.

## Testing the Plugin

```bash
# Run Claude with local plugin
claude --plugin-dir ./plugins/stemago-tools

# Verify skills appear (type "/" in Claude)
/stemago-tools:

# Test specific skill
/stemago-tools:beads-ready
```

## Issue Tracking with Beads

This project uses **Beads** (`bd`) for issue tracking instead of external systems.

```bash
bd ready              # Find tasks without blockers
bd show <id>          # View task details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd export -o .beads/issues.jsonl   # Issues als JSONL für Git schreiben (ohne -o: stdout)
```

## Release

- Beim Version-Bump drei Dateien synchron halten: `plugins/stemago-tools/.claude-plugin/plugin.json`, diese Datei (Project Overview) und `.claude-plugin/marketplace.json` (`metadata.version` und `plugins[0].version`). Ohne das Update in `marketplace.json` erkennt Claude Code keine neue Version.
- Zu jeder neuen Version gehört ein Eintrag oben in `CHANGELOG.md`.
- Der Marketplace-Clone unter `~/.claude/plugins/marketplaces/stemago-toolkit/` wird nicht automatisch gepullt. Nach einem `git push` dort `git pull` ausführen. Sonst liest Claude Code weiter die alte Version, egal wie oft `claude plugin update stemago-tools@stemago-toolkit` läuft.

## File Paths Convention

- Specs: `docs/specs/<feature-name>.md`
- Research cache: `docs/research/<topic>.md`
- Beads data: `.beads/issues.jsonl`
- Domain Language: `CONTEXT.md` (Projekt-Root)
- Bug Post-Mortems: `docs/post-mortems/<datum>-<bug>.md`
- Design-Mockups (`/redesign-studio`): `design/mockups/<richtung>/index.html`, Verifier-Reports `design/verify/`, Handoff `design/handoff-<slug>/`
- Build-Briefs (`/build-brief`): `docs/briefs/<datum>-<slug>.md` (der fertige Auftrags-Prompt, ohne Vorspann; das Interview dazu liegt als Capture unter `brainstorms/<datum>-brief-<slug>.md`, die Laufnotiz des späteren Laufs daneben als `docs/briefs/<datum>-<slug>.lauf.md`)
- Brainstorm-Captures: `brainstorms/<datum>-<topic-slug>.md` (Projekt-Root, bewusst NICHT unter `docs/` — ein vorhersehbarer Sammelort für rohe Interview-Erfassungen aus `/grill-me` und `/interview`. Polierte Ergebnisse wandern danach in `docs/` oder `projects/`.)

## Landing the Plane (Session Completion)

Der Session-Abschluss läuft über `/stemago-tools:land-the-plane`. Gepusht wird nach Rückfrage beim User. Schlägt Rebase oder Push fehl: nicht erzwingen, sondern den Fehler melden und im Handoff festhalten.

```bash
git pull --rebase
bd export -o .beads/issues.jsonl
git add .beads/issues.jsonl && git commit -m "chore: Beads-Export"   # nur nötig, wenn sich die Datei geändert hat
git push
bd dolt push         # Beads-Datenbank zum Dolt-Remote
git status  # sollte "up to date with origin" zeigen
```
