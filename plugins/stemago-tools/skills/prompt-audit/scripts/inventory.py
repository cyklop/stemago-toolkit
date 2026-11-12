#!/usr/bin/env python3
"""
Inventar aller Anweisungsquellen, die eine Claude-Code-Session in einem Projekt lädt
oder laden kann: CLAUDE.md-Kette samt @-Importen, Memory, Skills, Agents, Hooks,
Output-Styles, geplante Aufgaben, installierte Plugins.

Usage:
    python3 inventory.py [--project /pfad/zum/projekt]

Output: Textübersicht auf stdout. Das Skript liest nur.

Einstellungsdateien werden schlüsselweise gelesen. Hook-Befehle, env-Blöcke und
Header erscheinen nie im Wortlaut, weil dort Zugangsdaten stehen können.
"""

import argparse
import json
import os
import re
import subprocess
import time
from pathlib import Path

HOME = Path.home()
PRUNE = {"node_modules", ".git", "vendor", "dist", "build", ".next", "worktrees", ".venv", "__pycache__"}
SCRIPT_REF = re.compile(r"[\w./${}~-]+\.(?:sh|py|js|mjs|cmd|rb|ts)\b")

_git_cache: dict[str, tuple[str, set[str]] | None] = {}


def short(p: Path) -> str:
    s = str(p)
    return "~" + s[len(str(HOME)):] if s.startswith(str(HOME)) else s


def git_info(directory: Path):
    """(root, getrackte Dateien) des Repos, in dem directory liegt, sonst None."""
    key = str(directory)
    if key in _git_cache:
        return _git_cache[key]
    info = None
    try:
        root = subprocess.run(["git", "-C", key, "rev-parse", "--show-toplevel"],
                              capture_output=True, text=True, timeout=10)
        if root.returncode == 0:
            top = root.stdout.strip()
            if top in _git_cache:
                info = _git_cache[top]
            else:
                files = subprocess.run(["git", "-C", top, "ls-files"], capture_output=True, text=True, timeout=30)
                info = (top, set(files.stdout.splitlines()))
                _git_cache[top] = info
    except (OSError, subprocess.SubprocessError):
        info = None
    _git_cache[key] = info
    return info


def tracking(p: Path) -> str:
    """'git' = versioniert (Änderung per git umkehrbar), 'kein git' = vor Änderung sichern."""
    info = git_info(p.parent)
    if not info:
        return "kein git"
    top, files = info
    try:
        rel = str(p.resolve().relative_to(Path(top).resolve()))
    except ValueError:
        return "kein git"
    return "git" if rel in files else "kein git"


def read(p: Path) -> str:
    try:
        return p.read_text(errors="replace")
    except OSError:
        return ""


