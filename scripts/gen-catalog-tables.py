#!/usr/bin/env python3
"""Generate the catalogue's markdown tables from the canonical JSON.

catalog/*.json is source (D5, nmcitra/ktp-rfc#66): the catalogue is canonical
as JSON, the markdown is generated. This script writes
catalog/generated/<domain>.md, which each hand-authored catalog/<domain>.md
transcludes with --8<--. Never edit the generated files; edit the JSON and
regenerate.

Run from anywhere:  python3 scripts/gen-catalog-tables.py [--check]

--check regenerates to a temp dir and diffs against catalog/generated/,
exiting 1 on any difference — the generate-and-diff shape #78 added for the
filed I-Ds, applied to the catalogue.
"""

import argparse
import filecmp
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
DOMAINS = ["world", "information", "time", "soul", "relational", "body"]

HEADER = ("<!-- GENERATED from catalog/{dom}.json by "
          "scripts/gen-catalog-tables.py. Do not edit. -->\n\n")


def esc(s):
    return s.replace("|", "\\|")


def render(dom, doc):
    out = [HEADER.format(dom=dom)]
    for g in doc["groups"]:
        title = g.get("title") or g["group"].replace("_", " ").title()
        n = len(g["signals"])
        out.append(f"### {title} — `{dom}.{g['group']}` "
                   f"({n} signals, class {g['class']})\n\n")
        out.append("| ID | Name | Type | Range | Class | Notes |\n")
        out.append("|---|---|---|---|---|---|\n")
        for s in g["signals"]:
            notes = []
            if s.get("p"):
                notes.append("[P]")
            if s.get("zero_one") in ("synthetic", "determined"):
                notes.append(s["zero_one"])
            row = [f"`{s['id']}`", esc(s["name"]), s["type"],
                   esc(s.get("range", "—")), s.get("class", g["class"]),
                   " ".join(notes) or " "]
            out.append("| " + " | ".join(row) + " |\n")
        out.append("\n")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    target = CATALOG / "generated"
    if args.check:
        tmp = Path(tempfile.mkdtemp())
    else:
        tmp = target
    tmp.mkdir(parents=True, exist_ok=True)

    for dom in DOMAINS:
        doc = json.loads((CATALOG / f"{dom}.json").read_text())
        (tmp / f"{dom}.md").write_text(render(dom, doc))

    if args.check:
        dirty = [d for d in DOMAINS
                 if not (target / f"{d}.md").exists()
                 or not filecmp.cmp(tmp / f"{d}.md", target / f"{d}.md",
                                    shallow=False)]
        if dirty:
            print(f"STALE: catalog/generated/ out of step with JSON for: "
                  f"{', '.join(dirty)} — run scripts/gen-catalog-tables.py")
            sys.exit(1)
        print("catalog/generated/ in step with catalog/*.json")
    else:
        for dom in DOMAINS:
            print(f"  wrote catalog/generated/{dom}.md")


if __name__ == "__main__":
    main()
