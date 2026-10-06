---
name: github-ops
description: "GitHub Operationen - PRs, Issues, Reviews, CI-Status über die gh CLI. Verwende diesen Skill wenn der User Pull Requests erstellen oder mergen, Issues verwalten, PR-Reviews lesen oder abgeben, oder den CI-Status prüfen will. Auch bei 'erstelle einen PR', 'zeig offene Issues', 'merge den PR', 'erstelle ein Issue', 'was sagt die CI'. NICHT für das Review lokaler Änderungen — dafür /stemago-tools:review."
---

# GitHub-Operationen

Standardweg ist die `gh` CLI via Bash: sie ist authentifiziert, kennt das Repo aus dem Working Directory und braucht keinen MCP-Server.

## Vorab

```bash
gh auth status          # eingeloggt? sonst den User `! gh auth login` ausführen lassen
gh repo view --json nameWithOwner,defaultBranchRef
```

## Pull Requests

```bash
gh pr create --title "feat: ..." --body "..." [--draft] [--base main]
gh pr list --state open
gh pr view <nr> --json title,body,state,reviewDecision,statusCheckRollup
gh pr diff <nr>
gh pr checks <nr>                    # CI-Status
gh pr merge <nr> --squash            # oder --merge / --rebase
```

- Vor `gh pr create`: Branch muss gepusht sein (`git push -u origin <branch>`).
- PR-Titel folgen der Commit-Konvention des Projekts (siehe CLAUDE.md).
- `gh pr merge` und alles, was nach außen sichtbar ist (PR/Issue anlegen, kommentieren, Review abgeben), erst nach ausdrücklichem Auftrag oder Rückfrage ausführen.

## Reviews

```bash
gh pr review <nr> --approve | --request-changes | --comment --body "..."
gh api repos/{owner}/{repo}/pulls/<nr>/comments    # Inline-Review-Kommentare lesen
```

## Issues

```bash
gh issue create --title "Bug: ..." --body "..." --label bug
gh issue list --state open --label bug
gh issue view <nr> --comments
gh issue comment <nr> --body "..."
```

## Alles andere

`gh api <endpoint>` deckt die gesamte REST-API ab (`--paginate` für Listen, `--jq` zum Filtern). `{owner}` und `{repo}` werden automatisch aus dem aktuellen Repo ersetzt.

## GitHub-MCP (optional)

Ist in der Session ein GitHub-MCP-Server verbunden (`mcp__github__*`), kann er für Operationen ohne lokalen Checkout genutzt werden. Die Tool-Namen aus der Tool-Liste der Session nehmen, nicht aus dem Gedächtnis — sie haben sich zwischen den Server-Generationen geändert. Einrichtung: `/stemago-tools:setup --mcp`.

## Hinweise

- Lange Texte (PR-Body, Kommentare) per `--body-file` oder Heredoc übergeben, damit Zeilenumbrüche und Backticks erhalten bleiben.
- Rate Limits: bei Batch-Operationen `gh api rate_limit` prüfen.
