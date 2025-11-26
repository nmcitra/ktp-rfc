
Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


        Kinetic Trust Protocol (KTP) - Vector Identity Specification

Abstract

   This document specifies the Vector Identity system for the Kinetic
   Trust Protocol (KTP). Vector Identity replaces static credentials
   with trajectory-based authentication, where identity is proven
   through continuous movement rather than possession of secrets.

   The specification covers Trajectory Chains (cryptographically linked
   transaction histories), Proof of Resilience (attestations of survival
   under stress), Sponsorship Bonds (trust staking for new agents), and
   Lineage Evolution (the maturation path from dependent to autonomous).

Status of This Memo

   This document is a draft specification developed by the New Mexico
   Cyber Intelligence & Threat Response Alliance (NMCITRA). It has not
   been submitted to the IETF and does not represent an Internet
   Standard or consensus of any standards body.

   Feedback and contributions are welcome at:
   https://github.com/nmcitra/ktp-rfc

Copyright Notice

   Copyright (c) 2025 Chris Perkins / NMCITRA.
   This work is licensed under the Apache License, Version 2.0.

Table of Contents

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . . .  3
       1.1.  The Passport Fallacy  . . . . . . . . . . . . . . . . .  3
       1.2.  Identity as Trajectory  . . . . . . . . . . . . . . . .  4
       1.3.  Requirements Language . . . . . . . . . . . . . . . . .  5
   2.  Terminology . . . . . . . . . . . . . . . . . . . . . . . . .  5
   3.  Vector Identity Model . . . . . . . . . . . . . . . . . . . .  7
       3.1.  Identity as Verb  . . . . . . . . . . . . . . . . . . .  7
       3.2.  Position and Momentum . . . . . . . . . . . . . . . . .  8
       3.3.  Laminar vs. Turbulent Flow  . . . . . . . . . . . . . .  9
   4.  Trajectory Chains . . . . . . . . . . . . . . . . . . . . . . 10
       4.1.  Chain Structure . . . . . . . . . . . . . . . . . . . . 10
       4.2.  Transaction Records . . . . . . . . . . . . . . . . . . 11
       4.3.  Co-Signature Requirements . . . . . . . . . . . . . . . 13
       4.4.  Continuity Enforcement  . . . . . . . . . . . . . . . . 14
       4.5.  Chain Verification  . . . . . . . . . . . . . . . . . . 16
   5.  Proof of Resilience . . . . . . . . . . . . . . . . . . . . . 17
       5.1.  Attestation Structure . . . . . . . . . . . . . . . . . 17
       5.2.  Friction Categories . . . . . . . . . . . . . . . . . . 19
       5.3.  Resilience Score Calculation  . . . . . . . . . . . . . 20
       5.4.  Quality vs. Quantity  . . . . . . . . . . . . . . . . . 21
   6.  Sponsorship Bonds . . . . . . . . . . . . . . . . . . . . . . 22
       6.1.  The Genesis Problem . . . . . . . . . . . . . . . . . . 22
       6.2.  Bond Structure  . . . . . . . . . . . . . . . . . . . . 23
       6.3.  Stake Mechanics . . . . . . . . . . . . . . . . . . . . 25
       6.4.  Penalty and Release . . . . . . . . . . . . . . . . . . 26
       6.5.  Anti-Botnet Properties  . . . . . . . . . . . . . . . . 27
   7.  Identity Proofing Requirements  . . . . . . . . . . . . . . . 28
       7.1.  Identity Assurance Levels . . . . . . . . . . . . . . . 28
       7.2.  Sponsor Identity Requirements . . . . . . . . . . . . . 29
       7.3.  Identity Proofing Process . . . . . . . . . . . . . . . 30
       7.4.  Identity Binding  . . . . . . . . . . . . . . . . . . . 31
       7.5.  Automated Agent Identity  . . . . . . . . . . . . . . . 32
       7.6.  Proofing for High-Trust Actions . . . . . . . . . . . . 33
       7.7.  Privacy Considerations  . . . . . . . . . . . . . . . . 34
   8.  Lineage Evolution . . . . . . . . . . . . . . . . . . . . . . 35
       8.1.  Phase 1: Tethered (Apprentice)  . . . . . . . . . . . . 35
       8.2.  Phase 2: Divergent (Journeyman) . . . . . . . . . . . . 36
       8.3.  Phase 3: Persistent (Master)  . . . . . . . . . . . . . 37
       8.4.  Generation Numbering  . . . . . . . . . . . . . . . . . 38
       8.5.  Lineage Inheritance . . . . . . . . . . . . . . . . . . 39
   9.  Agent Identifier Format . . . . . . . . . . . . . . . . . . . 40
       9.1.  URI Structure . . . . . . . . . . . . . . . . . . . . . 40
       9.2.  Lineage Encoding  . . . . . . . . . . . . . . . . . . . 41
       9.3.  Examples  . . . . . . . . . . . . . . . . . . . . . . . 42
   10. Security Considerations . . . . . . . . . . . . . . . . . . . 43
   11. IANA Considerations . . . . . . . . . . . . . . . . . . . . . 45
   12. References  . . . . . . . . . . . . . . . . . . . . . . . . . 46
   Appendix A.  Trajectory Chain Examples  . . . . . . . . . . . . . 47
   Appendix B.  JSON Schemas . . . . . . . . . . . . . . . . . . . . 50
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 54


1.  Introduction

   Traditional identity systems treat identity as a static property -
   an entity either possesses the correct credential or it does not.
   This binary model fails catastrophically when credentials are stolen,
   forged, or replayed, because there is no mechanism to distinguish
   the legitimate holder from an impersonator.

   Vector Identity addresses this by treating identity as a trajectory
   rather than a position - a continuous line of movement through
   state space rather than a single point of authentication.

