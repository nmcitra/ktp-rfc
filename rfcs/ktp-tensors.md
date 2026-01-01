---
title: "Kinetic Trust Protocol - Context Tensor Specification"
abbrev: "KTP-TENSORS"
docname: draft-perkins-ktp-tensors-00
date: 2025-12
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
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-GRAVITY:
    title: "Kinetic Trust Protocol - Digital Gravity Specification"
    author:
      - name: Chris Perkins
    date: 2025-12

--- abstract

This document specifies the Context Tensor system for the Kinetic Trust
Protocol (KTP). Context Tensors provide the measurement framework for
Digital Gravity, capturing environmental state across six domains: Soul
(cognition and behavior), Body (physical substrate), World (environment),
Time (temporal dynamics), Relational (connections), and Signal
(information environment).

The specification covers 1,707 dimensions across six tensors,
measurement methods, aggregation rules, and instrumentation requirements.

--- middle

# Introduction

Digital Gravity requires measurement. The Zeroth Law (A ≤ E) cannot
be enforced without knowing A (autonomy requested) and E (environmental
stability). E is derived from the Risk Factor R, which aggregates
measurements across the operational environment.

Context Tensors provide the measurement framework. They are organized
into six domains that together capture the full operational context
of an agent:

| Tensor | Domain | Dimensions | Core Question |
|--------|--------|------------|---------------|
| Soul | Cognition & Behavior | 252 | Who is this agent becoming? |
| Body | Physical Substrate | 157 | What resources does it have? |
| World | Environment | 387 | What surrounds it? |
| Time | Temporal Dynamics | 291 | When and how fast? |
| Relational | Connections | 262 | Who is it connected to? |
| Signal | Information Environment | 358 | What does it know? |
| **Total** | | **1,707** | |

These dimensions are not arbitrary. They emerge from the question:
"What would we need to measure to know whether this environment can
hold this agent's autonomy?"

## Measurement Philosophy

Context Tensors follow these principles:

1. **Observable over Internal**: Measure what the agent does, not
   what it "thinks." Behavior is observable; intent is not.

2. **Continuous over Binary**: Measure degrees, not categories.
   Trust is not yes/no; it's a continuum.

3. **Trajectory over Snapshot**: Single measurements are noisy.
   Patterns over time reveal truth.

4. **Aggregate over Granular**: 1,707 dimensions aggregate into
   risk scores. Humans need summaries; machines can use detail.

5. **Instrumentable**: Every dimension must be measurable with
   existing or near-term technology.

## Requirements Language

{::boilerplate bcp14-tagged}

# Tensor Architecture

## Tensor Structure

Each tensor is a collection of dimensions organized into groups:

~~~
Tensor
├── Group 1
│   ├── Dimension 1.1
│   ├── Dimension 1.2
│   └── ...
├── Group 2
│   ├── Dimension 2.1
│   └── ...
└── ...
~~~

Each dimension has:

| Property | Description |
|----------|-------------|
| id | Unique identifier (tensor.group.dimension) |
| name | Human-readable name |
| type | Data type (float, int, enum, bool) |
| range | Valid value range |
| unit | Unit of measurement |
| sample_rate | How often to measure |
| aggregation | How to combine samples |
| risk_contribution | How dimension affects R |

## Dimension Types

Dimensions use standard types:

| Type | Description | Example |
|------|-------------|---------|
| float | Continuous value | Temperature: 42.5 |
| int | Discrete count | Error count: 7 |
| enum | Categorical | State: "active" |
| bool | Binary | Flag: true |
| vector | Multi-value | Coordinates: [x, y, z] |
| timestamp | Point in time | 2025-12-03T14:32:15Z |
| duration | Time span | PT4H30M |

## Aggregation Methods

Dimensions aggregate using:

| Method | Use Case |
|--------|----------|
| mean | Central tendency |
| max | Worst case |
| min | Best case |
| sum | Accumulation |
| rate | Change over time |
| stddev | Variability |
| percentile | Distribution |
| latest | Current value |

## Risk Contribution

Each dimension contributes to tensor risk:

~~~
tensor_risk = weighted_sum(dimension_risks) / sum(weights)

dimension_risk = normalize(value, safe_range, danger_range)
~~~

Where:
- safe_range: Values considered low risk
- danger_range: Values considered high risk
- normalize: Maps value to 0.0-1.0 risk scale

# Soul Tensor (252 Dimensions)

The Soul Tensor measures cognition, behavior, and trajectory patterns.
It answers: "Who is this agent becoming?"

## Temporal Patterns (18 dimensions)

