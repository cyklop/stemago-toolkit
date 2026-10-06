# Agent & Modell Analyse: stemago-toolkit — Mai 2026

> Statische Konfigurationsanalyse · 14 Agents · 12 Skills

---

## Übersicht

| Metrik | Wert |
|--------|------|
| Agents gesamt (konfiguriert) | 14 |
| Skills gesamt (konfiguriert) | 12 |
| Agents mit explizitem Modell | 4 |
| Agents ohne Modell-Angabe | 10 |
| Ghost-Agent-Referenzen | 4 nicht existierende Agents referenziert |

---

## Agents — Vollständige Liste

| Agent | Modell | Farbe | Von Skills/Agents genutzt |
|-------|--------|-------|---------------------------|
| `task-orchestrator` | sonnet | green | skills/interview |
| `task-executor` | sonnet | blue | task-orchestrator |
| `task-checker` | sonnet | yellow | (nicht direkt referenziert) |
| `research-agent` | sonnet | cyan | skills/interview, skills/review |
| `completion-gate` | (Standard) | purple | (nicht direkt referenziert) |
| `component-implementation-agent` | (Standard) | purple | task-orchestrator, task-executor |
| `feature-implementation-agent` | (Standard) | blue | task-executor |
| `infrastructure-implementation-agent` | (Standard) | orange | task-orchestrator, task-executor |
| `devops-agent` | (Standard) | orange | (nicht direkt referenziert) |
| `enhanced-quality-gate` | (Standard) | red | readiness-gate |
| `quality-agent` | (Standard) | yellow | skills/interview, skills/review |
| `readiness-gate` | (Standard) | orange | (nicht direkt referenziert) |
| `tdd-validation-agent` | (Standard) | red | task-orchestrator |
| `functional-testing-agent` | (Standard) | blue | (nicht direkt referenziert) |

---

## Modell-Verteilung (Konfiguration)

| Modell | Agents | Anteil |
|--------|--------|--------|
| Explizit `sonnet` | 4 | 29% |
| Standard (kein `model:`-Feld) | 10 | 71% |

**Hinweis**: Agents ohne `model:`-Angabe erben das Standardmodell der laufenden Claude-Instanz. Es gibt keinen einzigen Agent, der explizit Opus verwendet — das ist aus Kostenperspektive positiv.

Die vier Agents mit explizitem `model: sonnet` sind genau die zentral koordinierenden Agents:
- `task-orchestrator` — plant Parallelisierung, koordiniert Execution
- `task-executor` — delegiert an Implementierungs-Agents
- `task-checker` — QA-Spezialist, validiert Implementierungen
- `research-agent` — Context7-Recherche und Dokumentationssuche

---

## Overlap-Analyse: Doppelte QA-Systeme

Es gibt zwei parallele Qualitätsprüfungs-Systeme mit funktionaler Überschneidung:

### System A: quality-agent + completion-gate + readiness-gate (Mermaid-Graph-Stil)
- `quality-agent`: HANDOFF_TOKEN-basiertes Mermaid-System, routes to `@enhanced-project-manager-agent`
- `completion-gate`: Prüft Akzeptanzkriterien, ähnliches Format
- `readiness-gate`: Phasen-Übergang-Gate, routes to `@enhanced-project-manager-agent`

### System B: enhanced-quality-gate + tdd-validation-agent (Hub-and-Spoke-Stil)
- `enhanced-quality-gate`: Klares Hub-and-Spoke-Modell, gibt Kontrolle an Delegator zurück
- `tdd-validation-agent`: TDD-spezifische Validierung, deterministische Checks

**Problem**: System A referenziert `@enhanced-project-manager-agent` — ein Agent der nicht existiert. Diese Handoff-Pfade sind toter Code. System B folgt dem modernen Pattern und ist konsistent mit der CLAUDE.md-Architektur.

---

## Ghost-Referenzen: Nicht existierende Agents

