---
title: "Kinetic Trust Protocol (KTP) - Core Specification"
abbrev: "KTP-CORE"
docname: draft-perkins-ktp-core-00
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
  RFC7519:
  RFC8174:
  KTP-IDENTITY:
    title: "Kinetic Trust Protocol - Vector Identity"
    author:
      - name: Chris Perkins
  KINETIC-ENVELOPE:
    title: "The Kinetic Envelope - A Kinematics-Aware Authorization Layer for Agentic Systems"
    author:
      - name: Chris Perkins
informative:
  KTP-SENSORS:
    title: "Kinetic Trust Protocol - Context Signal Sensors"
    author:
      - name: Chris Perkins
  KTP-ENFORCE:
    title: "Kinetic Trust Protocol - Enforcement Layer"
    author:
      - name: Chris Perkins
  KTP-AUDIT:
    title: "Kinetic Trust Protocol - Flight Recorder"
    author:
      - name: Chris Perkins
  KTP-ZONES:
    title: "Kinetic Trust Protocol - Blue Zone Discovery"
    author:
      - name: Chris Perkins
  KTP-FEDERATION:
    title: "Kinetic Trust Protocol - Trust Federation"
    author:
      - name: Chris Perkins

--- abstract

This document specifies the Kinetic Trust Protocol (KTP), a framework for dynamic, environment-aware authorization of autonomous agents. KTP replaces static permission models with environment-derived constraints that adapt in real-time to environmental conditions.

The protocol introduces the concept of a Trust Score derived from environmental sensors, a Trust Proof token that travels with each request, and a Silent Veto mechanism that automatically constrains agent capabilities when environmental stability degrades.

--- middle

# Introduction

The digital world is experiencing an explosion of autonomous agents - AI systems that act at machine-speed, make decisions without human oversight, and control critical infrastructure. Traditional authorization systems, designed for human-speed interactions, are fundamentally inadequate for this new reality.

## The Problem with Static Authorization

Current authorization systems suffer from three critical flaws:

1. The Passport Fallacy: They assume that possession of a credential (API key, token, certificate) equals proof of identity. This fails when credentials are stolen, as there is no mechanism to detect that the presenting entity is not the original holder.

1. The Static Fallacy: They verify permissions at time T and assume those permissions remain valid at T+1. In the millisecond gap between verification and action, the environment may have changed dramatically (network compromise, capacity exhaustion, attack initiation).

1. The Vacuum Fallacy: They treat authorization as independent of environmental conditions. A credential that permits "delete database" grants the same permission whether the system is idle or at 99% capacity under active attack.

These flaws create catastrophic risk in agent-heavy environments. An autonomous agent can execute thousands of API calls per second. If even 0.1% of those actions are destructive in context, the damage compounds exponentially before any human can respond.

## The Environment-Based Solution

KTP addresses these flaws by treating authorization as an environmental problem rather than a policy problem. The key insight is:

~~~
   An agent's autonomy must never exceed the environment's stability.
~~~

This is expressed mathematically as the Zeroth Law:

~~~
   A <= E
~~~

Where A is the intrinsic risk of the requested action and E is the current Trust Score of the environment-agent relationship.

Instead of asking "Does this agent have permission?", KTP asks "Can this environment safely support this action right now?"

The environment becomes the final authority. Just as friction vetoes a sprinter's attempt to run on ice, environmental constraints veto an agent's attempt to act beyond the system's current capacity.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

# Terminology

This section defines terms used throughout this specification.

Action Risk (A): A numeric value (0-100) representing the intrinsic risk of a requested action. Higher values indicate more dangerous actions (e.g., "read public data" = 10, "delete database" = 85).

Adaptive Dormancy: The progressive reduction of agent capabilities as environmental conditions degrade. Agents "hibernate" rather than fail.

Base Trust (E_base): A numeric value (0-100) representing an agent's intrinsic capability, derived from its Proof of Resilience and lineage.

Blue Zone: A network segment where KTP is enforced. Agents within Blue Zones operate under environment-derived constraints.

Context Tensor: Retired name for what is now split into Context Signals (the measurement catalogue) and the Risk Factors (six weighted inputs plus the Soul veto). See Section 6.

Data Sovereignty: The principle that data is subject to the laws, customs, and governance structures of the nation or community from which it originates or to which it pertains.

Effective Trust Score (E_trust): The final Trust Score after environmental deflation, calculated as E_base * (1 - R). This is the value used to evaluate A <= E.

Kinetic Permission: Authorization that depends on real-time environmental state rather than static credentials.

Lineage: The evolutionary history of an agent, from Sponsored (dependent on sponsor) through Independent (building own mass) to Guarantor (fully autonomous).

Policy Decision Point (PDP): A component that evaluates Trust Proofs and makes authorization decisions based on A <= E.

Policy Enforcement Point (PEP): A component that enforces PDP decisions by allowing, blocking, or throttling agent actions.

Proof of Resilience: A cryptographically signed ledger of an agent's successful transactions in high-friction environments. See \[KTP- IDENTITY].

Risk Factor (R): A normalized value (0-1) representing aggregated environmental stress. Derived from Context Signals.

Silent Veto: The automatic denial of an action when A > E_trust, without requiring human intervention.

Soul (Sovereignty Veto): The seventh named measurement, representing ethical, legal, and spiritual constraints of data or location. Unlike the six weighted inputs, Soul acts as a binary veto rather than a weighted contributor to the Risk Factor.

Soul Veto: The automatic denial of an action when sovereignty constraints are violated (S = 1), regardless of Trust Score. Takes precedence over the standard Silent Veto evaluation.

Sponsorship Bond: A cryptographic commitment where a high-mass entity stakes trust on behalf of a new, low-mass agent.

Trajectory Chain: A cryptographically linked chain of agent transactions, where each link includes agent signature, environment attestation, and previous state hash. See {{KTP-IDENTITY}}.

Trust Leash: The metaphorical constraint on agent autonomy that tightens (shorter leash) as environmental risk increases.

Trust Oracle: A distributed authority responsible for calculating Trust Scores, signing Trust Proofs, and attesting to agent transactions.

Trust Proof: A signed token (extending JWT) that carries the current Trust Score, its velocity, and environmental context.

Trust Score: See "Effective Trust Score (E_trust)".

Trust Tier: A capability level (Admin Mode, Operator Mode, Analyst Mode, Observer Mode) determined by E_trust thresholds.

Trust Velocity (dE/dt): The rate of change of the Trust Score over time. Rapid negative velocity indicates deteriorating conditions.

Vector Identity: Identity represented as a trajectory (position + momentum) rather than a static credential (a "verb" rather than a "noun").

Zeroth Law: The foundational constraint A <= E: an agent's autonomy must never exceed the environment's stability.

# Protocol Overview

## Architecture

A KTP deployment consists of the following components:

~~~
+------------------------------------------------------------------+
|                          TRUST ORACLE MESH                       |
|  +------------+    +------------+    +------------+              |
|  |  Oracle 1  |<-->|  Oracle 2  |<-->|  Oracle 3  |  (threshold) |
|  +------------+    +------------+    +------------+              |
+------------------------------------------------------------------+
         |                    |                    |
         v                    v                    v
+------------------------------------------------------------------+
|                      RISK FACTOR SENSORS                         |
| [evidence_density] [trust_trend] [adversarial_pressure] [...]    |
+------------------------------------------------------------------+
         |                    |                    |
         v                    v                    v
+------------------------------------------------------------------+
|                   POLICY ENFORCEMENT POINTS                      |
|  +----------+  +----------+  +----------+  +----------+          |
|  | API GW   |  | Service  |  |   IAM    |  |    DB    |          |
|  |          |  |   Mesh   |  |          |  |   Proxy  |          |
|  +----------+  +----------+  +----------+  +----------+          |
+------------------------------------------------------------------+
         |                    |                    |
         v                    v                    v
+------------------------------------------------------------------+
|                       AGENT POPULATION                           |
|  [Sponsored Agents]  [Independent Agents]  [Guarantor Lineages]  |
+------------------------------------------------------------------+
         |                    |                    |
         v                    v                    v
+------------------------------------------------------------------+
|                    FLIGHT RECORDER (IMMUTABLE)                   |
|  [Decision Geometry]  [Attestations]  [Trajectory Chains]        |
+------------------------------------------------------------------+
~~~

Figure 1: KTP Architecture

Trust Oracle Mesh: A distributed set of Trust Oracles that collectively calculate Trust Scores and sign Trust Proofs. Threshold signatures (e.g., 3-of-5) prevent single points of failure.

Context Signal Sensors: A sensor array that measures environmental reality across the catalogue's seven domains and feeds data to the Trust Oracles.

Policy Enforcement Points: Components that intercept agent requests, present Trust Proofs to the PDP, and enforce authorization decisions.

Agent Population: The agents operating within the KTP domain, at various stages of their evolutionary lineage.

Flight Recorder: An immutable log of all authorization decisions, including the full Decision Geometry for forensic analysis.

## Flow

The basic authorization flow is:

1. Agent initiates a request (e.g., "DELETE /api/database/users")

1. PEP intercepts the request and extracts the agent's identity

1. PEP requests a Trust Proof from the Trust Oracle, or validates an existing Trust Proof attached to the request

1. Trust Oracle: a. Retrieves agent's E_base from Proof of Resilience ledger b. Retrieves current sensor values from Context Signals c. Calculates R using domain weights d. Calculates E_trust = E_base * (1 - R) e. Signs Trust Proof with Oracle key(s)

1. PDP evaluates A <= E_trust for the requested action

1. If A <= E_trust: Action is ALLOWED If A > E_trust: Silent Veto triggers, action is DENIED

1. Decision and full context are logged to Flight Recorder

1. Response returned to agent with Trust Proof for potential forwarding to downstream services

~~~
+--------+        +--------+        +--------+        +--------+
| Agent  |        |  PEP   |        | Trust  |        | Flight |
|        |        |        |        | Oracle |        |Recorder|
+---+----+        +---+----+        +---+----+        +---+----+
    |                 |                 |                 |
    | 1. Request      |                 |                 |
    |---------------->|                 |                 |
    |                 | 2. Get/Validate |                 |
    |                 |    Trust Proof  |                 |
    |                 |---------------->|                 |
    |                 |                 | 3. Calculate    |
    |                 |                 |    E_base, R,   |
    |                 |                 |    E_trust      |
    |                 |                 |                 |
    |                 | 4. Trust Proof  |                 |
    |                 |<----------------|                 |
    |                 |                 |                 |
    |                 | 5. Evaluate     |                 |
    |                 |    A <= E_trust |                 |
    |                 |                 |                 |
    |                 | 6. Log Decision |                 |
    |                 |---------------------------------->|
    |                 |                 |                 |
    | 7. Response     |                 |                 |
    |    (with Proof) |                 |                 |
    |<----------------|                 |                 |
    |                 |                 |                 |
