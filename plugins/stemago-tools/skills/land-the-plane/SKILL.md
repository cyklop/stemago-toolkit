---
name: land-the-plane
description: "Session-Ende Handoff mit Prompt für nächste Session"
---

# Land the Plane

Beendet die aktuelle Session sauber und generiert einen Handoff-Prompt für die nächste Session.

## Kontext

Das "Land the Plane" Pattern von Steve Yegge: Am Session-Ende wird der aktuelle Stand festgehalten und ein Prompt für die nächste Session generiert. So kann der Agent beim nächsten Start sofort produktiv weiterarbeiten.

## Workflow

### Schritt 1: Beads-Status prüfen

Prüfe ob Beads initialisiert ist:

```bash
ls .beads/ 2>/dev/null || echo "NOT_INITIALIZED"
```

Falls nicht initialisiert:

```markdown
## Beads nicht initialisiert

Führe zuerst `/beads-setup` aus, um Beads zu konfigurieren.
```

Stoppe hier.

### Schritt 2: Session-Fortschritt erfassen

**2.1 Heute erledigte Tasks sammeln:**

Nutze Beads MCP oder CLI:

```bash
bd list --status=closed --since=today --format=json
```

**2.2 Offene Tasks (ready) sammeln:**

```bash
bd ready --format=json
```

**2.3 Geblockte Tasks sammeln:**

```bash
bd blocked --format=json
```

### Schritt 3: Session-Kontext aus Konversation extrahieren

Analysiere die aktuelle Session nach:

1. **Was wurde erreicht?**
   - Implementierte Features
   - Behobene Bugs
   - Abgeschlossene Refactorings

2. **Was ist der aktuelle Stand?**
   - Welche Dateien wurden geändert?
   - Gibt es uncommitted Changes?
   - Welche Tests laufen/fehlschlagen?

3. **Was sind die nächsten Schritte?**
   - Welcher Task ist als nächstes dran?
   - Gibt es bekannte Blocker?
   - Welcher Kontext ist wichtig?

### Schritt 4: Git-Status prüfen

```bash
git status --porcelain
git stash list
git branch --show-current
```

### Schritt 5: Handoff-Prompt generieren

Erstelle einen strukturierten Prompt für die nächste Session:

```markdown
## Session-Handoff

### Erledigte Tasks
- [x] bd-xxxx - [Task-Titel]
- [x] bd-yyyy - [Task-Titel]

### Nächster Task
**bd-zzzz - [Task-Titel]** (Priorität X)

### Kontext für nächste Session
[Wichtige Informationen die der Agent wissen muss]

- Aktueller Branch: `feature/xxx`
- Letzte Änderung: [Datei/Komponente]
- Wichtig: [Kritische Info]

### Offene Fragen / Blocker
- [ ] [Falls vorhanden]

### Prompt für nächste Session
```
Fortsetzen bei: bd-zzzz [Task-Titel]
Kontext: [1-2 Sätze was bereits gemacht wurde]
Nächster Schritt: [Konkrete Aktion]
Branch: [aktueller Branch]
```
```

### Schritt 6: Handoff speichern

Speichere in `.beads/session-handoff.md`:

```bash
# Datei wird überschrieben bei jeder Session
```

### Schritt 7: Beads synchronisieren

```bash
bd sync
```

### Schritt 8: Zusammenfassung anzeigen

```markdown
## Session erfolgreich gelandet!

| Metrik | Wert |
|--------|------|
| Erledigte Tasks | X |
| Ready Tasks | Y |
| Geblockte Tasks | Z |

### Handoff gespeichert
Pfad: `.beads/session-handoff.md`

### Für nächste Session
Kopiere diesen Prompt:

---
[Generierter Prompt hier]
---

Oder starte die nächste Session mit:
```
Lies .beads/session-handoff.md und fahre fort.
```
```

## Integration mit /reflect

Dieser Skill fokussiert auf **Task-Status und Arbeitskontext**.
`/reflect` fokussiert auf **Learnings und Präferenzen**.

Beide ergänzen sich und sollten am Session-Ende ausgeführt werden:
1. `/land-the-plane` - Task-Handoff
2. `/reflect` - Learnings extrahieren

## Edge Cases

- **Keine Tasks erledigt**: Trotzdem Handoff generieren mit aktuellem Stand
- **Keine Ready Tasks**: Hinweis dass neue Tasks erstellt werden sollten
- **Uncommitted Changes**: Warnung ausgeben, Handoff trotzdem erstellen
- **Beads nicht initialisiert**: Auf `/beads-setup` verweisen

$ARGUMENTS
