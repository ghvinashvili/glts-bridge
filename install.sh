#!/usr/bin/env bash
# Register glts as a MessageDisplay hook and put the CLI on PATH.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINDIR="$HOME/.local/bin"
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

chmod +x "$REPO/bin/glts" "$REPO/bin/glts-hook"

mkdir -p "$BINDIR"
ln -sf "$REPO/bin/glts" "$BINDIR/glts"

[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.glts-backup"

"$REPO/bin/glts" on

echo
echo "CLI installed at $BINDIR/glts"
[ -f "$SETTINGS.glts-backup" ] && echo "Previous settings kept at $SETTINGS.glts-backup"
echo
echo "Try:  glts status        # is the bridge on?"
echo "      glts watch         # follow every conversion live"
echo "      glts try gamarjoba # convert one line"
echo "      glts off           # switch the bridge off again"
