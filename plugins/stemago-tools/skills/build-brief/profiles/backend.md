# Profil: Backend, CLI, Bibliothek

Gilt für alles ohne eigene Oberfläche: API-Endpunkte, Services, Worker, Importe und Migrationen, Kommandozeilen-Werkzeuge, Bibliotheken. Der Lauf beurteilt hier keine Bilder. Seine Belege sind Testergebnisse, Messwerte und echte Beispielausgaben.

## So sieht der Lauf sein Ergebnis

Über drei Wege, die sich ergänzen. Im Prompt stehen alle drei mit ihren Befehlen:

1. **Tests:** die Testbefehle des Projekts (aus `CLAUDE.md`, `package.json`, `composer.json`, `pyproject.toml`). Sie zeigen, ob es stimmt.
2. **Beispielaufrufe mit gespeicherter Ausgabe:** Der Lauf ruft das Ergebnis so auf, wie ein Nutzer es täte (HTTP-Anfrage gegen den lokalen Server, CLI-Befehl, Aufruf der Bibliothek in einem kurzen Skript), und legt Anfrage und Antwort als Datei ab. Sie zeigen, wie es sich anfühlt: Feldnamen, Fehlermeldungen, Reihenfolge, Lesbarkeit.
3. **Messungen:** ein kleines Messskript mit festem Datensatz, das Zeiten und Mengen ausgibt.

Such im Kontext, was davon schon da ist: Test-Framework, Testdatenbank oder Container-Setup, vorhandene Fixtures, ein Seed-Skript, ein Startbefehl für den lokalen Server. Fehlt eine Testdatenbank, klärst du im Interview, wogegen der Lauf arbeiten darf.

## Schalter für Zustände

Statt URL-Parametern: alles, was einen Lauf wiederholbar macht und schwer erreichbare Fälle direkt herstellt.

| Schalter | Zweck |
|---|---|
| Benannte Fixtures oder Seed-Szenarien (`leer`, `standard`, `gross`, `kaputt`) | derselbe Ausgangszustand bei jedem Lauf |
| Fester Zufall (`--seed <n>` oder Umgebungsvariable) | gleiche Ausgabe bei gleicher Eingabe, damit zwei Läufe vergleichbar sind |
| Feste Uhr (einstellbare Zeitquelle) | Fristen, Abläufe und Zeitzonen prüfen, ohne zu warten |
| `--dry-run` | zeigt, was geschehen würde, ohne zu schreiben |
| Attrappen für fremde Dienste (aufgezeichnete Antworten, lokaler Ersatz) | Fehlerfälle des Dienstes gezielt auslösen: Zeitüberschreitung, 429, kaputte Antwort |
| Fehler-Schalter (ein Parameter, der den n-ten Schritt scheitern lässt) | Abbruch mitten im Vorgang, Wiederanlauf, Idempotenz |
| Ausführliche Ausgabe (`--verbose`, strukturiertes Log) | sehen, welche Entscheidung der Code getroffen hat |

Schalter, die Fehler auslösen oder die Uhr verstellen, sind auf Test- und Entwicklungsumgebung begrenzt. Im Prompt steht, woran das hängt.

## Belege je Runde

- Die vollständige Ausgabe des Testlaufs, mit Zahl der Tests und Fehlschlägen.
- Eine Tabelle der Beispielaufrufe: Normalfall, jeder Randfall aus dem Auftrag, jeder Fehlerfall. Zu jedem die echte Ausgabe als Datei.
- Die Messwerte mit Datensatz und Maschine.
- Für Migrationen und Importe: Zeilenzahlen vorher und nachher, Stichproben, und ein zweiter Lauf, der zeigt, dass nichts doppelt entsteht.
- Für Bibliotheken und CLIs: die Hilfe-Ausgabe und ein Beispiel aus der Doku, das der Lauf wirklich ausgeführt hat.

Der Lauf liest die Ausgaben. Ein grüner Testlauf, dessen Beispielantworten niemand angesehen hat, belegt nur die Hälfte.

## Messwerte und Schwellen

Mit dem User festlegen, immer mit Messbedingung:

| Messwert | Beispiel für eine Schwelle |
|---|---|
| Antwortzeit (Median und 95. Perzentil) mit dem Datensatz `gross` | 95. Perzentil höchstens 200 ms lokal |
| Durchsatz oder Laufzeit eines Stapels | 100.000 Zeilen in höchstens 60 Sekunden |
| Speicher | höchstens 500 MB beim Datensatz `gross` |
| Zahl der Datenbankabfragen je Anfrage | höchstens 5, keine Abfrage in einer Schleife |
| Tests | alle grün, keiner übersprungen |

Einer davon wird der Messwert im Prozess, die übrigen stehen als harte Regeln da. Lokale Zeiten sind Vergleichswerte zwischen den Runden, keine Zusage für die Produktion.

## Rolle des Kritikers

Zwei Blickwinkel, beide im Prompt:

- Ein strenger Reviewer, der den Code übernehmen und in zwei Jahren noch warten muss. Er sucht Fehlerfälle ohne Behandlung, stille Datenverluste, Wettläufe, unklare Namen und Sonderfälle, die nur für die Tests existieren.
- Der erste Nutzer, der nur die Beispielausgaben und die Hilfe sieht. Er prüft, ob eine Fehlermeldung sagt, was falsch war und was zu tun ist, und ob er die Schnittstelle ohne Rückfrage benutzen könnte.

## Harte Regeln (Auswahl für den Prompt)

- Die Lösung gilt für alle gültigen Eingaben. Tests prüfen sie, sie definieren sie nicht: keine Sonderbehandlung für Testwerte, kein Abschwächen oder Löschen bestehender Tests, um sie grün zu bekommen. Hält der Lauf einen Test für falsch, nennt er ihn im Schlussbericht.
- Jeder Fehlerfall aus dem Auftrag hat ein festgelegtes Verhalten und eine Meldung, die Ursache und nächsten Schritt nennt.
- Schreibende Vorgänge sind wiederholbar, ohne doppelte Wirkung, oder der Prompt sagt, warum das hier nicht nötig ist.
- Öffentliche Schnittstellen, die schon Nutzer haben, bleiben kompatibel. Was sich ändert, steht im Schlussbericht.
- Keine Zugangsdaten in Code, Tests, Logs oder Beispielausgaben.
- Migrationen sind umkehrbar oder der Rückweg ist beschrieben.
- Nur die lokale Entwicklungs- oder Testdatenbank. Der Prompt nennt, woran der Lauf sie erkennt.

Verbotsliste, aus der du Vorschläge machst: Fehler verschlucken und einen leeren Erfolg melden, pauschale Wiederholungen ohne Obergrenze, eine Konfigurationsoption für jeden denkbaren Fall, eine neue Abstraktion für einen einzigen Aufrufer, Tests, die nur das Mock prüfen, Meldungen wie „Etwas ist schiefgelaufen".

## Hier nicht prüfbar

| Was | Ausweichweg oder Rückgabe |
|---|---|
| Last und Datenmengen der Produktion | Datensatz `gross` erzeugen und lokal messen; die echte Größenordnung kommt in die Liste „Von mir zu prüfen" |
| Echte fremde Dienste (Zahlung, E-Mail, Schnittstellen von Partnern) | gegen Attrappe oder Testmodus bauen; ein echter Durchlauf kommt in die Liste |
| Echte Produktionsdaten mit ihren Altlasten | Randfälle aus dem Interview als Fixtures nachbauen; ein Probelauf gegen eine Kopie kommt in die Liste |
| Gleichzeitigkeit unter echtem Verkehr | gezielte Tests für die benannten Wettläufe; Beobachtung im Betrieb kommt in die Liste |
| Deployment, Infrastruktur, Rechte | nicht Teil des Laufs; kommt in die Liste |
| Sicherheit | der Lauf prüft, was im Code sichtbar ist (Eingaben, Rechte, Geheimnisse); eine Sicherheitsprüfung ersetzt das nicht |

## Typische Risiken

- **Prüfweg zuerst:** Tests starten, einen bestehenden Endpunkt oder Befehl aufrufen, die Ausgabe ablegen. Eine Testdatenbank, die nicht erreichbar ist, fällt sonst erst nach der ersten Version auf.
- **Ein Durchstich zuerst:** ein Fall vollständig vom Eingang bis zur gespeicherten Wirkung, mit Test, Beispielausgabe und Messung. Erst dann die übrigen Fälle.
- **Lange Vorgänge** (Import, Migration, Neuaufbau eines Index): erst mit hundert Zeilen, dann mit allen, und nach jedem Lauf die Zahlen prüfen, weil ein abgebrochener Vorgang einen halben Zustand hinterlässt.
- **Grün durch Anpassung:** Wird ein Test rot, sucht der Lauf zuerst den Fehler im Code. Den Test ändert er nur, wenn sich die Anforderung laut Auftrag geändert hat.
- **Die falsche Datenbank:** Vor dem ersten schreibenden Befehl prüft der Lauf, wohin die Verbindung zeigt.

## Zusatzfragen im Interview

- Bei Baustein 1: Wer ruft das auf, wie oft, mit welchen Mengen? Was ist der größte realistische Fall?
- Bei Baustein 2: Gibt es Aufrufer, die sich auf das heutige Verhalten verlassen?
- Bei Baustein 4: Welche Fehlerfälle kennst du aus dem Betrieb? Was soll in jedem geschehen? Was darf auf keinen Fall doppelt passieren, verloren gehen oder nach außen sichtbar werden?
- Bei Baustein 7: Woran merkst du im Alltag, dass es gut ist: an der Geschwindigkeit, an den Meldungen, daran, dass du nicht mehr nachsehen musst?
- Bei den Grenzen: Wogegen darf der Lauf arbeiten: welche Datenbank, welche Dienste, welche Zugangsdaten?