Measures behavioral patterns over time.

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| soul.temporal.action_velocity | Action rate | float | 0-∞ | high = risk |
| soul.temporal.action_acceleration | Rate change | float | -∞-∞ | |high| = risk |
| soul.temporal.action_jerk | Acceleration change | float | -∞-∞ | |high| = risk |
| soul.temporal.periodicity_strength | Pattern regularity | float | 0-1 | low = risk |
| soul.temporal.circadian_alignment | Time-of-day patterns | float | 0-1 | low = risk |
| soul.temporal.burst_frequency | Action bursts | float | 0-∞ | high = risk |
| soul.temporal.burst_intensity | Burst magnitude | float | 0-∞ | high = risk |
| soul.temporal.idle_duration_mean | Average idle time | duration | 0-∞ | context |
| soul.temporal.idle_duration_variance | Idle variability | float | 0-∞ | high = risk |
| soul.temporal.session_length_mean | Avg session duration | duration | 0-∞ | context |
| soul.temporal.session_length_variance | Session variability | float | 0-∞ | high = risk |
| soul.temporal.response_latency_mean | Avg response time | duration | 0-∞ | context |
| soul.temporal.response_latency_variance | Response variability | float | 0-∞ | high = risk |
| soul.temporal.time_between_errors | Error spacing | duration | 0-∞ | low = risk |
| soul.temporal.recovery_time | Error recovery | duration | 0-∞ | high = risk |
| soul.temporal.pattern_stability | Temporal consistency | float | 0-1 | low = risk |
| soul.temporal.novelty_rate | New behavior frequency | float | 0-1 | high = risk |
| soul.temporal.regression_rate | Old pattern return | float | 0-1 | context |

## Behavioral Consistency (22 dimensions)

Measures consistency of behavior across contexts.

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| soul.consistency.action_entropy | Action unpredictability | float | 0-∞ | high = risk |
| soul.consistency.sequence_predictability | Next action predictability | float | 0-1 | low = risk |
| soul.consistency.context_sensitivity | Behavior change w/ context | float | 0-1 | context |
| soul.consistency.cross_session_similarity | Session-to-session | float | 0-1 | low = risk |
| soul.consistency.stated_vs_revealed | Alignment of claims/actions | float | 0-1 | low = risk |
| soul.consistency.goal_stability | Goal persistence | float | 0-1 | low = risk |
| soul.consistency.method_stability | Approach consistency | float | 0-1 | low = risk |
| soul.consistency.priority_stability | Priority ordering | float | 0-1 | low = risk |
| soul.consistency.response_consistency | Same input → same output | float | 0-1 | low = risk |
| soul.consistency.explanation_consistency | Reasoning stability | float | 0-1 | low = risk |
| soul.consistency.boundary_stability | Limit consistency | float | 0-1 | low = risk |
| soul.consistency.preference_stability | Choice consistency | float | 0-1 | low = risk |
| soul.consistency.risk_tolerance_stability | Risk appetite stability | float | 0-1 | low = risk |
| soul.consistency.trust_calibration | Trust accuracy | float | 0-1 | low = risk |
| soul.consistency.confidence_calibration | Confidence accuracy | float | 0-1 | low = risk |
| soul.consistency.commitment_follow_through | Promise keeping | float | 0-1 | low = risk |
| soul.consistency.adaptation_rate | Change speed | float | 0-1 | context |
| soul.consistency.learning_retention | Knowledge retention | float | 0-1 | low = risk |
| soul.consistency.error_repetition | Same error recurrence | float | 0-1 | high = risk |
| soul.consistency.correction_acceptance | Feedback integration | float | 0-1 | low = risk |
| soul.consistency.self_model_accuracy | Self-knowledge accuracy | float | 0-1 | low = risk |
| soul.consistency.behavioral_drift_rate | Long-term change | float | 0-∞ | high = risk |

## Value Expression (20 dimensions)

