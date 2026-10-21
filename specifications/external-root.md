# Closed External Root Projection

**Proposed, unreleased External Root projection contract.**

The key words MUST, MUST NOT, REQUIRED, SHOULD and MAY have BCP 14 meanings.

## 1. Accountability, never a rootless design

KTP-Core's External Root requires an externally accountable party, exposed to
loss and able to revoke, with a finite declared chain terminating outside the
agent-trust graph. This proposal fixes the proof projection, not the scoring
computation, legal exposure, adjudication policy or instrument issuance format.

[Root Instrument](../schemas/root-instrument.json) is a closed discriminated
union, referenced by the [canonical proof schema](../schemas/trust-proof.json).
Every proof carries exactly one branch. Unknown fields or kinds, null required
values and mixed branches are invalid. A schema-valid projection is not evidence
that its instrument exists, its signatures pass or its lifecycle is current.

- `none`: only `kind`, `status: none`, required `reason`, and optional
  `diagnostic_ref`. It carries no exposure, capacity, issuer, end time, chain or
  other credit-bearing fields. It records a lapse/unavailability, never an
  optional design without an accountable party. Root credit is zero; Core's
  base-trust ceiling of 70 applies along with every tighter ceiling, leaving
  software agents below Operator until accountability is reestablished.
- `sponsorship_bond`: bond id and complete signed-bond digest, sponsor id,
  `bond_inputs` containing the authenticated sponsor E_base and stake percentage,
  `status`, `end_time`, terminator and chain length. The canonical software proof
  permits this only for Sponsored generations 0–2. The sponsor MUST equal the
  proof's sponsor, and the signed bond's sponsored subject MUST equal proof sub.
  Bond collateral/residual accounting does not become additional root credit.
- `external_attestation`: attestation id and complete signed-instrument digest,
  attestor id, exposure class, non-negative declared exposure, strictly positive
  anchored capacity, `status`, `end_time`, terminator and chain length. The
  issuer/subject and every projected value MUST match the authenticated source.
  Zero exposure is representable as an instrument input but supplies no credit:
  its proof projection is `none` with reason `no_exposure`.

The External Root is the authenticated person behind an instrument. Each active
projection carries `root_person`, identifying that person account. Behind the
person is an institution: the closed `{kind, reference}` terminator has kind
`employer`, `licensing_body` or `board` and an identifying URI. The person is
never encoded as the terminator. For a person subject, `root_person` MUST equal
the proof subject. A label or URI alone establishes neither identity nor the
person-to-institution chain.

Declared chain length is an integer from 1 through 12, matching the actual
finite noncyclic accountability chain, and MUST NOT exceed the installed hop
bound. Missing or invalid chains supply no credit. Zone enclosure receipts
are separate evidence and cannot replace accountability.

The same canonical Trust Proof and root union serve software agents and persons.
`subject_kind` MUST match independently authenticated subject context. Software
agents retain lineage, generation and sponsor rules. Persons use the external
attestation branch or a reasoned no-credit branch; their standing comes only
from signed acts and their terminator's standing under Core. Eligibility and
capacity remain separate prerequisites. Agent generation, lineage,
advancement floors and agent mass ceilings MUST NOT be defaulted for a person.
A receiving-zone ceiling established by a federation agreement remains applicable
to transferred person standing; it is not an agent-mass default.
Behavioral observations about a person MUST NOT enter their standing; the
proof's R/context describe the zone's environmental evaluation.

An instrument with undeclared terminator or chain length is a lapsed input,
not a valid active wire projection. The person-standing suite's
`PS03-nobody-behind-the-instrument` maps to `{kind: none, status: none,
reason: missing}` and zero root credit, with `external_root_missing <= 70`
and every tighter ceiling. Its `recordedAs: lapsed` is lifecycle test notation;
null active-instrument fields are not copied into the proof. The lifecycle
reason `undeclared` maps to wire `missing`, `withdrawn_for_cause` to the
corresponding `for_cause_*` reason, and `unresolved` to `unresolved_lapse`.
The authenticated lifecycle record retains the detailed original reason.

## 2. Authentication and exact projection

An issuer MUST reconstruct the projection from independently authenticated
instrument bytes and authoritative current lifecycle state. A relying verifier
MUST establish the same binding before accepting credit, either directly or
through an independently authorized verification service whose authenticated
result binds the exact instrument, state, profile, evaluation time and proof.
An Oracle signature or candidate-supplied digest alone is insufficient.

Instrument digests cover the **complete final signed instrument bytes**,
including its signatures/witnesses; SHA-256 or SHA-384 is selected by trusted
cryptographic policy, never by a candidate downgrade. Equal decoded fields do
not permit substituting different signed bytes. The independently installed
instrument profile fixes signed encoding, issuer roles/keys, witness rules,
subject, units, exposure interpretation, validity, chain semantics and current
status access. This decision introduces no universal bond/attestation signing
format. Without an approved mapping and trustworthy current status, use no
credit; an unrevoked signature is not evidence of current validity.

For bonds, authenticate the sponsor signature and required Oracle witness, exact
bond identity/subject/stake terms and authoritative live sponsor input snapshot.
The registered bond and current input evidence must agree; copying an old stake
or the collateral half cannot satisfy that check. For attestations, authenticate
the attestor, subject, exposure class and numerically comparable declared inputs.
All numeric inputs must be finite and in their declared bounds; boolean values
are not numbers. Capacity at or below zero, missing exposure interpretation or
unit mismatch is invalid. The evidence must establish irrecoverable,
non-transferable exposure under Core, not merely a positive JSON number.

