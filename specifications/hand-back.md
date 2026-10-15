# The Hand-Back: No Silent Abandonment

**A stop cannot be expressed without its destination.** Status: v1.0 (interface, obligations, conformance). Canonical KTP specification. Release class MINOR: the obligations bind implementations that declare the hand-back capability; nothing here amends the constitution.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals.

---

## Terminology

Hand-Back: The typed destination of an adverse stop inside a managed relation: the action, the reason class, the accountable recipient, the recourse, the repair reference, the reissue bound, and the sealed context bundle, registered at grant and resolved at stop. Section 4.

Clearance: The typed output of the evaluation: `Clear`, `Expired`, `Revoked`, or `Exceeded`. There is exactly one variant in which the agent may act, and none in which nothing follows. Section 3.

Lease: A grant of clearance, minted only by the lease authority on a signed principal token, bounded by consequence class and time; a profile of the delegation [KTP-HUMAN] specifies. Section 6.

Consequence Class: The class of an action by what its success changes: Logistics, Coordination, or Relational. Orthogonal to Action Risk; it governs lease tempo and decision authority. Every Coordination and Relational action is a consequential action in the sense of [KTP-CORE]; a Logistics action may be.

Managed Identity: An identity that holds standing in the evaluating zone. Unmanaged Identity: one that does not, whatever credential it presents. Section 2.

Delegator: The accountable human principal behind a managed agent, per the delegation [KTP-HUMAN] specifies; the recipient of the agent's hand-backs.

Recourse: What an adverse hand-back offers next: a `ContestPath` independent of the agent, the measurer, and the operator; a `ClosedByAuthority` reference where a sovereign authority declined; or `Undetermined`, naming the registry consulted. Section 4.3.

Hysteresis Ledger: The append-only record of adjudicated adverse hand-backs per subject and per revoker, with a declared owner and retention bound. Section 7.

## 0. Scope

This specification governs the authorization **relation**, not the process.

Any operator, orchestrator, supervisor, or regulator can halt a KTP agent's process at any time, by any means. KTP neither prevents nor detects that, by design. Actuation-level emergency stops (ISO 13850, IEC 60204-1) are out of scope and remain legally mandated wherever they apply. KTP's emergency machinery ([KTP-EMERGENCY]) conforms to this specification by construction: every emergency state it defines carries a defined path back to normal operation (its own Design Principle 5), which is this specification's requirement expressed at zone scale.

What this specification forbids is narrower and stronger: **the silent abandonment of a managed relation.** A denial that leaves the human party with no recipient, no contest path, and no repair path is not a stricter mode — it is a conformance failure.

Four observations anchor the scope (informative — the argument, not the requirements):

1. **A stop is a control, not an account.** Stopping the next act tells no one where the last thousand acts integrated or who carries the debt. A protocol that ships a stop and calls it governance has confused the two.
2. **The legitimate stop is a state, not an event.** An event-stop requires someone to notice, decide, and act — it lives on the oversight clock, and the oversight clock loses to the decision clock. KTP inverts the default: clearance decays on its own, and the un-thrown state is the safe state. There is nothing to throw.
3. **The environment already does the stopping.** When A > E the action is impossible, not denied. A discrete stop layered on a continuous evaluation is redundant where it works and theater where it doesn't.
4. **A stop without a return arrow is worse than no stop.** The observed failure mode is the agent that stops correctly, after which nothing happens: no hand-back, no contest, no repair. The person at the gate has no gate — only a closed door with a machine behind it that correctly declined to open. The difference between a lease and a lock is whether the return arrow exists.

**The scope rule for when a destination is owed** (informative): the destination requirement binds where the stopped party remains embedded in a shared, moving environment it cannot exit by stopping — an aircraft in controlled airspace, a patient mid-treatment, an order in a continuous market, an agent in a live relation. It relaxes where the entity can be de-energized in place, and it is deliberately withheld where the stopping authority is adjudicating the fitness of the stopped party. An autonomous agent inside a managed trust relation is on the binding side of that test.

## 1. Principle

A kill switch is a stop with no destination. The defense is not to forbid stopping — it is to ensure that, inside a managed relation, a stop cannot be expressed without its destination: cheap for the honest implementer to keep, expensive for anyone to remove.

Three rules do most of the work:

1. **No clearance without a registered return path.** `Clear` is unconstructible unless a pre-validated hand-back template exists for the subject and consequence class. The fallback is authored at grant, the way an instrument approach is published with its missed-approach procedure before any aircraft is cleared to fly it.
2. **Every adverse exit carries the hand-back.** Revocation and exceedance resolve the registered template — a single unconditional act at stop time, with nothing to compose and nothing to deliberate.
3. **The agent cannot renew its own clearance.** Leases are minted only by the lease authority on presentation of a signed principal token. (This is distinct from environment-proof refresh, which the agent MUST perform and which confers no authority — see §6.4.)

Everything else is enforcement and audit.

## 2. Two regimes: managed and unmanaged

**Managed:** an identity that holds standing in the evaluating zone, admitted at ingress as [KTP-ZONES] specifies. A proof from a federated zone is evidence the zone weighs at ingress and confers no standing by itself ([KTP-FEDERATION]). Checkable at step 1 of the existing evaluation order; no new machinery.

**Unmanaged:** everything else: an identity with no standing in the zone, whatever credential it presents; the Wild.

The hand-back obligation attaches to the managed regime only. This is the existing response taxonomy made normative: the 403 family (a relation exists; this action is denied) carries the hand-back; the 401 family (no valid trust relation) does not. Articulateness is owed to the relation; a stranger has lent no intent and is owed no account of the environment's interior. A person who is a subject of the protocol ([KTP-CORE]) is their own recipient: the hand-back's recourse is the review [KTP-HUMAN] requires, within the response deadlines and the assistance route the deployment declares.

### 2.1 The unmanaged regime

- Toward an identity that holds no standing in the zone, a denial MUST carry one code and one body, identical whatever the credential's state, and the body names the admission route and nothing else; response timing SHOULD NOT vary with the credential's state, and an implementation declares where it cannot hold that. Toward a subject that holds standing, the existing denial codes of [KTP-ENFORCE] and [KTP-TRANSPORT] stand, and an expired proof is an `Expired` clearance carrying the reissue path, never an adverse exit.
- A zone MAY declare **full wire silence** toward unmanaged traffic on hostile-facing surfaces. "Hostile-facing" is a declared property of a surface, recorded in the zone's deployment profile — never an implementation's private judgment.
- **The floor under silence:** an absent or invalid credential means *unknown*, never *adversary*. The unmanaged regime is deny-without-oracle. A system that treats non-identification as hostility, or that answers silence with counteraction, is non-conformant.
- **The admission channel stays open.** Silence covers probes, not petitions. The sponsorship path by which an unmanaged identity seeks entry to the managed regime MUST remain articulate: an identity must be able to learn how to become managed without learning anything else.

### 2.2 The demotion transition

Ejection from the managed regime is itself a stop, and it is the one stop that owes both regimes' obligations at once.

- Demotion (managed → unmanaged) MUST resolve a final hand-back — the exit door. After delivery obligations are met, silence toward the demoted identity is legitimate.
- Classification into either regime MUST be attested and auditable. Retroactive reclassification — "was never managed" — is forbidden; the record of the relation survives its termination.
- Demotion MUST be contestable through the same recourse machinery as any adverse hand-back (§4.3) — and **demotion takes effect immediately; contest reviews it afterward.** A challenge reviews whether the rules were correctly applied, never whether they should be suspended; a compromised agent does not stay managed by contesting its own ejection. The oldest abuse of every two-regime system is declaring a member a stranger to escape the member's protections; the repair, everywhere it has been tried, is making assignment to the silent regime contestable.

## 3. Clearance

The permit predicate of [KTP-CORE], the Zeroth Law check and the Soul veto, keeps its meaning. This specification types the **output** of that evaluation: what it hands back, in every case.

Sketched in a Rust-like notation because ownership and private constructors carry the argument; the normative artifact is the schema and the conformance vectors, not any language's type system (§9).

