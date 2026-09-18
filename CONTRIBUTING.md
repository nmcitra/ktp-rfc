# Contributing to KTP-RFC

We welcome contributions to the Kinetic Trust Protocol specifications. Thank you for your interest in improving this project.

## The rules of the set

Read these before you write anything. They are the difference between a contribution that lands and one that stalls.

1. **Text, not code.** This repository holds normative text, schemas, and conformance vectors. Implementations live in their own repositories; a specification here cites a pinned release of one. Don't add code, generated readers, transcripts, or evidence bundles. The hygiene check will refuse them.

2. **Issue first, on a clock.** Every change starts as an issue with a class. A maintainer applies `decision-needed` and a `class:*` label, and the clock in [`DECISIONS.md`](DECISIONS.md) starts. Nothing is approved before its floor. Open the PR after the issue, not instead of it.

3. **Pin to tags.** Reference KTP by tag, never by `main`. State which release you profiled or built against, and whether your change is compatible with it. [`VERSIONING.md`](VERSIONING.md) says how.

4. **Interfaces and vectors are fixed; formulas are implementation-defined.** A specification in this set fixes the interface, the decision contract, and the conformance vectors. It does not publish the computation behind A or E. A conformant provider is one that reproduces the published decisions. Don't add a formula to normative text; add the vectors that any formula would have to satisfy.

5. **KTP names its terms.** Don't rename a protocol term to match your implementation's vocabulary. `scripts/check-vocabulary.py` is the authority on retired terms; the ones people most often reach for:
   - "Context Tensor" is retired. The catalogue is **Context Signals**; the scoring layer is the **Risk Factors**.
   - "God Mode" is retired. The top tier is **Admin Mode**.
   - The single-letter risk keys are retired. The JSON key is the name: `evidence_density`, `trust_trend`, `adversarial_pressure`, `moment_criticality`, `update_resistance`, `attestation_coverage`, and the `soul` veto, which is never a weighted key.
   - Physics words (mass, heat, momentum) survive only on lines marked *Analogy (informative)*.
   - "Internet" and "Web" are proper nouns.

6. **State the evidence limit.** Every claim says whether it is modeled, observed, or validated. Declaration checks, schema checks, and vector runs are prerequisites; they are never runtime certification, and a proposal must not present them as one.

7. **Provenance is recorded, not transferred.** Say who proposed it, who edited the text, who built it first, and whose implementation is the reference. The first implementer is recorded permanently. The specification stays governed by [`DECISIONS.md`](DECISIONS.md).

8. **Cite, don't restate.** If the set already says it, link the section. Spend your words on what the set doesn't say.

## How to contribute

**Report a defect.** A typo, inconsistency, or technical error in the specifications: [open an issue](https://github.com/nmcitra/ktp-rfc/issues) with the bug template. Be specific about the location.

**Propose a change.** A new specification, profile, or change to existing text: open an issue with the specification-proposal template. It asks for the class, the three questions, and the evidence limit, because that is what the decision record needs.

**Offer a reference implementation.** Something that runs against a specification here: open an issue with the reference-implementation template. It asks for a pinned release and the vectors you ran.

**Discuss.** Broader questions and implementation talk go in [Discussions](https://github.com/nmcitra/ktp-rfc/discussions).

## Pull request process

1. **Fork the repository** and branch from `main`.

2. **Edit the source, not the output.**
   - Internet-Draft-formatted specifications are authored in `rfc-src/`. `rfcs-md/` and `rfcs-txt/` are generated from it; `scripts/check-parity.py` fails if they drift.
   - Normative companions are in `specifications/`; their reference vectors in `specifications/conformance/`.
   - Schemas are in `schemas/`; the Context Signals catalogue in `catalog/`.
   - Site content is in `docs/`.

3. **Run the checks before you push.**
   ```bash
   scripts/check-all.sh
   ```
   That is the same sequence CI runs. Green locally, then open the PR.

4. **One PR per decision.** The PR names its issue and its entry in [`DECISIONS.md`](DECISIONS.md). A PR that carries two decisions gets split.

5. **Fill in the PR template.** It lists the gates. Every box is a real question.

6. **Respond to review.** A maintainer will review and may request changes.

7. **Merge.** Requires one maintainer approval, green checks, and an elapsed clock for the class.

## What belongs in this repository

This repository is the canonical normative artifact. Everything tracked here is
something a future RFC reader, an IETF submission, or a citation resolves
against — so a file that is not needed for that has a cost and no benefit. It
enlarges the citable surface, it is one more thing to keep in parity, and once
published it cannot be quietly withdrawn.

`scripts/check-repo-hygiene.py` enforces this, and it runs on every pull
request. It is an **allowlist**, not a denylist: a denylist only ever catches
the junk somebody already thought of, so a new *kind* of file has to be named in
the script, on purpose, with a reason, before it can land. Four categories exist
today:

| category | what it covers |
|---|---|
| **normative** | `rfc-src/`, `rfcs-md/`, `rfcs-txt/`, `specifications/`, `catalog/`, `schemas/`, and the root-level companions (`glossary.md`, `constitution.txt`) |
| **site** | `docs/`, `mkdocs.yml`, and the theme assets the build needs |
| **governance** | licence, attribution, versioning, decisions, the DOI record |
| **tooling** | `scripts/`, `.github/`, `.gitignore` |

If your change adds a file that does not fit one of these, that is a decision to
make deliberately — add the category with its reason, or leave the file out.
Deleting a file to satisfy the script is never the right move on its own.

Editor backups (`*.bak`, `*~`, `*.orig`), build output (`site/`), virtualenvs,
and transient logs never land, whatever else is true. These are accidents rather
than decisions, and `.gitignore` covers them so the question does not come up.

## Specification Governance

Changes to the specifications are made on a clock, through three questions, and recorded in [`DECISIONS.md`](DECISIONS.md). That file states the floor for each class of change, the labels that start the clock, and where every decision landed. [KTP-GOVERNANCE](rfcs-md/ktp-governance.md) describes governance *inside* the protocol, for zones and federations; it does not govern this repository.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.

## Questions?

If you have questions about contributing, please open a [Discussion](https://github.com/nmcitra/ktp-rfc/discussions) or reach out via the repository's issue tracker.

## License

By contributing to this project, you agree that your contributions will be licensed under the same [Apache License 2.0](LICENSE) that covers the project.

---

Thank you for helping to build a more trustworthy future for autonomous systems!
