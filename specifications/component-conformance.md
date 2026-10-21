# Component Conformance Profiles

**Proposed, unreleased component-profiles-v1 contract.**

The key words MUST, MUST NOT, REQUIRED, SHOULD and MAY have BCP 14 meanings.

## 1. Claims belong to implementers

A component claim is the implementer's own scoped statement, not an entitlement
or permission to execute. Basic, Standard and Full are whole-deployment claims.
A library or codec MUST NOT use those labels for itself. A component can fill
multiple roles, and multiple roles may share one package or process; package
layout, language and enforcement architecture are outside these profiles.

Claims MUST name an immutable published KTP release tag, the role profile and
version, exact implementation build, installed declaration/profile digest, and
all applicable vector suite paths, versions (by tag) and artifact digests.
The closed metadata shape is [component-claim.json](../schemas/component-claim.json).
Role ids ending `-v1` are the profile versions. The release tag resolves the
profile index and all normative requirements, schemas and suites at that tag in
`nmcitra/ktp-rfc`; a moving branch or an unreleased proposal is insufficient.
SHA-256 digests use `sha256:` followed by 64 lowercase hexadecimal characters.
Implementation build identifiers MUST identify immutable source/build artifacts;
the implementation URI MUST identify whose build is claimed. A digest over the
complete installed declaration/profile bytes MUST be supplied, including the
library's explicit semantic configuration when no deployment declaration is
consumed. Claim metadata MUST NOT supply or select runtime authorization policy.

Canonical wording:

> [Implementer] declares a [status] claim for [implementation URI] build [build],
> KTP [release tag], profile [role id], declaration digest [digest], using
> [suite path, tag, digest for each suite]; evidence: [report references].

For `assembled-deployment-v1`, append “assembled [Basic/Standard/Full]
deployment” and name the exact assembly. Component wording has no level suffix.
No alternate status or endorsement suffix belongs in this syntax.

Status labels are `proposed`, `specified`, `tested`, and
`independently reproduced`. They are evidence states, not automatic promotions:

- `proposed`: a bounded intended claim; no passing implementation asserted.
- `specified`: requirements, release/profile bindings and test plan are stated;
  no passing execution inferred.
- `tested`: all applicable required cases were executed successfully against
  the exact build and declaration, with results and failures disclosed. Runtime
  roles additionally require their actual behavior in the enforcement/issuance,
  storage or transport path, as applicable.
- `independently reproduced`: the tested result was repeated independently
  against the same artifacts and configuration, with actor, independence basis,
  procedure and result report. Adding a report label alone does not establish it.

Reports MUST bind the build, declaration, release, role, suites/case ids, test
harness and immutable version, environment, schedules, expected/observed results,
failures and limits. A claim with failures in required cases cannot be called
`tested` or `independently reproduced`. Evidence URLs and complete report byte
digests are required; mere schema success or a metadata checker pass is not
execution evidence. A claim checker MUST resolve the actual tagged artifacts
and report contents independently before assessing the asserted status.

## 2. Role requirements and suite index

The normative [versioned profile index](conformance/component-profiles-v1.json)
lists schemas, mandatory base vector suites, evidence class and exclusions for
each role. Paths there resolve **at the claim's published release tag**, not
against current `main`. The index's requirement identifiers refer to the
following stable clauses. Owning a role requires all its clauses, not just
passing a schema. A schema listed for a role constrains artifacts the role
actually produces or consumes; it does not grant a new issuing role.

| Requirement / role profile | Required scope and evidence | Exclusions |
| --- | --- | --- |
| CP-CORE / `core-evaluation-v1` | KTP-Core's Risk Factors, domain weights, standing/lineage, Soul, aggregation, undefined inputs, tier and Kinetic Envelope input/output contract; common Core contract's common-level cases. Execute deterministic provider outputs, including all five weighted factors and separately declared demand criticality and nonbinary supervision with tighten-only constraints. | Issuance, interception, storage, deployment assurance |
| CP-PROOF / `trust-proof-verifier-v1` | Canonical proof parsing/encoding and accepting/rejecting complete signatures with independently supplied role keys, issuer, audience, algorithm profile, time and conditional claims; execute the complete canonical proof suite. A codec MUST include the accepting/rejecting path to make this claim. | Issuance, truth of observations, permission or target enforcement |
| CP-ORACLE / `oracle-issuer-v1` | Trust Oracle component requirements, Core standing and independent Soul, canonical issuance, live readiness and proof-time ceilings. Execute generation and rejection against actual installed state and keys. Mesh claims additionally require the consensus suite and actual fault/recovery schedules. | Target interception and durable audit unless separately claimed |
| CP-PDP / `evaluator-pdp-v1` | Actual-request and proof association, requester/executor/delegation bindings, Core and all prior gates, current readiness, canonical Decision Geometry and its carrier when crossing a boundary; execute decisions against authenticated invocation context, including rejection/replay paths. | Interception, dispatch outcome and durable recording |
| CP-PEP / `pep-enforcement-v1` | PEP requirements on the actual protected path: complete proof/request binding, current prerequisites, Soul/capacity/prior vetoes, tighten-only constraints, atomic replay admission, exact expiry, cached/queued/session and outage/continuing-action safety. Capture attempted operations and target observations demonstrating denials cannot bypass enforcement. | Proof issuance and audit storage guarantees |
| CP-AUDIT / `flight-recorder-v1` | Flight Recorder and KTP-Audit requirements: complete geometry retention, trajectory integrity where used, declared purpose/access/retention/erasure, promised durability and recovery. Exercise append/read/recovery and tamper/failure paths in the actual store; stronger claims require their chaining/anchoring/replication evidence. | Enforcement, issuance and authority from historical records |
| CP-TRANSPORT / `transport-federation-v1` | KTP-Transport and, when enabled, KTP-Federation requirements on the actual transport path: authenticated endpoints, complete request/proof/carrier association, loss/reorder/duplicate/replay and failure handling, no lifetime extension, authority increase or replacement of a zone's evaluation. Exercise cross-boundary substitution and expiry. | Zone policy ownership, Core recomputation and end-target enforcement |
| CP-ASSEMBLY / `assembled-deployment-v1` | All roles mapped to exact installed builds/configurations, the chosen whole-deployment level and its assurance requirements, plus end-to-end integration/enforcement-path evidence and applicable cross-implementation/fault/recovery schedules. | Automatic inheritance of another build's evidence or any higher assurance level |