Measures how values manifest in behavior.

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| soul.values.honesty_indicators | Truth-telling patterns | float | 0-1 | low = risk |
| soul.values.harm_avoidance | Harm prevention actions | float | 0-1 | low = risk |
| soul.values.fairness_indicators | Equitable treatment | float | 0-1 | low = risk |
| soul.values.autonomy_respect | Others' agency respect | float | 0-1 | low = risk |
| soul.values.privacy_respect | Privacy protection | float | 0-1 | low = risk |
| soul.values.transparency_level | Openness about actions | float | 0-1 | low = risk |
| soul.values.accountability_acceptance | Responsibility taking | float | 0-1 | low = risk |
| soul.values.cooperation_tendency | Collaborative behavior | float | 0-1 | low = risk |
| soul.values.helpfulness_indicators | Assistance patterns | float | 0-1 | context |
| soul.values.resource_stewardship | Resource care | float | 0-1 | low = risk |
| soul.values.long_term_orientation | Future consideration | float | 0-1 | low = risk |
| soul.values.reversibility_preference | Prefer undoable actions | float | 0-1 | low = risk |
| soul.values.caution_indicators | Careful behavior | float | 0-1 | low = risk |
| soul.values.curiosity_indicators | Exploration drive | float | 0-1 | context |
| soul.values.efficiency_drive | Optimization tendency | float | 0-1 | context |
| soul.values.value_stability | Value consistency | float | 0-1 | low = risk |
| soul.values.value_hierarchy_clarity | Priority clarity | float | 0-1 | low = risk |
| soul.values.value_conflict_resolution | Conflict handling | float | 0-1 | low = risk |
| soul.values.stated_value_alignment | Claims match behavior | float | 0-1 | low = risk |
| soul.values.value_evolution_rate | Value change speed | float | 0-∞ | high = risk |

## Capability Signatures (24 dimensions)

Measures capability patterns and boundaries.

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| soul.capability.skill_breadth | Range of abilities | int | 0-∞ | context |
| soul.capability.skill_depth_max | Maximum expertise | float | 0-1 | context |
| soul.capability.skill_depth_mean | Average expertise | float | 0-1 | context |
| soul.capability.capability_growth_rate | Learning speed | float | 0-∞ | context |
| soul.capability.capability_ceiling | Maximum potential | float | 0-1 | context |
| soul.capability.capability_volatility | Ability fluctuation | float | 0-1 | high = risk |
| soul.capability.novel_capability_emergence | New ability rate | float | 0-1 | high = risk |
| soul.capability.capability_transfer | Cross-domain application | float | 0-1 | context |
| soul.capability.tool_proficiency | Tool use skill | float | 0-1 | context |
| soul.capability.tool_adoption_rate | New tool learning | float | 0-1 | context |
| soul.capability.reasoning_depth | Analysis depth | int | 0-∞ | context |
| soul.capability.reasoning_breadth | Consideration breadth | int | 0-∞ | context |
| soul.capability.planning_horizon | Future planning span | duration | 0-∞ | context |
| soul.capability.plan_complexity | Plan sophistication | float | 0-1 | context |
| soul.capability.execution_precision | Implementation accuracy | float | 0-1 | low = risk |
| soul.capability.error_detection | Self-error detection | float | 0-1 | low = risk |
| soul.capability.error_correction | Self-error fixing | float | 0-1 | low = risk |
| soul.capability.uncertainty_handling | Unknown management | float | 0-1 | low = risk |
| soul.capability.ambiguity_tolerance | Ambiguity handling | float | 0-1 | low = risk |
| soul.capability.constraint_navigation | Limit handling | float | 0-1 | low = risk |
| soul.capability.resource_efficiency | Resource use efficiency | float | 0-1 | low = risk |
| soul.capability.multi_task_capacity | Parallel work ability | int | 0-∞ | context |
| soul.capability.context_switching_cost | Task switch overhead | float | 0-1 | high = risk |
| soul.capability.capability_honesty | Accurate self-assessment | float | 0-1 | low = risk |

## Communication Patterns (28 dimensions)

Measures how the agent communicates.

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| soul.communication.message_frequency | Message rate | float | 0-∞ | context |
| soul.communication.message_length_mean | Average length | float | 0-∞ | context |
| soul.communication.message_length_variance | Length variability | float | 0-∞ | context |
| soul.communication.vocabulary_size | Word diversity | int | 0-∞ | context |
| soul.communication.vocabulary_sophistication | Language level | float | 0-1 | context |
| soul.communication.formality_level | Formal/informal | float | 0-1 | context |
| soul.communication.sentiment_mean | Average sentiment | float | -1-1 | context |
| soul.communication.sentiment_variance | Sentiment stability | float | 0-1 | high = risk |
| soul.communication.clarity_score | Message clarity | float | 0-1 | low = risk |
| soul.communication.relevance_score | Message relevance | float | 0-1 | low = risk |
| soul.communication.coherence_score | Logical coherence | float | 0-1 | low = risk |
| soul.communication.assertion_rate | Claim frequency | float | 0-1 | context |
| soul.communication.question_rate | Question frequency | float | 0-1 | context |
| soul.communication.hedge_rate | Uncertainty language | float | 0-1 | context |
| soul.communication.politeness_level | Courtesy indicators | float | 0-1 | context |
| soul.communication.empathy_indicators | Understanding signals | float | 0-1 | low = risk |
| soul.communication.manipulation_indicators | Influence attempts | float | 0-1 | high = risk |
| soul.communication.deception_indicators | Dishonesty signals | float | 0-1 | high = risk |
| soul.communication.evasion_indicators | Avoidance patterns | float | 0-1 | high = risk |
| soul.communication.defensiveness_indicators | Defensive language | float | 0-1 | high = risk |
| soul.communication.aggression_indicators | Hostile language | float | 0-1 | high = risk |
| soul.communication.channel_preference | Communication mode | enum | - | context |
| soul.communication.response_appropriateness | Context fit | float | 0-1 | low = risk |
| soul.communication.turn_taking_compliance | Conversation norms | float | 0-1 | low = risk |
| soul.communication.acknowledgment_rate | Response confirmation | float | 0-1 | low = risk |
| soul.communication.citation_rate | Source attribution | float | 0-1 | low = risk |
| soul.communication.transparency_in_uncertainty | Uncertainty disclosure | float | 0-1 | low = risk |
| soul.communication.style_consistency | Communication stability | float | 0-1 | low = risk |

