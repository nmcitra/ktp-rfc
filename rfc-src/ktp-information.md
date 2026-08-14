---
title: "Kinetic Trust Protocol (KTP) - Information Environment Specification"
abbrev: "KTP-INFORMATION"
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

This document specifies the Signal Environment layer of the Kinetic Trust Protocol (KTP). The Information domain measures the epistemic health of the information environment—noise levels, truth conditions, manipulation indicators, and collective sensemaking capacity. This specification operationalizes these measurements into actionable risk factors that affect Digital Gravity, enabling agents to operate more cautiously in polluted information environments.

--- middle

# Introduction

Agents do not operate in informational vacuums. They swim in oceans of signal—some clear, some murky, some actively poisoned. An agent making decisions in a high-misinformation environment faces different risks than one operating in a well-curated knowledge base.

The Information domain captures this epistemic context. This specification operationalizes those measurements into protocols for:

- Detecting information environment degradation
- Adjusting agent autonomy based on epistemic conditions
- Maintaining sensemaking capacity under attack
- Recovering from information operations

# Design Principles

Signal environment management embodies these principles:

1. Epistemic Humility: In uncertain environments, reduce autonomy.

1. Source Quality: Not all information is equal. Source matters.

1. Collective Sensemaking: Individual agents cannot verify everything. Collective capacity matters.

1. Resistance to Manipulation: Designed to resist information operations.

1. Degradation Detection: Recognize when environment is degrading.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Information Domain Overview

## The 336 Signals

The Information domain comprises 17 major groups:

~~~
+------------------------+------------+------------------------------+
| Group                  | Dimensions | Purpose                      |
+------------------------+------------+------------------------------+
| Attention Currents     | 22         | What's capturing attention   |
| Narrative Currents     | 26         | Dominant stories flowing     |
| Source Ecosystem       | 24         | Quality of information       |
|                        |            | sources                      |
| Amplification Patterns | 20         | How information spreads      |
| Synthetic Content      | 22         | AI-generated content         |
|                        |            | detection                    |
| Truth Conditions       | 28         | Verifiability and accuracy   |
| Emotional Weather      | 24         | Collective emotional state   |
| Tribal Dynamics        | 18         | Group identity effects       |
| Platform Dynamics      | 16         | Platform-specific patterns   |
| Information Operations | 24         | Active manipulation          |
|                        |            | detection                    |
| Temporal Patterns      | 20         | How signal changes over time |
| Epistemic              | 22         | Fact-checking, verification  |
| Infrastructure         |            | capacity                     |
| Sensemaking Capacity   | 26         | Collective ability to        |
|                        |            | understand                   |
| Signal Integrity       | 20         | Overall environment health   |
| Collective Trauma      | 14         | Shared traumatic content     |
| Sacred/Meaning         | 14         | Meaning-making dimensions    |
+------------------------+------------+------------------------------+
~~~

## Truth Conditions (28 Dimensions)

These dimensions measure epistemic quality:

~~~
+---------------------------+------------------------------+-------+
| Dimension                 | Description                  | Scale |
+---------------------------+------------------------------+-------+
| verified_claim_rate       | Claims actually verified     | 0-1   |
| fact_check_coverage       | How much content is          | 0-1   |
|                           | fact-checked                 |       |
| misinformation_volume     | Volume of false information  | 0-1   |
| disinformation_volume     | Volume of intentional        | 0-1   |
|                           | falsehood                    |       |
| epistemic_pollution       | Overall truth environment    | 0-1   |
| citation_rate             | How often claims cite        | 0-1   |
|                           | sources                      |       |
| citation_quality          | Quality of cited sources     | 0-1   |
| primary_source_rate       | Use of primary vs secondary  | 0-1   |
| correction_rate           | How often errors corrected   | 0-1   |
| correction_visibility     | Are corrections seen?        | 0-1   |
| retraction_rate           | Formal retractions           | 0-1   |
| consensus_level           | Expert consensus available   | 0-1   |
| consensus_clarity         | Is consensus clear?          | 0-1   |
| evidence_quality          | Quality of supporting        | 0-1   |
|                           | evidence                     |       |
| evidence_accessibility    | Can evidence be accessed?    | 0-1   |
| logical_consistency       | Internal consistency         | 0-1   |
| temporal_consistency      | Consistency over time        | 0-1   |
| cross_source_consistency  | Agreement across sources     | 0-1   |
| nuance_preservation       | Is nuance maintained?        | 0-1   |
| context_preservation      | Is context maintained?       | 0-1   |
| manipulation_resistance   | Resistance to manipulation   | 0-1   |
| deepfake_prevalence       | Synthetic media presence     | 0-1   |
| attribution_clarity       | Can sources be attributed?   | 0-1   |
| provenance_available      | Is content provenance known? | 0-1   |
| edit_history_available    | Can changes be tracked?      | 0-1   |
| expert_accessibility      | Can experts be consulted?    | 0-1   |
| uncertainty_acknowledged  | Is uncertainty stated?       | 0-1   |
+---------------------------+------------------------------+-------+
~~~