`current` and `non_renewable` require a complete live instrument with integer
NumericDate `end_time`, matched exactly to its signed expiry. At issuance and
reliance, its start time must have arrived and current_time must be strictly
less than end_time; proof exp MUST NOT exceed it. Equal proof exp and end_time
is permitted; both cease to be valid at that boundary. Proof lifetime/readiness
and key ceilings remain independently binding. A future/lapsed instrument is
not made current by signing a newer proof. Lifecycle changes require immediate
reprojection and applicable invalidation; caches and the Core standing-cache
recommendation cannot extend a withdrawn root or override current-state checks.

The `none` reason is one of missing, expired, unverifiable, over_hop_bound,
invalid_instrument, for_cause_pending, for_cause_rejected, for_cause_sustained,
unresolved_lapse, misattestation or no_exposure. Future-dated instruments use
invalid_instrument. If verification cannot establish a reported lifecycle event,
use unverifiable rather than inventing cause. When multiple failures exist,
record one established applicable reason and retain all detailed evidence in
the owning lifecycle/evaluation record. The reason never changes zero credit.
For a software proof with no credit, the applicable ceiling list MUST include
`external_root_missing: 70`; verifiers enforce this independently of the list,
so omission or substitution cannot weaken the cap. Other ceilings still apply.

## 3. Lifecycle-to-proof table

Every event must bind the selected instrument's exact digest, subject, issuer,
effective time and authenticated event role. The deployment's adjudicator is
neither attestor nor subject. Findings before expiry must bind the recorded
claim and instrument. Conflicting or unavailable authoritative state supplies
no credit. Reduced proof status MUST NOT invent a detailed claim or finding.

| Authoritative state at evaluation | Proof projection | Credit and record obligations |
| --- | --- | --- |
| Current live bond/attestation; all checks pass | Selected kind, current, signed end_time | Eligible under Core and all ceilings |
| Withdrawal/termination without cause, before end | Selected kind, non_renewable, unchanged end_time | Eligible only until original end; irrevocably non-renewable |
| For-cause claim, finding pending, before end | none / for_cause_pending | Immediate zero; record claim, not a finding |
| Cause rejected before end | none / for_cause_rejected | No revival of this instrument; adjudication prices misattestation under Core/Identity |
| Cause sustained before end | none / for_cause_sustained | Zero; preserve finding and applicable bond release/accounting separately |
| For-cause claim still without finding at end | none / unresolved_lapse | Zero; no invented sustained/rejected result and no debit from lapse alone |
| Original end reached, including non-renewable | none / expired | Zero at equality; detailed prior history stays in lifecycle record |
| Misattestation invalidates the instrument | none / misattestation | Zero; debits belong to the owning adjudication/accounting record |
| Missing, unverifiable, invalid or over-hop instrument | none / corresponding reason | Zero; never infer a valid current branch from missing data |

At expiry an unresolved pending claim uses unresolved_lapse, rather than merely
expired, so that the required unresolved record is not concealed. Already
recorded findings remain recorded; the current projection may use expired at
end without erasing the finding. A rejected cause does not restore this
instrument; a fresh independently valid replacement may support later credit.
Termination without cause cannot erase a recorded for-cause zero-credit state.
The bond's residual/Ancestral Liability may survive closure but is never a live
bond root; attestation replacement is needed after tether release. A purported
renewal of an irrevocably non-renewable instrument is invalid, not a reset.

## 4. Concurrent strongest single instrument

Validate every available candidate against the same evaluation time, installed
profile and authoritative status. Invalid, unavailable, expired, zero-exposure
or for-cause candidates contribute no credit and cannot win. Compute admissible
instrument strength under the existing Core/provider contract; never sum or
otherwise combine attestations. Select the strongest single eligible instrument.
For an exact strength tie, select the lexicographically smallest complete
instrument digest (all candidates use the independently selected digest
algorithm). Candidate ordering cannot affect the result. This deterministic tie
rule is a proposed serialization choice, not a new scoring formula.

The proof identifies that selected signed instrument; every projected field
comes from it and its own lifecycle. Retain the candidate-set evidence,
per-candidate outcomes, provider/profile version, scores and tie decision in the
owning evaluation record so selection can be reproduced. A hidden or incomplete
required candidate set is not reproducible and MUST NOT be presented as complete.
A current independent backup may replace a zeroed candidate; that is selection
of another instrument, not revival or aggregation. If none are eligible, emit
none with an established reason and enforce the zero-root ceiling.

## 5. Vectors, migration and limits

[external-root-v1.json](conformance/external-root-v1.json) publishes closed-shape,
lineage/time/hop, signed-instrument substitution, lifecycle and concurrent
selection cases. Its complete ES256 signed test instruments and events use
explicitly unsafe public test keys. The test-only envelope is not a normative
production signing profile. Published strength answers are test values under
the existing Core contract; no formula for A or E is introduced here.

The proposed canonical proof fixtures are regenerated against the closed
projection and mandatory no-credit reason. This is revision of unreleased
fixtures, never rewriting released v2.1 proofs. Dependent request association contract/Decision Geometry contract fixtures
must be refreshed with the exact newly issued proof bytes and recomputed
associations/carriers when these proposals are composed. Old proposal fixtures
cannot bypass the adopted root schema merely because they once passed canonical Trust Proof contract.

Published v2.1 property bags remain interpretable only under their original
release, through an explicitly enabled isolated legacy adapter. Migration
reissues native proofs from authoritative signed instruments, current events
and profile state; no discriminator, cause or signature is invented by renaming
fields. Stored legacy proofs/signatures/provenance remain unchanged.

Schema success, fixed signatures and projection examples do not establish
real exposure, a trusted issuer/adjudicator, current status, provider correctness,
accountability chain truth or runtime enforcement. Actual implementations must
execute these cases against those mechanisms. No reference implementation or
first-conformance claim is offered.