def frontmatter(text: str) -> dict[str, str]:
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    out: dict[str, str] = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        km = re.match(r"^\s{0,2}([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            out[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return out


def imports(p: Path, text: str) -> list[Path]:
    """@pfad-Zeilen außerhalb von Codeblöcken: Diese Dateien lädt Claude Code mit."""
    found, fenced = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = re.match(r"^@(\S+)\s*$", line.strip())
        if m:
            ref = os.path.expanduser(m.group(1))
            target = Path(ref) if os.path.isabs(ref) else (p.parent / ref)
            if target.is_file():
                found.append(target)
    return found


def line(kind: str, scope: str, p: Path, extra: str = "") -> str:
    text = read(p)
    return f"  {len(text):>6} Z  ~{len(text) // 4:>5} Tok  {tracking(p):8}  {scope:22}  {short(p)}{('  ' + extra) if extra else ''}"


def section(title: str, rows: list[str], empty: str = "keine") -> None:
    print(f"\n## {title}")
    if rows:
        print("\n".join(rows))
    else:
        print(f"  {empty}")


def load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return None


def hook_rows(label: str, hooks: dict) -> list[str]:
    grouped: dict[tuple[str, str, str], list[str]] = {}
    for event, entries in (hooks or {}).items():
        for entry in entries or []:
            matcher = entry.get("matcher") or "*"
            for h in entry.get("hooks") or []:
                cmd = str(h.get("command") or h.get("prompt") or "")
                refs = SCRIPT_REF.findall(cmd)
                what = ", ".join(os.path.basename(r) for r in refs[:3]) if refs else f"inline, {len(cmd)} Zeichen"
                grouped.setdefault((event, str(h.get("type", "?")), what), []).append(matcher)
    return [f"  {label:30}  {event:17} {kind:8} {what}  (matcher: {', '.join(dict.fromkeys(ms))})"
            for (event, kind, what), ms in grouped.items()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=os.getcwd())
    args = ap.parse_args()
    project = Path(args.project).resolve()

    print(f"# Inventar für {short(project)}  (Stand {time.strftime('%Y-%m-%d')})")
    print("Spalten: Zeichen, geschätzte Tokens (Zeichen/4), Versionierung, Geltung, Pfad")

    # ---------------------------------------------------------------- CLAUDE.md-Kette
    seen: set[Path] = set()
    rows: list[str] = []
    always = 0

    def add_md(p: Path, scope: str) -> None:
        nonlocal always
        rp = p.resolve()
        if rp in seen or not p.is_file():
            return
        seen.add(rp)
        text = read(p)
        always += len(text)
        rows.append(line("claude-md", scope, p))
        for imp in imports(p, text):
            if imp.resolve() not in seen:
                seen.add(imp.resolve())
                always += len(read(imp))
                rows.append(line("import", scope + " (@-Import)", imp))

    add_md(HOME / ".claude" / "CLAUDE.md", "user (alle Projekte)")
    chain = [project] + list(project.parents)
    for d in chain:
        scope = "projekt" if d == project else "elternordner (lädt mit)"
        for name in ("CLAUDE.md", "CLAUDE.local.md", ".claude/CLAUDE.md"):
            add_md(d / name, scope if "local" not in name else scope + ", lokal")
        rules = d / ".claude" / "rules"
        if rules.is_dir():
            for r in sorted(rules.glob("*.md")):
                fm = frontmatter(read(r))
                add_md(r, scope + (" (paths: nur passende Dateien)" if "paths" in fm else ""))
    agents_md = project / "AGENTS.md"
    if agents_md.is_file():
        rows.append(line("agents-md", "projekt (lädt nicht von selbst)", agents_md))
    section("CLAUDE.md-Kette (immer im Kontext)", rows)
    print(f"  Summe immer geladen: {always} Zeichen, ~{always // 4} Tokens")

    nested = []
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in PRUNE]
        depth = len(Path(root).relative_to(project).parts)
        if depth >= 4:
            dirs[:] = []
        if depth > 0 and "CLAUDE.md" in files:
            p = Path(root) / "CLAUDE.md"
            if p.resolve() not in seen:
                nested.append(line("claude-md", "unterordner (bei Bedarf)", p))
    section("CLAUDE.md in Unterordnern (laden nur dort)", nested)

    # ---------------------------------------------------------------- Memory
    slug = re.sub(r"[^A-Za-z0-9]", "-", str(project))
    mem = HOME / ".claude" / "projects" / slug / "memory"
    rows = []
    if mem.is_dir():
        for p in sorted(mem.glob("*.md")):
            fm = frontmatter(read(p))
            age = int((time.time() - p.stat().st_mtime) / 86400)
            kind = "Index, immer geladen" if p.name == "MEMORY.md" else f"type={fm.get('type', '?')}"
            rows.append(line("memory", "projekt-memory", p, f"{kind}, {age} Tage alt"))
    section("Memory", rows, "kein Memory-Verzeichnis für dieses Projekt")

    # ---------------------------------------------------------------- Einstellungen (schlüsselweise)
    settings_files = [(HOME / ".claude" / "settings.json", "user")]
    for d in reversed(chain):
        for name, sc in ((".claude/settings.json", "projekt"), (".claude/settings.local.json", "lokal")):
            p = d / name
            if p.is_file() and p != HOME / ".claude" / "settings.json":
                settings_files.append((p, sc if d == project else f"elternordner/{sc}"))
    overrides: dict[str, str] = {}
    enabled: dict[str, bool] = {}
    hook_lines: list[str] = []
    rows = []
    for p, sc in settings_files:
        data = load_json(p)
        if data is None:
            rows.append(f"  NICHT LESBAR (JSON-Fehler?): {short(p)}")
            continue
        facts = []
        for key in ("model", "effortLevel", "outputStyle", "language"):
            if data.get(key) is not None:
                facts.append(f"{key}={data[key]}")
        mode = (data.get("permissions") or {}).get("defaultMode")
        if mode:
            facts.append(f"defaultMode={mode}")
        for model, ms in (data.get("modelSettings") or {}).items():
            if isinstance(ms, dict) and ms.get("effortLevel"):
                facts.append(f"{model}: effort={ms['effortLevel']}")
        overrides.update(data.get("skillOverrides") or {})
        enabled.update(data.get("enabledPlugins") or {})
        hook_lines += hook_rows(f"{sc}: {p.name}", data.get("hooks") or {})
        rows.append(f"  {sc:20} {short(p)}  {'; '.join(facts) if facts else '(keine der geprüften Schlüssel)'}")
    section("Einstellungen (nur ausgewählte Schlüssel)", rows)

    # ---------------------------------------------------------------- Skills
    rows = []

    def skill_rows(base: Path, scope: str) -> None:
        if not base.is_dir():
            return
        for p in sorted(base.glob("*/SKILL.md")):
            if p.resolve() in seen:
                continue
            seen.add(p.resolve())
            fm = frontmatter(read(p))
            name = fm.get("name") or p.parent.name
            flags = []
            if overrides.get(name) == "off":
                flags.append("per skillOverrides AUS")
            if fm.get("disable-model-invocation") == "true":
                flags.append("nur manuell")
            flags.append(f"Beschreibung {len(fm.get('description', ''))} Z")
            rows.append(line("skill", scope, p, ", ".join(flags)))
            for extra in sorted(p.parent.glob("*.md")):
                if extra.name != "SKILL.md":
                    rows.append(line("skill-ref", scope + " (bei Bedarf)", extra))

    skill_rows(HOME / ".claude" / "skills", "user")
    for d in chain:
        skill_rows(d / ".claude" / "skills", "projekt" if d == project else "elternordner")
    for plug in sorted((project / "plugins").glob("*")) if (project / "plugins").is_dir() else []:
        skill_rows(plug / "skills", f"plugin-quelle {plug.name}")
    section("Skills (eigene)", rows)

    # ---------------------------------------------------------------- Agents
    rows = []

    def agent_rows(base: Path, scope: str) -> None:
        if not base.is_dir():
            return
        for p in sorted(base.rglob("*.md")):
            fm = frontmatter(read(p))
            if not fm.get("name"):
                continue
            rows.append(line("agent", scope, p, f"model={fm.get('model') or '(erbt Session-Modell)'}, Beschreibung {len(fm.get('description', ''))} Z"))

    agent_rows(HOME / ".claude" / "agents", "user")
    agent_rows(project / ".claude" / "agents", "projekt")
    for plug in sorted((project / "plugins").glob("*")) if (project / "plugins").is_dir() else []:
        agent_rows(plug / "agents", f"plugin-quelle {plug.name}")
    section("Agents (eigene)", rows)

    # ---------------------------------------------------------------- Output-Styles, Commands, Aufgaben
    rows = []
    for base, scope in ((HOME / ".claude" / "output-styles", "user"), (project / ".claude" / "output-styles", "projekt")):
        if base.is_dir():
            rows += [line("output-style", scope, p) for p in sorted(base.glob("*.md"))]
    section("Output-Styles", rows)

    rows = []
    for base, scope in ((HOME / ".claude" / "commands", "user"), (project / ".claude" / "commands", "projekt")):
        if base.is_dir():
            rows += [line("command", scope, p) for p in sorted(base.rglob("*.md"))]
    section("Commands", rows)

    rows = []
    tasks = HOME / ".claude" / "scheduled-tasks"
    if tasks.is_dir():
        rows = [line("aufgabe", "lokal geplant", p) for p in sorted(tasks.glob("*/SKILL.md"))]
    section("Geplante Aufgaben (lokal)", rows)
    print("  Cloud-Routinen stehen nicht auf der Platte: mit RemoteTrigger (action: list) abrufen, falls verfügbar.")

    # ---------------------------------------------------------------- Hooks
    for plug in sorted((project / "plugins").glob("*")) if (project / "plugins").is_dir() else []:
        data = load_json(plug / "hooks" / "hooks.json")
        if data:
            hook_lines += hook_rows(f"plugin-quelle {plug.name}", data.get("hooks") or {})
    section("Hooks (eigene; Befehle nie im Wortlaut)", hook_lines)

    # ---------------------------------------------------------------- Installierte Plugins (fremd)
    rows = []
    installed = load_json(HOME / ".claude" / "plugins" / "installed_plugins.json") or {}
    own_sources = {p.name for p in (project / "plugins").glob("*")} if (project / "plugins").is_dir() else set()
    for key, installs in (installed.get("plugins") or {}).items():
        for inst in installs or []:
            path = Path(inst.get("installPath") or "")
            state = enabled.get(key)
            status = "aktiv" if state is True else "AUS" if state is False else "Status nicht in den Einstellungen"
            n_sk = len(list(path.glob("skills/*/SKILL.md"))) if path.is_dir() else 0
            n_ag = len(list(path.glob("agents/*.md"))) if path.is_dir() else 0
            origin = "eigene Quelle im Projekt" if key.split("@")[0] in own_sources else "fremd, nicht editierbar"
            rows.append(f"  {key:44} {inst.get('version', '?'):10} {status:10} {n_sk:3} Skills {n_ag:3} Agents  {origin}")
            hooks = load_json(path / "hooks" / "hooks.json") if path.is_dir() else None
            if hooks and state is not False:
                for hl in hook_rows("    Hook", hooks.get("hooks") or {}):
                    if "SessionStart" in hl or "UserPromptSubmit" in hl:
                        rows.append(hl + "   <- Text landet im Kontext: Wortlaut prüfen")
                rows.append(f"    Pfad: {short(path)}")
    synced = HOME / ".claude" / "plugins" / "synced"
    if synced.is_dir():
        names = sorted({p.name for p in synced.glob("*/*") if p.is_dir()})
        for name in names:
            key = f"{name}@synced"
            state = enabled.get(key)
            local = any(k.split("@")[0] == name for k in (installed.get("plugins") or {}))
            status = ("AUS" if state is False else
                      "nicht geladen (lokale Installation gleichen Namens hat Vorrang)" if local else
                      "geladen (von claude.ai synchronisiert)")
            rows.append(f"  {key:44} {'':10} {status}")
    section("Installierte Plugins", rows)

    print("\nHinweis: 'kein git' heißt, die Datei vor einer Änderung zu sichern. 'fremd' heißt, sie nicht zu "
          "ändern, sondern eine Gegenregel in einer eigenen Datei vorzuschlagen.")


if __name__ == "__main__":
    main()
