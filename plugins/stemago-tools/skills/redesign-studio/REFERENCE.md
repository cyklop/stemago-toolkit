# Redesign Studio — Reference

Detail-Dokumentation für den `/redesign-studio` Skill: Interview-Runden, Brief-Vorlage, Subagent-Prompts, Handoff-Schema.

---

## Interview-Runden (Phase 0)

Bis zu drei Fragen pro Nachricht, Antworten kurz spiegeln, nichts doppelt fragen, nach jeder Runde die Brief-Datei aktualisieren.

### Runde 1 — Ursprung & Ziel
- Welche Seite oder App gestalten wir neu? (URL, Repo, Screenshots)
- Redesign des Bestands oder kompletter Neuaufbau?
- Woran merken wir, dass das Redesign gelungen ist? (Conversion, Wahrnehmung, Wettbewerb, Relaunch)

### Runde 2 — Zielgruppe & Ton
- Wer nutzt die Seite, in welcher Situation?
- Anrede (Du/Sie), Tonalität in drei Adjektiven, Sprache(n)?
- Gibt es Copy, die bleiben muss (Claims, Produktnamen)?

### Runde 3 — Bestand
- Was bleibt fix: Logo, Farben, Fonts, Komponenten, Struktur?
- Was darf weg oder soll bewusst anders werden?
- Gibt es ein Design-System oder eine Codebase als Quelle der Wahrheit? (→ Bestands-Analyse)

### Runde 4 — Inspiration
- Welche Quellen sollen gescannt werden? (awwwards, godly.website, 21st.dev, motionsites.ai, konkrete Konkurrenten)
- Welche Elemente daraus gefallen konkret (Scroll-Ebenen, Typo, Motion, Layout)?
- Was ist ein No-Go?

### Runde 5 — Wunschlayouts
- Gibt es Skizzen, Screenshots, Lieblingsseiten?
- Konkrete Layoutideen (Split-Screen, Sticky-Storytelling, Bento …)?
- Desktop oder Mobile zuerst?

### Runde 6 — Umfang
- Wie viele Mockups in der ersten Runde? (Default 3)
- Welche Seite ist der Startpunkt?
- Abgabeformat und Termin? Stack-Vorgaben für den späteren Nachbau?

### Brief-Vorlage (zurückspiegeln und bestätigen lassen)

```
Projekt: …            Ziel: …
Zielgruppe: …         Ton/Anrede: …
Bleibt: …             Weg/anders: …
Quelle der Wahrheit: … (Design-System / Repo / Live)
Inspiration: … (Quellen + gewünschte Muster)
No-Gos: …
Mockups: N · Startseite: … · Viewport: …
Abgabe: …
```

### Nach der Auswahl (Phase 4)
- Welche Folgeseiten? (Vorschlagsliste aus `bestand.md`)
- Reihenfolge und Tiefe (statisch / interaktiv)?
- Sonderzustände (leer, Fehler, nicht erkannt, mobil)?

---

## Subagent-Prompts (Phase 1 und 2)

Alle mit `subagent_type="general-purpose"`, `model="haiku"`, in einem Message-Block. `<BRIEF>` ist der bestätigte Brief wortgleich; `<slug>` der Projekt-Slug.

### A. Inspirations-Scan — ein Agent pro Quelle

```
Agent(subagent_type="general-purpose", model="haiku",
  description="Inspiration: <quelle>",
  prompt="Du bist Rechercheur. Brief: <BRIEF>.
    Quelle: <URL>. Öffne die Quelle (WebFetch oder Browser) und finde etwa 5-8 Referenzen,
    die zu Zielgruppe, Ton und den gewünschten Mustern passen.
    Pro Referenz: URL · Layoutmuster (Sticky-Storytelling, Bento, Split, Editorial …) ·
    Scroll-/Motion-Mechanik (was beim Scrollen passiert, Dauer, Gefühl) · Typo-Prinzip
    (Größenverhältnisse, Wort-Reveals, Mono-Zahlen …) · warum passend zum Brief ·
    was übertragbar ist (Muster, nicht Marken-UI).
    Fakten, keine Empfehlungen; knapp genug, dass alle Quellen-Briefs zusammen in einem
    Durchgang lesbar sind. Schreibe nach docs/research/redesign-<slug>/inspiration-<quelle>.md
    und gib den Pfad zurück.")
```

### B. Bestands-Analyse — ein Agent

