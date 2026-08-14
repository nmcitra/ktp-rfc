# Kinetic Trust Protocol (KTP) - Context Signal Sensor Specification


This document specifies the sensor requirements and configurations for Context Signals, the environmental measurement framework used by the Kinetic Trust Protocol (KTP).

The specification covers sensor types, normalization algorithms, domain-specific weight profiles, and the unique characteristics of the Soul (Sovereignty) dimension which acts as an independent veto mechanism rather than a weighted contributor.

# Introduction

Context Signals are the sensory nervous system of the Kinetic Trust Protocol. They measure environmental reality across seven inputs, providing the data needed to calculate the Risk Factor and evaluate sovereignty constraints.

This document provides detailed specifications for:

- The sensors and data feeds that populate each dimension
- Normalization algorithms for converting raw telemetry to 0-1 scale
- Domain-specific weight configurations
- The unique architecture of the Soul veto
- Quality requirements and validation procedures

The framework is designed to be modular at both the input level (new inputs can be added) and the feed level (sensors within each input can be configured per deployment).

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

# Sensor Architecture

## Modularity Principles

The sensor framework follows two levels of modularity:

Level 1 - Framework Modularity:

~~~
   The seven inputs defined in this specification represent the
   core measurement space. However, the architecture supports
   extension for domain-specific requirements.
~~~

~~~
   New dimensions MUST specify:
   - Unique identifier (a name, not conflicting with the six
     named inputs or soul)
   - Physics equivalent (conceptual grounding)
   - Contribution type: "weighted" (contributes to R) or "veto"
     (independent constraint like Soul)
   - Sensor feed specifications
   - Normalization rules
   - Recommended domain weights (if weighted type)
~~~

Level 2 - Feed Modularity:

~~~
   Each dimension aggregates multiple sensor feeds. Feeds are
   independently configurable:
~~~

~~~
   - Enable/disable per deployment
   - Adjust weights within dimension
   - Add custom feeds to existing dimensions
   - Configure local vs. federated sources
~~~

This modularity allows KTP to adapt to diverse deployment contexts while maintaining consistent measurement semantics.

## Feed Aggregation

For the six weighted inputs, feeds are aggregated using weighted average:

~~~
   dimension_value = sum(feed_weight[i] * feed_value[i]) /
                     sum(feed_weight[i])
~~~

Where: feed_weight[i] = Configured weight for feed i (default: 1.0) feed_value[i] = Normalized value (0-1) from feed i

For the Soul veto, feeds are aggregated using logical OR:

~~~
   S = 1 IF ANY enabled feed returns veto
   S = 0 IF ALL enabled feeds return clear
~~~

Feed configuration schema:

~~~
   {
     "dimension": "m",
     "feeds": [
       {
         "id": "co2-sensor",
         "type": "physical",
         "source": "mqtt://sensors.local/co2",
         "enabled": true,
         "weight": 1.0,
         "normalization": {
           "min": 400,
           "max": 2000,
           "invert": false
         },
         "refresh_interval_ms": 30000,
         "stale_threshold_ms": 120000
       },
       {
         "id": "badge-count",
         "type": "physical",
         "source": "https://access.local/api/count",
         "enabled": true,
         "weight": 1.5,
         "normalization": {
           "min": 0,
           "max": 5000,
           "invert": false
         },
         "refresh_interval_ms": 60000,
         "stale_threshold_ms": 300000
       }
     ],
     "aggregation": "weighted_average",
     "default_on_failure": 0.8
   }
~~~

Both feeds above declare a stale_threshold_ms of four to five times their refresh_interval_ms, which is the ratio Section 6.1 makes the default.

## Risk Domains (Node, Neighborhood, Global)

A critical challenge in environmental sensing is oscillation: rapid fluctuation in the Risk Factor caused by local noise, leading to unstable Trust Scores and excessive tier transitions.

Consider an agent operating near the Operator/Analyst tier boundary (E_trust ≈ 70). If a single sensor on a single node experiences a momentary spike—a brief CPU surge, a transient network blip—the agent could rapidly transition Operator → Analyst → Operator → Analyst, disrupting operations and creating audit noise.

To prevent this, KTP implements three-level Risk Domains:

2.3.1.  The Three Levels

Level 1 - Node Domain:

~~~
   The immediate context of a single resource or endpoint.