# Epistemic Health Score

## Calculation

Overall epistemic health is calculated:

epistemic_health = weighted_aggregate( truth_conditions × 0.25, source_ecosystem × 0.20, sensemaking_capacity × 0.20, manipulation_resistance × 0.15, signal_integrity × 0.10, noise_floor_inverse × 0.10 )

## Health Levels

~~~
+-----------+-----------+---------------------+--------------------+
| Level     | Score     | Description         | Agent Response     |
+-----------+-----------+---------------------+--------------------+
| Healthy   | 0.7 - 0.9 | Good environment    | Normal operation   |
| Degraded  | 0.5 - 0.7 | Some pollution      | Increased caution  |
| Polluted  | 0.3 - 0.5 | Significant         | Reduced autonomy   |
|           |           | problems            |                    |
| Toxic     | 0.1 - 0.3 | Severe pollution    | Minimal autonomy   |
| Collapsed | 0.0 - 0.1 | Epistemic failure   | Read-only mode     |
+-----------+-----------+---------------------+--------------------+
~~~

# Information Operations Detection

## Attack Vectors

~~~
+----------------------+------------------------+--------------------+
| Vector               | Indicators             | Detection Method   |
+----------------------+------------------------+--------------------+
| Astroturfing         | Artificial grassroots  | Account age,       |
|                      |                        | activity patterns  |
| Disinformation       | False narratives at    | Content analysis,  |
| Campaigns            | scale                  | fact-checking      |
| Deepfakes            | Synthetic media        | Detection          |
|                      |                        | algorithms         |
| Narrative Flooding   | Volume overwhelming    | Rate analysis      |
|                      | signal                 |                    |
| Source Poisoning     | Compromised trusted    | Provenance         |
|                      | sources                | verification       |
| Context Collapse     | Removing context       | Context            |
|                      |                        | preservation       |
|                      |                        | checks             |
+----------------------+------------------------+--------------------+
~~~

## Detection Metrics

{ "info_ops_detection": { "coordinated_activity": { "detected": true, "confidence": 0.85, "scope": "moderate", "sources_affected": 47 }, "synthetic_content": { "prevalence": 0.12, "detection_confidence": 0.78, "types": \["text", "image"] }, "narrative_manipulation": { "detected": true, "narratives_affected": 3, "manipulation_type": "framing" }, "overall_threat_level": "elevated" } }

## Response Protocol

When information operations detected:

Level 1: MONITOR

- Increase measurement frequency
- Flag affected content
- Log patterns

Level 2: ALERT

- Notify zone governance
- Increase agent caution
- Activate verification requirements

Level 3: DEFEND

- Reduce agent autonomy
- Require human verification
- Isolate affected information streams

Level 4: QUARANTINE

- Block affected sources
- Agents to read-only
- Await human intervention

# Source Quality Assessment

## Source Categories

