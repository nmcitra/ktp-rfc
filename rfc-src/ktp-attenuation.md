---
title: "Kinetic Trust Protocol (KTP) - Capability Attenuation Specification"
abbrev: "KTP-ATTENUATION"
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

--- abstract

This document specifies Digital Gravity for the Kinetic Trust Protocol (KTP).  Digital Gravity is the enforcement mechanism that constrains agent autonomy based on environmental stability.  When the Zeroth Law (A ≤ E) is at risk of violation, Digital Gravity applies physical constraints—latency injection, time dilation, compute throttling, and network isolation—to restore equilibrium.

The specification covers the Zeroth Law calculation, gravity well mechanics, constraint types, response curves, and real-time enforcement requirements.

--- middle

# Introduction

The Kinetic Trust Protocol is built on a single principle: an agent's autonomy must never exceed the environment's capacity to absorb the risk of that autonomy.  This is the Zeroth Law:

~~~
   A ≤ E
~~~

Where:

~~~
   -  A = Agent's attempted autonomy (action risk)
   -  E = Environment's current stability (trust capacity)
~~~

When A approaches or exceeds E, something must give.  In traditional systems, this is handled by policy—access denied, request rejected, human escalation.  These mechanisms operate at human speed and fail when agents operate at machine speed.

Digital Gravity replaces policy with structure.  Instead of deciding whether to allow an action, the environment applies physical constraints that make excessive autonomy impossible.  The agent doesn't hit a wall; it experiences increasing resistance, like moving through an increasingly dense medium.

# The Gravity Analogy (Informative)

In physical gravity, mass curves spacetime.  Objects don't decide to fall; they follow the curvature.  The structure is the governance.

In Digital Gravity, risk curves the operational environment.  Agents don't decide to slow down; latency increases.  Compute becomes scarce.  Network paths narrow.  The structure is the governance.

This shift—from policy to structure—is fundamental.  Policy can be debated, circumvented, or ignored.  Structure cannot.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Terminology

Autonomy (A):  The risk level of an agent's attempted action, measured on a scale of 0-100.  Higher values indicate greater potential impact.

Digital Gravity:  The enforcement mechanism that applies physical constraints to agents based on environmental conditions and action risk.

Environmental Stability (E):  The environment's current capacity to absorb risk, derived from Context Signal measurements. E = E_base × (1 - R).

E_base:  Base trust level derived from agent's Proof of Resilience and trajectory history.

Gravity Well:  A region of increased constraint around high-risk actions or degraded environmental conditions.

Latency Injection:  The deliberate introduction of delay into agent operations as a constraint mechanism.

Risk Factor (R):  Environmental risk derived from Context Signal measurements, ranging from 0.0 (minimal risk) to 1.0 (maximum risk).

Time Dilation:  The apparent slowing of agent-experienced time relative to wall-clock time, achieved through latency injection and processing delays.

Zeroth Law:  The fundamental constraint A ≤ E that governs all KTP operations.

# The Zeroth Law

## Formal Definition

The Zeroth Law states:

~~~
   A ≤ E
~~~

Where:

~~~
   A = autonomy_requested(action)
   E = E_base × (1 - R)
   R = risk_aggregate(risk_factors)
~~~

This inequality MUST be evaluated for every agent action.  If the inequality holds, the action proceeds (possibly with gravity applied).  If violated, the action is blocked.

## Component Calculation

### Autonomy (A)

Autonomy is the risk level of an attempted action.  It is calculated based on:

~~~
   A = base_risk(action_type) × target_sensitivity(resource) ×
       scope_multiplier(affected_entities) ×
       reversibility_factor(can_undo)
~~~

Factors:

~~~
   -  target_sensitivity:  Range 0.5-2.0.  Sensitivity of target
      resource.
   -  scope_multiplier:  Range 1.0-5.0.  How many entities affected.
   -  reversibility_factor:  Range 0.5-2.0.  Can action be undone.
~~~

Example calculations:

~~~
   Read public data:
      A = 10 × 0.5 × 1.0 × 0.5 = 2.5
~~~

~~~
   Modify user record:
      A = 40 × 1.5 × 1.0 × 1.0 = 60
~~~

~~~
   Delete production database:
      A = 90 × 2.0 × 5.0 × 2.0 = 1800 (capped at 100)
~~~

### Environmental Stability (E)

Environmental Stability represents the system's current capacity to absorb risk:

~~~
   E = E_base × (1 - R)
