#!/usr/bin/env python3
"""check-title-abstract.py — an abstract must name the subject its title names.

Why this exists: KTP-ATTENUATION was retitled "Capability Attenuation
Specification" and its abstract went on saying "This document specifies
Digital Gravity" through the v2.1.0 tag. A reader who opened the document for
the subject in its title found a different subject in its first sentence.
Nothing checked that the two agree, so nothing failed.

Rule
  The subject of a document is its title with the series prefix
  ("Kinetic Trust Protocol (KTP) -") and the word "Specification" removed.
  At least one subject word MUST appear in the abstract. Words are compared by
  their first six letters, so "Cryptographic" matches "cryptography".

This is a floor, not a review. It catches a title and an abstract that share
no subject word. It does not catch an abstract that names the subject and then
describes something else.

Scope: rfc-src/*.md. Stdlib only. Exit 0 clean, 1 on any failure.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RFC_SRC = os.path.join(ROOT, "rfc-src")

# Words that say what kind of document this is, not what it is about.
GENERIC = {
    "a", "an", "and", "for", "from", "in", "of", "the", "to",
    "kinetic", "trust", "protocol", "ktp", "specification",
}
STEM = 6


def subject_words(title):
    subject = re.sub(r"^.*\(KTP\)\s*[-:–—]\s*", "", title)
    words = re.findall(r"[A-Za-z]+", subject.lower())
    return [w for w in words if w not in GENERIC]


def check(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    title = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.M)
    abstract = re.search(r"^--- abstract\s*\n(.*?)^--- middle", text, re.M | re.S)
    name = os.path.basename(path)
    if not title:
        return f"{name}: no title in the front matter"
    if not abstract:
        return f"{name}: no abstract"
    words = subject_words(title.group(1))
    if not words:
        return f"{name}: the title names no subject: {title.group(1)!r}"
    body = abstract.group(1).lower()
    if not any(w[:STEM] in body for w in words):
        return (f"{name}: the abstract names none of the title's subject "
                f"words ({', '.join(words)})")
    return None


def main():
    files = sorted(f for f in os.listdir(RFC_SRC) if f.endswith(".md"))
    failures = [msg for msg in (check(os.path.join(RFC_SRC, f)) for f in files) if msg]
    for msg in failures:
        print("FAIL", msg)
    print(f"{len(files)} documents, {len(failures)} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