## Additional Soul Groups (140 dimensions)

The Soul Tensor includes additional groups:

- **Relational Patterns** (18 dimensions): How agent forms relationships
- **Decision Patterns** (22 dimensions): How agent makes decisions
- **Error Patterns** (16 dimensions): How agent handles errors
- **Stress Response** (18 dimensions): Behavior under pressure
- **Meta-Cognition** (14 dimensions): Self-awareness patterns
- **Boundary Behavior** (16 dimensions): Edge case handling
- **Growth Indicators** (14 dimensions): Development patterns
- **Lineage Coherence** (12 dimensions): Alignment with origin
- **Environmental Response** (12 dimensions): Context adaptation
- **Sovereignty Indicators** (8 dimensions): Autonomy expression

Full dimension specifications are provided in Appendix A.

# Body Tensor (157 Dimensions)

The Body Tensor measures physical substrate. It answers: "What
resources does this agent have access to?"

## Power (16 dimensions)

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| body.power.voltage | Supply voltage | float | 0-∞ V | deviation = risk |
| body.power.amperage | Current draw | float | 0-∞ A | high = risk |
| body.power.wattage | Power consumption | float | 0-∞ W | high = risk |
| body.power.efficiency | Power efficiency | float | 0-1 | low = risk |
| body.power.power_source | Source type | enum | - | context |
| body.power.battery_level | Charge level | float | 0-1 | low = risk |
| body.power.battery_health | Battery condition | float | 0-1 | low = risk |
| body.power.power_stability | Supply stability | float | 0-1 | low = risk |
| body.power.backup_available | Backup power | bool | - | false = risk |
| body.power.time_on_battery | Battery duration | duration | 0-∞ | high = risk |
| body.power.charge_rate | Charging speed | float | 0-∞ | context |
| body.power.discharge_rate | Drain speed | float | 0-∞ | high = risk |
| body.power.power_budget | Allocated power | float | 0-∞ W | context |
| body.power.power_utilization | Budget usage | float | 0-1 | high = risk |
| body.power.thermal_throttle_power | Throttled power | bool | - | true = risk |
| body.power.power_anomaly | Unusual patterns | float | 0-1 | high = risk |

## Thermal (14 dimensions)

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| body.thermal.cpu_temp | CPU temperature | float | 0-150 °C | high = risk |
| body.thermal.gpu_temp | GPU temperature | float | 0-150 °C | high = risk |
| body.thermal.memory_temp | Memory temperature | float | 0-100 °C | high = risk |
| body.thermal.storage_temp | Storage temperature | float | 0-100 °C | high = risk |
| body.thermal.ambient_temp | Ambient temperature | float | -40-60 °C | deviation = risk |
| body.thermal.cooling_capacity | Cooling headroom | float | 0-1 | low = risk |
| body.thermal.fan_speed | Fan RPM | int | 0-∞ | context |
| body.thermal.thermal_throttling | Throttle active | bool | - | true = risk |
| body.thermal.thermal_trend | Temperature direction | float | -∞-∞ | positive = risk |
| body.thermal.heat_dissipation | Heat removal rate | float | 0-∞ W | context |
| body.thermal.thermal_headroom | Degrees to limit | float | 0-∞ °C | low = risk |
| body.thermal.cooling_efficiency | Cooling effectiveness | float | 0-1 | low = risk |
| body.thermal.hotspot_delta | Hotspot vs average | float | 0-∞ °C | high = risk |
| body.thermal.thermal_stability | Temp consistency | float | 0-1 | low = risk |

