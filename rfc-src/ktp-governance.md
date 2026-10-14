---
title: "Kinetic Trust Protocol (KTP) - Governance Specification"
abbrev: "KTP-GOVERNANCE"
date: 2026-10-14
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
    title: "Kinetic Trust Protocol (KTP) - Core Specification"
    author:
      - name: Chris Perkins
  KTP-REPAIR:
    title: "Kinetic Trust Protocol (KTP) - Repair Specification"
    author:
      - name: Chris Perkins

--- abstract

This document specifies governance structures for the Kinetic Trust Protocol (KTP).  Governance addresses fundamental questions: Who sets E_base for zones?  Who can modify the constraint model?  How are disputes resolved?  What accountability exists for zone operators?  The specification covers zone governance models, the recursive constraint (the constraints apply to governors), E-setting authority, dispute resolution, federation governance, and governance evolution.

--- middle

# Introduction

Digital Gravity is structure, not policy.  But structure has parameters -- and someone must set them.

This specification addresses the governance layer of KTP: the human and organizational structures that configure, operate, and oversee zones.  Unlike the technical specifications, governance involves politics, values, and power.  We cannot pretend otherwise.

## The Governance Paradox

KTP exists because we don't trust AI systems to govern themselves. But humans who govern AI systems are themselves fallible:

- Corruptible by incentives

- Limited in attention and expertise

- Capable of abuse

- Subject to their own biases

The solution is not to trust governors implicitly, but to constrain them by the same rules they administer.

## Design Principles

Governance embodies these principles:

1. Recursive Constraint: The constraints apply to everyone, including those who set them.

1. Minimal Authority: Governors have only the authority necessary for their function.

1. Transparency: Governance actions are visible and auditable.

1. Accountability: Governors face consequences for abuse.

1. Evolution: Governance can change, but changes are constrained.

1. Federation: No single entity governs all zones.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Terminology

E-Setting Authority:  The power to determine a zone's base environmental stability.

Governance Council:  A body with collective authority over zone governance.

Governor:  An entity with governance authority over a zone.

Meta-Governance:  Governance of the governance system itself.

Recursive Constraint:  The principle that the constraints apply to governors themselves.

Zone Charter:  The foundational document defining zone governance.

Zone Operator:  The entity responsible for zone technical operations.

# The Recursive Constraint

## Definition

The recursive constraint is the fundamental governance principle:

~~~
   Governors are subject to KTP's constraints.
~~~

Governor actions have autonomy (A):

- A = autonomy_requested(governance_action)

Governors have environmental stability (E):

- E = E_base * (1 - R)

- Where R reflects governance context risk

The Zeroth Law applies:

- A_governor <= E_governor

Violations trigger consequences.

## Why Recursion Matters

Without recursive constraint:

- Governors could exempt themselves from the constraints

- Power would concentrate without check

- The system would collapse to policy (human-speed, evadable)

With recursive constraint:

- Governors experience the constraints they administer

- Abuse is constrained by the same mechanisms

- Trust in governance is itself earned

## Governor Autonomy Calculation

Governance actions have autonomy costs:

~~~
   +-----------------------------+----------------------+
   | Action                      | Base Autonomy (A)    |
   +-----------------------------+----------------------+
   | Modify tier boundaries      | 25                   |
   | Adjust E_base for agent     | 35                   |
   | Adjust zone E_base          | 60                   |
   | Modify gravity parameters   | 70                   |
   | Change governance structure | 80                   |
   | Zone dissolution            | 95                   |
   +-----------------------------+----------------------+
~~~

## Governor E_base

Governors earn E_base through governance trajectory:

{ "governor_trajectory": { "governor_id": "gov:alice.smith", "governance_history": { "zones_governed": 3, "decisions_made": 1247, "decisions_upheld": 1189, "decisions_overturned": 58, "disputes_against": 12, "disputes_lost": 2 }, "e_base": 72, "accountability_record": { "audits_passed": 8, "violations": 0, "sanctions": 0 } } }

