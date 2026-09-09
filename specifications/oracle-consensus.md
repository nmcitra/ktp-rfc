# Oracle Consensus Integration Contract

**Status: unreleased normative companion.** This document defines the requirements for claiming Byzantine agreement over KTP Oracle shared state. It replaces the earlier simplified consensus sketch. It is an integration contract for a reviewed protocol, not a new consensus algorithm or an implemented consensus engine.

The key words "MUST", "MUST NOT", "REQUIRED", "SHOULD", "SHOULD NOT", and "MAY" are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

## Scope and selected protocol

A mesh that claims Byzantine agreement MUST select a named, versioned, reviewed Byzantine fault tolerant state-machine replication protocol and pin the exact specification used. Its protocol specification MUST identify:

- The protocol and implementation versions, authenticated wire encodings, signature and digest rules, deterministic request validation, and state-transition rules.
- The supported membership size, fault budget, agreement thresholds for every relevant phase, and evidence required for final commitment.
- The rules and supporting safety argument for leader selection, view changes, persistent locks, checkpointing, state transfer, restart, and membership transitions.
- The fault, key-custody, storage, network, and scheduling assumptions for safety and progress, including how the exact deployed configuration satisfies those assumptions.
- The independent technical review and implementation verification supporting this configuration and these integration choices. A product name, an unversioned URL, or self-asserted protocol label does not satisfy this requirement.

Changing the algorithm, its phase thresholds, or its persistence or reconfiguration rules is a protocol change requiring the same review and authenticated configuration-transition process. The integration MUST NOT fill unspecified behavior with locally invented fallback rules. A protocol lacking a reviewed membership-change mechanism MUST use a fixed membership until a conforming transition mechanism has been selected and reviewed; deleting a member from a configuration file is not such a mechanism.

