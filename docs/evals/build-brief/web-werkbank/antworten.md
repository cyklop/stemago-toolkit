# Antwortblatt: Web-Feature im Next.js-Projekt „Werkbank"

Der User hat den Skill aufgerufen mit: „Auftragsübersicht mit Sofortsuche".

So liest du das Blatt: Zu jedem Thema steht die **Erstantwort** des Users. Ist sie vage, steht darunter die **Antwort auf Nachfrage**; sie gilt erst, wenn du nachgehakt hast. Zu allem, was hier nicht steht, sagt der User: „Dein Vorschlag passt."

## Einsatz und Publikum
Erstantwort: „Das ist für die Nutzer im Büro, es soll einfach besser werden."
Auf Nachfrage: „Frau Albers und Frau Demir, die beiden Disponentinnen. Sie haben die Seite den ganzen Tag offen und suchen am Telefon Aufträge, während der Kunde wartet, grob 150 Mal am Tag. Ich zeige es ihnen am Freitag eine halbe Stunde am Bürorechner (27 Zoll, 2560×1440, Chrome), danach entscheidet der Chef, ob wir den Rest der Verwaltung auch so umbauen."

## Anfrage
„Die Auftragsübersicht bekommt eine Sofortsuche und Statusfilter, damit man einen Auftrag am Telefon in ein paar Sekunden findet."

## Referenz
Erstantwort: „Die jetzige Seite halt. Die ist schlecht."
Auf Nachfrage (zu deinen Vorschlägen aus dem Code): „Stimmt alles. Dazu: Die Kunden nennen am Telefon nie die Auftragsnummer, sondern ihren Namen oder die Straße. Man muss also scrollen. Der Status steht als Datenbankwert da (WARTET_AUF_MATERIAL), der Termin als ISO-Zeitstempel. Und wenn man etwas gefunden hat und zurückkommt, ist die Suche weg."

## Star
Erstantwort: „Die Suche, die Filter und eine schöne Tabelle."
Auf Nachfrage (welches eine?): „Die Suche. Wenn ich nur 30 Sekunden habe, zeige ich: Ich tippe ‚mey' und der Auftrag von Meyer in der Gartenstraße steht oben, bevor ich fertig getippt habe."