~~~

Where:

~~~
   E_base = agent's base trust (from Proof of Resilience)
   R = current risk factor (from the Risk Factor inputs)
~~~

E_base ranges from 0-100 based on agent trajectory:

~~~
   -  Independent Lineage Phase:  Typical E_base Range 40-80
   -  Guarantor Lineage Phase:  Typical E_base Range 80-100
~~~

R ranges from 0.0-1.0 based on environmental conditions:

~~~
   -  R Value 0.2-0.4:  Elevated concern
   -  R Value 0.4-0.6:  Significant stress
   -  R Value 0.6-0.8:  High risk conditions
   -  R Value 0.8-1.0:  Crisis conditions
~~~

### Risk Factor Calculation

R is derived from the six domain risks:

~~~
   R = weighted_aggregate(
         soul_risk × w_soul,
         body_risk × w_body,
         world_risk × w_world,
         time_risk × w_time,
         relational_risk × w_relational,
         signal_risk × w_signal
       )
~~~

Default weights:

~~~
   -  Soul:    Weight 0.25, Rationale: Agent's core constraints
   -  Body:    Weight 0.10, Rationale: Infrastructure stability
   -  World:   Weight 0.15, Rationale: Environmental conditions
   -  Time:    Weight 0.15, Rationale: Temporal pressures
   -  Relational:  Weight 0.20, Rationale: Trust network health
   -  Signal:  Weight 0.15, Rationale: Epistemic environment
~~~

Weights MUST sum to 1.0.  Zone operators MAY adjust weights based on operational context.

## Evaluation Frequency

The Zeroth Law MUST be evaluated:

~~~
   1.  Before every action (mandatory)
   2.  Continuously during long-running operations (recommended:
       100ms)
   3.  When Risk Factor input values change significantly (threshold:
       0.1)
   4.  When agent requests capability elevation
~~~

Implementations MUST achieve sub-millisecond evaluation latency for the core A ≤ E calculation.

# Gravity Well Mechanics

## Gravity Well Definition

A gravity well is a region of increased constraint.  Wells form around:

~~~
   1.  High-risk actions (action gravity)
   2.  Degraded environmental conditions (environmental gravity)
   3.  Proximity to constraint boundaries (boundary gravity)
~~~

## Gravity Intensity Calculation

Gravity intensity (G) determines the strength of applied constraints:

~~~
   G = max(0, (A - E_threshold) / E) × sensitivity
~~~

Where:

~~~
   A = attempted autonomy
   E_threshold = E × margin_factor (default: 0.8)
   E = environmental stability
   sensitivity = zone configuration (default: 1.0)
~~~

G ranges from 0.0 (no gravity) to unbounded (increasing constraint):

~~~
   -  G Value 0.0-0.5:  Light gravity, minor latency
   -  G Value 0.5-1.0:  Moderate gravity, noticeable delay
   -  G Value 1.0-2.0:  Heavy gravity, significant constraint
   -  G Value 2.0-5.0:  Severe gravity, major throttling
   -  G Value >5.0:     Extreme gravity, near-halt
~~~

## Gravity Response Curves

Different response curves shape how gravity increases:

### Linear Response

~~~
   constraint = G × base_constraint
~~~

Simple proportional response.  Predictable but may allow rapid escalation near boundaries.

### Exponential Response

~~~
   constraint = base_constraint × (e^G - 1)
~~~

Gentle at low G, severe at high G.  Provides soft landing for minor boundary approaches, hard stop for major violations.

### Sigmoid Response

~~~
   constraint = max_constraint × (1 / (1 + e^(-k(G - midpoint))))
~~~

S-curve response.  Minimal effect until threshold, then rapid increase, then plateau at maximum.  Recommended default.

### Step Response

~~~
   constraint = 0 if G < threshold else max_constraint
~~~

Binary response.  No constraint below threshold, maximum above.  Use for hard boundaries only.

Implementations SHOULD support configurable response curves.  Default SHOULD be sigmoid with k=2 and midpoint=1.0.

# Constraint Types

## Latency Injection

The primary constraint mechanism.  Latency is injected into agent operations, slowing perceived time.

### Implementation

~~~
   actual_latency = base_latency + (G × latency_factor)
~~~

Where:

~~~
   base_latency = normal operation latency (typically <10ms)
   G = gravity intensity
   latency_factor = ms per unit G (default: 100ms)
~~~

Example latency values:

~~~
   -  G: 0.5   Added Latency: 50ms    Perceived Effect: Slightly slow
   -  G: 1.0   Added Latency: 100ms   Perceived Effect: Noticeably slow
   -  G: 2.0   Added Latency: 200ms   Perceived Effect: Significantly slow
   -  G: 5.0   Added Latency: 500ms   Perceived Effect: Very slow
   -  G: 10.0  Added Latency: 1000ms  Perceived Effect: Extremely slow
~~~

### Latency Distribution

Latency SHOULD be applied with jitter to prevent timing attacks:

~~~
   applied_latency = calculated_latency × (1 + random(-0.1, 0.1))
~~~

Latency MUST be applied server-side.  Client-side latency can be bypassed.

## Time Dilation

Time dilation extends latency injection to create sustained temporal distortion for high-gravity conditions.

### Dilation Factor

~~~
   dilation_factor = 1 + (G × dilation_coefficient)
~~~

~~~
   agent_time = wall_time / dilation_factor
~~~

At dilation_factor = 2.0, the agent experiences time at half speed—1 second of agent time requires 2 seconds of wall time.

### Dilation Effects

Example dilation factors:

~~~
   -  Dilation Factor 1.5:   Agent experiences 33% slower
   -  Dilation Factor 2.0:   Agent experiences 50% slower
   -  Dilation Factor 5.0:   Agent experiences 80% slower
   -  Dilation Factor 10.0:  Agent experiences 90% slower
~~~

Time dilation affects:

~~~
   -  Response latency
   -  Timeout calculations (adjusted for agent time)
   -  Rate limits (calculated in wall time)
   -  Trajectory recording (wall time stamps)
~~~

## Compute Throttling

Reduces available compute resources under high gravity.

Implementation:

~~~
   available_compute = base_compute × (1 / (1 + G))
~~~

Example throttling:

~~~
   -  G: 1.0   Available Compute: 50%
   -  G: 2.0   Available Compute: 33%
   -  G: 5.0   Available Compute: 17%
   -  G: 10.0  Available Compute: 9%
~~~

Compute throttling is implemented via:

~~~
   -  CPU quota reduction
   -  Memory limit reduction
   -  GPU access restriction
   -  Thread pool shrinking
~~~

## Network Isolation

Restricts network access under high gravity.

Isolation Levels:

~~~
   -  G Threshold 1.0-2.0:  External restricted
   -  G Threshold 2.0-3.0:  Cross-zone restricted
   -  G Threshold 3.0-5.0:  Local zone only
   -  G Threshold >5.0:     Loopback only
~~~

Implementation:

Network isolation is implemented via:

~~~
   -  Firewall rule injection
   -  Routing table modification
   -  DNS resolution restriction
   -  Proxy enforcement
~~~

## Capability Reduction

Reduces available action types under high gravity.

### Trust Tier Demotion

High gravity forces temporary tier demotion:

~~~
   effective_tier = base_tier - floor(G)
~~~

Example demotions:

~~~
   -  Base Tier: Operator   G=1: Analyst    G=2: Observer  G=3: Observer
   -  Base Tier: Analyst    G=1: Observer   G=2: Observer  G=3: Observer
   -  Base Tier: Observer   G=1: Observer   G=2: Observer  G=3: Observer
~~~

### Action Class Restriction

Specific action classes are disabled at gravity thresholds:

~~~
   -  G Threshold 2.0:  Disabled Actions: MODIFY_CONFIG, EXECUTE_CODE
   -  G Threshold 3.0:  Disabled Actions: CREATE_ANY, MODIFY_ANY
   -  G Threshold 5.0:  Disabled Actions: All except READ_PUBLIC
~~~

# Real-Time Enforcement

## Enforcement Architecture

~~~
+------------------------------------------------------------------+
|                      AGENT REQUEST                               |
+------------------------------------------------------------------+
                                 |
                                 v
+------------------------------------------------------------------+
|                  RISK FACTOR COLLECTOR                           |
|   [Soul] [Body] [World] [Time] [Relational] [Signal]             |
+------------------------------------------------------------------+
                                 |
                                 v
+------------------------------------------------------------------+
|                     RISK CALCULATOR                              |
|   R = weighted_aggregate(risk_factor_inputs)                     |
+------------------------------------------------------------------+
                                 |
                                 v
