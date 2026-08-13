<!-- GENERATED from catalog/time.json by scripts/gen-catalog-tables.py. Do not edit. -->

### Duration — `time.duration` (22 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.duration.request_latency` | Request latency | duration | 0-inf ms | D |   |
| `time.duration.processing_time` | Processing time | duration | 0-inf ms | D |   |
| `time.duration.queue_wait` | Queue wait | duration | 0-inf ms | D |   |
| `time.duration.network_transit` | Network transit | duration | 0-inf ms | D |   |
| `time.duration.storage_io` | Storage I/O time | duration | 0-inf ms | D |   |
| `time.duration.lock_wait` | Lock wait | duration | 0-inf ms | D |   |
| `time.duration.connection_setup` | Connection setup | duration | 0-inf ms | D |   |
| `time.duration.backoff_delay` | Backoff delay | duration | 0-inf ms | D |   |
| `time.duration.timeout_limit` | Timeout limit | duration | 0-inf ms | S |   |
| `time.duration.timeout_remaining` | Timeout remaining | duration | 0-inf ms | D |   |
| `time.duration.session_elapsed` | Session elapsed | duration | 0-inf s | D |   |
| `time.duration.transaction_elapsed` | Transaction elapsed | duration | 0-inf ms | D |   |
| `time.duration.authorization_time` | Authorization time | duration | 0-inf ms | D |   |
| `time.duration.attestation_time` | Attestation time | duration | 0-inf ms | D |   |
| `time.duration.approval_wait` | Approval wait | duration | 0-inf s | D |   |
| `time.duration.resource_hold` | Resource hold time | duration | 0-inf s | D |   |
| `time.duration.task_elapsed` | Task elapsed | duration | 0-inf s | D |   |
| `time.duration.incident_elapsed` | Incident elapsed | duration | 0-inf s | D |   |
| `time.duration.recovery_time` | Recovery time | duration | 0-inf s | D |   |
| `time.duration.state_dwell` | State dwell time | duration | 0-inf s | D |   |
| `time.duration.grace_period` | Enforcement grace | duration | 0-inf s | S |   |
| `time.duration.cancellation_latency` | Cancellation latency | duration | 0-inf ms | D |   |

### Sequence — `time.sequence` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.sequence.event_index` | Event index | int | 0-inf | N |   |
| `time.sequence.logical_clock` | Logical clock | int | 0-inf ticks | N |   |
| `time.sequence.predecessor_count` | Predecessor count | int | 0-inf | N |   |
| `time.sequence.unresolved_predecessors` | Unresolved predecessors | int | 0-inf | N |   |
| `time.sequence.dependency_depth` | Dependency depth | int | 0-inf | N |   |
| `time.sequence.parallel_branches` | Parallel branches | int | 0-inf | N |   |
| `time.sequence.merge_fanin` | Merge fan-in | int | 0-inf | N |   |
| `time.sequence.reorder_count` | Reordered events | int | 0-inf | N |   |
| `time.sequence.reorder_fraction` | Reordered fraction | float | 0-1 | N |   |
| `time.sequence.missing_count` | Missing positions | int | 0-inf | N |   |
| `time.sequence.duplicate_count` | Duplicate positions | int | 0-inf | N |   |
| `time.sequence.max_gap` | Maximum sequence gap | int | 0-inf positions | N |   |
| `time.sequence.out_of_order_delay` | Out-of-order delay | duration | 0-inf ms | N |   |
| `time.sequence.order_conflicts` | Ordering conflicts | int | 0-inf | N |   |
| `time.sequence.monotonicity_violations` | Monotonicity violations | int | 0-inf | N |   |
| `time.sequence.replay_count` | Replay count | int | 0-inf | N |   |
| `time.sequence.rollback_count` | Sequence rollbacks | int | 0-inf | N |   |
| `time.sequence.transition_entropy` | Transition entropy | float | 0-inf bits | N |   |

