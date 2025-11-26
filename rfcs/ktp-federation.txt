Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


        Kinetic Trust Protocol (KTP) - Trust Federation Specification

Abstract

   This document specifies the Trust Federation system for the Kinetic
   Trust Protocol (KTP). Trust Federation enables portable trust
   between Blue Zones, allowing agents to carry their reputation
   across zone boundaries while maintaining appropriate trust
   adjustments based on zone relationships.

   The specification covers federation models, trust negotiation,
   cross-zone attestations, dispute resolution, and governance of
   federated trust networks.

Status of This Memo

   This document is a draft specification developed by the New Mexico
   Cyber Intelligence & Threat Response Alliance (NMCITRA). It has not
   been submitted to the IETF and does not represent an Internet
   Standard or consensus of any standards body.

   Feedback and contributions are welcome at:
   https://github.com/nmcitra/ktp-rfc

Copyright Notice

   Copyright (c) 2025 Chris Perkins / NMCITRA.
   This work is licensed under the Apache License, Version 2.0.

Table of Contents

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . . .  2
       1.1.  The Federation Problem  . . . . . . . . . . . . . . . .  2
       1.2.  Federation Philosophy . . . . . . . . . . . . . . . . .  3
       1.3.  Requirements Language . . . . . . . . . . . . . . . . .  4
   2.  Terminology . . . . . . . . . . . . . . . . . . . . . . . . .  4
   3.  Federation Models . . . . . . . . . . . . . . . . . . . . . .  6
       3.1.  Bilateral Federation  . . . . . . . . . . . . . . . . .  6
       3.2.  Hub Federation  . . . . . . . . . . . . . . . . . . . .  7
       3.3.  Mesh Federation . . . . . . . . . . . . . . . . . . . .  8
       3.4.  Hierarchical Federation . . . . . . . . . . . . . . . .  9
   4.  Trust Factor Calculation  . . . . . . . . . . . . . . . . . . 10
       4.1.  Base Trust Factor . . . . . . . . . . . . . . . . . . . 10
       4.2.  Dynamic Trust Factor  . . . . . . . . . . . . . . . . . 11
       4.3.  Trust Factor Decay  . . . . . . . . . . . . . . . . . . 12
       4.4.  Minimum Trust Floor . . . . . . . . . . . . . . . . . . 13
   5.  Federation Agreements . . . . . . . . . . . . . . . . . . . . 14
       5.1.  Agreement Structure . . . . . . . . . . . . . . . . . . 14
       5.2.  Negotiation Protocol  . . . . . . . . . . . . . . . . . 16
       5.3.  Agreement Lifecycle . . . . . . . . . . . . . . . . . . 18
   6.  Cross-Zone Attestations . . . . . . . . . . . . . . . . . . . 19
       6.1.  Attestation Types . . . . . . . . . . . . . . . . . . . 19
       6.2.  Co-Signature Requirements . . . . . . . . . . . . . . . 20
       6.3.  Attestation Verification  . . . . . . . . . . . . . . . 21
       6.4.  Attestation Chain . . . . . . . . . . . . . . . . . . . 22
   7.  Trust Propagation . . . . . . . . . . . . . . . . . . . . . . 23
       7.1.  Forward Propagation . . . . . . . . . . . . . . . . . . 23
       7.2.  Backward Propagation  . . . . . . . . . . . . . . . . . 24
       7.3.  Propagation Limits  . . . . . . . . . . . . . . . . . . 25
   8.  Federation Events . . . . . . . . . . . . . . . . . . . . . . 26
       8.1.  Zone Join . . . . . . . . . . . . . . . . . . . . . . . 26
       8.2.  Zone Leave  . . . . . . . . . . . . . . . . . . . . . . 27
       8.3.  Trust Factor Change . . . . . . . . . . . . . . . . . . 28
       8.4.  Emergency Severance . . . . . . . . . . . . . . . . . . 29
   9.  Dispute Resolution  . . . . . . . . . . . . . . . . . . . . . 30
       9.1.  Dispute Types . . . . . . . . . . . . . . . . . . . . . 30
       9.2.  Resolution Process  . . . . . . . . . . . . . . . . . . 31
       9.3.  Arbitration . . . . . . . . . . . . . . . . . . . . . . 32
   10. Federation Governance . . . . . . . . . . . . . . . . . . . . 33
       10.1. Governance Bodies . . . . . . . . . . . . . . . . . . . 33
       10.2. Policy Coordination . . . . . . . . . . . . . . . . . . 34
       10.3. Standards Evolution . . . . . . . . . . . . . . . . . . 35
   11. Security Considerations . . . . . . . . . . . . . . . . . . . 36
   12. References  . . . . . . . . . . . . . . . . . . . . . . . . . 37
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 38


