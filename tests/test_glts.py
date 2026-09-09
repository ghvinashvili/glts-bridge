#!/usr/bin/env python3
"""Round-trip checks for the glts hook. Run: python3 tests/test_glts.py"""

import json
import os
import subprocess
import sys

HOOK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "glts-hook")


def display(delta, message_id="test", final=True):
    payload = json.dumps({"message_id": message_id, "final": final, "delta": delta})
    proc = subprocess.run([sys.executable, HOOK], input=payload, capture_output=True, text=True)
    if not proc.stdout:
        return delta
    return json.loads(proc.stdout)["hookSpecificOutput"]["displayContent"]


CASES = [
    ("gamarjoba, rogor xar?", "გამარჯობა, როგორ ხარ?"),
    ("cxrilebi: 651 da momxmarebeli 14.", "ცხრილები: 651 და მომხმარებელი 14."),
    # Capitalised words are proper nouns and stay in Latin.
    ("Docker daayenda.", "Docker დააყენდა."),
    # Inline code survives untouched.
    ("gaushvi `ddev start` brdzaneba.", "გაუშვი `ddev start` ბრძანება."),
    # URLs, paths and flags survive untouched.
    ("saiti https://drupal.ddev.site misamarthze.", "საიტი https://drupal.ddev.site მისამართზე."),
    ("flagi --force ar ginda.", "ფლაგი --force არ გინდა."),
    # Digraphs beat single letters.
    ("shvidi", "შვიდი"),
    ("chemi", "ჩემი"),
    ("tchreli", "ჭრელი"),
    ("dzalian", "ძალიან"),
    ("ghame", "ღამე"),
    ("zhamiani", "ჟამიანი"),
    ("thbilisi", "თბილისი"),
    ("phoshti", "ფოშტი"),
    # Words on the keep list stay in Latin.
    ("gaushvi python skripti.", "გაუშვი python სკრიპტი."),
    ("server-ze database daayenda.", "server-ზე database დააყენდა."),
    # A Georgian ending after a hyphen is still converted.
    ("python-is versia.", "python-ის ვერსია."),
    ("docker-shi mushaobs.", "docker-ში მუშაობს."),
    ("GitHub-ze avtvirthe.", "GitHub-ზე ავტვირთე."),
    # A backslash escapes a word that is not on the list.
    ("\\gamarjoba da gamarjoba", "gamarjoba და გამარჯობა"),
    # Flags survive, and a hyphen inside a word is not mistaken for one.
    ("flagi --force da -v.", "ფლაგი --force და -v."),
    # An ending after a code span is still an ending, not a flag.
    ("`README.md`-shi devs.", "`README.md`-ში დევს."),
    ("`git commit`-is shetyobineba.", "`git commit`-ის შეტყობინება."),
    # An apostrophe breaks a digraph that would otherwise win.
    ("khid'ze", "ხიდზე"),
    ("khidze", "ხიძე"),
]


def streaming_case():
    """A fenced block opened in one chunk stays literal in the next."""
    first = display("aq aris kodi:\n```bash\nsudo apt install ddev\n", "stream", final=False)
    second = display("echo gamarjoba\n```\nes iyo kodi.\n", "stream", final=True)
    return first, second


def main():
    failures = 0
    for source, expected in CASES:
        got = display(source)
        if got != expected:
            failures += 1
            print("FAIL  %r\n  expected %r\n  got      %r" % (source, expected, got))

    first, second = streaming_case()
    if "sudo apt install ddev" not in first:
        failures += 1
        print("FAIL  fenced code was transliterated in the first chunk: %r" % first)
    if "echo gamarjoba" not in second:
        failures += 1
        print("FAIL  fence state was lost between chunks: %r" % second)
    if "ეს იყო კოდი." not in second:
        failures += 1
        print("FAIL  text after the closing fence was not converted: %r" % second)

    print("%d case(s) failed" % failures if failures else "all cases passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
