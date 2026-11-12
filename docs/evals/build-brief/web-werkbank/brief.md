# Auftragsübersicht mit Sofortsuche

Frau Albers und Frau Demir, die beiden Disponentinnen im Büro, haben die Auftragsübersicht den ganzen Tag offen. Sie suchen darin rund 150 Mal am Tag einen Auftrag, während der Kunde am Telefon wartet. Am Freitag zeige ich ihnen das Ergebnis eine halbe Stunde lang am Bürorechner (27 Zoll, 2560×1440, Chrome). Danach entscheidet der Chef, ob der Rest der Verwaltung auf dieselbe Art umgebaut wird. Qualität ist das Ziel. Nimm dir die Zeit, die sie braucht.

## Der Auftrag

Die Anfrage: Die Auftragsübersicht unter `/auftraege` bekommt eine Sofortsuche und Statusfilter, damit eine Disponentin einen Auftrag am Telefon mit wenigen Tastendrücken findet.

Die Referenz: die heutige Seite `src/app/auftraege/page.tsx`. Sie lädt alle Aufträge und zeigt sie in einer Tabelle, die neuesten zuerst. Darüber steht ein Formular, das nach der exakten Auftragsnummer sucht, sobald man auf „Suchen" klickt. Schließe genau diese Lücken:

- Kunden nennen am Telefon ihren Namen oder ihre Straße, fast nie die Auftragsnummer. Die Suche hilft dann nicht, und man scrollt. → Die Suche findet über Kundenname, Straße, Ort, Auftragsnummer und Titel, beim Tippen und ohne Absenden.
- Der Status steht als Datenbankwert da (`WARTET_AUF_MATERIAL`), der Termin als ISO-Zeitstempel. → Beides steht in Klartext da, siehe unten.
- Wer einen Auftrag öffnet und zurückkommt, hat seine Suche verloren. → Suche und Filter stehen in der URL und überleben Zurück und Neuladen.
- Die Seite kennt nur den Fall „Aufträge vorhanden". → Jeder Zustand unten ist gestaltet.
- Die Seite lädt und zeichnet immer alle Aufträge. Bei 5.000 Aufträgen ist sie nicht mehr bedienbar. → Sie hält die Zeiten unten auch mit 5.000 Aufträgen.
- Die Datenbankabfrage steht in der Seite selbst. Das widerspricht der Konvention der `CLAUDE.md`. → Die Abfragen liegen unter `src/lib/db/`.

Der Star: die Suche. Ich tippe „mey", und der Auftrag von Meyer in der Gartenstraße steht in der ersten Zeile, bevor ich fertig getippt habe. Alles andere ordnet sich ihr unter: Die Filter sind eine einzige Zeile über der Liste. Farbe gibt es nur dort, wo sie etwas bedeutet. Bewegung gibt es nur, wo sie beim Verfolgen der Treffer hilft. Die Ansicht am Handy und die Seite eines einzelnen Auftrags sind einfach und fehlerfrei, mehr nicht.

