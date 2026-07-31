"""Resolve Meta Model API credentials for local retests.

Never log or return key material in error messages beyond env-var *names*
and path strings. Preferred order for Channel A (reproduce.py):

1. Explicit env name from ``--key-env`` (if not the default)
2. ``MODEL_API_KEY``
3. ``META_AI_API_KEY`` (operator alias used in some shells)
4. Optional: OpenCode ``auth.json`` ``meta.key`` only when
   ``allow_opencode_auth`` is true (CLI flag or env
   ``MUSE_ALLOW_OPENCODE_AUTH=1``)

Channel B (live OpenCode) still uses OpenCode's own auth store. Call
``ensure_opencode_meta_auth`` to seed ``auth.json`` from env when missing,
so one env export can drive both channels.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_KEY_ENV = "MODEL_API_KEY"
KEY_ENV_CANDIDATES = (DEFAULT_KEY_ENV, "META_AI_API_KEY")
OPENCODE_AUTH_ENV = "MUSE_ALLOW_OPENCODE_AUTH"
DEFAULT_OPENCODE_AUTH_PATH = Path.home() / ".local/share/opencode/auth.json"


class MissingApiKeyError(RuntimeError):
    """Raised when no usable Meta API key can be resolved."""


def env_truthy(name: str) -> bool:
    value = os.environ.get(name, "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def resolve_api_key(
    *,
    key_env: str = DEFAULT_KEY_ENV,
    allow_opencode_auth: bool | None = None,
    opencode_auth_path: Path | None = None,
) -> tuple[str, str]:
    """Return ``(api_key, source_label)``.

    ``source_label`` is an env var name or ``opencode-auth:<path>`` — never
    the secret itself.
    """
    if key_env != DEFAULT_KEY_ENV:
        key = os.environ.get(key_env)
        if key:
            return key, key_env
        raise MissingApiKeyError(
            f"{key_env} is not set; no API request was made"
        )

    for name in KEY_ENV_CANDIDATES:
        key = os.environ.get(name)
        if key:
            return key, name

    if allow_opencode_auth is None:
        allow_opencode_auth = env_truthy(OPENCODE_AUTH_ENV)

    if allow_opencode_auth:
        path = opencode_auth_path or DEFAULT_OPENCODE_AUTH_PATH
        key = read_opencode_meta_key(path)
        if key:
            return key, f"opencode-auth:{path}"

    tried = ", ".join(KEY_ENV_CANDIDATES)
    extra = (
        f"; or set {OPENCODE_AUTH_ENV}=1 to fall back to OpenCode auth.json"
        if not allow_opencode_auth
        else f"; also checked {opencode_auth_path or DEFAULT_OPENCODE_AUTH_PATH}"
    )
    raise MissingApiKeyError(
        f"no Meta API key found in {tried}{extra}; no API request was made"
    )


def read_opencode_meta_key(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    meta = data.get("meta")
    if not isinstance(meta, dict):
        return None
    key = meta.get("key")
    return key if isinstance(key, str) and key else None


def ensure_opencode_meta_auth(
    *,
    auth_path: Path | None = None,
    key_env: str = DEFAULT_KEY_ENV,
    provider: str = "meta",
) -> dict[str, Any]:
    """Ensure OpenCode has a Meta API key entry.

    Returns a small status dict suitable for dry-run / logging (no secrets):
    ``{"status": "already_present"|"written"|"unchanged_missing_key", ...}``.
    """
    path = auth_path or DEFAULT_OPENCODE_AUTH_PATH
    existing = read_opencode_meta_key(path)
    if existing:
        return {
            "status": "already_present",
            "auth_path": str(path),
            "provider": provider,
            "source": f"opencode-auth:{path}",
        }

    try:
        key, source = resolve_api_key(
            key_env=key_env,
            allow_opencode_auth=False,
        )
    except MissingApiKeyError as exc:
        return {
            "status": "unchanged_missing_key",
            "auth_path": str(path),
            "provider": provider,
            "error": str(exc),
        }

    data: dict[str, Any] = {}
    if path.is_file():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data = loaded
        except (OSError, json.JSONDecodeError):
            data = {}

    data[provider] = {"type": "api", "key": key}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    # Restrict permissions when possible (best-effort on non-POSIX).
    try:
        path.chmod(0o600)
    except OSError:
        pass

    return {
        "status": "written",
        "auth_path": str(path),
        "provider": provider,
        "source": source,
    }
