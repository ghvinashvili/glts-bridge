"""The typing buffer behind the glts input method.

Kept free of IBus so it can be tested on its own: it holds the Georgian text
the user reads and the Latin text the application will receive, and keeps the
two in step as characters are added and removed.
"""

# Georgian letter -> the Latin spelling glts reads back as that letter.
LATIN = {
    "ა": "a", "ბ": "b", "გ": "g", "დ": "d", "ე": "e", "ვ": "v", "ზ": "z",
    "თ": "th", "ი": "i", "კ": "k", "ლ": "l", "მ": "m", "ნ": "n", "ო": "o",
    "პ": "p", "ჟ": "zh", "რ": "r", "ს": "s", "ტ": "t", "უ": "u", "ფ": "ph",
    "ქ": "q", "ღ": "gh", "ყ": "y", "შ": "sh", "ჩ": "ch", "ც": "ts", "ძ": "dz",
    "წ": "w", "ჭ": "tch", "ხ": "kh", "ჯ": "j", "ჰ": "h",
}

# Sequences the reader treats as one letter. If two neighbouring letters would
# accidentally spell one of these, an apostrophe is pushed between them: ხიდზე
# must not arrive as "khidze", which reads back as ხიძე.
AMBIGUOUS = ("tch", "dz", "gh", "zh", "kh", "sh", "ch", "th", "ph", "ts")


def needs_break(latin, addition):
    """True when joining these two would spell a digraph that is not meant."""
    if not latin or not addition:
        return False
    joined = latin[-1] + addition[0]
    return any(seq.startswith(joined) for seq in AMBIGUOUS)


class Buffer:
    def __init__(self):
        self.shown = ""  # Georgian, what the user reads
        self.sent = ""   # Latin, what the application receives

    def add(self, char):
        """Take one typed character. Georgian letters gain a Latin spelling."""
        latin = LATIN.get(char, char)
        if needs_break(self.sent, latin):
            self.sent += "'"
        self.shown += char
        self.sent += latin

    def backspace(self):
        """Remove the last character from both sides. False if empty."""
        if not self.shown:
            return False
        last = self.shown[-1]
        self.shown = self.shown[:-1]
        self.sent = self.sent[: len(self.sent) - len(LATIN.get(last, last))]
        if self.sent.endswith("'"):
            self.sent = self.sent[:-1]
        return True

    def take(self):
        """Empty the buffer and return the Latin text to commit."""
        latin = self.sent
        self.shown = ""
        self.sent = ""
        return latin

    def clear(self):
        self.shown = ""
        self.sent = ""
