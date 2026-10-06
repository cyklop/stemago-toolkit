# Usage Report: stemago-toolkit — Mai 2026

> Zeitraum: 12.04. – 12.05.2026 · 2 Sessions analysiert

---

## Übersicht

| Metrik | Wert |
|--------|------|
| Sessions | 2 |
| Skill-Aufrufe gesamt | 6 |
| Agent-Einsätze gesamt | 7 |
| Aktiv genutzte Skills | 4 von 12 installierten (33%) |
| Aktiv genutzte Agents | 2 von 14 installierten (14%) |

---

## Skills — Nutzung

| Skill | Aufrufe | Anteil | Trend |
|-------|---------|--------|-------|
| `superpowers:brainstorming` | 2 | 33% | ↑ häufigster |
| `skill-creator:skill-creator` | 2 | 33% | ↑ häufigster |
| `superpowers:writing-plans` | 1 | 17% | |
| `superpowers:subagent-driven-development` | 1 | 17% | |

**Interpretation:** Der Monat war geprägt von Skill-Entwicklung und Planungsarbeit. Die häufigsten Aufrufe entfallen auf `superpowers:brainstorming` und `skill-creator:skill-creator` – beide in beide Sessions genutzt, was auf eine intensive Skill-Bauphase hinweist (vermutlich der `usage-report`-Skill selbst). Kein einziger `stemago-tools:`-nativer Skill wurde im Zeitraum aufgerufen.

### Nicht genutzte Skills ⚠️

Folgende **stemago-tools**-Skills waren installiert, wurden aber im Zeitraum **nicht ein einziges Mal** aufgerufen:

- `stemago-tools:reflect-config` — Meta-Skill für Konfigurationsanpassungen; seltener Spezialfall, aber 0 Aufrufe in 30 Tagen. Kandidat zur Konsolidierung mit `reflect`.
- `stemago-tools:db-inspect` — Datenbankinspektion. Kein aktives DB-Projekt in diesem Repo erkennbar. **Klarer Kandidat zum Entfernen.**
- `stemago-tools:reflect` — Session-End-Reflection. Wird bisher nicht als Skill aufgerufen, obwohl ein Hook existiert (session-reflect.sh). Potenziell redundant mit dem Hook.
- `stemago-tools:docs-lookup` — Kontextbasierte Dokumentationssuche. 0 Aufrufe — entweder unbekannt oder über Context7 direkt ersetzt.
- `stemago-tools:browser-test` — UI-Tests im Browser. Kein Frontend-Projekt aktiv — **Kandidat zum Entfernen** oder Auslagern.
- `stemago-tools:setup` — Einmal-Skill für Projektinitialisierung. Typischerweise selten genutzt, aber 0 Aufrufe ist normal. Behalten.
- `stemago-tools:github-ops` — GitHub-Operationen. 0 Aufrufe — unklar ob verdrängt durch `gh`-CLI-Direktnutzung.
- `stemago-tools:interview` — Feature-Requirement-Interviews. 0 Aufrufe trotz Planungsarbeit in der Session — evtl. unbewusst übersprungen zugunsten von `superpowers:writing-plans`.
- `stemago-tools:beads-ready` — Session-Start mit Beads. 0 Aufrufe, obwohl in CLAUDE.md als Workflow empfohlen.
- `stemago-tools:review` — Code Review Orchestration. 0 Aufrufe — evtl. durch `superpowers:receiving-code-review` ersetzt.
- `stemago-tools:land-the-plane` — Session-Abschluss-Handoff. 0 Aufrufe als Skill, wird aber durch SessionEnd-Hook abgedeckt.
- `stemago-tools:usage-report` — Dieser Report selbst. 0 Aufrufe (neu installiert).

---

## Agents — Einsatz

| Agent | Aufrufe | Modell | Notizen |
|-------|---------|--------|---------|
| `general-purpose` | 5 | nicht gesetzt (erbt Orchestrator) | Parallele Subagenten via superpowers |
| `stemago-tools:research-agent` | 2 | sonnet | Dokumentationsrecherche via Context7 |

**Interpretation:** Fast alle Agent-Aktivität geht auf `general-purpose`-Subagenten zurück – ein superpowers-Pattern, nicht stemago-tools-nativ. Die stemago-tools-Agents werden kaum eingesetzt.

### Nicht genutzte Agents ⚠️

**10 von 14 installierten Agents** wurden nicht aufgerufen:

- `task-orchestrator` — Koordiniert stemago-tools-Agenten. 0 Aufrufe: Die Orchestrierung läuft über `superpowers:subagent-driven-development` statt über diesen Agent. **Strukturelles Problem: zwei konkurrierende Orchestrierungsmodelle.**
- `task-checker` — Aufgabenprüfung. 0 Aufrufe. Kandidat zur Entfernung wenn task-orchestrator nicht genutzt wird.
- `task-executor` — Aufgabenausführung. 0 Aufrufe. Gleiche Situation wie task-checker.
- `feature-implementation-agent` — Feature-Implementierung. 0 Aufrufe. Stattdessen werden `general-purpose`-Agents genutzt.
- `component-implementation-agent` — UI-Komponenten. 0 Aufrufe. Kein aktives Frontend-Projekt.
- `infrastructure-implementation-agent` — Build/Tooling. 0 Aufrufe.
- `tdd-validation-agent` — TDD-Validierung. 0 Aufrufe trotz TDD-Methodologie im CLAUDE.md.
- `functional-testing-agent` — Funktionale Tests. 0 Aufrufe.
- `quality-agent` — Qualitätsprüfung. 0 Aufrufe.
- `enhanced-quality-gate` — Quality Gate. 0 Aufrufe.
- `completion-gate` — Completion-Prüfung. 0 Aufrufe.
- `readiness-gate` — Readiness-Prüfung. 0 Aufrufe.
- `devops-agent` — DevOps-Aufgaben. 0 Aufrufe.

---

## Modell-Verteilung

| Modell | Aufrufe | Anteil |
|--------|---------|--------|
| claude-opus-4-7 | 264 | 66% |
| claude-sonnet-4-6 | 131 | 33% |
| `<synthetic>` | 1 | <1% |

**Bewertung:** Opus dominiert mit 66% der Nachrichten. In der produktiven Session (07.05.) liefen die `general-purpose`-Subagenten alle unter Opus (264 Aufrufe), was auf fehlende Modell-Zuweisung in den superpowers-Agents hindeutet. Die 4 stemago-tools-Agents mit explizitem `model: sonnet` sind konfiguriert, werden aber kaum genutzt.

**Kostenoptimierungspotenzial:** Wenn `general-purpose`-Subagenten auf Sonnet umgestellt würden, könnten 60-70% der Opus-Kosten eingespart werden. Das erfordert aber Änderungen an superpowers-Skills, nicht an stemago-tools.

---

## Empfehlungen

1. **`db-inspect` und `browser-test` entfernen**: Beide Skills haben 0 Aufrufe und passen nicht zum aktuellen Toolkit-Charakter (kein DB- oder Frontend-Projekt). Entfernen reduziert die Skill-Liste von 12 auf 10 und vermindert Rauschen beim `/`-Menü.

2. **Nicht genutzte Orchestrierungs-Agents bereinigen**: `task-orchestrator`, `task-checker`, `task-executor` und alle `*-implementation-agent` sowie `*-gate`-Agents (insgesamt 9+ Agents) haben 0 Aufrufe. Das stemago-tools-Orchestrierungsmodell wird durch `superpowers`-Skills verdrängt. Entscheide ob du das superpowers-Modell oder das stemago-tools-Modell bevorzugst — dann die andere Seite bereinigen. Wenn superpowers bleibt, können 9+ Agents entfernt werden.

3. **`reflect-config` mit `reflect` zusammenführen**: Zwei separate Skills für Reflection-Themen (einer für Config, einer für Learnings) erzeugt unnötige Fragmentierung bei 0 Aufrufen für beide. Prüfe ob `reflect-config`-Funktionalität in `reflect` integriert werden kann.

4. **`beads-ready` und `land-the-plane` als Skill vs. Hook klären**: Beide sind als Skills installiert und als SessionEnd-Hooks konfiguriert. 0 Skill-Aufrufe — die Hook-Seite scheint zu funktionieren. Überlege, ob die doppelte Implementierung (Skill + Hook) notwendig ist oder ob einer der Wege ausreicht.

5. **`docs-lookup` und `github-ops` evaluieren**: Beide haben 0 Aufrufe. `docs-lookup` wird möglicherweise durch die direkte Context7-Integration ersetzt; `github-ops` durch direkte `gh`-CLI-Nutzung. Eine kurze Evaluation ob diese Skills aktiv eingesetzt werden würden oder ob die direkten Alternativen ausreichen, könnte weitere 2 Skills einsparen.

---

## Monatliche Automatisierung

Um diesen Report automatisch am 1. jeden Monats zu erhalten:

```
/schedule "Am 1. jeden Monats um 9 Uhr: /stemago-tools:usage-report ausführen"
```

Oder manuell mit: `/stemago-tools:usage-report --months 1`
