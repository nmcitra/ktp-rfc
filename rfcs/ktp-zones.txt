Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


          Kinetic Trust Protocol (KTP) - Blue Zone Specification

Abstract

   This document specifies Blue Zones for the Kinetic Trust Protocol
   (KTP). Blue Zones are network segments where Digital Physics is
   enforced—safe harbors on the internet where agents operate under
   physics-based constraints with cryptographic trust guarantees.

   The specification covers zone types and gradients, zone discovery
   mechanisms, ingress and egress protocols, and zone governance
   requirements.

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
       1.1.  The Need for Safe Harbors . . . . . . . . . . . . . . .  2
       1.2.  Zone Philosophy . . . . . . . . . . . . . . . . . . . .  3
       1.3.  Requirements Language . . . . . . . . . . . . . . . . .  4
   2.  Terminology . . . . . . . . . . . . . . . . . . . . . . . . .  4
   3.  Zone Types  . . . . . . . . . . . . . . . . . . . . . . . . .  6
       3.1.  Zone Gradient . . . . . . . . . . . . . . . . . . . . .  6
       3.2.  Deep Blue Zones . . . . . . . . . . . . . . . . . . . .  7
       3.3.  Blue Zones  . . . . . . . . . . . . . . . . . . . . . .  8
       3.4.  Cyan Zones  . . . . . . . . . . . . . . . . . . . . . .  9
       3.5.  Green Zones . . . . . . . . . . . . . . . . . . . . . . 10
       3.6.  Wild (Unzoned)  . . . . . . . . . . . . . . . . . . . . 11
   4.  Zone Architecture . . . . . . . . . . . . . . . . . . . . . . 12
       4.1.  Required Components . . . . . . . . . . . . . . . . . . 12
       4.2.  Zone Boundary . . . . . . . . . . . . . . . . . . . . . 13
       4.3.  Zone Gateway  . . . . . . . . . . . . . . . . . . . . . 14
   5.  Zone Discovery  . . . . . . . . . . . . . . . . . . . . . . . 15
       5.1.  DNS-Based Discovery . . . . . . . . . . . . . . . . . . 15
       5.2.  Well-Known URI Discovery  . . . . . . . . . . . . . . . 17
       5.3.  HTTP Header Discovery . . . . . . . . . . . . . . . . . 18
       5.4.  Service Mesh Discovery  . . . . . . . . . . . . . . . . 19
   6.  Zone Ingress  . . . . . . . . . . . . . . . . . . . . . . . . 20
       6.1.  Ingress Requirements  . . . . . . . . . . . . . . . . . 20
       6.2.  Trust Proof Validation  . . . . . . . . . . . . . . . . 21
       6.3.  Mass Requirements . . . . . . . . . . . . . . . . . . . 22
       6.4.  Sponsorship at Ingress  . . . . . . . . . . . . . . . . 23
       6.5.  Quarantine Zone . . . . . . . . . . . . . . . . . . . . 24
   7.  Zone Egress . . . . . . . . . . . . . . . . . . . . . . . . . 25
       7.1.  Exit Attestation  . . . . . . . . . . . . . . . . . . . 25
       7.2.  Trust Portability . . . . . . . . . . . . . . . . . . . 26
       7.3.  Cross-Zone Movement . . . . . . . . . . . . . . . . . . 27
   8.  Zone Governance . . . . . . . . . . . . . . . . . . . . . . . 28
       8.1.  Governance Requirements . . . . . . . . . . . . . . . . 28
       8.2.  Recursive Constraint  . . . . . . . . . . . . . . . . . 29
       8.3.  Zone Policy  . . . . . . . . . . . . . . . . . . . . . . 30
   9.  Zone Registration . . . . . . . . . . . . . . . . . . . . . . 31
       9.1.  Registry Structure  . . . . . . . . . . . . . . . . . . 31
       9.2.  Registration Process  . . . . . . . . . . . . . . . . . 32
       9.3.  Zone Genesis: The Bootstrap Protocol  . . . . . . . . . 33
             9.3.1.  The Bootstrap Paradox . . . . . . . . . . . . . 33
             9.3.2.  The Moment of Faith . . . . . . . . . . . . . . 34
             9.3.3.  Genesis Ceremony Requirements . . . . . . . . . 34
             9.3.4.  Identity Proofing for Genesis . . . . . . . . . 36
             9.3.5.  Genesis Block Structure . . . . . . . . . . . . 38
             9.3.6.  Post-Genesis Bootstrap  . . . . . . . . . . . . 40
             9.3.7.  Genesis for Federated Zones . . . . . . . . . . 41
             9.3.8.  Genesis Revocation  . . . . . . . . . . . . . . 42
   10. Security Considerations . . . . . . . . . . . . . . . . . . . 43
   11. IANA Considerations . . . . . . . . . . . . . . . . . . . . . 44
   12. References  . . . . . . . . . . . . . . . . . . . . . . . . . 45
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 46


