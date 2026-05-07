---
name: reflect-config
description: "Auto-Reflection-Einstellung steuern: aktivieren, deaktivieren oder Status anzeigen. Verwende bei 'reflect ein/aus', 'auto-reflect aktivieren', 'wie viele Learnings habe ich', 'ist Reflect aktiv'. Args: --on / --off / --status (Default: --status). NICHT verwenden um Learnings JETZT zu extrahieren — dafür gibt es /reflect."
argument-hint: "[--on|--off|--status]"
---

# /reflect-config - Auto-Reflection steuern

Konsolidierter Steuerungs-Skill für die automatische Session-Reflection. Ersetzt `reflect-on`, `reflect-off`, `reflect-status` (entfernt in v2.0.0).

Für die manuelle Extraktion von Learnings nutze `/reflect`.

## Argumente

- `--on` — Auto-Reflect aktivieren
- `--off` — Auto-Reflect deaktivieren
- `--status` — aktuellen Status + Learnings-Statistik anzeigen (Default)

## Argument-Routing

Werte `$ARGUMENTS` aus:
- Enthält `--on` → Subjob ON
- Enthält `--off` → Subjob OFF
- Sonst (inkl. `--status` oder leer) → Subjob STATUS

---

## Subjob ON (--on)

### Step 1: State-Datei erstellen

```bash
mkdir -p .claude/state
echo "enabled=$(date -Iseconds)" > .claude/state/reflect-enabled
```

### Step 2: Bestätigung

```
Auto-Reflect AKTIVIERT

Am Ende jeder Session wird automatisch analysiert:
- Korrektionen und explizite Anweisungen
- Erfolgreiche Patterns
- Implizite Präferenzen

Learnings werden gespeichert in:
   .claude/learnings/project-learnings.md

Befehle:
- /reflect-config --off    - Deaktivieren
- /reflect-config --status - Status anzeigen
- /reflect                 - Manuell auslösen
```

### Step 3: Hook-Hinweis

```
Die automatische Reflection wird durch den session-reflect Hook
am Session-Ende ausgelöst. Bei manuellen /compact oder Session-Wechsel
wird empfohlen /reflect manuell aufzurufen.
```

---

## Subjob OFF (--off)

### Step 1: State-Datei entfernen

```bash
rm -f .claude/state/reflect-enabled
```

### Step 2: Bestätigung

```
Auto-Reflect DEAKTIVIERT

Die automatische Session-Reflection ist nun ausgeschaltet.
Learnings werden nicht mehr automatisch extrahiert.

Du kannst weiterhin manuell /reflect aufrufen.

Befehle:
- /reflect-config --on    - Wieder aktivieren
- /reflect                - Manuell Learnings extrahieren
```

---

## Subjob STATUS (--status oder Default)

### Step 1: Auto-Reflect-Flag prüfen

```bash
if [ -f ".claude/state/reflect-enabled" ]; then
    cat .claude/state/reflect-enabled
fi
```

### Step 2: Learnings-Statistik

```
Read .claude/learnings/project-learnings.md
```

Zähle:
- HIGH / MEDIUM / LOW confidence Learnings
- Learnings pro Kategorie

### Step 3: Git-Historie

```bash
git log --oneline -5 -- .claude/learnings/project-learnings.md
```

### Step 4: Cleanup-Vorschläge

Identifiziere Learnings älter als 30 Tage.

### Step 5: Status-Output

```
REFLECTION SYSTEM STATUS

Auto-Reflect: AKTIV / INAKTIV
Aktiviert am: [Datum] (wenn aktiv)

LEARNINGS STATISTIK

HIGH Confidence:   XX
MEDIUM Confidence: XX
LOW Confidence:    XX
---
TOTAL:             XX

KATEGORIEN

Code Style:    X | Prisma/Database: X
Testing:       X | Git/Commits:     X
Architecture:  X | Tools/MCP:       X
UI/Components: X | API:             X

LETZTE ÄNDERUNGEN

[commit] learn: ... (vor X Tagen)

CLEANUP

X Learnings sind älter als 30 Tage. Führe /reflect aus um zu überprüfen.

Befehle:
- /reflect              - Learnings aus aktueller Session extrahieren
- /reflect-config --on  - Auto-Reflect aktivieren
- /reflect-config --off - Auto-Reflect deaktivieren
```

$ARGUMENTS
