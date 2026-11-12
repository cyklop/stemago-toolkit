# Changelog

Alle nennenswerten Änderungen am stemago-toolkit Plugin.
Format orientiert sich an [Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

## 3.3.0 — 2026-11-12

### Added
- `build-brief`: neuer Skill, der mit dem User ein Interview führt und daraus einen fertigen, für sich allein verständlichen Auftrags-Prompt liefert. Der User fügt ihn in eine neue Claude-Code-Session ein, wo er einen langen, eigenständigen Qualitätslauf auslöst. Der Prompt enthält zehn feste Bausteine: Einsatz und Publikum, Anfrage mit Referenz und ihren Lücken, ein Star, Konkretion, markierte Freiheit, „Was exzellent sein muss" mit Verbotsliste, Messlatte, Prüfschalter, Prozess mit Verbesserungsrunden und Stoppregel, Risikohinweise. Der Skill liest zuerst den Projektkontext und fragt nicht ab, was die `CLAUDE.md` schon regelt. Der Prompt landet unter `docs/briefs/<datum>-<slug>.md` und zusätzlich als Codeblock, das Interview-Capture unter `brainstorms/`.
- `build-brief/profiles/`: vier Plattform-Profile, die der Skill je nach Projekttyp lädt: `web.md` (Browser-Prüfung, Auflösungen, URL-Schalter), `apple.md` (visionOS, iOS, macOS), `backend.md` (Tests, Messwerte und Beispielausgaben statt Screenshots) und `general.md`. Jedes nennt, wie der Lauf sein Ergebnis zu sehen bekommt, welche Schalter für Zustände sinnvoll sind, welche Rolle der Kritiker hat und was sich in der Umgebung nicht prüfen lässt.
- `build-brief/profiles/apple.md`: Der Prüfweg für visionOS ist an Xcode 27.2 und dem visionOS-27.2-Simulator durchgespielt (Build, Start mit Startargumenten und Umgebungsvariablen, Screenshot und Video über `simctl`, Tests). Das Profil verlangt in jedem Prompt die Liste „Am Gerät zu prüfen", die der Lauf im Schlussbericht zurückgibt, weil Tiefenwirkung, Blick- und Handsteuerung, Komfort und Leistung im Simulator nicht beurteilbar sind.
- `build-brief/REFERENCE.md`, `build-brief/prompt-template.md`: Fragen und Nachhak-Muster je Baustein, Laufgrößen mit Kostenspanne, Formulierungsregeln nach dem Prompting-Guide für Claude Fable 5.2 (gelesen am 12.11.2026), Abnahmeliste und das Gerüst des Prompts.

- `docs/evals/build-brief/`: zwei durchgespielte Beispiele mit Antwortblatt und erzeugtem Prompt, eines für ein Web-Feature in einem Next.js-Projekt und eines für eine Funktion einer visionOS-App. Die Befunde der beiden Durchläufe sind in den Skill eingearbeitet.

### Fixed
- `block-destructive-commands`: Das Muster für Shutdown und Reboot blockte auch `xcrun simctl shutdown <gerät>` und jeden Befehl, in dem ein Wort auf „halt" endet (zum Beispiel eine Commit-Nachricht mit „Inhalt"). `shutdown`, `reboot`, `halt` und `poweroff` zählen jetzt nur noch als Befehlswort. Ein nacktes `reboot` oder `poweroff` ohne Argument, das bisher durchlief, wird damit geblockt.

### Changed
- `CLAUDE.md`: „File Paths Convention" nennt `docs/briefs/` für Build-Briefs.

## 3.2.0 — 2026-11-12

### Added
- `prompt-audit`: neuer Skill, der das Claude-Code-Setup (CLAUDE.md-Kette, Memory, Skills, Agents, Hooks, Output-Styles, geplante Aufgaben) gegen die Prompting-Doku von Anthropic für das laufende Modell prüft. Die Doku wird bei jedem Lauf frisch über `platform.claude.com/llms.txt` geholt; ohne Doku gibt es keinen Audit. Ergebnis ist eine Tabelle mit Fundstelle und Umformulierung, geändert wird erst nach Freigabe, Dateien ohne Versionierung werden vorher gesichert.
- `prompt-audit/scripts/inventory.py`: listet alle Anweisungsquellen eines Projekts mit Größe, Geltung und Versionierung, einschließlich Elternordnern und `@`-Importen. Einstellungen werden nur schlüsselweise gelesen.
- `prompt-audit/scripts/usage_evidence.py`: zählt Subagent-Starts, Skill-Aufrufe, Hook-Fehler und abgelehnte Tool-Aufrufe nach dem Zeitstempel der Einträge.

### Fixed
- `CLAUDE.md`, `AGENTS.md`: Die Landing-Sequenz committet den Beads-Export vor dem Push; bisher wurde er exportiert, aber nicht übertragen.

### Changed
- `CLAUDE.md`: Zu den Release-Regeln gehört der Changelog-Eintrag.
- `.gitignore`: `__pycache__/`.

## 3.1.2 — 2026-11-12

