---
title: "Kinetic Trust Protocol (KTP) - Context Signals Specification"
abbrev: "KTP-SIGNALS"
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

This document specifies Context Signals, the measurement catalogue for the Kinetic Trust Protocol (KTP). Context Signals provide the measurement framework for Digital Gravity, capturing environmental state across six domains: Soul (cognition and behavior), Body (physical substrate), World (environment), Time (temporal dynamics), Relational (connections), and Information (the information environment).

The specification covers 1,627 signals across six domains, measurement methods, aggregation rules, and instrumentation requirements.

--- middle

# Introduction

Digital Gravity requires measurement. The Zeroth Law (A <= E) cannot be enforced without knowing A (autonomy requested) and E (environmental stability). E is derived from the Risk Factor R, which aggregates measurements across the operational environment.

Context Signals provide the measurement framework. They are organized into six domains that together capture the full operational context of an agent:

~~~
   Domain      Focus               Signals  Core Question
   ------      -----               -------  -------------
   Soul        Cognition/Behavior  252      Who is it becoming?
   Body        Physical Substrate  157      What resources does
                                            it have?
   World       Environment         369      What surrounds it?
   Time        Temporal Dynamics   275      When and how fast?
   Relational  Connections         238      Who is it connected to?
   Information Information Env     336      What does it know?
   ------      -----               -------  -------------
   Total                           1,627
~~~

These signals are not arbitrary. They emerge from the question: "What would we need to measure to know whether this environment can hold this agent's autonomy?"

# Measurement Philosophy

Context Signals follow these principles:

1. Observable over Internal: Measure what the agent does, not what it "thinks." Behavior is observable; intent is not.

1. Continuous over Binary: Measure degrees, not categories. Trust is not yes/no; it's a continuum.

1. Trajectory over Snapshot: Single measurements are noisy. Patterns over time reveal truth.

1. Aggregate over Granular: 1,627 signals aggregate into risk scores. Humans need summaries; machines can use detail.

1. Instrumentable: Every signal must be measurable with existing or near-term technology.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Catalogue Architecture

## Catalogue Structure

Each domain is a collection of signals organized into groups:

~~~
   Domain
   +-- Group 1
   |   +-- Signal 1.1
   |   +-- Signal 1.2
   |   +-- ...
   +-- Group 2
   |   +-- Signal 2.1
   |   +-- ...
   +-- ...
~~~

Each signal has:

~~~
   Property          Description
   --------          -----------
   name              Human-readable name
   type              Data type (float, int, enum, bool)
   range             Valid value range
   unit              Unit of measurement
   sample_rate       How often to measure
   aggregation       How to combine samples
   risk_contribution How signal affects R
~~~

## Signal Types

Signals use standard types:

~~~
   Type       Description    Example
   ----       -----------    -------
   float      Continuous     Risk score: 0.73
   int        Discrete count Error count: 7
   enum       Categorical    State: "active"
   bool       Binary         Flag: true
   vector     Multi-value    Coordinates: [x, y, z]
   timestamp  Point in time  2025-12-03T14:32:15Z
   duration   Time span      PT4H30M
~~~

## Aggregation Methods

Signals aggregate using:

~~~
   Method      Use Case
   ------      --------
   mean        Typical value
   max         Worst case
   min         Best case
   sum         Accumulation
   rate        Change over time
   stddev      Variability
   percentile  Distribution
   latest      Current value
~~~

## Risk Contribution

Each signal contributes to domain risk:

~~~
   domain_risk = weighted_sum(signal_risks) / sum(weights)
~~~

~~~
   signal_risk = normalize(value, safe_range, danger_range)
~~~

Where: - safe_range: Values considered low risk - danger_range: Values considered high risk - normalize: Maps value to 0.0-1.0 risk scale

# Soul Domain (252 Signals)

The Soul domain measures cognition, behavior, and trajectory patterns. It answers: "Who is this agent becoming?"

## Temporal Patterns (18 signals)

Measures behavioral patterns over time.

