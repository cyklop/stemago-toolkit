# Usage Report: stemago-toolkit — Mai 2026

> Zeitraum: gesamte Projektlaufzeit (Jan 2026 – 12. Mai 2026) · 13 Sessions analysiert

---

## Übersicht

| Metrik | Wert |
|--------|------|
| Sessions gesamt | 13 |
| Subagent-Einsätze gesamt | 38 |
| Analysierte JSONL-Dateien | 40 |
| Gesamte Nachrichten | 2.948 |
| Model-Aufrufe (ohne synthetic) | 1.220 |
| Aktiv genutzte stemago-tools Skills | 0 von 12 |
| Aktiv genutzte stemago-tools Agents | 1 von 14 |

---

## Skills — Nutzung

### Explizit aufgerufene Skills (via Skill-Tool)

| Skill | Aufrufe | Quelle |
|-------|---------|--------|
| `superpowers:brainstorming` | 2 | Externer Skill (superpowers-Plugin) |
| `skill-creator:skill-creator` | 2 | Externer Skill |
| `superpowers:writing-plans` | 1 | Externer Skill |
| `superpowers:subagent-driven-development` | 1 | Externer Skill |

**Gesamt: 6 Skill-Aufrufe — ausschliesslich externe Skills.**

Sämtliche Skill-Aufrufe im gesamten Projektzeitraum gingen an externe Skills (`superpowers:*`, `skill-creator:*`), nicht an `stemago-tools`-Skills. Das ist erwartbar: Dieses Projekt ist das Toolkit selbst — die Sessions konzentrieren sich auf Tooling-Entwicklung und Skill-Erstellung (Meta-Arbeit), nicht auf Anwendungsentwicklung.

### Nicht aufgerufene stemago-tools Skills

Alle 12 installierten `stemago-tools`-Skills wurden bisher nicht via Skill-Tool aufgerufen:

| Skill | Bewertung |
|-------|-----------|
| `beads-ready` | Kern-Workflow-Skill; in anderen Projekten wahrscheinlich aktiv |
| `browser-test` | Kein UI-Projekt im Zeitraum |
| `db-inspect` | Kein Datenbankprojekt aktiv — Kandidat zur Entfernung |
| `docs-lookup` | Nützlich bei Library-Recherche; bisher kein Bedarf |
| `github-ops` | Kein PR/Issue-Workflow initiiert |
| `interview` | Stattdessen `superpowers:brainstorming` genutzt |
| `land-the-plane` | Automatisch via `session-land-the-plane.sh`-Hook |
| `reflect-config` | Nie aufgerufen |
| `reflect` | Nie aufgerufen |
| `review` | Kein Code-Review-Workflow initiiert |
| `setup` | Einmaliger Setup-Skill; logisch selten |
| `usage-report` | Wird erstmalig jetzt (in diesem Lauf) eingesetzt |

---

## Agents — Einsatz

### Agents mit Meta-Daten (explizit dispatched)

| Agent | Aufrufe | Session | Beschreibung |
|-------|---------|---------|--------------|
| `stemago-tools:research-agent` | 2 | f0b9273b | Dokumentationsrecherche via Context7 |
| `general-purpose` | 11 | c3b65b3e (6×), f0b9273b (5×) | Generischer Agent ohne Spezialisierung |

### Breakdown der `general-purpose`-Einsätze

**Session f0b9273b (07.05.2026):**
- Eval reflect-config skill description (claude-sonnet-4-6, 1 Nachricht)
- Eval setup skill description (claude-sonnet-4-6, 1 Nachricht)
- Eval review skill description (claude-sonnet-4-6, 3 Nachrichten)
- Implement Plan-Task 1: setup skill (claude-haiku-4-5, 23 Nachrichten)
- Implement Plan-Task 2: reflect-config skill (claude-haiku-4-5, 20 Nachrichten)

**Session c3b65b3e (12.05.2026):**
- Eval 1 WITH skill: Standard usage-report (claude-sonnet-4-6)
- Eval 1 WITHOUT skill: Standard usage-report baseline (claude-sonnet-4-6)
- Eval 2 WITH skill: Months parameter (claude-sonnet-4-6)
- Eval 2 WITHOUT skill: Months parameter baseline (claude-sonnet-4-6)
- Eval 3 WITH skill: Cleanup focus (claude-sonnet-4-6)
- Eval 3 WITHOUT skill: Cleanup focus baseline (claude-sonnet-4-6)

### Agents ohne Meta-Daten (weitere 25 Subagent-Einsätze)

| Session | Subagents | Modell | Zeitraum |
|---------|-----------|--------|----------|
| 048ed8f4 | 3 | claude-sonnet-4-5 | vor Mai 2026 |
| 0d15181f | 3 | claude-sonnet-4-5 | vor Mai 2026 |
| 10b82f78 | 3 | claude-haiku-4-5 | Jan 2026 |
| 1e05af3d | 1 | claude-haiku-4-5 | vor Mai 2026 |
| 66eb2c4b | 1 | claude-sonnet-4-5 | vor Mai 2026 |
| 75c34620 | 2 | claude-haiku-4-5 | vor Mai 2026 |
| a1e8c7f8 | 6 | sonnet-4-5 + haiku-4-5 | vor Mai 2026 |
| a1efa54b | 2 | claude-opus-4-5 (1×) | vor Mai 2026 |
| aaa3f022 | 1 | claude-haiku-4-5 | vor Mai 2026 |
| cf7cd0e1 | 2 | opus-4-5 + sonnet-4-5 | vor Mai 2026 |
| f78dde43 | 1 | claude-haiku-4-5 | vor Mai 2026 |