1.  Introduction

   The internet was not designed for autonomous agents. It was designed
   for human-speed interactions with implicit trust relationships. As
   autonomous agents proliferate, we need designated spaces where
   physics-based constraints are guaranteed—safe harbors where both
   humans and agents can operate with confidence.

   Blue Zones are these safe harbors.

1.1.  The Need for Safe Harbors

   The current internet has no mechanism to guarantee that an endpoint
   enforces any particular authorization model. An API might use OAuth,
   API keys, mutual TLS, or nothing at all. There is no way for an
   agent to know, before connecting, what rules will govern its
   behavior.

   This uncertainty creates several problems:

   1. Race to the Bottom: Without guaranteed constraints, competitive
      pressure drives toward permissiveness. Agents that honor
      constraints lose to agents that ignore them.

   2. Trust Vacuum: Without visible enforcement, trust cannot
      accumulate. Every interaction starts from zero.

   3. Liability Ambiguity: Without clear governance, it's unclear who
      is responsible when things go wrong.

   Blue Zones solve these problems by creating network segments where:

   - KTP enforcement is guaranteed
   - Trust is portable and visible
   - Governance is explicit and auditable
   - The physics are consistent and predictable


1.2.  Zone Philosophy

   Blue Zones embody several key principles:

   1. Opt-In Governance: Zones are voluntary. Operators choose to
      deploy KTP and advertise their zone. Agents choose to enter
      zones that match their needs.

   2. Gradient, Not Binary: Zones exist on a spectrum from Deep Blue
      (maximum physics) to Wild (no KTP). This allows gradual adoption
      and appropriate constraint levels for different use cases.

   3. Portable Trust: An agent's Trust Score and Proof of Resilience
      travel with it between zones. Good behavior in one zone
      creates value in others.

   4. Recursive Constraint: Zone governance is itself subject to KTP.
      Administrators cannot exempt themselves from physics.

   5. Transparent Boundaries: Zone boundaries are discoverable and
      explicit. Agents know when they enter and exit zones.


1.3.  Requirements Language

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174].


2.  Terminology

   Blue Zone:
      A network segment where KTP is fully enforced, including all
      seven Constitutional Laws.

   Cyan Zone:
      A network segment with partial KTP enforcement, typically
      excluding some advanced features.

   Deep Blue Zone:
      A network segment with maximum KTP enforcement, requiring high
      agent mass and full trajectory verification.

   Exit Attestation:
      A signed statement from a zone's Trust Oracle attesting to an
      agent's behavior during its time in the zone.

   Federation:
      A trust relationship between zones that allows portable trust
      and cross-zone attestations.

   Green Zone:
      A network segment with minimal KTP enforcement, primarily
      passthrough Trust Proof validation.

   Ingress:
      The process of entering a zone, including Trust Proof validation
      and mass verification.

   Quarantine Zone:
      A restricted area where agents with insufficient trust can
      operate with limited capabilities while building mass.

   Wild:
      Network segments with no KTP enforcement (legacy internet).

   Zone Boundary:
      The logical perimeter of a zone, enforced by Zone Gateways.

   Zone Gateway:
      A specialized PEP that controls ingress and egress from a zone.

   Zone Gradient:
      The spectrum of zone types from Deep Blue (maximum) to Wild
      (none).


3.  Zone Types

3.1.  Zone Gradient

   Zones exist on a gradient of enforcement intensity:

   +------------+----------+----------------------------------------+
   | Zone Type  | Color    | Enforcement Level                      |
   +------------+----------+----------------------------------------+
   | Deep Blue  | #000080  | Maximum: full trajectory, high mass    |
   | Blue       | #0000FF  | Full: KTP + sponsorship                |
   | Cyan       | #00FFFF  | Partial: lightweight Trust Proof       |
   | Green      | #00FF00  | Minimal: passthrough validation        |
   | Wild       | None     | None: legacy internet                  |
   +------------+----------+----------------------------------------+

   The gradient allows:

   - Appropriate constraints for different use cases
   - Gradual adoption path for organizations
   - Interoperability between zones at different levels
   - Clear expectations for agents and operators


3.2.  Deep Blue Zones

   Deep Blue Zones provide maximum physics enforcement. They are
   designed for critical infrastructure where the highest assurance
   is required.

   Requirements:

   1. Full KTP enforcement (all seven Constitutional Laws)
   2. Minimum agent mass: E_base >= 70
   3. Full trajectory chain verification
   4. Persistent lineage required (generation 6+)
   5. Continuous environmental sensing (all 7 tensors)
   6. Soul dimension always active
   7. Threshold-signed Trust Proofs (minimum 3-of-5)
   8. Flight Recorder with cryptographic chaining
   9. Sub-second Trust Proof refresh

   Use cases:

   - Financial trading systems
   - Healthcare data systems
   - Critical infrastructure control
   - Government classified networks
   - Nuclear facility controls

   Ingress requirements:

   - Valid Trust Proof from federated zone
   - E_base >= 70
   - Trajectory chain verification (last 1000 transactions)
   - No active Soul constraints
   - Sponsor not required (agent has sufficient mass)


