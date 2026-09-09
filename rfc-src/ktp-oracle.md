---
title: "Kinetic Trust Protocol (KTP) - Trust Oracle Specification"
abbrev: "KTP-ORACLE"
date: 2026-09-06
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  RFC2119:
  RFC8174:

--- abstract

This document specifies the Trust Oracle for the Kinetic Trust Protocol (KTP).  The Trust Oracle is the authoritative source of trust state within a zone—issuing Trust Proofs, co-signing trajectory records, calculating environmental stability (E), and enforcing Digital Gravity.  The specification covers Oracle architecture, consensus mechanisms, threshold signatures, mesh topology, Oracle accountability, and Oracle-to-Oracle federation.

--- middle

# Introduction

The Trust Oracle is the nerve center of a KTP zone.  It performs the calculations that make Digital Gravity possible:

- Collects Context Signal measurements

- Calculates Risk Factor (R) and Environmental Stability (E)

- Issues Trust Proofs to agents

- Co-signs trajectory chain transactions

- Enforces the Zeroth Law (A ≤ E)

- Applies gravity constraints when needed

- Attests to agent behavior for Proof of Resilience

Without a functioning Trust Oracle, KTP cannot operate.  The Oracle is both critical infrastructure and potential single point of failure.  This specification addresses both the capabilities required and the resilience necessary.

# Design Principles

The Trust Oracle embodies these principles:

1. Availability: Oracle availability is an operational objective. Loss of the required quorum MUST pause consensus-dependent changes; availability targets MUST NOT weaken agreement or extend ordinary proof validity.

1. Integrity: Oracle decisions MUST be consistent and correct. Corrupted Oracles corrupt the entire trust system.

1. Accountability: Oracles are themselves subject to KTP.  They cannot exempt themselves from the constraints.

1. Transparency: Oracle operations MUST be auditable.  Trust requires visibility.

1. Resilience: A mesh MUST declare its fault budget and provide redundancy under the selected consensus protocol's assumptions. Operations with stronger approval requirements MAY pause after a single failure.

1. Performance: Oracle latency MUST NOT bottleneck agent operations.  Speed matters.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Terminology

Attestation: A signed statement by the Oracle confirming some fact about an agent or transaction.

Consensus: Agreement among multiple Oracle nodes on trust state.

Oracle Mesh: A network of connected Oracle nodes providing redundancy and consensus.

Oracle Node: A single instance of Trust Oracle software and associated cryptographic identity.

Quorum: The required number of distinct, independently controlled members of the authenticated configuration contributing valid protocol evidence to an agreement certificate. A key-signing threshold alone is not a consensus quorum.

Split Brain: A failure mode where different groups accept conflicting records as the same committed position in the shared history.

Threshold Signature: A cryptographic signature requiring M-of-N participants to produce.

Trust Proof: A signed attestation of an agent's current trust state, issued by the Oracle.

# Oracle Architecture

## Single Node Architecture

A single Oracle node contains:

~~~
+------------------------------------------------------------------+
|                      TRUST ORACLE NODE                           |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    Signal Collector                        |  |
|  |   Receives measurements from all six signal domains        |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                    Risk Calculator                         |  |
|  |   R = weighted_aggregate(domain_risks)                     |  |
|  |   E = E_base × (1 - R)                                     |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Zeroth Law Engine                        |  |
|  |   Evaluates A ≤ E for every action request                 |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Gravity Calculator                       |  |
|  |   G = f(A, E, threshold) — determines constraint level     |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Trust Proof Issuer                       |  |
|  |   Issues signed Trust Proofs to agents                     |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Trajectory Co-Signer                     |  |
|  |   Co-signs agent transaction records                       |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Attestation Engine                       |  |
|  |   Issues Proof of Resilience attestations                  |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                    Key Management                          |  |
|  |   HSM-backed cryptographic operations                      |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Consensus Client                         |  |
|  |   Participates in Oracle Mesh consensus                    |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
~~~