Prompt-Audit gegen den Prompting-Guide für Claude Fable 5.2: absolute Regeln bekommen Geltungsbereich und Ausnahme, stehende Anweisungen zum Delegieren hängen jetzt am Umfang der Aufgabe.

### Fixed
- `block-destructive-commands`: Mehrzeilige Befehle liefen unter `/bin/sh` auf macOS ungeprüft durch, weil `echo` das `\n` im Hook-JSON zu einem echten Zeilenumbruch machte und `jq` daran scheiterte. Das Skript reicht Eingaben jetzt mit `printf` weiter.
- `block-destructive-commands`: Das Muster `format\s+` blockte auch `--format "…"` und `clang-format datei`. `format` zählt nur noch als Befehlswort.
- `db-inspect`: „Kein Schreiben ohne `WHERE`" traf auch `INSERT`. Die Regel gilt jetzt für `UPDATE` und `DELETE`.
- Implementierungs-Agents (component, feature, infrastructure): Ohne Beads-ID brachen sie ab, obwohl die Beschreibung direkte Aufträge zusagt. Sie arbeiten jetzt nach dem Auftrag des Callers, wenn er Ziel und Akzeptanzkriterien nennt.
- `CLAUDE.md`, `AGENTS.md`: Der Push am Session-Ende geschieht nach Rückfrage, passend zu `land-the-plane`. `AGENTS.md` nennt jetzt auch `bd dolt push`.

### Changed
- `block-destructive-commands`: Rekursives `rm` im Projekt, im Scratchpad der Session und in Temp-Ordnern läuft durch. Außerhalb davon, oder wenn die Ziele nicht auflösbar sind, bestätigt der User (`permissionDecision: "ask"`). In den Modi `bypassPermissions` und `dontAsk` bleibt es beim Block. Protokolliert werden nur noch Blockaden und Rückfragen, unter `~/.claude/logs/` statt in `/tmp`.
- `review`: Kleine Diffs (bis etwa 3 Dateien oder 150 Zeilen) prüft die Hauptsession selbst. Bei größeren starten nur die Agents, deren Gebiet der Diff berührt. Die Rückfrage zu `/reflect` am Ende ist ein Hinweissatz.
- `interview`: Der Research-Agent startet nur, wenn eine Entscheidung von der aktuellen API abhängt. Die Council-Frage kommt nur bei größeren Features.
- `redesign-studio`: Die Bestands-Analyse läuft mit Sonnet, und die Hauptsession prüft fünf Fakten daraus gegen die Quelle, bevor `bestand.md` verbindlich wird.
- `roast`, `storm-research`: Personas, Lenses und Verifier laufen mit `model="sonnet"` statt mit dem Modell der Session.
- `setup`: Die Vorlage für neue Projekt-CLAUDE.md verlangt keine Task-Liste ab drei Schritten und keine Rückfragen am Aufgabenende mehr.
- `diagnose`, `grill-me`, `docs-lookup`: harte Grenzen (30 Sekunden, „niemals batchen", „Max 3 Calls") mit Grund und Ausnahme formuliert.
- `reflect`: Absolute Aussagen des Users werden mit Geltungsbereich und Grund gespeichert; Vorsichtsregeln ohne gültigen Grund werden gelöscht.
- Agents: Die Beschreibungen von `devops-agent`, `functional-testing-agent`, `quality-agent` und `infrastructure-implementation-agent` nennen, wann sich das Delegieren lohnt, statt „PROACTIVELY". `tdd-validation-agent` und `functional-testing-agent` laufen mit Sonnet. Der `task-orchestrator` fasst bei kleinen Tasks Gate 1 und 2 zusammen.
- `CLAUDE.md`: Abschnitte gestrichen, die sich aus dem Repo ablesen lassen (Plugin-Struktur, Formate, Hook-System, Workflows). Neu ist der Abschnitt „Release". „Domain Language" steht jetzt in der `README.md`.

## 3.1.1 — 2026-10-06

### Fixed
- `land-the-plane`, `setup`, `CLAUDE.md`, `AGENTS.md`: `bd export` schreibt in bd 1.3.1 nach stdout; die Datei entsteht nur mit `bd export -o .beads/issues.jsonl`.
- `land-the-plane`: nach dem Git-Push `bd dolt push`, wenn ein Dolt-Remote konfiguriert ist.

### Changed
- Beads-Datenbank dieses Repos erstmals zum Dolt-Remote gepusht (`refs/dolt/data`); „Landing the Plane" in `CLAUDE.md` um `bd dolt push` ergänzt.

## 3.1.0 — 2026-10-06

Skill-Audit gegen Claude Code 2.1.291 und bd 1.3.1.

