import { prisma } from "@/lib/db/client";

// Auftragsübersicht. Suche nur nach exakter Auftragsnummer, per GET-Formular.
export default async function AuftraegePage({ searchParams }: { searchParams: Promise<{ nr?: string }> }) {
  const { nr } = await searchParams;
  const auftraege = await prisma.auftrag.findMany({
    where: nr ? { nummer: nr } : undefined,
    include: { kunde: true, monteur: true },
    orderBy: { erstelltAm: "desc" },
  });

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">Aufträge</h1>
      <form className="my-4 flex gap-2">
        <input name="nr" placeholder="Auftragsnummer" className="input input-bordered" defaultValue={nr} />
        <button className="btn">Suchen</button>
      </form>
      <table className="table">
        <thead>
          <tr>
            <th>Nummer</th>
            <th>Titel</th>
            <th>Kunde</th>
            <th>Status</th>
            <th>Termin</th>
            <th>Monteur</th>
          </tr>
        </thead>
        <tbody>
          {auftraege.map((a) => (
            <tr key={a.id}>
              <td>{a.nummer}</td>
              <td>{a.titel}</td>
              <td>{a.kunde.name}</td>
              <td>{a.status}</td>
              <td>{a.termin?.toISOString()}</td>
              <td>{a.monteur?.kuerzel}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}