| Referenzierter Agent | Referenziert von | Kontext |
|----------------------|------------------|---------|
| `@enhanced-project-manager-agent` | devops-agent, quality-agent, readiness-gate | Koordination nach Gate-Entscheidung |
| `@polish-implementation-agent` | quality-agent | Optimierung/Polish-Phase |
| `@testing-implementation-agent` | functional-testing-agent, tdd-validation-agent, task-orchestrator, task-executor | Unit-Testing |
| `@implementation-agent` | readiness-gate | Generische Implementierung bei Blockierung |

Diese Ghost-Referenzen entstammen einem früheren "kollektiven Agent"-Design, das nicht vollständig in die aktuelle Architektur überführt wurde.

---

## Tool-Inkonsistenz: context7-Benennung

| Schreibweise | Agents |
|--------------|--------|
| `mcp__context7__resolve-library-id` (Bindestrich) | component-implementation-agent, infrastructure-implementation-agent, research-agent, task-orchestrator |
| `mcp__context7__resolve_library_id` (Underscore) | task-checker, task-executor |

Beide Varianten sind inkonsistent — task-checker und task-executor sollten auf die Bindestrich-Variante vereinheitlicht werden.

---

## Empfehlungen

1. **Ghost-Agents auflösen**: Die Referenzen auf `@enhanced-project-manager-agent`, `@polish-implementation-agent`, `@testing-implementation-agent` und `@implementation-agent` sind tote Handoff-Pfade. Entweder echte Agent-Dateien erstellen oder auf existierende Agents (z.B. `task-orchestrator`) umleiten.

2. **Parallele QA-Systeme konsolidieren**: `quality-agent`, `completion-gate` und `readiness-gate` verwenden veraltetes Mermaid/HANDOFF_TOKEN-Routing und referenzieren nicht-existierende Agents. Prüfen ob sie durch `enhanced-quality-gate` + `tdd-validation-agent` ersetzt werden können.

3. **context7-Tool-Namen vereinheitlichen**: task-checker und task-executor auf `mcp__context7__resolve-library-id` (Bindestrich) angleichen.

4. **functional-testing-agent prüfen**: Referenziert 2 Ghost-Agents und wird von keiner Skill oder Orchestrierung aufgerufen. Falls Playwright-Testing nicht aktiv genutzt wird, Kandidat zum Entfernen.

5. **task-checker vs. enhanced-quality-gate konsolidieren**: Beide prüfen Implementierungsqualität (Build, Lint, Tests). task-checker ist nicht von Skills referenziert — klären ob er noch benötigt wird.

---

## Bereinigungskandidaten zusammengefasst

| Agent | Empfehlung | Begründung |
|-------|-----------|-----------|
| `quality-agent` | Überarbeiten oder entfernen | Mermaid-Style, Ghost-Agent-Route, überschneidet enhanced-quality-gate |
| `completion-gate` | Überarbeiten oder entfernen | Überschneidet enhanced-quality-gate, kein klares Alleinstellungsmerkmal |
| `readiness-gate` | Überarbeiten oder entfernen | Ghost-Agent-Routen, Phasen-Gate nicht im aktuellen Workflow |
| `functional-testing-agent` | Auf Aktivität prüfen | 2 Ghost-Referenzen, nicht von Skills genutzt |
| `task-checker` | Mit enhanced-quality-gate konsolidieren | Funktionale Überschneidung, nicht von Skills referenziert |
| `devops-agent` | Ghost-Referenz bereinigen | Eine Handoff-Route zu @enhanced-project-manager-agent bereinigen |

**Behalten (klar in Nutzung)**:
- `task-orchestrator`, `task-executor` — Kern der Ausführungspipeline
- `research-agent` — von interview und review Skills genutzt
- `component-implementation-agent`, `feature-implementation-agent`, `infrastructure-implementation-agent` — von task-executor/-orchestrator genutzt
- `enhanced-quality-gate`, `tdd-validation-agent` — modernes Hub-and-Spoke-Pattern, keine Ghost-Referenzen