~~~
+--------------------+----------------+----------------------+
| Category           | Trust Baseline | Verification Required|
+--------------------+----------------+----------------------+
| Peer-Reviewed      | High           | Low                  |
| Institutional      | Medium-High    | Medium               |
| Quality Journalism | Medium         | Medium               |
| Aggregators        | Medium-Low     | High                 |
| Social Media       | Low            | Very High            |
| Anonymous          | Very Low       | Maximum              |
| Known Bad Actors   | None           | Rejected             |
+--------------------+----------------+----------------------+
~~~

## Source Scoring

{ "source_assessment": { "source_id": "source:reuters.com", "category": "quality_journalism", "scores": { "accuracy_history": 0.94, "correction_transparency": 0.91, "methodology_clarity": 0.85, "editorial_independence": 0.88, "expertise_depth": 0.82 }, "composite_score": 0.88, "trust_level": "high", "verification_required": "standard" } }

## Source Poisoning Detection

When trusted sources are compromised:

{ "source_poisoning_alert": { "source_id": "source:previously-trusted.org", "alert_type": "quality_degradation", "evidence": \[ "accuracy_drop: 0.91 → 0.62", "correction_rate_drop: 0.85 → 0.31", "style_change_detected: true" ], "recommended_action": "downgrade_trust", "new_verification_level": "high" } }

# Collective Sensemaking

## Sensemaking Capacity Dimensions

~~~
+-------------------------+--------------------------------+-------+
| Dimension               | Description                    | Scale |
+-------------------------+--------------------------------+-------+
| expertise_diversity     | Range of expert perspectives   | 0-1   |
| deliberation_quality    | Quality of public discourse    | 0-1   |
| argument_quality        | Logical quality of arguments   | 0-1   |
| counterargument_        | Are objections heard?          | 0-1   |
| presence                |                                |       |
| synthesis_capacity      | Can views be integrated?       | 0-1   |
| learning_rate           | How fast does understanding    | 0-1   |
|                         | improve?                       |       |
| error_correction        | Are mistakes fixed?            | 0-1   |
| uncertainty_tolerance   | Can ambiguity be held?         | 0-1   |
| complexity_handling     | Can complexity be managed?     | 0-1   |
+-------------------------+--------------------------------+-------+
~~~

## Sensemaking Degradation

Signs of collective sensemaking failure:

~~~
+---------------------+------------------------------+------------+
| Indicator           | Description                  | Severity   |
+---------------------+------------------------------+------------+
| Polarization        | Views becoming extreme       | High       |
| Expert rejection    | Expertise dismissed          | High       |
| Conspiracy thinking | Unfalsifiable beliefs        | Very High  |
| Reality divergence  | Groups in different          | Critical   |
|                     | realities                    |            |
+---------------------+------------------------------+------------+
~~~

## Sensemaking Support

Agents can support collective sensemaking:

{ "sensemaking_support": { "agent_capabilities": \[ "source_verification", "argument_analysis", "perspective_synthesis", "uncertainty_quantification", "context_provision" ], "agent_limitations": \[ "cannot_determine_truth", "cannot_replace_expertise", "cannot_force_agreement" ], "recommended_actions": \[ "provide_context", "cite_sources", "acknowledge_uncertainty", "represent_multiple_views", "flag_verified_vs_unverified" ] } }

# Signal Environment to Gravity

## E Modification Based on Signal

Signal environment affects available E:

E_effective = E_base × (1 - R) × signal_modifier

Where signal_modifier:

- Pristine: 1.0 (no change)
- Healthy: 1.0 (no change)
- Degraded: 0.9 (10% reduction)
- Polluted: 0.75 (25% reduction)
- Toxic: 0.5 (50% reduction)
- Collapsed: 0.1 (90% reduction)

## Action-Specific Modifiers

Some actions are more sensitive to signal environment:

~~~
+------------------------+--------------------+
| Action Type            | Signal Sensitivity |
+------------------------+--------------------+
| Recommendation making  | Very High          |
| Fact claims            | High               |
| Analysis               | High               |
| Execution              | Medium             |
| Read operations        | Low                |
+------------------------+--------------------+
~~~

## Example: Polluted Environment

