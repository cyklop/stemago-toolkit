#!/bin/bash
# Session Land-the-Plane Hook
# Erinnert an Beads Handoff am Session-Ende wenn Beads initialisiert ist
#
# Wird durch SessionEnd Hook aufgerufen

# Prüfe ob Beads initialisiert ist (suche .beads/ im aktuellen oder Parent-Verzeichnis)
find_beads_dir() {
    local dir="$PWD"
    while [ "$dir" != "/" ]; do
        if [ -d "$dir/.beads" ]; then
            echo "$dir/.beads"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

BEADS_DIR=$(find_beads_dir)

# Falls kein Beads initialisiert - nichts tun
if [ -z "$BEADS_DIR" ]; then
    exit 0
fi

# Prüfe ob bd CLI verfügbar ist
if ! command -v bd &> /dev/null; then
    exit 0
fi

# Hole Ready-Tasks Anzahl (falls bd funktioniert)
READY_COUNT=$(bd ready --format=count 2>/dev/null || echo "?")

# Ausgabe für den User
cat << EOF

╔══════════════════════════════════════════════════════════╗
║           ✈️  LAND THE PLANE REMINDER                    ║
╠══════════════════════════════════════════════════════════╣
║ Beads ist aktiv in diesem Projekt.                       ║
║                                                          ║
║ Ready Tasks: $READY_COUNT                                         ║
║                                                          ║
║ Für sauberen Session-Handoff:                            ║
║ → /land-the-plane                                        ║
║                                                          ║
║ Der generierte Prompt hilft beim nächsten Session-Start. ║
╚══════════════════════════════════════════════════════════╝

EOF

exit 0
