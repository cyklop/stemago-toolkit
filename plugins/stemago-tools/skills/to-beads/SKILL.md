---
name: to-beads
description: "Plan, Konversation oder Spec schnell in Beads-Tasks zerlegen — ohne das vollständige Interview-Ritual. Verwende wenn: du bereits einen klaren Plan hast und daraus Tasks machen willst, nach einem externen Meeting Tasks angelegt werden sollen, eine Spec schon existiert und nur noch Tasks fehlen. Auch bei: 'mach daraus Tasks', 'leg das in Beads an', 'zerlege den Plan in Tasks', 'erstelle Tasks aus der Spec'. NICHT wenn Anforderungen erst noch geklärt werden müssen — dafür /interview."
argument-hint: "[spec-pfad oder plan-beschreibung]"
---

# to-beads — Plan → Beads-Tasks

Zerlege einen bestehenden Plan, eine Spec oder eine Konversation direkt in Beads-Tasks.

## Voraussetzung

Es muss bereits ein klarer Plan oder eine Spec existieren.
Falls nicht → `/interview` starten.

## Schritt 1: Eingabe ermitteln

Falls `$ARGUMENTS` vorhanden:
- Dateipfad (z.B. `docs/specs/feature.md`) → Datei lesen
- Freitext-Plan → direkt verwenden

Falls kein Argument: frage den User nach Plan oder Dateipfad.

## Schritt 2: Plan analysieren — Vertikal-Slicing

**Vertikal, nicht horizontal:**
- ✅ Vertikal: "User kann sich einloggen" (end-to-end: DB + API + UI)
- ❌ Horizontal: "Alle Datenbankmigrationen", "Alle API-Endpunkte"

**Jeder Task muss:**
- Eigenständig demonstrierbar sein (ein zeigbares Ergebnis)
- Von einem Agenten in einer Session machbar sein
- Klare Akzeptanzkriterien haben
- TDD-fähig sein (welcher Test beweist done?)

**Klassifikation pro Task:**
- **AFK** (Away From Keyboard): Agent kann alleine erledigen
- **HITL** (Human-In-The-Loop): Braucht Rückfragen oder menschliche Entscheidung (kennzeichnen!)

## Schritt 3: Task-Liste vorschlagen (vor dem Anlegen zeigen)

```markdown
## Vorgeschlagene Tasks

### [Task-Titel]
- Typ: task | bug | research
- Modus: AFK | HITL (Grund: ...)
- Akzeptanzkriterium: [Satz der beschreibt wann done]
- TDD-Signal: [Welcher Test/Check beweist es]
- Abhängig von: [anderer Task-Titel | —]

### [Nächster Task]
...

## Dependency-Graph
[Welche Tasks können parallel laufen, welche sequenziell]
```

Frage via **AskUserQuestion**:
1. **So anlegen** — Tasks direkt in Beads erstellen
2. **Anpassen** — Änderungen besprechen bevor Anlegen
3. **Abbrechen** — Nichts anlegen

## Schritt 4: Tasks in Beads anlegen

```javascript
// Kontext setzen
mcp__beads__context({ workspace_root: process.cwd() })

// Tasks anlegen (in Dependency-Reihenfolge)
mcp__beads__create({
  title: "Task-Titel",
  description: "Akzeptanzkriterium: [...]\nTDD-Signal: [...]\nBetroffene Dateien: [...]",
  issue_type: "task",
  priority: 2,
  labels: ["to-beads", "<feature-label>"]
})
```

Dependencies verknüpfen — nur echte Abhängigkeiten:
```javascript
mcp__beads__dep({
  issue_id: "abhaengiger-task-id",
  depends_on_id: "vorheriger-task-id",
  dep_type: "blocks"
})
```

## Schritt 5: Zusammenfassung zeigen

```markdown
## Tasks angelegt

- X Tasks erstellt
- Y sofort startbar (kein Blocker)
- Z blockiert (Dependencies)

Parallelisierbare Gruppen: [...]

Nächster Schritt: `bd ready` oder `/stemago-tools:beads-ready`
```
