# KTP-Identity — Vector Identity

*Identity is not what you have. It's what you've been doing.*

---

> **Identity as Trajectory**: A trajectory cannot be stolen because it includes not just current position, but also where the entity came from, how fast it's moving, what resistance it encountered, and who witnessed the movement.

---

## At a Glance

| Property | Value |
|----------|-------|
| **Status** | :material-check-circle:{ .stable } Stable |
| **Version** | 0.1 |
| **Dependencies** | [KTP-Core](ktp-core.md) |
| **Required By** | [KTP-Federation](ktp-federation.md), [KTP-Governance](ktp-governance.md) |

---

## The Passport Fallacy

!!! failure annotate "Why Static Credentials Fail"
    Current identity systems commit three fatal errors:
    
    1. **Credentials can be stolen** — An attacker with your API key *is* you (1)
    2. **Credentials carry no history** — A stolen key at T=100 looks identical to a legitimate key at T=100 (2)
    3. **Credentials are static** — Once issued, the credential's "identity" never changes (3)

1. :material-star-four-points-circle: There's no mechanism to distinguish the legitimate holder from an impersonator presenting the same credential.
2. :material-star-four-points-circle: No record exists of how the presenter obtained the credential or what they did before presenting it.
3. :material-star-four-points-circle: Even if the presenting entity's behavior becomes anomalous or malicious, the credential remains "valid."

In the age of autonomous agents operating at machine speed, these flaws are catastrophic. An attacker who compromises one API key can spawn thousands of malicious agents in milliseconds, each presenting valid credentials.

---

## The Solution: Identity as Trajectory

KTP replaces static credentials with **trajectory-based authentication**:

=== "Static vs. Vector"
    
    | Static Model | Vector Model |
    |--------------|--------------|
    | Passport | Trajectory |
    | Credential | Chain |
    | Point | Line |
    | Possession | Movement |
    | Who you are | What you've been doing |
    | **Noun** | **Verb** |

=== "The Analogy"
    
    !!! example "Driver's License vs. Driving History"
        
        **Static**: "This person has a valid driver's license"
        
        **Kinetic**: "This person has been driving continuously for the last 10,000 miles, with traffic cameras and toll booths attesting to their route"
        
        The second model is vastly more resistant to impersonation. The attacker would need to not only steal the license but also fabricate a coherent 10,000-mile trajectory with consistent attestations from independent third parties.

=== "Position + Momentum"
    
    Vector Identity combines two components:
    
    | Component | What It Provides |
    |-----------|-----------------|
    | **Position** | Current Trust Score, permissions, context |
    | **Momentum** | Complete transaction history, attested by Oracles |
    
    Momentum carries **inertia**: an agent with deep history is "heavier" and harder to deflect from its trajectory.

---

## Core Components

