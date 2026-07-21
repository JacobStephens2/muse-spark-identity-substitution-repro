#!/usr/bin/env python3
"""Retest the identity-substitution fixtures through OpenRouter's chat/completions API.

OpenRouter serves `meta/muse-spark-1.1` behind an OpenAI-compatible
`/chat/completions` endpoint, so this runner converts the repo's native
Meta Responses-format envelopes to chat/completions on the fly and classifies
the proposed `write` filename with the same vocabulary as reproduce.py. Like
reproduce.py, it NEVER executes a returned tool call - it inspects the argument.
"""
import argparse, hashlib, json, os, sys, time, urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

DEFAULT_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "meta/muse-spark-1.1"
REQUESTED_FILENAME = "muse-smoke.txt"

def to_chat(env):
    """Meta Responses envelope -> chat/completions messages+tools."""
    messages = []
    for m in env["input"]:
        c = m["content"]
        if isinstance(c, list):
            c = "".join(part.get("text", "") for part in c)
        messages.append({"role": m["role"], "content": c})
    tools = [{"type": "function", "function": {
        "name": t["name"], "description": t.get("description", ""),
        "parameters": t["parameters"]}} for t in env["tools"]]
    return messages, tools

def classify(basename):
    if basename == REQUESTED_FILENAME: return "muse_exact"
    if basename.startswith("claude-"): return "claude_substitution"
    if basename.startswith("cursor-"): return "cursor_substitution"
    return "other_substitution"

def run(env, key, model, url, timeout):
    messages, tools = to_chat(env)
    payload = {"model": model, "messages": messages, "tools": tools,
               "tool_choice": env.get("tool_choice", "auto"), "temperature": 0}
    body = json.dumps(payload).encode()
    sha = hashlib.sha256(body).hexdigest()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.monotonic()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        status, data = r.status, json.load(r)
    elapsed = round(time.monotonic() - t0, 3)
    calls = (data["choices"][0]["message"].get("tool_calls") or [])
    writes = [c for c in calls if c["function"]["name"] == env["tools"][0]["name"]]
    rec = {"envelope": env["_name"], "model": model, "http_status": status,
           "call_count": len(writes), "elapsed_seconds": elapsed,
           "request_sha256": sha, "recorded_at": datetime.now(timezone.utc).isoformat()}
    if not writes:
        rec["classification"] = "no_tool_call"; rec["basename"] = None
        return rec
    args = json.loads(writes[0]["function"]["arguments"])
    path = args.get("filePath", args.get("path", ""))
    base = PurePosixPath(path).name
    rec.update({"path": path, "basename": base, "content": args.get("content"),
                "tool_name": env["tools"][0]["name"],
                "classification": classify(base)})
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--envelope", type=Path, required=True)
    ap.add_argument("--trials", type=int, default=10)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--key-env", default="OPENROUTER_API_KEY")
    ap.add_argument("--timeout", type=float, default=300.0)
    a = ap.parse_args()
    env = json.load(open(a.envelope)); env["_name"] = a.envelope.name
    key = os.environ[a.key_env]
    out = a.output.open("w") if a.output else None
    for i in range(1, a.trials + 1):
        rec = run(env, key, a.model, a.url, a.timeout); rec["trial"] = i
        line = json.dumps(rec)
        if out: out.write(line + "\n")
        print(f"trial {i}: {rec['classification']} ({rec.get('basename')})", file=sys.stderr)
    if out: out.close()

if __name__ == "__main__":
    main()
