#!/bin/bash
# Session Reflect Hook
# Triggert automatische Reflection am Session-Ende wenn aktiviert
#
# Wird durch SessionStop Hook aufgerufen (wenn konfiguriert)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
STATE_DIR="$PROJECT_DIR/.claude/state"
REFLECT_FLAG="$STATE_DIR/reflect-enabled"
LAST_REFLECT="$STATE_DIR/last-reflect.json"

# Prüfe ob Auto-Reflect aktiviert ist
if [ ! -f "$REFLECT_FLAG" ]; then
    # Auto-Reflect nicht aktiv - nichts tun
    exit 0
fi

# Logge dass Auto-Reflect getriggert wurde
echo "🧠 Auto-Reflect: Session-Ende erkannt..."

# Erstelle Last-Reflect Timestamp
mkdir -p "$STATE_DIR"
cat > "$LAST_REFLECT" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "triggered_by": "session-end-hook",
  "status": "pending"
}
EOF

# Ausgabe für den User
cat << 'EOF'

╔══════════════════════════════════════════════════════════╗
║          🧠 AUTO-REFLECT GETRIGGERT                       ║
╠══════════════════════════════════════════════════════════╣
║ Auto-Reflection ist aktiviert.                           ║
║                                                          ║
║ Für manuelle Reflection in der nächsten Session:         ║
║ → Rufe /reflect auf um Learnings zu extrahieren          ║
║                                                          ║
║ 💡 Die automatische Analyse der Session-Learnings        ║
║    erfordert eine aktive Claude-Session.                 ║
║                                                          ║
║ Deaktivieren: /reflect-off                               ║
╚══════════════════════════════════════════════════════════╝

EOF

# Update Status
cat > "$LAST_REFLECT" << EOF
{
  "timestamp": "$(date -Iseconds)",
  "triggered_by": "session-end-hook",
  "status": "reminder-shown"
}
EOF

exit 0