### Nicht genutzte stemago-tools Agents

13 von 14 Agents wurden nie explizit eingesetzt:
`completion-gate`, `component-implementation-agent`, `devops-agent`, `enhanced-quality-gate`, `feature-implementation-agent`, `functional-testing-agent`, `infrastructure-implementation-agent`, `quality-agent`, `readiness-gate`, `task-checker`, `task-executor`, `task-orchestrator`, `tdd-validation-agent`

Der einzige genutzte stemago-tools Agent ist `research-agent` — zweimal eingesetzt für kontextbasierte Dokumentationsrecherche.

---

## Modell-Verteilung

### Gesamt (alle Sessions)

| Modell | Aufrufe | Anteil | Generation |
|--------|---------|--------|------------|
| `claude-sonnet-4-6` | 427 | 35.0% | aktuell |
| `claude-sonnet-4-5-20250929` | 288 | 23.6% | älter |
| `claude-opus-4-7` | 264 | 21.6% | aktuell |
| `claude-haiku-4-5-20251001` | 239 | 19.6% | älter |
| `claude-opus-4-5-20251101` | 2 | 0.2% | älter |
| **Gesamt** | **1.220** | **100%** | |

### Aktuelle Sessions (Mai 2026, nach Modell-Upgrade)

| Modell | Aufrufe | Herkunft |
|--------|---------|---------|
| `claude-opus-4-7` | 264 | Session f0b9273b (Orchestrierung/Planung) |
| `claude-sonnet-4-6` | 344 | Beide Sessions (Claude Code Client + Research-Agents + Evals) |
| `claude-haiku-4-5` | 28 | Subagenten für Skill-Implementierung (f0b9273b) |

In den aktuellen Sessions dominiert `claude-sonnet-4-6` als primäres Modell. `claude-opus-4-7` wurde ausschliesslich in der f0b9273b-Session eingesetzt — die intensive Planungs- und Konsolidierungs-Session (v2.0), was den hohen Opus-Anteil erklärt.

---

## Session-Übersicht

| Session | Datum | Schwerpunkt | Subagents |
|---------|-------|-------------|-----------|
| 8bf3da1 | Jan 2026 | Initiales Release | — |
| 10b82f78 | Jan 2026 | Plugin-Installation debuggen | 3 (haiku) |
| mehrere | Feb–Mär 2026 | Skill-Entwicklung v1.x (interview, review, docs-lookup etc.) | 20 (sonnet/haiku) |
| a1e8c7f8 | Mär 2026 | Skill-Optimierungen v1.4–1.5 | 6 (sonnet+haiku) |
| f0b9273b | 07.05.2026 | Plugin-Konsolidierung v2.0: Skill-Bereinigung, setup+reflect-config, Advisor-Integration | 7 |
| c3b65b3e | 12.05.2026 | Usage-Report Skill entwickeln und evaluieren | 6 |

---

## Empfehlungen

1. **`db-inspect` entfernen**: 0 Aufrufe über die gesamte Projektlaufzeit. Kein Datenbankprojekt aktiv. Falls ein DB-Projekt ansteht, kann der Skill leicht wieder hinzugefügt werden.

2. **`general-purpose`-Agenten systematisch ersetzen**: 11 von 13 Meta-Agenten-Einsätzen nutzen `general-purpose` statt spezialisierter Agents. Der `task-orchestrator` → `feature-implementation-agent`-Workflow ist konzipiert, aber noch nicht routiniert im Einsatz. Empfehlung: nächstes Feature-Projekt explizit mit `/stemago-tools:interview` + `task-orchestrator` starten.

3. **`stemago-tools:research-agent` ist der einzig bewährte Spezial-Agent**: Zweimal eingesetzt und bewährt. Dieser Workflow (research-agent für Context7-Recherche) sollte aktiv gefördert werden.

4. **Opus-Einsatz selektiv halten**: Die 264 Opus-4-7-Nachrichten aus f0b9273b sind für intensive Planungsphasen vertretbar — aber Implementierungs-Subagenten liefen korrekt auf `claude-haiku-4-5`, was kosteneffizient ist. Dieses Muster beibehalten.

5. **Usage-Report monatlich nutzen**: Jetzt, da der Skill gebaut wird, lohnt sich ein monatliches Review — insbesondere sobald das Toolkit in aktiven Anwendungsprojekten eingesetzt wird und Nutzungsdaten aussagekräftiger werden.

6. **`land-the-plane` manuell ergänzen**: Der Hook läuft automatisch am Session-Ende. Der Skill selbst wurde nie manuell aufgerufen. Mid-Session-Aufrufe vor langen Arbeitsphasen würden Kontext strukturierter sichern.

---

## Kontext-Hinweis

Da dieses Projekt das Toolkit selbst ist (Meta-Entwicklung), sind niedrige stemago-tools Skill-Nutzungszahlen strukturell erwartbar. Die eigentliche Nutzung der Skills findet in anderen Projekten statt (FamFlow, Vereinstool, SchoolAI etc.). Ein vollständiges Bild der Skill-Adoption würde eine projektübergreifende Auswertung erfordern.
