# Changelog

Alle nennenswerten Änderungen am stemago-toolkit Plugin.
Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

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
