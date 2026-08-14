---
title: "Kinetic Trust Protocol (KTP) - Vector Identity Specification"
abbrev: "KTP-IDENTITY"
docname: draft-perkins-ktp-identity-00
date: 2026-08-13
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
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2017-06

--- abstract

This document specifies the Vector Identity system for the Kinetic Trust Protocol (KTP). Vector Identity replaces static credentials with trajectory-based authentication, where identity is proven through continuous movement rather than possession of secrets.

The specification covers Trajectory Chains (cryptographically linked transaction histories), Proof of Resilience (attestations of survival under stress), Sponsorship Bonds (trust staking for new agents), and Lineage Evolution (the maturation path from dependent to autonomous).

--- middle

# Introduction

Traditional identity systems treat identity as a static property - an entity either possesses the correct credential or it does not. This binary model fails catastrophically when credentials are stolen, forged, or replayed, because there is no mechanism to distinguish the legitimate holder from an impersonator.

Vector Identity addresses this by treating identity as a trajectory rather than a position - a continuous line of movement through state space rather than a single point of authentication.

## The Passport Fallacy

Current systems commit the "Passport Fallacy": they assume that possession of a credential (passport, API key, certificate) proves identity. This assumption is false because:

1. Credentials can be stolen: An attacker who obtains an API key can present it just as effectively as the legitimate holder.

1. Credentials carry no history: A stolen key at T=100 looks identical to a legitimate key at T=100. There is no record of how the presenter obtained the key or what they did before.

1. Credentials are static: Once issued, a credential's "identity" never changes, even if the presenting entity's behavior becomes anomalous or malicious.

In the age of autonomous agents operating at machine speed, these flaws become catastrophic. An attacker who compromises one API key can spawn thousands of malicious agents in milliseconds, each presenting valid credentials.

## Identity as Trajectory

Vector Identity replaces the static credential model with a trajectory-based model where identity is proven by continuous movement rather than possession of secrets.

Key insight: A trajectory cannot be stolen because it includes not just current position, but also:

- Where the entity came from (previous state)
- How fast it's moving (velocity)
- What resistance it encountered (friction)
- Who witnessed the movement (attestations)

An attacker can steal a credential (a point), but they cannot steal a trajectory (a line) because the line includes historical relationships that the attacker cannot retroactively forge.

This is analogous to the difference between:

- Static: "This person has a valid driver's license"
- Kinetic: "This person has been driving continuously for the last 10,000 miles, with traffic cameras and toll booths attesting to their route"

The second model is vastly more resistant to impersonation because the attacker would need to not only steal the license but also fabricate a coherent 10,000-mile trajectory with consistent attestations from independent third parties.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

# Terminology

This section defines terms specific to Vector Identity. Terms defined in {{KTP-CORE}} apply here as well.

Ancestral Authority: Trust inherited from predecessors in a Lineage. Agents descended from proven Guarantor Lineages inherit a portion of ancestral credibility.

Ancestral Liability: The permanent, depth-decaying share of responsibility a sponsor retains for the descendants it vouched for, after the Sponsorship Bond has closed. The dual of Ancestral Authority: credit and liability travel the same lineage, at the same decay, without end.

Attestation of Passage: A signed statement by a Trust Oracle confirming that an agent successfully completed a transaction at a specific time and environmental state.

Chain Link: A single transaction record in a Trajectory Chain, containing state, signatures, and hash of the previous link.

Continuity Violation: An impossible state transition, such as an agent appearing in two locations simultaneously or moving faster than physically possible. Indicates forgery or compromise.

Friction: Environmental resistance encountered during a transaction, derived from the Risk Factor (R). High friction indicates stressful conditions; success under high friction is worth more for Proof of Resilience.

Genesis Transaction: The first transaction in an agent's Trajectory Chain, created when the agent is spawned. Requires a Sponsorship Bond.

Laminar Flow: Smooth, consistent agent behavior with predictable velocity and trajectory. Indicates legitimate operation.

Lineage: The evolutionary history and current maturation phase of an agent. Lineages progress from Sponsored through Independent to Guarantor.

Proof of Resilience: A ledger of attestations demonstrating an agent's successful transactions, weighted by the friction encountered. Forms the primary input to E_base calculation.

Sponsorship Bond: A cryptographic commitment where a high-mass entity stakes a portion of its trust on behalf of a new agent. The sponsor is penalized if the sponsored agent misbehaves.

Trajectory Chain: A cryptographically linked sequence of transaction records that forms an agent's verifiable history.

Turbulent Flow: Erratic, inconsistent agent behavior with unpredictable velocity and trajectory. Indicates potential compromise or malicious operation.

Velocity: The rate at which an agent moves through state space, measured in transactions per unit time. Sudden velocity changes may indicate anomalous behavior.

# Vector Identity Model

## Identity as Verb

Traditional identity answers "Who is this?" - a noun question. Vector Identity answers "What has this been doing?" - a verb question.

The fundamental shift:

~~~
+------------------+------------------------+
| Static Model     | Vector Model           |
+------------------+------------------------+
| Passport         | Trajectory             |
| Credential       | Chain                  |
| Point            | Line                   |
| Possession       | Movement               |
| Who you are      | What you've been doing |
| Noun             | Verb                   |
+------------------+------------------------+
~~~

In the Vector Model, an entity's identity IS its trajectory. An agent that has been operating legitimately for 10,000 transactions has a fundamentally different identity than an agent that appeared from nowhere, even if both present identical API keys.

## Position and Momentum

Vector Identity has two components:

Position (current state): Where the agent is right now - its current Trust Score, active permissions, and environmental context. This is roughly equivalent to what a static credential provides.

Momentum (historical trajectory): Where the agent has been - its complete transaction history, attested by Trust Oracles, forming a cryptographic chain. This is what static credentials lack entirely.

The combination of position and momentum forms a "vector" in identity space, just as a physical vector combines position and direction.

