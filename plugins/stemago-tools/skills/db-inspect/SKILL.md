---
name: db-inspect
description: "Datenbank inspizieren - Tabellen, Schema, Queries ausführen. Verwende diesen Skill wenn der User Datenbank-Inhalte sehen will, Tabellen oder Schema anzeigen möchte, SQL-Queries ausführen will, oder Daten debuggen muss. Auch bei 'was steht in der DB', 'zeig mir die Tabellen', 'Daten prüfen', 'Schema anschauen', 'Query ausführen', oder wenn Prisma-Migrationen gegen den DB-Stand geprüft werden sollen."
---

# Datenbank-Inspektion mit MariaDB MCP

Inspiziere die Datenbank über die `mcp__mariadb__*`-Tools: `list_databases`, `list_tables`, `describe_table`, `execute_query`. Der Parameter `database` ist überall optional (Default-Datenbank des Servers).

## Ablauf

1. **Orientieren**: `list_tables`, dann `describe_table` für die beteiligten Tabellen — nicht aus dem ORM-Schema raten, die Datenbank ist die Wahrheit.
2. **Abfragen**: `execute_query` mit einem gezielten `SELECT`. Immer `LIMIT` setzen, solange die Tabellengröße unbekannt ist; Spalten benennen statt `SELECT *` bei breiten Tabellen.
3. **Befund melden**: die Query, die relevanten Zeilen und was sie für die Ausgangsfrage bedeuten.

## Regeln

- **Lesend ist der Normalfall.** `execute_query` lässt auch `INSERT`, `UPDATE` und `DELETE` zu — schreibende Statements nur auf ausdrücklichen Auftrag, vorher das Statement und die betroffene Zeilenzahl (`SELECT COUNT(*)` mit derselben `WHERE`-Klausel) zeigen.
- **Kein Schreiben ohne `WHERE`.**
- **Schema-Fragen** über `describe_table`, nicht über rohes SQL.
- **Vor Migrationen**: Ist-Schema mit dem ORM-Schema (z.B. `prisma/schema.prisma`) vergleichen und Abweichungen nennen, bevor migriert wird. Nach der Migration stichprobenartig verifizieren.
- **Personenbezogene Daten** nur so weit ausgeben, wie die Frage es braucht.

## Typische Fragen

- „Warum zeigt die UI falsche Daten?" → betroffenen Datensatz samt Joins abfragen und mit der API-Antwort vergleichen.
- „Gibt es Waisen/Duplikate?" → `LEFT JOIN … WHERE x IS NULL` bzw. `GROUP BY … HAVING COUNT(*) > 1`.
- „Ist die Migration durch?" → `describe_table` plus Stichprobe der neuen Spalten.
