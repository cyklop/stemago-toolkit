# Profil: Web

Gilt für Web-Apps und Websites: Next.js, React, Vue, Svelte, Astro, Contao, Symfony mit Templates, reine HTML-Seiten. Das Profil unterscheidet zwei Arten von Vorhaben, weil ihre Regeln auseinandergehen:

- **Produkt-Oberfläche:** ein Feature in einer Anwendung (Formular, Übersicht, Suche, Dashboard, Ablauf über mehrere Schritte). Es zählen Zustände, Daten, Bedienbarkeit.
- **Schaustück:** eine Landingpage, eine 3D-Szene, eine Animation, ein Spiel. Es zählen das Bild, die Bewegung und die ersten Sekunden.

Welche Art vorliegt, entscheidest du aus dem Kontext. Du fragst nur bei einer Mischung, und dann nach dem Star.

## So sieht der Lauf sein Ergebnis

Über einen echten Browser, den er selbst steuert: lokalen Server starten, Seite laden, Eingaben senden (klicken, tippen, ziehen, scrollen, Tasten), Screenshots machen, Konsole und Netzwerk lesen.

Such im Kontext, was dafür schon da ist, und nenn das Werkzeug im Prompt beim Namen:

- Playwright oder Cypress in den `devDependencies`, vorhandene End-to-End-Tests
- ein Browser-MCP-Server in `.mcp.json` oder in der `CLAUDE.md` (Chrome DevTools, Playwright)
- der Startbefehl des lokalen Servers und sein Port (`package.json`-Skripte, `CLAUDE.md`, bei Contao oft DDEV oder der Symfony-Server)
- Testkonto und lokale Datenbank, falls die Seite eine Anmeldung braucht

Ist nichts da, klärst du im Interview, ob der Lauf Playwright als Entwicklungsabhängigkeit ins Projekt aufnehmen und den Browser dazu laden darf. Ohne Browser gibt es keinen Prüfweg, und dann ist dieses Vorgehen für das Vorhaben nicht geeignet. Sag das dem User, statt einen Prompt zu schreiben, dessen Runden blind laufen.

Feste Auflösungen gehören in den Prompt. Üblich sind 1440×900 und 390×844, bei Schaustücken zusätzlich 1920×1080. Maßgeblich ist das Gerät, auf dem das Publikum das Ergebnis sieht.

## Schalter für Zustände

URL-Parameter, die nur im Entwicklungsmodus wirken:

| Schalter | Zweck | Für |
|---|---|---|
| `?state=<name>` | einen benannten Zustand direkt anzeigen: `leer`, `laedt`, `fehler`, `voll`, `zuviel`, `ohne-rechte` | Produkt-Oberfläche |
| `?seed=<n>` | dieselben Testdaten bei jedem Aufruf, damit zwei Screenshots vergleichbar sind | beide |
| `?step=<n>` | einen Schritt in einem mehrstufigen Ablauf direkt öffnen | Produkt-Oberfläche |
| `?delay=<ms>` | Antworten verzögern, um Ladezustände und überholte Antworten zu sehen | Produkt-Oberfläche |
| `?t=<sekunden>` | Animation an einem Zeitpunkt einfrieren | Schaustück |
| `?s=<0..1>` | Scrollposition setzen | Schaustück mit Scroll-Regie |
| `?view=<name>` | eine Kamera oder Ansicht wählen | Schaustück |
| `?auto=1` | Ablauf spielt sich selbst (Demo, Bot); beweist, dass er durchläuft | Spiel, geführter Ablauf |
| `?motion=0` | Bewegung aus, für Standbilder und für den Vergleich mit `prefers-reduced-motion` | beide |

Parameter, die ohnehin zum Produkt gehören (Suchbegriff, Filter, Seite), zählen mit: Sie öffnen viele Zustände direkt und bleiben auch in der Produktion.

Bei Anwendungen mit Datenbank reicht ein URL-Parameter oft nicht. Dann gehören benannte Testdatensätze dazu: ein Seed-Skript mit Szenarien (zum Beispiel `leer`, `standard`, `gross`), das bei jedem Lauf dieselben Daten ergibt und gegen die lokale Entwicklungsdatenbank läuft. Dazu einige Ankerdatensätze, die der Prompt beim Namen nennt, damit Belege und Suchfälle sich darauf beziehen können. Der Prompt sagt, was jedes Szenario enthält und was es in der Datenbank nicht anrührt (zum Beispiel die Benutzerkonten).

Die Prüfschalter sind im Produktions-Build abgeschaltet. Im Prompt steht, woran das hängt (zum Beispiel `process.env.NODE_ENV !== 'production'`), damit der Lauf keine Hintertür ausliefert, und der Lauf belegt es mit einem Aufruf im Produktions-Build.

## Belege je Runde

