# Build-Brief — Reference

Einzelheiten zum `/build-brief`-Skill: Fragen und Nachhak-Muster je Baustein, harte Regeln, Laufgröße, Grenzen, Formulierungsregeln, Abnahme, Aufbau der Capture-Datei.

---

## Bausteine: Frage, Vorschlag, Nachhaken

Die Beispiele zeigen die Form. Übernimm sie nicht wörtlich: Jeder Prompt bekommt seine eigenen Inhalte aus dem Interview.

### 1. Einsatz und Publikum

- **Frage:** Wer sieht oder benutzt das Ergebnis zuerst, in welcher Lage und wie lange? Was passiert, wenn es nur durchschnittlich ist?
- **Vorschlag aus:** Zweck des Projekts in der `CLAUDE.md`, Art des Vorhabens.
- **Nachhaken:** „Die Nutzer" ist kein Publikum. Frag nach der einen Person und dem einen Moment: der Kunde in der Abnahme, die Sachbearbeiterin beim zweihundertsten Vorgang des Tages, der Entwickler, der die API zum ersten Mal aufruft.
- **Im Prompt:** ein bis drei Sätze ganz oben, in der Ich-Form des Users. Beispiel: „Ich zeige das Ergebnis am Donnerstag dem Kunden, zehn Minuten am Beamer, und er entscheidet danach über die zweite Phase. Qualität ist das Ziel. Nimm dir die Zeit, die sie braucht."

### 2. Anfrage und Referenz

- **Frage:** Was ist die Anfrage in einem Satz? Was gibt es schon, das dem am nächsten kommt: im eigenen Projekt, beim Wettbewerb, in einem früheren Versuch? Wie funktioniert es, und wo ist es schwach?
- **Vorschlag aus:** dem bestehenden Code oder der bestehenden Ansicht. Lies sie vorher und nenn zwei oder drei Schwächen, die du siehst.
- **Nachhaken:** Eine Referenz ohne benannte Schwäche ist nur ein Vorbild. Frag: „Was daran würdest du nicht noch einmal so bauen?" Gibt es keine Referenz, frag nach dem Gegenteil: „Woran würdest du die Standardlösung erkennen?"
- **Im Prompt:** die Anfrage, dann die Referenz mit ihrer Funktionsweise, dann der Satz „Schließe genau diese Lücken:" mit einer einzigen Liste der Form „Schwäche → was stattdessen da sein muss". Eine eigene Schwächenliste davor sagt dasselbe zweimal.

### 3. Der Star

- **Frage:** Wenn nur eine Sache herausragend werden kann, welche? Was darf dafür schlicht bleiben?
- **Vorschlag aus:** der Stelle, an der das Vorhaben sich von der Standardlösung unterscheidet.
- **Nachhaken:** Nennt der User drei Dinge, frag, welches er zeigt, wenn er nur dreißig Sekunden hat. Der Star ist ein Ding: eine Kernfunktion (die Suche, die beim Tippen schon das Richtige zeigt), ein Kernmoment (der Augenblick, in dem die Auswertung erscheint), ein Material oder eine Darstellung.
- **Im Prompt:** „Der Star ist …. Alles andere ordnet sich ihm unter:" und dazu, was das für den Rest heißt (zurückhaltende Farben, keine zweite Animation, einfache Nebenansichten).

### 4. Konkretion

- **Frage:** Welche Inhalte stehen wirklich da (echte Texte, echte Datensätze, echte Größenordnungen)? Welche Zustände gibt es: leer, lädt, Fehler, voll, zu viel, zu lang, ohne Rechte, offline? Welche Randfälle kennst du aus der Praxis? Welche Stellen sind schwer?
- **Vorschlag aus:** Datenmodell, vorhandenen Ansichten, Testfällen.
- **Nachhaken:** siehe „Adjektive auflösen". Für jede schwere Stelle fragst du nach dem falschen Freund, also der billigen Lösung, die der Lauf nicht abliefern soll, und schreibst sie als Satz der Form „X ist kein Y" in den Prompt. Beispiele: „Ein Spinner über der ganzen Seite ist kein Ladezustand." „Eine Liste mit Zeitstempeln ist kein Verlauf, den man lesen kann." „Ein Fehlertext ‚Etwas ist schiefgelaufen' ist keine Fehlermeldung."
- **Im Prompt:** der längste Teil. Absätze nach Thema, mit den Inhalten und Zuständen im Klartext.