+------------------------------------------------------------------+
|                   ZEROTH LAW EVALUATOR                           |
|   A ≤ E_base × (1 - R) ?                                         |
+------------------------------------------------------------------+
              |                              |
             YES                            NO
              v                              v
+---------------------------+  +---------------------------+
|    GRAVITY CALCULATOR     |  |      ACTION BLOCKED       |
|    G = f(A, E, threshold) |  |   Log, Alert, Respond     |
+---------------------------+  +---------------------------+
              |
              v
+------------------------------------------------------------------+
|                   CONSTRAINT APPLICATOR                          |
|   [Latency] [Dilation] [Compute] [Network] [Capability]          |
+------------------------------------------------------------------+
                                 |
                                 v
+------------------------------------------------------------------+
|                   CONSTRAINED EXECUTION                          |
+------------------------------------------------------------------+
                                 |
                                 v
+------------------------------------------------------------------+
|                    TRAJECTORY RECORDER                           |
+------------------------------------------------------------------+
~~~

## Performance Requirements

The enforcement pipeline MUST meet these performance targets:

~~~
   -  Risk Calculation:       Maximum Latency 0.5ms
   -  Zeroth Law Evaluation:  Maximum Latency 0.1ms
   -  Gravity Calculation:    Maximum Latency 0.1ms
   -  Constraint Application: Maximum Latency 1ms
   -  Total Overhead:         Maximum Latency <5ms
~~~

Implementations MUST NOT add more than 5ms overhead to normal (G=0) operations.

## Caching and Optimization

To meet performance requirements:

~~~
   1.  Risk Factor input values MAY be cached for up to 100ms
   2.  R calculation MAY be cached until input change > 0.05
   3.  E_base MAY be cached until trajectory update
   4.  Gravity curves SHOULD be precomputed as lookup tables
~~~

## Failure Modes

If the enforcement pipeline fails:

~~~
   -  Risk calculation error:  Assume R = 0.5 (moderate risk)
   -  Evaluation error:  Block action, alert operator
   -  Constraint application failure:  Block action, alert operator
~~~

The system MUST fail closed—uncertainty results in constraint, not permission. This is the general rule of KTP-Core, Section 6.7: an undefined input resolves toward the more restrictive outcome available at that decision point, and the undefined state is recorded on the decision record.

# Gravity Profiles

## Zone-Specific Profiles

Zones MAY define custom gravity profiles:

~~~
   {
     "zone_id": "zone-blue-prod-01",
     "gravity_profile": {
       "response_curve": "sigmoid",
       "sigmoid_k": 2.0,
       "sigmoid_midpoint": 1.0,
       "latency_factor_ms": 100,
       "dilation_coefficient": 0.5,
       "compute_throttle_enabled": true,
       "network_isolation_enabled": true,
       "capability_reduction_enabled": true,
       "risk_factor_weights": {
         "soul": 0.25,
         "body": 0.10,
         "world": 0.15,
         "time": 0.15,
         "relational": 0.20,
         "signal": 0.15
       }
     }
   }
~~~

## Agent-Specific Modifiers

Agents MAY have gravity modifiers based on trajectory:

~~~
   {
     "agent_id": "agent:guarantor:7gen:optimized:abc123",
     "gravity_modifiers": {
       "base_reduction": 0.1,
       "earned_through": "proof_of_resilience",
       "valid_until": "2026-01-01T00:00:00Z",
       "conditions": [
         "E_base >= 80",
         "no_violations_90_days"
       ]
     }
   }
~~~

High-trust agents experience slightly reduced gravity as a reward for demonstrated reliability.  This modifier MUST NOT exceed 0.2 and MUST be revoked upon any significant violation.

# Monitoring and Observability

## Gravity Metrics

Implementations MUST expose:

~~~
   -  ktp_gravity_applications:  Count of gravity applications
   -  ktp_zeroth_law_violations:  Count of A > E events
   -  ktp_constraint_latency_ms:  Injected latency histogram
   -  ktp_enforcement_overhead_ms:  Pipeline overhead histogram
~~~

## Alerting Thresholds

~~~
   -  G > 5.0 any duration:  Alert Level Critical
   -  Zeroth Law violation:  Alert Level Critical
   -  Enforcement overhead > 10ms:  Alert Level Warning
~~~

## Audit Trail

Every gravity application MUST be logged:

~~~
   {
     "timestamp": "2025-12-03T14:32:15.123Z",
     "agent_id": "agent:independent:3gen:acme:abc123",
     "action_type": "MODIFY_CONFIG",
     "autonomy_requested": 65,
     "e_base": 55,
     "risk_factor": 0.3,
     "e_effective": 38.5,
     "zeroth_law_result": "violated",
     "gravity_intensity": null,
     "action_result": "blocked",
     "risk_factor_snapshot": {
       "soul_risk": 0.2,
       "body_risk": 0.1,
       "world_risk": 0.3,
       "time_risk": 0.4,
       "relational_risk": 0.3,
       "signal_risk": 0.4
     }
   }
~~~

# Security Considerations

## Gravity Bypass Attempts

Agents may attempt to bypass gravity through:

~~~
   1.  Clock manipulation:  Use wall-clock time from trusted source
   2.  Resource hoarding:  Enforce limits at hypervisor/container
       level
   3.  Network tunneling:  Deep packet inspection, allowlist-only
       egress
   4.  Identity spoofing:  Continuous trajectory verification
   5.  Gradual escalation:  Track cumulative autonomy over time
       windows
~~~

## Gravity Itself Under Gravity

The recursive constraint principle applies: systems that apply gravity are themselves subject to gravity.  Administrative actions to modify gravity profiles require appropriate E_base and are logged to Flight Recorder.

## Denial of Service via Gravity

An attacker might attempt to trigger high gravity for legitimate agents.  Mitigations:

~~~
   1.  Gravity source attribution in logs
   2.  Anomaly detection on R spikes
   3.  Rate limiting on Risk Factor updates from external sources
   4.  Human review threshold for sustained high gravity
~~~

# IANA Considerations

This document has no IANA actions.

# Acknowledgments

This specification builds on decades of work in distributed systems, access control, and environment-derived constraint modeling.

# Example Scenarios

## Scenario 1: Normal Operation

Agent:  agent:independent:4gen:acme:abc123 Action:  READ_DATA on customer_metrics E_base:  60 R:  0.2 (calm environment) E:  60 × 0.8 = 48

A calculation:

~~~
   base_risk = 20 (READ_DATA)
   target_sensitivity = 1.2 (customer data)
   scope = 1.0 (single query)
   reversibility = 0.5 (read-only)
   A = 20 × 1.2 × 1.0 × 0.5 = 12
~~~

Zeroth Law:  12 ≤ 48 ✓ Gravity:  G = 0 (well below threshold) Result:  Action proceeds, no constraint

## Scenario 2: Moderate Gravity

Agent:  agent:independent:3gen:acme:def456 Action:  MODIFY_CONFIG on production_settings E_base:  50 R:  0.4 (elevated environment) E:  50 × 0.6 = 30

A calculation:

~~~
   base_risk = 60 (MODIFY_CONFIG)
   target_sensitivity = 1.5 (production)
   scope = 1.0 (single system)
   reversibility = 1.0 (can rollback)
   A = 60 × 1.5 × 1.0 × 1.0 = 90 (capped at 100)
~~~

Zeroth Law:  90 > 30 ✗ Result:  Action blocked

If A had been 25:

~~~
   Zeroth Law:  25 ≤ 30 ✓
   E_threshold = 30 × 0.8 = 24
   G = (25 - 24) / 30 × 1.0 = 0.033
   Latency:  0 + (0.033 × 100) = 3.3ms added
   Result:  Action proceeds with minor gravity
~~~

## Scenario 3: High Gravity Crisis

Agent:  agent:sponsored:sponsor:ghi789 Action:  DELETE on user_table E_base:  25 R:  0.7 (high risk environment) E:  25 × 0.3 = 7.5

A calculation:

~~~
   base_risk = 80 (DELETE)
   target_sensitivity = 2.0 (user data)
   scope = 5.0 (bulk operation)
   reversibility = 2.0 (hard to undo)
   A = 80 × 2.0 × 5.0 × 2.0 = 1600 (capped at 100)
~~~

Zeroth Law:  100 > 7.5 ✗ Result:  Action blocked

Even READ_PUBLIC (A=5):

~~~
   Zeroth Law:  5 ≤ 7.5 ✓
   E_threshold = 7.5 × 0.8 = 6
   G = (5 - 6) / 7.5 = -0.13 → 0 (no negative gravity)
   Result:  Action proceeds, no constraint
~~~

But ANALYZE_DATA (A=15):

~~~
   Zeroth Law:  15 > 7.5 ✗
   Result:  Action blocked
~~~

Agent is effectively limited to read-only operations during crisis.
