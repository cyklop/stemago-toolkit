---
name: interview
description: "Strukturiertes Interview über Features und Pläne mit tiefgehenden Fragen führen. Verwende diesen Skill wenn der User ein Feature besprechen, Anforderungen klären, oder eine Spec erarbeiten will. Auch bei 'lass uns das Feature planen', 'Interview starten', 'Anforderungen klären', 'Spec erstellen', 'was genau brauchen wir', oder wenn ein neues Feature vor der Implementierung durchdacht werden soll."
argument-hint: "[feature-name]"
---

# Spec-Based Interview

Führe ein strukturiertes Interview durch, um ein tiefes Verständnis der Anforderungen zu gewinnen.

## Deine Aufgabe

### Schritt 1: Spec lesen (falls vorhanden)

Prüfe ob eine Spec-Datei existiert:
- Pfad: `docs/specs/<feature-name>.md`
- Oder als Argument übergeben: $ARGUMENTS

Falls vorhanden, lies sie und verwende sie als Ausgangspunkt für das Interview.
Falls nicht vorhanden, starte das Interview von Grund auf.

### Schritt 2: Interview führen

Verwende das **AskUserQuestion** Tool um den User zu interviewen.

**Wichtig:**
- Stelle KEINE offensichtlichen Fragen
- Gehe in die TIEFE - frage nach Edge Cases, Trade-offs, Prioritäten
- Stelle 2-4 Fragen pro Runde, dann warte auf Antworten
- Fahre fort bis du ein vollständiges Bild hast

**Themengebiete für Fragen:**

1. **Scope & Ziele**
   - Was genau soll erreicht werden?
   - Was ist NICHT Teil des Scopes?
   - Welche Probleme werden gelöst?

2. **Technische Implementierung**
   - Welche bestehenden Patterns sollen verwendet werden?
   - Gibt es Performance-Anforderungen?
   - Wie soll mit Fehlern umgegangen werden?

3. **UI/UX Concerns**
   - Wie soll die Interaktion aussehen?
   - Mobile vs Desktop Priorität?
   - Accessibility-Anforderungen?

4. **Trade-offs & Prioritäten**
   - Zeit vs Qualität vs Features?
   - Was kann später kommen?
   - Was ist "must have" vs "nice to have"?

5. **Edge Cases**
   - Was passiert bei leeren Daten?
   - Wie mit Concurrent Access umgehen?
   - Rollback-Strategien?

6. **Integration**
   - Welche bestehenden Systeme sind betroffen?
   - API-Änderungen nötig?
   - Datenbankmigrationen?

### Nach jeder Fragerunde: Nächste Aktion wählen

Verwende **AskUserQuestion** mit folgenden Optionen:

1. **Vertiefen** - Weitere Fragen zu diesem Thema stellen
2. **Neues Thema** - Zum nächsten Themengebiet wechseln
3. **Spec speichern** - Erkenntnisse in Spec-Datei schreiben
4. **Tasks generieren** - Spec speichern und Beads-Tasks erstellen

### Schritt 3: Spec schreiben

Nachdem das Interview abgeschlossen ist, schreibe die Erkenntnisse in `docs/specs/<feature-name>.md`:

```markdown
# Feature Specification: [Name]

## Übersicht
[Kurze Beschreibung]

## Ziele
- [Ziel 1]
- [Ziel 2]

## Scope
### Inkludiert
- ...

### Exkludiert
- ...

## Technische Anforderungen
- ...

## UI/UX Anforderungen
- ...

## Edge Cases & Error Handling
- ...

## Offene Fragen
- ...

## Nächste Schritte
1. ...
```

### Schritt 4: Beads-Integration für Task-Generierung

Falls der User "Tasks generieren" wählt:

1. **Spec analysieren** und Tasks identifizieren
2. **Tasks erstellen** via `mcp__beads__create`:
   ```javascript
   // Für jeden identifizierten Task:
   mcp__beads__create({
     title: "Task-Titel",
     description: "Detaillierte Beschreibung",
     issue_type: "task", // oder "feature", "bug"
     priority: 2,
     labels: ["from-interview", "<feature-name>"]
   });
   ```

3. **Dependencies verknüpfen** via `mcp__beads__dep`:
   ```javascript
   // Wenn Task B von Task A abhängt:
   mcp__beads__dep({
     issue_id: "task-b-id",
     depends_on_id: "task-a-id",
     dep_type: "blocks"
   });
   ```

4. **Zusammenfassung zeigen**:
   - Anzahl erstellter Tasks
   - Dependency-Graph
   - Nächster empfohlener Schritt

### Schritt 5: Nächste Schritte

Zeige dem User eine Zusammenfassung:
- Spec-Datei Pfad: `docs/specs/<feature-name>.md`
- Anzahl erstellter Tasks mit Dependency-Graph

Dann verwende **AskUserQuestion** mit folgenden Optionen:

1. **Tasks parallel ausführen** - Task-Orchestrator startet parallele Bearbeitung durch spezialisierte Agents
2. **Ready Queue anzeigen** - Verfügbare Tasks ohne Blocker anzeigen
3. **Ersten Task manuell starten** - Details des ersten Tasks anzeigen und selbst bearbeiten
4. **Fertig** - Tasks für später aufheben

### Schritt 6: Ausführung basierend auf Auswahl

**Falls "Tasks parallel ausführen":**

Starte den Task-Orchestrator für parallele Koordination:

```
Task(
  subagent_type="task-orchestrator",
  prompt="Analysiere die Beads Task-Queue für Feature '<feature-name>'.
    Spec: docs/specs/<feature-name>.md
    Labels: from-interview, <feature-name>

    1. Nutze mcp__beads__ready um Tasks ohne Blocker zu finden
    2. Analysiere Dependencies für Parallelisierung
    3. Deploye spezialisierte Agents (component, feature, infrastructure)
    4. Koordiniere TDD-basierte Implementierung"
)
```

Bestätige dem User:
- Orchestrator gestartet
- Fortschritt mit `bd list` oder `bd stats` verfolgbar

**Falls "Ready Queue anzeigen":**
Führe `mcp__beads__ready` aus und zeige die Ergebnisse.

**Falls "Ersten Task manuell starten":**
Zeige den ersten Task mit `mcp__beads__show <first-ready-task-id>` und starte die Bearbeitung.

**Falls "Fertig":**
Bestätige dass Spec und Tasks gespeichert sind.

### Nächste Schritte nach der Implementierung

Weise den User auf diese weiterführenden Skills hin:

- `/review` — Code Review der Änderungen (Security, Performance, Qualität)
- `/reflect` — Session-Learnings extrahieren und speichern
- `/land-the-plane` — Session-Handoff für die nächste Session erstellen

$ARGUMENTS
