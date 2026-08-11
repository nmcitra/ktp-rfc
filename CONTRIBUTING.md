# Contributing to KTP-RFC

We welcome contributions to the Kinetic Trust Protocol specifications! Thank you for your interest in improving this project.

## How to Contribute

The KTP-RFC project accepts contributions in several forms:

**Reporting Issues**: If you find a bug, typo, inconsistency, or technical error in the specifications, please [open an issue](https://github.com/nmcitra/ktp-rfc/issues). Be as specific as possible about the location and nature of the problem.

**Suggesting Enhancements**: For new ideas, changes to the specification, or additional RFCs, please open an issue for discussion before creating a pull request. This allows the community to provide feedback and ensures your effort aligns with the project's direction.

**Pull Requests**: All changes must be submitted via pull request and reviewed before merging. This ensures quality and consistency across the specification documents.

**Discussions**: For broader questions, philosophical debates, or implementation discussions, please use the [Discussions](https://github.com/nmcitra/ktp-rfc/discussions) tab.

## Pull Request Process

1. **Fork the repository** and create a new branch from `main` for your changes.

2. **Make your changes** in the appropriate files:
   - RFC documents are in the `rfcs/` directory
   - Documentation site content is in the `docs/` directory
   - JSON schemas are in the `schemas/` directory

3. **Update documentation** if your changes affect:
   - The main README.md
   - The documentation site navigation (mkdocs.yml)
   - Any cross-references between RFCs

4. **Test your changes** by building the documentation site locally:
   ```bash
   mkdocs serve
   ```
   Then visit http://localhost:8000 to preview your changes.

5. **Follow the RFC format**: If you're creating or modifying RFC documents, maintain consistency with the existing structure and style. Each RFC should include:
   - Abstract
   - Status of This Memo
   - Table of Contents
   - Numbered sections
   - References (if applicable)

6. **Submit your pull request** with a clear description of:
   - What problem you're solving or what you're adding
   - Why this change is necessary or beneficial
   - Any related issues or discussions

7. **Respond to feedback**: A maintainer will review your PR and may request changes. Please be responsive to feedback and willing to iterate.

8. **Merge approval**: Your PR will be merged once it has been approved by at least one maintainer and all CI checks pass.

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
| **normative** | `rfcs/`, `rfcs-txt/`, and the root-level companions (`glossary.md`, `constitution.txt`) |
| **site** | `docs/`, `mkdocs.yml`, and the theme assets the build needs |
| **governance** | licence, attribution, versioning, the DOI record |
| **tooling** | `scripts/`, `.github/`, `.gitignore` |

If your change adds a file that does not fit one of these, that is a decision to
make deliberately — add the category with its reason, or leave the file out.
Deleting a file to satisfy the script is never the right move on its own.

Editor backups (`*.bak`, `*~`, `*.orig`), build output (`site/`), virtualenvs,
and transient logs never land, whatever else is true. These are accidents rather
than decisions, and `.gitignore` covers them so the question does not come up.

## Specification Governance

Changes to the core protocol specifications (particularly KTP-CORE, KTP-IDENTITY, KTP-CRYPTO) require careful consideration and may involve broader community discussion. Please see [KTP-GOVERNANCE](rfcs/ktp-governance.txt) for details on the specification amendment process.

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before participating.

## Questions?

If you have questions about contributing, please open a [Discussion](https://github.com/nmcitra/ktp-rfc/discussions) or reach out via the repository's issue tracker.

## License

By contributing to this project, you agree that your contributions will be licensed under the same [Apache License 2.0](LICENSE) that covers the project.

---

Thank you for helping to build a more trustworthy future for autonomous systems!
