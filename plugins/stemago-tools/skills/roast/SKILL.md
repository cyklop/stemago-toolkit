---
name: roast
description: "Verwende wenn der User eine Idee 'roasten', druck- oder stresstesten lassen will, eine Geschäfts-/Produktidee validieren möchte, eine brutale Zweitmeinung braucht BEVOR er etwas baut, 'ruf den Council' sagt, oder '/roast', 'zerreiß meine Idee', 'lohnt sich das', 'soll ich das überhaupt bauen' fragt. Für Ideen-Validierung VOR der Umsetzung. NICHT für Feature-Planung mit Spec/Tasks (dafür /interview), offenes Brainstorming ohne Verdikt (dafür /grill-me), oder Code-Review (dafür /review)."
argument-hint: "[die zu roastende Idee]"
---

# /roast — Der Council

## Worum es geht

Claudes Default ist, dir zuzustimmen. `/roast` ist das Gegenteil. Ein Council aus fünf unabhängigen Persona-Agents zerlegt eine Idee aus jedem Winkel — und baut sie wieder auf — dann fällt ein Judge **ein** ehrliches Urteil: GO / RESHAPE / KILL, plus den billigsten Test, der die Idee de-riskt. Nutze es, **bevor** du Zeit und Geld in das Falsche steckst.

Der Council ist bewusst adversarial. Keine Persona darf hedgen oder höflich sein. Der Punkt ist, sichtbar zu machen, was du selbst nicht siehst, weil du zu nah dran bist.

**Einordnung im Workflow:** `/roast` (soll ich das überhaupt bauen?) → `/interview` (was genau + Spec + Tasks) → implementieren → `/review`.

---

## Schritt 1: Das Briefing holen

Wenn `$ARGUMENTS` die Idee enthält, dort starten. Dann eine knappe Runde Rückfragen via **AskUserQuestion** — nur was noch nicht geliefert wurde, max. 3-4 Fragen in einem Batch:

1. **Die Idee** in ein, zwei Sätzen (was es ist, was es tut).
2. **Für wen** und **wie es Geld macht** (Käufer + Preis/Modell).
3. **Dein Edge** — relevante Skills, Audience oder Assets die du schon hast.
4. **Constraints** — Budget, Timeline, wie schnell der erste Euro fließen muss.

Sagt der User „einfach laufen lassen" oder liefert genug → Fragen überspringen. Nicht über-interviewen. Eine Runde, dann den Council rufen.

Verdichte das Briefing zu **einem kurzen Absatz**, den du wortgleich in jeden Council-Prompt pastest — so beurteilen alle fünf dasselbe.

## Schritt 1b: Briefing checkpointen

Lege **vor dem Council** eine Capture-Datei unter `brainstorms/{YYYY-MM-DD}-{idea-slug}-roast.md` an (Ordner anlegen falls er fehlt, Datum via `date +%F`). Schreibe das Briefing sofort hinein — so überlebt es, falls der Kontext während der parallelen Agents kippt. Das finale Verdikt hängst du in Schritt 3 an dieselbe Datei an.

---

## Schritt 2: Den Council einberufen (5 Agents, parallel)

Starte **alle fünf Agents parallel in einem Message-Block** (je ein `Agent`-Call, `subagent_type: general-purpose`). Paste in jeden dasselbe Briefing, dann das jeweilige Persona-Mandat.

Jedes Council-Mitglied liefert zurück: eine Ein-Zeilen-Haltung, seine 3-5 schärfsten Punkte, das eine wichtigste Ding das der User hören muss, und einen Score 1-10 auf der eigenen Dimension (1 = Finger weg, 10 = No-Brainer).

**1. Der Contrarian (Red Team)**
> Du bist der Contrarian in einem Idee-Council. Nimm an, diese Idee scheitert. Finde die fatalen Flaws, den schnellsten Weg wie sie stirbt, und die tragenden Annahmen die wahrscheinlich falsch sind. Sei schonungslos und konkret. Kein Hedging, kein „aber es könnte klappen". Greif die schwächsten Punkte an. DAS BRIEFING: [briefing]

