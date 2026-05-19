# Usage Report: stemago-toolkit Skills & Claude Code Activity
**Zeitraum:** 2026-02-12 bis 2026-05-12 (letzte 3 Monate)  
**Erstellt:** 2026-05-12  
**Datenquelle:** `~/.claude/history.jsonl`, `~/.claude/stats-cache.json`, Plugin-Metadaten

---

## Executive Summary

In den letzten 3 Monaten wurden **3.699 Interaktionen** in **224 Sessions** über **16 aktive Projekte** verzeichnet. Das meistgenutzte stemago-Skill ist `/interview` mit 114 Aufrufen — klar dominanter Workflow. Die Nutzung ist im März am stärksten, bricht im April/Mai deutlich ein.

---

## 1. Gesamtaktivität

| Metrik | Wert |
|---|---|
| Zeitraum | 2026-02-12 – 2026-05-12 |
| Gesamte Interaktionen | 3.699 |
| Sessions | 224 |
| Tool-Calls | 74.573 |
| Aktive Tage | 77 |
| Projekte | 16 |

### Aktivität nach Monat

| Monat | Interaktionen | Sessions | Tool-Calls | Aktive Tage |
|---|---|---|---|---|
| Feb 2026 (ab 12.) | 11.386 | 18 | 3.577 | 5 |
| Mär 2026 | 56.325 | 159 | 52.457 | 22 |
| Apr 2026 | 29.775 | 43 | 18.004 | 19 |
| Mai 2026 (bis 12.) | 1.555 | 4 | 535 | 3 |

> Hinweis: Die Interaktionszahlen aus stats-cache.json weichen von den history.jsonl-Einträgen ab, da stats-cache alle Nachrichten (User + Assistant) zählt, history.jsonl nur User-Inputs.

### Aktivste Wochen

| Woche | Interaktionen |
|---|---|
| 2026-W12 (16.–22. Mär) | 624 |
| 2026-W11 (9.–15. Mär) | 511 |
| 2026-W13 (23.–29. Mär) | 496 |
| 2026-W14 (30. Mär–5. Apr) | 417 |
| 2026-W15 (6.–12. Apr) | 376 |

---

## 2. Projektaktivität

| Projekt | Interaktionen |
|---|---|
| OfficePal | 863 |
| FamFlow | 541 |
| AILearning | 429 |
| BOTC_WB | 372 |
| cbk | 335 |
| Match_Admin | 286 |
| rememberme | 178 |
| Baruthia | 127 |
| PP_dice | 116 |
| trotzdemworks | 110 |
| trotzdemworks_tools | 98 |
| StorytellerPP | 74 |
| BattleMP | 69 |
| stemago-toolkit | 60 |
| Vereinstool | 32 |
| PraxiGo | 9 |

---

## 3. Skill-Nutzung (stemago-tools)

### Stemago Skills im Überblick

| Skill | Aufrufe | Hauptprojekte |
|---|---|---|
| `/interview` | **114** | OfficePal (30x), AILearning (18x), FamFlow (21x) |
| `/reflect` | 6 | FamFlow (3x), Match_Admin (2x), OfficePal (1x) |
| `/reflect-on` | 1 | OfficePal |

**Nicht genutzt** (verfügbar, aber 0 Aufrufe): `/review`, `/land-the-plane`, `/beads-ready`, `/browser-test`, `/db-inspect`, `/docs-lookup`, `/github-ops`, `/setup`, `/reflect-config`

### `/interview` — Detailanalyse

Das mit Abstand meistgenutzte stemago-Skill. Es deckt den kompletten Feature-Planungs-Workflow ab (Interview → Spec → Tasks).

| Monat | Aufrufe |
|---|---|
| Feb 2026 | 25 |
| Mär 2026 | 74 |
| Apr 2026 | 15 |

**Top-Projekte (gesamt):**
- OfficePal: 30x
- FamFlow: 22x
- AILearning: 18x
- StorytellerPP: 9x
- BOTC_WB: 6x
- PP_dice: 6x
- BattleMP: 4x
- Match_Admin: 8x

---

## 4. Alle Slash-Commands (vollständige Übersicht)

Enthält Claude-interne Commands (/exit, /clear, /resume) und Skills.

| Command | Aufrufe | Kategorie |
|---|---|---|
| `/exit` | 167 | System (Session beenden) |
| `/interview` | 114 | **stemago-Skill** |
| `/rate-limit-options` | 88 | System (Rate-Limit-Handling) |
| `/resume` | 84 | System (Session fortsetzen) |
| `/clear` | 65 | System (Kontext leeren) |
| `/plugin` | 12 | System (Plugin-Management) |
| `/model` | 11 | System (Modell wechseln) |
| `/init` | 7 | System (Projekt initialisieren) |
| `/status` | 6 | System |
| `/mcp` | 6 | System |
| `/effort` | 6 | System |
| `/reflect` | 5 | **stemago-Skill** |
| `/memory` | 5 | System |
| `/reload-plugins` | 3 | System |
| `/config` | 3 | System |
| `/advisor` | 3 | System |
| `/reflect-on` | 1 | **stemago-Skill (deprecated)** |
| `/skill-creator` | 1 | Plugin (skill-creator) |

