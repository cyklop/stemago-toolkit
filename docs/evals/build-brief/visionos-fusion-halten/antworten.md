# Antwortblatt: Funktion der Vision-Pro-App (EyeTrainingApp)

Der User hat den Skill aufgerufen mit: „Stufe 2 des Vergenztrainings (Fusion halten) verständlich machen".

So liest du das Blatt: Zu jedem Thema steht die **Erstantwort** des Users. Ist sie vage, steht darunter die **Antwort auf Nachfrage**; sie gilt erst, wenn du nachgehakt hast. Zu allem, was hier nicht steht, sagt der User: „Dein Vorschlag passt."

## Einsatz und Publikum
Erstantwort: „Für die Leute, die die App testen."
Auf Nachfrage: „Ich selbst und zwei Testpersonen, eine davon Orthoptistin. Sie setzen die Brille nächste Woche auf und machen je eine Sitzung von 5 Minuten. Die Orthoptistin entscheidet danach, ob sie die App ihren Patienten zum Ausprobieren gibt. Beim letzten Test hat sie Stufe 2 nach einer Minute abgebrochen, weil sie nicht verstanden hat, was sie tun soll."

## Anfrage
„Stufe 2 des Vergenztrainings, ‚Fusion halten', soll man ohne Erklärung verstehen: wann man pinchen soll, ob es gezählt hat, und wie die Sitzung läuft."

## Referenz
Erstantwort: „Die Stufe gibt es ja schon, sie funktioniert nur nicht gut."
Auf Nachfrage (zu deinen Vorschlägen aus dem Code): „Ja. Dazu aus dem Test am Gerät: Man erkennt nicht, wann der Puls kommt, er ist einfach plötzlich da. Ob der Pinch gezählt hat oder zu spät war, sieht gleich aus. Wenn die App den Abstand nachstellt, springt das Ziel, und das fühlt sich wie ein Fehler an. Und man weiß nie, wie lange es noch dauert."

## Star
Erstantwort: „Das Feedback und der Fortschritt und die Erklärung am Anfang."
Auf Nachfrage (welches eine?): „Der Puls am Ziel. Wenn der stimmt, braucht man die Erklärung kaum."

## Konkretion
- Der Puls kündigt sich an: Ein Ring zieht sich in etwa 0,6 Sekunden auf das Ziel zusammen, im Moment des Schließens ist der Pinch dran. Rhythmus etwa alle 2 Sekunden, wie heute.
- Treffer (Pinch im Fenster, einfaches Bild gehalten): Das Ziel antwortet kurz und ruhig. Verpasst (kein Pinch innerhalb von 1,5 Sekunden): eine andere, ebenso ruhige Antwort. Erstantwort dazu: „Es soll sich gut anfühlen." Auf Nachfrage: „Treffer: Das Ziel wird für 0,3 Sekunden etwas heller und ein leiser Ton. Verpasst: Der Ring löst sich nach außen auf, kein Ton, keine rote Farbe, kein Wackeln. Niemand soll sich bestraft fühlen."
- Wenn sich der Abstand ändert (Mikro-Anpassung nach Erfolg oder nach zwei Fehlern), gleitet das Ziel in etwa 0,8 Sekunden dorthin und springt nicht.
- Fortschritt: eine schmale Anzeige am unteren Rand des Sichtfelds, die die Sitzungszeit zeigt, ohne Zahlen. Sie darf nicht vom Ziel ablenken.
- Einstieg: die ersten drei Pulse sind langsamer (alle 3 Sekunden) und zählen nicht. Kein Textbildschirm davor.
- Fachliche Vorgaben, die bleiben: Abstände und Parameter kommen aus `VergenceProgressionEngine`, das Fehlfenster von 1,5 Sekunden bleibt, die Bewertung bleibt. Das Ziel steht auf Augenhöhe, in Stufe 2 nah am gemessenen Break-Punkt. Die Abstände, die der Code heute dafür ausrechnet, bleiben, der Lauf stellt das Ziel nicht näher.
- Schwere Stellen laut User: „Dass der Ring nicht wie ein Ladekreis aussieht. Und dass Treffer und Verpasst sich klar unterscheiden, ohne dass eines davon aufregt."
- Texte: deutsch, „Sie"-Anrede wie in der App.

