---
name: docs-lookup
description: "Aktuelle Dokumentation abrufen - React, Next.js, Tailwind, Prisma, DaisyUI, Zod, etc. Verwende diesen Skill wenn der User nach aktueller Library-Dokumentation fragt, wissen will wie ein API funktioniert, oder Best Practices für ein Framework braucht. Auch bei 'wie macht man X in Next.js', 'Prisma Syntax für Y', 'was ist neu in React 19', 'Tailwind Klasse für Z', oder wenn du selbst unsicher über aktuelle API-Syntax bist."
---

# Context7 MCP - Dokumentations-Lookup

Nutze den Context7 MCP Server um aktuelle Dokumentation für Libraries abzurufen.

## Verfügbare Tools

Der Tool-Präfix hängt davon ab, wie Context7 installiert ist: als eigener MCP-Server `mcp__context7__*`, als Claude-Code-Plugin `mcp__plugin_context7_context7__*`. Nutze den Präfix, der in dieser Session verfügbar ist — die Tool-Namen dahinter sind identisch.

### `mcp__context7__resolve-library-id`
Library-ID für Context7 ermitteln.
```
libraryName: "next.js"
query: "How to use server actions"
```

### `mcp__context7__query-docs`
Dokumentation abfragen (benötigt Library-ID von resolve).
```
libraryId: "/vercel/next.js"
query: "How to implement server actions with form handling"
```

## Workflow

1. **resolve-library-id** aufrufen um ID zu bekommen
2. **query-docs** mit der ID und spezifischer Frage

## Library-IDs

IDs nicht aus dem Gedächtnis nehmen — sie ändern sich, wenn Projekte umziehen. Immer zuerst `resolve-library-id`, dann die zurückgegebene ID verwenden. Welche Libraries und Versionen das Projekt nutzt, steht in `package.json` (bzw. dem Lockfile); die Version in die Query schreiben ("Next.js 15 App Router …").

## Anwendungsfälle

1. **API-Änderungen**: Was hat sich in neuer Version geändert?
2. **Best Practices**: Aktuelle empfohlene Patterns
3. **Syntax-Fragen**: Wie genau funktioniert Feature X?
4. **Migration**: Wie upgrade ich von Version A zu B?

## Hinweise

- **Spezifische Fragen stellen**: Je präziser, desto besser
- **Versions-Kontext**: Bei Next.js 15+ spezifisch danach fragen
- **Max 3 Calls**: Pro Frage nicht mehr als 3 Aufrufe
- **Fallback**: Bei fehlendem Result WebSearch nutzen