1.1.  The Passport Fallacy

   Current systems commit the "Passport Fallacy": they assume that
   possession of a credential (passport, API key, certificate) proves
   identity. This assumption is false because:

   1. Credentials can be stolen: An attacker who obtains an API key
      can present it just as effectively as the legitimate holder.

   2. Credentials carry no history: A stolen key at T=100 looks
      identical to a legitimate key at T=100. There is no record of
      how the presenter obtained the key or what they did before.

   3. Credentials are static: Once issued, a credential's "identity"
      never changes, even if the presenting entity's behavior becomes
      anomalous or malicious.

   In the age of autonomous agents operating at machine speed, these
   flaws become catastrophic. An attacker who compromises one API key
   can spawn thousands of malicious agents in milliseconds, each
   presenting valid credentials.

1.2.  Identity as Trajectory

   Vector Identity replaces the static credential model with a
   trajectory-based model where identity is proven by continuous
   movement rather than possession of secrets.

   Key insight: A trajectory cannot be stolen because it includes
   not just current position, but also:

   - Where the entity came from (previous state)
   - How fast it's moving (velocity)
   - What resistance it encountered (friction)
   - Who witnessed the movement (attestations)

   An attacker can steal a credential (a point), but they cannot
   steal a trajectory (a line) because the line includes historical
   relationships that the attacker cannot retroactively forge.

   This is analogous to the difference between:

   - Static: "This person has a valid driver's license"
   - Kinetic: "This person has been driving continuously for the
     last 10,000 miles, with traffic cameras and toll booths
     attesting to their route"

   The second model is vastly more resistant to impersonation because
   the attacker would need to not only steal the license but also
   fabricate a coherent 10,000-mile trajectory with consistent
   attestations from independent third parties.

1.3.  Requirements Language

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all
   capitals, as shown here.


2.  Terminology

   This section defines terms specific to Vector Identity. Terms
   defined in [KTP-CORE] apply here as well.

   Ancestral Authority:
      Trust inherited from predecessors in a Lineage. Agents descended
      from proven Persistent Lineages inherit a portion of ancestral
      credibility.

   Attestation of Passage:
      A signed statement by a Trust Oracle confirming that an agent
      successfully completed a transaction at a specific time and
      environmental state.

   Chain Link:
      A single transaction record in a Trajectory Chain, containing
      state, signatures, and hash of the previous link.

   Continuity Violation:
      An impossible state transition, such as an agent appearing in
      two locations simultaneously or moving faster than physically
      possible. Indicates forgery or compromise.

   Friction:
      Environmental resistance encountered during a transaction,
      derived from the Risk Factor (R). High friction indicates
      stressful conditions; success under high friction is worth
      more for Proof of Resilience.

   Genesis Transaction:
      The first transaction in an agent's Trajectory Chain, created
      when the agent is spawned. Requires a Sponsorship Bond.

   Laminar Flow:
      Smooth, consistent agent behavior with predictable velocity
      and trajectory. Indicates legitimate operation.

   Lineage:
      The evolutionary history and current maturation phase of an
      agent. Lineages progress from Tethered through Divergent to
      Persistent.

   Proof of Resilience:
      A ledger of attestations demonstrating an agent's successful
      transactions, weighted by the friction encountered. Forms the
      primary input to E_base calculation.

   Sponsorship Bond:
      A cryptographic commitment where a high-mass entity stakes a
      portion of its trust on behalf of a new agent. The sponsor
      is penalized if the sponsored agent misbehaves.

   Trajectory Chain:
      A cryptographically linked sequence of transaction records
      that forms an agent's verifiable history.

   Turbulent Flow:
      Erratic, inconsistent agent behavior with unpredictable
      velocity and trajectory. Indicates potential compromise
      or malicious operation.

   Velocity:
      The rate at which an agent moves through state space,
      measured in transactions per unit time. Sudden velocity
      changes may indicate anomalous behavior.


3.  Vector Identity Model

3.1.  Identity as Verb

   Traditional identity answers "Who is this?" - a noun question.
   Vector Identity answers "What has this been doing?" - a verb
   question.

   The fundamental shift:

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

   In the Vector Model, an entity's identity IS its trajectory. An
   agent that has been operating legitimately for 10,000 transactions
   has a fundamentally different identity than an agent that appeared
   from nowhere, even if both present identical API keys.


3.2.  Position and Momentum

   Vector Identity has two components:

   Position (current state):
      Where the agent is right now - its current Trust Score, active
      permissions, and environmental context. This is roughly
      equivalent to what a static credential provides.

   Momentum (historical trajectory):
      Where the agent has been - its complete transaction history,
      attested by Trust Oracles, forming a cryptographic chain. This
      is what static credentials lack entirely.

   The combination of position and momentum forms a "vector" in
   identity space, just as a physical vector combines position and
   direction.

   Momentum carries inertia: an agent with deep history is "heavier"
   and harder to deflect from its trajectory. This heaviness
   manifests as:

   - Higher E_base (more base trust)
   - More resistance to false accusations
   - Greater ability to sponsor new agents
   - Preferential treatment during network stress


3.3.  Laminar vs. Turbulent Flow

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

   Implementations SHOULD monitor agent flow patterns and flag
   transitions from laminar to turbulent as potential compromise
   indicators.

   The Trust Oracle MAY reduce an agent's E_base if sustained
   turbulent flow is detected, even if individual transactions
   succeed.


4.  Trajectory Chains

   The Trajectory Chain is the core data structure of Vector Identity.
   It is a cryptographically linked sequence of transaction records
   that forms an unforgeable history of agent behavior.

