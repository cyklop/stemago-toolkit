---
name: db-inspect
description: "Datenbank inspizieren - Tabellen, Schema, Queries ausführen"
---

# MariaDB MCP - Datenbank-Inspektion

Nutze den MariaDB MCP Server für alle Datenbank-Operationen.

## Verfügbare Tools

### `mcp__mariadb__list_databases`
Alle verfügbaren Datenbanken auflisten.

### `mcp__mariadb__list_tables`
Tabellen einer Datenbank auflisten.
```
database: "volleyball_dev"  # Optional, nutzt Default wenn nicht angegeben
```

### `mcp__mariadb__describe_table`
Schema einer Tabelle anzeigen (Spalten, Typen, Constraints).
```
table: "Tournament"
database: "volleyball_dev"  # Optional
```

### `mcp__mariadb__execute_query`
SQL-Query ausführen (SELECT, INSERT, UPDATE, DELETE, SHOW, DESCRIBE, EXPLAIN).
```
query: "SELECT * FROM Tournament WHERE slug = 'test'"
database: "volleyball_dev"  # Optional
```

## Typische Anwendungsfälle

1. **Daten prüfen**: Vor Änderungen schauen was existiert
2. **Schema verstehen**: Vor Prisma-Migrationen aktuellen Stand prüfen
3. **Debugging**: Warum zeigt die UI falsche Daten?
4. **Verifikation**: Nach Migration prüfen ob Daten korrekt sind

## Beispiel-Queries

```sql
-- Aktive Turniere mit Phasen
SELECT t.name, t.slug, COUNT(tp.id) as phases
FROM Tournament t
LEFT JOIN TournamentPhase tp ON tp.tournamentId = t.id
GROUP BY t.id;

-- Unbestätigte Anmeldungen
SELECT r.*, u.email FROM Registration r
JOIN User u ON u.id = r.userId
WHERE r.status = 'PENDING';
```

## Hinweise

- **Nur lesende Queries** für Debugging verwenden
- **Schreibende Queries** nur wenn explizit gewünscht
- Bei Schema-Fragen besser `describe_table` als raw SQL
