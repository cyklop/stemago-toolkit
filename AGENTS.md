# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd export -o .beads/issues.jsonl   # Issues als JSONL für Git schreiben (ohne -o: stdout)
```

## Landing the Plane (Session Completion)

A session should end with the work pushed, because unpushed work is invisible to the next session and to teammates:

1. File issues for anything that still needs follow-up.
2. Run the quality gates if code changed (tests, linters, build).
3. Update issue status: close finished work, update in-progress items.
4. Push, once the user has confirmed it:
   ```bash
   git pull --rebase
   bd export -o .beads/issues.jsonl
   git push
   bd dolt push   # Beads database to the Dolt remote
   git status  # should report "up to date with origin"
   ```
5. Clean up: clear stashes, prune remote branches.
6. Hand off: leave context for the next session (`/stemago-tools:land-the-plane`).

Ask before pushing (`/stemago-tools:land-the-plane` does this), then run the push yourself. If the rebase or the push fails, do not force it: report the error and note it in the handoff.
