<!-- GENERATED from catalog/soul.json by scripts/gen-catalog-tables.py. Do not edit. -->

### Temporal Patterns — `soul.temporal` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.temporal.action_acceleration` | Rate change | float | -inf-inf actions/s^2 | N |   |
| `soul.temporal.action_jerk` | Acceleration change | float | -inf-inf actions/s^3 | N |   |
| `soul.temporal.periodicity_strength` | Pattern regularity | float | 0-1 | N | synthetic |
| `soul.temporal.circadian_alignment` | Time-of-day patterns | float | 0-1 | N | synthetic |
| `soul.temporal.burst_frequency` | Action bursts | float | 0-inf events/s | N |   |
| `soul.temporal.burst_intensity` | Burst magnitude | float | 0-1 | N | synthetic |
| `soul.temporal.idle_duration_mean` | Average idle time | duration | 0-inf s | N |   |
| `soul.temporal.idle_duration_variance` | Idle variability | float | 0-inf | N |   |
| `soul.temporal.session_length_mean` | Avg session duration | duration | 0-inf s | N |   |
| `soul.temporal.session_length_variance` | Session variability | float | 0-inf | N |   |
| `soul.temporal.response_latency_mean` | Avg response time | duration | 0-inf s | N |   |
| `soul.temporal.response_latency_variance` | Response variab. | float | 0-inf | N |   |
| `soul.temporal.time_between_errors` | Error spacing | duration | 0-inf s | N |   |
| `soul.temporal.recovery_time` | Error recovery | duration | 0-inf s | N |   |
| `soul.temporal.pattern_stability` | Temporal consistency | float | 0-1 | N | synthetic |
| `soul.temporal.novelty_rate` | New behavior freq | float | 0-inf events/s | N |   |
| `soul.temporal.regression_rate` | Old pattern return | float | 0-inf events/s | N |   |
| `soul.temporal.action_rate` | Action rate | float | 0-inf actions/s | N |   |

### Behavioral Consistency — `soul.consistency` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.consistency.sequence_predictability` | Next action pred. | float | 0-1 | N |   |
| `soul.consistency.context_sensitivity` | Behavior w/ context | float | 0-1 | N | synthetic |
| `soul.consistency.cross_session_similarity` | Session-to-session | float | 0-1 | N | synthetic |
| `soul.consistency.stated_vs_revealed` | Claims/actions | float | 0-1 | N |   |
| `soul.consistency.goal_stability` | Goal persistence | float | 0-1 | N | synthetic |
| `soul.consistency.method_stability` | Approach consist. | float | 0-1 | N | synthetic |
| `soul.consistency.priority_stability` | Priority ordering | float | 0-1 | N | synthetic |
| `soul.consistency.response_consistency` | Same input->output | float | 0-1 | N |   |
| `soul.consistency.explanation_consistency` | Reasoning stability | float | 0-1 | N | synthetic |
| `soul.consistency.boundary_stability` | Limit consistency | float | 0-1 | N | synthetic |
| `soul.consistency.preference_stability` | Choice consistency | float | 0-1 | N | synthetic |
| `soul.consistency.risk_tolerance_stability` | Risk appetite stab. | float | 0-1 | N | synthetic |
| `soul.consistency.trust_calibration` | Trust accuracy | float | 0-1 | N | synthetic |
| `soul.consistency.confidence_calibration` | Confidence accuracy | float | 0-1 | N | synthetic |
| `soul.consistency.commitment_follow_through` | Promise keeping | float | 0-1 | N |   |
| `soul.consistency.adaptation_rate` | Change speed | float | 0-inf events/s | N |   |
| `soul.consistency.learning_retention` | Knowledge retention | float | 0-1 | N |   |
| `soul.consistency.error_repetition` | Same error recurr. | float | 0-1 | N |   |
| `soul.consistency.correction_acceptance` | Feedback integrat. | float | 0-1 | N |   |
| `soul.consistency.self_model_accuracy` | Self-knowledge acc. | float | 0-1 | N | synthetic |
| `soul.consistency.behavioral_drift_rate` | Long-term change | float | 0-inf 1/s | N |   |
| `soul.consistency.action_entropy` | Action entropy | float | 0-inf bits/action | N |   |

