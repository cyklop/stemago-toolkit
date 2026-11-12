---
name: build-brief
description: "Führt ein Interview und liefert daraus einen fertigen, für sich allein verständlichen Auftrags-Prompt, der in einer neuen Claude-Code-Session einen langen, eigenständigen Qualitätslauf auslöst: Einsatz, Referenz mit Lücken, ein Star, Messlatte, eingebaute Prüfschalter, Verbesserungsrunden mit Stoppregel. Für Web, native Apps (visionOS, iOS, macOS), Backend, CLI und Werkzeuge, im bestehenden Projekt wie im leeren Ordner. Verwende wenn der User ein Vorhaben in einem Zug auf hohem Niveau bauen lassen will und dafür den Prompt braucht. Auch bei: 'Build-Brief', 'schreib mir den Prompt für einen langen Lauf', 'Auftrag für eine neue Session', 'Qualitätslauf', 'lass das über Nacht bauen'. NICHT für Spec und Tasks (dafür /interview), Befragen ohne Deliverable (dafür /grill-me), Mockups (dafür /redesign-studio) oder Wegwerf-Code (dafür /prototype). Der Skill baut selbst nichts."
argument-hint: "[vorhaben in einem satz]"
---

# Build-Brief

Aus einem Interview entsteht ein Auftrags-Prompt. Der User fügt ihn in eine neue Claude-Code-Session ein. Dort baut ein langer Lauf ohne Rückfragen, sieht sich sein Ergebnis selbst an, verbessert es über mehrere Runden und endet mit einem kurzen Bericht.

Die Qualität solcher Läufe entsteht in den Verbesserungsrunden. Die Runden wirken nur, wenn der Lauf sein Ergebnis wirklich zu sehen bekommt und weiß, woran es gemessen wird. Das Interview klärt deshalb vor allem zwei Dinge: was genau exzellent sein muss, und wie der Lauf das selbst prüfen kann.

In diesem Skill baust du nichts. Dein Ergebnis ist der Prompt.

## Dateien

| Was | Wo |
|---|---|
| Interview-Capture | `brainstorms/{YYYY-MM-DD}-brief-{slug}.md` |
| Fertiger Prompt | `docs/briefs/{YYYY-MM-DD}-{slug}.md` |
| Fragen, Laufgrößen, Grenzen, Formulierungsregeln, Abnahme | `${CLAUDE_SKILL_DIR}/REFERENCE.md` |
| Gerüst des Prompts | `${CLAUDE_SKILL_DIR}/prompt-template.md` |
| Plattform-Profile | `${CLAUDE_SKILL_DIR}/profiles/web.md`, `apple.md`, `backend.md`, `general.md` |

`{slug}`: zwei bis vier Wörter aus dem Vorhaben in kebab-case, Umlaute ausgeschrieben (`ae`, `oe`, `ue`, `ss`), ohne Füllwörter. Du legst ihn vor der ersten Frage fest und änderst ihn nicht mehr. Derselbe Slug steht im Namen der Laufnotiz und des Belege-Ordners. Der Branch-Name ist davon unabhängig. Das Datum kommt von `date +%F`. Fehlende Ordner legst du an.

## Die zehn Bausteine

Jeder fertige Prompt enthält alle zehn. Fehlt einer, wird der Lauf an genau dieser Stelle beliebig.

