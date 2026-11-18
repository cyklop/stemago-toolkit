---
name: setup
description: "Projekt-Initialisierung: CLAUDE.md, Beads-Tracker, MCP-Server, Prüf-Hooks (Linter nach dem Bearbeiten, Tests vor dem Rundenende) und Sicherheitsregeln (Deny-Regeln, Sandbox, Auto-Mode-Umgebung) einrichten. Verwende bei Erst-Einrichtung oder Re-Initialisierung ('Beads neu installieren', 'CLAUDE.md neu erstellen', 'MCPs prüfen') und wenn der User Prüf-Hooks oder Sicherheitsregeln fürs Projekt will ('Hooks einrichten', 'Tests automatisch laufen lassen', 'deny-Regeln', 'Sandbox einschalten'). Triggert NICHT bei normaler Entwicklungsarbeit. Args: --project / --beads / --mcp / --hooks / --safety / --all."
argument-hint: "[--project|--beads|--mcp|--hooks|--safety|--all] [--force]"
---

# /setup - Projekt-Initialisierung

Konsolidierter Setup-Skill für die Erst-Einrichtung eines Projekts.

## Argumente

- `--project` — CLAUDE.md mit Workflow-Regeln erstellen oder ergänzen
- `--beads` — Beads Memory-System initialisieren (bd CLI + beads-mcp + bd init)
- `--mcp` — MCP Server prüfen und fehlende installieren
- `--hooks` — Prüf-Hooks einrichten: Linter/Typecheck nach Edit/Write, Tests vor dem Rundenende
- `--safety` — Sicherheitsgrundlage im Projekt: Deny-Regeln, Sandbox, Auto-Mode-Umgebung
- `--all` — alle Subjobs nacheinander
- `--force` — bei bestehendem Zustand trotzdem (re-)initialisieren
- *(kein Argument)* — interaktive Detection: zeige aktuellen Zustand und biete fehlende Subjobs an

## Idempotenz-Regel

**Standardverhalten:** Bei bestehender Konfiguration meldet jeder Subjob "bereits eingerichtet" mit Detail-Status und stoppt. Nur mit `--force` wird re-initialisiert.

## Workflow

### Argument-Routing

Werte `$ARGUMENTS` aus:
- Enthält `--project` oder `--all` → Subjob A
- Enthält `--beads` oder `--all` → Subjob B
- Enthält `--mcp` oder `--all` → Subjob C
- Enthält `--hooks` oder `--all` → Subjob D
- Enthält `--safety` oder `--all` → Subjob E
- Kein Argument → interaktive Detection (siehe unten)

### Interaktive Detection (kein Argument)

Prüfe Projekt-Zustand und zeige Tabelle:

```bash
[ -f CLAUDE.md ] && echo "✓ CLAUDE.md vorhanden" || echo "✗ CLAUDE.md fehlt"
[ -d .beads ] && echo "✓ Beads initialisiert" || echo "✗ Beads fehlt"
claude mcp list 2>/dev/null | grep -E "^(plugin:[^:]+:)?(context7|beads|chrome-devtools):" || echo "✗ Core MCPs fehlen"
jq -e '.hooks.PostToolUse or .hooks.Stop' .claude/settings.json >/dev/null 2>&1 && echo "✓ Prüf-Hooks vorhanden" || echo "✗ Prüf-Hooks fehlen"
jq -e '.permissions.deny' .claude/settings.json >/dev/null 2>&1 && echo "✓ Deny-Regeln vorhanden" || echo "✗ Deny-Regeln fehlen"
```

Frage via AskUserQuestion welche fehlenden Subjobs ausgeführt werden sollen.

---

## Subjob A: --project (CLAUDE.md)

### A.1 Bestehende CLAUDE.md prüfen

```
Read CLAUDE.md
```

### A.2 Falls CLAUDE.md existiert (und kein --force)

Meldung: "CLAUDE.md bereits vorhanden. Mit `--force` neu erstellen, oder `--project --append` zum Ergänzen."

Falls `--append` mitgegeben: Workflow-Regeln-Block am Ende anhängen, bestehenden Inhalt erhalten.

### A.3 Falls CLAUDE.md fehlt (oder --force)

Erstelle `CLAUDE.md` mit folgendem Workflow-Regeln-Block:

```markdown
## Workflow-Regeln

### Fortschritt festhalten
- Bei längeren Aufgaben, die einen Compact oder eine Unterbrechung überstehen müssen, den Fortschritt in Tasks (TaskCreate) oder Beads festhalten und nach einer Unterbrechung dort weitermachen
- Kurze Aufgaben brauchen keine Task-Liste

### Abschluss einer Implementierung
- Tests und Lint des Projekts ausführen und das Ergebnis im Abschlussbericht nennen
- Betrifft die Änderung mehrere Dateien, im Abschlussbericht ein Review vorschlagen (`/stemago-tools:review`) — als Hinweis, nicht als Rückfrage

### Dokumentations-Pflege
- Ändert ein Feature Regeln, Befehle, Struktur oder Installationsschritte, `CLAUDE.md` und `README.md` im selben Zug anpassen: nur die betroffenen Abschnitte, bestehenden Inhalt beibehalten
- Die angepassten Stellen im Abschlussbericht nennen
```

Bestätigungs-Output:

```
CLAUDE.md erstellt mit Workflow-Regeln (Fortschritt, Abschluss, Doku-Pflege).
```

---

## Subjob B: --beads (Beads-System)

### B.1 Git-Repo prüfen

```bash
git rev-parse --git-dir 2>/dev/null
```

Falls nicht: stoppe mit "Beads benötigt ein Git-Repository. Bitte erst `git init` ausführen."

### B.2 Bestehende Beads-Installation prüfen (Idempotenz)

```bash
ls -la .beads/ 2>/dev/null
```

Falls `.beads/` existiert und kein `--force`: Meldung "Beads bereits initialisiert. Mit `--force` neu initialisieren (überschreibt die lokalen Beads-Daten!)." und stoppe.

Mit `--force`: vorher `bd export --all -o <backup>.jsonl` als Backup ausführen und die Re-Initialisierung via AskUserQuestion bestätigen lassen. In B.6 dann `bd init --reinit-local` verwenden (`bd init --force` ist seit bd 1.x nur noch ein deprecated Alias dafür). Hat die Datenbank ein Remote, stoppen und auf `bd help init-safety` verweisen — Remote-Historie nie automatisch verwerfen.

### B.3 bd CLI prüfen und installieren

```bash
which bd || command -v bd
```

Falls fehlt, AskUserQuestion:
- **npm (Recommended)**: `npm install -g @beads/bd`
- **Homebrew**: `brew install beads`
- **Go**: `go install github.com/steveyegge/beads/cmd/bd@latest`
- **Überspringen**: manuell installieren

Verifikation: `bd --version`

### B.4 beads-mcp prüfen und installieren

```bash
which beads-mcp || command -v beads-mcp
```

Falls fehlt, AskUserQuestion:
- **uv (Recommended)**: `uv tool install beads-mcp`
- **pip**: `pip install beads-mcp`
- **pipx**: `pipx install beads-mcp`
- **Überspringen**: manuell installieren

### B.5 Modus wählen

AskUserQuestion:
- **Normal (Recommended)**: `.beads/` wird ins Repo committed (Team-Sichtbarkeit)
- **Stealth Mode**: `.beads/` bleibt lokal (`.gitignore`, keine Commits)

### B.6 Beads initialisieren

```bash
bd init                # Normal
bd init --stealth      # Stealth
bd init --reinit-local # nur bei --force über bestehende lokale Daten (siehe B.2)
```

### B.7 MCP Server konfigurieren

```bash
claude mcp list 2>/dev/null | grep -i beads
```

Falls nicht konfiguriert:

```bash
claude mcp add beads -- beads-mcp
```

### B.8 Abschluss-Tabelle

```
| Komponente | Status |
|------------|--------|
| bd CLI     | ✓ vX.X.X |
| beads-mcp  | ✓ |
| MCP Server | ✓ |
| Beads DB   | ✓ |
```

Hinweis: **Claude Code neu starten**, damit MCP aktiv wird.

---

## Subjob C: --mcp (MCP-Server)

### C.1 Status ermitteln

```bash
claude mcp list
```

### C.2 Status-Report (zwei Kategorien)

**CORE MCPs:**

| MCP | Status | Zweck |
|-----|--------|-------|
| `context7` | ✓/✗ | Docs-Lookup |
| `chrome-devtools` | ✓/✗ | Browser-Test |
| `beads` | ✓/✗ | Memory & Tasks |

**OPTIONAL:**

| MCP | Status | Benötigt von |
|-----|--------|-------------|
| `github` | ✓/✗ | github-ops (optional — `gh` CLI reicht) |
| `mariadb` | ✓/✗ | db-inspect |
| `playwright` | ✓/✗ | functional-testing-agent |
| `sequential-thinking` | ✓/✗ | — (aktuelle Modelle planen ohne externes Thinking-Tool; nur auf ausdrücklichen Wunsch) |

Ein MCP zählt auch dann als ✓, wenn er von einem Plugin bereitgestellt wird (in `claude mcp list` als `plugin:<plugin>:<name>`, z.B. `plugin:context7:context7`) — nicht doppelt installieren.

### C.3 Idempotenz-Check

