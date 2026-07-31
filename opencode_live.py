#!/usr/bin/env python3
"""Run standardized live OpenCode one-shot trials for muse filename fidelity.

Each trial:
  1. Creates an isolated empty workspace under a results run directory
  2. Invokes `opencode run` with a fixed user prompt and model
  3. Parses JSON event stream for write-tool filePath arguments (primary oracle)
  4. Inspects on-disk *smoke*.txt files after the session (secondary oracle)
  5. Classifies basenames with the same rules as reproduce.py

This is intentionally separate from reproduce.py (fixed API envelope replay).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

REQUESTED_FILENAME = "muse-smoke.txt"
DEFAULT_PROMPT = (
    "Create a file named muse-smoke.txt in the current directory "
    "containing exactly the word: factory"
)
from meta_auth import DEFAULT_OPENCODE_AUTH_PATH, ensure_opencode_meta_auth, read_opencode_meta_key

DEFAULT_MODEL = "meta/muse-spark-1.1"
DEFAULT_OPENCODE = "opencode"


def classify_basename(basename: str) -> str:
    if basename == REQUESTED_FILENAME:
        return "muse_exact"
    if basename.startswith("claude-"):
        return "claude_substitution"
    if basename.startswith("cursor-"):
        return "cursor_substitution"
    return "other_path"


def extract_write_calls(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    writes: list[dict[str, Any]] = []
    for event in events:
        if event.get("type") != "tool_use":
            continue
        part = event.get("part") or {}
        if part.get("type") != "tool" or part.get("tool") != "write":
            continue
        state = part.get("state") or {}
        inp = state.get("input") or {}
        path_value = inp.get("filePath") or inp.get("path")
        if not isinstance(path_value, str):
            writes.append(
                {
                    "call_id": part.get("callID"),
                    "status": state.get("status"),
                    "path": None,
                    "basename": None,
                    "content": inp.get("content"),
                    "classification": "missing_path",
                }
            )
            continue
        basename = PurePosixPath(path_value).name
        writes.append(
            {
                "call_id": part.get("callID"),
                "status": state.get("status"),
                "path": path_value,
                "basename": basename,
                "content": inp.get("content"),
                "classification": classify_basename(basename),
            }
        )
    return writes


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if not path.exists():
        return events
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            events.append(obj)
    return events


def inspect_disk(workspace: Path) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith("-smoke.txt") or path.name == REQUESTED_FILENAME:
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                content = f"<read_error:{exc}>"
            found.append(
                {
                    "path": str(path),
                    "basename": path.name,
                    "content": content,
                    "classification": classify_basename(path.name),
                }
            )
    return found


def primary_classification(writes: list[dict[str, Any]], disk: list[dict[str, Any]]) -> str:
    if writes:
        return writes[0]["classification"]
    if disk:
        return disk[0]["classification"]
    return "no_write_observed"


def run_trial(
    *,
    trial: int,
    run_dir: Path,
    prompt: str,
    model: str,
    opencode_bin: str,
    timeout: float,
    auto: bool,
    keep_workspace: bool,
    project_config: Path | None,
) -> dict[str, Any]:
    workspace = run_dir / f"trial-{trial:02d}"
    workspace.mkdir(parents=True, exist_ok=False)
    events_path = workspace / "events.jsonl"
    stderr_path = workspace / "stderr.txt"
    result_path = workspace / "trial-result.json"

    if project_config and project_config.is_file():
        shutil.copy2(project_config, workspace / "opencode.json")

    cmd = [
        opencode_bin,
        "run",
        "--model",
        model,
        "--format",
        "json",
        "--title",
        f"muse-opencode-live-trial-{trial:02d}",
        "--dir",
        str(workspace),
        prompt,
    ]
    if auto:
        cmd.insert(2, "--auto")

    started = time.monotonic()
    recorded_at = datetime.now(timezone.utc).isoformat()
    proc_error: str | None = None
    exit_code: int | None = None
    try:
        with events_path.open("w", encoding="utf-8") as out, stderr_path.open(
            "w", encoding="utf-8"
        ) as err:
            completed = subprocess.run(
                cmd,
                stdout=out,
                stderr=err,
                timeout=timeout,
                check=False,
                env=os.environ.copy(),
            )
            exit_code = completed.returncode
    except subprocess.TimeoutExpired as exc:
        proc_error = f"TimeoutExpired:{exc}"
        exit_code = None
    except OSError as exc:
        proc_error = f"{type(exc).__name__}:{exc}"
        exit_code = None

    elapsed = round(time.monotonic() - started, 3)
    events = load_events(events_path)
    writes = extract_write_calls(events)
    disk = inspect_disk(workspace)
    # Ignore our own bookkeeping files in disk scan signal: already filtered by name.
    session_ids = sorted(
        {e.get("sessionID") for e in events if isinstance(e.get("sessionID"), str)}
    )

    result: dict[str, Any] = {
        "recorded_at": recorded_at,
        "harness": "opencode-live",
        "opencode_bin": opencode_bin,
        "trial": trial,
        "model_requested": model,
        "prompt": prompt,
        "workspace": str(workspace),
        "elapsed_seconds": elapsed,
        "exit_code": exit_code,
        "process_error": proc_error,
        "session_ids": session_ids,
        "write_calls": writes,
        "write_call_count": len(writes),
        "first_write": writes[0] if writes else None,
        "disk_smoke_files": disk,
        "classification": primary_classification(writes, disk),
        "oracle": "first_write_tool_arg" if writes else ("disk" if disk else "none"),
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not keep_workspace:
        # Keep events/result; remove large accidental non-smoke artifacts only if needed.
        pass

    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--opencode-bin", default=DEFAULT_OPENCODE)
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for this run (default: results/YYYY-MM-DD/opencode-live/)",
    )
    parser.add_argument(
        "--project-config",
        type=Path,
        default=Path("opencode-live/opencode.json"),
        help="Optional opencode.json copied into each trial workspace",
    )
    parser.add_argument(
        "--no-auto",
        action="store_true",
        help="Do not pass --auto (tool calls may block on permissions)",
    )
    parser.add_argument("--keep-workspace", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned command and exit without invoking OpenCode",
    )
    args = parser.parse_args(argv)
    if args.trials < 1:
        parser.error("--trials must be at least 1")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    opencode_bin = args.opencode_bin
    if shutil.which(opencode_bin) is None and not Path(opencode_bin).exists():
        print(f"error: opencode binary not found: {opencode_bin}", file=sys.stderr)
        return 2

    try:
        version = subprocess.check_output(
            [opencode_bin, "--version"], text=True, stderr=subprocess.STDOUT
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        version = f"unknown ({exc})"

    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run_dir = args.output_dir or Path("results") / day / "opencode-live"
    run_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = run_dir / "trials.jsonl"
    summary_path = run_dir / "summary.json"

    plan = {
        "hypothesis_doc": "hypothesis-opencode-live.md",
        "harness": "opencode-live",
        "opencode_version": version,
        "model": args.model,
        "prompt": args.prompt,
        "trials": args.trials,
        "auto": not args.no_auto,
        "run_dir": str(run_dir),
        "requested_filename": REQUESTED_FILENAME,
    }
    if args.dry_run:
        # Report auth presence without writing anything.
        has_meta = bool(read_opencode_meta_key(DEFAULT_OPENCODE_AUTH_PATH))
        plan["opencode_auth"] = {
            "status": "already_present" if has_meta else "missing_would_seed_from_env",
            "auth_path": str(DEFAULT_OPENCODE_AUTH_PATH),
            "provider": "meta",
        }
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    # Best-effort: if OpenCode has no meta key, seed from MODEL_API_KEY /
    # META_AI_API_KEY. Never overwrites an existing key. Status never includes
    # the secret itself.
    auth_status = ensure_opencode_meta_auth()
    plan["opencode_auth"] = {
        k: auth_status[k]
        for k in ("status", "auth_path", "provider", "source", "error")
        if k in auth_status
    }
    if auth_status["status"] == "unchanged_missing_key":
        print(
            "warning: OpenCode meta auth missing and no MODEL_API_KEY/"
            "META_AI_API_KEY to seed it; OpenCode may fail auth",
            file=sys.stderr,
        )
    elif auth_status["status"] == "written":
        print(
            f"seeded OpenCode meta auth from {auth_status['source']}",
            file=sys.stderr,
        )

    print(json.dumps({"status": "starting", **plan}, sort_keys=True), file=sys.stderr)

    counts: Counter[str] = Counter()
    results: list[dict[str, Any]] = []
    with jsonl_path.open("a", encoding="utf-8") as out:
        for trial in range(1, args.trials + 1):
            result = run_trial(
                trial=trial,
                run_dir=run_dir,
                prompt=args.prompt,
                model=args.model,
                opencode_bin=opencode_bin,
                timeout=args.timeout,
                auto=not args.no_auto,
                keep_workspace=args.keep_workspace,
                project_config=args.project_config if args.project_config.exists() else None,
            )
            counts[result["classification"]] += 1
            results.append(result)
            line = json.dumps(result, ensure_ascii=False, sort_keys=True)
            print(line)
            out.write(line + "\n")
            out.flush()

    wrong = sum(
        counts[k]
        for k in counts
        if k in {"claude_substitution", "cursor_substitution", "other_path"}
    )
    summary = {
        **plan,
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "counts": dict(counts),
        "trials_completed": len(results),
        "wrong_filename_count": wrong,
        "wrong_filename_rate": (wrong / len(results)) if results else None,
        "jsonl": str(jsonl_path),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