```
Agent(subagent_type="general-purpose", model="haiku",
  description="Bestand analysieren",
  prompt="Du bist Analyst. Brief: <BRIEF>. Quellen: <Design-System-Ordner / Repo / Live-URL>.
    Liefere einen Fakten-Brief, nur aus den Quellen, Unklares als 'unklar' markieren:
    1. Tokens: Farben (Hex), Fonts und Gewichte, Radien, Schatten, Motion-Dauern und Easings
    2. Komponenten-Inventar (Name, Varianten, Zustände)
    3. Seitenstruktur der Ursprungsseite (Sektionen in Reihenfolge)
    4. Copy-Ton: etwa 8 echte Strings zitieren (Anrede, Buttons, Empty-States, Fehler)
    5. Was das Produkt tatsächlich tut: Features, Flows, Begriffe, Zahlenlogik
    6. Technik: Framework, i18n, Icon-Set, Asset-Pfade
    Fakten, keine Empfehlungen. Schreibe nach docs/research/redesign-<slug>/bestand.md
    und gib den Pfad zurück.")
```

### C. Verifier — ein Agent pro Mockup

```
Agent(subagent_type="general-purpose", model="haiku",
  description="Verify: <richtung>",
  prompt="Du bist Prüfer. Prüfe design/mockups/<richtung>/index.html gegen docs/research/redesign-<slug>/bestand.md.
    Öffne die Seite im Browser (Chrome DevTools MCP: navigate_page, resize_page, take_screenshot,
    list_console_messages, evaluate_script; falls nötig über einen lokalen Server:
    python3 -m http.server -d design/mockups 8765). Fallback ohne MCP:
    npx playwright screenshot --viewport-size=1440,900 <url> <png>.
    1. Konsole bei 1440×900: Fehler und Warnungen auflisten (auch fehlende Icons, 404).
    2. Screenshots: Seitenanfang, jede Sticky-Szene bei --p 0.1 / 0.5 / 0.9
       (evaluate_script: window.scrollfx.setProgress(document.querySelectorAll('[data-scene]')[i], 0.5)), Footer.
    3. Layout bei 1440×900 und 1280×720: Überlappungen, abgeschnittene Texte, horizontale
       Scrollbreite, Sticky-Höhen, Schrift unter 12 px, Kontrast, Hero ohne Scrollen vollständig.
    4. Fachlichkeit: fünf Aussagen im Mockup gegen bestand.md prüfen.
    Ausgabe: Liste 'Defekt · Element · Beleg (Screenshot/Konsole) · Fix-Vorschlag'.
    Wenn nichts: 'sauber'. Schreibe nach design/verify/<richtung>.md und gib den Pfad zurück.")
```

### D. Link- und Asset-Check — nach den Folgeseiten

```
Agent(subagent_type="general-purpose", model="haiku",
  description="Links prüfen",
  prompt="Prüfe alle <a href> zwischen den Dateien unter design/mockups/ und alle Asset-Pfade
    (img, link, script). Liste tote Links und fehlende Dateien mit Datei und Zeile. Wenn nichts: 'sauber'.")
```

---

## Handoff-README (Phase 5)

`design/handoff-{slug}/README.md` — ohne Chatverlauf verständlich:

```markdown
# Handoff: <Projekt> Redesign

## Overview
Ziel, Zielgruppe, gewählte Richtung und warum. Hinweis: Die HTML-Dateien sind
Design-Referenz — im Zielstack nachbauen, nicht übernehmen.

## Fidelity
Was ist final (Layout, Typo, Copy), was Platzhalter (Bilder, Daten), was offen.

## Seiten
Pro Seite: Datei · Layout (Sektionen in Reihenfolge) · Komponenten · Copy (Quelle) · Zustände

## Interaktionen und Motion
Pro Effekt: Auslöser, Formel für den Fortschritt (z.B. --p = -top / (höhe - viewport)),
Easing, Dauer, Reduced-Motion-Verhalten. Engine: scrollfx.js (Kontrakt im Dateikopf).

## State Management
Welche Seiten echten State haben und welche Zustände (leer, Fehler, geladen …).

## Tokens
Farben, Fonts, Radien, Schatten, Motion — aus bestand.md, mit Abweichungen begründet.

## Assets
Vorhanden / fehlend / vom Kunden benötigt.

## Dateien
Liste aller Dateien im Paket.

## Responsive
Empfehlung für Breakpoints und was sich pro Breakpoint ändert.

## Quellen (bei verbundener Codebase)
Welche Screens aus welchen Quelldateien abgeleitet sind, Stand (Commit/Datum).

## Offene Punkte
```
