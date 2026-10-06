---
name: browser-test
description: "UI im Browser testen - Screenshots, Interaktionen, DevTools. Verwende diesen Skill wenn der User die UI im Browser prüfen, Screenshots machen, Formulare testen, oder visuell verifizieren will ob Änderungen korrekt aussehen. Auch bei 'schau mal ob die Seite stimmt', 'mach einen Screenshot', 'teste das Formular', 'prüf die UI', 'was zeigt der Browser', oder wenn nach Code-Änderungen das Ergebnis im Browser validiert werden soll."
---

# Browser-Testing mit Chrome DevTools MCP

Teste UI-Änderungen im echten Browser über die `mcp__chrome-devtools__*`-Tools. Parameter stehen in den Tool-Schemas der Session — hier steht nur, was die Schemas nicht sagen.

## Ablauf

1. **Dev-Server klären**: Start-Befehl und Port aus dem Projekt (`package.json`, README, CLAUDE.md). Läuft er nicht, im Hintergrund starten und warten, bis der Port antwortet.
2. **Seite holen**: `list_pages` (bestehende Tabs) oder `new_page`. Fast alle Tools verlangen die `pageId` daraus.
3. **Navigieren**: `navigate_page` mit `type: "url"`.
4. **Snapshot**: `take_snapshot` liefert den A11y-Tree mit Element-UIDs — die Grundlage für jede Interaktion.
5. **Interagieren**: `click`, `fill`, `hover`, `press_key`; mehrere Formularfelder immer in einem `fill_form`-Aufruf.
6. **Warten**: `wait_for` mit dem erwarteten Text, bevor du das Ergebnis prüfst.
7. **Verifizieren**: erneut `take_snapshot` für Inhalt und Zustand, `take_screenshot` nur für das, was nur visuell prüfbar ist (Layout, Farben, Überlappungen).

## Regeln

- **Snapshot vor Screenshot**: billiger im Kontext und liefert die UIDs. Screenshots groß (`fullPage`) nur, wenn das Layout die Frage ist.
- **UIDs sind kurzlebig**: nach jeder Navigation und jeder größeren DOM-Änderung neu snapshotten.
- **Fehlersuche**: `list_console_messages` und `list_network_requests` zuerst, `get_network_request` für Details, `evaluate_script` für gezielte Zustandsabfragen (`() => document.title`).
- **Responsive**: `resize_page` bzw. `emulate`, pro Breakpoint ein Snapshot oder Screenshot.
- **Performance und Qualität**: `performance_start_trace` / `performance_stop_trace`, `lighthouse_audit`.
- **Aufräumen**: selbst geöffnete Tabs mit `close_page` schließen, selbst gestartete Dev-Server am Ende nennen oder beenden.

## Ergebnis melden

Was geprüft wurde (URL, Schritte), was funktioniert, was nicht — mit Konsolenfehlern und fehlgeschlagenen Requests im Wortlaut. Screenshots nur anhängen, wenn sie den Befund zeigen.
