---
name: Specification proposal
about: Propose a new specification, profile, or change to existing normative text
title: '[PROPOSAL] '
labels: needs-triage
assignees: ''

---

<!-- Read CONTRIBUTING.md "The rules of the set" first. This template is the
     shape of a DECISIONS.md entry, so what you write here is what gets recorded. -->

## Summary

One paragraph. What changes, and where in the set it lands (`rfc-src/`, `specifications/`, `schemas/`, `catalog/`).

## Class

Pick one. A maintainer confirms it and the clock starts. See DECISIONS.md §2.

- [ ] Clarification — states a requirement the set already implies; no conformant implementation changes
- [ ] MINOR — a specification, profile, or optional feature enters the set
- [ ] MAJOR — a conformant implementation stops conforming
- [ ] Vocabulary — a term is added, removed, split, or changes meaning

## Already covered, and what is owed

Cite what the set already says. Write only what it doesn't.

| Requirement | Where the set already covers it | What remains |
|---|---|---|
| | | |

## Proposed text or shape

The normative content, or its outline. Interfaces, decision contracts, and conformance vectors are fixed here; formulas behind A or E are implementation-defined and do not go in normative text.

## The three questions

Answer each separately. See DECISIONS.md §3.

**A. Is it sound?** Does it hold under the Zeroth Law and against the rest of the set?

**B. Does it break a conformant implementation?** If yes, it is MAJOR and needs a migration path.

**C. Will someone build it?** Name the implementer, or the reference implementation that already exists.

## Evidence and its limits

What has been modeled, observed, or validated, and what has not. Vector runs and schema checks are prerequisites, not runtime certification.

## Compatibility

Written against tag: `v` <!-- e.g. v2.1.0 -->
Compatible with that release: yes / no / with migration (say which)

## Provenance

- Proposed by:
- Text edited by:
- Built first by (if anything exists):
- Reference implementation (pinned release, if any):

## Alternatives considered

What else could solve this, and why not that.
