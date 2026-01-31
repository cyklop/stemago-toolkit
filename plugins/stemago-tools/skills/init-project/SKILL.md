---
name: init-project
description: "Projekt-CLAUDE.md mit Workflow-Regeln initialisieren"
---

# /init-project - Projekt Workflow-Regeln

Erstellt oder ergänzt eine CLAUDE.md im aktuellen Projekt mit Workflow-Regeln für strukturierte Aufgabenabarbeitung und automatische Code Reviews.

## Deine Aufgabe

### Schritt 1: Bestehende CLAUDE.md prüfen

Prüfe ob eine `CLAUDE.md` im Projekt-Root existiert:

```
Read CLAUDE.md
```

### Schritt 2a: Falls CLAUDE.md existiert

Zeige dem User den aktuellen Inhalt und frage:

```
Die Datei CLAUDE.md existiert bereits mit folgendem Inhalt:
[Inhalt anzeigen]

Soll ich die Workflow-Regeln ergänzen? [Ja/Nein]
```

Falls Ja: Füge die Workflow-Regeln als neuen Abschnitt am Ende ein (bestehenden Inhalt beibehalten).

### Schritt 2b: Falls keine CLAUDE.md existiert

Erstelle eine neue `CLAUDE.md` mit dem Template aus Schritt 3.

### Schritt 3: Workflow-Regeln einfügen

Füge folgende Abschnitte in die CLAUDE.md ein:

```markdown
## Workflow-Regeln

### Strukturierte Aufgaben-Abarbeitung
- Bei Aufgaben mit 3+ Schritten: IMMER zuerst eine Task-Liste mit TaskCreate erstellen
- Jeden Task auf `in_progress` setzen bevor du anfängst, auf `completed` wenn fertig
- NIEMALS eine Aufgabe als erledigt melden bevor ALLE Tasks completed sind
- Bei Unterbrechung/Compact: TaskList prüfen und offene Tasks weiterarbeiten

### Code Review am Aufgabenende
- Nach Abschluss einer Implementierung die 3+ Dateien betrifft:
  1. `git diff` der Änderungen anzeigen
  2. Frage: "Soll ich einen Code Review der Änderungen durchführen?"
  3. Bei Ja: Review auf Code-Qualität, Security, Performance, Konsistenz
  4. Review-Ergebnis als Zusammenfassung mit konkreten Verbesserungsvorschlägen

### Dokumentations-Pflege
- Nach Abschluss eines Features das neue Funktionalität, Skills, Agents oder Konfiguration hinzufügt:
  1. Prüfe ob `CLAUDE.md` aktualisiert werden muss (neue Regeln, Patterns, Konventionen)
  2. Prüfe ob `README.md` aktualisiert werden muss (neue Features, geänderte Struktur, Installationsschritte)
  3. Frage: "Sollen CLAUDE.md/README.md an die neuen Änderungen angepasst werden?"
  4. Bei Ja: Nur die relevanten Abschnitte aktualisieren, bestehenden Inhalt beibehalten
```

### Schritt 4: Bestätigung

Zeige dem User:

```
CLAUDE.md wurde erstellt/aktualisiert!

Aktive Workflow-Regeln:
- Strukturierte Aufgaben-Abarbeitung (TaskCreate bei 3+ Schritten)
- Code Review am Aufgabenende (bei 3+ geänderten Dateien)

Diese Regeln gelten ab sofort für jede Claude-Interaktion in diesem Projekt.
```

$ARGUMENTS