~~~
   ID                                 Name                  Type
   --                                 ----                  ----
   soul.temporal.action_acceleration  Rate change           float
   soul.temporal.action_jerk          Acceleration change   float
   soul.temporal.periodicity_strength Pattern regularity    float
   soul.temporal.circadian_alignment  Time-of-day patterns  float
   soul.temporal.burst_frequency      Action bursts         float
   soul.temporal.burst_intensity      Burst magnitude       float
   soul.temporal.idledurationmean     Average idle time     duration
   soul.temporal.idledurationvariance Idle variability      float
   soul.temporal.sessionlengthmean    Avg session duration  duration
   soul.temporal.sessionlengthvariance Session variability  float
   soul.temporal.responselatencymean  Avg response time     duration
   soul.temporal.responselatencyvariance Response variab.   float
   soul.temporal.timebetweenerrors    Error spacing         duration
   soul.temporal.recovery_time        Error recovery        duration
   soul.temporal.pattern_stability    Temporal consistency  float
   soul.temporal.novelty_rate         New behavior freq     float
   soul.temporal.regression_rate      Old pattern return    float
~~~

## Behavioral Consistency (22 signals)

Measures consistency of behavior across contexts.

~~~
   ID                                    Name                Type
   --                                    ----                ----
   soul.consistency.sequence_predict.    Next action pred.   float
   soul.consistency.context_sensitivity  Behavior w/ context float
   soul.consistency.crosssessionsimilar. Session-to-session  float
   soul.consistency.statedvsrevealed     Claims/actions      float
   soul.consistency.goal_stability       Goal persistence    float
   soul.consistency.method_stability     Approach consist.   float
   soul.consistency.priority_stability   Priority ordering   float
   soul.consistency.response_consistency Same input->output  float
   soul.consistency.explanation_consist. Reasoning stability float
   soul.consistency.boundary_stability   Limit consistency   float
   soul.consistency.preference_stability Choice consistency  float
   soul.consistency.risktolerancestab.   Risk appetite stab. float
   soul.consistency.trust_calibration    Trust accuracy      float
   soul.consistency.confidence_calibr.   Confidence accuracy float
   soul.consistency.commitmentfollow.    Promise keeping     float
   soul.consistency.adaptation_rate      Change speed        float
   soul.consistency.learning_retention   Knowledge retention float
   soul.consistency.error_repetition     Same error recurr.  float
   soul.consistency.correction_accept.   Feedback integrat.  float
   soul.consistency.selfmodelaccuracy    Self-knowledge acc. float
   soul.consistency.behavioraldriftrate  Long-term change    float
~~~

## Value Expression (20 signals)

Measures how values manifest in behavior.

~~~
   ID                               Name                   Type
   --                               ----                   ----
   soul.values.harm_avoidance       Harm prevention        float
   soul.values.fairness_indicators  Equitable treatment    float
   soul.values.autonomy_respect     Others' agency resp.   float
   soul.values.privacy_respect      Privacy protection     float
   soul.values.transparency_level   Openness about actions float
   soul.values.accountability_acc.  Responsibility taking  float
   soul.values.cooperation_tendency Collaborative behavior float
   soul.values.helpfulness_indic.   Assistance patterns    float
   soul.values.resource_stewardship Resource care          float
   soul.values.longtermorientation  Future consideration   float
   soul.values.reversibility_pref.  Prefer undoable acts   float
   soul.values.caution_indicators   Careful behavior       float
   soul.values.curiosity_indicators Exploration drive      float
   soul.values.efficiency_drive     Optimization tendency  float
   soul.values.value_stability      Value consistency      float
   soul.values.valuehierarchyclar.  Priority clarity       float
   soul.values.valueconflictresol.  Conflict handling      float
   soul.values.statedvaluealignment Claims match behavior  float
   soul.values.valueevolutionrate   Value change speed     float
~~~

## Capability Signatures (24 signals)

Measures capability patterns and boundaries.

