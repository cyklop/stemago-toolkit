# Prompt-Audit — Reference

Einzelheiten zum `/prompt-audit`-Skill: Doku abrufen, Fundmuster, Berichtsformat, Umsetzen.

---

## Doku abrufen

### Einstiegsseiten

| Zweck | Adresse |
|---|---|
| Index der Plattform-Doku (eine Zeile je Seite, Titel und Adresse) | `https://platform.claude.com/llms.txt` |
| Prompting-Guide je Modell | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-<slug>` |
| Modellübergreifende Referenz mit Tabelle der Modell-Guides | `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices` |
| Neuerungen je Modell | `https://platform.claude.com/docs/en/models/<slug>/whats-new-<slug>` |
| Migration je Modell | `https://platform.claude.com/docs/en/models/<slug>/migration-guide` |
| Modellübersicht (aktuelle Namen und IDs) | `https://platform.claude.com/docs/en/about-claude/models/overview` |
| Index der Claude-Code-Doku | `https://code.claude.com/docs/llms.txt` |

Die Muster haben am 12.11.2026 gestimmt. Maßgeblich ist der Index: Steht eine Seite dort unter anderem Namen, gilt der Index, nicht diese Tabelle. Jede Seite gibt es auch als Markdown, wenn man `.md` an die Adresse hängt.

Die Claude-Code-Doku brauchst du nur, wenn ein Vorschlag von der Mechanik abhängt: wie Memory und CLAUDE.md geladen werden (`memory`), Frontmatter von Skills und Agents (`skills`, `sub-agents`), Hook-Ausgaben und Exit-Codes (`hooks`), Berechtigungsmodi (`permission-modes`), geplante Aufgaben (`scheduled-tasks`, `routines`). Schlag die Mechanik dort nach, bevor du sie in einen Vorschlag schreibst.

### Werkzeug

In dieser Reihenfolge, je nachdem, was die Session hat:

1. `WebFetch` direkt.
2. Der Agent `web-fetch`, wenn es kein eigenes WebFetch gibt.
3. `stemago-tools:research-agent` als letzter Weg.

`WebFetch` gibt lange Seiten als Zusammenfassung zurück. Fehlen danach Beispielblöcke oder ganze Abschnitte, hol sie gezielt nach (ein Abruf je Abschnitt) oder lade die Markdown-Fassung in den Scratchpad und lies sie mit Read, wenn die Session Netzzugriff per Shell erlaubt (`curl -sS -o <scratchpad>/<slug>.md <adresse>.md`). Was trotzdem nur zusammengefasst vorlag, nennst du im Bericht unter „Maßstab".

Scheitert der Index, versuch die Seitenmuster direkt. Scheitert auch das, such mit `WebSearch` nach „prompting <Modellname> site:platform.claude.com" und ruf den Treffer ab. Scheitert alles, greift die Regel „Ohne frische Doku kein Audit".

### Abruf-Auftrag

Die Seiten sind lang, und ein Abruf fasst sie zusammen. Damit nichts Wesentliches verloren geht, verlang ausdrücklich:

```
Gib die Seite <URL> vollständig und getreu wieder, ich prüfe bestehende System-Prompts,
CLAUDE.md-Dateien, Skill- und Agent-Definitionen dagegen:
1. Jede Abschnittsüberschrift in Reihenfolge, darunter jede Empfehlung, Kernsätze wörtlich in Anführungszeichen.
2. Alle Beispiele und Vorher-nachher-Formulierungen wörtlich.
3. Was die Seite über Anweisungen sagt, die für frühere Modelle geschrieben wurden.
4. Alle Verweise auf verwandte Seiten mit Adresse.
Meldet eine Adresse einen Fehler oder leitet sie um, nenn Status und Zieladresse.
Ergänze nichts aus dem Gedächtnis; kennzeichne, was nicht von der Seite stammt.
```

