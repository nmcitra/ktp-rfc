Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


           Kinetic Trust Protocol (KTP) - Privacy Specification

Abstract

   This document specifies privacy requirements, protections, and
   data subject rights for the Kinetic Trust Protocol (KTP). It
   operationalizes global privacy frameworks including GDPR, CCPA,
   ICCPR Article 17, and other international privacy instruments.

   Privacy is not a feature. It is a fundamental human right.
   KTP is designed with privacy as a core architectural principle,
   not a compliance checkbox.

Status of This Memo

   This document is a draft specification developed by the New Mexico
   Cyber Intelligence & Threat Response Alliance (NMCITRA).

Copyright Notice

   Copyright (c) 2025 Chris Perkins / NMCITRA.
   Licensed under Apache License, Version 2.0.

Table of Contents

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . . .  3
       1.1.  Privacy as Human Right  . . . . . . . . . . . . . . . .  3
       1.2.  The Surveillance Paradox  . . . . . . . . . . . . . . .  4
       1.3.  Privacy Hierarchy . . . . . . . . . . . . . . . . . . .  5
       1.4.  Contextual Integrity  . . . . . . . . . . . . . . . . .  6
   2.  Foundational Principles . . . . . . . . . . . . . . . . . . .  8
       2.1.  Data Minimization . . . . . . . . . . . . . . . . . . .  8
       2.2.  Purpose Limitation  . . . . . . . . . . . . . . . . . . 10
       2.3.  Storage Limitation  . . . . . . . . . . . . . . . . . . 11
       2.4.  Transparency  . . . . . . . . . . . . . . . . . . . . . 12
       2.5.  Security  . . . . . . . . . . . . . . . . . . . . . . . 13
       2.6.  Accountability  . . . . . . . . . . . . . . . . . . . . 14
   3.  Data Classification . . . . . . . . . . . . . . . . . . . . . 15
       3.1.  Personal Data in KTP  . . . . . . . . . . . . . . . . . 15
       3.2.  Sensitive Personal Data . . . . . . . . . . . . . . . . 17
       3.3.  Behavioral Data . . . . . . . . . . . . . . . . . . . . 18
       3.4.  Derived Data  . . . . . . . . . . . . . . . . . . . . . 19
   4.  Data Subject Rights . . . . . . . . . . . . . . . . . . . . . 20
       4.1.  Right of Access . . . . . . . . . . . . . . . . . . . . 20
       4.2.  Right to Rectification  . . . . . . . . . . . . . . . . 22
       4.3.  Right to Erasure  . . . . . . . . . . . . . . . . . . . 23
       4.4.  Right to Restriction  . . . . . . . . . . . . . . . . . 26
       4.5.  Right to Data Portability . . . . . . . . . . . . . . . 27
       4.6.  Right to Object . . . . . . . . . . . . . . . . . . . . 28
       4.7.  Rights Related to Automated Decision-Making . . . . . . 29
   5.  Lawful Basis and Consent  . . . . . . . . . . . . . . . . . . 31
       5.1.  Lawful Basis for Processing . . . . . . . . . . . . . . 31
       5.2.  Consent Requirements  . . . . . . . . . . . . . . . . . 33
       5.3.  Children's Privacy  . . . . . . . . . . . . . . . . . . 35
   6.  Anti-Surveillance Architecture  . . . . . . . . . . . . . . . 36
       6.1.  No Mass Surveillance  . . . . . . . . . . . . . . . . . 36
       6.2.  No Function Creep . . . . . . . . . . . . . . . . . . . 38
       6.3.  No Backdoors  . . . . . . . . . . . . . . . . . . . . . 40
       6.4.  Proportionality . . . . . . . . . . . . . . . . . . . . 41
   7.  Technical Privacy Measures  . . . . . . . . . . . . . . . . . 43
       7.1.  Privacy by Design . . . . . . . . . . . . . . . . . . . 43
       7.2.  Anonymization and Pseudonymization  . . . . . . . . . . 44
       7.3.  Differential Privacy  . . . . . . . . . . . . . . . . . 46
       7.4.  Cryptographic Privacy . . . . . . . . . . . . . . . . . 47
       7.5.  Decentralized Identity  . . . . . . . . . . . . . . . . 49
   8.  Privacy Impact Assessments  . . . . . . . . . . . . . . . . . 50
       8.1.  When PIAs Are Required  . . . . . . . . . . . . . . . . 50
       8.2.  PIA Content . . . . . . . . . . . . . . . . . . . . . . 51
       8.3.  PIA Review Process  . . . . . . . . . . . . . . . . . . 52
   9.  Cross-Border Data Transfers . . . . . . . . . . . . . . . . . 53
       9.1.  Transfer Mechanisms . . . . . . . . . . . . . . . . . . 53
       9.2.  Data Localization . . . . . . . . . . . . . . . . . . . 55
       9.3.  Federation Privacy  . . . . . . . . . . . . . . . . . . 56
   10. Special Categories  . . . . . . . . . . . . . . . . . . . . . 57
       10.1. Healthcare Settings . . . . . . . . . . . . . . . . . . 57
       10.2. Employment Context  . . . . . . . . . . . . . . . . . . 59
       10.3. Financial Services  . . . . . . . . . . . . . . . . . . 60
       10.4. Law Enforcement . . . . . . . . . . . . . . . . . . . . 61
       10.5. National Security . . . . . . . . . . . . . . . . . . . 63
       10.6. Indigenous Data Sovereignty . . . . . . . . . . . . . . 64
   11. Regulatory Alignment  . . . . . . . . . . . . . . . . . . . . 68
       11.1. GDPR (European Union) . . . . . . . . . . . . . . . . . 68
       11.2. CCPA/CPRA (California)  . . . . . . . . . . . . . . . . 71
       11.3. ICCPR Article 17  . . . . . . . . . . . . . . . . . . . 73
       11.4. Contextual Integrity Framework  . . . . . . . . . . . . 74
       11.5. Indigenous Frameworks . . . . . . . . . . . . . . . . . 76
       11.6. Other Frameworks  . . . . . . . . . . . . . . . . . . . 78
   12. Privacy Governance  . . . . . . . . . . . . . . . . . . . . . 81
   13. Breach Notification . . . . . . . . . . . . . . . . . . . . . 83
   14. Security Considerations . . . . . . . . . . . . . . . . . . . 85
   15. References  . . . . . . . . . . . . . . . . . . . . . . . . . 86
   Appendix A.  Privacy Rights Matrix  . . . . . . . . . . . . . . . 89
   Appendix B.  Data Retention Schedule  . . . . . . . . . . . . . . 91
   Appendix C.  PIA Template . . . . . . . . . . . . . . . . . . . . 93
   Appendix D.  Contextual Integrity Assessment  . . . . . . . . . . 95
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 97


1.  Introduction

1.1.  Privacy as Human Right

   Privacy is a fundamental human right recognized by:

   - Universal Declaration of Human Rights (Article 12)
   - International Covenant on Civil and Political Rights (Article 17)
   - European Convention on Human Rights (Article 8)
   - Charter of Fundamental Rights of the EU (Articles 7, 8)

   ICCPR Article 17:

      "1. No one shall be subjected to arbitrary or unlawful
       interference with his privacy, family, home or correspondence,
       nor to unlawful attacks on his honour and reputation.

       2. Everyone has the right to the protection of the law against
       such interference or attacks."

   KTP treats privacy not as a regulatory burden but as a design
   constraint of equal importance to security. A system that
   provides security through surveillance is not acceptable.

1.2.  The Surveillance Paradox

   KTP faces a fundamental tension:

   SECURITY REQUIRES VISIBILITY
   - Trust Scores require behavioral observation
   - Context Tensor requires environmental monitoring
   - Flight Recorder requires comprehensive logging
   - Proof of Resilience requires historical data

   PRIVACY REQUIRES INVISIBILITY
   - Individuals should not be tracked
   - Behavior should not create dossiers
   - Actions should not be permanently recorded
   - Inferences should not be drawn without consent

   KTP resolves this paradox through:

   1. AGGREGATE OVER INDIVIDUAL
      Sensors measure environment, not individuals.
      Statistics over populations, not profiles.

   2. EPHEMERAL OVER PERMANENT
      Trust Proofs expire in seconds.
      Behavioral data has retention limits.
      Right to erasure is real, not theoretical.

   3. LOCAL OVER CENTRAL
      Trust calculation can be distributed.
      Data need not leave local zone.
      Federation transmits proofs, not raw data.

   4. AGENT OVER HUMAN
      KTP primarily tracks agents (software), not humans.
      Human data requires explicit consent.
      Human operators have privacy rights.

1.3.  Privacy Hierarchy

   When privacy interests conflict, KTP applies this hierarchy:

   1. INDIVIDUALS
      Individual human privacy is paramount.
      Individuals can opt out of non-essential processing.
      Individual rights override system convenience.

   2. COMMUNITIES
      Community privacy protections come second.
      Cultural data and traditional knowledge protected.
      Soul constraints can encode community privacy.

   3. ENTERPRISES
      Enterprise data protection comes third.
      Trade secrets and confidential data protected.
      But not at expense of individual rights.

   4. GOVERNMENT
      Government operational security comes fourth.
      Legitimate security needs accommodated.
      But not through mass surveillance.

   5. PUBLIC INTEREST
      Public interest processing comes last.
      Requires explicit legal basis.
      Subject to proportionality review.

   This hierarchy is normative. When a feature benefits
   enterprise but harms individual privacy, the feature
   is modified or rejected.


1.4.  Contextual Integrity

   "Privacy is neither a right to secrecy nor a right to control
   but a right to appropriate flow of personal information."
   - Helen Nissenbaum

1.4.1.  The Framework

   Contextual Integrity, developed by Helen Nissenbaum, provides
   a rigorous framework for evaluating privacy that goes beyond
   simple notice-and-consent. It argues that privacy violations
   occur when information flows violate context-specific norms.

   Every information flow has parameters:
   - SENDER: Who transmits the information
   - RECIPIENT: Who receives it
   - SUBJECT: Whose information it is
   - INFORMATION TYPE: What kind of information
   - TRANSMISSION PRINCIPLE: Under what terms (confidentiality,
     consent, reciprocity, etc.)

   Privacy is violated when any parameter violates the norms
   of the operative context.