~~~

~~~
   Scope: One server, one API instance, one database replica
   Update frequency: High (1-5 seconds)
   Sensors: Local CPU, local memory, local connections, local errors
   Weight in R: 30% (default)
~~~

~~~
   Node-level readings are the most granular and most volatile.
   They capture immediate conditions but are subject to noise.
~~~

Level 2 - Neighborhood Domain:

~~~
   The local cluster, service mesh, or subnet.
~~~

~~~
   Scope: Peer nodes, immediate dependencies, same availability zone
   Update frequency: Medium (10-30 seconds)
   Sensors: Cluster averages, mesh telemetry, subnet utilization
   Weight in R: 40% (default)
~~~

~~~
   Neighborhood-level readings smooth out individual node variance
   by aggregating across peers. A single node spike doesn't move
   the neighborhood, but coordinated degradation does.
~~~

Level 3 - Global Domain:

~~~
   The zone-wide or federation-wide environment.
~~~

~~~
   Scope: Entire Blue Zone, federated zones, external threat feeds
   Update frequency: Low (30-120 seconds)
   Sensors: Zone-wide aggregates, threat intelligence, external events
   Weight in R: 30% (default)
~~~

~~~
   Global-level readings capture broad trends and external factors.
   They change slowly but authoritatively. A global threat indicator
   affects all agents regardless of local conditions.
~~~

2.3.2.  Aggregation Formula

The final Risk Factor incorporates all three domains:

~~~
   R = (w_node × R_node) + (w_neighborhood × R_neighborhood) +
       (w_global × R_global)
~~~

Where w_node + w_neighborhood + w_global = 1.0

Default weights: w_node = 0.30 w_neighborhood = 0.40 w_global = 0.30

This weighting gives the neighborhood domain primary influence, which provides stability while remaining responsive.

2.3.3.  Anti-Oscillation Mechanics

The three-domain structure prevents oscillation through damping:

Scenario 1: Single Node Spike

~~~
   Node R jumps from 0.20 to 0.80 (local event)
   Neighborhood R unchanged at 0.25
   Global R unchanged at 0.20
~~~

~~~
   R_before = (0.30 × 0.20) + (0.40 × 0.25) + (0.30 × 0.20) = 0.22
   R_after  = (0.30 × 0.80) + (0.40 × 0.25) + (0.30 × 0.20) = 0.40
~~~

~~~
   Result: R increases, but not catastrophically. No tier transition
   if agent has buffer above threshold.
~~~

Scenario 2: Neighborhood Degradation

~~~
   Node R rises to 0.60 (local reflection of broader issue)
   Neighborhood R rises to 0.70 (many nodes affected)
   Global R unchanged at 0.20
~~~

~~~
   R = (0.30 × 0.60) + (0.40 × 0.70) + (0.30 × 0.20) = 0.52
~~~

~~~
   Result: Significant R increase. Likely tier transition, but
   justified because the neighborhood is actually degraded.
~~~

Scenario 3: Global Threat

~~~
   Node R unchanged at 0.20
   Neighborhood R unchanged at 0.25
   Global R rises to 0.80 (external threat intelligence)
~~~

~~~
   R = (0.30 × 0.20) + (0.40 × 0.25) + (0.30 × 0.80) = 0.40
~~~

~~~
   Result: R increases meaningfully even though local conditions
   are fine. The global threat affects all agents in the zone.
~~~

2.3.4.  Domain Configuration

Domain weights are configurable per deployment:

~~~
   {
     "risk_domains": {
       "node": {
         "weight": 0.30,
         "update_interval_ms": 5000,
         "sensors": ["cpu", "memory", "connections", "errors"]
       },
       "neighborhood": {
         "weight": 0.40,
         "update_interval_ms": 15000,
         "sensors": ["cluster_avg", "mesh_telemetry", "peer_health"]
       },
       "global": {
         "weight": 0.30,
         "update_interval_ms": 60000,
         "sensors": ["zone_aggregate", "threat_intel", "external_feeds"]
       }
     }
   }
~~~

For highly stable environments, increase neighborhood weight. For rapidly changing environments, increase node weight. For threat- sensitive environments, increase global weight.

2.3.5.  Hysteresis Complement

Risk Domains complement but do not replace hysteresis at tier boundaries (see [KTP-ENFORCE] Section 5.3). Both mechanisms work together:

- Risk Domains: Smooth input signal (prevent noisy R)
- Hysteresis: Smooth state transitions (prevent rapid tier changes)

Together, they create stable system behavior without sacrificing responsiveness to genuine environmental changes.

# The Six Weighted Inputs

## evidence_density

Analogy (informative): Mass (M) — Density / Mass (m)

Concept: The sheer weight of presence in the environment. High evidence_density naturally slows operations (Time Dilation) and increases the "cost" of movement.

Impact on Trust: High evidence_density correlates with network congestion, increased attack surface, and reduced diagnostic capability. Actions become more expensive as the environment becomes denser.

Sensor Feeds:

~~~
+------------------+------------------------------------------+
| Feed             | Description                              |
+------------------+------------------------------------------+
| CO2 Levels       | Parts per million, proxy for occupancy   |
| Crowd LIDAR      | Direct count via laser scanning          |
| Turnstile Count  | Badge swipes, physical access events     |
| RF Noise Floor   | Electromagnetic density (dBm)            |
| Device Count     | Active devices on network segment        |
| Thermal Imaging  | Heat signatures indicating presence      |
| WiFi Probe Count | Unique device probes detected            |
+------------------+------------------------------------------+
~~~

Normalization:

~~~
+------------------+----------+----------+----------+
| Feed             | s_min    | s_max    | Invert   |
+------------------+----------+----------+----------+
| CO2 (ppm)        | 400      | 2000     | No       |
| LIDAR count      | 0        | capacity | No       |
| Badge count      | 0        | capacity | No       |
| RF noise (dBm)   | -90      | -30      | No       |
| Device count     | 0        | max_dev  | No       |
+------------------+----------+----------+----------+
~~~

Refresh Interval: 30-60 seconds (physical changes slowly)

Example Calculation (Stadium):

~~~
   CO2 = 1800 ppm → (1800-400)/(2000-400) = 0.875
   LIDAR = 45000 of 50000 capacity → 45000/50000 = 0.900
   RF = -45 dBm → (-45-(-90))/(-30-(-90)) = 0.750
   Devices = 48000 of 60000 → 48000/60000 = 0.800
~~~

~~~
   With equal weights:
   M = (0.875 + 0.900 + 0.750 + 0.800) / 4 = 0.831
~~~

## trust_trend

Analogy (informative): Momentum (P) — Kinetic Energy
(KE = 1/2 mv²)

Concept: The speed and direction of data flow. High trust_trend means the system is moving fast. Sudden stops or turns (Vector Kinking) create massive G-forces (Risk).

Impact on Trust: High trust_trend leaves less capacity for additional load and increases the cost of course corrections. Actions that change system direction become increasingly expensive.

Sensor Feeds:

~~~
+------------------+------------------------------------------+
| Feed             | Description                              |
+------------------+------------------------------------------+
| Transaction Rate | API calls per second                     |
| Link Saturation  | Bandwidth utilization percentage         |
| Packet Velocity  | Packets per second on key interfaces     |
| Queue Depth      | Messages pending in critical queues      |
| Connection Count | Active TCP/WebSocket connections         |
| Throughput       | Bytes per second through gateways        |
| Event Frequency  | Domain events processed per second       |
+------------------+------------------------------------------+
~~~

Normalization:

~~~
+------------------+----------+----------+----------+
| Feed             | s_min    | s_max    | Invert   |
+------------------+----------+----------+----------+
| TPS              | 0        | max_tps  | No       |
| Link %           | 0        | 100      | No       |
| PPS              | 0        | max_pps  | No       |
| Queue depth      | 0        | max_q    | No       |
| Connections      | 0        | max_conn | No       |
+------------------+----------+----------+----------+
~~~

Refresh Interval: 1-5 seconds (kinetic state changes rapidly)

Example Calculation (Trading Platform):

~~~
   TPS = 45000 of 50000 max → 0.900
   Link = 78% → 0.780
   Queue = 8500 of 10000 max → 0.850
   Connections = 12000 of 15000 max → 0.800
~~~

~~~
   With equal weights:
   P = (0.900 + 0.780 + 0.850 + 0.800) / 4 = 0.833
~~~

## adversarial_pressure

Analogy (informative): Entropy / Temperature (T)

