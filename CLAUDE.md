# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**stemago-toolkit** is a Claude Code plugin providing development workflows, specialized agents, and safety hooks. Version 2.3.0.

## Testing the Plugin

```bash
# Run Claude with local plugin
claude --plugin-dir ./plugins/stemago-tools

# Verify skills appear (type "/" in Claude)
/stemago-tools:

# Test specific skill
/stemago-tools:beads-ready
```

## Issue Tracking with Beads

This project uses **Beads** (`bd`) for issue tracking instead of external systems.

```bash
bd ready              # Find tasks without blockers
bd show <id>          # View task details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Architecture

### Plugin Structure

```
plugins/stemago-tools/
├── .claude-plugin/plugin.json   # Plugin manifest (version, metadata)
├── skills/                      # User-invokable slash commands
│   └── <skill-name>/SKILL.md    # Skill definition (frontmatter + prompt)
├── agents/                      # Subagent definitions
│   └── <agent-name>.md          # Agent definition (frontmatter + system prompt)
└── hooks/
    ├── hooks.json               # Hook event bindings
    └── scripts/*.sh             # Hook implementations
```

### Skill Format

Skills are SKILL.md files with YAML frontmatter:
```yaml
---
name: skill-name
description: "What the skill does"
argument-hint: "[optional-args]"
---
# Prompt content follows...
```

### Agent Format

Agents are markdown files with YAML frontmatter:
```yaml
---
name: agent-name
description: When/how to use this agent
tools: tool1, tool2, mcp__server__tool
model: sonnet  # optional: sonnet, opus, haiku
color: green   # optional: terminal color
---
# System prompt content follows...
```

### Hook System

Hooks in `hooks.json` bind to events:
- **PreToolUse**: Runs before tool execution (can block)
- **SessionEnd**: Runs when session ends

Scripts receive tool context via stdin JSON and can output `{"decision": "block", "message": "..."}` to prevent execution.

## Key Workflows

### Session Start
```bash
/stemago-tools:beads-ready    # See available tasks
```

### Session End
```bash
/stemago-tools:land-the-plane # Generate handoff for next session
```

Hooks automatically remind about:
- Uncommitted changes
- Open Beads tasks
- Reflection (if enabled)

### Agent Orchestration

The task-orchestrator coordinates specialized agents:
- `infrastructure-implementation-agent` - Build systems, tooling
- `component-implementation-agent` - UI components
- `feature-implementation-agent` - Business logic
- `research-agent` - Context7 documentation lookup

All implementation agents follow TDD methodology (Red-Green-Refactor).

## File Paths Convention

- Specs: `docs/specs/<feature-name>.md`
- Research cache: `docs/research/<topic>.md`
- Beads data: `.beads/issues.jsonl`
- Domain Language: `CONTEXT.md` (Projekt-Root)
- Bug Post-Mortems: `docs/post-mortems/<datum>-<bug>.md`
- Brainstorm-Captures: `brainstorms/<datum>-<topic-slug>.md` (Projekt-Root, bewusst NICHT unter `docs/` — ein vorhersehbarer Sammelort für rohe Interview-Erfassungen aus `/grill-me` und `/interview`. Polierte Ergebnisse wandern danach in `docs/` oder `projects/`.)

## Domain Language (CONTEXT.md)

Jedes Projekt das stemago-tools nutzt, sollte eine `CONTEXT.md` im Root haben — ein lebendes Glossar für projektspezifische Begriffe.

**Format:**
```markdown
# CONTEXT.md — Domain Language

## Begriffe

### [Begriff]
[Präzise Definition in 1-2 Sätzen]
Abgrenzung zu: [verwandte Begriffe]

### [Begriff 2]
...
```

**Regeln:**
- Skills challengen vage Sprache sofort und ergänzen klare Definitionen direkt in `CONTEXT.md`
- Neue Begriffe werden inline während Interviews/Planung definiert — nicht nachträglich
- Bei Konflikten zwischen `CONTEXT.md` und Code: Code ist die Wahrheit, `CONTEXT.md` updaten
- Ein Begriff gilt als definiert sobald er in `CONTEXT.md` steht — danach challengen gilt nicht mehr

## Landing the Plane (Session Completion)

Work is NOT complete until `git push` succeeds:

```bash
git pull --rebase
bd sync
git push
git status  # Must show "up to date with origin"
```