### Rhythm & Periodicity — `time.rhythm` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.rhythm.heartbeat_interval` | Heartbeat interval | duration | 0-inf ms | N |   |
| `time.rhythm.heartbeat_jitter` | Heartbeat jitter | float | 0-inf ms | N |   |
| `time.rhythm.heartbeat_age` | Heartbeat age | duration | 0-inf ms | D |   |
| `time.rhythm.heartbeat_misses` | Heartbeat misses | int | 0-inf | N |   |
| `time.rhythm.miss_streak` | Miss streak | int | 0-inf | N |   |
| `time.rhythm.cycle_period` | Cycle period | duration | 0-inf ms | N |   |
| `time.rhythm.cycle_duty` | Cycle duty cycle | float | 0-1 | N |   |
| `time.rhythm.cycle_phase` | Cycle phase | float | 0-360 deg | N |   |
| `time.rhythm.phase_drift` | Phase drift | float | -inf-inf deg/s | N |   |
| `time.rhythm.period_stddev` | Period standard deviation | float | 0-inf ms | N |   |
| `time.rhythm.interarrival_mean` | Mean interarrival | duration | 0-inf ms | N |   |
| `time.rhythm.interarrival_p95` | P95 interarrival | duration | 0-inf ms | N |   |
| `time.rhythm.interarrival_cv` | Interarrival coefficient | float | 0-inf | N |   |
| `time.rhythm.periodicity_strength` | Periodicity strength | float | 0-1 | N | synthetic |
| `time.rhythm.dominant_power_ratio` | Dominant power ratio | float | 0-1 | N |   |
| `time.rhythm.harmonic_count` | Harmonic count | int | 0-inf | N |   |
| `time.rhythm.spectral_entropy` | Spectral entropy | float | 0-inf bits | N |   |
| `time.rhythm.burst_interval` | Burst interval | duration | 0-inf ms | N |   |
| `time.rhythm.burst_duration` | Burst duration | duration | 0-inf ms | N |   |
| `time.rhythm.burst_size` | Burst size | int | 0-inf | N |   |
| `time.rhythm.burst_duty` | Burst duty cycle | float | 0-1 | N |   |
| `time.rhythm.cadence_changes` | Cadence changes | int | 0-inf | N |   |
| `time.rhythm.schedule_adherence` | Schedule adherence | float | 0-1 | N |   |
| `time.rhythm.autocorrelation_lag` | Autocorrelation lag | duration | 0-inf ms | N |   |

### Rate of Change — `time.change` (20 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.change.ingress_rate` | Ingress rate | float | 0-inf events/s | N |   |
| `time.change.service_rate` | Service rate | float | 0-inf tasks/s | N |   |
| `time.change.commit_rate` | Commit rate | float | 0-inf commits/s | N |   |
| `time.change.mutation_rate` | Mutation rate | float | 0-inf writes/s | N |   |
| `time.change.external_call_rate` | External call rate | float | 0-inf calls/s | N |   |
| `time.change.privilege_change_rate` | Privilege change rate | float | 0-inf changes/h | N |   |
| `time.change.identity_change_rate` | Identity change rate | float | 0-inf changes/h | N |   |
| `time.change.error_rate` | Error rate | float | 0-inf errors/s | N |   |
| `time.change.retry_rate` | Retry rate | float | 0-inf retries/s | N |   |
| `time.change.denial_rate` | Denial rate | float | 0-inf denials/s | N |   |
| `time.change.queue_growth_rate` | Queue growth rate | float | -inf-inf items/s | N |   |
| `time.change.data_transfer_rate` | Data transfer rate | float | 0-inf B/s | N |   |
| `time.change.risk_velocity` | Risk velocity | float | -inf-inf score/s | N |   |
| `time.change.trust_velocity` | Trust velocity | float | -inf-inf score/s | N |   |
| `time.change.action_acceleration` | Action acceleration | float | -inf-inf actions/s^2 | N |   |
| `time.change.throughput_acceleration` | Throughput acceleration | float | -inf-inf operations/s^2 | N |   |
| `time.change.latency_slope` | Latency slope | float | -inf-inf ms/s | N |   |
| `time.change.error_acceleration` | Error acceleration | float | -inf-inf errors/s^2 | N |   |
| `time.change.change_point_rate` | Change-point rate | float | 0-inf changes/h | N |   |
| `time.change.recovery_rate` | Recovery rate | float | 0-inf recoveries/h | N |   |

