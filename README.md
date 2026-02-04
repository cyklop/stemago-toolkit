# stemago-toolkit

Claude Code development toolkit with MCP wrappers, specialized agents, and safety hooks.

## Nach der Installation

```bash
/stemago-tools:mcp-setup
```

Prüft welche empfohlenen MCP Server konfiguriert sind und installiert fehlende interaktiv.

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

### Skills (15)

| Skill | Description | Usage |
|-------|-------------|-------|
| `db-inspect` | MariaDB MCP wrapper for database inspection | `/stemago-tools:db-inspect` |
| `browser-test` | Chrome DevTools MCP for UI testing | `/stemago-tools:browser-test` |
| `docs-lookup` | Context7 MCP for documentation lookup | `/stemago-tools:docs-lookup` |
| `github-ops` | GitHub MCP for repository operations | `/stemago-tools:github-ops` |
| `interview` | Structured feature/plan interviews | `/stemago-tools:interview` |
| `reflect` | Session learning extractor | `/stemago-tools:reflect` |
| `reflect-on` | Enable automatic reflection | `/stemago-tools:reflect-on` |
| `reflect-off` | Disable automatic reflection | `/stemago-tools:reflect-off` |
| `reflect-status` | Show reflection system status | `/stemago-tools:reflect-status` |
| `mcp-setup` | MCP Server prüfen und fehlende installieren | `/stemago-tools:mcp-setup` |
| `init-project` | Projekt-CLAUDE.md mit Workflow-Regeln initialisieren | `/stemago-tools:init-project` |
| `review` | Code Review der letzten Änderungen durchführen | `/stemago-tools:review` |
| `beads-setup` | Beads Memory-System initialisieren | `/stemago-tools:beads-setup` |
| `beads-ready` | Tasks ohne Blocker anzeigen (Ready Queue) | `/stemago-tools:beads-ready` |
| `land-the-plane` | Session-Ende Handoff mit Prompt generieren | `/stemago-tools:land-the-plane` |

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
| `block-destructive-commands` | PreToolUse | Prevents dangerous git/system commands |
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
│       ├── skills/               # 15 Skills
│       │   ├── beads-setup/SKILL.md
│       │   ├── beads-ready/SKILL.md
│       │   ├── land-the-plane/SKILL.md
│       │   ├── db-inspect/SKILL.md
│       │   ├── browser-test/SKILL.md
│       │   ├── docs-lookup/SKILL.md
│       │   ├── github-ops/SKILL.md
│       │   ├── init-project/SKILL.md
│       │   ├── mcp-setup/SKILL.md
│       │   ├── interview/SKILL.md
│       │   ├── reflect/SKILL.md
│       │   ├── reflect-on/SKILL.md
│       │   ├── reflect-off/SKILL.md
│       │   ├── reflect-status/SKILL.md
│       │   └── review/SKILL.md
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
- MCP servers configured for MCP wrapper skills (use `/mcp-setup` to install)

## Beads Setup (Agent Memory)

Beads gibt AI-Agenten ein Session-übergreifendes Gedächtnis. Setup mit `/beads-setup` oder manuell:

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
/stemago-tools:beads-setup
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

## License

MIT
