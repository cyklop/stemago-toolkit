# stemago-tools v2.0.0 Consolidation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Konsolidiere 6 Skills auf 2, schärfe 3 Beschreibungen, dokumentiere Migration und bumpe das Plugin auf 2.0.0.

**Architecture:** Zwei neue Skills mit Argument-Routing (`setup --project|--beads|--mcp`, `reflect-config --on|--off|--status`) ersetzen 6 Einzel-Skills. Alte Verzeichnisse werden ersatzlos entfernt (Hard break, kein Alias). Hooks werden auf neue Befehle angepasst. Beschreibungen werden via skill-creator `run_loop` optimiert. Versions-Bump auf 2.0.0 erfolgt synchron in plugin.json + marketplace.json + CLAUDE.md.

**Tech Stack:** Markdown-basierte Skills, YAML-Frontmatter, Bash-Hooks, JSON-Manifeste. skill-creator-Tooling unter `~/.claude/plugins/cache/claude-plugins-official/skill-creator/`.

**Spec:** `docs/superpowers/specs/2026-05-07-stemago-tools-v2-consolidation-design.md`

---

## File Structure

**Create (3):**
- `plugins/stemago-tools/skills/setup/SKILL.md` — neuer konsolidierter Setup-Skill
- `plugins/stemago-tools/skills/reflect-config/SKILL.md` — neuer konsolidierter Reflect-Steuerungs-Skill
- `CHANGELOG.md` — neue Datei im Repo-Root

**Modify (5):**
- `plugins/stemago-tools/skills/review/SKILL.md` — nur Frontmatter-`description` schärfen, Body unverändert
- `plugins/stemago-tools/hooks/scripts/session-reflect.sh` — Hinweistext auf neuen Skill-Namen
- `plugins/stemago-tools/hooks/scripts/session-review-reminder.sh` — Hinweistext auf neuen Skill-Namen
- `plugins/stemago-tools/.claude-plugin/plugin.json` — Version 1.5.0 → 2.0.0
- `.claude-plugin/marketplace.json` — `metadata.version` + `plugins[0].version` → 2.0.0
- `CLAUDE.md` — Overview-Zeile Version 1.5.0 → 2.0.0
- `README.md` — neuer Abschnitt "Skills nach Projektphase"

**Delete (6 Verzeichnisse):**
- `plugins/stemago-tools/skills/init-project/`
- `plugins/stemago-tools/skills/beads-setup/`
- `plugins/stemago-tools/skills/mcp-setup/`
- `plugins/stemago-tools/skills/reflect-on/`
- `plugins/stemago-tools/skills/reflect-off/`
- `plugins/stemago-tools/skills/reflect-status/`

**Workspace (für skill-creator):**
- `docs/superpowers/specs/skill-eval-workspace/setup-eval.json`
- `docs/superpowers/specs/skill-eval-workspace/reflect-config-eval.json`
- `docs/superpowers/specs/skill-eval-workspace/review-eval.json`

---

## Task 1: setup/SKILL.md schreiben (Body)

**Files:**
- Create: `plugins/stemago-tools/skills/setup/SKILL.md`

Konsolidiert die Bodies von `init-project`, `beads-setup`, `mcp-setup` mit Argument-Routing. Idempotenz-Pflicht: bei bestehender Konfiguration meldet der Skill "bereits eingerichtet" statt zu überschreiben (außer `--force`).

- [ ] **Step 1: Verzeichnis und Datei anlegen**

```bash
mkdir -p plugins/stemago-tools/skills/setup
```

- [ ] **Step 2: SKILL.md schreiben**

Schreibe `plugins/stemago-tools/skills/setup/SKILL.md` mit folgendem Inhalt (Draft-Description, wird in Task 5 optimiert):

````markdown
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
````

- [ ] **Step 3: Verifizieren**

```bash
ls plugins/stemago-tools/skills/setup/SKILL.md && head -5 plugins/stemago-tools/skills/setup/SKILL.md
```

Erwartet: Datei existiert, Frontmatter mit `name: setup` ist sichtbar.

---

## Task 2: reflect-config/SKILL.md schreiben (Body)

**Files:**
- Create: `plugins/stemago-tools/skills/reflect-config/SKILL.md`

Konsolidiert `reflect-on`, `reflect-off`, `reflect-status` mit Argument-Routing. Default ist `--status`.

- [ ] **Step 1: Verzeichnis anlegen**

```bash
mkdir -p plugins/stemago-tools/skills/reflect-config
```

- [ ] **Step 2: SKILL.md schreiben**

Schreibe `plugins/stemago-tools/skills/reflect-config/SKILL.md`:

````markdown
---
name: reflect-config
description: "Auto-Reflection-Einstellung steuern: aktivieren, deaktivieren oder Status anzeigen. Verwende bei 'reflect ein/aus', 'auto-reflect aktivieren', 'wie viele Learnings habe ich', 'ist Reflect aktiv'. Args: --on / --off / --status (Default: --status). NICHT verwenden um Learnings JETZT zu extrahieren — dafür gibt es /reflect."
argument-hint: "[--on|--off|--status]"
---

# /reflect-config - Auto-Reflection steuern

Konsolidierter Steuerungs-Skill für die automatische Session-Reflection. Ersetzt `reflect-on`, `reflect-off`, `reflect-status` (entfernt in v2.0.0).

Für die manuelle Extraktion von Learnings nutze `/reflect`.

## Argumente

- `--on` — Auto-Reflect aktivieren
- `--off` — Auto-Reflect deaktivieren
- `--status` — aktuellen Status + Learnings-Statistik anzeigen (Default)

## Argument-Routing

Werte `$ARGUMENTS` aus:
- Enthält `--on` → Subjob ON
- Enthält `--off` → Subjob OFF
- Sonst (inkl. `--status` oder leer) → Subjob STATUS

---

## Subjob ON (--on)

### Step 1: State-Datei erstellen

```bash
mkdir -p .claude/state
echo "enabled=$(date -Iseconds)" > .claude/state/reflect-enabled
```

### Step 2: Bestätigung

```
Auto-Reflect AKTIVIERT

Am Ende jeder Session wird automatisch analysiert:
- Korrekturen und explizite Anweisungen
- Erfolgreiche Patterns
- Implizite Präferenzen

Learnings werden gespeichert in:
   .claude/learnings/project-learnings.md

Befehle:
- /reflect-config --off    - Deaktivieren
- /reflect-config --status - Status anzeigen
- /reflect                 - Manuell auslösen
```

### Step 3: Hook-Hinweis

```
Die automatische Reflection wird durch den session-reflect Hook
am Session-Ende ausgelöst. Bei manuellen /compact oder Session-Wechsel
wird empfohlen /reflect manuell aufzurufen.
```

---

## Subjob OFF (--off)

### Step 1: State-Datei entfernen

```bash
rm -f .claude/state/reflect-enabled
```

### Step 2: Bestätigung

```
Auto-Reflect DEAKTIVIERT

Die automatische Session-Reflection ist nun ausgeschaltet.
Learnings werden nicht mehr automatisch extrahiert.

Du kannst weiterhin manuell /reflect aufrufen.

Befehle:
- /reflect-config --on    - Wieder aktivieren
- /reflect                - Manuell Learnings extrahieren
```

---

## Subjob STATUS (--status oder Default)

### Step 1: Auto-Reflect-Flag prüfen

```bash
if [ -f ".claude/state/reflect-enabled" ]; then
    cat .claude/state/reflect-enabled
fi
```

### Step 2: Learnings-Statistik

```
Read .claude/learnings/project-learnings.md
```

Zähle:
- HIGH / MEDIUM / LOW confidence Learnings
- Learnings pro Kategorie

### Step 3: Git-Historie

```bash
git log --oneline -5 -- .claude/learnings/project-learnings.md
```

### Step 4: Cleanup-Vorschläge

Identifiziere Learnings älter als 30 Tage.

### Step 5: Status-Output

```
REFLECTION SYSTEM STATUS

Auto-Reflect: AKTIV / INAKTIV
Aktiviert am: [Datum] (wenn aktiv)

LEARNINGS STATISTIK

HIGH Confidence:   XX
MEDIUM Confidence: XX
LOW Confidence:    XX
---
TOTAL:             XX

KATEGORIEN

Code Style:    X | Prisma/Database: X
Testing:       X | Git/Commits:     X
Architecture:  X | Tools/MCP:       X
UI/Components: X | API:             X

LETZTE ÄNDERUNGEN

[commit] learn: ... (vor X Tagen)

CLEANUP

X Learnings sind älter als 30 Tage. Führe /reflect aus um zu überprüfen.

Befehle:
- /reflect              - Learnings aus aktueller Session extrahieren
- /reflect-config --on  - Auto-Reflect aktivieren
- /reflect-config --off - Auto-Reflect deaktivieren
```

$ARGUMENTS
````

- [ ] **Step 3: Verifizieren**

```bash
ls plugins/stemago-tools/skills/reflect-config/SKILL.md && head -5 plugins/stemago-tools/skills/reflect-config/SKILL.md
```

Erwartet: Datei existiert, `name: reflect-config` sichtbar.

---

## Task 3: review/SKILL.md description schärfen

**Files:**
- Modify: `plugins/stemago-tools/skills/review/SKILL.md` (nur Frontmatter `description`, Body unverändert)

- [ ] **Step 1: Aktuelle description ersetzen**

