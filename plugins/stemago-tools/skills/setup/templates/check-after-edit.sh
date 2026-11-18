#!/usr/bin/env bash
# PostToolUse-Hook (Edit|Write): prüft die gerade geänderte Datei.
# Aufruf aus .claude/settings.json:
#   bash .claude/hooks/check-after-edit.sh '<befehl mit {file}>' '<regex für Dateiendungen>'
# Beispiel:
#   bash .claude/hooks/check-after-edit.sh 'npx eslint {file}' '\.(ts|tsx|js|jsx)$'
# Exit 2 zeigt Claude die Fehlermeldung, damit es sie sofort behebt.
# Exit 0 bei Erfolg oder wenn die Datei nicht passt.

cmd_template="$1"
pattern="${2:-.*}"

file=$(jq -r '.tool_response.filePath // .tool_input.file_path // empty')
[ -z "$file" ] && exit 0
[ -f "$file" ] || exit 0
echo "$file" | grep -Eq "$pattern" || exit 0

cmd="${cmd_template//\{file\}/\"$file\"}"
if ! output=$(eval "$cmd" 2>&1); then
  {
    echo "Prüfung nach dem Bearbeiten von $file fehlgeschlagen:"
    echo "$output" | tail -40
  } >&2
  exit 2
fi
exit 0
