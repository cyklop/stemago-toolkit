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

### Skills (11)

| Skill | Description | Usage |
|-------|-------------|-------|
| `setup` | Projekt-Initialisierung: CLAUDE.md, Beads, MCPs (konsolidiert) | `/stemago-tools:setup [--project\|--beads\|--mcp\|--all]` |
| `reflect-config` | Auto-Reflection ein/aus + Status (konsolidiert) | `/stemago-tools:reflect-config [--on\|--off\|--status]` |
| `db-inspect` | MariaDB MCP wrapper for database inspection | `/stemago-tools:db-inspect` |
| `browser-test` | Chrome DevTools MCP for UI testing | `/stemago-tools:browser-test` |
| `docs-lookup` | Context7 MCP for documentation lookup | `/stemago-tools:docs-lookup` |
| `github-ops` | GitHub MCP for repository operations | `/stemago-tools:github-ops` |
| `interview` | Structured feature/plan interviews | `/stemago-tools:interview` |
| `reflect` | Session learning extractor (manuell) | `/stemago-tools:reflect` |
| `review` | Code Review der lokalen Änderungen gegen CLAUDE.md | `/stemago-tools:review` |
| `beads-ready` | Tasks ohne Blocker anzeigen (Ready Queue) | `/stemago-tools:beads-ready` |
| `land-the-plane` | Session-Ende Handoff mit Prompt generieren | `/stemago-tools:land-the-plane` |

### Skills nach Projektphase

In eingerichteten Projekten lassen sich Setup-/Operativ-Skills bei Bedarf via `/skills` deaktivieren, um die Liste übersichtlich zu halten.

**Onboarding (neue Projekte)**
- `setup` — CLAUDE.md, Beads und MCPs einrichten
- `interview` — Feature-Anforderungen klären, Spec erstellen
- `beads-ready` — Einstieg in offene Tasks

**Aktive Entwicklung**
- `docs-lookup`, `browser-test`, `db-inspect`, `github-ops` — MCP-Wrapper
- `review` — Code Review der lokalen Änderungen
- `reflect` — Learnings aus der Session extrahieren
- `land-the-plane` — Session-Handoff erzeugen

**Operativ / optional**
- `reflect-config` — Auto-Reflect aktivieren/deaktivieren/Status

### Agents (14)

#### Task Management (Beads-powered)
- `task-orchestrator` - Coordinates Beads task execution
- `task-executor` - Delegates to specialized agents for implementation
- `task-checker` - Quality assurance and TDD validation

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
- `completion-gate` - Task completion validation
- `readiness-gate` - Phase advancement validation
- `enhanced-quality-gate` - Security, performance, accessibility
- `tdd-validation-agent` - TDD methodology enforcement

### Hooks (4)

| Hook | Event | Description |
|------|-------|-------------|
| `block-destructive-commands` | PreToolUse | Prevents dangerous git/system commands (whitelists `git rm`) |
| `session-land-the-plane` | SessionEnd | Beads session handoff reminder |
| `session-reflect` | SessionEnd | Automatic reflection reminder |
| `session-review-reminder` | SessionEnd | Reminder for uncommitted changes |

## Structure

```
stemago-toolkit/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog
├── plugins/
│   └── stemago-tools/            # Main plugin
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── skills/               # 11 Skills
│       │   ├── beads-ready/SKILL.md
│       │   ├── browser-test/SKILL.md
│       │   ├── db-inspect/SKILL.md
│       │   ├── docs-lookup/SKILL.md
│       │   ├── github-ops/SKILL.md
│       │   ├── interview/SKILL.md
│       │   ├── land-the-plane/SKILL.md
│       │   ├── reflect/SKILL.md
│       │   ├── reflect-config/SKILL.md
│       │   ├── review/SKILL.md
│       │   └── setup/SKILL.md
│       ├── agents/               # 14 Agents
│       │   ├── task-orchestrator.md
│       │   ├── task-executor.md
│       │   ├── task-checker.md
│       │   ├── research-agent.md
│       │   ├── devops-agent.md
│       │   ├── quality-agent.md
│       │   ├── functional-testing-agent.md
│       │   ├── feature-implementation-agent.md
│       │   ├── component-implementation-agent.md
│       │   ├── infrastructure-implementation-agent.md
│       │   ├── completion-gate.md
│       │   ├── readiness-gate.md
│       │   ├── enhanced-quality-gate.md
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