1.4.2.  Contexts in KTP

   KTP operates across multiple contexts, each with distinct norms:

   SECURITY CONTEXT
   - Norms: Information flows to protect systems
   - Appropriate: Trust Scores, threat indicators, audit trails
   - Inappropriate: Content inspection, behavioral profiling

   EMPLOYMENT CONTEXT
   - Norms: Information flows for legitimate work purposes
   - Appropriate: Role-based access, audit for compliance
   - Inappropriate: Performance surveillance, personal monitoring

   HEALTHCARE CONTEXT
   - Norms: Information flows for treatment and safety
   - Appropriate: Emergency access, care coordination
   - Inappropriate: Marketing, employment decisions

   PERSONAL CONTEXT
   - Norms: Individual autonomy and control
   - Appropriate: Self-directed data portability
   - Inappropriate: Any flow without meaningful consent

   COMMUNITY CONTEXT
   - Norms: Collective benefit and cultural protocols
   - Appropriate: Community-approved data governance
   - Inappropriate: External extraction without community consent

1.4.3.  Contextual Integrity Analysis for KTP

   For each KTP data flow, we analyze:

   TRUST SCORE CALCULATION
   - Sender: Agent (via trajectory)
   - Recipient: Trust Oracle
   - Subject: Agent (and indirectly, operator)
   - Information: Behavioral metadata
   - Transmission: Contractual, for security
   - Assessment: Appropriate IF limited to security context,
     violates integrity IF used for employment/social purposes

   FLIGHT RECORDER LOGGING
   - Sender: All components
   - Recipient: Audit system
   - Subject: Agents, operators, resources
   - Information: Decision records
   - Transmission: Legal/compliance requirement
   - Assessment: Appropriate for audit context, requires
     access controls to prevent context collapse

   FEDERATION DATA SHARING
   - Sender: Origin zone
   - Recipient: Partner zone
   - Subject: Agents operating cross-zone
   - Information: Trust Proofs (not trajectories)
   - Transmission: Bilateral agreement
   - Assessment: Appropriate IF minimized to proofs,
     violates integrity IF raw data shared

1.4.4.  Implementation Requirements

   CI-001: Context Classification Required
   - Every data flow must identify operative context
   - Multiple contexts may apply (with strictest norms governing)

   CI-002: Norm Documentation
   - Document contextual norms for each deployment domain
   - Healthcare, finance, government have distinct norms

   CI-003: Context Collapse Prevention
   - Technical controls prevent data from crossing contexts
   - Security data cannot flow to HR systems
   - Health data cannot flow to marketing

   CI-004: Transmission Principle Enforcement
   - Each flow specifies transmission principle
   - System enforces stated principle
   - Violations logged and alerted

   CI-005: Context-Aware Consent
   - Consent tied to specific contexts
   - New context requires new consent
   - Context change disclosed to subject

1.4.5.  Contextual Integrity Assessment

   Before deployment, perform Contextual Integrity Assessment:

   1. IDENTIFY all information flows
   2. CLASSIFY each flow's context
   3. DETERMINE applicable norms (entrenched and evolving)
   4. EVALUATE whether flows conform to norms
   5. JUSTIFY any norm-departing flows
   6. IMPLEMENT controls for conformance
   7. MONITOR for context violations

   See Appendix D for assessment template.


2.  Foundational Principles

2.1.  Data Minimization

   "Collect only what you need. Keep only what you must."

2.1.1.  Collection Minimization

   KTP components MUST collect only data necessary for their
   function:

   TRUST ORACLE
   - Collects: Agent ID, action requests, timestamps
   - Does NOT collect: User identity, IP addresses, device info
   - Retention: Transient (proof generation only)

   SENSORS
   - Collect: Environmental readings (CPU, memory, network)
   - Do NOT collect: Request content, user behavior, PII
   - Retention: Aggregated immediately, raw data ephemeral

   FLIGHT RECORDER
   - Collects: Decisions, context, proofs (for audit)
   - Does NOT collect: Request payloads, user data
   - Retention: Per policy (default 7 years for compliance)

   PEP
   - Collects: Authorization decisions (for caching)
   - Does NOT collect: Request/response content
   - Retention: Cache lifetime only

2.1.2.  Adequacy Principle

   Data collected must be:
   - Adequate: Sufficient for stated purpose
   - Relevant: Related to stated purpose
   - Limited: Not excessive beyond purpose

   Example: To calculate Trust Score, we need:
   - Agent identity: YES (required)
   - Agent location: NO (not needed for calculation)
   - Agent owner's name: NO (not needed)
   - Historical action count: YES (for trajectory)
   - Historical action content: NO (only metadata)

2.1.3.  Implementation Requirements

   SENSOR-001: Sensors MUST NOT capture content of communications
   SENSOR-002: Sensors MUST aggregate readings before transmission
   SENSOR-003: Sensors SHOULD operate on statistical summaries

   ORACLE-001: Oracles MUST NOT log request payloads
   ORACLE-002: Oracles MUST NOT retain data beyond proof lifetime
   ORACLE-003: Oracles SHOULD process without persistent storage

   AUDIT-001: Flight Recorder MUST NOT capture user content
   AUDIT-002: Flight Recorder SHOULD capture only decision metadata
   AUDIT-003: Flight Recorder MUST support configurable redaction

2.2.  Purpose Limitation

   "Data collected for one purpose shall not be used for another."

2.2.1.  Defined Purposes

   KTP defines these lawful processing purposes:

   PURPOSE-TRUST: Trust Score calculation
   - Data: Agent ID, action metadata, trajectory summary
   - Users: Trust Oracle, PEP

   PURPOSE-AUDIT: Security audit and compliance
   - Data: Decision records, context snapshots
   - Users: Auditors, compliance officers

   PURPOSE-SECURITY: Security incident response
   - Data: Extended context during incidents
   - Users: Security team, incident responders

   PURPOSE-IMPROVEMENT: System improvement
   - Data: Anonymized/aggregated statistics only
   - Users: System administrators, developers

2.2.2.  Purpose Creep Prevention

   Data collected for PURPOSE-TRUST:
   - SHALL NOT be used for employee monitoring
   - SHALL NOT be used for performance evaluation
   - SHALL NOT be used for marketing
   - SHALL NOT be used for law enforcement (without legal process)
   - SHALL NOT be shared with third parties (without consent)

   New purposes require:
   - Privacy Impact Assessment
   - Data subject notification
   - Consent (where consent is the legal basis)
   - Technical Committee approval (for specification changes)

2.2.3.  Implementation Requirements

   PURPOSE-001: All data MUST be tagged with collection purpose
   PURPOSE-002: Access controls MUST enforce purpose limitation
   PURPOSE-003: Audit logs MUST record purpose of each access
   PURPOSE-004: Purpose changes MUST trigger review

2.3.  Storage Limitation

   "Don't keep what you don't need."

2.3.1.  Retention Limits

   +-------------------------------------------------------------------+
   | Data Type              | Default Retention | Maximum Retention    |
   +-------------------------------------------------------------------+
   | Trust Proofs           | 60 seconds        | 5 minutes (cached)   |
   | Context Tensor readings| 24 hours          | 7 days               |
   | Trajectory summaries   | 1 year            | 7 years              |
   | Flight Recorder (ops)  | 90 days           | 1 year               |
   | Flight Recorder (audit)| 7 years           | 10 years             |
   | Identity proofing      | Duration of agent | Duration + 1 year    |
   | Sensor raw readings    | 1 hour            | 24 hours             |
   +-------------------------------------------------------------------+

2.3.2.  Retention Justification

   Longer retention requires documented justification:
   - Legal requirement (cite specific law)
   - Contractual requirement (cite specific contract)
   - Business necessity (demonstrate necessity)

   All justifications subject to periodic review (annual minimum).

2.3.3.  Deletion Requirements

   DELETION-001: Data MUST be deleted when retention expires
   DELETION-002: Deletion MUST be cryptographic where possible
   DELETION-003: Deletion MUST include backups within 30 days
   DELETION-004: Deletion MUST be logged (metadata only)

2.4.  Transparency

   "People should know what you're doing with their data."

2.4.1.  Notice Requirements

   Before KTP processes personal data:

   NOTICE-001: Clear explanation of what data is collected
   NOTICE-002: Clear explanation of why data is collected
   NOTICE-003: Clear explanation of how long data is kept
   NOTICE-004: Clear explanation of who has access
   NOTICE-005: Clear explanation of data subject rights
   NOTICE-006: Contact information for privacy inquiries

2.4.2.  Transparency for Agents

   For AI agents (non-human):
   - Agent owners/operators receive notice
   - Agents cannot consent (owners must consent)
   - Agent behavior is visible to owners

   For human operators:
   - Full privacy notice required
   - Consent required where applicable
   - All rights apply (see Section 4)

2.4.3.  System Transparency

   KTP system operation is transparent:
   - Algorithms are published (this specification)
   - Weights and thresholds are documented
   - Trust calculation is explainable
   - Decisions are logged with rationale

2.5.  Security

   "Privacy requires security, but security does not require
    privacy violation."

2.5.1.  Security Measures

   All personal data MUST be protected by:

   - Encryption at rest (AES-256 minimum)
   - Encryption in transit (TLS 1.3)
   - Access controls (role-based, least privilege)
   - Audit logging (all access logged)
   - Integrity protection (cryptographic)

   See KTP-CRYPTO for detailed requirements.

2.5.2.  Breach Protection

   See Section 13 for breach notification requirements.

2.6.  Accountability

   "Someone is responsible. Someone is answerable."

2.6.1.  Controller and Processor

   In KTP deployments:

   DATA CONTROLLER (typically):
   - Organization deploying KTP zone
   - Determines purposes and means
   - Responsible for compliance

   DATA PROCESSOR (typically):
   - Trust Oracle operator (if different from controller)
   - Cloud infrastructure provider
   - Managed service providers

   Joint controllers possible for federated zones.

2.6.2.  Documentation Requirements

   Controllers MUST maintain:
   - Records of processing activities
   - Privacy Impact Assessments
   - Data subject request logs
   - Breach notification records
   - Consent records (where applicable)


3.  Data Classification

3.1.  Personal Data in KTP

3.1.1.  Definition

   Personal data is any information relating to an identified or
   identifiable natural person ("data subject").

   In KTP, this includes:

   DIRECTLY IDENTIFYING
   - Human agent identifiers (if linked to person)
   - Email addresses in identity proofing
   - Names in sponsorship records
   - Biometric data (if used for IAL3)

   INDIRECTLY IDENTIFYING
   - Agent identifiers (if agent is operated by single person)
   - Action patterns (if unique to individual)
   - Trajectory data (if reveals individual behavior)
   - Trust Scores (if used for individual decisions)

3.1.2.  Pseudonymous Data

   Data is pseudonymous if identifier is replaced by pseudonym,
   but re-identification remains possible.

   In KTP:
   - Agent IDs are pseudonyms for human operators
   - Re-identification possible via sponsorship chain
   - Pseudonymous data is still personal data
   - But may have reduced compliance burden

