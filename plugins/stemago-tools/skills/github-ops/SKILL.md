---
name: github-ops
description: "GitHub Operationen - PRs, Issues, Branches, Commits"
---

# GitHub MCP - Repository-Operationen

Nutze den GitHub MCP Server für Repository-Operationen. Für einfache Git-Befehle bevorzuge `gh` CLI via Bash.

## Verfügbare Tools

### Repository

**`mcp__github__search_repositories`**
```
query: "match-admin in:name"
```

**`mcp__github__get_file_contents`**
```
owner: "username"
repo: "Match_Admin"
path: "src/app/page.tsx"
branch: "main"  # Optional
```

### Branches & Commits

**`mcp__github__create_branch`**
```
owner: "username"
repo: "Match_Admin"
branch: "feature/new-feature"
from_branch: "main"  # Optional
```

**`mcp__github__list_commits`**
```
owner: "username"
repo: "Match_Admin"
sha: "main"  # Branch name
```

### Pull Requests

**`mcp__github__create_pull_request`**
```
owner: "username"
repo: "Match_Admin"
title: "feat: Add new feature"
head: "feature/new-feature"
base: "main"
body: "Description..."
draft: false
```

**`mcp__github__list_pull_requests`**
```
owner: "username"
repo: "Match_Admin"
state: "open"  # oder "closed", "all"
```

**`mcp__github__get_pull_request`**
```
owner: "username"
repo: "Match_Admin"
pull_number: 123
```

**`mcp__github__merge_pull_request`**
```
owner: "username"
repo: "Match_Admin"
pull_number: 123
merge_method: "squash"  # oder "merge", "rebase"
```

### Issues

**`mcp__github__create_issue`**
```
owner: "username"
repo: "Match_Admin"
title: "Bug: Something broken"
body: "Description..."
labels: ["bug"]
```

**`mcp__github__list_issues`**
```
owner: "username"
repo: "Match_Admin"
state: "open"
labels: ["bug"]
```

**`mcp__github__add_issue_comment`**
```
owner: "username"
repo: "Match_Admin"
issue_number: 42
body: "Comment text..."
```

### Code Reviews

**`mcp__github__create_pull_request_review`**
```
owner: "username"
repo: "Match_Admin"
pull_number: 123
event: "APPROVE"  # oder "REQUEST_CHANGES", "COMMENT"
body: "Looks good!"
```

**`mcp__github__get_pull_request_files`**
Geänderte Dateien eines PRs abrufen.

**`mcp__github__get_pull_request_comments`**
Review-Kommentare abrufen.

### File Operations

**`mcp__github__push_files`**
Mehrere Dateien in einem Commit pushen.

**`mcp__github__create_or_update_file`**
Einzelne Datei erstellen/aktualisieren.

## Wann MCP vs `gh` CLI?

### MCP bevorzugen für:
- Komplexe PR-Operationen
- Issue-Management
- Code Reviews
- Batch File Operations

### `gh` CLI bevorzugen für:
- Einfache Befehle: `gh pr view`, `gh issue list`
- Interaktive Operationen
- Lokale Git-Integration

## Typische Workflows

### PR erstellen
```bash
# Via gh CLI (einfacher)
gh pr create --title "feat: ..." --body "..."

# Via MCP (wenn mehr Kontrolle nötig)
mcp__github__create_pull_request
```

### Issue mit Bug-Label
```
mcp__github__create_issue mit labels: ["bug", "priority:high"]
```

### PR-Status prüfen
```
mcp__github__get_pull_request_status
```

## Hinweise

- **Lokale Commits zuerst**: MCP kann keine lokalen Commits erstellen
- **Branch muss existieren**: Vor PR remote Branch pushen
- **Rate Limits beachten**: GitHub API hat Limits