Ersetze in `plugins/stemago-tools/skills/review/SKILL.md` die Zeile mit `description:` durch:

```yaml
description: "stemago-tools Code Review: prüft die Änderungen seit dem letzten Commit gegen Projekt-Konventionen aus CLAUDE.md mit fünf parallelen Review-Agents (Security, Performance, Quality, Docs, Spec-Compliance). Verwende wenn der User 'Review bitte', 'prüf den Code' oder 'ist das so OK' sagt UND das Projekt eine CLAUDE.md mit Konventionen hat. NICHT verwenden für PR-Reviews oder gezielte Security-Audits — dafür github-ops oder /code-review oder /security-review."
```

- [ ] **Step 2: Verifizieren**

```bash
head -5 plugins/stemago-tools/skills/review/SKILL.md
```

Erwartet: Erste fünf Zeilen zeigen die neue description, name bleibt `review`.

---

## Task 4: Commit Skill-Drafts

- [ ] **Step 1: Stage und commit**

```bash
git add plugins/stemago-tools/skills/setup plugins/stemago-tools/skills/reflect-config plugins/stemago-tools/skills/review/SKILL.md docs/superpowers/specs/2026-05-07-stemago-tools-v2-consolidation-design.md docs/superpowers/plans/2026-05-07-stemago-tools-v2-consolidation.md
git commit -m "feat(skills): add consolidated setup and reflect-config skills, sharpen review description

- setup: replaces init-project + beads-setup + mcp-setup (with --project/--beads/--mcp/--all)
- reflect-config: replaces reflect-on + reflect-off + reflect-status (with --on/--off/--status)
- review: description tightened to disambiguate from /code-review and /security-review
- Spec and Plan documents added under docs/superpowers/

Old skill directories will be removed in a follow-up commit after description optimization."
```

- [ ] **Step 2: Verifizieren**

```bash
git log -1 --stat
```

Erwartet: Commit listet die drei neuen/geänderten Skill-Dateien sowie Spec/Plan.

---

## Task 5: Description Optimization (skill-creator run_loop)

**Files:**
- Create: `docs/superpowers/specs/skill-eval-workspace/setup-eval.json`
- Create: `docs/superpowers/specs/skill-eval-workspace/reflect-config-eval.json`
- Create: `docs/superpowers/specs/skill-eval-workspace/review-eval.json`

Optimiert die drei Beschreibungen automatisch durch das `run_loop`-Skript des skill-creator. User-Review der Eval-Sets vor dem Lauf.

- [ ] **Step 1: skill-creator-Pfad ermitteln**

```bash
ls ~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/run_loop.py 2>/dev/null
```

Erwartet: ein Pfad. Speichere ihn in einer Variable für spätere Schritte:

```bash
SKILL_CREATOR_DIR=$(dirname $(ls ~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/run_loop.py | head -1))/..
echo "$SKILL_CREATOR_DIR"
```

- [ ] **Step 2: Workspace anlegen**

```bash
mkdir -p docs/superpowers/specs/skill-eval-workspace
```

- [ ] **Step 3: Eval-Set für `setup` schreiben**

Schreibe `docs/superpowers/specs/skill-eval-workspace/setup-eval.json`:

```json
[
  {"query": "ich richte gerade ein neues Next.js-Projekt für einen Kunden ein und brauche die Workflow-Regeln aus CLAUDE.md, kannst du das einrichten?", "should_trigger": true},
  {"query": "Beads ist hier noch nicht installiert, kannst du das initialisieren? Wir wollen Tasks tracken im /Users/me/projekte/familienapp", "should_trigger": true},
  {"query": "wie ist der Stand der MCPs in dem Projekt? sind context7 und chrome-devtools überhaupt eingerichtet?", "should_trigger": true},
  {"query": "richte mir bitte alles ein — CLAUDE.md, Beads und die MCPs für ein neues Repo", "should_trigger": true},
  {"query": "kannst du Beads neu initialisieren? Die alte Datenbank ist kaputt und ich will frisch starten", "should_trigger": true},
  {"query": "ich glaube unsere CLAUDE.md fehlt komplett im backend-monorepo, kannst du sie mit den Workflow-Regeln neu erstellen?", "should_trigger": true},
  {"query": "der context7 MCP scheint zu fehlen, ich kriege ständig 'tool not available' wenn ich docs-lookup nutze", "should_trigger": true},
  {"query": "frisch geklontes Repo, was muss ich für Setup machen damit Beads und MCPs funktionieren?", "should_trigger": true},
  {"query": "der bd-Befehl ist nicht installiert, kannst du den auch mit aufsetzen?", "should_trigger": true},
  {"query": "in meinem famflow-projekt fehlt noch das Beads-tracking, mag das mal jemand initialisieren?", "should_trigger": true},
  {"query": "ich hab gerade einen Bug in der Auth-Logik gefixt, kannst du nochmal drüberschauen?", "should_trigger": false},
  {"query": "schreib mir die Migration für die neue users-Tabelle", "should_trigger": false},
  {"query": "wie funktioniert der OAuth-Flow in unserem Backend?", "should_trigger": false},
  {"query": "die MCP-Antwort vom github-server ist langsam, woran kann das liegen?", "should_trigger": false},
  {"query": "kannst du eine neue Beads-Task erstellen für 'Mobile Layout fixen'?", "should_trigger": false},
  {"query": "ich brauche einen Code Review für die Änderungen die ich gerade gepusht habe", "should_trigger": false},
  {"query": "gib mir bitte die aktuelle Doku zu Next.js 15 Server Actions", "should_trigger": false},
  {"query": "die CLAUDE.md ist da aber etwas veraltet, kannst du den Abschnitt zur Test-Strategie aktualisieren?", "should_trigger": false},
  {"query": "warum scheitert mein Deployment auf Plesk gerade?", "should_trigger": false},
  {"query": "speicher das als Learning: wir nutzen ab jetzt Zod für API-Validierung", "should_trigger": false}
]
```