3.1.3.  Anonymous Data

   Truly anonymous data is not personal data and not subject
   to privacy regulation.

   For data to be anonymous:
   - Cannot identify individual
   - Cannot be combined with other data to identify
   - Irreversibly anonymized

   KTP approaches to anonymization:
   - Aggregate statistics (min 50 agents per bucket)
   - Differential privacy (see Section 7.3)
   - K-anonymity with k≥10

3.2.  Sensitive Personal Data

   Some personal data requires heightened protection.

3.2.1.  Special Categories (GDPR Article 9)

   - Racial or ethnic origin
   - Political opinions
   - Religious or philosophical beliefs
   - Trade union membership
   - Genetic data
   - Biometric data (for identification)
   - Health data
   - Sex life or sexual orientation

   KTP SHOULD NOT process special categories.

   If unavoidable (e.g., biometric IAL3):
   - Explicit consent required
   - Processing minimized
   - Additional security measures
   - Immediate deletion when purpose fulfilled

3.2.2.  Criminal Data

   Data relating to criminal convictions requires legal basis.
   KTP Trust Scores MUST NOT be based on criminal history.

3.2.3.  Children's Data

   See Section 5.3.

3.3.  Behavioral Data

   Behavioral data is particularly sensitive because it reveals
   patterns, preferences, and predictions.

3.3.1.  Types in KTP

   TRAJECTORY DATA
   - History of agent actions
   - Basis for Trust Score
   - Reveals behavioral patterns
   - SENSITIVE: May reveal human operator behavior

   ACTION METADATA
   - What actions were requested
   - When actions occurred
   - Resource targets
   - SENSITIVE: May reveal work patterns

   CONTEXT TENSOR CONTRIBUTIONS
   - Individual sensor readings
   - Aggregated to zone level
   - NOT SENSITIVE: Environmental, not behavioral

3.3.2.  Behavioral Data Protections

   BEHAVIOR-001: Behavioral data MUST be aggregated where possible
   BEHAVIOR-002: Behavioral profiles MUST NOT be created for humans
   BEHAVIOR-003: Behavioral data MUST NOT be sold or shared
   BEHAVIOR-004: Behavioral data retention MUST be limited
   BEHAVIOR-005: Behavioral data MUST be deletable (right to erasure)

3.4.  Derived Data

   Derived data is created through inference from other data.

3.4.1.  Types in KTP

   TRUST SCORES
   - Derived from trajectory, context, lineage
   - Summarizes behavior in single number
   - May be considered personal data

   RISK ASSESSMENTS
   - Derived from sensor readings
   - Zone-level, not individual
   - Generally not personal data

   PREDICTIONS
   - If system predicts agent behavior
   - Based on historical patterns
   - PROHIBITED for human behavior prediction

3.4.2.  Derived Data Rights

   Data subjects have rights over derived data:
   - Right to know inferences are made
   - Right to access derived data
   - Right to explanation of derivation
   - Right to challenge inaccurate derived data


4.  Data Subject Rights

   Data subjects have rights over their personal data. KTP
   implementations MUST provide mechanisms to exercise these rights.

4.1.  Right of Access

   "You have the right to know what we know about you."

4.1.1.  Scope

   Data subjects may request:
   - Whether their data is processed
   - What data is processed
   - Purposes of processing
   - Categories of data
   - Recipients of data
   - Retention periods
   - Source of data (if not from subject)
   - Existence of automated decision-making

4.1.2.  Implementation

   ACCESS-001: Subject Access Request (SAR) endpoint REQUIRED
   ACCESS-002: Response within 30 days (GDPR) or 45 days (CCPA)
   ACCESS-003: No fee for first request per year
   ACCESS-004: Machine-readable format available
   ACCESS-005: Identity verification before disclosure

4.1.3.  KTP Access Endpoint

   GET /v1/privacy/subject-access/{subject_id}

   Response includes:
   {
     "subject_id": "...",
     "request_date": "...",
     "data_categories": [
       {
         "category": "agent_identity",
         "data": { ... },
         "purposes": ["trust_calculation"],
         "retention": "duration_of_agent",
         "source": "registration"
       },
       {
         "category": "trajectory_summary",
         "data": { ... },
         "purposes": ["trust_calculation", "audit"],
         "retention": "1_year",
         "source": "behavioral"
       }
     ],
     "automated_decisions": [
       {
         "type": "trust_score_calculation",
         "logic": "See KTP-CORE specification",
         "significance": "Determines access permissions"
       }
     ],
     "recipients": ["trust_oracle", "pep", "flight_recorder"],
     "your_rights": { ... }
   }

4.2.  Right to Rectification

   "You can correct what we got wrong."

4.2.1.  Scope

   Data subjects may request correction of:
   - Inaccurate data
   - Incomplete data

4.2.2.  Implementation

   RECTIFY-001: Rectification request endpoint REQUIRED
   RECTIFY-002: Response within 30 days
   RECTIFY-003: Notify recipients of corrections
   RECTIFY-004: Log rectification (but not original erroneous data)

4.2.3.  Limitations in KTP

   Some KTP data cannot be rectified:
   - Cryptographically signed records (integrity protected)
   - Trajectory chain entries (chain would break)

   For immutable data:
   - Append correction record instead
   - Original marked as corrected
   - Correction included in access requests

4.2.4.  KTP Rectification Endpoint

   POST /v1/privacy/rectification

   Request:
   {
     "subject_id": "...",
     "data_category": "agent_identity",
     "field": "metadata.purpose",
     "current_value": "Data processing agent",
     "correct_value": "Analytics agent",
     "evidence": "See attached documentation"
   }

4.3.  Right to Erasure

   "You can ask us to forget you."

   Also known as "Right to be Forgotten."

4.3.1.  Scope

   Data subjects may request erasure when:
   - Data no longer necessary for purpose
   - Consent withdrawn (and no other legal basis)
   - Subject objects (and no overriding interest)
   - Data unlawfully processed
   - Legal obligation requires deletion
   - Data collected from child

4.3.2.  Implementation

   ERASE-001: Erasure request endpoint REQUIRED
   ERASE-002: Response within 30 days
   ERASE-003: Erasure MUST include all copies
   ERASE-004: Erasure MUST include backups (within 30 days)
   ERASE-005: Notify recipients of erasure
   ERASE-006: Log erasure request (not erased data)

4.3.3.  Exceptions

   Erasure may be refused when data is needed for:
   - Legal claims defense
   - Legal obligation compliance
   - Public health reasons
   - Archiving in public interest
   - Exercise of free expression

   Refusal must be documented with specific justification.

4.3.4.  KTP Erasure Mechanics

   Erasing an agent:

   1. VERIFY identity and authority
   2. MARK agent as "erasure_pending"
   3. DELETE agent registry entry
   4. DELETE trajectory chain (or cryptographically shred)
   5. DELETE Trust Score state
   6. REDACT Flight Recorder entries (keep structure, remove PII)
   7. NOTIFY federated zones
   8. CONFIRM erasure to subject

   Flight Recorder special handling:
   - Decision records are audit-critical
   - Redact personal identifiers
   - Retain anonymized decision metadata
   - "Agent [REDACTED] performed action [type] at [time]"

4.3.5.  Cryptographic Erasure

   For encrypted data:
   - Delete encryption key
   - Data becomes cryptographically inaccessible
   - Equivalent to deletion for GDPR purposes

   KTP supports key-per-agent encryption:
   - Each agent's data encrypted with unique key
   - Erasure = delete key
   - Immediate, complete, verifiable

4.3.6.  KTP Erasure Endpoint

   DELETE /v1/privacy/erasure/{subject_id}

   Response:
   {
     "subject_id": "...",
     "erasure_status": "complete",
     "erased_categories": [
       "agent_identity",
       "trajectory_chain",
       "trust_score_state"
     ],
     "redacted_categories": [
       "flight_recorder_entries"
     ],
     "federated_zones_notified": ["zone:beta", "zone:gamma"],
     "completion_timestamp": "..."
   }

4.4.  Right to Restriction

   "You can ask us to stop using it (without deleting it)."

4.4.1.  Scope

   Data subjects may request restriction when:
   - Accuracy contested (pending verification)
   - Processing unlawful but erasure opposed
   - Data no longer needed but subject needs for legal claims
   - Subject has objected (pending verification of override)

4.4.2.  Implementation

   During restriction:
   - Data is stored but not processed
   - Only storage is lawful
   - Subject notified before lifting restriction

   RESTRICT-001: Restriction request endpoint REQUIRED
   RESTRICT-002: Technical measures to prevent processing
   RESTRICT-003: Flag data as restricted
   RESTRICT-004: Notify before unrestricting

4.5.  Right to Data Portability

   "You can take your data elsewhere."

4.5.1.  Scope

   Applies to:
   - Data provided by subject
   - Processed by automated means
   - Based on consent or contract

   Subject may request:
   - Data in structured, machine-readable format
   - Direct transmission to another controller (where feasible)

4.5.2.  Implementation

   PORTABLE-001: Export endpoint REQUIRED
   PORTABLE-002: Structured format (JSON, CSV)
   PORTABLE-003: No proprietary formats
   PORTABLE-004: Include all portable data
   PORTABLE-005: Direct transmission where technically feasible

4.5.3.  KTP Portability Format

   Portable data export:
   {
     "format": "ktp-export-v1",
     "export_date": "...",
     "subject_id": "...",
     "agent_data": {
       "identity": { ... },
       "public_key": "...",
       "lineage": { ... },
       "metadata": { ... }
     },
     "trajectory_summary": {
       "transaction_count": 1547832,
       "resilience_score": 12500,
       "oldest_record": "..."
     },
     "current_trust": {
       "e_base": 87,
       "tier": "operator"
     }
   }

   Note: Full trajectory chain may be large. Summary provided
   by default; full chain available on request.

4.6.  Right to Object

   "You can say no to certain processing."

4.6.1.  Scope

   Subjects may object to:
   - Processing based on legitimate interests
   - Processing for direct marketing (absolute right)
   - Processing for research/statistics

4.6.2.  Implementation

   OBJECT-001: Objection endpoint REQUIRED
   OBJECT-002: Stop processing unless compelling grounds shown
   OBJECT-003: Marketing objections honored immediately
   OBJECT-004: Document any override with justification

4.6.3.  Objection in KTP

   Objection to Trust Score calculation:
   - If agent is human-operated, objection may be valid
   - Controller must demonstrate compelling legitimate interest
   - If no compelling interest, agent cannot be processed
   - Agent effectively cannot participate in zone

   This creates tension: trust calculation requires data.
   Resolution: provide alternative (manual approval process)
   at subject's choice, with documented limitations.