## Konkretion
- Gesucht wird über Kundenname, Straße, Ort, Auftragsnummer (auch nur die letzten Ziffern, „412" findet A-2026-00412), Titel. Tippfehler: „Meier" soll „Meyer" finden, „Mueller" soll „Müller" finden.
- Ergebnisse erscheinen beim Tippen. Erstantwort zur Geschwindigkeit: „Es soll schnell sein." Auf Nachfrage: „Unter 150 Millisekunden vom Tastendruck bis die Liste steht, mit 5.000 Aufträgen lokal."
- Der Treffergrund ist sichtbar: der passende Teil ist hervorgehoben.
- Tastatur: `/` setzt den Fokus in die Suche, Pfeiltasten wandern durch die Treffer, Enter öffnet den Auftrag, Esc leert die Suche.
- Statusfilter als Chips über der Liste, mit Anzahl je Status. Mehrere wählbar. Status in Klartext: Neu, Geplant, In Arbeit, Wartet auf Material, Erledigt, Abgerechnet.
- Termin als „heute 14:30", „morgen", „Do, 14.11.", ohne Termin: „kein Termin" in gedämpfter Schrift.
- Suche und Filter stehen in der URL und überleben Zurück und Neuladen.
- Zustände: keine Aufträge überhaupt; keine Treffer (mit Vorschlag „Filter zurücksetzen"); Laden; Fehler der Datenbank; sehr langer Kundenname („Wohnungseigentümergemeinschaft Am Alten Güterbahnhof 12–18"); 5.000 Aufträge.
- Schwere Stellen laut User: „Dass die Liste beim Tippen nicht springt und flackert. Und dass man den Treffer nicht suchen muss, weil er irgendwo in der Mitte steht."
- Mobil: Die Monteure nutzen die Seite auch am Handy (390 px), dort reicht Suche plus Liste als Karten. Nebensache, darf aber nicht kaputt sein.

## Freiheit
„Wie die Zeile aufgebaut ist, überlasse ich dir. Auch wie die Suche technisch läuft (Postgres-Volltext, Trigramme, im Speicher): deine Entscheidung, solange die 150 ms halten. Die Sortierung der Treffer ist dein Entwurf, zum Beispiel: exakte Nummer zuerst, dann Namensanfang, dann der Rest, bei Gleichstand der nächste Termin oben."

## Exzellent / Nicht gewollt
Erstantwort: „Es soll modern und hochwertig aussehen."
Auf Nachfrage: „Modern heißt für mich: wie Linear oder die Suche in Raycast. Dicht, ruhig, alles per Tastatur, nichts wackelt. Nicht wie ein Admin-Template. Exzellent sein müssen: die Reihenfolge der Treffer, die Ruhe beim Tippen, die Lesbarkeit einer Zeile auf einen Blick, der leere Zustand. Nicht haben will ich: Karten mit Schatten, ein Suchfeld mit Button daneben, ein Lade-Spinner über der ganzen Tabelle, Pagination mit Seitenzahlen, bunte Status-Badges in sechs Farben."
Gründe auf Nachfrage: Button = zusätzlicher Schritt am Telefon; Spinner = Liste verschwindet beim Tippen; Pagination = man findet nichts, was auf Seite 3 steht; sechs Farben = unruhig, man liest die Farbe nicht mehr.

## Messlatte
Erstantwort: „Die Disponentinnen sollen zufrieden sein."
Auf Nachfrage: „Ein Screenshot der Übersicht geht als Produktbild einer gekauften Software durch. Und: Ich tippe drei Buchstaben eines Kundennamens, und der richtige Auftrag steht in der ersten Zeile, ohne dass sich die Liste dabei sichtbar neu aufbaut."

## Prüfbarkeit
„Mach einen Vorschlag." Wichtig ist dem User zusätzlich: ein Datensatz mit 5.000 Aufträgen und festem Seed, weil der jetzige Seed zufällig ist. Testkonto steht in der CLAUDE.md. Playwright ist im Projekt. Auflösungen: 2560×1440 (Bürorechner), 1440×900, 390×844.
Zu „nicht prüfbar": Die echten Daten des Betriebs (rund 3.800 Aufträge, viele Dubletten bei Kundennamen) bekommt der Lauf nicht. Das Verhalten am Telefon unter Zeitdruck auch nicht.

## Laufgröße
„Was kostet das?" → nach deiner Auskunft: Stufe mittel, 4 Runden mindestens, 60 Minuten. Messwert: die 150 ms mit 5.000 Aufträgen; darüber wird zuerst das behoben.

## Grenzen
- Schreiben nur in `src/app/auftraege/`, `src/components/`, `src/lib/db/`, `prisma/`, `tests/`. Rechnungen (`src/app/rechnungen/`) und Anmeldung (`src/lib/auth/`) nicht anfassen: laufen produktiv, und der Steuerberater hat die Rechnungslogik abgenommen.
- Branch: `feat/auftragssuche` vom aktuellen `main`. Commits ja, nach jeder Runde. Kein Push, kein PR.
- Neue Pakete: nur wenn nötig, mit Begründung im Bericht. Keine UI-Bibliothek zusätzlich zu DaisyUI.
- Datenbank: nur `werkbank_dev` lokal (Port 5433). Migrationen anlegen und lokal anwenden ist okay.
- Bestehender Code: so wenig wie möglich ändern außerhalb der Auftragsübersicht. Kein Aufräumen nebenbei.
- Prüfschalter: nur im Entwicklungsmodus.

## Risiken
Erstantwort: „Keine Ahnung, sag du."
Ergänzung nach deinem Vorschlag: „Beim letzten Mal hat jemand die Suche erst am Ende mit vielen Daten probiert, und dann war sie langsam. Also zuerst die Suche mit den 5.000 Aufträgen messen, bevor irgendetwas hübsch gemacht wird."

## Sprache des Prompts
Deutsch.
