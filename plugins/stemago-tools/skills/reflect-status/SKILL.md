---
name: reflect-status
description: "Zeige aktuellen Reflect-Status und letzte Learnings"
---

# /reflect-status - Reflection Status

Zeige den aktuellen Status des Reflection-Systems.

## Deine Aufgabe

### Schritt 1: Auto-Reflect Status prüfen

Prüfe ob Auto-Reflect aktiv ist:

```bash
if [ -f ".claude/state/reflect-enabled" ]; then
    cat .claude/state/reflect-enabled
fi
```

### Schritt 2: Learnings-Statistik

Lese die Learnings-Datei und erstelle eine Statistik:

```
Read .claude/learnings/project-learnings.md
```

Zähle:
- Anzahl HIGH confidence Learnings
- Anzahl MEDIUM confidence Learnings
- Anzahl LOW confidence Learnings
- Learnings pro Kategorie

### Schritt 3: Git-Historie

Zeige letzte Änderungen an Learnings:

```bash
git log --oneline -5 -- .claude/learnings/project-learnings.md
```

### Schritt 4: Cleanup-Vorschläge

Prüfe auf veraltete Learnings (älter als 30 Tage) und zeige Vorschläge.

### Schritt 5: Status-Output

Zeige zusammengefassten Status:

```
REFLECTION SYSTEM STATUS

Auto-Reflect: AKTIV / INAKTIV
Aktiviert am: [Datum] (wenn aktiv)

LEARNINGS STATISTIK

HIGH Confidence:   XX Learnings
MEDIUM Confidence: XX Learnings
LOW Confidence:    XX Learnings
---
TOTAL:             XX Learnings

KATEGORIEN

Code Style:      X  | Prisma/Database: X
Testing:         X  | Git/Commits:     X
Architecture:    X  | Tools/MCP:       X
UI/Components:   X  | API:             X

LETZTE ÄNDERUNGEN

[commit] learn: ... (vor X Tagen)
[commit] learn: ... (vor X Tagen)

CLEANUP VORSCHLÄGE

X Learnings sind älter als 30 Tage.
Führe /reflect aus um diese zu überprüfen.

Befehle:
- /reflect     - Learnings aus aktueller Session extrahieren
- /reflect-on  - Auto-Reflect aktivieren
- /reflect-off - Auto-Reflect deaktivieren
```

$ARGUMENTS
