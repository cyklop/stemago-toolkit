# Design Spec: usage-report Skill

**Datum:** 2026-05-12  
**Status:** Approved

---

## Ziel

Ein Skill der analysiert, wie Skills, Agents und Modelle in Claude-Sessions eines Projekts genutzt werden. Erzeugt einen interpretierten Markdown-Report mit Empfehlungen. Kann manuell oder monatlich per `/schedule` ausgeführt werden.

---

## Architektur

```
/stemago-tools:usage-report [--project <path>] [--months <n>]
     │
     ├─ 1. Bash-Skript extrahiert Rohdaten aus Session-JSONLs
     │       → Skills, Agents, Models, Session-Metadaten als JSON
     │
     ├─ 2. Konfiguration des Projekts lesen
     │       → Welche Skills/Agents/Hooks sind konfiguriert?
     │       → Plugin-Manifest, hooks.json, sessions-index.json
     │
     └─ 3. Claude interpretiert Rohdaten + Konfiguration
             → Trend-Analyse, Gap-Analyse, Empfehlungen
             → Ausgabe im Terminal + Speichern als Markdown
```

---

## Argumente

| Argument | Default | Beschreibung |
|----------|---------|--------------|
| `--project <path>` | aktuelles Verzeichnis (`$CWD`) | Projekt-Pfad für die Analyse |
| `--months <n>` | `1` | Anzahl Monate rückwärts die analysiert werden |

---

## Datenquellen

### Session-JSONLs
Pfad: `~/.claude/projects/<project-hash>/*.jsonl`

Relevante Felder:
- `type: "assistant"` + `message.model` → verwendetes Modell
- `type: "assistant"` + `message.content[].type == "tool_use"` + `name == "Skill"` + `input.skill` → Skill-Aufrufe
- `type: "assistant"` + `message.content[].type == "tool_use"` + `name == "Agent"` + `input.subagent_type` → Agent-Aufrufe
- `timestamp` → Zeitraum-Filterung

### Projekt-Konfiguration (Gap-Analyse)
- `plugins/*/skills/*/SKILL.md` → installierte Skills (frontmatter `name`)
- `plugins/*/agents/*.md` → installierte Agents (frontmatter `name`)
- `plugins/*/.claude-plugin/plugin.json` → Plugin-Metadaten
- `plugins/*/hooks/hooks.json` → konfigurierte Hooks

### sessions-index.json
Pfad: `~/.claude/projects/<project-hash>/sessions-index.json`  
Liefert: Session-Metadaten (Datum, Zusammenfassung, messageCount)

---

## Rohdaten-Skript (Python, inline per Bash)

Das Skript berechnet:
```json
{
  "period": { "from": "2026-04-12", "to": "2026-05-12" },
  "sessions": [
    {
      "id": "uuid",
      "date": "2026-05-07",
      "summary": "Plugin installation...",
      "skill_calls": ["stemago-tools:interview", "superpowers:brainstorming"],
      "agent_calls": ["research-agent"],
      "models": { "claude-opus-4-7": 12, "claude-sonnet-4-6": 3 }
    }
  ],
  "totals": {
    "session_count": 18,
    "skill_counts": { "stemago-tools:interview": 12 },
    "agent_counts": { "research-agent": 5 },
    "model_counts": { "claude-opus-4-7": 45, "claude-sonnet-4-6": 12 }
  }
}
```

---

## Report-Format (Claude-generiert)

```markdown
# Usage Report: <Projektname> — <Monat Jahr>

## Übersicht
- N Sessions analysiert | Zeitraum: TT.MM–TT.MM.JJJJ
- N aktive Skills | N nie genutzte Skills | N Agents eingesetzt

## Skills — Nutzung
| Skill | Aufrufe | Anteil |
|-------|---------|--------|
| stemago-tools:interview | 12 | 48% |
| superpowers:brainstorming | 8 | 32% |
...

## Nicht genutzte Skills
Skills die installiert, aber im Zeitraum nicht aufgerufen wurden:
- `stemago-tools:db-inspect` — Kandidat zum Entfernen oder Deaktivieren

## Agents — Einsatz
...

## Modell-Verteilung
- claude-opus-4-7: 78% (N Aufrufe)
- claude-sonnet-4-6: 22% (N Aufrufe)

## Empfehlungen
1. [konkreter Handlungsvorschlag]
2. ...

## Monatliche Automatisierung
Um diesen Report monatlich automatisch zu erstellen:
> /schedule "Am 1. jeden Monats: /stemago-tools:usage-report ausführen"
```

---

## Monatliche Automatisierung

Der Skill erklärt am Ende wie man ihn via `/schedule` einrichtet.  
**Kein automatisches Setup** — User entscheidet selbst.

Empfohlener Cron: 1. jeden Monats, 09:00 Uhr.

---

## Skill-Metadaten

- **Name:** `usage-report`
- **Plugin:** `stemago-tools`
- **Pfad:** `plugins/stemago-tools/skills/usage-report/SKILL.md`
- **Argument-Hint:** `[--project <path>] [--months <n>]`
- **Trigger-Beschreibung:** Wenn User Nutzungsanalyse, Report über Skills/Agents/Modelle, oder monatliche Auswertung anfragt