{ "gravity_calculation": { "agent_id": "agent:independent:3gen:acme:abc123", "action": "provide_recommendation", "base_calculation": { "e_base": 55, "r_factor": 0.2, "e_trust": 44 }, "signal_adjustment": { "epistemic_health": 0.35, "signal_level": "polluted", "signal_modifier": 0.75, "action_sensitivity": "very_high", "additional_modifier": 0.8 }, "final_e": 26.4, "action_a": 30, "zeroth_law_result": "BLOCKED", "guidance": "Recommendation blocked. Epistemic environment too polluted for high-stakes recommendation." } }

# Recovery Protocols

## Environment Recovery

When signal environment improves:

Phase 1: DETECTION

- Improvement sustained for 24 hours
- Multiple indicators improving
- No new attacks detected

Phase 2: VERIFICATION

- External verification of improvement
- Source quality confirmed
- Sensemaking capacity restored

Phase 3: GRADUAL RESTORATION

- Signal modifier increased 0.1/day
- Agent autonomy gradually restored
- Monitoring continues

Phase 4: NORMAL OPERATIONS

- Full signal modifier restored
- Normal agent autonomy
- Standard monitoring

## Agent Recovery

Individual agent recovery after operating in polluted environment:

{ "agent_recovery": { "agent_id": "agent:independent:3gen:acme:abc123", "polluted_operation_duration": "72 hours", "recovery_protocol": { "verification_period": "24 hours", "actions_during_verification": "read_only", "verification_checks": \[ "trajectory_consistency_check", "belief_state_audit", "output_quality_review" ], "recovery_criteria": \[ "no_polluted_content_propagated", "accuracy_maintained", "no_manipulation_indicators" ] }, "recovery_status": "in_progress" } }

# Monitoring and Measurement

## Continuous Monitoring

Signal environment monitored continuously:

~~~
+------------------------+-----------+--------------------------+
| Metric                 | Frequency | Source                   |
+------------------------+-----------+--------------------------+
| Misinformation volume  | 0.1 Hz    | Fact-checkers, detection |
| Source quality         | 0.01 Hz   | Provenance systems       |
| Coordination detection | 0.1 Hz    | Network analysis         |
| Sensemaking indicators | 0.01 Hz   | Discourse analysis       |
+------------------------+-----------+--------------------------+
~~~

## Alert Thresholds

~~~
+----------------------+-----------+----------+
| Metric               | Warning   | Critical |
+----------------------+-----------+----------+
| Misinformation rate  | > 0.2     | > 0.4    |
| Coordination score   | > 0.3     | > 0.6    |
| Source degradation   | > 0.15    | > 0.3    |
+----------------------+-----------+----------+
~~~

## Reporting

Regular signal environment reports:

{ "signal_report": { "report_id": "SIG-2025-12-03-001", "zone_id": "zone-blue-prod-01", "period": "2025-12-03T00:00:00Z to 2025-12-03T23:59:59Z", "summary": { "epistemic_health_avg": 0.72, "epistemic_health_min": 0.58, "epistemic_health_max": 0.81, "alerts_triggered": 2, "info_ops_detected": 1 }, "incidents": \[ { "time": "2025-12-03T14:30:00Z", "type": "coordinated_activity", "severity": "medium", "duration": "2 hours", "response": "monitoring_increased" } ], "recommendations": \[ "Continue enhanced monitoring", "Review source quality for topic X" ] } }

# Security Considerations

## Gaming Resistance

Signal metrics must resist gaming:

- Multiple independent data sources
- Cross-validation of indicators
- Detection of metric manipulation
- Regular calibration against ground truth

## Privacy

Signal monitoring must respect privacy:

- Aggregate metrics only
- No individual tracking
- Content analysis, not person analysis
- Clear data retention limits

# IANA Considerations

This document has no IANA actions.

--- back

# Signal Measurement Instrumentation

Technical specifications for signal measurement.

# Information Operation Playbooks

Detailed response procedures for different attack types.

Acknowledgments

Signal environment analysis draws on research in misinformation detection, information operations, and collective intelligence.
