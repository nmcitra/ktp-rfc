---
title: "Kinetic Trust Protocol (KTP) - Conformance Requirements Levels, Testing, and Certification"
abbrev: "KTP-CONFORMANCE"
docname: draft-perkins-ktp-conformance-00
date: 2026-09-07
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  RFC7519:
  RFC2119:
  RFC8174:

--- abstract

This document specifies conformance requirements for Kinetic Trust Protocol implementations. It defines three conformance levels (Basic, Standard, Full), test suite requirements, certification procedures, and interoperability verification.

The specification enables implementers to validate their KTP deployments and provides a framework for ecosystem interoperability.

--- middle

# Introduction

## Purpose

The Kinetic Trust Protocol comprises multiple components (Trust Oracle, Context Signal sensors, PEPs, Flight Recorder) that must work together correctly. Implementations from different vendors or development teams must interoperate.

This document establishes:

- Conformance levels for different deployment scenarios
- Specific requirements for each KTP component
- Test suites for validating implementations
- Certification procedures for claiming conformance
- Interoperability requirements for federation

Without conformance requirements, KTP implementations may be incompatible, insecure, or incomplete. This document provides the framework for a healthy implementation ecosystem.

## Scope

This document covers:

- Conformance levels (Basic, Standard, Full)
- Component-specific requirements
- Protocol requirements
- Test suite specifications
- Certification procedures
- Interoperability testing

This document does NOT cover:

- Specific implementation guidance (see future Implementation Guide)
- Performance benchmarks (deployment-specific)
- Security certification (SOC 2, FedRAMP, etc.)
- Domain-specific profiles (healthcare, finance, etc.)

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

# Terminology

Conformance Level:  A defined tier of KTP implementation completeness, with specific requirements for each level.

Component:  A distinct functional unit of KTP (Trust Oracle, Context Signal sensors, PEP, Flight Recorder, Agent).

Test Case:  A specific, reproducible test with defined inputs, expected outputs, and pass/fail criteria.

Test Suite:  A collection of test cases organized by category and conformance level.

Certification:  Formal attestation that an implementation meets conformance requirements for a specified level.

Self-Certification:  Certification based on self-executed test suite with published results.

Third-Party Certification:  Certification based on independent testing by an authorized certification body.

Interoperability:  The ability of different KTP implementations to work together correctly.

# Conformance Levels

KTP defines three conformance levels, each building on the previous.

## Level 1: Basic

Basic conformance provides minimum viable KTP functionality suitable for:

- Initial adoption and experimentation
- Low-risk environments
- Single-zone deployments
- Development and testing

### Basic Requirements Summary

Trust Oracle:

- Single Oracle (no mesh required)
- Trust Score calculation (E_trust = E_base × (1 - R))
- Trust Proof generation and signing
- Minimum 3 Risk Factor inputs

Risk Factors:

- Minimum 3 weighted inputs (adversarial_pressure, trust_trend, one other)
- Basic normalization (min/max scaling)
- Single risk domain (no Node/Neighborhood/Global separation)

Policy Enforcement Point:

- Zeroth Law enforcement (A <= E_trust)
- Trust Proof validation
- Binary allow/deny decisions
- Basic logging

Flight Recorder:

- Decision logging (allow/deny with context)
- Declared purpose-specific retention and erasure policy
- No immutability requirement

Agents:

- Unique identifier
- Trust Score tracking
- Basic trajectory (action log)

Protocol:

- Trust Proof JWT format
- ES256 or Ed25519 signatures
- 10-second maximum proof lifetime; expired at current_time = exp

### Basic Limitations

Basic conformance does NOT require:

- Oracle mesh or threshold signatures
- Soul veto or sovereignty constraints
- Trust tiers (just binary allow/deny)
- Federation capabilities
- Cryptographic chaining in Flight Recorder
- Proof of Resilience calculation

Basic single-Oracle operation provides no Byzantine consensus guarantee. Any implementation that claims Oracle mesh agreement, regardless of conformance level, MUST satisfy specifications/oracle-consensus.md and the runtime evidence requirements below. A threshold signature alone does not support that claim.

## Level 2: Standard

Standard conformance provides production-ready KTP functionality suitable for:

- Production deployments
- Multi-zone environments
- Regulatory compliance contexts
- Enterprise adoption

### Standard Requirements Summary

Trust Oracle:

- Oracle consensus mesh (minimum 4 members for one-Byzantine tolerance; default 5 members, decision quorum 4)
- Threshold signatures (2-of-3 minimum)
- Full Trust Score calculation
- Trust velocity tracking (dE/dt)
- All 6 weighted Risk Factor inputs

Risk Factors:

- All 6 weighted inputs (evidence_density, trust_trend, adversarial_pressure, moment_criticality, update_resistance, attestation_coverage)
- Soul veto support
- Risk domain separation (Node, Neighborhood, Global)
- Feed aggregation with configurable weights

Policy Enforcement Point:

- Zeroth Law enforcement
- Trust tier enforcement (all 5 tiers)
- Soul veto checking
- Graceful degradation on Oracle failure
- Detailed decision logging

Flight Recorder:

- Full Decision Geometry logging
- Cryptographic chaining (tamper-evident)
- Bounded decision retention under the approved data policy
- Explicit Soul-veto evidence purpose, access and retention
- Query interface for audit

Agents:

- Full trajectory chain
- Lineage tracking (Sponsored, Independent, Guarantor)
- Proof of Resilience calculation
- Sponsorship support

Protocol:

- Extended Trust Proof format
- Threshold signatures
- 10-second maximum proof lifetime, including outages; expired at current_time = exp
- Federation protocol support

### Standard Limitations

Standard conformance does NOT require:

- Deep Blue zone capability
- Full interplanetary/celestial support
- Sub-second Oracle mesh consensus latency; protected-state safety under specifications/oracle-consensus.md is still required
- Formal verification of components

## Level 3: Full

Full conformance provides comprehensive KTP functionality suitable for:

- Critical infrastructure
- High-security environments
- Deep Blue zone operation
- Federation anchors

### Full Requirements Summary

Trust Oracle:

- Geographically distributed mesh (minimum 5 nodes)
- Threshold signatures (3-of-5 minimum)
- Protected-state consensus with declared membership and Byzantine fault bound (default N = 5, f = 1, q = 4)
- Sub-second Trust Proof refresh
- Real-time consensus protocol
- Cryptographic audit trail

Risk Factors:

- All 7 inputs (including Soul)
- Full Indigenous Data Sovereignty support
- Sub-second sensor refresh for critical dimensions
- Sensor health monitoring and failover

Policy Enforcement Point:

- Complete enforcement at all zone types
- < 15ms evaluation latency
- Zero-downtime deployment support
- Defense in depth (multiple PEP layers)

Flight Recorder:

- Full Decision Geometry with counterfactuals
- External anchoring (blockchain or equivalent)
- Multi-region replication
- Forensic reconstruction capability
- Complete audit trail for certification

Agents:

- Complete trajectory chain with verification
- Cross-zone portable identity
- Attestation chain support
- Celestial wayfinding support (if applicable)

Protocol:

- All Trust Proof formats
- All signature algorithms
- Federation protocol (full)
- Celestial protocol (extended proofs)

### Full Additional Requirements

Full conformance additionally requires:

- Formal security review
- Penetration testing
- Incident response procedures
- Documented recovery procedures
- Third-party certification

## Level Comparison

~~~
+---------------------------+-------+----------+--------+
| Requirement               | Basic | Standard | Full   |
+---------------------------+-------+----------+--------+
| Oracle mesh               | -     | 3+ nodes | 5+     |
| Threshold signatures      | -     | 2-of-3   | 3-of-5 |
| Context dimensions        | 3+    | 6+       | 7      |
| Soul veto                 | -     | Yes      | Yes    |
| Risk domains              | 1     | 3        | 3      |
| Trust tiers               | -     | 5        | 5      |
| Flight Recorder chaining  | -     | Yes      | Yes    |
| External anchoring        | -     | -        | Yes    |
| Federation support        | -     | Yes      | Yes    |
| Celestial support         | -     | -        | Yes    |
| Proof lifetime (maximum)  | 10s   | 10s      | 10s    |
| PEP latency               | -     | < 50ms   | < 15ms |
| Decision retention        | Declared | Declared | Declared |
| Third-party cert required | No    | No       | Yes    |
+---------------------------+-------+----------+--------+
~~~

Implementations MAY claim partial compliance (e.g., "Standard with Full Flight Recorder") but MUST clearly document deviations.

# Component Requirements

## Trust Oracle Requirements

### Basic Oracle Requirements

MUST:

- Accept Risk Factor input
- Validate the deployed Risk Factor weights per \[KTP-CORE] Section 6.4 before use, including after reconfiguration; reject invalid declarations without silently rescaling them
- Calculate Risk Factor: R = Σ(w_i × D_i)
- Calculate E_trust: E_trust = E_base × (1 - R)
- Generate signed Trust Proofs
- Require the installed history-with-scoped-readiness policy and current matched operation-scoped readiness under specifications/operational-readiness.md; readiness is not an E_base term or permission to override a veto
- Support ES256 or Ed25519 signatures
- Expose health check endpoint
- Log all Trust Proof issuances

SHOULD:

- Support configurable dimension weights
- Cache recent Trust Proofs
- Provide metrics endpoint

MAY:

- Support single-node operation
- Use simplified E_base (static assignment)

### Standard Oracle Requirements

All Basic requirements, plus:

MUST:

- Operate as a consensus mesh with at least 4 authenticated members for f = 1; the default is N = 5, f = 1, q = 4
- Implement threshold signatures (2-of-3)
- Protect authoritative state under a reviewed, named and versioned consensus protocol satisfying specifications/oracle-consensus.md; verify committed standing before proof issuance or signing
- Support all 6 weighted dimensions
- Support the Soul veto
- Calculate and track dE/dt (Trust velocity)
- Support agent lineage tracking
- Calculate Proof of Resilience
- Implement graceful degradation
- Support federation protocol

The 2-of-3 requirement describes the signing configuration, which MAY use a subset of the consensus membership. It does not declare a three-member Byzantine consensus mesh. Consensus membership, decision quorum, fault bound, signing threshold, and any stronger operation-specific approval threshold MUST be declared separately. For the claimed Byzantine profile, f >= 1, N >= 3f + 1, and floor((N + f) / 2) + 1 <= q <= N - f. Quorum arithmetic and threshold signing alone do not establish conformance.