Concept: The chaotic energy or friction in the system. adversarial_pressure represents both active adversarial stress and system stress. Heat is the Deflator—as Heat rises, the structural integrity of Trust degrades.

Impact on Trust: High adversarial_pressure indicates a compromised or stressed environment where agent actions may be exploited, misattributed, or cause cascading failures. Sustained highs trigger the "Cool-Down" cycle (freezing agents to Observer Mode).

Sensor Feeds:

~~~
+------------------+------------------------------------------+
| Feed             | Description                              |
+------------------+------------------------------------------+
| WAF Blocks       | Blocked requests per minute              |
| Auth Velocity    | Failed auth attempts per second          |
| Port Scans       | Detected reconnaissance activity         |
| Entropy Rate     | Randomness in traffic patterns           |
| Error Rate       | Application errors per minute            |
| CPU Temperature  | Physical thermal load (celsius)          |
| Voltage Droop    | Power supply stress indicators           |
| Anomaly Score    | ML-derived anomaly detection             |
+------------------+------------------------------------------+
~~~

Normalization:

~~~
+------------------+----------+----------+----------+
| Feed             | s_min    | s_max    | Invert   |
+------------------+----------+----------+----------+
| WAF blocks/min   | 0        | 10000    | No       |
| Auth fails/sec   | 0        | 1000     | No       |
| Port scans/min   | 0        | 500      | No       |
| Error rate/min   | 0        | 1000     | No       |
| CPU temp (C)     | 40       | 90       | No       |
| Anomaly (0-100)  | 0        | 100      | No       |
+------------------+----------+----------+----------+
~~~

Refresh Interval: 1-5 seconds (adversarial conditions change fast)

Example Calculation (Under Attack):

~~~
   WAF blocks = 5000/min → 5000/10000 = 0.500
   Auth fails = 200/sec → 200/1000 = 0.200
   Port scans = 150/min → 150/500 = 0.300
   Anomaly = 75 → 75/100 = 0.750
~~~

~~~
   With equal weights:
   H = (0.500 + 0.200 + 0.300 + 0.750) / 4 = 0.438
~~~

## moment_criticality

Analogy (informative): Temporal Mechanics / Phase

Concept: The criticality of the current moment relative to an event horizon. A failure during "Kickoff" has infinitely higher gravity than a failure at 3:00 AM. Time dilates risk tolerance.

Impact on Trust: Near event horizons (go-live, kickoff, earnings call), the same action costs more trust. The system becomes more conservative as critical moments approach.

Sensor Feeds:

~~~
+------------------+------------------------------------------+
| Feed             | Description                              |
+------------------+------------------------------------------+
| Event Countdown  | Minutes to scheduled event               |
| Business Hours   | Current position in business cycle       |
| Maintenance Win  | Whether in scheduled maintenance         |
| Mission Phase    | rehearsal / pre-prod / live / post       |
| Quarter End      | Days to financial close                  |
| Deadline Timer   | Time to contractual SLA deadline         |
+------------------+------------------------------------------+
~~~

Normalization:

~~~
+------------------+----------+----------+----------+
| Feed             | s_min    | s_max    | Invert   |
+------------------+----------+----------+----------+
| Event countdown  | 72 hrs   | 0 hrs    | Yes      |
| Business hours   | off-peak | peak     | No       |
| Maintenance      | in maint | not maint| Yes      |
| Mission phase    | 0        | 3        | No       |
+------------------+----------+----------+----------+
~~~

Note: Time is typically inverted—72 hours out = low stress, 0 hours (event starting) = maximum stress.

Refresh Interval: 60 seconds (time is predictable)

Example Calculation (30 minutes to kickoff):

~~~
   Event countdown = 0.5 hrs → (72-0.5)/72 inverted = 0.993
   Mission phase = 3 (live) → 3/3 = 1.000
   Business hours = peak → 1.000
~~~

~~~
   With equal weights:
   T = (0.993 + 1.000 + 1.000) / 3 = 0.998
~~~

## update_resistance

Analogy (informative): Inertial Mass

Concept: The topological importance of a node—how hard is it to move or stop this asset? A core router has high update_resistance; an edge IoT device has low. High-resistance nodes resist change.

Impact on Trust: Changes to high-inertia systems carry disproportionate risk due to cascading effects. The Trust Score required to modify a high-inertia node is higher than for low-inertia nodes.