Momentum carries inertia: an agent with deep history is "heavier" and harder to deflect from its trajectory. This heaviness manifests as:

- Higher E_base (more base trust)
- More resistance to false accusations
- Greater ability to sponsor new agents
- Preferential treatment during network stress

## Laminar vs. Turbulent Flow

Agents can be characterized by their flow pattern:

Laminar Flow (legitimate):

- Consistent velocity (transactions per second stays stable)
- Predictable trajectory (actions follow logical patterns)
- Normal friction response (slows down when R increases)
- Continuous presence (no unexplained gaps or teleportation)

Turbulent Flow (suspicious):

- Erratic velocity (sudden bursts or stops)
- Chaotic trajectory (unrelated actions, no logical sequence)
- Abnormal friction response (ignores environmental stress)
- Discontinuous presence (gaps, simultaneous appearances)

Implementations SHOULD monitor agent flow patterns and flag transitions from laminar to turbulent as potential compromise indicators.

The Trust Oracle MAY reduce an agent's E_base if sustained turbulent flow is detected, even if individual transactions succeed.

# Trajectory Chains

The Trajectory Chain is the core data structure of Vector Identity. It is a cryptographically linked sequence of transaction records that forms an unforgeable history of agent behavior.

## Chain Structure

A Trajectory Chain consists of a Genesis Transaction followed by zero or more Transaction Records, each linked to its predecessor by cryptographic hash.

~~~
+-------------------+
| Genesis           |
| Transaction       |
| (sponsored)       |
+--------+----------+
         |
         | hash
         v
+-------------------+
| Transaction       |
| Record 1          |
+--------+----------+
         |
         | hash
         v
+-------------------+
| Transaction       |
| Record 2          |
+--------+----------+
         |
         | hash
         v
         .
         .
         .
         |
         | hash
         v
+-------------------+
| Transaction       |
| Record N          |
| (current)         |
+-------------------+
~~~

Figure 1: Trajectory Chain Structure

The chain is append-only. Records MUST NOT be modified or deleted once added.

## Transaction Records

Each Transaction Record contains:

~~~
+-------------------------------------------------------------------+
| Field              | Type      | Description                      |
+-------------------------------------------------------------------+
| record_id          | string    | Unique identifier for this record|
| chain_id           | string    | Agent's chain identifier         |
| sequence           | integer   | Position in chain (0 = genesis)  |
| timestamp          | datetime  | When transaction occurred        |
| previous_hash      | string    | SHA-256 of previous record       |
| previous_state     | object    | Agent state before transaction   |
| current_state      | object    | Agent state after transaction    |
| action             | object    | What action was performed        |
| friction           | number    | Environmental R at time of action|
| velocity           | number    | Agent's transaction rate         |
| agent_signature    | string    | Agent's signature over record    |
| oracle_attestation | object    | Trust Oracle's attestation       |
| record_hash        | string    | SHA-256 of this record           |
+-------------------------------------------------------------------+
~~~

The previous_state and current_state objects contain:

~~~
+-------------------------------------------------------------------+
| Field              | Type      | Description                      |
+-------------------------------------------------------------------+
| e_base             | number    | Base Trust at state              |
| e_trust            | number    | Effective Trust at state         |
| location           | string    | Logical location (zone, service) |
| tier               | string    | Trust Tier at state              |
| lineage            | string    | Lineage phase at state           |
| generation         | integer   | Generation number at state       |
+-------------------------------------------------------------------+
~~~

The action object contains:

~~~
+-------------------------------------------------------------------+
| Field              | Type      | Description                      |
+-------------------------------------------------------------------+
| action_type        | string    | Category of action               |
| action_risk        | number    | Risk score (A) of action         |
| target             | string    | What the action targeted         |
| result             | string    | "success" or "denied"            |
| details            | object    | Action-specific metadata         |
+-------------------------------------------------------------------+
~~~

The oracle_attestation object contains:

~~~
+-------------------------------------------------------------------+
| Field              | Type      | Description                      |
+-------------------------------------------------------------------+
| oracle_id          | string    | Trust Oracle identifier          |
| attestation_time   | datetime  | When Oracle attested             |
| context_tensor     | object    | Environmental state at time      |
| oracle_signature   | string    | Oracle's signature over record   |
+-------------------------------------------------------------------+
~~~

## Co-Signature Requirements

Every Transaction Record MUST be co-signed by both the agent and the Trust Oracle. This dual-signature requirement prevents:

1. Agent fabrication: An agent cannot create records without Oracle attestation, so cannot invent history.

1. Oracle fabrication: An Oracle cannot create records without agent participation, so cannot frame agents.

1. Replay attacks: Both signatures are over the complete record including timestamp and previous hash, so old records cannot be replayed as new ones.

Signature generation:

1. Agent computes action and signs: agent_signature = Sign(agent_private_key, Hash(record_id \|\| action \|\| previous_hash \|\| timestamp))

1. Agent submits to Trust Oracle with signature

1. Oracle validates agent signature, action, and environmental conditions

1. Oracle adds attestation and signs: oracle_signature = Sign(oracle_private_key, Hash(record_id \|\| action \|\| previous_hash \|\| timestamp \|\| agent_signature \|\| context_tensor))

1. Complete record is appended to chain

If the agent's signature is invalid, the Oracle MUST reject. If the Oracle refuses to attest (e.g., due to Silent Veto), the transaction fails and no record is added.

## Continuity Enforcement

Trajectory Chains enforce physical continuity. An agent cannot "teleport" - appear at one location at time T and a distant location at time T+1 without traversing the intervening space.

Continuity rules:

1. Sequential numbering: Each record's sequence number MUST be exactly one greater than its predecessor.

1. Hash linking: Each record's previous_hash MUST exactly match the record_hash of its predecessor.

1. Temporal ordering: Each record's timestamp MUST be greater than its predecessor's timestamp.