SHOULD:

- Geographic distribution of nodes
- Automatic failover
- Load balancing across nodes

### Full Oracle Requirements

All Standard requirements, plus:

MUST:

- Operate as 5+ node mesh
- Implement threshold signatures (3-of-5)
- Use a protected-state decision quorum of 4 for the default five-member, one-Byzantine deployment; other declarations MUST satisfy specifications/oracle-consensus.md
- Sub-second proof refresh capability
- Real-time consensus protocol
- Geographic distribution across 3+ regions
- Complete audit trail
- Support celestial protocol (extended proofs)
- External audit anchor support

SHOULD:

- Formal verification of consensus logic
- Hardware security module (HSM) for keys

## Risk Factor Requirements

### Basic Requirements

MUST:

- Support minimum 3 dimensions -  adversarial_pressure - required -  trust_trend - required -  One additional dimension
- Normalize values to 0-1 range
- Report sensor health status
- Handle sensor failure gracefully

SHOULD:

- Support configurable normalization
- Support multiple feeds per dimension
- Refresh within 60 seconds

### Standard Tensor Requirements

All Basic requirements, plus:

MUST:

- Support all 6 weighted inputs (evidence_density, trust_trend, adversarial_pressure, moment_criticality, update_resistance, attestation_coverage)
- Support the Soul veto
- Implement 3 risk domains (Node, Neighborhood, Global)
- Weighted aggregation across domains
- Feed-level configuration
- Sensor validation and quality metrics
- Refresh within 30 seconds

SHOULD:

- Support custom dimension extension
- Anomaly detection on sensor data
- Historical trend tracking

### Full Tensor Requirements

All Standard requirements, plus:

MUST:

- Full Indigenous Data Sovereignty support -  TK Label integration -  OCAP/CARE protocol support
- Sub-second refresh for critical dimensions
- Sensor redundancy (no single point of failure)
- Automatic failover between feeds
- Complete sensor audit trail

SHOULD:

- Formal specification of normalization
- Verified sensor calibration

## Policy Enforcement Point Requirements

### Basic PEP Requirements

MUST:

- Intercept all protected requests
- Validate Trust Proof signature
- Check Trust Proof expiration
- Enforce Zeroth Law (A <= E_trust)
- Return appropriate HTTP status codes
- Log all decisions

SHOULD:

- Cache Trust Proof validation
- Support multiple signature algorithms
- Provide bypass for health checks

### Standard PEP Requirements

All Basic requirements, plus:

MUST:

- Enforce Trust Tiers (all 5)
- Check Soul constraint (S = 0)
- Support action risk classification
- Graceful degradation on Oracle failure
- Report decisions to Flight Recorder
- Include full context in denial responses
- Support multiple deployment patterns

SHOULD:

- Evaluation latency < 50ms
- Support async Flight Recorder logging
- Circuit breaker for Oracle calls

### Full PEP Requirements

All Standard requirements, plus:

MUST:

- Evaluation latency < 15ms
- Zero-downtime deployment
- Defense in depth (multiple layers)
- Complete decision context to Flight Recorder
- Support all zone types
- Cryptographic binding to session

SHOULD:

- Formal verification of enforcement logic
- Hardware-accelerated cryptography

## Flight Recorder Requirements

### Basic Recorder Requirements

MUST:

- Log all authorization decisions
- Include: timestamp, agent, action, outcome, Trust Score
- Enforced declared retention and erasure policy
- Query by time range and agent

SHOULD:

- Include environmental context
- Support export format (JSON)

### Standard Recorder Requirements

All Basic requirements, plus:

MUST:

- Full Decision Geometry
- Cryptographic chaining (SHA-256)
- Tamper detection
- Bounded decision retention under the approved data policy
- Explicit Soul-veto evidence retention and erasure handling
- Multi-tier storage (hot/warm/cold)
- Query by: time, agent, outcome, environment
- Compliance export (SOC 2, GDPR, HIPAA)

SHOULD:

- Counterfactual analysis
- Aggregate analytics
- Anomaly detection

### Full Recorder Requirements

All Standard requirements, plus:

MUST:

- External anchoring (hourly minimum)
- Multi-region replication
- Complete forensic reconstruction while required evidence is retained; explicit verification limits after authorized erasure
- Third-party audit access
- Purpose-specific retention, justified holds and verified erasure for each record type
- Chain verification on query

SHOULD:

- Real-time chain verification
- Formal proof of immutability

## Agent Requirements

### Basic Agent Requirements

MUST:

- Unique agent identifier
- Obtain and present Trust Proof
- Refresh Trust Proof before expiration
- Handle denial gracefully

SHOULD:

- Cache Trust Proof appropriately
- Log own decisions locally

### Standard Agent Requirements

All Basic requirements, plus:

MUST:

- Maintain trajectory chain
- Support lineage (Sponsored, Independent, Guarantor)
- Handle tier transitions
- Support delegation (if human or delegating)
- Implement graceful degradation

SHOULD:

- Track own dE/dt
- Anticipate tier transitions
- Support sponsorship protocol