Sensor Feeds:

~~~
+------------------+------------------------------------------+
| Feed             | Description                              |
+------------------+------------------------------------------+
| Dependency Depth | Number of downstream services            |
| Degree Central.  | Connections in topology graph            |
| Betweenness      | Traffic that routes through this node    |
| Data Volume      | TB of data stored/processed              |
| User Count       | Active users dependent on service        |
| SLA Tier         | Contractual importance level             |
| Revenue Impact   | Dollars/minute if service fails          |
+------------------+------------------------------------------+
~~~

Normalization:

~~~
+------------------+----------+----------+----------+
| Feed             | s_min    | s_max    | Invert   |
+------------------+----------+----------+----------+
| Dependency count | 0        | 500      | No       |
| Degree centrality| 0        | max_deg  | No       |
| Betweenness      | 0        | 1        | No       |
| Data volume (TB) | 0        | 1000     | No       |
| User count       | 0        | max_user | No       |
+------------------+----------+----------+----------+
~~~

Refresh Interval: 300 seconds (topology changes slowly)

Example Calculation (Core Database):

~~~
   Dependencies = 250 of 500 → 0.500
   Betweenness = 0.85 → 0.850
   Data volume = 500 TB of 1000 → 0.500
   User count = 45000 of 50000 → 0.900
~~~

~~~
   With equal weights:
   I = (0.500 + 0.850 + 0.500 + 0.900) / 4 = 0.688
~~~

## attestation_coverage

Analogy (informative): Frame of Reference / Observer Effect

Concept: Who is watching? The stakes based on the population present and their sensitivity. The environment's constraints tighten when the Observer count is high or when specific observers (e.g., Regulators) are present.

Impact on Trust: Actions that would be routine become consequential when high-visibility observers are present. The reputational and regulatory implications of failure scale with observer sensitivity.

Sensor Feeds:

~~~
+------------------+------------------------------------------+
| Feed             | Description                              |
+------------------+------------------------------------------+
| VIP Presence     | Executives, board members logged in      |
| Regulator Flag   | Active regulatory observation            |
| Media Presence   | Press/media users active                 |
| Audit Mode       | Compliance audit in progress             |
| Life Safety      | Users in life-critical contexts          |
| External Ratio   | % of users who are external/customers    |
| Jurisdiction     | Regulatory jurisdictions involved        |
+------------------+------------------------------------------+
~~~

Normalization:

~~~
+------------------+----------+----------+----------+
| Feed             | s_min    | s_max    | Invert   |
+------------------+----------+----------+----------+
| VIP count        | 0        | 50       | No       |
| Regulator (bool) | 0        | 1        | No       |
| Audit (bool)     | 0        | 1        | No       |
| Life safety count| 0        | 1000     | No       |
| External %       | 0        | 100      | No       |
+------------------+----------+----------+----------+
~~~

Refresh Interval: 30 seconds (population changes moderately)

Example Calculation (Earnings Call):

~~~
   VIP count = 25 of 50 → 0.500
   Media = true → 1.000
   External % = 85% → 0.850
~~~

~~~
   With equal weights:
   O = (0.500 + 1.000 + 0.850) / 3 = 0.783
~~~

# The Soul Veto

## Overview

Analogy (informative): The Cosmological Constant / Immutable Law

Concept: The ethical, legal, and spiritual constraints of the physical location or data lineage. Soul represents constraints that exist independent of operational conditions—they are the "Spirit" of the data or place.

Unlike the six weighted dimensions, Soul operates as a binary veto:

~~~
   S = 0: No sovereignty constraints violated, action may proceed
          (subject to A <= E_trust evaluation)
   S = 1: Sovereignty constraint violated, action is FORBIDDEN
          (regardless of Trust Score)
~~~

This asymmetry is intentional. Sovereignty constraints encode immutable laws—legal treaties, cultural protocols, spiritual significance—that cannot be traded against operational convenience. No amount of trust can make a forbidden action permissible.

## Sensor Feeds

Soul aggregates feeds from multiple sovereignty frameworks:

~~~
+----------------------+------------------------------------------+
| Feed                 | Description                              |
+----------------------+------------------------------------------+
| TK Labels            | Traditional Knowledge labels per Local   |
|                      | Contexts framework                       |
| OCAP Registry        | First Nations OCAP protocol compliance   |
| CARE Principles      | Indigenous data governance principles    |
| Sacred Land Geofence | Geographic sovereignty boundaries        |
| Treaty Database      | Legal treaty constraints lookup          |
| Data Provenance      | Origin lineage sovereignty tracking      |
| Cultural Registry    | Cultural heritage protection flags       |
+----------------------+------------------------------------------+
~~~

4.2.1. Traditional Knowledge (TK) Labels

The Local Contexts project (localcontexts.org) provides a framework for Indigenous communities to express protocols for accessing and using traditional knowledge.

Relevant TK Labels that may trigger Soul veto:

- TK Attribution (TK A): Requires attribution to community
- TK Non-Commercial (TK NC): Prohibits commercial use
- TK Community Voice (TK CV): Requires community consent
- TK Outreach (TK O): Prohibits modification without consultation
- TK Culturally Sensitive (TK CS): Content has cultural restrictions
- TK Secret/Sacred (TK SS): Content must not be shared publicly

Integration: Query the Local Contexts API with data identifiers to retrieve applicable labels. If the requested action would violate any label's protocol, S = 1.

4.2.2. OCAP Principles (First Nations)

OCAP (Ownership, Control, Access, Possession) principles assert First Nations jurisdiction over data:

- Ownership: Community owns information collectively
- Control: Community controls all aspects of data management
- Access: Community determines access protocols
- Possession: Physical control of data remains with community

Integration: Check OCAP registry for data classification. If action would violate any OCAP principle (e.g., moving data outside tribal jurisdiction), S = 1.

4.2.3. CARE Principles

CARE principles (Collective benefit, Authority to control, Responsibility, Ethics) extend Indigenous data governance:

- Collective Benefit: Data must serve community interests
- Authority to Control: Community right to govern data use
- Responsibility: Users must respect community protocols
- Ethics: Data use must align with community values

Integration: Evaluate requested action against CARE framework. If action conflicts with any principle, S = 1.

4.2.4. Sacred Land Geofences

Physical locations may have sovereignty constraints independent of the data being processed. Sacred sites, treaty lands, and cultural heritage zones may prohibit certain activities.

Geofence types:

- Sacred Sites: Locations with spiritual significance
- Treaty Lands: Areas with specific legal constraints
- Cultural Zones: Protected cultural heritage areas
- Ceremonial Grounds: Locations with use restrictions

Integration: If agent or infrastructure is physically located within a geofenced area, check permitted actions. If requested action is prohibited, S = 1.

4.2.5. Treaty Database

Legal treaties between nations, tribes, and governments may impose constraints on data handling, especially for:

- Cross-border data transfer
- Data about treaty signatories
- Resources covered by treaty terms

Integration: Query treaty database with action context. If action would violate treaty terms, S = 1.

4.2.6. Data Provenance / Lineage Sovereignty

Data carries sovereignty constraints from its origin. Even if data has been copied to cloud infrastructure, the Soul of the data travels with it.

Provenance tracking includes:

- Collection location (where was data gathered?)
- Collection context (under what terms?)
- Subject community (whose data is this?)
- Derived works (what transformations occurred?)

Integration: Trace data lineage to origin. If origin carries sovereignty constraints that apply to requested action, S = 1.

## Veto Mechanics

Soul evaluation follows a strict sequence:

1. Identify applicable sovereignty frameworks for: -  The data being accessed -  The location of the agent -  The location of the infrastructure -  The subject of the data

1. For each applicable framework: -  Query the relevant registry/database -  Evaluate requested action against framework protocols -  If ANY framework returns veto, S = 1 -  If ANY query is UNDETERMINED, S = 1

A query is UNDETERMINED when no answer arrived: the registry was unreachable, returned an error, timed out, or returned nothing. These cases do not separate. A channel that returns nothing and a channel that was never reachable are indistinguishable to this decision, and an adversary who can produce one can produce the other, so an implementation MUST NOT branch on the difference. Only a framework that answers - including an answer of "no applicable constraint" - has returned a clearance. No cached or prior clearance substitutes for a current answer: Soul is queried on demand and has no staleness threshold (Section 6.1).

