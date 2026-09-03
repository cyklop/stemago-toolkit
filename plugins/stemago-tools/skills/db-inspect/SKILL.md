---
name: db-inspect
description: "Datenbank inspizieren - Tabellen, Schema, Queries ausführen. Verwende diesen Skill wenn der User Datenbank-Inhalte sehen will, Tabellen oder Schema anzeigen möchte, SQL-Queries ausführen will, oder Daten debuggen muss. Auch bei 'was steht in der DB', 'zeig mir die Tabellen', 'Daten prüfen', 'Schema anschauen', 'Query ausführen', oder wenn Prisma-Migrationen gegen den DB-Stand geprüft werden sollen."
---

# MariaDB MCP - Datenbank-Inspektion

Nutze den MariaDB MCP Server für alle Datenbank-Operationen.

## Verfügbare Tools

### `mcp__mariadb__list_databases`
Alle verfügbaren Datenbanken auflisten.

### `mcp__mariadb__list_tables`
Tabellen einer Datenbank auflisten.
```
database: "<datenbank>"  # Optional, nutzt Default wenn nicht angegeben
```

### `mcp__mariadb__describe_table`
Schema einer Tabelle anzeigen (Spalten, Typen, Constraints).
```
table: "<Tabelle>"
database: "<datenbank>"  # Optional
```

### `mcp__mariadb__execute_query`
SQL-Query ausführen (SELECT, INSERT, UPDATE, DELETE, SHOW, DESCRIBE, EXPLAIN).
```
query: "SELECT * FROM <Tabelle> WHERE <spalte> = '<wert>'"
database: "<datenbank>"  # Optional
```

## Typische Anwendungsfälle

1. **Daten prüfen**: Vor Änderungen schauen was existiert
2. **Schema verstehen**: Vor Prisma-Migrationen aktuellen Stand prüfen
3. **Debugging**: Warum zeigt die UI falsche Daten?
4. **Verifikation**: Nach Migration prüfen ob Daten korrekt sind

## Beispiel-Queries

```sql
-- Eltern mit Anzahl Kinder (1:n-Aggregation)
SELECT p.name, COUNT(c.id) AS children
FROM <Parent> p
LEFT JOIN <Child> c ON c.parentId = p.id
GROUP BY p.id;

-- Datensätze in einem bestimmten Status, mit Join auf den User
SELECT r.*, u.email FROM <Tabelle> r
JOIN User u ON u.id = r.userId
WHERE r.status = '<STATUS>';
```

## Hinweise

- **Nur lesende Queries** für Debugging verwenden
- **Schreibende Queries** nur wenn explizit gewünscht
- Bei Schema-Fragen besser `describe_table` als raw SQL