- [ ] **Step 4: Eval-Set für `reflect-config` schreiben**

Schreibe `docs/superpowers/specs/skill-eval-workspace/reflect-config-eval.json`:

```json
[
  {"query": "kannst du auto-reflect bitte einschalten? Ich will am Session-Ende automatisch Learnings extrahieren", "should_trigger": true},
  {"query": "schalte das automatische Lernen aus, das nervt mich gerade beim Refactoring", "should_trigger": true},
  {"query": "ist Auto-Reflect bei diesem Projekt aktiv oder nicht? Ich sehe nichts beim Session-Ende", "should_trigger": true},
  {"query": "wie viele Learnings habe ich bisher in dem famflow-Repo gesammelt?", "should_trigger": true},
  {"query": "zeig mir bitte den Status vom Reflection-System inklusive Statistik", "should_trigger": true},
  {"query": "auto-reflect an", "should_trigger": true},
  {"query": "auto-reflect aus", "should_trigger": true},
  {"query": "deaktiviere die automatische Learnings-Extraktion fürs Wochenende", "should_trigger": true},
  {"query": "ich will keine Learnings mehr am Ende automatisch sehen", "should_trigger": true},
  {"query": "wann wurde reflect zuletzt aktiviert in diesem Projekt?", "should_trigger": true},
  {"query": "extrahier jetzt bitte alle Learnings aus der aktuellen Session", "should_trigger": false},
  {"query": "speicher das was wir hier gerade besprochen haben als Learning ab", "should_trigger": false},
  {"query": "reflektiere mal kurz was wir heute gelernt haben und schreib das in die Learnings-Datei", "should_trigger": false},
  {"query": "was haben wir in dieser Session über Prisma gelernt?", "should_trigger": false},
  {"query": "lass uns das Refactoring nochmal durchgehen und prüfen ob alles passt", "should_trigger": false},
  {"query": "kannst du den Code-Review-Hook im Plugin aktivieren?", "should_trigger": false},
  {"query": "wie funktioniert der session-reflect.sh Hook eigentlich intern?", "should_trigger": false},
  {"query": "schreib mir die Doku zur reflect-Funktionalität in das README", "should_trigger": false},
  {"query": "ich sehe '.claude/state/reflect-enabled' im Repo — was ist das?", "should_trigger": false},
  {"query": "lösch bitte alle Learnings die älter als 60 Tage sind aus der Datei", "should_trigger": false}
]
```

- [ ] **Step 5: Eval-Set für `review` schreiben**

Schreibe `docs/superpowers/specs/skill-eval-workspace/review-eval.json`:

```json
[
  {"query": "kannst du den Code von dem letzten Commit reviewen? Ich hab die Auth umgebaut", "should_trigger": true},
  {"query": "Review bitte — die Änderungen an der Prisma-Schema-Migration", "should_trigger": true},
  {"query": "schau dir die geänderten Dateien an, ist das so OK was ich da gemacht habe?", "should_trigger": true},
  {"query": "prüf mal den Code ob da Security-Probleme drin sind, ich hab grad das Login refactored", "should_trigger": true},
  {"query": "gibt es Probleme in dem was ich heute geschrieben habe? CLAUDE.md sagt wir sollen reviewen wenn 3+ Dateien betroffen sind", "should_trigger": true},
  {"query": "ich hab in /Users/me/famflow gerade 5 Dateien geändert, kannst du das reviewen gegen unsere Konventionen?", "should_trigger": true},
  {"query": "Review der letzten Änderungen mit Fokus auf Performance und N+1 Queries bitte", "should_trigger": true},
  {"query": "validiere meine Implementation gegen die Spec docs/superpowers/specs/2026-05-07-stemago-tools-v2-consolidation-design.md", "should_trigger": true},
  {"query": "kannst du nochmal prüfen ob das so passt was ich gemacht habe? Ist alles committed", "should_trigger": true},
  {"query": "ich brauch einen Quality-Check bevor ich pushe, kann was übersehen sein", "should_trigger": true},
  {"query": "review PR #142 in dem repo stemago/famflow bitte", "should_trigger": false},
  {"query": "kannst du den offenen Pull Request von Lisa zu OAuth durchgehen?", "should_trigger": false},
  {"query": "mach einen vollständigen Security-Audit der gesamten Codebase", "should_trigger": false},
  {"query": "der CI Build ist rot, kannst du schauen warum?", "should_trigger": false},
  {"query": "ich brauche ein Code Review aber für einen GitHub PR, nicht lokal", "should_trigger": false},
  {"query": "wir haben kein CLAUDE.md im Projekt, kannst du trotzdem die Code-Qualität prüfen?", "should_trigger": false},
  {"query": "lass uns über die Architektur-Entscheidung von gestern brainstormen", "should_trigger": false},
  {"query": "schreib bitte Tests für die neue parseInvoice-Funktion", "should_trigger": false},
  {"query": "kannst du den Diff zwischen branch foo und main zeigen?", "should_trigger": false},
  {"query": "git status bitte und dann commit was offen ist", "should_trigger": false}
]
```

- [ ] **Step 6: Eval-Sets dem User zur Sichtung geben**

Zeige dem User die drei Pfade:
- `docs/superpowers/specs/skill-eval-workspace/setup-eval.json`
- `docs/superpowers/specs/skill-eval-workspace/reflect-config-eval.json`
- `docs/superpowers/specs/skill-eval-workspace/review-eval.json`

Optional: HTML-Reviewer öffnen (siehe skill-creator `assets/eval_review.html`). Wenn der User einfache Inline-Review bevorzugt, frage nach Anpassungen direkt.

**Halte hier an** und warte auf User-Approval (oder Edits) der Eval-Sets bevor Step 7 läuft.

- [ ] **Step 7: run_loop für `setup` starten (Background)**

```bash
SKILL_CREATOR_DIR=$(dirname $(ls ~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/run_loop.py | head -1))/..
cd "$SKILL_CREATOR_DIR" && nohup python -m scripts.run_loop \
  --eval-set /Users/schne1s/Projekte/stemago-toolkit/docs/superpowers/specs/skill-eval-workspace/setup-eval.json \
  --skill-path /Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools/skills/setup \
  --model claude-opus-4-7 \
  --max-iterations 5 \
  --verbose > /tmp/setup-optimization.log 2>&1 &
echo "Started: PID $!"
```

Schicke periodisch ein `tail -20 /tmp/setup-optimization.log`, damit der User Fortschritt sieht.

- [ ] **Step 8: run_loop für `reflect-config` starten**

```bash
SKILL_CREATOR_DIR=$(dirname $(ls ~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/run_loop.py | head -1))/..
cd "$SKILL_CREATOR_DIR" && nohup python -m scripts.run_loop \
  --eval-set /Users/schne1s/Projekte/stemago-toolkit/docs/superpowers/specs/skill-eval-workspace/reflect-config-eval.json \
  --skill-path /Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools/skills/reflect-config \
  --model claude-opus-4-7 \
  --max-iterations 5 \
  --verbose > /tmp/reflect-config-optimization.log 2>&1 &
echo "Started: PID $!"
```

- [ ] **Step 9: run_loop für `review` starten**

```bash
SKILL_CREATOR_DIR=$(dirname $(ls ~/.claude/plugins/cache/claude-plugins-official/skill-creator/*/skills/skill-creator/scripts/run_loop.py | head -1))/..
cd "$SKILL_CREATOR_DIR" && nohup python -m scripts.run_loop \
  --eval-set /Users/schne1s/Projekte/stemago-toolkit/docs/superpowers/specs/skill-eval-workspace/review-eval.json \
  --skill-path /Users/schne1s/Projekte/stemago-toolkit/plugins/stemago-tools/skills/review \
  --model claude-opus-4-7 \
  --max-iterations 5 \
  --verbose > /tmp/review-optimization.log 2>&1 &
echo "Started: PID $!"
```

- [ ] **Step 10: Auf Abschluss warten und Best Description einsetzen**