4.1.  Chain Structure

   A Trajectory Chain consists of a Genesis Transaction followed by
   zero or more Transaction Records, each linked to its predecessor
   by cryptographic hash.

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
          . . .
            |
            | hash
            v
   +-------------------+
   | Transaction       |
   | Record N          |
   | (current)         |
   +-------------------+

   Figure 1: Trajectory Chain Structure

   The chain is append-only. Records MUST NOT be modified or deleted
   once added.


4.2.  Transaction Records

   Each Transaction Record contains:

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

   The previous_state and current_state objects contain:

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

   The action object contains:

   +-------------------------------------------------------------------+
   | Field              | Type      | Description                      |
   +-------------------------------------------------------------------+
   | action_type        | string    | Category of action               |
   | action_risk        | number    | Risk score (A) of action         |
   | target             | string    | What the action targeted         |
   | result             | string    | "success" or "denied"            |
   | details            | object    | Action-specific metadata         |
   +-------------------------------------------------------------------+

   The oracle_attestation object contains:

   +-------------------------------------------------------------------+
   | Field              | Type      | Description                      |
   +-------------------------------------------------------------------+
   | oracle_id          | string    | Trust Oracle identifier          |
   | attestation_time   | datetime  | When Oracle attested             |
   | context_tensor     | object    | Environmental state at time      |
   | oracle_signature   | string    | Oracle's signature over record   |
   +-------------------------------------------------------------------+


4.3.  Co-Signature Requirements

   Every Transaction Record MUST be co-signed by both the agent and
   the Trust Oracle. This dual-signature requirement prevents:

   1. Agent fabrication: An agent cannot create records without
      Oracle attestation, so cannot invent history.

   2. Oracle fabrication: An Oracle cannot create records without
      agent participation, so cannot frame agents.

   3. Replay attacks: Both signatures are over the complete record
      including timestamp and previous hash, so old records cannot
      be replayed as new ones.

   Signature generation:

   1. Agent computes action and signs:
      agent_signature = Sign(agent_private_key,
        Hash(record_id || action || previous_hash || timestamp))

   2. Agent submits to Trust Oracle with signature

   3. Oracle validates agent signature, action, and environmental
      conditions

   4. Oracle adds attestation and signs:
      oracle_signature = Sign(oracle_private_key,
        Hash(record_id || action || previous_hash || timestamp ||
             agent_signature || context_tensor))

   5. Complete record is appended to chain

   If the agent's signature is invalid, the Oracle MUST reject.
   If the Oracle refuses to attest (e.g., due to Silent Veto), the
   transaction fails and no record is added.


4.4.  Continuity Enforcement

   Trajectory Chains enforce physical continuity. An agent cannot
   "teleport" - appear at one location at time T and a distant
   location at time T+1 without traversing the intervening space.

   Continuity rules:

   1. Sequential numbering: Each record's sequence number MUST be
      exactly one greater than its predecessor.

   2. Hash linking: Each record's previous_hash MUST exactly match
      the record_hash of its predecessor.

   3. Temporal ordering: Each record's timestamp MUST be greater
      than its predecessor's timestamp.

   4. State consistency: Each record's previous_state MUST match
      its predecessor's current_state.

   5. Velocity bounds: The distance traveled (state change) divided
      by time elapsed MUST be within configured velocity limits.

   Velocity bounds example:

   If an agent's maximum velocity is 100 actions per second, and
   the previous record was at T=1000 with action_count=5000, then
   a record at T=1001 cannot have action_count greater than 5100.

   Location-based continuity:

   If zones are logically distant (require traversal through
   intermediate zones), an agent cannot appear in Zone B at T=1001
   if it was in Zone A at T=1000 and the minimum traversal time
   from A to B is 10 seconds.

   Continuity violations:

   If a record fails any continuity check, the Trust Oracle MUST:

   1. Reject the transaction
   2. Flag the agent for investigation
   3. Log the violation to the Flight Recorder
   4. Optionally freeze the agent's Trust Score

   Continuity violations strongly indicate either agent compromise
   (attacker does not have previous records) or Oracle compromise
   (attacker attempting to forge records).


4.5.  Chain Verification

   Any party with access to a Trajectory Chain can verify its
   integrity by checking:

   1. Genesis validity: The genesis transaction is properly sponsored
      and signed by a valid sponsor.

   2. Chain integrity: For each record N (N > 0):
      - previous_hash(N) == record_hash(N-1)
      - sequence(N) == sequence(N-1) + 1
      - timestamp(N) > timestamp(N-1)
      - previous_state(N) == current_state(N-1)

   3. Signature validity: For each record:
      - agent_signature validates against agent's public key
      - oracle_signature validates against Oracle's public key

   4. Continuity: For each adjacent pair of records:
      - Velocity is within bounds
      - Location transitions are physically possible

   Verification can be performed:

   - Fully: Check every record from genesis to current (expensive
     but complete)

   - Sampled: Check random subset of records (faster but
     probabilistic)

   - Windowed: Check only recent N records (fastest but only
     validates recent history)

   Trust Oracles SHOULD perform full verification periodically.
   PEPs MAY perform windowed verification for real-time decisions.


5.  Proof of Resilience

   Proof of Resilience is a ledger of attestations demonstrating an
   agent's successful operation under stress. It is the primary
   input to E_base calculation.

5.1.  Attestation Structure

   Each Proof of Resilience attestation contains:

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

   Attestations are issued by Trust Oracles when:

   1. An agent successfully completes an action under elevated
      friction (R > 0.3)

   2. An agent gracefully degrades under high friction (enters
      Adaptive Dormancy appropriately)

   3. An agent recovers correctly after a period of degradation

   Attestations are NOT issued for routine operations under normal
   conditions. This ensures that Proof of Resilience reflects actual
   stress-tested behavior, not mere volume.


