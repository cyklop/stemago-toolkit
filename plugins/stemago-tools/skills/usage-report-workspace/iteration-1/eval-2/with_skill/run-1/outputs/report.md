# Usage Report: stemago-toolkit — Mai 2026

> Zeitraum: 12.04. – 12.05.2026 · 2 Sessions analysiert

---

## Übersicht

| Metrik | Wert |
|--------|------|
| Sessions | 2 |
| Skill-Aufrufe gesamt | 6 |
| Agent-Einsätze gesamt | 7 |
| Aktiv genutzte Skills | 0 von 12 installierten stemago-tools Skills |
| Aktiv genutzte Agents | 1 von 14 installierten stemago-tools Agents |

---

## Skills — Nutzung

| Skill | Aufrufe | Anteil | Trend |
|-------|---------|--------|-------|
| `superpowers:brainstorming` | 2 | 33% | externer Skill |
| `skill-creator:skill-creator` | 2 | 33% | externer Skill |
| `superpowers:writing-plans` | 1 | 17% | externer Skill |
| `superpowers:subagent-driven-development` | 1 | 17% | externer Skill |

Auffällig: Sämtliche Skill-Aufrufe im Zeitraum gingen an externe Skills (`superpowers:*`, `skill-creator:*`), nicht an `stemago-tools`-Skills. Das spiegelt wider, dass die Sessions dieses Monats auf Tooling-Entwicklung und Skill-Erstellung ausgerichtet waren — also Meta-Arbeit an dem Toolkit selbst, nicht an einem Projekt, das es nutzt.

### Nicht genutzte Skills (stemago-tools) ⚠️

Alle 12 installierten `stemago-tools`-Skills wurden im Zeitraum nicht aufgerufen:

- `beads-ready` — Kern-Workflow-Skill; wahrscheinlich in anderen Projekten aktiv, aber in der Toolkit-Eigenentwicklung wenig relevant
- `browser-test` — Spezialist-Skill; kein UI-Projekt im Zeitraum, logisch nicht aufgerufen
- `db-inspect` — Kein aktives DB-Projekt erkennbar; Kandidat zum Entfernen falls kein DB-Projekt geplant ist
- `docs-lookup` — Nützlich bei Library-Recherche; in reinen Tooling-Sessions selten gebraucht
- `github-ops` — Kein PR/Issue-Workflow im Zeitraum initiiert
- `interview` — Kein Feature-Interview initiiert; einer der Sessions war Brainstorming statt strukturiertem Interview
- `land-the-plane` — Session-Abschluss-Skill; ungenutzt — möglicherweise läuft der Hook stattdessen automatisch
- `reflect-config` — Konfigurationsreflexion; nie aufgerufen, obwohl `reflect` existiert
- `reflect` — Kein manuelles Reflect-Kommando im Zeitraum
- `review` — Kein Code-Review im Zeitraum initiiert
- `setup` — Einmaliger Setup-Skill; logisch selten gerufen
- `usage-report` — Wurde erstmalig in dieser Session erstellt; 0 historische Aufrufe

---

## Agents — Einsatz

| Agent | Aufrufe | Notizen |
|-------|---------|---------|
| `general-purpose` | 5 | Generischer Agent, kein stemago-tools-Spezialisten-Agent |
| `stemago-tools:research-agent` | 2 | Dokumentationsrecherche via Context7 |

### Nicht genutzte Agents (stemago-tools) ⚠️

13 von 14 installierten Agents wurden im Zeitraum nicht eingesetzt:

- `completion-gate` — Quality-Gate für Task-Abschlüsse; kein TDD-Workflow aktiv
- `component-implementation-agent` — Kein UI-Komponentenentwicklungs-Workflow
- `devops-agent` — Kein DevOps-Bedarf im Zeitraum
- `enhanced-quality-gate` — Erweitertes Quality-Gate; kein Einsatz, möglicherweise unbekannt
- `feature-implementation-agent` — Kein Feature-TDD-Workflow aktiv
- `functional-testing-agent` — Kein automatisiertes Testen initiiert
- `infrastructure-implementation-agent` — Kein Infrastruktur-Setup im Zeitraum
- `quality-agent` — Kein Quality-Review-Workflow
- `readiness-gate` — Kein PR-Readiness-Check
- `task-checker` — Kein Beads-Task-Checking-Workflow
- `task-executor` — Kein paralleles Task-Execution-Pattern
- `task-orchestrator` — Kein Multi-Agent-Orchestrierungs-Workflow initiiert
- `tdd-validation-agent` — Kein TDD-Zyklus aktiv

Der einzige genutzte stemago-tools Agent: `research-agent` — konsequent und zweimal eingesetzt für Dokumentationsrecherche in der Entwicklungs-Session.

---

## Modell-Verteilung

| Modell | Aufrufe | Anteil |
|--------|---------|--------|
| `claude-opus-4-7` | 264 | 66% |
| `claude-sonnet-4-6` | 131 | 33% |
| `<synthetic>` | 1 | <1% |

Die Verteilung zeigt eine klare Opus-Dominanz (66%). Da es sich hauptsächlich um Tooling-Entwicklungs-Sessions handelte, bei denen Subagenten (`general-purpose` × 5) eingesetzt wurden, ist der hohe Opus-Anteil kostenrelevant. Konkret: In Session `f0b9273b` liefen 264 Opus-Nachrichten — das entspricht dem intensiven Subagenten-Einsatz für Skill-Erstellung. Sonnet wurde für den initiierenden Claude-Code-Client genutzt (64 bzw. 67 Aufrufe). Die Relation ist vertretbar für kreative Planungs- und Entwicklungsarbeit, aber bei 5 `general-purpose`-Agenten-Aufrufen sollte geprüft werden, ob diese nicht auf Sonnet konfiguriert werden könnten.

---

## Empfehlungen

1. **`db-inspect` entfernen**: 0 Aufrufe in 30 Tagen, kein aktives DB-Projekt erkennbar. Falls in Zukunft ein DB-Projekt ansteht, kann der Skill leicht wieder installiert werden.

2. **`general-purpose`-Agenten durch stemago-tools-Spezialisten ersetzen**: 5 von 7 Agenteneinsätzen gingen an `general-purpose` statt an Spezialisten-Agents. Das deutet darauf hin, dass der Orchestrierungsworkflow (`task-orchestrator` → `feature-implementation-agent` etc.) noch nicht routiniert eingesetzt wird. Tipp: `/stemago-tools:interview` + `task-orchestrator`-Pattern als Standard etablieren.

3. **Opus-Kosten bei Subagenten prüfen**: 264 Opus-Aufrufe in einer einzigen Session sind teuer. Wenn `general-purpose`-Agenten für Code-Implementierungsaufgaben genutzt werden, lohnt es sich, den Agent-Aufruf explizit auf `claude-sonnet-4-6` umzustellen (falls das Aufgabenprofil es erlaubt).

4. **`land-the-plane` bewusst nutzen**: Der Skill wurde nicht manuell aufgerufen — der `session-land-the-plane.sh`-Hook läuft automatisch am Session-Ende, was gut ist. Aber der manuelle Aufruf mid-session (vor einem langen Abschnitt) kann helfen, den Kontext strukturiert zu sichern.

5. **Usage-Report monatlich automatisieren**: Jetzt, da der Skill existiert, lohnt sich ein monatlicher automatischer Report um Nutzungstrends über die Zeit zu sehen. Mit wachsenden Sessions werden die Daten aussagekräftiger.

---

## Monatliche Automatisierung

Um diesen Report automatisch am 1. jeden Monats zu erhalten:

```
/schedule "Am 1. jeden Monats um 9 Uhr: /stemago-tools:usage-report ausführen"
```

Oder manuell mit: `/stemago-tools:usage-report --months 1`