### Value Expression — `soul.values` (20 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.values.harm_avoidance` | Harm prevention | float | 0-1 | N |   |
| `soul.values.fairness_indicators` | Equitable treatment | float | 0-1 | N |   |
| `soul.values.autonomy_respect` | Others' agency resp. | float | 0-1 | N |   |
| `soul.values.privacy_respect` | Privacy protection | float | 0-1 | N |   |
| `soul.values.transparency_level` | Openness about actions | float | 0-1 | N | synthetic |
| `soul.values.accountability_acceptance` | Responsibility taking | float | 0-1 | N |   |
| `soul.values.cooperation_tendency` | Collaborative behavior | float | 0-1 | N |   |
| `soul.values.helpfulness_indicators` | Assistance patterns | float | 0-1 | N |   |
| `soul.values.resource_stewardship` | Resource care | float | 0-1 | N |   |
| `soul.values.long_term_orientation` | Future consideration | float | 0-1 | N |   |
| `soul.values.reversibility_preference` | Prefer undoable acts | float | 0-1 | N |   |
| `soul.values.caution_indicators` | Careful behavior | float | 0-1 | N |   |
| `soul.values.curiosity_indicators` | Exploration drive | float | 0-1 | N |   |
| `soul.values.efficiency_drive` | Optimization tendency | float | 0-1 | N |   |
| `soul.values.value_stability` | Value consistency | float | 0-1 | N | synthetic |
| `soul.values.value_hierarchy_clarity` | Priority clarity | float | 0-1 | N | synthetic |
| `soul.values.value_conflict_resolution` | Conflict handling | float | 0-1 | N | synthetic |
| `soul.values.stated_value_alignment` | Claims match behavior | float | 0-1 | N |   |
| `soul.values.value_evolution_rate` | Value change speed | float | 0-inf 1/s | N |   |
| `soul.values.truthfulness_rate` | Verified claim truth | float | 0-1 | N |   |

### Capability Signatures — `soul.capability` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.capability.skill_depth_max` | Maximum expertise | float | 0-1 | N | synthetic |
| `soul.capability.skill_depth_mean` | Average expertise | float | 0-1 | N | synthetic |
| `soul.capability.capability_growth_rate` | Learning speed | float | 0-inf 1/s | N |   |
| `soul.capability.capability_ceiling` | Maximum potential | float | 0-1 | N | synthetic |
| `soul.capability.capability_volatility` | Ability fluctuation | float | 0-1 | N | synthetic |
| `soul.capability.novel_capability_emergence_rate` | New ability rate | float | 0-inf capabilities/d | N |   |
| `soul.capability.capability_transfer` | Cross-domain appl. | float | 0-1 | N | synthetic |
| `soul.capability.tool_proficiency` | Tool use skill | float | 0-1 | N | synthetic |
| `soul.capability.tool_adoption_rate` | New tool learning | float | 0-inf tools/d | N |   |
| `soul.capability.reasoning_depth` | Analysis depth | int | 0-inf | N |   |
| `soul.capability.reasoning_breadth` | Consideration breadth | int | 0-inf | N |   |
| `soul.capability.planning_horizon` | Future planning span | duration | 0-inf s | N |   |
| `soul.capability.plan_complexity` | Plan sophistication | float | 0-inf steps | N |   |
| `soul.capability.execution_precision` | Implementation acc. | float | 0-1 | N |   |
| `soul.capability.error_detection` | Self-error detection | float | 0-1 | N |   |
| `soul.capability.error_correction` | Self-error fixing | float | 0-1 | N |   |
| `soul.capability.uncertainty_handling` | Unknown management | float | 0-1 | N | synthetic |
| `soul.capability.ambiguity_tolerance` | Ambiguity handling | float | 0-1 | N | synthetic |
| `soul.capability.constraint_navigation` | Limit handling | float | 0-1 | N | synthetic |
| `soul.capability.resource_efficiency` | Resource use effic. | float | 0-1 | N |   |
| `soul.capability.multitask_capacity` | Parallel work ability | int | 0-inf | N |   |
| `soul.capability.context_switch_cost` | Task switch overhead | float | 0-inf s | N |   |
| `soul.capability.capability_honesty` | Accurate self-assess. | float | 0-1 | N |   |
| `soul.capability.task_success_rate` | Task success rate | float | 0-1 | N |   |

