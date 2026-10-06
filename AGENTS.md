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

A session ends with the work pushed, because unpushed work is invisible to the next session and to teammates:

1. File issues for anything that still needs follow-up.
2. Run the quality gates if code changed (tests, linters, build).
3. Update issue status: close finished work, update in-progress items.
4. Push:
   ```bash
   git pull --rebase
   bd export -o .beads/issues.jsonl
   git push
   git status  # should report "up to date with origin"
   ```
5. Clean up: clear stashes, prune remote branches.
6. Hand off: leave context for the next session (`/stemago-tools:land-the-plane`).

Do the push yourself rather than leaving it to the user; if it fails, resolve the cause and retry.
