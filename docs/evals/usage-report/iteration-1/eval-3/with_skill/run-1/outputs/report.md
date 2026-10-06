# Usage Report: stemago-toolkit — Februar–Mai 2026

> Zeitraum: 11.02. – 12.05.2026 · 2 Sessions analysiert

---

## Übersicht

| Metrik | Wert |
|--------|------|
| Sessions | 2 |
| Skill-Aufrufe gesamt | 6 |
| Agent-Einsätze gesamt | 7 |
| Aktiv genutzte Skills (stemago-tools) | 0 von 12 installierten |
| Aktiv genutzte Agents | 2 von 14 installierten |

---

## Skills — Nutzung

| Skill | Aufrufe | Anteil | Trend |
|-------|---------|--------|-------|
| `superpowers:brainstorming` | 2 | 33% | häufigster |
| `skill-creator:skill-creator` | 2 | 33% | gleichauf |
| `superpowers:writing-plans` | 1 | 17% | einmalig |
| `superpowers:subagent-driven-development` | 1 | 17% | einmalig |

**Interpretation:** Alle genutzten Skills stammen aus externen Namespaces (`superpowers`, `skill-creator`) — kein einziger der 12 installierten `stemago-tools`-Skills wurde im Zeitraum direkt aufgerufen. Das spiegelt wider, dass die Sessions primär auf Skill-Entwicklung ausgerichtet waren, nicht auf den Einsatz des fertigen Toolkits.

### Nicht genutzte Skills ⚠️

Alle 12 installierten stemago-tools-Skills hatten 0 direkte Aufrufe im Zeitraum:

- `stemago-tools:db-inspect` — Kandidat zum Entfernen: kein aktives DB-Projekt in diesem Toolkit-Repo erkennbar
- `stemago-tools:browser-test` — Kein Frontend-Projekt im Toolkit; seltener Spezialfall
- `stemago-tools:reflect` — Session-Reflection-Workflow noch nicht etabliert
- `stemago-tools:reflect-config` — 0 Aufrufe; bei aktiver Konfigurationsarbeit relevant
- `stemago-tools:docs-lookup` — Könnte durch direkte Context7-Nutzung ersetzt werden
- `stemago-tools:setup` — Setup-Workflow möglicherweise abgeschlossen
- `stemago-tools:github-ops` — GitHub-Operationen offenbar direkt via `gh` CLI
- `stemago-tools:interview` — Feature-Planung ohne strukturiertes Interview
- `stemago-tools:beads-ready` — Beads-Workflow nicht aktiv als Skill aufgerufen
- `stemago-tools:review` — Code-Review über andere Kanäle (`/code-review`)
- `stemago-tools:land-the-plane` — Session-Abschluss ohne formalen Handoff
- `stemago-tools:usage-report` — Neu installiert (dieser Report ist der erste Einsatz)

---

## Agents — Einsatz

| Agent | Aufrufe | Notizen |
|-------|---------|---------|
| `general-purpose` | 5 | Alle in einer Session (07.05.2026) |
| `stemago-tools:research-agent` | 2 | Einziger stemago-tools-Agent mit Nutzung |

**Interpretation:** Der `general-purpose`-Agent dominiert mit 5 Aufrufen — Subagenten-Arbeit findet statt, aber ohne Spezialisierung auf die konfigurierten stemago-Agents. Der `research-agent` wurde zweimal eingesetzt, passend zur Skill-Entwicklungsaktivität.

### Nicht genutzte Agents ⚠️

12 von 14 installierten Agents hatten 0 Aufrufe:

- `task-checker`, `completion-gate`, `readiness-gate`, `enhanced-quality-gate` — Quality-Gate-Pipeline nie aktiviert
- `tdd-validation-agent`, `functional-testing-agent` — Testing-Agents ungenutzt; kein testgetriebenes Vorgehen erkennbar
- `task-orchestrator`, `task-executor` — Orchestrierungs-Layer ungenutzt
- `feature-implementation-agent`, `component-implementation-agent`, `infrastructure-implementation-agent` — Spezialisierte Implementierungs-Agents nie eingesetzt
- `devops-agent` — DevOps-Automatisierung nicht genutzt
- `quality-agent` — Qualitätsprüfung nicht via Agent

---

## Modell-Verteilung

| Modell | Aufrufe | Anteil |
|--------|---------|--------|
| `claude-opus-4-7` | 264 | 66.2% |
| `claude-sonnet-4-6` | 131 | 32.8% |
| `<synthetic>` | 1 | 0.3% |
| **Gesamt** | **396** | **100%** |

**Bewertung:** Opus dominiert mit 66% — das ist kritisch zu hinterfragen. Die Session vom 07.05. allein erzeugte 264 Opus-Aufrufe, fast ausschließlich durch 5 parallele `general-purpose`-Subagenten. Das deutet darauf hin, dass Subagenten standardmäßig auf Opus laufen. Eine Umstellung auf Sonnet könnte die Kosten um ca. 60% senken ohne messbare Qualitätseinbuße für typische Implementierungsaufgaben.

---

## Empfehlungen

1. **Subagenten-Modell auf Sonnet umstellen**: Die 5 `general-purpose`-Aufrufe erzeugten 264 Opus-Calls in einer Session. Prüfe ob die Agent-Frontmatter ein fehlendes `model: sonnet` hat — das ist das größte Einsparpotenzial.

2. **`stemago-tools:db-inspect` entfernen**: 0 Aufrufe in 90 Tagen, kein Datenbank-Projekt im Toolkit. Reduziert kognitiven Overhead im `/`-Menü ohne Verlust.

3. **TDD-Workflow evaluieren oder bereinigen**: Task-Checker, Completion-Gate, TDD-Validation-Agent und Functional-Testing-Agent sind konfiguriert aber nie genutzt. Entweder aktiv einführen oder entfernen, um die Konfiguration schlank zu halten.

4. **Session-Rituale etablieren**: `beads-ready` (Session-Start) und `land-the-plane` (Session-Ende) hatten 0 Aufrufe, obwohl beide dokumentiert sind. Ein konsequentes Ritual würde den Mehrwert des Toolkits steigern.

5. **`usage-report` monatlich planen**: Dieser erste Report zeigt, dass das Toolkit aktiv weiterentwickelt aber wenig genutzt wird. Ein monatlicher Report hilft, Nutzungsmuster über Zeit zu beobachten.

---

## Monatliche Automatisierung

Um diesen Report automatisch am 1. jeden Monats zu erhalten:

```
/schedule "Am 1. jeden Monats um 9 Uhr: /stemago-tools:usage-report ausführen"
```

Oder manuell mit: `/stemago-tools:usage-report --months 1`
