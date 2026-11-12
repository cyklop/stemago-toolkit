# Profil: Apple-nativ (visionOS, iOS, macOS)

Gilt für Apps, die mit Xcode gebaut werden: Swift, SwiftUI, RealityKit, UIKit, AppKit. Der Schwerpunkt liegt auf visionOS, weil dort am wenigsten ohne Gerät beurteilbar ist. Die Abschnitte zu iOS und macOS stehen am Ende.

**Stand der Prüfung:** 12.11.2026, Xcode 27.2, visionOS-27.2-Simulator, Mac mit Apple Silicon. Alle Befehle im Abschnitt „So sieht der Lauf sein Ergebnis" sind an diesem Tag an einer echten visionOS-App durchgelaufen (SwiftUI, RealityKit, zwei Immersive Spaces). Die Grenzen stammen aus der Apple-Dokumentation (Quellen am Ende) und aus Messungen im Simulator.

Xcode ändert Werkzeuge und Namen mit jeder Hauptversion. In Xcode 27 heißt die Simulator-Oberfläche Device Hub, eine eigene Simulator-App gibt es dort nicht mehr. Verlass dich deshalb weder auf diese Datei noch auf Vorwissen, wenn die lokale Version abweicht:

- Du selbst liest in Schritt 2 des Skills aus, was installiert ist (nächster Abschnitt). Das sind lesende Abfragen. Du baust und startest dabei nichts.
- Der Lauf beweist als ersten Schritt den Prüfweg. Das steht im Prompt.

## Vor dem Interview auslesen

```bash
xcodebuild -version
xcrun simctl list devices available        # Geräte und ihre Kennungen (UDID), nach Plattform
xcodebuild -list -project <App>.xcodeproj  # Schemes und Ziele
```

Dazu aus dem Projekt: Plattform (`SDKROOT`, `SUPPORTED_PLATFORMS` in `project.pbxproj`), Bundle-Kennung (`PRODUCT_BUNDLE_IDENTIFIER`), die Szenen der App (`WindowGroup`, `ImmersiveSpace` mit ihren IDs), die Wurzel-View, das Test-Framework, die Kennung des `Logger`-Untersystems, die `@AppStorage`- und `UserDefaults`-Schlüssel, und ob die App schon Startargumente auswertet (Suche nach `ProcessInfo`).

Liegt das Xcode-Projekt in einem Unterordner, brauchen die Befehle von der Wurzel des Repositorys aus `-project <unterordner>/<App>.xcodeproj`. Steht das in der `CLAUDE.md` nicht dabei, schreibst du es in den Prompt.

Nennt die `CLAUDE.md` des Projekts eine feste Simulator-Version (`OS=…`), gleich sie mit `simctl list` ab. Eine Version, die nicht installiert ist, lässt den Befehl scheitern. In den Prompt gehört dann die Kennung des Geräts (`id=<UDID>`) oder die Anweisung, sie zu Beginn auszulesen.

## So sieht der Lauf sein Ergebnis (visionOS)

Der ganze Weg läuft über die Kommandozeile. Device Hub muss dafür nicht geöffnet sein.

```bash
# 1. Für den Simulator bauen (eigener Ordner für Build-Produkte, damit der Pfad zur App feststeht)
xcodebuild build -project <App>.xcodeproj -scheme <Scheme> -configuration Debug \
  -destination 'generic/platform=visionOS Simulator' -derivedDataPath <build-ordner>
# Ergebnis: <build-ordner>/Build/Products/Debug-xrsimulator/<App>.app

# 2. Simulator starten und warten, bis er bereit ist
xcrun simctl boot <UDID>
xcrun simctl bootstatus <UDID> -b

# 3. App installieren und mit Schaltern starten
xcrun simctl install <UDID> <pfad-zur-app>
SIMCTL_CHILD_<NAME>=<wert> xcrun simctl launch --terminate-running-process <UDID> <bundle-id> -<schluessel> <wert>

# 4. Einige Sekunden warten, dann fotografieren
xcrun simctl io <UDID> screenshot <datei>.png

# 5. Bewegung: im Hintergrund aufnehmen, mit SIGINT beenden, Einzelbilder ziehen
xcrun simctl io <UDID> recordVideo --codec=h264 --force <datei>.mov > <datei>.log 2>&1 &
REC=$!
# … App mit Schaltern starten, einige Sekunden warten …
kill -INT $REC; wait $REC          # SIGINT beendet die Aufnahme, danach schreibt simctl die Datei fertig
ffmpeg -i <datei>.mov -vf "fps=10,scale=1280:-1" <ordner>/bild-%03d.png

# 6. Tests
xcodebuild test -project <App>.xcodeproj -scheme <Scheme> -destination 'platform=visionOS Simulator,id=<UDID>'
```