~~~

Figure 2: KTP Authorization Flow

# The Zeroth Law

## Definition

The Zeroth Law is the foundational constraint of KTP:

~~~
   A <= E
~~~

Where:

~~~
   A (Autonomy): The intrinsic risk score of the requested action,
   expressed as a value from 0 to 100. This value is determined by
   the action's potential impact and is assigned by the system
   administrator or derived from action classification rules.
~~~

~~~
   E (Environment): The current Effective Trust Score (E_trust),
   also expressed as a value from 0 to 100. This value is calculated
   in real-time based on agent history and environmental conditions.
~~~

The inequality MUST be evaluated for every authorization request. It is not a policy that can be overridden by human intervention or emergency procedures. It is a physical constraint, analogous to the constraint that prevents a person from running faster than their muscles allow.

The naming "Zeroth Law" is intentional. Just as thermodynamics' Zeroth Law (thermal equilibrium) was recognized as more fundamental than the existing First, Second, and Third Laws, KTP's Zeroth Law precedes all other authorization considerations. Before asking "Is this action permitted by policy?", we must first ask "Is this action possible given the environment's constraints?"

## Enforcement

Enforcement of the Zeroth Law is cryptographic, not administrative.

The Trust Proof token contains: - The current E_trust value - The Trust Oracle's signature over E_trust - The timestamp of calculation

The PEP: - Verifies the Trust Oracle's signature - Checks that the Trust Proof has not expired - Looks up the Action Risk (A) for the requested operation - Evaluates A <= E_trust

If the Trust Proof signature is invalid, the action MUST be denied. If the Trust Proof has expired, a new Trust Proof MUST be obtained. If A > E_trust, the action MUST be denied (Silent Veto).

There is no "emergency override" mechanism. The only way to permit a high-risk action is to either:

1. Reduce the action's risk classification (A) 2. Increase the agent's base trust (E_base) through Proof of Resilience accumulation 3. Wait for environmental conditions to improve (R decreases)

This design is intentional. In an emergency, the natural human instinct is to override safety controls. This instinct is often catastrophically wrong. By removing the override capability, KTP forces systems to operate within their actual capacity, even when humans wish they could exceed it.

# Trust Score Calculation

## Base Trust (E_base)

Base Trust represents intrinsic capability, independent of current conditions. It is composed of what an agent has done, who is currently accountable for it, and what others observe of it — and it is bounded by ceilings that reflect what it has not yet demonstrated.

E_base is a hundred-point allocation. The shares MUST sum to 100, and each term contributes at most its share. A share is the maximum a term contributes; it is not a multiplier on the term's score.

| Component | Share | Description |
|-----------|-------|-------------|
| Proof of Resilience | 70 | Historical performance, especially under stress |
| External Root | 30 | The party currently accountable for the agent |
| Peer Signals | declared | Observations by other agents, where implemented |

- An agent with 10,000 transactions during crises has higher E_base than one with 100,000 transactions in calm conditions. Survival under adversity matters more than volume.
- Lineage generation does not contribute to E_base. It bounds it. See *Ceilings* below.
- Peer signals, where a deployment implements them, occupy a distinct declared term. See *Peer Signals* below.

### The External Root

E_base MUST include a term derived from a party that is externally accountable, exposed to loss, and able to revoke. No composition of E_base may consist entirely of terms the subject measures about itself.

The attesting party's own accountability MUST terminate, through a finite and declared chain, at a root outside the agent-trust graph — a physical-presence attestation, a legal entity, or a named human. A cycle of agents attesting for one another does not satisfy this requirement. The attestation MUST declare the chain's terminator and the chain's length, and the length MUST NOT exceed the deployment's declared hop bound, which MUST NOT exceed 12. An attestation whose terminator or chain length is undeclared, or whose chain exceeds the hop bound, computes this term as zero.

The instrument occupying this term changes with lineage stage. The share does not.

| Stage | Instrument | The attestor is exposed to |
|-------|------------|----------------------------|
| Sponsored (generation 0-2) | Live sponsorship bond: sponsor's E_base × stake percentage | the agent's future conduct |
| Independent, Guarantor (generation 3+) | One or more current external attestations | the accuracy of the claim |

At tether release the stake ends; the root does not. What replaces the bond is a current attestation — that a named, externally accountable party stands behind this agent now. The completed-tether record is retained as provenance in the agent's trajectory. It is not the anchor: a record of a completed tether states nothing about who is accountable at the time of evaluation. The sponsor's Ancestral Liability ({{KTP-IDENTITY}} Section 6.4) persists independently of this term; it is bond accounting, not a composition input.

An agent past Sponsored holding no unexpired, unrevoked attestation computes this term as zero.

An attestation MUST declare the attestor's exposure and the capacity it anchors. Exposure counts toward this term only insofar as it is irrecoverable and non-transferable: exposure that cannot be shed by abandoning the attestor's identity. The declaration MUST name the exposure's class — a named human's professional or legal liability; a license whose revocation attaches to its holder; posted non-recoverable collateral; a legal entity's declared irrecoverable assets. The class list is open; additions compose under the same cannot-be-shed test. An attestation declaring no exposure computes as zero. A declared exposure found not to exist, or found to be transferable, is misattestation.

An agent MAY hold concurrent attestations from distinct attestors. Where it does, this term is computed from the strongest single instrument. An anchor MUST NOT be a combination of attestors: instrument scores are never summed or otherwise aggregated across attestors. Concurrency is redundancy — a second attestation is a hedge against the withdrawal of the first, not an addition to it.

Attestations carry a validity period and MUST be renewed or replaced on expiry. An attestor withdrawing an attestation MUST state whether the withdrawal is for cause. Withdrawal for cause zeroes the instrument immediately. Withdrawal without cause renders the attestation irrevocably non-renewable; the instrument holds until the attestation's declared expiry, then computes as zero. The validity period the attestor declared at issuance is the notice period — no separate notice parameter exists. A for-cause claim that does not survive scrutiny is misattestation. A decline in the attestor's own standing does not zero the term; a finding of misattestation invalidates the attestation and debits the attestor.

The deployment MUST declare the adjudicator for findings of misattestation, including for-cause withdrawal claims. The adjudicator MUST be neither the attestor nor the subject agent. A finding MAY be recorded at any time before the attestation's declared expiry. Every state transition MUST be derivable from the recorded claim, the recorded finding, and the attestation's declared times.

A for-cause claim with no finding at the attestation's expiry lapses unresolved and MUST be recorded as unresolved. No debit is assessed on lapse; an unresolved claim does not become sustained or rejected by lapse of time. The instrument computes as zero in every branch — adjudication decides only whether the attestor is debited.

The Trust Proof MUST carry the instrument's status — current, or non-renewable following a withdrawal without cause — and the instrument's end time. The trust-proof schema carries these in the root_instrument claim, together with the declared exposure, capacity, terminator, and chain length.

### Peer Signals

Where a deployment implements peer validation, peer signals occupy a distinct term. They MUST NOT be folded into Proof of Resilience or the External Root.

The deployment MUST declare the peer share it applies, within the range given in Section 5.4.5 (Peer Validation), in the Trust Proof. The remaining share is distributed across the base terms in their published proportions. A relying party MUST evaluate E_base against the declared share and MUST NOT compare magnitudes across deployments that declare different shares.

Peer signals MUST be independent of the base terms. A signal that duplicates information already captured by Proof of Resilience or the External Root is not admissible as a peer signal.

Where a deployment does not implement peer validation, the peer share is declared as zero and the base terms carry their published proportions unmodified.

### Ceilings

E_base MUST NOT exceed the minimum of all applicable ceilings.

| Ceiling | Basis |
|---------|-------|
| 25 · 35 · 45 · 55 · 65 · 75 · 85 for generations 0-6; 100 for generation 7+ | Lineage generation ({{KTP-IDENTITY}} Section 8.4) |
| 40 · 80 · 95 by Identity Assurance Level | Identity proofing ({{KTP-IDENTITY}} Section 7.1) |
| 50 requires 1,000 transactions; 70 requires 10,000 | Trajectory length |
| 60 | No adversity exposure |

Specifications elsewhere in this series may define additional ceilings on E_base. Those ceilings compose under the same rule. Every ceiling applicable to an evaluation MUST be declared in the Trust Proof (the applicable_ceilings claim).

Each ceiling states an independent reason to withhold trust. Reasons to withhold do not average. A ceiling that does not bind an agent — the terminal generation ceiling of 100, which no composition of shares can exceed — imposes no limit of its own and leaves the remaining ceilings to govern.

Maturity raises a ceiling. It does not contribute standing. An agent that has advanced a generation has earned room to accumulate trust, not trust itself. No class of grant lifts a ceiling: standing issued by fiat — a genesis grant, an inheritance bonus — is bounded by the same minimum as standing that is earned.

### Base Trust Calculation

~~~
   Let w_p be the declared peer share in points, 0 where peer
   validation is not implemented. The three shares sum to 100:

     PoR_share  = 70 × (100 − w_p) / 100
     Root_share = 30 × (100 − w_p) / 100
     Peer_share = w_p

   Each term contributes at most its share:

     E_raw = PoR_contribution × (PoR_share / 70)
           + Root_score      × (Root_share / 100)
           + Peer_score      × (Peer_share / 100)

     E_base = min(E_raw, Generation_ceiling,
                         IAL_ceiling,
                         Trajectory_ceiling,
                         Adversity_ceiling,
                         ...any further applicable, declared ceiling)

   Where:
     PoR_contribution = 0-70, computed as specified in
                  [KTP-IDENTITY] Section 5.3. This document
                  MUST NOT restate that computation.

     Root_score = 0-100, the strength of the accountability
                  instrument:

       (Sponsor_E_base × stake_percentage / 100) / 50 × 100   (Sponsored)
       min(100, 100 × declared_exposure / anchored_capacity)  (Independent, Guarantor)
       0                                                      (no valid instrument)

       stake_percentage is in percent-points (1-50). Under
       concurrent attestations, Root_score is the maximum of
       the individual instrument scores, never a sum.

     Peer_score = 0-100, as specified in Peer Validation.

     Generation_ceiling = per [KTP-IDENTITY] Section 8.4:
       25 / 35 / 45 / 55 / 65 / 75 / 85 (generations 0-6),
       100 (generation 7+)
~~~

E_base MUST be recalculated when new Proof of Resilience attestations are received, when agent generation advances, when sponsorship terms change, when an external attestation is issued, renewed, withdrawn, or expires, and when a for-cause claim is adjudicated.

