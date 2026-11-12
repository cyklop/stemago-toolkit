// Legt 40 Kunden, 14 Monteure und 220 Aufträge an.
// Zufällige Daten ohne festen Seed: jeder Lauf ergibt andere Namen und Termine.
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // … gekürzt …
}

main().finally(() => prisma.$disconnect());