4.7.  Rights Related to Automated Decision-Making

   "You have rights when machines decide about you."

4.7.1.  Scope

   Applies to decisions that:
   - Are solely automated (no human involvement)
   - Produce legal effects or similarly significant effects
   - Affect the data subject

   Rights include:
   - Right not to be subject to such decisions
   - Right to human intervention
   - Right to express point of view
   - Right to contest decision

4.7.2.  KTP and Automated Decisions

   KTP Trust Score calculation is automated.

   Is it "solely automated"?
   - Trust Proof issuance: Fully automated
   - But: Soul constraints add human judgment
   - But: Tier boundaries set by humans
   - Analysis: Not "solely" automated in most cases

   Does it produce "legal effects or similarly significant effects"?
   - Access denial: Potentially significant
   - Tier demotion: Significant for operator role
   - Hibernation: Very significant
   - Analysis: Yes, can be significant

4.7.3.  Implementation

   AUTOMATED-001: Document which decisions are automated
   AUTOMATED-002: Provide explanation of logic
   AUTOMATED-003: Human review available on request
   AUTOMATED-004: Allow contest of automated decisions
   AUTOMATED-005: Special protections for sensitive categories

4.7.4.  Human Review Process

   When subject requests human review of Trust Score:

   1. Automated processing paused
   2. Human reviewer examines:
      - Input data (trajectory, context)
      - Calculation logic
      - Output (Trust Score, tier)
      - Subject's concerns
   3. Reviewer may:
      - Confirm automated decision
      - Adjust manually (with documentation)
      - Escalate for further review
   4. Subject notified of outcome

   Response time: 7 days for routine, 24 hours if urgent.


5.  Lawful Basis and Consent

5.1.  Lawful Basis for Processing

   Personal data processing requires lawful basis.

5.1.1.  Available Bases (GDPR Article 6)

   (a) CONSENT: Subject has given consent
   (b) CONTRACT: Necessary for contract performance
   (c) LEGAL OBLIGATION: Required by law
   (d) VITAL INTERESTS: Protect someone's life
   (e) PUBLIC TASK: Official authority or public interest
   (f) LEGITIMATE INTERESTS: Controller's interests, balanced

5.1.2.  KTP Lawful Basis Analysis

   AGENT REGISTRATION
   - Primary basis: CONTRACT (participation agreement)
   - Alternative: CONSENT
   - Note: Agent agrees to processing by registering

   TRUST SCORE CALCULATION
   - Primary basis: LEGITIMATE INTERESTS
   - Legitimate interest: Zone security
   - Balancing: Minimal privacy impact (pseudonymous)
   - Alternative: CONTRACT (if in participation agreement)

   FLIGHT RECORDER LOGGING
   - Primary basis: LEGAL OBLIGATION (audit requirements)
   - Alternative: LEGITIMATE INTERESTS (security)
   - Note: Proportionality required

   IDENTITY PROOFING (HUMAN SPONSORS)
   - Primary basis: CONSENT (explicit)
   - Alternative: LEGAL OBLIGATION (if regulated industry)
   - Special categories: Biometric requires explicit consent

5.1.3.  Legitimate Interest Assessment

   When relying on legitimate interests:

   1. IDENTIFY the legitimate interest
      - Zone security
      - Fraud prevention
      - Network integrity

   2. NECESSITY test
      - Is processing necessary for interest?
      - Is there less intrusive alternative?

   3. BALANCING test
      - Impact on data subject
      - Reasonable expectations
      - Vulnerable individuals
      - Safeguards in place

   Document the assessment. Review annually.

5.2.  Consent Requirements

5.2.1.  Valid Consent

   Consent must be:

   FREELY GIVEN
   - No detriment for refusing
   - Genuine choice
   - Power imbalance considered

   SPECIFIC
   - For specific purpose(s)
   - Separate consent for separate purposes

   INFORMED
   - Clear information provided
   - Plain language
   - Identity of controller known

   UNAMBIGUOUS
   - Clear affirmative action
   - No pre-ticked boxes
   - Silence is not consent

5.2.2.  Consent for Special Categories

   Processing special category data (Section 3.2) requires
   EXPLICIT consent:

   - Written or recorded statement
   - Specifically mentioning the data type
   - Specifically mentioning the purpose
   - Subject demonstrably understood

5.2.3.  Withdrawal of Consent

   Consent can be withdrawn at any time.

   Withdrawal must be:
   - As easy as giving consent
   - Honored promptly
   - Without detriment to subject

   After withdrawal:
   - Processing stops
   - Data retained only if other basis exists
   - Or deleted per Section 4.3

5.2.4.  KTP Consent Implementation

   CONSENT-001: Consent recorded with timestamp
   CONSENT-002: Consent granular by purpose
   CONSENT-003: Withdrawal mechanism available
   CONSENT-004: Consent renewal for long-term processing
   CONSENT-005: Consent UI/UX reviewed for manipulation

5.3.  Children's Privacy

   Children deserve enhanced protection.

5.3.1.  Age Thresholds

   +-------------------------------------------------------------------+
   | Jurisdiction     | Digital Consent Age | Parental Required Below |
   +-------------------------------------------------------------------+
   | GDPR default     | 16                  | Yes                     |
   | GDPR (member)    | 13-16 (varies)      | Yes                     |
   | COPPA (US)       | 13                  | Yes                     |
   | UK Age Code      | 18 (for design)     | Enhanced protections    |
   +-------------------------------------------------------------------+

5.3.2.  KTP Child Protection

   CHILD-001: Age verification before human registration
   CHILD-002: Parental consent for children under threshold
   CHILD-003: No behavioral profiling of children
   CHILD-004: Enhanced data minimization for children
   CHILD-005: No retention beyond session for children
   CHILD-006: Easy parental access and deletion rights


6.  Anti-Surveillance Architecture

   "We build trust infrastructure, not surveillance infrastructure."

6.1.  No Mass Surveillance

6.1.1.  The EFF Concern

   The Electronic Frontier Foundation and similar organizations
   rightfully worry that any trust/identity system could become
   surveillance infrastructure.

   Historical examples:
   - SSN became universal identifier (scope creep)
   - CCTV became facial recognition network
   - Website cookies became behavioral tracking
   - Phone metadata became relationship mapping

   KTP must not repeat these mistakes.

6.1.2.  Architectural Safeguards

   SURVEILLANCE-001: No central database of all agent activity
   - Trajectory data stays in origin zone
   - Federation transmits proofs, not raw data
   - No cross-zone behavioral aggregation

   SURVEILLANCE-002: No persistent identifiers across contexts
   - Agents can have multiple identities
   - Linkability not required for function
   - Correlation by design prevented where possible

   SURVEILLANCE-003: No behavioral prediction of humans
   - Trust Scores predict agent behavior, not human behavior
   - Human operators not profiled
   - No "social credit" functionality

   SURVEILLANCE-004: No real-time location tracking
   - Context Tensor measures resources, not location
   - IP addresses not retained
   - Physical location not inferred

   SURVEILLANCE-005: No content inspection
   - Sensors measure metadata only
   - Request/response content not examined
   - End-to-end encryption preserved

6.1.3.  Design Patterns to Avoid

   KTP MUST NOT implement:

   - Universal unique identifiers that span contexts
   - Mandatory identity linking across systems
   - Behavioral fingerprinting of individuals
   - Social graph construction
   - Centralized query interface for subject lookup
   - Bulk data export capabilities
   - "Admin mode" that bypasses privacy controls

6.2.  No Function Creep

6.2.1.  The Function Creep Problem

   Function creep: Using a system for purposes beyond its
   original intent.

   KTP risk: Trust infrastructure → Social credit → Total control

   This is not hypothetical. It has happened before.

6.2.2.  Technical Barriers to Function Creep

   CREEP-001: Purpose tagging mandatory and enforced
   - Every data field tagged with permitted purposes
   - Access denied for non-matching purposes
   - Logged and alerted when attempted

   CREEP-002: Architectural separation
   - Trust calculation separate from enforcement
   - Audit separate from operations
   - No single system has all data

   CREEP-003: Deliberate capability limitation
   - Some things KTP cannot do by design
   - Cannot correlate across zones without federation
   - Cannot identify humans from agent behavior
   - Cannot reconstruct content from metadata

   CREEP-004: Change control for new purposes
   - New purposes require:
     * Privacy Impact Assessment
     * Public notice period (30 days)
     * Technical Committee approval
     * Implementation review

6.2.3.  Prohibited Uses

   The following uses are PROHIBITED and implementations MUST
   NOT support them:

   PROHIBITED-001: Social credit scoring of individuals
   PROHIBITED-002: Political opinion or affiliation tracking
   PROHIBITED-003: Religious belief or practice tracking
   PROHIBITED-004: Health status inference (without consent)
   PROHIBITED-005: Relationship or social graph mapping
   PROHIBITED-006: Real-time population surveillance
   PROHIBITED-007: Predictive policing input
   PROHIBITED-008: Immigration enforcement without due process
   PROHIBITED-009: Employment discrimination input
   PROHIBITED-010: Insurance underwriting without disclosure

   Implementations enabling prohibited uses are NON-CONFORMANT.

6.3.  No Backdoors

6.3.1.  The Backdoor Problem

   Governments and others pressure for "exceptional access":
   - Law enforcement access to encrypted data
   - Intelligence agency access to communications
   - "Lawful intercept" capabilities

   Backdoors are:
   - Technically dangerous (exploited by adversaries)
   - Ethically problematic (violate privacy rights)
   - Legally questionable (depending on jurisdiction)

6.3.2.  KTP Backdoor Prohibition

   BACKDOOR-001: No cryptographic backdoors
   - No key escrow with governments
   - No deliberately weakened algorithms
   - No hidden access mechanisms

   BACKDOOR-002: No administrative override for privacy
   - God Mode cannot bypass privacy controls
   - Erasure cannot be prevented by admin
   - Access requests cannot be suppressed

   BACKDOOR-003: No stealth surveillance mode
   - All monitoring is disclosed
   - No hidden data collection
   - No covert processing

   BACKDOOR-004: Warrant canary support
   - Organizations can publish warrant canaries
   - Absence of canary = potential government access
   - User notification where legally permitted

6.3.3.  Law Enforcement Access

   Law enforcement can access data through:

   LEGITIMATE PROCESS
   - Valid legal process (warrant, subpoena)
   - Specific, not bulk
   - Documented and auditable
   - Data subject notified (unless court order prohibits)

   Data provided:
   - Only data specified in legal process
   - Only data that exists (no creation of new data)
   - With documentation of what was provided
   - With challenge if process is overbroad

6.4.  Proportionality

