#!/bin/bash
# Session Review Reminder Hook
# Weist am Session-START auf uncommitted Änderungen im Workspace hin.
#
# Wird durch SessionStart Hook aufgerufen (matcher: startup, resume, clear).
# stdout wird als zusätzlicher Kontext injiziert -> knapper Klartext.

# Prüfe ob wir in einem Git-Repo sind
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    exit 0
fi

# Prüfe ob es uncommitted changes gibt
CHANGES=$(git status --porcelain 2>/dev/null)

if [ -z "$CHANGES" ]; then
    # Keine Änderungen - still beenden
    exit 0
fi

# Zähle geänderte Dateien
FILE_COUNT=$(printf '%s\n' "$CHANGES" | wc -l | tr -d ' ')

echo "[stemago-tools] $FILE_COUNT Datei(en) mit uncommitted changes im Workspace. Vor dem Commit ggf. reviewen: /stemago-tools:review."

exit 0
