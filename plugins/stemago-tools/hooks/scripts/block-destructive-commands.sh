#!/bin/sh
# block-destructive-commands.sh
# PreToolUse Hook - Block destructive commands before execution
# Exit code 2 = BLOCK execution, exit code 0 = ALLOW execution.
# Exit code 0 with a permissionDecision "ask" JSON on stdout = the user confirms.
# stdout must stay empty unless that JSON is printed.

# Only blocked commands and commands sent to the user for confirmation are
# logged, in a file only the user can read: commands can contain paths and secrets.
LOG_DIR="${HOME}/.claude/logs"
LOG_FILE="${LOG_DIR}/stemago-tools-blocked-commands.log"
timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

log() {
    ( umask 077; mkdir -p "$LOG_DIR" && echo "[$(timestamp)] $1" >> "$LOG_FILE" ) 2>/dev/null
}

# Read JSON input from stdin. The script passes it on with printf, never with
# echo: /bin/sh on macOS expands backslash escapes in echo, which turns the
# "\n" of a multi-line command into a raw newline, breaks the JSON and lets the
# command through unchecked.
INPUT_JSON=$(cat)

# Parse JSON using robust extraction (similar to test-driven-handoff.sh pattern)
TOOL_NAME=""
COMMAND=""
CWD=""
PERMISSION_MODE=""
SCRATCHPAD_DIR=""

# Try direct jq extraction first
if command -v jq >/dev/null 2>&1; then
    TOOL_NAME=$(printf '%s' "$INPUT_JSON" |jq -r '.tool_name' 2>/dev/null)
    COMMAND=$(printf '%s' "$INPUT_JSON" |jq -r '.tool_input.command // ""' 2>/dev/null)
    CWD=$(printf '%s' "$INPUT_JSON" |jq -r '.cwd // ""' 2>/dev/null)
    PERMISSION_MODE=$(printf '%s' "$INPUT_JSON" |jq -r '.permission_mode // ""' 2>/dev/null)
    SCRATCHPAD_DIR=$(printf '%s' "$INPUT_JSON" |jq -r '.scratchpad_dir // ""' 2>/dev/null)
fi