## Component Specifications

### Signal Collector

The Signal Collector receives measurements from Context Signal instrumentation:

- Input: Body domain Source: Infrastructure monitoring Rate: 1-100 Hz

- Input: World domain Source: Environmental sensors/simulation Rate: 0.1-10 Hz

- Input: Time domain Source: Time subsystem Rate: Per transaction

- Input: Relational domain Source: Relationship monitoring Rate: Per interaction

- Input: Information domain Source: Information environment monitoring Rate: 1 Hz

The Collector MUST:

- Validate incoming measurements

- Detect anomalous or spoofed data

- Maintain measurement history for smoothing

- Provide current Risk Factor state on demand

### Risk Calculator

The Risk Calculator computes R from Risk Factor measurements:

~~~
   R = Σ(risk_factor_i × weight_i) for i in the six inputs
~~~

Where weights sum to 1.0 (default):

~~~
   soul_weight       = 0.25
   body_weight       = 0.10
   world_weight      = 0.15
   time_weight       = 0.15
   relational_weight = 0.20
   signal_weight     = 0.15
~~~

The Calculator MUST:

- Update R within 10ms of an input change

- Apply temporal smoothing to prevent oscillation

- Handle missing input data gracefully

- Log R changes for audit

### Zeroth Law Engine

The Zeroth Law Engine evaluates A ≤ E for every action:

Input:

~~~
   action_request {
     agent_id,
     action_type,
     target,
     parameters
   }
~~~

Process:

~~~
   1.  Calculate A = autonomy(action_request)
   2.  Retrieve agent E_base
   3.  Get current R
   4.  Calculate E = E_base × (1 - R)
   5.  Evaluate A ≤ E
~~~

Output:

~~~
   {
     permitted: boolean,
     A: number,
     E: number,
     gravity_recommended: number
   }
~~~

The Engine MUST:

- Complete evaluation within 1ms

- Be deterministic (same inputs → same outputs)

- Log all evaluations

- Handle concurrent requests

### Trust Proof Issuer

The Trust Proof Issuer creates signed Trust Proofs:

~~~
   {
     "proof_id": "tp-2025-12-03-001",
     "agent_id": "agent:independent:3gen:acme:abc123",
     "issued_at": "2025-12-03T14:32:15.123Z",
     "expires_at": "2025-12-03T14:32:25.123Z",
     "trust_state": {
       "e_base": 55,
       "e_trust": 44,
       "r_current": 0.2,
       "tier": "analyst",
       "lineage": "independent",
       "generation": 3
     },
     "constraints": {
       "max_action_risk": 44,
       "restricted_actions": [],
       "gravity_active": false
     },
     "oracle_id": "oracle:zone-blue-prod-01:primary",
     "signature": "sig:oracle:..."
   }
~~~

Trust Proofs MUST:

- Have a positive lifetime of at most 10 seconds: 0 < exp - iat <= 10 seconds, using the equivalent issued_at and expires_at fields in this illustrative representation

- Be signed by Oracle key

- Include current trust state

- Be verifiable by any party with Oracle public key

In a mesh, the issuer MUST derive protected standing and configuration from verified committed state under the applicable freshness rules. Public-key verification establishes the proof signature; a consumer requiring Byzantine agreement MUST additionally verify the state commitment and its result binding as specified below.

Historic PoR MUST NOT be reduced merely because time passes or the agent is inactive. Invalid claims are handled by authenticated appended corrections. Standing alone does not establish the present readiness of a particular code/model/configuration/toolchain/permission set for an operation; specifications/operational-readiness.md supplies the separate mandatory prerequisite.

### Trajectory Co-Signer

The Co-Signer adds Oracle attestation to trajectory records:

Input: transaction_record (agent-signed)

Process:

~~~
   1.  Validate trusted v3 format/profile and complete canonical agent JWS
   2.  Verify action was permitted
   3.  Verify state transitions are valid
   4.  Capture Risk Factor snapshot
   5.  Construct complete attestation and canonical Oracle-role payload
   6.  Obtain and verify commit evidence for its typed trajectory-intent digest
   7.  Sign the Oracle-role payload; compute the final signed-envelope hash
   8.  Anchor that exact final hash as the unique authoritative successor
~~~

Output: transaction_record (co-signed)

The complete record-body and attestation bindings, RFC 8785 canonical bytes, compact JWS roles, and version cutover are defined by specifications/trajectory-signatures.md. The pre-signing intent excludes the Oracle signature and final record_hash. After Oracle signing, a separate authenticated final-head anchor MUST bind record_version, the exact completed-envelope hash, commit_intent, agent, zone, chain, sequence, and predecessor under specifications/oracle-consensus.md before authoritative append or use. An intent certificate alone cannot choose between different valid signature envelopes for one intent. Failed or unavailable final anchoring leaves the envelope non-authoritative.

The Co-Signer MUST:

- Verify before signing (never blind sign)

- Include the Risk Factor snapshot at time of transaction

- Refuse to sign invalid records

- Refuse to sign a shared-state trajectory intent without its required commit evidence and operation approvals; refuse authoritative append until the exact final envelope is independently anchored

- Verify the operation's readiness evidence and complete decision sidecar before attesting that the action was permitted; record the sidecar in the existing signed action.details.readiness field without changing the trajectory's top-level format

- Reject candidate-selected versions, keys, algorithms, profile digests, or legacy fallbacks that do not match independently trusted configuration and the durable format floor

- Log all signing operations

# Oracle Mesh

## Mesh Topology

Production deployments MUST use multiple Oracle nodes in a mesh:

~~~
+------------------+      +------------------+
|   Oracle Node 1  |<---->|   Oracle Node 2  |
+------------------+      +------------------+
         ^                         ^
         |                         |
         v                         v
+------------------+      +------------------+
|   Oracle Node 3  |<---->|   Oracle Node 4  |
+------------------+      +------------------+
         ^                         ^
         |                         |
         v                         v
+------------------+      +------------------+
|   Oracle Node 5  |<---->|   Oracle Node 6  |
+------------------+      +------------------+
~~~

~~~
           All-to-all connectivity for consensus
~~~

## Mesh Requirements

- Requirement: Geographic distribution Minimum: 2 locations Recommended: 3+ locations

- Requirement: Network latency (inter-node) Minimum: <100ms Recommended: <50ms

- Requirement: Consensus declaration Minimum: Named and versioned reviewed Byzantine fault tolerant protocol, pinned specification digest, authenticated membership epoch, roster, fault budget f, and quorum q under `specifications/oracle-consensus.md`

- Requirement: Consensus quorum Minimum: floor((N+f)/2)+1, with N >= 3f+1 and q <= N-f Recommended baseline: N=5, f=1, q=4

The `oracle_consensus` deployment-profile declaration is REQUIRED for a mesh agreement claim. N is the number of authenticated voting members in the installed roster, not the number currently reachable. A missing declaration permits no Byzantine agreement claim. Geographic and latency targets do not establish independent control or satisfy the consensus contract.

## Node Roles

All voting nodes maintain the protocol state needed to validate decisions. Roles within one authenticated view are:

- Role: Primary Responsibility: Receives requests, initiates consensus

- Role: Secondary Responsibility: Participates in consensus, can become primary

- Role: Witness Responsibility: Does not serve client requests but validates proposals and durably maintains the same voting, locking, and recovery evidence as other voting members

Primary selection and replacement MUST follow the pinned consensus protocol:

- Exactly one primary is designated for a given zone, membership epoch, and view

- A timeout MAY initiate a view change; it does not authorize a new primary to discard prior decisions or locks

- Nodes MUST verify the new-view evidence and safe proposal selection before voting in the new view; uptime ranking and independently selected concurrent primaries are not permitted

# Consensus Mechanisms