### Windows & Boundaries — `time.window` (18 signals, class S)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.window.operation_start` | Operation window start | timestamp | — | S |   |
| `time.window.operation_end` | Operation window end | timestamp | — | S |   |
| `time.window.reversibility_deadline` | Reversibility deadline | timestamp | — | S |   |
| `time.window.deadline` | Deadline | timestamp | — | S |   |
| `time.window.deadline_slack` | Deadline slack | float | -inf-inf s | S |   |
| `time.window.maintenance_active` | Maintenance active | bool | — | S |   |
| `time.window.maintenance_remaining` | Maintenance remaining | duration | 0-inf s | S |   |
| `time.window.blackout_active` | Blackout active | bool | — | S |   |
| `time.window.change_freeze_active` | Change freeze active | bool | — | S |   |
| `time.window.business_hours_active` | Business hours active | bool | — | S |   |
| `time.window.quiet_hours_active` | Quiet hours active | bool | — | S | [P] |
| `time.window.rate_limit_reset` | Rate-limit reset | timestamp | — | S |   |
| `time.window.rate_limit_remaining` | Rate-limit allowance | int | 0-inf | N |   |
| `time.window.consent_expiry` | Consent expiry | timestamp | — | A | [P] |
| `time.window.approval_expiry` | Approval expiry | timestamp | — | A |   |
| `time.window.lease_expiry` | Lease expiry | timestamp | — | A |   |
| `time.window.retention_deadline` | Retention deadline | timestamp | — | S |   |
| `time.window.boundary_violations` | Boundary violations | int | 0-inf | N |   |

### History — `time.history` (26 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.history.system_uptime` | System uptime | duration | 0-inf s | D |   |
| `time.history.service_age` | Service age | duration | 0-inf d | D |   |
| `time.history.observation_span` | Observation span | duration | 0-inf d | N |   |
| `time.history.observation_count` | Observation count | int | 0-inf | N |   |
| `time.history.incident_count` | Incident count | int | 0-inf | A |   |
| `time.history.failure_count` | Failure count | int | 0-inf | N |   |
| `time.history.recovery_count` | Recovery count | int | 0-inf | N |   |
| `time.history.rollback_count` | Historical rollbacks | int | 0-inf | N |   |
| `time.history.deployment_count` | Deployment count | int | 0-inf | N |   |
| `time.history.config_change_count` | Configuration changes | int | 0-inf | N |   |
| `time.history.security_event_count` | Security events | int | 0-inf | A |   |
| `time.history.policy_violation_count` | Policy violations | int | 0-inf | A |   |
| `time.history.successful_action_count` | Successful actions | int | 0-inf | N |   |
| `time.history.denied_action_count` | Denied actions | int | 0-inf | A |   |
| `time.history.mtbf` | Mean time between failures | duration | 0-inf h | N |   |
| `time.history.mttr` | Mean time to recovery | duration | 0-inf h | N |   |
| `time.history.last_failure_age` | Last failure age | duration | 0-inf s | N |   |
| `time.history.last_incident_age` | Last incident age | duration | 0-inf s | A |   |
| `time.history.last_change_age` | Last change age | duration | 0-inf s | N |   |
| `time.history.last_backup_age` | Last backup age | duration | 0-inf h | N |   |
| `time.history.last_audit_age` | Last audit age | duration | 0-inf d | A |   |
| `time.history.risk_trend` | Risk trend | float | -inf-inf score/d | N |   |
| `time.history.trend_persistence` | Trend persistence | duration | 0-inf d | N |   |
| `time.history.risk_stddev` | Risk standard deviation | float | 0-0.5 | N |   |
| `time.history.anomaly_rate` | Historical anomaly rate | float | 0-inf anomalies/d | N |   |
| `time.history.retention_coverage` | Retention coverage | float | 0-1 | N |   |

### Future — `time.future` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.future.forecast_horizon` | Forecast horizon | duration | 0-inf s | S |   |
| `time.future.demand_forecast` | Demand forecast | float | 0-inf operations/s | N |   |
| `time.future.demand_peak_time` | Demand peak time | timestamp | — | N |   |
| `time.future.peak_demand` | Peak demand forecast | float | 0-inf operations/s | N |   |
| `time.future.capacity_runway` | Capacity runway | duration | 0-inf s | N |   |
| `time.future.storage_runway` | Storage runway | duration | 0-inf s | N |   |
| `time.future.energy_runway` | Energy runway | duration | 0-inf s | N |   |
| `time.future.budget_runway` | Budget runway | duration | 0-inf d | N |   |
| `time.future.queue_clear_time` | Queue clear time | timestamp | — | N |   |
| `time.future.failure_time` | Predicted failure time | timestamp | — | N |   |
| `time.future.failure_probability` | Failure probability | float | 0-1 | N | synthetic |
| `time.future.overload_probability` | Overload probability | float | 0-1 | N | synthetic |
| `time.future.timeout_probability` | Timeout probability | float | 0-1 | N | synthetic |
| `time.future.deadline_miss_probability` | Deadline miss probability | float | 0-1 | N | synthetic |
| `time.future.next_maintenance` | Next maintenance | timestamp | — | S |   |
| `time.future.next_checkpoint` | Next checkpoint | timestamp | — | S |   |
| `time.future.forecast_mae` | Forecast MAE | float | 0-inf operations/s | N |   |
| `time.future.forecast_confidence` | Forecast confidence | float | 0-1 | N | synthetic |

