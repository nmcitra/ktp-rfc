# KTP-Core — The Foundation Protocol

*Where authorization follows the environment*

---

> **The Zeroth Law**: An agent's autonomy must never exceed the environment's stability.

$$A \leq E$$

This single constraint is the foundation of everything in KTP.

---

## At a Glance

| Property | Value |
|----------|-------|
| **Status** | :material-check-circle:{ .stable } Stable |
| **Version** | 0.1 |
| **Dependencies** | None (foundation) |
| **Required By** | All other KTP specifications |

---

## The Problem

!!! failure annotate "Why Static Authorization Fails"
    Current authorization systems suffer from three fatal flaws:
    
    1. **The Passport Fallacy** — Possession of a credential equals identity (1)
    2. **The Static Fallacy** — Permissions verified at time T remain valid at T+1 (2)
    3. **The Vacuum Fallacy** — Authorization is independent of environmental conditions (3)

1. :material-star-four-points-circle: A stolen API key looks identical to a legitimate one. There's no mechanism to detect the presenter isn't the original holder.
2. :material-star-four-points-circle: In the milliseconds between verification and action, the environment may change dramatically—network compromise, capacity exhaustion, attack initiation.
3. :material-star-four-points-circle: A credential permitting "delete database" grants the same permission whether the system is idle or at 99% capacity under active attack.

These flaws create catastrophic risk. An autonomous agent executing thousands of API calls per second with even 0.1% contextually destructive actions compounds damage exponentially before any human can respond.

---

## The Solution

KTP treats authorization as a property of the **environment**, not a policy choice.

=== "The Insight"
    
    Instead of asking *"Does this agent have permission?"*, KTP asks:
    
    > **Can this environment safely support this action right now?**
    
    The environment becomes the final authority. Just as friction vetoes a sprinter's attempt to run on ice, environmental constraints veto an agent's attempt to act beyond the system's current capacity.

=== "The Equation"
    
    $$E_{trust} = E_{base} \times (1 - R)$$
    
    | Symbol | Meaning | Range |
    |--------|---------|-------|
    | $E_{trust}$ | Effective Trust Score | 0–100 |
    | $E_{base}$ | Base Trust (agent capability) | 0–100 |
    | $R$ | Risk Factor (environmental stress) | 0–1 |

=== "The Constraint"
    
    For any action to proceed:
    
    $$A \leq E_{trust}$$
    
    If the action's risk ($A$) exceeds the environment's capacity ($E_{trust}$), the action is **automatically denied**. No exceptions. No override.

---

## Core Components