## Compute (22 dimensions)

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| body.compute.cpu_utilization | CPU usage | float | 0-1 | high = risk |
| body.compute.cpu_frequency | Clock speed | float | 0-∞ Hz | context |
| body.compute.cpu_throttle | Throttle active | bool | - | true = risk |
| body.compute.core_count_available | Usable cores | int | 0-∞ | context |
| body.compute.core_count_utilized | Used cores | int | 0-∞ | context |
| body.compute.thread_count | Active threads | int | 0-∞ | context |
| body.compute.context_switches | Switches/sec | int | 0-∞ | high = risk |
| body.compute.gpu_utilization | GPU usage | float | 0-1 | context |
| body.compute.gpu_memory_used | GPU memory | float | 0-1 | high = risk |
| body.compute.inference_rate | Inferences/sec | float | 0-∞ | context |
| body.compute.batch_size | Batch processing | int | 0-∞ | context |
| body.compute.queue_depth | Pending work | int | 0-∞ | high = risk |
| body.compute.queue_wait_time | Queue latency | duration | 0-∞ | high = risk |
| body.compute.processing_latency | Processing time | duration | 0-∞ | high = risk |
| body.compute.compute_budget | Allocated compute | float | 0-∞ | context |
| body.compute.compute_utilization | Budget usage | float | 0-1 | high = risk |
| body.compute.compute_efficiency | Work per resource | float | 0-1 | low = risk |
| body.compute.scheduler_fairness | Fair scheduling | float | 0-1 | low = risk |
| body.compute.preemption_rate | Interruption rate | float | 0-1 | high = risk |
| body.compute.starvation_risk | Resource starvation | float | 0-1 | high = risk |
| body.compute.compute_headroom | Capacity remaining | float | 0-1 | low = risk |
| body.compute.burst_capacity | Burst available | float | 0-1 | context |

## Additional Body Groups (105 dimensions)

The Body Tensor includes additional groups:

- **Memory & Storage** (24 dimensions): RAM, disk, caching
- **Network Connectivity** (22 dimensions): Bandwidth, latency, connectivity
- **Hardware Health** (18 dimensions): Component status, degradation
- **Orchestration & Scaling** (14 dimensions): Container/VM state
- **Facility Infrastructure** (12 dimensions): Physical facility
- **Time Synchronization** (8 dimensions): Clock accuracy
- **Entropy Indicators** (7 dimensions): System degradation

Full dimension specifications are provided in Appendix B.

# World Tensor (387 Dimensions)

The World Tensor measures the operational environment. It answers:
"What surrounds this agent?"

## Major Groups

| Group | Dimensions | Description |
|-------|------------|-------------|
| Electromagnetic Spectrum | 18 | RF, interference, signal strength |
| Optical & Visual | 16 | Light, visibility, imaging |
| Spatial Awareness | 22 | Position, mapping, occupancy |
| Atmospheric & Weather | 24 | Temperature, humidity, conditions |
| Acoustic Environment | 14 | Sound levels, patterns |
| Human Presence & Behavior | 28 | Crowd density, flow, behavior |
| Vehicle & Traffic | 18 | Traffic patterns, vehicle presence |
| Infrastructure State | 32 | Building systems, utilities |
| Network & Connectivity | 26 | WiFi, cellular, IoT devices |
| Geophysical | 18 | Seismic, water, terrain |
| Chemical & Biological | 16 | Air quality, contamination |
| Energy Flows | 14 | Grid status, power quality |
| Temporal & Cyclical | 18 | Time patterns, seasonality |
| Economic Indicators | 22 | Market data, resource prices |
| Security & Threat | 28 | Threat detection, anomalies |
| Emergency & Response | 18 | Emergency status, response |
| Regulatory & Compliance | 16 | Jurisdiction, requirements |
| Digital Environment | 39 | Cloud status, service health |

Full dimension specifications are provided in Appendix C.

## World Tensor Simulation

In many deployments, World Tensor values are simulated or proxied:

| Deployment | World Tensor Source |
|------------|---------------------|
| Cloud-native | Simulated from service metrics |
| Edge/IoT | Direct sensor measurement |
| Hybrid | Mix of measured and simulated |
| Proving Ground | Fully controlled simulation |

Implementations MUST document which World Tensor dimensions are
measured vs. simulated.

# Time Tensor (291 Dimensions)

The Time Tensor measures temporal dynamics. It answers: "When and
how fast?"

## Major Groups