### 5. Markierte Freiheit

- **Frage:** Wo willst du nichts festlegen? Wo ist dein Beispiel nur ein Beispiel?
- **Vorschlag aus:** allem, was der User im Gespräch mit „irgendwie" oder „zum Beispiel" beantwortet hat.
- **Nachhaken:** Frag bei jedem Detail aus Baustein 4, das der User nebenbei genannt hat: Vorgabe oder Beispiel?
- **Im Prompt:** ausdrücklich markieren. „Der Ablauf ist dein Entwurf, zum Beispiel: …" „Methode: deine. Bewährt hat sich …" „Die Namen sind Platzhalter, wähl bessere."

### 6. Was exzellent sein muss, und die Verbotsliste

- **Frage:** Welche drei bis sechs Dinge müssen herausragend sein, damit du das Ergebnis herzeigst? Und welche Standardlösungen willst du nicht sehen?
- **Vorschlag aus:** Star, schweren Stellen und den Schwächen der Referenz. Für die Verbotsliste: die naheliegenden Muster der Plattform (das Profil nennt einige).
- **Nachhaken:** Mehr als sechs Punkte sind eine Wunschliste. Lass streichen. Jedes Verbot bekommt in Stichworten seinen Grund, sonst verbietet es zu viel oder zu wenig.
- **Im Prompt:** „Was exzellent sein muss:" als Liste, jeder Punkt mit dem Detail, an dem man es erkennt. „Nicht gewollt:" als Liste mit Grund.

### 7. Messlatte