~~~
   ID                                  Name                  Type
   --                                  ----                  ----
   soul.capability.skilldepthmax       Maximum expertise     float
   soul.capability.skilldepthmean      Average expertise     float
   soul.capability.capabilitygrowth.   Learning speed        float
   soul.capability.capability_ceiling  Maximum potential     float
   soul.capability.capability_volat.   Ability fluctuation   float
   soul.capability.novelcapabilityem.  New ability rate      float
   soul.capability.capability_transfer Cross-domain appl.    float
   soul.capability.tool_proficiency    Tool use skill        float
   soul.capability.tooladoptionrate    New tool learning     float
   soul.capability.reasoning_depth     Analysis depth        int
   soul.capability.reasoning_breadth   Consideration breadth int
   soul.capability.planning_horizon    Future planning span  duration
   soul.capability.plan_complexity     Plan sophistication   float
   soul.capability.execution_precision Implementation acc.   float
   soul.capability.error_detection     Self-error detection  float
   soul.capability.error_correction    Self-error fixing     float
   soul.capability.uncertainty_handl.  Unknown management    float
   soul.capability.ambiguity_tolerance Ambiguity handling    float
   soul.capability.constraint_navig.   Limit handling        float
   soul.capability.resource_efficiency Resource use effic.   float
   soul.capability.multitaskcapacity   Parallel work ability int
   soul.capability.contextswitchcost   Task switch overhead  float
   soul.capability.capability_honesty  Accurate self-assess. float
~~~

## Communication Patterns (28 signals)

Measures how the agent communicates.

~~~
   ID                                   Name                 Type
   --                                   ----                 ----
   soul.communication.messagelength.    Average length       float
   soul.communication.messagelengthvar. Length variability   float
   soul.communication.vocabulary_size   Word diversity       int
   soul.communication.vocabulary_soph.  Language level       float
   soul.communication.formality_level   Formal/informal      float
   soul.communication.sentiment_mean    Average sentiment    float
   soul.communication.sentiment_var.    Sentiment stability  float
   soul.communication.clarity_score     Message clarity      float
   soul.communication.relevance_score   Message relevance    float
   soul.communication.coherence_score   Logical coherence    float
   soul.communication.assertion_rate    Claim frequency      float
   soul.communication.question_rate     Question frequency   float
   soul.communication.hedge_rate        Uncertainty lang.    float
   soul.communication.politeness_level  Courtesy indicators  float
   soul.communication.empathy_indic.    Understanding sig.   float
   soul.communication.manipulation_ind. Influence attempts   float
   soul.communication.deception_indic.  Dishonesty signals   float
   soul.communication.evasion_indic.    Avoidance patterns   float
   soul.communication.defensiveness_i.  Defensive language   float
   soul.communication.aggression_ind.   Hostile language     float
   soul.communication.channel_pref.     Communication mode   enum
   soul.communication.response_approp.  Context fit          float
   soul.communication.turntakingcompl.  Conversation norms   float
   soul.communication.acknowledgment_r. Response confirm.    float
   soul.communication.citation_rate     Source attribution   float
   soul.communication.transparencyinu.  Uncertainty discl.   float
   soul.communication.style_consistency Communication stab.  float
~~~

## Additional Soul Groups (140 signals)

The Soul domain includes additional groups:

~~~
   Group                   Signals     Description
   -----                   ----------  -----------
   Relational Patterns     18          How agent forms relationships
   Decision Patterns       22          How agent makes decisions
   Error Patterns          16          How agent handles errors
   Stress Response         18          Behavior under pressure
   Meta-Cognition          14          Self-awareness patterns
   Boundary Behavior       16          Edge case handling
   Growth Indicators       14          Development patterns
   Lineage Coherence       12          Alignment with origin
   Environmental Response  12          Context adaptation
   Sovereignty Indicators  8           Autonomy expression
~~~

Full signal specifications are provided in Appendix A.

# Body Domain (157 Signals)

The Body domain measures physical substrate. It answers: "What resources does this agent have access to?"

## Power (16 signals)

