---
name: land-the-plane
description: "Session-Ende Handoff mit Prompt für nächste Session. Verwende diesen Skill wenn der User die Session beenden, einen Handoff erstellen, oder den Stand für die nächste Session sichern will. Auch bei 'Feierabend', 'ich höre auf', 'Session beenden', 'mach einen Handoff', 'sichere den Stand', 'was muss die nächste Session wissen'."
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

Führe zuerst `/setup --beads` aus, um Beads zu konfigurieren.
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

Falls `/recap` verfügbar ist, führe es zuerst aus — es zeigt was passiert ist während das Terminal nicht im Fokus war und ergänzt den manuellen Kontext-Extrakt:

```bash
/recap
```

Analysiere dann die aktuelle Session nach:

1. **Was wurde erreicht?**
   - Implementierte Features
   - Behobene Bugs
   - Abgeschlossene Refactorings

2. **Was ist der aktuelle Stand?**
   - Welche Dateien wurden geändert? (die weißt du aus dieser Session — nicht neu ergrep­pen)
   - Gibt es uncommitted Changes?
   - Welche Tests laufen/fehlschlagen?

3. **Was läuft noch? (Running State)**
   - Background-Prozesse, die du mit `run_in_background` gestartet hast: **Shell-IDs + was es ist + Kill-Befehl**. Diese IDs sind load-bearing — die nächste Session findet sie sonst nicht.
   - Dev-Server / offene Ports (URL + Port).
   - Offene Worktrees / Branches.

4. **Wie verifiziert man, dass es noch läuft?**
   - Konkrete Befehle + erwartetes Ergebnis (z.B. `npm test` → grün, `curl localhost:3000/health` → 200).

5. **Was sind die nächsten Schritte?**
   - Welcher Task ist als nächstes dran?
   - Gibt es bekannte Blocker oder offene Fragen (an dich oder an den User)?
   - Welcher Kontext ist wichtig?

**Adressat des Handoffs = die nächste Instanz von DIR, kein Stakeholder.** Synthetisiere, was in dieser Session passiert ist — kein `git log`, keine breiten `Glob`-Sweeps.

### Schritt 4: Git-Status prüfen

```bash
git status --porcelain
git stash list
git branch --show-current
```

### Schritt 5: Handoff-Prompt generieren

Erstelle einen strukturierten Handoff. **Struktur-Stabilität ist Pflicht:** Hat eine Sektion nichts zu melden, schreibe „keine" — lass sie nie weg. Absolute Pfade verwenden (die nächste Session kann ein anderes Working Directory haben).

```markdown
## Session-Handoff — [Ein-Zeilen-Titel worum es ging]

### Erledigte Tasks
- [x] bd-xxxx - [Task-Titel]
- [x] bd-yyyy - [Task-Titel]

### Entscheidungen & was geliefert wurde
- [Entscheidung/Änderung] — [warum, und wo es liegt (absoluter Pfad bei Dateien)]

### Nächster Task
**bd-zzzz - [Task-Titel]** (Priorität X)

### Wichtigste Dateien für die nächste Session
- `[absoluter Pfad]` — [warum zuerst lesen]
- Plan-/Spec-Datei: `[Pfad]` (falls eine Spec/ein Plan die Session getrieben hat — hier zuerst nennen)

### Running State
- Background-Prozesse: [Shell-IDs + was es ist + Kill-Befehl] — oder „keine"
- Dev-Server / Ports: [URL + Port] — oder „keine"
- Offene Worktrees / Branches: [Pfade / aktueller Branch] — oder „keine"

### Verifikation — so bestätigt man, dass alles noch läuft
- `[Befehl]` — [erwartetes Ergebnis]

### Offene Fragen / Blocker / Deferred
- Deferred: [Punkt] — [warum verschoben]
- Offen: [Frage die User-Input braucht] — [Kontext]
- oder „keine"

### Prompt für nächste Session
```
Fortsetzen bei: bd-zzzz [Task-Titel]
Kontext: [1-2 Sätze was bereits gemacht wurde]
Nächster Schritt: [die eine wahrscheinlichste Aktion]
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
- **Beads nicht initialisiert**: Auf `/setup --beads` verweisen

$ARGUMENTS
