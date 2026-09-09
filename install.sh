#!/usr/bin/env bash
# Register khidi as a MessageDisplay hook in the user-level Claude Code settings.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$REPO/bin/khidi"
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

chmod +x "$HOOK"
mkdir -p "$(dirname "$SETTINGS")"
[ -f "$SETTINGS" ] || echo '{}' > "$SETTINGS"
cp "$SETTINGS" "$SETTINGS.khidi-backup"

HOOK="$HOOK" SETTINGS="$SETTINGS" python3 - <<'PY'
import json, os

settings_path = os.environ["SETTINGS"]
hook_path = os.environ["HOOK"]

with open(settings_path) as fh:
    settings = json.load(fh)

hooks = settings.setdefault("hooks", {})
entries = hooks.setdefault("MessageDisplay", [])

def already_there(entries):
    for entry in entries:
        for hook in entry.get("hooks", []):
            if hook.get("command") == hook_path:
                return True
    return False

if not already_there(entries):
    entries.append({"hooks": [{"type": "command", "command": hook_path}]})

with open(settings_path, "w") as fh:
    json.dump(settings, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print("registered %s in %s" % (hook_path, settings_path))
PY

echo "Backup of the previous settings: $SETTINGS.khidi-backup"
echo "Restart Claude Code for the hook to take effect."