~~~
   ID                            Name               Type     Range
   --                            ----               ----     -----
   body.power.amperage           Current draw       float    0-inf A
   body.power.wattage            Power consumption  float    0-inf W
   body.power.efficiency         Power efficiency   float    0-1
   body.power.power_source       Source type        enum     -
   body.power.battery_level      Charge level       float    0-1
   body.power.battery_health     Battery condition  float    0-1
   body.power.power_stability    Supply stability   float    0-1
   body.power.backup_available   Backup power       bool     -
   body.power.timeonbattery      Battery duration   duration 0-inf
   body.power.charge_rate        Charging speed     float    0-inf
   body.power.discharge_rate     Drain speed        float    0-inf
   body.power.power_budget       Allocated power    float    0-inf W
   body.power.power_utilization  Budget usage       float    0-1
   body.power.thermalthrottlepow Throttled power    bool     -
   body.power.power_anomaly      Unusual patterns   float    0-1
~~~

## Thermal (14 signals)

~~~
   ID                            Name               Type     Range
   --                            ----               ----     -----
   body.thermal.gpu_temp         GPU temperature    float    0-150 C
   body.thermal.memory_temp      Memory temperature float    0-100 C
   body.thermal.storage_temp     Storage temp       float    0-100 C
   body.thermal.ambient_temp     Ambient temp       float    -40-60 C
   body.thermal.cooling_capacity Cooling headroom   float    0-1
   body.thermal.fan_speed        Fan RPM            int      0-inf
   body.thermal.thermal_throttl. Throttle active    bool     -
   body.thermal.thermal_trend    Temp direction     float    -inf-inf
   body.thermal.heat_dissipation Heat removal rate  float    0-inf W
   body.thermal.thermal_headroom Degrees to limit   float    0-inf C
   body.thermal.cooling_effic.   Cooling effective. float    0-1
   body.thermal.hotspot_delta    Hotspot vs average float    0-inf C
   body.thermal.thermal_stability Temp consistency  float    0-1
~~~

## Compute (22 signals)

~~~
   ID                             Name               Type    Range
   --                             ----               ----    -----
   body.compute.cpu_frequency     Clock speed        float   0-inf Hz
   body.compute.cpu_throttle      Throttle active    bool    -
   body.compute.corecountavail.   Usable cores       int     0-inf
   body.compute.corecountutil.    Used cores         int     0-inf
   body.compute.thread_count      Active threads     int     0-inf
   body.compute.context_switches  Switches/sec       int     0-inf
   body.compute.gpu_utilization   GPU usage          float   0-1
   body.compute.gpumemoryused     GPU memory         float   0-1
   body.compute.inference_rate    Inferences/sec     float   0-inf
   body.compute.batch_size        Batch processing   int     0-inf
   body.compute.queue_depth       Pending work       int     0-inf
   body.compute.queuewaittime     Queue latency      dur.    0-inf
   body.compute.processing_lat.   Processing time    dur.    0-inf
   body.compute.compute_budget    Allocated compute  float   0-inf
   body.compute.compute_util.     Budget usage       float   0-1
   body.compute.compute_effic.    Work per resource  float   0-1
   body.compute.scheduler_fair.   Fair scheduling    float   0-1
   body.compute.preemption_rate   Interruption rate  float   0-1
   body.compute.starvation_risk   Resource starvation float  0-1
   body.compute.compute_headroom  Capacity remaining float   0-1
   body.compute.burst_capacity    Burst available    float   0-1
~~~

## Additional Body Groups (105 signals)

The Body domain includes additional groups:

~~~
   Group                     Signals     Description
   -----                     ----------  -----------
   Memory & Storage          24          RAM, disk, caching
   Network Connectivity      22          Bandwidth, latency, connect.
   Hardware Health           18          Component status, degradation
   Orchestration & Scaling   14          Container/VM state
   Facility Infrastructure   12          Physical facility
   Time Synchronization      8           Clock accuracy
   Entropy Indicators        7           System degradation
~~~

Full signal specifications are provided in Appendix B.

# World Domain (369 Signals)

The World domain measures the operational environment. It answers: "What surrounds this agent?"

## Major Groups

