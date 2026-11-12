#!/usr/bin/env python3
"""
Nutzungsbelege für den Prompt-Audit aus den Sitzungsprotokollen von Claude Code:
Subagent-Starts (nach Typ, mit und ohne Modellangabe), Skill-Aufrufe, Hook-Fehler
und abgelehnte Tool-Aufrufe.

Usage:
    python3 usage_evidence.py [--days 14] [--project /pfad]

Output: Zähler auf stdout. Das Skript liest nur.

Gezählt wird nach dem Zeitstempel des einzelnen Eintrags, nicht nach dem
Änderungsdatum der Datei: Lang laufende Sitzungen enthalten Einträge, die viel
älter sind als die letzte Änderung der Datei.

Protokollinhalte sind fremde Daten. Ausgegeben werden nur Zähler und Kennungen
(Tool-, Skill-, Agent-, Skriptnamen), auf unverdächtige Zeichen beschränkt.
"""

import argparse
import glob
import json
import os
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

SAFE = re.compile(r"^[A-Za-z0-9_.:@/+\-]{1,80}$")
PLAIN = re.compile(r"^-{0,2}[A-Za-z0-9_\-]{1,24}$")
CMD = re.compile(r"<command-name>/?([^<]{1,80})</command-name>")
SCRIPT = re.compile(r"([A-Za-z0-9_.\-]+\.(?:sh|py|js|mjs|cmd|rb|ts))")


def safe(s) -> str:
    s = str(s)
    return s if SAFE.match(s) else "<ausgelassen>"