3.3.  Blue Zones

   Blue Zones provide full KTP enforcement suitable for enterprise
   and regulated industries.

   Requirements:

   1. Full KTP enforcement (all seven Constitutional Laws)
   2. Minimum agent mass: E_base >= 50
   3. Trajectory chain verification (sampling)
   4. Divergent or Persistent lineage (generation 3+)
   5. Environmental sensing (minimum 5 tensors)
   6. Soul dimension active for labeled data
   7. Trust Proofs signed by zone Oracle
   8. Flight Recorder required
   9. Trust Proof refresh within 10 seconds

   Use cases:

   - Enterprise applications
   - E-commerce platforms
   - SaaS providers
   - Regulated industries (non-critical)
   - Research institutions

   Ingress requirements:

   - Valid Trust Proof from federated zone OR
   - Sponsorship from zone-resident agent
   - E_base >= 50 OR sponsored
   - Basic trajectory verification
   - Soul constraint check


3.4.  Cyan Zones

   Cyan Zones provide partial KTP enforcement for general commerce
   and early adopters.

   Requirements:

   1. Core KTP enforcement (Zeroth Law, Trust Tiers)
   2. Minimum agent mass: E_base >= 30 OR sponsored
   3. Lightweight trajectory (last transaction only)
   4. Any lineage permitted
   5. Environmental sensing (minimum 3 tensors)
   6. Soul dimension optional
   7. Trust Proofs signed by zone Oracle
   8. Flight Recorder recommended
   9. Trust Proof refresh within 30 seconds

   Use cases:

   - General web applications
   - Content delivery
   - Public APIs
   - Developer platforms
   - Early KTP adopters

   Ingress requirements:

   - Valid Trust Proof OR
   - Basic identity verification
   - Sponsorship available for new agents
   - Minimal trajectory check


