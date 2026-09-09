---
title: "Kinetic Trust Protocol (KTP) - Emergency Response Specification"
abbrev: "KTP-EMERGENCY"
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

This document specifies emergency response procedures for the Kinetic Trust Protocol (KTP).  When normal operations fail—zone collapse, mass agent compromise, Oracle failure, or coordinated attack—the system must degrade gracefully and recover systematically.  The specification covers emergency levels, circuit breakers, graceful degradation, zone collapse protocols, mass compromise response, recovery procedures, and post-incident analysis.

--- middle

# Introduction

Systems fail.  The question is not whether KTP zones will experience emergencies, but how they will respond when emergencies occur.

Digital Gravity is designed to constrain agents during normal operation.  But what happens when:

- The Trust Oracle fails?
- A majority of agents are compromised?
- The zone itself is under attack?
- Environmental stability (E) collapses to near-zero?
- Multiple failures cascade simultaneously?

This specification addresses these scenarios with structured emergency response—protocols that maintain safety while enabling recovery.

The authorization boundary for every procedure below is specifications/emergency-capability.md. Ordinary Trust Proofs expire normally, including during an outage. An emergency level, human approval, cached read, or heartbeat does not grant permission. Any separately authorized emergency action MUST match a preinstalled approved policy and retain the sovereignty, capacity, supervision, audit, and revocation checks defined by that companion.

# Design Principles

Emergency response embodies these principles:

1. Fail Safe: When in doubt, constrain.  Uncertainty should reduce autonomy, not increase it.

1. Graceful Degradation: Partial failure should not cause total failure.  Preserve what can be preserved.

1. Transparent Crisis: Emergencies should be visible.  Hidden failures are more dangerous than visible ones.

1. Human Escalation: Sufficiently severe emergencies require human judgment.  Machines cannot handle everything.

1. Recovery Path: Every emergency state must have a defined path back to normal operation.

1. Learning: Every emergency is an opportunity to improve. Post-incident analysis is mandatory.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Terminology

Circuit Breaker:  An automatic mechanism that disables functionality when failure thresholds are exceeded.

Degraded Mode:  Operational state with reduced capabilities but maintained safety.

Emergency Level:  Classification of emergency severity from Level 1 (minor) to Level 5 (catastrophic).

Graceful Degradation:  Controlled reduction in capability while maintaining core safety.

Mass Compromise:  Simultaneous compromise of multiple agents beyond normal incident response capacity.

Recovery Protocol:  Structured procedure for returning from emergency to normal operation.

Zone Collapse:  Complete loss of zone operational capability.

Zone Isolation:  Severing of zone connections to prevent emergency spread.

# Emergency Levels

## Level Classification

Emergencies are classified by severity:

~~~
+-------+--------------+---------------------------+----------------+
| Level | Name         | Trigger                   | Response Auth  |
+-------+--------------+---------------------------+----------------+
| 1     | Advisory     | Elevated indicators       | Automated      |
| 2     | Warning      | Component degradation     | Automated      |
| 3     | Critical     | Significant capability    | Automated +    |
|       |              | loss                      | Alert          |
| 4     | Severe       | Major system compromise   | Human required |
| 5     | Catastrophic | Zone survival threatened  | Human required |
+-------+--------------+---------------------------+----------------+
~~~

## Level 1: Advisory

Trigger conditions:

- R > 0.4 sustained for 15 minutes
- Single component degradation
- Anomalous behavior pattern detected
- External threat intelligence received

Automated response:

- Increase monitoring frequency
- Pre-position recovery resources
- Alert on-call personnel
- Log elevated state

Agent impact:

- No immediate impact
- Increased gravity sensitivity
- More frequent Trust Proof refresh

## Level 2: Warning

Trigger conditions:

- R > 0.6 sustained for 10 minutes
- Multiple component degradation
- Failed recovery from Level 1
- Coordinated anomalies detected

Automated response:

- Activate secondary systems
- Reduce non-essential operations
- Escalate alerts
- Begin incident documentation

Agent impact:

- All agents experience G += 0.5
- High-risk actions restricted
- Trust Proof expiration shortened
- New agent genesis paused

