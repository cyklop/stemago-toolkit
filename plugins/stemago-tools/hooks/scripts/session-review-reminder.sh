#!/bin/bash
# Session Review Reminder Hook
# Erinnert am Session-Ende an ungeprüfte Änderungen
#
# Wird durch SessionEnd Hook aufgerufen

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
FILE_COUNT=$(echo "$CHANGES" | wc -l | tr -d ' ')

cat << EOF

╔══════════════════════════════════════════════════════════╗
║          Code Review Reminder                            ║
╠══════════════════════════════════════════════════════════╣
║ Es gibt $FILE_COUNT ungeprüfte Datei(en) im Workspace.
║                                                          ║
║ Beim nächsten Start:                                     ║
║ → /stemago-tools:review                                  ║
║                                                          ║
║ Für automatische Reviews in Projekten:                   ║
║ → /stemago-tools:init-project                            ║
╚══════════════════════════════════════════════════════════╝

EOF

exit 0