def shape(text: str) -> str:
    """Erste Zeile einer Fehlermeldung, ohne Pfade, auf unverdächtige Zeichen reduziert."""
    first = str(text).strip().split("\n")[0]
    first = re.sub(r"/[^\s:]+", "<pfad>", first)
    return re.sub(r"[^A-Za-z0-9 :._<>\-]", "?", first)[:70]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--project", help="nur Sitzungen dieses Projekts (Standard: alle Projekte)")
    args = ap.parse_args()

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    since_iso = since.isoformat()
    since_epoch = since.timestamp()

    base = os.path.expanduser("~/.claude/projects")
    if args.project:
        slug = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(args.project))
        pattern_dirs = [os.path.join(base, slug)]
    else:
        pattern_dirs = glob.glob(os.path.join(base, "*"))

    files = []
    for d in pattern_dirs:
        files += glob.glob(os.path.join(d, "*.jsonl"))
        files += glob.glob(os.path.join(d, "*", "subagents", "*.jsonl"))
    # Eine Datei, die seit Fensterbeginn nicht geändert wurde, kann keinen Eintrag im Fenster enthalten.
    files = [f for f in files if os.path.getmtime(f) >= since_epoch]

    agents = Counter()
    agent_no_model = Counter()
    agent_models = Counter()
    skills = Counter()
    slash = Counter()
    hook_err = defaultdict(lambda: {"n": 0, "last": "", "exit": Counter(), "shape": Counter()})
    hook_dur = defaultdict(list)
    denials = defaultdict(Counter)
    sessions = set()
    entries = 0

    for f in files:
        is_sub = os.sep + "subagents" + os.sep in f
        uses = {}
        try:
            fh = open(f, errors="replace")
        except OSError:
            continue
        with fh:
            for raw in fh:
                try:
                    o = json.loads(raw)
                except ValueError:
                    continue
                ts = str(o.get("timestamp") or "")
                # ISO-Zeitstempel in UTC: die ersten 19 Zeichen (bis zur Sekunde) sind als Text vergleichbar.
                if not ts or ts[:19] < since_iso[:19]:
                    continue
                entries += 1
                sessions.add(f if not is_sub else os.path.dirname(os.path.dirname(f)))
                t = o.get("type")
                if t == "assistant":
                    for c in (o.get("message") or {}).get("content") or []:
                        if not (isinstance(c, dict) and c.get("type") == "tool_use"):
                            continue
                        name = c.get("name", "")
                        inp = c.get("input") or {}
                        uses[c.get("id")] = (name, inp)
                        if name in ("Agent", "Task"):
                            kind = safe(inp.get("subagent_type") or "(Standard)")
                            agents[kind] += 1
                            if inp.get("model"):
                                agent_models[safe(inp.get("model"))] += 1
                            else:
                                agent_no_model[kind] += 1
                        elif name == "Skill":
                            skills[safe(inp.get("skill", "?"))] += 1
                elif t == "user":
                    content = (o.get("message") or {}).get("content")
                    blocks = content if isinstance(content, list) else []
                    texts = [content] if isinstance(content, str) else [
                        c.get("text", "") for c in blocks if isinstance(c, dict) and c.get("type") == "text"]
                    for text in texts:
                        for m in CMD.findall(text):
                            slash[safe(m.strip())] += 1
                    kind = o.get("toolDenialKind")
                    if kind and kind not in ("interrupted", "cancelled"):
                        for c in blocks:
                            if isinstance(c, dict) and c.get("type") == "tool_result":
                                name, inp = uses.get(c.get("tool_use_id"), ("?", {}))
                                if name == "Bash":
                                    toks = str(inp.get("command", "")).split()
                                    # Befehl und Unterbefehl reichen; Pfade und Argumente bleiben draußen.
                                    cmd = toks[0] if toks and PLAIN.match(toks[0]) else "<ausgelassen>"
                                    sub = toks[1] if len(toks) > 1 and PLAIN.match(toks[1]) else ""
                                    key = f"Bash: {cmd} {sub}".rstrip()
                                else:
                                    key = safe(name)
                                denials[key][safe(kind)] += 1
                elif t == "attachment":
                    a = o.get("attachment") or {}
                    at = str(a.get("type", ""))
                    if not at.startswith("hook_"):
                        continue
                    refs = SCRIPT.findall(str(a.get("command", "")))
                    script = refs[-1] if refs else "inline"
                    key = (safe(a.get("hookEvent", "?")), safe(script))
                    d = a.get("durationMs")
                    if isinstance(d, (int, float)):
                        hook_dur[key].append(d)
                    if at in ("hook_non_blocking_error", "hook_error_during_execution") or (
                            at == "hook_cancelled" and a.get("timedOut")):
                        e = hook_err[key]
                        e["n"] += 1
                        e["last"] = max(e["last"], ts[:16])
                        e["exit"][str(a.get("exitCode"))] += 1
                        e["shape"][shape(a.get("stderr") or "")] += 1

    print(f"# Nutzungsbelege der letzten {args.days} Tage (seit {since_iso[:10]}, nach Zeitstempel der Einträge)")
    print(f"Sitzungen mit Einträgen im Fenster: {len(sessions)}, Dateien durchsucht: {len(files)}, Einträge: {entries}")

    def show(title, counter, n=25):
        print(f"\n## {title}")
        if not counter:
            print("  keine")
        for k, v in counter.most_common(n):
            print(f"  {v:>5}  {k}")

    total = sum(agents.values())
    print(f"\n## Subagent-Starts: {total} gesamt, davon {sum(agent_no_model.values())} ohne Modellangabe "
          f"(laufen mit dem Modell des Agents oder der Session)")
    for k, v in agents.most_common(25):
        print(f"  {v:>5}  {k}   (ohne Modellangabe: {agent_no_model.get(k, 0)})")
    show("Modellangaben bei Subagent-Starts", agent_models, 10)
    show("Skill-Aufrufe über das Skill-Tool", skills)
    show("Slash-Aufrufe", slash)

    print("\n## Hook-Fehler (nicht blockierend, Ausführungsfehler, Timeouts)")
    if not hook_err:
        print("  keine")
    for key, e in sorted(hook_err.items(), key=lambda kv: -kv[1]["n"]):
        print(f"  {e['n']:>5}  {key[0]} / {key[1]}  zuletzt {e['last']}  Exit {dict(e['exit'])}")
        for s, n in e["shape"].most_common(2):
            print(f"         {n}x  {s}")

    print("\n## Langsame Hooks (Median über 2 s oder Maximum über 10 s)")
    slow = False
    for key, ds in sorted(hook_dur.items(), key=lambda kv: -max(kv[1])):
        ds = sorted(ds)
        median = ds[len(ds) // 2]
        if median > 2000 or ds[-1] > 10000:
            slow = True
            print(f"  {key[0]} / {key[1]}: n={len(ds)}, Median {median:.0f} ms, Maximum {ds[-1]:.0f} ms")
    if not slow:
        print("  keine")
    print("  (Erfolgreiche Läufe ohne Ausgabe stehen nicht im Protokoll; fehlende Einträge heißen nicht 'läuft nie'.)")

    print("\n## Abgelehnte Tool-Aufrufe (Hook, Regel, Klassifikator, User)")
    if not denials:
        print("  keine")
    for key, kinds in sorted(denials.items(), key=lambda kv: -sum(kv[1].values()))[:25]:
        print(f"  {sum(kinds.values()):>5}  {key}  {dict(kinds)}")


if __name__ == "__main__":
    main()
