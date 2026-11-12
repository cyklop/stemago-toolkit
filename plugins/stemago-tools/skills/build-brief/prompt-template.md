# Build-Brief — Gerüst des Prompts

Das Gerüst gibt Reihenfolge und feste Bausteine vor. Text in `<…>` ersetzt du durch die Ergebnisse des Interviews. Wo „(Profil)" steht, setzt du die Textbausteine des Plattform-Profils ein und passt sie an das Vorhaben an. Die Zahlen in Klammern nennen den Baustein und stehen nicht im fertigen Prompt.

Die festen Absätze („Prozess", „Durchhalten und Grenzen", „Schlussbericht") übernimmst du sinngemäß. Kürze sie nicht auf Stichworte: Ihre Begründungen sind der Teil, der wirkt.

---

````markdown
# <Titel des Vorhabens>

<(1) Ein bis drei Sätze in der Ich-Form: wer das Ergebnis sieht oder benutzt, in welcher Lage, wie lange, und was davon abhängt.> Qualität ist das Ziel. Nimm dir die Zeit, die sie braucht.

## Der Auftrag

Die Anfrage: <(2) ein Satz>.

Die Referenz: <(2) was es schon gibt und wie es funktioniert, mit Pfad oder Adresse>. Schließe genau diese Lücken:

- <Schwäche> → <was stattdessen da sein muss>

Der Star: <(3) das eine Ding>. Alles andere ordnet sich ihm unter: <was das für den Rest heißt>.

<(4) Konkretion, in Absätzen nach Thema: die Inhalte im Klartext, die Zustände, die Randfälle. Jede schwere Stelle einzeln, mit ihrem Satz „X ist kein Y". Hier steht, wie es genau sein soll. Was die Lückenliste schon gesagt hat, wiederholst du nicht.>

<(5) Freiheit: „Der/die/das … ist dein Entwurf, zum Beispiel: …" · „Methode: deine. Bewährt hat sich …" · „… ist nur ein Beispiel, wähl Besseres." · „Annahme, die du mit Grund ändern darfst: …">

Was exzellent sein muss:

- <(6) Punkt, mit dem Merkmal, an dem man es an einem Beleg erkennt>
- <3 bis 6 Punkte>

Nicht gewollt:

- <(6) Standardlösung> (<Grund in Stichworten>)

Messlatte: <(7) ein prüfbarer Satz, am besten zweiteilig: ein Einzelergebnis, das einem Vergleich standhält, und ein Moment, den man zweimal zeigt>. <Falls ein Teil nur am Gerät oder im Betrieb prüfbar ist: „Den ersten Teil belegst du selbst. Den zweiten kann nur ich prüfen. Er steht als erster Punkt in der Liste …">

## Projekt, Werkzeuge und Dateien

- Du arbeitest in <Ordner oder „dem aktuellen Ordner">. <Bestehendes Projekt: „Stack, Konventionen und Befehle stehen in der `CLAUDE.md`. Sie gilt, soweit dieser Auftrag nichts anderes sagt." · Leerer Ordner: Einstiegsdatei, Stack oder „Stack: deine Wahl, begründe sie in einem Satz im Schlussbericht".>
- <Abweichungen von der `CLAUDE.md`, falls eine Angabe dort nicht zur lokalen Umgebung oder zum Code passt.>
- Branch: <Name>. Du committest nach der ersten Version und nach jeder Runde, damit jeder Stand zurückholbar ist.
- (Profil) <Womit du dein Ergebnis ansiehst: Werkzeug, Befehle, Auflösungen.>
- Belege (Screenshots, Ausgaben, Messprotokolle) legst du unter `<Belege-Ordner>` ab. Der Ordner wird nicht committet: <„Er steht in der `.gitignore`." oder „Trag ihn in die `.gitignore` ein.">. Die Belege der letzten Runde bleiben dort liegen.
- Führe eine Laufnotiz in `<Pfad>`: Startzeit, und je Runde die Belege, die drei schwächsten Dinge, was du geändert hast, die Messwerte. Bei einem langen Lauf wird dein Kontext zwischendurch verdichtet. Die Notiz und die Commits halten den Stand, auf dem du danach weitermachst. Die Notiz committest du mit.
- Dateien, die beim Start schon unversioniert im Arbeitsbaum liegen, gehören mir. Lass sie unverändert und nimm sie nicht in deine Commits auf.
- <Nur nach Absprache: „Du bist Eigentümer und langfristiger Maintainer dieser Codebasis, ihr Aufbau ist deine Sache." Sonst: „Der Auftrag ist eng." und welche Bereiche sich nach dem Lauf verhalten wie vorher.>

## Prüfbarkeit

Du kannst nur verbessern, was du gezielt ansehen kannst. Die folgenden Schalter gehören deshalb zum Auftrag. Bau sie mit der ersten Version:

- (Profil) `<Schalter>`: <was er einstellt, welche Zustände er erreichen muss>
- <Ein Schalter je wichtigem Zustand oder Moment aus dem Auftrag. Wirken zwei Schalter zusammen, steht da, wie.>

<Wo die Schalter aktiv sind: nur im Entwicklungs- oder Debug-Build, mit Grund. Ob ein Start über einen Schalter Daten speichert.>

In dieser Umgebung lässt sich nicht beurteilen:

- (Profil) <Punkt> → <Ausweichweg, den du baust> oder → kommt in die Liste „<Am Gerät zu prüfen / Von mir zu prüfen>" im Schlussbericht

Schreib „geprüft" nur zu dem, was du in diesem Lauf an einem Beleg gesehen hast. Alles andere heißt „nicht geprüft".

## Harte Regeln

- (Profil) <Regel> (<Grund>)
- <Regeln aus dem Interview. Für Bestand, der eine Regel heute verletzt: „nicht schlechter als heute", mit dem heutigen Wert.>

## Risiken

- <(10) Hinweis mit Grund und Handlung. Fast immer:> Bring zuerst <einen kleinen, benannten Ausschnitt> auf Zielqualität und bau erst dann den Rest. Sonst füllst du die ganze Fläche mit einem Ansatz, der die Messlatte nicht erreicht.
- (Profil) <weitere, zwei bis vier insgesamt>

## Prozess

1. **Prüfweg zuerst.** Halte die Startzeit in der Laufnotiz fest (`date`). Beweise dann am heutigen Stand oder am kleinsten möglichen Beispiel, dass du dein Ergebnis zu sehen bekommst: (Profil) <ein Screenshot, ein Testlauf, eine Messung>. Ohne funktionierenden Prüfweg sind alle Runden blind.
2. **Eine vollständige erste Version.** Alles aus dem Auftrag ist da und läuft, auch die Schalter. Prüfe sie über den Prüfweg und behebe jeden Fehler. Committe.
3. **Mindestens <N> Verbesserungsrunden.** In jeder Runde:
   - Sammle Belege: (Profil) <welche, über verschiedene Zustände und Momente. Bei knapper Zeit: in jeder Runde die Zustände, an denen der Star hängt, die volle Abdeckung nach der ersten Version und in der letzten Runde>.
   - Sieh dir jeden Beleg wirklich an. Ein Screenshot, den du nicht geöffnet hast, und eine Ausgabe, die du nicht gelesen hast, sind keine Belege.
   - Urteile als (Profil) <Rolle des Kritikers>, der das Ergebnis mit dem Besten seiner Art vergleicht und an der Messlatte misst.
   - Benenne die drei schwächsten Dinge.
   - Behebe sie.
   - Prüfe mit frischen Belegen, ob sie behoben sind. Trag die Runde in die Laufnotiz ein und committe.
4. **Messwert vor Neuem.** <Messwert> soll <mindestens / höchstens> <Schwelle> sein, gemessen <Messbedingung>. Verfehlt er die Schwelle, behebst du das, bevor du etwas hinzufügst.
5. **Schluss.** Du hörst auf, wenn eine weitere Runde <für das Publikum aus dem ersten Absatz> nicht mehr auffiele, frühestens nach den <N> Runden. Das Zeitlimit geht vor: <X> Minuten nach deinem Start schließt du die laufende Runde ab, prüfst sie und schreibst den Bericht, auch wenn es weniger als <N> Runden waren. Prüf die Uhrzeit am Ende jeder Runde.
6. **Schlussbericht**, siehe unten.

## Durchhalten und Grenzen

Während des Laufs sitzt niemand daneben. Arbeite den ganzen Auftrag ab, ohne auf eine Antwort zu warten. Wenn du merkst, dass du eine Restliste schreiben oder anbieten willst weiterzumachen, mach stattdessen mit dem nächsten Teil weiter.

Gewöhnliche Hindernisse (ein Fehler, eine Zeitüberschreitung, ein Werkzeug, das nicht antwortet, ein leeres Ergebnis) untersuchst du zuerst. Sind sie keine echte Sperre, arbeitest du dich mit deinen Mitteln hindurch: warten und wiederholen, die Anfrage korrigieren, einen anderen Weg nehmen.

Ohne Rückfrage erlaubt:

- <Dateien anlegen und ändern in den erlaubten Pfaden>
- <Hilfsdateien des Laufs: Laufnotiz, Belege-Ordner, die Zeile in der `.gitignore`, was der Prüfweg braucht>
- <Bauen, testen, lokaler Server oder Simulator, lokale Datenbank>
- <Commits auf dem Branch, Pakete im Projekt nach Absprache>

Nicht anfassen:

- <Grenze mit Geltungsbereich> (<Grund>). <Was du stattdessen tust.>
- <Push, Deploy, andere Datenbanken, globale Installationen, Pfade außerhalb: jeweils mit Grund>

Stößt du an eine dieser Grenzen, umgehst du sie nicht. Du arbeitest an allem weiter, was nicht davon abhängt, und nennst die Stelle im Schlussbericht.

Entscheidungen, die dieser Auftrag nicht vorhergesehen hat, triffst du selbst, und zwar so, wie es der Messlatte am besten dient. Halte sie in der Laufnotiz fest.

## Schlussbericht

Ich habe den Lauf nicht gesehen und komme aus anderer Arbeit. Schreib den Bericht so, dass er ohne Vorwissen verständlich ist: das Wichtigste zuerst, ganze Sätze, einfache Wörter, keine Abkürzungen, die du während der Arbeit erfunden hast. Er ist kurz und enthält:

1. Wie ich das Ergebnis starte und was ich in den ersten Sekunden tue.
2. Den besten Moment und den Schalter, der ihn direkt zeigt.
3. Was du gebaut und verwendet hast, einschließlich jeder neuen Abhängigkeit mit Grund.
4. Die Messwerte der letzten Runde neben ihrer Schwelle.
5. Bekannte Mängel, auch die, die du nicht beheben konntest.
6. Entscheidungen, die du für mich getroffen hast, Annahmen, die du geändert hast, und Grenzen, an die du gestoßen bist.
7. (Profil) Die Liste „<Am Gerät zu prüfen / Von mir zu prüfen>": jeder Punkt als Prüfschritt mit dem Schalter, der ihn vorbereitet, dem, worauf ich achten soll, und dem, woran ich erkenne, dass es stimmt.
````

---

## Hinweise zum Ausfüllen

- **Reihenfolge im Auftragsteil:** Sie folgt den Bausteinen 1 bis 7. Der Leser soll zuerst wissen, wofür er baut, dann was, dann woran es gemessen wird.
- **Jeder Abschnitt trägt Neues bei.** Die Lückenliste sagt, was heute falsch ist und in welche Richtung es geht. Die Konkretion sagt, wie es genau sein soll. „Was exzellent sein muss" sagt, woran man es an einem Beleg erkennt. Die Rückgabeliste sagt, was der User selbst prüft. Steht derselbe Punkt in drei Abschnitten mit denselben Worten, kürze zwei davon auf das, was nur dort hingehört.
- **Drei Listen:** „Nicht gewollt" ist Geschmack und Gestaltung, „Harte Regeln" ist Qualität, die immer gilt, „Nicht anfassen" ist Befugnis. Die Abgrenzung steht in `REFERENCE.md`, Abschnitt „Harte Regeln und die drei Listen".
- **Länge:** Der Auftragsteil trägt die Konkretion und ist der längste. Die beiden durchgespielten Beispiele für mittlere Vorhaben kamen auf 4.000 bis 5.000 Wörter. Das ist die obere Grenze für diese Stufe. Ein kleines Vorhaben kommt mit einem Drittel aus. Wird der Prompt länger, such zuerst nach Doppelungen und prüf dann, ob der Umfang noch zum Zeitlimit passt.
- **Titel:** ein Name für das Vorhaben, kein Satz. Er hilft dem User, den Lauf in der Session-Liste wiederzufinden.
- **Pfade für Laufnotiz und Belege:** `docs/briefs/{YYYY-MM-DD}-{slug}.lauf.md` für die Laufnotiz (wird committet) und `tmp/brief-{slug}/` für die Belege (steht in der `.gitignore`). Im leeren Ordner genügen `LAUF.md` und `belege/`. Beide müssen in den erlaubten Pfaden liegen, siehe `REFERENCE.md`, „Grenzen".
- **Befehle des Prüfwegs:** Stehen sie in der `CLAUDE.md` und stimmen, genügt der Verweis. Fehlen sie dort oder sind sie veraltet, schreibst du die Befehlsfolge aus dem Profil aus, mit den Werten des Projekts (Scheme, Kennung, Port).
- **Liste im Schlussbericht:** Sie heißt im Profil `apple.md` „Am Gerät zu prüfen", sonst „Von mir zu prüfen". Entfällt nur, wenn sich wirklich alles in der Prüfumgebung beurteilen lässt. Das ist selten.
- **Englische Fassung:** Will der User den Prompt auf Englisch, übersetzt du auch die festen Absätze. Schalternamen, Pfade und Befehle bleiben gleich.