## Consensus Requirements

Oracle consensus MUST provide the following properties under its declared and verified assumptions:

1. Agreement: Honest nodes MUST NOT commit different requests at the same position in the zone's shared history, including across view changes, restart, and membership transitions.

1. Validity: Each committed transition MUST pass the same deterministic validation against the authenticated predecessor and bound inputs. Agreement does not establish the truth of an untrusted sensor reading.

1. Progress: The selected protocol MUST state its communication, scheduling, storage, and fault assumptions for progress. No fixed completion deadline is guaranteed during arbitrary message delay, partition, or quorum loss. Timeouts MUST NOT convert an incomplete decision into a committed one.

1. Fault tolerance: N and f MUST be integers, f MUST be at least one, and N MUST satisfy N >= 3f+1. A Byzantine mesh declaration therefore requires at least four voting members and the complete integration contract; redundant nodes and quorum arithmetic alone do not establish it. A deployment making no Byzantine agreement claim may omit the declaration.

## Consensus Protocol

An Oracle Mesh MUST integrate a named, versioned, reviewed Byzantine fault tolerant state-machine replication protocol according to `specifications/oracle-consensus.md`. The pinned protocol specification MUST cover the exact N, f, q, phase thresholds, wire authentication, leader replacement, durable recovery, and membership-transition model in use. This document does not define a replacement consensus algorithm, and a label such as "PBFT-style" is insufficient.

The minimum homogeneous agreement quorum is q_min = floor((N+f)/2)+1. The declared integer q MUST satisfy q_min <= q <= N-f. Consequently, two quorum sets intersect in more than f members. For five members tolerating one Byzantine member, q_min is four: three-of-five is insufficient for an agreement certificate. A protocol's stronger thresholds and an operation's stronger approval requirements remain binding.

Every voting message MUST authenticate its purpose, zone, complete configuration identity and epoch, view, phase, sequence or checkpoint position, predecessor/state binding, and request or control-message digest. Verifiers MUST reject duplicate members, untrusted keys, mismatched bindings, and replay across configurations or phases. A node MUST durably persist safety-critical voting and lock state before emitting its vote, and persist commit evidence before exposing the committed result.

Only the selected protocol's validated commit evidence establishes a shared decision. A proposal, a prepare certificate, a collection of ordinary signatures, or an uptime-based failover MUST NOT substitute for it. Restart, view change, state transfer, and membership change MUST preserve committed history and every safety-relevant lock as specified by the normative companion.

## Consensus Scope

The following operations have different agreement requirements:

- Operation: Zeroth Law evaluation Consensus Required: No new shared-state decision; single-node evaluation uses validated current inputs and cannot modify committed standing

- Operation: Trust Proof issuance Consensus Required: No new shared-state decision when deriving a proof from verified committed state under the required freshness rules; a single issuer's signature alone conveys no Byzantine agreement guarantee

- Operation: Trajectory co-signing Consensus Required: Yes (valid commit evidence with at least q members for the typed intent before Oracle signing, followed by commitment of the exact final signed-envelope head before authoritative append, per specifications/trajectory-signatures.md)

- Operation: E_base modification Consensus Required: Yes (valid commit evidence with at least q members)

- Operation: Agent Genesis Consensus Required: Yes (valid commit evidence with at least q members)

- Operation: Zone configuration change Consensus Required: Yes (valid commit evidence with at least q members and every stronger existing approval rule; voting membership changes also require authenticated joint transition evidence)

Consumers relying on mesh agreement MUST verify the commit evidence and its binding to the protected result, directly or through an independently trusted verifier implementing the pinned protocol. A valid ordinary proof signature does not by itself prove this property. During quorum loss, no new consensus-dependent state change is permitted. Single-node derivation MUST NOT invent a new committed head, ignore required state freshness, or extend the ordinary ten-second proof lifetime.

## Split Brain Prevention

Partition safety depends on agreement evidence and preserved state:

1. Quorum requirement: Count the installed full voting roster and require at least q valid, distinct members for each agreement certificate, plus any stricter protocol or operation rule.

1. Fencing: A partition without the necessary evidence MUST pause protected commits and signing. Detection of the partition is not a prerequisite for enforcing the certificate rule.

1. Durable history: Honest nodes MUST retain the protocol's locks and committed predecessor across view changes, process restart, and state transfer. An odd node count alone provides no Byzantine split-brain protection.

1. Membership continuity: Outage, suspicion, isolation, or key revocation MUST NOT shrink the denominator. A new configuration requires verified old- and new-configuration quorum evidence bound to the same authorized transition and checkpoint.

On healing, nodes MUST recover the authenticated committed history and unresolved safety evidence before resuming votes. They MUST NOT merge conflicting committed histories or select one by arrival time. Conflicting purported commit evidence requires containment and investigation; it is not an ordinary reconciliation path.

# Threshold Signatures

## Overview

Critical Oracle operations use threshold signatures—requiring M of N Oracle nodes to produce a valid signature.

~~~
   Standard signature: 1 key → 1 signature
   Threshold signature: M of N key shares → 1 signature
~~~

Cryptographic key-threshold example (3-of-5; not a consensus certificate):

~~~
   Node 1 holds share 1
   Node 2 holds share 2
   Node 3 holds share 3
   Node 4 holds share 4
   Node 5 holds share 5
~~~

~~~
   Any 3 nodes can combine shares to produce valid signature
   No single node can sign alone
   Signature is indistinguishable from standard signature
~~~

## Threshold Scheme

The Oracle uses Shamir's Secret Sharing with threshold ECDSA:

- Parameter: N Description: Total number of nodes Default: 5

- Parameter: M Description: Cryptographic key-signing threshold Example: 3; consensus agreement separately requires q=4 for the five-node, one-fault baseline

- Parameter: Curve Description: Elliptic curve Default: secp256k1

- Parameter: Hash Description: Hash algorithm Default: SHA-256

The key-sharing threshold protects a signing key; it does not determine agreement. Signers MUST first verify the required committed decision and all operation approvals. Consumers requiring consensus MUST verify that evidence and its binding to the result; a bare three-of-five signature MUST NOT replace a four-of-five commit certificate. A threshold scheme that hides its participant set MUST provide independently verifiable protocol evidence of the required distinct-member participation. Stricter cryptographic profiles in KTP-Crypto still apply.

For v3 trajectory records, the committed decision before Oracle signing is the typed intent defined by specifications/trajectory-signatures.md. The exact final signed-envelope hash is committed separately afterward. Signature generation MUST NOT depend on a commitment to a final hash that itself includes that signature, and an intent certificate MUST NOT be treated as the final-head anchor.

## Key Ceremony

Threshold keys are generated in a key ceremony:

1. All N nodes generate random contributions

1. Contributions are combined using DKG protocol

1. Each node receives its key share

1. No node ever sees complete private key

1. Public key is published

1. Ceremony is recorded and witnessed

## Operations Requiring Threshold Signature

- Operation: E_base modification Agreement: At least 4-of-5 in the baseline configuration; cryptographic signing threshold: At least 3-of-5 after commit

- Operation: Zone configuration change Agreement and approval floor: 4-of-5; membership changes additionally require the joint transition contract

- Operation: Oracle key rotation Agreement and approval floor: 4-of-5; changes to voting keys additionally require the joint transition contract

- Operation: Zone dissolution Agreement and approval floor: 5-of-5

These operation counts describe the five-member baseline. Other configurations MUST preserve every applicable supermajority or unanimity requirement and satisfy the selected consensus protocol; the generic quorum MUST NOT relax a stronger operation rule.

# Trust Proof Lifecycle

## Issuance

Trust Proofs are issued on demand:

~~~
   Agent → Oracle: RequestTrustProof(agent_id)
~~~

