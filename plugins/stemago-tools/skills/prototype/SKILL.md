---
name: prototype
description: "Wegwerf-Code schreiben um eine konkrete Design-Frage zu beantworten — bevor man sich auf eine Implementierung festlegt. Verwende wenn eine Implementierungsentscheidung unklar ist, verschiedene Ansätze verglichen werden sollen, oder eine Idee schnell validiert werden muss. Auch bei: 'lass uns das ausprobieren', 'ich bin nicht sicher ob das funktioniert', 'können wir zwei Varianten vergleichen'. NICHT für Production-Code — explizit ephemeral."
argument-hint: "[design-frage]"
---

# Prototype — Wegwerf-Code der Fragen beantwortet

## Kernprinzip

**Formuliere zuerst die Frage.** "Dieser Prototype testet ob/wie [X]."

Ohne klare Frage kein Prototype — sonst wird er stillschweigend zu Production-Code (Prototype-Rot).

## Schritt 1: Frage klären

Formuliere gemeinsam mit dem User die Frage in einem Satz.
Wähle dann den Branch:

### Logic Branch (Standard)
Für State-Machines, Business-Logic, Algorithmen, Datenmodelle.
- Terminal-App ohne UI-Overhead
- In-Memory-State (keine Persistenz außer wenn sie die Frage betrifft)
- Kein Error Handling, keine Tests, keine Abstraktionen
- Nach jedem Schritt: relevanter State sichtbar ausgeben

### UI Branch (Design-Varianten)
Für Layout-Varianten, Interaction-Patterns, visuelle Alternativen.
- Mehrere Varianten auf einer Route, umschaltbar via URL-Parameter (`?variant=a|b|c`)
- Minimales Styling — genug zum Beurteilen, nicht mehr

## Schritt 2: Prototype bauen

Lege die Datei in `scratch/` ab oder markiere sie klar als Prototype.
Kommentar ganz oben:

```
// PROTOTYPE: Testet "[Frage]"
// Löschen sobald beantwortet — kein Production-Code.
```

**Regeln:**
- Kein Refactoring, kein Error Handling, keine Abstraktion
- Fokus auf Geschwindigkeit — Eleganz ist irrelevant
- State nach jeder Aktion ausgeben damit Änderungen sichtbar sind

## Schritt 3: Frage beantworten

Führe den Prototype aus. Beantworte die Frage explizit:

> "Die Frage war: [X]. Antwort: [Y]. Begründung: [Z]."

## Schritt 4: Entscheidung

Frage den User via **AskUserQuestion**:

1. **Integrieren** — Erkenntnisse in echten Code übernehmen, Prototype löschen
2. **Verwerfen** — Prototype löschen, Entscheidung trotzdem festhalten
3. **Vertiefen** — Weitere Iteration mit neuer Frage

**Dokumentiere die Antwort bevor gelöscht wird** — als ADR oder Commit-Message:
- ADR: `docs/adr/YYYY-MM-DD-<entscheidung>.md`
- Commit: `experiment: [Frage] → [Antwort]`

**Kein Prototype-Rot:** Wenn der User nicht löscht/integriert → explizit nachfragen.