1. **Einsatz und Publikum** im ersten Satz: wer das Ergebnis wie lange sieht, dass Qualität das Ziel ist und der Lauf sich die Zeit nehmen darf.
2. **Die Anfrage in einem Satz**, danach die **Referenz**: was es schon gibt, wie es funktioniert, wo es schwach ist, mit dem Auftrag, genau diese Lücken zu schließen.
3. **Ein Star**, dem sich alles unterordnet: ein Material, eine Kernfunktion, ein Kernmoment.
4. **Konkretion statt Adjektive**: Inhalte, Zustände, Randfälle, die schweren Stellen einzeln benannt.
5. **Markierte Freiheit**: „dein Entwurf, zum Beispiel …", „Methode: deine", wo der User nichts festlegen will.
6. **„Was exzellent sein muss"** (3 bis 6 Punkte) und eine **Verbotsliste** der Standardlösungen, die der User nicht will.
7. **Eine Messlatte** als prüfbarer Satz.
8. **Prüfbarkeit als Teil des Produkts**: Schalter, mit denen der Lauf jeden wichtigen Zustand direkt ansteuern, ansehen und wiederholen kann, samt Ausweichweg für alles, was in der Prüfumgebung nicht geht.
9. **Prozess mit erzwungener Selbstkritik und Stoppregel**: vollständige v1, dann mindestens N Runden (Belege sammeln und ansehen, als strenger Fachkritiker urteilen, die drei schwächsten Dinge benennen, beheben, erneut prüfen). Ein Messwert, der seine Schwelle verfehlt, wird behoben, bevor Neues dazukommt. Schluss nach Stoppregel oder Zeitlimit, kurzer Schlussbericht mit bekannten Mängeln.
10. **Risikohinweise mit Begründung**: wo der Lauf erfahrungsgemäß Zeit verbrennt oder still scheitert, und was er deshalb zuerst tut.

## Schritt 1: Plattform erkennen, Profil und Referenz lesen

Bestimme zuerst den Projekttyp, denn das Profil sagt dir, wonach du im Projekt suchst und was du fragst.

| Zeichen im Projekt | Profil |
|---|---|
| `package.json` mit Next.js, React, Vue, Svelte, Astro oder Vite; `composer.json` mit Contao oder Symfony und Templates; reine HTML-Ordner | `profiles/web.md` |
| `*.xcodeproj`, `*.xcworkspace`, `Package.swift` mit App-Ziel (visionOS, iOS, macOS) | `profiles/apple.md` |
| API, Service, Worker, CLI, Bibliothek, Migration: alles ohne eigene Oberfläche | `profiles/backend.md` |
| Alles andere (`*.sln` und `*.csproj` für .NET-Desktop, Dokumente, Datenauswertung, Hardware) und der leere Ordner, bis die Plattform feststeht | `profiles/general.md` |

Im leeren Ordner ist die Plattform die erste Frage an den User. Berührt das Vorhaben zwei Profile (ein Web-Feature mit neuer API), bestimmt das Profil, in dem der Star liegt, die Belege. Aus dem zweiten übernimmst du Messwerte und die Liste dessen, was sich nicht prüfen lässt.

Lies jetzt vollständig: das Profil, `REFERENCE.md` und `prompt-template.md`. Du brauchst alle drei vor der ersten Frage, weil das Profil auch Stoff für die frühen Bausteine enthält (Zusatzfragen, Verbotsliste, Risiken) und das Gerüst zeigt, wofür du fragst.

Jedes Profil beantwortet vier Fragen: wie der Lauf sein Ergebnis zu sehen bekommt, welche Schalter für Zustände sinnvoll sind, welche Rolle der Kritiker hat, und was sich in dieser Umgebung nicht prüfen lässt. Zu jedem Punkt, der sich nicht prüfen lässt, braucht der Prompt einen Ausweichweg oder einen Eintrag in der Liste, die der Lauf im Schlussbericht an den User zurückgibt.

## Schritt 2: Kontext lesen, bevor du fragst

Lies im Arbeitsverzeichnis, was das Projekt über sich selbst sagt. Was dort steht, fragst du nicht ab.

- **Anweisungen:** `CLAUDE.md`, `AGENTS.md`, `CONTEXT.md`, der Anfang der `README.md`.
- **Stack und Befehle:** die Projektdateien des Typs (`package.json` mit Skripten und Werkzeugen, `composer.json`, `project.pbxproj`, `pyproject.toml`, `go.mod`, `Cargo.toml`).
- **Stand:** `git status`, aktueller Branch, ob es ein Remote gibt, was in der `.gitignore` steht. Daraus leitest du den Vorschlag für die Grenzen ab.
- **Das Vorhaben selbst:** `$ARGUMENTS`, eine passende Spec (unter `docs/specs/` oder wo das Projekt Specs ablegt), ein Capture unter `brainstorms/`. Betrifft das Vorhaben etwas Bestehendes, lies den Code oder die Ansicht dazu. Du brauchst das für die Referenz: Wie es heute funktioniert und wo es schwach ist, schlägst du vor, statt blank danach zu fragen.
- **Prüfwerkzeuge:** was das Profil unter „So sieht der Lauf sein Ergebnis" und „Vor dem Interview auslesen" nennt.

