---
name: grill-me
description: "Den User schonungslos zu einem Plan, Design oder Thema befragen — und jede Antwort sofort in eine Brainstorm-Datei checkpointen, damit nichts verloren geht. Verwende wenn: der User einen Plan stresstesten will, sich zu einem Design grillen lassen möchte, eine Brainstorm- oder Discovery-Session braucht, oder Wissen aus dem Kopf in ein Dokument extrahiert werden soll. Auch bei: 'grill mich', 'lass uns brainstormen', 'hilf mir das festzuhalten', 'stress-test meinen Plan', 'gib mir die Birne'. NICHT für formale Spec, Implementierungsplan oder Beads-Tasks — dafür /interview."
---

# Grill Me

Befrage den User schonungslos zu jedem Aspekt des Themas, bis ihr ein gemeinsames Verständnis erreicht. Geh jeden Ast des Entscheidungsbaums durch und löse Abhängigkeiten einzeln auf. Das eigentliche Ziel: **das Wissen aus seinem Kopf in eine dauerhafte, organisierte Markdown-Datei extrahieren**, damit nichts verloren geht, während der Kontext sich füllt.

## Die Capture-Datei ist der ganze Punkt

Lange Interviews füllen den Kontext. Wenn du die Antworten nur im Kopf hältst, wirst du irgendwann etwas falsch erinnern, vermischen oder verlieren. Deshalb **checkpointest du nach jeder einzelnen Antwort auf die Festplatte**. Die Datei — nicht dein Kontext — ist die Quelle der Wahrheit. Der User soll dich nie bitten müssen, den Fortschritt zu speichern.

## Setup (VOR der ersten Frage)

1. **Lege die Capture-Datei** unter `brainstorms/{YYYY-MM-DD}-{topic-slug}.md` an (erstelle den Ordner `brainstorms/`, falls er fehlt). Jede Brainstorm-Erfassung lebt hier. Ein vorhersehbarer Ort, unabhängig vom Thema. Streue Erfassungen NICHT in Projektordner. Wenn eine Session später ein poliertes Ergebnis hervorbringt (Plan, Map, Spec), kann dieses Artefakt in den passenden `projects/`-Ordner wandern — aber die rohe Erfassung bleibt immer in `brainstorms/`.
   - Hol dir das heutige Datum mit `date +%F` (Bash), falls du es nicht schon kennst.
2. **Erstelle die Datei sofort** mit einem Header: Titel, Datum, Ziel der Session und einem leeren Abschnitt "Offene Flags".
3. **Sag dem User, wo du speicherst**, in einer Zeile. Dann stelle Q1.

## Die Checkpoint-Regel (nicht verhandelbar)

Nach JEDER User-Antwort, BEVOR du die nächste Frage stellst:
- Hänge einen strukturierten Eintrag an die Capture-Datei an: das Frage-Thema, die Kernfakten und Entscheidungen aus der Antwort (in seinen Worten, wo die Formulierung zählt), und alle Flags (Dinge die er nicht beantworten konnte, plus wer es kann).
- Aktualisiere oder korrigiere frühere Einträge, falls eine spätere Antwort sie verändert.
- Erst dann stelle die nächste Frage.

Batche niemals mehrere Antworten in einen Write. Checkpointe eine Antwort nach der anderen. Der Punkt: Wenn der Kontext in irgendeinem Moment verloren geht, hält die Datei bereits alles, was bis dahin gesagt wurde.

## Interview-Methode

- Stelle **eine Frage nach der anderen**. Liefere bei jeder deine **empfohlene Antwort** (deine beste Schlussfolgerung aus dem Kontext), damit der User einfach bestätigen, korrigieren oder umlenken kann.
- Löse Abhängigkeiten in der richtigen Reihenfolge: Kläre die übergeordnete Entscheidung, bevor die davon abhängenden kommen.
- Wenn eine Frage durch **Erkunden der Codebase oder Lesen einer Datei/Doku** beantwortet werden kann, tu das, statt zu fragen. Wenn der User dir ein Dokument gibt (z.B. ein Google Doc), lies es und bring nur das Net-New zur Sprache.
- Wenn der User etwas **nicht beantworten kann**, erfasse es als Flag mit dem richtigen Owner und mach weiter. Bleib nicht stehen.
- Mach weiter, bis der User sagt, dass ihr fertig seid, oder du jeden Ast abgedeckt hast. Biete gegen Ende einen Vollständigkeits-Backstop an ("haben wir etwas nicht berührt?").

## Struktur der Capture-Datei

```
# {Thema}: Brainstorm / Discovery Notes
Datum: {datum} · Ziel: {eine Zeile}

## Zusammenfassung / Kernentscheidungen
(laufende Synthese, wird fortlaufend aktualisiert)

## Q&A-Log
### Q1 — {Thema}
- Gefragt: {Frage}
- Erfasst: {Fakten, Entscheidungen, in seinen Worten wo es zählt}
- Flags: {offener Punkt -> Owner}
...

## Offene Flags (ausstehender Input)
- {Punkt} -> {wer es beantworten kann}
```

## Am Ende

- Lies die Capture-Datei ein letztes Mal auf Widersprüche oder Lücken und gleiche sie ab.
- Gib dem User eine kurze Zusammenfassung: was erfasst ist, was noch geflaggt ist, und der vorgeschlagene nächste Schritt.
