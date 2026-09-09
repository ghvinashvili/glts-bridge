#!/usr/bin/env bash
# Remove the khidi hook from Claude Code settings and take the CLI off PATH.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINDIR="$HOME/.local/bin"

"$REPO/bin/khidi" off

if [ -L "$BINDIR/khidi" ]; then
    rm -f "$BINDIR/khidi"
    echo "removed $BINDIR/khidi"
fi
