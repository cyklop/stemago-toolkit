## Session-Handoff — Skill-Audit des stemago-tools Plugins, Releases 3.1.0 und 3.1.1

Stand: 2026-10-06 · Branch `main` · HEAD beim Schreiben `3710dbf` (plus Handoff-Commit)

### Erledigte Tasks
- keine Beads-Tasks (die Datenbank ist leer; die Arbeit lief ohne Tasks)

### Entscheidungen & was geliefert wurde
- Alle 22 Skills gegen Claude Code 2.1.291 und bd 1.3.1 geprüft; Details in `/Users/schne1s/Projekte/stemago-toolkit/CHANGELOG.md` (Abschnitte 3.1.0 und 3.1.1).
- `reflect` / `reflect-config` schreiben ins eingebaute Memory von Claude Code statt nach `.claude/learnings/project-learnings.md` — User-Entscheidung. Die alte Datei ist aus dem Repo entfernt, ihr Inhalt stand schon im Memory.
- `land-the-plane` fragt nach Commit & Push (User-Entscheidung „mit Rückfrage") und pusht danach die Beads-Datenbank, wenn ein Dolt-Remote konfiguriert ist.
- `interview`: Council-Stress-Test per Rückfrage statt Pflicht — User-Entscheidung.
- `github-ops` auf `gh` CLI umgeschrieben; die alten Tool-Namen gehörten zum abgekündigten `@modelcontextprotocol/server-github`.
- `setup`: Playwright → `@executeautomation/playwright-mcp-server` (passt zu den Tools des `functional-testing-agent`), GitHub-MCP → offizieller Remote-Server; beide Installationsbefehle wurden nicht ausgeführt.
- Kontext-Injektion (```` ```! ````) und `allowed-tools` in `beads-ready`, `land-the-plane`, `usage-report`.
- Eval-Daten liegen unter `/Users/schne1s/Projekte/stemago-toolkit/docs/evals/usage-report/` statt im Plugin.
- Beads: Schema v53 → v66 migriert (`bd migrate --force`), danach `bd dolt push` — beides auf ausdrückliche Anweisung des Users. Diese Maschine ist der Migrator. Backup des alten `.beads/`: `/Users/schne1s/.claude/backups-stemago-beads-20261006-142005`.
- `bd export` schreibt in bd 1.3.1 nach stdout; überall auf `bd export -o .beads/issues.jsonl` korrigiert.
- Plugin 3.1.1 ist installiert (`claude plugin update`), Marketplace-Clone steht auf `3710dbf`.

### Nächster Task
**keiner in Beads.** Sinnvoll als Nächstes: die noch nicht real durchgespielten Skills einmal benutzen (siehe „Offene Fragen").

### Wichtigste Dateien für die nächste Session
- `/Users/schne1s/Projekte/stemago-toolkit/CHANGELOG.md` — was sich in 3.1.0 / 3.1.1 geändert hat
- `/Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools/skills/` — die Skills selbst
- `/Users/schne1s/.claude/projects/-Users-schne1s-Projekte-stemago-toolkit/memory/bd-cli-drift.md` — bd-Eigenheiten (Export mit `-o`, Migration, Dolt-Push)
- Plan-/Spec-Datei: keine

### Running State
- Background-Prozesse: keine
- Dev-Server / Ports: keine
- Offene Worktrees / Branches: nur `main`; im Remote zusätzlich `__dolt_remote_info__` und `refs/dolt/data` (gehören bd, nicht löschen)

### Verifikation — so bestätigt man, dass alles noch läuft
- `claude plugin validate /Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools` — „Validation passed" ohne Warnungen
- `bd status` (im Repo) — Übersicht ohne Migrations-Warnung, 0 Issues
- `git -C /Users/schne1s/Projekte/stemago-toolkit status -sb` — `## main...origin/main` ohne Abweichung
- `python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json')))['plugins']['stemago-tools@stemago-toolkit'][0]['version'])"` — `3.1.1`

### Offene Fragen / Blocker / Deferred
- Deferred: `reflect`, `interview`, `review` und der Report-Teil von `usage-report` sind seit dem Umbau nicht in einem echten Durchlauf gelaufen — sie schreiben Dateien bzw. starten mehrere Agents und wurden nicht nur zum Testen ausgelöst.
- Deferred: ob das `allowed-tools`-Muster in `usage-report` den Permission-Prompt wirklich spart, zeigt erst der erste Aufruf.
- Deferred: `beads-ready` nennt in den Quick Actions noch `/land-the-plane` ohne Plugin-Präfix; `land-the-plane` Schritt 1 nutzt noch `ls .beads/` statt Injektion.
- Deferred: `docs-lookup` wurde nicht gegen Context7 getestet (Plugin-MCP braucht Authentifizierung).
- Offen: keine Frage an den User.

### Prompt für nächste Session
```
Fortsetzen bei: kein offener Beads-Task — stemago-tools 3.1.1 ist released und installiert.
Kontext: Skill-Audit abgeschlossen (CHANGELOG 3.1.0/3.1.1), Beads-DB migriert und per bd dolt push veröffentlicht.
Nächster Schritt: /stemago-tools:reflect, /stemago-tools:review oder /stemago-tools:interview einmal real benutzen und Auffälligkeiten fixen.
Branch: main
```