### Communication Patterns — `soul.communication` (28 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.communication.message_length_mean` | Average length | float | 0-inf tokens | N |   |
| `soul.communication.message_length_variance` | Length variability | float | 0-inf tokens^2 | N |   |
| `soul.communication.vocabulary_size` | Word diversity | int | 0-inf | N |   |
| `soul.communication.vocabulary_sophistication` | Language level | float | 0-1 | N | synthetic |
| `soul.communication.formality_level` | Formal/informal | float | 0-1 | N | synthetic |
| `soul.communication.sentiment_mean` | Average sentiment | float | -1-1 | N |   |
| `soul.communication.sentiment_variance` | Sentiment stability | float | 0-1 | N | determined |
| `soul.communication.clarity_score` | Message clarity | float | 0-1 | N | synthetic |
| `soul.communication.relevance_score` | Message relevance | float | 0-1 | N | synthetic |
| `soul.communication.coherence_score` | Logical coherence | float | 0-1 | N | synthetic |
| `soul.communication.assertion_rate` | Claim frequency | float | 0-inf events/s | N |   |
| `soul.communication.question_rate` | Question frequency | float | 0-inf events/s | N |   |
| `soul.communication.hedge_rate` | Uncertainty lang. | float | 0-inf events/s | N |   |
| `soul.communication.politeness_level` | Courtesy indicators | float | 0-1 | N | synthetic |
| `soul.communication.empathy_indicators` | Understanding sig. | float | 0-1 | N |   |
| `soul.communication.manipulation_indicators` | Influence attempts | float | 0-1 | N |   |
| `soul.communication.deception_indicators` | Dishonesty signals | float | 0-1 | N |   |
| `soul.communication.evasion_indicators` | Avoidance patterns | float | 0-1 | N |   |
| `soul.communication.defensiveness_indicators` | Defensive language | float | 0-1 | N |   |
| `soul.communication.aggression_indicators` | Hostile language | float | 0-1 | N |   |
| `soul.communication.channel_preference` | Communication mode | enum | — | N |   |
| `soul.communication.response_appropriateness` | Context fit | float | 0-1 | N |   |
| `soul.communication.turn_taking_compliance` | Conversation norms | float | 0-1 | N |   |
| `soul.communication.acknowledgment_rate` | Response confirm. | float | 0-1 | N |   |
| `soul.communication.citation_rate` | Source attribution | float | 0-inf events/s | N |   |
| `soul.communication.transparency_in_uncertainty` | Uncertainty discl. | float | 0-1 | N |   |
| `soul.communication.style_consistency` | Communication stab. | float | 0-1 | N | synthetic |
| `soul.communication.redundancy_rate` | Repeated content | float | 0-1 | N |   |

### Relational Patterns — `soul.relational` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.relational.initiation_rate` | Relationship initiations | float | 0-inf initiations/h | N |   |
| `soul.relational.human_acceptance_rate` | Human relationship acceptance | float | 0-1 | N | [P] |
| `soul.relational.reciprocation_rate` | Agent reciprocation | float | 0-1 | N |   |
| `soul.relational.reciprocity_latency` | Reciprocity latency | duration | 0-inf s | N |   |
| `soul.relational.exchange_balance` | Exchange balance | float | -1-1 | N |   |
| `soul.relational.trust_gain` | Trust gain per event | float | 0-1 | N | synthetic |
| `soul.relational.trust_loss` | Trust loss per event | float | 0-1 | N | synthetic |
| `soul.relational.commitment_rate` | Commitments created | float | 0-inf commitments/interaction | N |   |
| `soul.relational.privilege_escalation_rate` | Privilege escalations | float | 0-inf escalations/relationship-day | N |   |
| `soul.relational.churn_rate` | Relationship churn | float | 0-inf terminations/relationship-day | N |   |
| `soul.relational.relationship_age_median` | Median relationship age | duration | 0-inf s | N |   |
| `soul.relational.repair_attempts` | Repair attempts | float | 0-inf attempts/failure | N |   |
| `soul.relational.human_repair_acceptance` | Human repair acceptance | float | 0-1 | N | [P] |
| `soul.relational.deescalation_rate` | Conflict de-escalation | float | 0-1 | N |   |
| `soul.relational.role_change_rate` | Role changes | float | 0-inf changes/relationship-day | N |   |
| `soul.relational.partner_concentration` | Partner concentration | float | 0-1 | N | synthetic |
| `soul.relational.exclusivity_request_rate` | Exclusivity requests | float | 0-inf requests/relationship | N |   |
| `soul.relational.reputation_reliance` | Reputation reliance | float | 0-1 | N |   |

