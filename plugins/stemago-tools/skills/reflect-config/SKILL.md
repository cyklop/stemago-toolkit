---
name: reflect-config
description: "Auto-Reflection-Einstellung steuern: aktivieren, deaktivieren oder Status anzeigen. Verwende bei 'reflect ein/aus', 'auto-reflect aktivieren', 'wie viele Learnings habe ich', 'ist Reflect aktiv'. Args: --on / --off / --status (Default: --status). NICHT verwenden um Learnings JETZT zu extrahieren — dafür gibt es /reflect."
argument-hint: "[--on|--off|--status]"
---

# /reflect-config - Auto-Reflection steuern

Steuert die Erinnerung an `/stemago-tools:reflect` beim Session-Start. Die Learnings selbst liegen im eingebauten Memory von Claude Code (Verzeichnis im System-Prompt, Abschnitt „Memory").

## Argument-Routing

Werte `$ARGUMENTS` aus:
- Enthält `--on` → Subjob ON
- Enthält `--off` → Subjob OFF
- Sonst (inkl. `--status` oder leer) → Subjob STATUS

---

## Subjob ON (--on)

```bash
mkdir -p .claude/state
echo "enabled=$(date -Iseconds)" > .claude/state/reflect-enabled
```

Bestätigung:

```
Auto-Reflect AKTIVIERT

Der session-reflect Hook erinnert beim Session-Start (startup, resume, clear)
daran, am Ende /reflect auszuführen. /reflect selbst läuft nicht automatisch —
vor /compact oder einem Session-Wechsel manuell aufrufen.

Learnings landen im Memory von Claude Code und werden in jeder Session geladen.

Befehle:
- /stemago-tools:reflect-config --off    - Deaktivieren
- /stemago-tools:reflect-config --status - Status anzeigen
- /stemago-tools:reflect                 - Manuell auslösen
```

---

## Subjob OFF (--off)

```bash
rm -f .claude/state/reflect-enabled
```

Bestätigung:

```
Auto-Reflect DEAKTIVIERT

Die Erinnerung beim Session-Start ist ausgeschaltet.
/stemago-tools:reflect lässt sich weiterhin manuell aufrufen.
```

---

## Subjob STATUS (--status oder Default)

### Step 1: Auto-Reflect-Flag prüfen

```bash
[ -f .claude/state/reflect-enabled ] && cat .claude/state/reflect-enabled
```

### Step 2: Memory-Statistik

Lies `MEMORY.md` im Memory-Verzeichnis der Session und die Frontmatter der dort verlinkten Dateien. Zähle die Memories pro Typ (`feedback`, `project`, `user`, `reference`).

Nennt der System-Prompt kein Memory-Verzeichnis: „Auto-Memory ist in dieser Session aus" melden und die Statistik auslassen.

### Step 3: Pflege-Hinweise

- Zeiger in `MEMORY.md`, deren Datei fehlt, und Dateien ohne Zeiger
- Memories, die Dateien, Funktionen oder Flags nennen, die es im Repo nicht mehr gibt
- Alt-Bestand: existiert noch `.claude/learnings/project-learnings.md`, auf die Migration via `/stemago-tools:reflect` hinweisen

### Step 4: Status-Output

```
REFLECTION SYSTEM STATUS

Auto-Reflect: AKTIV / INAKTIV
Aktiviert am: [Datum] (wenn aktiv)

MEMORY
Ort: <Memory-Verzeichnis>
feedback:  XX
project:   XX
user:      XX
reference: XX
---
TOTAL:     XX

PFLEGE
[Hinweise aus Step 3 oder „nichts zu tun"]
```