### Full Agent Requirements

All Standard requirements, plus:

MUST:

- Complete trajectory verification
- Cross-zone identity portability
- Attestation chain support
- Extended proof support (celestial)

SHOULD:

- Whakapapa chain maintenance
- Predictive trust awareness

# Protocol Requirements

## Trust Proof Format

### Basic Trust Proof

Format: JWT (RFC 7519)

Required claims:

~~~
   {
     "iss": "oracle-identifier",
     "sub": "agent-identifier",
     "iat": 1732547000,
     "exp": 1732547060,
     "ktp": {
       "e_base": 72,
       "e_trust": 68,
       "r": 0.056
     }
   }
~~~

Signature: ES256 or Ed25519

### Standard Trust Proof

All Basic claims, plus:

~~~
   {
     "ktp": {
       "e_base": 72,
       "e_trust": 68,
       "r": 0.056,
       "de_dt": -0.5,
       "tier": "analyst",
       "soul": 0,
       "sigma": 3.2,
       "trajectory_hash": "sha256:abc...",
       "context": {
         "evidence_density": 0.45,
         "trust_trend": 0.32,
         "adversarial_pressure": 0.28,
         "moment_criticality": 0.15,
         "update_resistance": 0.52,
         "attestation_coverage": 0.10
       }
     }
   }
~~~

Signature: Threshold (2-of-3)

### Full Trust Proof

All Standard claims, plus:

~~~
   {
     "ktp": {
       ...
       "lineage": {
         "type": "guarantor",
         "generation": 8,
         "sponsor": null
       },
       "resilience": {
         "score": 0.87,
         "events": 12,
         "ledger_hash": "sha256:def..."
       },
       "attestations": [
         {
           "issuer": "zone:blue-primary",
           "timestamp": "2025-11-24T00:00:00Z",
           "type": "behavior",
           "signature": "sig:..."
         }
       ]
     }
   }
~~~

Signature: Threshold (3-of-5) with key rotation support

## Zeroth Law Enforcement

### Enforcement Requirements (All Levels)

The Zeroth Law (A <= E_trust) MUST be enforced as follows:

1. Extract E_trust from Trust Proof
2. Determine action risk (A) from classification
3. Apply the input checks of \[KTP-CORE] Section 6.6: resolve undefined inputs restrictively; veto if no finite, non-negative, comparable A and E_trust remain
4. If E_trust = 0 or A > E_trust: supervision = silent_veto (Silent Veto); STOP before division or profile evaluation
5. Compute the Zeroth Law margin from A and E_trust
6. If margin <= M_veto: supervision = silent_veto (Silent Veto)
7. Otherwise: derive supervision and tightenedConstraints from the margin per \[KTP-CORE] Section 6.6 (proceed to other checks)

Declared thresholds MUST satisfy the finite-number and 0 <= M_veto < M_allow requirements of \[KTP-CORE] Section 6.6. An invalid declaration MUST NOT authorize execution. Omitting the declaration retains the existing zero-threshold default, including its veto at A = E_trust. The independent capacity veto is checked regardless of thresholds, and supervision MUST NOT lower any prior veto.

The substrate-independent boundary cases are published in specifications/conformance/capacity-gate-v1.json. Implementations MUST satisfy their admission and supervision requirements in addition to the applicable substrate vectors. These cases do not define the formula for A or E_trust.

Implementation MUST NOT:

- Allow override of Zeroth Law
- Skip Zeroth Law check under any condition
- Modify A or E_trust to force allow

Implementation MUST:

- Log all Zeroth Law evaluations
- Include A and E_trust in denial response
- Provide remediation guidance in denial

### Soul Constraint (Standard and Full)

Before Zeroth Law evaluation:

1. Check Soul constraint from Trust Proof
2. If S = 1: supervision = silent_veto with SOVEREIGNTY_CONSTRAINT (Soul Veto), skip Zeroth Law
3. If S = 0: Proceed to Zeroth Law

Soul Veto MUST:

- Take precedence over all other checks
- Be logged under its explicitly approved purpose, access and bounded retention policy
- Include constraint source in denial

## Tier Transitions

### Tier Boundaries (Standard and Full)

Implementations MUST use these boundaries:

~~~
+-------------+-----------------+
| Tier        | E_trust Range   |
+-------------+-----------------+
| Admin Mode  | >= 85           |
| Operator    | >= 72, < 85     |
| Analyst     | >= 58, < 72     |
| Observer    | >= 22, < 58     |
| Hibernation | < 22            |
+-------------+-----------------+
~~~

### Transition Handling

On tier transition:

MUST:

- Update agent's effective tier immediately
- Log transition to Flight Recorder
- Notify agent of transition (if possible)

SHOULD:

- Apply hysteresis (±2 points) to prevent oscillation
- Provide transition warning before demotion
- Allow grace period for in-flight operations

## Cryptographic Requirements

### Signature Algorithms

Basic Level:

- ES256 (ECDSA with P-256 and SHA-256) - REQUIRED
- Ed25519 - RECOMMENDED

Standard Level:

- ES256 - REQUIRED
- Ed25519 - REQUIRED
- Threshold signatures - REQUIRED

Full Level:

- All Standard algorithms
- ES384 (ECDSA with P-384) - RECOMMENDED
- Key rotation support - REQUIRED

### Hash Functions

All Levels:

- SHA-256 - REQUIRED for chaining and integrity
- SHA-384 - RECOMMENDED for Full level

### Key Management

Basic Level:

- Secure key storage
- Manual key rotation supported

Standard Level:

- HSM recommended for Oracle keys
- Automated key rotation
- Key versioning in proofs

Full Level:

- HSM required for Oracle keys
- Automated key rotation with zero downtime
- Complete key audit trail

# Test Suite

## Test Categories

The KTP test suite comprises four categories:

1. Unit Tests: Individual component functionality
2. Integration Tests: Component interaction
3. Interoperability Tests: Cross-implementation compatibility
4. Stress Tests: Performance under load

Each category has tests for each conformance level.

## Unit Tests

### Trust Oracle Unit Tests

Basic:

- TO-B-001: Risk Factor calculation accuracy
- TO-B-002: E_trust calculation accuracy
- TO-B-003: Trust Proof generation
- TO-B-004: Signature validation
- TO-B-005: Proof expiration enforcement

TO-B-005 MUST cover exact expiration (current_time = exp), the ten-second maximum at every conformance level, existing sessions, cached and queued requests, and continuing actions during Oracle failure. Invalid or unverifiable time MUST NOT extend authority. Implementations supporting emergency capability MUST additionally satisfy specifications/emergency-capability.md and the downstream cases in specifications/conformance/outage-safety-v1.json. A schema-valid policy is not evidence of verified approval, activation, or protected runtime enforcement.

Standard:

- TO-S-001: Threshold signature generation
- TO-S-002: Trust velocity calculation
- TO-S-003: Proof of Resilience calculation
- TO-S-004: Soul constraint handling
- TO-S-005: Mesh consensus (simulated)

Full:

- TO-F-001: Sub-second proof refresh
- TO-F-002: Real-time consensus
- TO-F-003: Geographic distribution handling
- TO-F-004: Extended proof generation (celestial)

### Oracle Consensus Adversarial Tests and Evidence

Implementations claiming Oracle mesh agreement MUST exercise the applicable requirements in specifications/oracle-consensus.md and specifications/conformance/oracle-consensus-v1.json against the selected protocol implementation. This applies to TO-S-005 and TO-F-002 and to any Basic implementation making a mesh agreement claim. Required adversarial coverage includes:

- A five-member, one-Byzantine leader equivocation schedule: conflicting values at the same sequence/predecessor obtain the disjoint honest voter sets {A, B} and {C, D}, with malicious X voting in both sets. Three votes MUST NOT establish either protected-state commitment under the default four-vote decision quorum.
- Quorum loss and delayed, reordered, duplicated, or replayed messages; signers MUST be distinct authenticated members of the installed configuration, and a partition MUST NOT lower its quorum or self-authorize a replacement membership.
- Conflicting votes and recovery after a crash at each durable vote, prepared/lock, and commit boundary; restarting MUST NOT erase safety obligations or permit conflicting commits.
- Leader/view changes with prepared or committed state, delayed old-view evidence, and safe lock transitions as defined by the selected protocol.
- Membership transitions, old and new epochs, configuration or key rollback, and evidence bound to the wrong zone, epoch, view, phase, sequence, predecessor, or operation.
- Threshold signing requests without verified commit evidence, valid signatures attached to the wrong committed result, and single-node proof issuance from uncommitted standing.
- Progress with the declared responsive honest quorum under the protocol's stated network assumptions, and safe cessation of new protected-state commitments without it; existing proof expiry and emergency boundaries remain in force.

Runtime certification evidence MUST identify the protocol and immutable version, implementation/build, declaration and installed configuration, fault and network model, review artifact, test schedules, durable-storage/recovery behavior, and observed decision and signing traces sufficient to check that no two conflicting protected-state commitments occurred. It MUST include actual implementation execution for the applicable cases and justify any protocol-specific mapping of the vectors. Full conformance retains independent certification requirements.

Declaration validation, JSON Schema checks, quorum-intersection calculations, and abstract model or repository vector checks are useful prerequisites. They MUST NOT be presented as runtime certification or proof that an implementation preserves agreement across crashes, view changes, or membership changes. Merely passing TO-S-005 in a simulator does not satisfy these implementation evidence requirements.

### Trajectory Signature, Head, and Cutover Tests

Every implementation issuing or accepting active trajectory records MUST satisfy specifications/trajectory-signatures.md and the schema at schemas/transaction-record.json with record_version = "ktp-trajectory-v3". The required executable format/cryptographic cases are in specifications/conformance/trajectory-signatures-v3.json, and mandatory downstream lifecycle cases are in specifications/conformance/trajectory-lifecycle-v3.json. Required coverage includes:

- Complete body binding: mutate every protected identity, zone, chain, sequence, timestamp, predecessor, previous/current state, action and nested action.details, friction, velocity, level, profile, and migration field while retaining the signatures. Include schema-valid changes to E_base and tier so a schema rejection is not mistaken for signature verification.
- Complete attestation binding: mutate Oracle identity, attestation time, each Risk Factor, or the exact embedded agent JWS; the Oracle signature MUST fail.
- RFC 8785 interoperability: object-order and whitespace equivalence, Unicode property ordering, escaped strings, numeric serialization and safe-integer limits, and rejection of duplicate names, invalid surrogates, or non-finite/out-of-profile numbers. Verify embedded payload bytes against reconstructed canonical bytes.
- Role and configuration binding: wrong agent/Oracle typ, unprotected or extra header members, wrong trusted key, algorithm or profile, detached/mismatched payload, candidate-selected downgrade, missing version, and v2 fallback after the durable v3 cutover MUST fail.
- Final-envelope hashing at Levels 1/2 and Level 3, including both exact signatures, and final-head evidence bound to record_version, the exact hash, commit_intent, agent, zone, chain, sequence, and predecessor. A valid signature pair with an unanchored or altered tail MUST NOT establish authority.
- Distinct commit-intent and final-head stages: changing the Oracle signature can produce another valid envelope for one intent; only the independently anchored final hash may be authoritative. An intent certificate alone, an unresolved evidence reference, or a candidate-chosen head MUST be insufficient.
- Legacy archival and migration: preserve original v2 bytes; reject automatic conversion or re-signing; verify the independently signed checkpoint, legacy head/archive, revalidated carried state, authorized target genesis/profile, and the new genesis checkpoint digest before separate final-genesis anchoring. Test double succession, checkpoint reuse, stale profile/key state, restart/restore rollback, and membership changes requiring the consensus joint transition.

Passing the repository schema, canonicalization, signature, and hash fixtures establishes only those exercised properties. It MUST NOT be reported as proof of an installed consensus runtime, trusted-key custody, independently verified carried state, correct governance approval, durable storage, or live head/migration enforcement. The helper's supported classical algorithms and Level 3 hash checks do not establish required hybrid signatures, threshold participation, or full Level 3 conformance. Certification additionally requires deployment execution traces showing the selected protocol's intent commitment, unique final-head selection, crash recovery, and durable single-use cutover under the Oracle consensus evidence requirements above. Legacy archive verification MUST NOT be counted as active-v3 conformance.

### Historical Standing and Scoped Readiness Tests

Active deployments MUST use the v3 deployment profile's standing_policy = {mode: "history-with-scoped-readiness-v1", profile_id, version, digest} and satisfy specifications/operational-readiness.md. They MUST reject standing_decay_rate and a missing or incompatible standing policy as active declarations. The archived published v2 schema is evidence for interpreting old records, not a permissive runtime fallback. Schema shape, semantic/cryptographic checks, and downstream runtime obligations are separate.

Required coverage includes:

- Keeping the applicable historical PoR contribution unchanged when only elapsed time or inactivity changes; distinguish this from an authenticated appended correction invalidating a historical claim and from other instruments' existing expiry/ceiling rules. Readiness expiry or renewal MUST NOT subtract or mint PoR.
- Exact operation, subject, lineage, software/model/configuration/toolchain/permissions, zone/resource/environment/parameter, and installed-profile matching. Missing operations or evidence MUST deny that operation; old historical standing, a narrow assessment, or another operation's pass MUST NOT reactivate every capability.
- Fresh challenge binding, every required check exactly once, and expiry bounded by the oldest required observation plus the installed maximum age. Heartbeats, new attestation IDs, a new cheap check, re-signing, or ordinary proof refresh MUST NOT refresh older required evidence.
- Complete canonical attestation and decision signatures with correct role, key, algorithm, and all nested bindings; wrong or substituted complete proof, request, assessment, profile, epoch, or signature envelope MUST fail. Include schema-valid mutations so schema rejection is not confused with cryptographic coverage.
- Independently registered complete active-attestation digest and readiness epoch, atomic challenge consumption, conflicting registration, known revocation or invalidation, and restoration of stale profiles or status after restart/failover. A still-valid unregistered or superseded signature MUST be insufficient.
- Ordinary proof and decision expiration at the exact boundary. The ordinary proof MUST NOT outlive the readiness supporting its dependent authority; the sidecar MUST expire no later than the proof, readiness, or applicable key validity. Continuing execution MUST cease through its existing bounded safe transition when a required condition is lost.
- A safe separately authorized assessment route that does not borrow the missing production authority, grant standing credits, lower supervision, or reverse Soul, capacity, or an earlier veto. Relabeling the blocked production operation as an assessment MUST fail.
- Durable migration to the active standing-policy/profile/format floor. Existing agents retain admissible historical PoR but begin with readiness unestablished for dependent scopes until independently assessed and activated. Renaming a lineage or profile, using an archived v2 declaration, or restoring a backup MUST NOT evade the floor or invalidation state.

scripts/readiness.py and scripts/test-readiness.py exercise supported declaration, semantic, and cryptographic checks with supplied trusted context. specifications/conformance/readiness-lifecycle-v1.json defines the required downstream lifecycle cases. Passing reference tests MUST NOT be presented as proof of actual assessment, independently authenticated running artifacts, assessor competence or independence, safe scope mapping, trusted registry installation, durable challenge/epoch stores, an Oracle consensus implementation, or ordinary authorization. Runtime conformance requires evidence for those deployed mechanisms. Neither the new prerequisite nor a passing assessment establishes fairness of evidence opportunities or calibration of the logarithmic PoR curve and tier attainment.

