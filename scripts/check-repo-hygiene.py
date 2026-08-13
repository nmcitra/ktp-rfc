#!/usr/bin/env python3
"""Repo hygiene gate — what is allowed to land in the RFC repo, and nothing else.

This repo is the canonical normative artifact. Everything tracked here is
something a future RFC reader, an IETF datatracker submission, or a citation
resolves against. A file that is not needed for that has a cost and no benefit:
it enlarges the citable surface, it is one more thing to keep in parity, and
once published it cannot be quietly withdrawn.

WHY AN ALLOWLIST AND NOT A DENYLIST

    A denylist only ever catches the junk somebody already thought of. `.bak`
    files got in because nothing said they could not; the next thing gets in the
    same way. An allowlist inverts the burden — a new *kind* of file has to be
    named here, on purpose, with a reason, before it can land. The reason
    travels with the rule so a later reader knows why the category exists.

    The categories below are the answer to "is it needed for the spec?" Adding
    one is a decision. Deleting a file to satisfy this script is not.

Usage:  python3 scripts/check-repo-hygiene.py [--verbose]
Exit 1 if anything tracked falls outside the allowlist, or if a never-land
pattern is tracked at all.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Every tracked path must match exactly one of these. Category first so the
# report groups by intent rather than by directory.
ALLOWED = [
    ("normative", r"^rfcs/[^/]+\.md$",
     "the spec set — the reason this repo exists"),
    ("normative", r"^rfcs-txt/[^/]+\.txt$",
     "the canonical .txt half; parity with rfcs/ is checked separately"),
    ("normative", r"^(glossary\.md|constitution\.txt)$",
     "root-level normative companions to the set"),

    ("site", r"^docs/.*\.(md|json)$",
     "mkdocs content the site mirrors; docs/ is in vocabulary scope (#64, D)"),
    ("site", r"^docs/(javascripts|stylesheets|overrides)/.*$",
     "mkdocs theme assets — needed to build, not to read the spec"),
    ("site", r"^docs/assets/.*$",
     "mkdocs images — needed to build, not to read the spec"),
    ("site", r"^docs/rfcs$",
     "symlink to ../rfcs — how mkdocs serves the spec set without a second copy"),
    ("site", r"^mkdocs\.yml$", "the site build config"),

    ("governance", r"^(LICENSE|NOTICE|CITATION\.cff|\.zenodo\.json)$",
     "licensing, attribution, and the DOI record"),
    ("governance", r"^(CONTRIBUTING|CODE_OF_CONDUCT|PROVENANCE|VERSIONING|README)\.md$",
     "how the set is contributed to, versioned, and cited"),
    ("governance", r"^SECURITY-NOTES\.md$",
     "defects found in a published tag, readable before the release that "
     "corrects them — tags never move, so this is the only place they can go"),

    ("tooling", r"^scripts/[^/]+\.(py|sh)$",
     "the executable success criteria — checkable or they are aspirations"),
    ("tooling", r"^\.github/(workflows|ISSUE_TEMPLATE)/.*$",
     "CI and issue templates"),
    ("tooling", r"^\.github/PULL_REQUEST_TEMPLATE\.md$", "PR template"),
    ("tooling", r"^\.gitignore$", "the first half of this gate"),
]

# These never land, whatever else is true. A file matching one of these is not
# a category question — it is an accident that got committed.
NEVER = [
    (r"\.bak$", "editor backup — a .bak is never the authoritative copy"),
    (r"~$", "editor backup"),
    (r"\.sw[op]$", "vim swap file"),
    (r"(^|/)\.DS_Store$", "macOS directory metadata"),
    (r"(^|/)__pycache__/", "Python bytecode"),
    (r"\.py[cod]$", "Python bytecode"),
    (r"^(venv|env|ENV)/", "a virtualenv belongs to a machine, not to a repo"),
    (r"^site/", "mkdocs build output — regenerated, never authored"),
    (r"(^|/)node_modules/", "dependency tree"),
    (r"\.(log|tmp)$", "transient output"),
]


def tracked():
    out = subprocess.run(["git", "-C", HERE, "ls-files"],
                         capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p]


def audit(paths):
    never, unlisted, ok = [], [], {}
    for p in paths:
        hit = next((why for pat, why in NEVER if re.search(pat, p)), None)
        if hit:
            never.append((p, hit))
            continue
        cat = next((c for c, pat, _ in ALLOWED if re.match(pat, p)), None)
        if cat:
            ok.setdefault(cat, []).append(p)
        else:
            unlisted.append(p)
    return never, unlisted, ok


def main():
    verbose = "--verbose" in sys.argv
    paths = tracked()
    never, unlisted, ok = audit(paths)

    print("Repo hygiene — only what a future RFC reader needs\n")
    print(f"{'category':<14}{'files':>7}   what it is for")
    print("-" * 92)
    for cat in ("normative", "site", "governance", "tooling"):
        reasons = [why for c, _, why in ALLOWED if c == cat]
        print(f"{cat:<14}{len(ok.get(cat, [])):>7}   {reasons[0][:60]}")
    print()

    if never:
        print("MUST NOT BE TRACKED — these are accidents, not decisions:")
        for p, why in never:
            print(f"  {p:<52} {why}")
        print()

    if unlisted:
        print("NOT IN ANY CATEGORY — either it belongs and the allowlist needs a")
        print("new entry with a reason, or it does not belong and should go:")
        for p in unlisted:
            print(f"  {p}")
        print()

    if verbose:
        for cat in ("normative", "site", "governance", "tooling"):
            print(f"\n--- {cat} ({len(ok.get(cat, []))})")
            for p in ok.get(cat, []):
                print(f"  {p}")

    total = len(never) + len(unlisted)
    print(f"[{len(paths)} tracked · {len(never)} must-not-be-tracked · "
          f"{len(unlisted)} uncategorised]")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