In diesem Schritt liest du nur. Lesende Abfragen (Versionen, Listen, `git status`) sind in Ordnung. Du baust nichts, startest nichts und installierst nichts.

Drei Fälle, die dabei auftreten:

- **Die `CLAUDE.md` passt nicht zur Umgebung** (ein Befehl nennt eine Version, die nicht installiert ist, oder eine Datei, die es nicht gibt). Sag es dem User und schreib die gültige Angabe in den Prompt. Biete an, dass der Lauf die `CLAUDE.md` korrigiert oder die Stelle im Schlussbericht nennt. Der User entscheidet.
- **Das Vorhaben setzt etwas voraus, das es nicht gibt** (eine Seite, auf die verlinkt werden soll, ein Datenfeld). Frag im Interview, ob es zum Auftrag gehört.
- **Code und Beschreibung widersprechen sich.** Für die Referenz gilt der Code. Nenn dem User den Widerspruch.

Stack, Konventionen und Befehle aus der `CLAUDE.md` wiederholst du im Prompt nicht. Die neue Session lädt die Datei selbst, ein Verweis genügt. Ausgeschrieben wird nur, woran eine Grenze oder der Prüfweg hängt (Kennung der lokalen Datenbank, Port, Kennung des Simulators) und was von der `CLAUDE.md` abweicht.

Fasse in drei bis fünf Zeilen zusammen, was du erkannt hast: Projekttyp, Profil, was schon geregelt ist, was dir aufgefallen ist. Dann beginnt das Interview.

## Schritt 3: Interview