## Level 3: Critical

Trigger conditions:

- R > 0.8 sustained for 5 minutes
- Oracle node failure (below quorum risk)
- Confirmed security incident
- Cascading failures detected

Automated response:

- Activate all redundancy
- Isolate affected components
- Page all on-call personnel
- Enable emergency logging

Agent impact:

- All agents demoted one tier
- Only essential actions permitted
- Trust Proof expiration: 5 seconds
- Inter-zone traffic restricted

## Level 4: Severe

Trigger conditions:

- Oracle quorum lost
- Mass agent compromise confirmed
- Zone boundary breach
- R approaching 1.0

Required response:

- Human authorization required in addition to the applicable ordinary or separately declared emergency authorization
- Emergency governance activated
- External notification (federation, regulators)
- Consider zone isolation

Agent impact:

- All agents restricted to Observer mode
- Read operations remain subject to valid ordinary authorization or an explicitly matched separate emergency capability
- Trust Proof issuance stops; existing proofs retain their original expiration
- Prepare for potential evacuation

## Level 5: Catastrophic

Trigger conditions:

- Oracle mesh completely failed
- Zone integrity compromised
- Uncontrolled cascade in progress
- No recovery path visible

Required response:

- Zone shutdown authorized
- Complete isolation
- External incident command
- Forensic preservation

Agent impact:

- All agent operations halted
- Zone evacuation initiated
- Trajectory records preserved
- Await recovery or dissolution

# Circuit Breakers

## Concept

Circuit breakers automatically disable functionality when failure thresholds are exceeded.  Like electrical circuit breakers, they prevent cascading failure.

~~~
   Normal Operation
         |
         v
   [Failure Counter]
         |
         | threshold exceeded
         v
   [Circuit OPEN] -----> Operations Blocked
         |
         | cooldown period
         v
   [Circuit HALF-OPEN] --> Test Operations
         |
         | success          | failure
         v                  v
   [Circuit CLOSED]    [Circuit OPEN]
         |
         v
   Normal Operation
~~~

## Circuit Types

~~~
+-------------+------------------------+----------------------------+
| Circuit     | Protects               | Trigger                    |
+-------------+------------------------+----------------------------+
| Consensus   | Oracle consensus       | Consensus failures > 3     |
|             |                        | consecutive                |
| Trajectory  | Transaction signing    | Signing failures > 5/sec   |
| Federation  | Cross-zone operations  | Federation errors > 10/min |
| Agent       | Agent operations       | Violations > threshold     |
| Action      |                        |                            |
+-------------+------------------------+----------------------------+
~~~

## Circuit Configuration

{ "circuit_breakers": { "trust_proof": { "failure_threshold": 10, "failure_window_seconds": 1, "cooldown_seconds": 30, "half_open_test_count": 3 }, "consensus": { "failure_threshold": 3, "failure_window_seconds": 60, "cooldown_seconds": 120, "half_open_test_count": 1 }, "trajectory": { "failure_threshold": 5, "failure_window_seconds": 1, "cooldown_seconds": 60, "half_open_test_count": 3 } } }

## Circuit States

~~~
+-----------+-----------------------------------------------------+
| State     | Behavior                                            |
+-----------+-----------------------------------------------------+
| CLOSED    | Normal operation, failures counted                  |
| OPEN      | Operations blocked, cooldown active                 |
| HALF-OPEN | Limited test operations permitted                   |
+-----------+-----------------------------------------------------+
~~~

## Agent-Specific Circuits

Individual agents have circuit breakers:

{ "agent_circuit": { "agent_id": "agent:independent:3gen:acme:abc123", "violation_threshold": 5, "violation_window_seconds": 300, "cooldown_seconds": 600, "current_state": "CLOSED", "violation_count": 2, "last_violation": "2025-12-03T14:30:00Z" } }

When an agent's circuit opens:

- Agent restricted to Observer mode
- Alert sent to sponsor
- Trajectory flagged for review
- Manual reset required after cooldown

# Graceful Degradation

## Degradation Ladder

