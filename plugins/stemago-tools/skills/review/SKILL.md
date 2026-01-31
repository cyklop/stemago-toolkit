---
name: review
description: "Code Review der letzten Änderungen durchführen"
---

# /review - Code Review

Führe einen strukturierten Code Review der letzten Änderungen durch.

## Deine Aufgabe

### Schritt 1: Änderungen ermitteln

Führe folgende Befehle aus um die zu reviewenden Änderungen zu finden:

```bash
git diff HEAD
git diff --cached
```

Falls beide leer sind, reviewe den letzten Commit:

```bash
git diff HEAD~1
```

Falls auch das leer ist: "Keine Änderungen zum Reviewen gefunden."

### Schritt 2: Geänderte Dateien analysieren

Liste alle geänderten Dateien auf und lies jede einzeln. Analysiere auf:

1. **Code-Qualität und Konsistenz**
   - Naming-Konventionen eingehalten?
   - Konsistenz mit bestehendem Code?
   - Unnötige Komplexität?
   - Duplizierter Code?

2. **Security (OWASP Top 10)**
   - SQL Injection
   - XSS
   - Command Injection
   - Unsichere Deserialisierung
   - Hartcodierte Secrets/Credentials
   - Fehlende Input-Validierung

3. **Performance**
   - N+1 Queries
   - Unnötige Re-Renders
   - Fehlende Indizes
   - Große Payloads
   - Memory Leaks

4. **Error Handling**
   - Unbehandelte Exceptions
   - Fehlende Null-Checks
   - Unklare Fehlermeldungen

5. **Pattern-Einhaltung**
   - Passt der Code zu bestehenden Patterns im Projekt?
   - Werden etablierte Konventionen befolgt?

6. **Dokumentations-Aktualität**
   - Neue exports/APIs ohne Dokumentation?
   - README.md veraltet (Features, Struktur, Installationsschritte)?
   - CLAUDE.md veraltet (Regeln passen nicht mehr zum Code)?

### Schritt 3: Review-Ergebnis

Zeige eine strukturierte Zusammenfassung:

```
## Code Review Ergebnis

### Geprüfte Dateien
- file1.ts (geändert)
- file2.ts (neu)

### Findings

#### Critical
- [Security] file1.ts:42 - SQL Injection möglich bei unsanitized Input
  → Vorschlag: Parameterized Query verwenden

#### Warning
- [Performance] file2.ts:15 - N+1 Query in Loop
  → Vorschlag: Batch-Query verwenden

#### Info
- [Konsistenz] file1.ts:10 - Naming weicht von Projekt-Konvention ab
  → Vorschlag: camelCase statt snake_case

#### Docs
- [Dokumentation] README.md - Neuer Skill "xyz" fehlt in der Skills-Tabelle
  → Vorschlag: Skills-Tabelle und Strukturbaum aktualisieren

### Zusammenfassung
- Critical: X | Warning: Y | Info: Z
- Gesamtbewertung: [Gut/Akzeptabel/Verbesserung nötig]
```

### Schritt 4: Fixes anbieten

Falls Findings vorhanden:

```
Soll ich die Findings direkt beheben?
- Alle Findings beheben
- Nur Critical/Warning beheben
- Nein, nur als Info
```

$ARGUMENTS
