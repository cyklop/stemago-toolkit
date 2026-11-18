#!/usr/bin/env bash
# Stop-Hook: lässt die Tests laufen, bevor Claude die Runde beendet,
# aber nur wenn im Arbeitsbaum Code-Dateien geändert sind.
# Aufruf aus .claude/settings.json:
#   bash .claude/hooks/verify-on-stop.sh '<testbefehl>' '<regex für Code-Dateien>'
# Beispiel:
#   bash .claude/hooks/verify-on-stop.sh 'npm test --silent' '\.(ts|tsx|js|jsx)$'
# Exit 2 schickt Claude mit der Fehlerausgabe zurück an die Arbeit.
# Nach einem solchen Rücksprung (stop_hook_active) blockt der Hook nicht erneut,
# damit keine Endlosschleife entsteht; der Fehler bleibt dann im Bericht sichtbar.

test_cmd="$1"
pattern="${2:-.*}"

input=$(cat)
if [ "$(echo "$input" | jq -r '.stop_hook_active // false')" = "true" ]; then
  exit 0
fi

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0
changed=$(git status --porcelain | awk '{print $NF}' | grep -E "$pattern")
[ -z "$changed" ] && exit 0

if ! output=$(eval "$test_cmd" 2>&1); then
  {
    echo "Tests schlagen fehl (geänderte Dateien: $(echo "$changed" | tr '\n' ' ')):"
    echo "$output" | tail -60
    echo "Behebe die Fehler oder nenne sie im Bericht ausdrücklich als offen."
  } >&2
  exit 2
fi
exit 0