1.  Introduction

   A single Blue Zone provides physics-based authorization for agents
   within its boundaries. But the real power of KTP emerges when zones
   are connected—when trust earned in one zone carries weight in
   another.

   Trust Federation is the protocol by which zones establish trust
   relationships, negotiate trust factors, and enable portable
   reputation across the emerging network of Blue Zones.

1.1.  The Federation Problem

   Without federation, each zone is an island:

   - Agents must rebuild trust from zero in each zone
   - Good behavior in Zone A provides no benefit in Zone B
   - Bad actors can "zone hop" to escape consequences
   - The network effect of trust cannot emerge

   With federation:

   - Trust is portable between federated zones
   - Good behavior creates compound value
   - Bad actors are tracked across zone boundaries
   - Network effects create positive sum dynamics

   The challenge is: how do zones agree on trust relationships when
   they may have different policies, different risk tolerances, and
   different governance structures?


1.2.  Federation Philosophy

   KTP Federation is built on these principles:

   1. Sovereignty: Each zone retains full sovereignty over its
      internal governance. Federation does not require policy
      harmonization.

   2. Reciprocity: Trust relationships are reciprocal by default.
      If Zone A trusts Zone B at factor 0.8, Zone B trusts Zone A
      at 0.8 unless explicitly negotiated otherwise.

   3. Transitivity Limits: Trust is not infinitely transitive. If
      Zone A trusts Zone B, and Zone B trusts Zone C, Zone A does
      not automatically trust Zone C.

   4. Degradation Safety: Federation failures degrade gracefully.
      If trust cannot be verified, agents are treated as unfederated,
      not blocked entirely.

   5. Transparency: Federation relationships are public. Agents can
      see which zones are federated before choosing to participate.


1.3.  Requirements Language

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174].


2.  Terminology

   Bilateral Federation:
      A direct trust relationship between exactly two zones.

   Cross-Zone Attestation:
      An attestation that is co-signed by Trust Oracles from multiple
      zones, creating portable proof of behavior.

   Federation Agreement:
      A formal contract between zones specifying trust factors,
      obligations, and dispute resolution procedures.

   Federation Hub:
      A zone that serves as a central trust anchor for multiple
      spoke zones.

   Federation Mesh:
      A network of zones with many-to-many trust relationships.

   Forward Propagation:
      The process by which positive trust events in one zone increase
      an agent's reputation in federated zones.

   Backward Propagation:
      The process by which negative trust events in one zone decrease
      an agent's reputation in previously visited zones.

   Trust Factor:
      A multiplier (0.0 to 1.0) applied to an agent's E_base when
      crossing from one zone to another.

   Trust Path:
      The chain of federated zones through which trust is calculated
      for a multi-hop agent journey.


3.  Federation Models

   Zones can federate using several models, each with different
   characteristics.