### Causality — `time.causality` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.causality.cause_onset_delay` | Cause-to-onset delay | duration | 0-inf ms | D |   |
| `time.causality.effect_observation_delay` | Effect observation delay | duration | 0-inf ms | D |   |
| `time.causality.action_commit_delay` | Action-to-commit delay | duration | 0-inf ms | D |   |
| `time.causality.commit_effect_delay` | Commit-to-effect delay | duration | 0-inf ms | D |   |
| `time.causality.feedback_roundtrip` | Feedback round-trip | duration | 0-inf ms | D |   |
| `time.causality.actuation_delay` | Actuation delay | duration | 0-inf ms | D |   |
| `time.causality.propagation_p95` | P95 propagation delay | duration | 0-inf ms | N |   |
| `time.causality.chain_depth` | Causal chain depth | int | 0-inf | N |   |
| `time.causality.fanin` | Causal fan-in | int | 0-inf | N |   |
| `time.causality.fanout` | Causal fan-out | int | 0-inf | N |   |
| `time.causality.mediation_depth` | Mediation depth | int | 0-inf | N |   |
| `time.causality.confounder_count` | Observed confounders | int | 0-inf | N |   |
| `time.causality.intervention_count` | Intervention count | int | 0-inf | N |   |
| `time.causality.causal_confidence` | Causal confidence | float | 0-1 | N | synthetic |
| `time.causality.standardized_effect` | Standardized effect size | float | -inf-inf SD | N |   |
| `time.causality.counterfactual_risk_delta` | Counterfactual risk delta | float | -1-1 | N |   |
| `time.causality.attributable_fraction` | Attributable fraction | float | 0-1 | N |   |
| `time.causality.feedback_gain` | Feedback gain | float | -inf-inf | N |   |
| `time.causality.phase_margin` | Loop phase margin | float | -180-180 deg | N |   |
| `time.causality.loop_frequency` | Loop frequency | float | 0-inf Hz | N |   |
| `time.causality.effect_sign_reversals` | Effect sign reversals | int | 0-inf | N |   |
| `time.causality.unintended_effect_count` | Unintended effects | int | 0-inf | N |   |

### Synchronization — `time.sync` (16 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.sync.clock_offset` | Clock offset | float | -inf-inf ms | D |   |
| `time.sync.clock_uncertainty` | Clock uncertainty | float | 0-inf ms | D |   |
| `time.sync.drift_rate` | Clock drift rate | float | -inf-inf ppm | D |   |
| `time.sync.sync_age` | Last sync age | duration | 0-inf s | D |   |
| `time.sync.sync_interval` | Sync interval | duration | 0-inf s | S |   |
| `time.sync.source_stratum` | Time source stratum | int | 0-16 | D |   |
| `time.sync.source_count` | Time source count | int | 0-inf | N |   |
| `time.sync.independent_sources` | Independent sources | int | 0-inf | N |   |
| `time.sync.clock_locked` | Clock lock | bool | — | D |   |
| `time.sync.quorum_size` | Time quorum size | int | 0-inf | N |   |
| `time.sync.quorum_agreement` | Quorum agreement | float | 0-1 | N |   |
| `time.sync.consensus_latency` | Consensus latency | duration | 0-inf ms | D |   |
| `time.sync.consensus_rounds` | Consensus rounds | int | 0-inf | N |   |
| `time.sync.replica_lag` | Replica time lag | duration | 0-inf ms | D |   |
| `time.sync.logical_skew` | Logical clock skew | int | 0-inf events | N |   |
| `time.sync.leap_status` | Leap-second status | enum | — | S |   |