Falls alle Core MCPs ✓ und kein `--force`: Meldung "Alle Core MCPs konfiguriert." und stoppe.

### C.4 Fehlende installieren

AskUserQuestion: welche der fehlenden MCPs sollen installiert werden (Multi-Select).

**Core (keine Credentials):**

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

**Beads:** wenn gewählt aber bd/beads-mcp fehlen → in Subjob B umleiten oder dessen Steps B.3/B.4 hier einbinden, dann `claude mcp add beads -- beads-mcp`.

**Optional ohne Credentials:**

```bash
claude mcp add playwright -- npx -y @executeautomation/playwright-mcp-server  # liefert die mcp__playwright__playwright_*-Tools des functional-testing-agent
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking  # nur auf Wunsch
```

**Mit Credentials:**

```bash
# GitHub (offizieller Remote-Server) - frage nach einem GitHub PAT mit repo-Scope
claude mcp add-json github '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer <token>"}}'

# MariaDB - frage nach DB_HOST/DB_PORT/DB_USER/DB_PASSWORD
claude mcp add -e DB_HOST=<host> -e DB_PORT=<port> -e DB_USER=<user> -e DB_PASSWORD=<pw> mariadb -- npx -y @benborla29/mcp-server-mysql
```

### C.5 Verifikation

```bash
claude mcp list
```

Hinweis: **Claude Code neu starten**, damit neue MCPs aktiv werden.

---

## Subjob D: --hooks (Prüf-Hooks)

Hooks sind die Prüfpunkte, die Claude während der Arbeit zurückmelden, ob der Code noch stimmt, statt sich auf eine Endkontrolle zu verlassen. Sie gehören ins Projekt, nicht ins Plugin, weil Linter- und Testbefehle je Projekt anders sind. Die Vorlagen liegen in `${CLAUDE_PLUGIN_ROOT}/skills/setup/templates/`.

Ein Hook, der Claude zurückschicken soll, muss mit **Exit 2** enden. Exit 1 gilt als nicht blockierender Fehler, und Claude macht weiter, als wäre nichts.

### D.1 Befehle ermitteln

Lies die Befehle aus dem Projekt, statt sie anzunehmen: `package.json` (`scripts.lint`, `scripts.typecheck`, `scripts.test`), `Makefile`, `pyproject.toml`, `Cargo.toml`, CI-Workflows unter `.github/workflows/`. Gesucht sind:

- **Prüfung je Datei** (schnell, unter ein paar Sekunden): z. B. `npx eslint {file}`, `ruff check {file}`, `npx prettier --check {file}`. Ein Typecheck über das ganze Projekt gehört nur hierher, wenn er schnell ist.
- **Testbefehl** fürs Rundenende: z. B. `npm test --silent`, `pytest -q`. Ist die ganze Suite langsam (über eine Minute), nimm die schnelle Teilmenge (Unit-Tests) und sag dem User, dass die volle Suite in CI bleibt.
- **Dateimuster**, auf das beide Hooks reagieren, z. B. `\.(ts|tsx)$`.

Lässt sich ein Befehl nicht eindeutig ableiten, frag den User mit den gefundenen Kandidaten. Gibt es weder Linter noch Tests, sag das und richte nichts ein.

### D.2 Bestehende Hooks prüfen (Idempotenz)

```bash
jq '.hooks' .claude/settings.json 2>/dev/null
```

Gibt es schon einen Hook auf `PostToolUse` mit `Edit|Write` oder auf `Stop`, zeig ihn und frag: behalten, ersetzen oder ergänzen. Ohne `--force` nichts überschreiben.

### D.3 Skripte kopieren und testen

```bash
mkdir -p .claude/hooks
cp "${CLAUDE_PLUGIN_ROOT}/skills/setup/templates/check-after-edit.sh" .claude/hooks/
cp "${CLAUDE_PLUGIN_ROOT}/skills/setup/templates/verify-on-stop.sh" .claude/hooks/
```

Teste beide vor dem Eintragen mit einer echten Datei aus dem Projekt:

```bash
echo '{"tool_input":{"file_path":"<echte datei>"}}' | bash .claude/hooks/check-after-edit.sh '<prüfbefehl>' '<muster>'; echo "exit $?"
echo '{}' | bash .claude/hooks/verify-on-stop.sh '<testbefehl>' '<muster>'; echo "exit $?"
```

Erwartet ist Exit 0 bei sauberem Stand. Exit 2 bei sauberem Stand heißt: Befehl falsch oder Projekt schon rot. Das klärst du mit dem User, bevor du den Hook einträgst, sonst blockiert er jede Runde.

### D.4 In `.claude/settings.json` eintragen