As conditions worsen, capabilities reduce in order:

~~~
   Level 0: Full Operation
         |
         v (R > 0.3)
   Level 1: Elevated Monitoring
         |
         v (R > 0.5)
   Level 2: Reduced Throughput
         |
         v (R > 0.7)
   Level 3: Essential Only
         |
         v (R > 0.9)
   Level 4: Read Only
         |
         v (Oracle failure)
   Level 5: Preservation Mode
         |
         v (Zone failure)
   Level 6: Shutdown
~~~

## Degradation Actions

~~~
+-------+----------------------------------------------------------+
| Level | Disabled Capabilities                                    |
+-------+----------------------------------------------------------+
| 2     | New agent genesis, bulk operations                       |
| 3     | Tier promotions, high-risk actions                       |
| 4     | All write operations, agent mobility                     |
| 5     | All agent operations (preserve data)                     |
| 6     | All operations (orderly shutdown)                        |
+-------+----------------------------------------------------------+
~~~

## Capability Preservation Priority

When degrading, preserve in order:

1. Safety (always preserved)

~~~
    -  Zeroth Law enforcement
    -  Circuit breakers
    -  Audit logging
~~~

1. Integrity (authorization checks remain mandatory)

~~~
    -  Trajectory chain consistency
    -  Trust Proof validity
    -  Consensus integrity
~~~

Proof signature, original expiration, and the established signing quorum MUST NOT be relaxed to preserve availability. A cached read is still an action requiring authorization.

1. Availability (degrade first)

~~~
    -  New agent operations
    -  High-risk actions
    -  Non-essential features
~~~

## Degradation Communication

Agents MUST be informed of degraded state:

{ "zone_status": { "zone_id": "zone-blue-prod-01", "status": "DEGRADED", "degradation_level": 3, "disabled_capabilities": \[ "tier_promotion", "high_risk_actions", "new_genesis" ], "reason": "Elevated risk factor", "r_current": 0.75, "estimated_recovery": "2025-12-03T15:00:00Z", "agent_guidance": "Limit operations to essential only" } }

# Zone Collapse Protocol

## Definition

Zone collapse occurs when a zone can no longer maintain basic operations:

- Oracle mesh completely unavailable
- Zone integrity compromised beyond repair
- Uncontrolled cascade with no recovery path
- Governance decision to terminate zone

## Collapse Detection

Automatic collapse detection:

~~~
   IF oracle_quorum_available = false
      AND recovery_attempts > max_attempts
      AND time_since_quorum_loss > max_duration
   THEN TRIGGER zone_collapse_protocol
~~~

Manual collapse declaration:

- Zone administrator authorization (IAL3)
- Federation notification
- Regulatory notification if required

## Collapse Sequence

T+0: Collapse declared

- Zone status -> COLLAPSING
- All operations halted
- Federation notified
- External communication blocked

T+1min: Agent notification

- All agents notified of collapse
- Evacuation window opens
- Exit Attestations issued for eligible agents

T+5min: Trajectory preservation

- All trajectory chains exported
- Flight Recorder sealed
- Cryptographic hashes published

T+15min: Agent evacuation

- Agents may exit to federated zones
- Trust transfer with collapse attestation
- Agents without exit path -> frozen

T+30min: Zone isolation

- All external connections severed
- Zone boundary hardened
- Internal operations continue for preservation

T+60min: Final preservation

- Complete state snapshot
- Forensic package created
- Recovery point established

T+120min: Zone offline

- All systems shut down
- Zone status -> COLLAPSED
- Post-mortem begins

## Agent Evacuation

During collapse, agents can evacuate to federated zones:

{ "evacuation_attestation": { "attestation_type": "zone_collapse_evacuation", "origin_zone": "zone-blue-prod-01", "collapse_timestamp": "2025-12-03T14:00:00Z", "agent_id": "agent:independent:3gen:acme:abc123", "agent_state_at_collapse": { "e_base": 55, "trajectory_length": 4721, "lineage": "independent", "generation": 3 }, "trajectory_hash": "sha256:abc123...", "destination_zone": "zone-blue-prod-02", "transfer_terms": { "e_base_transferred": 44, "transfer_factor": 0.8, "collapse_penalty": 0.0 }, "signatures": { "origin_zone": "sig:zone-blue-prod-01:...", "destination_zone": "sig:zone-blue-prod-02:..." } } }

