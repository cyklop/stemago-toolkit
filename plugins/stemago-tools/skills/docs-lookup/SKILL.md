---
name: docs-lookup
description: "Aktuelle Dokumentation abrufen - React, Next.js, Tailwind, etc."
---

# Context7 MCP - Dokumentations-Lookup

Nutze den Context7 MCP Server um aktuelle Dokumentation für Libraries abzurufen.

## Verfügbare Tools

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

## Wichtige Libraries

| Library | ID | Verwendung |
|---------|-----|------------|
| Next.js | `/vercel/next.js` | App Router, Server Components |
| React | `/facebook/react` | Hooks, Components |
| Prisma | `/prisma/prisma` | ORM, Schema, Queries |
| Tailwind CSS | `/tailwindlabs/tailwindcss` | Styling |
| DaisyUI | `/saadeghi/daisyui` | UI Components |
| Zod | `/colinhacks/zod` | Validation |
| NextAuth.js | `/nextauthjs/next-auth` | Authentication |
| React Hook Form | `/react-hook-form/react-hook-form` | Formulare |
| date-fns | `/date-fns/date-fns` | Datum/Zeit |
| Playwright | `/microsoft/playwright` | E2E Testing |
| Vitest | `/vitest-dev/vitest` | Unit Testing |

## Typische Anfragen

### Next.js 15
```
libraryId: "/vercel/next.js"
query: "App Router params as Promise in Next.js 15"
```

### React 19
```
libraryId: "/facebook/react"
query: "useTransition and server actions"
```

### Prisma
```
libraryId: "/prisma/prisma"
query: "How to create a migration with optional field"
```

### DaisyUI
```
libraryId: "/saadeghi/daisyui"
query: "Modal component with form"
```

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