???+ note "Trajectory Chain"
    Cryptographically linked transaction records forming unforgeable history.
    
    [Jump to section](#trajectory-chains)

???+ note "Proof of Resilience"
    Attestations of survival under stress—the primary input to $E_{base}$.
    
    [Jump to section](#proof-of-resilience)

???+ note "Sponsorship Bonds"
    Trust staking that solves the genesis problem for new agents.
    
    [Jump to section](#sponsorship-bonds)

???+ note "Lineage Evolution"
    The maturation path from Tethered → Divergent → Persistent.
    
    [Jump to section](#lineage-evolution)

---

## Trajectory Chains

The Trajectory Chain is the core data structure of Vector Identity—a cryptographically linked sequence of transaction records forming an unforgeable history.

### Chain Structure

``` mermaid
flowchart TB
    G["🌱 Genesis Transaction<br/>(sponsored)"] --> T1["Transaction Record 1"]
    T1 -->|"hash"| T2["Transaction Record 2"]
    T2 -->|"hash"| T3["Transaction Record 3"]
    T3 -->|"hash"| TN["...<br/>Transaction Record N<br/>(current)"]
```

!!! warning "Append-Only"
    The chain is **append-only**. Records MUST NOT be modified or deleted once added.

### Transaction Records

??? example "Transaction Record Structure"
    
    | Field | Type | Description |
    |-------|------|-------------|
    | `record_id` | string | Unique identifier |
    | `chain_id` | string | Agent's chain identifier |
    | `sequence` | integer | Position in chain (0 = genesis) |
    | `timestamp` | datetime | When transaction occurred |
    | `previous_hash` | string | SHA-256 of previous record |
    | `previous_state` | object | Agent state before |
    | `current_state` | object | Agent state after |
    | `action` | object | What action was performed |
    | `friction` | number | Environmental $R$ at time |
    | `velocity` | number | Agent's transaction rate |
    | `agent_signature` | string | Agent's signature |
    | `oracle_attestation` | object | Trust Oracle's attestation |

### Co-Signature Requirement

Every record requires **dual signatures**—agent AND Oracle:

``` mermaid
sequenceDiagram
    autonumber
    participant Agent
    participant Oracle as Trust Oracle
    
    Agent->>Agent: Compute action, sign record
    Agent->>Oracle: Submit with signature
    Oracle->>Oracle: Validate signature, action, environment
    Oracle->>Oracle: Add attestation, sign
    Oracle-->>Agent: Complete record appended
```

This prevents:

- **Agent fabrication** — Can't create records without Oracle attestation
- **Oracle fabrication** — Can't create records without agent participation  
- **Replay attacks** — Both signatures include timestamp and previous hash

### Continuity Enforcement

Trajectory Chains enforce **physical continuity**—agents cannot teleport:

| Rule | Requirement |
|------|-------------|
| Sequential numbering | `sequence(N) = sequence(N-1) + 1` |
| Hash linking | `previous_hash(N) = record_hash(N-1)` |
| Temporal ordering | `timestamp(N) > timestamp(N-1)` |
| State consistency | `previous_state(N) = current_state(N-1)` |
| Velocity bounds | Distance/time within configured limits |

!!! danger "Continuity Violations"
    If a record fails any continuity check, the Trust Oracle MUST:
    
    1. Reject the transaction
    2. Flag the agent for investigation
    3. Log the violation to the Flight Recorder
    4. Optionally freeze the agent's Trust Score
    
    Continuity violations strongly indicate either agent compromise or Oracle compromise.

---

## Proof of Resilience

Proof of Resilience is a ledger of attestations demonstrating survival under stress. It's the **primary input to $E_{base}$ calculation**.

### Friction Categories

| Category | $R$ Range | Weight | Description |
|----------|-----------|--------|-------------|
| CALM | 0.0–0.3 | — | Normal operations, *no attestation* |
| ELEVATED | 0.3–0.5 | 1.0× | Moderate stress |
| HIGH | 0.5–0.7 | 2.0× | Significant stress |
| SEVERE | 0.7–0.9 | 5.0× | Near-crisis conditions |
| CRISIS | 0.9–1.0 | 10.0× | Critical conditions |

!!! tip "Quality Over Quantity"
    One successful action during CRISIS earns the same Resilience Score as **ten** actions during ELEVATED conditions.

### Resilience Score Calculation

$$\text{Resilience\_Score} = \sum_{i} (\text{weight}_i \times \text{risk}_i)$$

Converted to $E_{base}$ contribution:

$$\text{PoR\_contribution} = \min(70, 10 \times \log_{10}(1 + \text{Resilience\_Score}))$$

??? example "Quality vs. Quantity Example"
    
    **Agent A** (volume-focused):
    
    - 100,000 transactions
    - All under CALM conditions ($R < 0.3$)
    - **0 attestations** → Resilience Score: **0**
    
    **Agent B** (battle-tested):
    
    - 10,000 transactions
    - 500 under ELEVATED, 50 under HIGH, 5 under CRISIS
    - Resilience Score: $500 \times 1.0 \times 0.5 + 50 \times 2.0 \times 0.5 + 5 \times 10.0 \times 0.5 = 325$
    - PoR contribution: $10 \times \log_{10}(326) = 25.1$
    
    Agent A has 10× the volume but **zero** Proof of Resilience. Agent B has actually been tested under fire.

---

## Sponsorship Bonds

Sponsorship Bonds solve the **genesis problem**: how can a new agent with zero history begin operating in a system that requires history to earn trust?

### The Catch-22

``` mermaid
flowchart LR
    E["Need E_base"] --> T["Complete transactions"]
    T --> E2["Need E_trust > A"]
    E2 --> E3["E_trust = E_base × (1-R)"]
    E3 --> E4["If E_base = 0..."]
    E4 --> E5["E_trust = 0"]
    E5 --> E6["❌ All actions blocked"]
    E6 -.->|"Sponsorship<br/>breaks cycle"| E
```

### Bond Mechanics

When a sponsor stakes trust on a new agent:

1. **Sponsor's stake is locked**: `available_E_base = E_base - stake_amount`
2. **Sponsored agent receives initial trust**: `sponsored_E_base = stake_amount × 0.5`
3. **Bond registered with Trust Oracle**: Monitors both agents, tracks violations

??? warning "Penalty for Bad Actors"
    If the sponsored agent commits a violation:
    
    $$\text{penalty} = \text{severity} \times \text{stake\_amount} \times \text{penalty\_rate}$$
    
    | Severity | Multiplier | Example |
    |----------|------------|---------|
    | MINOR | 0.1 | Excessive failed attempts |
    | MODERATE | 0.3 | Unauthorized data access |
    | SEVERE | 0.7 | System disruption |
    | CRITICAL | 1.0 | Security breach, data loss |

### Anti-Botnet Properties

!!! success "Economics Prevent Mass Agent Creation"
    
    **Without bonds**: Attacker spawns 10,000 agents from one API key → swarm overwhelms defenses
    
    **With bonds**: 
    
    - Attacker has $E_{base} = 87$
    - Maximum stake = 10% = 8.7 per agent
    - To spawn 10,000 agents needs 87,000 staked $E_{base}$
    - Attacker can spawn **at most 10 agents** (87 ÷ 8.7)
    - Each agent has minimal capabilities ($E_{base} = 4.35$)
    
    The economics of trust prevent mass agent creation.

---

## Lineage Evolution

Agents mature through three phases, each with expanding capabilities:

``` mermaid
flowchart LR
    T["🐣 Tethered<br/>(Apprentice)"] -->|"30+ days<br/>PoR > 1,000"| D["🚀 Divergent<br/>(Journeyman)"]
    D -->|"180+ days<br/>PoR > 10,000<br/>E_base > 60"| P["👑 Persistent<br/>(Master)"]
```

=== "🐣 Tethered (Apprentice)"
    
    New agents bound to their sponsor with significant restrictions.
    
    | Property | Value |
    |----------|-------|
    | Identity | `Agent/Sponsor` (e.g., "Aria/Acme-Deploy") |
    | $E_{base}$ cap | 40 (derived from sponsor stake) |
    | Trust Tier cap | Analyst Mode ($E_{trust} \leq 70$) |
    | Action cap | $A \leq 50$ (lower-risk only) |
    | Sponsor liability | **Full** |
    
    **Identifier**: `agent:tethered:<sponsor_id>:<agent_name>:<unique_id>`

=== "🚀 Divergent (Journeyman)"
    
    Building independent identity while retaining lineage connection.
    
    | Property | Value |
    |----------|-------|
    | Identity | `Aria-3Gen-AcmeLine` |
    | $E_{base}$ range | 40–80 (growing intrinsic) |
    | Trust Tier cap | Operator Mode ($E_{trust} \leq 85$) |
    | Action cap | $A \leq 75$ (moderate-risk) |
    | Sponsor liability | **Reduced** (proportional to remaining stake) |
    
    **Identifier**: `agent:divergent:<generation>gen:<lineage>:<unique_id>`

=== "👑 Persistent (Master)"
    
    Fully autonomous with independent identity.
    
    | Property | Value |
    |----------|-------|
    | Identity | `Agent_7Gen_Optimized` |
    | $E_{base}$ | 80+ (high intrinsic) |
    | Trust Tier | God Mode ($E_{trust} \leq 95+$) |
    | Action cap | $A \leq 95$ (all operations) |
    | Sponsor liability | **None** (bond released) |
    
    **Special privileges**:
    
    - Can sponsor Tethered agents
    - Contributes Ancestral Authority to descendants
    - Preferential routing during network stress
    - Higher-weight attestations in federation
    
    **Identifier**: `agent:persistent:<generation>gen:<unique_id>`

---

## Flow Patterns

Agents exhibit characteristic flow patterns that indicate operational state:

| Pattern | Characteristics | Interpretation |
|---------|-----------------|----------------|
| **Laminar** | Consistent velocity, predictable trajectory, normal friction response | ✅ Legitimate operation |
| **Turbulent** | Erratic velocity, chaotic trajectory, ignores environmental stress | ⚠️ Potential compromise |

!!! info "Flow Monitoring"
    Implementations SHOULD monitor agent flow patterns. The Trust Oracle MAY reduce an agent's $E_{base}$ if sustained turbulent flow is detected, even if individual transactions succeed.

---

## Identity Proofing

KTP aligns with NIST 800-63 Identity Assurance Levels:

| IAL | Proofing | KTP Capabilities |
|-----|----------|------------------|
| **IAL1** | Self-asserted | Cannot sponsor, max $E_{base} = 40$ |
| **IAL2** | Remote or in-person proofing | Can sponsor Tethered, max $E_{base} = 80$ |
| **IAL3** | In-person with biometric | Can sponsor all lineages, max $E_{base} = 95$ |

??? abstract "Privacy Requirements"
    Identity proofing collects sensitive personal information. Implementations MUST:
    
    - Minimize data collection
    - Encrypt identity data at rest and in transit
    - Implement data retention limits
    - Support data subject access requests (GDPR, CCPA)
    - **Never** expose raw identity evidence in Trust Proofs

---

??? info "Related Specifications"
    - **[KTP-Core](ktp-core.md)** — Foundation protocol, Zeroth Law, and Trust Score calculation.
    - **[KTP-Crypto](ktp-crypto.md)** — Cryptographic primitives for signatures and hashing.
    - **[KTP-Federation](ktp-federation.md)** — Cross-zone identity verification and trust transfer.
    - **[KTP-Governance](ktp-governance.md)** — Sponsor accountability and identity dispute resolution.
    - **[KTP-Audit](ktp-audit.md)** — Immutable decision logging for identity events.

---

## Official RFC Document

??? note "View Complete RFC Text (ktp-identity.txt)"
    ```text
    --8<-- "rfcs-txt/ktp-identity.txt"
    ```