Wenn alle drei Loops fertig sind (Reports per HTML im Browser sichtbar), prüfe in jedem Skill-Verzeichnis ob das `run_loop` die `description` im SKILL.md bereits ersetzt hat. Falls die JSON-Ergebnisse separat sind, lese `best_description` aus dem Output-JSON und ersetze die `description:` Zeile manuell im SKILL.md.

Verifikation:

```bash
grep -E "^description:" plugins/stemago-tools/skills/setup/SKILL.md
grep -E "^description:" plugins/stemago-tools/skills/reflect-config/SKILL.md
grep -E "^description:" plugins/stemago-tools/skills/review/SKILL.md
```

Erwartet: jede Zeile zeigt eine optimierte `description`, Test-Score ≥ 80% laut Report.

- [ ] **Step 11: Optimierte Descriptions committen**

```bash
git add plugins/stemago-tools/skills/setup/SKILL.md plugins/stemago-tools/skills/reflect-config/SKILL.md plugins/stemago-tools/skills/review/SKILL.md docs/superpowers/specs/skill-eval-workspace/
git commit -m "feat(skills): optimize descriptions via skill-creator run_loop

Test scores after 5-iteration optimization:
- setup: <score>%
- reflect-config: <score>%
- review: <score>%"
```

---

## Task 6: Hooks anpassen

**Files:**
- Modify: `plugins/stemago-tools/hooks/scripts/session-reflect.sh:line-with-reflect-off`
- Modify: `plugins/stemago-tools/hooks/scripts/session-review-reminder.sh:line-with-init-project`

- [ ] **Step 1: session-reflect.sh anpassen**

Ersetze in `plugins/stemago-tools/hooks/scripts/session-reflect.sh` die Zeile

```
║ Deaktivieren: /reflect-off                               ║
```

durch

```
║ Deaktivieren: /reflect-config --off                      ║
```

(Box-Breite gleich halten — bei Bedarf Spaces anpassen.)

- [ ] **Step 2: session-review-reminder.sh anpassen**

Ersetze in `plugins/stemago-tools/hooks/scripts/session-review-reminder.sh` die Zeile

```
║ → /stemago-tools:init-project                            ║
```

durch

```
║ → /stemago-tools:setup --project                         ║
```

(Box-Breite anpassen.)

- [ ] **Step 3: Verifizieren — keine alten Skill-Namen mehr**

```bash
grep -rE "init-project|beads-setup|mcp-setup|reflect-on|reflect-off|reflect-status" plugins/stemago-tools/hooks/ plugins/stemago-tools/agents/
```

Erwartet: leere Ausgabe.

- [ ] **Step 4: Hook-Skripte syntaktisch prüfen**

```bash
bash -n plugins/stemago-tools/hooks/scripts/session-reflect.sh
bash -n plugins/stemago-tools/hooks/scripts/session-review-reminder.sh
```

Erwartet: kein Output (keine Syntax-Fehler).

- [ ] **Step 5: Commit**

```bash
git add plugins/stemago-tools/hooks/scripts/session-reflect.sh plugins/stemago-tools/hooks/scripts/session-review-reminder.sh
git commit -m "fix(hooks): point to consolidated skill names (setup, reflect-config)"
```

---

## Task 7: Alte Skill-Verzeichnisse entfernen

**Files (delete):**
- `plugins/stemago-tools/skills/init-project/`
- `plugins/stemago-tools/skills/beads-setup/`
- `plugins/stemago-tools/skills/mcp-setup/`
- `plugins/stemago-tools/skills/reflect-on/`
- `plugins/stemago-tools/skills/reflect-off/`
- `plugins/stemago-tools/skills/reflect-status/`

- [ ] **Step 1: Pre-Check (keine externen Referenzen)**

```bash
grep -rE "init-project|beads-setup|mcp-setup|reflect-on|reflect-off|reflect-status" plugins/stemago-tools/ docs/ CLAUDE.md README.md AGENTS.md 2>/dev/null | grep -v "skills/init-project/SKILL.md\|skills/beads-setup/SKILL.md\|skills/mcp-setup/SKILL.md\|skills/reflect-on/SKILL.md\|skills/reflect-off/SKILL.md\|skills/reflect-status/SKILL.md\|CHANGELOG.md\|specs/2026-05-07\|plans/2026-05-07"
```

Erwartet: leer (alle Referenzen entweder Spec/Plan/CHANGELOG oder die zu löschenden Skill-Bodies selbst).

- [ ] **Step 2: Verzeichnisse mit `git rm -r` entfernen**

```bash
git rm -r plugins/stemago-tools/skills/init-project plugins/stemago-tools/skills/beads-setup plugins/stemago-tools/skills/mcp-setup plugins/stemago-tools/skills/reflect-on plugins/stemago-tools/skills/reflect-off plugins/stemago-tools/skills/reflect-status
```

- [ ] **Step 3: Skill-Liste verifizieren**

