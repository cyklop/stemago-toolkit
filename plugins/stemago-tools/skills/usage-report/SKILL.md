---
name: usage-report
description: "Wertet Claude-Session-Daten aus und zeigt welche Skills, Agents und Modelle tatsächlich genutzt werden — im Unterschied zu dem was nur konfiguriert ist. Erstellt einen strukturierten Report mit Gap-Analyse und konkreten Empfehlungen zum Bereinigen oder Optimieren des Claude-Setups. Nutze diesen Skill immer wenn der User wissen will welche Skills oder Agents wirklich in Verwendung sind, ob installierte Tools überhaupt aufgerufen werden, was aus dem claude-Setup entfernt werden kann, welche Modelle eingesetzt werden, oder wie das Claude-Tooling im Projekt genutzt wird — auch bei vagen Formulierungen wie 'was nutze ich eigentlich', 'sind alle Skills in Gebrauch', 'claude-setup aufräumen', 'ungenutzte Agents finden', 'welche Tools werden wirklich verwendet', 'Auswertung der claude-Nutzung', oder wenn jemand seinen Skill/Agent-Bestand bereinigen möchte."
argument-hint: "[--project <path>] [--months <n>]"
---

# /stemago-tools:usage-report

Erstelle eine Nutzungsauswertung für Claude-Skills, -Agents und -Modelle in diesem Projekt.

## Argumente aus `$ARGUMENTS` lesen

Bevor du startest, parse die Argumente:
- `--project <path>` — zu analysierender Projekt-Pfad (Standard: aktuelles Verzeichnis)
- `--months <n>` — Anzahl Monate rückwärts (Standard: 1)

Wenn kein `--project` angegeben ist, verwende den Pfad des aktuellen Arbeitsverzeichnisses (`pwd`).

---

## Schritt 1: Rohdaten extrahieren

Führe das Extraktions-Skript aus. Das Skript liegt relativ zum SKILL.md:

```bash
SKILL_DIR="$(dirname "$CLAUDE_SKILL_PATH")"
PROJECT_PATH="$(pwd)"  # oder den --project Wert aus $ARGUMENTS
MONTHS=1               # oder den --months Wert aus $ARGUMENTS

python3 "$SKILL_DIR/scripts/extract_session_data.py" \
  --project "$PROJECT_PATH" \
  --months "$MONTHS"
```

Das Skript gibt JSON auf stdout aus mit dieser Struktur:
```json
{
  "project": "/pfad/zum/projekt",
  "period": { "from": "2026-04-12", "to": "2026-05-12", "months": 1 },
  "sessions": [
    {
      "id": "uuid",
      "date": "2026-05-07",
      "summary": "Kurzbeschreibung der Session",
      "message_count": 42,
      "skill_calls": ["stemago-tools:interview", "superpowers:brainstorming"],
      "agent_calls": ["research-agent"],
      "model_counts": { "claude-opus-4-7": 12, "claude-sonnet-4-6": 3 }
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

Falls ein `error`-Feld zurückkommt, melde den Fehler dem User und stoppe.

---

## Schritt 2: Projekt-Konfiguration lesen

Lies die installierten Skills, Agents und Hooks — das ist die Basis für die Gap-Analyse (was ist konfiguriert, aber nicht genutzt?).

```bash
# Installierte Skills
find "$PROJECT_PATH/plugins" -name "SKILL.md" 2>/dev/null | xargs grep -l "^name:" 2>/dev/null

# Installierte Agents
find "$PROJECT_PATH/plugins" -name "*.md" -path "*/agents/*" 2>/dev/null | xargs grep -l "^name:" 2>/dev/null

# Plugin-Manifest
find "$PROJECT_PATH/plugins" -name "plugin.json" 2>/dev/null

