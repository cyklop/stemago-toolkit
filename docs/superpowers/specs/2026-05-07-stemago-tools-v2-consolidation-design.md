# stemago-tools v2.0.0 — Skill-Konsolidierung & Beschreibungs-Schärfung

**Datum:** 2026-05-07
**Status:** Design (Pre-Implementation)
**Auslöser:** Feedback aus FamFlow-Kontext: Plugin liefert 16 Skills, davon mehrere Setup-only oder duplikatartig. Im aktiven Projekt-Alltag entsteht Rauschen in der Skill-Liste.

## Ziele

1. Skill-Anzahl reduzieren ohne Funktionalitätsverlust (16 → 11).
2. Verbleibende Skills mit präziseren Beschreibungen ausstatten, sodass Auto-Trigger nicht spontan in eingerichteten Projekten feuern.
3. Klare Doku, welche Skills in welcher Projektphase sinnvoll sind.

## Nicht-Ziele

- Sub-Plugin-Split (verworfen wegen Versionierungs- und Cache-Komplexität).
- Backwards-Compat Aliases (verworfen, da sie die Konsolidierungs-Wirkung neutralisieren).
- Anpassung der unveränderten Skills (`docs-lookup`, `browser-test`, `db-inspect`, `github-ops`, `interview`, `beads-ready`, `land-the-plane`, `reflect`).

## Architektur-Änderungen

### Konsolidierung 1: `setup` (ersetzt 3 Skills)

**Ersetzt:** `init-project`, `beads-setup`, `mcp-setup`

**Neuer Skill:** `plugins/stemago-tools/skills/setup/SKILL.md`

**Argument-Schema:**
- `--project` — CLAUDE.md erstellen (entspricht altem `init-project`)
- `--beads` — Beads installieren und konfigurieren (entspricht altem `beads-setup`)
- `--mcp` — MCP-Server prüfen/installieren (entspricht altem `mcp-setup`)
- `--all` — alle drei Subjobs nacheinander
- *(kein Argument)* — interaktive Detection + Auswahl

**Idempotenz-Anforderung:** Skill prüft existierenden Zustand und meldet "bereits eingerichtet" statt blind zu überschreiben. `--force` ergänzt für bewusste Re-Initialisierung.

**Beschreibung (Draft):**
> Projekt-Initialisierung: CLAUDE.md, Beads-Tracker oder MCP-Server einrichten. Verwende NUR bei expliziter Erst-Einrichtung oder Re-Initialisierung ('Beads neu installieren', 'CLAUDE.md neu erstellen', 'MCPs prüfen'). Triggert NICHT bei normaler Entwicklungsarbeit. Args: --project / --beads / --mcp / --all.

### Konsolidierung 2: `reflect-config` (ersetzt 3 Skills)

**Ersetzt:** `reflect-on`, `reflect-off`, `reflect-status`

**Neuer Skill:** `plugins/stemago-tools/skills/reflect-config/SKILL.md`

**Argument-Schema:**
- `--on` — Auto-Reflection aktivieren (entspricht altem `reflect-on`)
- `--off` — deaktivieren (entspricht altem `reflect-off`)
- `--status` — Status anzeigen (Default, entspricht altem `reflect-status`)

**Beschreibung (Draft):**
> Auto-Reflection-Einstellung steuern: aktivieren, deaktivieren oder Status anzeigen. Verwende bei 'reflect ein/aus', 'auto-reflect aktivieren', 'wie viele Learnings habe ich', 'ist Reflect aktiv'. Args: --on / --off / --status (Default: --status).

### Anpassung: `review` (Beschreibung schärfen)

**Pfad bleibt:** `plugins/stemago-tools/skills/review/SKILL.md`

**Body unverändert. Frontmatter `description` wird gegen `code-review:code-review` und das Standard-`review`-Skill abgegrenzt.**

**Beschreibung (Draft):**
> stemago-tools Code Review: prüft die Änderungen seit dem letzten Commit gegen Projekt-Konventionen aus CLAUDE.md. Verwende wenn der User 'Review bitte' sagt UND das Projekt eine CLAUDE.md mit Konventionen hat. NICHT verwenden für PR-Reviews (dafür github-ops oder /code-review).

## Hook-Anpassungen

Zwei Hook-Skripte referenzieren alte Skill-Namen und müssen angepasst werden:

1. `plugins/stemago-tools/hooks/scripts/session-reflect.sh` — Hinweistext `Deaktivieren: /reflect-off` → `Deaktivieren: /reflect-config --off`
2. `plugins/stemago-tools/hooks/scripts/session-review-reminder.sh` — Hinweistext `→ /stemago-tools:init-project` → `→ /stemago-tools:setup --project`

## Versions-Bump (3-Datei-Sync)

Major Bump auf **2.0.0**:

1. `plugins/stemago-tools/.claude-plugin/plugin.json` → `"version": "2.0.0"`
2. `.claude-plugin/marketplace.json` → `metadata.version` UND `plugins[0].version` → `"2.0.0"`
3. `CLAUDE.md` Overview-Zeile → `Version 2.0.0`

Begründung Major: Hard-break (entfernte Skill-Namen). User mit Skripten/Aliases auf alte Namen müssen umstellen.

## Dokumentation

### CHANGELOG.md (neu anlegen)

Existiert noch nicht im Repo. Anlage mit Eintrag:

```
## 2.0.0 — 2026-05-07
### Breaking
- Konsolidierung: init-project + beads-setup + mcp-setup → setup
  Migration:
    /init-project       → /setup --project
    /beads-setup        → /setup --beads
    /mcp-setup          → /setup --mcp
- Konsolidierung: reflect-on + reflect-off + reflect-status → reflect-config
  Migration:
    /reflect-on         → /reflect-config --on
    /reflect-off        → /reflect-config --off
    /reflect-status     → /reflect-config --status (oder default)
### Changed
- review: Beschreibung gegenüber Standard-/code-review-Skills geschärft
- setup: idempotent (meldet bereits eingerichteten Zustand statt zu überschreiben), --force für Re-Init
### Removed
- Skills init-project, beads-setup, mcp-setup, reflect-on, reflect-off, reflect-status (siehe Migration)
```

### README-Erweiterung

Neuer Abschnitt `## Skills nach Projektphase` mit 3 Phasen:

- **Onboarding** (neue Projekte): `setup`, `interview`, `beads-ready`
- **Aktive Entwicklung**: `docs-lookup`, `browser-test`, `db-inspect`, `github-ops`, `review`, `reflect`, `land-the-plane`
- **Operativ/optional**: `reflect-config` (nur bei Konfigurationsbedarf)

Plus Hinweis: in eingerichteten Projekten per `/skills` Setup-Skills selektiv deaktivieren falls gewünscht.

## Description Optimization (skill-creator Workflow)

Vor Implementation: Die drei betroffenen Beschreibungen (`setup`, `reflect-config`, `review`) durch den skill-creator-Workflow optimieren.

**Vorgehen:**
1. Eval-Set pro Skill (10 should-trigger / 10 should-not-trigger), realistische User-Anfragen.
2. User reviewt Eval-Set via HTML-Reviewer.
3. `scripts.run_loop` mit `--max-iterations 5` und Modell `claude-opus-4-7` läuft Background.
4. Beste Description (Test-Score) wird ins SKILL.md übernommen.

**Test-Coverage:**
- `setup`: Trigger bei Re-Init-Anfragen, kein Trigger bei normalem Dev-Work.
- `reflect-config`: Trigger bei Auto-Reflect-Steuerung, kein Trigger bei "speicher das als Learning" (das ist `reflect`).
- `review`: Trigger bei lokalem Code-Check, kein Trigger bei PR-Review-Anfragen.

## Implementations-Reihenfolge

1. Skill-Drafts schreiben (setup/SKILL.md, reflect-config/SKILL.md)
2. review/SKILL.md Frontmatter-Update
3. Description Optimization Loop (skill-creator)
4. Optimierte Descriptions einsetzen
5. Hook-Skripte anpassen
6. Alte Skill-Verzeichnisse löschen (init-project, beads-setup, mcp-setup, reflect-on, reflect-off, reflect-status)
7. CHANGELOG.md anlegen
8. README erweitern
9. Drei-Datei-Versions-Bump 2.0.0
10. Commit + Push + Marketplace-Clone manuell pullen (laut Memory-Hinweis)

## Risiken & Mitigationen

| Risiko | Mitigation |
|---|---|
| Hooks/Agents im Userland referenzieren alte Skill-Namen | CHANGELOG mit Migration-Tabelle prominent. Major-Bump signalisiert Breaking. |
| Memory-Drift: User-Memory hält alte Skill-Namen für Empfehlungen | Out-of-Scope für dieses Refactoring. User aktualisiert eigene Memory bei Bedarf. |
| Plugin-Cache: alte Version bleibt aktiv | Memory-Hinweis greift: `cd ~/.claude/plugins/marketplaces/stemago-toolkit && git pull` nach Push. |
| skill-creator run_loop schlägt für eine Description fehl | Fallback: manuelle Iteration der Description, dokumentiert im Spec. |

## Erfolgskriterien

- 16 → 11 Skills im Plugin gelistet.
- Alle drei optimierten Descriptions erreichen ≥80% Test-Score in der run_loop.
- Hooks zeigen neue Skill-Namen.
- CHANGELOG vorhanden mit Migration-Tabelle.
- README zeigt Phasen-Doku.
- `claude --plugin-dir ./plugins/stemago-tools` listet die neuen Skills korrekt.
- Plugin.json + marketplace.json + CLAUDE.md auf 2.0.0 synchron.
