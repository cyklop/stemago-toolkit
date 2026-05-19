# Project Learnings

Automatisch extrahierte Learnings aus Sessions. Wird von `/reflect` verwaltet.

---

## Tools/MCP

### Plugin-Versionierung (MEDIUM)
_Session: 2026-02-08_

Beim Plugin-Version-Bump muessen DREI Dateien synchron aktualisiert werden:
- `plugins/stemago-tools/.claude-plugin/plugin.json`
- `CLAUDE.md` (Version im Project Overview)
- `.claude-plugin/marketplace.json` (beide Version-Felder: metadata + plugins)

Ohne marketplace.json-Update erkennt der Claude Code Plugin-Update-Mechanismus keine neuen Versionen.

### Plugin-Cache-Architektur (MEDIUM)
_Session: 2026-02-08_

Claude Code Plugin-System hat 3 Ebenen:
- **Marketplace-Clone**: `~/.claude/plugins/marketplaces/<name>/` (git clone)
- **Installations-Cache**: `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`
- **Metadaten**: `~/.claude/plugins/installed_plugins.json`

### Plugin-Update-Befehle (MEDIUM)
_Session: 2026-02-08_

1. `claude plugin update stemago-tools@stemago-toolkit` (Standard)
2. `/plugin marketplace update stemago-toolkit` (Marketplace refreshen)
3. Deinstall + Reinstall als Fallback

---

## Git/Commits

### Commit-Konvention (MEDIUM)
_Session: 2026-02-08_

- `feat:` fuer neue Features
- `chore:` fuer Version-Bumps, Maintenance
- `fix:` fuer Bugfixes
- `learn:` fuer Learnings-Updates

---

## Architecture

### End-to-End Workflow-Denken (LOW)
_Session: 2026-02-08_

User bevorzugt vollstaendige Workflows statt isolierter Schritte.
Beispiel: Interview -> Spec -> Tasks -> Execute -> Review -> Reflect

### Direkte Anweisungen (LOW)
_Session: 2026-02-08_

User gibt kurze, praezise Anweisungen ("commit this and push it with a new version").
Keine langen Erklaerungen noetig - direkt umsetzen.