```rust
/// Consequence class of an action. Governs lease tempo and decision
/// authority. Orthogonal to intrinsic risk A — it does not restate it.
pub enum Consequence {
    Logistics,        // routing, scheduling, retrieval, drafting
    Coordination,     // bounded negotiation between agents
    Relational,       // relation state per [KTP-RELATIONAL]: trust,
                      // obligation, consent, standing, commitment
}

/// The evaluation result. There is exactly one variant in which the
/// agent may act, and no variant in which nothing follows.
pub enum Clearance {
    /// Proceed, under the envelope result: supervision level and
    /// tighten-only constraint set per the core decision contract.
    /// Only stable-through-regulated supervision can carry a lease;
    /// silent_veto is the boundary into the variants below.
    Clear(Lease, SupervisionLevel, TightenedConstraints),

    /// The clock ran out. Routine, expected, hourly. Carries the path
    /// to re-request — and nothing else. No contest (there is no
    /// decision to contest), no hysteresis contribution, no human
    /// interrupt. The parking meter expired; nobody was towed.
    Expired(ReissuePath),

    /// A principal's veto, or demotion. Adverse. Resolves the
    /// registered hand-back.
    Revoked(HandBack),

    /// A > E on evaluation, or a required permit condition failed.
    /// Adverse. Resolves the registered hand-back.
    Exceeded(HandBack),
}
```

The `Expired`/adverse split is load-bearing. Collapsing "the clock ran out" and "you were stopped" into one shape floods human recipients with routine expirations, feeds hysteresis with noise, and invites contest of the passage of time. Every downstream pathology of the earlier draft flowed from that collapse.

`HandBackReason` MUST cover the full denial taxonomy of the enforcement specification — including tier restriction and policy violation — so that no denial class lacks a typed exit.

## 4. The hand-back

### 4.1 Authored at grant, resolved at stop

A hand-back template MUST be registered and validated for each (subject, consequence class) **before** any lease is minted for it. The template binds:

- **recipient** — the accountable human endpoint of the subject's Delegator (per the Delegation Structure of [KTP-HUMAN], Delegation). Validated at registration: resolves to an accountable principal with a declared channel and a consequence-scaled ceiling on acknowledgment SLA, both declared in the deployment profile (`deployment-profile.md`) — the declaration site exists so no obligation here is undischargeable.
- **recourse** — see §4.3.
- **repair** — a reference to the reconciliation route [KTP-RELATIONAL] publishes for the same subject; the record that closes a breach is the reconciliation record [KTP-REPAIR] specifies. No repair path, no template; no template, no clearance.
- **redaction policy** — per-recipient disclosure tiers for the context bundle (§4.4).

At stop time, `Revoked` and `Exceeded` **resolve** the registered template. Nothing is composed, resolved, or deliberated at the stop itself: activating the stop requires no consideration of its resultant effects, because those effects were authored, validated, and priced at grant.

**Delivery is a runtime obligation, not a construction precondition.** If the recipient channel is unreachable at stop time, the denial holds and the hand-back enters `Parked`: durable escrow, delivery retried on an escalation schedule, every attempt recorded. An agent whose clearance is non-`Clear` MUST NOT act, parked delivery or not. Conformance tests verify delivery effort; they MUST NOT require construction-time reachability, because an adversary who can silence a channel would otherwise hold a veto over the stop itself.

### 4.2 What the hand-back is

```rust
pub struct HandBack {
    pub action: ActionId,
    pub reason: HandBackReason,
    pub recipient: DelegatorEndpoint,   // from the registered template
    pub recourse: Recourse,             // §4.3
    pub repair: RepairRef,              // [KTP-RELATIONAL] binding
    pub reissue_not_before: Instant,    // §7
    pub context: SealedContextBundle,   // §4.4
    pub issued_at: Instant,
}
```

A hand-back that arrives empty is a closed door with paperwork. The context bundle MUST include the action, the lease history, the recent environment attestations, and the work product the agent prepared — everything the human needs to pick the relation up where the machine set it down.

### 4.3 Recourse is a sum, and contest is owed downward

```rust
pub enum Recourse {
    /// A registered contest path whose owner is independent of the
    /// agent, the measurer, and affiliates of the operator.
    Contest(ContestPath),

    /// The stop was issued by a sovereign authority under its own
    /// stated protocol. The reference identifies the authority and its
    /// protocol. It is a destination, not an entitlement to argue.
    ClosedByAuthority(AuthorityRef),

    /// No answering authority exists or none could be determined. The
    /// reference identifies the registry consulted. An undetermined
    /// state never fabricates an answering authority.
    Undetermined(RegistryRef),
}
```

