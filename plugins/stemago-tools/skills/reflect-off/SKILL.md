---
name: reflect-off
description: "Deaktiviere automatische Session-Reflection"
---

# /reflect-off - Auto-Reflect deaktivieren

Deaktiviere die automatische Session-Reflection.

## Deine Aufgabe

### Schritt 1: State-Datei entfernen

Lösche die Flag-Datei:

```bash
rm -f .claude/state/reflect-enabled
```

### Schritt 2: Bestätigung

Zeige dem User:

```
Auto-Reflect DEAKTIVIERT

Die automatische Session-Reflection ist nun ausgeschaltet.
Learnings werden nicht mehr automatisch extrahiert.

Du kannst weiterhin manuell /reflect aufrufen um Learnings
aus der aktuellen Session zu extrahieren.

Befehle:
- /reflect-on  - Wieder aktivieren
- /reflect     - Manuell Learnings extrahieren
```

$ARGUMENTS
