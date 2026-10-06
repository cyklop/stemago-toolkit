---
name: redesign-studio
description: "Website-Redesign oder Neuaufbau von der ersten Frage bis zum Handoff: Interview, Recherche mit günstigen Subagents, N deutlich unterschiedliche HTML-Mockups mit Verifikation, Auswahl per Vergleichsboard, Folgeseiten, Handoff-Paket. Verwende wenn der User eine Seite oder App neu gestalten, Entwürfe sehen oder einen Relaunch vorbereiten will. Auch bei: 'Redesign', 'neues Design', 'Website neu aufbauen', 'Mockups erstellen', 'mach mir Entwürfe für …', 'Relaunch', 'Landingpage neu', oder wenn Inspirationsseiten (awwwards, godly, 21st.dev, motionsites) verlinkt werden und Entwürfe gewünscht sind. NICHT für einzelne Komponenten-Varianten (dafür /prototype), UI-Prüfung im Browser (dafür /browser-test) oder Ideen-Validierung (dafür /roast)."
argument-hint: "[url-oder-repo]"
---

# Redesign Studio

Der komplette Weg **Brief → Interview → Recherche → N Mockups → Auswahl → Folgeseiten → Handoff**, als eigenständige HTML-Prototypen im Repo.

Arbeitsteilung: **Du denkst, entscheidest und gestaltest. Günstige Subagents (`model="haiku"`) lesen, sammeln und prüfen.** Jeder Subagent bekommt den Brief, `bestand.md`, eine präzise Aufgabe und ein Ausgabeformat; er liefert Fakten, keine Empfehlungen. Rohquellen (Inspirationsseiten, Codebase-Dumps) bleiben aus deinem Kontext — du liest nur die Briefs der Subagents.

## Dateien

| Was | Wo |
|---|---|
| Brief (Interview-Capture) | `brainstorms/{YYYY-MM-DD}-redesign-{slug}.md` |
| Recherche-Briefs | `docs/research/redesign-{slug}/inspiration-<quelle>.md` und `…/bestand.md` |
| Mockups | `design/mockups/<richtung>/index.html` — eigenständiges HTML, CSS inline |
| Scroll-Engine | `design/mockups/scrollfx.js` — einmal pro Projekt aus diesem Skill-Ordner kopieren: `cp "${CLAUDE_SKILL_DIR}/scrollfx.js" design/mockups/` |
| Vergleichsboard | `design/mockups/index.html` |
| Verifier-Reports | `design/verify/<richtung>.md` |
| Handoff | `design/handoff-{slug}/` |

`{slug}` ist kebab-case aus Projekt oder Seite, `<richtung>` der Slug der Design-Richtung, Datum via `date +%F`.

## Phase 0: Interview

Zuerst die Bestandsquellen klären: Gibt es ein Design-System, eine Codebase, eine Live-URL? Was `$ARGUMENTS` liefert (URL, Repo-Pfad), gilt als bekannt und wird nicht erfragt.

Das Interview ist ein Gespräch, kein Formular: bis zu drei Fragen pro Nachricht, jede Antwort kurz zurückspiegeln, nichts fragen, was der Brief schon beantwortet. Die sechs Runden (Ursprung & Ziel, Zielgruppe & Ton, Bestand, Inspiration, Wunschlayouts, Umfang) mit ihren Fragen stehen in `REFERENCE.md`.

**Checkpoint nach jeder Runde:** Antworten und Entscheidungen in die Brief-Datei unter `brainstorms/` schreiben, bevor die nächste Runde kommt — die Datei ist die Quelle der Wahrheit, nicht dein Kontext (Mechanik: `/grill-me`). Am Ende den Brief nach der Vorlage in `REFERENCE.md` zurückspiegeln und bestätigen lassen. Er ist die Vorgabe für alle Subagents und für dich.

Defaults, wenn der User nichts anderes sagt: **3 Mockups**, Startpunkt Startseite, Desktop zuerst.

## Phase 1: Recherche (parallele Subagents)

Alle Agents in **einem** Message-Block starten (`subagent_type="general-purpose"`, `model="haiku"`); die Prompts stehen in `REFERENCE.md`.

- **Inspirations-Scan**, ein Agent pro Quelle: Referenzen, die zu Zielgruppe, Ton und den gewünschten Mustern passen — Layoutmuster, Scroll-Mechanik, Typo-Prinzip, was übertragbar ist. Muster, keine Marken-UI.
- **Bestands-Analyse**, ein Agent: Tokens, Komponenten-Inventar, Seitenstruktur, echte Copy-Strings, was das Produkt tatsächlich tut, Technik. `bestand.md` ist danach verbindlich für Branding und Fachlichkeit in allen Mockups.