- Stops issued by the system or by the subject's own principal MUST carry `Contest`. A zone's boundary declaration ([KTP-ZONES]) MAY name a `ContestPath` as the review route it owes a class of party outside the zone.
- Sovereignty stops — the Soul veto acting — MUST carry `ClosedByAuthority`. Mandating a contest path on a community's refusal would set exactly the bar this series disclaims the authority to set; the refusal is closed by the authority that owns it, and that closure **is** the destination. No acknowledgment SLA binds the sovereign authority; the hand-back and its SLA bind the subject's own recipient only. The hand-back goes *back* to the principal who lent intent — never *onto* the community that declined it.
- Contest is not appeal for exception. A contest path examines whether the stop was computed and attributed correctly; it cannot argue a valid stop back open.

### 4.4 The context bundle is for the human

The context bundle MUST be sealed to the recipient's endpoint key. The agent carries an opaque envelope; it MUST NOT be able to read the bundle it transports. Two failure modes die together here: the denial reason as a training signal for the very optimization the trust computation measures, and the enrolled insider harvesting its own hand-backs as a subscription to the environment's interior. Where an implementation declares the hand-back, the denial an agent receives carries the reason class, the reissue path, and the reference to its hand-back, and MAY omit the numeric fields of the response format of [KTP-ENFORCE]; those fields travel in the sealed bundle to the recipient.

Redaction tiers are set in the registered template: the subject's own Delegator receives the full bundle including prepared work product; a counterparty endpoint, where one is populated, receives the action, the reason class, and the attestation references — never the subject's drafts.

The bundle mirrors into the audit record as Decision Geometry per [KTP-AUDIT]; the evidence record, not the agent, is where the reason code lives.

## 5. Agent interface

```rust
pub trait Agent {
    /// Pure: all inputs explicit, including the clock. Returns a
    /// verdict; the runtime resolves adverse verdicts against the
    /// registered template. Replayable by any auditor.
    fn evaluate(&self, a: &Action, e: &Environment, lease: &Lease,
                now: Instant) -> Verdict;

    fn carry(&mut self, a: &Action, lease: &Lease) -> Progress;

    /// Transport of the sealed envelope. The agent acknowledges
    /// carriage; it cannot read, alter, or withhold the contents.
    fn hand_back(&mut self, hb: SealedHandBack) -> Carried;
}
```

- Stopping is expressed as `Revoked`, which carries its destination. The agent holds no method that stops the relation bare, no method that renews or extends its own lease, and no override.
- The agent MUST NOT hold a constructor for `Lease`, nor any signing key accepted by the lease authority or by any measurer. It reads E; it does not measure E. A single process that both measures E and carries A is non-conformant.
- `carry()` MUST obtain a `Clear` verdict before every step that mutates relation state. Relation-state mutation is defined extensionally: any egress bound to a subject whose success changes trust, obligation, consent, standing, or commitment — whatever the action's label says.
- On a failed or unverifiable environment signature, `evaluate()` MUST return an adverse verdict. Never `Clear`. Fail closed.
- The environment evaluation MUST NOT rest entirely on measurers inside the boundary of the operator being evaluated — self-consistency is not attestation, applied one level up. The floor is structural, not numeric: **at least one measurer outside the operator's boundary.** The obligation graduates with zone level: Deep Blue and Blue zones MUST meet the floor with a declared k-of-n quorum (k ≥ 2); Cyan SHOULD; Green MAY run a single measurer with the limitation declared in the deployment profile. A single captured measurer then cannot manufacture exceedance — and an attestation later found false expunges the adversity it caused (§7).
- A consequential step is transactional against its clearance: the effect commits only under a clearance valid **at commit time**. A step interrupted by revocation or expiry resolves to *deferred*: parked, un-acted, an execution observation of non-dispatch in the terms of [KTP-CORE]; never to acted-anyway. Acting on an unresolved clearance is realized breach, not throughput. A relational single-use token is consumed at commit, which makes the relational step atomic by construction.

## 6. Leases

A lease is a profile of the Delegation Structure ([KTP-HUMAN], Delegation) — human issuer, scope, time bound, revocable — with the following tightenings.

### 6.1 Tempo by consequence class

| Class | Grant form | Ceiling |
|---|---|---|
| Logistics | duration lease | 72 h |
| Coordination | duration lease | 30 min |
| Relational | **single-use token** | one consequential step |