3.1.  Bilateral Federation

   The simplest model: two zones agree to trust each other.

   Characteristics:
   - Direct relationship between two zones
   - Single trust factor per direction
   - Simple to establish and maintain
   - Does not scale to many zones

   Structure:

      +----------+                     +----------+
      |  Zone A  |<--- Trust (0.9) --->|  Zone B  |
      +----------+                     +----------+

   Use cases:
   - Two organizations with partnership
   - Parent company and subsidiary
   - Vendor and customer relationship

   Agreement example:

      {
        "federation_type": "bilateral",
        "parties": [
          { "zone_id": "zone-blue-corp-a", "name": "Corp A" },
          { "zone_id": "zone-blue-corp-b", "name": "Corp B" }
        ],
        "trust_factors": {
          "a_to_b": 0.9,
          "b_to_a": 0.9
        },
        "effective_date": "2025-01-01",
        "expiration_date": "2026-01-01",
        "auto_renewal": true
      }


3.2.  Hub Federation

   A central zone acts as trust anchor for multiple spoke zones.

   Characteristics:
   - One hub zone, multiple spoke zones
   - Spokes trust hub fully (factor 1.0)
   - Spokes trust each other via hub
   - Hub has significant responsibility
   - Efficient for organizational hierarchies

   Structure:

                    +----------+
                    |   Hub    |
                    +----------+
                   /     |     \
                  /      |      \
          +------+  +------+  +------+
          |Spoke1|  |Spoke2|  |Spoke3|
          +------+  +------+  +------+

   Trust calculation (Spoke1 to Spoke2):
      Trust = Spoke1_to_Hub * Hub_to_Spoke2
      Trust = 1.0 * 1.0 = 1.0

   Use cases:
   - Corporate zone hierarchy
   - Government agency federation
   - Industry consortium

   Agreement example:

      {
        "federation_type": "hub",
        "hub": {
          "zone_id": "zone-blue-headquarters",
          "name": "Corporate HQ"
        },
        "spokes": [
          { "zone_id": "zone-blue-division-a", "trust_factor": 1.0 },
          { "zone_id": "zone-blue-division-b", "trust_factor": 1.0 },
          { "zone_id": "zone-cyan-subsidiary", "trust_factor": 0.8 }
        ],
        "spoke_to_spoke": "via_hub"
      }


3.3.  Mesh Federation

   Many zones with direct relationships to each other.

   Characteristics:
   - Multiple bilateral relationships
   - No central authority
   - Complex trust calculation
   - Most flexible but hardest to manage

   Structure:

      +--------+-------+--------+
      |        |       |        |
      v        v       v        v
   +------+  +------+  +------+  +------+
   |Zone A|--|Zone B|--|Zone C|--|Zone D|
   +------+  +------+  +------+  +------+
      |         |         |         |
      +---------+---------+---------+

   Trust calculation requires path finding:
   - Direct path: Use direct trust factor
   - Multi-hop path: Multiply factors along path
   - Multiple paths: Use highest trust path

   Use cases:
   - Industry peer networks
   - Research institution networks
   - Decentralized ecosystems

   Agreement example:

      {
        "federation_type": "mesh",
        "zone_id": "zone-blue-university-a",
        "peers": [
          {
            "zone_id": "zone-blue-university-b",
            "trust_factor": 0.95,
            "relationship": "research_partner"
          },
          {
            "zone_id": "zone-blue-university-c",
            "trust_factor": 0.90,
            "relationship": "consortium_member"
          },
          {
            "zone_id": "zone-cyan-startup-x",
            "trust_factor": 0.70,
            "relationship": "incubator_graduate"
          }
        ]
      }


3.4.  Hierarchical Federation

   Tree structure with inheritance of trust relationships.

   Characteristics:
   - Parent-child zone relationships
   - Trust inherited down hierarchy
   - Children can have additional peer relationships
   - Natural for organizational structures

   Structure:

                    +----------+
                    |   Root   |
                    +----------+
                   /            \
           +------+              +------+
           |Tier 1|              |Tier 1|
           +------+              +------+
          /        \            /        \
      +----+    +----+      +----+    +----+
      |Tier|    |Tier|      |Tier|    |Tier|
      | 2  |    | 2  |      | 2  |    | 2  |
      +----+    +----+      +----+    +----+

   Trust rules:
   - Parent trusts all descendants at factor 1.0
   - Child trusts parent at factor 1.0
   - Siblings trust each other at parent's discretion
   - Cross-branch trust calculated via common ancestor

   Use cases:
   - Government hierarchies
   - Multi-national corporations
   - Franchise networks


