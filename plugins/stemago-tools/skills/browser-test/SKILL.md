---
name: browser-test
description: "UI im Browser testen - Screenshots, Interaktionen, DevTools"
---

# Chrome DevTools MCP - Browser-Testing

Nutze den Chrome DevTools MCP Server um UI-Änderungen im echten Browser zu testen.

## Wichtigste Tools

### Navigation & Snapshots

**`mcp__chrome-devtools__navigate_page`**
```
url: "http://localhost:3000/admin/tournaments"
type: "url"  # oder "back", "forward", "reload"
```

**`mcp__chrome-devtools__take_snapshot`**
A11y-Tree mit Element-UIDs abrufen. Bevorzuge dies vor Screenshots.

**`mcp__chrome-devtools__take_screenshot`**
Visueller Screenshot der Seite.
```
fullPage: true  # Komplette Seite statt Viewport
```

### Interaktionen

**`mcp__chrome-devtools__click`**
```
uid: "element-uid-from-snapshot"
dblClick: false  # Optional für Doppelklick
```

**`mcp__chrome-devtools__fill`**
```
uid: "input-uid-from-snapshot"
value: "Test Eingabe"
```

**`mcp__chrome-devtools__hover`**
```
uid: "element-uid"
```

**`mcp__chrome-devtools__press_key`**
```
key: "Enter"  # oder "Control+A", "Escape" etc.
```

### Formulare

**`mcp__chrome-devtools__fill_form`**
Mehrere Felder auf einmal ausfüllen:
```json
{
  "elements": [
    {"uid": "name-input", "value": "Test Team"},
    {"uid": "email-input", "value": "test@example.com"}
  ]
}
```

### Debugging

**`mcp__chrome-devtools__list_console_messages`**
Console-Logs der Seite abrufen.

**`mcp__chrome-devtools__list_network_requests`**
Netzwerk-Requests inspizieren.

**`mcp__chrome-devtools__get_network_request`**
Details eines spezifischen Requests.

**`mcp__chrome-devtools__evaluate_script`**
JavaScript im Browser ausführen:
```
function: "() => document.title"
```

## Typischer Workflow

1. **Navigieren**: `navigate_page` zur gewünschten URL
2. **Snapshot**: `take_snapshot` um UIDs zu bekommen
3. **Interagieren**: `click`, `fill`, `hover` mit UIDs
4. **Verifizieren**: `take_screenshot` oder erneut `take_snapshot`

## Anwendungsfälle

- **UI-Änderungen testen**: Nach Code-Änderung im Browser prüfen
- **Formulare debuggen**: Eingaben simulieren, Validierung testen
- **Responsive Design**: Seite resizen mit `resize_page`
- **Performance**: `performance_start_trace` für Traces
- **Fehlersuche**: Console-Logs und Network-Requests prüfen

## Seiten-Management

**`mcp__chrome-devtools__list_pages`** - Offene Tabs auflisten
**`mcp__chrome-devtools__select_page`** - Tab auswählen
**`mcp__chrome-devtools__new_page`** - Neuen Tab öffnen
**`mcp__chrome-devtools__close_page`** - Tab schließen

## Hinweise

- **Snapshot bevorzugen**: Effizienter als Screenshots für Navigation
- **UIDs sind temporär**: Nach Navigation neu snapshottten
- **Dev Server muss laufen**: `npm run dev` auf Port 3000
- **Wait for**: `wait_for` um auf Text zu warten bevor weiter