The original [Practical Byzantine Fault Tolerance algorithm](https://www.usenix.org/legacy/publications/library/proceedings/osdi99/full_papers/castro/castro_html/node4.html) explains why normal-case voting, view changes, and certified checkpoints must preserve one history. Its presented algorithm assumes `N = 3f + 1`. The earlier KTP sketch copied `2f + 1` while also presenting five members and one fault. That combination does not establish the required quorum intersection. This companion does not certify a modified PBFT algorithm for five members; the selected protocol's reviewed specification MUST support the actual configuration.

## Declaration and trust anchors

The [`deployment-profile.json`](../schemas/deployment-profile.json) `oracle_consensus` object declares:

| Field | Meaning |
|---|---|
| `protocol_id`, `protocol_version` | The selected, versioned protocol integration |
| `protocol_spec_digest` | Digest of the exact pinned specification bytes, including its fixed references to implementation and review evidence |
| `membership_epoch` | Monotonically increasing configuration epoch |
| `members` | Full voting roster, with each member's `node_id`, `key_id`, and `control_domain` |
| `fault_tolerance` | Maximum tolerated Byzantine voting members, f |
| `quorum` | Declared homogeneous agreement quorum, q |

The installed declaration and its complete configuration digest MUST be authenticated by the deployment's pre-existing governance trust anchors. A proposal MUST NOT supply its own trusted roster or approving keys. The initial roster MUST be commissioned through that established process before the first mesh decision. Later epochs require the membership-transition procedure below. A valid declaration is not evidence that commissioning or a transition occurred.

The complete configuration identity MUST bind the zone, entire roster and key bindings, epoch, protocol identity/version/specification digest, f, q, operation-specific approval rules, and the applicable cryptographic and deterministic evaluation profiles. Those bindings MUST NOT be mutable while retaining the same configuration identity. The pinned protocol specification defines the exact encoding and digest computation; implementations MUST reject ambiguous encodings, duplicate object names, and nonfinite numbers rather than signing divergent interpretations. Digests and signatures MUST meet the trusted deployment's KTP-Crypto profile, including SHA-384 where Level 3 requires it.

Each counted member MUST have one authenticated voting identity, its own verified key binding, and independent control. `node_id`, `key_id`, and `control_domain` labels MUST each be distinct within a roster. Several keys, machines, regions, or aliases under one control domain MUST NOT be counted as independent votes. Distinct declaration strings alone do not prove independence; commissioning and subsequent reviews MUST establish the actual control and custody boundaries.

The declaration is optional only for deployments that make no Byzantine mesh agreement claim. Absence, an invalid declaration, an unknown protocol, or an unverifiable configuration MUST NOT fall back to a majority-vote or threshold-signature claim of Byzantine agreement. This declaration format requires `f >= 1` and at least four members. A deployment claiming no Byzantine tolerance omits `oracle_consensus`; it does not submit `f = 0` as a valid mesh declaration.

## Quorum arithmetic and its limits

Let N be the number of members in the full authenticated installed roster. N is not the number of available or responding nodes. Let f and q be the declared integer fault budget and quorum. The following requirements apply:

```text
f >= 1
N >= 3f + 1
q_min = floor((N + f) / 2) + 1
q_min <= q <= N - f
```

The declared `fault_tolerance`, `quorum`, and `membership_epoch` MUST use positive JSON integer tokens; booleans, fractional or floating-point tokens, and nonfinite values are invalid. N is derived from the roster length, not separately declared. The membership epoch starts at one or higher and MUST increase at every authenticated configuration transition.

The recommended baseline is `N = 5`, `f = 1`, `q = 4`. Every homogeneous agreement certificate MUST contain valid evidence from at least q distinct installed members. The same floor applies to certificates that establish a prepared/locked state, commitment, a certified checkpoint, or acceptance of a new view. A phase that combines a primary proposal with supporting votes MUST count distinct members in the combined evidence, not count the primary twice. Smaller thresholds used only to request retransmission or initiate a view change MUST NOT be treated as agreement evidence.

The selected protocol's actual phase thresholds and evidence rules remain binding and MAY be stricter. Cross-phase safety requires the reviewed protocol's intersection conditions, not just two commit quorums. Any alternative phase structure MUST provide reviewed evidence that its safety-relevant certificate sets retain honest intersection and satisfy this agreement floor; a lower phase threshold cannot be justified solely by retaining q at final commit. If a protocol requires a threshold above the declared q, the higher threshold applies. The protocol's progress claim MUST account for each actual threshold and the possibility that all f faulty members withhold messages.

For any two q-member sets, their overlap is at least `2q - N`. Requiring `2q - N > f` ensures at least one honest member in the overlap. With five members and one fault, three-member groups can overlap only at the faulty member: `{X, A, B}` and `{X, C, D}`. Four-member groups overlap in at least three members. Honest members preserving the reviewed protocol's voting and locking rules then prevent the conflicting decisions that those rules forbid. Arithmetic alone does not supply those rules.

The upper bound `q <= N - f` permits the core agreement service to progress without votes from faulty members under the selected protocol's remaining progress assumptions. It does not weaken stricter operation approvals. For example, five-of-five approval for zone dissolution remains five-of-five and can pause when one member is unavailable.

## Authenticated messages and result binding

Before counting a vote, a verifier MUST authenticate the sender against the installed roster and verify the exact bytes required by the selected protocol. Each voting message MUST bind, either directly or through a signed collision-resistant digest:

1. The protocol identity/version and a distinct consensus-message purpose.
2. The zone and complete configuration identity, including membership epoch.
3. The authenticated view and phase or control-message type.
4. The sequence or checkpoint position and the committed predecessor or applicable state binding.
5. The complete proposed request digest, or complete control-message digest for a checkpoint, view change, or membership transition.

The pinned wire specification MUST define these bindings for every message type and disallow confusion between ordinary signatures, proposal votes, prepared/locked evidence, commit evidence, and configuration approvals. Votes counted toward one homogeneous certificate MUST NOT mix different zones, epochs, views, phases, positions, predecessors, or request digests. The selected protocol MAY define composite evidence, such as a proposal with supporting phase votes, a new-view record carrying earlier-view locks, or a joint transition containing old- and new-configuration certificates. Each constituent MUST be independently verified in its own bound context, and the composite's signed purpose and native validation rules MUST authenticate the relationship among those constituents. This does not permit counting an old or differently scoped vote toward a new certificate's threshold. An aggregate or threshold signature MUST retain independently verifiable evidence of the required distinct-member participation and the protocol's commitment predicates; signature validity alone is insufficient.

The complete request MUST bind the authenticated requester, operation, parameters, relevant evaluation inputs, and intended state transition. Every honest voting node MUST validate the same request against the same certified predecessor under the pinned deterministic rules. A local clock reading or unbound mutable sensor lookup MUST NOT cause different transitions after agreement on the same request. Consensus orders and validates the supplied evidence; it does not prove that a sensor reported physical truth.

Only the selected protocol's validated final commit evidence permits a new protected state transition or a signature attesting to that committed transition. A prepared certificate, a coordinator's assertion, a timeout, or q ordinary signatures with no protocol evidence MUST NOT be accepted as final commitment. Execution MUST respect the committed ordering and the protocol's duplicate-request controls.

For v3 trajectory records, `trajectory-signatures.md` defines two nonrecursive bindings: commitment to the complete proposed Oracle signing payload through its typed `commit_intent`, followed by selection of the exact completed signed-record hash as the final head. The final signature and the certificate that commits its payload cannot be included in their own signing input. Both required commitments and their contextual bindings MUST verify before the record or resulting standing becomes authoritative. A committed intent alone is not an accepted final trajectory head, and another valid signature over the same intent cannot replace the selected final hash.

Consumers relying on mesh agreement MUST verify the commit evidence, installed configuration, and binding from that evidence to the exact protected result. An independently trusted verifier implementing the pinned protocol MAY perform this verification, but trusting a sole Oracle signature is not equivalent to tolerating a Byzantine Oracle. A compact threshold signature MAY accompany the result; its key threshold remains distinct from the agreement quorum.

## Durable voting, locks, and recovery

Before a node releases a signed vote, it MUST durably record that vote and every safety-relevant state change it causes, including its accepted configuration, view, prepared/locked evidence, and any protocol-authorized lock transition. The signing path MUST NOT emit the signature if this persistence fails. Before exposing a committed result or signing a protected record, it MUST durably record the required commit evidence and resulting state.

An honest node MUST NOT issue conflicting votes where the selected protocol forbids them. Changing view does not by itself release a lock. A lock MAY change only when the reviewed protocol's authenticated evidence permits that specific transition; the evidence and new state MUST be durable before the next vote. Committed requests and their order MUST never be replaced by a later view.

Storage and key use MUST be protected against rollback and concurrent reuse. Restart, restoring a backup, cloning a machine, rotating a signing process, or replacing local storage MUST NOT permit the same member to vote again from an earlier configuration, view, or lock state. A node that cannot verify its preserved safety state MUST stop voting and recover through the selected protocol's authenticated recovery procedure. It MUST NOT initialize itself as a fresh voting member using its old key.

A checkpoint MUST carry the protocol's validated certification, identify the exact state and committed position, and preserve the evidence necessary for unresolved decisions. State transfer MUST verify the checkpoint, configuration continuity, and all required subsequent state before resuming votes. Log truncation MUST occur only under the selected protocol's certified-checkpoint rules. A signed but stale snapshot does not authorize rollback or deletion of a later lock.

## Leader and view changes

The selected protocol MUST designate a single legitimate primary for a given zone, configuration epoch, and view. Different nodes may temporarily know different views during network delay; their protocol checks MUST nevertheless preserve agreement. Uptime ranking, an operator's preference, or a timeout alone does not authenticate a replacement primary.

Entering a new view MUST require the protocol's authenticated new-view evidence with at least q distinct members and any stronger native threshold. That evidence MUST identify the selected certified checkpoint and carry the prepared, locked, or committed evidence needed to preserve every value that could already have committed. The replacement primary MUST derive its permitted proposals using the pinned safe-selection rule.

Each honest member MUST independently verify that rule and the supporting evidence before voting in the new view. It MUST reject a proposal that discards a prior commitment or releases a lock without the protocol's required justification. A leader MUST NOT select its preferred history, retain only responsive members, or conceal a known conflicting certificate to restart the same position. Incomplete evidence causes a pause and recovery, not permission to start over.

## Membership and configuration changes

Adding, removing, or replacing a voting member or key; changing f or q; changing protocol or verification rules; and changing the control domains underlying a roster are authenticated configuration transitions. A heartbeat timeout, failed region, compromise suspicion, isolation, or key revocation MUST NOT change the installed N or reduce its required thresholds.

A transition MUST be authorized under the installed governance and operation rules and the selected protocol's reviewed reconfiguration procedure. At minimum:

1. The transition identifies the exact old and new configuration digests, a strictly increasing epoch, the authorized change, and a common certified checkpoint and final old-configuration position.
2. The old configuration commits the transition with valid old-configuration agreement evidence meeting its q and all stricter approval requirements.
3. The new members authenticate that old evidence and verify the checkpoint, state transfer, and safety-relevant unresolved state. The new configuration supplies its required quorum evidence accepting the same transition and checkpoint under its own valid N, f, and q.
4. The transition becomes active only through the selected protocol's joint transition evidence binding both configurations to that common boundary. Both quorums are counted against their own full authenticated rosters; the candidate roster cannot authorize its own installation.
5. Durable fencing prevents the old configuration from committing ordinary successors beyond its final boundary and prevents the new configuration from acting before the transition becomes effective. Verifiers retain authenticated configuration continuity and reject replay from superseded epochs.

The selected protocol MUST specify the sequencing, handoff, unresolved-slot handling, and recovery behavior that make these obligations safe. Independent signatures from old and new keys without that state transition are insufficient. If either required quorum or any stronger approval is unavailable, the transition MUST pause. A timeout MUST NOT reduce either denominator. A member shared by both configurations may contribute separately to each configuration's evidence, but MUST be counted only once within each certificate.

Revoking compromised key use MAY immediately stop its messages from being accepted. Its seat still remains in the installed denominator until a valid transition removes or replaces it. Revocation can therefore halt progress; it does not authorize a smaller emergency committee. Loss of the evidence needed to establish the current epoch or transition state MUST stop protected commits until authenticated recovery succeeds.

## Partition behavior and operation boundaries

Safety MUST hold during arbitrary network delays and partitions within the declared fault and storage model. Progress is conditional on the selected protocol's stated assumptions, including sufficient communication among the needed participants. A consensus latency target or recovery deadline is not permission to finalize an incomplete round.

In the five-member baseline, four participating members can meet the minimum agreement threshold. Three cannot. One faulty member withholding votes and one honest member unreachable is enough to halt protected updates. Neither partition may remove the other from the roster to resume. On reconnection, nodes recover the certified history and unresolved safety evidence; they do not merge conflicting committed branches.

Trajectory co-signing, E_base modification, agent genesis, and zone configuration changes MUST wait for valid commit evidence and any stronger operation approval. An operation requiring four-of-five or five-of-five approval retains that requirement even if its cryptographic key can sign with fewer shares. No operation may lower q or use an ordinary signature to label an uncommitted update as committed.

A local Zeroth Law calculation need not create a new mesh decision. A permitted single-node Trust Proof issuer may derive a proof from verified committed state under the required freshness checks, but its signature alone conveys no Byzantine agreement guarantee. During a partition it MUST NOT invent newer standing, ignore a required state-freshness check, or prolong an ordinary proof. The ordinary `0 < exp - iat <= 10` and `iat <= current_time < exp` rules remain binding. The separate emergency capability cannot lower consensus thresholds or change its own authority during an outage.

## Verification and conformance limits

[`oracle-consensus-v1.json`](conformance/oracle-consensus-v1.json) defines mandatory downstream adversarial scenarios. A claiming implementation MUST test the five-node equivocation case, insufficient or mismatched certificates, view changes with prior decisions, restart and storage rollback, stale checkpoints, and membership transitions with missing or conflicting old/new evidence. Passing only a normal-case vote-count test is insufficient.

The repository's declaration checker and arithmetic regressions validate declaration shape, member-label uniqueness, and the stated quorum inequalities. They do not execute a consensus protocol, verify independent control or signatures, establish durable storage, prove view-change or membership safety, or certify any named implementation. Deployment conformance additionally requires the selected protocol's technical review, integration verification, and execution of the adversarial cases against the actual implementation.
