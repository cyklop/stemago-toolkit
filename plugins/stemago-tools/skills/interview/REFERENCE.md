# Interview — Reference

Detail-Dokumentation für den `/interview` Skill. Lies diese Datei wenn du:
- Das Spec-Template brauchst
- Konkrete Beispiel-Fragen für ein Themengebiet suchst
- Task-Erstellungs-Code-Beispiele brauchst

---

## Fragegebiete (Schritt 2)

### 1. Scope & Ziele
- Was genau soll erreicht werden?
- Was ist explizit NICHT Teil des Scopes?
- Welche Probleme werden gelöst — für wen?
- Was zählt als Erfolg (messbar)?

### 2. Technische Implementierung
- Welche bestehenden Patterns/Libraries sollen verwendet werden?
- Gibt es Performance-Anforderungen (konkrete Zahlen)?
- Wie soll mit Fehlern umgegangen werden?
- Welche Datenmenge wird erwartet?

### 3. UI/UX
- Wie soll die Interaktion konkret aussehen?
- Mobile vs. Desktop — Priorität?
- Accessibility-Anforderungen?
- Wenn UI-Mockup hilfreich: `Skill(skill="generate-image", args="<Beschreibung>")`

### 4. Trade-offs & Prioritäten
- Zeit vs. Qualität vs. Features — was hat Priorität?
- Was kann in einem späteren Release kommen?
- Was ist "must have" vs. "nice to have"?

### 5. Edge Cases
- Was passiert bei leeren / ungültigen Daten?
- Concurrent Access — mehrere User gleichzeitig?
- Offline-Verhalten?
- Rollback-Strategie bei Fehlern?

### 6. Integration
- Welche bestehenden Systeme sind betroffen?
- API-Änderungen nötig?
- Datenbankmigrationen?
- Breaking Changes für andere Teams?

---

## Spec-Template (Schritt 4)

```markdown
# Feature Specification: [Name]

## Übersicht
[Kurze Beschreibung — 2-3 Sätze]

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

---

## Task-Erstellung Code-Beispiele (Schritt 5)

```javascript
// Kontext setzen
mcp__beads__context({ workspace_root: process.cwd() })

// Task anlegen
mcp__beads__create({
  title: "Task-Titel",
  description: `Akzeptanzkriterien:
- [Kriterium 1]
- [Kriterium 2]

TDD-Ansatz:
- Zuerst schreiben: [welcher Test]
- Test-Befehl: [npm test ... / pytest ...]

Betroffene Dateien:
- src/path/to/new-file.ts (neu)
- src/path/to/existing.ts (modifizieren: [was genau])`,
  issue_type: "task",
  priority: 2,
  labels: ["from-interview", "<feature-name>"]
})

// Dependencies verknüpfen (nur echte Abhängigkeiten)
mcp__beads__dep({
  issue_id: "abhaengiger-task-id",
  depends_on_id: "vorheriger-task-id",
  dep_type: "blocks"
})
```

---

## Task-Orchestrator starten (Schritt 6)

```javascript
Agent({
  subagent_type: "task-orchestrator",
  prompt: `Analysiere und bearbeite die Beads Task-Queue für Feature '<feature-name>'.
    Spec: docs/specs/<feature-name>.md
    Labels: from-interview, <feature-name>

    STRATEGIE:
    1. mcp__beads__ready → alle Tasks ohne Blocker identifizieren
    2. Alle unabhängigen Tasks PARALLEL über spezialisierte Agents starten
    3. Sobald Task abgeschlossen → prüfen ob neue Tasks freigeschaltet
    4. Wiederholen bis alle Tasks erledigt
    5. Abschluss melden`
})
```

---

## Terminologie-Challenge — Beispiele

| Vager Begriff | Gegenfrage |
|---|---|
| "skalierbar" | "Was bedeutet skalierbar konkret — 100 User? 10.000? Horizontale Skalierung?" |
| "einfach" | "Einfach für wen — Developer oder Endnutzer?" |
| "schnell" | "Was zählt als schnell — unter 100ms? Unter 1s?" |
| "flexibel" | "Flexibel in welcher Dimension — konfigurierbar, erweiterbar, oder beides?" |
| "viele User" | "Welche Größenordnung — 10? 1.000? 100.000?" |
| projektspezifischer Begriff | "Was zählt für euch als [Begriff] — gibt es ein konkretes Beispiel?" |
