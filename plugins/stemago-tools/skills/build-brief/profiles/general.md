# Profil: Allgemein

Gilt für alles, was die anderen Profile nicht abdecken: Desktop-Apps (.NET, macOS ohne Simulator), Dokumente und Berichte, Datenauswertungen, Automationen, Hardware-nahe Werkzeuge, und der leere Ordner, solange die Plattform nicht feststeht.

Dieses Profil gibt keine fertigen Antworten. Es gibt dir die vier Fragen, die du im Interview für diese Plattform selbst klärst, und die Regel, die für alle gilt: **Der Lauf beweist seinen Prüfweg, bevor er baut.**

Steht nach den ersten Fragen fest, dass das Vorhaben doch ins Web, zu Apple oder ins Backend gehört, lädst du das passende Profil nach.

## Die vier Fragen

### 1. Wie bekommt der Lauf sein Ergebnis zu sehen?

Geh mit dem User die Möglichkeiten durch, von der stärksten zur schwächsten:

| Weg | Geeignet für | Zu klären |
|---|---|---|
| Das Ergebnis als Bild: Screenshot des Fensters, gerenderte Seite, exportierte Grafik | Desktop-Apps, Dokumente, Diagramme, Berichte | Gibt es einen Befehl, der ohne Handgriff ein Bild erzeugt? Braucht er eine Freigabe des Betriebssystems? |
| Das Ergebnis als Text oder Daten: Ausgabe, Export, Protokoll | Auswertungen, Automationen, Konverter | Gegen welche bekannte, richtige Ausgabe wird verglichen? |
| Automatische Tests | Logik in jeder Art von Projekt | Welches Framework, welcher Befehl? |
| Eine Messung | alles mit Zeit, Menge oder Genauigkeit | Welcher Wert, welche Bedingung? |
| Gar nicht | Hardware, echte Geräte, Wirkung auf Menschen | Dann kommt es in die Liste „Von mir zu prüfen" |

Bei Dokumenten ist der Prüfweg das gerenderte Ergebnis (PDF-Seiten als Bilder), nicht die Quelldatei. Bei Desktop-Apps ohne Screenshot-Weg bleibt oft nur: die Logik in Tests, die Oberfläche in einer Vorschau oder einem UI-Test-Framework, die Sichtprüfung beim User.

Findet ihr keinen Weg, auf dem der Lauf wenigstens den Star des Vorhabens beurteilen kann, ist ein langer eigenständiger Lauf das falsche Mittel. Sag das dem User. Ein Lauf, der sein Ergebnis nicht sieht, wiederholt nur seine erste Version.

### 2. Welche Schalter machen Zustände erreichbar?

Übertrag das Prinzip auf die Plattform: Jeder wichtige Zustand ist mit einem Aufruf herstellbar, ohne Handgriffe und bei jedem Mal gleich.

- Startargumente oder Umgebungsvariablen der Anwendung (`--state <name>`, `--seed <n>`, `--time <t>`)
- benannte Beispieldateien oder Datensätze (`leer`, `standard`, `gross`, `kaputt`)
- ein Selbstlauf (`--auto`), wenn Bedienung von außen nicht geht
- eine feste Uhr und fester Zufall, damit zwei Läufe vergleichbar sind
- bei Dokumenten: eine Kurzfassung mit je einem Beispiel für jedes Element (Tabelle, Abbildung, lange Überschrift, Fußnote)

### 3. Welche Rolle hat der Kritiker?

Der strengste Fachmensch, der dieses Ergebnis beruflich beurteilt. Frag den User, wer das in seinem Fall ist: die Lektorin, der Controller, der Prüfingenieur, die Kundin in der Abnahme. Im Prompt steht die Rolle mit dem, worauf sie zuerst schaut.

### 4. Was lässt sich in dieser Umgebung nicht prüfen?

Frag ausdrücklich danach und schlag vor, was du vermutest. Zu jedem Punkt gibt es entweder einen Ausweichweg, den der Lauf baut, oder einen Eintrag in der Liste „Von mir zu prüfen". Typisch: echte Geräte und Peripherie, andere Betriebssysteme und Versionen, Drucker und Papier, Daten, auf die der Lauf keinen Zugriff hat, Verhalten über Tage, und ob es dem Publikum gefällt.

## Belege, Messwerte, harte Regeln

Leite sie aus den Antworten ab:

- **Belege je Runde:** mindestens drei verschiedene Zustände oder Ausschnitte über den Prüfweg aus Frage 1, dazu die Ausgabe der Tests.
- **Messwert und Schwelle:** der eine Wert, an dem der User im Alltag merkt, dass es gut ist. Gibt es keinen messbaren, nimm eine Zählung (zum Beispiel: kein Element läuft über den Seitenrand, keine Warnung im Build).
- **Harte Regeln:** echte Inhalte statt Platzhalter. Keine Annahme als Tatsache ausgeben. Nichts außerhalb der erlaubten Pfade. Dazu das, was der User für diese Plattform nennt.
- **Verbotsliste:** Frag, woran man in diesem Fach die lieblose Standardlösung erkennt.

## Typische Risiken

- **Prüfweg zuerst:** Das ist hier der wichtigste Hinweis, weil der Weg nicht erprobt ist. Der Lauf erzeugt an einem bestehenden oder trivialen Beispiel einen Beleg und öffnet ihn. Gelingt das nach einigen Versuchen nicht, weicht er auf den nächstschwächeren Weg aus der Tabelle aus und nennt das im Schlussbericht.
- **Ein Ausschnitt zuerst:** ein Element, eine Seite, ein Fall auf Zielqualität, dann der Rest.
- **Lange Schritte** (Rendern, Exportieren, Berechnen): erst klein, dann ganz, und nach jedem Lauf die erzeugten Dateien prüfen.
- **Freigaben des Betriebssystems** (Bildschirmaufnahme, Bedienungshilfen, Zugriff auf Ordner): Der Lauf kann sie nicht selbst erteilen. Braucht der Prüfweg eine, klärt der User das vor dem Start, oder der Prompt nennt den Ausweichweg.

## Zusatzfragen im Interview

- Bei Baustein 1: Auf welcher Maschine und in welcher Umgebung läuft das Ergebnis am Ende? Ist das dieselbe, auf der der Lauf arbeitet?
- Bei Baustein 2: Gibt es ein Beispiel für ein gelungenes Ergebnis dieser Art, mit dem der Lauf vergleichen kann?
- Bei Baustein 7: Was prüfst du selbst als Erstes, wenn du das Ergebnis bekommst?
- Bei Baustein 8: Die vier Fragen oben.
- Bei den Grenzen: Was muss installiert sein, damit der Lauf bauen und prüfen kann, und ist es das schon?