# Hooks
find "$PROJECT_PATH/plugins" -name "hooks.json" 2>/dev/null
```

Lies die Frontmatter-`name`-Felder aus den gefundenen Dateien, um die vollständige Liste konfigurierter Skills und Agents zu erhalten.

---

## Schritt 3: Report generieren

Du hast jetzt:
- **Rohdaten**: tatsächliche Nutzung (skill_counts, agent_counts, model_counts)
- **Konfiguration**: installierte Skills und Agents

Erstelle daraus einen aussagekräftigen Report. Denk dabei wie ein Analyst, nicht wie ein Datenaggregator — die Zahlen allein sind weniger wertvoll als ihre Interpretation.

### Was macht einen guten Report aus?

**Gap-Analyse**: Was ist installiert, aber wird nicht genutzt? Das sind die wertvollsten Findings — sie zeigen entweder tote Ballast-Konfiguration oder unentdeckte Potenziale.

**Verhältnisse statt nur Absolutzahlen**: "Interview: 12 Aufrufe" ist weniger aussagekräftig als "Interview macht 48% aller Skill-Aufrufe aus — klar dominant".

**Modell-Verteilung bewerten**: Opus ist teuer und leistungsstark — wird er für die richtigen Aufgaben eingesetzt? Wenn Opus 90%+ ist, lohnt es sich zu fragen ob Subagenten auf Sonnet umgestellt werden könnten.

**Empfehlungen konkret halten**: Nicht "Skills entfernen erwägen" sondern "`stemago-tools:db-inspect` kann entfernt werden — 0 Aufrufe in 30 Tagen, kein aktives DB-Projekt erkennbar".

### Report-Format

Verwende EXAKT diese Markdown-Struktur:

```markdown
# Usage Report: [Projektname] — [Monat Jahr]

> Zeitraum: [TT.MM.] – [TT.MM.JJJJ] · [N] Sessions analysiert

---

## Übersicht

| Metrik | Wert |
|--------|------|
| Sessions | N |
| Skill-Aufrufe gesamt | N |
| Agent-Einsätze gesamt | N |
| Aktiv genutzte Skills | N von M installierten |
| Aktiv genutzte Agents | N von M installierten |

---

## Skills — Nutzung

| Skill | Aufrufe | Anteil | Trend |
|-------|---------|--------|-------|
| `skill-name` | 12 | 48% | ↑ häufigster |
| ... | | | |

[Kurze Interpretation: Was dominiert und warum könnte das so sein?]

### Nicht genutzte Skills ⚠️

Falls vorhanden — Skills die installiert aber im Zeitraum nicht aufgerufen wurden:

- `skill-name` — [kurze Einschätzung: Kandidat zum Entfernen / seltener Spezialfall / neu installiert?]

Falls alle Skills genutzt werden: "Alle installierten Skills wurden im Zeitraum mindestens einmal genutzt. ✓"

---

## Agents — Einsatz

| Agent | Aufrufe | Notizen |
|-------|---------|---------|
| `agent-name` | 5 | |

### Nicht genutzte Agents ⚠️

[Analog zu Skills]

---

## Modell-Verteilung

| Modell | Aufrufe | Anteil |
|--------|---------|--------|
| claude-opus-4-7 | 45 | 78% |
| claude-sonnet-4-6 | 12 | 22% |

[Bewertung: Ist die Verteilung sinnvoll? Gibt es Optimierungspotenzial?]

---

## Empfehlungen

[Maximal 5 konkrete, priorisierte Handlungsempfehlungen. Nummeriert. Jede mit einer klaren Handlung:]

1. **[Titel]**: [Was genau tun und warum]
2. ...

---

## Monatliche Automatisierung

Um diesen Report automatisch am 1. jeden Monats zu erhalten:

```
/schedule "Am 1. jeden Monats um 9 Uhr: /stemago-tools:usage-report ausführen"
```

Oder manuell mit: `/stemago-tools:usage-report --months 1`
```

---

## Schritt 4: Report speichern

Speichere den Report in:
```
[PROJECT_PATH]/docs/reports/usage-[YYYY-MM].md
```

Erstelle das Verzeichnis falls nötig (`mkdir -p`).

Zeige den vollständigen Report auch im Terminal aus (nicht nur "gespeichert unter...").

Sage dem User am Ende:
> "Report gespeichert unter `docs/reports/usage-YYYY-MM.md`. Um ihn monatlich automatisch zu erstellen, nutze `/schedule` wie oben beschrieben."

$ARGUMENTS
