---
name: interview
description: "Strukturiertes Interview über Features und Anforderungen führen, das in einen formalen Deliverable mündet — Spec, Implementierungsplan und Beads-Tasks. Verwende diesen Skill wenn der User: ein neues Feature planen will und am Ende eine Spec/Tasks braucht, Anforderungen für eine konkrete Umsetzung klären möchte, 'was brauchen wir für X' fragt, oder eine existierende Spec als Basis für Tasks nutzen will. Auch bei: 'Feature planen', 'Spec erstellen', 'Anforderungen für die Umsetzung klären'. NICHT verwenden für: Bug-Fixes, Code Reviews, direkte Implementierungsaufträge, oder Fragen zu bestehenden APIs/Libraries. Wenn nur Wissen aus dem Kopf extrahiert, ein Plan gestresstestet oder offen gebrainstormt werden soll OHNE formalen Spec-Output — dafür /grill-me."
argument-hint: "[feature-name]"
---

# Spec-Based Interview

Führe ein strukturiertes Interview durch, um ein tiefes Verständnis der Anforderungen zu gewinnen.

## Grundprinzipien

- **YAGNI**: Hinterfrage jede Anforderung — brauchen wir das wirklich JETZT? Wenn der User "und vielleicht noch X" sagt: "Ist X für den ersten Release nötig?"
- Stelle KEINE offensichtlichen Fragen — gehe in die TIEFE (Edge Cases, Trade-offs, Prioritäten)
- **Challengiere vage Sprache sofort**: "smart", "flexibel", "skalierbar", "einfach" → sofort fragen: "Was meinst du konkret mit X?"
- **Eine Frage nach der anderen** (im Grill-Modus): tiefere Antworten als bei Listen

---

## Schritt 1: Spec lesen (falls vorhanden)

Prüfe `docs/specs/<feature-name>.md` oder `$ARGUMENTS`.
Falls vorhanden → als Ausgangspunkt nutzen. Falls nicht → Interview von Grund auf starten.

---

## Schritt 1b: Capture-Datei anlegen (Checkpoint-Disziplin)

Lange Interviews füllen den Kontext. Damit nichts verloren geht, bevor die Spec geschrieben wird, lege **vor der ersten Frage** eine Capture-Datei unter `brainstorms/{YYYY-MM-DD}-{feature-slug}.md` an (Ordner anlegen falls er fehlt — Datum via `date +%F`).

**Checkpoint nach jeder Interview-Runde, bevor die nächste kommt:** Antworten, Entscheidungen (in den Worten des Users wo es zählt) und offene Flags (Punkt → Owner) dort festhalten. Die Datei — nicht dein Kontext — ist die Quelle der Wahrheit. Wird der Kontext mittendrin verloren, hält die Datei bereits alles bisher Gesagte. Beim Schreiben der Spec (Schritt 4) verdichtest du dieses Capture zum finalen Dokument; die rohe Erfassung bleibt in `brainstorms/`.

→ Detail-Mechanik und Dateistruktur: siehe `/grill-me`.

---

## Schritt 2: Interview führen

Verwende **AskUserQuestion**. Stelle 2-4 Fragen pro Runde.

**Fragegebiete:** Scope & Ziele, Technische Implementierung, UI/UX, Trade-offs, Edge Cases, Integration.
→ Details und Beispiel-Fragen: lies `REFERENCE.md` in diesem Skill-Verzeichnis.

#### Terminologie-Challenge (Grill-Modus)

Vage Begriffe **sofort** stoppen: "Kurz stopp — was meinst du genau mit '[Begriff]'?"

Trigger: "smart", "flexibel", "skalierbar", "einfach", "robust", "viele User", "schnell", jeder projektspezifische Fachbegriff.

Falls `CONTEXT.md` existiert: zuerst lesen, neue klare Definitionen dort ergänzen.

#### Design-Stress-Test

Nach jeder Designentscheidung proaktiv herausfordern:
- "Was passiert wenn [Worst-Case-Szenario]?"
- "Stell dir vor es ist 6 Monate später und der Ansatz hat nicht funktioniert — was wäre der Grund?"

#### Docs-Recherche

Sobald Libraries/Frameworks genannt werden, Research-Agent parallel starten:
```
Agent(subagent_type="research-agent", model="haiku",
  prompt="Recherchiere aktuelle Dokumentation für <library> via Context7.
    Fokus: aktuelle API, Breaking Changes, empfohlene Patterns. Kurze Zusammenfassung.")
```

---

## Schritt 2b: Lösungsansätze vorschlagen

Nach 2-3 Fragerunden: **2-3 Lösungsansätze** vorstellen.
- Kurze Beschreibung + Trade-offs + Empfehlung
- YAGNI: der einfachste Ansatz der die Anforderungen erfüllt ist oft der beste

Via **AskUserQuestion** Ansatz wählen lassen. **Erst fortfahren wenn ein Ansatz gewählt ist.**

---

## Schritt 3: Abschluss-Optionen (nach jeder Runde ab 2b)

Via **AskUserQuestion** immer diese 4 Optionen anbieten:

1. **Vertiefen** — weitere Fragen
2. **Spec speichern** → Schritt 4 → 4b
3. **Spec & Tasks erstellen** → Schritt 4 → 4b → 4c → 5
4. **Abbrechen** — kurze Zusammenfassung, kein Dokument

---

## Advisor-Check vor Spec

`advisor()` aufrufen bevor die Spec geschrieben wird. Sieht das gesamte Transcript — findet Lücken, Widersprüche, YAGNI-Verletzungen.

---

## Schritt 4: Spec schreiben

Schreibe nach `docs/specs/<feature-name>.md`.
→ Spec-Template: lies `REFERENCE.md` in diesem Skill-Verzeichnis.

---

## Schritt 4b: Spec-Review-Loop (max 3 Iterationen)

```
Agent(subagent_type="quality-agent", model="sonnet",
  prompt="Reviewe docs/specs/<feature-name>.md auf:
    Vollständigkeit, Widersprüche, YAGNI, Umsetzbarkeit, Klarheit.
    Konkrete Verbesserungsvorschläge.")
```

Findings zeigen → User entscheidet ob Anpassungen. Danach: **explizites Approval einholen** bevor Tasks erstellt werden.

---

## Schritt 4c: Implementierungsplan erstellen

Codebase erkunden (Glob/Grep), dann:
- **File Structure Map**: welche Dateien neu / modifiziert
- **Task-Dekomposition**: unabhängige Tasks mit Akzeptanzkriterien, TDD-Ansatz, Test-Befehlen

Plan via **AskUserQuestion** zeigen und Feedback abwarten.

---

## Schritt 5: Beads-Tasks generieren

→ Task-Format und Code-Beispiele: lies `REFERENCE.md` in diesem Skill-Verzeichnis.

Tasks anlegen via `mcp__beads__create`, Dependencies via `mcp__beads__dep`.

Zusammenfassung: Spec-Pfad, Anzahl Tasks, Dependency-Graph, Parallelisierungsgruppen.

---

## Schritt 6: Parallele Bearbeitung starten

Via **AskUserQuestion**:
1. **Jetzt parallel bearbeiten** → Task-Orchestrator starten
2. **Fertig** → Tasks für später aufheben, auf `/stemago-tools:beads-ready` hinweisen

---

## Schritt 7: Review & Reflect

Nachdem alle Tasks erledigt:

**7a:** `/review` anbieten → ausführen falls gewünscht.
**7b:** `/reflect` anbieten → ausführen falls gewünscht.
**7c:** Finale Zusammenfassung: Spec-Pfad, Tasks, Review-Ergebnis, Learnings.