# Fallback to grep/sed if jq fails or returns null
if [ -z "$TOOL_NAME" ] || [ "$TOOL_NAME" = "null" ]; then
    TOOL_NAME=$(printf '%s' "$INPUT_JSON" |grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
fi

if [ -z "$COMMAND" ] || [ "$COMMAND" = "null" ]; then
    COMMAND=$(printf '%s' "$INPUT_JSON" |grep -o '"command":"[^"]*"' | sed 's/.*"command":"\([^"]*\)".*/\1/')
fi

# Only check Bash tool commands
if [ "$TOOL_NAME" != "Bash" ]; then
    exit 0
fi

# Function to block command with reason
block_command() {
    local reason="$1"
    local command="$2"
    
    echo "🚫 BLOCKED: $reason" >&2
    echo "Command: $command" >&2
    echo "Use manual approval or sandbox environment for dangerous operations" >&2
    
    log "BLOCKED: $reason - Command: $command"
    exit 2  # Claude Code convention for blocking
}

# Check for filesystem destruction patterns
check_filesystem_destruction() {
    local cmd="$1"

    # Whitelist: `git rm` is fully reversible via git history — skip filesystem checks.
    # Genuinely destructive git operations are still caught in check_git_destruction.
    if printf '%s\n' "$cmd" | grep -qE "^[[:space:]]*git[[:space:]]+rm([[:space:]]|$)"; then
        return 0
    fi

    # Recursive deletion is handled last, in check_recursive_delete.

    # Format commands: mkfs.* anywhere, 'format' only as the command word. A bare
    # 'format\s+' also matched options and tools such as '--format "%h"' or
    # 'clang-format file.c'.
    if printf '%s\n' "$cmd" | grep -qiE "mkfs\.|(^|[;&|(])[[:space:]]*(sudo[[:space:]]+)?format([[:space:]]|$)"; then
        block_command "filesystem formatting command" "$cmd"
    fi
    
    # Direct device writing
    if printf '%s\n' "$cmd" | grep -qiE "dd\s+.*of=/dev/"; then
        block_command "direct device writing with dd" "$cmd"
    fi
    
    # System directory modifications
    if printf '%s\n' "$cmd" | grep -qE ">\s*/etc/|>\s*/boot/|>\s*/sys/|>\s*/proc/"; then
        block_command "writing to critical system directories" "$cmd"
    fi
}

# Check for git destructive operations
check_git_destruction() {
    local cmd="$1"
    
    # Hard reset (loses uncommitted changes)
    if printf '%s\n' "$cmd" | grep -qiE "git\s+reset\s+--hard"; then
        block_command "git hard reset loses uncommitted changes" "$cmd"
    fi
    
    # Force clean working directory
    if printf '%s\n' "$cmd" | grep -qiE "git\s+clean\s+.*-.*f.*d|git\s+clean\s+.*-.*d.*f"; then
        block_command "git force clean removes untracked files" "$cmd"
    fi
    
    # Force push (can overwrite remote history)
    if printf '%s\n' "$cmd" | grep -qiE "git\s+push\s+.*--force"; then
        block_command "git force push can overwrite remote history" "$cmd"
    fi
    
    # Rebase with force
    if printf '%s\n' "$cmd" | grep -qiE "git\s+rebase\s+.*--force"; then
        block_command "git force rebase can lose commits" "$cmd"
    fi
}

# Check for package manager destructive operations
check_package_manager_destruction() {
    local cmd="$1"
    
    # npm create commands (can overwrite directories)
    if printf '%s\n' "$cmd" | grep -qiE "npm\s+create\s+"; then
        block_command "npm create can overwrite existing directories" "$cmd"
    fi
    
    # npx create commands
    if printf '%s\n' "$cmd" | grep -qiE "npx\s+create-"; then
        block_command "npx create commands can overwrite files" "$cmd"
    fi
    
    # yarn create commands
    if printf '%s\n' "$cmd" | grep -qiE "yarn\s+create\s+"; then
        block_command "yarn create can overwrite directories" "$cmd"
    fi
    
    # pnpm create commands
    if printf '%s\n' "$cmd" | grep -qiE "pnpm\s+create\s+"; then
        block_command "pnpm create can overwrite directories" "$cmd"
    fi
    
    # Force package installations (can break dependencies)
    if printf '%s\n' "$cmd" | grep -qiE "npm\s+install\s+.*--force"; then
        block_command "npm install --force can break dependencies" "$cmd"
    fi
    
    # pip force reinstall
    if printf '%s\n' "$cmd" | grep -qiE "pip\s+install\s+.*--force-reinstall"; then
        block_command "pip force reinstall can break dependencies" "$cmd"
    fi
}

# Check for database destruction
check_database_destruction() {
    local cmd="$1"
    
    # Drop database/table commands
    if printf '%s\n' "$cmd" | grep -qiE "drop\s+(database|table|schema)"; then
        block_command "database/table/schema drop command" "$cmd"
    fi
    
    # Truncate table commands
    if printf '%s\n' "$cmd" | grep -qiE "truncate\s+table"; then
        block_command "table truncation command" "$cmd"
    fi
    
    # Dangerous DELETE statements
    if printf '%s\n' "$cmd" | grep -qiE "delete\s+from.*where\s+1\s*=\s*1"; then
        block_command "delete all rows statement" "$cmd"
    fi
}

# Check for docker/container destruction
check_container_destruction() {
    local cmd="$1"
    
    # Docker system prune
    if printf '%s\n' "$cmd" | grep -qiE "docker\s+system\s+prune\s+.*-f"; then
        block_command "docker force system prune removes all unused data" "$cmd"
    fi
    
    # Docker remove all containers
    if printf '%s\n' "$cmd" | grep -qiE "docker\s+rm\s+.*\$\(docker\s+ps"; then
        block_command "docker remove all containers command" "$cmd"
    fi
    
    # Kubernetes force delete
    if printf '%s\n' "$cmd" | grep -qiE "kubectl\s+delete\s+.*--force"; then
        block_command "kubectl force delete can cause data loss" "$cmd"
    fi
}

# Check for network/download risks (Anthropic recommends blocking curl/wget)
check_network_risks() {
    local cmd="$1"
    
    # curl downloads to sensitive locations
    if printf '%s\n' "$cmd" | grep -qiE "curl\s+.*>\s*/etc/|curl\s+.*>\s*/usr/|curl\s+.*>\s*/bin/"; then
        block_command "curl download to system directories" "$cmd"
    fi
    
    # wget downloads to sensitive locations  
    if printf '%s\n' "$cmd" | grep -qiE "wget\s+.*-O\s*/etc/|wget\s+.*-O\s*/usr/|wget\s+.*-O\s*/bin/"; then
        block_command "wget download to system directories" "$cmd"
    fi
    
    # Piping untrusted content directly (Anthropic warns against this)
    if printf '%s\n' "$cmd" | grep -qiE "curl\s+.*\|\s*(sh|bash|zsh)|wget\s+.*\|\s*(sh|bash|zsh)"; then
        block_command "piping downloaded content to shell is dangerous" "$cmd"
    fi
}

# Check for process/system destruction
check_system_destruction() {
    local cmd="$1"
    
    # Kill all processes
    if printf '%s\n' "$cmd" | grep -qiE "killall\s+.*-9"; then
        block_command "killall with SIGKILL can cause data loss" "$cmd"
    fi
    
    # System shutdown/reboot: only as the command word. A bare 'shutdown\s+' also
    # matched subcommands such as 'xcrun simctl shutdown <device>', and 'halt\s+'
    # matched any text ending in "halt", for example a commit message with "Inhalt".
    if printf '%s\n' "$cmd" | grep -qiE "(^|[;&|(])[[:space:]]*(sudo[[:space:]]+)?(shutdown|reboot|halt|poweroff)([[:space:]]|$)"; then
        block_command "system shutdown/reboot command" "$cmd"
    fi
    
    # chmod 777 on system directories
    if printf '%s\n' "$cmd" | grep -qE "chmod\s+777\s+/"; then
        block_command "chmod 777 on system directories is dangerous" "$cmd"
    fi
    
    # Suspicious bash with encoded content
    if printf '%s\n' "$cmd" | grep -qiE "bash\s+-c\s+.*base64|sh\s+-c\s+.*base64"; then
        block_command "suspicious encoded bash execution" "$cmd"
    fi
}

# Is this absolute path (no trailing slash) clearly inside the project, the
# session scratchpad or a temp directory? Never the root's whole content, never
# version-control data.
path_is_safe() {
    local p="$1" root rest first
    for root in "${CLAUDE_PROJECT_DIR:-}" "$SCRATCHPAD_DIR" "/tmp" "/private/tmp" "${TMPDIR:-}"; do
        root="${root%/}"
        # A session started in / or in the home directory has no project to protect paths by.
        if [ -z "$root" ] || [ "$root" = "${HOME%/}" ]; then
            continue
        fi
        case "$p" in
            "$root"/*)
                rest="${p#"$root"/}"
                first="${rest%%/*}"
                case "$first" in
                    ''|*[*?[]*) return 1 ;;
                esac
                case "/$rest/" in
                    */.git/*) return 1 ;;
                esac
                return 0
                ;;
        esac
    done
    return 1
}

# Can every target of every recursive rm in this command be resolved from the
# command text alone, and does it lie inside the project, the scratchpad or a
# temp directory? Returns 0 = clearly safe, 1 = outside or not resolvable.
# Variables, command substitution, ~, .., braces, backslashes, a wrapped rm
# (sudo, env, xargs, find -exec, bash -c ...) and relative paths after a cd all
# count as not resolvable. Runs in a subshell so 'set -f' does not leak.
rm_targets_are_safe() (
    cmd="$1"
    set -f

    case "$cmd" in
        *'$'*|*'`'*|*'~'*|*'..'*|*'{'*|*'\'*) return 1 ;;
    esac
    [ -n "$CWD" ] || return 1

    has_cd=0
    if printf '%s\n' "$cmd" | grep -qE '(^|[;&|(]|[[:space:]])(cd|pushd|popd)([[:space:]]|$)'; then
        has_cd=1
    fi

    # Quotes only group words. Splitting a quoted path at its spaces yields
    # pieces that each have to be safe, so dropping the quotes cannot turn an
    # outside path into an inside one.
    segments=$(printf '%s\n' "$cmd" | tr -d "\"'" | tr ';&|()' '\n\n\n\n\n')

    while IFS= read -r seg; do
        set -- $seg
        [ $# -gt 0 ] || continue
        # 'git rm' is reversible through history.
        [ "$1" = "git" ] && continue
        if [ "$1" != "rm" ]; then
            # rm behind a wrapper, with a path, or in another spelling (the
            # default macOS file system ignores case): not resolvable here.
            for word in "$@"; do
                case "$word" in
                    [rR][mM]|*/[rR][mM]) return 1 ;;
                esac
            done
            continue
        fi
        shift

        recursive=0
        targets=""
        for arg in "$@"; do
            case "$arg" in
                --recursive) recursive=1 ;;
                --*) ;;
                -*) case "$arg" in *[rR]*) recursive=1 ;; esac ;;
                [0-9]'>'*|'>'*|'<'*) ;;
                *) targets="$targets $arg" ;;
            esac
        done
        [ "$recursive" -eq 1 ] || continue
        [ -n "$targets" ] || return 1

        for target in $targets; do
            case "$target" in
                /*) abs="$target" ;;
                *)
                    [ "$has_cd" -eq 0 ] || return 1
                    target="${target#./}"
                    first="${target%%/*}"
                    case "$first" in
                        ''|.|*[*?[]*) return 1 ;;
                    esac
                    abs="$CWD/$target"
                    ;;
            esac
            while :; do
                case "$abs" in
                    */.) abs="${abs%/.}" ;;
                    */) abs="${abs%/}" ;;
                    *) break ;;
                esac
            done
            case "$abs" in
                *//*|*/./*) return 1 ;;
            esac
            path_is_safe "$abs" || return 1
        done
    done <<EOF