6.4.1.  The Proportionality Principle

   Privacy interference must be:
   - Necessary for stated purpose
   - Proportionate to harm prevented
   - Minimally intrusive means used

   Per European Court of Human Rights jurisprudence.

6.4.2.  KTP Proportionality Requirements

   PROPORTIONAL-001: Least intrusive means
   - If purpose achievable with less data, use less data
   - If purpose achievable without personal data, don't use it
   - If purpose achievable with anonymized data, anonymize

   PROPORTIONAL-002: Balancing required
   - Document privacy impact
   - Document security benefit
   - Show benefit outweighs harm
   - Review periodically

   PROPORTIONAL-003: Graduated response
   - Low-risk situations: minimal data collection
   - High-risk situations: proportionately more
   - Emergency: time-limited expanded collection
   - Return to minimal after emergency


7.  Technical Privacy Measures

7.1.  Privacy by Design

   Privacy by Design (PbD) principles (Ann Cavoukian):

   1. Proactive not reactive
   2. Privacy as default
   3. Privacy embedded in design
   4. Full functionality (positive-sum)
   5. End-to-end security
   6. Visibility and transparency
   7. Respect for user privacy

7.1.1.  KTP Privacy by Design

   PBD-001: Privacy requirements in every RFC
   - Every specification includes privacy section
   - Privacy Working Group reviews all changes

   PBD-002: Privacy-preserving defaults
   - Minimal data collection by default
   - Shortest retention by default
   - Most restrictive sharing by default

   PBD-003: Privacy in development lifecycle
   - Privacy review at design phase
   - Privacy testing in QA
   - Privacy audit pre-deployment

7.2.  Anonymization and Pseudonymization

7.2.1.  Pseudonymization

   Pseudonymization replaces identifiers with pseudonyms while
   maintaining linkability within dataset.

   KTP uses pseudonymization:
   - Agent IDs are pseudonyms
   - Real identity held by sponsor (if human)
   - Reduces risk, but still personal data

7.2.2.  Anonymization

   Anonymization removes all identifying information so that
   re-identification is not possible.

   Techniques:
   - Generalization (age 34 → age 30-40)
   - Suppression (remove identifying fields)
   - Noise addition (perturb values)
   - Data swapping (exchange between records)
   - Synthetic data generation

   KTP anonymization standards:
   - K-anonymity with k ≥ 10 (at minimum)
   - L-diversity for sensitive attributes
   - T-closeness where applicable

7.2.3.  Implementation

   ANON-001: Anonymization function provided
   ANON-002: Anonymized exports for research
   ANON-003: Re-identification risk assessment
   ANON-004: No anonymization reversal attempts

7.3.  Differential Privacy

   Differential privacy provides mathematical guarantee that
   individual contribution cannot be detected.

7.3.1.  Application in KTP

   DP for aggregate statistics:
   - Context Tensor zone-wide statistics
   - Trust Score distributions
   - System performance metrics

   Implementation:
   - Add calibrated noise to queries
   - Privacy budget tracking
   - Query restrictions when budget exhausted

7.3.2.  Parameters

   DIFFERENTIAL-001: ε (epsilon) ≤ 1.0 for default
   DIFFERENTIAL-002: Privacy budget per entity per day
   DIFFERENTIAL-003: Composition accounting
   DIFFERENTIAL-004: No raw data access for stats

7.4.  Cryptographic Privacy

7.4.1.  Encryption

   Encryption protects confidentiality:
   - At rest: AES-256-GCM
   - In transit: TLS 1.3
   - Key per agent: Enables cryptographic erasure

7.4.2.  Zero-Knowledge Proofs

   ZKPs can prove properties without revealing data.

   Potential KTP applications:
   - Prove Trust Score > threshold without revealing exact score
   - Prove age > 18 without revealing birth date
   - Prove membership in group without revealing identity

   Status: OPTIONAL, for future consideration

7.4.3.  Homomorphic Encryption

   Homomorphic encryption allows computation on encrypted data.

   Potential KTP applications:
   - Trust Score calculation on encrypted trajectory
   - Aggregate statistics without decryption

   Status: EXPERIMENTAL, performance not yet practical

7.5.  Decentralized Identity

7.5.1.  Self-Sovereign Identity Alignment

   Self-sovereign identity (SSI) principles:

   - User controls identity
   - User controls data sharing
   - Minimal disclosure
   - Portability
   - No vendor lock-in

   KTP supports SSI:
   - Agents can have multiple identities
   - Data portability (Section 4.5)
   - No central identity provider required
   - Open specification enables choice

7.5.2.  Decentralized Identifiers (DIDs)

   KTP agent identifiers can be DIDs:

   did:ktp:zone:alpha:agent:a1b2c3d4

   Benefits:
   - No central registry required
   - Verifiable without contacting issuer
   - Portable across zones

   Status: RECOMMENDED for Level 3


8.  Privacy Impact Assessments

8.1.  When PIAs Are Required

   Privacy Impact Assessment (PIA) required before:

   PIA-TRIGGER-001: Deploying new KTP zone
   PIA-TRIGGER-002: Significant processing changes
   PIA-TRIGGER-003: New data categories processed
   PIA-TRIGGER-004: New technology deployment
   PIA-TRIGGER-005: Cross-border data transfers (new)
   PIA-TRIGGER-006: Large-scale processing
   PIA-TRIGGER-007: Systematic monitoring

   Per GDPR Article 35 and equivalent requirements.

8.2.  PIA Content

   PIA must include:

   PIA-CONTENT-001: Description of processing
   - What data, what purposes, what means

   PIA-CONTENT-002: Necessity assessment
   - Why is this processing necessary?
   - What alternatives were considered?

   PIA-CONTENT-003: Risk assessment
   - Risks to data subjects
   - Likelihood and severity
   - Sources of risk

   PIA-CONTENT-004: Mitigation measures
   - Technical measures
   - Organizational measures
   - Residual risk after mitigation

   PIA-CONTENT-005: Stakeholder consultation
   - Data subject consultation (if appropriate)
   - DPO consultation
   - Expert consultation (for high-risk)

   See Appendix C for PIA template.

8.3.  PIA Review Process

   1. DRAFT PIA by privacy team
   2. REVIEW by Data Protection Officer
   3. CONSULT stakeholders
   4. REVISE based on feedback
   5. APPROVE by controller
   6. PUBLISH (redacted if necessary)
   7. IMPLEMENT measures
   8. REVIEW annually


9.  Cross-Border Data Transfers

9.1.  Transfer Mechanisms

9.1.1.  GDPR Requirements

   Transfers outside EEA require legal basis:

   ADEQUACY DECISION
   - Country deemed adequate by European Commission
   - Data can flow like intra-EU
   - Currently: UK, Japan, Korea, Argentina, etc.

   APPROPRIATE SAFEGUARDS
   - Standard Contractual Clauses (SCCs)
   - Binding Corporate Rules (BCRs)
   - Codes of Conduct with binding commitments
   - Certification mechanisms

   DEROGATIONS
   - Explicit consent (for specific transfer)
   - Contract necessity
   - Legal claims
   - Vital interests
   - Public register

9.1.2.  KTP Transfer Mechanism

   TRANSFER-001: SCCs for federation with non-adequate countries
   TRANSFER-002: Supplementary measures as required
   TRANSFER-003: Transfer Impact Assessment before new routes
   TRANSFER-004: Data localization option available

9.1.3.  US-EU Transfers

   Following Schrems II:
   - Privacy Shield invalidated
   - SCCs require supplementary measures
   - EU-US Data Privacy Framework (new adequacy)

   KTP deployments must assess:
   - US surveillance laws applicability
   - Effectiveness of safeguards
   - Supplementary technical measures

9.2.  Data Localization

9.2.1.  Jurisdictional Requirements

   Some jurisdictions require data localization:
   - Russia (personal data of citizens)
   - China (important data, personal data)
   - India (certain sensitive data)
   - Others emerging

9.2.2.  KTP Localization Support

   LOCALIZE-001: Zone-local processing option
   - Data never leaves zone
   - Federation disabled for zone
   - Cross-zone proofs not accepted

   LOCALIZE-002: Residency tagging
   - Data tagged with residency requirement
   - Technical controls prevent transfer
   - Audit of transfer attempts

9.3.  Federation Privacy

   Federation introduces cross-zone data flows.

9.3.1.  Federation Data Types

   Minimal data in federation:
   - Trust Proofs (pseudonymous)
   - Zone status (aggregate)
   - Heartbeats (operational)

   NOT transferred:
   - Raw trajectory data
   - Individual sensor readings
   - Flight Recorder entries
   - Identity proofing data

9.3.2.  Federation Privacy Requirements

   FED-PRIVACY-001: Minimize federation data
   FED-PRIVACY-002: Pseudonymize where possible
   FED-PRIVACY-003: Legal basis for each federation partner
   FED-PRIVACY-004: Data Processing Agreement required
   FED-PRIVACY-005: Right to withdraw from federation


10.  Special Categories

10.1.  Healthcare Settings

   Healthcare has unique privacy requirements.

10.1.1.  Regulatory Framework

   - HIPAA (US): Protected Health Information
   - GDPR Article 9: Health data is special category
   - National laws: Additional protections

10.1.2.  Healthcare KTP Requirements

   HEALTH-001: Health data not in Trust Score calculation
   - Trust Score based on behavior, not health
   - No inference of health status from behavior

   HEALTH-002: BAA required for covered entities
   - Business Associate Agreement for HIPAA
   - Data Processing Agreement for GDPR

   HEALTH-003: Minimum necessary for healthcare operations
   - Only access needed for treatment
   - Audit of all PHI access

   HEALTH-004: Emergency access procedures
   - Break-glass for emergencies
   - Retrospective audit required
   - See KTP-PROBLEMS Hospital Problem

10.1.3.  Healthcare-Specific Protections

   - No Trust Score impact from healthcare access patterns
   - No behavioral profiling in healthcare context
   - Patient choice respected (opt-out of enhanced monitoring)
   - De-identification for research (Safe Harbor or Expert)

10.2.  Employment Context

   Employment creates power imbalance affecting consent validity.

10.2.1.  Regulatory Framework

   - GDPR: Consent may not be valid due to imbalance
   - CCPA: Employee data exemption (ending)
   - Labor laws: Various protections

10.2.2.  Employment KTP Requirements

   EMPLOY-001: Legitimate interest, not consent
   - Don't rely on employee consent
   - Use legitimate interest with balancing
   - Document necessity

   EMPLOY-002: No Trust Score in HR decisions
   - Trust Score not for hiring
   - Trust Score not for firing
   - Trust Score not for promotion
   - Trust Score for system access only

   EMPLOY-003: Works council consultation (where applicable)
   - EU: Worker representation rights
   - Consultation before deployment
   - Ongoing monitoring governance

   EMPLOY-004: Employee transparency
   - Clear notice of monitoring
   - Access to own data
   - Challenge mechanisms

