#!/usr/bin/env python3
"""check-section-refs.py — section citations must land on the section they name.

Why this exists: v2.0.0 inserted ktp-core §6.3 (the Carriage Interface) and
every later subsection of §6 moved down one. Headings are numbered by the
toolchain, so nothing in rfc-src/ changed and 32 citations across 12 files
pointed one section off through two published tags (SN-005). A number alone
cannot be checked against intent, so citations into another document carry the
heading they mean, and this gate checks number and heading agree:

    [KTP-CORE] Section 6.7 (Aggregation Algorithm)
    {{KTP-CORE}} Section 6.8 (Undefined Inputs)
    `ktp-core` §6.5 (Domain Weights)

Rules
  1. A section citation that names a heading in parentheses MUST resolve, in
     the cited document's generated numbering, to a heading with that text.
  2. Every section citation into an rfc-src document MUST resolve to a heading
     that exists.
  3. Citations with no heading are counted and reported; they do not fail. The
     count only goes down.

Numbering follows kramdown-rfc: the first `#` after `--- middle` is Section 1;
`##` is N.M; `###` is N.M.K. Fenced blocks (~~~ or ```) are skipped. Back
matter is lettered and is not resolved here.

Scope: rfc-src/*.md, specifications/*.md, specifications/conformance/*.json,
catalog/*.md, schemas/*.json. Stdlib only. Exit 0 clean, 1 on any failure.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RFC_SRC = os.path.join(ROOT, "rfc-src")

SCAN = [
    ("rfc-src", ".md"),
    ("specifications", ".md"),
    ("specifications/conformance", ".json"),
    ("catalog", ".md"),
    ("schemas", ".json"),
]

# [KTP-CORE] / \[KTP-CORE] / {{KTP-CORE}} / `[KTP-CORE]` / `ktp-core` / KTP-Core,
# followed by "Section" or "§", a dotted number, and an optional "(Heading)".
CITE = re.compile(
    r"(?P<doc>(?:\\?\[|\{\{|`\[?)?(?i:KTP-[A-Z][A-Z-]*)(?:\]|\}\}|\]?`)?),?\s+"
    r"(?:Section|§)\s*(?P<num>\d+(?:\.\d+)+)"
    r"(?:\s*\((?P<title>[^()\n]{1,80})\))?"
)
# A bare "Section N.M" with no document in front refers to the same document.
SELF = re.compile(
    r"\bSection\s+(?P<num>\d+(?:\.\d+)+)"
    r"(?:\s*\((?P<title>[^()\n]{1,80})\))?"
)

# Citations whose target heading no longer exists. Each is named here with the
# reason, never exempted by silence; the cross-document reference repair (the
# pass that re-homes them) deletes its line as it fixes the site, and the gate
# fails on an exemption that no longer matches anything, so the list only
# shrinks. Keyed by (file, cited document, cited section).
EXEMPT = {
    ("rfc-src/ktp-core.md", "ktp-sensors", "6.1"): "sensors §6 lost its subsections in the v2 rewrite; feed staleness now lives under §2.2",
    ("rfc-src/ktp-sensors.md", "ktp-sensors", "6.1"): "self-citation to a pre-v2 §6.1 (staleness default)",
    ("rfc-src/ktp-sensors.md", "ktp-sensors", "6.2"): "self-citation to a pre-v2 §6.2 (feed availability)",
    ("rfc-src/ktp-sensors.md", "ktp-sensors", "5.2"): "self-citation to a pre-v2 §5.2",
    ("rfc-src/ktp-sensors.md", "ktp-sensors", "7.1"): "self-citation; §7 (Security Considerations) has no subsections",
    ("rfc-src/ktp-transport.md", "ktp-core", "5.9"): "ktp-core §5 has five subsections; the aggregation-window rule moved",
    ("rfc-src/ktp-transport.md", "ktp-sensors", "6.2"): "pre-v2 sensors §6.2 (feed availability)",
    ("rfc-src/ktp-problems.md", "ktp-human", "10.3"): "ktp-human has no §10",
    ("rfc-src/ktp-problems.md", "ktp-governance", "3.1.5"): "ktp-governance §3 has no numbered subsections",
    ("rfc-src/ktp-threat-model.md", "ktp-human", "5.4"): "ktp-human §5 has three subsections",
    ("specifications/deployment-profile.md", "ktp-sensors", "6.1"): "pre-v2 sensors §6.1 (staleness default)",
    ("specifications/conformance/aggregation-empty-window-v1.json", "ktp-core", "5.9"): "ktp-core §5 has five subsections; the aggregation-window rule moved",
    ("catalog/index.md", "ktp-sensors", "6.2"): "pre-v2 sensors §6.2 (feed availability)",
    ("catalog/meta.md", "ktp-sensors", "6.2"): "pre-v2 sensors §6.2 (feed availability)",
    ("catalog/meta.md", "ktp-sensors", "6.1"): "pre-v2 sensors §6.1 (staleness default)",
    ("catalog/soul.md", "ktp-sensors", "6.1"): "pre-v2 sensors §6.1 (staleness default)",
}

# A parenthetical that cites an issue or starts "per " is provenance, not a
# heading claim.
PROVENANCE = re.compile(r"^(per\b|#\d|.*#\d)")

FENCE = re.compile(r"^(~~~|```)")


def heading_map(path):
    """{'6.7': 'Aggregation Algorithm', ...} from kramdown-rfc numbering."""
    nums = {}
    counters = [0, 0, 0, 0, 0, 0]
    in_middle = False
    in_fence = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if line.startswith("--- middle"):
                in_middle = True
                continue
            if line.startswith("--- back"):
                break
            if not in_middle:
                continue
            m = re.match(r"^(#{1,6})\s+(.*?)\s*(\{:.*\})?\s*$", line)
            if not m:
                continue
            level = len(m.group(1))
            counters[level - 1] += 1
            for i in range(level, 6):
                counters[i] = 0
            number = ".".join(str(c) for c in counters[:level])
            nums[number] = m.group(2).strip()
    return nums


def doc_key(token):
    return re.sub(r"[^a-z-]", "", token.lower())


def norm(s):
    s = re.sub(r"\s*\([^()]*\)\s*$", "", s)   # drop a heading's own trailing parenthetical
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    maps = {}
    for name in sorted(os.listdir(RFC_SRC)):
        if name.endswith(".md"):
            maps[name[:-3]] = heading_map(os.path.join(RFC_SRC, name))

    failures, bare, titled = [], 0, 0
    used = set()
    for sub, ext in SCAN:
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(ext):
                continue
            path = os.path.join(d, name)
            rel = os.path.relpath(path, ROOT)
            self_doc = name[:-3] if sub == "rfc-src" else None
            in_fence = False
            with open(path, encoding="utf-8") as fh:
                for lineno, line in enumerate(fh, 1):
                    if ext == ".md" and FENCE.match(line):
                        in_fence = not in_fence
                        continue
                    if in_fence:
                        continue
                    seen = set()
                    for m in CITE.finditer(line):
                        key = doc_key(m.group("doc"))
                        if key not in maps:
                            continue
                        seen.add(m.start("num"))
                        title = m.group("title")
                        if title and PROVENANCE.match(title):
                            title = None
                        check(rel, lineno, key, m.group("num"), title,
                              maps, failures, used)
                        if title:
                            titled += 1
                        else:
                            bare += 1
                    if self_doc:
                        for m in SELF.finditer(line):
                            if m.start("num") in seen:
                                continue
                            title = m.group("title")
                            if title and PROVENANCE.match(title):
                                title = None
                            check(rel, lineno, self_doc, m.group("num"),
                                  title, maps, failures, used)
                            if title:
                                titled += 1
                            else:
                                bare += 1

    for stale in sorted(set(EXEMPT) - used):
        failures.append(f"exemption {stale} matches nothing — remove it")
    for f in failures:
        print("FAIL", f)
    print(f"section citations: {titled} named, {bare} bare, "
          f"{len(used)} exempt by name, {len(failures)} failing")
    return 1 if failures else 0


def check(rel, lineno, key, num, title, maps, failures, used):
    target = maps[key].get(num)
    if target is None:
        if (rel, key, num) in EXEMPT:
            used.add((rel, key, num))
            return
        failures.append(f"{rel}:{lineno}: {key} Section {num} does not exist")
        return
    if title and norm(title) != norm(target):
        failures.append(
            f"{rel}:{lineno}: {key} Section {num} is '{target}', "
            f"citation names '{title}'")


if __name__ == "__main__":
    sys.exit(main())