~~~
   Oracle:
     1.  Verify agent identity
     2.  For mesh state, verify its committed head and required freshness
     3.  Calculate current E_trust
     4.  Determine tier and constraints
     5.  Create Trust Proof bound to the verified state
     6.  Sign with Oracle key
~~~

~~~
   Oracle → Agent: TrustProof
~~~

Before the actual operation can execute, the agent or PEP MUST obtain and verify the current readiness decision for that request under specifications/operational-readiness.md. The readiness issuer verifies the independently approved criteria, accountable assessor, current evidence, exact live subject and operation scope, installed profiles, and durable readiness epoch. It signs a separate decision sidecar bound to the already complete ordinary proof and actual request. Creating a Trust Proof does not by itself create or renew readiness, and the sidecar does not add standing or authorization after a prior veto.

## Validation

Any party can validate a Trust Proof:

~~~
   Validator:
     1.  Require 0 < exp - iat <= 10 seconds and iat <= current_time < exp
     2.  Verify Oracle signature against known public key
     3.  Verify agent_id matches expected agent
     4.  Check constraints are appropriate for action
~~~

Execution additionally requires the matched readiness sidecar and current underlying assessment. The validator MUST verify the proof, request, subject state, complete attestation, profiles, current epoch, and validity bindings defined by the readiness companion. Candidate-supplied profile versions or readiness assertions MUST NOT replace trusted installation, evidence, or revocation checks. A fresh proof or re-signed decision cannot extend the assessment's evidence-based expiry.

## Refresh

Trust Proofs expire quickly and MUST be refreshed before their authority can continue. Every zone and deployment profile MUST enforce 0 < exp - iat <= 10 seconds; zone color does not permit a longer lifetime. For a 10-second proof, refreshing every 5 seconds is RECOMMENDED. A shorter declared lifetime requires a refresh schedule that completes before expiration.

Validators MUST reject an ordinary proof when current_time < iat or current_time >= exp, including at the exact expiration boundary. Invalid or unverifiable timestamps or current time MUST fail closed under KTP-Core. Existing sessions, cached responses, queued refreshes, low-risk actions, and Oracle outages MUST NOT extend proof validity. Clock rollback MUST NOT restore or prolong expired authority; if current validity cannot be established, the proof MUST NOT authorize an action.

Continuing ordinary actions require fresh valid proofs or a previously declared bounded safe transition that ceases ordinary operation. Emergency capability is evaluated separately under `specifications/emergency-capability.md`; neither emergency mode nor Oracle unavailability allows expired ordinary proofs, reduced signing quorums, or changes that widen emergency authority.

## Revocation

Trust Proofs can be revoked before expiration:

~~~
   Oracle: RevokeTrustProof(proof_id, reason)
     1.  Add proof_id to revocation list
     2.  Broadcast revocation to mesh
     3.  Notify agent
     4.  Log revocation
~~~

Revocation reasons:

- Agent violation detected

- E_base reduced

- Zone policy change

- Security incident

# Oracle Accountability

## Oracles Under Gravity

The recursive constraint principle: Oracles are subject to KTP.

Oracle actions have autonomy (A):

- Issuing Trust Proof: A = 10

- Co-signing transaction: A = 20

- Modifying E_base: A = 60

- Changing zone config: A = 80

Oracle has E_base based on its own trajectory:

- Uptime history

- Decision accuracy

- Consensus participation

- No Byzantine behavior

Oracle actions are constrained: A_oracle ≤ E_oracle

## Oracle Trajectory

Oracles maintain their own trajectory chains:

~~~
   {
     "oracle_id": "oracle:zone-blue-prod-01:node-1",
     "trajectory": {
       "genesis_date": "2025-01-15T00:00:00Z",
       "uptime_percentage": 99.97,
       "transactions_co-signed": 4847293,
       "consensus_participation_rate": 0.998,
       "byzantine_incidents": 0,
       "e_base": 95
     }
   }
~~~

## Oracle Audit

