---
name: skill-creator
description: Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, references, and assets.
---

# Skill Creator

Guidance for creating effective skills — modular packages that extend capabilities with specialized knowledge, workflows, and tools.

## Core Principles

### Concise is Key

The context window is shared. Only add what the model doesn't already know. Prefer concise examples over verbose explanations.

### Degrees of Freedom

Match specificity to fragility:
- **High freedom** (text instructions): Multiple valid approaches, context-dependent decisions
- **Medium freedom** (pseudocode/parameterized scripts): Preferred pattern exists, some variation OK
- **Low freedom** (specific scripts): Fragile operations, consistency critical

### Progressive Disclosure

Three-level loading to manage context:
1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — loaded when skill triggers (<5k words, <500 lines)
3. **Bundled resources** — loaded as needed (unlimited)

## Skill Anatomy

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name, description (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/      — Executable code for deterministic/repeated tasks
    ├── references/   — Docs loaded into context as needed
    └── assets/       — Files used in output (templates, icons, fonts)
```

### Frontmatter

```yaml
---
name: skill-name
description: "What it does AND when to use it. All trigger info goes here — the body only loads after triggering."
---
```

### Naming

- Lowercase, digits, hyphens only
- Under 64 characters
- Prefer short, verb-led phrases
- Namespace by tool when it improves clarity (e.g., `gh-address-comments`)

### What NOT to Include

No README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, or auxiliary docs. Only files the agent needs to do the job.

## Creation Process

### Step 1: Understand with Examples

Ask the user:
- What functionality should the skill support?
- Give concrete usage examples
- What should trigger this skill?

### Step 2: Plan Reusable Contents

For each example, identify:
1. What code gets rewritten each time → `scripts/`
2. What schemas/docs need rediscovery → `references/`
3. What boilerplate/templates are reused → `assets/`

### Step 3: Initialize

Create the skill directory under the appropriate skills path:

```bash
mkdir -p <skills-path>/<skill-name>
```

Create `SKILL.md` with frontmatter and TODO placeholders. Add resource directories only if needed.

### Step 4: Implement

- Start with reusable resources (scripts, references, assets)
- Test added scripts by running them
- Write SKILL.md body — imperative form, concise
- Reference bundled resources with clear "when to read" guidance
- Keep SKILL.md under 500 lines; split into reference files when approaching limit

#### Progressive Disclosure Patterns

**Pattern 1 — High-level guide with references:**
```markdown
## Quick start
[core example]

## Advanced
- **Feature X**: See [references/x.md](references/x.md)
```

**Pattern 2 — Domain-specific organization:**
```
skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── domain-a.md
    └── domain-b.md
```

**Pattern 3 — Conditional details:**
```markdown
## Basic usage
[inline]

**For advanced case**: See [references/advanced.md](references/advanced.md)
```

Keep references one level deep. Add table of contents for files >100 lines.

### Step 5: Validate and Review

Check:
- YAML frontmatter has `name` and `description`
- Description includes both what and when-to-use
- No extraneous files (README, CHANGELOG, etc.)
- SKILL.md under 500 lines
- All referenced files exist
- Scripts tested and working

### Step 6: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or resources
4. Test again