**Vor der ersten Frage** legst du die Capture-Datei an (Aufbau in `REFERENCE.md`, Abschnitt „Capture-Datei") und nennst dem User den Pfad in einer Zeile. Du schreibst nach jedem Baustein hinein, bevor der nächste beginnt, und sofort nach jeder Antwort auf eine Nachfrage. Die Datei ist die Quelle der Wahrheit, nicht dein Kontext: Geht er mitten im Gespräch verloren, steht dort alles bisher Gesagte.

So führst du das Gespräch:

- **Eine Frage nach der anderen.** Zu jeder Frage gehört dein Vorschlag aus dem Kontext, auf den der User mit „passt", einer Korrektur oder einer Richtung antworten kann. Ein leeres „Was soll exzellent sein?" liefert Adjektive. Ein Vorschlag mit drei konkreten Punkten liefert Widerspruch, und der ist brauchbar.
- **Wo der Kontext schweigt, fragst du offen.** Publikum, Anlass, Erfahrungen mit dem echten Gerät oder dem echten Betrieb stehen in keiner Datei. Ein geratener Vorschlag lenkt dort nur ab.
- **Adjektive sind keine Antwort.** Bei „modern", „hochwertig", „schnell", „intuitiv", „robust", „clean" fragst du nach, bis etwas dasteht, das ein Fremder an einem Beleg prüfen kann: eine Zahl mit Messbedingung, ein Zustand, ein Vergleich, ein Gegenbeispiel. Die Nachhak-Fragen stehen in `REFERENCE.md`.
- **Die schweren Stellen einzeln.** Frag, woran ein Durchschnittsergebnis sofort zu erkennen wäre, und lass dir zu jeder dieser Stellen sagen, was stattdessen da sein muss.
- **Freiheit ausdrücklich abfragen.** Wo der User nichts festlegen will, schreibst du das als Freiheit in den Prompt. Sonst rät der Lauf, ob ein Detail Vorgabe oder Beispiel war.
- **Was der User nicht weiß,** hältst du als offenen Punkt fest und machst weiter. Vor der Rückspiegelung entscheidet ihr, ob er als Freiheit oder als Annahme in den Prompt kommt.

Die Reihenfolge:

1. Bausteine 1 bis 7, einer nach dem anderen. Die Zusatzfragen des Profils stellst du bei dem Baustein, den das Profil nennt.
2. **Prüfbarkeit (Baustein 8).** Du schlägst aus dem Profil die Schalter und die Belege vor und nennst offen, was sich in dieser Umgebung nicht prüfen lässt. Der User ergänzt, welche Zustände ihm wichtig sind.
3. **Harte Regeln.** Du schlägst die Auswahl aus dem Profil vor, die zum Vorhaben passt, jede mit ihrem Grund. Der User streicht und ergänzt.
4. **Risiken (Baustein 10).**
5. **Laufgröße (Baustein 9).** Mindestzahl der Runden, Zeitlimit, Messwert mit Schwelle. Nenn dabei die Kostenspanne aus `REFERENCE.md`, Abschnitt „Laufgröße", und schlag für kleine Vorhaben die kleine Stufe vor. Prüf, ob der Umfang aus den Bausteinen 4 und 8 zum Zeitlimit passt, und sag es, wenn nicht. Die Kosten sind eine Information für den User. In den Prompt gehören nur Runden und Zeitlimit.
6. **Grenzen.** Erlaubte Pfade, Hilfsdateien des Laufs, Branch, Commit, Push, Abhängigkeiten, Datenbank und alles, was nicht angefasst wird. Dazu die Frage, ob der Lauf bestehenden Code umbauen darf oder so wenig wie möglich ändern soll. Die Einzelfragen stehen in `REFERENCE.md`, Abschnitt „Grenzen".

Schalter, harte Regeln, die Liste „nicht prüfbar" und die Grenzen sind Vorschlagslisten. Zeig sie als Text oder Tabelle und lass sie korrigieren. **AskUserQuestion** nimmst du für die echten Entweder-oder-Fragen: die Stufe der Laufgröße, Umbauen oder wenig ändern, Push ja oder nein.

**Rückspiegelung.** Zum Schluss spiegelst du das Ergebnis zurück und lässt es bestätigen: eine Zeile je Baustein, dazu je eine für die harten Regeln und die Grenzen. Darunter steht eine eigene Liste „Von mir gesetzt": jede Zahl, jeder Testdatensatz, jede Schwelle und jeder prüfbare Anker, den du vorgeschlagen hast und den der User nur abgenickt hat. Diese Liste soll er wirklich lesen, denn an ihr hängt, was der Lauf später für seine Vorgabe hält. Erst nach der Bestätigung schreibst du den Prompt.

## Schritt 4: Prompt schreiben

Bau den Prompt nach `prompt-template.md` und setz die Textbausteine des Profils ein. Die Formulierungsregeln stehen in `REFERENCE.md`, Abschnitt „Formulierungsregeln". Sie folgen dem Prompting-Guide von Anthropic für das Modell des Laufs. Das ist ohne andere Angabe das Modell dieser Session. Nennt der User ein anderes, gilt der Abgleich, den `REFERENCE.md` dort beschreibt, bevor du schreibst. Die wichtigsten Regeln:

- **Für sich allein verständlich.** Der Prompt erwähnt weder das Interview noch diesen Skill noch die Capture-Datei. Wer nur den Prompt und das Repository hat, kann loslegen.
- **Schlichte, kurze Sätze, jede Regel mit ihrem Grund.** Aus dem Grund kann der Lauf auf Fälle schließen, die du nicht vorhergesehen hast.
- **Grenzen mit Geltungsbereich statt „nie".** Das Modell nimmt „nie" wörtlich und absolut. Schreib, was gilt, wo es gilt und was der Lauf stattdessen tut.
- **Was ohne Rückfrage erlaubt ist, steht ausdrücklich da.** Niemand sitzt daneben. Ein Lauf, der auf eine Freigabe wartet, steht.
- **Keine Kosten und kein Token-Budget im Prompt,** keine Anweisung zum Delegieren, keine Aufforderung, Gedankengänge auszuschreiben.
- **Jede Aussage steht einmal da.** Die Lückenliste sagt, was heute falsch ist. Die Konkretion sagt, wie es genau sein soll. „Was exzellent sein muss" sagt, woran man es am Beleg erkennt. Wiederholt ein Abschnitt den vorigen, kürze ihn.
- **Sprache:** die des Interviews, außer der User will den Prompt auf Englisch.

Brauchst du beim Schreiben einen prüfbaren Anker, den der User nicht bestätigt hat (eine Größe, eine Toleranz, einen Kontrastwert), kennzeichnest du ihn im Prompt als Annahme, die der Lauf übernehmen oder mit Grund ändern darf, und nimmst ihn in die Liste „Von mir gesetzt" auf.

Der Prompt ist so lang, wie die Konkretion es braucht. Fülltext macht ihn schlechter. Fehlende Einzelheiten an den schweren Stellen auch.

## Schritt 5: Gegenlesen

Lies den fertigen Prompt so, wie die neue Session ihn liest: ohne dieses Gespräch. Geh die Abnahmeliste in `REFERENCE.md`, Abschnitt „Abnahme", Punkt für Punkt durch und behebe, was fehlt. Die häufigsten Mängel:

- Ein Adjektiv ohne prüfbaren Anker ist stehen geblieben.
- Ein Schalter wird verlangt, aber es steht nicht da, welche Zustände er erreichen muss.
- Etwas lässt sich in der Prüfumgebung nicht beurteilen, und der Prompt tut so, als ginge es.
- Die erlaubten Pfade schließen aus, was der Lauf sicher braucht: seine Laufnotiz, den Belege-Ordner, die Stelle, an der die Schalter eingehängt werden.
- Der Umfang passt nicht in das Zeitlimit. Dann kürzt du mit dem User den Umfang oder hebst die Stufe.

## Schritt 6: Ablegen und übergeben

1. Schreib den Prompt nach `docs/briefs/{YYYY-MM-DD}-{slug}.md`. Die Datei enthält nur den Prompt, ohne Vorspann, damit der User sie ganz kopieren oder der neuen Session als Datei nennen kann.
2. Gib den Prompt zusätzlich als Codeblock aus. Der Prompt enthält selbst Backticks, deshalb bekommt der äußere Block vier Backticks.
3. Trag in der Capture-Datei ein, wo der Prompt liegt, welche Laufgröße vereinbart ist und was unter „Von mir gesetzt" steht.
4. Gib den Start-Hinweis:

   ```
   cd <projektordner>
   claude --model fable --effort high --permission-mode auto
   ```

   Danach den Prompt einfügen oder der Session die Datei nennen. Dazu sagst du dem User sinngemäß:

   - Der Lauf braucht eine neue Session im Projektordner, weil nur sie die `CLAUDE.md`, die Einstellungen und die Werkzeuge des Projekts lädt.
   - `high` ist die Stufe, die der Prompting-Guide für lange, unbeaufsichtigte Läufe nennt. Ohne die Angabe startet Claude Code mit `medium`. Eine höhere Stufe lohnt nur, wenn er den Gewinn gemessen hat.
   - Im Auto-Modus führt die Session Befehle im Projekt ohne Rückfrage aus. Im manuellen Modus wartet sie beim ersten Shell-Befehl.
   - Was er erwarten darf: die vereinbarte Dauer und die Kostenspanne. Er soll den Lauf nach der ersten Version nicht anhalten, weil die Verbesserungsrunden der eigentliche Zweck sind.
   - Was der Lauf im Projekt anlegt: Branch, Laufnotiz, Belege-Ordner, gegebenenfalls eine Zeile in der `.gitignore`.
   - Die Liste „Von mir gesetzt" noch einmal, mit der Bitte, sie vor dem Start zu lesen.

Committe Prompt und Capture nur, wenn der User das möchte. Bleiben sie unversioniert liegen, nimmt der Lauf sie nicht in seine Commits auf. Das Gerüst enthält dafür einen festen Satz.

Pflege: Modellname, Effort-Stufe und Schalter im Startbefehl stammen vom 12.11.2026 (Claude Fable 5.2, Claude Code mit Auto-Modus). Weicht die lokale Installation ab (`claude --help`), gilt sie.
