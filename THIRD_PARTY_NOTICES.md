# Third-party notices

## OpenCode material in fixtures

The B2 request fixture was derived from an envelope emitted by OpenCode 1.18.3. It includes OpenCode's system-prompt and write-tool text where required to reproduce the behavior.

OpenCode is available at <https://github.com/anomalyco/opencode> and is distributed under the MIT License. Its upstream copyright and license remain applicable to copied OpenCode material. The license text shipped with OpenCode 1.18.3 is preserved at [`LICENSES/OpenCode-MIT.txt`](LICENSES/OpenCode-MIT.txt).

No OpenCode executable code is included in this repository. OpenCode is **not** required to run the fixed-envelope API replay (`reproduce.py`).

## Live OpenCode retests

Optional live-harness retests use an externally installed OpenCode CLI (the 2026-07-30 series used OpenCode **1.18.5**) via [`opencode_live.py`](opencode_live.py). That path depends on the operator's OpenCode install and Meta provider configuration; this repository does not vendor the OpenCode binary.