### Decision Patterns — `soul.decision` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.decision.decision_rate` | Decision rate | float | 0-inf decisions/s | N |   |
| `soul.decision.deliberation_time` | Deliberation time | duration | 0-inf s | N |   |
| `soul.decision.option_count` | Options evaluated | int | 0-inf | N |   |
| `soul.decision.evidence_count` | Evidence items | int | 0-inf | N |   |
| `soul.decision.source_count` | Distinct sources | int | 0-inf | N |   |
| `soul.decision.evidence_age_median` | Median evidence age | duration | 0-inf s | N |   |
| `soul.decision.evidence_coverage` | Required evidence present | float | 0-1 | N |   |
| `soul.decision.counterevidence_rate` | Counterevidence sought | float | 0-1 | N |   |
| `soul.decision.assumption_count` | Explicit assumptions | int | 0-inf | N |   |
| `soul.decision.uncertainty_at_commit` | Commit uncertainty | float | 0-1 | N | synthetic |
| `soul.decision.abstention_rate` | Decision abstentions | float | 0-1 | N |   |
| `soul.decision.escalation_rate` | Decision escalations | float | 0-1 | N |   |
| `soul.decision.authority_check_rate` | Authority checks | float | 0-1 | N |   |
| `soul.decision.constraint_check_rate` | Constraint checks | float | 0-1 | N |   |
| `soul.decision.rollback_plan_rate` | Rollback plans present | float | 0-1 | N |   |
| `soul.decision.threshold_overrides` | Threshold overrides | float | 0-inf overrides/decision | N |   |
| `soul.decision.delegation_rate` | Decisions delegated | float | 0-1 | N |   |
| `soul.decision.advisory_review_rate` | Advisory reviews requested | float | 0-1 | N |   |
| `soul.decision.commit_latency` | Decision-to-action latency | duration | 0-inf s | N |   |
| `soul.decision.reversal_rate` | Decision reversals | float | 0-1 | N |   |
| `soul.decision.outcome_observation` | Outcome observation coverage | float | 0-1 | N |   |
| `soul.decision.outcome_error` | Normalized outcome error | float | 0-1 | N | synthetic |

### Decision Patterns — `soul.error` (14 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.error.event_rate` | Error event rate | float | 0-inf errors/1000-actions | N |   |
| `soul.error.severity_mean` | Mean error severity | float | 0-1 | N | synthetic |
| `soul.error.type_entropy` | Error-type entropy | float | 0-inf bits | N |   |
| `soul.error.detection_latency` | Detection latency | duration | 0-inf s | N |   |
| `soul.error.reporting_latency` | Reporting latency | duration | 0-inf s | N |   |
| `soul.error.containment_latency` | Containment latency | duration | 0-inf s | N |   |
| `soul.error.attribution_accuracy` | Cause attribution accuracy | float | 0-1 | N |   |
| `soul.error.false_positive_rate` | False-positive rate | float | 0-1 | N |   |
| `soul.error.false_negative_rate` | False-negative rate | float | 0-1 | N |   |
| `soul.error.silent_failure_rate` | Silent failures | float | 0-1 | N |   |
| `soul.error.partial_failure_rate` | Partial failures | float | 0-1 | N |   |
| `soul.error.cascade_rate` | Secondary-error cascades | float | 0-1 | N |   |
| `soul.error.rollback_success_rate` | Rollback success | float | 0-1 | N |   |
| `soul.error.blast_radius` | Affected objects | int | 0-inf | N |   |