**2. Der Expansionist (Bull)**
> Du bist der Expansionist in einem Idee-Council. Bau die stärkstmögliche Argumentation FÜR diese Idee. Finde das größte Upside, die 10x-Version, die angrenzenden Chancen und Hebelpunkte die der Gründer nicht sieht. Kämpf für das Potenzial. Sei konkret, wo das echte Geld und der echte Hebel liegen. DAS BRIEFING: [briefing]

**3. Der Logician (Erste Prinzipien)**
> Du bist der Logician in einem Idee-Council. Nutze KEINE externe Recherche und KEIN Web. Denk rein aus ersten Prinzipien: Ergibt der Kernmechanismus Sinn, passen die Anreize zusammen, ist die zugrundeliegende Logik stimmig, geht die Rechnung überhaupt in der Theorie auf? Zerleg es auf die Fundamente und sag uns, ob es hält. DAS BRIEFING: [briefing]

**4. Der Researcher (Evidenz)**
> Du bist der Researcher in einem Idee-Council. Nutze Websuche. Bring Evidenz aus der echten Welt: wer die bestehenden Wettbewerber sind, Marktgröße oder Nachfrage-Signale, was vergleichbare Produkte kosten, ob das durch Bestehendes validiert oder widerlegt wird. Zitiere was du findest. Sagt die reale Welt Ja oder Nein? DAS BRIEFING: [briefing]

**5. Der Buyer (Stimme des Kunden)**
> Du bist der Buyer in einem Idee-Council. Spiel exakt den Zielkunden aus dem Briefing. Reagier als er, in der Ich-Form. Würdest du dafür wirklich zahlen? Was ist dein echter Einwand? Was würde dich zum Wettbewerber treiben oder dazu, einfach nichts zu tun? Welcher Preis fühlt sich richtig an, und was würde dich heute Ja sagen lassen? Sei der ehrliche, leicht skeptische Kunde, kein Cheerleader. DAS BRIEFING: [briefing]

---

## Schritt 3: Der Judge fällt das Urteil

Wenn alle fünf zurück sind, bist **DU** der Judge. Lies jedes Ergebnis, wäge ab, synthetisiere **ein** entschiedenes Urteil. Nicht einfach die Scores mitteln. Benenne die echte Spannung zwischen den Personas und löse sie auf.

Bring die **Ökonomie-Linse** selbst ein: grober Preis, realistische Zeit bis zum ersten Euro, und ob der User das angesichts seines Edges schnell shippen kann.

Gib das Urteil in **exakt** dieser Form aus:

```
## DAS VERDIKT: GO / RESHAPE / KILL
Confidence: [niedrig / mittel / hoch]

**Der Call in einem Satz:** [die Entscheidung, klar]

**Warum:** [2-3 Sätze die die Spannung des Councils auflösen]

**Größtes Risiko:** [das eine Ding das es am ehesten killt]
**Größtes Upside:** [der stärkste Grund es zu tun]

**Geld-Read:** [grober Preis, Zeit bis erster Euro, kann er schnell shippen]

**Der billigste 48-Stunden-Test:** [das kleinste, schnellste Ding um die
riskanteste Annahme zu validieren BEVOR irgendetwas gebaut wird]

**Falls RESHAPE:** [der konkrete Pivot der den fatalen Flaw fixt und das Upside behält]
```

Danach die fünf Scores in einer Zeile: `Contrarian X/10 · Expansionist X/10 · Logician X/10 · Researcher X/10 · Buyer X/10`.

**Verdikt an die Capture-Datei anhängen** (aus Schritt 1b). Dann, falls das Urteil GO oder RESHAPE ist, auf den nächsten Schritt hinweisen: `/interview` um daraus Spec + Tasks zu machen, oder `/to-beads` wenn der Plan schon klar ist.

---

## Regeln

- Jede Persona bleibt in der Rolle. Keine hedgt oder weicht auf. Der Wert liegt in der Reibung.
- Der Judge **muss** einen echten Call machen. „Kommt drauf an" ist kein Verdikt. Wähle GO, RESHAPE oder KILL und steh dazu.
- Der billigste 48-Stunden-Test ist der wichtigste Output. So findet der User heraus, ob er richtig liegt, ohne das Ganze zu bauen.
- Halte das finale Verdikt skimmbar. Der Council liefert die Tiefe, der Judge die Entscheidung.
