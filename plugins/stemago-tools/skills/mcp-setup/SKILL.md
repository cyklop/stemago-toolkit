---
name: mcp-setup
description: "MCP Server prüfen und fehlende installieren"
---

# MCP Server Setup

Prüfe welche empfohlenen MCP Server konfiguriert sind und installiere fehlende interaktiv.

## Workflow

### Schritt 1: Status ermitteln

Führe `claude mcp list` aus und parse den Output. Jede Zeile enthält den MCP-Namen vor dem Doppelpunkt und den Status (✓ oder ✗).

```bash
claude mcp list
```

### Schritt 2: Status-Report anzeigen

Zeige dem User eine Übersicht in zwei Kategorien:

**CORE MCPs (empfohlen für alle Projekte):**

| MCP | Status | Zweck |
|-----|--------|-------|
| `context7` | ✓/✗ | Docs-Lookup, Research-Agent |
| `sequential-thinking` | ✓/✗ | Komplexe Reasoning-Aufgaben |
| `chrome-devtools` | ✓/✗ | Browser-Test, UI-Inspektion |
| `beads` | ✓/✗ | Agent-Memory, Task-Tracking |

**OPTIONALE MCPs (für bestimmte Skills/Agents):**

| MCP | Status | Benötigt von |
|-----|--------|-------------|
| `github` | ✓/✗ | `/stemago-tools:github-ops` (braucht GITHUB_TOKEN) |
| `mariadb` | ✓/✗ | `/stemago-tools:db-inspect` (braucht DB-Credentials) |
| `playwright` | ✓/✗ | functional-testing-agent |

Ersetze ✓/✗ mit dem tatsächlichen Status aus dem `claude mcp list` Output.

### Schritt 3: Fehlende MCPs installieren

Falls MCPs fehlen (✗), frage den User mit AskUserQuestion welche installiert werden sollen. Biete Core und optionale MCPs getrennt an.

**Core MCPs (keine Credentials nötig) - direkt installieren:**

```bash
# Context7 - Docs Lookup
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest

# Sequential Thinking - Reasoning
claude mcp add sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking

# Chrome DevTools - Browser Testing
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest

# Beads - Agent Memory & Task Tracking
# WICHTIG: Beads hat Voraussetzungen - siehe Schritt 3.1
claude mcp add beads -- beads-mcp
```

**Schritt 3.1: Beads-Voraussetzungen prüfen (falls Beads gewählt)**

Beads benötigt zwei Komponenten die NICHT über `claude mcp add` installiert werden:

```bash
# 1. Prüfe bd CLI
which bd || command -v bd
```

Falls bd fehlt, frage mit AskUserQuestion:

```
bd CLI (Beads) nicht gefunden. Installieren?

- **npm (Recommended)**: npm install -g @beads/bd
- **Homebrew**: brew install beads
- **Go**: go install github.com/steveyegge/beads/cmd/bd@latest
- **Überspringen**: Später manuell installieren
```

Je nach Wahl ausführen.

```bash
# 2. Prüfe beads-mcp
which beads-mcp || command -v beads-mcp
```

Falls beads-mcp fehlt, frage mit AskUserQuestion:

```
beads-mcp (Python MCP Server) nicht gefunden. Installieren?

- **uv (Recommended)**: uv tool install beads-mcp
- **pip**: pip install beads-mcp
- **pipx**: pipx install beads-mcp
- **Überspringen**: Später manuell installieren
```

Je nach Wahl ausführen.

**Erst wenn beide Komponenten installiert sind**, den MCP Server hinzufügen:

```bash
claude mcp add beads -- beads-mcp
```

**Optionale MCPs (keine Credentials nötig):**

```bash
# Playwright - Functional Testing
claude mcp add playwright -- npx -y @anthropic/mcp-server-playwright@latest
```

**MCPs mit Credentials - erst nach Token/Zugangsdaten fragen:**

```bash
# GitHub - braucht Personal Access Token
claude mcp add -e GITHUB_PERSONAL_ACCESS_TOKEN=<token> github -- npx -y @modelcontextprotocol/server-github

# MariaDB - braucht DB-Zugangsdaten
claude mcp add -e DB_HOST=<host> -e DB_PORT=<port> -e DB_USER=<user> -e DB_PASSWORD=<pw> mariadb -- npx -y @benborla29/mcp-server-mysql
```

Bei GitHub: Frage nach dem `GITHUB_PERSONAL_ACCESS_TOKEN`.
Bei MariaDB: Frage nach `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`.

### Schritt 4: Verifikation

Nach der Installation:

1. `claude mcp list` erneut ausführen
2. Finalen Status als Tabelle anzeigen
3. Hinweis ausgeben: **Claude Code muss neu gestartet werden, damit die neuen MCP Server aktiv werden.**

## Wichtig

- Nur fehlende MCPs zur Installation anbieten
- Bereits installierte MCPs nicht nochmal installieren
- Bei Credentials-MCPs: Keine Dummy-Werte verwenden, immer den User fragen
- Installationsfehler klar kommunizieren
