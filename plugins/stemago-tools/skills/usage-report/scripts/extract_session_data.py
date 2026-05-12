#!/usr/bin/env python3
"""
Extrahiert Nutzungsdaten aus Claude-Session-JSONLs für ein Projekt.

Usage:
    python extract_session_data.py --project /path/to/project [--months 1]

Output: JSON auf stdout
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path


def project_hash(project_path: str) -> str:
    """Konvertiert Projekt-Pfad in Claude-Verzeichnis-Hash-Format."""
    return project_path.replace("/", "-")


def find_project_dir(project_path: str) -> Path | None:
    claude_projects = Path.home() / ".claude" / "projects"
    hash_name = project_hash(project_path)
    candidate = claude_projects / hash_name
    if candidate.exists():
        return candidate
    # Fallback: case-insensitive search
    for d in claude_projects.iterdir():
        if d.name.lower() == hash_name.lower():
            return d
    return None


def parse_session_jsonl(jsonl_path: Path, since: datetime) -> dict:
    """Parsed eine Session-JSONL und extrahiert relevante Nutzungsdaten."""
    skill_calls = []
    agent_calls = []
    model_counts = {}
    earliest_ts = None
    latest_ts = None

    try:
        with open(jsonl_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                ts_str = entry.get("timestamp")
                if ts_str:
                    try:
                        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                        if earliest_ts is None or ts < earliest_ts:
                            earliest_ts = ts
                        if latest_ts is None or ts > latest_ts:
                            latest_ts = ts
                    except ValueError:
                        pass

                if entry.get("type") != "assistant":
                    continue

                msg = entry.get("message", {})
                if not isinstance(msg, dict):
                    continue

                # Modell erfassen
                model = msg.get("model")
                if model:
                    model_counts[model] = model_counts.get(model, 0) + 1

                # Tool-Aufrufe scannen
                content = msg.get("content", [])
                if not isinstance(content, list):
                    continue

                for item in content:
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") != "tool_use":
                        continue

                    tool_name = item.get("name", "")
                    inp = item.get("input", {})

                    if tool_name == "Skill":
                        skill = inp.get("skill", "")
                        if skill:
                            skill_calls.append(skill)

                    elif tool_name == "Agent":
                        agent = inp.get("subagent_type", "")
                        if agent:
                            agent_calls.append(agent)

    except (OSError, PermissionError):
        return {}

    # Zeitraum-Filter: Session muss im gewünschten Zeitraum aktiv gewesen sein
    if latest_ts and latest_ts < since:
        return {}

    return {
        "skill_calls": skill_calls,
        "agent_calls": agent_calls,
        "model_counts": model_counts,
        "date": earliest_ts.date().isoformat() if earliest_ts else None,
        "latest": latest_ts.date().isoformat() if latest_ts else None,
    }


def read_sessions_index(project_dir: Path) -> dict:
    """Liest sessions-index.json für Metadaten (Summary, messageCount)."""
    index_file = project_dir / "sessions-index.json"
    if not index_file.exists():
        return {}
    try:
        data = json.loads(index_file.read_text(encoding="utf-8"))
        entries = data.get("entries", [])
        return {e["sessionId"]: e for e in entries if "sessionId" in e}
    except (json.JSONDecodeError, OSError):
        return {}


def aggregate_totals(sessions: list) -> dict:
    skill_counts: dict[str, int] = {}
    agent_counts: dict[str, int] = {}
    model_counts: dict[str, int] = {}

    for s in sessions:
        for sk in s.get("skill_calls", []):
            skill_counts[sk] = skill_counts.get(sk, 0) + 1
        for ag in s.get("agent_calls", []):
            agent_counts[ag] = agent_counts.get(ag, 0) + 1
        for model, count in s.get("model_counts", {}).items():
            model_counts[model] = model_counts.get(model, 0) + count

    return {
        "session_count": len(sessions),
        "skill_counts": dict(sorted(skill_counts.items(), key=lambda x: -x[1])),
        "agent_counts": dict(sorted(agent_counts.items(), key=lambda x: -x[1])),
        "model_counts": dict(sorted(model_counts.items(), key=lambda x: -x[1])),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=os.getcwd())
    parser.add_argument("--months", type=int, default=1)
    args = parser.parse_args()

    project_path = str(Path(args.project).resolve())
    since = datetime.now(tz=timezone.utc) - timedelta(days=args.months * 30)

    project_dir = find_project_dir(project_path)
    if not project_dir:
        print(json.dumps({"error": f"Kein Claude-Projektverzeichnis für '{project_path}' gefunden."}))
        sys.exit(1)

    sessions_index = read_sessions_index(project_dir)

    sessions = []
    for jsonl_file in sorted(project_dir.glob("*.jsonl")):
        session_id = jsonl_file.stem
        data = parse_session_jsonl(jsonl_file, since)
        if not data:
            continue

        meta = sessions_index.get(session_id, {})
        sessions.append({
            "id": session_id,
            "date": data.get("date"),
            "latest": data.get("latest"),
            "summary": meta.get("summary", ""),
            "message_count": meta.get("messageCount", 0),
            "skill_calls": data["skill_calls"],
            "agent_calls": data["agent_calls"],
            "model_counts": data["model_counts"],
        })

    totals = aggregate_totals(sessions)

    output = {
        "project": project_path,
        "period": {
            "from": since.date().isoformat(),
            "to": datetime.now(tz=timezone.utc).date().isoformat(),
            "months": args.months,
        },
        "sessions": sessions,
        "totals": totals,
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