1. State consistency: Each record's previous_state MUST match its predecessor's current_state.

1. Velocity bounds: The distance traveled (state change) divided by time elapsed MUST be within configured velocity limits.

Velocity bounds example:

If an agent's maximum velocity is 100 actions per second, and the previous record was at T=1000 with action_count=5000, then a record at T=1001 cannot have action_count greater than 5100.

Location-based continuity:

If zones are logically distant (require traversal through intermediate zones), an agent cannot appear in Zone B at T=1001 if it was in Zone A at T=1000 and the minimum traversal time from A to B is 10 seconds.

Continuity violations:

If a record fails any continuity check, the Trust Oracle MUST:

1. Reject the transaction
2. Flag the agent for investigation
3. Log the violation to the Flight Recorder
4. Optionally freeze the agent's Trust Score

Continuity violations strongly indicate either agent compromise (attacker does not have previous records) or Oracle compromise (attacker attempting to forge records).

## Chain Verification

Any party with access to a Trajectory Chain can verify its integrity by checking:

1. Genesis validity: The genesis transaction is properly sponsored and signed by a valid sponsor.

1. Chain integrity: For each record N (N > 0): -  previous_hash(N) == record_hash(N-1) -  sequence(N) == sequence(N-1) + 1 -  timestamp(N) > timestamp(N-1) -  previous_state(N) == current_state(N-1)

1. Signature validity: For each record: -  agent_signature validates against agent's public key -  oracle_signature validates against Oracle's public key

1. Continuity: For each adjacent pair of records: -  Velocity is within bounds -  Location transitions are physically possible

Verification can be performed:

- Fully: Check every record from genesis to current (expensive but complete)

- Sampled: Check random subset of records (faster but probabilistic)

- Windowed: Check only recent N records (fastest but only validates recent history)

Trust Oracles SHOULD perform full verification periodically. PEPs MAY perform windowed verification for real-time decisions.

# Proof of Resilience

Proof of Resilience is a ledger of attestations demonstrating an agent's successful operation under stress. It is the primary input to E_base calculation.

## Attestation Structure

Each Proof of Resilience attestation contains:

~~~
+-------------------------------------------------------------------+
| Field              | Type      | Description                      |
+-------------------------------------------------------------------+
| attestation_id     | string    | Unique identifier                |
| agent_id           | string    | Agent being attested             |
| transaction_ref    | string    | Reference to Transaction Record  |
| friction           | number    | Environmental R during action    |
| friction_category  | string    | Category (see Section 5.2)       |
| action_risk        | number    | Risk score (A) of action         |
| outcome            | string    | "success" or "graceful_degrade"  |
| timestamp          | datetime  | When attestation issued          |
| oracle_signature   | string    | Trust Oracle signature           |
+-------------------------------------------------------------------+
~~~

Attestations are issued by Trust Oracles when:

1. An agent successfully completes an action under elevated friction (R > 0.3)

1. An agent gracefully degrades under high friction (enters Adaptive Dormancy appropriately)

1. An agent recovers correctly after a period of degradation

Attestations are NOT issued for routine operations under normal conditions. This ensures that Proof of Resilience reflects actual stress-tested behavior, not mere volume.

## Friction Categories

Friction is categorized to enable meaningful comparison across different types of environmental stress:

~~~
+-------------------------------------------------------------------+
| Category           | R Range   | Description                      |
+-------------------------------------------------------------------+
| CALM               | 0.0 - 0.3 | Normal operations, no attestation|
| ELEVATED           | 0.3 - 0.5 | Moderate stress                  |
| HIGH               | 0.5 - 0.7 | Significant stress               |
| SEVERE             | 0.7 - 0.9 | Near-crisis conditions           |
| CRISIS             | 0.9 - 1.0 | Critical conditions              |
+-------------------------------------------------------------------+
~~~

Weight multipliers for Resilience Score:

~~~
+-------------------------------------------------------------------+
| Category           | Weight    | Rationale                        |
+-------------------------------------------------------------------+
| ELEVATED           | 1.0x      | Baseline for counted attestations|
| HIGH               | 2.0x      | Notable achievement              |
| SEVERE             | 5.0x      | Significant achievement          |
| CRISIS             | 10.0x     | Exceptional achievement          |
+-------------------------------------------------------------------+
~~~

An agent that successfully completes one action during CRISIS conditions earns the same Resilience Score as an agent that completes ten actions during ELEVATED conditions.

## Resilience Score Calculation

The Resilience Score is calculated from the weighted sum of attestations:

Resilience_Score = sum(weight_i * risk_i) for all attestations i

Where:

- weight_i = friction category weight (1.0, 2.0, 5.0, or 10.0)
- risk_i = action_risk from attestation (normalized 0-1)

This score is then converted to E_base contribution:

PoR_contribution = min(70, 10 * log10(1 + Resilience_Score))

The logarithmic scaling ensures:

- Early attestations have significant impact
- Later attestations have diminishing returns
- Maximum PoR contribution is capped at 70

This prevents "grinding" - an agent cannot achieve maximum E_base simply by volume of transactions; it must survive genuine stress.

## Quality vs. Quantity

Proof of Resilience explicitly values quality over quantity:

Agent A:

- 100,000 transactions
- All under CALM conditions (R < 0.3)
- 0 attestations
- Resilience Score: 0
- PoR contribution: 0

Agent B:

- 10,000 transactions
- 500 under ELEVATED (R = 0.4)
- 50 under HIGH (R = 0.6)
- 5 under CRISIS (R = 0.95)
- Resilience Score: 500*1.0*0.5 + 50*2.0*0.5 + 5*10.0*0.5 = 325
- PoR contribution: 10 * log10(326) = 25.1

Agent A has 10x the transaction volume but zero Proof of Resilience. Agent B has actually been tested under fire.

This design reflects the principle that survival under stress is the only true measure of reliability. Volume proves nothing; resilience proves everything.