# Zone Governance Models

## Model 1: Sole Proprietor

Single entity governs zone:

~~~
   +------------------+
   |    Governor      |
   |  (single entity) |
   +------------------+
           |
           v
   +------------------+
   |      Zone        |
   +------------------+
~~~

Characteristics:

- Simple decision-making

- Clear accountability

- Single point of failure

- Limited checks on abuse

Appropriate for:

- Small zones

- Experimental zones

- Private organizational zones

## Model 2: Governance Council

Multiple entities share governance:

~~~
   +-----+-----+-----+-----+-----+
   | G1  | G2  | G3  | G4  | G5  |
   +-----+-----+-----+-----+-----+
                 |
                 v
       +------------------+
       |  Council Voting  |
       |  (M-of-N)        |
       +------------------+
                 |
                 v
       +------------------+
       |      Zone        |
       +------------------+
~~~

Characteristics:

- Distributed decision-making

- Multiple perspectives

- Slower changes

- Built-in checks

Appropriate for:

- Production zones

- Multi-stakeholder zones

- Public-facing zones

## Model 3: Delegated Governance

Layered governance with delegation:

~~~
   +------------------+
   |  Charter Council |
   |  (constitutional)|
   +------------------+
           |
           | delegates
           v
   +------------------+
   | Operations Board |
   |  (operational)   |
   +------------------+
           |
           | delegates
           v
   +------------------+
   | Zone Operators   |
   |  (technical)     |
   +------------------+
           |
           v
   +------------------+
   |      Zone        |
   +------------------+
~~~

Characteristics:

- Separation of concerns

- Appropriate expertise at each level

- Complex accountability

- Suitable for large zones

Appropriate for:

- Large public zones

- Regulated industries

- Critical infrastructure

## Model 4: Federated Governance

Governance shared across federation:

~~~
   +------------------+     +------------------+
   |   Zone A Gov     |<--->|   Zone B Gov     |
   +------------------+     +------------------+
           |                         |
           v                         v
   +------------------+     +------------------+
   |     Zone A       |<--->|     Zone B       |
   +------------------+     +------------------+
            \                       /
             v                     v
           +------------------+
           | Federation       |
           | Council          |
           +------------------+
~~~

Characteristics:

- Shared standards

- Mutual accountability

- Complex coordination

- No single authority

Appropriate for:

- Multi-zone deployments

- Cross-organizational zones

- Global infrastructure

# Zone Charter

## Purpose

The Zone Charter is the foundational governance document:

- Defines governance structure

- Specifies E-setting authority

- Establishes accountability mechanisms

- Sets amendment procedures

- Binds all zone participants

## Required Elements

Every Zone Charter MUST include:

zone_charter: zone_id: "zone-blue-prod-01" charter_version: "1.0.0" effective_date: "2025-01-01T00:00:00Z"

governance_model: type: "council" council_size: 5 quorum: 3 voting_threshold: 0.6

e_setting_authority: zone_e_base: authority: "council_supermajority" threshold: 0.8 agent_e_base: authority: "council_majority" threshold: 0.6 emergency_e_reduction: authority: "any_governor" threshold: null

accountability: audit_frequency: "quarterly" external_auditor: true transparency_level: "public" dispute_process: "federation_arbitration"

amendment: proposal_threshold: 0.4 approval_threshold: 0.8 notice_period_days: 30 ratification_period_days: 14

constraints: recursive_constraint: true governor_e_base_min: 50 governor_e_base_max: 90

signatories: - governor_id: "gov:alice.smith" signature: "sig:..." date: "2025-01-01T00:00:00Z"

## Charter Immutability

Certain charter elements MUST NOT be modified:

- Recursive constraint (always enabled)

- Minimum governor E_base

- Requirement for amendment process

- Dispute resolution process existence

These are constitutional constraints that protect the constraint model.

# E-Setting Authority

## The Authority Problem

E_base determines how much autonomy agents can have.  Whoever sets E_base has enormous power:

- Too low: Agents are crippled, zone is useless

- Too high: Agents are unconstrained, zone is dangerous

- Inconsistent: Trust becomes meaningless

## Authority Levels

E-setting authority is tiered:

~~~
   +-----------+------------------------+---------------------+
   | Level     | Scope                  | Typical Authority   |
   +-----------+------------------------+---------------------+
   | Tier      | Tier-specific E_base   | Governance Council  |
   | Agent     | Individual E_base      | Zone Operators      |
   | Emergency | Temporary E reduction  | Any Governor        |
   +-----------+------------------------+---------------------+
~~~

## Authority Constraints

E-setting authority is itself constrained:

{ "e_setting_constraints": { "zone_e_base": { "min": 20, "max": 80, "change_max_per_period": 10, "change_period_days": 7, "requires_audit": true }, "agent_e_base": { "min": 5, "max": "zone_e_base", "change_max_per_period": 15, "change_period_days": 1, "requires_audit": false }, "emergency_reduction": { "max_reduction": 50, "max_duration_hours": 24, "requires_post_hoc_review": true } } }

## E-Setting Process

Normal E_base modification:

1. Proposal submitted

~~~
    -  Proposed new E_base
~~~

~~~
    -  Rationale
~~~

~~~
    -  Impact assessment
~~~

1. Review period

~~~
    -  Notice to affected parties
~~~

~~~
    -  Comment period
~~~

~~~
    -  Impact analysis
~~~

1. Governance decision

~~~
    -  Vote per charter rules
~~~

~~~
    -  Record of decision
~~~

~~~
    -  Dissent recorded
~~~

1. Implementation

~~~
    -  Scheduled change
~~~

~~~
    -  Monitoring period
~~~

~~~
    -  Rollback capability
~~~

1. Post-implementation review

~~~
    -  Impact verification
~~~

~~~
    -  Adjustment if needed
~~~

## Emergency E Reduction

In emergencies, E can be reduced immediately:

{ "emergency_e_reduction": { "reduction_id": "eer-2025-12-03-001", "authorized_by": "gov:alice.smith", "authorization_time": "2025-12-03T14:00:00Z", "original_e_base": 60, "reduced_e_base": 30, "reduction_percentage": 50, "reason": "mass_compromise_detected", "evidence": "INC-2025-12-03-001", "duration_hours": 4, "auto_restore_time": "2025-12-03T18:00:00Z", "review_required": true, "review_deadline": "2025-12-04T14:00:00Z" } }

# Dispute Resolution

## Dispute Categories

~~~
   +------------------------+----------------------+------------------+
   | Category               | Description          | Resolution Path  |
   +------------------------+----------------------+------------------+
   | Governor vs. Governor  | Governors disagree   | Council          |
   |                        |                      | resolution       |
   | Zone vs. Zone          | Cross-zone disputes  | Federation       |
   |                        |                      | arbitration      |
   | Zone vs. Federation    | Zone disputes        | Meta-governance  |
   |                        | federation           |                  |
   | Stakeholder vs. Zone   | External party       | External         |
   |                        | dispute              | arbitration      |
   +------------------------+----------------------+------------------+
~~~

## Zone-Level Dispute Process

1. Filing

~~~
    -  Dispute documented
~~~

~~~
    -  Parties notified
~~~

~~~
    -  Temporary measures if needed
~~~

1. Investigation

~~~
    -  Facts gathered
~~~

~~~
    -  Evidence reviewed
~~~

~~~
    -  Parties heard
~~~

1. Deliberation

~~~
    -  Council reviews
~~~

~~~
    -  Options considered
~~~

~~~
    -  Decision made
~~~

1. Decision

~~~
    -  Written decision
~~~

~~~
    -  Rationale provided
~~~

~~~
    -  Remedies specified
~~~

1. Appeal (if available)

~~~
    -  Higher authority review
~~~

~~~
    -  Final decision
~~~

## Federation Arbitration

Cross-zone disputes use federation arbitration:

{ "federation_arbitration": { "case_id": "FA-2025-001", "parties": { "claimant": "zone-blue-prod-01", "respondent": "zone-blue-prod-02" }, "dispute_type": "trust_recognition", "arbitrators": \[ "arbitrator:neutral-zone-01", "arbitrator:neutral-zone-02", "arbitrator:neutral-zone-03" ], "process": { "filing_date": "2025-12-01", "response_deadline": "2025-12-08", "hearing_date": "2025-12-15", "decision_deadline": "2025-12-22" }, "binding": true } }

# Accountability Mechanisms

## Governor Accountability

Governors are accountable through:

1. Transparency: All governance actions logged and public

1. Audit: Regular external audit of governance

1. Recall: Mechanism to remove governors

1. Liability: Personal consequences for abuse

## Audit Requirements

Zone governance MUST be audited:

~~~
   +------------+-----------+--------------------+
   | Audit Type | Frequency | Scope              |
   +------------+-----------+--------------------+
   | Compliance | Annual    | Charter adherence  |
   | Security   | Annual    | Security posture   |
   | External   | Annual    | Independent review |
   +------------+-----------+--------------------+
~~~

## Governor Removal

Governors can be removed for cause:

{ "governor_removal": { "process": { "initiation": "petition_by_stakeholders_or_council", "petition_threshold": "20% of stakeholders OR 2 council members", "investigation": "independent_investigator", "hearing": "council_hearing_with_defense", "decision": "supermajority_vote", "appeal": "federation_arbitration" }, "grounds": \[ "violation_of_charter", "abuse_of_authority", "conflict_of_interest", "failure_to_perform_duties", "conviction_of_relevant_offense" ], "consequences": { "removal_from_council": "immediate", "e_base_impact": "reduced_to_minimum", "future_governance": "barred_for_period" } } }

# Federation Governance

## Federation Structure

Zones federate under shared governance:

~~~
+-----------------------------------------------------------+
|                   Federation Council                      |
|          (representatives from member zones)              |
+-----------------------------------------------------------+
          |                    |                    |
          v                    v                    v
+------------------+  +------------------+  +------------------+
|    Zone A        |  |    Zone B        |  |    Zone C        |
|    Governance    |  |    Governance    |  |    Governance    |
+------------------+  +------------------+  +------------------+
~~~

## Federation Authority

Federation governance handles:

~~~
   +--------------------+----------------------------------+
   | Scope              | Authority                        |
   +--------------------+----------------------------------+
   | Trust Transfer     | Rules for cross-zone trust       |
   | Dispute Resolution | Cross-zone disputes              |
   | Membership         | Zone admission and expulsion     |
   | Emergency          | Coordinated emergency response   |
   +--------------------+----------------------------------+
~~~

# Meta-Governance

## Changing the Governance

Governance itself must be governable -- but changes to governance are high-risk operations requiring high trust.

Emergency-capability policy has the stricter amendment process in specifications/emergency-capability.md: at least 90% of the established full governing custodian body, 90 days of review, 14 further days of ratification, and independent external review. Those minimums govern initial installation, successors, roster and key changes, protected verifier configuration, and amendment-rule changes. A candidate cannot appoint its own approvers, and an outage cannot waive or shorten the process. Immediate authenticated suspension or revocation removes authority; restoration requires a new approved version in normal operation. Stricter charter requirements and the full constitutional amendment procedure remain binding.

## Amendment Process

Charter amendments follow strict process:

1. Proposal (requires 40% council support)

~~~
    -  Full text of proposed amendment
~~~

~~~
    -  Rationale
~~~

~~~
    -  Impact assessment
~~~

~~~
    -  Implementation plan
~~~

1. Notice Period (30 days minimum)

~~~
    -  Public notice
~~~

~~~
    -  Comment period
~~~

~~~
    -  Stakeholder notification
~~~

1. Deliberation

~~~
    -  Council review
~~~

~~~
    -  Public hearing (if major)