3.5.  Green Zones

   Green Zones provide minimal KTP enforcement, primarily serving
   as a bridge between Wild internet and KTP zones.

   Requirements:

   1. Trust Proof passthrough (validate but don't require)
   2. No minimum mass requirement
   3. No trajectory verification
   4. Any lineage permitted
   5. Environmental sensing optional
   6. Soul dimension not enforced
   7. Trust Proofs validated if present
   8. Flight Recorder optional
   9. No Trust Proof refresh requirement

   Use cases:

   - Public websites
   - Open APIs
   - Adoption on-ramps
   - Testing environments
   - Legacy system interfaces

   Ingress requirements:

   - None required
   - Trust Proof honored if provided
   - Agents without Trust Proof treated as E_trust = 0


3.6.  Wild (Unzoned)

   Wild refers to network segments with no KTP enforcement—the
   legacy internet as it exists today.

   Characteristics:

   - No Trust Oracle
   - No Trust Proof validation
   - No environmental sensing
   - Traditional authorization (if any)
   - No trust portability
   - No KTP audit trail

   Agents entering Wild from a zone:

   - Lose KTP protections
   - Cannot accumulate Proof of Resilience
   - Should exercise caution
   - May re-enter zones with prior Trust Score

   Agents entering zones from Wild:

   - Must obtain Trust Proof (may require sponsorship)
   - Start with E_base based on any prior zone history
   - May enter Quarantine Zone first


4.  Zone Architecture

4.1.  Required Components

   A Blue Zone requires the following components:

   +------------------------------------------------------------------+
   |                          BLUE ZONE                               |
   |                                                                  |
   |  +------------------------------------------------------------+  |
   |  |                   Trust Oracle Mesh                         |  |
   |  |     [Oracle 1] <--> [Oracle 2] <--> [Oracle 3]             |  |
   |  |              (threshold signatures)                         |  |
   |  +------------------------------------------------------------+  |
   |                              |                                   |
   |  +------------------------------------------------------------+  |
   |  |                Context Tensor Sensors                       |  |
   |  |   [M] [P] [H] [T] [I] [O] [S]                              |  |
   |  +------------------------------------------------------------+  |
   |                              |                                   |
   |  +------------------------------------------------------------+  |
   |  |               Policy Enforcement Points                     |  |
   |  |   [API GW PEP] [Service Mesh PEP] [IAM PEP] [DB PEP]       |  |
   |  +------------------------------------------------------------+  |
   |                              |                                   |
   |  +------------------------------------------------------------+  |
   |  |                  Agent Population                           |  |
   |  |   [Tethered] [Divergent] [Persistent]                      |  |
   |  +------------------------------------------------------------+  |
   |                              |                                   |
   |  +------------------------------------------------------------+  |
   |  |              Flight Recorder (Immutable)                    |  |
   |  +------------------------------------------------------------+  |
   |                                                                  |
   +------------------------------------------------------------------+
                                  |
                          [ZONE GATEWAY]
                                  |
   +------------------------------------------------------------------+
   |                     EXTERNAL (Other Zones / Wild)               |
   +------------------------------------------------------------------+

   Figure 1: Blue Zone Architecture


4.2.  Zone Boundary

   The zone boundary is the logical perimeter where KTP enforcement
   begins and ends. All traffic crossing the boundary MUST pass
   through a Zone Gateway.

   Boundary characteristics:

   1. Well-defined: Clear network segmentation (VLAN, subnet, etc.)
   2. Enforceable: No bypass paths around Zone Gateway
   3. Monitored: All boundary crossings logged
   4. Discoverable: Advertised via discovery mechanisms

   Boundary enforcement:

   - Network-level: Firewall rules, routing policies
   - Application-level: API gateway enforcement
   - Service-level: Service mesh policies


4.3.  Zone Gateway

   The Zone Gateway is a specialized PEP that controls zone ingress
   and egress.

   Gateway responsibilities:

   1. Validate Trust Proofs from external zones
   2. Verify agent mass meets zone minimum
   3. Check trajectory chain continuity
   4. Evaluate Soul constraints
   5. Issue zone-local Trust Proofs
   6. Generate Exit Attestations
   7. Translate between zone trust levels
   8. Log all boundary crossings

   Gateway configuration:

      {
        "zone_id": "zone-blue-prod-01",
        "zone_type": "blue",
        "min_mass": 50,
        "federation": {
          "trusted_zones": [
            "zone-blue-prod-02",
            "zone-deep-blue-critical"
          ],
          "trust_factor": {
            "zone-blue-prod-02": 1.0,
            "zone-deep-blue-critical": 1.0,
            "zone-cyan-staging": 0.8,
            "unknown": 0.5
          }
        },
        "ingress": {
          "require_trust_proof": true,
          "allow_sponsorship": true,
          "quarantine_enabled": true
        },
        "egress": {
          "issue_exit_attestation": true,
          "attestation_detail": "full"
        }
      }


5.  Zone Discovery

   Agents need to discover zone characteristics before entering.
   Multiple discovery mechanisms are supported.

5.1.  DNS-Based Discovery

   Zones SHOULD publish a DNS TXT record for discovery:

   Record format:

      _ktp.<domain>. IN TXT "v=ktp1; zone=<type>; oracle=<url>;
                             min_mass=<n>; federation=<mode>"

   Fields:

   v: Protocol version (ktp1)
   zone: Zone type (deep-blue, blue, cyan, green)
   oracle: Trust Oracle URL
   min_mass: Minimum E_base required for entry
   federation: Federation mode (open, closed, list)

   Examples:

      _ktp.example.com. IN TXT "v=ktp1; zone=blue;
          oracle=https://oracle.example.com; min_mass=50;
          federation=open"

      _ktp.critical.gov. IN TXT "v=ktp1; zone=deep-blue;
          oracle=https://oracle.critical.gov; min_mass=70;
          federation=closed"

   Discovery process:

   1. Agent queries _ktp.<target_domain> TXT record
   2. Parse response to extract zone parameters
   3. Verify Oracle certificate
   4. Determine if agent meets entry requirements
   5. Proceed with ingress protocol


5.2.  Well-Known URI Discovery

   Zones MUST publish zone information at a well-known URI:

   URI: https://<domain>/.well-known/ktp-zone

   Response format:

      {
        "version": "ktp1",
        "zone_id": "zone-blue-prod-01",
        "zone_type": "blue",
        "zone_name": "Example Production Zone",
        "operator": {
          "name": "Example Corporation",
          "contact": "security@example.com"
        },
        "trust_oracle": {
          "url": "https://oracle.example.com",
          "public_key": "-----BEGIN PUBLIC KEY-----...",
          "quorum": "3-of-5"
        },
        "requirements": {
          "min_mass": 50,
          "min_lineage": "divergent",
          "trajectory_verification": true,
          "soul_enforcement": true
        },
        "federation": {
          "mode": "open",
          "trusted_zones": [
            {
              "zone_id": "zone-blue-prod-02",
              "trust_factor": 1.0
            }
          ]
        },
        "ingress": {
          "gateway_url": "https://gateway.example.com",
          "sponsorship_available": true,
          "quarantine_available": true
        },
        "governance": {
          "policy_url": "https://example.com/ktp-policy",
          "audit_url": "https://audit.example.com"
        }
      }


5.3.  HTTP Header Discovery

   Zones SHOULD include KTP headers in HTTP responses:

   Headers:

      X-KTP-Zone: blue
      X-KTP-Zone-ID: zone-blue-prod-01
      X-KTP-Oracle: https://oracle.example.com
      X-KTP-Min-Mass: 50
      X-KTP-Federation: open

   This allows agents to discover zone characteristics from any
   HTTP interaction with zone resources.


5.4.  Service Mesh Discovery

   In service mesh environments, zone information can be discovered
   via mesh configuration:

   Istio example:

      apiVersion: networking.istio.io/v1alpha3
      kind: DestinationRule
      metadata:
        name: ktp-zone-config
        annotations:
          ktp.zone/type: "blue"
          ktp.zone/id: "zone-blue-prod-01"
          ktp.zone/oracle: "https://oracle.example.com"
          ktp.zone/min-mass: "50"

   Linkerd example:

      apiVersion: policy.linkerd.io/v1beta1
      kind: Server
      metadata:
        name: ktp-protected-server
        annotations:
          ktp.zone/type: "blue"
          ktp.zone/id: "zone-blue-prod-01"


6.  Zone Ingress

6.1.  Ingress Requirements

   To enter a zone, an agent must satisfy the zone's ingress
   requirements:

   +-------------+--------------------------------------------------+
   | Zone Type   | Ingress Requirements                             |
   +-------------+--------------------------------------------------+
   | Deep Blue   | Trust Proof + E_base >= 70 + trajectory          |
   | Blue        | Trust Proof + E_base >= 50 OR sponsorship        |
   | Cyan        | Trust Proof OR identity + optional sponsorship   |
   | Green       | None (Trust Proof honored if present)            |
   +-------------+--------------------------------------------------+


6.2.  Trust Proof Validation

   When an agent presents a Trust Proof at zone ingress:

   1. Verify signature against known Trust Oracles
      - Own zone's Oracle
      - Federated zones' Oracles

   2. Check expiration
      - Trust Proof must not be expired
      - Tolerance: 5 seconds clock skew

   3. Verify Soul constraint
      - If S = 1, deny entry
      - Log Soul veto attempt

   4. Check E_base against zone minimum
      - If E_base < min_mass, offer sponsorship or quarantine

   5. Verify trajectory chain (if required)
      - Request trajectory verification from source zone
      - Check for continuity violations

   6. Issue zone-local Trust Proof
      - Sign with zone's Oracle key
      - Apply federation trust factor to E_base


6.3.  Mass Requirements

   Different zones require different minimum mass (E_base):

   Mass calculation at ingress:

      E_base_zone = E_base_external * federation_trust_factor

   If E_base_zone < zone_min_mass:
      - Offer sponsorship (if available)
      - Offer quarantine (if available)
      - Deny entry

   Example:

      Agent from Cyan zone (E_base = 45) entering Blue zone
      Federation trust factor for Cyan: 0.8
      E_base_zone = 45 * 0.8 = 36
      Blue zone min_mass = 50
      36 < 50: Agent needs sponsorship or quarantine


6.4.  Sponsorship at Ingress

   Agents with insufficient mass can enter via sponsorship:

   1. Agent requests sponsorship from zone-resident sponsor
   2. Sponsor evaluates agent's trajectory and purpose
   3. Sponsor issues Sponsorship Bond
   4. Zone Gateway validates bond
   5. Agent enters as Tethered to sponsor
   6. Sponsor's trust is at stake for agent's behavior

   Sponsorship bond at ingress:

      {
        "bond_type": "ingress_sponsorship",
        "sponsor_id": "agent:persistent:corp:sponsor123",
        "sponsored_id": "agent:external:unknown:newagent",
        "zone_id": "zone-blue-prod-01",
        "stake_percentage": 0.15,
        "duration": "PT24H",
        "purpose": "Data analysis integration",
        "restrictions": [
          "max_action_risk: 60",
          "allowed_resources: /api/data/*",
          "denied_resources: /api/admin/*"
        ]
      }


6.5.  Quarantine Zone

   Zones MAY provide a Quarantine Zone for agents that don't meet
   entry requirements but aren't actively malicious:

   Quarantine characteristics:

   - Limited capabilities (Observer Mode or below)
   - Restricted resource access
   - Monitored behavior
   - Opportunity to build mass
   - Path to full zone entry

   Quarantine progression:

   1. Agent enters quarantine with E_trust = 20
   2. Agent performs low-risk actions successfully
   3. Trust Oracle issues attestations
   4. E_base accumulates via Proof of Resilience
   5. When E_base >= zone_min_mass, agent can exit quarantine
   6. Agent transitions to full zone membership


7.  Zone Egress

7.1.  Exit Attestation

   When an agent exits a zone, the zone SHOULD issue an Exit
   Attestation summarizing the agent's behavior:

      {
        "attestation_type": "exit",
        "zone_id": "zone-blue-prod-01",
        "agent_id": "agent:7gen:optimized:a1b2c3d4",
        "entry_time": "2025-11-25T10:00:00Z",
        "exit_time": "2025-11-25T18:00:00Z",
        "duration_seconds": 28800,
        "summary": {
          "actions_total": 4721,
          "actions_allowed": 4709,
          "actions_vetoed": 12,
          "veto_rate": 0.0025,
          "tier_history": ["operator", "analyst", "operator"],
          "min_e_trust": 68,
          "max_e_trust": 92,
          "avg_e_trust": 84,
          "soul_vetoes": 0,
          "attestations_earned": 47
        },
        "behavior_rating": "excellent",
        "signature": "sig:oracle:xyz789..."
      }

   Exit Attestations become part of the agent's portable reputation.


7.2.  Trust Portability

   An agent's trust is portable between federated zones:

   Trust components that travel:

   - E_base (adjusted by federation factor)
   - Proof of Resilience ledger
   - Trajectory chain
   - Exit Attestations from previous zones

   Trust components that don't travel:

   - Zone-specific permissions
   - Local relationships
   - Zone-specific attestations (converted to Exit Attestation)


7.3.  Cross-Zone Movement

   When moving between zones:

   1. Agent requests exit from current zone
   2. Current zone issues Exit Attestation
   3. Agent presents Trust Proof + Exit Attestation to new zone
   4. New zone validates credentials
   5. New zone calculates adjusted E_base
   6. New zone issues zone-local Trust Proof
   7. Agent enters new zone

   Cross-zone transaction:

      Zone A                    Agent                    Zone B
         |                        |                        |
         |<-- Request Exit -------|                        |
         |                        |                        |
         |--- Exit Attestation -->|                        |
         |                        |                        |
         |                        |--- Trust Proof ------->|
         |                        |    + Exit Attestation  |
         |                        |                        |
         |                        |<-- Zone-B Trust Proof --|
         |                        |                        |
         |                        |    [Agent now in Zone B]


8.  Zone Governance

8.1.  Governance Requirements

   Every zone MUST have documented governance:

   1. Zone Policy: What rules apply within the zone
   2. Operator Identity: Who operates the zone
   3. Contact Information: How to reach zone operators
   4. Dispute Resolution: How conflicts are resolved
   5. Audit Access: How governance can be verified

   Governance document:

      {
        "zone_id": "zone-blue-prod-01",
        "governance_version": "1.0",
        "effective_date": "2025-01-01",
        "operator": {
          "legal_name": "Example Corporation",
          "jurisdiction": "US-NM",
          "contact": "security@example.com"
        },
        "policy": {
          "ktp_version": "1.0",
          "constitutional_laws": "all",
          "custom_policies": [
            "https://example.com/ktp-policy-addendum"
          ]
        },
        "audit": {
          "flight_recorder": "https://audit.example.com",
          "third_party_auditor": "Example Audit LLC",
          "audit_schedule": "quarterly"
        },
        "disputes": {
          "process": "https://example.com/dispute-resolution",
          "arbitration": "JAMS",
          "jurisdiction": "US-NM"
        }
      }


8.2.  Recursive Constraint

   Zone governance is subject to KTP itself (Article VII of the
   Constitution). This means:

   1. Zone administrators are agents within the zone
   2. Administrator actions require Trust Proof
   3. Administrator actions are logged to Flight Recorder
   4. A <= E_trust applies to administrative actions
   5. Administrators cannot exempt themselves from physics

   This prevents governance hypocrisy where rules apply to others
   but not to the rule-makers.


8.3.  Zone Policy

   Zones MAY define custom policies beyond base KTP:

   Policy types:

   1. Action restrictions: Additional limits on action classes
   2. Resource restrictions: Specific resources with custom rules
   3. Time restrictions: Hours of operation, maintenance windows
   4. Agent restrictions: Requirements beyond KTP baseline

   Policy example:

      {
        "policy_id": "zone-blue-prod-01-policy",
        "extends": "ktp-base",
        "custom_rules": [
          {
            "rule_id": "no-prod-deploy-friday",
            "description": "No production deployments on Friday",
            "condition": {
              "day_of_week": [5],
              "action_class": "execute_deploy"
            },
            "effect": "deny"
          },
          {
            "rule_id": "pii-requires-analyst",
            "description": "PII access requires Analyst tier",
            "condition": {
              "resource": "/api/users/*/pii",
              "tier": ["observer"]
            },
            "effect": "deny"
          }
        ]
      }


9.  Zone Registration

9.1.  Registry Structure

   A public registry of zones enables discovery and federation:

   Registry entry:

      {
        "zone_id": "zone-blue-prod-01",
        "zone_type": "blue",
        "operator": "Example Corporation",
        "domain": "example.com",
        "oracle_url": "https://oracle.example.com",
        "oracle_public_key": "-----BEGIN PUBLIC KEY-----...",
        "discovery_url": "https://example.com/.well-known/ktp-zone",
        "registered": "2025-01-15T00:00:00Z",
        "last_verified": "2025-11-25T00:00:00Z",
        "status": "active",
        "federation": {
          "mode": "open",
          "partners": ["zone-blue-prod-02"]
        }
      }


9.2.  Registration Process

   To register a zone:

   1. Deploy KTP infrastructure meeting zone type requirements
   2. Publish discovery information (DNS, well-known URI)
   3. Submit registration to zone registry
   4. Registry verifies:
      - Discovery endpoints accessible
      - Oracle responding
      - Governance documentation complete
   5. Registry issues zone certificate
   6. Zone appears in public registry
   7. Periodic re-verification (recommended: monthly)


9.3.  Zone Genesis: The Bootstrap Protocol

   Every zone faces a bootstrap paradox: Trust Oracles need trust to
   operate, but cannot earn trust without operating. This section
   specifies how the first zone is created — the "moment of faith"
   that anchors the entire trust chain.

9.3.1.  The Bootstrap Paradox

   The paradox formally stated:

   - Trust Oracles issue Trust Proofs
   - Trust Proofs require a trusted Oracle signature
   - Oracle trust requires a trajectory of successful operation
   - Trajectory requires the Oracle to already be operating
   - Operating requires being trusted
   - Circular dependency: No starting point

   KTP resolves this paradox by grounding the initial trust in
   HUMAN IDENTITY VERIFICATION, not agent trajectory. The trust
   chain starts with verified humans, not with machines.

9.3.2.  The Moment of Faith

   Every trust system has a "moment of faith" — an initial trust
   assumption that cannot be derived from the system itself. In KTP,
   that moment is:

   "We trust verified humans to bootstrap verified machines."

   This is explicit, auditable, and bounded:
   - Explicit: The genesis ceremony is documented
   - Auditable: All participants are identity-proofed
   - Bounded: Genesis humans have limited ongoing authority

   The alternative — trusting machines to bootstrap machines —
   creates infinite regress. Human identity verification provides
   the ground.

9.3.3.  Genesis Ceremony Requirements

   Zone genesis MUST follow a formal ceremony:

   PHASE 1: TRUSTEE ASSEMBLY

   1. Identify M-of-N genesis trustees (recommended: 5-of-7)
   2. Each trustee MUST be identity-proofed to IAL3 by an
      accredited Identity Proofing Provider (see Section 9.3.4)
   3. Trustees MUST represent diverse interests:
      - At least 2 from different organizations
      - At least 1 independent technical expert
      - At least 1 legal/governance expert
   4. No single organization may control more than 2 trustees
   5. All trustees must sign Genesis Commitment document

   PHASE 2: INFRASTRUCTURE VERIFICATION

   1. Independent auditor verifies zone infrastructure:
      - Hardware security (HSMs installed, tamper-evident)
      - Software integrity (hashes match published values)
      - Network isolation (air-gapped during ceremony)
      - Conformance to KTP-CONFORMANCE requirements
   2. Auditor issues Infrastructure Attestation
   3. Attestation is signed and published

   PHASE 3: KEY GENERATION

   1. Conducted in physically secure, air-gapped environment
   2. HSMs generate zone root keypair
   3. M-of-N threshold signatures configured for trustees
   4. Root key NEVER exists in assembled form after ceremony
   5. Each trustee receives encrypted key share
   6. Key shares stored in geographically distributed locations

   PHASE 4: GENESIS BLOCK

   1. First Trust Oracle is initialized with:
      - Zone root public key
      - Genesis timestamp
      - Trustee public keys and IAL attestations
      - Infrastructure Attestation reference
      - Zone governance document hash
   2. Genesis block is signed by M-of-N trustees
   3. Genesis block becomes the immutable anchor

   PHASE 5: PUBLICATION

   1. Genesis block published to zone registry
   2. Trustee identities published (or hashes, if privacy required)
   3. IAL attestations published or verifiably referenced
   4. Ceremony recording archived (video, audit log)
   5. Independent witness attestations collected

9.3.4.  Identity Proofing for Genesis

   Genesis trustees MUST be proofed by an Identity Proofing Provider
   (IdP) that meets:

   ACCREDITATION REQUIREMENTS:
   - Certified to perform IAL3 proofing per NIST 800-63A
   - FedRAMP authorized (for US government zones) OR
   - eIDAS qualified (for EU zones) OR
   - Equivalent national certification
   - SOC 2 Type II audit within past 12 months
   - Published proofing procedures

   PROOFING PROCESS:
   - In-person verification with trained operator
   - Government-issued photo ID inspection (minimum 2 documents)
   - Biometric capture (photo, fingerprint recommended)
   - Liveness detection (anti-spoofing)
   - Database verification (where legally permitted)
   - Proofing assertion issued with cryptographic binding

   ACCEPTABLE IdP EXAMPLES:
   - Government identity agencies (DMV, passport office)
   - Qualified Trust Service Providers (QTSPs)
   - FedRAMP-authorized identity providers
   - Notary public with identity verification authority
   - Financial institutions with KYC compliance

   The IdP provides a signed Identity Assertion:

      {
        "assertion_type": "ial3_proofing",
        "subject": {
          "name_hash": "sha256:abc123...",
          "document_types": ["passport", "drivers_license"],
          "proofing_date": "2025-11-20",
          "proofing_location": "Albuquerque, NM, USA",
          "proofing_method": "in_person_biometric"
        },
        "provider": {
          "name": "Acme Identity Services",
          "accreditation": "FedRAMP_High",
          "accreditation_id": "FED-1234-5678"
        },
        "assertion_id": "ial3:acme:2025:987654",
        "validity_period": "P3Y",
        "signature": "sig:provider:xyz..."
      }

9.3.5.  Genesis Block Structure

   The Genesis Block is the zone's immutable origin:

      {
        "block_type": "genesis",
        "zone_id": "zone:blue:example:prod-01",
        "version": "1.0",
        "timestamp": "2025-11-25T14:00:00Z",
        
        "trustees": [
          {
            "trustee_id": "trustee:genesis:1",
            "name_hash": "sha256:abc...",
            "organization": "Example Corp",
            "ial_assertion": "ial3:acme:2025:987654",
            "public_key": "-----BEGIN PUBLIC KEY-----...",
            "role": "technical"
          },
          // ... additional trustees
        ],
        
        "threshold": {
          "m": 5,
          "n": 7,
          "scheme": "shamir_threshold"
        },
        
        "infrastructure": {
          "attestation_ref": "audit:infra:2025:xyz789",
          "auditor": "SecureAudit LLC",
          "audit_date": "2025-11-24",
          "conformance_level": "level2"
        },
        
        "zone_config": {
          "type": "blue",
          "governance_hash": "sha256:gov123...",
          "initial_policy_hash": "sha256:pol456..."
        },
        
        "oracle": {
          "oracle_id": "oracle:genesis:zone:example",
          "public_key": "-----BEGIN PUBLIC KEY-----...",
          "hsm_attestation": "hsm:vendor:model:serial:attestation"
        },
        
        "witnesses": [
          {
            "witness_id": "witness:independent:1",
            "attestation": "I witnessed the genesis ceremony...",
            "signature": "sig:witness:..."
          }
        ],
        
        "ceremony": {
          "location": "Secure Facility, Albuquerque, NM",
          "recording_hash": "sha256:vid789...",
          "audit_log_hash": "sha256:log012..."
        },
        
        "signatures": [
          {
            "trustee_id": "trustee:genesis:1",
            "signature": "sig:trustee:1:..."
          },
          // ... M-of-N signatures required
        ]
      }

9.3.6.  Post-Genesis Bootstrap

   After genesis, the zone bootstraps operational trust:

   FIRST 24 HOURS (Genesis Window):
   - Only genesis trustees can operate as agents
   - Trustees manually verify first operational agents
   - Each new agent requires M-of-N trustee approval
   - Maximum 10 agents can be created

   DAYS 2-7 (Nursery Period):
   - Genesis agents begin accumulating trajectory
   - E_base starts at 50 (granted by genesis)
   - Actions limited to low-risk operations
   - Trust Oracle begins issuing attestations

   DAYS 8-30 (Incubation Period):
   - Agents with sufficient trajectory can sponsor new agents
   - Normal sponsorship rules apply
   - Genesis trustees retain override authority
   - Regular security audits required

   DAY 31+ (Operational):
   - Normal KTP operations
   - Genesis trustee authority limited to:
      - Key recovery ceremonies
      - Zone dissolution
      - Emergency shutdown
   - No ongoing operational authority

9.3.7.  Genesis for Federated Zones

   When a new zone joins an existing federation:

   OPTION A: INDEPENDENT GENESIS
   - Full genesis ceremony as above
   - Federation agreement signed post-genesis
   - Trust established via federation protocol

   OPTION B: SPONSORED GENESIS (Recommended)
   - Existing federation member sponsors new zone
   - Sponsor attests to zone governance and infrastructure
   - Reduced trustee requirement (3-of-5 minimum)
   - Sponsor's trust is at stake for zone behavior
   - Faster path to operational status

   Sponsored genesis requirements:
   - Sponsor must be established zone (> 90 days operational)
   - Sponsor must have E_base > 80
   - Sponsor stakes 10% of zone trust on new zone
   - New zone begins with Federation Trust Factor = 0.5

9.3.8.  Genesis Revocation

   If the genesis is compromised (trustee breach, key exposure):

   1. Any trustee can initiate revocation
   2. M-of-N trustees must confirm
   3. Zone enters EMERGENCY mode
   4. All Trust Proofs invalidated
   5. New genesis ceremony required
   6. Agents must re-establish trust from zero

   This is catastrophic but recoverable. The explicit genesis
   ceremony means we know exactly what was trusted and can
   precisely revoke that trust.


10. Security Considerations

   10.1. Zone Spoofing

   Attackers may create fake zones to capture agent credentials.

   Mitigations:
   - Verify zone certificates
   - Use registry lookup before entering unknown zones
   - Validate Oracle public keys via multiple channels
   - Warning on unregistered zones

   10.2. Federation Abuse

   Malicious zones might issue fraudulent Exit Attestations.

   Mitigations:
   - Apply trust factor to federated zones
   - Verify attestation signatures
   - Track attestation patterns for anomalies
   - Revoke federation from misbehaving zones

   10.3. Gateway Bypass

   Attackers may attempt to enter zones without passing through
   gateways.

   Mitigations:
   - Network-level enforcement (firewall, routing)
   - Service mesh enforcement
   - Anomaly detection for ungated traffic
   - Regular boundary audits


11. IANA Considerations

   11.1. Well-Known URI Registration

   URI suffix: ktp-zone
   Specification document: This document
   Related information: KTP zone discovery

   11.2. DNS Service Name

   Service name: _ktp
   Protocol: tcp
   Specification: This document


12. References

12.1.  Normative References

   [KTP-CORE]
              Perkins, C., "Kinetic Trust Protocol - Core
              Specification", NMCITRA, November 2025.

   [KTP-ENFORCE]
              Perkins, C., "Kinetic Trust Protocol - Enforcement Layer
              Specification", NMCITRA, November 2025.

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.

12.2.  Informative References

   [KTP-FEDERATION]
              Perkins, C., "Kinetic Trust Protocol - Trust Federation
              Specification", NMCITRA, November 2025.


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