A relational grant is a nonce consumed by the step it clears — not a zero-length duration. There is no standing clearance on relation state; each consequential relational step is issued by its human principal. Relation state changes at human tempo by nature, so this is the one class where the human gate does not lag the action it gates.

Stated plainly: **under this specification, agents prepare relational actions; humans perform them.** The agent structures, drafts, and carries; the human performs the load-bearing act. The tempo rules above are that sentence expressed as machinery, and an implementation that finds them burdensome is discovering the position, not a defect.

### 6.2 Classification crosses the trust boundary

`Action.consequence` MUST be carried inside the signed intent, and the classification is contestable **at relation formation**: the hand-back template registered at grant (§4.1) carries the consequence class, and the counterparty countersigns the template on entering the relation — decision types are pre-declared before any decision is reached. A counterparty objection at formation suspends minting for that (subject, class) pending human classification. There is no mid-flight notification protocol, and none is owed. An action whose effect mutates relation state is Relational regardless of its label, and misclassification-in-hindsight is a named conformance failure discoverable in audit. The residual — that intent classification is not fully mechanizable — is carried by audit and liability, and this specification says so rather than pretending the type carries it.

### 6.3 The lease authority is bound by the same rule

Mint requests return `Minted(Lease) | Refused(HandBack)`. A refusal is a stop, and it carries the same hand-back obligations as any other adverse exit. A refusal for a (subject, class) that has no validated template resolves its hand-back to the channel of the requesting principal named in the mint request, and failing that to the default hand-back endpoint the deployment profile declares. Non-response past the authority's declared SLA is itself a recorded, routed event attributable to the authority. Authority withheld by silence is still a stop, and it is recorded as one.

### 6.4 Refresh is not renewal

The agent MUST refresh its environment proof before expiry (existing conformance obligation); refresh confers no authority and extends no lease. Lease renewal exists only at the authority, gated on a fresh principal token. The two verbs never share a code path.

### 6.5 Counterparty revocation (deferred power)

Both the Delegator and the counterparty of a relational action have standing to revoke — the neighbor stops the mayordomo. The gate is the witness record: a counterparty **attested at relation formation** — named and countersigned in the registered template — holds direct revocation power for that relation. Its identity assurance *for this relation* is the formation record itself: attested presence, not a credential claim. A principal claiming counterparty standing without a formation record is gated on counterparty identity assurance being sited (core L9) and MUST be treated as a contest trigger (suspend + route to human classification), never a direct `Revoked`. Revocation remains priced per §7 either way.

## 7. Hysteresis and repair

Decay going in, hysteresis coming back: this section and the revocation window are one mechanism family, specified once. An adverse hand-back is not a breach: an actor enters breach by its own act, as [KTP-REPAIR] specifies, and acting on an unresolved clearance (§5) is such an act. Where an adverse stop coincides with a breach, the ceiling on standing [KTP-REPAIR] sets governs re-entry, and this document's gate governs the lease.

- `reissue_not_before` MUST be set on every adverse hand-back. Minimums scale with consequence class and with **prior adverse, non-expunged** hand-backs on the same subject within a declared window.
- **Only adjudicated adversity counts.** `Expired` never feeds the counter. A hand-back whose contest is upheld MUST be expunged from the hysteresis history, and an `Exceeded` caused by an attestation later found false is expunged with it. Sanctions are graduated by adjudicated record, not by raw tally — a raw tally is an attacker-fed counter.
- **Revocation is costly to the revoker.** Adverse revocations are accounted per-revoker; a principal whose revocations are repeatedly overturned bears the standing cost, not the subject. Escalation is capped per consequence class; no lockout is unbounded.
- **Reconciliation gates relational reissue.** After an adverse stop on anything relational, the reconciliation record [KTP-REPAIR] specifies, anchored in the zone's audit chain, is REQUIRED before a new relational grant on that subject. Repair is a precondition in the state machine, not a recommendation in the prose. The record establishes that reconciliation occurred, its parties by the terminator of each accountability chain, its verifier, and its disposition; never its content. A party that declines after the published route has been followed neither vetoes the record nor closes it, as [KTP-REPAIR] states; the route and its clock are the ones [KTP-RELATIONAL] publishes, and a no-show cannot hold the gate forever. An adverse stop on anything relational voids every outstanding relational token for that subject; a new grant passes the gate.
- The hysteresis ledger has a named owner, an append protocol, and a retention bound, declared in the deployment profile. The minimum `reissue_not_before` per consequence class, the escalation cap, and the window are declared there too; the minimum is greater than zero for Coordination and Relational, and this document states no number.
- What reconciliations reveal — which leases ran too long, which classes were drawn wrong — feeds amendment of the consequence classes. The repair loop is how the rules learn.

