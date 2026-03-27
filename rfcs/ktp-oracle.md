---
title: "Kinetic Trust Protocol - Trust Oracle Specification"
abbrev: "KTP-ORACLE"
docname: draft-perkins-ktp-oracle-00
date: 2025-12
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

informative:
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-GRAVITY:
    title: "Kinetic Trust Protocol - Digital Gravity Specification"
    author:
      - name: Chris Perkins
    date: 2025-12

--- abstract

This document specifies the Trust Oracle for the Kinetic Trust Protocol
(KTP). The Trust Oracle is the authoritative source of trust state within
a zone—issuing Trust Proofs, co-signing trajectory records, calculating
environmental stability (E), and enforcing Digital Gravity. The
specification covers Oracle architecture, consensus mechanisms, threshold
signatures, mesh topology, Oracle accountability, and Oracle-to-Oracle
federation.

--- middle

# Introduction

The Trust Oracle is the nerve center of a KTP zone. It performs the
calculations that make Digital Gravity possible:

- Collects Context Tensor measurements
- Calculates Risk Factor (R) and Environmental Stability (E)
- Issues Trust Proofs to agents
- Co-signs trajectory chain transactions
- Enforces the Zeroth Law (A ≤ E)
- Applies gravity constraints when needed
- Attests to agent behavior for Proof of Resilience

Without a functioning Trust Oracle, KTP cannot operate. The Oracle
is both critical infrastructure and potential single point of failure.
This specification addresses both the capabilities required and the
resilience necessary.

## Design Principles

The Trust Oracle embodies these principles:

1. **Availability**: The Oracle MUST be available for zone operation.
   Downtime means agents cannot act.

2. **Integrity**: Oracle decisions MUST be consistent and correct.
   Corrupted Oracles corrupt the entire trust system.

3. **Accountability**: Oracles are themselves subject to KTP. They
   cannot exempt themselves from physics.

4. **Transparency**: Oracle operations MUST be auditable. Trust
   requires visibility.

5. **Resilience**: Single Oracle failure MUST NOT disable the zone.
   Redundancy is required.

6. **Performance**: Oracle latency MUST NOT bottleneck agent
   operations. Speed matters.

## Requirements Language

{::boilerplate bcp14-tagged}

# Terminology

Attestation
: A signed statement by the Oracle confirming some fact about an
  agent or transaction.

Consensus
: Agreement among multiple Oracle nodes on trust state.

Oracle Mesh
: A network of connected Oracle nodes providing redundancy and
  consensus.

Oracle Node
: A single instance of Trust Oracle software and associated
  cryptographic identity.

Quorum
: The minimum number of Oracle nodes required for valid decisions.

Split Brain
: A failure mode where Oracle nodes disagree and cannot reach
  consensus.

Threshold Signature
: A cryptographic signature requiring M-of-N participants to
  produce.

Trust Proof
: A signed attestation of an agent's current trust state, issued
  by the Oracle.

# Oracle Architecture

## Single Node Architecture

A single Oracle node contains:

~~~
+------------------------------------------------------------------+
|                       TRUST ORACLE NODE                          |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    Tensor Collector                         |  |
|  |   Receives measurements from all six Context Tensors        |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                    Risk Calculator                          |  |
|  |   R = weighted_aggregate(tensor_risks)                      |  |
|  |   E = E_base × (1 - R)                                      |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Zeroth Law Engine                         |  |
|  |   Evaluates A ≤ E for every action request                  |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Gravity Calculator                        |  |
|  |   G = f(A, E, threshold) — determines constraint level      |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Trust Proof Issuer                        |  |
|  |   Issues signed Trust Proofs to agents                      |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                  Trajectory Co-Signer                       |  |
|  |   Co-signs agent transaction records                        |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Attestation Engine                        |  |
|  |   Issues Proof of Resilience attestations                   |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                    Key Management                           |  |
|  |   HSM-backed cryptographic operations                       |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|  +------------------------------------------------------------+  |
|  |                   Consensus Client                          |  |
|  |   Participates in Oracle Mesh consensus                     |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
~~~

## Component Specifications

### Tensor Collector

The Tensor Collector receives measurements from Context Tensor
instrumentation:

| Input | Source | Rate |
|-------|--------|------|
| Soul Tensor | Agent behavior monitoring | Per transaction |
| Body Tensor | Infrastructure monitoring | 1-100 Hz |
| World Tensor | Environmental sensors/simulation | 0.1-10 Hz |
| Time Tensor | Time subsystem | Per transaction |
| Relational Tensor | Relationship monitoring | Per interaction |
| Signal Tensor | Information environment monitoring | 1 Hz |

The Collector MUST:
- Validate incoming measurements
- Detect anomalous or spoofed data
- Maintain measurement history for smoothing
- Provide current tensor state on demand

### Risk Calculator

The Risk Calculator computes R from tensor measurements:

~~~
R = Σ(tensor_risk_i × weight_i) for i in tensors

Where weights sum to 1.0 (default):
  soul_weight = 0.25
  body_weight = 0.10
  world_weight = 0.15
  time_weight = 0.15
  relational_weight = 0.20
  signal_weight = 0.15
~~~

The Calculator MUST:
- Update R within 10ms of tensor change
- Apply temporal smoothing to prevent oscillation
- Handle missing tensor data gracefully
- Log R changes for audit

### Zeroth Law Engine

The Zeroth Law Engine evaluates A ≤ E for every action:

~~~
Input: action_request {
  agent_id,
  action_type,
  target,
  parameters
}

Process:
  1. Calculate A = autonomy(action_request)
  2. Retrieve agent E_base
  3. Get current R
  4. Calculate E = E_base × (1 - R)
  5. Evaluate A ≤ E

