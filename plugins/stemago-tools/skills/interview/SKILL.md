---
name: interview
description: "Conduct a structured interview about features/plans using deep questioning"
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

### Schritt 5: Bestätigung

Zeige dem User eine Zusammenfassung:
- Spec-Datei Pfad: `docs/specs/<feature-name>.md`
- Erstellte Tasks (falls gewählt)
- Empfohlene nächste Schritte

$ARGUMENTS
