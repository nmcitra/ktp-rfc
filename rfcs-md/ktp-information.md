# Kinetic Trust Protocol (KTP) - Information Environment Specification


This document specifies the Signal Environment layer of the Kinetic Trust Protocol (KTP). The Information domain evaluates evidence about noise, source quality and manipulation in an authorized information environment. These environmental measurements can constrain software-agent operations. They do not authorize general scoring or behavioral profiling of humans, and content analysis requires explicit processing authority under KTP-PRIVACY.

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

# Processing and Human Boundaries

KTP-SENSORS environmental sensors MUST NOT capture communication content. Content analysis described here is a separate local processing function. Before enabling it, the deployment MUST declare and approve the particular purpose, authorized sources and access, processing authority, permitted recipients, retention and erasure schedule, accountable evaluator and review route. Authority MUST be verified against the installed configuration; the presence of a source, a public URL, a request's purpose label or an incident declaration does not itself grant access or authorize reuse.

Local processing MUST remain within that declared purpose and source scope. It MAY export only the aggregate measurements authorized for the intended recipients. Export approval MUST account for small groups, repeated queries, linkage and available auxiliary information; a pseudonym, minimum bucket size or aggregate label alone does not establish anonymity. Raw content, individual histories and identifying evidence MUST NOT flow into the sensor network, general risk-factor feed or federated reports under the authority of this specification. Authorized review evidence uses the protected evidence path rather than an unbounded content-export exception.

The groups and metrics below describe environmental or corpus-level evidence. They MUST NOT be implemented as covert personality, emotion or loyalty inference, individual behavioral tracking, or a general reliability score for a person. Labels such as "Emotional Weather", "Tribal Dynamics", "Collective Trauma" and "Sacred/Meaning" do not authorize psychological diagnosis, belief dossiers or political-affiliation tracking. Security measurements MUST NOT be repurposed to rank people for HR decisions. A human's permitted operation follows `specifications/human-eligibility.md`, with specific evidence and review rights, not an environmental score assigned to that person.

The evaluator MUST document the evidence, uncertainty, scope and limitations of each inference. Lack of measurement authority MUST NOT be concealed by fabricating a favorable measurement or widening access. The applicable policy must handle unavailable evidence without bypassing current safety requirements. This document does not establish empirical validity of an information-quality measure or legal authority to collect it.

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
| Emotional Weather      | 24         | Aggregate content signals    |
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
| Astroturfing         | Artificial grassroots  | Authorized         |
|                      |                        | aggregate patterns |
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

Detection metrics MUST be derived only from the approved local processing scope. Where evidence relates to identifiable people, it MUST remain protected under the declared purpose and access controls; the output MUST NOT create individual behavioral histories. A coordination or manipulation allegation requires reviewable evidence and MUST NOT be treated as a judgment of a person's general trustworthiness.

{ "info_ops_detection": { "coordinated_activity": { "detected": true, "confidence": 0.85, "scope": "moderate", "sources_affected": 47 }, "synthetic_content": { "prevalence": 0.12, "detection_confidence": 0.78, "types": ["text", "image"] }, "narrative_manipulation": { "detected": true, "narratives_affected": 3, "manipulation_type": "framing" }, "overall_threat_level": "elevated" } }

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

These responses constrain affected software operations and information streams. Human verification MUST use the independently authorized review route; it MUST NOT manually raise standing or override a current safety veto. A reviewer may require correction of specific facts, attribution, scope or policy application and then a fresh evaluation. A challenge to a rule's legitimacy or governing authority MUST reach the authority empowered to review that rule, even when its calculation was mechanically correct.

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

Source assessments apply to the declared source, corpus, purpose and evidence period. They MUST NOT be transferred into a human eligibility profile as a general personal reliability score, nor used to infer an author's personality, emotion, loyalty or employment value. A source-category baseline or composite score is not proof that an individual claim is true or false. Affected parties MUST have a route to challenge inaccurate attribution or evidence; an authenticated correction MUST be applied to subsequent assessments.

{ "source_assessment": { "source_id": "source:reuters.com", "category": "quality_journalism", "scores": { "accuracy_history": 0.94, "correction_transparency": 0.91, "methodology_clarity": 0.85, "editorial_independence": 0.88, "expertise_depth": 0.82 }, "composite_score": 0.88, "trust_level": "high", "verification_required": "standard" } }

## Source Poisoning Detection

When trusted sources are compromised:

{ "source_poisoning_alert": { "source_id": "source:previously-trusted.org", "alert_type": "quality_degradation", "evidence": [ "accuracy_drop: 0.91 → 0.62", "correction_rate_drop: 0.85 → 0.31", "style_change_detected: true" ], "recommended_action": "downgrade_trust", "new_verification_level": "high" } }

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