Was dabei gemessen und beobachtet wurde. Das gehört als Wissen in den Prompt, wo es das Vorhaben betrifft:

- **Der Screenshot zeigt eine einzelne, flache Ansicht** des simulierten Raums aus einem festen Blickpunkt, 3840×2160 Pixel beim Gerätetyp „Apple Vision Pro". Das App-Fenster füllt davon nur die Mitte. Der Lauf schneidet deshalb zu, bevor er urteilt (`sips -c <höhe> <breite> bild.png --out ausschnitt.png` schneidet mittig), und verkleinert große Bilder vor dem Ansehen (`sips -Z 1600 …`).
- **Der Blickpunkt lässt sich von der Kommandozeile nicht bewegen.** `simctl` hat keinen Befehl für Kamera, Tippen oder Pinch. Bewegen und Bedienen geht nur von Hand in Device Hub. Inhalte, die der Lauf beurteilen soll, müssen also aus dem Startblickpunkt sichtbar sein, oder ein Schalter rückt sie für die Prüfung dorthin.
- **Die Bildrate der Einzelbilder folgt der kürzesten Bewegung.** Eine Bewegung von 0,6 Sekunden braucht mindestens 10 Bilder je Sekunde, sonst bleiben drei Bilder übrig.
- **Direkt nach dem Start zeigt der Screenshot nur das Startbild** der App. Fünf bis acht Sekunden warten, oder besser: Die App schreibt eine Logzeile, sobald der Zustand steht, und der Lauf wartet darauf.
- **`print`-Ausgaben** erscheinen mit `xcrun simctl launch --console-pty …` (blockiert, bis die App endet, also im Hintergrund starten). Mit `--stdout=<datei>` blieb die Datei während des Laufs leer, weil die Ausgabe gepuffert wird. Meldungen über `Logger` liest der Lauf mit `xcrun simctl spawn <UDID> log show --last 1m --style compact --predicate 'subsystem == "<kennung>"'`.
- **Zeiten:** sauberer Build einer kleinen App etwa 45 Sekunden, Testlauf etwa 2 Minuten, erster Start eines neu angelegten Simulators über 2 Minuten, ein späterer Start 13 Sekunden. Der Lauf nimmt ein vorhandenes Gerät und lässt es über die Runden hinweg laufen.
- **Nach `xcodebuild test` war der Simulator heruntergefahren.** `xcrun simctl bootstatus <UDID> -b` startet ihn bei Bedarf und wartet, bis er bereit ist. Der Lauf ruft es vor jedem `launch` auf.
- **Herunterfahren muss der Lauf den Simulator nicht.** Schutz-Hooks können `simctl shutdown` und `simctl reboot` für System-Befehle halten und blocken (so der Hook von stemago-tools bis Version 3.2.0). Das ist dann eine Sperre, die der Lauf stehen lässt.
- **Signatur:** Der Simulator-Build lief ohne Entwicklerkonto durch („Sign to Run Locally").

## Schalter für Zustände

Startargumente und Umgebungsvariablen übernehmen die Rolle der URL-Parameter.

- **Startargumente der Form `-schluessel wert`** landen in den `UserDefaults` der App. `@AppStorage("schluessel")` und `UserDefaults.standard` lesen sie ohne weiteren Code. Geprüft: Ein Start mit `-hasAcceptedDisclaimer YES` übersprang den Hinweisdialog einer App, die diesen Wert in `@AppStorage` hält. Der Wert gilt nur für diesen Start und wird nicht gespeichert.
- **Umgebungsvariablen** setzt man beim Aufruf mit dem Präfix `SIMCTL_CHILD_`. Die App liest sie ohne Präfix aus `ProcessInfo.processInfo.environment`.
- **Ein Immersive Space lässt sich nur aus einer View öffnen** (`openImmersiveSpace` aus der Umgebung). Der Schalter wird deshalb in der Wurzel-View ausgewertet, zum Beispiel in einem `.task`. Geprüft: Start mit Umgebungsvariable, die App bereitet den Zustand vor und öffnet den Space, der Screenshot zeigt den RealityKit-Inhalt.
- **Ein Start je Zustand.** `--terminate-running-process` beendet die laufende Instanz, damit jeder Screenshot von einem frischen, bekannten Zustand stammt.

Schalter, die du im Interview vorschlägst (die Namen legt ihr gemeinsam fest):

| Schalter | Zweck |
|---|---|
| `-briefState <name>` | einen benannten Zustand direkt öffnen: eine Ansicht, eine Phase eines Ablaufs, einen bestimmten Immersive Space |
| `-briefSeed <n>` | feste Testdaten und feste Zufallsfolge |
| `-briefTime <sekunden>` | eine Animation oder einen Ablauf an einem Zeitpunkt anhalten |
| `-briefAuto <variante>` | der Ablauf spielt sich selbst durch, weil Tippen und Pinch von der Kommandozeile nicht gehen. Die Varianten bilden die Fälle ab, die der Lauf sehen muss, zum Beispiel `treffer`, `verpasst`, `wechsel` |
| `-briefPlace <name>` | Inhalte für die Prüfung in den Startblickpunkt rücken (zum Beispiel `nah`, `seite`), weil sich die Kamera nicht bewegen lässt |
| `-briefHead <meter>` oder ein fester Wert beim Direktstart | Kopfhöhe und andere Tracking-Werte vorgeben, weil der Simulator dafür keine echten liefert |
| vorhandene `@AppStorage`- und `UserDefaults`-Schlüssel | Erststart-Dialoge überspringen, gespeicherte Stände vorgeben (Level, Einstellungen) |

**Wie die Schalter zusammenwirken, steht im Prompt.** Ein Beispiel: `-briefState uebung-halten -briefAuto treffer -briefTime 0.3` öffnet den Zustand, lässt den Selbstlauf einmal treffen und hält den Ablauf 0,3 Sekunden nach Beginn des Zustands an. `-briefTime` zählt ab dem Moment, in dem der gewählte Zustand steht, nicht ab dem Start der App.

**Wo die Schalter eingehängt werden:** Die Auswertung braucht die Wurzel-View oder den Einstiegspunkt der App, das Debug-Menü einen Platz im Hauptfenster. Liegen diese Dateien außerhalb der erlaubten Pfade, vereinbarst du im Interview eine Ausnahme oder einen Ausweichort (zum Beispiel ein Modifier, der im Einstiegspunkt an die Wurzel-View gehängt wird).

**Was ein Prüfstart speichert:** Ein Start über Schalter oder Debug-Menü schreibt keine dauerhaften Stände (Level, Verlauf, Statistik). Sonst verfälscht die Prüfung am Gerät die echten Daten des Users.

Die Schalter wirken nur im Debug-Build (`#if DEBUG`), damit sie nicht in den App Store gelangen. Damit der User am Gerät dieselben Zustände erreicht, verlangt der Prompt zusätzlich einen der beiden Wege: ein Debug-Menü in der App, das die Zustände auflistet, oder die Angabe der Argumente für das Xcode-Schema (Run → Arguments), über das Xcode Startargumente und Umgebungsvariablen an die App gibt.

## Belege je Runde

- Je wichtigem Zustand ein Screenshot, zugeschnitten auf das Fenster oder den Inhalt, dazu das unbeschnittene Bild für Lage und Größe im Raum.
- Für Bewegung und Abläufe eine Bildfolge aus einer Aufnahme.
- Ausgabe von `xcodebuild test` für die Logik. Alles, was sich als reine Funktion fassen lässt (Zustandsmaschinen, Berechnungen, Parameter), gehört in Unit-Tests, weil der Simulator dafür der schwächste Prüfweg ist.
- Die Logzeilen der App für Werte, die im Bild nicht stehen: Abstände in Metern, Größen, Zeitpunkte, welche Phase aktiv ist.
- Build ohne neue Warnungen.

Für räumliche Inhalte gilt: Der Lauf kann Lage, Größe und Abstand nicht sehen, aber berechnen. Der Prompt verlangt deshalb, dass die App die räumlichen Maße ihrer Inhalte im Debug-Build ausgibt (Entfernung zum Kopf, Sehwinkel, Größe), und der Lauf prüft sie gegen die Vorgaben aus dem Auftrag.

## Messwerte und Schwellen

| Messwert | Schwelle | Bemerkung |
|---|---|---|
| Unit-Tests | alle grün | |
| Build-Warnungen | keine neue gegenüber dem Stand zu Beginn | Der Lauf hält die vorhandenen Warnungen im ersten Schritt fest. Bestehende außerhalb der erlaubten Pfade kann er nicht beheben. |
| Räumliche Maße aus dem Log | innerhalb der Vorgaben aus dem Auftrag | zum Beispiel Mindestabstand, Sehwinkel von Bedienflächen |
| Lesbarkeit im Screenshot | jeder Text im zugeschnittenen Bild lesbar | ersetzt nicht die Prüfung durch die Optik des Geräts |

Bildrate und Zeitmessungen sind im Simulator kein Messwert. Apple schreibt dazu, dass man sich wegen der Unterschiede zwischen Simulator und Gerät nicht auf Zeitangaben verlassen kann. Sie kommen in die Liste „Am Gerät zu prüfen".

## Rolle des Kritikers

Ein strenger Gestalter für räumliche Oberflächen, der die Gestaltungsrichtlinien von Apple für visionOS kennt und jeden Screenshot mit den besten Apps der Plattform vergleicht. Er achtet auf Lesbarkeit vor wechselndem Hintergrund, Größe und Abstand der Bedienflächen, Ruhe im Bild und darauf, ob man ohne Erklärung weiß, wohin man schauen und was man tun soll. Bei jedem Urteil sagt er dazu, ob es am Screenshot belegbar ist oder erst am Gerät.

## Harte Regeln (Auswahl für den Prompt)

Die Regeln gelten für das, was der Lauf neu baut. Macht das bestehende Produkt etwas mit Absicht anders (ein sehr naher Abstand, weil die Übung ihn verlangt, eine Annäherung auf den Nutzer zu), schreibst du „nicht näher und nicht schneller als heute" und nennst den heutigen Wert aus dem Code.

- Jede ARKit-Funktion wird vor der Nutzung mit `isSupported` abgefragt, und es gibt einen Weg ohne sie (im Simulator fehlen die meisten, und am Gerät kann der Nutzer die Freigabe verweigern).
- Die Prüfschalter sind nur im Debug-Build aktiv.
- Inhalte in einem Immersive Space erscheinen in einem bequemen Abstand und auf Augenhöhe. Die Werte stehen im Auftrag und im Log.
- Keine erzwungene Bewegung des ganzen Bildes, keine schnellen Bewegungen auf den Nutzer zu, außer der Auftrag verlangt sie ausdrücklich (Komfort lässt sich im Simulator nicht prüfen, deshalb gilt hier die vorsichtige Vorgabe).
- Texte in der Sprache der App, keine Platzhalter.
- Bestehende fachliche Aussagen und Hinweise der App bleiben unverändert, soweit der Auftrag sie nicht nennt (zum Beispiel medizinische Hinweise).

## Im Simulator nicht prüfbar

| Was | Stand | Folge für den Prompt |
|---|---|---|
| Tiefenwirkung, Stereobild, Vergenz | Der Screenshot ist ein flaches Einzelbild. | Maße über das Log prüfen. Die Wirkung kommt in die Liste. |
| Blicksteuerung | In Device Hub steht der Mauszeiger für den Blick. Von der Kommandozeile gibt es keine Eingabe. | Zustände über Schalter. Trefferflächen nach Maß. Die Bedienung kommt in die Liste. |
| Hand-Tracking, eigene Gesten | `HandTrackingProvider.isSupported` war im Simulator `false`. | Logik hinter den Gesten in Unit-Tests. Die Gesten kommen in die Liste. |
| Ebenen und Raumerkennung | `PlaneDetectionProvider.isSupported` und `SceneReconstructionProvider.isSupported` waren `false`. | Weg ohne diese Daten bauen. Verhalten im echten Raum kommt in die Liste. |
| Kopfposition | `WorldTrackingProvider.isSupported` war `true`, die Werte sind aber simuliert. Eine Abfrage der Kopfhöhe ergab in der geprüften App 0,0 m. | Werte aus dem Simulator nicht als echt behandeln. Für die Prüfung einen festen Wert per Schalter vorgeben. |
| Komfort | Nicht beurteilbar: Abstand, Bewegung, Dauer, Nackenhaltung, Ermüdung der Augen. | Vorsichtige Vorgaben als harte Regel. Kommt in die Liste. |
| Leistung | Apple: Zeitangaben aus dem Simulator sind nicht belastbar. Am Gerät strebt das System 90 Bilder pro Sekunde an und kann bei Wärme die Rate halbieren. | Kein Messwert im Lauf. Messung mit Instruments am Gerät kommt in die Liste. |
| Passthrough und echtes Licht | Der Simulator zeigt gerenderte Beispielräume. Wechseln lässt sich die Szene nur von Hand in Device Hub. | Lesbarkeit im Beispielraum prüfen. Der echte Raum kommt in die Liste. |
| Lesbarkeit durch die Optik | Laut Apple können Screenshots aus dem Simulator eine andere Größe und ein anderes Seitenverhältnis haben als die vom Gerät. | Schriftgrößen nach den Vorgaben der Plattform. Kommt in die Liste. |
| Ton im Raum | Der Lauf hört nichts. | Kommt in die Liste. |
| Bedienung durch Tippen und Pinch im Lauf | `simctl` hat dafür keinen Befehl. UI-Tests mit XCUITest sind ein möglicher Weg, hier aber nicht geprüft. | `-briefAuto 1` verlangen. Will der Lauf UI-Tests nutzen, beweist er sie zuerst an einem einzelnen Tipp. |

## Die Liste „Am Gerät zu prüfen"

Jeder Prompt aus diesem Profil verlangt sie, und der Lauf gibt sie im Schlussbericht zurück. Du füllst sie im Interview mit dem User vor: Geh die Tabelle oben durch und nimm jeden Punkt auf, der das Vorhaben trifft. Der Lauf ergänzt, was ihm unterwegs auffällt.

Textbaustein für den Prompt:

```
Im Simulator siehst du ein flaches Bild aus einem festen Blickpunkt. Tiefenwirkung, Blick- und
Handsteuerung, Komfort und Leistung kannst du dort nicht beurteilen. Behaupte dazu nichts.
Führe stattdessen die Liste „Am Gerät zu prüfen" und gib sie im Schlussbericht zurück.
Jeder Eintrag hat drei Teile: der Zustand und wie ich ihn am Gerät erreiche (Debug-Menü oder
Startargument), worauf ich achten soll, und woran ich erkenne, dass es stimmt.
Mindestens diese Punkte stehen darin: <Punkte aus dem Interview>.
```

Ein guter Eintrag ist ein Prüfschritt und keine Überschrift. „Tiefe prüfen" hilft dem User nicht. Brauchbar ist: „Zustand `uebung-nah` öffnen. Die Kugel soll in 40 cm Abstand auf Augenhöhe stehen und einfach erscheinen, nicht doppelt. Wenn du sie doppelt siehst oder sie tiefer als das Kinn steht, stimmt die Kopfhöhe nicht."

## Typische Risiken

- **Prüfweg zuerst:** bauen, starten, einen Screenshot öffnen, bevor irgendetwas geändert wird. Ein fehlender Simulator, ein falsches Scheme oder eine veraltete Versionsangabe fällt sonst erst nach der ersten Version auf.
- **Ein Zustand zuerst:** einen einzigen Zustand über den Schalter ansteuern, fotografieren und auf Zielqualität bringen, dann die übrigen. Scheitert der Schalter-Mechanismus, scheitert er sonst für alle zugleich.
- **Der Build ist langsam.** Jede Runde kostet Build, Installation und einen Start je Zustand. Der Lauf sammelt Änderungen und baut dann, statt nach jeder Zeile zu bauen. Bei der Laufgröße zählt das mit: Rechne je Runde 5 bis 10 Minuten Wartezeit dazu (`REFERENCE.md`, „Laufgröße").
- **Ob der Inhalt im Screenshot überhaupt erscheint,** zeigt erst der erste Zustand. Inhalte am Kopf-Anker oder sehr nah am Blickpunkt können im Bild fehlen oder abgeschnitten sein. Der Prompt nennt dafür den Ausweichweg: Der Inhalt wird nur für den Beleg per Schalter an einen festen Punkt vor den Blickpunkt gesetzt, und der Bericht nennt das.
- **Der Simulator verdeckt Fehler,** die nur am Gerät auftreten (Kopfposition, Tracking, Freigaben). Was der Lauf nur im Simulator gesehen hat, nennt er im Bericht so.
- **Fehlende Simulator-Laufzeit:** Ohne installierte visionOS-Laufzeit scheitert der Build (die `CLAUDE.md` des geprüften Projekts nennt den Schritt `RealityAssetsCompile`). Nachinstallieren ist ein Eingriff in die Maschine des Users. Der Lauf meldet das und installiert nichts nach, außer der Auftrag erlaubt es.

## Zusatzfragen im Interview

- Bei Baustein 1: Wann und wie lange hast du das Gerät zur Hand, um die Liste abzuarbeiten? Daraus ergibt sich, wie lang die Liste sein darf und wie viel der Lauf auf Annahmen bauen darf.
- Bei Baustein 2: Was am Verhalten am Gerät weißt du schon, das der Simulator nicht zeigt (ein Abstand, der sich zu nah anfühlt, eine Geste, die oft danebengeht)?
- Bei Baustein 4: Welche Abstände, Größen und Zeiten sind fachlich vorgegeben (zum Beispiel 40 cm, 3 m, 2 Sekunden)? Sie werden zu Maßen im Log.
- Bei Baustein 8: Welche Zustände und Phasen muss ich einzeln sehen können? Welche davon liegen in einem Immersive Space?
- Bei Baustein 8: Gibt es Erststart-Dialoge oder gespeicherte Stände, die für die Prüfung übersprungen oder vorgegeben werden müssen?
- Bei den Grenzen: Liegen Einstiegspunkt und Wurzel-View in den erlaubten Pfaden? Darf ein Prüfstart am Gerät echte Stände schreiben?

## iOS und iPadOS

Der Weg ist derselbe wie bei visionOS: `xcodebuild` mit `-destination 'platform=iOS Simulator,id=<UDID>'`, danach `simctl install`, `launch`, `io screenshot`. Der Screenshot zeigt hier den ganzen Bildschirm des Geräts. Startargumente und `SIMCTL_CHILD_` funktionieren genauso, weil es dieselben `simctl`-Befehle sind. An einem iOS-Projekt durchgespielt wurde dieser Abschnitt nicht. Der Lauf beweist den Prüfweg deshalb zuerst. Nicht prüfbar im Simulator: Kamera, Sensoren, Haptik, Leistung, Akku, echte Push-Zustellung, Bedienung mit dem Daumen an einem echten Gerät.

## macOS

Für macOS-Apps gibt es keinen Simulator. Die App läuft direkt auf dem Mac, und Screenshots brauchen eine Bildschirmaufnahme-Freigabe für das Programm, das sie macht. Dieser Weg ist hier nicht geprüft. Nimm für macOS-Apps `profiles/general.md` dazu und lass den Lauf den Prüfweg als Erstes beweisen: bauen, starten, ein Bild des Fensters erzeugen und öffnen. Gelingt das nicht, stützt sich der Lauf auf Unit-Tests, UI-Tests und SwiftUI-Vorschauen, und die Sichtprüfung kommt in die Liste „Von mir zu prüfen".

## Quellen

Apple-Dokumentation, gelesen am 12.11.2026:

- Running your app on simulated or physical devices: `https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices`
- Interacting with your visionOS app in Device Hub: `https://developer.apple.com/documentation/xcode/interacting-with-your-visionos-app-in-device-hub`
- Capturing screenshots and videos from devices: `https://developer.apple.com/documentation/xcode/capturing-screenshots-and-videos-from-devices`
- Customizing the build schemes for a project: `https://developer.apple.com/documentation/xcode/customizing-the-build-schemes-for-a-project`
- `DataProvider.isSupported`: `https://developer.apple.com/documentation/arkit/dataprovider/issupported`
- Setting up access to ARKit data: `https://developer.apple.com/documentation/visionos/setting-up-access-to-arkit-data`
- Analyzing the performance of your visionOS app: `https://developer.apple.com/documentation/visionos/analyzing-the-performance-of-your-visionos-app`

Lokal geprüft: `xcodebuild -version`, `xcrun simctl help`, `simctl help launch`, `simctl help io` und der oben beschriebene Durchlauf.
