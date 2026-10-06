# stemago-toolkit

Claude Code development toolkit with MCP wrappers, specialized agents, and safety hooks.

## Nach der Installation

```bash
/stemago-tools:setup --mcp
```

Prüft welche empfohlenen MCP Server konfiguriert sind und installiert fehlende interaktiv. Für komplette Erst-Einrichtung (CLAUDE.md + Beads + MCPs): `/stemago-tools:setup --all`.

## Installation

### Add Marketplace (once)
```bash
/plugin marketplace add github:USER/stemago-toolkit
```

### Install Plugin
```bash
/plugin install stemago-tools@stemago-toolkit
```

### Or Install Directly from GitHub
```bash
/plugin install github:USER/stemago-toolkit
```

## Features

### Skills (22)

| Skill | Description | Usage |
|-------|-------------|-------|
| `setup` | Projekt-Initialisierung: CLAUDE.md, Beads, MCPs (konsolidiert) | `/stemago-tools:setup [--project\|--beads\|--mcp\|--all]` |
| `reflect-config` | Auto-Reflection ein/aus + Status (konsolidiert) | `/stemago-tools:reflect-config [--on\|--off\|--status]` |
| `db-inspect` | MariaDB MCP wrapper for database inspection | `/stemago-tools:db-inspect` |
| `browser-test` | Chrome DevTools MCP for UI testing | `/stemago-tools:browser-test` |
| `docs-lookup` | Context7 MCP for documentation lookup | `/stemago-tools:docs-lookup` |
| `github-ops` | GitHub operations via `gh` CLI (PRs, issues, reviews, CI) | `/stemago-tools:github-ops` |
| `interview` | Structured feature/plan interviews | `/stemago-tools:interview` |
| `reflect` | Session learning extractor → Claude Code Memory (manuell) | `/stemago-tools:reflect` |
| `review` | Code Review der lokalen Änderungen gegen CLAUDE.md | `/stemago-tools:review` |
| `beads-ready` | Tasks ohne Blocker anzeigen (Ready Queue) | `/stemago-tools:beads-ready` |
| `land-the-plane` | Session-Ende Handoff mit Prompt generieren | `/stemago-tools:land-the-plane` |
| `grill-me` | Schonungsloses Interview mit Checkpoint-Datei in `brainstorms/` | `/stemago-tools:grill-me` |
| `to-beads` | Plan oder Spec direkt in Beads-Tasks zerlegen | `/stemago-tools:to-beads [spec-pfad]` |
| `roast` | Idee vom Fünfer-Council zerlegen lassen: GO / RESHAPE / KILL | `/stemago-tools:roast [idee]` |
| `storm-research` | Mehrperspektivische, quellenverifizierte Recherche als HTML-Briefing | `/stemago-tools:storm-research [thema]` |
| `diagnose` | Strukturiertes Debugging, Feedback-Loop zuerst | `/stemago-tools:diagnose [bug]` |
| `prototype` | Wegwerf-Code, der eine Design-Frage beantwortet | `/stemago-tools:prototype [frage]` |
| `architecture-review` | Deep-Modules-Check: Reibungspunkte und Vertiefungs-Kandidaten | `/stemago-tools:architecture-review [pfad]` |
| `zoom-out` | Karte eines Codebereichs: Module, Caller, Dependencies, Grenzen | `/stemago-tools:zoom-out` |
| `usage-report` | Nutzungsauswertung von Skills, Agents und Modellen | `/stemago-tools:usage-report [--months n]` |
| `caveman` | Ultra-komprimierter Antwortmodus zum Token-Sparen | `/stemago-tools:caveman` |
| `redesign-studio` | Website-Redesign: Interview, Recherche, N Mockups, Auswahl, Folgeseiten, Handoff | `/stemago-tools:redesign-studio [url-oder-repo]` |

### Skills nach Projektphase

In eingerichteten Projekten lassen sich Setup-/Operativ-Skills bei Bedarf via `/skills` deaktivieren, um die Liste übersichtlich zu halten.

**Onboarding (neue Projekte)**
- `setup` — CLAUDE.md, Beads und MCPs einrichten
- `interview` — Feature-Anforderungen klären, Spec erstellen
- `beads-ready` — Einstieg in offene Tasks

**Aktive Entwicklung**
- `docs-lookup`, `browser-test`, `db-inspect` — MCP-Wrapper
- `github-ops` — GitHub über `gh` CLI
- `review` — Code Review der lokalen Änderungen
- `reflect` — Learnings aus der Session ins Memory von Claude Code sichern
- `land-the-plane` — Session-Handoff erzeugen

**Operativ / optional**
- `reflect-config` — Auto-Reflect aktivieren/deaktivieren/Status

### Agents (9)

#### Task Management (Beads-powered)
- `task-orchestrator` - Plans Beads task execution, routes tasks to implementation agents and gates completion

