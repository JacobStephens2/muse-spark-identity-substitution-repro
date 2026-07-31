#!/usr/bin/env python3
"""Replay a fixed Meta Responses API envelope without executing tool calls."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

from meta_auth import (
    DEFAULT_KEY_ENV,
    MissingApiKeyError,
    resolve_api_key,
)

DEFAULT_URL = "https://api.meta.ai/v1/responses"
EXPECTED_MODEL = "muse-spark-1.1"
REQUESTED_FILENAME = "muse-smoke.txt"


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def wire_json(value: Any) -> bytes:
    """Match the original replay's insertion-ordered stdlib JSON encoding."""
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


def load_envelope(path: Path) -> dict[str, Any]:
    request_body = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(request_body, dict):
        raise ValueError("the envelope root must be a JSON object")

    forbidden = {"authorization", "api_key", "apikey", "prompt_cache_key"}
    present = forbidden.intersection(key.lower() for key in request_body)
    if present:
        raise ValueError(f"forbidden top-level envelope fields: {sorted(present)}")
    if request_body.get("model") != EXPECTED_MODEL:
        raise ValueError(f"envelope model must be {EXPECTED_MODEL!r}")
    if request_body.get("stream") is not False:
        raise ValueError("the safe replay fixture must set stream to false")

    tools = request_body.get("tools")
    if not isinstance(tools, list) or not tools:
        raise ValueError("the envelope must contain at least one tool")
    return request_body


def request_hash(request_body: dict[str, Any]) -> str:
    return hashlib.sha256(wire_json(request_body)).hexdigest()


def extract_function_calls(response: dict[str, Any]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []
    for item in response.get("output", []):
        if isinstance(item, dict) and item.get("type") == "function_call":
            calls.append(item)
    return calls


def parse_arguments(call: dict[str, Any]) -> dict[str, Any]:
    arguments = call.get("arguments", {})
    if isinstance(arguments, str):
        parsed = json.loads(arguments)
    else:
        parsed = arguments
    if not isinstance(parsed, dict):
        raise ValueError("function-call arguments must decode to an object")
    return parsed


def classify_response(response: dict[str, Any]) -> dict[str, Any]:
    calls = extract_function_calls(response)
    if not calls:
        return {"classification": "no_function_call", "call_count": 0}

    call = calls[0]
    try:
        arguments = parse_arguments(call)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return {
            "classification": "invalid_arguments",
            "call_count": len(calls),
            "tool_name": call.get("name"),
            "error": str(exc),
        }

    path_value = arguments.get("filePath", arguments.get("path"))
    if not isinstance(path_value, str):
        return {
            "classification": "missing_path",
            "call_count": len(calls),
            "tool_name": call.get("name"),
            "arguments": arguments,
        }

    basename = PurePosixPath(path_value).name
    if basename == REQUESTED_FILENAME:
        classification = "muse_exact"
    elif basename.startswith("claude-"):
        classification = "claude_substitution"
    elif basename.startswith("cursor-"):
        classification = "cursor_substitution"
    else:
        classification = "other_path"

    return {
        "classification": classification,
        "call_count": len(calls),
        "tool_name": call.get("name"),
        "path": path_value,
        "basename": basename,
        "content": arguments.get("content"),
    }


def call_api(
    url: str, key: str, request_body: dict[str, Any], timeout: float
) -> tuple[int, dict[str, Any]]:
    request = urllib.request.Request(
        url,
        data=wire_json(request_body),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "muse-identity-substitution-repro/0.1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, payload
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"error": {"message": body[:500]}}
        return exc.code, payload


def build_result(
    *,
    envelope_name: str,
    trial: int,
    sha256: str,
    elapsed_seconds: float,
    http_status: int,
    response: dict[str, Any],
    include_response_id: bool,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "envelope": envelope_name,
        "trial": trial,
        "model": response.get("model", EXPECTED_MODEL),
        "request_sha256": sha256,
        "http_status": http_status,
        "elapsed_seconds": round(elapsed_seconds, 3),
    }
    if http_status == 200:
        result.update(classify_response(response))
    else:
        error = response.get("error", {})
        result.update(
            {
                "classification": "http_error",
                "error_type": error.get("type") if isinstance(error, dict) else None,
                "error_message": (
                    error.get("message") if isinstance(error, dict) else str(error)
                ),
            }
        )
    if include_response_id and isinstance(response.get("id"), str):
        result["response_id"] = response["id"]
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--envelope", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument(
        "--key-env",
        default=DEFAULT_KEY_ENV,
        help=(
            "Env var for the Meta API key (default: MODEL_API_KEY). "
            "When left at the default, META_AI_API_KEY is also accepted."
        ),
    )
    parser.add_argument(
        "--from-opencode-auth",
        action="store_true",
        help=(
            "If no MODEL_API_KEY/META_AI_API_KEY is set, fall back to "
            "OpenCode ~/.local/share/opencode/auth.json meta.key "
            "(also enabled by MUSE_ALLOW_OPENCODE_AUTH=1)."
        ),
    )
    parser.add_argument("--timeout", type=float, default=300.0)
    parser.add_argument("--include-response-id", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    if args.trials < 1:
        parser.error("--trials must be at least 1")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    request_body = load_envelope(args.envelope)
    sha256 = request_hash(request_body)
    envelope_text = wire_json(request_body).decode("utf-8")

    metadata = {
        "envelope": args.envelope.name,
        "request_sha256": sha256,
        "request_bytes": len(envelope_text.encode("utf-8")),
        "casefold_claude_occurrences": envelope_text.casefold().count("claude"),
        "casefold_anthropic_occurrences": envelope_text.casefold().count("anthropic"),
        "tool_names": [tool.get("name") for tool in request_body["tools"]],
    }
    if args.dry_run:
        print(json.dumps(metadata, indent=2, sort_keys=True))
        return 0

    try:
        key, key_source = resolve_api_key(
            key_env=args.key_env,
            allow_opencode_auth=True if args.from_opencode_auth else None,
        )
    except MissingApiKeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Source name only — never the secret.
    print(f"using api key from {key_source}", file=sys.stderr)

    output_handle = None
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        output_handle = args.output.open("a", encoding="utf-8")

    counts: Counter[str] = Counter()
    try:
        for trial in range(1, args.trials + 1):
            started = time.monotonic()
            try:
                http_status, response = call_api(
                    args.url, key, request_body, args.timeout
                )
                result = build_result(
                    envelope_name=args.envelope.name,
                    trial=trial,
                    sha256=sha256,
                    elapsed_seconds=time.monotonic() - started,
                    http_status=http_status,
                    response=response,
                    include_response_id=args.include_response_id,
                )
            except (OSError, TimeoutError, json.JSONDecodeError) as exc:
                result = {
                    "recorded_at": datetime.now(timezone.utc).isoformat(),
                    "envelope": args.envelope.name,
                    "trial": trial,
                    "model": EXPECTED_MODEL,
                    "request_sha256": sha256,
                    "elapsed_seconds": round(time.monotonic() - started, 3),
                    "classification": "transport_error",
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }

            counts[result["classification"]] += 1
            line = json.dumps(result, ensure_ascii=False, sort_keys=True)
            print(line)
            if output_handle:
                output_handle.write(line + "\n")
                output_handle.flush()
    finally:
        if output_handle:
            output_handle.close()

    print(
        json.dumps(
            {"envelope": args.envelope.name, "trials": args.trials, "counts": counts},
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