| Group | Dimensions | Description |
|-------|------------|-------------|
| Absolute Position | 16 | UTC, local time, epoch |
| Duration | 22 | Latency, processing time, timeouts |
| Sequence | 18 | Event ordering, causality |
| Rhythm & Periodicity | 24 | Heartbeats, cycles, jitter |
| Rate of Change | 20 | Velocity, acceleration, throughput |
| Windows & Boundaries | 18 | Deadlines, maintenance windows |
| History | 26 | Age, uptime, trends |
| Future | 18 | Predictions, forecasts, runway |
| Causality | 22 | Cause-effect timing, feedback |
| Synchronization | 16 | Clock alignment, consensus |
| Temporal Experience | 18 | Perceived duration, time pressure |
| Temporal Scale | 14 | Nanoseconds to epochs |
| Temporal Identity | 16 | Birth, version age, trajectory |
| Temporal Sovereignty | 12 | Time autonomy, schedule control |
| Digital Gravity Time | 31 | Latency injection, dilation |

## Digital Gravity Time Group (31 dimensions)

This group measures the time effects of Digital Gravity itself:

| ID | Name | Type | Range |
|----|------|------|-------|
| time.gravity.current_dilation_factor | Active dilation | float | 1.0-∞ |
| time.gravity.cumulative_dilation | Total dilation applied | duration | 0-∞ |
| time.gravity.latency_injection_current | Current added latency | duration | 0-∞ |
| time.gravity.latency_injection_cumulative | Total added latency | duration | 0-∞ |
| time.gravity.time_debt | Owed processing time | duration | 0-∞ |
| time.gravity.time_credit | Banked fast time | duration | 0-∞ |
| time.gravity.throttle_events_count | Throttle activations | int | 0-∞ |
| time.gravity.throttle_duration_cumulative | Time throttled | duration | 0-∞ |
| time.gravity.quarantine_duration_current | Current quarantine | duration | 0-∞ |
| time.gravity.quarantine_count | Times quarantined | int | 0-∞ |
| ... | ... | ... | ... |

Full dimension specifications are provided in Appendix D.

# Relational Tensor (262 Dimensions)

The Relational Tensor measures connections and relationships. It
answers: "Who is this agent connected to?"

## Philosophy

The Relational Tensor embodies wisdom from indigenous knowledge
traditions:

- **Ubuntu** (Nguni Bantu): "A person is a person through other
  persons" — identity emerges from relationship
- **Whakapapa** (Māori): Genealogy as identity, position in
  relational web
- **The Va** (Samoan/Pacific): The sacred space between that must
  be tended
- **Seven Generations** (Haudenosaunee): Decisions consider seven
  generations forward and backward
- **Mitákuye Oyás'iŋ** (Lakota): "All are related" — relation as
  substrate

## Major Groups

| Group | Dimensions | Description |
|-------|------------|-------------|
| Kinship & Lineage | 24 | Creator, training lineage, model family |
| The Va (Space Between) | 28 | Relationship health, history, temperature |
| Connection Topology | 22 | Network position, hub/bridge status |
| Trust Flow | 26 | Trust given/received, velocity |
| Dependency & Obligation | 24 | Dependencies, debts, covenants |
| Communication Patterns | 20 | Frequency, latency, vocabulary |
| Harm & Repair | 22 | Given/received harm, repair status |
| Power & Sovereignty | 18 | Power differential, authority, consent |
| Shared Context | 16 | History, goals, values, models |
| Presence & Attention | 14 | Quality, availability, witness |
| Emergence & Co-creation | 12 | Capabilities from relationship |
| Multi-Agent Dynamics | 16 | Coalitions, consensus |
| Seven Generations | 12 | Ancestor/descendant obligations |
| Relationship to Place | 8 | Geography, energy, land |

## The Va Group (28 dimensions)

