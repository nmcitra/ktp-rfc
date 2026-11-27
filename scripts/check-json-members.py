#!/usr/bin/env python3
"""check-json-members.py — no JSON object in the set names a member twice.

Why this exists: a JSON parser that meets the same member name twice in one
object keeps the last and says nothing. Two proposals that each add the same
member to a schema merge without a text conflict, and the result parses, so
every other gate reads a schema one of the two authors did not write. Nothing
checked for a repeated name, so nothing failed.

Rule
  In every tracked .json file under schemas/, specifications/ and catalog/,
  each object MUST name each of its members once. The file MUST also parse.

Scope: schemas/, specifications/, catalog/. Stdlib only. Exit 0 clean, 1 on
any failure.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCOPE = ("schemas", "specifications", "catalog")


def tracked():
    out = subprocess.run(["git", "ls-files", "--", *SCOPE], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    return sorted(p for p in out.splitlines() if p.endswith(".json"))


def repeated(text):
    """The member names an object in this text carries more than once."""
    found = []

    def pairs(items):
        seen = set()
        for name, _ in items:
            if name in seen and name not in found:
                found.append(name)
            seen.add(name)
        return dict(items)

    json.loads(text, object_pairs_hook=pairs)
    return found


def main():
    fails = []
    paths = tracked()
    for path in paths:
        try:
            names = repeated((ROOT / path).read_text(encoding="utf-8"))
        except ValueError as err:
            fails.append(f"{path}: does not parse: {err}")
            continue
        for name in names:
            fails.append(f'{path}: an object names "{name}" more than once')
    if fails:
        print("\n".join(fails))
        print(f"\ncheck-json-members: {len(fails)} failure(s)")
        return 1
    print(f"check-json-members: {len(paths)} files, each member named once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