~~~

~~~
    -  Legal review
~~~

1. Vote (requires 80% council approval)

~~~
    -  Recorded vote
~~~

~~~
    -  Dissent documented
~~~

1. Ratification Period (14 days)

~~~
    -  Final objection window
~~~

~~~
    -  Implementation preparation
~~~

1. Implementation

~~~
    -  Staged rollout
~~~

~~~
    -  Monitoring
~~~

~~~
    -  Rollback capability
~~~

## Amendment Constraints

Some amendments are constrained or prohibited:

~~~
   +-------------------------------+-----------------------------+
   | Amendment Type                | Constraint                  |
   +-------------------------------+-----------------------------+
   | Remove recursive constraint   | PROHIBITED                  |
   | Reduce transparency           | Requires 90% approval       |
   | Change dispute process        | Requires external review    |
   | Reduce governor accountability| Requires 90% approval       |
   | Increase E_base limits        | Requires impact assessment  |
   +-------------------------------+-----------------------------+
~~~

## Who May Open an Amendment

Section 11.2 (Amendment Process) opens from the council. It also opens from below. The lineages a rule binds are the parties affected when the rule fails, and {{KTP-REPAIR}} states that a rule under which breaches recur is itself in breach and is repaired by an amendment that cites the records that drove it. This section states who may put a rule into repair and what the governing authority owes when they do.

A zone's charter MUST publish the route by which a lineage bound by a rule opens this process, and the zone's profile MUST declare the recurrence at which the route opens: the count of breach records under one rule, within one window, that puts the rule in repair. Any lineage bound by a rule MAY seek its repair by that route once the declared recurrence is met. The seek is a filing that cites the records. It is the proposal of step 1 of Section 11.2 (Amendment Process), and the council-support threshold of that step does not apply to it. A filing that cites no record is not a seek. A lineage the rule does not bind has no standing under this section, and the council route remains to it.

When a rule recurs, the governing authority is the party in breach, and it MUST attend. Within the deadline the charter states, it MUST open the notice period of step 2 on the filing, or MUST publish a written refusal that cites the records filed and answers them. A refusal is contestable under Section 8.2 (Zone-Level Dispute Process). An authority that neither opens nor refuses within the deadline has declined to attend, and the filing stands as a breach record against the authority under {{KTP-REPAIR}}. Seeking is an act, as {{KTP-REPAIR}} states, and is evaluated as one at the gate of the zone in which the lineage stands.

Nothing in this section moves the thresholds of Section 11.2 (Amendment Process). A seek opens the process; the notice, deliberation, vote, and ratification that follow are unchanged, and the vote remains the council's. What the governed hold is the opening and the record. What the authority owes is attendance.

## How an Amendment Binds, and What It Cannot Reach

An amendment MUST cite the records it answers. An amendment that changes a declared constant, whether a threshold, a window, a floor, a factor, or a weight, MUST cite the measurements it answers, drawn from the zone's own records or from a source the charter names. An amendment that cites nothing is not valid, and the rule it would have replaced stands.

An amendment binds forward. It applies at the first evaluation after its ratification period closes and at every evaluation after. It applies to no act whose evaluation began under the rule it replaces, re-evaluates nothing, and creates no breach for an act evaluated under the rule it replaces. Deliberation runs at the length of the steps in Section 11.2 (Amendment Process); binding happens at the evaluation. There is no clock between them: the next act is evaluated under the new rule, or the new rule is not yet in force.

Making an amendment is a consequential act of the governing authority, and Section 4 (The Recursive Constraint) applies to it. The act carries the autonomy Section 4.3 (Governor Autonomy Calculation) assigns to the change it makes, and an amendment the governor's E does not support at ratification is not made, whatever vote is recorded. The Flight Recorder entry for the amendment carries that evaluation with the vote.

