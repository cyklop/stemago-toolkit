---
name: land-the-plane
description: "Session-Ende Handoff mit Prompt für nächste Session. Verwende diesen Skill wenn der User die Session beenden, einen Handoff erstellen, oder den Stand für die nächste Session sichern will. Auch bei 'Feierabend', 'ich höre auf', 'Session beenden', 'mach einen Handoff', 'sichere den Stand', 'was muss die nächste Session wissen'."
allowed-tools: Bash(bd list *) Bash(bd ready *) Bash(bd blocked *) Bash(bd export *) Bash(git status *) Bash(git stash list *) Bash(git branch --show-current)
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
bd list --status closed --closed-after "$(date +%F)" --json
```

**2.2 Offene Tasks (ready) sammeln:**

```bash
bd ready --json
```

**2.3 Geblockte Tasks sammeln:**

```bash
bd blocked --json
```

### Schritt 3: Session-Kontext aus Konversation extrahieren

Analysiere die aktuelle Session nach:

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

Stand beim Laden des Skills (Branch, geänderte Dateien, Stashes):

```!
git branch --show-current 2>&1 || true
git status --porcelain 2>&1 || true
git stash list 2>&1 || true
```

Steht dort `[shell command execution disabled by policy]`, die drei Befehle selbst ausführen. Hat sich seitdem etwas geändert (z.B. durch Schritt 6 und 7), vor Schritt 8 `git status --short` neu abrufen.

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

### Schritt 7: Beads exportieren

```bash
bd export -o .beads/issues.jsonl   # ohne -o schreibt bd export nur nach stdout
```

### Schritt 8: Commit & Push (mit Rückfrage)

Zeige `git status --short` und frage via **AskUserQuestion**:

1. **Committen und pushen** — Stand ins Remote bringen
2. **Nur committen** — lokal sichern, nicht pushen
3. **Nichts** — Working Tree bleibt wie er ist

Bei 1 oder 2: nur die Dateien dieser Session plus `.beads/issues.jsonl` und `.beads/session-handoff.md` stagen (kein `git add -A`), Commit-Message nach der Konvention des Projekts. Bei 1 danach:

```bash
git pull --rebase
git push
git status   # muss "up to date with origin" zeigen
```

Ist ein Dolt-Remote konfiguriert (`bd dolt remote list` zeigt einen Eintrag), danach `bd dolt push`, damit auch die Beads-Datenbank im Remote landet.

Schlägt der Rebase oder Push fehl: nicht erzwingen, Fehler zeigen und im Handoff unter „Offene Fragen / Blocker" festhalten. Bei 2 oder 3 im Handoff vermerken, dass der Stand nicht gepusht ist.

### Schritt 9: Zusammenfassung anzeigen

```markdown
## Session erfolgreich gelandet!

| Metrik | Wert |
|--------|------|
| Erledigte Tasks | X |
| Ready Tasks | Y |
| Geblockte Tasks | Z |
| Git | gepusht / nur committet / uncommittet |

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
- **Uncommitted Changes**: Handoff trotzdem erstellen, in Schritt 8 klären
- **Kein Remote / kein Git-Repo**: Schritt 8 überspringen bzw. nur Commit anbieten
- **Beads nicht initialisiert**: Auf `/setup --beads` verweisen