10.3.  Financial Services

10.3.1.  Regulatory Framework

   - GLBA (US): Financial privacy
   - PSD2 (EU): Payment data
   - PCI-DSS: Card data
   - National banking laws

10.3.2.  Financial KTP Requirements

   FINANCE-001: Segregation from financial data
   - KTP does not access transaction content
   - Trust Score from metadata only
   - No financial decision impact

   FINANCE-002: Audit requirements
   - Financial audit needs met
   - Flight Recorder adequate for compliance
   - Retention per regulatory requirements

   FINANCE-003: Customer notice
   - Privacy notice includes KTP processing
   - Opt-out where regulation permits

10.4.  Law Enforcement

   Law enforcement access requires special care.

10.4.1.  General Principles

   - Rule of law: Legal process required
   - Proportionality: Request must be proportionate
   - Minimization: Only necessary data
   - Transparency: Notify subject where permitted

10.4.2.  KTP Law Enforcement Requirements

   LE-001: Valid legal process required
   - Warrant for content
   - Subpoena for metadata (where applicable)
   - Court order for ongoing access

   LE-002: Specific, not bulk
   - Individual subject identified
   - Time period specified
   - Data types specified
   - No fishing expeditions

   LE-003: Challenge overbroad requests
   - Legal review before compliance
   - Challenge in court if appropriate
   - Partial compliance if possible

   LE-004: Transparency where permitted
   - Notify data subject unless prohibited
   - Publish aggregate statistics
   - Warrant canary

   LE-005: No direct access
   - No API for law enforcement
   - All requests through legal process
   - Human review before disclosure

10.5.  National Security

   National security presents tension with privacy.

10.5.1.  General Principles

   - Necessity: Must be necessary, not convenient
   - Proportionality: Balanced against rights
   - Legality: Authorized by law
   - Oversight: Subject to judicial/independent oversight

10.5.2.  KTP National Security Position

   NS-001: No mass surveillance capability
   - Bulk access not supported
   - Technical architecture prevents
   - Policy prohibits

   NS-002: Legal process required
   - Same as law enforcement
   - Court order or equivalent
   - No informal requests

   NS-003: No secret capabilities
   - No hidden features for agencies
   - No undisclosed access
   - No "exceptional access" backdoors

   NS-004: International standards
   - Necessary and Proportionate principles
   - UN Special Rapporteur guidance
   - NGO input considered


10.6.  Indigenous Data Sovereignty

   Indigenous peoples have inherent rights over their data.
   These rights derive from sovereignty, not from Western
   privacy frameworks.

10.6.1.  Foundational Recognition

   "Data is a living taonga (treasure). It carries the breath
   of our ancestors and speaks to our future generations."
   - Māori Data Sovereignty Network

   Indigenous Data Sovereignty recognizes that:
   - Indigenous peoples have rights to control data FROM them
   - Indigenous peoples have rights to control data ABOUT them
   - Collective rights exist alongside individual rights
   - Data governance follows cultural protocols
   - Western privacy frameworks are insufficient

   KTP acknowledges these rights and provides mechanisms
   for their implementation.

10.6.2.  International Instruments

   UNITED NATIONS DECLARATION ON THE RIGHTS OF INDIGENOUS PEOPLES
   (UNDRIP, 2007)

   Article 31:
   "Indigenous peoples have the right to maintain, control,
   protect and develop their cultural heritage, traditional
   knowledge and traditional cultural expressions, as well as
   the manifestations of their sciences, technologies and
   cultures, including... genetic resources, seeds, medicines,
   knowledge of the properties of fauna and flora..."

   Article 18:
   "Indigenous peoples have the right to participate in
   decision-making in matters which would affect their rights,
   through representatives chosen by themselves in accordance
   with their own procedures..."

   Article 19 (Free, Prior and Informed Consent):
   "States shall consult and cooperate in good faith with the
   indigenous peoples concerned through their own representative
   institutions in order to obtain their free, prior and informed
   consent before adopting and implementing legislative or
   administrative measures that may affect them."

   ILO CONVENTION 169 (Indigenous and Tribal Peoples, 1989)
   - Consultation and participation rights
   - Respect for customs and traditions
   - Prior consultation for development projects

10.6.3.  Indigenous Data Governance Frameworks

   CARE PRINCIPLES FOR INDIGENOUS DATA GOVERNANCE
   (Global Indigenous Data Alliance, 2019)

   C - COLLECTIVE BENEFIT
   - Data ecosystems shall be designed to enable Indigenous
     peoples to derive benefit from data
   - Inclusive development and innovation
   - Improved governance and citizen engagement
   - Equitable outcomes

   A - AUTHORITY TO CONTROL
   - Indigenous peoples' rights and interests in Indigenous data
     must be recognized and their authority to control such data
     respected
   - Indigenous data governance
   - Governance of Indigenous data
   - Self-determination

   R - RESPONSIBILITY
   - Those working with Indigenous data have a responsibility
     to share how those data are used to support Indigenous
     peoples' self-determination and collective benefit
   - For positive relationships
   - For expanding capability and capacity
   - For Indigenous languages and worldviews

   E - ETHICS
   - Indigenous peoples' rights and wellbeing should be the
     primary concern at all stages of the data life cycle
   - For minimizing harm and maximizing benefit
   - For justice
   - For future use

   OCAP® PRINCIPLES (First Nations Information Governance Centre)
   (Specific to First Nations in Canada)

   O - OWNERSHIP
   - A community or group owns information collectively in the
     same way an individual owns their personal information

   C - CONTROL
   - Indigenous peoples, their communities and representative
     bodies are within their rights to seek control over all
     aspects of research and information management processes

   A - ACCESS
   - Indigenous peoples must have access to information and data
     about themselves and their communities

   P - POSSESSION
   - Physical control of data. Possession is a mechanism to
     assert and protect ownership and control

   TE MANA RARAUNGA (Māori Data Sovereignty Network)
   - Whakapapa (relationships and origins)
   - Whanaungatanga (kinship and collective responsibility)
   - Kotahitanga (unity and collective action)
   - Kaitiakitanga (guardianship and stewardship)
   - Manaakitanga (hospitality and care)
   - Rangatiratanga (self-determination and sovereignty)

10.6.4.  KTP Indigenous Data Requirements

   IND-001: Recognition of Collective Rights
   - Individual consent insufficient for Indigenous data
   - Community consent mechanisms required
   - Traditional governance structures respected

   IND-002: Indigenous Data Classification
   - Data ABOUT Indigenous peoples
   - Data COLLECTED BY Indigenous peoples
   - Data WITH Indigenous knowledge
   - Traditional knowledge and cultural expressions
   - Genetic and biological data

   IND-003: Free, Prior and Informed Consent (FPIC)
   - Before processing Indigenous data
   - Through appropriate community representatives
   - In culturally appropriate manner
   - With right to refuse without penalty

   IND-004: Indigenous Data Governance Zones
   - Zones can be governed by Indigenous communities
   - Zone policies follow traditional protocols
   - Soul constraints encode community decisions
   - External access requires community consent

   IND-005: No Extraction Without Consent
   - Data cannot be extracted from Indigenous zones
   - Federation only with explicit community agreement
   - Research use requires community approval
   - Commercial use requires benefit-sharing

   IND-006: Repatriation Rights
   - Communities can request return of data
   - Historical data subject to repatriation
   - Erasure on community request

   IND-007: Cultural Protocol Integration
   - Data handling follows cultural protocols
   - Sacred/restricted data categories supported
   - Seasonal or ceremonial access restrictions
   - Gender-based access restrictions where appropriate

10.6.5.  Implementation Mechanisms

   INDIGENOUS DATA SOVEREIGNTY ZONES

   KTP supports Indigenous-governed zones:
   {
     "zone_id": "zone:iwi:ngati-example",
     "governance": {
       "type": "indigenous_collective",
       "authority": "Ngāti Example Iwi Authority",
       "protocols": "te_mana_raraunga",
       "consent_mechanism": "hui_decision"
     },
     "soul_constraints": [
       {
         "constraint_type": "FPIC_REQUIRED",
         "scope": "all_external_access",
         "authority": "iwi_governance_board"
       },
       {
         "constraint_type": "NO_EXTRACTION",
         "scope": "traditional_knowledge",
         "exceptions": "community_approved_research"
       }
     ]
   }

   COMMUNITY CONSENT ENDPOINTS

   POST /v1/indigenous/consent-request
   {
     "requesting_entity": "...",
     "purpose": "research|commercial|government|other",
     "data_scope": "...",
     "duration": "...",
     "benefit_sharing": { ... },
     "community_id": "...",
     "cultural_protocol_acknowledgment": true
   }

   Response requires community process completion:
   {
     "consent_status": "pending_hui|approved|denied",
     "consent_authority": "...",
     "conditions": [ ... ],
     "benefit_sharing_agreement": { ... },
     "expiration": "..."
   }

10.6.6.  Traditional Knowledge Protection

   Traditional Knowledge (TK) requires special protection:

   TK-001: TK is not "public domain"
   - Prior publication does not void rights
   - Misappropriated TK can be reclaimed
   - Cultural protocols continue to apply

   TK-002: TK Classification
   - Sacred/secret: Never shared without ceremony
   - Restricted: Limited by gender, age, initiation
   - Community: Shared within community
   - Public: Appropriate for external sharing

   TK-003: TK in KTP
   - TK data type recognized
   - Access controls per classification
   - No machine learning on TK without consent
   - No derivative works without permission

10.6.7.  Researcher and Developer Obligations

   Those building KTP systems involving Indigenous data must:

   1. ENGAGE EARLY
      - Before design decisions
      - Not just before deployment
      - Throughout development

   2. RESPECT GOVERNANCE
      - Follow community decision processes
      - Accept "no" as valid answer
      - Don't pressure for consent

   3. BUILD RELATIONSHIPS
      - Long-term engagement, not extraction
      - Reciprocity and mutual benefit
      - Cultural competency development

   4. SHARE BENEFITS
      - Capacity building in communities
      - Data skills transfer
      - Economic benefit sharing
      - Recognition and attribution

   5. RETURN DATA
      - Communities receive copies
      - Results shared first with communities
      - Interpretation involves communities


11.  Regulatory Alignment

11.1.  GDPR (European Union)

   General Data Protection Regulation (EU) 2016/679