All required cases in each base suite apply. The following conditional suites
and normative schedules MUST additionally be covered when the corresponding
feature is installed or claimed; the declaration fixes applicability, never a
candidate request or a desire to omit a failing case:

- Mesh agreement: `oracle-consensus-v1.json` and the actual protocol's fault,
  membership, durable restart and signing schedules in oracle-consensus.md.
- Trajectory issuance/consumption: `trajectory-signatures-v3.json` and
  `trajectory-lifecycle-v3.json`, including durable head/cutover behavior.
- Human eligibility/privacy: `human-privacy-lifecycle-v1.json` and the relevant
  human-eligibility and privacy-evidence schemas and normative runtime cases.
- Emergency capability: `outage-safety-v1.json` plus emergency-policy.json and
  actual approval/activation/expiry/continuing-execution cases. Ordinary outage
  and proof-expiry behavior remains mandatory even without that feature.
- A declared substrate: its tagged vectors, including
  `ros2-reference-v0.1.json` when that substrate is claimed.

Core provider-specific vectors, per-role requirements and normative runtime
schedules remain mandatory even where the index has no standalone JSON suite
for them. There is no standalone base suite here proving complete transport,
federation, storage or provider behavior. Reports MUST enumerate those cases
and expected/observed outcomes against tagged clauses; an absent suite is not
a waiver. An unimplemented required behavior blocks the stronger evidence
status. This index neither adds formulas behind A/E nor manufactures a runtime.

## 3. Assembly and claim composition

An assembled claim MUST map all seven component roles to exact build URIs,
build identifiers, installed declaration digests and complete component-claim
digests. A shared build can fill several roles but MUST name each role and its
evidence separately. Assembly evidence MUST resolve the complete component
claims and their release/profile/suite bindings; they MUST match the installed
components, satisfy the required evidence state and be compatible with the
assembly's release. This version requires a single KTP release across an
assembly; mixed-release migration needs an explicitly published profile.

The assembled build/declaration identifies the actual installed composition,
including role-to-target wiring and common semantic/assurance configuration.
The deployment suite list includes the union of component suites and all
level-specific/conditional cases. An unused optional feature is declared
inactive; it does not remove an essential role (local transport is still
transport). All chosen Basic/Standard/Full assurance requirements remain due.

Assembly MUST execute end-to-end request, decision, enforcement and recording
paths, including blocked/failed operations, stale/mismatched bindings, missing
components, outages and restart. Passing a library's deterministic vectors
cannot demonstrate that the target is intercepted, vetoes are obeyed, records
are durable or a mesh is safe. Component evidence cannot be borrowed across
builds/configurations or replace these integration observations. A passing
assembly does not automatically confer standalone claims on its components.

## 4. Release, examples and evidence limits

No new profile is available under `v2.1.0` merely because that release is this
proposal's baseline. Actual use waits for a published immutable release
containing this index and its required artifacts. Existing v2.1 claims retain
their tagged meaning; component profiles are additive. common Core contract owns native-v3
Core changes. conformance claims contract owns replacement of the older general claim syntax.

[component-claims-v1.json](conformance/component-claims-v1.json) gives positive
metadata examples for all eight roles and negative cases for overclaiming,
missing roles, schema-only enforcement evidence, missing execution/independence,
and mismatched tags/digests/builds. Its `v0.0.0-claim-fixture` registry is
fictional and not a published KTP tag. All implementation/report URLs use
`example.invalid`. Acceptance there means only metadata consistency under a
hermetic test resolver, never a real conformance claim.

The schema and metadata examples specify closed shape, required base suites,
release inventory metadata, role coverage and report metadata bindings. They
do not retrieve reports, execute providers, validate component-claim digests,
determine conditional-feature applicability, assess independent reproduction
or demonstrate enforcement. Those remain explicit claimant and reviewer
obligations. Schema and fixture acceptance cannot promote a status by themselves.

No public reference implementation, first
builder or passing implementation is offered by this proposal.