## Post-Collapse

After collapse:

- Trajectory data available via federation
- Forensic package available for analysis
- Zone may be re-established with new genesis
- Agents may return after re-establishment

# Mass Compromise Response

## Definition

Mass compromise occurs when:

- More than 10% of zone agents compromised
- Coordinated attack affecting multiple agents
- Systemic vulnerability exploitation
- Compromised sponsor affecting all sponsored agents

## Detection

Mass compromise indicators:

- Sudden trajectory divergence across agents
- Coordinated anomalous behavior
- Simultaneous constraint violations
- Common attack pattern detected

Detection threshold:

{ "mass_compromise_detection": { "compromised_agent_threshold_percent": 10, "coordinated_anomaly_threshold": 20, "trajectory_divergence_threshold": 0.5, "detection_window_seconds": 300 } }

## Response Protocol

T+0: Mass compromise detected

- Emergency Level 4 declared
- All agent operations paused
- Forensic capture initiated

T+1min: Triage

- Identify affected vs. unaffected agents
- Isolate affected agents
- Preserve affected trajectories

T+5min: Containment

- Affected agents quarantined
- Sponsorship chains reviewed
- Common attack vector identified

T+15min: Scope assessment

- Full impact determined
- Recovery options evaluated
- Communication to stakeholders

T+30min: Recovery decision

- Option A: Selective remediation
- Option B: Mass reset
- Option C: Zone collapse

T+60min+: Execute decision

- Implement chosen recovery path
- Monitor for recurrence
- Update defenses

## Quarantine Protocol

Compromised agents are quarantined:

{ "quarantine": { "agent_id": "agent:independent:3gen:acme:abc123", "quarantine_start": "2025-12-03T14:05:00Z", "reason": "mass_compromise_suspected", "evidence": \[ "trajectory_divergence: 0.7", "coordinated_anomaly: true", "attack_pattern_match: true" ], "quarantine_state": { "operations_permitted": "none", "monitoring_level": "maximum", "trajectory_frozen": true, "sponsor_notified": true }, "release_conditions": \[ "forensic_analysis_complete", "remediation_verified", "sponsor_authorization" ] } }

## Recovery Options

Option A: Selective Remediation

For limited compromise:

- Identify and quarantine affected agents
- Remediate root cause
- Verify agent integrity
- Gradual release from quarantine

Option B: Mass Reset

For widespread compromise:

- All affected agents reset to genesis
- E_base set to sponsored minimum
- Trajectory chains preserved but flagged
- Agents must re-earn trust

Option C: Zone Collapse

For unrecoverable compromise:

- Zone collapse protocol initiated
- All agents evacuated or frozen
- Zone re-established fresh
- New genesis ceremony required

# Oracle Failure Response

## Single Node Failure

Single node failure is routine:

Detection:  Heartbeat timeout (5 seconds)

Response:

1. Remove failed node from request routing without changing authenticated membership, quorum, or the fault budget
2. Redistribute load to remaining nodes
3. Alert operations
4. Begin node recovery

Recovery: Node rejoins only after its health check and the authenticated state, membership, and durable voting/lock recovery checks in `specifications/oracle-consensus.md`. An unavailable node is not automatically removed from the voting committee.

## Quorum Degradation

When nodes fail but quorum remains:

Detection: Fewer members are available, but the established consensus quorum and signing requirements remain achievable. In the default five-member mesh this requires four distinct eligible consensus participants.

Response:

1. Alert: quorum degraded
2. Retain the established consensus and signing requirements; do not reduce them during failure
3. Prioritize critical operations
4. Accelerate node recovery

Recovery:  Nodes rejoin, full quorum restored

## Quorum Loss

When the established quorum cannot be obtained (including unavailable or withholding members):

Detection:  Cannot achieve consensus

Response:

1. Emergency Level 4 declared
2. All write operations halted
3. Read operations from cache only while ordinarily authorized or explicitly permitted by a separately verified emergency capability
4. Human escalation required

Recovery:

- Option A: Restore nodes to regain quorum
- Option B: Evaluate already approved emergency capability through its independent verification path, without issuing ordinary proofs
- Option C: Zone collapse if unrecoverable

## Emergency Quorum

If normal quorum cannot be restored, an administrator MUST NOT create a reduced emergency quorum to issue ordinary Trust Proofs or amend emergency policy. The earlier single-administrator, two-node recipe is withdrawn.

The separate capability in specifications/emergency-capability.md MAY be activated only under its preinstalled policy. Its multiple-custodian signatures authorize the exact emergency activation; they are not a substitute Oracle quorum. If its independent checks cannot be completed, the action is denied.

# Recovery Procedures

## Recovery Phases

Phase 1: STABILIZE

- Stop bleeding (prevent further damage)
- Establish stable baseline
- Assess current state

Phase 2: ASSESS

- Full damage assessment
- Root cause identification
- Recovery options evaluation

Phase 3: PLAN

- Recovery plan development
- Resource allocation
- Timeline establishment

Phase 4: EXECUTE

- Systematic recovery execution
- Continuous monitoring
- Checkpoint verification

Phase 5: VERIFY

- Recovery completeness check
- Security verification
- Performance validation

Phase 6: NORMALIZE

- Return to normal operations
- Remove emergency measures
- Update documentation

## Recovery Checklist

Pre-recovery:

- \[ ] Emergency contained
- \[ ] Root cause identified
- \[ ] Recovery plan approved
- \[ ] Resources available
- \[ ] Stakeholders notified

During recovery:

- \[ ] Progress tracked
- \[ ] Checkpoints verified
- \[ ] Anomalies investigated
- \[ ] Documentation updated

Post-recovery:

- \[ ] Full functionality verified
- \[ ] Security posture confirmed
- \[ ] Performance acceptable
- \[ ] Monitoring normal
- \[ ] Post-incident review scheduled

## Recovery Verification

Before declaring recovery complete:

{ "recovery_verification": { "oracle_health": { "quorum_status": "full", "node_health": "all_healthy", "consensus_functioning": true }, "agent_health": { "agents_operational": 4721, "agents_quarantined": 0, "agents_evacuated": 0 }, "zone_health": { "r_current": 0.15, "degradation_level": 0, "circuits_open": 0 }, "security_posture": { "vulnerability_remediated": true, "monitoring_enhanced": true, "attack_vector_blocked": true }, "verification_timestamp": "2025-12-03T16:00:00Z", "verified_by": "admin:alice.smith" } }

# Post-Incident Analysis

## Requirements

Post-incident analysis is REQUIRED for:

- Any Level 3 or higher emergency
- Any zone collapse or near-collapse
- Any mass compromise
- Any Oracle quorum loss

## Analysis Framework

1. TIMELINE

~~~
    -  Minute-by-minute reconstruction
    -  Decision points identified
    -  Delays documented
~~~

1. ROOT CAUSE

~~~
    -  Technical cause
    -  Contributing factors
    -  Systemic issues
~~~

1. RESPONSE EVALUATION

~~~
    -  What worked well
    -  What didn't work
    -  Near misses
~~~

1. IMPACT ASSESSMENT

~~~
    -  Agents affected
    -  Trajectory impact
    -  Trust impact
    -  Business impact
~~~

1. LESSONS LEARNED

~~~
    -  What to improve
    -  What to add
    -  What to remove
~~~

1. ACTION ITEMS

~~~
    -  Specific improvements
    -  Owners assigned
    -  Deadlines set
~~~

## Post-Incident Report