11.1.1.  Alignment Summary

   +-------------------------------------------------------------------+
   | GDPR Requirement              | KTP Implementation               |
   +-------------------------------------------------------------------+
   | Lawful basis (Art. 6)         | Section 5.1                      |
   | Special categories (Art. 9)   | Section 3.2, 5.2.2               |
   | Transparency (Art. 12-14)     | Section 2.4                      |
   | Data subject rights (Art. 15-22)| Section 4                      |
   | Data protection by design (Art. 25)| Section 7.1                 |
   | Security (Art. 32)            | Section 2.5, KTP-CRYPTO          |
   | Breach notification (Art. 33-34)| Section 13                     |
   | DPIA (Art. 35)                | Section 8                        |
   | Data transfers (Art. 44-49)   | Section 9                        |
   | DPO (Art. 37-39)              | Section 12                       |
   +-------------------------------------------------------------------+

11.1.2.  GDPR-Specific Requirements

   GDPR-001: DPO designation where required
   GDPR-002: Records of processing activities
   GDPR-003: Representative in EU (if applicable)
   GDPR-004: Supervisory authority cooperation

11.2.  CCPA/CPRA (California)

   California Consumer Privacy Act / Privacy Rights Act

11.2.1.  Alignment Summary

   +-------------------------------------------------------------------+
   | CCPA/CPRA Requirement         | KTP Implementation               |
   +-------------------------------------------------------------------+
   | Right to know (§1798.100)     | Section 4.1                      |
   | Right to delete (§1798.105)   | Section 4.3                      |
   | Right to opt-out (§1798.120)  | Section 4.6                      |
   | Right to correct (§1798.106)  | Section 4.2                      |
   | Right to portability (§1798.130)| Section 4.5                    |
   | Data minimization             | Section 2.1                      |
   | Purpose limitation            | Section 2.2                      |
   | Security (§1798.81.5)         | Section 2.5                      |
   +-------------------------------------------------------------------+

11.2.2.  CCPA-Specific Requirements

   CCPA-001: "Do Not Sell" support
   - KTP does not sell personal information
   - But tracking across sites could trigger
   - Implement opt-out where applicable

   CCPA-002: No financial incentives for data
   - No discount for more data
   - No penalty for less data

   CCPA-003: Authorized agent support
   - Third party can exercise rights
   - Verification required

11.3.  ICCPR Article 17

   International Covenant on Civil and Political Rights

11.3.1.  Alignment

   ICCPR requires protection against arbitrary or unlawful
   interference with privacy.

   KTP alignment:
   - Lawful basis required (not arbitrary)
   - Proportionality review (not excessive)
   - Legal protections (judicial oversight)
   - No discrimination

11.3.2.  Human Rights Due Diligence

   ICCPR-001: Human rights impact assessment
   - Consider deployment impacts
   - Especially in high-risk jurisdictions
   - Document and mitigate

   ICCPR-002: No deployment for rights violations
   - Decline deployment if used for oppression
   - Soul constraints can encode refusal
   - Exit strategy for existing deployments

11.4.  Contextual Integrity Framework

   Helen Nissenbaum's Contextual Integrity provides a philosophical
   and practical framework for privacy that KTP operationalizes.

11.4.1.  Framework Elements

   INFORMATIONAL NORMS
   - Context-specific rules governing information flow
   - Determine appropriate transmission principles
   - Evolve with social practice

   ACTORS
   - Data subjects, senders, recipients
   - Roles define expectations

   ATTRIBUTES
   - Types of information
   - Context determines sensitivity

   TRANSMISSION PRINCIPLES
   - Confidentiality, consent, reciprocity
   - Notice, entitlement, forced

11.4.2.  KTP Alignment

   +-------------------------------------------------------------------+
   | CI Element             | KTP Implementation                       |
   +-------------------------------------------------------------------+
   | Context identification | Zone purpose, domain classification     |
   | Actor roles            | Agent lineage, sponsor relationships    |
   | Information types      | Data classification (§3)                 |
   | Transmission principles| Purpose limitation (§2.2), consent (§5) |
   | Norm enforcement       | Soul constraints, PEP policies           |
   | Context collapse       | Zone isolation, federation controls      |
   +-------------------------------------------------------------------+

   CI-ALIGN-001: Context documentation for each zone
   CI-ALIGN-002: Norm specification in zone policy
   CI-ALIGN-003: Transmission principle enforcement
   CI-ALIGN-004: Context integrity assessment (Appendix D)

11.4.3.  Context Collapse Prevention

   Context collapse occurs when information flows across contexts
   inappropriately. KTP prevents this through:

   - Zone boundaries (architectural)
   - Purpose tagging (metadata)
   - Access controls (enforcement)
   - Federation restrictions (policy)

11.5.  Indigenous Frameworks

   Indigenous Data Sovereignty frameworks have emerged as critical
   complements to Western privacy law.

11.5.1.  Framework Comparison

   +-------------------------------------------------------------------+
   | Framework        | Origin    | Focus                              |
   +-------------------------------------------------------------------+
   | CARE Principles  | Global    | Collective benefit, authority      |
   | OCAP®            | Canada    | Ownership, control, access, possess|
   | Te Mana Raraunga | Aotearoa  | Māori data sovereignty             |
   | USIDSN          | USA       | US Indigenous data sovereignty      |
   | Maiam nayri      | Australia | Aboriginal data sovereignty         |
   +-------------------------------------------------------------------+

11.5.2.  Integration with Privacy Law

   Indigenous frameworks complement GDPR/CCPA by adding:

   - Collective rights (not just individual)
   - Community consent (not just individual consent)
   - Benefit sharing (not just non-harm)
   - Repatriation rights (not just portability)
   - Traditional knowledge protection (not just PII)

   KTP implements these through Section 10.6.

11.5.3.  Key References

   - UNDRIP (2007): Articles 18, 19, 31
   - ILO Convention 169 (1989)
   - CARE Principles (2019)
   - OCAP® Principles (First Nations, Canada)
   - Te Mana Raraunga Charter (2018)

11.6.  Other Frameworks

11.6.1.  APEC Privacy Framework

   Asia-Pacific Economic Cooperation

   Principles:
   - Preventing harm
   - Notice
   - Collection limitation
   - Use limitation
   - Choice
   - Integrity
   - Security
   - Access and correction
   - Accountability

   KTP fully aligned.

11.6.2.  OECD Privacy Guidelines

   Organisation for Economic Co-operation and Development (1980/2013)

   Principles:
   - Collection limitation
   - Data quality
   - Purpose specification
   - Use limitation
   - Security safeguards
   - Openness
   - Individual participation
   - Accountability

   KTP fully aligned.

11.6.3.  Council of Europe Convention 108+

   Convention for the Protection of Individuals with regard to
   Automatic Processing of Personal Data (modernized)

   KTP aligns with:
   - Legitimate processing
   - Data quality
   - Special categories
   - Data subject rights
   - Trans-border flows
   - Supervisory authorities

11.6.4.  Other National Laws

   KTP designed to align with:

   - Brazil LGPD (Lei Geral de Proteção de Dados)
   - India DPDP (Digital Personal Data Protection)
   - Japan APPI (Act on Protection of Personal Information)
   - South Korea PIPA (Personal Information Protection Act)
   - Australia Privacy Act 1988
   - Canada PIPEDA (Personal Information Protection and Electronic
     Documents Act)
   - Singapore PDPA (Personal Data Protection Act)
   - Thailand PDPA
   - South Africa POPIA

   Consult local counsel for specific jurisdiction.


12.  Privacy Governance

12.1.  Data Protection Officer

   Where required (GDPR, national law), appoint DPO.

   DPO role:
   - Advise on compliance
   - Monitor compliance
   - Cooperate with authorities
   - Contact point for subjects

12.2.  Privacy Team

   PRIVACY-TEAM-001: Privacy expertise in development
   PRIVACY-TEAM-002: Privacy review in change process
   PRIVACY-TEAM-003: Privacy training for staff
   PRIVACY-TEAM-004: Privacy incident response capability

12.3.  Documentation

   Maintain:
   - Records of processing activities
   - PIAs and reviews
   - Consent records
   - Data subject requests and responses
   - Breach records
   - Training records


13.  Breach Notification

13.1.  Definition

   Personal data breach: Security incident leading to accidental or
   unlawful destruction, loss, alteration, unauthorized disclosure,
   or access to personal data.

13.2.  Detection

   BREACH-001: Monitoring for breach indicators
   BREACH-002: Incident classification procedure
   BREACH-003: Breach determination within 24 hours

13.3.  Notification Requirements

   AUTHORITY NOTIFICATION (GDPR: 72 hours)
   - To supervisory authority
   - Unless unlikely to result in risk
   - Include: nature, categories, numbers, consequences, measures

   SUBJECT NOTIFICATION (without undue delay)
   - When high risk to rights and freedoms
   - Clear, plain language
   - Include: nature, contact, consequences, measures

13.4.  Documentation

   BREACH-004: Document all breaches
   BREACH-005: Document decision not to notify (with justification)
   BREACH-006: Retain records for supervision


14.  Security Considerations

   Security and privacy are complementary, not competing.

14.1.  Privacy Requires Security

   Without security:
   - Data cannot be protected
   - Access controls meaningless
   - Encryption useless

14.2.  Security Does Not Require Privacy Violation

   Security can be achieved without:
   - Mass surveillance
   - Behavioral profiling
   - Content inspection
   - Permanent retention

   KTP proves this.

14.3.  Privacy Enhancing Technologies

   Invest in PETs:
   - Differential privacy
   - Zero-knowledge proofs
   - Secure multi-party computation
   - Federated learning
   - Homomorphic encryption


15.  References

15.1.  Legal Instruments

   [UDHR]     United Nations, "Universal Declaration of Human Rights",
              1948.

   [ICCPR]    United Nations, "International Covenant on Civil and
              Political Rights", 1966.

   [GDPR]     European Parliament, "General Data Protection Regulation
              (EU) 2016/679", 2016.

   [CCPA]     California Legislature, "California Consumer Privacy
              Act of 2018", 2018.

   [CPRA]     California Legislature, "California Privacy Rights
              Act of 2020", 2020.

   [COE108]   Council of Europe, "Convention for the Protection of
              Individuals with regard to Automatic Processing of
              Personal Data" (Convention 108+), 2018.

   [APEC]     Asia-Pacific Economic Cooperation, "APEC Privacy
              Framework", 2015.

   [OECD]     OECD, "Guidelines Governing the Protection of Privacy
              and Transborder Flows of Personal Data", 2013.

15.2.  Guidance

   [A29WP]    Article 29 Working Party/EDPB Opinions and Guidelines.

   [NIST-PF]  NIST, "Privacy Framework: A Tool for Improving Privacy
              through Enterprise Risk Management", 2020.

   [CAVOUKIAN] Cavoukian, A., "Privacy by Design: The 7 Foundational
              Principles", 2011.

