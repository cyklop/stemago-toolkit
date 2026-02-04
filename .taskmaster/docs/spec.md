# Feature Specification: Beads Integration

## Übersicht

Integration von Steve Yegges "Beads" Memory-System in das stemago-toolkit als Ersatz für Task Master. Beads gibt AI-Coding-Agenten ein persistentes, strukturiertes Gedächtnis für Session-übergreifendes Arbeiten.

## Ziele

- AI-Agent erhält Session-übergreifendes Gedächtnis ("50 First Dates" Problem lösen)
- Task Master vollständig durch Beads ersetzen
- Nahtlose Integration mit bestehendem /reflect-System
- Bestehende Agent-Architektur auf Beads migrieren

## Scope

### Inkludiert

1. **MCP Server Integration**
   - `beads-mcp` als MCP Server einbinden
   - Setup-Skill für Installation und Konfiguration
   - Automatische Erkennung in `/mcp-setup`

2. **Skills**
   - `/beads-setup` - Initialisierung mit Stealth/Normal-Mode Wahl
   - `/beads-ready` - Zeigt Tasks ohne Blocker (ready queue)
   - `/land-the-plane` - Session-Ende Handoff mit Prompt-Generierung

3. **Hook-Integration**
   - SessionEnd-Hook: `/reflect` + "Land the Plane" automatisch nacheinander
   - Automatisches Task-Status-Update bei Session-Ende

4. **Agent-Migration**
   - `task-orchestrator.md` → Beads-basiert umschreiben
   - `task-executor.md` → Beads-Tools statt Task Master MCP
   - `task-checker.md` → Validierung gegen Beads-Tasks
   - Alle Task Master MCP-Referenzen entfernen

5. **Konfigurierbarkeit**
   - User wählt bei Setup: Stealth Mode (lokal) vs. Committed (.beads/ im Repo)
   - Einstellung in `.claude/settings.local.json` speichern

### Exkludiert

- Eigene Beads-Reimplementation (wir nutzen das offizielle bd CLI/MCP)
- Änderungen am Core /reflect-System (bleibt für Learnings)
- Multi-Agent-Messaging (MCP Agent Mail ist separates Feature)
- Beads Web-UI oder Viewer

## Technische Anforderungen

### MCP Server Setup

```json
// In .claude/settings.json oder mcp_servers.json
{
  "mcpServers": {
    "beads": {
      "command": "npx",
      "args": ["-y", "beads-mcp"],
      "env": {}
    }
  }
}
```

### Beads CLI Voraussetzung

```bash
# User muss bd global installiert haben
npm install -g @beads/bd
# oder
brew install beads
```

### Erwartete MCP Tools (von beads-mcp)

- `beads_ready` - Liste der ready Tasks
- `beads_create` - Task erstellen
- `beads_show` - Task-Details anzeigen
- `beads_update` - Task-Status ändern
- `beads_dep_add` - Dependency hinzufügen
- `beads_sync` - Mit Git synchronisieren

### Hook-Konfiguration

```json
// hooks/hooks.json erweitern
{
  "hooks": [
    {
      "event": "SessionEnd",
      "command": "scripts/session-land-the-plane.sh"
    }
  ]
}
```

## UI/UX Anforderungen

### /beads-setup Flow

1. Prüfe ob `bd` CLI installiert ist
2. Falls nicht: Installationsanleitung zeigen
3. Falls ja: Frage nach Modus (Stealth/Normal)
4. `bd init` oder `bd init --stealth` ausführen
5. MCP Server Konfiguration hinzufügen
6. Erfolgsbestätigung

### /land-the-plane Output

```markdown
## Session-Handoff generiert

### Erledigte Tasks
- [x] bd-a3f8.1 - API Endpoint implementiert
- [x] bd-a3f8.2 - Tests geschrieben

### Offene Tasks (ready)
- [ ] bd-a3f8.3 - Frontend-Integration (Priorität 0)
- [ ] bd-a3f8.4 - Error Handling (Priorität 1)

### Prompt für nächste Session
```
Fortsetzen bei: bd-a3f8.3 Frontend-Integration
Kontext: API ist fertig (/api/users), Tests grün.
Nächster Schritt: UserList-Komponente mit useSWR anbinden.
Blocker: Keine
```

Gespeichert in: .beads/session-handoff.md
```

## Edge Cases & Error Handling

1. **bd CLI nicht installiert**
   - Setup-Skill zeigt Installationsanleitung
   - Skill funktioniert nicht ohne CLI → klare Fehlermeldung

2. **Kein Git-Repository**
   - Beads braucht Git → Fehlermeldung: "Bitte erst `git init` ausführen"

3. **Bestehende .beads/ Daten**
   - Bei `bd init` in bestehendem Projekt: Warnung, nicht überschreiben

4. **Konflikt mit Task Master**
   - Migrations-Skill: bestehende Task Master Tasks nach Beads exportieren?
   - Oder sauberer Neustart empfehlen

5. **Offline-Nutzung**
   - Beads funktioniert offline (SQLite Cache)
   - Sync passiert bei nächster Git-Operation

6. **Merge-Konflikte in .beads/**
   - Beads Hash-IDs verhindern die meisten Konflikte
   - Falls doch: `bd sync` löst automatisch

## Integration mit bestehendem System

### /reflect bleibt unverändert
- Weiterhin für Learnings/Präferenzen zuständig
- Speichert in `.claude/learnings/`
- Kein Overlap mit Beads

### SessionEnd-Hook Reihenfolge
1. Beads: Task-Status updaten, "Land the Plane" Prompt generieren
2. /reflect: Learnings aus Session extrahieren
3. Reminder für uncommitted changes (bestehender Hook)

### Agent-Migration Strategie

| Alter Agent | Änderung |
|-------------|----------|
| task-orchestrator | `mcp__task-master__*` → `mcp__beads__*` |
| task-executor | Task-Lookup via Beads statt Task Master |
| task-checker | Validierung gegen Beads-Tasks |
| research-agent | Keine Änderung (nutzt kein Task Master) |

## Offene Fragen

1. **beads-mcp Stabilität** - Ist das MCP-Paket production-ready? Dokumentation prüfen.
2. **Memory Decay Konfiguration** - Kann man einstellen wann/wie Tasks zusammengefasst werden?
3. **Export von Task Master** - Lohnt sich ein Migrations-Script oder Neustart?

## Nächste Schritte

1. `beads-mcp` Dokumentation prüfen (verfügbare Tools)
2. `/beads-setup` Skill implementieren
3. `/land-the-plane` Skill implementieren
4. SessionEnd-Hook erweitern
5. Agents migrieren (task-orchestrator zuerst)
6. Task Master MCP aus Empfehlungen entfernen
7. README.md aktualisieren

## Quellen

- [Steve Yegge: Introducing Beads](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)
- [GitHub: steveyegge/beads](https://github.com/steveyegge/beads)
- [Beads Best Practices](https://steve-yegge.medium.com/beads-best-practices-2db636b9760c)
- [Paddo.dev: Beads Analysis](https://paddo.dev/blog/beads-memory-for-coding-agents/)
