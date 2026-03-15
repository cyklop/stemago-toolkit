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

### Schritt 3: Interview-Abschluss — Immer zwei Optionen anbieten

Nach jeder Fragerunde verwende **AskUserQuestion** mit IMMER diesen Optionen:

1. **Vertiefen** — Vertiefende Fragen stellen (zu aktuellem oder neuem Thema)
2. **Spec speichern** — Interview abschließen und Erkenntnisse als Spec-Datei sichern
3. **Spec & Tasks erstellen** — Interview abschließen, Spec schreiben UND Beads-Tasks generieren

**Wiederhole diesen Schritt** bis der User Option 2 oder 3 wählt.

Falls "Spec speichern": Weiter mit Schritt 4, dann Abschluss (Spec-Pfad zeigen, auf `/stemago-tools:beads-ready` hinweisen).
Falls "Spec & Tasks erstellen": Weiter mit Schritt 4, dann Schritt 5.

### Schritt 4: Spec schreiben

Schreibe die Erkenntnisse in `docs/specs/<feature-name>.md`:

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
```

### Schritt 5: Beads-Tasks generieren

1. **Spec analysieren** und Tasks identifizieren — zerlege in möglichst unabhängige, parallelisierbare Einheiten
2. **Tasks erstellen** via `mcp__beads__create`:
   ```javascript
   mcp__beads__create({
     title: "Task-Titel",
     description: "Detaillierte Beschreibung mit Akzeptanzkriterien",
     issue_type: "task",
     priority: 2,
     labels: ["from-interview", "<feature-name>"]
   });
   ```

3. **Dependencies verknüpfen** via `mcp__beads__dep` — nur wo echte Abhängigkeiten bestehen:
   ```javascript
   mcp__beads__dep({
     issue_id: "task-b-id",
     depends_on_id: "task-a-id",
     dep_type: "blocks"
   });
   ```

4. **Zusammenfassung zeigen**:
   - Spec-Datei Pfad
   - Anzahl erstellter Tasks
   - Dependency-Graph (welche parallel, welche sequentiell)
   - Geschätzte Parallelisierungsgruppen

### Schritt 6: Parallele Task-Bearbeitung starten

Frage den User via **AskUserQuestion**:

1. **Jetzt parallel bearbeiten** — Alle unabhängigen Tasks sofort starten
2. **Fertig** — Tasks für später aufheben

**Falls "Jetzt parallel bearbeiten":**

Starte den Task-Orchestrator für maximale Parallelisierung:

```
Agent(
  subagent_type="task-orchestrator",
  prompt="Analysiere und bearbeite die Beads Task-Queue für Feature '<feature-name>'.
    Spec: docs/specs/<feature-name>.md
    Labels: from-interview, <feature-name>

    STRATEGIE:
    1. Nutze mcp__beads__ready um alle Tasks ohne Blocker zu identifizieren
    2. Starte ALLE unabhängigen Tasks PARALLEL über spezialisierte Agents
    3. Sobald ein Task abgeschlossen ist, prüfe ob neue Tasks freigeschaltet wurden
    4. Wiederhole bis alle Tasks erledigt sind
    5. Melde den Abschluss aller Tasks zurück"
)
```

**Warte auf Abschluss des Orchestrators**, dann weiter mit Schritt 7.

**Falls "Fertig":**
Bestätige dass Spec und Tasks gespeichert sind. Weise auf `/stemago-tools:beads-ready` hin.

### Schritt 7: Review & Reflect — Abschluss-Workflow

Nachdem ALLE Tasks abgeschlossen sind, führe den Abschluss-Workflow durch:

**7a: Review anbieten**

Frage den User via **AskUserQuestion**:

> Alle Tasks sind abgeschlossen. Möchtest du ein Code Review durchführen?

1. **Review starten** — `/review` ausführen
2. **Überspringen** — Direkt zu Reflect

Falls "Review starten": Führe den `/review` Skill aus. Warte auf Abschluss.

**7b: Reflect anbieten**

Frage den User via **AskUserQuestion**:

> Möchtest du die Session-Learnings extrahieren?

1. **Reflect starten** — `/reflect` ausführen
2. **Fertig** — Session beenden

Falls "Reflect starten": Führe den `/reflect` Skill aus.

**7c: Abschluss**

Zeige eine finale Zusammenfassung:
- Spec-Datei: `docs/specs/<feature-name>.md`
- Erstellte/abgeschlossene Tasks
- Review-Ergebnis (falls durchgeführt)
- Gespeicherte Learnings (falls reflektiert)

$ARGUMENTS