#### Development
- `research-agent` - Technical research using Context7
- `devops-agent` - Deployment, CI/CD, infrastructure
- `quality-agent` - Code review, accessibility, security

#### Implementation
- `functional-testing-agent` - Browser testing with Playwright
- `feature-implementation-agent` - Business logic and data services
- `component-implementation-agent` - UI components and styling
- `infrastructure-implementation-agent` - Build systems and tooling

#### Quality Gates
- `tdd-validation-agent` - Runs tests and build, returns PASS/FAIL with remediation items

### Hooks (4)

| Hook | Event | Description |
|------|-------|-------------|
| `block-destructive-commands` | PreToolUse | Prevents dangerous git/system commands (whitelists `git rm`) |
| `session-land-the-plane` | SessionStart | Beads session handoff reminder |
| `session-reflect` | SessionStart | Reminder to run /reflect at session end (if enabled) |
| `session-review-reminder` | SessionStart | Reminder for uncommitted changes |

## Structure

```
stemago-toolkit/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog
├── plugins/
│   └── stemago-tools/            # Main plugin
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── skills/               # 22 Skills (je SKILL.md)
│       │   ├── architecture-review/
│       │   ├── beads-ready/
│       │   ├── browser-test/
│       │   ├── caveman/
│       │   ├── db-inspect/
│       │   ├── diagnose/
│       │   ├── docs-lookup/
│       │   ├── github-ops/
│       │   ├── grill-me/
│       │   ├── interview/
│       │   ├── land-the-plane/
│       │   ├── prototype/
│       │   ├── redesign-studio/
│       │   ├── reflect/
│       │   ├── reflect-config/
│       │   ├── review/
│       │   ├── roast/
│       │   ├── setup/
│       │   ├── storm-research/
│       │   ├── to-beads/
│       │   ├── usage-report/
│       │   └── zoom-out/
│       ├── agents/               # 9 Agents
│       │   ├── task-orchestrator.md
│       │   ├── research-agent.md
│       │   ├── devops-agent.md
│       │   ├── quality-agent.md
│       │   ├── functional-testing-agent.md
│       │   ├── feature-implementation-agent.md
│       │   ├── component-implementation-agent.md
│       │   ├── infrastructure-implementation-agent.md
│       │   └── tdd-validation-agent.md
│       └── hooks/
│           ├── hooks.json        # Hook configuration
│           └── scripts/
│               ├── block-destructive-commands.sh
│               ├── session-land-the-plane.sh
│               ├── session-reflect.sh
│               └── session-review-reminder.sh
├── CHANGELOG.md
└── README.md
```

## Local Testing

```bash
# Test plugin directly
claude --plugin-dir ./plugins/stemago-tools

# Verify skills appear
/
# (should show stemago-tools: skills in the list)

# Test a skill
/stemago-tools:db-inspect
```

## Requirements

- Claude Code v2.1.7+
- MCP servers configured for MCP wrapper skills (use `/stemago-tools:setup --mcp` to install)

## Beads Setup (Agent Memory)

Beads gibt AI-Agenten ein Session-übergreifendes Gedächtnis. Setup mit `/stemago-tools:setup --beads` oder manuell:

### Schnellstart

```bash
# 1. bd CLI installieren (wähle eine Option)
npm install -g @beads/bd          # npm (empfohlen)
brew install beads                 # Homebrew (macOS)
go install github.com/steveyegge/beads/cmd/bd@latest  # Go

# 2. MCP Server installieren (wähle eine Option)
uv tool install beads-mcp          # uv (empfohlen)
pip install beads-mcp              # pip
pipx install beads-mcp             # pipx

# 3. MCP konfigurieren
claude mcp add beads -- beads-mcp

# 4. Claude Code neu starten

# 5. In einem Projekt initialisieren
bd init                            # Normal (committed)
bd init --stealth                  # Stealth (lokal)
```

### Oder automatisch

```bash
/stemago-tools:setup --beads
```

Der Skill prüft und installiert fehlende Komponenten interaktiv.

### Beads Workflow

```
Session Start → /beads-ready (was ist zu tun?)
     ↓
Arbeiten → bd create/update für Tasks
     ↓
Session Ende → /land-the-plane (Handoff generieren)
```

## Migration v1.x → v2.0

Siehe [CHANGELOG.md](CHANGELOG.md) für die vollständige Migration. Kurzform:

| Alt | Neu |
|-----|-----|
| `/init-project` | `/setup --project` |
| `/beads-setup` | `/setup --beads` |
| `/mcp-setup` | `/setup --mcp` |
| `/reflect-on` | `/reflect-config --on` |
| `/reflect-off` | `/reflect-config --off` |
| `/reflect-status` | `/reflect-config --status` |

## License

MIT
