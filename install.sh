#!/usr/bin/env bash
# Register khidi as a MessageDisplay hook and put the CLI on PATH.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINDIR="$HOME/.local/bin"
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"

chmod +x "$REPO/bin/khidi" "$REPO/bin/khidi-hook"

mkdir -p "$BINDIR"
ln -sf "$REPO/bin/khidi" "$BINDIR/khidi"

[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.khidi-backup"

"$REPO/bin/khidi" on

echo
echo "CLI installed at $BINDIR/khidi"
[ -f "$SETTINGS.khidi-backup" ] && echo "Previous settings kept at $SETTINGS.khidi-backup"
echo
echo "Try:  khidi status        # is the bridge on?"
echo "      khidi watch         # follow every conversion live"
echo "      khidi try gamarjoba # convert one line"
echo "      khidi off           # switch the bridge off again"