- **Frage:** Welcher eine Satz entscheidet am Ende, ob es gelungen ist, und zwar so, dass ein Fremder ihn an einem Beleg prüfen kann?
- **Vorschlag aus:** Publikum und Star. Zwei Teile haben sich bewährt: ein Standbild oder Einzelergebnis, das einem Vergleich standhält, und ein Moment, den man gern zweimal zeigt.
- **Nachhaken:** „Es soll professionell wirken" ist keine Messlatte. Prüfbar ist: „Ein Screenshot der Übersicht geht in der Kundenpräsentation als fertiges Produkt durch, und die Suche findet den Vorgang, bevor ich das dritte Zeichen getippt habe."
- **Ein Teil ist nur am echten Gerät oder im echten Betrieb prüfbar:** Das kommt vor (zum Beispiel „eine Testperson macht die ersten fünf Schritte richtig"). Dann teilst du die Messlatte. Den Teil, den der Lauf an einem Beleg prüfen kann, misst der Kritiker. Der andere Teil steht als erster Eintrag in der Liste, die der Lauf zurückgibt, und der Prompt sagt das ausdrücklich. Ohne belegbaren Teil ist die Messlatte nicht fertig.
- **Im Prompt:** ein Absatz „Messlatte:", am Ende des Auftragsteils.

### 8. Prüfbarkeit

- **Frage:** Welche Zustände und Momente muss der Lauf gezielt ansteuern können, um sie zu beurteilen? Was davon ist ohne Schalter nur mühsam oder zufällig zu erreichen?
- **Vorschlag aus:** dem Profil (Schalter, Belege) und den Zuständen aus Baustein 4.
- **Nachhaken:** Geh die Liste „Hier nicht prüfbar" des Profils mit dem User durch. Zu jedem Punkt, der das Vorhaben trifft, entscheidet ihr: Ausweichweg (ein zweiter Bedienweg, ein Testdatensatz, ein Messskript) oder Eintrag in die Liste, die der Lauf an den User zurückgibt.
- **Im Prompt:** eigener Abschnitt. Die Schalter sind Teil des Produkts und werden mitgebaut, mit Namen, erreichbaren Zuständen und der Regel, wo sie abgeschaltet sind (zum Beispiel nur im Debug-Build).

### 9. Prozess und Stoppregel

- **Frage:** siehe „Laufgröße".
- **Im Prompt:** der Prozessblock aus `prompt-template.md` mit Rundenzahl, Zeitlimit, Belegen und Kritikerrolle aus dem Profil. Die Stoppregel hat zwei Teile: „wenn eine weitere Runde am Ergebnis nicht mehr auffiele" und das Zeitlimit. Das Zeitlimit geht vor: Ist es erreicht, schließt der Lauf die laufende Runde ab und berichtet, auch wenn die Mindestzahl der Runden nicht voll ist. Der Satz „Nimm dir die Zeit" im ersten Absatz widerspricht dem nicht. Er sagt, dass der Lauf nicht nach der ersten Version aufhören soll. Das Limit ist die Obergrenze.

### 10. Risiken

- **Frage:** Wo ist so etwas schon einmal schiefgegangen? Welcher Schritt dauert lange oder kann abbrechen? Wo wäre es teuer, erst am Ende zu merken, dass der Ansatz nicht trägt?
- **Vorschlag aus:** dem Abschnitt „Typische Risiken" des Profils.
- **Nachhaken:** Jeder Hinweis braucht seinen Grund und die Handlung, die daraus folgt. „Vorsicht bei der Migration" hilft nicht. „Leg die Migration zuerst auf einer Kopie der Entwicklungsdatenbank an und prüf die Zeilenzahlen, weil ein Fehler im Mapping sonst erst in der Auswertung auffällt" hilft.
- **Im Prompt:** zwei bis vier Hinweise. Fast immer dabei: „Bring zuerst einen kleinen Ausschnitt auf Zielqualität und bau erst dann den Rest, weil du sonst die ganze Fläche mit einem Ansatz füllst, der die Messlatte nicht erreicht." Und: „Prüfe den Prüfweg zuerst", siehe Profil.

---

## Adjektive auflösen

| Der User sagt | Du fragst |
|---|---|
| modern, zeitgemäß | Nenn mir ein Produkt, das es trifft, und eines, das es verfehlt. Was genau ist der Unterschied auf einem Screenshot? |
| hochwertig, professionell, edel | Welche drei Details würde ein Fachmann als Erstes prüfen? Was wäre das Erkennungszeichen von billig? |
| schnell, flüssig | Welche Zahl, gemessen woran und unter welcher Bedingung (Datenmenge, Gerät, Netz)? |
| intuitiv, einfach | Wer schafft was in wie vielen Sekunden, ohne Erklärung, beim ersten Mal? |
| robust, stabil | Welche Fehlerfälle müssen ohne Datenverlust durchlaufen? Was darf bei welchem Fehler passieren? |
| clean, aufgeräumt | Was darf auf der Ansicht nicht mehr stehen? Wie viele Dinge sieht man auf einen Blick? |
| flexibel, erweiterbar | Welche eine Erweiterung kommt sicher? Alles andere bleibt draußen. |
| schön, ansprechend | Welches Bild, welches Material, welche Stimmung? Was wäre das Gegenteil? |

Ein Adjektiv ist aufgelöst, wenn ein Fremder an einem Screenshot, einer Ausgabe oder einem Messwert entscheiden kann, ob es zutrifft.

**Vergleichsprodukte:** Nennt der User Produkte als Maßstab, dürfen sie einmal im Prompt stehen. Der Lauf hat sie beim Urteilen aber nicht vor sich. Frag deshalb nach, was genau an ihnen gemeint ist, und schreib das als eigene Anker dazu (Zeilen je Bildschirm, was sich beim Tippen bewegen darf, welche Tasten genügen).

**Weiche Reste:** Auch eine Antwort auf Nachfrage enthält oft noch weiche Wörter („etwas heller", „leise", „schmal"). Frag noch einmal, oder setz selbst einen Anker und führ ihn in der Liste „Von mir gesetzt". Im Prompt steht er dann als Annahme, die der Lauf mit Grund ändern darf.

---

## Harte Regeln und die drei Listen

Die harten Regeln sind kein eigener Baustein, aber ein eigener Schritt im Interview: Du schlägst aus dem Profil die Regeln vor, die das Vorhaben treffen, jede mit Grund, und der User streicht und ergänzt. Findest du für eine Regel keinen Grund, der in diesem Vorhaben gilt, lass sie weg.

Verlangt eine Regel des Profils etwas, das das bestehende Produkt heute anders macht (ein Abstand, eine Geschwindigkeit, eine fehlende Abfrage), gilt sie für das Neue. Für den Bestand schreibst du „nicht schlechter als heute" und nennst den heutigen Wert.

Der Prompt hat drei Listen, die leicht verschwimmen. So grenzt du sie ab:

| Liste | Enthält | Beispiel |
|---|---|---|
| „Nicht gewollt" (Baustein 6) | Lösungen, die der User nicht sehen will: Geschmack und Gestaltung | „Blättern mit Seitenzahlen" |
| „Harte Regeln" | Qualität, die für jedes Ergebnis gilt, gleich wie es gestaltet ist | „Keine Fehler in der Konsole" |
| „Nicht anfassen" | Befugnis: was der Lauf nicht ändern oder auslösen darf | „Kein Push" |

Ein Punkt steht in genau einer Liste. Zustände und Inhalte, die schon in der Konkretion stehen, wiederholt keine der drei.

---

## Laufgröße

Die Werte stammen aus 13 dokumentierten Läufen auf Claude Fable 5.2 (Web-Demos, hohe Effort-Stufe): 45 bis 210 Minuten, 4 bis 8 Verbesserungsrunden, 11 bis 103 US-Dollar je Lauf zu API-Preisen. Die Stufe „klein" lag in diesen Läufen nicht vor und ist geschätzt.

| Stufe | Passt zu | Runden (mindestens) | Zeitlimit | Kosten zu API-Preisen |
|---|---|---|---|---|
| klein | eine Komponente, ein Endpunkt, ein CLI-Befehl, eine einzelne Ansicht | 2 bis 3 | 30 bis 45 Minuten | geschätzt 5 bis 15 US-Dollar |
| mittel | ein Feature mit mehreren Zuständen, eine Seite | 4 | 45 bis 60 Minuten | 10 bis 20 US-Dollar (zwei Läufe, beide rund 14) |
| groß | eine Kernfunktion mit eigener Technik, ein Bereich mit mehreren Ansichten | 6 | 90 bis 150 Minuten | 11 bis 38 US-Dollar (zehn Läufe) |
| sehr groß | ein ganzes Produkt mit vielen Systemen | 8 | 210 Minuten | rund 100 US-Dollar (ein Lauf: 103) |

**Welche Stufe:** Passt ein Vorhaben auf zwei Stufen, entscheidet, wie viel der Lauf erst finden muss. Ein Feature aus bekannten Teilen ist „mittel", auch mit vielen Zuständen. Braucht der Star eine eigene Technik, die erst gefunden und gemessen werden muss (eine Suche mit Rangfolge, ein Renderverfahren, eine Zeitsteuerung), ist es „groß".

**Langsame Prüfwege:** Die Zeiten stammen aus dem Web, wo ein Beleg Sekunden kostet. Kostet eine Runde durch Build, Installation und Tests mehrere Minuten Wartezeit (native Apps, große Testsuiten), rechnest du je Runde 5 bis 10 Minuten dazu und nennst dem User das höhere Zeitlimit. Das ist eine Schätzung aus gemessenen Build- und Testzeiten, keine Erfahrung aus solchen Läufen.

**Umfang gegen Zeit:** Zähl, was die erste Version enthalten muss (Funktionen, Zustände, Schalter, Testdaten) und wie viele Belege jede Runde verlangt. Passt das nicht in das Limit, greift die Uhr vor der letzten Runde, und die Runden waren der Zweck. Dann kürzt ihr den Umfang, oder die Stufe steigt. Die Belege je Runde wachsen nicht mit der Zahl der Zustände: Bei knapper Zeit verlangt der Prompt in jeder Runde die Zustände, an denen der Star hängt, und die volle Abdeckung nur nach der ersten Version und in der letzten Runde.

So nennst du es dem User: Stufe vorschlagen, Spanne dazu, und der Hinweis, dass die Zahlen von Web-Demos stammen und sein Lauf abweichen wird. Auf einem Abo zählt der Lauf gegen das Nutzungslimit statt gegen eine Rechnung. Für kleine Vorhaben schlägst du die kleine Stufe vor. Sechs Runden an einem einzelnen Endpunkt verbrennen Zeit, ohne dass das Ergebnis besser wird.

**Messwert und Schwelle:** Frag nach dem einen Wert, an dem sich entscheidet, ob weitergebaut wird, mit Schwelle, Richtung („mindestens" oder „höchstens") und Messbedingung. Das Profil nennt die üblichen. Im Prompt steht die Regel: Verfehlt der Wert seine Schwelle, wird das behoben, bevor Neues dazukommt. Die übrigen Messwerte des Profils, die das Vorhaben treffen, stehen als harte Regeln da und im Schlussbericht neben ihrer Schwelle.

**In den Prompt gehören Runden, Zeitlimit und Schwelle. Die Kosten nicht.** Laut Prompting-Guide verändert ein Budget, das dem Modell gezeigt wird, wie viel es ausgibt.

---

## Grenzen

Zeig diese Punkte als Tabelle mit deinem Vorschlag aus dem Kontext und lass den User korrigieren. Gleiche danach die erlaubten Pfade mit dem ab, was der Lauf sicher braucht (Zeilen „Hilfsdateien" und „Einhängepunkte"). Im Prompt steht jede Grenze mit Geltungsbereich, Grund und dem, was der Lauf stattdessen tut.

| Punkt | Frage | Üblicher Vorschlag |
|---|---|---|
| Pfade | Wo darf der Lauf schreiben, was fasst er nicht an? | das Projekt, ausgenommen benannte Ordner (Produktivkonfiguration, fremde Module, generierter Code) |
| Hilfsdateien des Laufs | Darf der Lauf anlegen, was er für Notiz und Prüfweg braucht? | ja: Laufnotiz unter `docs/briefs/`, Belege unter `tmp/brief-{slug}/` mit einer Zeile in der `.gitignore`, dazu je nach Profil Paketdateien mit Lock-Datei, Testkonfiguration, Browser für die Prüfung |
| Einhängepunkte | Liegen die Stellen, an denen Schalter und Testdaten eingehängt werden, in den erlaubten Pfaden? | Einstiegspunkt der App, Wurzel-View oder Layout, Seed-Skript. Liegt einer außerhalb, vereinbart ihr diese eine Datei als Ausnahme oder einen Ausweichort |
| `CLAUDE.md` | Darf der Lauf sie korrigieren, wenn sie nach seiner Arbeit nicht mehr stimmt? | nein, er nennt die Stellen mit Vorschlag im Schlussbericht |
| Branch | Auf welchem Branch arbeitet er? | neuer Branch `brief/{slug}` vom aktuellen Stand |
| Commit | Darf er committen, wie oft? | ja, nach der v1 und nach jeder Runde, damit jeder Stand zurückholbar ist |
| Push, PR, Deploy | Darf er pushen oder einen PR öffnen? | nein, der User sieht sich das Ergebnis erst an |
| Abhängigkeiten | Darf er Pakete im Projekt hinzufügen? | ja, wenn er im Schlussbericht jede neue Abhängigkeit mit Grund nennt; nichts global |
| Daten | Welche Datenbank, welche Dienste? | nur die lokale Entwicklungsdatenbank und Testdaten; Migrationen anlegen, aber nur lokal anwenden |
| Bestehender Code | Umbauen oder so wenig wie möglich ändern? | siehe unten |
| Prüfschalter | Bleiben sie im Produkt? | ja, aber nur im Entwicklungs- oder Debug-Build aktiv |
| Belege | Wohin mit Screenshots und Messprotokollen? | der Belege-Ordner aus „Hilfsdateien"; er steht in der `.gitignore` und wird nicht committet; die Belege der letzten Runde bleiben liegen |
| Daten der Prüfläufe | Schreiben Starts über Prüfschalter echte Stände (Fortschritt, Verlauf, Statistik)? | nein, ein Start über einen Prüfschalter speichert nichts Dauerhaftes |

**Bestehender Code:** Der Prompting-Guide für Fable 5.2 beschreibt, dass das Modell stark darauf achtet, wem der Code gehört. Ohne Angabe baut es eher an, auch wenn dabei Doppelungen entstehen. Mit dem Satz „Du bist Eigentümer und langfristiger Maintainer dieser Codebasis, ihr Aufbau ist deine Sache" räumt es deutlich häufiger auf, ändert dann aber auch Dinge, um die niemand gebeten hat. Der Satz gehört in den Prompt, wenn der Ordner leer ist oder der User den Umbau ausdrücklich will. Im bestehenden Projekt mit engem Auftrag bleibt er weg, und der Prompt sagt stattdessen, welche Bereiche unverändert bleiben. Eine Regel wie „keine Aufräumarbeiten nebenbei" hebt den Eigentümer-Satz laut Guide nicht zuverlässig auf. Beides zusammen ergibt also keinen Mittelweg.

---

## Formulierungsregeln

Stand: Prompting-Guide für Claude Fable 5.2 und die modellübergreifenden Best Practices, gelesen am 12.11.2026.

- `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2`
- `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`

**Abgleich:** Soll der Lauf auf einem anderen Modell starten, oder ist der Stand oben älter als etwa drei Monate, hol den Guide zum Modell so, wie `/stemago-tools:prompt-audit` es in Schritt 1 beschreibt (Index `https://platform.claude.com/llms.txt`, Seite `prompting-claude-<slug>`), und gleiche die Regeln unten ab. Was die Doku nicht mehr trägt, lässt du weg.

| Regel | Was die Doku sagt | Folge für den Prompt |
|---|---|---|
| Klar und ausdrücklich | Das Modell soll wie ein fähiger neuer Kollege ohne Kontext behandelt werden. Probe: Könnte ein Kollege mit wenig Kontext dem Prompt folgen? | Der Prompt steht für sich. Schritte, bei denen die Reihenfolge zählt, sind nummeriert. |
| Grund nennen | Eine Begründung hilft dem Modell, auf andere Fälle zu schließen. | Jede Regel und jede Grenze hat einen Halbsatz Grund. |
| „nie" ist absolut | Das Modell behandelt eine Anweisung mit „never" als absolut. Besser „ask for approval before deleting files" als „never delete files". | Grenzen mit Geltungsbereich und Ersatzhandlung. |
| Freigaben benennen | „Freier handeln" ist zu vage. Die Schritte, die keine Freigabe brauchen, werden aufgezählt. Stoppbedingungen wie „beim ersten Fehler anhalten" blockieren eigenständige Arbeit. | Liste „Ohne Rückfrage erlaubt" im Prompt. Keine pauschalen Stoppbedingungen. |
| Zu Ende arbeiten | Bei langen Aufgaben endet ein Turn manchmal zu früh: mit einer Restliste, einem Angebot weiterzumachen oder an einem gewöhnlichen Hindernis. Die Doku gibt dafür einen Textbaustein. | Der Abschnitt „Durchhalten" im Gerüst: gewöhnliche Hindernisse diagnostizieren und überwinden, bewusste Sperren stehen lassen und melden. |
| Effort | `high` für lange, unbeaufsichtigte Läufe. Darüber sind die Gewinne ungleichmäßig. | Start-Hinweis mit `--effort high`. Im Prompt selbst steht dazu nichts. |
| Budget | Ein großes Token-Budget im Prompt erhöht die Ausgaben bei gleicher Leistung. | Keine Kosten, keine Token-Zahlen. Zeitlimit und Runden bleiben, weil sie die Stoppregel sind. |
| Delegieren | Stehende Anweisungen zum Delegieren erhöhen die Kosten. Das Modell delegiert von sich aus, wenn es passt. | Kein Satz, der Subagents verlangt. |
| Gedankengänge | Aufforderungen, die Überlegungen in die Antwort zu schreiben, sollen raus. | Der Kritiker benennt Befunde („die drei schwächsten Dinge"), nicht seinen Denkweg. |
| Eigentum | Siehe „Grenzen", Bestehender Code. | Eigentümer-Satz nur nach Absprache. |
| Stilregeln | Harte Stilgrenzen („höchstens 20 Wörter") machen den Text abgehackt. | Der Schlussbericht bekommt Inhalte vorgegeben, keine Zeilenzahl. |
| Schlussbericht | Wer den Bericht liest, hat die Arbeit nicht gesehen. Kernpunkte zuerst, einfache Wörter, keine erfundenen Abkürzungen. | Abschnitt „Schlussbericht" im Gerüst. |
| Stand sichern | Bei langen Läufen wird der Kontext verdichtet. Fortschrittsnotizen und Git halten den Stand. | Eine Laufnotiz je Runde und ein Commit je Runde. |
| Prüfwerkzeuge | Je länger der Lauf, desto wichtiger sind Werkzeuge, mit denen das Modell selbst prüft. | Baustein 8 und das Profil. |
| Verweis statt Kopie | Die neue Session lädt die `CLAUDE.md` selbst (Mechanik von Claude Code, keine Aussage des Guides). | Verwiesen wird auf Stack, Konventionen, Befehle. Ausgeschrieben wird, woran eine Grenze oder der Prüfweg hängt, und was von der `CLAUDE.md` abweicht. |
| Tests | Tests prüfen die Lösung, sie definieren sie nicht. Keine Sonderfälle nur für den Test, keine Tests abschwächen. | Regel im Profil `backend.md`, bei Bedarf auch in den anderen. |

---

## Abnahme

Bevor der Prompt abgelegt wird, muss jede Zeile stimmen.

**Die zehn Bausteine**

- [ ] 1 Der erste Absatz nennt Publikum, Dauer, Qualität als Ziel und die Erlaubnis, sich Zeit zu nehmen.
- [ ] 2 Die Anfrage steht in einem Satz da. Die Referenz nennt ihre Funktionsweise, und eine Liste „Schwäche → stattdessen" sagt, welche Lücken zu schließen sind.
- [ ] 3 Genau ein Star ist benannt, und es steht da, was sich ihm unterordnet.
- [ ] 4 Inhalte, Zustände und Randfälle stehen im Klartext da. Jede schwere Stelle hat ihren Satz „X ist kein Y". Kein Adjektiv steht ohne prüfbaren Anker.
- [ ] 5 Freiheit ist markiert („dein Entwurf", „zum Beispiel", „Methode: deine").
- [ ] 6 „Was exzellent sein muss" hat 3 bis 6 Punkte. Die Verbotsliste nennt Gründe.
- [ ] 7 Die Messlatte ist ein Satz, den ein Fremder an einem Beleg prüfen kann. Ein Teil, der nur am Gerät oder im Betrieb prüfbar ist, ist als solcher benannt und steht in der Rückgabeliste.
- [ ] 8 Die Schalter haben Namen und erreichbare Zustände. Für alles, was sich hier nicht prüfen lässt, gibt es einen Ausweichweg oder einen Eintrag in der Rückgabeliste.
- [ ] 9 Der Prozess nennt v1, Mindestzahl der Runden, Belege, Kritikerrolle, die drei schwächsten Dinge, Messwert mit Schwelle und Richtung, Stoppregel, Zeitlimit mit Vorrang und Schlussbericht. Der Umfang passt in das Zeitlimit.
- [ ] 10 Zwei bis vier Risikohinweise, jeder mit Grund und Handlung.

**Für sich allein verständlich**

- [ ] Kein Bezug auf das Interview, den Skill, die Capture-Datei oder „wie besprochen".
- [ ] Jeder Fachbegriff des Projekts ist beim ersten Auftreten erklärt oder steht in der `CLAUDE.md` oder `CONTEXT.md`, auf die verwiesen wird.
- [ ] Pfade, Befehle und Schalternamen sind ausgeschrieben.
- [ ] Was die `CLAUDE.md` regelt, ist verwiesen und nicht kopiert. Ausgeschrieben ist nur, woran eine Grenze oder der Prüfweg hängt. Abweichungen von ihr sind ausdrücklich genannt.

**Grenzen und Ton**

- [ ] Die harten Regeln sind mit dem User abgestimmt, jede hat ihren Grund, und keine wiederholt die Konkretion.
- [ ] Die erlaubten Pfade enthalten Laufnotiz, Belege-Ordner und die Einhängepunkte der Schalter. Der Prompt sagt, wie der Belege-Ordner aus den Commits bleibt.
- [ ] Jede Aussage steht einmal da. Lückenliste, Konkretion und „Was exzellent sein muss" sagen Verschiedenes.
- [ ] Was du selbst gesetzt hast, steht im Prompt als Annahme und in der Liste „Von mir gesetzt".
- [ ] „Ohne Rückfrage erlaubt" und „Nicht anfassen" stehen als zwei Listen da, jede Grenze mit Grund.
- [ ] Keine Kosten, kein Token-Budget, keine Anweisung zum Delegieren, keine Aufforderung, den Denkweg auszuschreiben.
- [ ] Der Eigentümer-Satz steht nur da, wenn er vereinbart ist.
- [ ] Kurze Sätze, kein Fülltext, keine Großbuchstaben-Befehle.

---

## Capture-Datei

```
# Build-Brief: {Vorhaben}
Datum: {datum} · Projekt: {ordner} · Profil: {profil}

## Erkannter Kontext
(Projekttyp, Stack, was die CLAUDE.md schon regelt, vorhandene Prüfwerkzeuge, Branch)

## Bausteine
### 1 Einsatz und Publikum
### 2 Anfrage und Referenz
### 3 Star
### 4 Konkretion
### 5 Freiheit
### 6 Exzellent / Nicht gewollt
### 7 Messlatte
### 8 Prüfbarkeit (Schalter, Belege, nicht prüfbar)
### 9 Laufgröße (Runden, Zeitlimit, Messwert und Schwelle)
### 10 Risiken

## Harte Regeln

## Grenzen

## Offene Punkte
- {Punkt} -> als Freiheit oder als Annahme in den Prompt?

## Von mir gesetzt
- {Zahl, Testdatensatz, Schwelle oder Anker, den der User nur abgenickt oder nicht gesehen hat}

## Ergebnis
Prompt: docs/briefs/{datum}-{slug}.md · Laufgröße: {stufe} · Sprache: {sprache} · Modell: {modell}
```

Unter jedem Baustein steht, was der User gesagt hat, in seinen Worten, wo die Formulierung zählt. War die erste Antwort vage, steht die Antwort auf die Nachfrage da. Was von dir stammt, bekommt den Zusatz „(Vorschlag, bestätigt)" und steht gesammelt unter „Von mir gesetzt".