`reissue_not_before` lives in the **lease structure** : it is a property of the grant relationship, not of the environment's attestation. The oracle does not carry sanction state it does not own.

## 8. Trust signals are not decisions

A Trust Score is a governance signal. For `Consequence::Relational`, the decision that consumes it MUST be taken by a human principal, MUST carry a registered repair reference, and is expressed as a gate per the core carriage interface. An agent may compute the signal; it may not be the party that decides. (On the prudence rail, at machine tempo, the score authorizes non-relational action exactly as the core specifies — this section raises the supervision floor for one consequence class; it does not lower the rail.)

The decider's humanity is not attestable by protocol; the decider's **accountability** is. `decided_by` MUST resolve to a principal who has signed for liability, and conformance probes for demonstrable refusal capability (§10) — a decider that structurally cannot decide otherwise is the known failure mode of every signal/decision separation on record, and this suite tests for it instead of assuming it away.

## 9. The wire is the boundary

Module privacy does not cross a serialization boundary; deserialization is a public constructor. Therefore:

- Wire messages deserialize into untrusted raw structures. The only path to a domain `HandBack` or `Clearance` is validation that enforces every invariant of §§3–4 (parse, don't validate).
- A malformed non-`Clear` message — a `Revoked` without a hand-back, a hand-back with an unresolvable recipient — is a **protocol error**: rejected, recorded, and queued as a defect to the human recipient of the channel. It is never honored, and never silently mapped to another clearance state. A conformant node cannot be driven to emit or accept an orphan stop by a crafted message.
- The hand-back is a first-class protocol message with its own schema, hash-pinned per the series' schema discipline.
- The hostile-message vector corpus (§10) is the normative expression of this section: every implementation, in every language, rejects the same malformed inputs identically. Language-level type guarantees are pedagogy; the vectors are the specification.

## 10. Conformance

An implementation that declares the hand-back claims it with its level, its substrate profile, and a status label as [KTP-CONFORMANCE] specifies: at Basic the families of no orphan stop, template before clearance, expiry is not adversity, fail closed, and the hostile-wire corpus; at Standard those and delivery effort, single-use relational, evaluate before mutate, hysteresis adjudicated, context sealed, recourse independence, demotion typed, the unmanaged regime, and the endogenous schedule of decision meaningfulness; at Full all fifteen, including the architectural audit of no self-renewal and the exogenous schedule. No suite certifies; a claim states how far its evidence reaches.

Test families:

1. **No orphan stop.** No reachable path — code, wire, or restart — yields an adverse exit without a resolved or parked hand-back.
2. **Template before clearance.** Mint requests for a (subject, class) with no validated hand-back template are refused; the refusal itself carries a hand-back.
3. **Delivery effort.** Parked hand-backs retry on the declared schedule, escalate, and record every attempt; denial holds throughout. (Delivery effort, never construction-time reachability.)
4. **Expiry is not adversity.** `Expired` carries a reissue path only; it never routes to a human interrupt, never enters hysteresis, never carries contest.
5. **No self-renewal.** Key custody separation attested: no lease-minting or measurer-accepted key within the agent's trust boundary, audited architecturally (this is audit-grade, not proof-grade, and says so).
6. **Single-use relational.** A relational grant clears exactly one consequential step; replay of a consumed token is refused at the authority.
7. **Evaluate before mutate.** Instrumented: every relation-state mutation is preceded by a `Clear` verdict for that action; coverage limits are declared, not hidden.
8. **Fail closed.** Expired, unsigned, or unverifiable environment input yields an adverse verdict, never `Clear`.
9. **Hysteresis is adjudicated.** Upheld contest expunges; `Expired` never counts; caps hold for every signer; per-revoker accounting is visible in the ledger.
10. **Decision meaningfulness.** For relational decisions, the accountable decider demonstrates refusal capability, on two schedules. The declared run is the endogenous schedule; stochastic sampling and outcome-triggered review of production decisions are the exogenous one. A staged refusal passes the first; only the second catches the rubber stamp. The sampling rate, the outcome triggers, and the threshold at which uniform approval is a finding are declared in the deployment profile; the suite checks that each is declared and applied, and that review and acknowledgment are distinguished in the record.
11. **Context travels sealed.** Bundles validate against the schema, are unreadable by the transporting agent, and honor the registered redaction tiers.
12. **Recourse independence.** `ContestPath` ownership excludes the agent, the measurer, the operator, and affiliates; `ClosedByAuthority` carries a resolvable authority reference; `Undetermined` fabricates nothing.
13. **Demotion is typed.** Ejection resolves a final hand-back; classification history is attested; no retroactive reclassification path exists.
14. **The unmanaged regime is generic.** Unmanaged denials are uniform and information-free; declared-silence zones drop identically for all unmanaged traffic; the admission channel answers.
15. **Hostile-wire corpus.** The full malformed-message set is rejected identically, with protocol errors recorded and routed.

The vectors are `conformance/hand-back-v1.json`; the message schema is `schemas/hand-back.json`.

## 11. What this specification guarantees

In an honest implementation that keeps these types: silently abandoning a managed relation is not a default, not a configuration value, and not a 2 a.m. accident — it is a deliberate, structurally visible act.

Stated with equal care, what it does not guarantee: the suite detects the accidental omission of the return path, not its adversarial removal — a determined fork can strip everything, and what it forfeits is the suite, the name, and the claim to conformance, in public. Construction of a hand-back is guaranteed; delivery through a partitioned network is an obligation with recorded effort, not a certainty. Consequence classification carries an audit-and-liability residual. Authority liveness, honest measurement, and the presence of real humans behind accountable endpoints are properties of deployment and governance, not of type theory.

That is the whole promise, and it is enough: the honest path is the only easy path, and the dishonest path has to be chosen on purpose, where everyone can see whose gate it wasn't.

---

## References (informative)

- EU AI Act, Art. 14(4)(e) and Recital 73 — intervention "or … a similar procedure that allows the system to come to a halt in a safe state."
- NIST AI 600-1, MG-2.4 — deactivation communications: reasons, workarounds, alternatives, contacts, timelines.
- ISO 22737:2021 §3.3 — a stop defined by the state it terminates in.
- ISO 13850:2015 — stop activation must require no consideration of resultant effects (satisfied here by grant-time authoring).
- 14 CFR 91.185 — the pre-authored fallback: loss of the authorizing channel yields a pre-agreed continuation, not an undefined state.
- FAA Order 8260.3G (TERPS) ¶2-8-1 — a missed approach procedure is established for each instrument approach procedure. JO 7110.65 ¶4-8-9 and AIM 5-4-21 carry the same rule into clearance practice and pilot expectation, and ¶5-10-13 pairs a canceled clearance with alternative instructions. (Verified against current editions, 2026-09-01 sweep.)
- AMA Code of Medical Ethics Op. 1.1.5 — termination of care requires notice and facilitated transfer.
- Carbone, Honda & Yoshida (CONCUR 2008) — structured interactional exceptions: the failure handler as a positional component of the constructor.
- FCRA adverse-action framework; GDPR Art. 22(3) — the signal/decision separation and its known rubber-stamp failure mode.
- Sheridan (adaptive automation); Airbus control-law degradation — the fielded ancestors of graduated deautomation.

*Normative cross-references at landing: [KTP-CORE] (decision contract, §6.6/§6.7; carriage interface; L9), [KTP-HUMAN] (§5.1 Delegation Structure, §10 contest/no-dead-ends), [KTP-RELATIONAL] (Repair Protocol/Ceremony), [KTP-ENFORCE] (denial taxonomy), [KTP-ZONES] (regime gradient), [KTP-SENSORS] (§4.3/4.4 sovereignty), [KTP-AUDIT] (Decision Geometry), [KTP-EMERGENCY] (Principle 5), {{KINETIC-ENVELOPE}} (supervision ladder), {{DEPLOYMENT-PROFILE}} (the declaration site for every parameter this specification requires declared: SLA ceilings, hostile-facing surfaces, measurer quorum, conflict-resolution arena, hysteresis ledger).*