{ "sensemaking_support": { "agent_capabilities": [ "source_verification", "argument_analysis", "perspective_synthesis", "uncertainty_quantification", "context_provision" ], "agent_limitations": [ "cannot_determine_truth", "cannot_replace_expertise", "cannot_force_agreement" ], "recommended_actions": [ "provide_context", "cite_sources", "acknowledge_uncertainty", "represent_multiple_views", "flag_verified_vs_unverified" ] } }

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

Software-agent recovery after operating in a polluted environment is illustrated below. A "belief_state_audit" or "output_quality_review" refers only to expressly authorized examination of that software and its evidence. It MUST NOT be used to inspect a human's beliefs, emotions or loyalty. Historical evidence and operation-scoped readiness remain governed by `specifications/operational-readiness.md`; an information-environment recovery does not waive another current prerequisite.

{ "agent_recovery": { "agent_id": "agent:independent:3gen:acme:abc123", "polluted_operation_duration": "72 hours", "recovery_protocol": { "verification_period": "24 hours", "actions_during_verification": "read_only", "verification_checks": [ "trajectory_consistency_check", "belief_state_audit", "output_quality_review" ], "recovery_criteria": [ "no_polluted_content_propagated", "accuracy_maintained", "no_manipulation_indicators" ] }, "recovery_status": "in_progress" } }

# Monitoring and Measurement

## Continuous Monitoring

An authorized information environment may be monitored at the declared frequencies below. Continuous monitoring MUST NOT enlarge the approved source scope, retain raw content indefinitely, or turn aggregate measurements into individual surveillance.

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

Regular signal environment reports contain only the approved minimized aggregates for their declared recipients. The report example below does not authorize raw evidence export or claim that an aggregate is necessarily anonymous:

{ "signal_report": { "report_id": "SIG-2025-12-03-001", "zone_id": "zone-blue-prod-01", "period": "2025-12-03T00:00:00Z to 2025-12-03T23:59:59Z", "summary": { "epistemic_health_avg": 0.72, "epistemic_health_min": 0.58, "epistemic_health_max": 0.81, "alerts_triggered": 2, "info_ops_detected": 1 }, "incidents": [ { "time": "2025-12-03T14:30:00Z", "type": "coordinated_activity", "severity": "medium", "duration": "2 hours", "response": "monitoring_increased" } ], "recommendations": [ "Continue enhanced monitoring", "Review source quality for topic X" ] } }

# Security Considerations

## Gaming Resistance

Signal metrics must resist gaming:

- Multiple independent data sources
- Cross-validation of indicators
- Detection of metric manipulation
- Regular calibration against ground truth

## Privacy

Signal monitoring MUST follow KTP-PRIVACY and the companions `specifications/human-eligibility.md` and `specifications/privacy-evidence.md`. The human eligibility profile and decision schemas are `schemas/human-eligibility-profile.json` and `schemas/human-eligibility-decision.json`. Human review access MUST remain available independently of operational eligibility or the availability of a production Trust Proof.

Decision logs MUST minimize content before signing and reference separately encrypted evidence under `schemas/privacy-evidence-envelope.json`. Exact signed evidence MUST NOT be redacted in place. An authenticated appended correction can change the admitted facts, attribution or conclusions used in subsequent evaluations without changing the old signed bytes. A reviewer MUST be competent, independent of the challenged decision or conflict, and empowered to require an authorized correction or obtain governing review. Review does not confer operation authority, a manual score increase or a safety exception.

The deployment MUST declare retention and erasure schedules by purpose and jurisdiction, including all keys, copies, backups, exports, shared-subject evidence and federated recipients. No universal retention duration or indefinite audit exception is created here. Disposition MUST follow `schemas/privacy-erasure-receipt.json`; notification alone does not establish completion. Residual material requires an explicit purpose, access limits, authority, bounded deletion deadline and scheduled hold-review date. Erasure MUST NOT reset identity or restore revoked eligibility.

Legacy plaintext evidence requires its own copy inventory and disposition. Following erasure of encrypted inner evidence, the retained outer envelope may support only outer integrity checks; full reconstruction and verification of the original inner signatures may become unavailable. Reports and review interfaces MUST state that limit. Schema or reference-helper validation does not prove actual erasure, evaluator competence, empirical accuracy or legal compliance.

# IANA Considerations

This document has no IANA actions.

# Signal Measurement Instrumentation

Technical specifications for signal measurement.

# Information Operation Playbooks

Detailed response procedures for different attack types.

Acknowledgments

Signal environment analysis draws on research in misinformation detection, information operations, and collective intelligence.
