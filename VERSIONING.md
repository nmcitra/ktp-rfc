# Versioning and Release Policy

The Kinetic Trust Protocol is published as a single RFC series that versions
**as a set**. A release fixes the whole series at one point, so an
implementation can name one version and know which text every specification in
the set refers to.

## Tags

Tags are the version. They are bare and numeric:

```
vMAJOR.MINOR.PATCH
```

The descriptive name of a release — "Lovelace," "Provenance infrastructure" —
lives in the release **title** and notes, never in the tag. Pin to the tag.
Treat any descriptive suffix on an older tag as historical, not as a naming
convention to follow.

| Version | Tag | Name |
|---|---|---|
| 1.0.0 | `v1.0.0` | Reference Implementation (Lovelace) |
| 1.0.1 | `v1.0.1-provenance` | Provenance infrastructure |

> `v1.0.1-provenance` carries a descriptive suffix. That was a one-time
> deviation from the rule above and is left in place rather than rewritten,
> because published tags are not moved (see "Immutability"). Every tag from
> `v1.1.0` onward is bare.

## What each number means

- **MAJOR** — a normative change: a previously conformant implementation is no
  longer conformant. A term in a calculation changes shape, a permitted value
  is removed, a MUST is added or altered.
- **MINOR** — new normative material that does not invalidate existing
  conformant implementations: an added specification, an added optional
  capability, a clarified requirement that was already implied.
- **PATCH** — editorial only: typos, formatting, reference-link repair, prose
  that changes no requirement.

Ambiguity resolves upward. If a change *might* make a conformant implementation
non-conformant, it is MAJOR.

## What triggers a release

A release is a citable artifact — each one is archived to Zenodo with a DOI and
recorded in `CITATION.cff`. That bar is deliberate. A release happens when:

- a normative change lands (MAJOR),
- a specification enters or is retired from the set (MAJOR or MINOR),
- a stable citation point is needed by an implementer or a downstream
  specification, or
- a retraction is required (see below).

Editorial commits accumulate on `main` and ride the next release. They do not
get their own DOI.

## Immutability

**A published tag is never moved or deleted.** Whatever text was released under
a version stays reachable at that version, permanently. Downstream work pins to
a tag on that promise.

A correction — even a retraction of something wrong enough to warrant one — is a
**new release** that says so. It is never a quiet edit under an existing tag.

## Pinning guidance for downstream specifications

Reference KTP by tag, not by `main`. State the version you profiled or built
against. If a later release changes the material you relied on, your reference
still resolves to the text you actually used, and you upgrade deliberately
rather than by surprise.

## Current version

The latest release is authoritative. `CITATION.cff` names it; the repository
README links it.