- Screenshots der wichtigen Zustände in den vereinbarten Auflösungen. Bei Schaustücken mindestens drei verschiedene Momente und ein Eingabezustand, bei Scroll-Regie sechs oder mehr Scrollpositionen.
- Für Bewegung: eine Bildfolge im Abstand von etwa 0,1 Sekunden über die wichtigste Bewegung. Ein Einzelbild zeigt nicht, ob etwas ruckt oder flackert.
- Konsole und Netzwerk: keine Fehler, keine fehlgeschlagenen Anfragen.
- Ein durchgespielter Ablauf mit Eingaben aus dem Skript, vom Einstieg bis zum Ende.
- Ausgabe der vorhandenen Tests.

Viele Zustände mal mehrere Auflösungen ergeben schnell mehr Belege, als eine Runde trägt. Dann gilt die Regel aus `REFERENCE.md`, „Laufgröße": in jeder Runde die Zustände des Stars in der Hauptauflösung, die volle Abdeckung nach der ersten Version und in der letzten Runde.

## Messwerte und Schwellen

| Art | Messwert | Übliche Schwelle |
|---|---|---|
| Schaustück | Bildrate bei 1920×1080 | mindestens 50 Bilder pro Sekunde |
| Produkt-Oberfläche | Zeit bis zur bedienbaren Ansicht mit dem Datensatz `gross` | mit dem User festlegen, zum Beispiel höchstens 1 Sekunde |
| Produkt-Oberfläche | Antwortzeit der wichtigsten Aktion (Suche, Speichern) | mit dem User festlegen, als 95. Perzentil |
| beide | Konsolenfehler | 0 |
| beide | automatische Prüfung der Barrierefreiheit (axe, Lighthouse) | keine schweren Verstöße |

Einer davon wird der Messwert im Prozess, die übrigen stehen als harte Regeln da.

**Wogegen gemessen wird:** Zeiten misst der Lauf gegen den lokalen Produktions-Build, nicht gegen den Entwicklungsserver. Der übersetzt Seiten beim ersten Aufruf und verfälscht die Werte. Die Prüfschalter wirken dort nicht, die Messung nutzt deshalb Testdaten und die Parameter des Produkts. Lässt sich der Produktions-Build lokal nicht starten oder anmelden, misst der Lauf nach einem Aufwärmdurchlauf im Entwicklungsmodus und schreibt das in den Bericht.

Lokal gemessene Zeiten sagen nichts über die Produktion. Im Prompt steht deshalb die Messbedingung dabei, und die echte Ladezeit kommt in die Liste „Von mir zu prüfen".

## Rolle des Kritikers

- Schaustück: ein strenger Art Director, der das Bild mit der besten Arbeit dieser Art vergleicht.
- Produkt-Oberfläche: ein strenger Produktdesigner, der die Ansicht zum ersten Mal sieht und sie mit den besten Werkzeugen dieser Art vergleicht. Er prüft, ob man ohne Erklärung weiß, was zu tun ist, ob jeder Zustand gestaltet ist und ob echte Inhalte hineinpassen.
- Bei allem, was jemand täglich und oft bedient (Suche, Erfassung, Ablauf): zusätzlich die Person aus dem ersten Absatz des Prompts, die es zum zweihundertsten Mal tut.

## Harte Regeln (Auswahl für den Prompt)

Jede mit ihrem üblichen Grund. Passt der Grund nicht zum Vorhaben, lass die Regel weg oder nimm den aus dem Gespräch.

Für beide Arten:

- Echte Texte in der Sprache und Anrede des Produkts, keine Blindtexte, keine Emojis als Icons (Platzhalter verdecken, ob das Layout mit echten Inhalten hält).
- Keine Fehler in der Konsole und keine fehlgeschlagenen Anfragen (sie fallen in der Vorführung nicht auf, im Betrieb schon).
- Bedienbar mit der Tastatur, sichtbarer Fokus, ausreichender Kontrast (wer viel damit arbeitet, greift nicht zur Maus, und nicht jeder sieht gleich gut).
- Bewegung respektiert `prefers-reduced-motion` (manche Menschen vertragen Bewegung im Bild nicht).
- Nichts lädt von fremden Servern, was der Auftrag nicht nennt: Schriften, Skripte, Tracking (Datenschutz, und die Seite soll ohne fremde Dienste laufen).

Produkt-Oberfläche:

- Jede Ansicht hat die Zustände leer, lädt, Fehler und voll, und jeder ist gestaltet (im Betrieb kommen alle vor, im Entwurf fehlen sie gern).
- Lange Namen, große Zahlen und fehlende Werte brechen das Layout nicht (echte Daten sind unordentlicher als Testdaten).
- Vorhandene Komponenten, Farben und Abstände des Projekts werden verwendet. Neues nur dort, wo das Bestehende den Star nicht trägt (das Neue soll aussehen, als gehöre es dazu).
- Eine Fehlermeldung sagt, was passiert ist und was der Nutzer tun kann (sonst ruft er an).

Schaustück:

- Die Seite wirkt beim Laden ohne Eingabe lebendig und reagiert in der ersten Sekunde auf Maus oder Tastatur (die ersten Sekunden entscheiden, ob jemand bleibt).
- Ton startet stumm, mit einem sichtbaren Schalter. Die Seite ist ohne Ton vollständig (Browser sperren Ton ohne Klick, und viele sehen die Seite stumm).
- Eigenständige Arbeit: keine Kopie eines bestimmten bestehenden Produkts, Spiels, Films oder Markenauftritts (fremde Rechte).