Output: {
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

~~~json
{
  "proof_id": "tp-2025-12-03-001",
  "agent_id": "agent:divergent:3gen:acme:abc123",
  "issued_at": "2025-12-03T14:32:15.123Z",
  "expires_at": "2025-12-03T14:32:25.123Z",
  "trust_state": {
    "e_base": 55,
    "e_trust": 44,
    "r_current": 0.2,
    "tier": "analyst",
    "lineage": "divergent",
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
- Have short expiration (default: 10 seconds)
- Be signed by Oracle key
- Include current trust state
- Be verifiable by any party with Oracle public key

### Trajectory Co-Signer

The Co-Signer adds Oracle attestation to trajectory records:

~~~
Input: transaction_record (agent-signed)

Process:
  1. Verify agent signature
  2. Verify action was permitted
  3. Verify state transitions are valid
  4. Capture tensor snapshot
  5. Add Oracle attestation
  6. Sign complete record

Output: transaction_record (co-signed)
~~~

The Co-Signer MUST:
- Verify before signing (never blind sign)
- Include tensor snapshot at time of transaction
- Refuse to sign invalid records
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

All-to-all connectivity for consensus
~~~

## Mesh Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Node count | 3 | 5-7 |
| Geographic distribution | 2 locations | 3+ locations |
| Network latency (inter-node) | <100ms | <50ms |
| Quorum for operations | (N/2)+1 | (2N/3)+1 |

## Node Roles

All nodes are peers, but roles may be assigned:

| Role | Responsibility |
|------|----------------|
| Primary | Receives agent requests, coordinates consensus |
| Secondary | Participates in consensus, can become primary |
| Witness | Participates in consensus, does not serve requests |

Primary selection uses leader election:
- Highest-uptime node becomes primary
- Automatic failover on primary failure
- No single primary required (multi-primary possible)

# Consensus Mechanisms

## Consensus Requirements

Oracle consensus must achieve:

1. **Agreement**: All honest nodes reach same decision
2. **Validity**: Decision reflects actual trust state
3. **Termination**: Decision is reached in bounded time
4. **Fault tolerance**: Tolerates f < N/3 Byzantine failures

## Consensus Protocol

The Oracle Mesh uses a simplified PBFT-style consensus:

~~~
Phase 1: PRE-PREPARE
  Primary receives request
  Primary assigns sequence number
  Primary broadcasts <PRE-PREPARE, seq, request> to all nodes

Phase 2: PREPARE
  Nodes verify request
  Nodes broadcast <PREPARE, seq, digest> to all nodes
  Node enters PREPARED state when 2f+1 PREPARE messages received

Phase 3: COMMIT
  Nodes broadcast <COMMIT, seq, digest> to all nodes
  Node enters COMMITTED state when 2f+1 COMMIT messages received
  Node executes request and responds to client
~~~

## Consensus Scope

Not all operations require full consensus:

| Operation | Consensus Required |
|-----------|-------------------|
| Trust Proof issuance | No (single node sufficient) |
| Zeroth Law evaluation | No (single node sufficient) |
| Trajectory co-signing | Yes (quorum required) |
| E_base modification | Yes (quorum required) |
| Agent Genesis | Yes (quorum required) |
| Zone configuration change | Yes (supermajority required) |

## Split Brain Prevention

Split brain occurs when network partition creates multiple
sub-quorums. Prevention:

1. **Quorum requirement**: Operations require (N/2)+1 nodes
2. **Fencing**: Partitioned nodes fence themselves
3. **Witness nodes**: Odd number of nodes prevents even splits
4. **Merge protocol**: Reconciliation when partition heals

# Threshold Signatures

## Overview

Critical Oracle operations use threshold signatures—requiring M of N
Oracle nodes to produce a valid signature.

~~~
Standard signature: 1 key → 1 signature
Threshold signature: M of N key shares → 1 signature

Example (3-of-5):
  Node 1 holds share 1
  Node 2 holds share 2
  Node 3 holds share 3
  Node 4 holds share 4
  Node 5 holds share 5

  Any 3 nodes can combine shares to produce valid signature
  No single node can sign alone
  Signature is indistinguishable from standard signature
~~~

## Threshold Scheme

The Oracle uses Shamir's Secret Sharing with threshold ECDSA:

| Parameter | Description | Default |
|-----------|-------------|---------|
| N | Total key shares | 5 |
| M | Threshold for signing | 3 |
| Curve | Elliptic curve | secp256k1 |
| Hash | Hash algorithm | SHA-256 |

## Key Ceremony

Threshold keys are generated in a key ceremony:

~~~
1. All N nodes generate random contributions
2. Contributions are combined using DKG protocol
3. Each node receives its key share
4. No node ever sees complete private key
5. Public key is published
6. Ceremony is recorded and witnessed
~~~

## Operations Requiring Threshold Signature

| Operation | Threshold |
|-----------|-----------|
| Agent Genesis transaction | 3-of-5 |
| E_base modification | 3-of-5 |
| Zone configuration change | 4-of-5 |
| Oracle key rotation | 4-of-5 |
| Zone dissolution | 5-of-5 |

# Trust Proof Lifecycle

## Issuance

Trust Proofs are issued on demand:

~~~
Agent → Oracle: RequestTrustProof(agent_id)
Oracle:
  1. Verify agent identity
  2. Calculate current E_trust
  3. Determine tier and constraints
  4. Create Trust Proof
  5. Sign with Oracle key
Oracle → Agent: TrustProof
~~~

## Validation

Any party can validate a Trust Proof:

~~~
Validator:
  1. Check proof not expired
  2. Verify Oracle signature against known public key
  3. Verify agent_id matches expected agent
  4. Check constraints are appropriate for action
~~~

## Refresh

Trust Proofs expire quickly and must be refreshed:

| Zone Type | Default Expiration | Refresh Recommendation |
|-----------|-------------------|------------------------|
| Deep Blue | 5 seconds | Continuous |
| Blue | 10 seconds | Every 5 seconds |
| Cyan | 30 seconds | Every 15 seconds |
| Green | 60 seconds | Every 30 seconds |

## Revocation

Trust Proofs can be revoked before expiration:

~~~
Oracle: RevokeTrustProof(proof_id, reason)
  1. Add proof_id to revocation list
  2. Broadcast revocation to mesh
  3. Notify agent
  4. Log revocation
~~~

Revocation reasons:
- Agent violation detected
- E_base reduced
- Zone policy change
- Security incident

# Oracle Accountability

## Oracles Under Gravity

The recursive constraint principle: Oracles are subject to KTP.

~~~
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
~~~

## Oracle Trajectory

Oracles maintain their own trajectory chains:

~~~json
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

| Event | Logged Data |
|-------|-------------|
| Trust Proof issued | Proof details, agent, timestamp |
| Transaction co-signed | Transaction hash, agent, result |
| Zeroth Law evaluation | A, E, result, agent, action |
| Consensus participation | Vote, sequence, outcome |
| Configuration change | Change details, authorizer |

## Oracle Misbehavior

Detected misbehavior triggers consequences:

| Misbehavior | Detection | Consequence |
|-------------|-----------|-------------|
| Signing invalid transaction | Peer verification | E_base reduction |
| Consensus equivocation | Protocol detection | Removal from mesh |
| Availability failure | Heartbeat timeout | Temporary removal |
| Byzantine behavior | BFT detection | Permanent removal |

# Federation

## Oracle-to-Oracle Federation

Oracles in different zones can federate:

~~~
Zone A Oracle <---> Zone B Oracle

Federation enables:
  - Cross-zone Trust Proof validation
  - Trajectory verification requests
  - Exit Attestation verification
  - Coordinated emergency response
~~~

## Federation Establishment

~~~
1. Zone A Oracle requests federation with Zone B
2. Zone B reviews Zone A governance and attestations
3. Both zones sign Federation Agreement
4. Public keys exchanged
5. Trust factors established
6. Federation active
~~~

## Federation Trust Factor

Trust is discounted across federation:

~~~json
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

| Operation | Federation Requirement |
|-----------|----------------------|
| Validate foreign Trust Proof | Federation active |
| Verify foreign trajectory | Federation active |
| Accept Exit Attestation | Federation active |
| Cross-zone agent migration | Federation active |

# Performance Requirements

## Latency Targets

| Operation | Target | Maximum |
|-----------|--------|---------|
| Trust Proof issuance | 5ms | 20ms |
| Zeroth Law evaluation | 1ms | 5ms |
| Transaction co-signing | 10ms | 50ms |
| Consensus round | 50ms | 200ms |

## Throughput Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Trust Proofs/second | 10,000 | Per node |
| Evaluations/second | 100,000 | Per node |
| Co-signatures/second | 1,000 | Consensus limited |

## Availability Targets

| Metric | Target |
|--------|--------|
| Zone availability | 99.99% |
| Single node availability | 99.9% |
| Recovery time (node failure) | <10 seconds |
| Recovery time (quorum loss) | <60 seconds |

# Deployment Models

## Cloud Deployment

~~~
+------------------+    +------------------+    +------------------+
|   Region A       |    |   Region B       |    |   Region C       |
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
|   Data Center A  |    |   Data Center B  |
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
|   On-Premises    |    |   Cloud A        |    |   Cloud B        |
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

The mesh tolerates Byzantine (malicious) nodes:

- Up to f < N/3 Byzantine nodes tolerated
- Byzantine behavior detected by protocol
- Detected Byzantine nodes removed
- Mesh continues with remaining honest nodes

## Oracle Compromise Response

If Oracle compromise is detected:

1. Isolate compromised node
2. Revoke node's key share
3. Issue key rotation if threshold compromised
4. Audit all recent decisions
5. Notify affected agents
6. Post-incident review

# IANA Considerations

This document has no IANA actions.

--- back

# Appendix A: Oracle Node Specification

Hardware and software requirements for Oracle nodes.

## Minimum Hardware

| Component | Requirement |
|-----------|-------------|
| CPU | 8 cores, 3+ GHz |
| RAM | 32 GB |
| Storage | 500 GB NVMe SSD |
| Network | 1 Gbps |
| HSM | FIPS 140-2 Level 3 |

## Recommended Hardware

| Component | Requirement |
|-----------|-------------|
| CPU | 16+ cores, 3.5+ GHz |
| RAM | 64 GB |
| Storage | 1 TB NVMe SSD (RAID) |
| Network | 10 Gbps |
| HSM | FIPS 140-2 Level 3, HA |

# Appendix B: Consensus Protocol Details

Detailed specification of the consensus protocol.

# Appendix C: Threshold Signature Implementation

Implementation guidance for threshold ECDSA.

# Acknowledgments

The Trust Oracle design draws on distributed systems research,
Byzantine fault tolerance literature, and production experience
with consensus systems.
