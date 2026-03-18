---
name: interview
description: "Strukturiertes Interview über Features und Anforderungen führen, dann Spec und Implementierungsplan erstellen. Verwende diesen Skill IMMER wenn der User: ein neues Feature planen oder besprechen will, Anforderungen klären möchte, eine Spec oder einen Plan braucht, 'was brauchen wir für X' fragt, eine grobe Feature-Idee hat die durchdacht werden soll, oder eine existierende Spec als Basis für Tasks nutzen will. Auch bei: 'lass uns das durchsprechen', 'können wir die Anforderungen klären', 'ich hab eine Idee für...', 'Interview starten', 'Feature planen', 'Spec erstellen'. NICHT verwenden für: Bug-Fixes, Code Reviews, direkte Implementierungsaufträge, oder Fragen zu bestehenden APIs/Libraries."
argument-hint: "[feature-name]"
---

# Spec-Based Interview

Führe ein strukturiertes Interview durch, um ein tiefes Verständnis der Anforderungen zu gewinnen.

## Grundprinzipien

- **YAGNI** (You Aren't Gonna Need It): Hinterfrage aktiv jede Anforderung — brauchen wir das wirklich JETZT? Filtere Feature-Creep heraus. Wenn der User "und vielleicht noch X" sagt, frage: "Ist X für den ersten Release nötig, oder kann das später kommen?"
- Stelle KEINE offensichtlichen Fragen
- Gehe in die TIEFE — frage nach Edge Cases, Trade-offs, Prioritäten

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
- Stelle 2-4 Fragen pro Runde, dann warte auf Antworten
- Wende das YAGNI-Prinzip aktiv an: Challenge Anforderungen die nach Overengineering klingen
- Fahre fort bis du ein vollständiges Bild hast

**Scope-Check:** Falls das Feature mehrere unabhängige Subsysteme umfasst, schlage vor es in separate Specs aufzuteilen. Jede Spec sollte eigenständig testbare Software produzieren.

**Themengebiete für Fragen:**

1. **Scope & Ziele**
   - Was genau soll erreicht werden?
   - Was ist NICHT Teil des Scopes?
   - Welche Probleme werden gelöst?

2. **Technische Implementierung** (mit Docs-Recherche)
   - Welche bestehenden Patterns sollen verwendet werden?
   - Gibt es Performance-Anforderungen?
   - Wie soll mit Fehlern umgegangen werden?
   - **Docs-Check**: Sobald Libraries/Frameworks genannt werden, starte parallel einen Research-Agent (haiku) um aktuelle Best Practices und API-Änderungen zu recherchieren:
     ```
     Agent(
       subagent_type="research-agent",
       model="haiku",
       description="Docs für <library>",
       prompt="Recherchiere aktuelle Dokumentation für <library> via Context7.
         Fokus: aktuelle API, Breaking Changes, empfohlene Patterns.
         Kurze Zusammenfassung der relevanten Findings."
     )
     ```
   - Fließe die Recherche-Ergebnisse in die Fragen ein (z.B. "Wisst ihr, dass X seit v15 deprecated ist?")

3. **UI/UX Concerns**
   - Wie soll die Interaktion aussehen?
   - Mobile vs Desktop Priorität?
   - Accessibility-Anforderungen?
   - **Visual Companion**: Wenn UI/UX-Themen besprochen werden, biete an Mockups oder Diagramme zu generieren:
     ```
     Skill(skill="generate-image", args="<Beschreibung des UI-Mockups/Diagramms>")
     ```
     Nutze dies für: Wireframes, Layout-Varianten, Flowcharts, Architektur-Diagramme.
     Generiere Visuals proaktiv wenn sie die Diskussion voranbringen.

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

### Schritt 2b: Lösungsansätze vorschlagen

Sobald genug Kontext für eine fundierte Einschätzung gesammelt wurde (typisch nach 2-3 Fragerunden), schlage **2-3 Lösungsansätze** vor:

- Jeder Ansatz mit kurzer Beschreibung (2-3 Sätze)
- **Trade-offs** pro Ansatz: Was gewinnt man, was verliert man?
- **Empfehlung**: Welchen Ansatz empfiehlst du und warum?
- Berücksichtige YAGNI: Der einfachste Ansatz der die Anforderungen erfüllt ist oft der beste

Frage den User via **AskUserQuestion** welchen Ansatz er bevorzugt, oder ob ein Hybrid-Ansatz gewünscht ist.

**Fahre erst mit dem Interview fort, wenn ein Ansatz gewählt wurde.** Der gewählte Ansatz bestimmt die Richtung der verbleibenden Fragen.

### Schritt 3: Interview-Abschluss — Optionen nach jeder Runde

Nach jeder Fragerunde (ab Schritt 2b, also nachdem ein Lösungsansatz gewählt wurde) verwende **AskUserQuestion** mit IMMER diesen Optionen:

1. **Vertiefen** — Vertiefende Fragen stellen (zu aktuellem oder neuem Thema)
2. **Spec speichern** — Interview abschließen und Erkenntnisse als Spec-Datei sichern
3. **Spec & Tasks erstellen** — Interview abschließen, Spec schreiben UND Beads-Tasks generieren
4. **Abbrechen** — Interview beenden ohne Spec (z.B. wenn das Feature keinen Sinn mehr macht)

**Wiederhole diesen Schritt** bis der User Option 2, 3 oder 4 wählt.

Falls "Spec speichern": Weiter mit Schritt 4 → 4b → Abschluss.
Falls "Spec & Tasks erstellen": Weiter mit Schritt 4 → 4b → 4c → 5.
Falls "Abbrechen": Bestätige Abbruch, fasse kurz zusammen was besprochen wurde (für den Fall dass der User später zurückkommen will).

### Schritt 4: Spec schreiben

Schreibe die Erkenntnisse in `docs/specs/<feature-name>.md`:

```markdown
# Feature Specification: [Name]

## Übersicht
[Kurze Beschreibung]

## Ziele
- [Ziel 1]
- [Ziel 2]

## Gewählter Lösungsansatz
[Beschreibung des gewählten Ansatzes und Begründung]

### Verworfene Alternativen
- [Ansatz B]: [Warum verworfen]
- [Ansatz C]: [Warum verworfen]

## Scope
### Inkludiert
- ...

### Exkludiert (YAGNI)
- ... [mit Begründung warum bewusst ausgeschlossen]

## Technische Anforderungen
- ...

## Docs-Recherche Ergebnisse
[Erkenntnisse aus Context7-Recherche: aktuelle APIs, Breaking Changes, Best Practices]

## UI/UX Anforderungen
- ...

## Edge Cases & Error Handling
- ...

## Offene Fragen
- ...
```

### Schritt 4b: Spec-Review-Loop

Bevor die Spec finalisiert wird, durchlaufe einen Review-Loop (max 3 Iterationen):

1. **Review-Agent starten**:
   ```
   Agent(
     subagent_type="quality-agent",
     model="sonnet",
     description="Spec Review für <feature-name>",
     prompt="Reviewe die Spec-Datei docs/specs/<feature-name>.md auf:
       - Vollständigkeit: Fehlen wichtige Aspekte?
       - Widersprüche: Widersprechen sich Anforderungen?
       - YAGNI: Gibt es überflüssige Anforderungen?
       - Umsetzbarkeit: Sind alle Anforderungen technisch machbar?
       - Klarheit: Sind Anforderungen eindeutig formuliert?
       Gib konkrete Verbesserungsvorschläge zurück."
   )
   ```

2. **Findings dem User zeigen**: Präsentiere die Review-Ergebnisse und frage ob Anpassungen gewünscht sind.

3. **Spec anpassen**: Falls der User Änderungen wünscht, aktualisiere die Spec und wiederhole den Review (max 3 Iterationen).

4. **Approval-Gate**: Der User muss die finale Spec explizit freigeben bevor Tasks erstellt werden:
   > "Die Spec ist reviewt und bereit. Soll ich sie so finalisieren und mit der Task-Erstellung fortfahren?"

**Ohne explizites Approval keine Task-Erstellung.**

### Schritt 4c: Implementierungsplan erstellen

Nachdem die Spec approved wurde, erstelle einen Implementierungsplan bevor Tasks generiert werden. Der Plan ist eine Struktur-Skizze — konkreter Code und exakte Zeilen folgen erst bei der Task-Ausführung durch die Implementation-Agents.

**Codebase explorieren:**
Bevor du den Plan schreibst, erkunde die bestehende Codebase um realistische Pfade und Patterns zu verwenden:
- Glob/Grep um bestehende Dateistruktur und Patterns zu verstehen
- Relevante Dateien lesen die modifiziert werden müssen

**File Structure Mapping:**
Mappe welche Dateien erstellt oder modifiziert werden müssen:
```markdown
## File Structure

### Neue Dateien
- `src/path/to/new-file.ts` — [Verantwortung]
- `tests/path/to/test-file.test.ts` — [Was wird getestet]

### Modifizierte Dateien
- `src/path/to/existing.ts` — [Was wird geändert]
```

**Task-Dekomposition:**
Zerlege in unabhängige Tasks mit klarer Abgrenzung:
- Welche Dateien gehören zusammen (ändern sich gemeinsam)?
- Was kann parallel bearbeitet werden?
- Wo gibt es echte Abhängigkeiten?

Pro Task definieren:
- Klares Ziel und Akzeptanzkriterien
- Betroffene Dateien (erstellen/modifizieren)
- TDD-Ansatz: Was soll zuerst getestet werden?
- Test-Befehle die der Agent ausführen soll

**Plan dem User zeigen** via **AskUserQuestion** und auf Feedback warten bevor Tasks erstellt werden.

### Schritt 5: Beads-Tasks generieren

1. **Tasks aus Implementierungsplan ableiten** — jeder Task enthält:
   - Akzeptanzkriterien aus der Spec
   - File-Mapping aus dem Plan (welche Dateien betroffen)
   - Bite-sized Steps aus dem Plan
   - Exakte Test-Befehle

2. **Tasks erstellen** via `mcp__beads__create` — jeder Task enthält Akzeptanzkriterien, betroffene Dateien, TDD-Ansatz und Test-Befehle aus dem Implementierungsplan:
   ```javascript
   mcp__beads__create({
     title: "Task-Titel",
     description: "Akzeptanzkriterien, Dateien, TDD-Steps aus dem Plan",
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
