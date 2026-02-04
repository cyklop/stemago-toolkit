---
name: beads-setup
description: "Beads Memory-System initialisieren und konfigurieren"
---

# Beads Setup

Initialisiert das Beads Memory-System für AI-Agent Session-Tracking. Installiert fehlende Abhängigkeiten automatisch.

## Workflow

### Schritt 1: Git-Repository prüfen

```bash
git rev-parse --git-dir 2>/dev/null
```

Falls kein Git-Repo: Stoppe mit Meldung "Beads benötigt ein Git-Repository. Bitte erst `git init` ausführen."

### Schritt 2: bd CLI prüfen und installieren

```bash
which bd || command -v bd
```

Falls bd nicht gefunden, frage mit AskUserQuestion:

```
bd CLI nicht gefunden. Wie möchtest du installieren?

- **npm (Recommended)**: Schnellste Option für Node.js Nutzer
- **Homebrew**: Für macOS Nutzer ohne Node.js
- **Go**: Für Go-Entwickler
- **Überspringen**: Manuell installieren
```

Je nach Wahl ausführen:

```bash
# npm (empfohlen)
npm install -g @beads/bd

# Homebrew (macOS)
brew install beads

# Go
go install github.com/steveyegge/beads/cmd/bd@latest
```

Nach Installation verifizieren:

```bash
bd --version
```

Falls Installation fehlschlägt, zeige Fehlermeldung und stoppe.

### Schritt 3: beads-mcp prüfen und installieren

Prüfe ob beads-mcp verfügbar ist:

```bash
which beads-mcp || command -v beads-mcp || python -c "import beads_mcp" 2>/dev/null
```

Falls nicht gefunden, frage mit AskUserQuestion:

```
beads-mcp (MCP Server) nicht gefunden. Wie möchtest du installieren?

- **uv (Recommended)**: Schnellster Python Package Manager
- **pip**: Standard Python Installation
- **pipx**: Isolierte Installation
- **Überspringen**: MCP später manuell konfigurieren
```

Je nach Wahl ausführen:

```bash
# uv (empfohlen - schnellster)
uv tool install beads-mcp

# pip
pip install beads-mcp

# pipx (isoliert)
pipx install beads-mcp
```

Nach Installation verifizieren:

```bash
beads-mcp --help 2>/dev/null || echo "Installation erfolgreich"
```

### Schritt 4: Bestehende Beads-Installation prüfen

```bash
ls -la .beads/ 2>/dev/null
```

Falls `.beads/` existiert, frage mit AskUserQuestion:

```
Beads bereits initialisiert. Was möchtest du tun?

- **Fortfahren**: Bestehende Installation nutzen
- **Neu initialisieren**: ACHTUNG - löscht bestehende Tasks!
```

### Schritt 5: Modus wählen

Frage mit AskUserQuestion:

```
Wie soll Beads konfiguriert werden?

- **Normal (Recommended)**: .beads/ wird ins Repository committed
  → Team-Mitglieder sehen Task-History
  → Vollständige Git-Integration

- **Stealth Mode**: .beads/ bleibt lokal (.gitignore)
  → Nur für dich sichtbar
  → Keine Commits, keine Merge-Konflikte
```

### Schritt 6: Beads initialisieren

Je nach Wahl:

```bash
# Normal Mode
bd init

# Stealth Mode
bd init --stealth
```

Zeige Output dem User.

### Schritt 7: MCP Server konfigurieren

Prüfe ob beads MCP bereits konfiguriert ist:

```bash
claude mcp list 2>/dev/null | grep -i beads
```

Falls nicht konfiguriert und beads-mcp installiert:

```bash
claude mcp add beads -- beads-mcp
```

Falls `claude mcp add` fehlschlägt, zeige manuelle Anleitung:

```markdown
## MCP manuell konfigurieren

Falls `claude mcp add` nicht funktioniert, füge zu deiner MCP-Konfiguration hinzu:

**~/.claude/settings.json** oder **mcp_servers.json**:
```json
{
  "mcpServers": {
    "beads": {
      "command": "beads-mcp"
    }
  }
}
```
```

### Schritt 8: Einstellungen speichern

Speichere die Konfiguration in `.claude/settings.local.json`:

```json
{
  "beads": {
    "mode": "normal|stealth",
    "initialized": true,
    "initializedAt": "ISO-timestamp"
  }
}
```

Falls die Datei existiert, merge die neuen Einstellungen.

### Schritt 9: Abschluss

Zeige Zusammenfassung:

```markdown
## Beads erfolgreich eingerichtet!

### Installation
| Komponente | Status |
|------------|--------|
| bd CLI | ✓ installiert (vX.X.X) |
| beads-mcp | ✓ installiert |
| MCP Server | ✓ konfiguriert |
| Beads DB | ✓ initialisiert |

### Konfiguration
| Setting | Wert |
|---------|------|
| Modus | Normal / Stealth |
| Datenbank | .beads/ |

### Nächste Schritte

1. **Claude Code neu starten** - damit MCP Server aktiv wird
2. **Tasks erstellen**: `bd create "Task-Titel" -p 1`
3. **Ready-Queue**: `/beads-ready` zeigt Tasks ohne Blocker
4. **Session-Ende**: `/land-the-plane` für Handoff

### Wichtige Befehle

| Befehl | Funktion |
|--------|----------|
| `bd ready` | Tasks ohne Blocker anzeigen |
| `bd create "Titel" -p 0` | Neuen Task erstellen (Priorität 0-3) |
| `bd show <id>` | Task-Details anzeigen |
| `bd stats` | Projekt-Statistiken |
| `bd list` | Alle Tasks anzeigen |

### Prioritäten-Legende
| Priorität | Bedeutung |
|-----------|-----------|
| 0 | Kritisch - Sofort |
| 1 | Hoch - Heute |
| 2 | Normal - Diese Woche |
| 3 | Niedrig - Irgendwann |
```

## Voraussetzungen-Check (Zusammenfassung)

| Komponente | Prüfung | Installation |
|------------|---------|--------------|
| Git | `git rev-parse --git-dir` | Muss vorhanden sein |
| bd CLI | `which bd` | npm/brew/go |
| beads-mcp | `which beads-mcp` | uv/pip/pipx |
| MCP Config | `claude mcp list` | `claude mcp add` |

## Edge Cases

- **Kein Git**: Klare Fehlermeldung, Setup abbrechen
- **npm/pip nicht verfügbar**: Alternative Installationsmethode anbieten
- **Installation fehlgeschlagen**: Fehler anzeigen, manuelle Anleitung
- **Bereits initialisiert**: Fragen ob fortfahren oder neu
- **MCP add fehlschlägt**: Manuelle Konfigurationsanleitung zeigen

$ARGUMENTS