## Freiheit
„Form und Farbe des Rings sind dein Entwurf, zum Beispiel ein dünner heller Ring, der von etwa doppeltem Zieldurchmesser auf den Zielrand schrumpft. Wie die Fortschrittsanzeige aussieht, auch. Technik: deine, RealityKit-Animation oder eigenes System."

## Exzellent / Nicht gewollt
Erstantwort: „Es soll ruhig und hochwertig wirken."
Auf Nachfrage: „Ruhig heißt: Im Bild bewegt sich immer nur eine Sache, und nichts blinkt. Exzellent sein müssen: der Moment, in dem der Ring schließt (man muss ihn kommen sehen), der Unterschied zwischen Treffer und Verpasst, das Gleiten bei der Abstandsänderung, die ersten drei Pulse. Nicht haben will ich: rote Fehlerfarbe, Text im Raum während der Übung, Partikel oder Konfetti, einen Countdown mit Zahlen, Vibrationsgefühl durch Wackeln."
Gründe auf Nachfrage: Rot und Wackeln = Stress, schadet der Fusion; Text im Raum = der Blick verlässt das Ziel; Partikel = lenken ab; Zahlen = man schaut auf die Uhr statt aufs Ziel.

## Messlatte
Erstantwort: „Die Orthoptistin soll es verstehen."
Auf Nachfrage: „Eine Bildfolge über einen Puls zeigt ohne Erklärung, wann der Pinch dran ist. Und am Gerät macht jemand, der die App nie gesehen hat, die ersten fünf Pulse richtig, ohne zu fragen." (Der zweite Teil geht nur am Gerät, das weiß der User.)

## Prüfbarkeit
„Mach einen Vorschlag." Dem User wichtig: Stufe 2 direkt starten können, ohne Menü, Disclaimer, Kalibrierung und Countdown. Treffer und Verpasst gezielt auslösen können. Die Abstandsänderung gezielt auslösen können. Den Einstieg (erste drei Pulse) einzeln sehen.
Zu „nicht prüfbar": Der User hat die Brille ab Dienstag wieder und nimmt sich eine Stunde für die Prüfliste. Aus früheren Tests weiß er: Unter 30 cm fühlt sich das Ziel für ihn anstrengend an; Pinch wird manchmal nicht erkannt, wenn die Hand im Schoß liegt.

## Laufgröße
„Was kostet das?" → nach deiner Auskunft: Stufe mittel, mindestens 4 Runden, 75 Minuten, weil der Build langsam ist. Messwert: alle Unit-Tests grün und keine Build-Warnung im eigenen Code; rot wird zuerst behoben.

## Grenzen
- Schreiben nur in `EyeTrainingApp/EyeTrainingApp/Views/Exercises/`, `EyeTrainingApp/EyeTrainingApp/Services/`, `EyeTrainingApp/EyeTrainingApp/App/`, `EyeTrainingApp/EyeTrainingAppTests/`. `VergenceProgressionEngine` und `ScoreCalculator` nur lesen: Die Regeln sind fachlich abgestimmt und getestet.
- Der medizinische Hinweis (Disclaimer) und alle fachlichen Bezeichnungen bleiben unverändert.
- Branch: `feat/fusion-halten-puls`. Commits ja, nach jeder Runde. Kein Push.
- Keine neuen Pakete.
- Nichts installieren, keine Simulator-Laufzeiten nachladen, keine Simulatoren anlegen oder löschen. Vorhandenes Gerät „Apple Vision Pro" benutzen.
- Bestehender Code: außerhalb von Stufe 2 so wenig wie möglich ändern.
- Prüfschalter nur im Debug-Build; zusätzlich ein Debug-Menü, damit der User die Zustände am Gerät erreicht.

## Risiken
Erstantwort: „Sag du."
Ergänzung nach deinem Vorschlag: „Die Zeitsteuerung des Pulses läuft heute in der View. Wenn man das anfasst, verschiebt sich leicht das Fehlfenster, und dann stimmt die Bewertung nicht mehr. Also die Zeitlogik zuerst als testbare Funktion herausziehen und mit Tests festhalten, bevor die Darstellung drankommt."

## Sprache des Prompts
Deutsch.
