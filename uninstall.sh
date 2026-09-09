#!/usr/bin/env bash
# Remove the glts hook from Claude Code settings and take the CLI off PATH.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINDIR="$HOME/.local/bin"

"$REPO/bin/glts" off

if [ -L "$BINDIR/glts" ]; then
    rm -f "$BINDIR/glts"
    echo "removed $BINDIR/glts"
fi
