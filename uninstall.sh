#!/usr/bin/env bash
# Remove khidi from the user-level Claude Code settings.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$REPO/bin/khidi"
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

[ -f "$SETTINGS" ] || { echo "no settings file at $SETTINGS"; exit 0; }

HOOK="$HOOK" SETTINGS="$SETTINGS" python3 - <<'PY'
import json, os

settings_path = os.environ["SETTINGS"]
hook_path = os.environ["HOOK"]

with open(settings_path) as fh:
    settings = json.load(fh)

entries = settings.get("hooks", {}).get("MessageDisplay", [])
kept = []
for entry in entries:
    hooks = [h for h in entry.get("hooks", []) if h.get("command") != hook_path]
    if hooks:
        kept.append({**entry, "hooks": hooks})

if kept:
    settings["hooks"]["MessageDisplay"] = kept
else:
    settings.get("hooks", {}).pop("MessageDisplay", None)
    if not settings.get("hooks"):
        settings.pop("hooks", None)

with open(settings_path, "w") as fh:
    json.dump(settings, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print("removed %s from %s" % (hook_path, settings_path))
PY

echo "Restart Claude Code for the change to take effect."