An unanswered sovereignty query is an undefined input under [KTP-CORE] Section 6.7: it MUST NOT resolve toward permission, and the veto is the only more restrictive outcome this decision point offers. The undetermined state MUST be recorded on the decision record, so a veto raised for silence reads apart from a veto returned by a framework in audit.

1. If S = 1: -  Immediately return SOVEREIGNTY_CONSTRAINT error -  Do NOT proceed to A <= E_trust evaluation -  Log veto with full constraint details

Veto Response Format:

~~~
   {
     "error": "SOVEREIGNTY_CONSTRAINT",
     "message": "Action violates data sovereignty",
     "soul": {
       "soul": 1,
       "constraint_type": "tk_label",
       "constraint_id": "TK-NC-001",
       "constraint_name": "TK Non-Commercial",
       "authority": "https://localcontexts.org/label/tk-nc/",
       "community": "Example Indigenous Community",
       "remediation": "Contact community data steward for
                       commercial licensing"
     },
     "e_trust": 95,
     "note": "Trust Score is sufficient for action risk, but
              action is forbidden by sovereignty constraint"
   }
~~~

A veto raised for an UNDETERMINED query does not fabricate an answering authority. The response names the registry that was queried and the failure observed, and its remediation is retry or escalation to the registry operator rather than community contact.

## Integration with Indigenous Data Sovereignty

The Soul veto is designed to operationalize Indigenous Data Sovereignty principles within technical systems. Key design decisions:

1. Community Authority: Soul feeds should be controlled by the communities they represent, not by the KTP implementation. The Trust Oracle queries community-controlled registries.

1. Immutability: Soul constraints cannot be overridden by operational considerations. This reflects that sovereignty is not negotiable.

1. Specificity: Soul evaluations are action-specific. A community may permit "read" but not "modify", or "internal use" but not "external sharing".

1. Portability: Soul travels with data. When data moves between systems, its sovereignty constraints must be preserved and enforced.

1. Transparency: Soul vetoes include full attribution to the authorizing community and constraint, enabling appropriate follow- up.

Recommended Implementation:

- Partner with Indigenous data governance organizations
- Use standard APIs (Local Contexts, tribal registries)
- Implement data lineage tracking from point of collection
- Provide clear remediation paths (who to contact for exceptions)
- Support community-defined consent workflows

# Domain Weight Profiles

Different deployment domains weight the six weighted dimensions differently. Soul is not weighted—it always acts as an independent veto.

Weights MUST sum to 1.0 across the six named inputs.

5.1. Pre-defined Profiles

Stadium/Event Network: evidence_density=0.25, trust_trend=0.25, adversarial_pressure=0.20, moment_criticality=0.15, update_resistance=0.10, attestation_coverage=0.05 Rationale: Physical density and momentum dominate; events have hard deadlines.

Financial Trading: evidence_density=0.05, trust_trend=0.30, adversarial_pressure=0.25, moment_criticality=0.20, update_resistance=0.15, attestation_coverage=0.05 Rationale: Speed is critical; adversarial pressure high; market hours create temporal constraints.

Healthcare: evidence_density=0.10, trust_trend=0.15, adversarial_pressure=0.25, moment_criticality=0.15, update_resistance=0.20, attestation_coverage=0.15 Rationale: Patient safety (inertia) paramount; regulatory observation (observer) significant; attacks can be fatal.

Cloud Infrastructure: evidence_density=0.05, trust_trend=0.25, adversarial_pressure=0.30, moment_criticality=0.10, update_resistance=0.25, attestation_coverage=0.05 Rationale: Adversarial pressure and topology (inertia) dominate; physical presence less relevant.

Indigenous Data Repository: evidence_density=0.10, trust_trend=0.10, adversarial_pressure=0.20, moment_criticality=0.10, update_resistance=0.15, attestation_coverage=0.35 Rationale: High Observer weight reflects community oversight importance; Soul veto always active for labeled data.

Government/Military: evidence_density=0.15, trust_trend=0.15, adversarial_pressure=0.30, moment_criticality=0.15, update_resistance=0.15, attestation_coverage=0.10 Rationale: Adversarial pressure highest priority; balanced across other dimensions.

5.2. Custom Profiles

Implementations MUST allow custom weight configuration. Configuration schema:

~~~
   {
     "profile_id": "custom-retail",
     "name": "Retail Point of Sale",
     "weights": {
       "evidence_density": 0.20,
       "trust_trend": 0.20,
       "adversarial_pressure": 0.25,
       "moment_criticality": 0.15,
       "update_resistance": 0.10,
       "attestation_coverage": 0.10
     },
     "soul_enabled": true,
     "soul_feeds": ["tk_labels", "geofence"],
     "description": "Retail environment with customer data"
   }
~~~

# Sensor Quality and Validation

Sensor data quality directly impacts Trust Score accuracy. Poor sensor data can lead to either over-permissive (dangerous) or over- restrictive (operationally harmful) authorization.

6.1. Freshness Requirements

Freshness is a property of the individual feed, not of the Risk Factor it contributes to. A single Risk Factor aggregates feeds whose refresh rates differ by orders of magnitude, so no single staleness figure describes the set. Each feed therefore declares its own.

Every feed declares refresh_interval_ms and stale_threshold_ms (see Section 2.2). Where stale_threshold_ms is not declared, it DEFAULTS to five times that feed's refresh_interval_ms. A deployment MAY declare a shorter threshold. A deployment MUST NOT declare a longer one without recording the reason in the sensor configuration.

A feed whose most recent observation is older than its stale_threshold_ms is UNAVAILABLE for the purposes of Section 6.2. There is no separate stale behavior: a reading too old to be current is not a reading, and Section 6.2 governs it.

An implementation MUST NOT substitute the last known value for an observation that has passed its staleness threshold. A stale value is not a conservative value. Whoever can suppress a feed also chooses the moment at which it is suppressed, so a frozen reading is selected by the adversary rather than by the environment. This is the attack named in Section 7.1, and holding a value past its threshold is what enables it.

Soul is queried on demand and has no staleness threshold. A current query is REQUIRED. A sovereignty registry that does not answer has not returned a clearance, and an implementation MUST NOT treat an unanswered query as the absence of a veto.

6.2. Sensor Failure Handling

If a sensor feed fails:

1. Mark feed as degraded
2. If < 50% of dimension's feeds available: -  Use conservative default (dimension-specific)
3. If no feeds available: -  Use maximum stress value (1.0) for that dimension
4. Log sensor failure for investigation
5. Alert operators if failure persists > threshold

A feed is AVAILABLE only if it has both answered and returned an observation that is current under Section 6.1. A feed that has failed and a feed whose most recent observation has passed its staleness threshold are equally unavailable, and an implementation MUST NOT count either as available in step 2's fraction. This is the same count reported as feeds_active in the audit record (see [KTP-AUDIT] Section 3.2), so two conformant implementations observing the same environment record the same number.

Availability is a property of the feed. Section 5.2 of [KTP-CORE] states the rule for the Context Signal a feed populates and for the Risk Factor the signals aggregate into; a signal may be unavailable while every feed populating it is healthy.

6.3. Cross-Validation

Where possible, validate sensors against correlated feeds:

- CO2 should correlate with badge count
- Transaction rate should correlate with connection count
- Multiple anomaly detectors should agree

If sensors disagree significantly, use the more conservative (higher stress) value pending investigation.

# Security Considerations

7.1. Sensor Manipulation

Attackers may attempt to suppress attack indicators to lower R, then strike when Trust Scores rise.

Mitigations:

- Implement minimum R floor during suspicious conditions
- Use multiple independent sensors per dimension
- Monitor for coordinated sensor value changes
- Implement hysteresis (R rises fast, falls slowly)

7.2. Soul Feed Compromise

If an attacker can modify Soul registries, they could enable forbidden actions or deny legitimate ones.

Mitigations:

- Soul registries should be controlled by authoritative communities, not by KTP operators
- Use cryptographic signatures on Soul feed responses
- Implement multi-source validation for Soul constraints
- Log all Soul evaluations for audit

7.3. Sensor Spoofing

Attackers may inject false sensor data.

Mitigations:

- Authenticate sensor data sources
- Use encrypted channels for sensor telemetry
- Implement physical security for sensor hardware
- Detect anomalous sensor patterns

# IANA Considerations

This document requests registration of the following media types:

8.1. Sensor Feed Configuration

Type name: application Subtype name: ktp-sensor-config+json Description: KTP sensor feed configuration

8.2. Soul Constraint Response

Type name: application Subtype name: ktp-soul-constraint+json Description: KTP sovereignty constraint evaluation
