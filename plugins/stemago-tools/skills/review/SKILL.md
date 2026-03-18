---
name: review
description: "Code Review der letzten Änderungen durchführen. Verwende diesen Skill wenn der User Code prüfen lassen will, nach einem Review fragt, oder die Qualität der Änderungen validieren möchte. Auch bei 'prüf mal den Code', 'ist das so OK', 'gibt es Probleme', 'Security-Check', 'schau dir die Änderungen an', 'Review bitte', oder wenn nach einer Implementierung die Code-Qualität geprüft werden soll."
---

# /review - Code Review

Führe einen strukturierten, parallelisierten Code Review der letzten Änderungen durch.

## Deine Aufgabe

### Schritt 1: Änderungen ermitteln

Ermittle die exakte Git-Range für den Review:

```bash
# Exakte Range bestimmen
BASE_SHA=$(git merge-base HEAD origin/main 2>/dev/null || git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)

# Diff der Range
git diff --stat $BASE_SHA..$HEAD_SHA
git diff --name-only $BASE_SHA..$HEAD_SHA
git diff $BASE_SHA..$HEAD_SHA
```

Falls die Range leer ist, falle zurück auf:
```bash
git diff HEAD
git diff --cached
```

Falls auch das leer ist: "Keine Änderungen zum Reviewen gefunden." — Abbruch.

### Schritt 2: Kontext sammeln

Lies NICHT nur den Diff — lies die **vollständigen geänderten Dateien** sowie **direkt abhängige Dateien** (Imports, aufgerufene Module, Typdefinitionen). Nur mit dem vollen Kontext kann ein Review Qualität liefern.

Ermittle abhängige Dateien:
- Folge Imports der geänderten Dateien
- Prüfe welche Dateien die geänderten Exports verwenden (via Grep)
- Lies relevante Typdefinitionen und Interfaces

**Spec/Plan-Referenz ermitteln:**
- Prüfe ob eine zugehörige Spec existiert: `docs/specs/<feature-name>.md`
- Prüfe ob ein Implementierungsplan existiert
- Falls vorhanden, lies diese als Referenz für den Spec-Compliance-Check

### Schritt 3: Parallele Review-Agents starten

Starte **fünf spezialisierte Review-Agents parallel** — jeder fokussiert auf sein Gebiet:

```
# Agent 1: Security Review (haiku — regelbasiert, schnell)
Agent(
  subagent_type="quality-agent",
  model="haiku",
  description="Security Review",
  prompt="Analysiere diese Dateien auf Security-Probleme (OWASP Top 10):
    Geänderte Dateien: <liste>
    Diff: <diff>

    Prüfe auf: SQL Injection, XSS, Command Injection, unsichere Deserialisierung,
    hartcodierte Secrets/Credentials, fehlende Input-Validierung, CSRF, Path Traversal.

    Ausgabe: Liste mit Severity (critical/warning/info), Datei:Zeile, Beschreibung, Vorschlag.
    Falls keine Findings: 'Keine Security-Probleme gefunden.'"
)

# Agent 2: Performance & Error Handling (haiku — pattern-matching)
Agent(
  subagent_type="quality-agent",
  model="haiku",
  description="Performance Review",
  prompt="Analysiere diese Dateien auf Performance und Error Handling:
    Geänderte Dateien: <liste>
    Diff: <diff>

    Performance: N+1 Queries, unnötige Re-Renders, fehlende Indizes, große Payloads, Memory Leaks.
    Error Handling: Unbehandelte Exceptions, fehlende Null-Checks, unklare Fehlermeldungen.

    Ausgabe: Liste mit Severity (critical/warning/info), Datei:Zeile, Beschreibung, Vorschlag.
    Falls keine Findings: 'Keine Performance/Error-Probleme gefunden.'"
)

# Agent 3: Code-Qualität, Patterns & Docs (sonnet — braucht Urteilsvermögen)
Agent(
  subagent_type="quality-agent",
  model="sonnet",
  description="Quality & Pattern Review",
  prompt="Analysiere diese Dateien auf Code-Qualität, Pattern-Einhaltung und Dokumentation:
    Geänderte Dateien: <liste>
    Vollständige Dateien + Kontext-Dateien: <inhalt>
    Diff: <diff>

    Code-Qualität: Naming-Konventionen, Konsistenz, unnötige Komplexität, Duplizierung.
    Pattern-Einhaltung: Passt der Code zu bestehenden Patterns im Projekt?
    Dokumentation: Neue exports/APIs ohne Docs? README/CLAUDE.md veraltet?

    WICHTIG: Nenne auch explizit was GUT gemacht wurde (Strengths).

    Ausgabe:
    1. Strengths: Was ist gut gelungen? (spezifisch mit Datei:Zeile)
    2. Findings: Liste mit Severity (critical/warning/info), Datei:Zeile, Beschreibung, Vorschlag.
    Falls keine Findings: 'Keine Qualitäts-Probleme gefunden.'"
)

# Agent 4: Docs-Validierung (haiku + Context7 — aktuelle API-Prüfung)
Agent(
  subagent_type="research-agent",
  model="haiku",
  description="Docs Validation",
  prompt="Prüfe ob der geänderte Code aktuelle Library-APIs und Best Practices verwendet.
    Geänderte Dateien: <liste>
    Diff: <diff>

    VORGEHEN:
    1. Identifiziere alle verwendeten Libraries/Frameworks im Diff
    2. Recherchiere via Context7 die aktuelle Dokumentation für jede Library
    3. Prüfe auf: deprecated APIs, veraltete Patterns, bessere Alternativen in aktueller Version

    Ausgabe: Liste mit Severity (warning/info), Datei:Zeile, Beschreibung, aktuelle Alternative.
    Falls alles aktuell: 'Alle verwendeten APIs sind aktuell.'"
)

# Agent 5: Spec-Compliance (sonnet — nur wenn Spec/Plan vorhanden)
Agent(
  subagent_type="quality-agent",
  model="sonnet",
  description="Spec-Compliance Review",
  prompt="Prüfe ob die Implementierung die Spec/Plan-Anforderungen erfüllt:
    Spec/Plan: <spec-inhalt>
    Geänderte Dateien: <liste>
    Diff: <diff>

    Prüfe:
    1. Sind ALLE Anforderungen/Akzeptanzkriterien aus der Spec erfüllt?
    2. Wurde etwas implementiert das NICHT in der Spec steht? (Scope Creep / Over-building)
    3. Fehlt etwas das in der Spec steht? (Under-building)
    4. Breaking Changes dokumentiert?

    Ausgabe:
    - Spec-Compliance: ✅ Vollständig / ⚠️ Teilweise / ❌ Abweichungen
    - Details: Was erfüllt, was fehlt, was überflüssig
    Falls keine Spec vorhanden: 'Keine Spec gefunden — Spec-Compliance-Check übersprungen.'"
)
```

