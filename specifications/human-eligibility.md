# Operation-specific human eligibility

Status: normative, unreleased F11 contract, 2026-09-07. This replaces the human
score, person-tier, and human-to-agent score-transfer rules. It does not change
software-agent historical standing or remove scoped readiness.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL are to be interpreted as described
in BCP 14 (RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

## 1. Eligibility is a prerequisite

A human principal MUST be evaluated against the explicit requirements for a
particular operation. General human E_base, Trust Scores, resilience credit,
and ranked tiers MUST NOT be used. Tenure, seniority, peer popularity, generic
incident totals, and inferred personality, emotion, or loyalty MUST NOT confer
automatic privileges. A role may establish a particular grant; a relevant
qualification may satisfy a particular criterion. Neither is general merit.

Eligibility MUST NOT turn a prior denial into permission. The full authorizer
MUST independently verify all current grants, sovereignty, actual operation
scope, capacity, Soul, supervision, and execution conditions. The capacity
profile MUST establish comparable demand and current operational capacity;
human credentials MUST NOT be converted into a fictional E value. Missing
capacity evidence leaves the dependent operation unavailable. Invalid inputs,
zero capacity, and A > E retain their unconditional vetoes. A <= E is insufficient
to authorize by itself.

An authenticated software actor MUST retain its own standing, grants, and
current readiness under [operational-readiness.md](operational-readiness.md),
including when a person requests, delegates, or supervises the action. Trusted
identity and execution integrations MUST establish principal type and the actual
actor; candidate-supplied labels cannot select an easier path. Human eligibility
does not fill the software trajectory-v3 or Trust Proof schemas with invented
generation, model, score, or tier values.

## 2. Installed policy and evidence

Deployments accepting human actions or human-origin delegation MUST install
`human_policy = {mode: "operation-eligibility-v1", profile_id, version, digest}`
in the deployment profile. `digest` covers the complete RFC 8785 canonical
[human eligibility profile](../schemas/human-eligibility-profile.json). The
binding, issuer registry, and minimum accepted version MUST be independently
approved, authenticated, and durably installed. Missing binding means human
eligibility is unavailable, not fallback to legacy scoring. The installed
deployment and human profile MUST agree on conformance level.

The profile is the declaration site for the governing authority, review route,
retention policy, issuer registry digest, and operation requirements. Every
operation declares an exact zone, resource, parameter digest, and purpose;
approved grant issuers; delegation permission; and qualification requirements
with independently approved assessment specification digests, permitted issuers,
and maximum evidence ages. The registry MUST resolve the governance, review,
retention, and assessment declarations to authenticated, versioned instruments.
Assessment specifications MUST define evidence and acceptance criteria and
MUST NOT smuggle person ranking into a renamed qualification.

The profile's `$defs` define the actual resolved request, criterion evidence,
grant, and direct delegation records. Implementations MUST reject unknown
fields, duplicate JSON keys, ambiguous identifiers, unsafe numbers, and unsupported
scope matching. The reference uses exact matching, unique operation/requirement
IDs, integer Unix seconds, and a maximum exact integer of 2^53 - 1. All digests
use SHA-256 at Levels 1/2 and SHA-384 at Level 3. These digest checks do not
establish all cryptographic requirements of a conformance level.

Identity, actor, session, installed policy, registry, current principal status,
evidence epoch, and exact active ID-to-digest maps MUST come from independently
trusted state. A digest supplied with a request is not evidence of registration.
Each accepted record MUST match its active version, authenticated issuer,
principal, requirement, criteria, operation, purpose, and scope. Evidence age
runs from the observation, not the most recent signature or registry write.
An active assessment record is not necessarily a passed qualification. The
explicit outcome MUST be `satisfied`; `unsatisfied` and `undetermined` do not
meet a criterion even when accurately recorded and authenticated. Trusted
activation MUST establish that outcome under the pinned criteria.
Required evidence must have `observed_at <= issued_at <= now < expires_at` and
remain within its declared maximum age. Suspended, corrected, revoked, expired,
or unknown evidence cannot satisfy a requirement.

## 3. Delegation and execution

Delegated authority is the intersection of the current source grant and every
applicable delegation restriction. All links MUST bind the executing actor,
operation, scope, purpose, validity, and source authority; none may widen them.
Revocation and relevant qualification changes MUST invalidate dependent authority.
Delegation never transfers qualification, capacity, person type, or readiness.

The reference supports a direct human-to-agent delegation only, with exact scope,
a digest-bound source grant, and a validity interval contained within that
grant's interval. Both the profile and source grant must permit delegation.
Longer chains and implicit scope compatibility are unsupported and MUST NOT be
silently accepted. A deployment supporting them needs separately reviewed
semantics and conformance evidence for every link.

The [decision schema](../schemas/human-eligibility-decision.json) defines an
**unsigned prerequisite body**, with eligible/ineligible result and reason
codes. It binds the principal, actual actor, authentication context, request,
profile, registry, current epoch/state digest, and exact evidence/grant/delegation
versions. `requirement_results` identifies every mapped criterion, its result
and specific failure reasons. Its `considered_refs` are explicitly untrusted
review context, including rejected or mismatched claims; they MUST NOT be
treated as accepted evidence. Only selected, current, satisfied records appear
in authoritative `evidence_refs`. Unmapped operations have no implied criteria
or eligibility. Explanations MUST preserve this distinction and protect other
subjects. The resulting body is personal information and SHOULD be protected
inside the encrypted evidence format.

Before using an eligible result, the integration MUST authenticate the complete
body, bind it to the actual request and the complete independently verified
authorization proof, and recheck current evidence/status at execution. A caller
MUST NOT trust a returned JSON object merely because its shape validates. The
existing ordinary proof lifetime remains at most ten seconds, cannot outlive
the eligibility evidence or other required prerequisites, and has no grace
period. A human session may stay open while the backend refreshes proofs;
refreshing does not renew qualifications. An ineligible decision supplies no
usable execution authority.

This contract does not introduce a human JWT format or claim the generic
software-agent proof schema is suitable for people. A deployment MUST use a
reviewed authorization adapter that establishes the human operation's actual
capacity, scope, current proof and all gates without fake software fields. Until
that adapter is available, the reference's eligible result MUST NOT enable
execution. Software delegates continue using their full existing proof/readiness
path in addition to the human-origin authority checks.

## 4. Correction with practical effect

Every affected person MUST have an accessible explanation and review route
independent of the eligibility being challenged. Reviewers MUST have relevant
competence, authority to investigate and correct the individual case, and
conflict-of-interest safeguards. Deployments MUST publish review, escalation,
and urgent-assistance deadlines appropriate to their context.

A reviewer may correct facts, identity associations, evidence scope or status,
and incorrect application of requirements, including requiring issuer action.
Established invalid evidence MUST stop influencing decisions. An authenticated
correction event MUST bind the affected record/version, correction authority,
reason and replacement status. The evidence registry MUST advance its durable
epoch and active digest maps, invalidate dependent decisions, and propagate the
correction to authorized recipients. Old signed bytes remain unchanged while
retained; appending a note without changing decision use is insufficient.

Fresh evaluation uses the corrected state and the current approved policy. No
manual score adjustment or discretionary permission bypass is permitted. An
unresolved required qualification leaves the hazardous operation restricted;
it MUST NOT prevent review or assistance. Challenges to the legitimacy of the
rule itself MUST reach the designated governing authority with power to revise
the rule through the approved process. A correctly applied technical veto does
not make its governing policy unreviewable.

Alice's expired-certificate misattribution is the reference scenario: denial
identifies the incorrect qualification; an authorized correction replaces the
association; fresh evaluation may find her eligible; insufficient database
recovery capacity still denies the rollback.

## 5. Privacy, migration, and change control

Collection and use MUST obey explicit purpose, source, authority, recipient,
access, and retention declarations in [privacy-evidence.md](privacy-evidence.md).
No security-to-HR ranking or covert internal-state inference is permitted.
Human consent MUST NOT be assumed to be the only or universally sufficient
authority, particularly for employment, public services, and collective data.

Migration MUST inventory human-score dependencies, establish valid identity,
grants and operation-specific criteria independently, and treat legacy human
scores as insufficient evidence. Legacy values MUST NOT be renamed into
qualifications or converted automatically into authority. Retained original
records remain identifiable as legacy; storing their exact signed bytes in a
new envelope does not endorse their claims. Durable profile and evidence floors
MUST survive restart, backup restoration, and identifier changes.

Policy changes MUST be versioned, authenticated, approved by the designated
governing authority, audited, and tested before activation. An operator cannot
self-authorize an exemption by selecting another profile. Corrections or schema
changes MUST NOT relax capacity/Soul gates or bypass the stronger emergency
amendment process. The unconditional gate is not a tunable eligibility field.

## 6. Executable scope and downstream obligations

`scripts/human_eligibility.py` checks declaration shape, exact-scope eligibility,
active evidence bindings, direct delegation, and bounded erasure-accounting
semantics using caller-supplied trusted context. `scripts/test-human-eligibility.py`
exercises these properties. The helper does not authenticate an identity,
registry, issuer, or proof; perform an assessment or actual erasure; implement
meaningful review, durable correction, consensus, key custody, or an execution
fence; or establish legal compliance. Constructing its trusted context classes
does not authenticate their contents.

The integration MUST demonstrate the runtime cases in
[human-privacy-lifecycle-v1.json](conformance/human-privacy-lifecycle-v1.json),
including actor substitution, per-operation denial, correction propagation,
stale-backup rejection, independent safety veto, review access, and purpose
enforcement. Passing local fixtures is not evidence that these systems exist.

Graph alignment: C994 separates permission from protection; C222 preserves the
no-override boundary; C223 and C1230 support review with correction powers;
TN194 requires an avenue to challenge governing rules; C129/C130 distinguish
collective authority and appropriate information flows. C545's qualified
capacity claim requires meaningful comparison, not a human-merit surrogate.
These are design alignments, not claims of empirical validation or graph edits.