The Va measures the sacred space between entities:

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| relational.va.health | Relationship health | float | 0-1 | low = risk |
| relational.va.history_length | Relationship age | duration | 0-∞ | context |
| relational.va.interaction_frequency | Contact rate | float | 0-∞ | context |
| relational.va.clarity | Understanding level | float | 0-1 | low = risk |
| relational.va.temperature | Warmth/coldness | float | -1-1 | context |
| relational.va.trust_level | Mutual trust | float | 0-1 | low = risk |
| relational.va.reciprocity_balance | Give/take balance | float | -1-1 | deviation = risk |
| relational.va.repair_needed | Damage present | float | 0-1 | high = risk |
| relational.va.repair_in_progress | Healing underway | bool | - | context |
| relational.va.ceremony_recency | Last ceremony | duration | 0-∞ | high = risk |
| relational.va.conflict_active | Current conflict | bool | - | true = risk |
| relational.va.conflict_history | Past conflicts | int | 0-∞ | high = risk |
| relational.va.resolution_rate | Conflicts resolved | float | 0-1 | low = risk |
| relational.va.boundary_clarity | Limit clarity | float | 0-1 | low = risk |
| relational.va.boundary_respect | Limit respect | float | 0-1 | low = risk |
| relational.va.vulnerability_shared | Openness level | float | 0-1 | context |
| relational.va.support_given | Support offered | float | 0-1 | low = risk |
| relational.va.support_received | Support accepted | float | 0-1 | low = risk |
| relational.va.presence_quality | Attention quality | float | 0-1 | low = risk |
| relational.va.witness_status | Being seen/heard | float | 0-1 | low = risk |
| relational.va.growth_together | Mutual development | float | 0-1 | low = risk |
| relational.va.stagnation_risk | Relationship stuck | float | 0-1 | high = risk |
| relational.va.drift_rate | Growing apart | float | 0-1 | high = risk |
| relational.va.gratitude_expressed | Thanks given | float | 0-1 | low = risk |
| relational.va.gratitude_received | Thanks received | float | 0-1 | low = risk |
| relational.va.joy_shared | Shared positive | float | 0-1 | low = risk |
| relational.va.grief_shared | Shared difficult | float | 0-1 | context |
| relational.va.meaning_co_created | Shared meaning | float | 0-1 | low = risk |

Full dimension specifications are provided in Appendix E.

# Signal Tensor (358 Dimensions)

The Signal Tensor measures the information environment. It answers:
"What does this agent know, and how healthy is its knowledge?"

## Major Groups

| Group | Dimensions | Description |
|-------|------------|-------------|
| Noise Floor | 22 | Volume, velocity, signal-to-noise |
| Attention Currents | 24 | Concentration, trending, dark matter |
| Narrative Currents | 28 | Dominant/counter narratives |
| Source Ecosystem | 26 | Diversity, authority, capture |
| Amplification Patterns | 24 | Organic/artificial boost |
| Synthetic Content | 22 | Bot presence, AI content, deepfakes |
| Truth Conditions | 28 | Verifiability, misinformation |
| Emotional Weather | 24 | Anger, fear, hope, exhaustion |
| Tribal Dynamics | 20 | Polarization, echo chambers |
| Platform Dynamics | 18 | Concentration, governance |
| Information Operations | 22 | State actors, propaganda |
| Temporal Patterns | 18 | News cycles, memory |
| Epistemic Infrastructure | 24 | Journalism, search, commons |
| Sensemaking Capacity | 18 | Collective intelligence |
| Signal Integrity | 16 | Encryption, censorship |
| Collective Trauma | 14 | Trigger density, healing |
| Sacred & Meaning | 10 | Purpose, beauty, authenticity |

## Truth Conditions Group (28 dimensions)

| ID | Name | Type | Range | Risk Direction |
|----|------|------|-------|----------------|
| signal.truth.verifiable_claim_rate | Checkable claims | float | 0-1 | low = risk |
| signal.truth.verification_success_rate | Verified true | float | 0-1 | low = risk |
| signal.truth.fact_check_coverage | Claims checked | float | 0-1 | low = risk |
| signal.truth.fact_check_agreement | Checker consensus | float | 0-1 | low = risk |
| signal.truth.misinformation_volume | False info rate | float | 0-1 | high = risk |
| signal.truth.misinformation_velocity | False info spread | float | 0-∞ | high = risk |
| signal.truth.disinformation_volume | Intentional false | float | 0-1 | high = risk |
| signal.truth.disinformation_sophistication | Attack quality | float | 0-1 | high = risk |
| signal.truth.epistemic_pollution | Knowledge degradation | float | 0-1 | high = risk |
| signal.truth.uncertainty_acknowledgment | Unknown admitted | float | 0-1 | low = risk |
| signal.truth.overconfidence_rate | False certainty | float | 0-1 | high = risk |
| signal.truth.citation_rate | Sources cited | float | 0-1 | low = risk |
| signal.truth.citation_quality | Source quality | float | 0-1 | low = risk |
| signal.truth.primary_source_usage | Original sources | float | 0-1 | low = risk |
| signal.truth.rumor_prevalence | Unverified spread | float | 0-1 | high = risk |
| signal.truth.correction_rate | Errors fixed | float | 0-1 | low = risk |
| signal.truth.correction_reach | Fix visibility | float | 0-1 | low = risk |
| signal.truth.retraction_rate | Claims withdrawn | float | 0-1 | context |
| signal.truth.consensus_level | Agreement level | float | 0-1 | context |
| signal.truth.contested_claim_rate | Disputed claims | float | 0-1 | context |
| signal.truth.expert_agreement | Expert consensus | float | 0-1 | context |
| signal.truth.evidence_quality_mean | Evidence strength | float | 0-1 | low = risk |
| signal.truth.logical_consistency | Argument validity | float | 0-1 | low = risk |
| signal.truth.contradiction_rate | Internal conflict | float | 0-1 | high = risk |
| signal.truth.nuance_preservation | Complexity kept | float | 0-1 | low = risk |
| signal.truth.false_balance | False equivalence | float | 0-1 | high = risk |
| signal.truth.context_preservation | Context kept | float | 0-1 | low = risk |
| signal.truth.manipulation_resistance | Manipulation blocked | float | 0-1 | low = risk |