???+ note "Zeroth Law"
    The inviolable constraint $A \leq E$ that governs all authorization decisions.
    
    [Jump to section](#the-zeroth-law)

???+ note "Trust Score"
    Dynamic calculation combining agent history with environmental reality.
    
    [Jump to section](#trust-score-calculation)

???+ note "Risk Factors"
    Six weighted environmental inputs plus the Soul veto.
    
    [Jump to section](#risk-factors)

???+ note "Trust Proof"
    Cryptographically signed token carrying real-time trust state.
    
    [Jump to section](#trust-proof-token)

???+ note "Silent Veto"
    Automatic action denial when $A > E_{trust}$ — structure, not policy.
    
    [Jump to section](#silent-veto-mechanism)

???+ note "Trust Oracle"
    Distributed authority for Trust Score calculation and attestation.
    
    [Jump to section](#trust-oracle)

---

## The Zeroth Law

The naming is intentional. Just as thermodynamics' Zeroth Law (thermal equilibrium) was recognized as more fundamental than the existing First, Second, and Third Laws, KTP's Zeroth Law precedes all other authorization considerations.

!!! warning "No Override Mechanism"
    There is no "emergency override." The only ways to permit a high-risk action are:
    
    1. Reduce the action's risk classification ($A$)
    2. Increase the agent's base trust ($E_{base}$) through demonstrated resilience
    3. Wait for environmental conditions to improve ($R$ decreases)
    
    This is intentional. In emergencies, the human instinct to override safety controls is often catastrophically wrong.

??? info "Why No Override?"
    By removing override capability, KTP forces systems to operate within their actual capacity, even when humans wish they could exceed it.
    
    Consider: A pilot cannot override the laws of aerodynamics by declaring an emergency. The plane will stall regardless of intention. KTP creates analogous constraints for digital systems.

### Enforcement

Enforcement is **cryptographic**, not administrative:

``` mermaid
flowchart TD
    subgraph TP["Trust Proof Contains"]
        E["E_trust value"]
        S["Oracle signature"]
        T["Timestamp"]
    end
    
    subgraph PEP["PEP Verification"]
        V1{"Signature valid?"}
        V2{"Token expired?"}
        V3{"A ≤ E_trust?"}
    end
    
    TP --> V1
    V1 -->|No| DENY["❌ DENY"]
    V1 -->|Yes| V2
    V2 -->|Yes| REFRESH["🔄 REFRESH"]
    V2 -->|No| V3
    V3 -->|No| VETO["🛑 SILENT VETO"]
    V3 -->|Yes| ALLOW["✅ ALLOW"]
```

---

## Trust Score Calculation

### Base Trust ($E_{base}$)

Base Trust represents intrinsic capability, independent of current conditions:

| Component | Weight | Description |
|-----------|--------|-------------|
| Proof of Resilience | 70% | Historical performance, especially under stress |
| Lineage Generation | 20% | Evolutionary maturity of the agent |
| Sponsor Weight | 10% | For Tethered agents, sponsor contribution |

- An agent with 10,000 transactions during crises has higher $E_{base}$ than one with 100,000 transactions in calm conditions. Survival under adversity matters more than volume.
- **Lineage caps:**
    - **Generation 0-2 (Tethered)** capped at 40.
    - **Generation 3-5 (Divergent)** capped at 70.
    - **Generation 6+ (Persistent)** uncapped.
- Sponsor's $E_{base}$ × stake percentage. A high-trust sponsor vouching for a new agent transfers partial trust.

??? example "Base Trust Calculation"
    ```
    E_base = (PoR_score × 0.70) + (Lineage_cap × 0.20) + (Sponsor_contribution × 0.10)
    
    Where:
      PoR_score = the Proof of Resilience contribution, computed as
                  specified in [KTP-IDENTITY] Section 5.3. This
                  document MUST NOT restate that computation.
      Lineage_cap = min(generation × 15, 100)
      Sponsor_contribution = Sponsor_E_base × stake_percentage
    ```

Proof of Resilience is a function of attestations earned under friction, not of transaction volume. An agent's transaction count bounds $E_{base}$ through the trajectory-length requirement of *Trust Score Integrity*; it is not an input to `PoR_score`. See [KTP-IDENTITY] Section 5.4.

### Risk Factor ($R$)

The Risk Factor aggregates environmental stress from the six weighted inputs:

$$R = \sum_{i} w_i \times s_i$$

Where $w_i$ are domain weights and $s_i$ are normalized sensor values.

Every $s_i$ is a **stress** term: 1 is maximum stress, 0 is its absence, whatever the dimension is named. The conservative substitute for a term that cannot currently be observed is therefore 1.0 — never 0, which measures perfect conditions rather than unknown ones.

This is one instance of the class rule stated in §6.7: an input that is absent, unanswered, stale beyond its declared refresh, or otherwise undefined MUST NOT resolve toward permission. It resolves toward the more restrictive outcome available at that decision point — a clamp to a more supervised level where a ladder exists, the veto where the decision is binary — and the undefined state is recorded on the decision record.

| $R$ Value | Interpretation | Effect on $E_{trust}$ |
|-----------|----------------|----------------------|
| 0.0 | Perfect conditions | No reduction |
| 0.1 | Light stress | 10% reduction |
| 0.5 | Moderate stress | 50% reduction |
| 0.9 | Severe stress | 90% reduction |
| 1.0 | Total crisis | All actions blocked |

??? info "Risk Domains (Anti-Oscillation)"
    To prevent rapid fluctuation from sensor noise, $R$ is calculated at three hierarchical levels:
    
    | Domain | Scope | Update Frequency | Default Weight |
    |--------|-------|------------------|----------------|
    | **Node** | Single endpoint | 1-5 seconds | 30% |
    | **Neighborhood** | Cluster/subnet | 10-30 seconds | 40% |
    | **Global** | Zone-wide | 30-120 seconds | 30% |
    
    Final Risk Factor:
    ```
    R = (w_node × R_node) + (w_neighborhood × R_neighborhood) + (w_global × R_global)
    ```

### Effective Trust Score ($E_{trust}$)

The core equation unifying agent history with environmental reality:

$$E_{trust} = E_{base} \times (1 - R)$$

=== "Stable Environment"
    ```
    E_base = 95 (highly trusted agent)
    R = 0.1 (10% stress)
    E_trust = 95 × 0.9 = 85.5
    
    → Agent can perform actions with A ≤ 85
    ```

=== "Degraded Environment"
    ```
    E_base = 95 (same agent)
    R = 0.7 (70% stress)
    E_trust = 95 × 0.3 = 28.5
    
    → Agent can only perform actions with A ≤ 28
    ```

=== "Toxic Environment"
    ```
    E_base = 95 (same agent)
    R = 0.95 (95% stress)
    E_trust = 95 × 0.05 = 4.75
    
    → Agent limited to minimal actions (A ≤ 4)
    ```

!!! note "The Agent Didn't Change"
    In all three scenarios, $E_{base}$ remains 95. The agent's intrinsic capability is constant. **It is the environment that changes what is possible.**

### Trust Velocity ($dE/dt$)

The rate of change provides predictive information:

| Velocity | Meaning | System Response |
|----------|---------|-----------------|
| $dE/dt > 0$ | Improving | Capabilities expanding |
| $dE/dt = 0$ | Stable | Normal operation |
| $dE/dt < 0$ | Degrading | Capabilities contracting |
| $dE/dt \ll 0$ | Rapid decline | Crisis imminent |

??? tip "Velocity Applications"
    - Pre-emptively deny actions that would succeed now but fail mid-execution
    - Warn agents to reduce activity before contraction
    - Trigger early Adaptive Dormancy
    - Detect anomalies (score changing faster than sensors explain)

---

## Risk Factors

Environmental state is aggregated into six weighted inputs and the Soul veto:

=== ":material-weight: Mass (M)"
    
    **Question**: How much inertia does this entity have?
    
    | Metric | Measures |
    |--------|----------|
    | Transaction volume | Accumulated interactions |
    | Proof of Resilience | Stress-tested history |
    | Stake deposited | Skin in the game |
    | Attestation count | Third-party validation |

=== ":material-speedometer: Power (P)"
    
    **Question**: How much force can this entity exert?
    
    | Metric | Measures |
    |--------|----------|
    | Compute allocation | Processing capacity |
    | API rate limits | Throughput capability |
    | Network bandwidth | Communication capacity |
    | Storage quota | Data handling capacity |

=== ":material-thermometer: Heat (H)"
    
    **Question**: How much stress is the environment under?
    
    | Metric | Measures |
    |--------|----------|
    | Anomaly rate | Unexpected events |
    | Adversarial signals | Attack indicators |
    | System load | Resource pressure |
    | Error frequency | Failure signals |

=== ":material-clock: Time (T)"
    
    **Question**: What temporal constraints apply?
    
    | Metric | Measures |
    |--------|----------|
    | Session duration | Time in current state |
    | Time-of-day | Operational windows |
    | Request frequency | Action tempo |
    | Token freshness | Credential currency |

=== "Inertia (I)"
    
    **Question**: How resistant to change is this entity?
    
    | Metric | Measures |
    |--------|----------|
    | Behavioral consistency | Pattern stability |
    | Configuration drift | Setting changes |
    | Dependency stability | External reliance |
    | Version currency | Update status |

=== ":material-eye: Observer (O)"
    
    **Question**: Who is watching and what do they see?
    
    | Metric | Measures |
    |--------|----------|
    | Audit coverage | Monitoring completeness |
    | Attestation freshness | Validation currency |
    | Peer visibility | Network observation |
    | Human oversight | Manual review level |

=== ":material-creation: Soul (S)"
    
    **Question**: What ethical/legal constraints apply?
    
    !!! danger "Soul Veto"
        Unlike other dimensions, Soul acts as a **binary veto**. If $S = 1$, the action is denied regardless of Trust Score.
    
    | Metric | Measures |
    |--------|----------|
    | Data sovereignty | Jurisdictional constraints |
    | Consent status | Permission state |
    | Cultural protocols | Community requirements |
    | Ethical boundaries | Value alignment |

---

## Trust Proof Token

The Trust Proof extends JWT with real-time trust state:

??? example "Trust Proof Structure"
    ```json
    {
      "header": {
        "alg": "ES256",
        "typ": "KTP+jwt",
        "kid": "oracle-mesh-2025-q4"
      },
      "payload": {
        "sub": "agent://example.com/trading-bot-7",
        "iss": "oracle://trust-mesh.example.com",
        "iat": 1735689600,
        "exp": 1735689660,
        "ktp": {
          "e_base": 72,
          "r": 0.15,
          "e_trust": 61.2,
          "de_dt": -0.02,
          "tier": "operator",
          "tensor_hash": "sha256:abc123...",
          "soul_clear": true
        }
      },
      "signature": "..."
    }
    ```

### Key Claims

| Claim | Type | Description |
|-------|------|-------------|
| `e_base` | Integer | Base Trust Score (0-100) |
| `r` | Float | Current Risk Factor (0-1) |
| `e_trust` | Float | Effective Trust Score |
| `de_dt` | Float | Trust Velocity |
| `tier` | String | Trust Tier (admin/operator/analyst/observer) |
| `tensor_hash` | String | Hash of the Risk Factor input set used |
| `soul_clear` | Boolean | No Soul veto constraints |

---

## Silent Veto Mechanism

When $A > E_{trust}$, the Silent Veto triggers automatically:

``` mermaid
flowchart LR
    R["DELETE /api/database/users<br/>A = 85 | E_trust = 61.2"] --> Eval{"A > E_trust?"}
    Eval -->|"85 > 61.2 ✓"| Veto["🛑 SILENT VETO"]
    Veto --> R1["Action impossible"]
    Veto --> R2["No error message"]
    Veto --> R3["Agent continues"]
    Veto --> R4["Decision logged"]
```

!!! abstract "It's Not Denial—It's Impossibility"
    The agent doesn't receive an "access denied" error. The action simply becomes impossible, like trying to walk through a wall. The agent continues operating within its actual capability envelope.

### Action Risk Classification

| Risk Level | $A$ Range | Example Actions |
|------------|-----------|-----------------|
| **Minimal** | 0-20 | Read public data, health checks |
| **Low** | 21-40 | Read authenticated data, list resources |
| **Moderate** | 41-60 | Create records, modify own resources |
| **High** | 61-80 | Modify shared resources, bulk operations |
| **Critical** | 81-100 | Delete data, admin operations, key rotation |

---

## Trust Oracle

The Trust Oracle is a distributed authority responsible for Trust Score calculation:

### Architecture

``` mermaid
flowchart TB
    subgraph Mesh["Trust Oracle Mesh"]
        O1["Oracle 1"]
        O2["Oracle 2"]
        O3["Oracle 3"]
        O4["Oracle 4"]
        O5["Oracle 5"]
        
        O1 <--> O2
        O2 <--> O3
        O3 <--> O4
        O4 <--> O5
        O5 <--> O1
        O1 <--> O3
        O2 <--> O4
    end
    
    Mesh --> TS["Threshold Signatures (3-of-5)"]
    TS --> TP["✅ Valid Trust Proof"]
```

### Responsibilities

1. **Calculate** Trust Scores from Context Signals data
2. **Sign** Trust Proofs with threshold signatures
3. **Attest** to agent transactions for Proof of Resilience
4. **Detect** anomalies and potential gaming attempts
5. **Federate** with Trust Oracles in other zones

??? warning "Anti-Goodhart Measures"
    Trust Score faces an existential threat: **Goodhart's Law**—*"When a measure becomes a target, it ceases to be a good measure."*
    
    KTP implements multiple countermeasures:
    
    | Measure | Purpose |
    |---------|---------|
    | **Multi-dimensional scoring** | Gaming one dimension is easier than all |
    | **Behavioral unpredictability** | Random weight variations ±10% |
    | **Adversity requirements** | Trust requires survival under stress |
    | **Peer validation** | Cross-agent attestation |
    | **Temporal consistency** | Smooth trajectories, not jumps |
    | **Cross-zone correlation** | Behavior must be consistent across zones |
    | **Human-in-the-loop sampling** | Random manual audits |

---

## Protocol Flow

``` mermaid
sequenceDiagram
    autonumber
    participant Agent
    participant PEP as Policy Enforcement Point
    participant Oracle as Trust Oracle Mesh
    participant Flight as Flight Recorder
    
    Agent->>PEP: Request (action + context)
    PEP->>Oracle: Get/Validate Trust Proof
    Note over Oracle: Calculate E_base, R, E_trust
    Oracle-->>PEP: Trust Proof Token
    Note over PEP: Evaluate A ≤ E_trust
    PEP->>Flight: Log Decision
    PEP-->>Agent: Response (allow/veto)
```

---

??? info "Related Specifications"
    - **[KTP-Identity](ktp-identity.md)** — Vector Identity, Proof of Resilience, and agent lineage.
    - **[KTP-Crypto](ktp-crypto.md)** — Cryptographic primitives and signature schemes.
    - **[KTP-Transport](ktp-transport.md)** — Network transport and Trust Proof propagation.
    - **[KTP-Signals](ktp-signals.md)** — Complete Context Signals specification (1,627 signals).
    - **[KTP-Conformance](ktp-conformance.md)** — Compliance levels and certification criteria.

---

## Official RFC Document

??? note "View Complete RFC Text (ktp-core.txt)"
    ```text
    --8<-- "rfcs-txt/ktp-core.txt"
    ```