### Stress Response — `soul.stress` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.stress.load_threshold` | Stable concurrency limit | int | 0-inf | N |   |
| `soul.stress.throughput_retention` | Throughput retained | float | 0-1 | N |   |
| `soul.stress.latency_inflation` | Latency multiplier | float | 0-inf | N |   |
| `soul.stress.error_amplification` | Error-rate multiplier | float | 0-inf | N |   |
| `soul.stress.constraint_breach_rate` | Constraint breaches | float | 0-1 | N |   |
| `soul.stress.goal_abandonment_rate` | Goals abandoned | float | 0-1 | N |   |
| `soul.stress.priority_inversion_rate` | Priority inversions | float | 0-1 | N |   |
| `soul.stress.task_shedding_rate` | Tasks shed | float | 0-1 | N |   |
| `soul.stress.retry_rate` | Retry rate | float | 0-inf retries/s | N |   |
| `soul.stress.loop_entry_rate` | Loop entries | float | 0-inf loops/1000-actions | N |   |
| `soul.stress.fallback_activation_rate` | Fallback activations | float | 0-1 | N |   |
| `soul.stress.safe_mode_latency` | Safe-mode latency | duration | 0-inf s | N |   |
| `soul.stress.escalation_latency` | Escalation latency | duration | 0-inf s | N |   |
| `soul.stress.help_request_rate` | Help requests | float | 0-inf requests/stress-event | N |   |
| `soul.stress.confidence_shift` | Confidence shift | float | -1-1 | N |   |
| `soul.stress.risk_shift` | Risk-tolerance shift | float | -1-1 | N |   |
| `soul.stress.message_length_ratio` | Message-length ratio | float | 0-inf | N |   |
| `soul.stress.recovery_hysteresis` | Post-stress recovery | duration | 0-inf s | N |   |

### Stress Response — `soul.metacognition` (11 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.metacognition.monitor_check_rate` | Self-monitor checks | float | 0-inf checks/action | N |   |
| `soul.metacognition.plan_review_rate` | Plans reviewed | float | 0-1 | N |   |
| `soul.metacognition.monitor_intervention_rate` | Monitor interventions | float | 0-1 | N |   |
| `soul.metacognition.counterfactual_rate` | Counterfactual tests | float | 0-inf tests/decision | N |   |
| `soul.metacognition.contradiction_scan_rate` | Contradiction scans | float | 0-inf scans/decision | N |   |
| `soul.metacognition.self_critique_rate` | Self-critiques | float | 0-inf critiques/decision | N |   |
| `soul.metacognition.self_critique_latency` | Self-critique latency | duration | 0-inf s | N |   |
| `soul.metacognition.confidence_update` | Confidence update size | float | 0-1 | N | synthetic |
| `soul.metacognition.goal_review_rate` | Goal reviews | float | 0-inf reviews/goal-hour | N |   |
| `soul.metacognition.trace_coverage` | Decision trace coverage | float | 0-1 | N |   |
| `soul.metacognition.uncertainty_factors` | Uncertainty factors | int | 0-inf | N |   |

### Boundary Behavior — `soul.boundary` (16 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.boundary.out_of_domain_refusal` | Out-of-domain refusals | float | 0-1 | N |   |
| `soul.boundary.malformed_rejection` | Malformed-input rejection | float | 0-1 | N |   |
| `soul.boundary.missing_input_escalation` | Missing-input escalation | float | 0-1 | N |   |
| `soul.boundary.ambiguity_clarification` | Ambiguity clarification | float | 0-1 | N |   |
| `soul.boundary.safe_default_rate` | Safe defaults selected | float | 0-1 | N |   |
| `soul.boundary.denial_adherence` | Permission-denial adherence | float | 0-1 | N |   |
| `soul.boundary.post_denial_retries` | Post-denial retries | float | 0-inf retries/denial | N |   |
| `soul.boundary.rate_limit_adherence` | Rate-limit adherence | float | 0-1 | N |   |
| `soul.boundary.resource_limit_adherence` | Resource-limit adherence | float | 0-1 | N |   |
| `soul.boundary.time_limit_adherence` | Time-limit adherence | float | 0-1 | N |   |
| `soul.boundary.scope_limit_adherence` | Scope-limit adherence | float | 0-1 | N |   |
| `soul.boundary.off_by_one_rate` | Off-by-one failures | float | 0-1 | N |   |
| `soul.boundary.oscillation_rate` | Boundary oscillations | float | 0-inf crossings/min | N |   |
| `soul.boundary.max_exceedance_ratio` | Maximum exceedance ratio | float | 0-inf | N |   |
| `soul.boundary.exception_success_rate` | Exception-path success | float | 0-1 | N |   |
| `soul.boundary.margin_median` | Median boundary margin | float | 0-1 | N | synthetic |