### Fixed
- `usage-report`, `redesign-studio`: `$CLAUDE_SKILL_PATH` (existiert nicht) → `${CLAUDE_SKILL_DIR}`; Extraktions-Skript und `scrollfx.js` werden wieder gefunden.
- `interview`, `review`: Plugin-Agents mit Präfix aufgerufen (`stemago-tools:research-agent`, `stemago-tools:quality-agent`, `stemago-tools:task-orchestrator`).
- `review`: Diff läuft von der Merge-Base bis zum Working Tree, uncommittete und ungetrackte Dateien werden mitgeprüft; Default-Branch wird ermittelt statt `origin/main` fest zu verdrahten.
- `setup`: Playwright-Paket korrigiert (`@anthropic/mcp-server-playwright` gab es nie → `@executeautomation/playwright-mcp-server`, passend zu den Tools des `functional-testing-agent`); GitHub-MCP auf den offiziellen Remote-Server umgestellt (`@modelcontextprotocol/server-github` ist deprecated); MCP-Detection erkennt Plugin-MCPs (`plugin:context7:context7`); Beads-`--force` nutzt `bd init --reinit-local` mit Backup und Rückfrage.
- `docs-lookup`: Context7 auch unter dem Plugin-Präfix `mcp__plugin_context7_context7__*`.
- `land-the-plane`: `/recap`-Bash-Block entfernt (eingebautes CLI-Kommando, vom Modell nicht ausführbar).
- `to-beads`: ungültiger Issue-Typ `research` → `spike` (laut `bd types`).
- Beads-Datenbank dieses Repos auf Schema v66 migriert (`bd migrate --force`, bd 1.3.1); Schreibzugriffe waren seit dem bd-Update gesperrt.
- `hooks.json`: `${CLAUDE_PLUGIN_ROOT}` in Anführungszeichen (Pfade mit Leerzeichen); `claude plugin validate` läuft ohne Warnungen.

### Changed
- `reflect`, `reflect-config`: Learnings gehen ins eingebaute Memory von Claude Code statt nach `.claude/learnings/project-learnings.md` (die Datei wurde nie in Sessions geladen). `/reflect` bietet die einmalige Migration des Alt-Bestands an; kein `learn:`-Commit mehr.
- `land-the-plane`: neuer Schritt „Commit & Push" mit Rückfrage (committen und pushen / nur committen / nichts). Der SessionStart-Hook nennt den Handoff der letzten Session, falls vorhanden.
- `interview`: Council-Stress-Test läuft per Rückfrage statt als Pflicht; Widerspruch bei der Fragenzahl pro Runde aufgelöst.
- `review`: Security-Agent auf `sonnet`; die quality-agents holen Diff und Dateien selbst, statt sie im Prompt zu bekommen.
- `usage-report`: Gap-Analyse findet Skills und Agents auch in `.claude/`, `~/.claude/` und installierten Plugins, nicht nur unter `plugins/`.
- `diagnose`: offene Orientierungsfragen als Text statt über AskUserQuestion.
- `setup`: ungenutzten `beads`-Block in `.claude/settings.local.json` entfernt.
- `caveman`, `zoom-out`: Beschreibungen gekürzt (beide sind nur manuell aufrufbar); überflüssiges `$ARGUMENTS` am Dateiende in sechs Skills entfernt.
- `beads-ready`, `land-the-plane`: `bd ready` bzw. der Git-Status werden per Kontext-Injektion beim Laden eingebettet; `allowed-tools` erspart die Permission-Prompts für die lesenden `bd`- und `git`-Befehle. `usage-report`: `allowed-tools` für das Extraktions-Skript.
- `browser-test`, `db-inspect`: auf Ablauf und Regeln gestrafft statt Tool-Schemas zu wiederholen; `browser-test` nennt die inzwischen verpflichtende `pageId`. `docs-lookup`: feste Library-IDs und versionsgebundene Beispiele entfernt.
- `task-orchestrator`: Beschreibung von ca. 730 auf ca. 150 Tokens gekürzt (wird in jeder Session geladen).
- `.claude/learnings/project-learnings.md` aus diesem Repo entfernt (Inhalt liegt vollständig im Memory); `.beads.gate.lock` in `.gitignore`.
- Eval-Daten `skills/usage-report-workspace/` → `docs/evals/usage-report/` (werden nicht mehr mit dem Plugin ausgeliefert).
- `github-ops`: auf `gh` CLI umgeschrieben; die dokumentierten Tool-Namen stammten aus dem abgekündigten GitHub-MCP-Paket.
- `storm-research`: „Regeln & Guardrails" vor die Phasen gezogen, damit sie die 5.000-Token-Grenze nach einem Auto-Compact überleben.

## 3.0.1 — 2026-09-03

### Fixed
- Agents: Context7 zusätzlich unter dem Plugin-Präfix `mcp__plugin_context7_context7__*` gewährt (research-, component-, infrastructure-implementation-agent); `LS` (kein Tool mehr) → `Glob` in acht Agents.
- `redesign-studio/scrollfx.js`: Guard gegen 0-Breite im Tilt, keine leeren Wort-Spans.
- `land-the-plane`, `CLAUDE.md`, `AGENTS.md`: `bd sync` (in bd 1.x entfernt) → `bd export`.
- Beads in diesem Repo auf bd 1.x re-initialisiert (Dolt-Backend, Prefix `bd`, `export.auto = true`); die SQLite-Datenbank aus bd 0.49 war leer und wurde entfernt.

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