5.2.  Friction Categories

   Friction is categorized to enable meaningful comparison across
   different types of environmental stress:

   +-------------------------------------------------------------------+
   | Category           | R Range   | Description                      |
   +-------------------------------------------------------------------+
   | CALM               | 0.0 - 0.3 | Normal operations, no attestation|
   | ELEVATED           | 0.3 - 0.5 | Moderate stress                  |
   | HIGH               | 0.5 - 0.7 | Significant stress               |
   | SEVERE             | 0.7 - 0.9 | Near-crisis conditions           |
   | CRISIS             | 0.9 - 1.0 | Critical conditions              |
   +-------------------------------------------------------------------+

   Weight multipliers for Resilience Score:

   +-------------------------------------------------------------------+
   | Category           | Weight    | Rationale                        |
   +-------------------------------------------------------------------+
   | ELEVATED           | 1.0x      | Baseline for counted attestations|
   | HIGH               | 2.0x      | Notable achievement              |
   | SEVERE             | 5.0x      | Significant achievement          |
   | CRISIS             | 10.0x     | Exceptional achievement          |
   +-------------------------------------------------------------------+

   An agent that successfully completes one action during CRISIS
   conditions earns the same Resilience Score as an agent that
   completes ten actions during ELEVATED conditions.


5.3.  Resilience Score Calculation

   The Resilience Score is calculated from the weighted sum of
   attestations:

   Resilience_Score = sum(weight_i * risk_i) for all attestations i

   Where:
      weight_i = friction category weight (1.0, 2.0, 5.0, or 10.0)
      risk_i = action_risk from attestation (normalized 0-1)

   This score is then converted to E_base contribution:

   PoR_contribution = min(70, 10 * log10(1 + Resilience_Score))

   The logarithmic scaling ensures:
   - Early attestations have significant impact
   - Later attestations have diminishing returns
   - Maximum PoR contribution is capped at 70

   This prevents "grinding" - an agent cannot achieve maximum E_base
   simply by volume of transactions; it must survive genuine stress.


5.4.  Quality vs. Quantity

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

   Agent A has 10x the transaction volume but zero Proof of
   Resilience. Agent B has actually been tested under fire.

   This design reflects the principle that survival under stress
   is the only true measure of reliability. Volume proves nothing;
   resilience proves everything.


6.  Sponsorship Bonds

   Sponsorship Bonds solve the genesis problem: how can a new agent
   with zero history begin operating in a system that requires
   history to earn trust?

6.1.  The Genesis Problem

   The Zeroth Law (A <= E) creates a catch-22 for new agents:

   - To earn E_base, an agent must complete transactions
   - To complete transactions, an agent needs E_trust > A
   - E_trust = E_base * (1 - R)
   - If E_base = 0, then E_trust = 0 regardless of R
   - If E_trust = 0, all non-trivial actions are blocked
   - Therefore, new agents cannot do anything

   Sponsorship Bonds break this cycle by allowing established agents
   to "lend" a portion of their trust to new agents.

6.2.  Bond Structure

   A Sponsorship Bond contains:

   +-------------------------------------------------------------------+
   | Field              | Type      | Description                      |
   +-------------------------------------------------------------------+
   | bond_id            | string    | Unique identifier                |
   | sponsor_id         | string    | Sponsoring agent identifier      |
   | sponsored_id       | string    | New agent identifier             |
   | stake_percentage   | number    | Percentage of sponsor's E_base   |
   | stake_amount       | number    | Absolute E_base staked           |
   | penalty_rate       | number    | Penalty multiplier for violations|
   | duration           | duration  | How long bond remains active     |
   | created_at         | datetime  | When bond was created            |
   | expires_at         | datetime  | When bond expires                |
   | status             | string    | "active", "released", "penalized"|
   | sponsor_signature  | string    | Sponsor's commitment signature   |
   | oracle_witness     | string    | Oracle's witness signature       |
   +-------------------------------------------------------------------+

   The stake_amount is calculated from the sponsor's current E_base:

   stake_amount = sponsor_E_base * (stake_percentage / 100)


6.3.  Stake Mechanics

   When a Sponsorship Bond is created:

   1. Sponsor's effective stake is reduced:
      sponsor_available_E_base = sponsor_E_base - stake_amount

   2. Sponsored agent receives initial E_base:
      sponsored_E_base = stake_amount * 0.5

      (The sponsored agent receives only half the staked amount;
      the other half is held as collateral)

   3. Bond is registered with Trust Oracle:
      Oracle records bond, monitors both agents, tracks violations

   The sponsored agent can now begin operating with non-zero E_trust,
   but is limited by the stake amount and the "Tethered" lineage
   restrictions (see Section 7.1).

   As the sponsored agent accumulates its own Proof of Resilience,
   its intrinsic E_base grows. The stake contribution gradually
   decreases as a percentage of total E_base.


6.4.  Penalty and Release

   Penalty conditions:

   If the sponsored agent commits a violation (action that damages
   the system or violates policy), the sponsor is penalized:

   penalty = violation_severity * stake_amount * penalty_rate

   The penalty is deducted from the sponsor's E_base, potentially
   dropping them to a lower Trust Tier.

   Violation severities:

   +-------------------------------------------------------------------+
   | Severity           | Multiplier | Example                         |
   +-------------------------------------------------------------------+
   | MINOR              | 0.1        | Excessive failed attempts       |
   | MODERATE           | 0.3        | Unauthorized data access        |
   | SEVERE             | 0.7        | System disruption               |
   | CRITICAL           | 1.0        | Security breach, data loss      |
   +-------------------------------------------------------------------+

   Release conditions:

   A Sponsorship Bond is released (sponsor recovers staked E_base)
   when:

   1. Duration expires without violations, OR

   2. Sponsored agent reaches Divergent lineage (has sufficient
      intrinsic E_base to operate independently)

   Upon release:
   - Sponsor's E_base is restored
   - Sponsored agent retains accumulated intrinsic E_base
   - Bond is marked "released" in Oracle records