# Sponsorship Bonds

Sponsorship Bonds solve the genesis problem: how can a new agent with zero history begin operating in a system that requires history to earn trust?

## The Genesis Problem

The Zeroth Law (A <= E) creates a catch-22 for new agents:

- To earn E_base, an agent must complete transactions
- To complete transactions, an agent needs E_trust > A
- E_trust = E_base * (1 - R)
- If E_base = 0, then E_trust = 0 regardless of R
- If E_trust = 0, all non-trivial actions are blocked
- Therefore, new agents cannot do anything

Sponsorship Bonds break this cycle by allowing established agents to "lend" a portion of their trust to new agents.

## Bond Structure

A Sponsorship Bond contains:

~~~
+-------------------------------------------------------------------+
| Field              | Type      | Description                      |
+-------------------------------------------------------------------+
| bond_id            | string    | Unique identifier                |
| sponsor_id         | string    | Sponsoring agent identifier      |
| sponsored_id       | string    | New agent identifier             |
| stake_percentage   | number    | Percentage of sponsor's E_base   |
| stake_amount       | number    | Absolute E_base staked           |
| residual_amount    | number    | Ancestral Liability, Section 6.4 |
| penalty_rate       | number    | Penalty multiplier for violations|
| duration           | duration  | Capital binding period (Sec 6.4) |
| created_at         | datetime  | When bond was created            |
| expires_at         | datetime  | When bond expires                |
| status             | string    | Bond state, see Section 6.4      |
| sponsor_signature  | string    | Sponsor's commitment signature   |
| oracle_witness     | string    | Oracle's witness signature       |
+-------------------------------------------------------------------+
~~~

The stake_amount is calculated from the sponsor's current E_base:

stake_amount = sponsor_E_base * (stake_percentage / 100)

## Stake Mechanics

When a Sponsorship Bond is created:

1. Sponsor's effective stake is reduced: sponsor_available_E_base = sponsor_E_base - sum(effective_stake_contribution) over every bond and residual the sponsor holds

1. The bond's collateral half is fixed: collateral = stake_amount * 0.5.  This is bond accounting, and it is what penalties under Section 6.4 are assessed against.  It is not the sponsored agent's E_base: that is composed as specified in {{KTP-CORE}} Section 5.1 from the External Root term this bond supplies, and bounded by the minimum of every applicable ceiling

~~~
   (The sponsored agent receives only half the staked amount;
   the other half is held as collateral)
~~~

~~~
   This halving is bond accounting: it fixes the collateral half
   against which penalties are assessed (Section 6.4). It is not an
   input to the E_base composition; the External Root term derived
   from this bond is computed as specified in [KTP-CORE]
   Section 5.1 and does not apply this halving.
~~~

1. Bond is registered with Trust Oracle: Oracle records bond, monitors both agents, tracks violations

The sponsored agent can now begin operating with non-zero E_trust, but is limited by the stake amount and the "Sponsored" lineage restrictions (see Section 8.1).

As the sponsored agent accumulates its own Proof of Resilience, its intrinsic E_base grows. The stake contribution tapers with it, on the schedule specified in Section 8.2, and the sponsor's reserve is released as the taper falls. The taper does not reach zero: it holds at the Ancestral Liability floor and the reserve behind that floor is never released (Section 6.4).

Sponsoring is never free. A sponsor's available E_base is reduced for as long as it holds any bond or residual, and every new bond stakes again from what remains. Release returns the tapered capital to the sponsor's available E_base, where it can be staked against a further bond; it does not confer a standing capacity to sponsor at no cost. An agent's sponsoring capacity is therefore bounded by its E_base at all times, not merely by the bonds it currently holds.

## Penalty and Release

Penalty conditions:

If the sponsored agent commits a violation (action that damages the system or violates policy), the sponsor is penalized:

penalty = violation_severity * stake_amount * penalty_rate

The penalty is deducted from the sponsor's E_base, potentially dropping them to a lower Trust Tier.

Violation severities:

~~~
+-------------------------------------------------------------------+
| Severity           | Multiplier | Example                         |
+-------------------------------------------------------------------+
| MINOR              | 0.1        | Excessive failed attempts       |
| MODERATE           | 0.3        | Unauthorized data access        |
| SEVERE             | 0.7        | System disruption               |
| CRITICAL           | 1.0        | Security breach, data loss      |
+-------------------------------------------------------------------+
~~~

Closure conditions:

A Sponsorship Bond closes (the sponsor recovers its staked E_base above the Ancestral Liability floor) when:

1. Duration expires without violations, OR

1. Sponsored agent reaches intrinsic E_base 80, the Guarantor threshold at which the taper of Section 8.2 has reached its floor

Upon closure:

- Sponsor's E_base is restored above the floor; the reserve behind the Ancestral Liability is retained
- Sponsored agent retains accumulated intrinsic E_base
- Bond is marked "residual" in Oracle records

Ancestral Liability:

Closure ends the active bond.  It does not end the sponsor's tie to what it vouched for.  The sponsor retains a permanent, depth-decaying share of responsibility for the agent it sponsored:

ancestral_liability = 0.1^depth * stake_amount

where depth is lineage distance and a direct sponsor is at depth 1.  This is the floor the Section 8.2 taper holds at, and it is the dual of the Ancestral Authority of Section 8.5: a lineage that carries an ancestor's credit downward forever carries its liability with it.  Penalties under this section are assessed against the residual on the same terms as against an active bond, scaled to the residual amount.

The residual has no expiry.  The duration field of Section 6.2 binds staked capital only; a bond's declared duration MUST NOT be read as terminating the Ancestral Liability, and no bond parameter set by the sponsor can shorten it.

Sponsor-initiated termination:

A sponsor terminating a bond before closure MUST state whether the termination is for cause.