## Verbotsliste: Vorschläge

Produkt-Oberfläche: Karten mit Schatten, wo eine Liste gemeint ist. Ein Suchfeld mit Knopf daneben. Ein Spinner über der ganzen Ansicht. Blättern mit Seitenzahlen bei durchsuchbaren Listen. Status als bunte Badges in vielen Farben. Die Tabelle oder das Formular der Komponenten-Bibliothek ohne Anpassung. Bestätigungsdialoge für alles. Platzhaltertexte als einzige Beschriftung eines Feldes.

Schaustück: violette Verläufe auf Weiß. Karten in Dreierreihe mit Icon, Titel, Text. Standardschriften ohne Entscheidung (Inter, Roboto, Systemschrift). Glas-Optik überall. Stockfotos und Platzhalter-Illustrationen. Standardmaterialien der 3D-Bibliothek.

## Hier nicht prüfbar

| Was | Ausweichweg oder Rückgabe |
|---|---|
| Echte Geräte: Touch, Safari auf dem iPhone, kleine Android-Geräte, der Bildschirm des Publikums | Auflösungen im Browser prüfen; das Gerät kommt in die Liste „Von mir zu prüfen" |
| Zeigersperre (Pointer Lock) und Vollbild im Browser ohne Fenster | zweiten Bedienweg bauen, der immer geht (Ziehen mit gedrückter Taste, Pfeiltasten) |
| Ton | Der Lauf hört nichts. Er kann prüfen, dass Ton erst nach dem Klick startet und dass die Seite ohne Ton vollständig ist. Der Klang kommt in die Liste. |
| Ladezeit und Verhalten unter Produktionsdaten und echtem Netz | lokal mit dem Datensatz `gross` messen; die echte Messung kommt in die Liste |
| Die echten Daten mit ihren Altlasten (Dubletten, kaputte Einträge) | die bekannten Fälle als Ankerdatensätze nachbauen; der Test mit echten Daten kommt in die Liste |
| Dienste Dritter: Zahlung, E-Mail-Versand, Anmeldung über fremde Anbieter | gegen Testmodus oder Attrappe bauen; der echte Durchlauf kommt in die Liste |
| Bildrate auf dem Gerät des Publikums | auf der lokalen Grafikkarte messen und die Hardware im Bericht nennen |
| Die Bedienung in der echten Lage (am Telefon, unter Zeitdruck, mit Handschuhen) | den Weg nur mit der Tastatur durchspielen und Schritte zählen; die echte Lage kommt in die Liste |
| Ob es dem Publikum gefällt | bleibt beim User |

## Typische Risiken

- **Prüfweg zuerst:** Server starten, anmelden, eine Seite laden, einen Screenshot öffnen. Ein Browser, der nicht startet, eine Datenbank, die nicht läuft, oder eine Anmeldung, die scheitert, fällt sonst erst in Runde 1 auf.
- **Ein Ausschnitt zuerst:** eine Ansicht in einem Zustand (oder bei Schaustücken der Hauptblick) auf Zielqualität, dann der Rest.
- **Messen, bevor gestaltet wird:** Hängt der Star an einer Zeit (Suche, Ladezeit), baut der Lauf zuerst den großen Datensatz und die Messung. Eine langsame Abfrage unter einer fertigen Oberfläche ist teurer zu beheben.
- **Lange Rechenschritte** (Bilder erzeugen, Daten importieren, gebackenes Licht): erst klein testen und nach jedem Lauf die erzeugten Dateien prüfen, weil ein abgebrochener Schritt unvollständige Dateien hinterlässt.
- **Datenbank:** nur die lokale Entwicklungsdatenbank. Der Prompt nennt, woran der Lauf sie erkennt (Host, Port, Name), und der Lauf prüft das vor dem ersten schreibenden Befehl.
- **Hängender Server:** Ein alter Prozess auf demselben Port liefert alte Stände aus, und ein Produktions-Build zeigt Änderungen erst nach einem neuen Build. Der Lauf prüft vor jeder Runde, dass der Server den aktuellen Stand zeigt.

## Zusatzfragen im Interview

- Bei Baustein 1: Auf welchem Gerät und in welcher Auflösung sieht das Publikum das Ergebnis?
- Bei Baustein 2: Welche bestehenden Seiten oder Komponenten setzen den Maßstab, in den sich das Neue einfügen muss?
- Bei Baustein 4: Welche Zustände gibt es in den echten Daten, die im Entwurf gern fehlen (der Kunde mit dem sehr langen Namen, das Konto ohne Einträge, die Liste mit 5.000 Zeilen, zwei Kunden mit demselben Namen)?
- Bei Baustein 8: Gibt es ein Testkonto und einen wiederholbaren Datensatz, oder legt der Lauf beides an?
- Bei den Grenzen: Darf der Lauf Pakete, Testkonfiguration und den Browser für die Prüfung hinzufügen?
