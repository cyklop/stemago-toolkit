---
name: setup
description: "Projekt-Initialisierung: CLAUDE.md, Beads-Tracker oder MCP-Server einrichten. Verwende NUR bei expliziter Erst-Einrichtung oder Re-Initialisierung ('Beads neu installieren', 'CLAUDE.md neu erstellen', 'MCPs prüfen'). Triggert NICHT bei normaler Entwicklungsarbeit. Args: --project / --beads / --mcp / --all."
argument-hint: "[--project|--beads|--mcp|--all] [--force]"
---

# /setup - Projekt-Initialisierung

Konsolidierter Setup-Skill für Erst-Einrichtung eines Projekts. Ersetzt die früheren Einzel-Skills `init-project`, `beads-setup`, `mcp-setup` (entfernt in v2.0.0).

## Argumente

- `--project` — CLAUDE.md mit Workflow-Regeln erstellen oder ergänzen
- `--beads` — Beads Memory-System initialisieren (bd CLI + beads-mcp + bd init)
- `--mcp` — MCP Server prüfen und fehlende installieren
- `--all` — alle drei Subjobs nacheinander
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
- Kein Argument → interaktive Detection (siehe unten)

### Interaktive Detection (kein Argument)

Prüfe Projekt-Zustand und zeige Tabelle:

```bash
[ -f CLAUDE.md ] && echo "✓ CLAUDE.md vorhanden" || echo "✗ CLAUDE.md fehlt"
[ -d .beads ] && echo "✓ Beads initialisiert" || echo "✗ Beads fehlt"
claude mcp list 2>/dev/null | grep -E "^(context7|beads|chrome-devtools|sequential-thinking)" || echo "✗ Core MCPs fehlen"
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

### Strukturierte Aufgaben-Abarbeitung
- Bei Aufgaben mit 3+ Schritten: IMMER zuerst eine Task-Liste mit TaskCreate erstellen
- Jeden Task auf `in_progress` setzen bevor du anfängst, auf `completed` wenn fertig
- NIEMALS eine Aufgabe als erledigt melden bevor ALLE Tasks completed sind
- Bei Unterbrechung/Compact: TaskList prüfen und offene Tasks weiterarbeiten

### Code Review am Aufgabenende
- Nach Abschluss einer Implementierung die 3+ Dateien betrifft:
  1. `git diff` der Änderungen anzeigen
  2. Frage: "Soll ich einen Code Review der Änderungen durchführen?"
  3. Bei Ja: Review auf Code-Qualität, Security, Performance, Konsistenz
  4. Review-Ergebnis als Zusammenfassung mit konkreten Verbesserungsvorschlägen

### Dokumentations-Pflege
- Nach Abschluss eines Features das neue Funktionalität, Skills, Agents oder Konfiguration hinzufügt:
  1. Prüfe ob `CLAUDE.md` aktualisiert werden muss (neue Regeln, Patterns, Konventionen)
  2. Prüfe ob `README.md` aktualisiert werden muss (neue Features, geänderte Struktur, Installationsschritte)
  3. Frage: "Sollen CLAUDE.md/README.md an die neuen Änderungen angepasst werden?"
  4. Bei Ja: Nur die relevanten Abschnitte aktualisieren, bestehenden Inhalt beibehalten
```

Bestätigungs-Output:

```
CLAUDE.md erstellt mit Workflow-Regeln (Tasks, Code Review, Doku-Pflege).
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

Falls `.beads/` existiert und kein `--force`: Meldung "Beads bereits initialisiert. Mit `--force` neu initialisieren (löscht bestehende Tasks!)." und stoppe.

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
bd init           # Normal
bd init --stealth # Stealth
```

### B.7 MCP Server konfigurieren

```bash
claude mcp list 2>/dev/null | grep -i beads
```

Falls nicht konfiguriert:

```bash
claude mcp add beads -- beads-mcp
```

### B.8 Einstellungen speichern

Speichere in `.claude/settings.local.json`:

```json
{
  "beads": {
    "mode": "normal|stealth",
    "initialized": true,
    "initializedAt": "ISO-timestamp"
  }
}
```

Bestehende Datei mergen, nicht überschreiben.

### B.9 Abschluss-Tabelle

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
| `sequential-thinking` | ✓/✗ | Reasoning |
| `chrome-devtools` | ✓/✗ | Browser-Test |
| `beads` | ✓/✗ | Memory & Tasks |

**OPTIONAL:**

| MCP | Status | Benötigt von |
|-----|--------|-------------|
| `github` | ✓/✗ | github-ops |
| `mariadb` | ✓/✗ | db-inspect |
| `playwright` | ✓/✗ | functional-testing-agent |

### C.3 Idempotenz-Check

Falls alle Core MCPs ✓ und kein `--force`: Meldung "Alle Core MCPs konfiguriert." und stoppe.

### C.4 Fehlende installieren

AskUserQuestion: welche der fehlenden MCPs sollen installiert werden (Multi-Select).

**Core (keine Credentials):**

```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

**Beads:** wenn gewählt aber bd/beads-mcp fehlen → in Subjob B umleiten oder dessen Steps B.3/B.4 hier einbinden, dann `claude mcp add beads -- beads-mcp`.

**Optional ohne Credentials:**

```bash
claude mcp add playwright -- npx -y @anthropic/mcp-server-playwright@latest
```

**Mit Credentials:**

```bash
# GitHub - frage nach GITHUB_PERSONAL_ACCESS_TOKEN
claude mcp add -e GITHUB_PERSONAL_ACCESS_TOKEN=<token> github -- npx -y @modelcontextprotocol/server-github

# MariaDB - frage nach DB_HOST/DB_PORT/DB_USER/DB_PASSWORD
claude mcp add -e DB_HOST=<host> -e DB_PORT=<port> -e DB_USER=<user> -e DB_PASSWORD=<pw> mariadb -- npx -y @benborla29/mcp-server-mysql
```

### C.5 Verifikation

```bash
claude mcp list
```

Hinweis: **Claude Code neu starten**, damit neue MCPs aktiv werden.

---

## Wichtig

- Bereits installierte/konfigurierte Komponenten nicht erneut behandeln (außer `--force`).
- Bei Credentials immer User fragen, niemals Dummy-Werte.
- Installationsfehler klar kommunizieren.

$ARGUMENTS