{ "incident_report": { "incident_id": "INC-2025-12-03-001", "zone_id": "zone-blue-prod-01", "severity": "Level 3 - Critical", "duration_minutes": 47, "summary": "Oracle node failure led to temporary quorum degradation", "timeline": \[ { "timestamp": "2025-12-03T14:00:00Z", "event": "Oracle node 3 unresponsive" }, { "timestamp": "2025-12-03T14:00:05Z", "event": "Node removed from routing; authenticated committee and quorum retained" } ], "root_cause": { "primary": "Hardware failure in Oracle node 3", "contributing": \[ "Delayed hardware replacement", "Insufficient geographic distribution" ] }, "impact": { "agents_affected": 127, "operations_delayed": 4721, "trust_impact": "minimal" }, "response_evaluation": { "effective": \[ "Automatic failover functioned correctly", "Agent communication timely" ], "needs_improvement": \[ "Recovery time exceeded target", "Alert routing delayed" ] }, "action_items": \[ { "action": "Review a sixth Oracle member and, if supported, install through the authenticated joint transition", "owner": "infrastructure_team", "deadline": "2025-12-15" }, { "action": "Improve alert routing", "owner": "operations_team", "deadline": "2025-12-10" } ], "report_author": "admin:bob.jones", "report_date": "2025-12-04" } }

# Communication During Emergencies

## Internal Communication

~~~
+------------+---------------+-----------------------------------+
| Audience   | Channel       | Content                           |
+------------+---------------+-----------------------------------+
| Management | Email/Call    | Impact and timeline               |
| Engineers  | Chat/Bridge   | Technical coordination            |
| All Staff  | Broadcast     | Status and guidance               |
+------------+---------------+-----------------------------------+
~~~

## External Communication

~~~
+------------+---------------------+------------------------------+
| Audience   | Channel             | Content                      |
+------------+---------------------+------------------------------+
| Regulators | Formal notification | Compliance-relevant details  |
| Agents     | Zone status API     | Operational guidance         |
| Sponsors   | Direct notification | Agent status                 |
+------------+---------------------+------------------------------+
~~~

## Communication Templates

Emergency declaration:

~~~
   EMERGENCY DECLARED - [Zone ID]
   Level: [1-5]
   Time: [timestamp]
   Status: [brief description]
   Agent Impact: [current restrictions]
   Estimated Recovery: [time or "assessing"]
   Next Update: [time]
~~~

Status update:

~~~
   STATUS UPDATE - [Zone ID] - [Update #]
   Level: [current level]
   Progress: [recovery status]
   Changes: [what's changed]
   Agent Impact: [current restrictions]
   Next Update: [time]
~~~

Recovery announcement:

~~~
   RECOVERY COMPLETE - [Zone ID]
   Duration: [total time]
   Final Status: Normal operations resumed
   Remaining Actions: [any ongoing items]
   Post-Incident Review: [scheduled date]
~~~

# Security Considerations

## Emergency Protocol Security

Emergency procedures themselves must be secured:

- Emergency credentials stored separately
- Break-glass procedures audited
- Emergency access time-limited
- All emergency actions logged

## Attack During Emergency

Attackers may exploit emergencies:

- Increased monitoring during emergencies
- No security shortcuts during recovery
- Verify identity of "helpers"
- Assume compromise until verified

## Emergency Credential Management

Emergency credentials MUST follow specifications/emergency-capability.md. Activation requires at least two independent custodians from an established roster of at least three, lasts no more than four hours, and cannot automatically renew. Scope and budgets are fixed by the approved policy; repeated activation cannot reset them during the same incident.

Changing or installing that policy requires at least 90% approval from the established full governing custodian body, 90 days of review, 14 further days of ratification, and independent external review. The same controls protect changes to custodians, keys, verifier configuration, and the amendment rules. No outage waiver exists. Authenticated suspension or revocation is immediate; restoration requires a new approved version through the protected process in normal operation.

# IANA Considerations

This document has no IANA actions.

--- back

# Emergency Runbooks

Detailed step-by-step procedures for common emergencies.

Runbook: Oracle Node Failure

Runbook: Quorum Loss

Runbook: Mass Agent Compromise

Runbook: Zone Collapse

# Communication Templates

Complete templates for emergency communications.

# Recovery Checklists

Detailed checklists for recovery procedures.

Acknowledgments

Emergency response procedures draw on incident management best practices from SRE, NIST, and operational experience with distributed systems.