15.3.  Contextual Integrity

   [NISSENBAUM]
              Nissenbaum, H., "Privacy in Context: Technology, Policy,
              and the Integrity of Social Life", Stanford University
              Press, 2010.

   [NISSENBAUM-RESPECTINGCONTEXT]
              Nissenbaum, H., "Respecting Context to Protect Privacy:
              Why Meaning Matters", Science and Engineering Ethics,
              24(3), 831-852, 2018.

   [CI-FRAMEWORK]
              Nissenbaum, H., "A Contextual Approach to Privacy Online",
              Daedalus, 140(4), 32-48, 2011.

15.4.  Indigenous Data Sovereignty

   [UNDRIP]   United Nations, "Declaration on the Rights of Indigenous
              Peoples", A/RES/61/295, 2007.

   [ILO169]   International Labour Organization, "Indigenous and Tribal
              Peoples Convention", C169, 1989.

   [CARE]     Global Indigenous Data Alliance, "CARE Principles for
              Indigenous Data Governance", 2019.
              https://www.gida-global.org/care

   [OCAP]     First Nations Information Governance Centre, "The First
              Nations Principles of OCAP®", 2014.
              https://fnigc.ca/ocap-training/

   [TEMANARARAUNGA]
              Te Mana Raraunga, "Māori Data Sovereignty Network Charter",
              2018. https://www.temanararaunga.maori.nz/

   [USIDSN]   US Indigenous Data Sovereignty Network,
              https://usindigenousdata.org/

   [MAIMNAYRIWINGARA]
              Maiam nayri Wingara, "Indigenous Data Sovereignty
              Communique", 2018.
              https://www.maiamnayriwingara.org/

   [RAINIE-RODRIGUEZ]
              Rainie, S.C., Schultz, J.L., Briggs, E., Riggs, P., and
              Palmanteer-Holder, N.L., "Data as a Strategic Resource:
              Self-determination, Governance, and the Data Challenge
              for Indigenous Nations in the United States", International
              Indigenous Policy Journal, 8(2), 2017.

15.5.  Civil Society

   [EFF]      Electronic Frontier Foundation, various publications,
              https://eff.org/

   [ACCESSNOW] Access Now, various publications,
              https://accessnow.org/

   [EPICORG]  Electronic Privacy Information Center,
              https://epic.org/

   [NECESS]   Necessary and Proportionate: International Principles
              on the Application of Human Rights to Communications
              Surveillance, 2014.


Appendix A.  Privacy Rights Matrix

   +-------------------------------------------------------------------+
   | Right            | GDPR | CCPA | LGPD | APPI | PIPA | PDPA-SG    |
   +-------------------------------------------------------------------+
   | Access           | Yes  | Yes  | Yes  | Yes  | Yes  | Yes        |
   | Rectification    | Yes  | Yes  | Yes  | Yes  | Yes  | Yes        |
   | Erasure          | Yes  | Yes  | Yes  | Lim  | Yes  | Yes        |
   | Portability      | Yes  | Yes  | Yes  | No   | Yes  | Yes        |
   | Object           | Yes  | Lim  | Yes  | No   | Yes  | Lim        |
   | Restrict         | Yes  | No   | Yes  | No   | Lim  | No         |
   | Not be profiled  | Yes  | Lim  | Yes  | No   | No   | Lim        |
   | Withdraw consent | Yes  | N/A  | Yes  | Yes  | Yes  | Yes        |
   +-------------------------------------------------------------------+


Appendix B.  Data Retention Schedule

   +-------------------------------------------------------------------+
   | Data Category          | Default    | Maximum  | Legal Basis     |
   +-------------------------------------------------------------------+
   | Trust Proofs           | 60 sec     | 5 min    | Function        |
   | Trust Scores (current) | Current    | Current  | Function        |
   | Trust Scores (history) | 90 days    | 1 year   | Audit           |
   | Context Tensor         | 24 hours   | 7 days   | Function        |
   | Trajectory (active)    | Lifetime   | Lifetime | Trust calc      |
   | Trajectory (archived)  | 1 year     | 7 years  | Audit           |
   | Flight Recorder        | 7 years    | 10 years | Legal/Audit     |
   | Agent identity         | Lifetime   | Life+1yr | Function        |
   | Sponsorship records    | 7 years    | 10 years | Accountability  |
   | Consent records        | 7 years    | 10 years | Proof           |
   | Access request logs    | 3 years    | 7 years  | Compliance      |
   | Breach records         | 7 years    | Indef    | Compliance      |
   +-------------------------------------------------------------------+


Appendix C.  PIA Template

   SECTION 1: PROCESSING DESCRIPTION

   1.1 What data will be processed?
   1.2 What are the purposes of processing?
   1.3 Who are the data subjects?
   1.4 What is the lawful basis?
   1.5 How long will data be retained?
   1.6 Who will have access?

   SECTION 2: NECESSITY ASSESSMENT

   2.1 Is this processing necessary for the purpose?
   2.2 What alternatives were considered?
   2.3 Why were alternatives rejected?
   2.4 Can the purpose be achieved with less data?

   SECTION 3: RISK ASSESSMENT

   3.1 What are the risks to data subjects?
   3.2 What is the likelihood of each risk?
   3.3 What is the severity of each risk?
   3.4 Risk matrix (likelihood × severity)

   SECTION 4: MITIGATION MEASURES

   4.1 Technical measures
   4.2 Organizational measures
   4.3 Residual risk after mitigation
   4.4 Is residual risk acceptable?

   SECTION 5: CONSULTATION

   5.1 DPO consultation (date, findings)
   5.2 Data subject consultation (if applicable)
   5.3 Expert consultation (if high risk)

   SECTION 6: APPROVAL

   6.1 Approver name and title
   6.2 Approval date
   6.3 Review date
   6.4 Conditions (if any)


Appendix D.  Contextual Integrity Assessment

   Based on Nissenbaum's Contextual Integrity framework.

   SECTION 1: CONTEXT IDENTIFICATION

   1.1 What is the operative social context?
       [ ] Healthcare   [ ] Employment   [ ] Financial
       [ ] Education    [ ] Commercial   [ ] Government
       [ ] Personal     [ ] Community    [ ] Research
       [ ] Other: _____________

   1.2 What are the governing norms of this context?
       (Describe entrenched informational norms)

   1.3 Are there evolving norms to consider?
       (New technologies or practices may shift norms)

   SECTION 2: INFORMATION FLOW MAPPING

   For each information flow in the system:

   2.1 Sender: Who/what transmits the information?
   2.2 Subject: Whose information is it?
   2.3 Recipient: Who/what receives the information?
   2.4 Information Type: What kind of information?
   2.5 Transmission Principle:
       [ ] Consent      [ ] Confidentiality  [ ] Reciprocity
       [ ] Notice       [ ] Entitlement      [ ] Need-to-know
       [ ] Legal requirement  [ ] Other: _____________

   SECTION 3: NORM CONFORMITY ANALYSIS

   3.1 Does this flow conform to entrenched norms?
       [ ] Yes - flow is appropriate to context
       [ ] No - flow violates contextual norms
       [ ] Uncertain - norms are unclear or evolving

   3.2 If non-conforming, what norm is violated?
       - Actor violation (wrong sender or recipient)
       - Attribute violation (wrong information type)
       - Transmission principle violation

   3.3 Justification for norm-departing flow:
       (Must provide compelling argument why departure is acceptable)

   SECTION 4: CONTEXT COLLAPSE RISK

   4.1 Could information flow across context boundaries?
       [ ] Yes  [ ] No

   4.2 What controls prevent context collapse?
       - Technical: _____________
       - Policy: _____________
       - Contractual: _____________

   4.3 Residual context collapse risk:
       [ ] High  [ ] Medium  [ ] Low

   SECTION 5: INDIGENOUS DATA CONSIDERATIONS

   5.1 Does processing involve Indigenous peoples' data?
       [ ] Yes  [ ] No  [ ] Unknown

   5.2 If yes, which Indigenous data frameworks apply?
       [ ] CARE Principles  [ ] OCAP®  [ ] Te Mana Raraunga
       [ ] UNDRIP Article 31  [ ] Other: _____________

   5.3 Has community consent been obtained through
       appropriate cultural processes?
       [ ] Yes  [ ] No  [ ] Not applicable  [ ] In progress

   5.4 Is benefit-sharing arrangement in place?
       [ ] Yes  [ ] No  [ ] Not applicable

   SECTION 6: ASSESSMENT OUTCOME

   6.1 Overall assessment:
       [ ] Flows conform to contextual norms
       [ ] Flows depart from norms with justification
       [ ] Flows violate norms - redesign required

   6.2 Required modifications:

   6.3 Assessor: _____________
   6.4 Date: _____________
   6.5 Review date: _____________


Appendix E.  Indigenous Data Sovereignty Checklist

   For deployments affecting Indigenous communities.

   PRE-ENGAGEMENT

   [ ] Identified relevant Indigenous communities
   [ ] Researched applicable Indigenous data frameworks
   [ ] Identified appropriate community representatives
   [ ] Reviewed UNDRIP and relevant national legislation
   [ ] Prepared culturally appropriate engagement approach

   CONSULTATION

   [ ] Engaged community through their governance structures
   [ ] Provided complete information in accessible format
   [ ] Allowed adequate time for community deliberation
   [ ] Respected community's right to say no
   [ ] Documented consultation process

   CONSENT

   [ ] Obtained Free, Prior and Informed Consent (FPIC)
   [ ] Consent obtained through culturally appropriate process
   [ ] Consent is specific to purpose and scope
   [ ] Community understands right to withdraw consent
   [ ] Consent documented per community preference

   DATA GOVERNANCE

   [ ] Community has authority over their data
   [ ] Data governance follows community protocols
   [ ] Community access to their data ensured
   [ ] Community can request data deletion/repatriation
   [ ] No extraction without community approval

   BENEFIT SHARING

   [ ] Benefits identified and documented
   [ ] Benefit-sharing agreement in place
   [ ] Capacity building included
   [ ] Community attribution/recognition included
   [ ] Economic benefits fairly distributed

   ONGOING RELATIONSHIP

   [ ] Regular reporting to community
   [ ] Community can raise concerns
   [ ] Process for addressing grievances
   [ ] Relationship managed for long-term
   [ ] Community involvement in research outputs

   TRADITIONAL KNOWLEDGE

   [ ] TK identified and classified
   [ ] TK access controls implemented
   [ ] No unauthorized TK disclosure
   [ ] No machine learning on TK without consent
   [ ] TK holders properly attributed


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