```bash
ls plugins/stemago-tools/skills/
```

Erwartet: 11 Verzeichnisse: `beads-ready  browser-test  db-inspect  docs-lookup  github-ops  interview  land-the-plane  reflect  reflect-config  review  setup`.

- [ ] **Step 4: Commit**

```bash
git commit -m "feat(skills)!: remove deprecated skills replaced by setup/reflect-config

BREAKING CHANGE: removed skills consolidated in v2.0.0
- init-project → /setup --project
- beads-setup → /setup --beads
- mcp-setup → /setup --mcp
- reflect-on → /reflect-config --on
- reflect-off → /reflect-config --off
- reflect-status → /reflect-config --status (or default)"
```

---

## Task 8: CHANGELOG.md anlegen

**Files:**
- Create: `CHANGELOG.md`

- [ ] **Step 1: CHANGELOG.md schreiben**

Schreibe `CHANGELOG.md` im Repo-Root:

```markdown
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

### Removed
- Skills `init-project`, `beads-setup`, `mcp-setup`, `reflect-on`, `reflect-off`, `reflect-status` (siehe Migration oben).

### Migration
1. Eigene Skripte/Aliases aktualisieren: alte Skill-Namen durch neue Befehle ersetzen.
2. Plugin-Cache aktualisieren: `cd ~/.claude/plugins/marketplaces/stemago-toolkit && git pull`.
3. Plugin-Update: `claude plugin update stemago-tools@stemago-toolkit` oder `/plugin marketplace update stemago-toolkit`.

## 1.5.0
Vorgängerversion (siehe Git-Historie für Details).
```

- [ ] **Step 2: Verifizieren**

```bash
head -30 CHANGELOG.md
```

Erwartet: Header und Migration-Tabelle sichtbar.

---

## Task 9: README erweitern

**Files:**
- Modify: `README.md` (neuer Abschnitt am Ende)

- [ ] **Step 1: Aktuellen README-Stand prüfen**

```bash
grep -n "^##" README.md
```

Notiere bestehende Abschnitte. Der neue Abschnitt kommt vor "## Lizenz" / "## License" (falls vorhanden), sonst am Ende.

- [ ] **Step 2: Abschnitt anhängen**

Füge folgenden Abschnitt in README.md ein (vor Lizenz, sonst am Ende):

```markdown
## Skills nach Projektphase

Die 11 Skills decken unterschiedliche Phasen ab. In eingerichteten Projekten lassen sich die Setup-Skills bei Bedarf via `/skills` deaktivieren, um die Liste übersichtlich zu halten.

### Onboarding (neue Projekte)
- `setup` — CLAUDE.md, Beads und MCPs einrichten (Args: `--project --beads --mcp --all`)
- `interview` — Feature-Anforderungen klären, Spec erstellen
- `beads-ready` — Einstieg in offene Tasks

### Aktive Entwicklung
- `docs-lookup` — aktuelle Library-Dokumentation
- `browser-test` — UI im Browser validieren
- `db-inspect` — Datenbank inspizieren
- `github-ops` — PRs, Issues, Branches
- `review` — Code Review der lokalen Änderungen
- `reflect` — Learnings aus der Session extrahieren
- `land-the-plane` — Session-Handoff erzeugen

### Operativ / optional
- `reflect-config` — Auto-Reflect aktivieren/deaktivieren/Status

### Empfehlung
In matured projects (Setup steht, MCPs konfiguriert): `setup` und `reflect-config` per `/skills disable` ausblenden, bis sie wieder gebraucht werden.
```

- [ ] **Step 3: Verifizieren**

```bash
grep -A2 "Skills nach Projektphase" README.md | head -5
```

Erwartet: Überschrift mit Intro-Zeile.

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md README.md
git commit -m "docs: add CHANGELOG.md for v2.0.0 and Skills-by-Phase section in README"
```

---

## Task 10: Versions-Bump auf 2.0.0

**Files:**
- Modify: `plugins/stemago-tools/.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `CLAUDE.md`

Drei-Datei-Sync (laut Memory-Hinweis kritisch).

- [ ] **Step 1: plugin.json bumpen**

Ersetze in `plugins/stemago-tools/.claude-plugin/plugin.json` die Zeile

```json
"version": "1.5.0",
```

durch

```json
"version": "2.0.0",
```

- [ ] **Step 2: marketplace.json bumpen (zwei Stellen)**

In `.claude-plugin/marketplace.json` ersetze BEIDE Vorkommen von `"version": "1.5.0"` durch `"version": "2.0.0"` — `metadata.version` UND `plugins[0].version`. Verifiziere mit:

```bash
grep -n '"version"' .claude-plugin/marketplace.json
```