**Synthese (du):** Aus den Briefs N deutlich unterschiedliche Richtungen ableiten, jede in drei Zeilen: Name, Kernidee, Signature-Element (das, was man sich merkt). Die Unterschiede liegen auf benennbaren Achsen — hell/dunkel, editorial/produktnah, narrativ/strukturell, ruhig/kinetisch — nie drei Varianten derselben Idee. Richtungen kurz vorstellen; widerspricht der User nicht, bauen.

## Phase 2: N Mockups bauen und verifizieren

Für jedes Mockup:

- **Branding aus `bestand.md`**: Tokens, Fonts, Logo, Icon-Set. Keine erfundenen Farben; fehlt etwas, aus der Palette ableiten.
- **Fachlich korrekt**: Screens, Zahlen und Flows nur so, wie `bestand.md` sie beschreibt. Bei Unsicherheit neutral formulieren statt raten — erfundenes Produktverhalten (Sperren, Limits, Freigaben) ist der teuerste Fehler, weil es im Handoff als Anforderung gelesen wird.
- **Copy** im Ton des Bestands, richtige Anrede, keine Platzhalter.
- **Keine erfundenen Fotos**: fehlt Bildmaterial, dann Platzhalter-Slots oder CSS-UI-Mockups, und den User um echte Assets bitten.
- **Bewegung, wo sie dem Inhalt dient**: `scrollfx.js` liefert `data-reveal`, `data-parallax`, `data-scene` (setzt `--p` von 0 bis 1), `data-counter` und `data-tilt`, jeweils mit `prefers-reduced-motion`-Fallback; der Kontrakt steht im Kopf der Datei. Der Hero ist ohne Scrollen vollständig sichtbar.
- Startseite vollständig von Nav bis Footer, Desktop zuerst; fehlende Mobile-Breakpoints in der Zusammenfassung nennen.

**Verifikation pro Mockup** (Subagent, `haiku`, Prompt in `REFERENCE.md`): Konsole, Screenshots (Anfang, jede Sticky-Szene bei `--p` 0.1 / 0.5 / 0.9, Footer), Layout-Checks bei 1440×900 und 1280×720, fünf Fachaussagen gegen `bestand.md`. Ergebnis nach `design/verify/<richtung>.md`. Defekte fixt du, dann läuft der Verifier erneut, bis er „sauber" meldet.

## Phase 3: Auswahl

`design/mockups/index.html` als Vergleichsboard bauen: pro Richtung Name, Kernidee, Vorschau (Screenshot aus der Verifikation) und Link. Dem User öffnen (`open design/mockups/index.html`).

Via **AskUserQuestion** wählen lassen: welche Richtung, was daraus mitnehmen, was ändern. Kombinationen sind erlaubt („Layout von A, Bewegung von B"). Feedback ins gewählte Mockup einarbeiten; die anderen bleiben unverändert, sie sind die Historie.

## Phase 4: Folgeseiten

Aus `bestand.md` eine Vorschlagsliste ableiten (z.B. Blog-Übersicht, Blog-Detail, Login, Preise, Über uns, Dashboard) und via **AskUserQuestion** (multiSelect) klären: welche Seiten, in welcher Reihenfolge, statisch oder interaktiv, welche Zustände (leer, Fehler, mobil). Erst dann bauen.

Bauregeln: gleiche Nav, Footer, Tokens und Motion-Sprache wie das gewählte Mockup; Querverlinkung zwischen allen Seiten; echte Strings aus dem Bestand (i18n-Dateien); jede Seite durch den Verifier. Interaktive Seiten bekommen echten State für ihre Zustände.

## Phase 5: Handoff-Paket

`design/handoff-{slug}/` mit `README.md` (Schema in `REFERENCE.md`), allen Mockup-Dateien, `scrollfx.js`, Assets und Token-CSS. Screenshots nur auf Wunsch. Am Ende den Pfad nennen; bei verbundener Codebase im README festhalten, welche Screens aus welchen Quelldateien abgeleitet sind.

## Abnahme

- Die N Richtungen sind auf den ersten Blick unterscheidbar.
- Kein Konsolenfehler, keine Überlappungen, alle Szenen in allen Fortschrittszuständen geprüft.
- Branding und Fachlichkeit stimmen mit `bestand.md` überein.
- Copy vollständig, richtiger Ton, richtige Anrede.
- Reduced-Motion-Fallback vorhanden.
- Handoff-README ist ohne Chatverlauf verständlich.

Reihenfolge ist Teil der Qualität: kein Mockup vor dem bestätigten Brief, keine Folgeseite vor geklärter Anzahl und Zuständen.