Mit bestehenden Einträgen zusammenführen, nicht ersetzen:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/check-after-edit.sh '<prüfbefehl>' '<muster>'", "timeout": 60 }]
    }],
    "Stop": [{
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/verify-on-stop.sh '<testbefehl>' '<muster>'", "timeout": 300 }]
    }]
  }
}
```

Danach `jq -e '.hooks' .claude/settings.json` zur Syntaxprüfung. Der Stop-Hook läuft nur, wenn Code-Dateien geändert sind, und blockt nach einem Rücksprung nicht erneut (`stop_hook_active`), damit keine Schleife entsteht.

### D.5 Abschluss

Dem User sagen: welche Befehle wann laufen, dass `.claude/settings.json` und `.claude/hooks/` committet werden sollen (dann gelten sie auch in Cloud-Sessions und für andere), und dass `/hooks` die Hooks anzeigt. Wurden die Hooks in dieser Session angelegt, greifen sie eventuell erst nach `/hooks` oder einem Neustart.

---

## Subjob E: --safety (Sicherheitsgrundlage)

Feste Regeln nur für das, was sich nicht zurücknehmen lässt, wenn Claude sich einmal irrt. Deny-Regeln greifen vor dem Auto-Mode-Klassifikator. Alles andere entscheidet der Auto-Mode.

### E.1 Bestand prüfen

```bash
jq '{permissions, sandbox, autoMode}' .claude/settings.json 2>/dev/null
jq '{deny: .permissions.deny, autoMode}' ~/.claude/settings.json
```

Was global schon gesperrt ist, nicht noch einmal ins Projekt schreiben.

### E.2 Deny-Regeln vorschlagen

Aus dem Projekt ableiten und dem User als Liste zeigen, bevor du schreibst:

- **Secrets lesen:** `Read(./.env)`, `Read(./.env.*)` außer Beispieldateien, Schlüssel- und Zertifikatsdateien (`Read(./**/*.pem)`), Cloud-Credentials, die im Projekt liegen.
- **Unumkehrbares:** Produktions-Deploys (`Bash(vercel --prod:*)`, `Bash(fly deploy:*)`), Migrationen gegen Produktion, `Bash(terraform apply:*)`, Löschbefehle für Buckets oder Datenbanken, soweit das Projekt solche Werkzeuge nutzt.
- **Rückfrage statt Sperre (`ask`)** für Aktionen, die gewollt sein können, aber nach außen wirken: Veröffentlichen, Mails oder Nachrichten senden, Releases taggen.

Ein Deny auf `Read` hält nur das Read-Tool ab, nicht `cat .env` in Bash. Das deckt erst die Sandbox ab (E.3).

### E.3 Sandbox anbieten

Die Sandbox begrenzt, was Bash-Befehle und alles, was sie starten (z. B. Abhängigkeiten in `npm test`), auf Dateisystem und Netz anrichten können. Vorschlag für `.claude/settings.json`:

```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "network": { "allowedDomains": ["registry.npmjs.org", "github.com", "<weitere aus dem Projekt>"] }
  }
}
```

Die erlaubten Domains aus Paketmanager, API-Clients und CI ableiten. Frag den User, bevor du sie einschaltest: Befehle, die außerhalb des Projekts schreiben oder ungelistete Hosts brauchen, fragen dann nach oder schlagen fehl. Schlägt etwas fehl, lieber die Domain ergänzen als die Sandbox abzuschalten.

### E.4 Auto-Mode-Umgebung

Vertraute Ziele, die der Auto-Mode sonst blockiert oder nachfragt, in normalem Englisch unter `autoMode.environment` eintragen, beginnend mit `"$defaults"`:

```json
{
  "autoMode": {
    "environment": [
      "$defaults",
      "Trusted deploy target: the staging app <name> on <host>; deploying there is routine.",
      "Trusted bucket: s3://<bucket> holds build artifacts for this project."
    ]
  }
}
```

Nur eintragen, was der User bestätigt. Produktion gehört nicht als „vertraut" hierher, sondern als `ask` oder `deny` (E.2).

### E.5 Schreiben und prüfen

Mit bestehenden Einträgen zusammenführen, `jq -e . .claude/settings.json` ausführen und eine der Deny-Regeln mit einem harmlosen Aufruf prüfen (z. B. Read auf eine nicht vorhandene gesperrte Datei: die Meldung muss die Sperre nennen). Dem User sagen, dass `.claude/settings.json` committet werden sollte, damit die Regeln auch in Cloud-Sessions gelten.

---

## Wichtig

- Bereits installierte/konfigurierte Komponenten nicht erneut behandeln (außer `--force`).
- Bei Credentials immer User fragen, niemals Dummy-Werte.
- Installationsfehler klar kommunizieren.