$segments
EOF
    return 0
)

# Recursive deletion (rm -r / -R / -rf / -fr / --recursive, any flag order).
# Inside the project, the scratchpad or a temp directory it runs. Anywhere else,
# or when the targets cannot be resolved, the user confirms it. In permission
# modes where nobody is asked, it stays blocked.
check_recursive_delete() {
    local cmd="$1"

    # The recursive flag must be a real option token: 'rm' anchored to a command
    # boundary (or the end of a path such as /bin/rm), the flag preceded by
    # whitespace and starting with a dash, and we never scan past a command
    # separator (; & |). This avoids false positives on filenames like
    # 'reflect-enabled'.
    if ! printf '%s\n' "$cmd" | grep -qiE '(^|[;&|(/]|[[:space:]])rm([[:space:]][^;&|]*)?[[:space:]](-[A-Za-z]*[rR]|--recursive)'; then
        return 0
    fi

    if rm_targets_are_safe "$cmd"; then
        return 0
    fi

    case "$PERMISSION_MODE" in
        bypassPermissions|dontAsk)
            block_command "recursive deletion (rm -r/-rf) outside the project, scratchpad and temp directories" "$cmd"
            ;;
    esac

    log "ASK: recursive deletion - Command: $cmd"
    printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Recursive deletion (rm -r) outside the project, the session scratchpad and temp directories, or with targets the hook cannot resolve. Please confirm."}}'
    exit 0
}

# Run all destructive command checks
check_filesystem_destruction "$COMMAND"
check_git_destruction "$COMMAND"
check_package_manager_destruction "$COMMAND"
check_database_destruction "$COMMAND"
check_container_destruction "$COMMAND"
check_network_risks "$COMMAND"
check_system_destruction "$COMMAND"
# Last, because it can hand the decision to the user instead of blocking.
check_recursive_delete "$COMMAND"

# If we get here, command is safe to execute
exit 0