6.5.  Anti-Botnet Properties

   Sponsorship Bonds prevent "spray and pray" botnet attacks where
   an attacker spawns thousands of malicious agents.

   Attack scenario without bonds:
      Attacker obtains one API key
      Spawns 10,000 agent instances
      Each instance has valid credentials
      Swarm overwhelms defenses

   Attack scenario with bonds:
      Attacker obtains one API key (E_base = 87)
      Maximum stake = 10% of E_base = 8.7 per agent
      To spawn 10,000 agents, needs 87,000 staked E_base
      Attacker has only 87 E_base
      Can spawn at most 10 agents (87 / 8.7 = 10)
      Each agent has minimal capabilities (E_base = 4.35)
      Swarm is negligible

   The economics of trust prevent mass agent creation. High-trust
   entities can sponsor more agents, but they are accountable for
   those agents' behavior. Low-trust entities cannot sponsor
   meaningful numbers of agents.

   This creates natural rate-limiting based on accumulated trust
   rather than administrative quotas.


7.  Identity Proofing Requirements

   Before an entity can become a sponsor or hold significant trust
   within KTP, their identity must be verified to an appropriate
   assurance level. This section aligns with NIST Special Publication
   800-63 Digital Identity Guidelines.

7.1.  Identity Assurance Levels

   KTP recognizes three Identity Assurance Levels (IAL) from NIST
   800-63-3:

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
      - KTP capability: Can sponsor Tethered agents, max E_base = 80

   IAL3 - In-Person Proofing with Biometric:
      - Physical presence required
      - Trained operator verifies identity
      - Biometric captured and verified against document
      - Suitable for: High-trust roles, infrastructure sponsors
      - KTP capability: Can sponsor any lineage, max E_base = 95

7.2.  Sponsor Identity Requirements

   Sponsors MUST be identity-proofed to at least IAL2 before being
   permitted to sponsor other agents. This requirement ensures
   accountability for the agents they introduce to the system.

   +-------------------+----------------------------+------------------+
   | Sponsor IAL       | Can Sponsor                | Max Staked E_base|
   +-------------------+----------------------------+------------------+
   | IAL1              | None (cannot sponsor)      | 0                |
   | IAL2              | Tethered agents only       | 20               |
   | IAL3              | All lineages               | 50               |
   +-------------------+----------------------------+------------------+

   The rationale: If a sponsor creates malicious agents, there must
   be a verified identity to hold accountable. Anonymous sponsors
   could create agent swarms without consequence.

7.3.  Identity Proofing Process

   KTP-compliant identity proofing follows NIST 800-63A:

   Step 1: Resolution
      Collect identity evidence (government ID, biometric, address)

   Step 2: Validation
      Verify evidence is genuine (document authentication, database
      checks, biometric comparison)

   Step 3: Verification
      Confirm the applicant is the person described by the evidence
      (knowledge-based verification, biometric matching, in-person)

   The proofing process MUST be performed by an authorized Identity
   Service Provider (ISP) that:

   - Holds appropriate certifications (FedRAMP, SOC 2, etc.)
   - Implements NIST 800-63A requirements
   - Maintains audit trail of proofing events
   - Provides revocation capability

7.4.  Identity Binding

   After proofing, the verified identity is bound to the KTP agent
   identity:

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
          "sponsor_lineages": ["tethered"],
          "max_stake": 20,
          "max_e_base": 80
        }
      }

   Identity proofing MUST be renewed before expiration. Failure to
   renew downgrades the agent's IAL and corresponding capabilities.

7.5.  Automated Agent Identity

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

7.6.  Proofing for High-Trust Actions

   Certain actions require real-time identity re-verification:

   +----------------------------+-------------------+------------------+
   | Action                     | Minimum IAL       | Re-verification  |
   +----------------------------+-------------------+------------------+
   | Standard operations        | IAL1              | None             |
   | Sponsorship creation       | IAL2              | None             |
   | Tier promotion to Operator | IAL2              | 30-day validity  |
   | Tier promotion to God Mode | IAL3              | Session          |
   | Zone administration        | IAL3              | Session          |
   | Federation agreement       | IAL3              | Transaction      |
   +----------------------------+-------------------+------------------+

   Re-verification requirements:
   - None: Initial proofing sufficient
   - 30-day validity: Proofing must be within last 30 days
   - Session: Biometric or MFA required for this session
   - Transaction: Biometric or MFA required for this specific action