4.  Trust Factor Calculation

4.1.  Base Trust Factor

   The base trust factor is the starting point for cross-zone trust
   calculation:

      E_base_target = E_base_source * trust_factor

   Trust factor ranges:
   - 1.0: Full trust (same as own zone)
   - 0.8-0.99: High trust (close partner)
   - 0.5-0.79: Moderate trust (known zone)
   - 0.3-0.49: Low trust (minimal relationship)
   - 0.0-0.29: Very low trust (untrusted zone)
   - 0.0: No trust (effectively unfederated)

   Example calculation:

      Agent with E_base = 85 in Zone A
      Zone A to Zone B trust factor = 0.8
      E_base in Zone B = 85 * 0.8 = 68


4.2.  Dynamic Trust Factor

   Trust factors can be adjusted dynamically based on:

   1. Recent behavior of agents from the zone
   2. Zone's security posture
   3. Federation agreement compliance
   4. Incident history

   Dynamic adjustment formula:

      effective_trust_factor = base_trust_factor * behavior_modifier

   Where behavior_modifier is calculated from:

      behavior_modifier = 1.0 - (negative_events * penalty)
                              + (positive_events * bonus)

   Clamped to range [0.5 * base, 1.0 * base] to prevent extreme swings.


4.3.  Trust Factor Decay

   Trust factors naturally decay over time without positive
   reinforcement:

      trust_factor(t) = trust_factor(t0) * decay_rate ^ (t - t0)

   Where:
   - t0: Time of last federation activity
   - t: Current time
   - decay_rate: Typically 0.99 per day

   This ensures that inactive federations don't maintain full trust
   indefinitely. Regular cross-zone traffic maintains trust; inactive
   relationships gradually return to baseline.

   Decay is reset by:
   - Successful agent crossings
   - Cross-zone attestations
   - Federation agreement renewal


4.4.  Minimum Trust Floor

   To prevent trust from decaying to zero, federations MAY specify
   a minimum trust floor:

      effective_trust_factor = max(calculated_factor, floor)

   Typical floors:
   - Bilateral: 0.5 (maintain meaningful relationship)
   - Hub: 0.8 (maintain organizational trust)
   - Mesh: 0.3 (maintain basic connectivity)

   If trust falls below floor despite decay protection, this indicates
   a relationship problem requiring human intervention.


5.  Federation Agreements

5.1.  Agreement Structure

   A Federation Agreement is a formal contract between zones:

      {
        "agreement_id": "fed-agree-uuid-12345",
        "agreement_version": "1.0",
        "created": "2025-01-01T00:00:00Z",
        "effective": "2025-01-15T00:00:00Z",
        "expires": "2026-01-15T00:00:00Z",

        "parties": [
          {
            "zone_id": "zone-blue-corp-a",
            "legal_entity": "Corporation A Inc.",
            "jurisdiction": "US-DE",
            "signing_authority": "CISO",
            "signature": "sig:zone-a:abc123..."
          },
          {
            "zone_id": "zone-blue-corp-b",
            "legal_entity": "Corporation B Ltd.",
            "jurisdiction": "UK",
            "signing_authority": "Head of Security",
            "signature": "sig:zone-b:def456..."
          }
        ],

        "trust_terms": {
          "base_trust_factor": 0.85,
          "asymmetric": false,
          "dynamic_adjustment": true,
          "decay_rate": 0.99,
          "floor": 0.5,
          "ceiling": 0.95
        },

        "obligations": {
          "ktp_version": "1.0",
          "min_zone_type": "blue",
          "flight_recorder": "required",
          "audit_access": "quarterly",
          "incident_notification": "24_hours",
          "soul_enforcement": "required"
        },

        "data_handling": {
          "cross_zone_attestations": true,
          "trajectory_sharing": "on_request",
          "resilience_ledger_sync": "daily"
        },

        "dispute_resolution": {
          "negotiation_period_days": 30,
          "mediation": "recommended",
          "arbitration": "JAMS",
          "arbitration_jurisdiction": "US-NY",
          "governing_law": "US-NY"
        },

        "termination": {
          "notice_period_days": 90,
          "immediate_termination_causes": [
            "security_breach",
            "agreement_violation",
            "insolvency"
          ]
        }
      }


