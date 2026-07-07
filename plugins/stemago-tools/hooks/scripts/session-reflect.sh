#!/bin/bash
# Session Reflect Reminder Hook
# Erinnert am Session-START daran, am Ende /reflect auszuführen — sofern
# Auto-Reflect aktiviert ist.
#
# Wird durch SessionStart Hook aufgerufen (matcher: startup, resume, clear).
# stdout wird als zusätzlicher Kontext injiziert -> knapper Klartext.
#
# Das Flag wird projektrelativ geprüft (.claude/state/reflect-enabled),
# konsistent mit dem /reflect-config Skill, der es dort anlegt.

REFLECT_FLAG=".claude/state/reflect-enabled"

# Prüfe ob Auto-Reflect aktiviert ist
if [ ! -f "$REFLECT_FLAG" ]; then
    # Auto-Reflect nicht aktiv - nichts tun
    exit 0
fi

echo "[stemago-tools] Auto-Reflect ist aktiviert. Denk am Session-Ende daran, Learnings zu sichern: /stemago-tools:reflect."

exit 0
