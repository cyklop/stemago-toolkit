# Prompt-Audit stemago-tools — 2026-09-03

Audit der Prompt-Oberfläche des Plugins auf veraltete Prompting-Muster („Cruft"), nach dem Verfahren aus `/claude-api prompt-audit`. Zwei Deliverables: dieser Report und der Patch `prompt-audit-2026-09-03.patch` im selben Ordner. **Status: Patch am 2026-09-03 vollständig angewendet** (Version 2.4.2 → 3.0.0, siehe `CHANGELOG.md`). Der Patch bleibt als Nachweis liegen; `git apply -R` nimmt ihn zurück.

## Annahmen (Schritt 0)

| | Annahme | Herleitung |
|---|---|---|
| **Scope** | Gesamte Prompt-Oberfläche des Repos: 21 `SKILL.md` + `interview/REFERENCE.md`, 14 Agent-Definitionen, 4 Hook-Skripte + `hooks.json`, `CLAUDE.md`, `AGENTS.md`, `.claude/learnings/project-learnings.md` (≈ 5.200 Zeilen) | Aufruf ohne Datei/Verzeichnis → ganzes Arbeitsverzeichnis |
| **Ziel-Modell** | Aktuelle Claude-Code-Generation: **Claude Fable 5.1** in der Hauptsession; Subagents über die Aliase `haiku` / `sonnet` / `opus` | Keine dokumentierte Migration; das Repo pinnt keine Modell-IDs (nur Aliase); die Session läuft auf Fable 5.1 |
| **Provider** | Ausschließlich Claude Code / Anthropic; keine Fremd-Provider-Marker gefunden | grep über das Repo |

Nicht im Scope: `docs/superpowers/**`, `CHANGELOG.md`, `usage-report-workspace/**` (Eval-Daten, erreichen das Modell nicht), die Hook-Skripte selbst (reine Klartext-Reminder, sauber).

## Provenienz (Schritt 2)

- **Alle 14 Agents stammen aus dem Initial-Commit `8bf3da1` (2026-01-26)** und wurden seitdem nur für die Umbenennung Taskmaster → Beads angefasst (`84c4f16`, `22b0d0d`) plus einmal `ff099d5` (Orchestrator/Executor, 2026-03-18). Sie sind Importe aus dem „claude-code-sub-agent-collective"-Template (Selbstbezeichnung in `task-checker.md:9`), geschrieben für die Modellgeneration Mitte 2025.
- **Die Skills sind jung** (Mai–Juli 2026) und weitgehend sauber. Befunde dort sind fast alle *faktische* Drift (CLI-Flags, Tool-Namen, Hook-Verhalten), kein Prompting-Stil.
- **Nutzung**: Der Usage-Report `docs/reports/usage-2026-05.md` zeigt 0 Aufrufe für 13 der 14 Agents; nur `research-agent` wurde genutzt. Fünf Agents werden von keinem Skill und keinem anderen Agent referenziert.

## Zusammenfassung

| Gruppe | Befunde | davon High |
|---|---|---|
| 1 — Veralteter Prompt-Text (Druck-Sprache, Choreografie, Grader-Vokabular, Fossilien) | 12 | 8 |
| 2 — Brüchige Skill-/Rule-Dateien (rottende Fakten, Projekt-Hardcodes) | 8 | 2 |
| 3 — Tool-/Agent-Verträge (Tool-Namen, Aufrufform, tote Referenzen) | 6 | 4 |
| 4 — Architektur (redundante Subagents, LLM für deterministische Checks) | 1 | 0 |
| Flag-only (Low) | 11 | — |

**Die drei wirksamsten Befunde:**

1. **`quality-agent` — der einzige Agent, den `/review`, `/interview` und der Orchestrator tatsächlich aufrufen — trägt ein System-Prompt aus einem Mermaid-Graphen, der ihm befiehlt, „den Endpunkt-Text exakt zu kopieren", vorher `mcp__beads__show` zu holen und mit `HANDOFF_TOKEN` zu antworten.** Der Aufrufer in `review/SKILL.md` verlangt dagegen eine Severity-Liste mit `Datei:Zeile`. Jeder `/review`-Lauf lässt den Subagent zwei unvereinbare Output-Verträge versöhnen. (H8)
2. **`task-orchestrator` widerspricht sich selbst**: Zeile 12 „Do NOT call Task() from an agent" gegen Zeile 372 „You MUST end your response with actual Task() tool calls", Zeile 369 „never through HANDOFF TO" gegen Zeile 388 „HANDOFF TO: @target-agent-name" — plus ein Hook (`handoff-automation.sh`), der die Tokens auswerten soll und nicht existiert. Dazu Taskmaster-Tools (`analyze_project_complexity`), die Beads nicht hat. (H1, H2)
3. **Tote Verträge in fast allen Agents**: Routing-Ziele, die es nicht gibt (`@enhanced-project-manager-agent`, `@polish-implementation-agent`, `testing-implementation-agent`, `task-generator-agent`, …), drei Protokoll-Dateien, die `research-agent` „IMMER zuerst" lesen soll und die nirgends existieren, Context7-Tool-Namen in drei Schreibweisen (aktuell ist `query-docs`), und MCP-Tools, die als Bash-Befehle notiert sind (`mcp__beads__show --id=<ID>`). (H3–H6)

Der Patch schrumpft die Agents von 2.141 auf 411 Zeilen (166 KB → 26 KB) — nicht als Selbstzweck, sondern weil praktisch jede entfernte Zeile eine der oben genannten Kategorien trifft. Kontext (Zuständigkeiten, Review-Gates, Status-Protokoll, Modellwahl) bleibt erhalten und ist an einer Stelle statt an vier.

---

## Befunde — High

### H1 · Sich widersprechende Endformate im Orchestrator
- **Ort:** `plugins/stemago-tools/agents/task-orchestrator.md:12` vs `:372`; `:369` vs `:388`; `:414`
- **Evidenz:** „Do NOT call Task() from an agent" ↔ „You MUST end your response with actual Task() tool calls"; „never through HANDOFF TO instructions" ↔ „HANDOFF TO: @target-agent-name"; „This format ensures the handoff-automation.sh hook detects your routing instruction" (kein solcher Hook in `hooks.json`)
- **Muster:** 1d Patch-Akkretion / nicht durchgesetzte Anweisung; drei „MANDATORY ENDING"-Blöcke (`:379-427`)
- **Warum obsolet:** Beide Fassungen stehen seit dem Initial-Import nebeneinander (git blame). Das Modell verbringt Aufwand damit, sich für eine zu entscheiden, und fällt unvorhersehbar. Subagents können in Claude Code keine Subagents starten — die Hub-Direktive (`:12-14`) ist die einzig funktionierende Variante.
- **Confidence:** High · **Aktion:** `rewrite` — ein Endformat (Hub-Direktive), siehe Patch

### H2 · Taskmaster-Fossilien mit falscher bd-Syntax
- **Ort:** `task-orchestrator.md:20,69,298-299,315`; `task-executor.md:12,20,22,56-58,160`; `readiness-gate.md:14`; `devops-agent.md:14`; `quality-agent.md:14`; `task-checker.md:157-161`
- **Evidenz:** „TASKMASTER "DONE" STATUS IS MEANINGLESS"; „GET TASKMASTER TASK DETAILS"; `analyze_project_complexity`, `complexity_report`; `mcp__beads__show --id=X --projectRoot=$(pwd)`; `bd update --id=<id> --prompt="…"`; Status `done`, `pending`, `review`
- **Muster:** 1d Fossil (abgelöstes Tooling) / 2 rottende Fakten
- **Warum obsolet:** Taskmaster wurde in `84c4f16`/`22b0d0d` durch Beads ersetzt; die Umbenennung hat diese Stellen ausgelassen. bd 1.1.0 kennt weder `--prompt` noch `--projectRoot` noch die Stati `done`/`review`/`pending` (verifiziert: `bd update --help` — Stati sind `open, in_progress, blocked, deferred, closed`).
- **Confidence:** High · **Aktion:** `rewrite` / `remove`

### H3 · Routing auf Agents, die es nicht gibt
- **Ort:** `readiness-gate.md:49,62,66`; `devops-agent.md:90`; `quality-agent.md:90,92`; `functional-testing-agent.md:19,21`; `task-executor.md:49`; `task-orchestrator.md:326`; `tdd-validation-agent.md:178`; `research-agent.md:31,39,141-157`
- **Evidenz:** `@enhanced-project-manager-agent`, `@polish-implementation-agent`, `@implementation-agent`, `testing-implementation-agent`, `task-generator-agent`, `prd-parser-agent`
- **Muster:** 1d Fossil / 3 hängende Referenz
- **Warum obsolet:** Keiner dieser Agents existiert in `agents/` (verifiziert). Jede Route dorthin endet im Nichts — der Agent erfindet einen Handoff oder bleibt stehen.
- **Confidence:** High · **Aktion:** `remove` / `rewrite`

### H4 · research-agent liest Protokoll-Dateien, die nicht existieren
- **Ort:** `research-agent.md:13-16, 91-97, 159, 166`
- **Evidenz:** „**FIRST**: I read the protocol documents … `.claude/docs/RESEARCH-CACHE-PROTOCOL.md` … `RESEARCH-BEST-PRACTICES.md` … `RESEARCH-EXAMPLES.md`"; „❌ Skip protocol documents (I always read them first)"
- **Muster:** 2 rottende Fakten / 1d Fossil
- **Warum obsolet:** Die Dateien existieren nirgends im Repo (`find`). Jeder Aufruf beginnt mit drei fehlschlagenden Reads, und die „Entscheidungsmatrix", nach der der Agent arbeiten soll, gibt es nicht. Das ist der einzige Agent mit realer Nutzung (2 Aufrufe im Mai).
- **Confidence:** High · **Aktion:** `rewrite` — Cache-first, Context7 vor Gedächtnis, Beispiele verbatim, Output-Schema; siehe Patch

### H5 · Context7-Tool-Namen in drei Schreibweisen, keine aktuell
- **Ort:** `research-agent.md:4,119,125`; `component-implementation-agent.md:4,89,93`; `infrastructure-implementation-agent.md:4,84,89,94`; `task-orchestrator.md:4`; `task-checker.md:4`; `task-executor.md:4,138-139`
- **Evidenz:** `mcp__context7__get-library-docs`, `mcp__context7__get_library_docs`, `mcp__context7__resolve_library_id`
- **Muster:** 3 Vertragsgenauigkeit / 2 rottende Fakten
- **Warum obsolet:** Context7 heißt heute `resolve-library-id` + `query-docs` — `docs-lookup/SKILL.md:12,19` nutzt bereits die richtigen Namen. Ein `tools:`-Grant auf einen nicht existierenden Namen gewährt nichts: der Agent wird zur Doku-Recherche aufgefordert und hat kein Tool dafür.
- **Confidence:** High · **Aktion:** `rewrite` (umbenennen). Hinweis: Der Präfix hängt von der Registrierung ab — `mcp__context7__` via `claude mcp add`, `mcp__plugin_context7_context7__` bei Installation als Plugin (so in dieser Session). Das betrifft auch `docs-lookup` (L11).

### H6 · MCP-Tools als Shell-Befehle notiert
- **Ort:** `component-implementation-agent.md:32,62`; `feature-implementation-agent.md:32,62`; `infrastructure-implementation-agent.md:32,57`; `task-executor.md:20,22`
- **Evidenz:** ```bash … mcp__beads__show --id=<PROVIDED_ID>``` als „MANDATORY FIRST ACTION"
- **Muster:** 3 Vertrags-Mismatch
- **Warum obsolet:** MCP-Tools werden als Tool-Call mit JSON-Argumenten aufgerufen, nicht in Bash; der Befehl schlägt fehl, und der Agent darf laut Prompt „ONLY THEN" weiterarbeiten.
- **Confidence:** High · **Aktion:** `rewrite`

### H7 · HANDOFF_TOKEN, „FORMAT FAILURE = failure", COLLECTIVE_HANDOFF_READY
- **Ort:** `readiness-gate.md:8,12,38-66,69-74`; `devops-agent.md:8,12,77-94,97-102`; `quality-agent.md:8,12,77-94,97-102`; `completion-gate.md:47-55`; `component-implementation-agent.md:154-157,163-167`; `feature-implementation-agent.md:137-141`; `infrastructure-implementation-agent.md:166-169`; `tdd-validation-agent.md:106-123,155-183`
- **Evidenz:** „HANDOFF_TOKEN: READINESS_READY_R8K7"; „FORMAT FAILURE: Missing any required section = readiness gate failure"; „Hook detects completion → Route to @tdd-validation-agent"; „COLLECTIVE_HANDOFF_READY"
- **Muster:** 1c Grader-Vokabular · 1d nicht durchgesetzte Anweisung · 1a Druck
- **Warum obsolet:** Die Tokens waren die Schnittstelle des Handoff-Hooks des Ursprungs-Templates; dieses Plugin hat ihn nie ausgeliefert (`hooks.json` hat drei Reminder und einen Blocker). Kein Codepfad prüft die Tokens. Den Bewertungsapparat statt der Anforderung zu beschreiben, lenkt Aufwand auf Formatkonformität statt auf die Arbeit.
- **Confidence:** High · **Aktion:** `remove`

### H8 · Mermaid-„Decision Path" als Ersatz für Urteilsvermögen
- **Ort:** `readiness-gate.md:8-104`; `devops-agent.md:8-128`; `quality-agent.md:8-128`
- **Evidenz:** „CRITICAL EXECUTION RULE: I must follow the mermaid decision path and output the COMPLETE CONTENT from the endpoint node I reach … copy it exactly as written"; Knoten wie „Conduct penetration testing", „Test application compatibility with NVDA, JAWS, and VoiceOver screen readers", „production load simulation and chaos engineering", „Implement Infrastructure as Code with Terraform"; Endpunkt-Texte mit vorgefertigten Ergebnissen („task completion 95%+ … testing coverage 85%+")
- **Muster:** 1c Schritt-für-Schritt-Choreografie für Urteilsaufgaben · 1b Exact-Output-Scaffold · 3 Vertrag ≠ Verhalten
- **Warum obsolet:** Der Graph schreibt pro Knoten sechs Pflichtschritte vor, die ein Subagent mit Read/Grep/Bash nicht ausführen kann, und der Endpunkt-Text ist eine Konserve, die der Agent unabhängig vom Befund kopieren soll — das Ergebnis ist vorgeschrieben, nicht beobachtet. Aktuelle Modelle planen ein Review selbst; das Skript ersetzt Urteil durch Template. **Höchste Wirkung bei `quality-agent`**: er wird von `review/SKILL.md:55-146` (haiku/sonnet), `interview/SKILL.md:122` und dem Orchestrator mit eigenen Output-Vorgaben aufgerufen, die dem System-Prompt widersprechen („ALWAYS get Beads task details first" bei einem Diff-Review ohne Task).
- **Confidence:** High · **Aktion:** `rewrite` — Prosa-Vertrag (Scope, Dimensionen, was verifiziert gilt, Output, PASS/FAIL-Modus); siehe Patch

### H9 · bd-Flags, die es nicht gibt
- **Ort:** `plugins/stemago-tools/skills/land-the-plane/SKILL.md:41,47,53`
- **Evidenz:** `bd list --status=closed --since=today --format=json`, `bd ready --format=json`, `bd blocked --format=json`
- **Muster:** 2 rottende Fakten
- **Warum obsolet:** bd 1.1.0 hat kein `--since`; `--format` nimmt `digraph`/`dot`/Go-Template, JSON ist das globale `--json` (verifiziert: `bd list --help`). Der Hook `session-land-the-plane.sh:35-38` weiß das bereits („bd 1.x kennt kein --format=count").
- **Confidence:** High · **Aktion:** `rewrite` → `bd list --status closed --closed-after "$(date +%F)" --json`, `bd ready --json`, `bd blocked --json`

### H10 · Text, der die Hook-Migration (v2.4.2) überlebt hat
- **Ort:** `CLAUDE.md:79-82`; `README.md` Hook-Tabelle; `reflect-config/SKILL.md:42,58-62,79-80`; `reflect/SKILL.md:117`
- **Evidenz:** „**SessionEnd**: Runs when session ends"; „Am Ende jeder Session wird automatisch analysiert"; „Die automatische Reflection wird durch den session-reflect Hook am Session-Ende ausgelöst"; „für automatische Reflection am Session-Ende"
- **Muster:** 1d Fossil
- **Warum obsolet:** `hooks.json` bindet `SessionStart` (startup/resume/clear); `session-reflect.sh:20` gibt nur eine Erinnerung aus. Nichts führt `/reflect` automatisch aus. Ein Modell, dem „automatisch" versprochen wird, überspringt den manuellen Aufruf.
- **Confidence:** High · **Aktion:** `rewrite`

### H11 · „Crisis Protocol" und Evidenz-Theater im Orchestrator
- **Ort:** `task-orchestrator.md:9-93` und `:301-365`
- **Evidenz:** „TDD VALIDATION CRISIS PROTOCOL — MANDATORY BLOCKING"; „AGENTS LIE ABOUT TDD COMPLETION"; „NO SHORTCUTS"; RED/GREEN/REFACTOR als „Orchestrierungs-Phasen"; „✅ mcp__beads__list executed [X] times with projectRoot"
- **Muster:** 1a Druck-Sprache (27 Caps-Marker in einer Datei) · 1c Grader-Vokabular · 1c Wiederholung als Verstärkung (die Regel „nicht schließen ohne Gates" steht viermal in abweichender Wortwahl)
- **Warum obsolet:** Register gegen Agents von Mitte 2025 getunt, die falsche Fertigmeldungen lieferten. Die eigentliche Regel steht einmal sauber im Two-Stage-Review-Abschnitt (`:105-153`, 2026-03-18) — für aktuelle Modelle reicht einmal; das Krisen-Register erzeugt einen ängstlichen, hedgenden Orchestrator, und das Evidenz-Template ist ein Selbstbericht, den niemand prüft.
- **Confidence:** High (Duplikate/unenforced) · Medium (Register) · **Aktion:** `rewrite`

---

## Befunde — Medium

### M1 · Redundante Subagents (Roster)
- **Ort:** `enhanced-quality-gate.md` ≡ `quality-agent.md` (gleiche Tools bis auf `getDiagnostics`, gleicher Auftrag, einziger Unterschied: binäres PASS/FAIL); `completion-gate.md` ≡ `task-checker.md` ≡ Gate 1 + Gate 3 des Orchestrator-Flows; `readiness-gate.md` = `bd stats` + `bd blocked` in ein LLM gewickelt; `task-executor.md` wiederholt Routing, Modellwahl und Status-Protokoll des Orchestrators wörtlich und kann als Subagent die Agents, für die er existiert, nicht starten
- **Evidenz:** Usage-Report 2026-05: 13 von 14 Agents 0 Aufrufe; keiner der fünf wird von einem Skill oder anderen Agent referenziert
- **Muster:** 4 redundante Spezialisten · 4 LLM als Executor eines deterministischen Plans (readiness-gate)
- **Warum obsolet:** Zwei Agents mit gleichem Auftrag und nahezu gleichem Prompt sind ein Agent, der den Unterschied als Input nimmt.
- **Confidence:** Medium (dokumentierte Gruppe-4-Zeile, Überlappung verifizierbar; Löschen ist deine Entscheidung) · **Aktion:** `remove` fünf Dateien + `move`: PASS/FAIL-Modus → `quality-agent`; Modellwahl-Heuristik + TASK-ASSIGNMENT-Template → `task-orchestrator`; Verifikations-Report → `tdd-validation-agent`. Jede Löschung ist ein eigener Hunk.

### M2 · 🚨-Druck und Test-Obergrenze in den Implementation-Agents
- **Ort:** `component-implementation-agent.md:12-36,45-48`; `feature-implementation-agent.md:12-36,45-48`; `infrastructure-implementation-agent.md:12-36,124`
- **Evidenz:** „🚨 CRITICAL: MANDATORY TASK FETCHING PROTOCOL … I MUST … ONLY THEN"; „🚨 CRITICAL: MAXIMUM 5 TESTS ONLY"
- **Muster:** 1a Druck · 1f numerische Obergrenze
- **Warum obsolet:** Die Task-ID-Pflicht ist ein echter Vertrag (bleibt, in Normallautstärke). „Maximal 5 Tests" kodiert „baue keine erschöpfende Suite, bevor die Implementierung steht" — das befolgen aktuelle Modelle als Absicht; die harte Zahl lässt den Agent bei 5 aufhören, wenn die Akzeptanzkriterien 7 brauchen.
- **Confidence:** Medium · **Aktion:** `rewrite` („die wenigen Tests, die das Kernverhalten festnageln")

### M3 · Stack- und Umgebungsannahmen des Template-Autors
- **Ort:** `infrastructure-implementation-agent.md:51,116,120,128` („WSL2"); `feature-implementation-agent.md:85,110` („React Context, Zustand, or Redux"); `component-implementation-agent.md:90,132-133` („vanilla javascript", „Jest, Testing Library, Cypress", „Create React App"); `infrastructure-implementation-agent.md:83-97` (Vite/React/TS hart verdrahtet); `research-agent.md:129` („best practices 2025")
- **Muster:** 2 rottende Spezifika / Recency-Trap
- **Warum obsolet:** Die Skills des Plugins dokumentieren einen Next.js/Prisma/DaisyUI/Vitest/Playwright-Stack (`docs-lookup:33-45`); hart kodierte Fremd-Stacks lenken Recherche auf die falschen Libraries; WSL2 ist auf macOS irrelevant.
- **Confidence:** Medium · **Aktion:** `rewrite` („dem bestehenden Stack des Projekts folgen")

### M4 · task-checker: Herkunfts-Narrativ, Tugend-Padding, widersprüchliche Schwellen
- **Ort:** `task-checker.md:9,35,37,121` („our claude-code-sub-agent-collective standards", „Hub-and-Spoke Verification"); `:141-145` („BE THOROUGH / BE SPECIFIC / BE FAIR / BE CONSTRUCTIVE / BE EFFICIENT"); `:119` („>90% coverage" — gegen die 5-Test-Grenze der Implementer); `:147-153` (Tool-Liste dupliziert Frontmatter; „NEVER use Write/Edit" ist bereits durch den Grant erzwungen)
- **Muster:** 1d Historien-Narrativ · 1c generische Tugenden · 1d Patch-Akkretion (Schwellen widersprechen sich) · 1d bereits im Code erzwungen
- **Confidence:** Medium · **Aktion:** durch M1 abgedeckt (`remove`); falls behalten: `rewrite`

### M5 · AGENTS.md in Alarm-Register, Duplikat von CLAUDE.md
- **Ort:** `AGENTS.md:17-39`
- **Evidenz:** „you MUST complete ALL steps", „MANDATORY WORKFLOW", „CRITICAL RULES", „NEVER stop before pushing", „NEVER say 'ready to push when you are'" (7 Caps-Marker auf 40 Zeilen); `CLAUDE.md:144-153` sagt dasselbe in Normallautstärke
- **Muster:** 1a Druck · Duplikate, die sich im Register widersprechen
- **Warum obsolet:** Aktuelle Modelle befolgen die schlichte Aussage; das ängstliche Register färbt auf den Output ab. Hinweis: von `bd onboard` generiert — eine Neu-Generierung bringt es zurück.
- **Confidence:** Medium · **Aktion:** `rewrite`

### M6 · `sequential-thinking` als „Core MCP: Reasoning"
- **Ort:** `setup/SKILL.md:41,213,237`
- **Muster:** 1b Scaffold, das ein API-Feature ersetzt („use the think tool to plan")
- **Warum obsolet:** Adaptives Thinking ist auf dem Ziel-Modell immer an; ein permanent geladenes externes Think-Tool kostet in jeder Session Schema-Tokens und lädt zu Über-Planung ein.
- **Confidence:** Medium · **Aktion:** `rewrite` — aus „Core" nach „Optional, nur auf Wunsch"

### M7 · Generierter CLAUDE.md-Block schreit
- **Ort:** `setup/SKILL.md:69-73`
- **Evidenz:** „IMMER zuerst eine Task-Liste … NIEMALS eine Aufgabe als erledigt melden bevor ALLE Tasks completed sind"
- **Muster:** 1a Druck (in einer Rule-Datei, die der Skill in jedes neue Projekt schreibt)
- **Confidence:** Medium · **Aktion:** `rewrite` mit Begründung („so überlebt der Fortschritt einen Compact")

### M8 · `advisor()` — Aufruf einer Funktion, die es nicht gibt
- **Ort:** `interview/SKILL.md:106-108` (unbedingt); `review/SKILL.md:151-153` („falls verfügbar")
- **Muster:** 2 rottende Spezifika
- **Warum obsolet:** Kein solches Tool in der aktuellen Claude-Code-Toolliste (verifiziert in dieser Session); Anthropics „advisor" ist ein Server-Tool der Messages API, kein Claude-Code-Tool. Der unbedingte Aufruf in `interview` lässt das Modell entweder so tun als ob oder scheitern.
- **Confidence:** Medium · **Aktion:** `rewrite` — Zweck behalten (Konsistenz-Check vor der Spec; False-Positive-Check nach den Review-Agents), Funktionsaufruf entfernen

### M9 · Orchestrator-Prompt verlangt, was ein Subagent nicht kann
- **Ort:** `interview/REFERENCE.md:156-168`
- **Evidenz:** „Alle unabhängigen Tasks PARALLEL über spezialisierte Agents starten"
- **Muster:** 3 Vertrags-Mismatch
- **Warum obsolet:** Subagents können in Claude Code keine Subagents starten (das sagt `task-orchestrator.md:12` selbst). Der Skill muss als Hub agieren.
- **Confidence:** Medium · **Aktion:** `rewrite` (Hub-Muster: Orchestrator plant, Skill startet)

### M10 · Wort-Obergrenzen in den STORM-Lens-Prompts
- **Ort:** `storm-research/SKILL.md:33,35,37,39,41` („Under 400 words."), `:79` („Under 280 words.")
- **Muster:** 1f numerische Output-Obergrenze
- **Warum obsolet:** Caps gegen Padding getunt; auf dem Ziel-Modell kappen sie die Evidenz-Bullets, von denen die Synthese lebt. **Einschränkung:** Der Skill markiert die Prompts als „kalibriert — nicht übersetzen" (2026-07-06). Das ist der Hunk, den du am ehesten ablehnst — dann behalten und die Kalibrierung mit/ohne Cap einmal vergleichen.
- **Confidence:** Medium · **Aktion:** `rewrite` („Keep it tight: a brief, not an essay.")

### M11 · Projekt-Hardcodes in generischen MCP-Wrapper-Skills
- **Ort:** `db-inspect/SKILL.md:18,24-25,31-32,44-54` (`volleyball_dev`, `Tournament`, `Registration`); `github-ops/SKILL.md:16-115` (`Match_Admin`, `username` ×11); `browser-test/SKILL.md:16,109` (`/admin/tournaments`, „Port 3000")
- **Muster:** 2 rottende Spezifika / Recency-Trap in einem Plugin für alle Projekte
- **Warum obsolet:** Beispiele sind das stärkste Signal im Prompt — das Modell matcht sie und zielt auf Tabellen/Repos, die es im nächsten Projekt nicht gibt.
- **Confidence:** Medium · **Aktion:** `rewrite` (Platzhalter)

### M12 · `Task`/`TodoWrite` als Tool-Namen
- **Ort:** `task-executor.md:4,13,21,46-49,137,145-155`; `task-orchestrator.md:4,12,76,83,89,324-326,369-374`; `task-checker.md:4`; `research-agent.md:21`
- **Muster:** 2 rottende Spezifika
- **Warum obsolet:** Das Subagent-Tool heißt in aktuellem Claude Code `Agent` (die Skills nutzen bereits `Agent(...)`); `TodoWrite` ist nicht in der aktuellen Toolliste. Ein Grant auf einen nicht existierenden Namen gewährt nichts.
- **Confidence:** Medium (Umbenennung in dieser Session verifizierbar; Aliasing in anderen Versionen nicht ausgeschlossen) · **Aktion:** `rewrite` — durch Orchestrator-Rewrite und Löschungen abgedeckt

### M13 · functional-testing-agent soll mit Context7 recherchieren — ohne Context7
- **Ort:** `functional-testing-agent.md:27`
- **Muster:** 3 Vertrags-Mismatch (Tool nicht im Grant)
- **Confidence:** Medium · **Aktion:** `remove`

### M14 · tdd-validation-agent: hart kodierte npm-Skripte, Tasks erzeugen ohne `create`, Hook-Architektur
- **Ort:** `tdd-validation-agent.md:26-40` (`npm run test:unit / test:integration / test:e2e / typecheck`); `:88` („generate specific Beads tasks" — kein `mcp__beads__create` im Grant); `:106-123` („Two-Checkpoint Architecture … Hook detects completion")
- **Muster:** 2 rottende Spezifika · 3 Vertrag · 1d Fossil
- **Confidence:** Medium/High · **Aktion:** `rewrite` — Skripte aus `package.json` lesen, Remediation als dispatch-fertige Liste, Hook-Abschnitt entfernen

---

## Flag-only (Low) — keine Änderung vorgeschlagen

- **L1** Nacktes `$ARGUMENTS` am Dateiende (`beads-ready:99`, `reflect:120`, `reflect-config:158`, `land-the-plane:199`, `review:244`, `setup:275`, `usage-report:205`) — Idiom aus der Commands-Ära; bei Skills, die `$ARGUMENTS` schon in der Prosa auswerten, doppelte Injektion. Harmlos.
- **L2** Drei „WICHTIG"-Marker in `review/SKILL.md:100,149,212`, Caps in `interview:13-16` — milde 1a-Dichte, jeweils mit Grund in der Nähe.
- **L3** Versions-Pins „Next.js 15", „React 19" in `docs-lookup:49-58,83` — illustrativ, rotten mit der Zeit.
- **L4** `docs-lookup:84` „Max 3 Calls" — Kostenbudget für Tool-Calls, plausibel.
- **L5** Beispiel-Modell-IDs `claude-opus-4-7`/`claude-sonnet-4-6` in `usage-report:48,55,162-163` — Beispieldaten, keine Pins.
- **L6** `github-ops:162` `mcp__github__get_pull_request_status` — nicht verifizierbar (GitHub-MCP hier nicht verbunden).
- **L7** `land-the-plane:58-62` `/recap` — gehedged; Existenz nicht verifiziert.
- **L8** `setup:70,73` `TaskCreate`/`TaskList` — in dieser Session nicht in der Toolliste sichtbar; nicht verifizierbar.
- **L9** `interview/SKILL.md:85` Anti-Rationalisierungs-Absatz („Diese Rationalisierungen zählen NICHT: …") — Prohibitions-Cluster, aber am 2026-07-06 gegen einen *demonstrierten* Fehler der aktuellen Generation eingefügt (`66e2f31`). **Behalten**; erst auf Fable 5.1 nachtesten, dann ggf. kürzen.
- **L10** `block-destructive-commands.sh:17` Kommentar „similar to test-driven-handoff.sh pattern" — Skript existiert nicht; nur Kommentar.
- **L11** Context7-Präfix ist umgebungsabhängig (`mcp__context7__` vs `mcp__plugin_context7_context7__`); betrifft `docs-lookup` und die korrigierten Agent-Grants gleichermaßen.

## Bewusst nicht geflaggt (Keep-Liste)

- **Skill-Descriptions mit Trigger-Phrasen-Listen** („Auch bei: …") — Routing-Text, gegen einen Trigger-Eval getunt (`64e3375`, `73346d5`). Bleibt.
- **`caveman`** — die Verbotsliste *ist* das Produkt (vom User eingeschalteter Stilmodus).
- **`grill-me:21-28`** („nicht verhandelbar", „niemals batchen") — eine betonte Regel mit Grund (Kontextverlust).
- **`diagnose:151-157`** Anti-Pattern-Recap — einmalige Schlussrekapitulation.
- **Two-Stage Review und Implementer-Status-Protokoll** im Orchestrator — echtes Protokoll mit Gründen; im Rewrite erhalten.
- **Hook-Skripte** — knappe Einzeiler, so wie sie sein sollen.
- **Skills Mai–Juli 2026** (`grill-me`, `roast`, `to-beads`, `prototype`, `zoom-out`, `architecture-review`, `diagnose`, `storm-research` bis auf M10, `usage-report`, `beads-ready`) — sauber, keine Änderung.

## Gruppe 4 — Hinweise ohne Diff

- **Token-Accounting:** `usage-report` zählt Aufrufe pro Skill/Agent/Modell, keine Tokens. Für Roster-Entscheidungen reicht das; die Token-Kosten pro Agent (z. B. 166 KB Agent-Prompts) bleiben unsichtbar.
- **Caching:** Keine Befunde — Plugin-Inhalte laden on demand, Hook-Output ist sessionbezogen.

---

## Vorgeschlagener Diff (Schritt 6)

Datei: `docs/reports/prompt-audit-2026-09-03.patch` — 28 Dateien, +305 / −2.063, `git apply --check` gegen den aktuellen Working Tree: sauber.

| Bereich | Änderung |
|---|---|
| **Rewrite** (H1, H2, H4, H5, H6, H7, H8, H11, M2, M3, M12, M13, M14) | `task-orchestrator`, `quality-agent`, `devops-agent`, `research-agent`, `tdd-validation-agent`, `functional-testing-agent`, `component-`/`feature-`/`infrastructure-implementation-agent` |
| **Löschen + Einfalten** (M1) | `completion-gate`, `readiness-gate`, `enhanced-quality-gate`, `task-executor`, `task-checker` |
| **Fakten-Fixes** (H9, H10, M8, M9) | `land-the-plane`, `reflect`, `reflect-config`, `CLAUDE.md`, `README.md`, `interview/SKILL.md`, `interview/REFERENCE.md`, `review` |
| **Register / Scaffold** (M5, M6, M7, M10) | `AGENTS.md`, `setup`, `storm-research` |
| **Platzhalter** (M11) | `db-inspect`, `github-ops`, `browser-test` |

Anwenden — alles oder selektiv:

```bash
# alles
git apply docs/reports/prompt-audit-2026-09-03.patch

# nur bestimmte Dateien
git apply --include='plugins/stemago-tools/agents/quality-agent.md' \
          --include='plugins/stemago-tools/skills/land-the-plane/SKILL.md' \
          docs/reports/prompt-audit-2026-09-03.patch

# alles außer den Löschungen
git apply --exclude='plugins/stemago-tools/agents/*-gate.md' \
          --exclude='plugins/stemago-tools/agents/task-executor.md' \
          --exclude='plugins/stemago-tools/agents/task-checker.md' \
          docs/reports/prompt-audit-2026-09-03.patch
```

**Entscheidungen im Patch, die du kippen kannst:**
- `research-agent` bekommt `Write` (nur `docs/research/`), damit er cachen kann, wie es der Prompt schon vorher verlangte — Tool-Erweiterung.
- `task-orchestrator` verliert `Task` und die Context7-Tools (Hub-Muster; er recherchiert nicht selbst).
- `quality-agent` bekommt `mcp__ide__getDiagnostics` (aus `enhanced-quality-gate` gefaltet).
- Agents bleiben Englisch (wie bisher), Skill-Edits Deutsch; die deutschen Review-Prompts im Orchestrator sind unverändert.

**Nach dem Anwenden:** Version bumpen (drei Dateien: `plugin.json`, `CLAUDE.md`, `marketplace.json`) — das Entfernen von Agents ist nach deiner Konvention ein Breaking Change → 3.0.0; `README.md` Skill-Zähler („11 Skills") ist unabhängig davon veraltet.

## Verifikation (Schritt 7) — Entfernen ist eine Hypothese

1. **`/review` auf einem kleinen echten Diff** vor und nach dem `quality-agent`-Rewrite: Liefert der Subagent die Severity-Liste mit `Datei:Zeile`, die der Skill verlangt, ohne HANDOFF-Präambel?
2. **`/interview` einmal bis Schritt 6** durchspielen: Kommt vom Orchestrator eine Hub-Direktive zurück, und startet der Skill die genannten Agents parallel?
3. **`storm-research`** ein Thema mit und ohne Wort-Cap laufen lassen und die Briefs vergleichen — erst dann M10 übernehmen oder verwerfen.
4. **`/land-the-plane`** einmal ausführen: Die drei bd-Befehle müssen JSON liefern.
5. Bei jedem neuen Modell-Release erneut auditieren; die Agent-Dateien sind Modell-Artefakte.