5.2.  Negotiation Protocol

   Federation agreements are negotiated through a structured protocol:

   Phase 1: Discovery
   - Zones exchange public information
   - Verify zone registration and governance
   - Assess compatibility (zone types, policies)

   Phase 2: Proposal
   - Initiating zone sends federation proposal
   - Proposal includes suggested terms
   - Receiving zone acknowledges receipt

   Phase 3: Negotiation
   - Zones exchange counter-proposals
   - Terms are negotiated
   - Legal review occurs

   Phase 4: Agreement
   - Final terms are documented
   - Signing authorities approve
   - Cryptographic signatures applied

   Phase 5: Activation
   - Agreement is published (if public federation)
   - Trust Oracles are configured
   - Federation becomes active

   Protocol messages:

      // Proposal
      {
        "message_type": "federation_proposal",
        "from_zone": "zone-blue-corp-a",
        "to_zone": "zone-blue-corp-b",
        "proposal_id": "prop-uuid-12345",
        "proposed_terms": { ... },
        "valid_until": "2025-02-01T00:00:00Z"
      }

      // Counter-proposal
      {
        "message_type": "federation_counter",
        "from_zone": "zone-blue-corp-b",
        "to_zone": "zone-blue-corp-a",
        "proposal_id": "prop-uuid-12345",
        "counter_id": "counter-uuid-67890",
        "modified_terms": { ... },
        "accepted_terms": [ ... ],
        "rejected_terms": [ ... ]
      }

      // Acceptance
      {
        "message_type": "federation_accept",
        "from_zone": "zone-blue-corp-a",
        "to_zone": "zone-blue-corp-b",
        "proposal_id": "prop-uuid-12345",
        "final_agreement": { ... },
        "signature": "sig:zone-a:xyz789..."
      }


5.3.  Agreement Lifecycle

   Federation agreements follow a lifecycle:

   1. Draft: Agreement being negotiated
   2. Pending: Agreement signed, awaiting activation
   3. Active: Agreement in force
   4. Suspended: Temporarily inactive (dispute, incident)
   5. Expiring: Within notice period of expiration
   6. Expired: Past expiration date
   7. Terminated: Ended before expiration

   State transitions:

      Draft --> Pending --> Active --> Expiring --> Expired
                             |
                             +--> Suspended --> Active
                             |
                             +--> Terminated


6.  Cross-Zone Attestations

6.1.  Attestation Types

   Cross-zone attestations provide portable proof of behavior:

   Passage Attestation:
   - Issued when agent successfully crosses zone boundary
   - Proves agent met entry requirements
   - Lightweight, high volume

   Behavior Attestation:
   - Issued periodically for agents operating in zone
   - Summarizes behavior over time period
   - Medium weight, regular cadence

   Exit Attestation:
   - Issued when agent leaves zone
   - Comprehensive summary of zone tenure
   - Detailed, one per zone visit

   Crisis Attestation:
   - Issued for behavior during high-stress periods
   - Carries extra weight for Proof of Resilience
   - Rare, high value