7.7.  Privacy Considerations

   Identity proofing collects sensitive personal information. KTP
   implementations MUST:

   - Minimize data collection (collect only what's needed for IAL)
   - Encrypt identity data at rest and in transit
   - Implement data retention limits
   - Support data subject access requests (GDPR, CCPA)
   - Separate identity proofing data from operational logs
   - Never expose raw identity evidence in Trust Proofs

   Trust Proofs include proofing assertions (IAL level, provider,
   date) but NEVER include the underlying identity evidence.


8.  Lineage Evolution

   Lineage tracks the maturation of an agent from dependent newcomer
   to autonomous veteran. It consists of three phases.

8.1.  Phase 1: Tethered (Apprentice)

   New agents begin in the Tethered phase. They are bound to their
   sponsor and operate under significant restrictions.

   Characteristics:

   - Identity: Appears as "Agent/Sponsor" (e.g., "Aria/Acme-Deploy")
   - E_base: Derived primarily from sponsor stake (intrinsic < 40)
   - Trust Tier: Capped at Analyst Mode (cannot exceed E_trust = 70)
   - Actions: Limited to lower-risk operations (A <= 50)
   - Sponsor: Fully liable for agent's behavior

   Duration: Until agent accumulates Resilience Score > 1000 AND
   has operated for > 30 days

   Purpose: The Tethered phase protects the system from unproven
   agents while allowing them to build history. Sponsors provide
   economic accountability; if they spawn bad agents, they suffer
   real consequences.

   Identifier format:
      agent:tethered:<sponsor_id>:<agent_name>:<unique_id>

   Example:
      agent:tethered:acme-deploy:aria:7f8a9b2c


8.2.  Phase 2: Divergent (Journeyman)

   Agents that survive Tethered phase with positive history advance
   to Divergent. They begin building independent identity while
   retaining connection to their lineage.

   Characteristics:

   - Identity: Independent with lineage suffix
     (e.g., "Aria-3Gen-AcmeLine")
   - E_base: Growing intrinsic component (40 <= E_base < 80)
   - Trust Tier: Can reach Operator Mode (E_trust up to 85)
   - Actions: Can perform moderate-risk operations (A <= 75)
   - Sponsor: Reduced liability (proportional to remaining stake)

   Duration: Until agent accumulates Resilience Score > 10,000 AND
   has operated for > 180 days AND intrinsic E_base > 60

   Inheritance ratio: As intrinsic E_base grows, the sponsor stake
   contribution decreases proportionally:

   effective_stake_contribution =
      stake_amount * (1 - (intrinsic_E_base / 80))

   At intrinsic_E_base = 60, sponsor contributes only 25% of
   original stake to agent's E_base.

   Identifier format:
      agent:divergent:<generation>gen:<lineage>:<unique_id>

   Example:
      agent:divergent:3gen:acme-line:7f8a9b2c


8.3.  Phase 3: Persistent (Master)

   Agents that survive Divergent phase with strong history achieve
   Persistent status. They are fully autonomous entities with
   independent identity and the ability to sponsor others.

   Characteristics:

   - Identity: Fully independent
     (e.g., "Agent_7Gen_Optimized")
   - E_base: High intrinsic value (E_base >= 80)
   - Trust Tier: Can achieve God Mode (E_trust up to 95+)
   - Actions: Can perform all operations (A <= 95)
   - Sponsor: Bond released, no remaining liability

   Special privileges:

   - Can sponsor Tethered agents (become a sponsor themselves)
   - Contributes to Ancestral Authority of descendants
   - May receive preferential routing during network stress
   - Attestations carry higher weight in cross-zone federation

   Identifier format:
      agent:persistent:<generation>gen:<name>:<unique_id>

   Example:
      agent:persistent:7gen:optimized:7f8a9b2c


8.4.  Generation Numbering

   Generation tracks evolutionary depth within a lineage:

   - Generation 0: Original spawned agent (Tethered)
   - Generation 1-2: Early maturation (late Tethered / early Divergent)
   - Generation 3-5: Mid maturation (Divergent)
   - Generation 6+: Full maturation (Persistent)

   Generation advances based on:

   1. Time: Minimum 60 days per generation
   2. Resilience: Minimum 2,000 Resilience Score per generation
   3. Survival: No CRITICAL violations in current generation

   Generation caps E_base:

   +-------------------------------------------------------------------+
   | Generation         | E_base Cap | Lineage Phase                   |
   +-------------------------------------------------------------------+
   | 0                  | 25         | Tethered                        |
   | 1                  | 35         | Tethered                        |
   | 2                  | 45         | Tethered / Divergent            |
   | 3                  | 55         | Divergent                       |
   | 4                  | 65         | Divergent                       |
   | 5                  | 75         | Divergent                       |
   | 6                  | 85         | Divergent / Persistent          |
   | 7+                 | 100        | Persistent                      |
   +-------------------------------------------------------------------+


8.5.  Lineage Inheritance

   Agents can inherit Ancestral Authority from their sponsors and
   lineage predecessors:

   Ancestral_Authority = sum(0.1^depth * ancestor_E_base)
      for ancestors at depth 1, 2, 3...

   Example:
   - Sponsor (depth 1): E_base = 90 -> 0.1 * 90 = 9.0
   - Sponsor's sponsor (depth 2): E_base = 95 -> 0.01 * 95 = 0.95
   - Total Ancestral Authority: 9.95

   Ancestral Authority:
   - Adds to initial E_base for Tethered agents
   - Provides "benefit of the doubt" during ambiguous situations
   - May enable faster generation advancement
   - Decays over time if agent diverges from ancestral behavior

   This creates "noble lineages" - sequences of agents that have
   proven themselves over time. Being descended from a strong
   lineage provides advantages, but the agent must still prove
   itself through its own Proof of Resilience.


9.  Agent Identifier Format

9.1.  URI Structure

   Agent identifiers use a URI format:

   agent:<lineage>:<qualifiers>:<unique_id>

   Components:

   - Scheme: Always "agent"
   - Lineage: One of "tethered", "divergent", "persistent"
   - Qualifiers: Lineage-specific additional information
   - Unique ID: UUID or hash-based unique identifier


9.2.  Lineage Encoding

   Tethered agents:
      agent:tethered:<sponsor_id>:<agent_name>:<unique_id>

   Divergent agents:
      agent:divergent:<N>gen:<lineage_name>:<unique_id>

   Persistent agents:
      agent:persistent:<N>gen:<name>:<unique_id>


9.3.  Examples

   Newly spawned agent sponsored by "acme-deploy":
      agent:tethered:acme-deploy:aria:7f8a9b2c-1234-5678-9abc-def012345678

   Third-generation agent in the Acme lineage:
      agent:divergent:3gen:acme-line:8e9f0a1b-2345-6789-abcd-ef0123456789

   Seventh-generation autonomous agent:
      agent:persistent:7gen:optimized:9f0a1b2c-3456-789a-bcde-f01234567890

   Full Trust Proof "sub" claim:
      "sub": "agent:persistent:7gen:optimized:9f0a1b2c-3456-789a-bcde-f01234567890"


10.  Security Considerations

10.1.  Trajectory Chain Attacks

   Attack: Forging historical transactions
   Mitigation: Every transaction requires Oracle co-signature; attacker
   cannot forge Oracle signatures without compromising Oracle

   Attack: Stealing trajectory chain
   Mitigation: Chain includes agent signature; attacker cannot sign
   new transactions without agent's private key

   Attack: Replaying old transactions
   Mitigation: Each transaction includes previous hash; replayed
   transaction would have wrong previous hash

   Attack: Parallel chain creation
   Mitigation: Continuity enforcement detects gaps and impossible
   transitions

10.2.  Sponsorship Attacks

   Attack: Sponsor creates malicious agents
   Mitigation: Sponsor is penalized for agent violations; economic
   disincentive prevents abuse

   Attack: Attacker compromises high-E_base sponsor
   Mitigation: Staking reduces sponsor's available E_base; limits
   damage from single compromise

   Attack: Sybil attack through multiple sponsors
   Mitigation: Each sponsor can only stake what they have; total
   attack capacity is bounded by total legitimate trust in system

10.3.  Lineage Gaming

   Attack: Agent rapidly advances generations
   Mitigation: Time minimums prevent rushing; Resilience requirements
   ensure actual stress testing

   Attack: Agent accumulates fake Resilience
   Mitigation: Attestations require Oracle signatures during actual
   elevated friction; cannot be manufactured

10.4.  Privacy Considerations

   Trajectory Chains contain detailed behavioral history. Implementa-
   tions SHOULD consider:

   - Access controls on chain data
   - Retention policies for old transactions
   - Aggregation rather than raw disclosure where possible
   - Zero-knowledge proofs for "has trajectory" without revealing
     trajectory details


11. IANA Considerations

11.1.  URI Scheme Registration

   Scheme name: agent
   Status: Provisional
   Applications/protocols: KTP Vector Identity
   Contact: [TBD]
   Change controller: IETF
   References: This document


12. References

12.1.  Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.

   [RFC8174]  Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC
              2119 Key Words", BCP 14, RFC 8174, May 2017.

   [KTP-CORE] Perkins, C., "Kinetic Trust Protocol - Core
              Specification", Work in Progress.

   [NIST800-63-3]
              Grassi, P., et al., "Digital Identity Guidelines",
              NIST Special Publication 800-63-3, June 2017.
              https://doi.org/10.6028/NIST.SP.800-63-3

   [NIST800-63A]
              Grassi, P., et al., "Digital Identity Guidelines:
              Enrollment and Identity Proofing", NIST Special
              Publication 800-63A, June 2017.
              https://doi.org/10.6028/NIST.SP.800-63a

12.2.  Informative References

   [KTP-AUDIT]
              Perkins, C., "Kinetic Trust Protocol - Flight Recorder",
              Work in Progress.

   [NIST800-171]
              Ross, R., et al., "Protecting Controlled Unclassified
              Information in Nonfederal Systems and Organizations",
              NIST Special Publication 800-171 Rev. 2, February 2020.
              https://doi.org/10.6028/NIST.SP.800-171r2

   [NIST800-63B]
              Grassi, P., et al., "Digital Identity Guidelines:
              Authentication and Lifecycle Management", NIST Special
              Publication 800-63B, June 2017.
              https://doi.org/10.6028/NIST.SP.800-63b

   [NIST800-63C]
              Grassi, P., et al., "Digital Identity Guidelines:
              Federation and Assertions", NIST Special Publication
              800-63C, June 2017.
              https://doi.org/10.6028/NIST.SP.800-63c


Appendix A.  Trajectory Chain Examples

A.1.  Genesis Transaction

   {
     "record_id": "tr-001-genesis",
     "chain_id": "chain-aria-7f8a9b2c",
     "sequence": 0,
     "timestamp": "2025-01-15T10:00:00Z",
     "previous_hash": null,
     "previous_state": null,
     "current_state": {
       "e_base": 4.35,
       "e_trust": 3.92,
       "location": "zone-alpha",
       "tier": "observer",
       "lineage": "tethered",
       "generation": 0
     },
     "action": {
       "action_type": "GENESIS",
       "action_risk": 0,
       "target": null,
       "result": "success",
       "details": {
         "sponsor": "acme-deploy",
         "bond_id": "bond-acme-001"
       }
     },
     "friction": 0.1,
     "velocity": 0,
     "agent_signature": "MEUCIQDr...",
     "oracle_attestation": {
       "oracle_id": "oracle-alpha-1",
       "attestation_time": "2025-01-15T10:00:01Z",
       "context_tensor": {
         "m": 0.1, "v": 0.15, "h": 0.05, "t": 0.2, "i": 0.1, "o": 0.05
       },
       "oracle_signature": "MEQCIG..."
     },
     "record_hash": "sha256:abc123..."
   }


A.2.  Normal Transaction Record

   {
     "record_id": "tr-1547",
     "chain_id": "chain-aria-7f8a9b2c",
     "sequence": 1547,
     "timestamp": "2025-06-20T14:32:15Z",
     "previous_hash": "sha256:def456...",
     "previous_state": {
       "e_base": 52.3,
       "e_trust": 41.8,
       "location": "zone-alpha",
       "tier": "analyst",
       "lineage": "divergent",
       "generation": 3
     },
     "current_state": {
       "e_base": 52.4,
       "e_trust": 41.9,
       "location": "zone-alpha",
       "tier": "analyst",
       "lineage": "divergent",
       "generation": 3
     },
     "action": {
       "action_type": "READ",
       "action_risk": 30,
       "target": "/api/data/customer-metrics",
       "result": "success",
       "details": {
         "records_accessed": 150,
         "data_classification": "internal"
       }
     },
     "friction": 0.2,
     "velocity": 12.5,
     "agent_signature": "MEUCIQDs...",
     "oracle_attestation": {
       "oracle_id": "oracle-alpha-2",
       "attestation_time": "2025-06-20T14:32:16Z",
       "context_tensor": {
         "m": 0.2, "v": 0.3, "h": 0.1, "t": 0.15, "i": 0.2, "o": 0.1
       },
       "oracle_signature": "MEQCIH..."
     },
     "record_hash": "sha256:789abc..."
   }


Appendix B.  JSON Schemas

B.1.  Transaction Record Schema

   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "$id": "https://ktp.example.org/schemas/transaction-record.json",
     "title": "KTP Transaction Record",
     "type": "object",
     "required": [
       "record_id", "chain_id", "sequence", "timestamp",
       "current_state", "action", "friction", "velocity",
       "agent_signature", "oracle_attestation", "record_hash"
     ],
     "properties": {
       "record_id": { "type": "string" },
       "chain_id": { "type": "string" },
       "sequence": { "type": "integer", "minimum": 0 },
       "timestamp": { "type": "string", "format": "date-time" },
       "previous_hash": { "type": ["string", "null"] },
       "previous_state": {
         "oneOf": [
           { "$ref": "#/$defs/agentState" },
           { "type": "null" }
         ]
       },
       "current_state": { "$ref": "#/$defs/agentState" },
       "action": { "$ref": "#/$defs/action" },
       "friction": { "type": "number", "minimum": 0, "maximum": 1 },
       "velocity": { "type": "number", "minimum": 0 },
       "agent_signature": { "type": "string" },
       "oracle_attestation": { "$ref": "#/$defs/oracleAttestation" },
       "record_hash": { "type": "string" }
     },
     "$defs": {
       "agentState": {
         "type": "object",
         "required": ["e_base", "e_trust", "location", "tier",
                      "lineage", "generation"],
         "properties": {
           "e_base": { "type": "number", "minimum": 0, "maximum": 100 },
           "e_trust": { "type": "number", "minimum": 0, "maximum": 100 },
           "location": { "type": "string" },
           "tier": {
             "type": "string",
             "enum": ["observer", "analyst", "operator", "god"]
           },
           "lineage": {
             "type": "string",
             "enum": ["tethered", "divergent", "persistent"]
           },
           "generation": { "type": "integer", "minimum": 0 }
         }
       },
       "action": {
         "type": "object",
         "required": ["action_type", "action_risk", "result"],
         "properties": {
           "action_type": { "type": "string" },
           "action_risk": { "type": "number", "minimum": 0, "maximum": 100 },
           "target": { "type": ["string", "null"] },
           "result": { "type": "string", "enum": ["success", "denied"] },
           "details": { "type": "object" }
         }
       },
       "oracleAttestation": {
         "type": "object",
         "required": ["oracle_id", "attestation_time",
                      "context_tensor", "oracle_signature"],
         "properties": {
           "oracle_id": { "type": "string" },
           "attestation_time": { "type": "string", "format": "date-time" },
           "context_tensor": { "$ref": "#/$defs/contextTensor" },
           "oracle_signature": { "type": "string" }
         }
       },
       "contextTensor": {
         "type": "object",
         "required": ["m", "v", "h", "t", "i", "o"],
         "properties": {
           "m": { "type": "number", "minimum": 0, "maximum": 1 },
           "v": { "type": "number", "minimum": 0, "maximum": 1 },
           "h": { "type": "number", "minimum": 0, "maximum": 1 },
           "t": { "type": "number", "minimum": 0, "maximum": 1 },
           "i": { "type": "number", "minimum": 0, "maximum": 1 },
           "o": { "type": "number", "minimum": 0, "maximum": 1 }
         }
       }
     }
   }


B.2.  Sponsorship Bond Schema

   {
     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "$id": "https://ktp.example.org/schemas/sponsorship-bond.json",
     "title": "KTP Sponsorship Bond",
     "type": "object",
     "required": [
       "bond_id", "sponsor_id", "sponsored_id", "stake_percentage",
       "stake_amount", "penalty_rate", "duration", "created_at",
       "expires_at", "status", "sponsor_signature", "oracle_witness"
     ],
     "properties": {
       "bond_id": { "type": "string" },
       "sponsor_id": { "type": "string", "format": "uri" },
       "sponsored_id": { "type": "string", "format": "uri" },
       "stake_percentage": {
         "type": "number", "minimum": 1, "maximum": 50
       },
       "stake_amount": {
         "type": "number", "minimum": 0, "maximum": 50
       },
       "penalty_rate": {
         "type": "number", "minimum": 1, "maximum": 5
       },
       "duration": { "type": "string", "format": "duration" },
       "created_at": { "type": "string", "format": "date-time" },
       "expires_at": { "type": "string", "format": "date-time" },
       "status": {
         "type": "string",
         "enum": ["active", "released", "penalized"]
       },
       "sponsor_signature": { "type": "string" },
       "oracle_witness": { "type": "string" }
     }
   }


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