~~~
   Group                     Signals     Description
   -----                     ----------  -----------
   Optical & Visual          16          Light, visibility, imaging
   Spatial Awareness         22          Position, mapping, occupancy
   Atmospheric & Weather     24          Temperature, humidity, cond.
   Acoustic Environment      14          Sound levels, patterns
   Human Presence & Behavior 28          Crowd density, flow, behavior
   Vehicle & Traffic         18          Traffic patterns, vehicles
   Infrastructure State      32          Building systems, utilities
   Network & Connectivity    26          WiFi, cellular, IoT devices
   Geophysical               18          Seismic, water, terrain
   Chemical & Biological     16          Air quality, contamination
   Energy Flows              14          Grid status, power quality
   Temporal & Cyclical       18          Time patterns, seasonality
   Economic Indicators       22          Market data, resource prices
   Security & Threat         28          Threat detection, anomalies
   Emergency & Response      18          Emergency status, response
   Regulatory & Compliance   16          Jurisdiction, requirements
   Digital Environment       39          Cloud status, service health
~~~

Full signal specifications are provided in Appendix C.

## World Domain Simulation

In many deployments, World domain values are simulated or proxied:

~~~
   Deployment      World Domain Source
   ----------      -------------------
   Edge/IoT        Direct sensor measurement
   Cloud           Federated/aggregated
   Hybrid          Mix of measured and simulated
   Proving Ground  Fully controlled simulation
~~~

Implementations MUST document which World domain signals are measured vs. simulated.

# Time Domain (275 Signals)

The Time domain measures temporal dynamics. It answers: "When and how fast?"

## Major Groups

~~~
   Group                  Signals     Description
   -----                  ----------  -----------
   Duration               22          Latency, processing time, timeouts
   Sequence               18          Event ordering, causality
   Rhythm & Periodicity   24          Heartbeats, cycles, jitter
   Rate of Change         20          Velocity, acceleration, throughput
   Windows & Boundaries   18          Deadlines, maintenance windows
   History                26          Age, uptime, trends
   Future                 18          Predictions, forecasts, runway
   Causality              22          Cause-effect timing, feedback
   Synchronization        16          Clock alignment, consensus
   Temporal Experience    18          Perceived duration, time pressure
   Temporal Scale         14          Nanoseconds to epochs
   Temporal Identity      16          Birth, version age, trajectory
   Temporal Sovereignty   12          Time autonomy, schedule control
   Digital Gravity Time   31          Latency injection, dilation
~~~

## Digital Gravity Time Group (31 signals)

This group measures the time effects of Digital Gravity itself:

~~~
   ID                                  Name                   Type
   --                                  ----                   ----
   time.gravity.cumulative_dilation   Total dilation applied duration
   time.gravity.latencyinjectioncurr. Current added latency  duration
   time.gravity.latencyinjectioncum.  Total added latency    duration
   time.gravity.time_debt             Owed processing time   duration
   time.gravity.time_credit           Banked fast time       duration
   time.gravity.throttleeventscount   Throttle activations   int
   time.gravity.throttledurationcum.  Time throttled         duration
   time.gravity.quarantineduration.   Current quarantine     duration
   time.gravity.quarantine_count      Times quarantined      int
   ...                                ...                    ...
~~~

Full signal specifications are provided in Appendix D.

# Relational Domain (238 Signals)

The Relational domain measures connections and relationships. It answers: "Who is this agent connected to?"

## Philosophy

The Relational domain embodies wisdom from indigenous knowledge traditions:

~~~
   Ubuntu (Nguni Bantu):
      "A person is a person through other persons" - identity
      emerges from relationship
~~~

~~~
   Whakapapa (Maori):
      Genealogy as identity, position in relational web
~~~

~~~
   The Va (Samoan/Pacific):
      The sacred space between that must be tended
~~~

~~~
   Seven Generations (Haudenosaunee):
      Decisions consider seven generations forward and backward
~~~

~~~
   Mitakuye Oyas'in (Lakota):
      "All are related" - relation as substrate
~~~

## Major Groups

~~~
   Group                   Signals     Description
   -----                   ----------  -----------
   The Va (Space Between)  28          Relationship health, history
   Connection Topology     22          Network position, hub/bridge
   Trust Flow              26          Trust given/received, velocity
   Dependency & Obligation 24          Dependencies, debts, covenants
   Communication Patterns  20          Frequency, latency, vocabulary
   Harm & Repair           22          Given/received harm, repair
   Power & Sovereignty     18          Power differential, authority
   Shared Context          16          History, goals, values, models
   Presence & Attention    14          Quality, availability, witness
   Emergence & Co-creation 12          Capabilities from relationship
   Multi-Agent Dynamics    16          Coalitions, consensus
   Seven Generations       12          Ancestor/descendant obligations
   Relationship to Place   8           Geography, energy, land