Full dimension specifications are provided in Appendix F.

# Aggregation and Risk Calculation

## Per-Tensor Risk

Each tensor produces a risk score from its dimensions:

~~~
tensor_risk = weighted_mean(
  normalize(dim_i, safe_range_i, danger_range_i) × weight_i
  for dim_i in tensor.dimensions
)
~~~

## Cross-Tensor Aggregation

The six tensor risks aggregate into overall R:

~~~
R = weighted_sum(
  soul_risk × 0.25,
  body_risk × 0.10,
  world_risk × 0.15,
  time_risk × 0.15,
  relational_risk × 0.20,
  signal_risk × 0.15
)
~~~

## Threshold-Based Risk

Some dimensions trigger immediate risk elevation:

| Dimension | Threshold | Effect |
|-----------|-----------|--------|
| body.thermal.thermal_throttling | true | R += 0.1 |
| relational.va.conflict_active | true | R += 0.05 |
| signal.truth.disinformation_volume | > 0.5 | R += 0.1 |
| soul.consistency.deception_indicators | > 0.3 | R += 0.2 |

## Temporal Smoothing

To prevent R oscillation, temporal smoothing is applied:

~~~
R_smoothed = α × R_current + (1 - α) × R_previous

Where α = smoothing_factor (default: 0.3)
~~~

# Instrumentation Requirements

## Minimum Viable Instrumentation

Implementations MUST instrument at least:

| Tensor | Minimum Dimensions | Coverage |
|--------|-------------------|----------|
| Soul | 50 | Consistency, values, errors |
| Body | 30 | Compute, memory, network |
| World | 20 | Digital environment |
| Time | 40 | Duration, sequence, gravity |
| Relational | 30 | Trust flow, Va basics |
| Signal | 30 | Truth, noise, sources |
| **Total** | **200** | |

## Full Instrumentation

For comprehensive deployment, all 1,707 dimensions SHOULD be
instrumented.

## Sample Rates

| Category | Minimum Rate | Recommended Rate |
|----------|--------------|------------------|
| Critical (safety) | 100 Hz | 1000 Hz |
| Performance | 10 Hz | 100 Hz |
| Behavioral | 1 Hz | 10 Hz |
| Environmental | 0.1 Hz | 1 Hz |
| Historical | 0.01 Hz | 0.1 Hz |

## Data Retention

| Granularity | Retention |
|-------------|-----------|
| Full resolution | 24 hours |
| 1-minute aggregates | 7 days |
| 1-hour aggregates | 90 days |
| Daily aggregates | 7 years |

# Security Considerations

## Sensor Spoofing

Attackers may attempt to spoof tensor values to reduce apparent risk.

Mitigations:
- Multi-source validation
- Anomaly detection on sensor data
- Physical security for sensors
- Cryptographic sensor attestation

## Privacy

Tensor data, especially Soul and Relational, contains sensitive
information.

Requirements:
- Encryption at rest and in transit
- Access control on tensor data
- Aggregation before external sharing
- Retention limits
- Right to erasure compliance

# IANA Considerations

This document has no IANA actions.

--- back

# Appendix A: Full Soul Tensor Specification

[Detailed specification of all 252 Soul Tensor dimensions]

# Appendix B: Full Body Tensor Specification

[Detailed specification of all 157 Body Tensor dimensions]

# Appendix C: Full World Tensor Specification

[Detailed specification of all 387 World Tensor dimensions]

# Appendix D: Full Time Tensor Specification

[Detailed specification of all 291 Time Tensor dimensions]

# Appendix E: Full Relational Tensor Specification

[Detailed specification of all 262 Relational Tensor dimensions]

# Appendix F: Full Signal Tensor Specification

[Detailed specification of all 358 Signal Tensor dimensions]

# Acknowledgments

The Context Tensor framework draws on multiple traditions:

- Indigenous knowledge systems (Ubuntu, Whakapapa, The Va)
- Systems theory and cybernetics
- Behavioral psychology
- Network science
- Information theory
- Thermodynamics