**Wonach gesucht wird.** Kundenname, Straße, Ort, Auftragsnummer, Titel. Groß- und Kleinschreibung spielt keine Rolle. „mueller" findet „Müller", „strasse" findet „Straße". Ähnliche Schreibweisen finden einander: „Meier" findet „Meyer". Ein exakter Treffer steht dabei vor einem ähnlichen. Bei der Nummer genügen die letzten Ziffern: „412" findet `A-2026-00412`. Mehrere Wörter grenzen ein: „müller bahnhof" findet den Müller in der Bahnhofstraße. Ein Schrägstrich im Suchfeld ist ein normales Zeichen („12/14").

**Beim Tippen.** Die Liste folgt jedem Tastendruck. Solange eine Antwort aussteht, bleibt die bisherige Liste stehen. Zeilen, die Treffer bleiben, behalten ihren Platz, soweit die Reihenfolge es erlaubt. Kopf, Suchfeld, Filterzeile und Spalten ändern beim Tippen weder Höhe noch Breite. Eine ältere Antwort, die nach einer neueren eintrifft, wird verworfen. Eine Liste, die bei jedem Tastendruck leer wird und sich neu füllt, ist keine Sofortsuche.

**Der Treffer steht oben.** Ein Treffer in Zeile 14 ist kein gefundener Auftrag. Die Disponentin liest nur die ersten zwei oder drei Zeilen. Die Reihenfolge ist deshalb die schwerste Stelle des Auftrags. Der erste Treffer ist vorgewählt, sodass Enter ihn sofort öffnet.

**Warum etwas ein Treffer ist.** Der passende Teil ist in der Zeile hervorgehoben, auch bei einem ähnlichen Treffer („Meyer" bei der Eingabe „Meier") und bei der Nummer. Die Hervorhebung ändert die Breite des Textes nicht.

**Tastatur.** `/` setzt den Fokus in die Suche, wenn er nicht schon in einem Eingabefeld steht. Die Pfeiltasten wandern durch die Treffer, der Fokus bleibt dabei im Suchfeld. Enter öffnet den gewählten Auftrag. Esc leert die Suche. Der Weg vom Laden der Seite bis zum geöffneten Auftrag von Meyer ist fünf Tasten lang: `/`, `m`, `e`, `y`, Enter. Gibt es schon eine Seite für einen einzelnen Auftrag, führt Enter dorthin. Gibt es keine, legst du `src/app/auftraege/[id]/page.tsx` an: Nummer, Titel, Beschreibung, Kunde mit Adresse und Telefon, Status, Termin, Monteur, und ein Weg zurück zur Übersicht.

**Statusfilter.** Chips in einer Zeile über der Liste, einer je Status, mehrere gleichzeitig wählbar. Die Namen: Neu, Geplant, In Arbeit, Wartet auf Material, Erledigt, Abgerechnet. Jeder Chip zeigt eine Anzahl. Sie bezieht sich auf die aktuelle Suche: Bei „mey" steht dort, wie viele der Meyer-Treffer in diesem Status liegen. Ein Chip mit der Anzahl 0 bleibt an seinem Platz und wird gedämpft, damit die Zeile beim Tippen nicht springt.

**Die Zeile.** Am Telefon wird nach Name und Adresse gefragt. Kundenname, Straße und Ort sind deshalb das, was man in einer Zeile zuerst liest. Der Datensatz enthält absichtlich mehrere Kunden mit demselben Namen. Sie müssen an Straße und Ort zu unterscheiden sein, ohne die Zeile zu öffnen. Der Status steht als Wort da. Der Termin steht in der Zeitzone Europe/Berlin als „heute 14:30", „morgen 08:00" oder „Mo, 16.11.". Ohne Termin steht „kein Termin" in gedämpfter Schrift. Ohne Monteur bleibt die Stelle ruhig, zum Beispiel mit einem Strich. Der längste Kundenname im Datensatz ist „Wohnungseigentümergemeinschaft Am Alten Güterbahnhof 12–18". Er darf weder die Spalten verschieben noch die Zeile höher machen als die anderen.

**Dichte.** Bei 1440×900 sind ohne Scrollen mindestens 14 Aufträge zu sehen, bei 2560×1440 mindestens 24. Bei 2560 Pixeln Breite läuft die Liste nicht über den ganzen Bildschirm auseinander: Name und Termin einer Zeile liegen so nah beieinander, dass man beide liest, ohne den Kopf zu drehen, zum Beispiel durch eine Liste von höchstens etwa 1.400 Pixeln Breite.

**URL.** Die Suche steht als `?q=`, die Filter als `?status=` in der URL (mehrere Werte durch Komma getrennt, zum Beispiel `?q=mey&status=geplant,in-arbeit`). Tippen ersetzt den Eintrag im Verlauf des Browsers, statt für jeden Buchstaben einen neuen anzulegen. Zurück führt also zur vorigen Seite, nicht zum vorigen Buchstaben. Wer einen Auftrag öffnet und zurückgeht, findet Suche, Filter und gewählte Zeile wieder vor. Alte Links mit `?nr=` funktionieren weiter.

**Zustände.** Jeder ist gestaltet und über einen Schalter direkt erreichbar (siehe „Prüfbarkeit"):

- Keine Treffer. Dieser Zustand kommt täglich vor und ist der wichtigste der leeren Zustände. Er nennt den Suchbegriff und die aktiven Filter. Er bietet „Filter zurücksetzen" an, wenn Filter aktiv sind, und sagt, wie viele Treffer es ohne Filter gäbe. „Keine Daten" ist kein leerer Zustand.
- Keine Aufträge überhaupt (neue Installation). Ein Satz, was hier stehen wird.
- Laden. Beim ersten Aufruf stehen Platzhalterzeilen in der Höhe der echten Zeilen. Während des Tippens bleibt die Liste stehen. Dauert eine Antwort länger als etwa 300 Millisekunden, zeigt ein kleines Zeichen am Suchfeld, dass gesucht wird. Ein Spinner über der Tabelle ist kein Ladezustand.
- Fehler der Datenbank. Die Meldung sagt, was passiert ist und was man tun kann, und bietet „Erneut versuchen" an. Die Eingabe im Suchfeld bleibt erhalten. „Etwas ist schiefgelaufen" ist keine Fehlermeldung.
- 5.000 Aufträge ohne Suche. Das Suchfeld nimmt spätestens eine Sekunde nach dem Aufruf Eingaben an (lokal, Produktions-Build, Szenario `gross`). Die Seite sagt, wie viele Aufträge es gibt und wie viele sie zeigt.

**Am Handy.** Die Monteure öffnen die Seite auch am Handy (390 Pixel breit). Dort genügen das Suchfeld und die Aufträge als gestapelte Blöcke ohne Schatten. Das ist eine Nebensache, aber nichts darf überlaufen oder unbedienbar sein. An den Rechten ändert sich nichts: Wer heute welche Aufträge sieht, sieht sie weiter.

Deine Entscheidung, wo ich nichts festlege:

- Der Aufbau der Zeile ist dein Entwurf, innerhalb der Vorgaben oben.
- Methode der Suche: deine. Volltext in Postgres, Trigramme, ein Index im Speicher oder etwas anderes, solange der Messwert unten hält.
- Die Reihenfolge der Treffer ist dein Entwurf, zum Beispiel: exakte Nummer zuerst, dann Wortanfang im Namen, dann der Rest, bei Gleichstand der nächste Termin oben. Die Suchfälle unten müssen aufgehen.
- Die Reihenfolge ohne Suche ist dein Entwurf, zum Beispiel: die nächsten Termine oben.
- Wie viele Zeilen die Seite auf einmal zeichnet und wie sie weitere holt, ist deine Sache. Seitenzahlen sind ausgeschlossen, siehe unten.
- Wie der Status aussieht, ist dein Entwurf, zum Beispiel ein Wort mit einem kleinen Zeichen in zwei Tönen für „offen" und „abgeschlossen".
- Die Filterzeile am Handy ist dein Entwurf, zum Beispiel waagerecht verschiebbar.
- Termine in der Vergangenheit und in einem anderen Jahr: dein Entwurf, zum Beispiel „gestern 09:00" und „14.11.2025".

Was exzellent sein muss:

- Die Reihenfolge der Treffer. Bei jedem Suchfall unten steht der erwartete Auftrag in Zeile 1.
- Die Ruhe beim Tippen. In einer Bildfolge über die Eingabe „mey" ist die Liste in keinem Bild leer, und Kopf, Filterzeile und Spalten stehen in jedem Bild an derselben Stelle.
- Die Lesbarkeit einer Zeile. Wer die Seite zum ersten Mal sieht, nennt nach einem Blick auf eine Zeile den Kunden, die Adresse, den Status und den Termin, ohne eine Spaltenüberschrift zu lesen.
- Der Zustand „Keine Treffer". Er führt mit einem Tastendruck oder einem Klick zurück zu einer Liste mit Treffern.

Maßstab für Dichte, Ruhe und Tastaturbedienung sind die Listen in Linear und die Suche in Raycast. Das Gegenbild ist ein Admin-Template.

Nicht gewollt:

- Karten mit Schatten (kosten Platz, die Liste wird unruhig, es passen weniger Aufträge auf den Bildschirm)
- Ein Suchfeld mit Knopf daneben (ein zusätzlicher Schritt am Telefon)
- Ein Lade-Spinner über der ganzen Tabelle (die Liste verschwindet beim Tippen)
- Blättern mit Seitenzahlen (was auf Seite 3 steht, findet niemand)
- Status-Badges in sechs Farben (unruhig, und nach einer Woche liest niemand mehr die Farbe)
- Die DaisyUI-Tabelle ohne Anpassung (daran erkennt man das Admin-Template)
- Eine Verzögerung nach dem Tastendruck, die man spürt (sie verbraucht die 150 Millisekunden, bevor die Suche beginnt)

Messlatte: Ein Screenshot der Übersicht bei 2560×1440 mit 5.000 Aufträgen und der Eingabe „mey" geht als Produktbild einer gekauften Software durch. Und: Ich tippe drei Buchstaben eines Kundennamens, und der richtige Auftrag steht in der ersten Zeile, ohne dass sich die Liste dabei sichtbar neu aufbaut.

## Projekt, Werkzeuge und Dateien

- Du arbeitest im aktuellen Ordner, dem Projekt Werkbank. Stack, Konventionen, Befehle, die lokale Datenbank und das Testkonto stehen in der `CLAUDE.md`. Sie gilt, soweit dieser Auftrag nichts anderes sagt.
- Branch: `feat/auftragssuche`, neu vom aktuellen `main`. Du committest nach der ersten Version und nach jeder Runde, damit jeder Stand zurückholbar ist.
- Dein Ergebnis siehst du über Playwright an. Es ist im Projekt (`@playwright/test`), ein erster Test liegt unter `tests/e2e/auftraege.spec.ts`. Fehlt der Browser dazu, lädst du ihn mit `npx playwright install chromium`. Auflösungen: 2560×1440 (der Bürorechner, hier entscheidet sich die Vorführung), 1440×900 und 390×844, jeweils mit Skalierung 1.
- Belege (Screenshots, Bildfolgen, Ausgaben, Messprotokolle) legst du unter `tmp/brief-auftragsuebersicht-sofortsuche/` ab. Der Ordner wird nicht committet. Trag ihn dafür in die `.gitignore` ein, falls er dort fehlt. Die Belege der letzten Runde bleiben dort liegen.
- Führe eine Laufnotiz in `docs/briefs/2026-11-12-auftragsuebersicht-sofortsuche.lauf.md`: Startzeit, und je Runde die Belege, die drei schwächsten Dinge, was du geändert hast, die Messwerte. Bei einem langen Lauf wird dein Kontext zwischendurch verdichtet. Die Notiz und die Commits halten den Stand, auf dem du danach weitermachst. Die Notiz committest du mit.
- Der Auftrag ist eng. Außerhalb der Auftragsübersicht änderst du so wenig wie möglich. In `src/components/` und `src/lib/db/` legst du neue Dateien an, statt bestehende umzubauen, weil andere Seiten sie verwenden. Musst du eine bestehende Datei dort ändern, bleibt ihr Verhalten für die anderen Aufrufer gleich, und du nennst die Änderung im Schlussbericht.
- Dateien, die beim Start schon unversioniert im Arbeitsbaum liegen, gehören mir. Lass sie unverändert und nimm sie nicht in deine Commits auf.

## Prüfbarkeit

Du kannst nur verbessern, was du gezielt ansehen kannst. Die folgenden Schalter gehören deshalb zum Auftrag. Bau sie mit der ersten Version:

- **Testdaten mit festem Seed.** Das heutige `prisma/seed.ts` würfelt bei jedem Lauf neue Namen und Termine. Zwei Screenshots sind damit nicht vergleichbar. Erweitere es um drei Szenarien, die bei jedem Lauf dieselben Daten ergeben: `npm run db:seed -- --szenario=leer` (keine Kunden, keine Aufträge), `--szenario=standard` (40 Kunden, 220 Aufträge; das ist auch der Stand ohne Angabe, damit der Befehl aus der `CLAUDE.md` weiter gilt) und `--szenario=gross` (5.000 Aufträge bei rund 900 Kunden). Termine liegen relativ zum Tag des Seed-Laufs, damit es immer Aufträge für heute und morgen gibt. Die Szenarien ersetzen nur Kunden, Monteure und Aufträge. Alles andere in der Datenbank bleibt stehen, vor allem die Benutzerkonten, weil sonst die Anmeldung nicht mehr geht.
- **Ankerdatensätze**, in `standard` und `gross` gleich:
  - Kundin Annegret Meyer, Gartenstraße 7, 26135 Oldenburg, mit dem Auftrag `A-2026-00412` „Gastherme: jährliche Wartung", Geplant, Termin heute 14:30.
  - Kunde Meyerhoff Immobilien GmbH, Lindenallee 3, Oldenburg, mit einem Auftrag in fünf Tagen. Kein Kunde heißt Meier oder Maier.
  - Kunde Jürgen Müller, Bahnhofstraße 21, 26180 Rastede. In `gross` gibt es zwölf weitere Kunden namens Müller in anderen Straßen und Orten.
  - Kunde „Wohnungseigentümergemeinschaft Am Alten Güterbahnhof 12–18" mit einem Auftrag „Druckminderer tauschen", ohne Termin und ohne Monteur.
  - Mindestens ein Auftrag in jedem der sechs Status.
  
  Die Schreibweise der Namen folgt dem bestehenden Seed-Skript. Die übrigen Daten sind deine Sache. Sie dürfen die Suchfälle nicht mehrdeutig machen.
- **Suchfälle**, als Playwright-Test gegen `gross`. Erwartet ist jeweils die erste Zeile: „mey" → `A-2026-00412` · „meier" → ein Auftrag von Annegret Meyer · „412" → `A-2026-00412` · „garten" → `A-2026-00412` · „mueller bahnhof" → der Auftrag von Jürgen Müller · „wohnungseig" → „Druckminderer tauschen" · „druckmind" → „Druckminderer tauschen". Ergänze eigene Fälle, wo dir die Reihenfolge unsicher vorkommt.
- **`?state=<name>`** auf `/auftraege`: `laedt` hält den Ladezustand des ersten Aufrufs fest, `fehler` lässt die Abfrage der Aufträge scheitern, `leer` zeigt die Seite so, als gäbe es keine Aufträge. So siehst du diese Zustände, ohne die Datenbank umzustellen.
- **`?verzoegerung=<ms>`**: verzögert jede Antwort der Suche um die angegebene Zeit. Damit siehst du, ob die Liste bei langsamer Antwort stehen bleibt und ob überholte Antworten verworfen werden.
- **`?q=` und `?status=`** gehören zum Produkt und öffnen jeden Such- und Filterzustand direkt: keine Treffer mit `?q=zzzz`, der lange Name mit `?q=wohnungseig`.

`?state` und `?verzoegerung` wirken nur, wenn `process.env.NODE_ENV !== 'production'` gilt, damit keine Hintertür ausgeliefert wird. Beleg dafür: Im Produktions-Build zeigt `/auftraege?state=fehler` die normale Liste.

**Messung der Antwortzeit.** Ein Skript tippt die Suchfälle Zeichen für Zeichen und misst je Tastendruck die Zeit, bis die Liste den Stand dieser Eingabe zeigt. Gemessen wird mit dem Szenario `gross` gegen den lokalen Produktions-Build (`npm run build`, dann `npx next start -p 3101`), weil der Entwicklungsserver Seiten beim ersten Aufruf übersetzt und die Zeiten verfälscht. Der Wert ist das 95. Perzentil über alle Tastendrücke. Dasselbe Skript misst die Zeit vom Aufruf der Seite bis zur ersten angenommenen Eingabe. Wie das Skript erkennt, dass die Liste steht, ist deine Methode. Lässt sich der Produktions-Build lokal nicht anmelden oder starten, misst du nach einem Aufwärmdurchlauf im Entwicklungsmodus und schreibst das in den Bericht.

In dieser Umgebung lässt sich nicht beurteilen:

- Die echten Daten des Betriebs (rund 3.800 Aufträge, viele gleiche Kundennamen) → die zwölf Müller im Szenario `gross` stehen dafür ein; der Test mit den echten Daten kommt in die Liste „Von mir zu prüfen".
- Die Bedienung am Telefon unter Zeitdruck → du spielst den Weg `/`, „mey", Enter, Zurück nur mit der Tastatur durch und zählst die Tasten; das Telefonat selbst kommt in die Liste.
- Echte Geräte: der Bürorechner mit seiner Skalierung, das Handy der Monteure mit Touch und Safari → du prüfst die drei Auflösungen im Browser; die Geräte kommen in die Liste.
- Die Antwortzeit auf dem Server des Betriebs → du misst lokal und nennst im Bericht den Rechner, auf dem du gemessen hast; die echte Messung kommt in die Liste.
- Ob es den beiden Disponentinnen gefällt → das bleibt bei mir.

Schreib „geprüft" nur zu dem, was du in diesem Lauf an einem Beleg gesehen hast. Alles andere heißt „nicht geprüft".

## Harte Regeln

- Alle Texte der Oberfläche sind echte Texte in Sprache und Anrede der `CLAUDE.md`, auch in den leeren Zuständen und Meldungen. Keine Blindtexte und keine Emojis als Icons, weil Platzhalter verdecken, ob das Layout mit echten Inhalten hält.
- Keine Fehler in der Konsole und keine fehlgeschlagenen Anfragen, ausgenommen der erzwungene Zustand `?state=fehler`. Ein Fehler in der Konsole fällt in der Vorführung nicht auf, im Betrieb aber schon.
- Alles ist mit der Tastatur bedienbar, der Fokus ist sichtbar, der Kontrast beträgt auch bei gedämpftem Text mindestens 4,5:1, weil die Disponentin beim Telefonieren nicht zur Maus greift und den ganzen Tag auf diese Seite sieht.
- Bewegung respektiert `prefers-reduced-motion`. Bei dieser Einstellung wechselt die Liste ohne Übergang.
- Nichts wird von fremden Servern geladen (Schriften, Skripte), weil die Anwendung heute ohne fremde Dienste auskommt und das so bleiben soll.
- Farben, Abstände und Komponenten kommen aus dem Theme `werkbank` und aus DaisyUI, angepasst an die Vorgaben oben. Die Theme-Datei selbst bleibt unverändert, weil sie alle Seiten betrifft.
- Die Suchfälle prüfen die Reihenfolge, sie legen sie nicht fest. Bau keine Sonderbehandlung für die Ankerdatensätze ein, denn die echten Kunden heißen anders. Der bestehende Test bleibt gültig: Die Überschrift „Aufträge" bleibt.

## Risiken

- **Die Suche zuerst messen.** Beim letzten Versuch wurde die Suche erst am Ende mit vielen Daten ausprobiert, und sie war zu langsam. Bau deshalb zuerst das Szenario `gross`, die Suchabfrage und die Messung. Erst wenn die Suchfälle aufgehen und der Messwert hält, gestaltest du.
- **Dann ein Ausschnitt.** Bring zuerst die Liste mit der Eingabe „mey" bei 2560×1440 auf Zielqualität und bau erst dann Filter, Zustände und die Ansicht am Handy. Sonst füllst du die ganze Fläche mit einer Zeile, die die Messlatte nicht erreicht.
- **Die Datenbank erkennen.** Du arbeitest nur gegen die lokale Entwicklungsdatenbank: `DATABASE_URL` in `.env.local` zeigt auf `localhost:5433` und `werkbank_dev`. Prüf das vor dem ersten Seed-Lauf und vor jeder Migration. Zeigt die Adresse woandershin, änderst du an der Datenbank nichts und nennst das im Bericht. Lies vorher, wie das bestehende Seed-Skript aufräumt, weil Rechnungen und Konten an den Aufträgen hängen können.
- **Der alte Server.** Ein Prozess, der noch auf Port 3100 oder 3101 läuft, liefert einen alten Stand aus, und der Produktions-Build zeigt Änderungen erst nach einem neuen `npm run build`. Prüf vor jeder Runde, dass der Server den aktuellen Stand zeigt.

## Prozess

1. **Prüfweg zuerst.** Halte die Startzeit in der Laufnotiz fest (`date`). Beweise dann am kleinsten möglichen Beispiel, dass du dein Ergebnis zu sehen bekommst: Datenbank und Entwicklungsserver laut `CLAUDE.md` starten, mit dem Testkonto anmelden, die heutige Seite `/auftraege` bei 2560×1440 als Screenshot speichern und den Screenshot öffnen. Ohne funktionierenden Prüfweg sind alle Runden blind.
2. **Eine vollständige erste Version.** Alles aus dem Auftrag ist da und läuft, auch die Schalter, in der Reihenfolge aus dem Abschnitt „Risiken". Prüfe sie über den Prüfweg und behebe jeden Fehler. Committe.
3. **Mindestens vier Verbesserungsrunden.** In jeder Runde:
   - Sammle Belege. Bei 2560×1440 mit dem Szenario `gross`: die Liste ohne Suche, „mey", „meier", „412", „mueller bahnhof", „mey" mit zwei gewählten Filtern, keine Treffer, der lange Name, `?state=leer`, `?state=laedt`, `?state=fehler`. Bei 1440×900 und 390×844: die Liste ohne Suche, „mey", keine Treffer. Dazu eine Bildfolge im Abstand von etwa 0,1 Sekunden über die Eingabe „mey" mit `?verzoegerung=200`, die Ausgabe der Konsole und des Netzwerks, der Tastaturdurchlauf `/`, „mey", Enter, Zurück, die Ausgabe von `npm run test` und `npm run test:e2e` und die Messung der Antwortzeit.
   - Sieh dir jeden Beleg wirklich an. Ein Screenshot, den du nicht geöffnet hast, und eine Ausgabe, die du nicht gelesen hast, sind keine Belege.
   - Urteile als strenger Produktdesigner, der die Ansicht zum ersten Mal sieht, sie mit den besten Werkzeugen dieser Art vergleicht und an der Messlatte misst. Urteile danach als Frau Albers, die zum 150. Mal an diesem Tag einen Auftrag sucht, während der Kunde wartet.
   - Benenne die drei schwächsten Dinge.
   - Behebe sie.
   - Prüfe mit frischen Belegen, ob sie behoben sind. Trag die Runde in die Laufnotiz ein und committe.
4. **Messwert vor Neuem.** Liegt das 95. Perzentil der Antwortzeit über 150 Millisekunden (Szenario `gross`, lokal, gemessen wie oben) oder geht ein Suchfall nicht auf: Behebe das, bevor du etwas hinzufügst oder verschönerst.
5. **Schluss.** Du hörst auf, wenn eine weitere Runde Frau Albers und Frau Demir in der Vorführung nicht mehr auffiele, frühestens nach den vier Runden, oder 60 Minuten nach deinem Start. Prüf die Uhrzeit am Ende jeder Runde. Das Zeitlimit geht vor: Ist es erreicht, bringst du die laufende Behebung zu Ende, prüfst sie und schreibst den Bericht, auch wenn noch keine vier Runden voll sind. Lass die Datenbank am Ende im Szenario `gross` stehen, weil ich damit vorführe.
6. **Schlussbericht**, siehe unten.

## Durchhalten und Grenzen

Während des Laufs sitzt niemand daneben. Arbeite den ganzen Auftrag ab, ohne auf eine Antwort zu warten. Wenn du merkst, dass du eine Restliste schreiben oder anbieten willst weiterzumachen, mach stattdessen mit dem nächsten Teil weiter.

Gewöhnliche Hindernisse (ein Fehler, eine Zeitüberschreitung, ein Werkzeug, das nicht antwortet, ein leeres Ergebnis, eine Datenbank, die noch nicht läuft) untersuchst du zuerst. Sind sie keine echte Sperre, arbeitest du dich mit deinen Mitteln hindurch: warten und wiederholen, die Anfrage korrigieren, einen anderen Weg nehmen.

Ohne Rückfrage erlaubt:

- Dateien anlegen und ändern in `src/app/auftraege/`, `src/components/`, `src/lib/db/`, `prisma/` und `tests/`
- `package.json` und die Lock-Datei für neue Skripte und Pakete, die Playwright-Konfiguration, eine Zeile in der `.gitignore`, die Laufnotiz und der Ordner für die Belege
- Die lokale Datenbank starten, die Szenarien einspielen, Migrationen anlegen und auf `werkbank_dev` anwenden (auch einen Index oder eine Postgres-Erweiterung für die Suche)
- Entwicklungsserver, Produktions-Build und lokaler Start auf den Ports 3100 und 3101, Vitest, Playwright, `npx playwright install chromium`
- Commits auf `feat/auftragssuche`
- Ein neues Paket im Projekt, wenn es nötig ist. Du nennst es im Schlussbericht mit Grund.

Nicht anfassen:

- `src/app/rechnungen/` und `src/lib/auth/` bleiben unverändert (beides läuft produktiv, und der Steuerberater hat die Rechnungslogik abgenommen). Brauchst du dort etwas, baust du es auf deiner Seite und nennst die Stelle im Bericht.
- Bestehende Modelle und Spalten im Prisma-Schema bleiben, wie sie sind (Rechnungen und Anmeldung hängen daran). Ergänzen darfst du Indizes, Erweiterungen und neue Spalten, die nur der Suche dienen.
- Alle Pfade im Projekt, die nicht in der Liste oben stehen, und alles außerhalb des Projektordners bleiben unverändert (der Auftrag ist eng, und nebenbei aufgeräumter Code macht die Durchsicht schwer).
- Kein Push, kein Pull Request, kein Deploy (ich sehe mir das Ergebnis zuerst an).
- Keine andere Datenbank als `werkbank_dev` auf `localhost:5433` (alles andere könnten echte Daten sein).
- Keine weitere UI-Bibliothek neben DaisyUI (Vorgabe des Projekts) und keine globalen Installationen außer dem Browser für Playwright (mein Rechner soll bleiben, wie er ist).

Stößt du an eine dieser Grenzen, umgehst du sie nicht. Du arbeitest an allem weiter, was nicht davon abhängt, und nennst die Stelle im Schlussbericht.

Entscheidungen, die dieser Auftrag nicht vorhergesehen hat, triffst du selbst, und zwar so, wie es der Messlatte am besten dient. Halte sie in der Laufnotiz fest.

## Schlussbericht

Ich habe den Lauf nicht gesehen und komme aus anderer Arbeit. Schreib den Bericht so, dass er ohne Vorwissen verständlich ist: das Wichtigste zuerst, ganze Sätze, einfache Wörter, keine Abkürzungen, die du während der Arbeit erfunden hast. Er ist kurz und enthält:

1. Wie ich das Ergebnis starte und was ich in den ersten Sekunden tue.
2. Den besten Moment und die URL, die ihn direkt zeigt.
3. Was du gebaut und verwendet hast: die Methode der Suche in zwei Sätzen, jede Migration, jede neue Abhängigkeit mit Grund, jede geänderte Datei außerhalb von `src/app/auftraege/`.
4. Die Messwerte der letzten Runde neben ihrer Schwelle: das 95. Perzentil der Antwortzeit neben 150 Millisekunden, die Zeit bis zur ersten Eingabe neben einer Sekunde, den Rechner, die Angabe, ob gegen den Produktions-Build gemessen wurde, und die Zahl der bestandenen Suchfälle.
5. Bekannte Mängel, auch die, die du nicht beheben konntest.
6. Entscheidungen, die du für mich getroffen hast, und Grenzen, an die du gestoßen bist.
7. In welchem Szenario die Datenbank steht und wie ich den Standard wiederherstelle.
8. Die Liste „Von mir zu prüfen": jeder Punkt als Prüfschritt mit der URL oder dem Befehl, der ihn vorbereitet, und dem, worauf ich achten soll. Dazu gehören mindestens die echten Daten des Betriebs, ein Telefonat mit Frau Albers oder Frau Demir, der Bürorechner, ein Handy eines Monteurs und die Antwortzeit auf dem Server.