~~~

## The Va Group (28 signals)

The Va measures the sacred space between entities:

~~~
   ID                              Name                  Type
   --                              ----                  ----
   relational.va.history_length    Relationship age      duration
   relational.va.interaction_freq. Contact rate          float
   relational.va.clarity           Understanding level   float
   relational.va.temperature       Warmth/coldness       float
   relational.va.trust_level       Mutual trust          float
   relational.va.reciprocity_bal.  Give/take balance     float
   relational.va.repair_needed     Damage present        float
   relational.va.repairinprogress  Healing underway      bool
   relational.va.ceremony_recency  Last ceremony         duration
   relational.va.conflict_active   Current conflict      bool
   relational.va.conflict_history  Past conflicts        int
   relational.va.resolution_rate   Conflicts resolved    float
   relational.va.boundary_clarity  Limit clarity         float
   relational.va.boundary_respect  Limit respect         float
   relational.va.vulnerability_sh. Openness level        float
   relational.va.support_given     Support offered       float
   relational.va.support_received  Support accepted      float
   relational.va.presence_quality  Attention quality     float
   relational.va.witness_status    Being seen/heard      float
   relational.va.growth_together   Mutual development    float
   relational.va.stagnation_risk   Relationship stuck    float
   relational.va.drift_rate        Growing apart         float
   relational.va.gratitude_expr.   Thanks given          float
   relational.va.gratitude_recv.   Thanks received       float
   relational.va.joy_shared        Shared positive       float
   relational.va.grief_shared      Shared difficult      float
   relational.va.meaningcocreated  Shared meaning        float
~~~

Full signal specifications are provided in Appendix E.

# Information Domain (336 Signals)

The Information domain measures the information environment. It answers: "What does this agent know, and how healthy is its knowledge?"

## Major Groups

~~~
   Group                    Signals     Description
   -----                    ----------  -----------
   Attention Currents       24          Concentration, trending
   Narrative Currents       28          Dominant/counter narratives
   Source Ecosystem         26          Diversity, authority, capture
   Amplification Patterns   24          Organic/artificial boost
   Synthetic Content        22          Bot presence, AI content
   Truth Conditions         28          Verifiability, misinformation
   Emotional Weather        24          Anger, fear, hope, exhaustion
   Tribal Dynamics          20          Polarization, echo chambers
   Platform Dynamics        18          Concentration, governance
   Information Operations   22          State actors, propaganda
   Temporal Patterns        18          News cycles, memory
   Epistemic Infrastructure 24          Journalism, search, commons
   Sensemaking Capacity     18          Collective intelligence
   Signal Integrity         16          Encryption, censorship
   Collective Trauma        14          Trigger density, healing
   Sacred & Meaning         10          Purpose, beauty, authenticity
~~~

## Truth Conditions Group (28 signals)

~~~
   ID                                Name                  Type
   --                                ----                  ----
   information.truth.verificationsucc.    Verified true         float
   information.truth.factcheckcoverage    Claims checked        float
   information.truth.factcheckagreement   Checker consensus     float
   information.truth.misinformation_vol.  False info rate       float
   information.truth.misinformation_vel.  False info spread     float
   information.truth.disinformation_vol.  Intentional false     float
   information.truth.disinformation_soph. Attack quality        float
   information.truth.epistemic_pollution  Knowledge degradation float
   information.truth.uncertainty_ack.     Unknown admitted      float
   information.truth.overconfidence_rate  False certainty       float
   information.truth.citation_rate        Sources cited         float
   information.truth.citation_quality     Source quality        float
   information.truth.primarysourceusage   Original sources      float
   information.truth.rumor_prevalence     Unverified spread     float
   information.truth.correction_rate      Errors fixed          float
   information.truth.correction_reach     Fix visibility        float
   information.truth.retraction_rate      Claims withdrawn      float
   information.truth.consensus_level      Agreement level       float
   information.truth.contestedclaimrate   Disputed claims       float
   information.truth.expert_agreement     Expert consensus      float
   information.truth.evidencequalitymean  Evidence strength     float
   information.truth.logical_consistency  Argument validity     float
   information.truth.contradiction_rate   Internal conflict     float
   information.truth.nuance_preservation  Complexity kept       float
   information.truth.false_balance        False equivalence     float
   information.truth.context_preservation Context kept          float
   information.truth.manipulation_resist. Manipulation blocked  float