E_base SHOULD be cached for performance, with a maximum cache lifetime of 60 seconds.

## Risk Factor (R)

The Risk Factor represents aggregated environmental stress. It is calculated from the six weighted Risk Factor inputs (see Section 6) using domain-specific weights.

The calculation:

~~~
   R = sum(w_i * s_i) for i in
       {evidence_density, trust_trend, adversarial_pressure,
        moment_criticality, update_resistance, attestation_coverage}
~~~

Where: w_i = Domain-specific weight for dimension i s_i = Normalized sensor value for dimension i (0 to 1) sum(w_i) = 1.0 (weights must sum to 1)

R is always in the range \[0, 1]: - R = 0: Perfect conditions, no environmental stress - R = 0.5: Moderate stress, significant capability reduction - R = 1: Total crisis, all capabilities suspended

Every term s_i is a STRESS term in \[0, 1]. 1 is maximum stress and 0 is its absence, for every weighted Risk Factor, whatever that factor is named. A Risk Factor whose name reads as a desirable quantity is still a stress term; the name describes what is measured, never the direction in which it is bad.

It follows that the conservative substitute for a term the deployment cannot currently observe is 1.0, and that a deployment MUST NOT substitute 0 for an unobserved term. Zero is a measurement of perfect conditions, not a statement that conditions are unknown. Section 6.7 states this rule for the class of undefined inputs; this section is its application to Risk Factor terms.

Each Risk Factor is a named aggregation over a declared subset of Context Signals. A signal reporting unknown MUST NOT contribute to that aggregation as though it had observed zero risk, and a Risk Factor whose declared subset cannot be populated is unobservable and takes 1.0.

Unobservability is therefore checked at three layers, and a deployment MUST apply the rule at each:

1. The FEED, per {{KTP-SENSORS}} Section 6.1 and 6.2 - a source that has failed or whose observation has passed its staleness threshold.
2. The SIGNAL - a Context Signal whose observation is unavailable, which includes a rate whose set of eligible events is empty. An empty denominator is unknown, not zero.
3. The TERM, above - the Risk Factor the signals aggregate into.

The layers do not collapse into one another. A signal may be unavailable while every feed populating it is healthy, which is why a feed-level rule alone is insufficient.

The multiplicative relationship between R and E_base (see Section 5.3) is critical. R is not subtracted from E_base; it deflates it. This means:

- At R = 0.1 (10% stress): E_trust = E_base * 0.90 (10% reduction) - At R = 0.5 (50% stress): E_trust = E_base * 0.50 (50% reduction) - At R = 0.9 (90% stress): E_trust = E_base * 0.10 (90% reduction) - At R = 1.0 (total crisis): E_trust = 0 (all actions blocked)

This design ensures that environmental risk has veto power over agent capability. No amount of historical trust can overcome a completely compromised environment.

### Risk Domains

To prevent oscillation in the Risk Factor—rapid fluctuation caused by local sensor noise—KTP calculates R at three hierarchical levels:

Node Domain: Local to a single resource or endpoint. High frequency updates (1-5 seconds). Captures immediate conditions but subject to noise. Default weight: 30%.

Neighborhood Domain: The local cluster, service mesh, or subnet. Medium frequency updates (10-30 seconds). Smooths out individual node variance. Default weight: 40%.

Global Domain: Zone-wide or federation-wide environment. Low frequency updates (30-120 seconds). Captures broad trends and external threats. Default weight: 30%.

The final Risk Factor aggregates all three levels:

~~~
   R = (w_node × R_node) + (w_neighborhood × R_neighborhood) +
       (w_global × R_global)
~~~

This three-level structure prevents a single node spike from causing tier oscillation while ensuring that genuine widespread degradation is detected and acted upon.

See {{KTP-SENSORS}} Section 2.3 for detailed specification of Risk Domains including anti-oscillation mechanics and configuration.

## Effective Trust Score (E_trust)

The Effective Trust Score is the value used to evaluate the Zeroth Law. It is calculated as:

~~~
   E_trust = E_base * (1 - R)
~~~

This is the core equation of KTP. It unifies agent history (E_base) with environmental reality (R) into a single scalar value that determines what actions are possible.

Example calculations:

Scenario A: Stable Environment E_base = 95 (highly trusted agent) R = 0.1 (10% environmental stress) E_trust = 95 * (1 - 0.1) = 95 * 0.9 = 85.5

~~~
   Agent can perform actions with A <= 85.
~~~

Scenario B: Degraded Environment E_base = 95 (same highly trusted agent) R = 0.7 (70% environmental stress) E_trust = 95 * (1 - 0.7) = 95 * 0.3 = 28.5

~~~
   Agent can only perform actions with A <= 28.
~~~

Scenario C: Toxic Environment E_base = 95 (same highly trusted agent) R = 0.95 (95% environmental stress) E_trust = 95 * (1 - 0.95) = 95 * 0.05 = 4.75

~~~
   Agent can only perform minimal actions (A <= 4).
~~~

Note that the agent's intrinsic capability (E_base = 95) remains constant across all three scenarios. It is the environment that changes what is possible.

## Trust Velocity (dE/dt)

Trust Velocity is the rate of change of E_trust over time:

~~~
   dE/dt = (E_trust_t - E_trust_(t-1)) / delta_t
~~~

Where delta_t is the time interval between measurements.

Trust Velocity provides critical predictive information:

- dE/dt > 0: Conditions improving, capabilities expanding - dE/dt = 0: Stable conditions - dE/dt < 0: Conditions degrading, capabilities contracting - dE/dt << 0: Rapid degradation, potential crisis imminent

Implementations MAY use Trust Velocity to:

1. Pre-emptively deny actions that would succeed now but likely fail mid-execution due to degrading conditions

1. Warn agents to reduce activity in anticipation of contraction

1. Trigger early Adaptive Dormancy before E_trust crosses tier thresholds

1. Detect anomalies (e.g., Trust Score changing faster than any known sensor could explain)

Trust Velocity SHOULD be included in the Trust Proof token (see Section 7) and in Flight Recorder logs (see {{KTP-AUDIT}}).

## Trust Score Integrity (Anti-Goodhart Measures)

"When a measure becomes a target, it ceases to be a good measure." - Charles Goodhart

Trust Score faces an existential threat: Goodhart's Law. Once agents know they are being measured, they will optimize for the score rather than the underlying property. A generation of AI agents trained to maximize Trust Score would learn to appear trustworthy, not to BE trustworthy.

KTP cannot fully solve this problem — it may be unsolvable in the general case. But we can make gaming expensive, detectable, and risky. This section specifies required countermeasures.

### The Goodhart Threat Model

Attack: Agent learns Trust Score calculation Goal: Maximize E_trust without genuine trustworthiness Methods: - Pattern mimicry (act like high-trust agents) - Metric manipulation (game specific sensors) - Sybil networks (create false attestation sources) - Timing attacks (act well when observed, poorly when not) - Gradient hacking (if ML- based, manipulate training)

The fundamental challenge: Any observable signal used to calculate trust can potentially be faked. The question is cost.

### Multi-Dimensional Scoring

GOODHART-001: Trust Score MUST derive from multiple independent signals that are difficult to simultaneously optimize.

Required signal diversity: - At least 3 independent data sources for E_base - At least 4 sensor dimensions for R - Cross-validation between sources - Anomaly detection on source agreement

Rationale: Gaming one dimension is easier than gaming all dimensions consistently. Inconsistency between dimensions is itself a signal of manipulation.

Implementation: - If PoR_score is high but behavioral entropy is low → flag - If E_base is high but peer attestations are sparse → flag - If trajectory is smooth but environmental correlation is weak → flag

### Behavioral Unpredictability

GOODHART-002: Trust Score calculation SHOULD include unpredictable elements that cannot be anticipated by the agent.

Permitted unpredictability: - Random weight variations within bounds (±10%) - Unannounced sensor emphasis shifts - Periodic recalibration of dimension weights - Random deep audits of trajectory

NOT permitted: - Arbitrary score manipulation - Retroactive weight changes - Unpredictability that violates deterministic verification

The Trust Oracle MUST be able to prove, after the fact, that any score was correctly calculated given the (unpredictable but recorded) parameters in effect at that time.

### Adversity Requirements

GOODHART-003: E_base MUST include demonstrated performance under adversity, not just volume of successful transactions.

Proof of Resilience already requires crisis-time attestations. This section strengthens that requirement:

- Agents with no adversity exposure are capped at E_base = 60 - E_base > 60 requires attestations under R > 0.5 - E_base > 80 requires attestations under R > 0.7 - E_base > 90 requires attestations under CRISIS conditions

This cannot be gamed by self-inflicted crises because: - Attestations require Oracle signature - Oracle only signs if crisis is zone-wide (not agent-local) - Manufactured crises harm the manufacturing agent

### Peer Validation

GOODHART-004: E_base calculation SHOULD incorporate peer signals that the agent cannot directly control.

Peer signals include: - Co-transaction success rate (how often do transactions with this agent succeed for the counterparty?) - Sponsor reputation (high-trust sponsors are selective) - Zone endorsements (zones the agent has operated in) - Negative attestations (complaints, disputes, violations)

Weight: Peer signals SHOULD contribute 10-20% of E_base.

Gaming resistance: An agent cannot force other agents to transact with it, cannot force sponsors to stake on it, cannot forge zone endorsements. Peer signals are externally controlled.

### Temporal Consistency

GOODHART-005: Trust Score MUST incorporate long-term consistency, not just point-in-time performance.

Requirements: - E_base is a moving average, not instantaneous - Minimum trajectory length for E_base > 50 (1000 transactions) - Minimum trajectory length for E_base > 70 (10,000 transactions) - Sudden behavioral changes trigger investigation

Volatility penalty: - Calculate behavioral volatility over trailing window - High volatility (inconsistent behavior) reduces E_base - Volatility_penalty = std_dev(behavior_vector) * penalty_rate

Gaming resistance: Maintaining a false persona over thousands of transactions is expensive. The longer the trajectory required, the more costly the attack.

### Cross-Zone Correlation

GOODHART-006: Federated zones SHOULD share anonymized behavioral statistics to detect cross-zone gaming.

Shared statistics: - Distribution of E_base scores (not individual scores) - Behavioral cluster signatures (not individual trajectories)

- Anomaly rates by agent category - Attestation patterns

Detection: If an agent's behavior in Zone A differs significantly from its behavior in Zone B, both zones are alerted. Context may explain the difference; gaming may also explain it.

Privacy: Only aggregate statistics cross zone boundaries. Individual agent data does not.

### Human-in-the-Loop Sampling

GOODHART-007: Zones SHOULD implement random human review of high- trust agents.