**WICHTIG:** Alle fünf Agents in EINEM Message-Block starten für echte Parallelität. Agent 5 nur starten wenn eine Spec/Plan-Datei gefunden wurde.

### Schritt 4: Review-Ergebnis konsolidieren

Sammle die Ergebnisse aller Agents und zeige eine konsolidierte Übersicht:

```
## Code Review Ergebnis

### Git-Range
`<BASE_SHA>..<HEAD_SHA>` (<N> Commits, <M> Dateien)

### Geprüfte Dateien
- file1.ts (geändert)
- file2.ts (neu)
- file3.ts (Kontext — importiert file1)

### Stärken
- Saubere Trennung von Concerns (file1.ts:15-42)
- Umfassende Test-Coverage (18 Tests, alle Edge Cases abgedeckt)
- Gutes Error Handling mit Fallbacks (file2.ts:85-92)

### Spec-Compliance
✅ Vollständig — Alle Anforderungen aus der Spec erfüllt.
(oder ⚠️/❌ mit Details)

### Findings

#### Critical
- [Security] file1.ts:42 - SQL Injection möglich bei unsanitized Input
  → Vorschlag: Parameterized Query verwenden

#### Warning
- [Performance] file2.ts:15 - N+1 Query in Loop
  → Vorschlag: Batch-Query verwenden

#### Info
- [Konsistenz] file1.ts:10 - Naming weicht von Projekt-Konvention ab
  → Vorschlag: camelCase statt snake_case

#### Deprecated/Veraltet
- [API] file1.ts:8 - `getServerSideProps` ist in Next.js 15 deprecated
  → Vorschlag: Server Component mit async verwenden (laut aktueller Docs)

### Zusammenfassung
- Critical: X | Warning: Y | Info: Z | Deprecated: V
- **Ready to merge?** [Yes / With fixes / No]
- **Begründung:** [1-2 Sätze technische Einschätzung]
```

### Schritt 5: Nächste Aktion — Immer User fragen

Falls Findings vorhanden, frage den User via **AskUserQuestion**:

1. **Alle Findings beheben** — Alle Critical, Warning und Info-Findings fixen
2. **Nur Critical/Warning beheben** — Info-Findings ignorieren
3. **Als Beads-Tasks tracken** — Findings als Tasks in Beads erstellen (für spätere Bearbeitung)
4. **Nichts tun** — Nur zur Kenntnis nehmen

**WICHTIG:** Keine automatischen Fixes — IMMER erst Rückfrage mit dem User.

**Push-Back Guidance:** Falls du als Reviewer ein Finding für falsch hältst, erkläre dem User warum mit technischer Begründung. Zeige Code/Tests die beweisen dass es korrekt ist. Reviewer-Feedback ist beratend, nicht absolut — aber ignoriere valide technische Kritik nicht.

**Falls "Alle Findings beheben" oder "Nur Critical/Warning beheben":**

Behebe die gewählten Findings. Danach automatisch:
1. Tests laufen lassen (falls vorhanden): `npm test` / `npm run lint` / projektspezifisch
2. Ergebnis zeigen — welche Findings behoben, ob Tests grün sind

**Falls "Als Beads-Tasks tracken":**

Erstelle für jedes Finding einen Beads-Task:
```javascript
mcp__beads__create({
  title: "[Review] <Finding-Titel>",
  description: "Severity: <critical/warning/info>\nDatei: <datei:zeile>\n\nBeschreibung: <beschreibung>\nVorschlag: <vorschlag>",
  issue_type: "bug",
  priority: 1, // critical=1, warning=2, info=3
  labels: ["from-review", "<severity>"]
});
```

Zeige Zusammenfassung der erstellten Tasks.

### Schritt 6: Reflect anbieten

Nach Abschluss (Fixes oder Task-Erstellung), frage den User via **AskUserQuestion**:

1. **Reflect starten** — `/reflect` ausführen um Session-Learnings zu extrahieren
2. **Fertig** — Review abschließen

$ARGUMENTS