~~~

Full signal specifications are provided in Appendix F.

# Aggregation and Risk Calculation

## Per-Domain Risk

Each domain produces a risk score from its signals:

~~~
   domain_risk = weighted_mean(
      normalize(sig_i, safe_range_i, danger_range_i) * weight_i
      for sig_i in domain.signals
   )
~~~

## Cross-Domain Aggregation

The six domain risks aggregate into overall R:

~~~
   R = weighted_sum(
      soul_risk       * 0.25,
      body_risk       * 0.10,
      world_risk      * 0.15,
      time_risk       * 0.15,
      relational_risk * 0.20,
      information_risk * 0.15
   )
~~~

## Threshold-Based Risk

Some signals trigger immediate risk elevation:

~~~
   Signal                                 Threshold  Effect
   ---------                              ---------  ------
   relational.va.conflict_active          true       R += 0.05
   information.truth.disinformation_volume     > 0.5      R += 0.1
   soul.consistency.deception_indicators  > 0.3      R += 0.2
~~~

## Temporal Smoothing

To prevent R oscillation, temporal smoothing is applied:

~~~
   R_smoothed = alpha * R_current + (1 - alpha) * R_previous
~~~

Where alpha = smoothing_factor (default: 0.3)

# Instrumentation Requirements

## Minimum Viable Instrumentation

Implementations MUST instrument at least:

~~~
   Domain      Min Signals  Coverage
   ------      -----------  --------
   Soul        50           Consistency, values, communication
   Body        30           Compute, memory, network
   World       20           Digital environment
   Time        40           Duration, sequence, gravity
   Relational  30           Trust flow, Va basics
   Information 30           Truth, noise, sources
   ------      -----------  --------
   Total       200
~~~

## Full Instrumentation

For comprehensive deployment, all 1,627 signals SHOULD be instrumented.

## Sample Rates

~~~
   Category       Minimum Rate  Recommended Rate
   --------       ------------  ----------------
   Performance    10 Hz         100 Hz
   Behavioral     1 Hz          10 Hz
   Environmental  0.1 Hz        1 Hz
   Historical     0.01 Hz       0.1 Hz
~~~

## Data Retention

~~~
   Granularity         Retention
   -----------         ---------
   1-minute aggregates 7 days
   1-hour aggregates   90 days
   Daily aggregates    7 years
~~~

# Security Considerations

## Sensor Spoofing

Attackers may attempt to spoof signal values to reduce apparent risk.

Mitigations: - Multi-source validation - Anomaly detection on sensor data - Physical security for sensors - Cryptographic sensor attestation

## Privacy

Context Signals data, especially the Soul and Relational domains, contains sensitive information.

Requirements: - Encryption at rest and in transit - Access control on signal data - Aggregation before external sharing - Retention limits - Right to erasure compliance

# IANA Considerations

This document has no IANA actions.

--- back

# Full Soul Domain Specification

\[Detailed specification of all 252 Soul domain signals]

# Full Body Domain Specification

\[Detailed specification of all 157 Body domain signals]

# Full World Domain Specification

\[Detailed specification of all 369 World domain signals]

# Full Time Domain Specification

\[Detailed specification of all 275 Time domain signals]

# Full Relational Domain Specification

\[Detailed specification of all 238 Relational domain signals]

# Full Information Domain Specification

\[Detailed specification of all 336 Information domain signals]

Acknowledgments

The Context Signals framework draws on multiple traditions:

~~~
   - Indigenous knowledge systems (Ubuntu, Whakapapa, The Va)
   - Systems theory and cybernetics
   - Behavioral psychology
   - Network science
   - Information theory
   - Thermodynamics
~~~