---

## 5. Installierte Plugins

| Plugin | Version | Installiert am | Zuletzt aktualisiert |
|---|---|---|---|
| stemago-tools@stemago-toolkit | 2.0.1 | 2026-02-08 | 2026-05-07 |
| skill-creator@claude-plugins-official | unknown | 2026-03-06 | 2026-03-25 |
| superpowers@claude-plugins-official | 5.1.0 | 2026-03-17 | 2026-05-07 |
| context7@claude-plugins-official | unknown | 2026-03-17 | 2026-03-25 |
| code-review@claude-plugins-official | unknown | 2026-03-17 | 2026-03-25 |
| code-simplifier@claude-plugins-official | 1.0.0 | 2026-03-17 | 2026-03-17 |
| warp@claude-code-warp | 2.0.0 | 2026-04-10 | 2026-04-10 |

**Plugin-Milestones:**
- **2026-02-08**: stemago-tools initial installiert (v1.x)
- **2026-03-06**: skill-creator installiert
- **2026-03-17**: superpowers, context7, code-review, code-simplifier als Paket installiert
- **2026-04-10**: warp installiert
- **2026-05-07**: stemago-tools auf v2.0.1 aktualisiert (Skill-Konsolidierung)

---

## 6. Plugin-Versionen & Entwicklung (stemago-toolkit)

| Datum | Version | Highlights |
|---|---|---|
| 2026-02-08 | 1.x | Initial-Installation |
| 2026-03-07 | 1.4.0 | Skill-Beschreibungen optimiert (besseres Triggering) |
| 2026-03-15 | 1.4.x | Context7 in interview + review integriert |
| 2026-03-18 | 1.5.0 | Superpowers-Pattern in Skills integriert |
| 2026-05-07 | 2.0.0 | Breaking: Skill-Konsolidierung (init-project/beads-setup/mcp-setup → setup) |
| 2026-05-07 | 2.0.1 | Advisor-Guidance + /recap in Workflow-Skills |

---

## 7. Modell-Nutzung

Der `/model`-Command wurde 11x aufgerufen, hauptsächlich im März/April. Auffällige Entries:

- `/model sonet` / `/model Sonet` — Tippfehler bei Sonnet-Auswahl (2026-03-30, 2026-04-10)
- `/model opus` — Explizit Opus gewählt (2026-03-31, Baruthia)
- `/model auto` — Auto-Modus (2026-04-10, cbk)

Kein konsistentes Muster — Modell-Wechsel wurden situativ vorgenommen, nicht systematisch.

---

## 8. Erkenntnisse & Bewertung

### Was funktioniert gut
- **`/interview`** ist fest im Workflow etabliert — wird project-übergreifend für Feature-Planung genutzt
- **Hohe Kontinuität** über 3 Monate in 16 verschiedenen Projekten
- **März** war der produktivste Monat (22 aktive Tage, 159 Sessions)

### Untergenutzte Skills
Folgende Skills sind verfügbar, tauchen im Zeitraum aber **gar nicht** in der history.jsonl auf:
- `/review` (stemago) — Könnte nach Code-Änderungen stärker eingesetzt werden
- `/land-the-plane` — Session-Abschluss-Workflow, stattdessen wird meist /exit benutzt
- `/beads-ready` — Kein Einsatz, obwohl Beads als Issue-Tracker konfiguriert ist
- `/browser-test`, `/db-inspect`, `/docs-lookup`, `/github-ops` — Spezialisierte Skills ohne Nutzung

### Reflexions-Nutzung
Mit nur 6 `/reflect`-Aufrufen in 3 Monaten wird das explizite Session-Learning selten genutzt. Die automatisch angelegten `project-learnings.md`-Dateien existieren in 6 Projekten, was auf Hook-triggered Reflection hindeutet.

### Rate-Limit-Vorfälle
88 `/rate-limit-options`-Aufrufe konzentrieren sich auf OfficePal (39x) und Match_Admin/StorytellerPP. Dies deutet auf intensive Sessions mit hohem Token-Verbrauch in diesen Projekten hin.

---

## 9. Empfehlungen

1. **`/land-the-plane` etablieren**: Statt `/exit` als Session-Abschluss nutzen — sichert Kontext und TODO-State
2. **`/beads-ready` als Session-Start**: Zeigt offene Tasks — aktuell nicht im Workflow integriert
3. **`/reflect` Häufigkeit erhöhen**: Bei produktiven Sessions (10+ Interaktionen) als Gewohnheit
4. **`/review` nach Implementierungen**: Aktuell kein systematisches Code-Review nach Feature-Entwicklung erkennbar
5. **Modell-Konsistenz**: Die verschiedenen Tippfehler bei `/model` deuten auf manuelle Wechsel hin — ggf. default model fest setzen

---

*Report generiert via history.jsonl Analyse (3.699 Einträge) + stats-cache.json (99.041 Messages) + Plugin-Metadaten*
