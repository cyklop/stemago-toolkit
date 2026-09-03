# Changelog

Alle nennenswerten Änderungen am stemago-toolkit Plugin.
Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## 3.0.0 — 2026-09-03

Prompt-Audit (`/claude-api prompt-audit`) komplett umgesetzt. Report und Patch: `docs/reports/prompt-audit-2026-09-03.{md,patch}`.

### Breaking
- Agents entfernt (Duplikate ohne Aufrufer, 0 Aufrufe laut Usage-Report 2026-05):
  - `enhanced-quality-gate` → PASS/FAIL-Gate-Modus in `quality-agent` gefaltet
  - `completion-gate`, `task-checker` → Akzeptanzkriterien-Check in `quality-agent` (Gate 1) und `tdd-validation-agent` (Gate 3)
  - `readiness-gate` → `bd stats` / `bd blocked` im `task-orchestrator`
  - `task-executor` → Modellwahl-Heuristik und Task-Assignment-Template in `task-orchestrator`
- `task-orchestrator` arbeitet im Hub-Muster: plant und endet mit `Use the <agent> subagent to …`; der aufrufende Skill startet die Agents (Subagents können in Claude Code keine Subagents starten). Tools `Task` und Context7 entfernt.

### Added
- `redesign-studio`: Website-Redesign von Interview bis Handoff — Brief-Checkpoint in `brainstorms/`, Recherche-Subagents (haiku), N unterscheidbare HTML-Mockups mit Verifier, Vergleichsboard, Folgeseiten, Handoff-Paket. Liefert `scrollfx.js` (Reveal, Parallax, Sticky-Szenen mit `--p`, Zähler, Tilt, Reduced-Motion) mit. Eingearbeitet nach den Audit-Regeln: kein Claude-Design-Zweig, `Agent` statt `Task`, keine Zeilen-Obergrenzen, Pfade nach Plugin-Konvention.

### Changed
- Alle neun verbleibenden Agents neu geschrieben (2.141 → 411 Zeilen): Mermaid-Decision-Paths, `HANDOFF_TOKEN`/`COLLECTIVE_HANDOFF_READY`, Taskmaster-Reste (`--projectRoot`, `--prompt`, Status `done`), Routing auf nicht existierende Agents, „Crisis Protocol"-Register und Template-Stack-Annahmen (WSL2, CRA, Redux) entfernt. Zuständigkeiten, Two-Stage-Review und Status-Protokoll (`DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED`) erhalten.
- Context7-Tool-Namen vereinheitlicht auf `mcp__context7__resolve-library-id` + `mcp__context7__query-docs`.
- `research-agent`: Protokoll-Dateien (`.claude/docs/RESEARCH-*.md`, existierten nie) entfernt; darf jetzt nach `docs/research/` schreiben (Cache).
- `quality-agent`: bekommt `mcp__ide__getDiagnostics`; kein Beads-Pflichtabruf mehr bei Diff-Reviews.
- `land-the-plane`: bd-Befehle auf bd 1.x korrigiert (`--json`, `--closed-after` statt `--since`/`--format=json`).
- `reflect`, `reflect-config`, `CLAUDE.md`, `README.md`: Hook-Beschreibung an v2.4.2 angepasst (SessionStart-Reminder, keine automatische Reflection).
- `interview`, `review`: `advisor()`-Aufrufe durch Konsistenz- bzw. Plausibilitäts-Check ersetzt; `interview/REFERENCE.md` Orchestrator-Prompt auf Hub-Muster.
- `setup`: `sequential-thinking` von Core nach Optional; generierter CLAUDE.md-Block in Normallautstärke.
- `storm-research`: Wort-Obergrenzen in den Lens-/Verifier-Prompts durch qualitative Längenvorgabe ersetzt.
- `db-inspect`, `github-ops`, `browser-test`: projektspezifische Beispielwerte durch Platzhalter ersetzt.
- `AGENTS.md`: Landing-the-Plane-Regeln ohne Caps-Register, mit Begründung.

## 2.0.0 — 2026-05-07

### Breaking
- Konsolidierung: `init-project` + `beads-setup` + `mcp-setup` → `setup` mit Argumenten
  - `/init-project`  → `/setup --project`
  - `/beads-setup`   → `/setup --beads`
  - `/mcp-setup`     → `/setup --mcp`
  - Neu: `/setup --all` und interaktive Detection bei Aufruf ohne Argument
- Konsolidierung: `reflect-on` + `reflect-off` + `reflect-status` → `reflect-config` mit Argumenten
  - `/reflect-on`     → `/reflect-config --on`
  - `/reflect-off`    → `/reflect-config --off`
  - `/reflect-status` → `/reflect-config --status` (oder Default)

### Changed
- `review`: Beschreibung gegenüber `code-review:code-review` und Standard-`review` geschärft. Body unverändert.
- `setup`: idempotent — meldet bereits eingerichteten Zustand statt zu überschreiben. `--force` für bewusste Re-Init.
- Hooks: `session-reflect.sh` und `session-review-reminder.sh` zeigen die neuen Skill-Namen.
- Cross-References in `beads-ready`, `land-the-plane`, `reflect` aktualisiert.

### Fixed
- `block-destructive-commands.sh`: `git rm <path>` wurde fälschlich als `rm -rf` blockiert wenn der Pfad sowohl 'r' als auch 'f' enthielt (z.B. `reflect-*`). `git rm` ist nun whitelisted, da via git-Historie reversibel.

### Removed
- Skills `init-project`, `beads-setup`, `mcp-setup`, `reflect-on`, `reflect-off`, `reflect-status` (siehe Migration oben).

### Verifikation
- Alle drei optimierten Beschreibungen bestehen Subagent-Trigger-Eval (Threshold 80%):
  - `setup`: 95% (19/20)
  - `reflect-config`: 100% (20/20)
  - `review`: 100% (20/20)

### Migration
1. Eigene Skripte/Aliases aktualisieren: alte Skill-Namen durch neue Befehle ersetzen.
2. Plugin-Cache aktualisieren: `cd ~/.claude/plugins/marketplaces/stemago-toolkit && git pull`.
3. Plugin-Update: `claude plugin update stemago-tools@stemago-toolkit` oder `/plugin marketplace update stemago-toolkit`.

## 1.5.0
Vorgängerversion (siehe Git-Historie für Details).