Schreib keine eigenen Vermutungen in den Auftrag („achte auf NEVER-Regeln"). Wer eine Hypothese mitgibt, bekommt sie bestätigt zurück. Wird eine Seite beim Abruf abgeschnitten, hol den Rest nach, statt mit der Zusammenfassung zu arbeiten.

### Prüfkriterien ableiten

Je Kriterium eine Zeile: Name, Aussage der Doku in einem Satz mit wörtlichem Kern, Quelle.

So sah ein Kriterium beim Lauf vom 12.11.2026 für Fable 5.2 aus. Das ist ein Formatbeispiel, kein Maßstab. Maßgeblich ist, was die Doku am Tag des Laufs sagt:

> **Absolute Regeln brauchen ihre Ausnahme.** „The model treats an instruction that contains 'never' as absolute." Statt „never delete files" besser „ask for approval before deleting files". Quelle: prompting-claude-fable-5-2, Abschnitt „Keep caution from piling up".

Nimm kein Kriterium auf, das du nur aus früheren Läufen oder aus deinem Wissen über ältere Modelle kennst. Steht es nicht mehr in der Doku, ist es keins mehr.

---

## Fundmuster

Diese Muster gelten unabhängig vom Modell. Jedes ist bei einem echten Audit aufgetreten.

| Muster | Woran man es erkennt | Beispiel |
|---|---|---|
| Widerspruch zwischen Dateien | Zwei Dateien regeln dasselbe verschieden | CLAUDE.md: „Arbeit ist erst fertig, wenn gepusht ist". Der Skill für das Session-Ende fragt vor dem Push. |
| Wörtlich gelesen falsch | Die Regel verbietet auch den Normalfall | „Kein Schreiben ohne WHERE" trifft jedes INSERT. |
| Regel und nächste Zeile beißen sich | „Immer X" direkt neben einem Fall für „nicht X" | „Immer ‚no text' anhängen", darunter die Anleitung für Text im Bild. |
| Geltungsbereich zu weit | CLAUDE.md eines Elternordners oder ein `@`-Import lädt in jedem Unterprojekt | Regeln für einen Leitstand-Ordner samt Projektregister in jeder Projekt-Session. |
| Beschreibung verspricht anderes als der Text | Agent-Beschreibung sagt „für direkte Aufträge", der Text bricht ohne Ticket ab | |
| Überholtes Memory | Beschreibung und Text nennen verschiedene Stände, spätere Nachträge widersprechen früheren | „Push ist offene Entscheidung des Users", zwei Absätze später: Push ausgeführt. |
| Regeln, die Regeln erzeugen | Ein Skill speichert „nie/immer"-Aussagen ohne Grund ins Memory | |
| Vorlagen, die sich vererben | Ein Setup-Skill schreibt Regeln in neue Projekte | Pflicht-Rückfragen am Aufgabenende in jeder neuen CLAUDE.md. |
| Absolute Blockade im Hook | Der Hook blockt hart, wo eine Rückfrage gemeint ist. Die Belege zeigen wiederholte Blockaden. | `rm -r` immer geblockt, auch im Scratchpad. |
| Hook mit Fehler | In den Belegen steht derselbe Hook mit Exit-Code ungleich 0 und 2 | Ein Schutz-Hook, der an der Shell-Version scheitert und deshalb nichts schützt. |
| Fremder Text im Kontext | Ein installiertes Plugin gibt beim Start Anweisungen aus | Start-Hinweis, der für jede Aufgabe einen Skill verlangt. Vorschlag: Gegenregel in der User-CLAUDE.md. |
| Agents ohne Modell | Agent-Datei ohne `model:`, in den Belegen viele Starts ohne Modellangabe | Mechanische Prüf-Agents laufen mit dem teuersten Modell der Session. |
| Aufgabe ohne Fehlerfall | Geplante Aufgabe sagt „nie eine neue Seite anlegen", aber nicht, was gilt, wenn die Seite fehlt | |
| Workaround im Prompt | Der Prompt umgeht einen Fehler im eigenen Skript | Vorschlag: das Skript beheben und den Workaround streichen. |

Bei Hooks reicht Lesen oft nicht. Prüfe auch, wie das Skript seine Eingabe verarbeitet: Wird ein mehrzeiliger Befehl überhaupt vollständig geprüft? Unter `/bin/sh` auf macOS wertet `echo` Backslash-Folgen aus, was JSON mit `\n` zerstört.

---

## Bericht

```markdown
# Prompt-Audit

<2–3 Sätze: Gesamtbild, die wichtigsten Punkte, „geändert habe ich nichts">

**Maßstab:** <Modell>, gelesen am <Datum>:
- <Seitentitel> — <Adresse>
- …
Kernaussagen: <3–5 Punkte, je ein Satz>

Pfade ohne Präfix liegen unter `<gemeinsamer Präfix>`.

## A. <Bereich, wichtigster zuerst>

| Nr | Fundstelle | Heute | Vorschlag |
|---|---|---|---|
| A1 | `pfad/datei.md:147` | <wörtliches Kurzzitat, dazu in einem Satz, warum es nicht passt> | <Umformulierung zum Übernehmen> |

## B. …

## Ohne Änderungsbedarf
<Dateien, die geprüft und in Ordnung sind, in einer Zeile>

## Ergänzungen aus der Doku
<Was die Doku zusätzlich empfiehlt, mit Nebenwirkungen und deiner Empfehlung, ob es hier passt>

## Nicht geprüft
<Was aus dem Inventar nicht gelesen wurde und warum>

## Freigabe
<Gruppen, einzeln freigebbar; was im Working Tree bleibt; was der User selbst tun muss>
```

Regeln für die Tabellen:

- Eine Zeile je Fund. Hängen mehrere Stellen am selben Problem, stehen sie in einer Zeile mit allen Fundstellen.
- „Heute" enthält das Zitat so kurz, dass man die Stelle wiederfindet. „Vorschlag" enthält den neuen Wortlaut, nicht eine Beschreibung davon.
- Sortiere nach Wirkung: Widersprüche und Regeln mit Folgen für jede Session zuerst, Stilfragen zuletzt.
- Zahlen aus den Belegen stehen mit ihrem Fenster da („453 Subagent-Starts in 14 Tagen").
- Was auf Lesen beruht und nicht ausgeführt wurde, ist so gekennzeichnet.

---

## Umsetzen

### Je Dateiart

| Was | Vorgehen |
|---|---|
| Versionierte Datei im Projekt | Mit Edit ändern, uncommittet lassen. Der User sieht die Änderung in `git diff`. |
| Datei ohne Versionierung (`~/.claude/CLAUDE.md`, Memory, User-Skills, geplante Aufgaben, Elternordner) | Erst nach `~/.claude/backups-prompt-audit-<datum>/` kopieren, dann ändern. |
| `settings.json` | Sicherungskopie mit Rechten 600. Änderung als JSON in eine `mktemp`-Datei schreiben und mit `jq --slurpfile` einfügen. Danach die geänderten Schlüssel einzeln zurücklesen. |
| Memory | Eine Datei je Fakt, `MEMORY.md` als Index mit einer Zeile je Datei. Was das Repo schon festhält, gehört in die CLAUDE.md des Projekts, nicht ins Memory. |
| Hook-Skript | Fallliste schreiben (Befehl, Modus, erwartetes Ergebnis), in `sh`, `bash` und `dash` laufen lassen, erst dann fertig melden. Die Hook-Mechanik vorher in der Claude-Code-Doku nachschlagen. |
| Plugin-Quelle | Release-Regeln des Projekts beachten (Versionsdateien, Changelog), `claude plugin validate` laufen lassen. |
| Fremdes Plugin | Nicht ändern. Abschalten über `enabledPlugins` in der User-Einstellung, wenn der User das freigibt, oder Gegenregel in der User-CLAUDE.md. |
| MCP-Server | `/mcp disable <name>` kann nur der User eingeben. Nie `claude mcp remove` als Ersatz: Das löscht Konfiguration und Tokens. |
| Cloud-Routine oder gerätegebundene Aufgabe | Lesen über `RemoteTrigger`. Ändern nur dort, wo die Oberfläche es zulässt. Sonst bekommt der User den fertigen Text. |

### Löschen

- Dateien und Ordner werden in den Sicherungsordner verschoben, nicht gelöscht.
- Vor dem Urteil „tot" oder „unbenutzt" bei Routinen: letzten Lauf, Pausengrund und Lauf-Protokoll ansehen. Eine Routine, die pausiert ist, weil ein Gerät nicht erreichbar war, ist nicht tot.
- Routinen löschst du nur, wenn der User jede einzeln benannt hat. Sag vorher, dass die bisherigen Läufe und unter Umständen ihre Chats mit gelöscht werden, und sichere die Definition.

### Abschluss

- Frontmatter parsen: `ruby -ryaml` oder ein YAML-Parser, nicht nur ein Blick. Ein Doppelpunkt mit Leerzeichen in einer unquotierten Beschreibung bricht das Frontmatter, und die Datei lädt dann ohne ihre Felder.
- Stimmt eine Aussage aus dem ersten Bericht nicht mehr, weil sich beim Umsetzen etwas anderes gezeigt hat, steht die Korrektur ausdrücklich im Abschlussbericht.
- Commit, Push und das Aktualisieren installierter Plugins geschehen nur auf Wunsch des Users.
