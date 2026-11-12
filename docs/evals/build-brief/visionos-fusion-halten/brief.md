# Fusion halten: der Puls am Ziel

Nächste Woche setzen drei Personen die Vision Pro auf und machen je eine Sitzung von 5 Minuten im Vergenztraining: ich selbst und zwei Testpersonen, eine davon Orthoptistin. Sie entscheidet danach, ob sie die App ihren Patienten zum Ausprobieren gibt. Beim letzten Test hat sie Stufe 2 nach einer Minute abgebrochen, weil sie nicht verstanden hat, was sie tun soll. Qualität ist das Ziel. Nimm dir die Zeit, die sie braucht.

## Der Auftrag

Die Anfrage: Stufe 2 des Vergenztrainings, „Fusion halten", soll man ohne Erklärung verstehen: wann man pinchen soll, ob der Pinch gezählt hat, und wie die Sitzung läuft.

Die Referenz: die heutige Stufe 2, `VergenceStage2View` in `EyeTrainingApp/EyeTrainingApp/Views/Exercises/VergenceTrainingView.swift`, zusammen mit der Textkarte in `EyeTrainingApp/EyeTrainingApp/Views/Exercises/ExerciseOverlay.swift`. So funktioniert sie: Eine cyanfarbene Kugel (Radius 2 cm), das Ziel, hängt am Kopf-Anker. Sie nähert sich von 40 cm bis zur Haltedistanz (`exerciseManager.vergenceParams.holdDistanceCm`, heute 15, 12 oder 10 cm für Level 4, 5 oder 6) und bleibt dort stehen. Alle 2 Sekunden kommt ein Puls: Ein weißes Fadenkreuz-Symbol vor der Kugel wächst für 0,35 Sekunden auf das 1,5-Fache. Wer das Ziel in diesem Moment einfach und nicht doppelt sieht, pincht. Ein Pinch innerhalb von 1,5 Sekunden zählt. Nach `holdDurationSeconds / 2` bestätigten Pulsen (mindestens einem) ist der Haltedurchgang geschafft. Ein verpasster Puls beendet ihn als Fehlschlag. In beiden Fällen meldet die View das Ergebnis mit `recordVergenceHold(success:)`, das Ziel springt auf 40 cm zurück und nähert sich neu.

Zwei Begriffe für diesen Auftrag: Ein Haltedurchgang reicht von der Ankunft des Ziels auf der Haltedistanz bis zu seinem Ergebnis (geschafft oder Fehlschlag). Ein Puls ist die einzelne Aufforderung zum Pinch innerhalb eines Haltedurchgangs.

Ihre Schwächen, aus dem Test am Gerät und aus dem Code:

- Man erkennt nicht, wann der Puls kommt. Er ist plötzlich da und nach 0,35 Sekunden vorbei.
- Ob der Pinch gezählt hat oder zu spät war, sieht gleich aus. Ein bestätigter Puls und ein geschaffter Haltedurchgang zeigen dasselbe grüne Häkchen. Ein Pinch außerhalb des Fensters wird stumm verworfen.
- Ein Fehlschlag zeigt für 0,5 Sekunden ein rotes Kreuz, ohne Grund.
- Nach jedem Haltedurchgang wird der Abstand hart auf 40 cm gesetzt (`distance = 0.40`). Das Ziel springt, und das fühlt sich wie ein Fehler an.
- Man weiß nie, wie lange es noch dauert. Uhr, Zähler und Anweisung stehen auf einer Karte, die 1 m entfernt und 25 cm über Augenhöhe hängt. Das Ziel steht 10 bis 15 cm vor den Augen. Wer die Karte liest, gibt die Fusion auf, die er halten soll.
- Der Anweisungstext gilt für alle drei Stufen und beschreibt Stufe 1 („Pinchen Sie, wenn es doppelt erscheint oder wenn Sie es wieder klar sehen"). In Stufe 2 bedeutet der Pinch das Gegenteil.
- Der Puls-Zeitgeber läuft ab dem Erscheinen der Ansicht frei. Der erste Puls kommt 0 bis 2 Sekunden nach der Ankunft des Ziels, also zufällig.
- Die Zeitlogik steckt in der View (`Timer`, `DispatchQueue.main.asyncAfter`) und ist nicht getestet.

Schließe genau diese Lücken:

- Puls ohne Ankündigung → Ein Ring zieht sich auf das Ziel zusammen. Der Moment, in dem er schließt, ist der Moment für den Pinch.
- Gezählt und nicht gezählt sehen gleich aus → Treffer, Verpasst und „Halten geschafft" bekommen drei Antworten am Ziel, die man im Standbild auseinanderhält.
- Rotes Kreuz → eine ruhige Antwort ohne Rot, ohne Wackeln.
- Springendes Ziel → Jede Abstandsänderung gleitet.
- Karte mit Text und Zahlen in anderer Tiefe → Während Stufe 2 steht kein Text im Raum. Alles, was man zum Halten wissen muss, ist am Ziel ablesbar. Für die Sitzungszeit gibt es eine schmale Anzeige ohne Zahlen.
- Anweisung, die Stufe 1 beschreibt → Stufe 2 bekommt auf dem vorhandenen Vorbereitungsbildschirm ihren eigenen Satz. Die ersten Pulse der Sitzung erklären den Rest.
- Zufälliger erster Puls → ein fester Einstieg nach der ersten Ankunft des Ziels.
- Ungetestete Zeitlogik → eine reine, getestete Funktion, die die View nur noch darstellt.

Der Star: der Puls am Ziel, also der Ring, der sich schließt, und die Antwort des Ziels darauf. Alles andere ordnet sich ihm unter: Neben dem Puls bewegt sich nichts. Die Fortschrittsanzeige ist schmal und still. Stufe 1 und Stufe 3 bleiben, wie sie sind. Das Debug-Menü ist schlicht.

**Der Puls.** Ein Ring zieht sich in etwa 0,6 Sekunden auf das Ziel zusammen. Im Moment des Schließens ist der Pinch dran. Der Rhythmus bleibt bei etwa 2 Sekunden von Schließen zu Schließen. Ein Kreis, der sich im Uhrzeigersinn füllt, ist keine Ankündigung: Er sieht aus wie ein Ladekreis und sagt „warten" statt „gleich sind Sie dran". Der Ring wird deshalb als Ganzes kleiner. Das Fehlfenster bleibt, wie es ist: Bleibt der Pinch bis 1,5 Sekunden nach dem Schließen aus, ist der Puls verpasst. Neu ist eine Toleranz nach vorn: Ein Pinch bis 0,2 Sekunden vor dem Schließen zählt als Treffer, weil Menschen einem Rhythmus leicht vorauseilen und sich sonst für richtiges Verhalten übergangen fühlen. Mehrere Pinches in einem Fenster zählen einmal. Ein Pinch außerhalb jedes Fensters (während der Annäherung, zwischen zwei Pulsen) bekommt keine Antwort und wird nicht gewertet.

Eine schwere Stelle dabei: Bei 2 Sekunden Rhythmus und 0,6 Sekunden Ring müsste der nächste Ring 1,4 Sekunden nach dem Schließen beginnen, das Fehlfenster endet aber erst nach 1,5 Sekunden. Zwei Ringe zugleich sind keine Ankündigung. Die Lösung ist deine, solange das Fensterende bei 1,5 Sekunden bleibt und zu jedem Zeitpunkt höchstens ein Ring zu sehen ist. Der Rhythmus darf sich dafür um diese Zehntelsekunde dehnen.

**Treffer, Verpasst, Geschafft.** Treffer (Pinch im Fenster): Das Ziel wird für etwa 0,3 Sekunden heller, und zwar so viel, dass man es im Standbild neben dem Ruhezustand sofort erkennt, ohne dass es blendet. Dazu kommt ein leiser Ton, der nicht länger dauert als das Aufhellen. Verpasst: Der Ring löst sich nach außen auf, ohne Ton. Ist der verpasste Puls ein gewerteter, endet der Haltedurchgang wie heute als Fehlschlag, und das Ziel gleitet danach zurück. Erst löst sich der Ring auf, dann gleitet das Ziel, damit sich nur eine Sache bewegt. Geschafft (der letzte nötige Treffer eines Haltedurchgangs): eine eigene, dritte Antwort, die man im Standbild vom einzelnen Treffer unterscheidet und für die dieselben Verbote gelten. Danach gleitet das Ziel zurück. Eine andere Farbe ist kein Unterschied zwischen Treffer und Verpasst: Die beiden unterscheiden sich in Form und Richtung (das Ziel antwortet selbst, oder der Ring geht nach außen weg), sodass man sie auch in einem Graustufenbild auseinanderhält. Niemand soll sich bestraft fühlen, denn Stress schadet der Fusion, um die es in der Übung geht.

Der Fortschritt innerhalb eines Haltedurchgangs ist am Ziel selbst ablesbar, ohne Zahl und ohne eigenes Element daneben: wie viele Treffer schon da sind und wie viele noch fehlen. Die Zahl der nötigen Treffer liegt je nach Level und Feinanpassung zwischen 2 und 9 und kann sich nach einem geschafften Haltedurchgang ändern, weil die Feinanpassung in der Sitzung (`microStep`, siehe `CLAUDE.md`) in Stufe 2 die Haltezeit verlängert. Deine Darstellung muss beide Enden tragen.

**Der Einstieg.** Die ersten drei Pulse einer Sitzung sind langsamer (alle 3 Sekunden) und zählen nicht. Sie kommen einmal je Sitzung, nach der ersten Ankunft des Ziels auf der Haltedistanz. Ein Pinch bekommt die Treffer-Antwort, ein fehlender Pinch die Ring-Auflösung, aber das Ziel bleibt stehen, nichts wird gewertet und `recordVergenceHold` wird nicht aufgerufen. Die Sitzungszeit läuft dabei weiter. Danach geht es ohne Bruch in den gewerteten Rhythmus über. Ein Textbildschirm ist kein Einstieg: Vor der Übung kommt nichts Neues dazu.

**Bewegung des Ziels.** Jede Änderung des Abstands gleitet. Das Zurückweichen von der Haltedistanz auf 40 cm dauert etwa 0,8 Sekunden und beginnt und endet weich. Ein Sprung ist keine Abstandsänderung. Die Annäherung von 40 cm zur Haltedistanz behält ihre heutige Geschwindigkeit (0,16 m/s) und läuft weich aus, statt hart anzuhalten. Zur Einordnung: In Stufe 2 ändert sich die Haltedistanz innerhalb einer Sitzung nicht. Sie wechselt nur mit dem Level. Der Sprung, den man heute sieht, ist das Zurücksetzen nach jedem Haltedurchgang.

**Fortschritt der Sitzung.** Eine schmale Anzeige am unteren Rand des Sichtfelds zeigt, wie viel der Sitzungszeit vorbei ist, ohne Zahlen. Schmal heißt: eine Linie und keine Fläche, im Bild deutlich flacher als das Ziel. Eine Uhr mit Ziffern ist für diese Übung keine Fortschrittsanzeige, weil man dann auf die Uhr schaut statt aufs Ziel. Die Anzeige darf den Blick nicht vom Ziel ziehen. Eine Annahme, die du übernimmst: Sie liegt in derselben Tiefe wie das Ziel und nicht näher am Auge. Wer auf 10 bis 15 cm konvergiert, sieht alles in anderer Tiefe doppelt.

**Text.** Während Stufe 2 läuft, wird die Karte `ExerciseOverlay` nicht gezeigt. Stufe 1 und Stufe 3 behalten sie unverändert. Der Knopf „Beenden" aus `ExerciseView.swift` bleibt, weil man jederzeit abbrechen können muss. Der vorhandene Vorbereitungsbildschirm (`ExerciseCalibrationView`) zeigt für Stufe 2 einen eigenen Satz statt des gemeinsamen Textes, zum Beispiel: „Halten Sie das Ziel einfach. Pinchen Sie jedes Mal, wenn sich der Ring um das Ziel schließt." Die Texte für Stufe 1 und Stufe 3 bleiben. Alle Texte sind deutsch und in der „Sie"-Anrede der App.

**Randfälle.** Läuft die Sitzungszeit mitten in einem Haltedurchgang ab, endet die Sitzung wie heute, und der offene Durchgang wird nicht gewertet. Ein neuer Durchgang macht offene Zeitprüfungen des alten ungültig (heute über `currentPulseId`). Die Trefferfläche für den Pinch bleibt mindestens so groß wie heute (Kugel mit 2 cm Radius). Ring und Anzeige fangen den Pinch nicht ab.

**Was fachlich feststeht.** Abstände, Haltezeiten und die Zahl der nötigen Treffer kommen wie heute aus `VergenceProgressionEngine` über `exerciseManager.vergenceParams`. Das Fehlfenster endet 1,5 Sekunden nach dem Schließen. Die Bewertung bleibt: genau ein Aufruf von `recordVergenceHold(success:)` je gewertetem Haltedurchgang. Das Ziel steht auf Augenhöhe am Kopf-Anker. Du stellst es nicht näher, als der Code es heute ausrechnet.

Deine Freiheit: Form und Farbe des Rings sind dein Entwurf, zum Beispiel ein dünner heller Ring, der von etwa doppeltem Zieldurchmesser auf den Zielrand schrumpft. Das Aussehen der Fortschrittsanzeige, die Antwort „Geschafft" und die Darstellung des Fortschritts im Haltedurchgang sind ebenfalls dein Entwurf. Technik: deine, RealityKit-Animation oder ein eigenes System. Den Ton erzeugst du im Code oder aus einer Datei, die du selbst herstellst und in einen der erlaubten Ordner legst. Ob das heutige Fadenkreuz bleibt, entscheidest du. Der Satz auf dem Vorbereitungsbildschirm ist ein Beispiel, wähl einen besseren, wenn du einen findest. Die Zeiten mit „etwa" (0,6, 2, 3, 0,3 und 0,8 Sekunden) sind Richtwerte, die du um wenige Zehntel verschieben darfst, wenn die Belege es nahelegen. Die 1,5 Sekunden sind fest.

Was exzellent sein muss:

- Der Moment, in dem der Ring schließt. Man sieht ihn kommen: In einer Bildfolge mit 10 Bildern je Sekunde ist der Ring von Bild zu Bild erkennbar kleiner, und das Bild des Schließens ist eindeutig.
- Der Unterschied zwischen Treffer und Verpasst. Je ein Standbild genügt, um sie zu unterscheiden, auch ohne Farbe. Keines der beiden enthält Rot, Blinken oder eine schnelle Bewegung.
- Das Gleiten bei der Abstandsänderung. In keinem Bild der Folge steht das Ziel plötzlich woanders, Anfang und Ende sind weich.
- Die ersten drei Pulse. Sie sind sichtbar langsamer, nichts wird gewertet, und der Übergang in den gewerteten Rhythmus hat keinen Bruch.
- Die Ruhe. Im Bild bewegt sich immer nur eine Sache, und nichts blinkt. Die Fortschrittsanzeige braucht die ganze Sitzung für ihre Länge und fällt deshalb in einer Bildfolge über wenige Sekunden nicht als Bewegung auf.

Nicht gewollt:

- Rote Fehlerfarbe (Stress, schadet der Fusion).
- Wackeln oder Zittern als Rückmeldung (Stress, fühlt sich wie Vibration an).
- Text im Raum während der Übung (der Blick verlässt das Ziel).
- Partikel oder Konfetti (lenken ab).
- Ein Countdown mit Zahlen (man schaut auf die Uhr statt aufs Ziel).
- Ein Ring, der sich wie ein Ladekreis füllt (sagt „warten", nicht „jetzt").

Messlatte: Eine Bildfolge über einen Puls zeigt ohne Erklärung, wann der Pinch dran ist. Und am Gerät macht jemand, der die App nie gesehen hat, die ersten fünf Pulse richtig, ohne zu fragen. Den ersten Teil belegst du selbst. Den zweiten kann nur ich am Gerät prüfen. Er steht deshalb als erster Punkt in der Liste „Am Gerät zu prüfen".

## Projekt, Werkzeuge und Dateien

- Du arbeitest im aktuellen Ordner, der Wurzel des Repositorys. Stack, Konventionen und Befehle stehen in der `CLAUDE.md`. Sie gilt, soweit dieser Auftrag nichts anderes sagt.
- Abweichungen von der `CLAUDE.md`, geprüft am 12.11.2026 mit Xcode 27.2:
  - Die `CLAUDE.md` nennt für Tests `OS=26.5`. Installiert ist nur visionOS 27.2. Nimm das vorhandene Gerät „Apple Vision Pro" über seine Kennung: `id=9A0BB462-5518-4871-92F9-18230DCB9160`. Findest du sie nicht, lies `xcrun simctl list devices available` und nimm das Gerät „Apple Vision Pro" unter visionOS.
  - Die Befehle der `CLAUDE.md` haben kein `-project`. Von der Wurzel aus brauchst du `-project EyeTrainingApp/EyeTrainingApp.xcodeproj`.
  - Die `CLAUDE.md` zählt vier Testsuiten auf. Im Ordner `EyeTrainingApp/EyeTrainingAppTests/` liegen acht. Alle müssen grün bleiben.
- Neue Swift-Dateien in den erlaubten Ordnern übernimmt das Projekt von selbst (synchronisierte Ordnergruppen). Die Datei `project.pbxproj` brauchst du nicht zu ändern.
- Testsuiten, die `ExerciseStorage.shared` berühren, sind wie die vorhandenen mit `@Suite(.serialized)` und `@MainActor` markiert, weil sie sonst über die gemeinsamen `UserDefaults` gegeneinander laufen.
- Branch: `feat/fusion-halten-puls`, neu vom aktuellen Stand von `main`. Du committest nach der ersten Version und nach jeder Runde, damit jeder Stand zurückholbar ist.
- So siehst du dein Ergebnis. Alles läuft über die Kommandozeile, von der Wurzel des Repositorys aus:

  ```bash
  UDID=9A0BB462-5518-4871-92F9-18230DCB9160
  B=tmp/brief-fusion-halten

  # Für den Simulator bauen (eigener Ordner, damit der Pfad zur App feststeht)
  xcodebuild build -project EyeTrainingApp/EyeTrainingApp.xcodeproj -scheme EyeTrainingApp \
    -configuration Debug -destination 'generic/platform=visionOS Simulator' -derivedDataPath $B/build
  # Ergebnis: $B/build/Build/Products/Debug-xrsimulator/EyeTrainingApp.app (prüf den Namen nach dem ersten Build)

  # Simulator starten, falls nötig, und warten, bis er bereit ist (vor jedem Start der App)
  xcrun simctl bootstatus $UDID -b

  # Installieren und einen Zustand starten (ein Start je Zustand)
  xcrun simctl install $UDID $B/build/Build/Products/Debug-xrsimulator/EyeTrainingApp.app
  xcrun simctl launch --terminate-running-process $UDID STEMAGO.EyeTrainingApp \
    -hasAcceptedDisclaimer YES -vergenceLevel 4 -briefState stufe2-halten -briefAuto treffer

  # Standbild
  xcrun simctl io $UDID screenshot $B/runde-1/halten.png

  # Bewegung: aufnehmen, mit SIGINT beenden, Einzelbilder ziehen
  xcrun simctl io $UDID recordVideo --codec=h264 --force $B/runde-1/puls.mov
  ffmpeg -i $B/runde-1/puls.mov -vf "fps=10,scale=1280:-1" $B/runde-1/puls/bild-%03d.png

  # Logzeilen der App
  xcrun simctl spawn $UDID log show --last 1m --style compact \
    --predicate 'subsystem == "STEMAGO.EyeTrainingApp" AND category == "Stufe2"'

  # Tests
  xcodebuild test -project EyeTrainingApp/EyeTrainingApp.xcodeproj -scheme EyeTrainingApp \
    -destination "platform=visionOS Simulator,id=$UDID"
  ```

  Was du dazu wissen musst: Der Screenshot ist ein einzelnes flaches Bild aus einem festen Blickpunkt, 3840×2160 Pixel. Schneide auf den Inhalt zu (`sips -c <höhe> <breite> bild.png --out ausschnitt.png`) und verkleinere große Bilder vor dem Ansehen (`sips -Z 1600 …`). Den Blickpunkt kannst du von der Kommandozeile nicht bewegen, und Tippen oder Pinch gibt es dort nicht. Direkt nach dem Start zeigt der Screenshot nur das Startbild. Warte auf die Logzeile, die den Zustand meldet (siehe „Prüfbarkeit"). Nach `xcodebuild test` ist der Simulator heruntergefahren, `bootstatus -b` startet ihn wieder. Ein sauberer Build dauert etwa 45 Sekunden, ein Testlauf etwa 2 Minuten.
- Belege (Screenshots, Bildfolgen, Ausgaben) und Build-Produkte legst du unter `tmp/brief-fusion-halten/` ab, je Runde ein Unterordner. Der Ordner wird nicht committet. Die `.gitignore` kennt `tmp/` noch nicht: Ergänze dort die eine Zeile `tmp/`. Die Belege der letzten Runde bleiben liegen.
- Führe eine Laufnotiz in `docs/briefs/2026-11-12-vergenztraining-stufe-2-fusion-halten.lauf.md`: Startzeit, und je Runde die Belege, die drei schwächsten Dinge, was du geändert hast, die Messwerte. Bei einem langen Lauf wird dein Kontext zwischendurch verdichtet. Die Notiz und die Commits halten den Stand, auf dem du danach weitermachst. Die Notiz wird committet.
- Der Auftrag ist eng. Außerhalb von Stufe 2 änderst du so wenig wie möglich. Stufe 1, Stufe 3, die anderen Übungen, das Menü und der Sehtest (in der `CLAUDE.md` „Vision Assessment") verhalten sich nach dem Lauf wie vorher. `VergenceTrainingView.swift` und `ExerciseOverlay.swift` teilen sich die Stufen: Ändere dort nur, was Stufe 2 braucht.

## Prüfbarkeit

Du kannst nur verbessern, was du gezielt ansehen kannst. Die folgenden Schalter gehören deshalb zum Auftrag. Bau sie mit der ersten Version. Es sind Startargumente der Form `-schluessel wert`. Sie landen in den `UserDefaults` der App und gelten nur für diesen Start.

- `-hasAcceptedDisclaimer YES` (gibt es schon, als `@AppStorage`): überspringt den medizinischen Hinweis für diesen Start. Am Hinweis selbst änderst du nichts.
- `-vergenceLevel 4|5|6` (gibt es schon, als Schlüssel von `ExerciseStorage`): wählt Haltedistanz (15, 12, 10 cm) und Haltezeit (5, 10, 15 Sekunden). Fehlt das Argument oder liegt das gespeicherte Level außerhalb von 4 bis 6, nimmt ein `-briefState`-Start Level 4.
- `-briefState <name>`: öffnet einen Zustand direkt, ohne Menü, Hinweis, Vorbereitungsbildschirm und Countdown. Er muss diese Zustände erreichen:
  - `stufe2`: Sitzung in Stufe 2 von Anfang an (Annäherung, dann Einstieg).
  - `stufe2-einstieg`: Das Ziel steht auf der Haltedistanz, der erste der drei Einstiegspulse beginnt.
  - `stufe2-halten`: Das Ziel steht auf der Haltedistanz, der Einstieg ist vorbei, der erste gewertete Puls beginnt.
  - `stufe2-letzter`: ein Haltedurchgang, in dem nur noch ein Treffer fehlt. Zeigt zusammen mit `-briefAuto treffer` die Antwort „Geschafft" und das Zurückgleiten danach.
  - `stufe2-ruecklauf`: Das Zurückgleiten von der Haltedistanz auf 40 cm beginnt sofort, danach die neue Annäherung.
- `-briefAuto treffer|verpasst|wechsel`: ersetzt den Pinch, weil du von der Kommandozeile nicht pinchen kannst. `treffer` pincht 0,3 Sekunden nach jedem Schließen, `verpasst` pincht nie, `wechsel` trifft zweimal und pincht dann nicht mehr.
- `-briefTime <sekunden>`: hält den Ablauf so viele Sekunden nach Beginn des gewählten Zustands an, für Standbilder (zum Beispiel Ring auf halbem Weg, Moment des Schließens, Mitte der Treffer-Antwort, Mitte des Gleitens).
- `-briefProgress <0 bis 1>`: gibt den Anteil der abgelaufenen Sitzungszeit vor, damit du die Fortschrittsanzeige am Anfang, in der Mitte und kurz vor dem Ende siehst.

Einen Immersive Space kann nur eine View öffnen (`openImmersiveSpace`). Werte `-briefState` deshalb an der Wurzel-View aus. `MainMenu.swift` liegt außerhalb der erlaubten Ordner: Häng die Auswertung in `EyeTrainingApp/EyeTrainingApp/App/` an `MainMenu()` an, zum Beispiel als Modifier mit einem `.task`. Der Direktstart ruft die Kopfhöhen-Erfassung über ARKit nicht auf, weil der Simulator dafür keine echten Werte liefert, und setzt 1,5 m.

Die App schreibt im Debug-Build Logzeilen über `Logger` mit dem Untersystem `STEMAGO.EyeTrainingApp` und der Kategorie `Stufe2` (das Projekt verwendet zwei Untersysteme, nimm dieses): eine Zeile, sobald ein per Schalter gewählter Zustand steht, und je Ereignis die Werte, die im Bild nicht stehen. Das sind der Abstand des Ziels zum Kopf in Metern, der Durchmesser des Rings am Anfang und beim Schließen in Metern und als Sehwinkel, die Strichstärke des Rings als Sehwinkel, die Zeitpunkte von Schließen, Fensterende und Pinch mit der Wertung, die Dauer des Gleitens, Tiefe und Größe der Fortschrittsanzeige, und ob der Ton ausgelöst wurde.

Die Schalter, die Logzeilen und das Debug-Menü sind nur im Debug-Build aktiv (`#if DEBUG`), damit sie nicht in den App Store gelangen. Damit ich dieselben Zustände am Gerät erreiche, baust du ein Debug-Menü, das sie auflistet und startet. Es ist im Debug-Build vom Hauptfenster aus erreichbar und hängt ebenfalls in `App/`. Sitzungen, die über einen Schalter oder das Debug-Menü starten, schreiben weder das Level noch einen Eintrag in den Verlauf, damit meine echten Trainingsdaten am Gerät sauber bleiben.

In dieser Umgebung lässt sich nicht beurteilen:

- Tiefenwirkung und Vergenz: ob Ring und Ziel in einer Tiefe verschmelzen und ob die Fortschrittsanzeige einfach oder doppelt erscheint → Du prüfst die Maße über das Log (Ring und Anzeige in der Tiefe des Ziels). Die Wirkung kommt in die Liste „Am Gerät zu prüfen".
- Pinch und Blick → `-briefAuto` ersetzt den Pinch, die Zeitlogik prüfst du in Unit-Tests. Die Bedienung kommt in die Liste.
- Das Zeitgefühl des Rhythmus. Zeiten aus dem Simulator sind kein Messwert, weil Simulator und Gerät sich darin unterscheiden → Die Zeitlogik bekommt die Zeit als Eingabe und wird in Unit-Tests mit festen Zeitpunkten geprüft. Das Gefühl kommt in die Liste.
- Komfort. Ich weiß vom Gerät, dass sich ein Ziel unter 30 cm für mich anstrengend anfühlt → Die Abstände bleiben, wie sie sind, und nichts Neues liegt näher am Auge als das Ziel. Kommt in die Liste.
- Der Ton. Du hörst nichts → Du prüfst im Log, dass er genau bei einem Treffer ausgelöst wird. Lautstärke und Klang kommen in die Liste.
- Sichtbarkeit des dünnen Rings durch die Optik der Brille → Annahme: Strichstärke mindestens 0,2 Grad Sehwinkel, im Log ausgegeben. Kommt in die Liste.
- Echtes Licht und echter Raum. Stell am ersten Screenshot fest, vor welchem Hintergrund die Übung läuft, und halte es in der Laufnotiz fest → Lesbarkeit prüfst du vor diesem Hintergrund. Der echte Raum kommt in die Liste.
- Handerkennung. Ich weiß vom Gerät, dass ein Pinch manchmal nicht erkannt wird, wenn die Hand im Schoß liegt. Ein nicht erkannter Pinch sieht für die App wie „Verpasst" aus → Du löst das nicht. Kommt in die Liste.

Im Simulator siehst du ein flaches Bild aus einem festen Blickpunkt. Tiefenwirkung, Blick- und Handsteuerung, Komfort und Leistung kannst du dort nicht beurteilen. Behaupte dazu nichts. Führe stattdessen die Liste „Am Gerät zu prüfen" und gib sie im Schlussbericht zurück. Jeder Eintrag hat drei Teile: der Zustand und wie ich ihn am Gerät erreiche (Eintrag im Debug-Menü), worauf ich achten soll, und woran ich erkenne, dass es stimmt. Ich habe die Brille ab Dienstag und eine Stunde für die Liste. Sie muss in dieser Stunde zu schaffen sein, das Wichtigste zuerst. Mindestens diese Punkte stehen darin:

1. Jemand, der die App nie gesehen hat, macht die ersten fünf Pulse richtig, ohne zu fragen.
2. Ring und Ziel erscheinen bei 15, 12 und 10 cm als ein Gegenstand in einer Tiefe, der Ring nicht doppelt.
3. Man sieht den Ring kommen, auch wenn man fest auf das Ziel schaut. Der dünne Ring ist durch die Optik gut sichtbar.
4. Treffer und Verpasst unterscheiden sich, ohne dass man den Blick vom Ziel nimmt. Keines erschreckt. Der Ton ist hörbar und leise.
5. Das Zurückgleiten wirkt ruhig und nicht wie ein Fehler.
6. Die Fortschrittsanzeige ist am Rand wahrnehmbar, erscheint nicht doppelt und zieht den Blick nicht weg.
7. Der Rhythmus stimmt am Gerät: 3 Sekunden im Einstieg, danach 2 Sekunden. Ein Pinch knapp vor dem Schließen zählt.
8. Pinch mit der Hand im Schoß: Wird er erkannt?
9. Komfort über 5 Minuten bei der Haltedistanz.

Schreib „geprüft" nur zu dem, was du in diesem Lauf an einem Beleg gesehen hast. Alles andere heißt „nicht geprüft".

## Harte Regeln

- Abstände, Haltezeiten, das Ende des Fehlfensters und die Bewertung bleiben, wie sie sind (fachlich abgestimmt und getestet). Die Einstiegspulse werden nicht gewertet und nicht gemeldet.
- Nichts Neues liegt näher am Auge als das Ziel, und das Ziel steht nicht näher als heute (Komfort lässt sich im Simulator nicht prüfen, deshalb gilt die vorsichtige Vorgabe).
- Keine Bewegung auf die Person zu ist schneller als die heutige Annäherung von 0,16 m/s (aus demselben Grund).
- Prüfschalter, Logzeilen und Debug-Menü sind nur im Debug-Build aktiv (sie gehören nicht in den App Store).
- Du brauchst für diesen Auftrag keine neue ARKit-Funktion. Falls doch, fragst du sie vor der Nutzung mit `isSupported` ab und baust einen Weg ohne sie (im Simulator fehlen die meisten, und am Gerät kann die Freigabe verweigert sein).
- Texte sind deutsch, in der „Sie"-Anrede, ohne Platzhalter (so spricht die App überall).
- Der medizinische Hinweis und die fachlichen Bezeichnungen der App („Vergenztraining", „Fusion halten", „Level") bleiben unverändert (sie sind fachlich abgestimmt).
- Tests prüfen die Lösung, sie legen sie nicht fest. Du schwächst keinen vorhandenen Test ab und baust keinen Sonderfall nur für einen Test (sonst sagt ein grüner Lauf nichts mehr). Widerspricht ein vorhandener Test diesem Auftrag, lässt du ihn stehen und nennst ihn im Schlussbericht.

## Risiken

- Zieh zuerst die Zeitlogik des Pulses aus der View in eine reine Funktion, die die Zeit als Eingabe bekommt, und halte das heutige Verhalten mit Tests fest: Puls-Rhythmus, Fensterende nach 1,5 Sekunden, Zahl der nötigen Treffer, genau eine Meldung je Haltedurchgang. Erst danach kommen Einstieg, Toleranz und Darstellung. Wer die Zeitsteuerung in der View anfasst, verschiebt leicht das Fehlfenster, und dann stimmt die Bewertung nicht mehr, ohne dass ein Bild es zeigt.
- Bring zuerst einen einzigen Zustand auf Zielqualität: `stufe2-halten` mit einem Ring, der sich schließt, und der Treffer-Antwort. Bau erst dann Einstieg, Gleiten und Fortschrittsanzeige. Sonst füllst du die ganze Stufe mit einem Ansatz, der die Messlatte nicht erreicht, und scheitert der Schalter-Mechanismus, scheitert er für alle Zustände zugleich. An diesem ersten Zustand zeigt sich auch erst, ob ein Inhalt am Kopf-Anker in 10 bis 15 cm im Screenshot des Simulators zu sehen ist, denn ohne Pinch erreichst du Stufe 2 heute nicht. Ist er nicht zu sehen, setzt du den Inhalt nur für den Beleg per Schalter an einen festen Punkt im Raum vor den Blickpunkt, nicht näher als die Haltedistanz, und nennst das im Bericht.
- Der Build ist langsam. Jede Runde kostet Build, Installation und einen Start je Zustand. Sammle Änderungen und bau dann, statt nach jeder Zeile zu bauen. Sonst reicht die Zeit nicht für vier Runden.
- Der Simulator verdeckt, was nur am Gerät auffällt (Tiefe, Zeitgefühl, Handerkennung). Was du nur im Simulator gesehen hast, nennst du im Bericht so. Sonst lese ich „funktioniert" und verlasse mich am Dienstag darauf.

## Prozess

1. **Prüfweg zuerst.** Halte die Startzeit in der Laufnotiz fest (`date`). Beweise dann am heutigen Stand, bevor du etwas änderst, dass du dein Ergebnis zu sehen bekommst: bauen, mit `-hasAcceptedDisclaimer YES` starten, einen Screenshot machen und öffnen, einmal `xcodebuild test` laufen lassen. Halte fest, welche Build-Warnungen es schon gibt. Ohne funktionierenden Prüfweg sind alle Runden blind.
2. **Eine vollständige erste Version.** Alles aus dem Auftrag ist da und läuft, auch die Schalter und das Debug-Menü. Prüfe sie über den Prüfweg und behebe jeden Fehler. Committe.
3. **Mindestens 4 Verbesserungsrunden.** In jeder Runde:
   - Sammle Belege: je eine Bildfolge über einen Puls mit Treffer und mit Verpasst (10 Bilder je Sekunde), Standbilder von Ring auf halbem Weg, Moment des Schließens, Treffer, Ring-Auflösung, „Geschafft", Mitte des Gleitens, einem Einstiegspuls und der Fortschrittsanzeige an drei Stellen, dazu die Logzeilen mit Maßen und Zeitpunkten, die Ausgabe von `xcodebuild test` und die Build-Ausgabe.
   - Sieh dir jeden Beleg wirklich an. Ein Screenshot, den du nicht geöffnet hast, und eine Ausgabe, die du nicht gelesen hast, sind keine Belege.
   - Urteile als strenger Gestalter für räumliche Oberflächen, der die Gestaltungsrichtlinien von Apple für visionOS kennt, jeden Beleg mit den besten Apps der Plattform vergleicht und an der Messlatte misst. Er achtet auf Ruhe im Bild und darauf, ob man ohne Erklärung weiß, wohin man schauen und was man tun soll. Bei jedem Urteil sagt er dazu, ob es am Beleg belegbar ist oder erst am Gerät.
   - Benenne die drei schwächsten Dinge.
   - Behebe sie.
   - Prüfe mit frischen Belegen, ob sie behoben sind. Trag die Runde in die Laufnotiz ein und committe.
4. **Messwert vor Neuem.** Schlägt ein Unit-Test fehl, oder meldet der Build eine Warnung in einer Datei der erlaubten Ordner, die es zu Beginn noch nicht gab: Behebe das, bevor du etwas hinzufügst. Die räumlichen Maße aus dem Log liegen innerhalb der Vorgaben dieses Auftrags.
5. **Schluss.** Du hörst auf, wenn eine weitere Runde der Orthoptistin in ihrer ersten Minute in Stufe 2 nicht mehr auffiele, frühestens nach den 4 Runden. Das Zeitlimit geht vor: 75 Minuten nach deinem Start schließt du die laufende Runde ab und schreibst den Bericht, auch wenn es weniger als 4 Runden waren. Prüf die Uhrzeit am Ende jeder Runde.
6. **Schlussbericht**, siehe unten.

## Durchhalten und Grenzen

Während des Laufs sitzt niemand daneben. Arbeite den ganzen Auftrag ab, ohne auf eine Antwort zu warten. Wenn du merkst, dass du eine Restliste schreiben oder anbieten willst weiterzumachen, mach stattdessen mit dem nächsten Teil weiter.

Gewöhnliche Hindernisse (ein Fehler, eine Zeitüberschreitung, ein Werkzeug, das nicht antwortet, ein leeres Ergebnis) untersuchst du zuerst. Sind sie keine echte Sperre, arbeitest du dich mit deinen Mitteln hindurch: warten und wiederholen, die Anfrage korrigieren, einen anderen Weg nehmen.

Ohne Rückfrage erlaubt:

- Dateien anlegen und ändern in `EyeTrainingApp/EyeTrainingApp/Views/Exercises/`, `EyeTrainingApp/EyeTrainingApp/Services/`, `EyeTrainingApp/EyeTrainingApp/App/` und `EyeTrainingApp/EyeTrainingAppTests/`.
- Die Laufnotiz unter `docs/briefs/`, alles unter `tmp/brief-fusion-halten/` und die eine Zeile `tmp/` in der `.gitignore`.
- Den Branch `feat/fusion-halten-puls` anlegen und darauf committen.
- Bauen und testen mit `xcodebuild`. Den vorhandenen Simulator „Apple Vision Pro" starten, die App dort installieren, starten und beenden, Screenshots und Aufnahmen machen, Logs lesen. Die Daten der App im Simulator darfst du verändern.
- `ffmpeg` und `sips` für die Belege.

Nicht anfassen:

- `VergenceProgressionEngine.swift` und `ScoreCalculator.swift`: nur lesen (die Regeln sind fachlich abgestimmt und getestet). Brauchst du dort etwas anderes, baust du es außen herum und nennst es im Bericht.
- Alles außerhalb der vier Ordner, ausgenommen Laufnotiz, Belege und die eine Zeile in der `.gitignore`. Dazu gehören `Views/MainMenu.swift`, `Views/ExerciseView.swift`, `Views/Assessment/`, `Models/`, `Packages/`, `Info.plist`, `project.pbxproj` und `docs/superpowers/` (der Auftrag ist eng, und ich will den Unterschied nachher überblicken können).
- Die `CLAUDE.md` des Projekts (ich pflege sie selbst). Sätze dort, die nach deinem Lauf nicht mehr stimmen, nennst du im Schlussbericht mit einem Vorschlag.
- Push, Pull Request und andere Branches (ich sehe mir das Ergebnis erst an).
- Neue Pakete oder Abhängigkeiten (für diesen Auftrag reicht, was Apple mitliefert).
- Die Maschine: nichts installieren, keine Simulator-Laufzeiten nachladen, keine Simulatoren anlegen, löschen, herunterfahren oder neu starten (das sind Eingriffe in meinen Rechner, und ein Schutz-Hook kann sie blocken). Fehlt etwas, meldest du es.

Stößt du an eine dieser Grenzen, umgehst du sie nicht. Du arbeitest an allem weiter, was nicht davon abhängt, und nennst die Stelle im Schlussbericht.

Entscheidungen, die dieser Auftrag nicht vorhergesehen hat, triffst du selbst, und zwar so, wie es der Messlatte am besten dient. Halte sie in der Laufnotiz fest.

## Schlussbericht

Ich habe den Lauf nicht gesehen und komme aus anderer Arbeit. Schreib den Bericht so, dass er ohne Vorwissen verständlich ist: das Wichtigste zuerst, ganze Sätze, einfache Wörter, keine Abkürzungen, die du während der Arbeit erfunden hast. Er ist kurz und enthält:

1. Wie ich das Ergebnis starte und was ich in den ersten Sekunden tue, im Simulator und am Gerät.
2. Den besten Moment und den Schalter, der ihn direkt zeigt.
3. Was du gebaut und verwendet hast, und wie die Zeitlogik jetzt aufgeteilt ist.
4. Die Messwerte der letzten Runde neben ihrer Schwelle: Tests, Build-Warnungen, die räumlichen Maße aus dem Log.
5. Bekannte Mängel, auch die, die du nicht beheben konntest.
6. Entscheidungen, die du für mich getroffen hast, Grenzen, an die du gestoßen bist, und die Sätze der `CLAUDE.md`, die nicht mehr stimmen.
7. Die Liste „Am Gerät zu prüfen": jeder Punkt als Prüfschritt mit dem Eintrag im Debug-Menü, der ihn vorbereitet, dem, worauf ich achten soll, und dem, woran ich erkenne, dass es stimmt.
