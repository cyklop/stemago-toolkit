---
name: reflect
description: "Session Learning Extractor - Analysiert die aktuelle Session und sichert Learnings im Memory von Claude Code, damit sie in zukünftigen Sessions automatisch geladen werden. Verwende diesen Skill wenn der User Learnings speichern will, am Session-Ende reflektieren möchte, oder fragt 'was haben wir gelernt', 'speicher das als Learning', 'was war wichtig in dieser Session'. Auch bei 'reflektiere', 'Learnings extrahieren', oder wenn der User explizit um Reflection bittet."
---

# /reflect - Session Learning Extractor

Analysiere die aktuelle Session und sichere die Learnings im **eingebauten Memory von Claude Code**. Dort werden sie in jeder künftigen Session dieses Projekts automatisch geladen — eine eigene Learnings-Datei im Repo wird nicht mehr gepflegt.

## Wohin geschrieben wird

Das Memory-Verzeichnis dieser Session steht im System-Prompt (Abschnitt „Memory", in der Regel `~/.claude/projects/<projekt-slug>/memory/`). Halte dich an das dort beschriebene Format: **eine Datei pro Fakt** mit Frontmatter (`name`, `description`, `type`) und eine Zeiger-Zeile im Index `MEMORY.md`.

Nennt der System-Prompt kein Memory-Verzeichnis, ist Auto-Memory in dieser Session aus. Dann nichts schreiben: zeige die Vorschau aus Schritt 3 und sag dem User, dass er Memory aktivieren (`/memory`) oder die Punkte selbst in die `CLAUDE.md` übernehmen kann.

## Schritt 1: Session-Analyse

Scanne die gesamte Konversation nach:

1. **Explizite Korrekturen** (HIGH)
   - User sagt "nicht X, sondern Y", "Das ist falsch, verwende stattdessen..."
   - "NIE/IMMER X tun", direkte Anweisungen mit "muss", "soll nicht"

2. **Bestätigte Patterns** (MEDIUM)
   - Lösungen, die funktioniert haben und positives Feedback bekamen ("Das war gut", "Genau so")

3. **Implizite Präferenzen** (LOW)
   - User wählt konsistent eine Option, wiederholte Anpassungen in gleiche Richtung

Ein Learning muss **dauerhaft** und **anwendbar** sein: es ändert dein Verhalten in künftigen Sessions. Nicht ins Memory gehören: was das Repo schon festhält (Code-Struktur, Git-Historie, `CLAUDE.md`), erledigte Arbeit, Task-Status, einmalige Details dieser Session.

## Schritt 2: Typ zuordnen

| Typ | Inhalt |
|---|---|
| `feedback` | Korrekturen und bestätigte Arbeitsweisen — mit **Why:** und **How to apply:** |
| `project` | Ziele, Constraints, laufende Vorhaben, die nicht aus dem Code ableitbar sind |
| `user` | Rolle, Expertise, Präferenzen des Users |
| `reference` | Zeiger auf externe Ressourcen (URLs, Dashboards, Tickets) |

## Schritt 3: Vorschau zeigen

```markdown
## Gefundene Learnings

### HIGH (explizite Anweisungen) — werden gespeichert
- [feedback] "Migrations nie mit 'chore:' committen" — Why: …

### MEDIUM (bestätigte Patterns) — werden gespeichert
- [feedback] "E2E-Tests mit data-testid statt Text-Selektoren"

### LOW (Beobachtungen) — nur auf Wunsch
- [user] "Bevorzugt btn-primary für Hauptaktionen"
```

Frage via **AskUserQuestion**: **HIGH + MEDIUM speichern** / **Alle speichern** / **Nichts speichern**. Einzelne Punkte kann der User über „Other" streichen oder umformulieren.

## Schritt 4: Nach Bestätigung speichern

1. **Bestehendes Memory lesen**: `MEMORY.md` und die Dateien, die thematisch passen.
2. **Zusammenführen statt duplizieren**: Deckt ein bestehendes Memory das Learning ab, diese Datei aktualisieren. Widerspricht die Session einem bestehenden Memory, es korrigieren oder löschen (samt Zeile in `MEMORY.md`).
3. **Neue Memories schreiben**: eine Datei pro Fakt, danach die Zeiger-Zeile in `MEMORY.md`. Wortlaut des Users erhalten, wo die Formulierung zählt; eigene Interpretation als solche kennzeichnen.

Kein Git-Commit: das Memory liegt außerhalb des Repos.

## Schritt 5: Alt-Bestand migrieren (einmalig)

Existiert noch `.claude/learnings/project-learnings.md` aus früheren Plugin-Versionen, biete an, die weiterhin gültigen Einträge ins Memory zu übernehmen. Nach der Übernahme die Datei nicht selbst löschen — dem User überlassen.

## Output

```
Reflection abgeschlossen!

Gespeichert: X neu, Y aktualisiert, Z entfernt
Übersprungen (bereits abgedeckt): N
Ort: <Memory-Verzeichnis>

Tipp: /stemago-tools:reflect-config --on schaltet beim Session-Start eine Erinnerung an /reflect ein
```