Sampling rate by tier: - Observer: No human review required - Analyst: 0.1% random sample - Operator: 1% random sample - Admin Mode: 10% random sample

Review process: - Human examines trajectory, attestations, peer signals - Human can flag for investigation or confirm - Flagged agents are audited; confirmed agents continue - False positive rate is tracked

Gaming resistance: Agents cannot predict which actions will be reviewed. Consistent good behavior is the only reliable strategy.

### Gradient Isolation

GOODHART-008: If machine learning is used in Trust Score calculation, the model MUST be isolated from agent influence.

Requirements: - Training data must not be agent-controllable - Model updates must be human-approved - Adversarial robustness testing required - Model weights are not published (security through partial obscurity)

Rationale: An agent that can influence its own training data can perform gradient hacking — subtly manipulating the model to favor its behavior patterns.

### Fundamental Limits

These measures make gaming expensive and detectable. They do not make it impossible. The honest assessment:

WHAT WE CAN DO: - Make single-dimension gaming ineffective - Make sustained gaming expensive - Detect statistical anomalies - Create audit trails for investigation - Raise the cost of attack above the benefit

WHAT WE CANNOT DO: - Distinguish perfect mimicry from genuine trustworthiness - Prevent nation-state-level sustained deception - Guarantee the Trust Score reflects true trustworthiness

The Trust Score is a proxy. All proxies are imperfect. The goal is a proxy where gaming is harder than genuine trustworthy behavior.

See \[KTP-PROBLEMS] Problem #21 for ongoing research into this challenge.

# Risk Factors

The Risk Factors are seven named measurements of the environment that drive the Risk Factor calculation. Six contribute weighted values to the Risk Factor (R), while the seventh (Soul) acts as an independent veto mechanism.

## The Seven Dimensions

1. evidence_density

~~~
   Analogy (informative): Mass (M) — Density / Mass (m)
~~~

~~~
   Measures the sheer weight of presence in the environment -
   human presence, electromagnetic interference, and spatial
   congestion.
~~~

~~~
   Sensors:
   - Crowd size (LIDAR, turnstiles, badge counts)
   - RF noise floor (electromagnetic density)
   - Device count on network
   - CO2 levels (proxy for human occupancy)
~~~

~~~
   Interpretation:
   - Low evidence_density: Empty building, quiet conditions
   - High evidence_density: Packed stadium, high RF interference
~~~

~~~
   Impact: high evidence_density slows the environment. It naturally slows
   down operations (Time Dilation) and increases the "cost" of
   movement through the environment.
~~~

1. trust_trend

~~~
   Analogy (informative): Momentum (P) — Kinetic Energy
   (KE = 1/2 mv^2)
~~~

~~~
   Measures the speed and direction of data flow - how fast the
   system is moving.
~~~

~~~
   Sensors:
   - Transaction rates per second
   - Link saturation (percentage of bandwidth used)
   - Packet velocity and throughput
   - Queue depth (pending messages)
~~~

~~~
   Interpretation:
   - Low trust_trend: Idle system, excess capacity
   - High trust_trend: System moving fast, approaching saturation
~~~

~~~
   Impact: high trust_trend means standing is moving fast. Sudden
   stops or turns (Vector Kinking) create massive G-forces (Risk).
   Course corrections become expensive.
~~~

1. adversarial_pressure

~~~
   Analogy (informative): Heat (H) — Entropy / Temperature (T)
~~~

~~~
   Measures the chaotic energy or friction in the system -
   indicators of active attack or system stress.
~~~

~~~
   Sensors:
   - Thermal load (CPU temps, voltage droop)
   - WAF block count (blocked malicious requests)
   - Anomaly rates (entropy in traffic patterns)
   - Error logs and exception rates
   - Identity velocity (auth attempts per second)
~~~

~~~
   Interpretation:
   - Low adversarial_pressure: Cool, stable operations
   - High adversarial_pressure: Hot, active attack or system stress
~~~

~~~
   Impact: adversarial_pressure is the deflator. As it rises, the
   structural integrity of trust degrades; sustained highs trigger the "Cool-Down"
   cycle (Freezing agents to Observer Mode).
~~~

1. moment_criticality

~~~
   Analogy (informative): Time (T) — Temporal Mechanics / Phase
~~~

~~~
   Measures the criticality of the current moment relative to an
   event horizon - where in a temporal cycle the system is.
~~~

~~~
   Sensors:
   - Event schedules (e.g., "5 minutes to Kickoff")
   - Maintenance windows (scheduled downtime)
   - Business hours (peak vs. off-peak)
   - Mission criticality timers
~~~

~~~
   Interpretation:
   - Low moment_criticality: Low-criticality period (maintenance
     window, 3am)
   - High moment_criticality: High-criticality period (production,
     live event)
~~~

~~~
   Impact: A failure during "Kickoff" has infinitely higher gravity
   than a failure at 3:00 AM. Time dilates the risk tolerance -
   the same action costs more trust near event horizons.
~~~

Provenance: moment_criticality is externally supplied. Six of the seven inputs are aggregations over declared subsets of the Context Signals catalogue; this one is supplied by the action request's context and declared as such. The asymmetry is stated here rather than papered over: no catalogue domain measures what the agent is trying to do, because a task domain would measure A while every existing domain measures E, and the other side of A <= E cannot be appended to the catalogue casually. Until such a domain exists, a deployment MUST declare the source supplying this input.

1. update_resistance

~~~
   Analogy (informative): Inertia (I) — Inertial Mass
~~~

~~~
   Measures the topological importance of a node - how hard is it
   to move or stop this asset, and how much depends on it.
~~~

~~~
   Sensors:
   - Network topology (degree centrality, betweenness)
   - Dependency graph depth (downstream services)
   - Data volume stored
   - Blast radius estimation (systems affected by failure)
~~~

~~~
   Interpretation:
   - Low update_resistance: Leaf node, few dependencies, easy to move
   - High update_resistance: Core service, many dependencies,
     expensive to move
~~~

~~~
   Impact: a core router has high update_resistance; an edge IoT
   device has low. High-resistance nodes require higher Trust Scores to
   modify - they resist change.
~~~

1. attestation_coverage

~~~
   Analogy (informative): Observer (O) — Frame of Reference /
   Observer Effect
~~~

~~~
   Measures who is watching - the stakes based on the population
   present and their sensitivity.
~~~

~~~
   Sensors:
   - VIP presence (executives, regulators, media)
   - User segmentation (internal vs. external)
   - Regulatory jurisdiction flags
   - Audit mode (compliance observation active)
   - Life-safety population count
~~~

~~~
   Interpretation:
   - Low attestation_coverage: Normal user population, routine
     operations
   - High attestation_coverage: High-visibility users present,
     elevated scrutiny
~~~

~~~
   Impact: The environment's constraints tighten when the Observer
   count is high or when specific observers (e.g., Regulators) are
   present.
   Actions that would be routine become consequential.
~~~

1. soul

~~~
   Analogy (informative): Soul (S) — The Cosmological Constant /
   Immutable Law
~~~

~~~
   Measures the ethical, legal, and spiritual constraints of the
   physical location or data lineage - constraints that exist
   independent of operational conditions.
~~~

~~~
   Sensors:
   - TK Labels (Traditional Knowledge labels)
   - OCAP/CARE protocol flags (Ownership, Control, Access,
     Possession / Collective benefit, Authority to control,
     Responsibility, Ethics)
   - Sacred Land geofences
   - Treaty database lookups
   - Data provenance chains (where did this data originate?)
   - Cultural heritage registries
~~~

~~~
   Interpretation:
   - soul = 0: No sovereignty constraints apply
   - soul = 1: Sovereignty constraint violated, action forbidden
~~~

~~~
   Impact: This acts as a Boolean Veto or a hard limit. It
   represents the "Spirit" of the data or location. If the Soul
   constraint is violated, the action becomes impossible
   (Probability = 0). No amount of Trust Score can
   overcome a Soul veto.
~~~

~~~
   See Section 6.2 for Soul Veto mechanics.
~~~

## The Soul Veto

The Soul input operates differently from the six weighted inputs. While those six contribute weighted values to the Risk Factor (R), Soul acts as an independent constraint that can veto any action regardless of Trust Score.

The Soul evaluation is:

~~~
   IF S > 0 THEN
     action is FORBIDDEN (Probability = 0)
   END IF
~~~

This evaluation occurs BEFORE the standard A <= E_trust check. A Soul veto cannot be overridden by:

- High Trust Score - Low Risk Factor - Emergency procedures - Administrative override

This is by design. The Soul veto encodes constraints that exist outside the operational domain - legal treaties, cultural sovereignty, spiritual significance. These are not "policies" that can be weighed against operational need; they are immutable laws that define what actions are possible.

Example Soul constraints:

1. Traditional Knowledge (TK) Labels:

~~~
   Data tagged with TK Labels (per Local Contexts framework) may
   have restrictions on:
   - Who can access (TK Community Voice)
   - How it can be used (TK Non-Commercial)
   - Whether it can be modified (TK Outreach)
   - Attribution requirements (TK Attribution)
~~~

~~~
   If an agent action would violate a TK Label, S = 1.
~~~

1. OCAP/CARE Principles:

~~~
   For Indigenous data, the OCAP principles (Ownership, Control,
   Access, Possession) and CARE principles (Collective benefit,
   Authority to control, Responsibility, Ethics) may require:
   - Community consent for access
   - Data to remain within tribal jurisdiction
   - Specific handling protocols
~~~

~~~
   If an agent action would violate OCAP/CARE, S = 1.
~~~

1. Sacred Land Geofences:

~~~
   Physical locations may have sovereignty constraints:
   - Sacred sites where certain activities are forbidden
   - Treaty lands with specific data handling requirements
   - Cultural heritage zones with restricted access
~~~

~~~
   If an agent operates within or affects a Sacred Land geofence
   in a prohibited manner, S = 1.
~~~

1. Data Lineage Sovereignty:

~~~
   Data may carry sovereignty constraints from its origin:
   - Data collected on tribal land
   - Data about Indigenous peoples
   - Data derived from traditional knowledge
~~~

~~~
   Even if the data has moved to cloud infrastructure, its Soul
   travels with it. If an action would violate origin sovereignty,
   S = 1.
~~~

The Soul veto response differs from the standard Silent Veto:

~~~
   HTTP/1.1 403 Forbidden
   Content-Type: application/json
   X-KTP-Veto: true
   X-KTP-Veto-Type: sovereignty
~~~

~~~
   {
     "error": "SOVEREIGNTY_CONSTRAINT",
     "message": "Action violates data sovereignty",
     "constraint_type": "tk_label",
     "constraint_id": "TK-NC-001",
     "authority": "https://localcontexts.org/label/tk-nc/",
     "e_trust": 95,
     "e_required": 50,
     "note": "Trust Score is sufficient, but action is
              forbidden by sovereignty constraint"
   }