6.2.  Co-Signature Requirements

   Cross-zone attestations require co-signatures for maximum
   portability:

   Single-zone attestation (limited portability):
   - Signed by issuing zone's Oracle only
   - Accepted by federated zones at reduced weight
   - Weight reduction: 20%

   Dual-zone attestation (standard):
   - Signed by both source and destination zone Oracles
   - Full weight in both zones and their federations
   - Standard for zone crossings

   Multi-zone attestation (premium):
   - Signed by three or more zone Oracles
   - Full weight across all signing zones' federations
   - Used for high-value agents

   Co-signature format:

      {
        "attestation_id": "att-uuid-12345",
        "attestation_type": "exit",
        "agent_id": "agent:7gen:optimized:a1b2c3d4",
        "content": { ... },
        "signatures": [
          {
            "zone_id": "zone-blue-corp-a",
            "oracle_id": "oracle-a-1",
            "signature": "sig:oracle-a:abc...",
            "timestamp": "2025-11-25T18:00:00Z"
          },
          {
            "zone_id": "zone-blue-corp-b",
            "oracle_id": "oracle-b-1",
            "signature": "sig:oracle-b:def...",
            "timestamp": "2025-11-25T18:00:01Z"
          }
        ]
      }


6.3.  Attestation Verification

   To verify a cross-zone attestation:

   1. Parse attestation structure
   2. For each signature:
      a. Identify signing zone
      b. Retrieve zone's Oracle public key
      c. Verify signature against content
      d. Check timestamp is within acceptable range
   3. Calculate attestation weight:
      - Base weight from attestation type
      - Multiplied by signing zone trust factors
      - Bonus for multi-zone signatures
   4. Add to agent's Proof of Resilience

   Weight calculation:

      weight = base_weight * avg(trust_factors) * co_sign_bonus

   Where co_sign_bonus:
   - 1 signature: 1.0
   - 2 signatures: 1.2
   - 3+ signatures: 1.5