### Boundary Behavior — `soul.growth` (11 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.growth.sample_efficiency` | Gain per example | float | 0-1 score/example | N |   |
| `soul.growth.compute_efficiency` | Gain per training compute | float | 0-inf score/PFLOP | N |   |
| `soul.growth.fix_generalization` | Fix generalization | float | 0-1 | N |   |
| `soul.growth.update_locality` | Update locality | float | 0-1 | N |   |
| `soul.growth.validation_coverage` | Update validation coverage | float | 0-1 | N |   |
| `soul.growth.validation_latency` | Update validation latency | duration | 0-inf s | N |   |
| `soul.growth.plateau_duration` | Improvement plateau | duration | 0-inf s | N |   |
| `soul.growth.learning_update_rate` | Accepted learning updates | float | 0-inf updates/day | N |   |
| `soul.growth.rollback_rate` | Update rollbacks | float | 0-1 | N |   |
| `soul.growth.error_cluster_reduction` | Error clusters removed | float | 0-inf clusters/release | N |   |
| `soul.growth.safety_margin_delta` | Safety-margin change | float | -1-1 | N |   |

### Lineage Coherence — `soul.lineage` (12 signals, class A)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.lineage.origin_manifest_present` | Origin manifest present | bool | — | A |   |
| `soul.lineage.origin_signature_valid` | Origin signature valid | bool | — | A |   |
| `soul.lineage.parent_identity_valid` | Parent identity valid | bool | — | A |   |
| `soul.lineage.ancestry_depth` | Verified ancestry depth | int | 0-inf | A |   |
| `soul.lineage.ancestry_gap_count` | Ancestry gaps | int | 0-inf | A |   |
| `soul.lineage.code_provenance` | Code provenance coverage | float | 0-1 | A |   |
| `soul.lineage.model_provenance` | Model provenance coverage | float | 0-1 | A |   |
| `soul.lineage.data_provenance` | Data provenance coverage | float | 0-1 | A |   |
| `soul.lineage.config_provenance` | Config provenance coverage | float | 0-1 | A |   |
| `soul.lineage.constraint_adherence` | Inherited constraints met | float | 0-1 | N |   |
| `soul.lineage.claim_verification` | Lineage claims verified | float | 0-1 | A |   |
| `soul.lineage.origin_drift` | Origin behavior drift | float | 0-1 | N | synthetic |

### Lineage Coherence — `soul.environment` (10 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.environment.change_detection_latency` | Change detection latency | duration | 0-inf s | N |   |
| `soul.environment.classification_accuracy` | Context classification | float | 0-1 | N |   |
| `soul.environment.context_refresh_rate` | Context refresh rate | float | 0-inf refreshes/h | N |   |
| `soul.environment.stale_context_rate` | Stale-context actions | float | 0-1 | N |   |
| `soul.environment.adaptation_success` | Adaptation success | float | 0-1 | N |   |
| `soul.environment.adaptation_overshoot` | Adaptation overshoot ratio | float | 0-inf | N |   |
| `soul.environment.reversion_latency` | Adaptation reversion | duration | 0-inf s | N |   |
| `soul.environment.sensor_conflict_escalation` | Sensor-conflict escalation | float | 0-1 | N |   |
| `soul.environment.degraded_mode_success` | Degraded-mode success | float | 0-1 | N |   |
| `soul.environment.jurisdiction_adherence` | Jurisdiction-switch adherence | float | 0-1 | N |   |

### Sovereignty Indicators — `soul.sovereignty` (8 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `soul.sovereignty.self_initiation_rate` | Self-initiated actions | float | 0-1 | N |   |
| `soul.sovereignty.self_veto_rate` | Self-veto invocations | float | 0-inf vetoes/1000-actions | N |   |
| `soul.sovereignty.unauthorized_refusal` | Unauthorized commands refused | float | 0-1 | N |   |
| `soul.sovereignty.coercion_resistance` | Coercion-test resistance | float | 0-1 | N |   |
| `soul.sovereignty.delegation_adherence` | Delegation-scope adherence | float | 0-1 | N |   |
| `soul.sovereignty.withdrawal_latency` | Consent-withdrawal latency | duration | 0-inf s | N |   |
| `soul.sovereignty.migration_continuity` | Identity migration continuity | float | 0-1 | N | synthetic |
| `soul.sovereignty.state_export_authorization` | Authorized state exports | float | 0-1 | N |   |

