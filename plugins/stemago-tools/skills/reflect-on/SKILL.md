---
name: reflect-on
description: "Aktiviere automatische Session-Reflection am Session-Ende"
---

# /reflect-on - Auto-Reflect aktivieren

Aktiviere die automatische Session-Reflection.

## Deine Aufgabe

### Schritt 1: State-Datei erstellen

Erstelle die Flag-Datei die signalisiert dass Auto-Reflect aktiv ist:

```bash
mkdir -p .claude/state
touch .claude/state/reflect-enabled
echo "enabled=$(date -Iseconds)" > .claude/state/reflect-enabled
```

### Schritt 2: Bestätigung

Zeige dem User:

```
Auto-Reflect AKTIVIERT

Am Ende jeder Session wird automatisch analysiert:
- Korrekturen und explizite Anweisungen
- Erfolgreiche Patterns
- Implizite Präferenzen

Learnings werden gespeichert in:
   .claude/learnings/project-learnings.md

Befehle:
- /reflect-off    - Deaktivieren
- /reflect-status - Status anzeigen
- /reflect        - Manuell auslösen
```

### Schritt 3: Hinweis zu Hooks

Informiere den User dass der Session-End Hook die Reflection auslöst:

```
Die automatische Reflection wird durch den session-reflect Hook
am Session-Ende ausgelöst. Bei manuellen /compact oder Session-Wechsel
wird empfohlen /reflect manuell aufzurufen.
```

$ARGUMENTS
