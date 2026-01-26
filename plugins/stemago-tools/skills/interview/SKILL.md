---
name: interview
description: "Conduct a structured interview about features/plans using deep questioning"
argument-hint: "[spec-file] or [feature-name]"
---

# Spec-Based Interview

Führe ein strukturiertes Interview durch, um ein tiefes Verständnis der Anforderungen zu gewinnen.

## Deine Aufgabe

### Schritt 1: Spec lesen (falls vorhanden)

Prüfe ob eine Spec-Datei existiert:
- Primär: `.taskmaster/docs/spec.md`
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

### Schritt 3: Spec schreiben

Nachdem das Interview abgeschlossen ist, schreibe die Erkenntnisse in `.taskmaster/docs/spec.md`:

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

### Schritt 4: Bestätigung

Zeige dem User eine Zusammenfassung und frage ob er die Spec anpassen oder direkt Tasks generieren möchte.
Nächster Schritt wäre: /tm:parse-prd .taskmaster/docs/spec.md

$ARGUMENTS
