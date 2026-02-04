---
name: beads-ready
description: "Zeigt Tasks ohne Blocker (Ready Queue)"
---

# Beads Ready

Zeigt alle Tasks die keine offenen Blocker haben und bearbeitet werden können.

## Workflow

### Schritt 1: Beads-Status prüfen

```bash
ls .beads/ 2>/dev/null || echo "NOT_INITIALIZED"
```

Falls nicht initialisiert:

```markdown
## Beads nicht initialisiert

Führe zuerst `/beads-setup` aus, um Beads zu konfigurieren.
```

Stoppe hier.

### Schritt 2: Ready Tasks abrufen

Nutze Beads MCP Tool oder CLI:

```bash
bd ready
```

### Schritt 3: Formatierte Ausgabe

**Falls Tasks vorhanden:**

```markdown
## Ready Queue

| ID | Priorität | Titel | Typ |
|----|-----------|-------|-----|
| bd-a1b2 | 0 (kritisch) | API Endpoint implementieren | task |
| bd-c3d4 | 1 (hoch) | Tests schreiben | task |
| bd-e5f6 | 2 (normal) | Dokumentation | chore |

### Empfehlung
Starte mit **bd-a1b2** (höchste Priorität).

Details anzeigen: `bd show bd-a1b2`
```

**Falls keine Tasks:**

```markdown
## Ready Queue leer

Keine Tasks ohne Blocker gefunden.

### Optionen

1. **Neue Tasks erstellen**:
   ```bash
   bd create "Task-Titel" -p 1
   ```

2. **Alle Tasks anzeigen**:
   ```bash
   bd list
   ```

3. **Geblockte Tasks prüfen**:
   ```bash
   bd blocked
   ```
```

### Schritt 4: Quick Actions anbieten

```markdown
### Quick Actions

- `/land-the-plane` - Session beenden mit Handoff
- `bd show <id>` - Task-Details anzeigen
- `bd create "Titel"` - Neuen Task erstellen
```

## Prioritäten-Legende

| Priorität | Bedeutung |
|-----------|-----------|
| 0 | Kritisch - Sofort bearbeiten |
| 1 | Hoch - Heute erledigen |
| 2 | Normal - Diese Woche |
| 3 | Niedrig - Irgendwann |

$ARGUMENTS