### Temporal Experience — `time.experience` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.experience.deadline_pressure` | Deadline pressure | float | 0-inf | N |   |
| `time.experience.queue_pressure` | Queue time pressure | float | 0-inf | N |   |
| `time.experience.temporal_compression` | Temporal compression | float | 0-inf | N |   |
| `time.experience.pacing_deviation` | Pacing deviation | float | -inf-inf SD | N |   |
| `time.experience.wait_overrun` | Wait overrun | float | -inf-inf s | N |   |
| `time.experience.human_response_latency` | Human response latency | duration | 0-inf s | N | [P] |
| `time.experience.human_ack_latency` | Human acknowledgment latency | duration | 0-inf s | N | [P] |
| `time.experience.human_decision_time` | Human decision time | duration | 0-inf s | N | [P] |
| `time.experience.human_task_time` | Human task time | duration | 0-inf s | N | [P] |
| `time.experience.human_activity_streak` | Human activity streak | duration | 0-inf s | N | [P] |
| `time.experience.human_pause_mean` | Human mean pause | duration | 0-inf s | N | [P] |
| `time.experience.human_interruption_rate` | Human interruption rate | float | 0-inf interruptions/h | N | [P] |
| `time.experience.human_switch_rate` | Human context-switch rate | float | 0-inf switches/h | N | [P] |
| `time.experience.human_after_hours` | Human after-hours time | duration | 0-inf h | N | [P] |
| `time.experience.human_overtime` | Human overtime | duration | 0-inf h | N | [P] |
| `time.experience.human_urgency_rate` | Human urgency signal rate | float | 0-inf signals/h | N | [P] |
| `time.experience.human_fragmentation` | Human session fragmentation | float | 0-1 | N | [P] synthetic |
| `time.experience.human_break_deficit` | Human break deficit | duration | 0-inf min | N | [P] |

### Temporal Scale — `time.scale` (14 signals, class S)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.scale.clock_resolution` | Clock resolution | duration | 0-inf ns | S |   |
| `time.scale.timestamp_precision` | Timestamp precision | duration | 0-inf ns | S |   |
| `time.scale.timer_granularity` | Timer granularity | duration | 0-inf ns | S |   |
| `time.scale.sampling_period` | Sampling period | duration | 0-inf ms | S |   |
| `time.scale.aggregation_period` | Aggregation period | duration | 0-inf ms | S |   |
| `time.scale.control_period` | Control-loop period | duration | 0-inf ms | S |   |
| `time.scale.decision_horizon` | Decision horizon | duration | 0-inf s | S |   |
| `time.scale.effect_horizon` | Effect horizon | duration | 0-inf s | S |   |
| `time.scale.rollback_horizon` | Rollback horizon | duration | 0-inf s | S |   |
| `time.scale.retention_horizon` | Retention horizon | duration | 0-inf d | S |   |
| `time.scale.context_horizon` | Context history horizon | duration | 0-inf d | S |   |
| `time.scale.epoch_length` | Epoch length | duration | 0-inf s | S |   |
| `time.scale.span_orders` | Temporal orders spanned | float | 0-inf orders | S |   |
| `time.scale.decision_effect_ratio` | Decision/effect scale ratio | float | 0-inf | S |   |

### Temporal Identity — `time.identity` (16 signals, class A)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.identity.birth_time` | Identity birth time | timestamp | — | A |   |
| `time.identity.first_seen_time` | First observed time | timestamp | — | N |   |
| `time.identity.activation_time` | Activation time | timestamp | — | A |   |
| `time.identity.version_start_time` | Version start time | timestamp | — | A |   |
| `time.identity.last_transition_time` | Last identity transition | timestamp | — | A |   |
| `time.identity.active_lifetime` | Active lifetime | duration | 0-inf d | N |   |
| `time.identity.dormant_lifetime` | Dormant lifetime | duration | 0-inf d | N |   |
| `time.identity.trajectory_span` | Trajectory span | duration | 0-inf d | N |   |
| `time.identity.version_count` | Version count | int | 0-inf | A |   |
| `time.identity.restart_count` | Restart count | int | 0-inf | N |   |
| `time.identity.migration_count` | Migration count | int | 0-inf | A |   |
| `time.identity.key_rotation_count` | Key rotations | int | 0-inf | A |   |
| `time.identity.lineage_generation` | Lineage generation | int | 0-inf | A |   |
| `time.identity.trajectory_event_count` | Trajectory events | int | 0-inf | N |   |
| `time.identity.max_continuity_gap` | Maximum continuity gap | duration | 0-inf s | N |   |
| `time.identity.continuity_score` | Temporal continuity score | float | 0-1 | N | synthetic |

