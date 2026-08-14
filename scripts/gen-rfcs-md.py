#!/usr/bin/env python3
"""gen-rfcs-md.py — generate rfcs-md/*.md, the clean render of rfc-src/*.md.

rfc-src/ is kramdown-rfc SOURCE, not something meant to be read raw: it
carries a front-matter block (title, docname, category, author, the
normative/informative reference table) and three bare section markers
(--- abstract / --- middle / --- back) that the kramdown-rfc + xml2rfc
toolchain consumes to build the five filed Internet-Drafts. Neither
GitHub's file viewer nor MkDocs strips this — browse rfc-src/ktp-core.md
directly and the front matter renders as a garbled text dump, and the
markers render as stray "--- abstract" lines in the middle of the page.

rfcs/ used to be a second, hand-authored, MkDocs-styled representation —
retired 2026-08-14 because it drifted (missing the entire Limits section)
with no gate able to see the omission; check-parity.py could only catch
rfcs/ asserting something rfc-src/ didn't, never rfc-src/ having material
rfcs/ lacked. Two independently-maintained representations of the same
normative text is the exact drift class this whole release existed to
kill in the catalogue and the schemas; it should not survive in the docs
build either.

rfcs-md/ replaces it as GENERATED output — mechanically derived, so drift
between it and rfc-src/ is impossible by construction rather than merely
gated. It feeds the GitHub Pages site alone (mkdocs.yml's nav, via the
docs/rfcs symlink, now repointed at rfcs-md/); it is not itself normative
and is never hand-edited.

What the strip does:
  - extract `title:` from front matter, emit as the H1
  - the --- abstract .. --- middle span becomes the intro paragraph(s)
  - --- middle .. --- back (or EOF if no --- back) is the body
  - --- back .. EOF, if present, is appended after the body
  - {{TOKEN}} citations -> [TOKEN] — matches the bracket form
    xml2rfc's own .txt output already uses for the five filed specs
  - kramdown's markdown-link-escaping (\\[ \\]) -> plain brackets;
    needed only inside the kramdown-rfc toolchain, not for a commonmark
    renderer

Usage:
  python3 scripts/gen-rfcs-md.py            regenerate rfcs-md/
  python3 scripts/gen-rfcs-md.py --check     regenerate to a temp dir,
                                              diff against rfcs-md/, fail
                                              on any difference
"""
import os
import re
import sys
import filecmp
import shutil
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "rfc-src")
CITATION = re.compile(r"\{\{([A-Z0-9-]+)\}\}")
ESCAPED_BRACKET = re.compile(r"\\([\[\]])")


def title_of(front_matter):
    m = re.search(r'^title:\s*"(.*)"\s*$', front_matter, re.M)
    return m.group(1) if m else None


def render(text, name):
    i = text.index("--- abstract\n")
    front = text[:i]
    j = text.index("--- middle\n")
    abstract = text[i + len("--- abstract\n"):j]
    k = text.find("--- back\n")
    if k == -1:
        body, back = text[j + len("--- middle\n"):], ""
    else:
        body, back = text[j + len("--- middle\n"):k], text[k + len("--- back\n"):]

    title = title_of(front) or name
    parts = [f"# {title}\n", abstract.strip(), body.strip()]
    if back.strip():
        parts.append(back.strip())
    out = "\n\n".join(p for p in parts if p) + "\n"

    out = CITATION.sub(r"[\1]", out)
    out = ESCAPED_BRACKET.sub(r"\1", out)
    return out


INDEX_HEADER = """# Kinetic Trust Protocol — Specifications

The 27 KTP specifications. Five are filed as Internet-Drafts and are also
available as generated plain-text RFCs in `rfcs-txt/`; all 27 are rendered
here for reading on the documentation site.

"""


def build_index(names):
    filed = {"ktp-core", "ktp-identity", "ktp-problems", "ktp-enforce",
             "ktp-conformance"}
    lines = [INDEX_HEADER]
    for name in names:
        text = open(os.path.join(SRC, f"{name}.md"), encoding="utf-8").read()
        i = text.index("--- abstract\n")
        title = title_of(text[:i]) or name
        mark = " *(filed Internet-Draft)*" if name in filed else ""
        lines.append(f"- [{title}]({name}.md){mark}")
    return "\n".join(lines) + "\n"


def main():
    check = "--check" in sys.argv
    outdir = tempfile.mkdtemp() if check else os.path.join(HERE, "rfcs-md")
    if not check:
        os.makedirs(outdir, exist_ok=True)

    names = sorted(f[:-3] for f in os.listdir(SRC) if f.endswith(".md"))
    for name in names:
        text = open(os.path.join(SRC, f"{name}.md"), encoding="utf-8").read()
        rendered = render(text, name)
        open(os.path.join(outdir, f"{name}.md"), "w", encoding="utf-8").write(rendered)
    open(os.path.join(outdir, "index.md"), "w", encoding="utf-8").write(build_index(names))

    if not check:
        # drop any stale generated file for a source that no longer exists.
        # "index" has no rfc-src counterpart by construction -- it is the
        # listing this script itself just wrote, not orphaned.
        keep = set(names) | {"index"}
        for f in os.listdir(outdir):
            if f.endswith(".md") and f[:-3] not in keep:
                os.remove(os.path.join(outdir, f))
        print(f"generated {len(names)} file(s) into rfcs-md/")
        return 0

    live = os.path.join(HERE, "rfcs-md")
    live_files = set(f for f in os.listdir(live) if f.endswith(".md")) if os.path.isdir(live) else set()
    gen_files = set(f"{n}.md" for n in names) | {"index.md"}
    rc = 0
    if live_files != gen_files:
        missing, extra = gen_files - live_files, live_files - gen_files
        if missing:
            print(f"STALE: rfcs-md/ is missing {sorted(missing)}", file=sys.stderr)
        if extra:
            print(f"STALE: rfcs-md/ has orphaned {sorted(extra)}", file=sys.stderr)
        rc = 1
    for f in sorted(gen_files & live_files):
        if not filecmp.cmp(os.path.join(outdir, f), os.path.join(live, f), shallow=False):
            print(f"STALE: rfcs-md/{f} differs from regenerated output", file=sys.stderr)
            rc = 1
    shutil.rmtree(outdir)
    if rc == 0:
        print("rfcs-md/ in step with rfc-src/ (27 sources)")
    return rc


if __name__ == "__main__":
    sys.exit(main())