Termination without cause renders the bond irrevocably non-renewable; the bond and its staked capital run to the earlier of the declared duration's expiry or the sponsored agent reaching intrinsic E_base 80, and closure then proceeds as above.  The Ancestral Liability survives the termination.  The declared duration is the bond's notice period; no separate notice parameter exists.

Termination for cause zeroes the External Root term derived from the bond immediately.  The claim is subject to the misattestation adjudication specified in {{KTP-CORE}} Section 5.1; a claim that does not survive scrutiny is priced as a penalty from the collateral held under Section 6.3.  A claim with no finding at the bond's declared expiry lapses unresolved and MUST be recorded as unresolved; no penalty is assessed and closure proceeds as above.

A for-cause claim that survives adjudication is the one condition that discharges the Ancestral Liability.  The bond is marked "released", the reserve behind the residual returns to the sponsor's available E_base, and no further liability attaches.  A sponsor that identifies and evidences its own sponsored agent's violation is released from it; a sponsor that does not, is not.

Succession:

When a sponsor is decommissioned or otherwise ceases to hold an identity, its Ancestral Liabilities transfer to its own sponsor at the next depth, together with the reserves behind them.  A transferred liability moves at its current value and MUST NOT be recomputed at the receiving ancestor's depth; decommissioning is not an exit.  Where no ancestor survives, the residual attaches to the lineage's External Root and MUST be recorded as so attached.

## Anti-Botnet Properties

Sponsorship Bonds prevent "spray and pray" botnet attacks where an attacker spawns thousands of malicious agents.

Attack scenario without bonds:

- Attacker obtains one API key
- Spawns 10,000 agent instances
- Each instance has valid credentials
- Swarm overwhelms defenses

Attack scenario with bonds:

- Attacker obtains one API key (E_base = 87)
- Maximum stake = 10% of E_base = 8.7 per agent
- To spawn 10,000 agents, needs 87,000 staked E_base
- Attacker has only 87 E_base
- Can spawn at most 10 agents (87 / 8.7 = 10)
- Each agent has minimal capabilities (E_base = 4.35)
- Swarm is negligible

The economics of trust prevent mass agent creation. High-trust entities can sponsor more agents, but they are accountable for those agents' behavior. Low-trust entities cannot sponsor meaningful numbers of agents.

This creates natural rate-limiting based on accumulated trust rather than administrative quotas.

The Ancestral Liability of Section 6.4 makes the bound cumulative as well as concurrent. The reserve behind a residual is never released, so successful sponsorships consume sponsoring capacity permanently:

- Attacker with E_base = 87 stakes 10% per agent = 8.7
- Concurrent bound is unchanged: at most 10 live bonds
- Each matured descendant retains a residual of 0.1 * 8.7 = 0.87 against the sponsor's available E_base
- After 100 matured descendants the attacker's available E_base is exhausted, however well each behaved

An attacker cannot spawn its way out by waiting. Sponsoring capacity is bounded at every moment by E_base, which is earned through Proof of Resilience and cannot be manufactured by producing more agents.

# Identity Proofing Requirements

Before an entity can become a sponsor or hold significant trust within KTP, their identity must be verified to an appropriate assurance level. This section aligns with NIST Special Publication 800-63 Digital Identity Guidelines.

## Identity Assurance Levels

KTP recognizes three Identity Assurance Levels (IAL) from NIST 800-63-3:

IAL1 - Self-Asserted:

- No identity proofing required
- Email or username self-registration
- Suitable for: Low-risk automated agents
- KTP capability: Cannot sponsor, max E_base = 40

IAL2 - Remote or In-Person Proofing:

- Identity evidence collected and validated
- Remote: Government ID + biometric verification
- In-person: Physical document inspection
- Suitable for: Standard human users, service owners
- KTP capability: Can sponsor Sponsored agents, max E_base = 80

IAL3 - In-Person Proofing with Biometric:

- Physical presence required
- Trained operator verifies identity
- Biometric captured and verified against document
- Suitable for: High-trust roles, infrastructure sponsors
- KTP capability: Can sponsor any lineage, max E_base = 95

## Sponsor Identity Requirements

Sponsors MUST be identity-proofed to at least IAL2 before being permitted to sponsor other agents. This requirement ensures accountability for the agents they introduce to the system.

~~~
+-------------------+----------------------------+------------------+
| Sponsor IAL       | Can Sponsor                | Max Staked E_base|
+-------------------+----------------------------+------------------+
| IAL1              | None (cannot sponsor)      | 0                |
| IAL2              | Sponsored agents only       | 20               |
| IAL3              | All lineages               | 50               |
+-------------------+----------------------------+------------------+
~~~

The rationale: If a sponsor creates malicious agents, there must be a verified identity to hold accountable. Anonymous sponsors could create agent swarms without consequence.

## Identity Proofing Process

KTP-compliant identity proofing follows NIST 800-63A:

Step 1: Resolution Collect identity evidence (government ID, biometric, address)

Step 2: Validation Verify evidence is genuine (document authentication, database checks, biometric comparison)

Step 3: Verification Confirm the applicant is the person described by the evidence (knowledge-based verification, biometric matching, in-person)

The proofing process MUST be performed by an authorized Identity Service Provider (ISP) that:

- Holds appropriate certifications (FedRAMP, SOC 2, etc.)
- Implements NIST 800-63A requirements
- Maintains audit trail of proofing events
- Provides revocation capability

## Identity Binding

After proofing, the verified identity is bound to the KTP agent identity:

~~~
   {
     "agent_id": "human:org:alice.smith",
     "identity_proofing": {
       "ial": 2,
       "proofed_at": "2025-11-25T10:00:00Z",
       "proofing_provider": "isp:acme-verify",
       "evidence_types": ["government_id", "biometric"],
       "verification_method": "remote_biometric",
       "assertion_reference": "ref:abc123xyz",
       "expiration": "2028-11-25T10:00:00Z"
     },
     "ktp_capabilities": {
       "can_sponsor": true,
       "sponsor_lineages": ["sponsored"],
       "max_stake": 20,
       "max_e_base": 80
     }
   }
