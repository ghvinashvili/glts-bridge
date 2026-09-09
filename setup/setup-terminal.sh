#!/usr/bin/env bash
# Make Georgian readable and typable in a terminal.
#
# Two problems, neither of them caused by GLTS Bridge, both of which have to be
# solved before Georgian in a terminal is usable at all:
#
#   1. Most monospace fonts have no Georgian glyphs, so the terminal falls back
#      to a proportional Georgian face. Inside a fixed cell grid those letters
#      overlap each other.
#   2. Debian's /etc/inputrc leaves convert-meta on, which turns the high bytes
#      of a UTF-8 character into ESC sequences, so Georgian typed at the bare
#      shell prompt comes out mangled.
#
# Run with --system to install for every user instead of just this one.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SYSTEM=0
[ "${1:-}" = "--system" ] && SYSTEM=1

if [ "$SYSTEM" = 1 ]; then
    FONT_TARGET=/etc/fonts/conf.d/60-georgian-mono.conf
    INPUTRC=/etc/inputrc
    RUN=sudo
else
    FONT_TARGET="$HOME/.config/fontconfig/conf.d/60-georgian-mono.conf"
    INPUTRC="$HOME/.inputrc"
    RUN=
fi

echo "==> font: routing monospace Georgian to DejaVu Sans Mono"
$RUN mkdir -p "$(dirname "$FONT_TARGET")"
$RUN install -m 0644 "$HERE/60-georgian-mono.conf" "$FONT_TARGET"
fc-cache -f >/dev/null
echo "    $FONT_TARGET"

echo "==> readline: keeping UTF-8 bytes intact at the prompt"
if [ ! -f "$INPUTRC" ]; then
    if [ "$SYSTEM" = 0 ]; then
        printf '$include /etc/inputrc\n' | $RUN tee "$INPUTRC" >/dev/null
    else
        $RUN touch "$INPUTRC"
    fi
fi
if grep -q '^set convert-meta off' "$INPUTRC"; then
    echo "    already set in $INPUTRC"
else
    grep -v '^#' "$HERE/inputrc-georgian" | grep -v '^$' | $RUN tee -a "$INPUTRC" >/dev/null
    echo "    appended to $INPUTRC"
fi

echo
echo "Open a new terminal window for both to take effect."
echo "Check the font with:  fc-match 'Monospace:lang=ka'"
