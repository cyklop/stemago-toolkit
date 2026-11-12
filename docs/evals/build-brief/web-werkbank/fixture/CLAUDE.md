# CLAUDE.md

## Projekt

**Werkbank** ist die Auftragsverwaltung eines Sanitär- und Heizungsbetriebs mit 14 Monteuren. Das Büro (zwei Disponentinnen) legt Aufträge an, plant Termine und schreibt Rechnungen. Die Monteure sehen ihre Aufträge am Handy.

## Stack

- Next.js 15 (App Router, Server Components, Server Actions), React 19, TypeScript strict
- Prisma 6 mit PostgreSQL. Lokal: Datenbank `werkbank_dev` über `docker compose up -d db` (Port 5433). `DATABASE_URL` steht in `.env.local`.
- Tailwind 4 mit DaisyUI 5, Theme `werkbank` in `src/app/globals.css`. Keine weiteren UI-Bibliotheken.
- Validierung mit Zod an jeder Server Action.

## Befehle

```bash
npm run dev          # http://localhost:3100
npm run test         # Vitest (Unit)
npm run test:e2e     # Playwright, braucht laufenden dev-Server
npm run db:seed      # Testdaten: 40 Kunden, 220 Aufträge
npx prisma migrate dev --name <name>
```

## Konventionen

- Sprache der Oberfläche: Deutsch, Anrede „du".
- Server Components als Standard, `"use client"` nur wo Interaktion es verlangt.
- Datenzugriff nur über `src/lib/db/*.ts`, nie direkt aus Komponenten.
- Commits: `feat:`, `fix:`, `chore:`.
- Anmeldung lokal: `buero@werkbank.test` / `werkbank` (Rolle Büro).