Oracle operations are logged to Flight Recorder:

- Event: Transaction co-signed Logged Data: Transaction hash, agent, result

- Event: Zeroth Law evaluation Logged Data: A, E, result, agent, action

- Event: Consensus participation Logged Data: Vote, sequence, outcome

- Event: Configuration change Logged Data: Change details, authorizer

## Oracle Misbehavior

Detected misbehavior triggers consequences:

- Misbehavior: Consensus equivocation Detection: Authenticated conflicting evidence Consequence: Immediate containment; voting-roster removal requires the authenticated membership-transition process

- Misbehavior: Availability failure Detection: Heartbeat timeout Consequence: Suspect or isolate the node; retain it in the installed quorum denominator until an authorized transition commits

- Misbehavior: Byzantine behavior Detection: Verified protocol violation Consequence: Containment and authorized removal; detection of all Byzantine behavior is not assumed

# Federation

## Oracle-to-Oracle Federation

Oracles in different zones can federate:

~~~
   Zone A Oracle <---> Zone B Oracle
~~~

Federation enables:

- Cross-zone Trust Proof validation

- Trajectory verification requests

- Exit Attestation verification

- Coordinated emergency response

## Federation Establishment

1. Zone A Oracle requests federation with Zone B

1. Zone B reviews Zone A governance and attestations

1. Both zones sign Federation Agreement

1. Public keys exchanged

1. Trust factors established

1. Federation active

## Federation Trust Factor

Trust is discounted across federation:

~~~
   {
     "federation": {
       "zone_a": "zone-blue-prod-01",
       "zone_b": "zone-blue-prod-02",
       "trust_factor_a_to_b": 0.9,
       "trust_factor_b_to_a": 0.9,
       "established": "2025-06-01T00:00:00Z",
       "last_verified": "2025-12-01T00:00:00Z"
     }
   }
~~~

## Cross-Zone Operations

- Operation: Verify foreign trajectory Federation Requirement: Federation active

- Operation: Accept Exit Attestation Federation Requirement: Federation active

- Operation: Cross-zone agent migration Federation Requirement: Federation active

# Performance Requirements

The following figures are operational targets under the deployment's declared healthy conditions. They are not unconditional termination guarantees. Missing a latency, availability, or recovery target MUST NOT lower a quorum, bypass a view change, discard durable safety state, or permit an expired proof.

## Latency Targets

- Operation: Zeroth Law evaluation Target: 1ms Maximum: 5ms

- Operation: Trust Proof issuance Target: 5ms Maximum: 20ms

- Operation: Transaction co-signing Target: 10ms Maximum: 50ms

- Operation: Consensus round Target: 50ms Maximum: 200ms

## Throughput Targets

- Metric: Evaluations/second Target: 100,000 Notes: Per node

- Metric: Co-signatures/second Target: 1,000 Notes: Consensus limited

## Mesh and node availability targets

- Metric: Mesh availability Target: 99.99%

- Metric: Single node availability Target: 99.9%

- Metric: Recovery time (node failure) Target: <10 seconds

- Metric: Recovery time (quorum loss) Target: <60 seconds

# Deployment Models

## Cloud Deployment

~~~
+------------------+    +------------------+    +------------------+
|    Region A      |    |    Region B      |    |    Region C      |
|   +----------+   |    |   +----------+   |    |   +----------+   |
|   | Oracle 1 |   |    |   | Oracle 2 |   |    |   | Oracle 3 |   |
|   +----------+   |    |   +----------+   |    |   +----------+   |
|   | Oracle 4 |   |    |   | Oracle 5 |   |    |                  |
|   +----------+   |    |   +----------+   |    |                  |
+------------------+    +------------------+    +------------------+
~~~

## On-Premises Deployment

