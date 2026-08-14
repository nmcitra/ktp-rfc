# Context Signals — Time

When the agent acts, how fast, and against what clock.

MEASUREMENT CONVENTIONS

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement
envelope (#79), §4 the five observation classes and what each class makes MUST
(#87), §5 label sets (#68), §6 ranges and normalization, §7 aliases. Nothing
in this section overrides any of them.

What this section supplies is the binding: which observation class each Time
group takes, and which of its rows take a different one.

Group assignments. A group's class is the default for its rows; the named
exceptions take the class given. Four of the five classes are present —
N 167 · S 51 · D 39 · A 18, totalling 275. There is no class P: Time reads no
third party's number.

  duration      D   timeout_limit, grace_period S
  sequence      N   —
  rhythm        N   heartbeat_age D
  change        N   —
  window        S   consent_expiry, approval_expiry, lease_expiry A;
                    rate_limit_remaining, boundary_violations N
  history       N   system_uptime, service_age D; incident_count,
                    last_incident_age, security_event_count,
                    policy_violation_count, denied_action_count,
                    last_audit_age A
  future        N   next_maintenance, next_checkpoint, forecast_horizon S
  causality     N   cause_onset_delay, effect_observation_delay,
                    action_commit_delay, commit_effect_delay,
                    feedback_roundtrip, actuation_delay D
  sync          D   source_count, independent_sources, quorum_size,
                    quorum_agreement, consensus_rounds, logical_skew N;
                    sync_interval, leap_status S
  experience    N   —
  scale         S   —
  identity      A   first_seen_time, active_lifetime, dormant_lifetime,
                    trajectory_span, restart_count, trajectory_event_count,
                    max_continuity_gap, continuity_score N
  sovereignty   S   preemption_count, forced_delay_total,
                    forced_acceleration, notice_compliance,
                    human_override_latency N; schedule_consent A
  gravity       N   current_latency_injection S; current_quarantine_duration D
  throttle      N   active, mode, target_rate, bucket_capacity, refill_rate,
                    burst_limit, release_batch_size, recovery_ramp,
                    escalation_level, override_active S; cooldown_remaining D

An interval measured by a clock is class D, and the clock is the instrument.
This is what makes `duration` a D group in a domain with no physical sensor in
it: the subject is the operation whose start and end are stamped, the
population is n/a because one operation is not a set, and the instrument
identity that class D demands is the time source and its discipline — which
is what `time.sync.*` and `body.clock.*` carry. A latency reported as a mean
or a percentile is not this. That value is computed over a set of operations,
so it is class N and its population is that set.

`time.identity` is class A because a worldline is a record an authority kept.
The exceptions are the rows the deployment observed for itself, and the split
is legible in one pair: `birth_time` is the issuer's, `first_seen_time` is
ours, and a deployment that declares the second as the first has lost the
provenance the group exists to carry.

Class A's *unknown, not zero* clause is load-bearing in `history` and
`window`. `policy_violation_count` reading zero because the policy engine was
not running is not a compliant period, and `consent_expiry` returning no
record is not consent.

Projected values. Fourteen `time.future` rows describe periods that have not
happened, so they have no observation window: demand_forecast,
demand_peak_time, peak_demand, capacity_runway, storage_runway, energy_runway,
budget_runway, queue_clear_time, failure_time, failure_probability,
overload_probability, timeout_probability, deadline_miss_probability,
forecast_confidence. Add `time.causality.counterfactual_risk_delta`, which is
an estimate of a period that did not happen at all. They are held in their
nearest observed class and marked here rather than reclassified. Front matter
§4 names PROJECTED as a candidate sixth class and declines to add it, because
nmcitra/ktp-rfc#73 and #74 own that question.

The other four `time.future` rows are not projections and are not marked.
`next_maintenance` and `next_checkpoint` are calendar reads, `forecast_horizon`
is a declared model parameter, and `forecast_mae` is a backtest over resolved
forecasts — scoring a forecast is an observation; the forecast is not.

Bare 0-1 ranges. Nineteen Time signals carry a bare 0-1. Ten are ratios with a
real denominator and satisfy the catalogue rule by declaring that denominator
as their population; no normalization function exists for them and none is to
be invented: sequence.reorder_fraction, rhythm.cycle_duty,
rhythm.dominant_power_ratio, rhythm.burst_duty, rhythm.schedule_adherence,
history.retention_coverage, causality.attributable_fraction,
sync.quorum_agreement, sovereignty.notice_compliance, throttle.duty_cycle.
Nine are synthetic scores with no natural denominator and MUST declare a
normalization function in the deployment profile:
rhythm.periodicity_strength, future.failure_probability,
future.overload_probability, future.timeout_probability,
future.deadline_miss_probability, future.forecast_confidence,
causality.causal_confidence, experience.human_fragmentation,
identity.continuity_score. None is fully determined.

Five of those nine — the four `future` probabilities and forecast_confidence —
are projected values, so the function that produces them is a model rather
than a normalization. Declaring the model identity and version is the
instrument obligation, not a substitute for the normalization function, and
whether a projected value may be aggregated at all is #73's and #74's.

Where a ratio's denominator is gated by a predicate — on-time, independent,
compliant, usable — the predicate is a label set and is declared under the
catalogue-wide label-set rule, not here.

Privacy. Seventeen Time signals carry the [P] mark. The rule governing the
mark is open under nmcitra/ktp-rfc#67, and nothing in this section authorizes,
restricts or interprets it.


## Signals

The tables below are generated from the canonical JSON (`catalog/time.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/time.md"