### Risk Factor Unit Tests

Basic:

- CT-B-001: Dimension normalization
- CT-B-002: Risk Factor aggregation
- CT-B-003: Sensor failure handling
- CT-B-004: Configuration loading

Standard:

- CT-S-001: All 7 input support
- CT-S-002: Risk domain aggregation
- CT-S-003: Feed weighting
- CT-S-004: Soul veto logic
- CT-S-005: Sensor validation

Full:

- CT-F-001: TK Label integration
- CT-F-002: Sub-second refresh
- CT-F-003: Sensor redundancy failover

### PEP Unit Tests

Basic:

- PEP-B-001: Trust Proof validation
- PEP-B-002: Zeroth Law enforcement
- PEP-B-003: Denial response format
- PEP-B-004: Logging completeness

Standard:

- PEP-S-001: Tier enforcement
- PEP-S-002: Soul veto enforcement
- PEP-S-003: Action risk classification
- PEP-S-004: Graceful degradation
- PEP-S-005: Decision Geometry reporting

Full:

- PEP-F-001: Latency < 15ms
- PEP-F-002: Zero-downtime update
- PEP-F-003: Defense in depth

### Flight Recorder Unit Tests

Basic:

- FR-B-001: Decision logging
- FR-B-002: Retention enforcement
- FR-B-003: Query by time range
- FR-B-004: Query by agent

Standard:

- FR-S-001: Cryptographic chaining
- FR-S-002: Tamper detection
- FR-S-003: Decision Geometry completeness
- FR-S-004: Multi-tier storage
- FR-S-005: Compliance export

Full:

- FR-F-001: External anchoring
- FR-F-002: Multi-region replication
- FR-F-003: Forensic reconstruction
- FR-F-004: Chain verification performance

## Integration Tests

### End-to-End Flow Tests

Basic:

- INT-B-001: Agent obtains proof and accesses resource
- INT-B-002: Agent denied due to A > E_trust
- INT-B-003: Environmental change affects E_trust

Standard:

- INT-S-001: Tier transition on E_trust change
- INT-S-002: Soul veto propagation
- INT-S-003: Oracle mesh failover
- INT-S-004: Federation handshake
- INT-S-005: Complete audit trail verification

Full:

- INT-F-001: Cross-zone agent migration
- INT-F-002: Celestial transit simulation
- INT-F-003: Complete disaster recovery

### Failure Mode Tests

All Levels:

- FAIL-001: Oracle unavailable
- FAIL-002: Sensor failure
- FAIL-003: PEP failure
- FAIL-004: Flight Recorder failure
- FAIL-005: Network partition

Standard/Full:

- FAIL-S-001: Oracle mesh node failure
- FAIL-S-002: Threshold signature node loss
- FAIL-S-003: Federation partner unavailable

## Interoperability Tests

### Trust Proof Exchange

- INTEROP-001: Proof generated by Impl A, validated by Impl B
- INTEROP-002: Threshold proof with mixed implementations
- INTEROP-003: Proof with all optional claims

### Federation Protocol

- INTEROP-010: Zone discovery across implementations
- INTEROP-011: Cross-zone attestation
- INTEROP-012: Trust factor negotiation

### Flight Recorder

- INTEROP-020: Decision record format compatibility
- INTEROP-021: Chain verification across implementations
- INTEROP-022: Export format compatibility

## Stress Tests

### Load Tests

- STRESS-001: 1000 proofs/second sustained
- STRESS-002: 10000 PEP evaluations/second
- STRESS-003: 1000 concurrent agents
- STRESS-004: Flight Recorder write throughput

### Chaos Tests

- CHAOS-001: Random Oracle node failure
- CHAOS-002: Random sensor failure
- CHAOS-003: Network latency injection
- CHAOS-004: Clock skew injection

# Certification Process

## Self-Certification

Self-certification is available for Basic and Standard levels.

### Self-Certification Process

1. Execute complete test suite for target level
2. Document all test results
3. Document any deviations with justification
4. Publish results to public repository
5. Submit certification claim

### Self-Certification Requirements

MUST:

- Pass 100% of required tests for level
- Document test execution environment
- Make test results publicly available
- Maintain certification with each release

MAY:

- Skip optional tests (clearly documented)
- Use custom test execution framework (if equivalent)

## Third-Party Certification

Third-party certification is required for Full level and available for all levels.

### Certification Bodies

Authorized certification bodies must:

- Demonstrate KTP expertise
- Maintain independence from implementers
- Follow documented certification procedures
- Publish certification criteria
- Maintain certification records

### Third-Party Process

1. Implementer submits for certification
2. Certification body reviews documentation
3. Certification body executes test suite
4. Certification body performs security review (Full only)
5. Certification body issues certificate or findings
6. Certificate published to registry

## Certification Maintenance

### Recertification Triggers

Recertification required when:

- Major version release
- Security vulnerability discovered and patched
- Significant architecture change
- Conformance level upgrade
- Annual renewal (Full level)

### Certification Revocation

Certification may be revoked for:

- Discovered non-compliance
- Security incident demonstrating inadequacy
- Failure to address reported issues
- False certification claims

# Interoperability

## Cross-Implementation Testing

Interoperability between implementations is essential for federation and ecosystem health.

### Interoperability Events

Regular interoperability testing events:

- Quarterly virtual plugfests
- Annual in-person interop event
- Continuous integration testing (automated)

### Interoperability Matrix

Maintain public matrix showing tested implementation pairs and compatibility status.

## Federation Compatibility

For federation to work, implementations must agree on:

- Zone discovery protocol
- Trust Proof format
- Attestation format
- Federation agreement structure

Interoperability tests verify cross-implementation federation.

## Version Compatibility

Implementations SHOULD support:

- Current specification version
- Previous major version (18-month deprecation)

Version negotiation required for federation.

# Conformance Claims

## Claim Format

Conformance claims MUST follow this format:

"\[Product Name] \[Version] conforms to KTP \[Level] per \[KTP-CONFORMANCE] \[Version], \[self-certified/certified by \[Certification Body]] on \[Date]."

Example:

"AcmeTrust v2.1 conforms to KTP Standard per KTP-CONFORMANCE v0.1, self-certified on 2025-11-25."

## Claim Verification

Claims can be verified by:

- Reviewing published test results (self-certification)
- Checking certification registry (third-party)
- Executing interoperability tests

# Security Considerations

## Test Suite Security

The test suite itself must be secure:

- Test data must not contain real credentials
- Test environments must be isolated
- Test results must be integrity-protected

## Certification Security

Certification process must be secure:

- Certification bodies must be vetted
- Certificates must be tamper-evident
- Revocation must be prompt and public

## Implementation Security

Conformance does not guarantee security:

- Conformance tests verify protocol correctness
- Security review is separate (required for Full)
- Deployment security is implementer responsibility

## Human Eligibility and Privacy Evidence Conformance

Deployments accepting human actions or human-origin delegation MUST satisfy specifications/human-eligibility.md and install the authenticated human_policy binding. Human eligibility is separate from software-agent standing and scoped readiness. A person label supplied by a request MUST NOT choose the verification path; the actual executing actor remains independently authenticated. Capacity, Soul, current grants and all ordinary-proof freshness requirements remain mandatory.

All deployments retaining personal evidence MUST satisfy specifications/privacy-evidence.md, including purpose boundaries, meaningful correction, limited retention, and truthful verification after erasure. Existing signed records MUST NOT be redacted in place. Schema validity and reference helper success establish neither identity nor legal compliance nor production erasure.

Required deployment cases are specifications/conformance/human-privacy-lifecycle-v1.json. Conformance evidence MUST distinguish repository-executed shape, semantic and cryptographic tests from runtime identity, assessment, authorization-adapter, review, state propagation, storage and disposal tests. An unsigned eligible decision body or erasure receipt MUST NOT itself be accepted as authenticated authority. Review and assistance MUST remain available when eligibility is denied. No conformance level creates a blanket permanent personal-data archive.

--- back

# Changes from v1

This appendix records what a v1 implementation must change to conform to
v2.0.0.  The break is deliberate and there is no dual-accept period: an
implementation reads v1 or it reads v2.

## The lineage stage names

The three lineage stages are renamed on the wire and in prose.  Numeric
protobuf values are unchanged, so only the symbol names move.

| v1 | v2.0.0 |
|----|--------|
| `tethered` | `sponsored` |
| `divergent` | `independent` |
| `persistent` | `guarantor` |

This affects agent identifier strings (`agent:<stage>:...`), the `lineage`
enum, and the protobuf `LineageType` member names.  The v1 words each carried
an unintended security reading - in jailbreak and intrusion vocabulary,
"tethered" means a compromise that dies at reboot and "persistent" is the
established word for one that survives a restart - and the three together read
as a coherent escalation narrative rather than as a maturity ladder.  Stage 3
is now named for what it can be held to rather than what it is freed of.

## The Trust Tier thresholds

| Tier | v1 | v2.0.0 |
|------|----|--------|
| Admin Mode | `E_trust >= 95` | `E_trust >= 85` |
| Operator Mode | `E_trust >= 85` | `E_trust >= 72` |
| Analyst Mode | `E_trust >= 70` | `E_trust >= 58` |
| Observer Mode | `E_trust >= 50` | `E_trust >= 22` |
| Hibernation | `E_trust < 50` | `E_trust < 22` |

The v1 set was unreachable from the v1 generation ceilings: generations 0
through 2 were capped below the lowest threshold, so an agent was in
Hibernation by lineage rather than by environment, and the top tier could not
be reached in any zone at the calm conditions the specification's own worked
example uses.  The generation ceilings are unchanged; one table moved, not two.

Two consequences travel with the change.  Hibernation exit moves from
`E_trust >= 55` to `E_trust >= 24`, because a five-point hysteresis over a
floor of 50 becomes a thirty-three-point one over a floor of 22.  And the
stable-conditions requirement for the top tier moves from `R < 0.05` to
`R < 0.10`, because 0.05 is stricter than the calm baseline the corpus
illustrates.

## Requirements Language

This document now invokes BCP 14.  Its normative keywords were previously
capitalised without the paragraph that gives them meaning.
