# stemago-toolkit

Claude Code development toolkit with MCP wrappers, specialized agents, and safety hooks.

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

### Skills (9)

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

### Agents (14)

#### Task Management
- `task-orchestrator` - Coordinates Task Master task execution
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

### Hooks (2)

| Hook | Event | Description |
|------|-------|-------------|
| `block-destructive-commands` | PreToolUse | Prevents dangerous git/system commands |
| `session-reflect` | SessionEnd | Automatic reflection reminder |

## Structure

```
stemago-toolkit/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog
├── plugins/
│   └── stemago-tools/            # Main plugin
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── skills/               # 9 Skills
│       │   ├── db-inspect/SKILL.md
│       │   ├── browser-test/SKILL.md
│       │   ├── docs-lookup/SKILL.md
│       │   ├── github-ops/SKILL.md
│       │   ├── interview/SKILL.md
│       │   ├── reflect/SKILL.md
│       │   ├── reflect-on/SKILL.md
│       │   ├── reflect-off/SKILL.md
│       │   └── reflect-status/SKILL.md
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
│               └── session-reflect.sh
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
- MCP servers configured for MCP wrapper skills:
  - `mariadb` for `db-inspect`
  - `chrome-devtools` for `browser-test`
  - `context7` for `docs-lookup`
  - `github` for `github-ops`

## License

MIT