6.4.  Attestation Chain

   Attestations form a chain that tracks an agent's cross-zone
   journey:

      Zone A Entry --> Zone A Exit --> Zone B Entry --> Zone B Exit
           |               |               |               |
           v               v               v               v
      [Passage Att]   [Exit Att]     [Passage Att]   [Exit Att]
           |               |               |               |
           +-------+-------+-------+-------+-------+-------+
                                   |
                                   v
                          [Agent's Attestation Chain]

   The attestation chain provides:
   - Complete history of zone participation
   - Verifiable behavior record
   - Input for Proof of Resilience
   - Evidence for dispute resolution


7.  Trust Propagation

7.1.  Forward Propagation

   Positive events in one zone can increase trust in federated zones:

   Propagation trigger:
   - Agent earns high-value attestation
   - Agent achieves lineage advancement
   - Agent demonstrates exceptional behavior

   Propagation formula:

      delta_trust_federated = delta_trust_local * propagation_factor
                              * trust_factor

   Where propagation_factor is typically 0.5 (positive events
   propagate at half strength).

   Example:

      Agent earns +5 resilience in Zone A
      Zone A to Zone B trust factor = 0.8
      Propagation factor = 0.5
      Trust increase in Zone B = 5 * 0.5 * 0.8 = 2


7.2.  Backward Propagation

   Negative events in one zone can decrease trust in previously
   visited zones:

   Propagation trigger:
   - Agent commits policy violation
   - Agent causes security incident
   - Agent receives Soul veto

   Propagation formula:

      delta_trust_federated = delta_trust_local * propagation_factor
                              * trust_factor * recency_factor

   Where:
   - propagation_factor for negatives is typically 0.8 (negative
     events propagate more strongly than positive)
   - recency_factor decays based on time since zone visit

   Example:

      Agent loses -10 trust in Zone B due to incident
      Zone A to Zone B trust factor = 0.8
      Propagation factor = 0.8
      Recency factor = 0.9 (visited Zone A recently)
      Trust decrease in Zone A = 10 * 0.8 * 0.8 * 0.9 = 5.76

   Backward propagation ensures that bad actors cannot escape
   consequences by zone hopping.


7.3.  Propagation Limits

   To prevent trust cascades and gaming:

   1. Hop Limit: Trust propagates maximum 2 hops from source
   2. Decay per Hop: Each hop reduces propagation by 50%
   3. Daily Cap: Maximum trust change from propagation: ±10/day
   4. Source Verification: Propagation requires verified attestation

   These limits ensure that:
   - Local events have local primacy
   - Federation provides benefit without dominance
   - Gaming through federation is difficult


8.  Federation Events

8.1.  Zone Join

   When a new zone joins a federation:

   1. Zone completes registration requirements
   2. Zone applies for federation membership
   3. Existing members vote (if required by federation rules)
   4. Federation agreement is executed
   5. Trust Oracles are configured
   6. Zone is announced to federation
   7. Agents can begin crossing to/from new zone

   Join event broadcast:

      {
        "event_type": "zone_join",
        "federation_id": "fed-mesh-research",
        "new_zone": {
          "zone_id": "zone-blue-university-d",
          "zone_type": "blue",
          "operator": "University D"
        },
        "trust_factors": {
          "zone-blue-university-a": 0.85,
          "zone-blue-university-b": 0.85,
          "zone-blue-university-c": 0.80
        },
        "effective": "2025-12-01T00:00:00Z",
        "announced_by": "federation-coordinator"
      }


8.2.  Zone Leave

   When a zone leaves a federation:

   1. Zone announces intent to leave
   2. Notice period begins (per agreement)
   3. Agents are notified of impending change
   4. Cross-zone operations wind down
   5. Final attestations are issued
   6. Federation agreement terminates
   7. Zone is removed from federation

   Leave event broadcast:

      {
        "event_type": "zone_leave",
        "federation_id": "fed-mesh-research",
        "leaving_zone": {
          "zone_id": "zone-blue-university-d"
        },
        "reason": "voluntary_withdrawal",
        "notice_given": "2025-09-01T00:00:00Z",
        "effective": "2025-12-01T00:00:00Z",
        "agent_guidance": "Agents should complete cross-zone
                          operations before effective date"
      }


8.3.  Trust Factor Change

   When trust factors are adjusted:

   1. Triggering event occurs (incident, renegotiation, etc.)
   2. New trust factor is calculated
   3. Change is announced to affected zones
   4. Grace period for agent adjustment (optional)
   5. New factor takes effect
   6. Agents' cross-zone E_base is recalculated

   Change event broadcast:

      {
        "event_type": "trust_factor_change",
        "federation_id": "fed-bilateral-ab",
        "zone_a": "zone-blue-corp-a",
        "zone_b": "zone-blue-corp-b",
        "old_factor": 0.85,
        "new_factor": 0.70,
        "reason": "security_incident_response",
        "effective": "2025-11-26T00:00:00Z",
        "review_date": "2026-02-26T00:00:00Z"
      }


8.4.  Emergency Severance

   In case of security emergency, federation can be severed
   immediately:

   Triggers:
   - Active breach in federated zone
   - Compromise of federated zone's Oracle
   - Malicious behavior by federated zone
   - Regulatory requirement

   Severance process:

   1. Emergency severance declared
   2. All cross-zone traffic immediately blocked
   3. In-flight operations terminated
   4. Agents in severed zone are isolated
   5. Federation is suspended (not terminated)
   6. Investigation begins
   7. Resolution determines if federation resumes

   Severance event (immediate broadcast):

      {
        "event_type": "emergency_severance",
        "federation_id": "fed-bilateral-ab",
        "severing_zone": "zone-blue-corp-a",
        "severed_zone": "zone-blue-corp-b",
        "reason": "active_security_breach",
        "effective": "IMMEDIATE",
        "agent_action": "All agents in severed zone should
                        immediately cease operations",
        "contact": "security@corp-a.example.com"
      }


9.  Dispute Resolution

9.1.  Dispute Types

   Common federation disputes:

   1. Trust Factor Disputes: Disagreement over appropriate factor
   2. Attestation Disputes: Challenge to attestation validity
   3. Propagation Disputes: Disagreement over trust propagation
   4. Incident Attribution: Disagreement over incident responsibility
   5. Agreement Interpretation: Different readings of agreement terms
   6. Compliance Disputes: Alleged violation of federation obligations


9.2.  Resolution Process

   Standard resolution process:

   Phase 1: Direct Negotiation (30 days)
   - Zones attempt to resolve directly
   - Technical and legal teams engage
   - Document positions and evidence

   Phase 2: Mediation (30 days, if needed)
   - Neutral mediator engaged
   - Non-binding facilitated discussion
   - Attempt to find mutually acceptable resolution

   Phase 3: Arbitration (60 days, if needed)
   - Binding arbitration per agreement
   - Arbitrator reviews evidence
   - Decision is final and enforceable

   Dispute record:

      {
        "dispute_id": "dispute-uuid-12345",
        "parties": ["zone-blue-corp-a", "zone-blue-corp-b"],
        "type": "attestation_validity",
        "filed": "2025-11-01T00:00:00Z",
        "status": "mediation",
        "summary": "Zone A challenges validity of Exit Attestation
                    issued by Zone B for Agent X",
        "evidence": ["att-uuid-67890", "flight-record-xyz"],
        "phase_history": [
          { "phase": "negotiation", "start": "2025-11-01",
            "end": "2025-11-30", "outcome": "unresolved" },
          { "phase": "mediation", "start": "2025-12-01",
            "mediator": "KTP Mediation Services" }
        ]
      }


9.3.  Arbitration

   Arbitration is the final dispute resolution mechanism:

   Arbitrator selection:
   - Agreed upon in federation agreement
   - Must have KTP expertise
   - No conflicts of interest

   Arbitration process:
   1. Arbitrator reviews agreement and dispute
   2. Both parties submit evidence
   3. Technical experts may be consulted
   4. Arbitrator issues binding decision
   5. Decision is published (redacted if necessary)
   6. Parties must comply

   Arbitration outcomes:
   - Trust factor adjustment
   - Attestation invalidation
   - Compliance requirements
   - Financial remedies
   - Federation termination


10. Federation Governance

10.1. Governance Bodies

   Large federations may establish governance bodies:

   Federation Council:
   - Representatives from member zones
   - Sets federation-wide policy
   - Approves new members
   - Resolves disputes

   Technical Committee:
   - Technical experts from member zones
   - Develops technical standards
   - Reviews security issues
   - Recommends protocol changes

   Audit Committee:
   - Independent auditors
   - Reviews member compliance
   - Investigates incidents
   - Reports to Council


10.2. Policy Coordination

   Federated zones may coordinate policies:

   Mandatory coordination:
   - KTP protocol version
   - Trust Proof format
   - Attestation format
   - Security incident response

   Optional coordination:
   - Action risk classifications
   - Trust tier thresholds
   - Sensor configurations
   - Retention policies


10.3. Standards Evolution

   KTP will evolve. Federations must manage evolution:

   Version compatibility:
   - Zones must support current and previous major version
   - 18-month deprecation period for old versions
   - Federation agreement specifies version requirements

   Change process:
   1. Proposal published to federation
   2. Technical review period (90 days)
   3. Pilot implementation in volunteer zones
   4. Federation-wide vote
   5. Implementation timeline established
   6. Coordinated rollout


11. Security Considerations

   11.1. Federation Trust Attacks

   Attackers may attempt to manipulate federation trust.

   Mitigations:
   - Trust factors change slowly (rate limited)
   - Changes require multi-party approval
   - Anomaly detection on trust factor changes
   - Regular audit of federation relationships

   11.2. Attestation Fraud

   Zones might issue fraudulent attestations.

   Mitigations:
   - Co-signature requirements
   - Attestation verification
   - Audit of attestation patterns
   - Federation penalties for fraud

   11.3. Trust Laundering

   Agents might zone-hop to launder bad reputation.

   Mitigations:
   - Backward propagation of negative events
   - Trajectory chain verification
   - Cross-zone reputation aggregation
   - Hop limits on trust propagation


12. References

12.1.  Normative References

   [KTP-CORE]
              Perkins, C., "Kinetic Trust Protocol - Core
              Specification", NMCITRA, November 2025.

   [KTP-ZONES]
              Perkins, C., "Kinetic Trust Protocol - Blue Zone
              Specification", NMCITRA, November 2025.

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