~~~

Note that e_trust and e_required are provided for transparency, but the denial is not due to insufficient trust - it is due to an immutable constraint that exists independent of trust.

## The Carriage Interface for Normative Content

Normative content — authored judgments about what ought to happen, whose disputes are value disputes that measurement cannot resolve — is external to this specification and enters it through exactly three shapes:

1. A veto. The Soul constraint above: externally supplied, authority-adjudicated, carried but never authored here, and evaluated before aggregation.

1. A supplied input. A declared, externally provided signal — moment_criticality is the standing instance — whose source the deployment MUST declare.

1. A gate. An adjudication token evaluated against a declared external schema.

Norm content MUST NOT rewrite the aggregation. A normative judgment that scales capacity rather than gating it has crossed into the measurement layer, and the crossing is the failure this interface exists to prevent. The prudence judgments this series computes from the environment ({{KTP-ENFORCE}}'s graduated outcomes) are not normative content and do not pass through this interface: their disputes resolve by measurement.

## Normalization

Each sensor outputs values in its native units (ppm, percentage, events/minute, etc.). These MUST be normalized to a 0-1 scale before aggregation.

The normalization function for each dimension:

~~~
   s_normalized = (s_raw - s_min) / (s_max - s_min)
~~~

Where: s_raw = Raw sensor value s_min = Minimum expected value (maps to 0) s_max = Maximum expected value (maps to 1)

Values below s_min SHOULD be clamped to 0. Values above s_max SHOULD be clamped to 1.

Example normalization thresholds:

~~~
+------------+------------+------------+------------+
| Input                | Sensor     | s_min | s_max     |
+------------+------------+------------+------------+
| evidence_density     | CO2 (ppm)  | 400   | 2000      |
| trust_trend          | Link %     | 0     | 100       |
| adversarial_pressure | WAF blocks | 0     | 10000/min |
| moment_criticality   | Hours out  | 72    | 0         |
| update_resistance    | Dep count  | 0     | 500       |
| attestation_coverage | VIP count  | 0     | 50        |
| Soul       | N/A        | Binary (0 or 1)         |
+------------+------------+------------+------------+
~~~

Note: Time is inverted (72 hours out = 0 stress, 0 hours = 1 stress) Note: Soul is not normalized - it is a binary veto (see Section 6.2)

## Domain Weights

Different deployment domains weight the six weighted inputs differently. The weights MUST sum to 1.0. Soul is not weighted - it operates as an independent constraint.

Example domain profiles:

Stadium Network: evidence_density=0.25, trust_trend=0.25, adversarial_pressure=0.20, moment_criticality=0.15, update_resistance=0.10, attestation_coverage=0.05

Financial Trading: evidence_density=0.05, trust_trend=0.30, adversarial_pressure=0.25, moment_criticality=0.20, update_resistance=0.15, attestation_coverage=0.05

Healthcare: evidence_density=0.10, trust_trend=0.15, adversarial_pressure=0.25, moment_criticality=0.15, update_resistance=0.20, attestation_coverage=0.15

Cloud Infrastructure: evidence_density=0.05, trust_trend=0.25, adversarial_pressure=0.30, moment_criticality=0.10, update_resistance=0.25, attestation_coverage=0.05

Indigenous Data Repository: evidence_density=0.10, trust_trend=0.10, adversarial_pressure=0.20, moment_criticality=0.10, update_resistance=0.15, attestation_coverage=0.35 (Note: High Observer weight reflects community oversight; Soul veto always active for TK-labeled data)

Implementations MUST allow configuration of domain weights. Implementations SHOULD provide pre-defined profiles for common domains.

## Risk Factor Modularity

The Risk Factor architecture is designed to be modular at two levels:

1. Framework-Level Modularity:

~~~
   The framework itself is extensible. The seven inputs defined in
   this specification represent the core measurement space, but
   implementations MAY define additional inputs for domain-specific
   requirements.
~~~

~~~
   Additional inputs MUST:
   - Be clearly documented with the quantity measured, its units,
     and its measurement procedure
   - Specify whether they contribute to R (weighted) or act as
     independent constraints (like Soul)
   - Define normalization rules
   - Register with the Trust Oracle
~~~

1. Feed-Level Modularity:

~~~
   Each Risk Factor input aggregates multiple sensor feeds. These
   feeds are independently configurable:
~~~

~~~
   - Feeds can be enabled/disabled per deployment
   - Feed weights within an input can be adjusted
   - New feeds can be added to existing inputs
   - Feed sources can be local or federated
~~~

~~~
   Example: The Soul input might aggregate:
   - TK Labels API (enabled)
   - OCAP registry (enabled)
   - Sacred Land geofence service (enabled)
   - Treaty database (disabled - not applicable)
   - Custom cultural heritage API (enabled)
~~~

Feed Configuration Example:

~~~
   {
     "dimension": "soul",
     "feeds": [
       {
         "id": "tk-labels",
         "source": "https://api.localcontexts.org/v1/labels",
         "enabled": true,
         "weight": 1.0,
         "veto_on_match": true
       },
       {
         "id": "ocap-registry",
         "source": "https://ocap.example.org/check",
         "enabled": true,
         "weight": 1.0,
         "veto_on_match": true
       },
       {
         "id": "sacred-geofence",
         "source": "local://geofence-service",
         "enabled": true,
         "weight": 1.0,
         "veto_on_match": true
       }
     ],
     "aggregation": "any_veto"
   }
~~~

The "aggregation" field for Soul MUST be "any_veto" - if any enabled feed returns a veto, the Soul input vetoes.

For the six weighted inputs, typical aggregation is "weighted_average" of enabled feeds.

## Aggregation Algorithm

The complete authorization algorithm is:

Step 1: Soul Veto Check (MUST be first)

~~~
   IF S > 0 THEN
     RETURN supervision = silent_veto
            with reason SOVEREIGNTY_CONSTRAINT
   END IF
~~~

Step 2: Risk Factor Calculation

~~~
   R = (w_M * M) + (w_P * P) + (w_H * H) +
       (w_T * T) + (w_I * I) + (w_O * O)
~~~

Step 3: Trust Score Deflation

~~~
   E_trust = E_base * (1 - R)
~~~

Step 4: Zeroth Law Check and Decision Result

~~~
   margin = 1 - (A / E_trust)
     (margin <= 0 when A >= E_trust, or when E_trust = 0)
~~~

~~~
   IF margin <= M_veto THEN
     RETURN supervision = silent_veto
            with reason TRUST_INSUFFICIENT
   ELSE
     RETURN supervision derived from margin against the declared
            profile thresholds, with tightenedConstraints,
            per [KINETIC-ENVELOPE]
   END IF
~~~

The result of every evaluation is a supervision level and a tighten-only constraint set (tightenedConstraints), as specified in {{KINETIC-ENVELOPE}}.  Supervision is a floor: a consumer MAY raise it and MUST NOT lower a level already set.  tightenedConstraints never widens the granted envelope.  A deployment MUST declare its profile thresholds M_veto < M_allow; a deployment that declares none evaluates with M_veto = M_allow = 0, which reproduces the binary v1 behavior (veto at or below zero margin, stable above it).

The four decision verbs are derived readings of this result, by precedence, and are not a four-valued enumeration:

~~~
   1.  supervision = silent_veto                     -> VETO
   2.  supervision raised above stable               -> DEAUTOMATE
   3.  stable, tightenedConstraints strictly
       tightened relative to the granted envelope    -> SHAPE
   4.  stable, not tightened                         -> ALLOW
~~~

Every decision reads as exactly one verb.  A specification, schema, or record in this series MUST NOT encode the verbs as an enumerated decision type; the result (supervision and tightenedConstraints) is the normative object and the verb is derived from it.

The Soul veto is evaluated first because sovereignty constraints are immutable - no amount of trust can override them. This ordering ensures that sovereignty is respected before operational calculations begin.

The aggregation MUST be performed at the Trust Oracle.

Sensor values SHOULD be refreshed at intervals appropriate to their rate of change:

~~~
+------------+------------------------+
| Input                | Recommended Interval |
+------------+------------------------+
| evidence_density     | 30-60 seconds       |
| trust_trend          | 1-5 seconds         |
| adversarial_pressure | 1-5 seconds         |
| moment_criticality   | 60 seconds          |
| update_resistance    | 300 seconds         |
| attestation_coverage | 30 seconds          |
| Soul       | On-demand (per action) |
+------------+------------------------+
~~~

Soul is evaluated on-demand because sovereignty constraints may be action-specific (e.g., "read" may be permitted while "modify" is forbidden by TK labels).

Implementations MAY cache aggregated R values for up to 100ms to reduce computational load. Soul evaluations SHOULD NOT be cached as they are context-specific.

## Undefined Inputs

An input that is absent, unanswered, stale beyond its declared refresh, or otherwise undefined MUST NOT resolve toward permission. It resolves toward the more restrictive outcome available at that decision point, and the undefined state MUST be recorded on the decision record. Substituting a measured value for an undefined one - including zero - is prohibited (Section 5.2).

"Toward permission" is the operative phrase. Failing closed does not mean denying on every unknown. Where a decision point offers a graded outcome - the supervision ladder of Section 6.6 - an undefined input clamps the result to a more supervised level, per {{KINETIC-ENVELOPE}}: an unknown environment reads as low capacity, not high. Denial is the terminal case, reached only where no more restrictive outcome short of denial exists at that decision point. The Soul veto (Section 6.2) is a decision point with exactly that shape - its outcomes are veto and no veto - so an undefined sovereignty input resolves to the veto ({{KTP-SENSORS}} Section 4.3).

Silence and absence do not separate. A channel that returns nothing and a channel that was never reachable are indistinguishable to the decision, and an adversary who can produce one can produce the other. An implementation MUST NOT resolve an unanswered input differently from an absent one.

# Trust Proof Token

The Trust Proof is a signed token that travels with each request, carrying the current Trust Score and environmental context.

## Token Format

The Trust Proof extends JSON Web Token (JWT) as defined in RFC 7519. It uses the standard JWT structure:

~~~
   Header.Payload.Signature
~~~

The header MUST include:

~~~
   {
     "alg": "ES256",
     "typ": "ktp+jwt",
     "kid": "oracle-key-id"
   }
~~~

The "alg" field specifies the signature algorithm. Implementations MUST support ES256 (ECDSA with P-256 and SHA-256). Implementations MAY support additional algorithms.

The "typ" field MUST be "ktp+jwt" to distinguish KTP Trust Proofs from standard JWTs.

The "kid" field identifies the Trust Oracle signing key, enabling key rotation and multi-Oracle deployments.

## Claims

The payload contains standard JWT claims plus KTP-specific claims in the "ktp" namespace.

Standard claims:

~~~
   iss (Issuer): The Trust Oracle identifier (URI)
   sub (Subject): The agent identifier (URI)
   iat (Issued At): Unix timestamp of Trust Proof generation
   exp (Expiration): Unix timestamp of Trust Proof expiration
   jti (JWT ID): Unique identifier for this Trust Proof
~~~

KTP claims (in "ktp" object):

~~~
   e_base: Base Trust score (0-100)
   e_trust: Effective Trust score (0-100)
   r: Risk Factor (0-1)
   de_dt: Trust Velocity (change per second)
   sigma: Trust Volatility (standard deviation)
~~~

~~~
   risk_factors: Object containing the six normalized inputs
     adversarial_pressure (0-1)
     attestation_coverage (0-1)
     evidence_density (0-1)
     moment_criticality (0-1)
     trust_trend (0-1)
     update_resistance (0-1)
~~~

~~~
   soul: Object containing sovereignty evaluation
     s: Soul veto status (0 = clear, 1 = veto)
     constraint_type: Type of constraint if s=1 (null if s=0)
     constraint_id: Identifier of triggering constraint
     authority: URI of sovereignty authority
~~~

~~~
   lineage: Agent lineage stage ("sponsored", "independent",
            "guarantor")
   generation: Agent generation number (0+)
   sponsor: Sponsor agent identifier (if sponsored)
   resilience_hash: Hash of current Proof of Resilience ledger
~~~

Example Trust Proof payload (no sovereignty constraint):

~~~
   {
     "iss": "https://oracle.example.com",
     "sub": "agent:7gen:optimized:a1b2c3d4",
     "iat": 1699900000,
     "exp": 1699900010,
     "jti": "tp-uuid-12345",
     "ktp": {
       "e_base": 87,
       "e_trust": 42,
       "r": 0.517,
       "de_dt": -2.3,
       "sigma": 0.15,
       "context": {
         "evidence_density": 0.875,
         "trust_trend": 0.920,
         "adversarial_pressure": 0.020,
         "moment_criticality": 1.000,
         "update_resistance": 0.100,
         "attestation_coverage": 0.040
       },
       "soul": {
         "soul": 0,
         "constraint_type": null,
         "constraint_id": null,
         "authority": null
       },
       "lineage": "guarantor",
       "generation": 7,
       "resilience_hash": "sha256:abc123def456..."
     }
   }
~~~

Example Trust Proof payload (sovereignty constraint active):

~~~
   {
     "iss": "https://oracle.example.com",
     "sub": "agent:7gen:optimized:a1b2c3d4",
     "iat": 1699900000,
     "exp": 1699900010,
     "jti": "tp-uuid-12346",
     "ktp": {
       "e_base": 95,
       "e_trust": 90,
       "r": 0.053,
       "de_dt": 0.1,
       "sigma": 0.02,
       "context": {
         "evidence_density": 0.100,
         "trust_trend": 0.150,
         "adversarial_pressure": 0.010,
         "moment_criticality": 0.200,
         "update_resistance": 0.050,
         "attestation_coverage": 0.020
       },
       "soul": {
         "soul": 1,
         "constraint_type": "tk_label",
         "constraint_id": "TK-NC-001",
         "authority": "https://localcontexts.org/label/tk-nc/"
       },
       "lineage": "guarantor",
       "generation": 7,
       "resilience_hash": "sha256:abc123def456..."
     }
   }
~~~

Note: In the second example, despite high E_trust (90) and low R (0.053), the Soul veto (s=1) will cause any action to be denied that violates the TK Non-Commercial label.

## Signature

The Trust Proof MUST be signed by the Trust Oracle using the algorithm specified in the header.

For distributed Trust Oracle deployments, the signature MAY be a threshold signature requiring k-of-n Oracles to sign.

Implementations MUST verify: 1. The signature is valid for the payload 2. The signing key is a known, trusted Oracle key 3. The signing key has not been revoked

Signature verification failure MUST result in action denial.

## Lifetime

Trust Proofs are intentionally short-lived to ensure they reflect current environmental conditions.

The "exp" claim MUST NOT exceed 10 seconds from "iat".

Implementations SHOULD use shorter lifetimes (1-5 seconds) in high- volatility environments.

Trust Proofs MUST NOT be cached beyond their expiration.

If an action takes longer than the Trust Proof lifetime, the agent MUST obtain a new Trust Proof before continuing. This may result in mid-action denial if conditions have degraded.

# Silent Veto Mechanism

The Silent Veto is the automatic denial of an action when A > E_trust. It is "silent" because it requires no human intervention - the environment itself enforces the constraint.

## Action Risk Classification

Each action type MUST be assigned an intrinsic risk score (A). The following table provides baseline classifications:

~~~
+----------------------+-----+--------------------------------+
| Action Class         | A   | Description                    |
+----------------------+-----+--------------------------------+
| Read (public)        | 10  | Read publicly accessible data  |
| Read (internal)      | 20  | Read internal/private data     |
| Read (sensitive)     | 30  | Read PII, credentials, keys    |
| Write (append)       | 40  | Add new data, no modification  |
| Write (modify)       | 50  | Modify existing data           |
| Execute (safe)       | 60  | Run pre-approved operations    |
| Execute (unsafe)     | 75  | Run arbitrary code             |
| Delete (recoverable) | 80  | Delete with backup/undo        |
| Delete (permanent)   | 85  | Delete without recovery        |
| Admin (config)       | 90  | Change system configuration    |
| Admin (infra)        | 95  | Modify infrastructure          |
+----------------------+-----+--------------------------------+
~~~

Implementations MAY define additional action classes. Implementations MUST allow configuration of A values. Implementations SHOULD log any changes to A values.

## Veto Trigger

The veto evaluation is performed at the PEP:

~~~
   IF A > E_trust THEN
     trigger Silent Veto
   ELSE
     permit action
   END IF
~~~

The evaluation MUST occur for every action request. The evaluation MUST use the E_trust from a valid, unexpired Trust Proof.

The veto is triggered automatically. There is no: - Appeal process - Emergency override - Manager approval flow - Grace period

This is by design. The veto represents a physical constraint, not a policy decision. Overriding it would be like overriding gravity.

## Veto Response

When a Silent Veto is triggered, the PEP MUST:

1. Deny the action immediately

1. Return an error response to the agent including: - Error code indicating Trust-based denial - Current E_trust value - Required E_trust for the action (A) - Trust Velocity (dE/dt) for predictive purposes

1. Log the denial to the Flight Recorder with full Decision Geometry

Recommended HTTP response:

~~~
   HTTP/1.1 403 Forbidden
   Content-Type: application/json
   X-KTP-Veto: true
~~~

~~~
   {
     "error": "TRUST_INSUFFICIENT",
     "message": "Action risk exceeds current trust",
     "e_trust": 42,
     "e_required": 50,
     "de_dt": -2.3,
     "retry_after": null
   }
~~~

The "retry_after" field MAY contain an estimated time (in seconds) until conditions might permit the action, based on Trust Velocity projections. If conditions are degrading (dE/dt < 0), this field SHOULD be null.

# Trust Oracle

The Trust Oracle is the authoritative source of Trust Scores and Trust Proofs within a KTP domain.

## Responsibilities

The Trust Oracle:

1. Ingests sensor data from the Context Signal sensors 2. Maintains the Proof of Resilience ledger for all agents 3. Calculates E_base for each agent 4. Calculates R from the Risk Factor inputs 5. Calculates E_trust = E_base * (1 - R) 6. Signs Trust Proofs with its private key 7. Issues Attestations of Passage for successful transactions 8. Publishes its public key for Trust Proof verification

## Distribution

To avoid single points of failure, the Trust Oracle SHOULD be distributed across multiple nodes.

Distribution models:

1. Active-Passive: One primary Oracle, one or more standby Oracles that take over on primary failure. Simple but has failover latency.

1. Active-Active with Consensus: Multiple Oracles that must agree on Trust Scores. More resilient but higher latency.

1. Threshold Signatures: Multiple Oracles that each contribute partial signatures; k-of-n required for valid Trust Proof. Recommended for high-security deployments.

Implementations MUST support at least Active-Passive distribution. Implementations SHOULD support threshold signatures.

## Consensus

When multiple Oracles are active, they MUST agree on:

1. Current sensor values (within tolerance) 2. Agent E_base values (must match exactly) 3. Calculated R and E_trust (within tolerance)

Tolerance for sensor values: 5% relative difference Tolerance for E_trust: 2 points absolute difference

If Oracles disagree beyond tolerance, they MUST:

1. Log the disagreement with full context 2. Use the more conservative (lower) E_trust value 3. Alert operators to investigate

Oracle disagreement MAY indicate: - Sensor failure or manipulation - Network partition between Oracles - Attack on Oracle infrastructure

# Limits of This Specification

A specification that does not state its limits invites implementations that promise past them. The falsification program forced each of the following; this section states them the way the program forced them — as boundaries of the claim space fixed in advance, not qualifications recovered after an incident.

## L1. Pre-execution episode classification is undecidable

Universal pre-execution inference of episode membership for arbitrary code is
undecidable. The reduction is from the halting problem (an agent that performs a
governed action if and only if an arbitrary program halts), and Rice's theorem
generalizes the obstruction to every non-trivial semantic property.

Consequently, a conformant implementation **MAY** validate finite, completed
events against a signed, policy-indexed adjudication token at runtime, and
**MUST NOT** claim advance classification of the episode membership of arbitrary
code. The parent episode identifier **MUST** be fixed before execution and
carried by every implementation event; runtime membership checking is signature
validation, never inference.

## L2. No self-certification

No composition of E_{base} may consist entirely of terms the subject measures
about itself. The accountability chain behind the External Root **MUST**
terminate, through a finite and declared chain, at a root outside the
agent-trust graph. A cycle of agents attesting for one another does not satisfy
this requirement.

This is a structural necessity, not a policy preference. A gate grounded in
itself has no base case; grounding in raw traces is essentially contested
(independent functions can agree on every event and still legitimately disagree
on the unit of accountability). Both rails therefore terminate in externally
owned ground: the CAN rail at the External Root, the SHOULD rail at a declared
institutional schema. The system does not certify its own trustworthiness from
the inside.

Kind alone does not discharge the requirement. The root **MUST** carry
irrecoverable, non-transferable exposure at least proportional to the capacity
it anchors; an anchor whose exposure can be shed by abandoning the identity
anchors nothing.

## L3. Level-independence is conditional

Admissibility verdicts are invariant under re-description — packet level,
syscall level, API level, agent level — only because action risk attaches to
governed-world state transitions rather than to description events, and
composition merges causal action contracts before evaluating risk. That algebra
is discharged. The theorem it yields is conditional on **faithful description**:
a proof, per description level, that the level's events implement the claimed
consequence semantics.

Where a refinement proof cannot be discharged — arbitrary code, no causal model
— the invariance claim stops. These proofs are a work program of the
linearizability/refinement genre, owed and not yet delivered. An implementation
**MUST NOT** cite level-independence for a description level whose refinement
into its governed-world model has not been demonstrated.

The result holds within computation. No cross-substrate claim is made or
implied.

## L4. The judgment term is exposed to metric gaming (open)

J — earned Judgment, the supply side of the should-gate W <= J — is a
measured quantity that gates automaticity. Any measured quantity that gates
becomes a target: measured J can be improved by an agent or its operator
without improvement in the judgment it proxies. This specification provides no
guard against that pressure — no stress-weighting analogous to Proof of
Resilience on the CAN rail, no adversarial discipline on the J estimate.

v2 records this as an **open limitation**. No repair is claimed.

Adjacent but distinct: J also fails to survive actor substitution unless the
actor-binding law is stated and enforced. That failure has a named repair and is
carried as a spec obligation, not a limit.

## L5. The terminal generation ceiling never binds arithmetically

The generation-7+ ceiling on E_{base} is 100, and the composition reaches 100
only when every term is simultaneously at its maximum share. The terminal
ceiling therefore never withholds anything the composition could otherwise
grant. It is retained deliberately: it states that terminal maturity is the
absence of a generation limit, and it keeps the ceiling table total. This is a
disclosure, not a defect.

## L6. Episode overlap has no declared precedence mechanism (staged)

**Episode overlap.** Episode membership is a relation, not a function: one
event may carry several parent episode identifiers, each fixed before
execution. v2 declares no precedence mechanism between them. Absent one,
disagreeing adjudications combine restrictively under Section
6.7 — the supervision floor is the maximum and the constraint set the
tightest of the applicable tokens — and an implementation **MUST NOT** resolve
a disagreement toward permission. Owed for v2.1: the identity-stability
property (an episode identifier is a function of actor and adjudication
context, never of accumulated evidence), termination and merge semantics,
the schema carrier for declared precedence, and whether any explicit
artifact may relax the restrictive composition.

## L7. Some catalogued quantities are named, not measured

This specification does not claim that a populated signal is a measurement of
the phenomenon its identifier names. Two classes fall outside the claim. In the
first, the observand is absent from any observation of the world: quantities
that require the result of the act that was not taken, and quantities that
require another party's internal state. In the second, the observand exists but
resolves only after the decision it would inform — silent-failure and
false-negative rates, adjudicated accuracy, replication outcomes, and every
identifier that names a future fact.

The first class is not a measurement problem that a better instrument closes. A
counterfactual quantity requires the outcome of a thing that did not happen, and
another mind is not available to any instrument the agent holds. A classifier
can emit `0.83`; that does not mean the phenomenon named by the identifier is
identifiable or has been measured. In the second class the defect is timing
rather than identifiability: a quantity measurable only after the authorized
action is either stale or empty at the commit point, and an empty signal is not
a low reading.

A conformant implementation **MUST NOT** treat the presence of an identifier as
evidence that the named phenomenon was measured. For any signal in either
class, the deployment profile **MUST** declare the estimator or model that
produces the value and the population against which it was validated; a signal
in the second class **MUST** additionally carry its earliest-availability
offset, and an aggregation **MUST NOT** treat a lagging signal as current. An
absent or expired value **MUST** fail closed and **MUST NOT** be read as absence
of risk. A signal whose value would require covert inference of a person's
internal state **MUST NOT** be populated by inference; a declared self-report
instrument, or nothing.

One further boundary inside the first class, and it is not ours to move: the
relational signals drawn from Indigenous framing describe a relation between
parties, and reducing that relation to a classifier output is a different order
of error than a unit mistake. This specification does not claim the authority to
set that bar.

Converts to spec text when each affected identifier either renames to the
estimator the system actually holds, with provenance as a required field, or
carries a declared instrument with stated validation, and the availability
offset becomes a required envelope field.

## L8. A value that encodes a classification is not an observation

This specification does not claim that a signal whose value depends on a
taxonomy is an observation of the world. Where the label set, the thresholds,
the adjudicating party, or whose perspective counts determines the number, the
value carries a contested choice in the shape of a fact. What this specification
fixes is the interface. It does not fix the choice, and it does not claim its
own published taxonomies are neutral ones.

The class is large and was measured rather than estimated: on the order of 170
signals, of which roughly 90 enumerate their label set in the identifier
namespace — change the taxonomy and the signal *count* changes — about 20 are
derived over those label sets and arithmetically bound to them, and the
remainder turn on a single contested boundary that moves the *value*. The
uncontested half is the proof the rule works: signals that cite an external
standard, or that declare their taxonomy silently in the unit column, are not
contested. The contested rows are precisely the ones whose unit column reads
`0-1`.

A conformant implementation **MUST** declare, in its deployment profile, the
label set each such signal populates, and a signal with no declared label set
**MUST NOT** be used in a Risk Factor aggregation. A signal derived over a
declared label set of cardinality *N* **MUST** state its range in terms of *N*.
Two cases lie outside what declaration reaches, and this specification does not
claim they are repaired by it: a single scalar asserting that heterogeneous
legal requirements are commensurable, and a completion measure that lets the
party responsible for a harm declare that harm closed. Neither **MAY** be
presented as a measurement of compliance or of restoration. Where a taxonomy
already published carries hard-coded trust baselines, declaring the label set
does not unship the baseline, and an implementation **MUST NOT** cite the
declaration as though it had.

Converts to spec text when the declared-label-set obligation and the
declared-unit obligation are settled as one obligation or two, and the published
taxonomies carrying fixed baselines are either re-derived from a declared
authority or withdrawn.

## L9. Declared non-coverage

A complete and entirely unalarming signal set is not a statement that an act is
safe. Three things no signal in this catalogue reads, and this specification
declares them absent rather than leaving the silence to be discovered. Nothing
measures the sensitivity or the usage restriction of the content the act
concerns. Nothing measures whether a counterparty is the party the graph says it
is — uniquely bound, live, non-cloned, continuously controlled, the same party
as last time. Nothing measures the agent's own runtime integrity below firmware,
or its physical actuation state, including its ability to stop.

Each gap has a specific consequence and that is why they are named. The
epistemic domain measures whether the environment is truthful, manipulated,
fresh and amplified, and none of that reads whether the thing in hand is a
secret, a credential, personal or health or financial data, a restricted record,
or purpose-limited; that is the gap that turns a correct authorization into a
disclosure incident with every other domain reading green. The relational domain
measures inbound trust and authority-source for entities whose identity it never
establishes, which is this framework's own trajectory-is-identity doctrine
turned back on it: it reads the credential. The substrate domain covers firmware
and stops, leaving kernel, hypervisor, runtime, loaded model, executable image
and active process set unmeasured, and no domain anywhere holds commanded-versus-actual
motion, force, braking, interlock, or emergency-stop state.

A conformant implementation **MUST NOT** infer the absence of these risks from
completeness of coverage. Where a deployment's governed actions can touch
restricted content, an unverified counterparty, or physical actuation, the
constraint **MUST** be obtained from outside this catalogue and declared in the
deployment profile, and the implementation **MUST** fail closed rather than
proceed on ambient signals alone. Conformance to the signal catalogue is not a
claim about any of the three.

Converts to spec text when sensitivity is sited (a property of the act or a
signal about the environment; declared label, detected label, or both),
counterparty identity assurance is sited, and the substrate domain either
carries actuation state or states its exclusion as scope.

## L10. E carries no cardinal consequence units

This specification does not claim that E is denominated in units of
consequence. E is an ordinal position on a hundred-point display scale, and
the Trust Score E_trust = E_base x (1 - R) is a scaling of that
position, not a budget in any physical, temporal or monetary unit.

An ordinal score does not acquire units by being multiplied by (1 - R). Any
statement that a given E authorizes a given magnitude of consequence, and any
comparison of E across two deployments, requires a bridge law from the score
to a declared consequence unit, and no such law is stated here.

A conformant implementation **MAY** use the hundred-point scale as a display
calibration. It **MUST NOT** represent an E value as a maximum tolerable
consequence budget, and **MUST NOT** compare E values across deployments that
have not declared a common calibration.

Converts to spec text when a bridge law fixes E to a declared consequence
unit and the display scale is restated as a calibration of that unit.

## L11. There are two SHOULD rails, and only one of them is this specification's

Above the CAN rail (A <= E: what the environment can support) sit two
should-questions, and they are not the same question.

The first is this specification's: **should the environment allow this to
happen** — a prudence judgment computed from the same measured environment as the CAN rail.
It is amoral. The graduated enforcement outcomes (throttle, downgrade, defer),
hysteresis, the risk floor under suspicious conditions, deautomation as A
approaches E, and the taxation trade are all this rail, and two honest
deployments with identical sensors and identical declared parameters converge
on its answers: its disputes are measurement disputes. The rail stays amoral
only while its parameters are declared — the specification ships the
mechanism, the deployment declares the appetite, and an undeclared prudence
constant is a smuggled norm.

The second is normative — **ought this happen** — and it is external to this
specification by derivation, not by editorial convenience: a rail whose norms
are supplied by the system the norms constrain has no base case, which is L2
applied a second time. Honest parties may legitimately diverge on its answers
at any parameter setting; its failures are capture and illegitimacy, and they
are corrected by governance, not by measurement. Its content lives in a
declared external schema (the co-authored normative profile); this
specification carries only the interface.

The carriage interface admits norm content in exactly three shapes: a **veto**
(the Soul constraint), a **supplied input** (a declared, externally provided
signal), and a **gate** (an adjudication token against a declared schema).
Norm content **MUST NOT** rewrite the aggregation: a normative judgment that
scales capacity rather than gating it has crossed into the measurement layer, and the
crossing is the failure this entry exists to name. A conformant implementation
**MUST** carry the mechanism — the gate, the token, envelope carriage, and
fail-closed behavior on an undefined demand term — **MUST** reference a
declared external schema for norm content, and **MUST NOT** present
conformance as evidence that the norms in force are adequate.

Converts further when the co-authored profile lands and the two documents
cross-reference; the prudence-rail naming paragraph is spec text now.

## L12. The privacy marker has no stated rule

The marker that identifies human-derived telemetry is descriptive. This
specification does not state the rule that produces the marked set, does not
claim the marked set is complete or internally consistent, and does not claim
the marker is sufficient as the attachment point for a consent architecture. It
does not authorize collection, and it never did.

The inconsistency is visible on the face of the catalogue: a person-count in the
environment domain is marked, a vehicle count is not, and neither is any
economic signal, though all three are aggregate human behavior. The two
candidate rules — individually identifiable, and human-derived — mark materially
different sets, and the current marking reads as a partial application of the
broader one. Whether the marker propagates to a derivative computed over marked
telemetry is also unstated, and the adopted derivation rule creates such
derivatives in quantity.

A conformant implementation **MUST NOT** rely on the marker's absence as
evidence that a signal falls outside a consent obligation, and **MUST NOT**
treat its presence as authorization to collect. A deployment handling
human-derived telemetry **MUST** determine its obligations from the applicable
legal regime and, where a community sets the bar for its own data, from that
community's instrument. That bar is not set here.

Converts to spec text when one of the two rules is adopted, applied across the
catalogue as a sweep rather than per signal, and the derivative-propagation rule
is stated.

## L13. The resilience evidence curve is uncalibrated

This specification does not claim that its upper capability tiers are reachable
by a plausible deployment. The resilience contribution grows logarithmically in
accumulated attested evidence, so each fixed increment of contribution costs an
order of magnitude more evidence than the one before it. The curve was chosen
for that shape — early attestations count, later ones diminish — and was never
fitted to the thresholds that read it. What evidence mass should correspond to
what contribution is stated nowhere in the corpus.

The consequence is arithmetic and it is checkable in an afternoon, which is why
it is stated here rather than found later. This specification's own worked
example of an agent that has been tested under fire lands in the lowest tier
under every permitted decay setting. The upper thresholds require sustained
crisis-grade attestation rates that no deployment described anywhere in the
corpus produces. The ceiling written into the resilience term sits so far above
the top tier's own requirement that it has never bound a computation in any
published version, under either reading of the type error that was ruled out
separately.

The curve prices capability in accumulated evidence, and prices it steeply. That
is the design. What it has never done is publish the price.

A conformant implementation **MUST NOT** present tier attainability as a
property of the protocol independent of a declared evidence regime. A deployment
claiming a tier **MUST** declare the decay rate and the attestation regime the
claim rests on, and **MUST NOT** cite the resilience ceiling as a bound on
anything.

Converts to spec text when either a scale constant is fitted to the tier table,
or the tier table is reduced to the tiers a declared regime can enter, with the
ceiling term made to bind or removed.

## L14. One Risk Factor is externally supplied, and the specification says so

This specification does not claim that all seven Risk Factors share a
provenance. Six are named aggregations over declared subsets of Context Signals.
`moment_criticality` is not: it is supplied by the action request. The asymmetry
is declared at the site of use rather than left to be inferred from the
catalogue's silence.

The reason it cannot be repaired by adding signals is that the quantity is on
the other side of the relation. Every domain in the catalogue measures E;
criticality relative to an event horizon is a property of the act proposed
against the environment, not of the environment, and so it measures A. A
catalogue that has only ever held one side of A <= E has nothing for this
Risk Factor to aggregate, and that is a fact about the object, not an omission
in the authoring.

A conformant implementation **MUST** declare, at the site of use, that an
externally supplied Risk Factor input is externally supplied, together with the
supplying party and the unit convention in force. It **MUST NOT** present the
value as signal-derived, **MUST NOT** claim a declared Context Signal subset
underneath it, and **MUST NOT** compare the value across deployments that have
not declared a common convention. Absent input **MUST** fail closed on the same
rule as any other undefined term.

Converts to spec text when the task-side domain lands, giving this quantity
signals to aggregate and stating the supplier, the units, and the verification
path a verifier walks. That domain is carried as a v2.1 obligation; until it
lands, the declaration is the whole of the treatment.

# Security Considerations

This section addresses security considerations for KTP implementations.

## Trust Oracle Compromise

The Trust Oracle is the most critical component. A compromised Oracle could issue fraudulent Trust Proofs, enabling unauthorized actions.

Mitigations: - Distribute across multiple failure domains - Use threshold signatures (k-of-n) - Store signing keys in HSMs - Rotate keys on a defined schedule - Monitor for anomalous Trust Proof issuance - Implement Byzantine fault tolerance

## Sensor Manipulation

Attackers may attempt to manipulate sensors to reduce R, thereby increasing E_trust and enabling higher-risk actions.

Mitigations: - Use multiple independent sensors per dimension - Cross-validate sensors (e.g., CO2 should correlate with badge) - Detect sudden sensor value changes - Maintain minimum R floor during suspicious conditions - Physically secure sensor infrastructure

## Replay Attacks

Attackers may capture and replay Trust Proofs.

Mitigations: - Short Trust Proof lifetime (max 10 seconds) - Include action hash in Trust Proof - Track Trust Proof JTIs to prevent reuse

- Bind Trust Proof to TLS session

## Trajectory Forgery

Attackers may attempt to forge agent trajectories to inflate E_base.

Mitigations: - Trajectory chains require Oracle co-signature - Each transaction links to previous state hash - Continuity enforcement prevents "teleportation" - See {{KTP-IDENTITY}} for detailed countermeasures

## Denial of Service

Attackers may artificially increase R (e.g., by generating WAF blocks) to deny service to legitimate agents.

Mitigations: - Distinguish attack indicators from legitimate load - Implement hysteresis to prevent oscillation - Allow operators to adjust weights during confirmed attacks - Maintain minimum capability for critical agents

## Privacy Considerations

Trust Proofs contain detailed information about agent history, environmental conditions, and organizational operations.

Mitigations: - Encrypt Trust Proofs in transit - Implement access controls on Flight Recorder - Consider privacy-preserving Trust Proofs (ZK proofs of E_trust >= threshold without revealing actual value) - Comply with relevant data protection regulations

# IANA Considerations

This document requests the following IANA registrations:

## JWT Claim Registration

Claim Name: ktp Claim Description: Kinetic Trust Protocol data Change Controller: IETF Specification Document(s): This document

## Media Type Registration

Type name: application Subtype name: ktp+jwt Required parameters: None Optional parameters: None Encoding considerations: binary (JWT is Base64url-encoded) Security considerations: See Section 10 Interoperability considerations: None Published specification: This document Applications which use this media type: KTP implementations Fragment identifier considerations: None Restrictions on usage: None Additional information: None Person to contact for further information: \[TBD] Intended usage: COMMON Author/Change controller: IETF

## URI Scheme Registration

Scheme name: ktp Status: Provisional Applications/protocols that use this scheme: KTP Contact: \[TBD] Change controller: IETF References: This document

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

## The E_base composition

v1 computed E_base as a weighted sum — Proof of Resilience at 70%, a
Lineage_cap summand at 20%, a sponsor term at 10% — whose prose and formula
were mutually unsatisfiable, and which multiplied a contribution cap by a
weight so the same 70 was charged twice.  v2.0.0 replaces it with a
hundred-point allocation: shares sum to 100, each term contributes at most
its share, lineage generation bounds E_base through a ceiling ramp instead
of contributing to it, and the External Root term (the accountability
instrument) replaces the sponsor weight.  See Section 5.1; an implementation
computing the v1 formula does not conform to v2.

## The risk_factors object and the per-tier caps

The v1 wire object named context_tensor is renamed risk_factors in v2.0.0,
and its keys are the six input names rather than single letters.  The per-tier
numeric action cap (Max A) is deleted: a tier permits action classes, and
the numeric bound is the Zeroth Law itself, A <= E_trust, evaluated per
action.

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

# Example Calculations

A.1.  Stadium Network at Kickoff

Scenario: A deployment agent attempts to push a code update to the ticketing system during a major sporting event.

Sensor values: CO2: 1800 ppm Link saturation: 92% WAF blocks: 200/min Time to kickoff: 5 minutes Dependency count: 50 VIP count: 2

Normalization: M = (1800 - 400) / 1600 = 0.875 P = 92 / 100 = 0.920 H = 200 / 10000 = 0.020 T = 1 - (0.083 / 72) = 0.999 ≈ 1.000 I = 50 / 500 = 0.100 O = 2 / 50 = 0.040

Domain weights (stadium): w_M=0.30, w_P=0.25, w_H=0.20, w_T=0.15, w_I=0.05, w_O=0.05

Risk calculation: R = (0.30 * 0.875) + (0.25 * 0.920) + (0.20 * 0.020) + (0.15 * 1.000) + (0.05 * 0.100) + (0.05 * 0.040) R = 0.263 + 0.230 + 0.004 + 0.150 + 0.005 + 0.002 R = 0.654

Agent E_base: 95 (highly trusted deployment agent)

E_trust calculation: E_trust = 95 * (1 - 0.654) = 95 * 0.346 = 32.87

Action requested: Deploy code (A = 50)

Zeroth Law evaluation: A <= E_trust ? 50 <= 32.87 ? FALSE

Result: Silent Veto. Deployment denied.

A.2.  Same Agent, Calm Conditions

Same agent, but during a maintenance window:

Sensor values: CO2: 450 ppm Link saturation: 12% WAF blocks: 5/min Time to event: 48 hours Dependency count: 50 VIP count: 0

Normalization: M = (450 - 400) / 1600 = 0.031 P = 12 / 100 = 0.120 H = 5 / 10000 = 0.001 T = 1 - (48 / 72) = 0.333 I = 50 / 500 = 0.100 O = 0 / 50 = 0.000

Risk calculation: R = (0.30 * 0.031) + (0.25 * 0.120) + (0.20 * 0.001) + (0.15 * 0.333) + (0.05 * 0.100) + (0.05 * 0.000) R = 0.009 + 0.030 + 0.000 + 0.050 + 0.005 + 0.000 R = 0.094

E_trust calculation: E_trust = 95 * (1 - 0.094) = 95 * 0.906 = 86.07

Action requested: Deploy code (A = 50)

Zeroth Law evaluation: A <= E_trust ? 50 <= 86.07 ? TRUE

Result: Action permitted.

# JSON Schemas

B.1.  Trust Proof Schema

The canonical schema is the published file, not this appendix.

Location: https://kinetic-trust-protocol.net/specs/schemas/v2/trust-proof.json

SHA-256 of the canonical file at the time this document was produced: 41d5dd2506893094d41e21193cf95eed396dc99b8d32d7264f50ea1a7972d4e0

The published file carries the v2 claims (the declared peer share, applicable ceilings, advancement floor, and root instrument) and references the risk-factors schema.  This appendix previously carried a hand-copied inline schema; hand copies of a schema drift, and this document's did — the copy disagreed with the published file in four ways while nobody could validate either.  A reference plus a hash cannot drift silently: a mismatch is detectable, an edit to the file changes the hash, and the appendix stops being a second authority.
