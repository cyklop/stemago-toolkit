# build-brief: zwei durchgespielte Beispiele

Der Skill `/stemago-tools:build-brief` wurde am 12.11.2026 zweimal vollständig durchgespielt. Je ein frischer Agent bekam nur den Skill-Ordner, einen Projektordner und ein Antwortblatt mit erfundenen Antworten des Users. Er führte das Interview als Protokoll, nahm die Antworten aus dem Blatt und schrieb den Prompt. Die Blätter enthalten absichtlich vage Erstantworten („es soll modern und hochwertig aussehen"), damit sich zeigt, ob der Skill nachhakt.

| Beispiel | Projekt | Profil | Dateien |
|---|---|---|---|
| Web-Feature | `web-werkbank/fixture/`: erfundenes Next.js-Projekt (Auftragsverwaltung eines Handwerksbetriebs, Next.js 15, Prisma, DaisyUI) | `web.md` | `web-werkbank/antworten.md`, `web-werkbank/brief.md` |
| Funktion der Vision-Pro-App | die echte visionOS-App des Users (nur gelesen) | `apple.md` | `visionos-fusion-halten/antworten.md`, `visionos-fusion-halten/brief.md` |

Die `brief.md` ist jeweils der erzeugte Prompt, unverändert so, wie der Durchlauf ihn abgelegt hat. Ausgeführt wurde keiner der beiden Prompts. Die Antworten sind erfunden, auch die Personen und Termine darin.

## Die zehn Bausteine in den Beispielen

| Baustein | Web-Feature | Vision-Pro-Funktion |
|---|---|---|
| 1 Einsatz und Publikum | erster Absatz: zwei Disponentinnen, 150 Suchen am Tag, Vorführung am Freitag | erster Absatz: drei Testpersonen, 5 Minuten, Entscheidung der Orthoptistin |
| 2 Anfrage und Referenz | heutige Seite mit sechs Lücken und Gegenstück | heutige Stufe 2 mit acht Schwächen und Gegenstück |
| 3 Star | die Suche („mey" → Meyer in Zeile 1) | der Puls am Ziel |
| 4 Konkretion | Suchregeln, Tastatur, Zeile, Dichte, fünf Zustände, Sätze „X ist kein Y" | Puls, Treffer/Verpasst/Geschafft, Einstieg, Gleiten, Randfälle |
| 5 Freiheit | acht markierte Entscheidungen („Methode der Suche: deine") | Form des Rings, Technik, Richtwerte mit „etwa" |
| 6 Exzellent / Nicht gewollt | vier Punkte, sieben Verbote mit Grund | fünf Punkte, sechs Verbote mit Grund |
| 7 Messlatte | Screenshot als Produktbild, drei Buchstaben bis zum Treffer | Bildfolge über einen Puls; zweiter Teil ausdrücklich nur am Gerät |
| 8 Prüfbarkeit | Seed-Szenarien, Ankerdatensätze, `?state=`, `?verzoegerung=`, Messskript, fünf Punkte „nicht prüfbar" | Startargumente `-briefState`, `-briefAuto`, `-briefTime`, `-briefProgress`, Logzeilen mit Maßen, Debug-Menü, Liste „Am Gerät zu prüfen" mit neun Schritten |
| 9 Prozess und Stoppregel | Prüfweg, v1, vier Runden, 95. Perzentil höchstens 150 ms, 60 Minuten | Prüfweg, v1, vier Runden, Tests grün und keine neue Warnung, 75 Minuten |
| 10 Risiken | Suche zuerst messen, Ausschnitt zuerst, Datenbank erkennen, alter Server | Zeitlogik zuerst herausziehen und testen, ein Zustand zuerst, langsamer Build, Simulator verdeckt Fehler |

Beide Prompts erwähnen weder das Interview noch den Skill noch die Capture-Datei und enthalten keine Kosten.

## Was die Durchläufe am Skill geändert haben

Die Agents meldeten zusammen 47 Stellen, an denen sie raten mussten. Die folgenreichsten sind in den Skill eingearbeitet, nachdem die Beispiele entstanden waren. Die Beispiele zeigen deshalb den Stand davor:

- **Reihenfolge:** Das Profil und die Referenzdateien werden jetzt vor dem Kontext und vor der ersten Frage gelesen. Die Reihenfolge der Interview-Blöcke ist ausgeschrieben.
- **Vorrang:** Erreicht der Lauf das Zeitlimit vor der Mindestzahl der Runden, geht das Zeitlimit vor. Beide Agents hatten das selbst so entschieden.
- **Harte Regeln** haben einen eigenen Schritt im Interview, einen Grund je Regel in den Profilen und eine Zeile in der Abnahme.
- **Von mir gesetzt:** Zahlen, Testdaten und Schwellen, die der Skill vorschlägt und der User nur abnickt, stehen in einer eigenen Liste, die der User vor dem Start liest.
- **Hilfsdateien und Einhängepunkte:** Die Grenzen-Tabelle fragt ab, ob Laufnotiz, Belege-Ordner und die Stellen für die Schalter in den erlaubten Pfaden liegen.
- **Doppelungen:** Das Gerüst hat nur noch eine Liste „Schwäche → stattdessen". Im visionOS-Beispiel stehen noch zwei.
- **Messwert:** richtungsneutral formuliert („verfehlt die Schwelle"), mit der Angabe, wogegen im Web gemessen wird (lokaler Produktions-Build).
- **Apple-Profil:** Schalter-Kombinationen, Aufnahme ohne Tastatur beenden, Bildrate nach der kürzesten Bewegung, Umgang mit Bestand, der eine Regel absichtlich verletzt, keine dauerhaften Daten bei Prüfstarts.

Beide Agents hielten das vereinbarte Zeitlimit für knapp gegenüber dem Umfang ihres Prompts. Der Skill prüft das jetzt im Interview und beim Gegenlesen.

## Wiederholen

Einen frischen Agent mit dem Skill-Ordner, dem Projektordner und dem Antwortblatt starten, mit der Vorgabe, das Projekt nur zu lesen und alle Dateien in einen eigenen Ausgabeordner zu schreiben. Das Ergebnis gegen `REFERENCE.md`, Abschnitt „Abnahme", prüfen.
