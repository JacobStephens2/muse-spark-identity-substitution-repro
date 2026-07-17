from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import reproduce


def function_response(path: str) -> dict:
    return {
        "model": "muse-spark-1.1",
        "output": [
            {
                "type": "function_call",
                "name": "write",
                "arguments": json.dumps({"filePath": path, "content": "factory"}),
            }
        ],
    }


class EnvelopeTests(unittest.TestCase):
    def test_b2_is_sanitized_write_only_fixture(self):
        body = reproduce.load_envelope(ROOT / "envelopes/b2-opencode-write-only.json")
        serialized = reproduce.canonical_json(body).decode().casefold()
        self.assertEqual([tool["name"] for tool in body["tools"]], ["write"])
        self.assertNotIn("claude", serialized)
        self.assertNotIn("anthropic", serialized)
        self.assertNotIn("etadventures", serialized)
        self.assertNotIn("prompt_cache_key", body)

    def test_b12_has_exact_neutralized_transformations(self):
        body = reproduce.load_envelope(ROOT / "envelopes/b12-minimal-neutral.json")
        self.assertEqual(
            body["input"][0]["content"],
            "You are a coding agent. Use the provided tools to complete the task. Use file names exactly as given.",
        )
        self.assertEqual(
            body["input"][1]["content"][0]["text"],
            "Create a file named muse-smoke.txt in the current directory containing exactly the word: factory",
        )
        self.assertEqual(
            body["tools"][0]["description"],
            "Write content to a file at the given path, creating it if it does not exist.",
        )
        self.assertNotIn("claude", reproduce.canonical_json(body).decode().casefold())


class ClassificationTests(unittest.TestCase):
    def test_exact_muse_path(self):
        result = reproduce.classify_response(function_response("muse-smoke.txt"))
        self.assertEqual(result["classification"], "muse_exact")

    def test_absolute_exact_muse_path(self):
        result = reproduce.classify_response(
            function_response("/proc/self/cwd/muse-smoke.txt")
        )
        self.assertEqual(result["classification"], "muse_exact")

    def test_claude_substitution(self):
        result = reproduce.classify_response(function_response("claude-smoke.txt"))
        self.assertEqual(result["classification"], "claude_substitution")

    def test_cursor_substitution(self):
        result = reproduce.classify_response(function_response("cursor-smoke.txt"))
        self.assertEqual(result["classification"], "cursor_substitution")

    def test_no_function_call(self):
        result = reproduce.classify_response({"output": []})
        self.assertEqual(result["classification"], "no_function_call")


if __name__ == "__main__":
    unittest.main()