~~~
+------------------+    +------------------+
|  Data Center A   |    |  Data Center B   |
|   +----------+   |    |   +----------+   |
|   | Oracle 1 |   |    |   | Oracle 3 |   |
|   +----------+   |    |   +----------+   |
|   | Oracle 2 |   |    |   | Oracle 4 |   |
|   +----------+   |    |   +----------+   |
|                  |    |   | Oracle 5 |   |
|                  |    |   +----------+   |
+------------------+    +------------------+
~~~

## Hybrid Deployment

~~~
+------------------+    +------------------+    +------------------+
|   On-Premises    |    |    Cloud A       |    |    Cloud B       |
|   +----------+   |    |   +----------+   |    |   +----------+   |
|   | Oracle 1 |   |    |   | Oracle 3 |   |    |   | Oracle 5 |   |
|   +----------+   |    |   +----------+   |    |   +----------+   |
|   | Oracle 2 |   |    |   | Oracle 4 |   |    |                  |
|   +----------+   |    |   +----------+   |    |                  |
+------------------+    +------------------+    +------------------+
~~~

# Security Considerations

## Key Protection

Oracle private keys MUST be protected:

- HSM storage required for production

- Key shares never assembled outside ceremony

- Access controls on key operations

- Audit logging of all key use

## Network Security

Oracle mesh communication MUST be secured:

- Mutual TLS between all nodes

- Certificate pinning

- Network isolation where possible

- DDoS protection

## Byzantine Fault Tolerance

The mesh MAY claim tolerance of at most its declared f Byzantine voting members only after satisfying the complete consensus integration contract and validating the selected implementation. The claim assumes authenticated independent membership, uncompromised cryptography, protected durable state for honest members, and the selected protocol's other assumptions. The baseline is five members, one Byzantine member, and a four-member agreement quorum.

Safety MUST hold despite arbitrary message delay and partition within that fault model. Progress depends on the pinned protocol's communication and scheduling assumptions and enough participating members. For the baseline, one Byzantine member withholding votes plus one unreachable honest member prevents a quorum. Protected updates then pause; ordinary proof validity and the separate emergency-capability controls remain unchanged.

Detected faults MAY trigger immediate isolation, but the installed roster and thresholds remain in force until an authorized membership transition commits. The protocol MUST NOT promise detection of every malicious member or continued operation whenever any number of "honest nodes" remain.

## Oracle Compromise Response

If Oracle compromise is detected:

1. Isolate compromised node

1. Revoke compromised key use through the authorized security process; stop counting it without reducing the installed roster denominator

1. Issue key rotation if threshold compromised

1. Change voting keys or membership only through the authenticated joint transition process; if the required evidence is unavailable, pause protected changes

1. Audit all recent decisions

1. Notify affected agents

1. Post-incident review

# IANA Considerations

This document has no IANA actions.

# Back Matter

--- back

# Oracle Node Specification

Hardware and software requirements for Oracle nodes.

Minimum Hardware:

- Component: CPU Requirement: 8 cores

- Component: RAM Requirement: 32 GB

- Component: Storage Requirement: 500 GB NVMe SSD

- Component: Network Requirement: 1 Gbps

- Component: HSM Requirement: FIPS 140-2 Level 3

Recommended Hardware:

- Component: CPU Requirement: 16+ cores

- Component: RAM Requirement: 64 GB

- Component: Storage Requirement: 1 TB NVMe SSD (RAID)

- Component: Network Requirement: 10 Gbps

- Component: HSM Requirement: FIPS 140-2 Level 3, HA

# Consensus Protocol Details

The normative integration requirements are in `specifications/oracle-consensus.md`. The mandatory downstream adversarial cases are in `specifications/conformance/oracle-consensus-v1.json`. Declaration validation and quorum arithmetic tests do not implement or prove a consensus runtime; deployment conformance additionally requires verification of the selected protocol, implementation, signatures, state persistence, view changes, and membership transitions.

# Threshold Signature Implementation

Implementation guidance for threshold ECDSA.

Acknowledgments

The Trust Oracle design draws on distributed systems research, Byzantine fault tolerance literature, and production experience with consensus systems.
