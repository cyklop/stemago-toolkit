---
name: reflect
description: "Session Learning Extractor - Analysiert Session und extrahiert Learnings"
---

# /reflect - Session Learning Extractor

Analysiere die aktuelle Session und extrahiere Learnings für zukünftige Sessions.

## Deine Aufgabe

### Schritt 1: Session-Analyse

Scanne die gesamte Konversation nach:

1. **Explizite Korrekturen** (HIGH confidence)
   - User sagt "nicht X, sondern Y"
   - "Das ist falsch, verwende stattdessen..."
   - "NIE/IMMER X tun"
   - Direkte Anweisungen mit "muss", "soll nicht"

2. **Erfolgreiche Patterns** (MEDIUM confidence)
   - Lösungen die funktioniert haben
   - Patterns die positives Feedback erhielten
   - "Das war gut", "Genau so"

3. **Implizite Präferenzen** (LOW confidence)
   - User wählt konsistent eine Option
   - Wiederholte Anpassungen in gleiche Richtung
   - Stil-Präferenzen (Kommentare, Formatierung)

### Schritt 2: Kategorisierung

Ordne jedes Learning einer Kategorie zu:

- **Code Style**: Formatierung, Kommentare, Naming
- **Prisma/Database**: Migrationen, Schema-Änderungen
- **Testing**: Test-Patterns, E2E, Unit Tests
- **Git/Commits**: Commit-Messages, Branch-Naming
- **Architecture**: Struktur, Patterns, Best Practices
- **Tools/MCP**: Tool-Nutzung, MCP-Präferenzen
- **UI/Components**: DaisyUI, Tailwind, React-Patterns
- **API**: Endpoints, Validation, Error-Handling

### Schritt 3: Vorschau generieren

Zeige dem User eine Vorschau der extrahierten Learnings:

```markdown
## Gefundene Learnings

### HIGH Confidence (Explizite Anweisungen)
- [Code Style] "Immer deutsche Kommentare in UI-Komponenten"
- [Prisma/Database] "Migrations nie mit 'chore:' committen"

### MEDIUM Confidence (Erfolgreiche Patterns)
- [Testing] "E2E-Tests mit data-testid statt Text-Selektoren"

### LOW Confidence (Beobachtungen)
- [UI/Components] "Bevorzugt btn-primary für Hauptaktionen"

Sollen diese Learnings übernommen werden? [Ja/Nein/Bearbeiten]
```

### Schritt 4: Nach Bestätigung

1. **Lese bestehende Learnings**:
   ```
   Read .claude/learnings/project-learnings.md
   ```

2. **Merge neue Learnings** (Duplikate vermeiden):
   - Prüfe ob ähnliches Learning existiert
   - Update Confidence wenn nötig (LOW -> MEDIUM -> HIGH)
   - Füge neue Learnings an richtige Kategorie an

3. **Schreibe aktualisierte Datei**:
   ```
   Write .claude/learnings/project-learnings.md
   ```

4. **Git Commit** (wenn Git verfügbar):
   ```bash
   git add .claude/learnings/project-learnings.md
   git commit -m "learn: add session learnings - [Anzahl] new patterns"
   ```

### Schritt 5: Cleanup-Check (Optional)

Prüfe bei jedem Reflect ob alte Learnings noch relevant sind:

1. Lese Git-Log für Learnings-Datei
2. Für Learnings älter als 30 Tage:
   ```
   Folgende Learnings sind älter als 30 Tage:
   - [Category] "Learning text..." (hinzugefügt vor 45 Tagen)

   Noch relevant? [Ja/Entfernen]
   ```

## Output Format

Am Ende zeige:

```
Reflection abgeschlossen!

Statistik:
- HIGH: X neue Learnings
- MEDIUM: Y neue Learnings
- LOW: Z neue Learnings
- Duplikate übersprungen: N

Gespeichert in: .claude/learnings/project-learnings.md
Git Commit: [commit hash] (wenn committed)

Tipp: Verwende /reflect-on für automatische Reflection am Session-Ende
```

$ARGUMENTS