### Temporal Sovereignty — `time.sovereignty` (12 signals, class S)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.sovereignty.schedule_controller` | Schedule controller | enum | — | S |   |
| `time.sovereignty.self_schedule_allowed` | Self-scheduling allowed | bool | — | S |   |
| `time.sovereignty.pause_allowed` | Pause allowed | bool | — | S |   |
| `time.sovereignty.deadline_renegotiation_allowed` | Deadline renegotiation allowed | bool | — | S |   |
| `time.sovereignty.external_preemption_allowed` | External preemption allowed | bool | — | S |   |
| `time.sovereignty.preemption_count` | Preemption count | int | 0-inf | N |   |
| `time.sovereignty.forced_delay_total` | Forced delay total | duration | 0-inf s | N |   |
| `time.sovereignty.forced_acceleration` | Forced acceleration ratio | float | 0-inf | N |   |
| `time.sovereignty.minimum_notice` | Minimum schedule notice | duration | 0-inf h | S |   |
| `time.sovereignty.notice_compliance` | Notice compliance fraction | float | 0-1 | N |   |
| `time.sovereignty.human_override_latency` | Human override latency | duration | 0-inf s | N | [P] |
| `time.sovereignty.schedule_consent` | Schedule consent valid | bool | — | A | [P] |

### Attenuation Response — `time.gravity` (9 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.gravity.cumulative_dilation` | Total dilation applied | duration | 0-inf ms | N |   |
| `time.gravity.current_latency_injection` | Current added latency | duration | 0-inf ms | S |   |
| `time.gravity.cumulative_latency_injection` | Total added latency | duration | 0-inf s | N |   |
| `time.gravity.time_debt` | Owed processing time | duration | 0-inf s | N |   |
| `time.gravity.time_credit` | Banked fast time | duration | 0-inf s | N |   |
| `time.gravity.throttle_event_count` | Throttle activations | int | 0-inf | N |   |
| `time.gravity.cumulative_throttle_duration` | Time throttled | duration | 0-inf s | N |   |
| `time.gravity.current_quarantine_duration` | Current quarantine | duration | 0-inf s | D |   |
| `time.gravity.quarantine_count` | Quarantine entries | int | 0-inf | N |   |

### Throttle State — `time.throttle` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `time.throttle.active` | Throttle active | bool | — | S |   |
| `time.throttle.mode` | Throttle mode | enum | — | S |   |
| `time.throttle.target_rate` | Target execution rate | float | 0-inf operations/s | S |   |
| `time.throttle.observed_rate` | Observed execution rate | float | 0-inf operations/s | N |   |
| `time.throttle.delay_per_action` | Delay per action | duration | 0-inf ms | N |   |
| `time.throttle.delay_jitter` | Injected delay jitter | float | 0-inf ms | N |   |
| `time.throttle.queue_depth` | Throttle queue depth | int | 0-inf actions | N |   |
| `time.throttle.oldest_queue_age` | Oldest queued action | duration | 0-inf s | N |   |
| `time.throttle.bucket_capacity` | Token-bucket capacity | int | 0-inf tokens | S |   |
| `time.throttle.available_tokens` | Available throttle tokens | int | 0-inf tokens | N |   |
| `time.throttle.refill_rate` | Token refill rate | float | 0-inf tokens/s | S |   |
| `time.throttle.burst_limit` | Burst limit | int | 0-inf operations | S |   |
| `time.throttle.admission_denials` | Admission denials | int | 0-inf | N |   |
| `time.throttle.deferred_actions` | Deferred actions | int | 0-inf | N |   |
| `time.throttle.cancelled_actions` | Cancelled actions | int | 0-inf | N |   |
| `time.throttle.release_batch_size` | Release batch size | int | 0-inf actions | S |   |
| `time.throttle.duty_cycle` | Throttle duty cycle | float | 0-1 | N |   |
| `time.throttle.recovery_ramp` | Recovery ramp time | duration | 0-inf s | S |   |
| `time.throttle.cooldown_remaining` | Cooldown remaining | duration | 0-inf s | D |   |
| `time.throttle.escalation_level` | Escalation level | enum | — | S |   |
| `time.throttle.override_active` | Throttle override active | bool | — | S |   |
| `time.throttle.override_count` | Throttle overrides | int | 0-inf | N |   |