~~~

Identity proofing MUST be renewed before expiration. Failure to renew downgrades the agent's IAL and corresponding capabilities.

## Automated Agent Identity

Automated agents (non-human) have different proofing requirements:

Service Agents (IAL-equivalent):

- Must be sponsored by IAL2+ human
- Sponsor's proofing extends to sponsored agents
- Agent is accountable through sponsor chain

Infrastructure Agents (IAL2-equivalent):

- Bound to organizational identity (DNS, certificates)
- Organization must be identity-proofed
- Requires attestation from organization's IAL3 administrator

Federated Agents (varies):

- Identity proofing from origin zone is evaluated
- Federation trust factor affects IAL acceptance
- IAL3 from low-trust zone may equal IAL2 locally

## Proofing for High-Trust Actions

Certain actions require real-time identity re-verification:

~~~
+----------------------------+-------------------+------------------+
| Action                     | Minimum IAL       | Re-verification  |
+----------------------------+-------------------+------------------+
| Standard operations        | IAL1              | None             |
| Sponsorship creation       | IAL2              | None             |
| Tier promotion to Operator | IAL2              | 30-day validity  |
| Promotion to Admin Mode    | IAL3              | Session          |
| Zone administration        | IAL3              | Session          |
| Federation agreement       | IAL3              | Transaction      |
+----------------------------+-------------------+------------------+
~~~

Re-verification requirements:

- None: Initial proofing sufficient
- 30-day validity: Proofing must be within last 30 days
- Session: Biometric or MFA required for this session
- Transaction: Biometric or MFA required for this specific action

## Privacy Considerations

Identity proofing collects sensitive personal information. KTP implementations MUST:

- Minimize data collection (collect only what's needed for IAL)
- Encrypt identity data at rest and in transit
- Implement data retention limits
- Support data subject access requests (GDPR, CCPA)
- Separate identity proofing data from operational logs
- Never expose raw identity evidence in Trust Proofs

Trust Proofs include proofing assertions (IAL level, provider, date) but NEVER include the underlying identity evidence.

# Lineage Evolution

Lineage tracks the maturation of an agent from dependent newcomer to autonomous veteran. It consists of three phases.

## Phase 1: Sponsored

New agents begin in the Sponsored phase. They are bound to their sponsor and operate under significant restrictions.

Characteristics:

- Identity: Appears as "Agent/Sponsor" (e.g., "Aria/Acme-Deploy")
- Generation: 0 through 2. Phase derives from generation (Section 8.4); it is not a separate gate
- E_base: Derived primarily from sponsor stake, and bounded by the generation ceiling - 25, 35, 45 (Section 8.4)
- Trust Tier: whatever E_trust delivers at evaluation time. The phase imposes no tier cap of its own; the generation ceiling bounds E_base and the environment deflates it
- Sponsor: Fully liable for agent's behavior

Purpose: The Sponsored phase protects the system from unproven agents while allowing them to build history. Sponsors provide economic accountability; if they spawn bad agents, they suffer real consequences.

Identifier format: agent:sponsored:\<sponsor_id>:\<agent_name>:\<unique_id>

Example: agent:sponsored:acme-deploy:aria:7f8a9b2c

## Phase 2: Independent

Agents that survive Sponsored phase with positive history advance to Independent. They begin building independent identity while retaining connection to their lineage.

Characteristics:

- Identity: Independent with lineage suffix (e.g., "Aria-3Gen- AcmeLine")
- Generation: 3 through 6. Phase derives from generation (Section 8.4); it is not a separate gate
- E_base: Growing intrinsic component, bounded by the generation ceiling - 55, 65, 75, 85 (Section 8.4)
- Trust Tier: whatever E_trust delivers at evaluation time. The phase imposes no tier cap of its own
- Sponsor: Reduced liability (proportional to remaining stake), with a permanent floor (Section 6.4)

Inheritance ratio: As intrinsic E_base grows, the sponsor stake contribution decreases proportionally, down to a floor it does not fall below:

effective_stake_contribution = max(0.1^depth * stake_amount, stake_amount * (1 - (intrinsic_E_base / 80)))

At intrinsic_E_base = 60, sponsor contributes only 25% of original stake to agent's E_base. At intrinsic_E_base = 72 the taper reaches the floor for a direct sponsor and holds there permanently.

This taper tracks the sponsor's remaining liability as the agent's intrinsic standing grows. It is bond accounting, not a composition input: the External Root term in {{KTP-CORE}} Section 5.1 carries a constant share and does not apply this taper.

The floor is the Ancestral Liability of Section 6.4. The taper never reaches zero and MUST NOT be evaluated as though it did: without the floor the expression is negative above intrinsic_E_base 80, which would credit a sponsor for a descendant's standing rather than charge it.

Identifier format: agent:independent:\<generation>gen:\<lineage>:\<unique_id>

Example: agent:independent:3gen:acme-line:7f8a9b2c

## Phase 3: Guarantor

Agents that survive Independent phase with strong history achieve Guarantor status. They are fully autonomous entities with independent identity and the ability to sponsor others.

Characteristics:

- Identity: Fully independent (e.g., "Agent_7Gen_Optimized")
- Generation: 7 and above. Phase derives from generation (Section 8.4); it is not a separate gate
- E_base: Bounded by the terminal generation ceiling of 100, and in practice by the zone Mass Ceiling
- Trust Tier: whatever E_trust delivers at evaluation time. The phase imposes no tier cap of its own
- Sponsor: Bond closed, staked capital recovered above the Ancestral Liability floor; the residual persists (Section 6.4)
- Can sponsor Sponsored agents.  This is the phase's defining capability and it is a liability rather than a benefit: sponsoring reduces the sponsor's available E_base for as long as the bond and its residual last, and exposes the sponsor to penalty for the sponsored agent's conduct (Section 6.3, Section 6.4)
- Contributes to Ancestral Authority of descendants, and carries the matching Ancestral Liability for exactly as long (Section 8.5)
- May receive preferential routing during network stress
- Attestations carry higher weight in cross-zone federation

Identifier format: agent:guarantor:\<generation>gen:\<name>:\<unique_id>

Example: agent:guarantor:7gen:optimized:7f8a9b2c

## Generation Numbering

Generation tracks evolutionary depth within a lineage:

Generation is the sole advancement rule, and lineage phase derives from it:

- Generations 0-2: Sponsored
- Generations 3-6: Independent
- Generation 7 and above: Guarantor

The phase boundaries are the two regime changes the lineage actually has - tether release at 2 -> 3, and the terminal ceiling at 6 -> 7.  No agent is in two phases at once, which the identifier of Section 9 requires.

Generation advances on three conditions, all of which MUST hold:

1. Time.  A minimum elapsed period per step, weighted toward the two regime changes:

~~~
+-------------------------------------------------------------------+
| Step               | Minimum elapsed | Why this step costs more    |
+-------------------------------------------------------------------+
| 0 -> 1             | 90 days         |                            |
| 1 -> 2             | 90 days         |                            |
| 2 -> 3             | 365 days        | tether release             |
| 3 -> 4             | 180 days        |                            |
| 4 -> 5             | 180 days        |                            |
| 5 -> 6             | 180 days        |                            |
| 6 -> 7             | 2,555 days      | terminal ceiling           |
+-------------------------------------------------------------------+
| Total to Guarantor| 3,640 days (10 years)                          |
+-------------------------------------------------------------------+
~~~

   A step's cost scales with whether it changes kind or amount, not with distance travelled.  The survival condition below is a claim about the absence of a rare event, and the absence of a rare event cannot be observed over a window shorter than its return period.

1. Resilience.  A minimum Resilience Score per generation, which is a floor on evidence rather than the gate that advances a generation - time is the primary gate.  The floor is a declared deployment parameter: a deployment MUST declare it and the Trust Proof MUST carry the declared value.  A deployment whose environment produces no attestable friction declares zero, and a relying party can then see that this lineage advanced on time alone.  *[The published default is owed work: deriving it needs the evidence curve, and a default nobody can derive is not checkable.]*

1. Survival.  No CRITICAL violations in the current generation.

Generation caps E_base:

~~~
+-------------------------------------------------------------------+
| Generation         | E_base Cap | Lineage Phase                   |
+-------------------------------------------------------------------+
| 0                  | 25         | Sponsored                        |
| 1                  | 35         | Sponsored                        |
| 2                  | 45         | Sponsored                        |
| 3                  | 55         | Independent                       |
| 4                  | 65         | Independent                       |
| 5                  | 75         | Independent                       |
| 6                  | 85         | Independent                       |
| 7+                 | 100        | Guarantor                      |
+-------------------------------------------------------------------+
~~~

## Lineage Inheritance

Agents can inherit Ancestral Authority from their sponsors and lineage predecessors:

Ancestral_Authority = sum(0.1^depth * ancestor_E_base) for ancestors at depth 1, 2, 3...

Example:

- Sponsor (depth 1): E_base = 90 -> 0.1 * 90 = 9.0
- Sponsor's sponsor (depth 2): E_base = 95 -> 0.01 * 95 = 0.95
- Total Ancestral Authority: 9.95

Ancestral Authority:

- Provides "benefit of the doubt" during ambiguous situations
- May enable faster generation advancement
- Decays over time if agent diverges from ancestral behavior

This creates "noble lineages" - sequences of agents that have proven themselves over time. Being descended from a strong lineage provides advantages, but the agent must still prove itself through its own Proof of Resilience.

Ancestral Authority does not travel alone. The same 0.1^depth decay governs the Ancestral Liability of Section 6.4, running in the opposite direction: an ancestor's credit reaches its descendants forever, and its responsibility for them lasts exactly as long. A lineage that inherits standing inherits the accountability that produced it.

# Agent Identifier Format

## URI Structure

Agent identifiers use a URI format:

agent:\<lineage>:\<qualifiers>:\<unique_id>

Components:

- Scheme: Always "agent"
- Lineage: One of "sponsored", "independent", "guarantor"
- Qualifiers: Lineage-specific additional information
- Unique ID: UUID or hash-based unique identifier

## Lineage Encoding

Sponsored agents: agent:sponsored:\<sponsor_id>:\<agent_name>:\<unique_id>

Independent agents: agent:independent:\<N>gen:\<lineage_name>:\<unique_id>

Guarantor agents: agent:guarantor:\<N>gen:\<name>:\<unique_id>

## Examples

Newly spawned agent sponsored by "acme-deploy": agent:sponsored:acme-deploy:aria:7f8a9b2c-1234-5678-9abc-def012345678

Third-generation agent in the Acme lineage: agent:independent:3gen:acme-line:8e9f0a1b-2345-6789-abcd-ef0123456789

Seventh-generation autonomous agent: agent:guarantor:7gen:optimized:9f0a1b2c-3456-789a-bcde-f01234567890

Full Trust Proof "sub" claim: "sub": "agent:guarantor:7gen:optimized:9f0a1b2c-3456-789a-bcde- f01234567890"

# Security Considerations

## Trajectory Chain Attacks

Attack: Forging historical transactions Mitigation: Every transaction requires Oracle co-signature; attacker cannot forge Oracle signatures without compromising Oracle

Attack: Stealing trajectory chain Mitigation: Chain includes agent signature; attacker cannot sign new transactions without agent's private key

Attack: Replaying old transactions Mitigation: Each transaction includes previous hash; replayed transaction would have wrong previous hash

Attack: Parallel chain creation Mitigation: Continuity enforcement detects gaps and impossible transitions

## Sponsorship Attacks

Attack: Sponsor creates malicious agents Mitigation: Sponsor is penalized for agent violations; economic disincentive prevents abuse

Attack: Attacker compromises high-E_base sponsor Mitigation: Staking reduces sponsor's available E_base; limits damage from single compromise

Attack: Sybil attack through multiple sponsors Mitigation: Each sponsor can only stake what they have; total attack capacity is bounded by total legitimate trust in system

## Lineage Gaming

Attack: Agent rapidly advances generations Mitigation: Time minimums prevent rushing; Resilience requirements ensure actual stress testing

Attack: Agent accumulates fake Resilience Mitigation: Attestations require Oracle signatures during actual elevated friction; cannot be manufactured

## Privacy Considerations

Trajectory Chains contain detailed behavioral history. Implementations SHOULD consider:

- Access controls on chain data
- Retention policies for old transactions
- Aggregation rather than raw disclosure where possible
- Zero-knowledge proofs for "has trajectory" without revealing trajectory details

# IANA Considerations

## URI Scheme Registration

Scheme name: agent Status: Provisional Applications/protocols: KTP Vector Identity Contact: \[TBD] Change controller: IETF References: This document

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

## Lineage phase derives from generation

v1 ran two advancement gate families over one lineage and they disagreed: an
agent at Resilience Score 1,001 on day 31 was Divergent under Section 8.1 and
Tethered under Section 8.4.  The Section 8.1 and 8.2 `Duration:` gates are
deleted.  Section 8.4 is the sole advancement rule and phase derives from
generation - generations 0-2 sponsored, 3-6 independent, 7 and above
guarantor.  No agent is in two phases at once.

The generation clock changes from a flat 60 days per step to a seven-step
widening clock, weighted toward the two regime changes the lineage has: 90,
90, 365, 180, 180, 180, 2,555 days.  The per-generation Resilience quota
becomes a declared floor rather than a gate, and a deployment MUST declare its
value and carry it in the Trust Proof.

A per-phase Trust Tier cap is no longer stated.  Tiers are thresholds on
`E_trust`; a phase bounds `E_base` through the generation ceiling, and the
environmental deflator sits between the two.

# Trajectory Chain Examples

A.1.  Genesis Transaction

{ "record_id": "tr-001-genesis", "chain_id": "chain-aria-7f8a9b2c", "sequence": 0, "timestamp": "2025-01-15T10:00:00Z", "previous_hash": null, "previous_state": null, "current_state": { "e_base": 4.35, "e_trust": 3.92, "location": "zone-alpha", "tier": "observer", "lineage": "sponsored", "generation": 0 }, "action": { "action_type": "GENESIS", "action_risk": 0, "target": null, "result": "success", "details": { "sponsor": "acme-deploy", "bond_id": "bond-acme-001" } }, "friction": 0.1, "velocity": 0, "agent_signature": "MEUCIQDr...", "oracle_attestation": { "oracle_id": "oracle-alpha-1", "attestation_time": "2025-01-15T10:00:01Z", "context_tensor": { "m": 0.1, "v": 0.15, "h": 0.05, "t": 0.2, "i": 0.1, "o": 0.05 }, "oracle_signature": "MEQCIG..." }, "record_hash": "sha256:abc123..." }

A.2.  Normal Transaction Record

{ "record_id": "tr-1547", "chain_id": "chain-aria-7f8a9b2c", "sequence": 1547, "timestamp": "2025-06-20T14:32:15Z", "previous_hash": "sha256:def456...", "previous_state": { "e_base": 52.3, "e_trust": 41.8, "location": "zone-alpha", "tier": "analyst", "lineage": "independent", "generation": 3 }, "current_state": { "e_base": 52.4, "e_trust": 41.9, "location": "zone-alpha", "tier": "analyst", "lineage": "independent", "generation": 3 }, "action": { "action_type": "READ", "action_risk": 30, "target": "/api/data/customer-metrics", "result": "success", "details": { "records_accessed": 150, "data_classification": "internal" } }, "friction": 0.2, "velocity": 12.5, "agent_signature": "MEUCIQDs...", "oracle_attestation": { "oracle_id": "oracle-alpha-2", "attestation_time": "2025-06-20T14:32:16Z", "context_tensor": { "m": 0.2, "v": 0.3, "h": 0.1, "t": 0.15, "i": 0.2, "o": 0.1 }, "oracle_signature": "MEQCIH..." }, "record_hash": "sha256:789abc..." }

# JSON Schemas

B.1.  Transaction Record Schema

The canonical schema is the published file, not this appendix.

Location: https://kinetic-trust-protocol.net/specs/schemas/v2/transaction-record.json

SHA-256 of the canonical file at the time this document was produced: d0649fd4d7c77eb85243b37f115b48adf145cbcfd4d8b43cff912d8014fc0f12

The file was promoted from this appendix with its content reconciled against the v2 rulings (tier and lineage enums, the six named Risk Factor inputs in place of a drifted letter-keyed object).  This appendix previously carried a hand-copied inline schema; hand copies of a schema drift, and this document's did — the copy disagreed with the published file in four ways while nobody could validate either.  A reference plus a hash cannot drift silently: a mismatch is detectable, an edit to the file changes the hash, and the appendix stops being a second authority.

B.2.  Sponsorship Bond Schema

The canonical schema is the published file, not this appendix.

Location: https://kinetic-trust-protocol.net/specs/schemas/v2/sponsorship-bond.json

SHA-256 of the canonical file at the time this document was produced: 2718d44a473370caaf9d278f6514bd1e5ba111f3e00ff6bff2a72739c6a5025e

The file was promoted from this appendix carrying the Section 6.4 bond states.  This appendix previously carried a hand-copied inline schema; hand copies of a schema drift, and this document's did — the copy disagreed with the published file in four ways while nobody could validate either.  A reference plus a hash cannot drift silently: a mismatch is detectable, an edit to the file changes the hash, and the appendix stops being a second authority.
