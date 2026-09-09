#!/usr/bin/env python3
"""Both halves of the bridge must agree.

Type Georgian through the input method's buffer, send the Latin it produces
through the display hook, and the Georgian should come back unchanged.
Run: python3 tests/test_roundtrip.py [file-of-georgian-lines]
"""

import importlib.machinery
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ibus"))

from glts_buffer import Buffer  # noqa: E402

_loader = importlib.machinery.SourceFileLoader("glts_hook", os.path.join(ROOT, "bin", "glts-hook"))
_spec = importlib.util.spec_from_loader("glts_hook", _loader)
hook = importlib.util.module_from_spec(_spec)
_loader.exec_module(hook)

SENTENCES = [
    "გამარჯობა, როგორ ხარ?",
    "ხიდი ორივე მხარეს მუშაობს.",
    "დააყენე დოკერი და გაუშვი საიტი.",
    "ეს ტექსტი ლათინურად მოდის და ქართულად ჩანს.",
    "წყალი, ჭიქა, ძაღლი, ჟურნალი, ღამე, ხიდზე, თოვლი.",
    "მე რომ ვწერ, შენამდე ლათინური ასოებით უნდა მოვიდეს.",
]


def roundtrip(text):
    buffer = Buffer()
    for char in text:
        buffer.add(char)
    latin = buffer.take()
    return latin, hook.convert_delta(latin, "roundtrip", True)


def document_case():
    """A whole document must survive Georgian -> Latin -> Georgian."""
    text = "\n".join(
        [
            "# სათაური",
            "",
            "ეს არის `settings.json` ფაილი და https://drupal.ddev.site ბმული.",
            "ე.ი. აბრევიატურაც უნდა დაბრუნდეს.",
            "დრუპალ არის ქართული სიტყვა, Drupal კი პროდუქტის სახელი.",
            "",
            "```bash",
            "sudo apt install ddev",
            "```",
            "",
            "დასასრული.",
        ]
    )
    return text, hook.convert_delta(hook.to_latin(text, True), "doc", True)


def writing_case():
    """Latin drafted by the model must become the intended Georgian file."""
    draft = "# sathauri\n\nes aris `settings.json` da https://drupal.ddev.site.\n"
    want = "# სათაური\n\nეს არის `settings.json` და https://drupal.ddev.site.\n"
    return want, hook.convert_delta(draft, "write", True)


def main():
    lines = SENTENCES
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as fh:
            lines = [line.strip() for line in fh if line.strip()]

    failures = 0
    for text in lines:
        latin, back = roundtrip(text)
        if back != text:
            failures += 1
            if failures <= 10:
                print("FAIL  %s\n  latin %s\n  back  %s" % (text, latin, back))

    want, got = writing_case()
    if got != want:
        failures += 1
        print("FAIL  writing a document\n  want %r\n  got  %r" % (want, got))

    source, back = document_case()
    if back != source:
        failures += 1
        print("FAIL  document did not survive the trip")
        for a, b in zip(source.split("\n"), back.split("\n")):
            if a != b:
                print("  %r\n  %r" % (a, b))

    print("%d of %d line(s) failed" % (failures, len(lines)) if failures
          else "all %d line(s) round-tripped, document included" % len(lines))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
