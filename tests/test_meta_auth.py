from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import meta_auth


class ResolveApiKeyTests(unittest.TestCase):
    def test_prefers_model_api_key(self):
        env = {
            "MODEL_API_KEY": "from-model",
            "META_AI_API_KEY": "from-meta",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            key, source = meta_auth.resolve_api_key(allow_opencode_auth=False)
        self.assertEqual(key, "from-model")
        self.assertEqual(source, "MODEL_API_KEY")

    def test_falls_back_to_meta_ai_api_key(self):
        env = {"META_AI_API_KEY": "from-meta"}
        with mock.patch.dict(os.environ, env, clear=True):
            key, source = meta_auth.resolve_api_key(allow_opencode_auth=False)
        self.assertEqual(key, "from-meta")
        self.assertEqual(source, "META_AI_API_KEY")

    def test_explicit_key_env_only(self):
        env = {
            "MODEL_API_KEY": "from-model",
            "CUSTOM_KEY": "from-custom",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            key, source = meta_auth.resolve_api_key(
                key_env="CUSTOM_KEY", allow_opencode_auth=False
            )
        self.assertEqual(key, "from-custom")
        self.assertEqual(source, "CUSTOM_KEY")

    def test_missing_raises(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(meta_auth.MissingApiKeyError):
                meta_auth.resolve_api_key(allow_opencode_auth=False)

    def test_opencode_auth_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            auth_path = Path(tmp) / "auth.json"
            auth_path.write_text(
                json.dumps({"meta": {"type": "api", "key": "from-opencode"}}),
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {}, clear=True):
                key, source = meta_auth.resolve_api_key(
                    allow_opencode_auth=True,
                    opencode_auth_path=auth_path,
                )
        self.assertEqual(key, "from-opencode")
        self.assertTrue(source.startswith("opencode-auth:"))


class EnsureOpencodeAuthTests(unittest.TestCase):
    def test_already_present_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            auth_path = Path(tmp) / "auth.json"
            auth_path.write_text(
                json.dumps(
                    {
                        "meta": {"type": "api", "key": "existing"},
                        "other": {"type": "api", "key": "keep-me"},
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.dict(
                os.environ, {"MODEL_API_KEY": "new-key"}, clear=True
            ):
                status = meta_auth.ensure_opencode_meta_auth(auth_path=auth_path)
            data = json.loads(auth_path.read_text(encoding="utf-8"))
        self.assertEqual(status["status"], "already_present")
        self.assertEqual(data["meta"]["key"], "existing")
        self.assertEqual(data["other"]["key"], "keep-me")

    def test_seeds_from_env_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            auth_path = Path(tmp) / "auth.json"
            with mock.patch.dict(
                os.environ, {"META_AI_API_KEY": "seed-me"}, clear=True
            ):
                status = meta_auth.ensure_opencode_meta_auth(auth_path=auth_path)
            data = json.loads(auth_path.read_text(encoding="utf-8"))
        self.assertEqual(status["status"], "written")
        self.assertEqual(status["source"], "META_AI_API_KEY")
        self.assertEqual(data["meta"], {"type": "api", "key": "seed-me"})


if __name__ == "__main__":
    unittest.main()