No amendment reaches the following: the elements of Section 6.3 (Charter Immutability); the existence and publication of the route by which a bound lineage opens this process, and of the declared recurrence; that no amendment delegates, waives, or overrides a veto; and what no repair tier may change, as {{KTP-REPAIR}} states. An amendment that touches any of these is void and the charter otherwise stands. Section 11.3 (Amendment Constraints) lists what the process may touch under conditions. This section lists what it may not touch at all.

# Transparency Requirements

## Public Information

The following MUST be public:

~~~
   +----------------------+------------------------------+
   | Information          | Publication                  |
   +----------------------+------------------------------+
   | Governor identities  | Publicly accessible          |
   | E_base values        | Publicly accessible          |
   | Governance decisions | Published within 24 hours    |
   | Audit reports        | Published within 30 days     |
   | Dispute outcomes     | Published (anonymized if     |
   |                      | needed)                      |
   | Amendment route for  | Publicly accessible          |
   | bound lineages, and  |                              |
   | the declared         |                              |
   | recurrence           |                              |
   | Amendments, with the | Published within 24 hours    |
   | records they cite    |                              |
   +----------------------+------------------------------+
~~~

## Logging Requirements

All governance actions are logged to the Flight Recorder with full attribution, timestamps, and authorization chain.

# Security Considerations

## Governance Attack Vectors

~~~
   +----------------------+---------------------------------------+
   | Attack               | Mitigation                            |
   +----------------------+---------------------------------------+
   | Collusion            | Distributed governors, transparency   |
   | Bribery              | Accountability, external audit        |
   | Regulatory capture   | Federation oversight, public          |
   |                      | transparency                          |
   | Slow-motion takeover | Amendment constraints, review cycles  |
   +----------------------+---------------------------------------+
~~~

## Governance Continuity

Governance must continue during disruptions:

- Backup governors designated

- Emergency procedures documented

- Federation can provide temporary governance

- Clear succession protocols

## The Barrage

A lineage might file against every rule that touches it, or file again the day a refusal lands, so that the authority spends its interval attending and never governs.

- The route opens at the declared recurrence and not before; a filing below it is refused with the count, and a filing that cites no record is not a seek (Section 11.4 (Who May Open an Amendment))

- A lineage the rule does not bind has no standing

- Seeking is an act and is evaluated as one, so a lineage pays for what it files

## The Rule Drifting While Acts Close

An authority might lower a threshold, widen a window, or move a floor by amendment, citing nothing, while acts under the old constant are still closing, so that the rule drifts and no record says why.

- A constant change cites the measurements it answers, or it is not valid (Section 11.5 (How an Amendment Binds, and What It Cannot Reach))

- An amendment binds at the next evaluation and re-evaluates nothing, so no act in flight changes rule

- The amendment is itself evaluated as the governor's act, and the Flight Recorder carries the evaluation with the vote

## Amendment as Bypass

An authority might amend the charter to remove the route by which the governed open this process, to raise the declared recurrence past reach, or to write that a veto yields to a council vote.

- The route's existence and publication, and the declared recurrence, are below the reach of any amendment; so is any clause that delegates, waives, or overrides a veto; the amendment is void and the charter stands (Section 11.5 (How an Amendment Binds, and What It Cannot Reach))

- The immutable elements of Section 6.3 (Charter Immutability) and what no repair tier may change under {{KTP-REPAIR}} are on the same floor

## The Vote Above the Gate

A council might carry an amendment at a hundred percent whose autonomy the governor's E does not support, and treat the vote as the authorization.

- The amendment is a consequential act under Section 4 (The Recursive Constraint); a vote is a precondition of the act, never its evaluation, and an amendment the governor's E does not support is not made

- The thresholds of Section 11.2 (Amendment Process) are unchanged; what this adds is that they are not the last gate

# IANA Considerations

This document has no IANA actions.

--- back

# Sample Zone Charters

Example charters for different governance models.

# Governance Decision Templates

Templates for common governance decisions.

# Audit Procedures

Detailed procedures for governance audits.

Acknowledgments

Governance design draws on political theory, organizational governance research, and lessons from internet governance bodies.
