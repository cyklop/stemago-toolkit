---
name: diagnose
description: "Strukturiertes Debugging für hartnäckige Bugs, Regressions und unerwartetes Verhalten — mit Feedback-Loop-First-Ansatz. Verwende diesen Skill IMMER bei: Bugs die sich nicht sofort erklären lassen, Testfehlern die keinen offensichtlichen Fix haben, Performance-Regressions, 'es funktioniert manchmal nicht', 'ich verstehe nicht warum'. NICHT verwenden für: offensichtliche Tippfehler, bekannte Konfigurationsprobleme mit sofortigem Fix."
argument-hint: "[bug-beschreibung]"
---

# Diagnose — Strukturiertes Debugging

## Kernprinzip: Feedback-Loop zuerst

Der häufigste Debugging-Fehler: direkt in den Code gehen ohne reproduzierbares Fail-Signal.
**Baue zuerst einen deterministischen Feedback-Loop — alles andere kommt danach.**

## Workflow

### Phase 1: Orient — Problem verstehen

Stelle dem User maximal 3 gezielte Fragen via **AskUserQuestion**:

1. **Was wurde erwartet vs. was passiert?** (konkretes Verhalten, keine Vermutungen)
2. **Wann hat es zuletzt funktioniert?** (letzter bekannter guter Zustand, Git-Commit wenn möglich)
3. **Ist es deterministisch?** (immer, manchmal, unter bestimmten Bedingungen)

Prüfe parallel:
```bash
git log --oneline -10        # Letzte Änderungen
git diff HEAD~5..HEAD --stat # Was hat sich geändert?
```

Formuliere daraus eine **Problemhypothese** in einem Satz — bevor es weitergeht.

---

### Phase 2: Feedback-Loop aufbauen (PFLICHT — vor allem anderen)

Ohne deterministisches Signal ist jede Hypothese Spekulation.

**Ziel:** Ein Befehl der in unter 30 Sekunden automatisch zeigt: ✅ Fixed / ❌ Broken.

Optionen (in dieser Präferenz-Reihenfolge):

| Option | Beispiel | Wann |
|---|---|---|
| Failing Unit/Integration-Test | `npm test -- --testNamePattern="bug"` | Immer bevorzugt |
| curl/HTTP-Script | `curl -s /api/endpoint \| jq '.status'` | API-Bugs |
| CLI-Befehl mit Exit-Code | `node script.js && echo OK \|\| echo FAIL` | Prozess-Bugs |
| Browser-Skript | Playwright-Snippet | UI-Bugs |

**Der Feedback-Loop muss:**
- Deterministisch sein (kein "manchmal rot")
- Automatisch pass/fail signalisieren (kein manuelles Interpretieren)
- In unter 30s laufen (sonst wird er nicht benutzt)

Zeige dem User den Feedback-Loop-Befehl und führe ihn aus. Er muss **rot** sein bevor es weitergeht.

**Falls kein automatischer Feedback-Loop möglich ist:** Dokumentiere die manuelle Reproduktionssequenz exakt (Schritte, Daten, Umgebung).

---

### Phase 3: Reproduzieren

Führe den Feedback-Loop aus und bestätige: Bug ist reproduzierbar = ❌ Rot.

Falls der Feedback-Loop **nicht** rot ist:
- Entweder ist der Bug bereits gefixt (prüfen!)
- Oder der Feedback-Loop ist falsch kalibriert (zurück zu Phase 2)

---

### Phase 4: Hypothesen — geordnet nach Wahrscheinlichkeit

Entwickle **2-4 Hypothesen** ohne sofort Code zu ändern.

Pro Hypothese:
- **Was würde diese Hypothese erklären?**
- **Was würde sie widerlegen?** (konkrete Überprüfung)
- **Wahrscheinlichkeit:** hoch / mittel / niedrig

Ordne nach Wahrscheinlichkeit und prüfe die wahrscheinlichste zuerst.

**Heuristiken:**
- Letzte Änderungen (git log) sind häufiger schuld als alter Code
- Umgebungsunterschiede (dev vs. prod, Node-Version) vor Logik-Bugs prüfen
- Externe Dependencies vor eigener Logik prüfen

---

### Phase 5: Instrumentieren — eine Hypothese nach der anderen

**Nicht:** Logs überall hinstreuen.
**Sondern:** Gezielt die erste Hypothese überprüfen, dann Feedback-Loop ausführen.

```bash
# Minimal-Instrumentierung: nur was nötig ist um Hypothese 1 zu testen
# z.B. console.log an genau einer Stelle, oder Breakpoint an genau einer Funktion
```

Hypothese bestätigt → weiter zu Phase 6.
Hypothese widerlegt → nächste Hypothese, erneut instrumentieren.

**Grenze:** Nach 3 instrumentierten Hypothesen ohne Ergebnis → zurück zu Phase 1 (Problem falsch verstanden).

---

### Phase 6: Fixen

**Minimale Änderung** die den Bug behebt.

Kein Refactoring während des Fixes. Kein "während ich schon dabei bin".
Einziges Ziel: Feedback-Loop wird grün.

Führe nach dem Fix sofort aus:
```bash
# Feedback-Loop (muss jetzt ✅ grün sein)
# Alle anderen bestehenden Tests (keine Regressions einführen)
```

---

### Phase 7: Regression-Test sichern

**Der Feedback-Loop bleibt im Repo.** Kein Fix ohne dauerhaften Test.

Falls der Feedback-Loop ein Ad-hoc-Script war: in echten Test umwandeln.
Falls es bereits ein Test war: sicherstellen dass er Teil der normalen Test-Suite ist.

```bash
git add <test-file>
# Commit: "test: regression test für <bug-beschreibung>"
```

---

### Phase 8: Post-Mortem (optional, aber wertvoll)

Bei schweren Bugs (> 1h Debugging-Zeit):

```markdown
## Bug Post-Mortem

**Root Cause:** [Eigentliche Ursache in einem Satz]
**Warum nicht früher gefunden:** [Fehlende Tests? Schlechte Fehlermeldung? Annahme?]
**Verhindert durch:** [Welcher Test/Check hätte es abgefangen?]
**Systemisch:** [Gibt es ähnliche Stellen im Code die dasselbe Problem haben könnten?]
```

Speichere in `docs/post-mortems/<datum>-<bug>.md`.

---

## Anti-Patterns — was du NICHT tun sollst

- ❌ Code ändern ohne Feedback-Loop
- ❌ Mehrere Hypothesen gleichzeitig testen
- ❌ Den Fix committen ohne Regressions-Test
- ❌ "Ich probiere mal X" ohne Hypothese dahinter
- ❌ Umgebungsvariablen ändern ohne zu verstehen warum