Erwartet: zwei Zeilen, beide zeigen `"2.0.0"`.

- [ ] **Step 3: CLAUDE.md Overview-Zeile bumpen**

Ersetze in `CLAUDE.md` die Zeile

```
**stemago-toolkit** is a Claude Code plugin providing development workflows, specialized agents, and safety hooks. Version 1.5.0.
```

durch

```
**stemago-toolkit** is a Claude Code plugin providing development workflows, specialized agents, and safety hooks. Version 2.0.0.
```

- [ ] **Step 4: Sync verifizieren**

```bash
grep -E "1\.5\.0|2\.0\.0" plugins/stemago-tools/.claude-plugin/plugin.json .claude-plugin/marketplace.json CLAUDE.md
```

Erwartet: nur `2.0.0`-Treffer, kein `1.5.0` mehr.

- [ ] **Step 5: Commit**

```bash
git add plugins/stemago-tools/.claude-plugin/plugin.json .claude-plugin/marketplace.json CLAUDE.md
git commit -m "chore: bump version to 2.0.0 (breaking — skill consolidation)

Synchronized version bump across:
- plugins/stemago-tools/.claude-plugin/plugin.json
- .claude-plugin/marketplace.json (metadata + plugins[0])
- CLAUDE.md (overview line)"
```

---

## Task 11: Plugin lokal verifizieren

- [ ] **Step 1: Skill-Liste über CLI prüfen**

```bash
claude --plugin-dir ./plugins/stemago-tools --help 2>&1 | head -5
```

(Erwartet: kein Fehler. Plugin lädt.)

Falls `claude` einen interaktiven Modus startet: stoppe nach Verifikation.

Manueller Smoke-Test (durch User):
```
claude --plugin-dir ./plugins/stemago-tools
# dann im Prompt:
/stemago-tools:
```

Erwartet im Listing: `setup`, `reflect-config`, KEINE alten Namen (init-project, beads-setup, mcp-setup, reflect-on/off/status).

- [ ] **Step 2: Frontmatter-Validierung der neuen Skills**

```bash
for skill in plugins/stemago-tools/skills/*/SKILL.md; do
  echo "=== $skill ==="
  head -5 "$skill"
done
```

Erwartet: Jede Datei hat valides YAML-Frontmatter (`---`...`---`) mit `name:` und `description:`.

- [ ] **Step 3: Hook-Skripte ausführbar?**

```bash
ls -la plugins/stemago-tools/hooks/scripts/*.sh
```

Erwartet: Execute-Bit gesetzt für alle .sh-Dateien.

---

## Task 12: Push & Marketplace-Clone aktualisieren

Laut Memory-Hinweis: Marketplace-Clone wird NICHT automatisch gepullt.

- [ ] **Step 1: Lokalen Stand prüfen**

```bash
git status
git log --oneline origin/main..HEAD
```

Erwartet: clean working tree, mehrere neue Commits seit `origin/main`.

- [ ] **Step 2: User-Bestätigung einholen**

Frage den User explizit: "Plan-Schritte sind durch. Push to `origin/main` und Marketplace-Clone-Pull jetzt durchführen?"

(Push ist remote-wirksam — laut System-Anweisung "Carefully consider reversibility" zwingend mit User-OK.)

- [ ] **Step 3: Push (nur nach OK)**

```bash
git push origin main
```

- [ ] **Step 4: Marketplace-Clone aktualisieren**

```bash
cd ~/.claude/plugins/marketplaces/stemago-toolkit && git pull && cd -
```

Erwartet: Pull zieht die neuen Commits.

- [ ] **Step 5: Plugin-Update im Claude-Cache**

Bitte den User folgenden Befehl im Claude-Code Hauptprozess auszuführen:

```
/plugin marketplace update stemago-toolkit
```

Dann Verifikation der installierten Version:

```bash
cat ~/.claude/plugins/installed_plugins.json | grep -A2 stemago-tools
```

Erwartet: Version 2.0.0 sichtbar.

---

## Erfolgskriterien (Definition of Done)

- [ ] Plugin listet exakt 11 Skills (siehe Task 7 Step 3).
- [ ] Drei optimierte Descriptions sind eingesetzt, Test-Scores dokumentiert (Task 5 Step 11).
- [ ] Hooks zeigen ausschließlich neue Skill-Namen (Task 6 Step 3).
- [ ] CHANGELOG.md vorhanden mit Migrationstabelle (Task 8).
- [ ] README.md zeigt "Skills nach Projektphase"-Abschnitt (Task 9).
- [ ] Versions-Sync auf 2.0.0 in allen drei Dateien (Task 10 Step 4).
- [ ] Push erfolgreich, Marketplace-Clone gepullt (Task 12).
- [ ] `git status` zeigt "up to date with origin/main".
