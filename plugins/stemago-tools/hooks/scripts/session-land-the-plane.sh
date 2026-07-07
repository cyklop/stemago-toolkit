#!/bin/bash
# Session Beads Reminder Hook
# Weist am Session-START auf aktive Beads-Tasks hin und erinnert an den
# Land-the-Plane-Handoff am Ende.
#
# Wird durch SessionStart Hook aufgerufen (matcher: startup, resume, clear).
# stdout eines SessionStart-Hooks wird als zusätzlicher Kontext injiziert,
# daher knapper Klartext statt ASCII-Box.

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

# Ready-Tasks robust zählen. bd 1.x kennt kein --format=count; wir zählen die
# JSON-Ausgabe. Schlägt bd fehl (z.B. DB nicht geladen), bleibt COUNT_LINE leer.
COUNT_LINE=""
READY_JSON=$(bd ready --json 2>/dev/null)
if [ -n "$READY_JSON" ]; then
    READY_COUNT=$(printf '%s' "$READY_JSON" | python3 -c 'import sys,json
try:
    d=json.load(sys.stdin)
    print(len(d) if isinstance(d,list) else len(d.get("issues",[])))
except Exception:
    pass' 2>/dev/null)
    if [ -n "$READY_COUNT" ]; then
        COUNT_LINE=" ($READY_COUNT Ready-Task(s))"
    fi
fi

# Kontext-Hinweis für das Modell/den User
echo "[stemago-tools] Beads ist in diesem Projekt aktiv${COUNT_LINE}. Ready-Queue: /stemago-tools:beads-ready. Am Session-Ende für sauberen Handoff: /stemago-tools:land-the-plane."

exit 0
