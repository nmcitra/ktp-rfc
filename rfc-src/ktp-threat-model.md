---
title: "Kinetic Trust Protocol (KTP) - Threat Model Specification"
abbrev: "KTP-THREAT-MODEL"
date: 2026-08-13
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-CRYPTO:
    title: "Kinetic Trust Protocol - Cryptographic Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-ENFORCE:
    title: "Kinetic Trust Protocol - Enforcement Layer Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  RFC2119:
  RFC8174:
informative:
  STRIDE:
    title: "The STRIDE Threat Model"
    author:
      - name: Chris Perkins
  DREAD:
    title: "DREAD Risk Assessment Model"
    author:
      - name: Chris Perkins
  OWASP:
    title: "OWASP Threat Modeling"
    author:
      - name: Chris Perkins

--- abstract

This document specifies the formal threat model for the Kinetic Trust Protocol (KTP). It identifies assets, threat actors, attack vectors, and mitigations across all KTP components.

The specification uses the STRIDE methodology to analyze threats systematically and maps each threat to specific KTP mitigations documented in companion specifications.

--- middle

# Introduction

## Purpose

This threat model serves three purposes:

1. IDENTIFY risks before deployment, not after incident

1. DOCUMENT security rationale for design decisions

1. GUIDE implementers toward secure implementations

Every security system has failure modes. This document makes KTP's failure modes explicit.

## Scope

This threat model covers:

- All components defined in KTP specifications
- All communication paths between components
- All stored data and state
- All cryptographic operations

This threat model does NOT cover:

- Threats to systems protected BY KTP (that's the application's threat model)
- Physical security of data centers
- Human factors beyond insider threat
- Legal and compliance risks (see KTP-PROBLEMS)

## Methodology

This document uses:

STRIDE: Systematic threat categorization

- Spoofing (authentication)
- Tampering (integrity)
- Repudiation (non-repudiation)
- Information Disclosure (confidentiality)
- Denial of Service (availability)
- Elevation of Privilege (authorization)

ATTACK TREES: Hierarchical threat decomposition

DREAD: Risk scoring (Damage, Reproducibility, Exploitability, Affected Users, Discoverability)

Each threat includes:

- ID: Unique identifier (TM-STRIDE-NNN)
- Description: What the threat is
- Attack Vector: How attacker achieves it
- Preconditions: What must be true for attack
- Impact: Consequences if successful
- Likelihood: Probability assessment
- Mitigations: How KTP addresses it
- Residual Risk: What remains after mitigation
- References: Related KTP specifications

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

# System Overview

## Components

~~~
+-------------------------------------------------------------------+
| Component          | Function               | Trust Level         |
+-------------------------------------------------------------------+
| Trust Oracle       | Calculate Trust Scores | Highest             |
| Policy Enforcement | Enforce A ≤ E          | High                |
|   Point (PEP)      |                        |                     |
| Flight Recorder    | Immutable audit log    | High                |
| Sensor Aggregator  | Collect sensor data    | Medium              |
| Sensors            | Measure environment    | Medium              |
| Agents             | Request actions        | Variable (E_trust)  |
| Federation Gateway | Inter-zone trust       | High                |
+-------------------------------------------------------------------+
~~~

## Data Flows

Primary flows:

1. TRUST PROOF REQUEST Agent → Trust Oracle → Agent Data: Agent ID, Trust Proof Classification: Sensitive

1. AUTHORIZATION REQUEST Agent → PEP → Trust Oracle → PEP → Agent Data: Action, Trust Proof, Decision Classification: Sensitive

1. SENSOR DATA Sensors → Aggregator → Trust Oracle Data: Environmental readings Classification: Internal

1. AUDIT DATA All components → Flight Recorder Data: Decisions, context, signatures Classification: Protected

1. FEDERATION Zone A Oracle ↔ Zone B Oracle Data: Trust attestations, Zone state Classification: Sensitive

## Trust Boundaries

Trust boundaries exist at:

1. ZONE BOUNDARY Between zones (Blue Zone ↔ Cyan Zone) Control: Federation Gateway, Trust Factor

1. ORACLE BOUNDARY Between Oracle mesh and other components Control: mTLS, Threshold signatures

1. AGENT BOUNDARY Between agents and system Control: Trust Proofs, PEP enforcement

1. NETWORK BOUNDARY Between networks Control: TLS, Firewalls

Diagram:

~~~
+------------------Zone Alpha------------------+ |
| |  +--------+      +--------+      +--------+  | |  | Oracle
|<---->| Oracle |<---->| Oracle |  | |  +--------+      +--------+
+--------+  | |       ^              ^              ^        | |
|              |              |        | |  +--------+     +--------+
+--------+    | |  |  PEP   |     |Sensors |     |Flight  |    | |
+--------+     +--------+     |Recorder|    | |       ^
+--------+    | |       |                                      | |
+--------+                                  | |  | Agents |
| |  +--------+                                  | |
| +----------------------------------------------+ | | Federation v
+------------------Zone Beta-------------------+
~~~

# Assets

## Cryptographic Assets

ASSET: Oracle Signing Keys Description: Threshold key shares for Trust Proof signing Location: HSM (Level 2+) or software keystore (Level 1) Sensitivity: CRITICAL Compromise Impact: Forge any Trust Proof, undermine entire system Protection: Threshold cryptography, HSM, key ceremony

ASSET: Agent Identity Keys Description: Private keys for agent authentication Location: Agent keystore Sensitivity: HIGH Compromise Impact: Impersonate agent, inherit Trust Score Protection: Key rotation, trajectory anomaly detection

ASSET: TLS Certificates Description: X.509 certificates for transport security Location: Component keystores Sensitivity: HIGH Compromise Impact: Man-in-the-middle attacks Protection: Certificate pinning, short validity, OCSP

ASSET: Root of Trust Key Description: Master key for key hierarchy Location: Offline HSM Sensitivity: CRITICAL Compromise Impact: Sign fraudulent subordinate keys Protection: Ceremony, multi-person access, geographic distribution

## Identity Assets

ASSET: Agent Registry Description: Database of registered agents and attributes Location: Trust Oracle Sensitivity: HIGH Compromise Impact: Register rogue agents, manipulate identities Protection: Access control, audit logging, integrity checks

ASSET: Trajectory Chains Description: Cryptographic history of agent actions Location: Trust Oracle / distributed storage Sensitivity: HIGH Compromise Impact: Falsify agent history, manipulate E_base Protection: Cryptographic chaining, co-signatures

ASSET: Sponsorship Bonds Description: Records of agent sponsorship relationships Location: Trust Oracle Sensitivity: MEDIUM Compromise Impact: Create unaccountable agents Protection: Bond verification, sponsor identity proofing

## State Assets

ASSET: Trust Scores Description: Current E_base and E_trust for all agents Location: Trust Oracle (computed), cached at PEPs Sensitivity: HIGH Compromise Impact: Grant unearned trust, deny legitimate trust Protection: Computation integrity, cache validation

ASSET: Risk Factor Input State Description: Current environmental readings (the six weighted inputs and the Soul veto) Location: Trust Oracle Sensitivity: MEDIUM Compromise Impact: Manipulate Risk Factor calculation Protection: Sensor diversity, outlier detection

ASSET: Zone Configuration Description: Zone policies, thresholds, weights Location: Trust Oracle configuration Sensitivity: HIGH Compromise Impact: Weaken security policies Protection: Configuration signing, audit, access control

ASSET: Soul Constraints Description: Immutable veto conditions Location: Trust Oracle Sensitivity: CRITICAL Compromise Impact: Bypass cultural/sovereignty protections Protection: Immutability, separate authority

## Audit Assets

ASSET: Flight Recorder Log Description: Immutable record of all decisions Location: Flight Recorder storage Sensitivity: HIGH (integrity) / MEDIUM (confidentiality) Compromise Impact: Destroy evidence, enable repudiation Protection: Cryptographic chaining, external anchoring

ASSET: Key Ceremony Records Description: Documentation of key generation/rotation Location: Secure archive Sensitivity: MEDIUM Compromise Impact: Undermine key provenance claims Protection: Physical security, witnesses, recording

# Threat Actors

## External Attackers

ACTOR: Opportunistic Attacker Motivation: Financial gain, disruption Capabilities: Standard hacking tools, purchased credentials Resources: Limited budget, limited time Targets: Exposed endpoints, known vulnerabilities Risk Level: MEDIUM (common, but limited capability)

ACTOR: Organized Crime Motivation: Ransomware, data theft, fraud Capabilities: Advanced tools, zero-days, social engineering Resources: Significant budget, dedicated teams Targets: High-value data, payment systems Risk Level: HIGH (capable and motivated)

## Malicious Insiders

ACTOR: Rogue Administrator Motivation: Sabotage, theft, coercion Capabilities: Legitimate access, system knowledge Resources: Inside position, credentials Targets: Configuration, keys, data Risk Level: HIGH (access bypasses perimeter)

ACTOR: Compromised Employee Motivation: External coercion, financial Capabilities: Limited by role, but legitimate access Resources: Attacker-provided tools, guidance Targets: Credentials, sensitive data Risk Level: MEDIUM (limited scope, but inside)

Note: KTP applies Governance Recursion - administrators are agents subject to Trust Scores. This limits insider risk.

## Compromised Agents

ACTOR: Hijacked Service Account Motivation: Pivot point for lateral movement Capabilities: Inherited Trust Score, legitimate actions Resources: Compromised credentials Targets: Systems agent can access Risk Level: HIGH (legitimate-looking activity)

ACTOR: Malicious AI Agent Motivation: Misaligned objectives, adversarial input Capabilities: Autonomous action, rapid iteration Resources: Compute, API access Targets: Systems within capability tier Risk Level: HIGH (speed and autonomy)

Note: KTP's Trust Score model inherently limits compromised agent capability to their current tier.

## Nation-State Actors

ACTOR: State Intelligence Service Motivation: Espionage, sabotage, strategic advantage Capabilities: Zero-days, supply chain compromise, vast resources Resources: Effectively unlimited budget and personnel Targets: Critical infrastructure, strategic data Risk Level: CRITICAL (highest capability)

ACTOR: State-Sponsored Group Motivation: Economic espionage, political disruption Capabilities: Advanced persistent threat (APT) techniques Resources: State backing, long-term commitment Targets: Economic targets, political targets Risk Level: HIGH (persistent and capable)

Note: KTP cannot fully prevent nation-state attacks but can increase cost and reduce blast radius.

# STRIDE Analysis

## Spoofing

Definition: Pretending to be something or someone else

### TM-S-001: Agent Identity Spoofing

Description: Attacker impersonates legitimate agent

Attack Vector:

1. Steal agent's private key
2. Obtain agent's credentials through phishing
3. Exploit key generation weakness

Preconditions:

- Access to agent's private key OR
- Ability to forge signatures

Impact: HIGH

- Inherit victim's Trust Score
- Perform actions as victim
- Taint victim's trajectory

Likelihood: MEDIUM

- Key theft requires prior compromise
- Signature forgery requires crypto break

Mitigations:

- Strong key generation (KTP-CRYPTO §8.2)
- HSM storage for high-value keys (KTP-CRYPTO §9)
- Trajectory anomaly detection (KTP-IDENTITY §4.4)
- Key rotation procedures (KTP-CRYPTO §8.4)

Residual Risk: LOW

- Mitigations effective for most attackers
- Nation-state may still succeed with targeted attack

References: KTP-IDENTITY, KTP-CRYPTO

### TM-S-002: Oracle Impersonation

Description: Attacker impersonates Trust Oracle

Attack Vector:

1. Compromise threshold number of Oracle keys
2. Deploy rogue Oracle with stolen keys
3. Man-in-the-middle Oracle traffic

Preconditions:

- Compromise k-of-n Oracle key shares OR
- Ability to intercept Oracle traffic

Impact: CRITICAL

- Issue fraudulent Trust Proofs
- Manipulate any agent's effective trust
- Undermine entire zone security

Likelihood: LOW

- Requires compromising multiple HSMs
- Threshold cryptography significantly raises bar

Mitigations:

- Threshold signatures (KTP-CRYPTO §4.3)
- HSM key protection (KTP-CRYPTO §9)
- Geographic distribution (KTP-PROBLEMS §7)
- Certificate pinning for Oracle connections

Residual Risk: LOW

- Attack is expensive and detectable
- Even if successful, scope limited to zone

References: KTP-CRYPTO, KTP-PROBLEMS §5

### TM-S-003: Sensor Spoofing

Description: Attacker sends fake sensor data

Attack Vector: 1. Compromise sensor authentication 2. Inject data into sensor network 3. Replace physical sensor with malicious one

Preconditions: - Access to sensor network OR - Compromise of sensor credentials

Impact: MEDIUM - Manipulate Context Signal readings - Potentially inflate/deflate Risk Factor - Affect Trust Scores zone-wide

Likelihood: MEDIUM - Sensors are distributed, many attack surfaces - But individual sensor impact limited

Mitigations: - Sensor authentication (KTP-SENSORS §6) - Outlier detection (KTP-SENSORS §2.3) - Sensor diversity (multiple types per dimension) - Risk Domain aggregation (KTP-SENSORS §2.3)

Residual Risk: MEDIUM - Single sensor has limited impact - Coordinated attack on many sensors still possible

References: KTP-SENSORS, KTP-PROBLEMS §14

### TM-S-004: Federation Zone Spoofing

Description: Attacker impersonates federated zone

Attack Vector: 1. Register rogue zone with similar name 2. Compromise federation gateway 3. DNS hijacking of zone endpoints

Preconditions: - Ability to intercept zone discovery OR - Compromise of federation credentials

Impact: HIGH - Accept fraudulent foreign Trust Proofs - Inject malicious agents via federation - Undermine cross-zone trust

Likelihood: LOW - Federation requires explicit agreements - Zone discovery uses signed responses

Mitigations: - Signed zone discovery (KTP-FEDERATION §4) - Federation agreements with key exchange - Trust Factor limits foreign trust (KTP-FEDERATION §5) - Certificate pinning for federation

Residual Risk: LOW - Multiple layers of verification - Trust Factor limits damage if bypassed

References: KTP-FEDERATION, KTP-ZONES

## Tampering

Definition: Modifying data or code without authorization

### TM-T-001: Trust Proof Tampering

Description: Modify Trust Proof to change claims

Attack Vector: 1. Intercept Trust Proof in transit 2. Modify E_trust, tier, or other claims 3. Re-sign with forged signature

Preconditions: - Ability to intercept proofs AND - Ability to forge Oracle signatures

Impact: CRITICAL - Escalate agent privileges - Bypass Zeroth Law - Access unauthorized resources

Likelihood: VERY LOW - Requires breaking cryptographic signatures - TLS prevents transit interception

Mitigations: - Cryptographic signatures (KTP-CRYPTO §4) - TLS for all transport (KTP-TRANSPORT §5) - Short proof lifetime (seconds) - PEP signature verification

Residual Risk: VERY LOW - Would require fundamental crypto break

References: KTP-CRYPTO, KTP-TRANSPORT

### TM-T-002: Trajectory Chain Tampering

Description: Modify agent's historical trajectory

Attack Vector: 1. Gain access to trajectory storage 2. Modify historical transaction records 3. Recalculate chain hashes

Preconditions: - Write access to trajectory storage AND - Ability to forge Oracle attestations

Impact: HIGH - Inflate E_base through fake history - Hide evidence of past misbehavior - Manipulate Proof of Resilience

Likelihood: LOW - Each record requires Oracle co-signature - Hash chain detects modification

Mitigations: - Cryptographic chaining (KTP-IDENTITY §4.1) - Oracle co-signatures on transactions (KTP-IDENTITY §4.3) - External anchoring (Level 3) - Integrity verification (KTP-AUDIT)

Residual Risk: LOW - Attack detectable through chain verification - Would require sustained Oracle compromise

References: KTP-IDENTITY, KTP-AUDIT

### TM-T-003: Flight Recorder Tampering

Description: Modify or delete audit records

Attack Vector: 1. Gain administrative access to Flight Recorder 2. Modify records to hide activity 3. Delete incriminating records

Preconditions: - Administrative access to Flight Recorder OR - Compromise of Flight Recorder integrity

Impact: HIGH - Destroy forensic evidence - Enable repudiation of actions - Cover up security incidents

Likelihood: MEDIUM - Flight Recorder is high-value target - Administrators may have access

Mitigations: - Append-only storage (KTP-AUDIT §5) - Cryptographic chaining (KTP-AUDIT §4) - External anchoring (blockchain, trusted third party) - Separation of duties - Multi-site replication (Level 3)

Residual Risk: MEDIUM - Append-only can be circumvented with sufficient access - External anchoring provides strong protection

References: KTP-AUDIT

### TM-T-004: Configuration Tampering

Description: Modify zone security configuration

Attack Vector: 1. Gain admin access to Trust Oracle 2. Modify thresholds, weights, policies 3. Weaken security without detection

Preconditions: - Administrative access to configuration

Impact: HIGH - Lower security thresholds - Weaken Trust Tier boundaries - Disable Soul constraints (attempt)

Likelihood: MEDIUM - Configuration changes require admin - But admins exist and can be compromised

Mitigations: - Configuration signing (KTP-CORE §7) - Configuration audit logging - Governance Recursion (admins have Trust Scores) - Change notification and review - Soul constraints are immutable

Residual Risk: MEDIUM - Legitimate admin can make changes - Review processes may miss subtle weakening

References: KTP-CORE, KTP-HUMAN

## Repudiation

Definition: Denying having performed an action

### TM-R-001: Action Repudiation

Description: Agent denies performing action

Attack Vector: 1. Perform action 2. Claim action was performed by someone else 3. Claim system error or false attribution

Preconditions: - Inadequate audit logging OR - Ability to tamper with logs

Impact: MEDIUM - Evade accountability - Complicate incident response

- Enable fraud

Likelihood: LOW - Flight Recorder captures all decisions - Cryptographic signatures prove authorization

Mitigations: - Flight Recorder logging (KTP-AUDIT) - Agent signatures on requests - Trust Proof binding to agent - Cryptographic chain of evidence

Residual Risk: LOW - Strong non-repudiation properties - Agent signed, Oracle attested, immutably logged

References: KTP-AUDIT, KTP-IDENTITY

### TM-R-002: Oracle Decision Repudiation

Description: Oracle denies issuing Trust Proof

Attack Vector: 1. Issue Trust Proof 2. Later claim proof was forged

1. Deny responsibility for decision

Preconditions: - Inadequate proof archival OR - Ability to forge timestamps

Impact: MEDIUM - Undermine trust in Oracle - Complicate dispute resolution - Create legal uncertainty

Likelihood: VERY LOW - Threshold signatures prove Oracle consensus - Flight Recorder archives all proofs

Mitigations: - Threshold signatures (multiple Oracles must agree) - Flight Recorder archives (KTP-AUDIT) - External timestamping - Proof includes Oracle key ID

Residual Risk: VERY LOW - Cryptographic proof of Oracle involvement

References: KTP-CRYPTO, KTP-AUDIT

### TM-R-003: Sponsorship Repudiation

Description: Sponsor denies sponsoring malicious agent

Attack Vector: 1. Sponsor agent 2. Agent behaves maliciously 3. Sponsor claims bond was forged

Preconditions: - Inadequate sponsorship records

Impact: MEDIUM - Evade accountability for sponsored agents - Undermine sponsorship incentives

Likelihood: LOW - Sponsorship bonds are signed by sponsor - Witnessed by Oracle

Mitigations: - Sponsor signature on bond (KTP-IDENTITY §6.2) - Oracle witness signature - Bond stored in Flight Recorder - Identity proofing for sponsors (KTP-IDENTITY §7)

Residual Risk: LOW - Strong cryptographic evidence of sponsorship

References: KTP-IDENTITY

## Information Disclosure

Definition: Exposing information to unauthorized parties

### TM-I-001: Trust Score Disclosure

Description: Expose agent Trust Scores to unauthorized parties

Attack Vector: 1. Intercept Trust Proofs in transit 2. Query Trust Oracle without authorization 3. Infer scores from behavior patterns

Preconditions: - Access to network traffic OR - Unauthorized Oracle API access OR - Ability to observe agent behavior

Impact: LOW-MEDIUM - Privacy violation - Enable targeted attacks on low-trust agents - Competitive intelligence

Likelihood: MEDIUM - Trust Proofs travel over network - Scores visible to authorized parties

Mitigations: - TLS encryption for all transport (KTP-TRANSPORT §5) - API authentication and authorization - Score visibility controls (KTP-HUMAN §3.4) - Minimum necessary disclosure principle

Residual Risk: MEDIUM - Scores necessarily visible to some parties - Inference from behavior difficult to prevent

References: KTP-TRANSPORT, KTP-HUMAN

### TM-I-002: Trajectory Disclosure

Description: Expose agent's behavioral history

Attack Vector: 1. Gain unauthorized access to trajectory storage 2. Query trajectory through Oracle API 3. Correlation of logged events

Preconditions: - Access to trajectory data OR - Unauthorized Oracle queries

Impact: MEDIUM - Privacy violation - Behavioral analysis - Pattern exploitation

Likelihood: MEDIUM - Trajectories stored for Trust calculation - May be queried for audit/compliance

Mitigations: - Access controls on trajectory data - Trajectory aggregation (reveal summary, not detail) - Retention limits - Audit logging of trajectory access

Residual Risk: MEDIUM - Some trajectory access necessary for system operation - Aggregation limits exposure

References: KTP-IDENTITY, KTP-AUDIT

### TM-I-003: Sensor Data Disclosure

Description: Expose raw sensor readings

Attack Vector: 1. Intercept sensor-to-aggregator traffic 2. Compromise aggregator 3. Side-channel inference

Preconditions: - Access to sensor network OR - Aggregator compromise

Impact: LOW-MEDIUM - Reveal infrastructure state - Enable timing attacks - Competitive intelligence

Likelihood: MEDIUM - Sensor data in transit - Aggregator stores readings

Mitigations: - TLS for sensor transport - Aggregation and summarization - Limited retention of raw readings - Sensor data access controls

Residual Risk: LOW - Sensor data is environmental, not personal - Aggregation limits utility of disclosure

References: KTP-SENSORS, KTP-TRANSPORT

### TM-I-004: Cryptographic Key Disclosure

Description: Expose private keys

Attack Vector: 1. Memory disclosure vulnerability 2. Backup/export of keys 3. Side-channel attack on HSM

Preconditions: - Memory access OR - Key export capability OR - Physical/electrical access to HSM

Impact: CRITICAL - Complete identity compromise - Forge signatures - Impersonate any entity

Likelihood: LOW - HSMs prevent extraction (Level 2+) - Memory protection techniques

Mitigations: - HSM storage (KTP-CRYPTO §9) - Non-extractable keys - Memory protection (mlock, secure wipe) - Side-channel resistant implementations

Residual Risk: LOW - HSMs provide strong protection - Nation-state may have exotic attacks

References: KTP-CRYPTO

## Denial of Service

Definition: Making system unavailable to legitimate users

### TM-D-001: Trust Oracle DoS

Description: Make Trust Oracle unavailable

Attack Vector: 1. Flood Oracle with requests 2. Exploit resource exhaustion bug 3. Network-level DDoS

Preconditions: - Ability to send traffic to Oracle

Impact: HIGH - Agents cannot get Trust Proofs - System enters fail- safe mode - Operations disrupted

Likelihood: MEDIUM - Oracle is central service - DDoS attacks are common

Mitigations: - Rate limiting (KTP-TRANSPORT §14) - Oracle mesh distribution - DDoS protection infrastructure - Cached Trust Proofs (short-term operation) - Fail-safe mode (deny uncertain actions)

Residual Risk: MEDIUM - Sophisticated DDoS can overwhelm defenses - But fail-safe maintains security

References: KTP-TRANSPORT, KTP-ENFORCE

### TM-D-002: Sensor Flooding

Description: Overwhelm sensors or aggregators

Attack Vector: 1. Generate massive fake sensor data 2. Exploit aggregator processing limits 3. Network saturation

Preconditions: - Access to sensor network

Impact: MEDIUM - Context Signals become unreliable - Trust Scores potentially incorrect - Possible cascading effects

Likelihood: MEDIUM - Sensors distributed, large attack surface

Mitigations: - Sensor authentication (KTP-SENSORS §6) - Rate limiting per sensor - Aggregator capacity planning - Graceful degradation (use last known good) - Fail-safe to conservative Trust Scores

Residual Risk: MEDIUM - Coordinated attack can still impact - Fail- safe limits security impact

References: KTP-SENSORS, KTP-PROBLEMS §14

### TM-D-003: Flight Recorder DoS

Description: Prevent audit logging

Attack Vector: 1. Fill storage with garbage 2. Overwhelm write capacity 3. Network partition Flight Recorder

Preconditions: - Ability to generate audit events OR - Network access to Flight Recorder

Impact: MEDIUM-HIGH - Audit gap enables untracked activity - Compliance violation - Forensic blind spot

Likelihood: MEDIUM - Flight Recorder must accept high volume

Mitigations: - Write rate limiting - Storage capacity monitoring - Buffering at source (temporary local storage) - Multiple Flight Recorder instances - Audit of audit failures

Residual Risk: MEDIUM - Temporary gaps possible under attack - Buffering provides some resilience

References: KTP-AUDIT

### TM-D-004: Federation DoS

Description: Disrupt inter-zone communication

Attack Vector: 1. Flood federation gateway 2. Exploit federation protocol 3. Man-in-the-middle dropping packets

Preconditions: - Access to federation network

Impact: MEDIUM - Cross-zone trust breaks down - Agents cannot operate across zones - Federation heartbeat failure

Likelihood: LOW-MEDIUM - Federation traffic is lower volume - But critical for multi-zone deployments

Mitigations: - Rate limiting on federation gateway - Multiple federation paths - Grace periods for heartbeat failure - Fall back to independent zone operation

Residual Risk: LOW - Zones can operate independently - Cross-zone actions fail safe

References: KTP-FEDERATION

## Elevation of Privilege

Definition: Gaining capabilities beyond those authorized

### TM-E-001: Trust Score Manipulation

Description: Artificially increase Trust Score

Attack Vector: 1. Poison baseline over time (boiling frog) 2. Compromise sensors to report false low risk 3. Generate fake Proof of Resilience

Preconditions: - Ability to influence sensors OR - Long-term access for baseline manipulation

Impact: HIGH - Gain unearned capabilities - Access unauthorized resources - Perform unauthorized actions

Likelihood: MEDIUM - Multiple attack paths exist - Some require sustained effort

Mitigations: - Baseline drift detection (KTP-PROBLEMS §6) - External anchor baselines - Sensor diversity and outlier detection - Oracle co-signature on attestations - Resilience score quality over quantity

Residual Risk: MEDIUM - Sophisticated, patient attacker may succeed - Detection mechanisms provide defense in depth

References: KTP-PROBLEMS §4, KTP-SENSORS

### TM-E-002: Tier Boundary Bypass

Description: Perform actions above current tier

Attack Vector: 1. Exploit PEP implementation flaw 2. Race condition during tier transition 3. Forge Trust Proof with higher tier

Preconditions: - PEP vulnerability OR - Timing window during transition OR - Signature forgery capability

Impact: HIGH - Exceed authorized capabilities - Perform privileged operations

Likelihood: LOW - Tier enforcement is straightforward check - Signature forgery is difficult

Mitigations: - Simple tier check implementation - Proof validation before check - Hysteresis prevents rapid tier changes - PEP implementation testing

Residual Risk: LOW - Attack surface is limited - Mitigations are effective

References: KTP-ENFORCE

### TM-E-003: Administrator Privilege Abuse

Description: Administrator exceeds authorized actions

Attack Vector: 1. Use admin access for unauthorized changes 2. Exempt self from Trust Score constraints 3. Grant excessive permissions

Preconditions: - Administrative access

Impact: HIGH - Undermine security model - Create backdoors - Compromise integrity

Likelihood: MEDIUM - Administrators exist - Traditional systems allow admin override

Mitigations: - Governance Recursion (KTP-HUMAN §5.4) - Administrators have Trust Scores - Admin actions logged to Flight Recorder - No override mechanism exists - Multi-person admin (Level 3)

Residual Risk: MEDIUM - KTP explicitly addresses this - But determined malicious admin has options

References: KTP-HUMAN, Constitution Article VII

### TM-E-004: Soul Constraint Bypass

Description: Bypass immutable Soul veto

Attack Vector: 1. Disable Soul veto processing 2. Modify Soul constraint configuration 3. Exploit Soul check implementation

Preconditions: - Ability to modify Oracle code OR - Configuration access to Soul constraints

Impact: CRITICAL - Violate sovereignty constraints - Access protected cultural data - Override non-negotiable restrictions

Likelihood: VERY LOW - Soul constraints are architecturally separate

- Checked before Trust Score calculation

Mitigations: - Soul checked before other calculations - Immutable constraint storage - Separate authority for Soul configuration - Flight Recorder logs Soul vetoes (7-year retention)

Residual Risk: LOW - Architecture provides strong protection - Attack requires fundamental system compromise

References: KTP-CORE §6, Constitution Article X

# Component-Specific Threats

## Trust Oracle Threats

The Trust Oracle is the highest-value target.

TM-TO-001: Oracle Key Extraction Threat: Extract signing key shares from Oracle Attack: HSM side-channel, memory dump, insider theft Impact: CRITICAL - forge Trust Proofs Mitigation: HSM (Level 2+), threshold crypto, ceremony Risk: LOW (Level 2+), MEDIUM (Level 1)

TM-TO-002: Oracle Consensus Manipulation Threat: Manipulate threshold signing consensus Attack: Compromise k-of-n Oracles, Byzantine behavior Impact: HIGH - issue fraudulent proofs Mitigation: Geographic distribution, threshold selection Risk: LOW

TM-TO-003: Oracle Configuration Attack Threat: Modify Oracle security parameters Attack: Admin compromise, config injection Impact: HIGH - weaken security zone-wide Mitigation: Config signing, audit, admin Trust Scores Risk: MEDIUM

TM-TO-004: Oracle State Corruption Threat: Corrupt in-memory Trust Score state Attack: Memory corruption exploit, race condition Impact: HIGH - incorrect Trust Scores Mitigation: Memory safety, state validation, consensus Risk: LOW

TM-TO-005: Oracle Time Manipulation Threat: Manipulate Oracle's time source Attack: NTP attack, GPS spoofing Impact: MEDIUM - timestamp manipulation Mitigation: Multiple time sources, Roughtime Risk: MEDIUM

~~~
Summary:
+-------------------------------------------------------------------+
| Threat       | Impact   | Likelihood | Risk     | Mitigation      |
+-------------------------------------------------------------------+
| TM-TO-001    | CRITICAL | LOW        | MEDIUM   | HSM, threshold  |
| TM-TO-002    | HIGH     | LOW        | LOW      | Distribution    |
| TM-TO-003    | HIGH     | MEDIUM     | MEDIUM   | Signing, audit  |
| TM-TO-004    | HIGH     | LOW        | LOW      | Validation      |
| TM-TO-005    | MEDIUM   | MEDIUM     | MEDIUM   | Multiple sources|
+-------------------------------------------------------------------+
~~~

## PEP Threats

TM-PEP-001: PEP Bypass Threat: Route traffic around PEP Attack: Network reconfiguration, direct access Impact: HIGH - enforcement bypassed Mitigation: Network segmentation, multiple PEPs Risk: MEDIUM

TM-PEP-002: PEP Compromise Threat: Compromise PEP to allow all traffic Attack: Exploit PEP vulnerability, config change Impact: HIGH

- zone-wide enforcement failure Mitigation: Defense in depth, PEP monitoring Risk: MEDIUM

TM-PEP-003: Stale Cache Exploitation Threat: Use cached Trust Proof after revocation Attack: Continue using revoked proof during cache window Impact: MEDIUM - temporary unauthorized access Mitigation: Short cache TTL, push invalidation Risk: MEDIUM

TM-PEP-004: PEP Decision Override Threat: Override PEP decision externally Attack: Admin interface abuse Impact: HIGH - bypass Zeroth Law Mitigation: No override mechanism, audit Risk: LOW (by design)

~~~
Summary:
+-------------------------------------------------------------------+
| Threat       | Impact   | Likelihood | Risk     | Mitigation      |
+-------------------------------------------------------------------+
| TM-PEP-001   | HIGH     | MEDIUM     | MEDIUM   | Segmentation    |
| TM-PEP-002   | HIGH     | MEDIUM     | MEDIUM   | Defense in depth|
| TM-PEP-003   | MEDIUM   | MEDIUM     | MEDIUM   | Short TTL, push |
| TM-PEP-004   | HIGH     | LOW        | LOW      | No override     |
+-------------------------------------------------------------------+
~~~

## Sensor Threats

TM-SEN-001: Sensor Spoofing Threat: Inject false sensor readings Attack: Fake sensor, compromised sensor Impact: MEDIUM - manipulate Risk Factor Mitigation: Authentication, diversity, outliers Risk: MEDIUM

TM-SEN-002: Sensor Flooding Threat: Overwhelm sensor aggregation Attack: High-volume fake readings Impact: MEDIUM - DoS on sensor system Mitigation: Rate limiting, authentication Risk: MEDIUM

TM-SEN-003: Baseline Poisoning Threat: Gradually shift baseline to mask attack Attack: Slow, sustained false readings Impact: HIGH - undetected attack preparation Mitigation: Drift detection, external anchors Risk: MEDIUM

TM-SEN-004: Sensor Denial Threat: Disable sensors to blind system Attack: Network partition, physical destruction Impact: MEDIUM - reduced visibility Mitigation: Redundancy, fail-safe conservative Risk: MEDIUM

~~~
Summary:
+-------------------------------------------------------------------+
| Threat       | Impact   | Likelihood | Risk     | Mitigation      |
+-------------------------------------------------------------------+
| TM-SEN-001   | MEDIUM   | MEDIUM     | MEDIUM   | Auth, diversity |
| TM-SEN-002   | MEDIUM   | MEDIUM     | MEDIUM   | Rate limiting   |
| TM-SEN-003   | HIGH     | MEDIUM     | MEDIUM   | Drift detection |
| TM-SEN-004   | MEDIUM   | MEDIUM     | MEDIUM   | Redundancy      |
+-------------------------------------------------------------------+
~~~

## Flight Recorder Threats

TM-FR-001: Record Deletion Threat: Delete audit records Attack: Admin access, storage compromise Impact: HIGH - destroy evidence Mitigation: Append-only, external anchoring Risk: MEDIUM

TM-FR-002: Record Modification Threat: Alter historical records Attack: Storage compromise, admin abuse Impact: HIGH - falsify audit trail Mitigation: Cryptographic chaining, anchoring Risk: LOW

TM-FR-003: Record Disclosure Threat: Unauthorized access to audit data Attack: Storage breach, API abuse Impact: MEDIUM - privacy, competitive Mitigation: Access control, encryption at rest Risk: MEDIUM

TM-FR-004: Chain Gap Threat: Create gap in audit chain Attack: DoS during critical period Impact: MEDIUM - audit blind spot Mitigation: Buffering, gap detection, alerts Risk: MEDIUM

~~~
Summary:
+-------------------------------------------------------------------+
| Threat       | Impact   | Likelihood | Risk     | Mitigation      |
+-------------------------------------------------------------------+
| TM-FR-001    | HIGH     | MEDIUM     | MEDIUM   | Append-only     |
| TM-FR-002    | HIGH     | LOW        | LOW      | Chaining        |
| TM-FR-003    | MEDIUM   | MEDIUM     | MEDIUM   | Access control  |
| TM-FR-004    | MEDIUM   | MEDIUM     | MEDIUM   | Buffering       |
+-------------------------------------------------------------------+
~~~

## Federation Threats

TM-FED-001: Rogue Zone Threat: Federate with malicious zone Attack: Social engineering, compromised agreement Impact: HIGH - trust malicious proofs Mitigation: Agreement verification, Trust Factor Risk: LOW

TM-FED-002: Trust Factor Manipulation Threat: Artificially inflate foreign zone trust Attack: Config change, collusion Impact: MEDIUM - excessive foreign trust Mitigation: Trust Factor limits, audit Risk: MEDIUM

TM-FED-003: Federation Partition Threat: Isolate zones from each other Attack: Network attack, DNS hijacking Impact: MEDIUM - federation disruption Mitigation: Multiple paths, independent operation Risk: MEDIUM

TM-FED-004: Cross-Zone Attack Escalation Threat: Use federation to attack multiple zones Attack: Compromise one zone, propagate via federation Impact: HIGH - multi-zone compromise Mitigation: Trust Factor limits blast radius Risk: LOW

~~~
Summary:
+-------------------------------------------------------------------+
| Threat       | Impact   | Likelihood | Risk     | Mitigation      |
+-------------------------------------------------------------------+
| TM-FED-001   | HIGH     | LOW        | LOW      | Verification    |
| TM-FED-002   | MEDIUM   | MEDIUM     | MEDIUM   | Limits, audit   |
| TM-FED-003   | MEDIUM   | MEDIUM     | MEDIUM   | Redundancy      |
| TM-FED-004   | HIGH     | LOW        | LOW      | Trust Factor    |
+-------------------------------------------------------------------+
~~~

# Attack Trees

## Bypass Zeroth Law

Goal: Perform action A where A > E_trust

OR ├── \[1] Increase E_trust │   OR │   ├── \[1.1] Manipulate E_base │ │   OR │   │   ├── \[1.1.1] Falsify trajectory history │   │   │   AND │   │   │   ├── Compromise Oracle co-signature │   │   │   └── Modify trajectory storage │   │   │   Difficulty: HIGH │   │   │ │   │   ├── \[1.1.2] Generate fake Proof of Resilience │   │   │   AND │   │   │ ├── Create artificial stress conditions │   │   │   └── Get Oracle attestation under false pretense │   │   │   Difficulty: MEDIUM │   │ │ │   │   └── \[1.1.3] Steal high-E_base agent identity │   │ AND │   │       ├── Obtain agent private key │   │       └── Evade trajectory anomaly detection │   │       Difficulty: MEDIUM │   │ │ └── \[1.2] Manipulate Risk Factor │       OR │       ├── \[1.2.1] Compromise sensors to report low risk │       │   Difficulty: MEDIUM (need multiple sensors) │       │ │       └── \[1.2.2] Poison baseline over time │           Difficulty: MEDIUM-HIGH (needs patience) │ ├── \[2] Decrease A (action risk) │   OR │   ├── \[2.1] Modify risk classification │   │   AND │   │   ├── Gain config access │   │   └── Change action risk score │   │   Difficulty: MEDIUM (detectable) │ │ │   └── \[2.2] Misrepresent action │       AND │       ├── Call different API than intended action │       └── Achieve same effect │ Difficulty: LOW-MEDIUM (depends on API design) │ ├── \[3] Bypass PEP │ OR │   ├── \[3.1] Route around PEP │   │   Difficulty: MEDIUM (network dependent) │   │ │   ├── \[3.2] Compromise PEP │   │   Difficulty: MEDIUM-HIGH │   │ │   └── \[3.3] Exploit PEP vulnerability │ Difficulty: MEDIUM (if vulnerability exists) │ └── \[4] Forge Trust Proof (See Attack Tree 7.2) Difficulty: HIGH

Minimum Difficulty Path: \[2.2] or \[3.1] Mitigation Focus: API design, network segmentation

## Forge Trust Proof

Goal: Create valid Trust Proof without Oracle authorization

OR ├── \[1] Obtain Oracle signing capability │   OR │   ├── \[1.1] Compromise k-of-n Oracle key shares │   │   AND │   │   ├── Identify HSM locations │   │   ├── Compromise k HSMs │   │   └── Extract key shares │   │   Difficulty: VERY HIGH (Level 2+) │   │ │   ├── \[1.2] Exploit threshold signing protocol │   │   Difficulty: VERY HIGH (requires crypto break) │   │ │   └── \[1.3] Insider collusion (k administrators) │       AND │       ├── Recruit k insiders with key access │       └── Coordinate signing │       Difficulty: HIGH (needs k colluders) │ ├── \[2] Replay valid Trust Proof │   AND │   ├── Capture valid proof │   └── Use before expiration │   Difficulty: LOW (but short window) │   Impact: LIMITED (only for captured agent) │ └── \[3] Exploit signature verification flaw AND ├── Find verification vulnerability └── Craft proof that passes broken check Difficulty: HIGH (requires implementation flaw)

Minimum Difficulty Path: \[2] Replay (but limited impact) Most Concerning Path: \[1.3] Insider collusion Mitigation Focus: Short proof lifetime, insider controls

## Corrupt Trust Score

Goal: Cause Oracle to calculate incorrect Trust Score

OR ├── \[1] Corrupt E_base calculation │   (See Attack Tree 7.1, node 1.1) │ ├── \[2] Corrupt Risk Factor calculation │   OR │   ├── \[2.1] Feed false sensor data │   │   OR │   │   ├── \[2.1.1] Spoof sensors (instant) │   │   │   Difficulty: MEDIUM (need critical mass) │   │ │ │   │   └── \[2.1.2] Poison baseline (slow) │   │       Difficulty: MEDIUM (needs time) │   │ │   ├── \[2.2] Compromise aggregator │   │ Difficulty: MEDIUM-HIGH │   │ │   └── \[2.3] Manipulate dimension weights │       AND │       ├── Gain config access │       └── Modify weights │       Difficulty: MEDIUM │ └── \[3] Corrupt calculation itself OR ├── \[3.1] Exploit calculation bug │   Difficulty: HIGH (requires finding bug) │ └── \[3.2] Memory corruption attack Difficulty: HIGH (memory safety)

Minimum Difficulty Path: \[2.1.1] or \[2.1.2] Mitigation Focus: Sensor security, baseline protection

## Evade Audit

Goal: Perform action without Flight Recorder evidence

OR ├── \[1] Prevent record creation │   OR │   ├── \[1.1] DoS Flight Recorder during action │   │   Difficulty: MEDIUM (local buffering helps) │   │ │   ├── \[1.2] Exploit logging gap │   │   Difficulty: MEDIUM (depends on implementation) │   │ │   └── \[1.3] Disable logging component │       Difficulty: HIGH (monitored) │ ├── \[2] Delete records after creation │   OR │   ├── \[2.1] Admin access to storage │   │   Difficulty: MEDIUM-HIGH (append-only) │   │ │   └── \[2.2] Compromise external anchor │       Difficulty: VERY HIGH (blockchain/third party) │ ├── \[3] Modify records after creation │ AND │   ├── Gain write access │   └── Recompute chain hashes │ Difficulty: HIGH (need Oracle keys) │ └── \[4] Create plausible deniability AND ├── Create cover story └── Exploit ambiguity in records Difficulty: MEDIUM (but records are detailed)

Minimum Difficulty Path: \[1.1] or \[4] Mitigation Focus: Buffering, record completeness

# Risk Assessment

## Risk Matrix

Impact scale: - CRITICAL: System-wide compromise, data breach - HIGH: Zone-wide impact, significant breach - MEDIUM: Limited impact, partial compromise - LOW: Minimal impact, quickly recoverable

Likelihood scale: - HIGH: Likely to occur annually - MEDIUM: May occur over system lifetime - LOW: Unlikely but possible - VERY LOW: Requires exceptional circumstances

Risk = Impact × Likelihood

~~~
+-------------------------------------------------------------------+
|                    |        Impact                                |
| Likelihood         | CRITICAL | HIGH   | MEDIUM | LOW            |
+-------------------------------------------------------------------+
| HIGH               | CRITICAL | HIGH   | MEDIUM | LOW            |
| MEDIUM             | HIGH     | MEDIUM | MEDIUM | LOW            |
| LOW                | MEDIUM   | MEDIUM | LOW    | LOW            |
| VERY LOW           | MEDIUM   | LOW    | LOW    | VERY LOW       |
+-------------------------------------------------------------------+
~~~

Top risks by residual risk (after mitigation):

~~~
+-------------------------------------------------------------------+
| Threat             | Impact   | Likelihood | Residual Risk        |
+-------------------------------------------------------------------+
| TM-E-001 Score     | HIGH     | MEDIUM     | MEDIUM               |
|   manipulation     |          |            |                      |
| TM-SEN-003 Baseline| HIGH     | MEDIUM     | MEDIUM               |
|   poisoning        |          |            |                      |
| TM-TO-003 Config   | HIGH     | MEDIUM     | MEDIUM               |
|   attack           |          |            |                      |
| TM-E-003 Admin     | HIGH     | MEDIUM     | MEDIUM               |
|   abuse            |          |            |                      |
| TM-PEP-001 Bypass  | HIGH     | MEDIUM     | MEDIUM               |
| TM-D-001 Oracle DoS| HIGH     | MEDIUM     | MEDIUM               |
+-------------------------------------------------------------------+
~~~

## Residual Risks

Risks that remain after all mitigations:

### Nation-State Attacks

Description: Well-resourced state actor with advanced capabilities

Residual because: - Effectively unlimited resources - Zero-day capabilities - Supply chain access - Insider recruitment

Acceptance: KTP increases attack cost significantly. Perfect defense against nation-states is not achievable. Focus on detection and limiting blast radius.

### Insider with Physical Access

Description: Malicious insider with physical access to HSMs

Residual because: - Physical access bypasses many controls - HSM side-channels exist - Multi-person controls help but don't eliminate

Acceptance: Multi-person access, geographic distribution, and audit provide defense in depth. Some residual risk accepted.

### Novel Cryptographic Attacks

Description: Future attack on current cryptographic algorithms

Residual because: - Cryptography may be broken in future - Quantum computers may emerge faster than expected

Acceptance: Cryptographic agility allows transition. Hybrid signatures provide hedge. Monitor cryptographic developments.

### Coordinated Multi-Vector Attack

Description: Simultaneous attack on multiple components

Residual because: - Mitigations assume sequential attacks - Coordinated attack may overwhelm response

Acceptance: Defense in depth limits damage. Each component fails independently. Monitoring enables detection.

### Long-Term Baseline Manipulation

Description: Patient attacker slowly poisons baselines

Residual because: - Drift detection has limits - Very slow changes may evade detection

Acceptance: External anchors, cross-zone correlation, and periodic rebaselining from known-good states limit exposure.

# Security Requirements

Based on threat analysis, implementations MUST meet these security requirements:

SR-001: Cryptographic Signatures All Trust Proofs MUST be cryptographically signed per KTP-CRYPTO. Rationale: Prevents forgery (TM-T-001)

SR-002: Threshold Signing Level 2+ MUST use threshold signatures for Trust Proofs. Rationale: Prevents single-point compromise (TM-S-002)

SR-003: Transport Security All communication MUST use TLS 1.3. Rationale: Prevents interception (TM-I-*)

SR-004: Sensor Authentication All sensors MUST authenticate to aggregators. Rationale: Prevents spoofing (TM-SEN-001)

SR-005: Sensor Diversity Each Risk Factor input SHOULD have multiple sensor types. Rationale: Limits single-sensor compromise impact

SR-006: Outlier Detection Sensor aggregation MUST implement outlier detection. Rationale: Detects sensor spoofing

SR-007: Baseline Drift Detection Implementations MUST detect baseline drift. Rationale: Prevents baseline poisoning (TM-SEN-003)

SR-008: Flight Recorder Integrity Flight Recorder MUST use cryptographic chaining. Rationale: Prevents tampering (TM-FR-002)

SR-009: Append-Only Audit Flight Recorder MUST be append-only. Rationale: Prevents deletion (TM-FR-001)

SR-010: No Override Mechanism Implementations MUST NOT include override for Zeroth Law. Rationale: Prevents privilege escalation (TM-E-003)

SR-011: Administrator Trust Scores Administrators MUST have Trust Scores and be subject to A ≤ E. Rationale: Limits insider abuse (TM-E-003)

SR-012: Short Proof Lifetime Trust Proofs MUST expire within 60 seconds. Rationale: Limits replay window (TM-S-001)

SR-013: Rate Limiting All endpoints MUST implement rate limiting. Rationale: Limits DoS impact (TM-D-*)

SR-014: Fail-Safe Mode Loss of Oracle MUST result in fail-safe (deny uncertain). Rationale: Security not degraded by availability attack

SR-015: Soul Immutability Soul constraints MUST NOT be modifiable through normal config. Rationale: Prevents sovereignty bypass (TM-E-004)

# Assumptions and Dependencies

This threat model assumes:

## Cryptographic Assumptions

- ECDSA/EdDSA signatures cannot be forged without private key - Hash functions are collision-resistant - TLS 1.3 provides confidentiality and integrity - HSMs protect keys from extraction

If violated: Fundamental security properties fail

## Operational Assumptions

- HSMs are operated according to vendor guidelines - Key ceremonies are conducted correctly - Administrators follow security procedures
- Monitoring is reviewed and actioned

If violated: Mitigations may not be effective

## Infrastructure Assumptions

- Network segmentation is correctly implemented - Time sources are reasonably accurate - Hardware is not compromised at manufacture - Physical security of data centers is adequate

If violated: Multiple threats become more likely

## Dependencies

External dependencies that affect security:

- HSM vendor security - TLS library security - Operating system security - Cloud provider security (if applicable) - PKI infrastructure - Time synchronization infrastructure

Each dependency is a potential attack surface.

--- back

# Threat Catalog

Complete listing of all identified threats:

~~~
Spoofing Threats:
+-------------------------------------------------------------------+
| ID        | Name                    | Risk   | Reference          |
+-------------------------------------------------------------------+
| TM-S-001  | Agent Identity Spoofing | LOW    | §5.1.1             |
| TM-S-002  | Oracle Impersonation    | LOW    | §5.1.2             |
| TM-S-003  | Sensor Spoofing         | MEDIUM | §5.1.3             |
| TM-S-004  | Federation Zone Spoofing| LOW    | §5.1.4             |
+-------------------------------------------------------------------+
~~~

~~~
Tampering Threats:
+-------------------------------------------------------------------+
| ID        | Name                    | Risk   | Reference          |
+-------------------------------------------------------------------+
| TM-T-001  | Trust Proof Tampering   | V.LOW  | §5.2.1             |
| TM-T-002  | Trajectory Tampering    | LOW    | §5.2.2             |
| TM-T-003  | Flight Recorder Tamper  | MEDIUM | §5.2.3             |
| TM-T-004  | Configuration Tampering | MEDIUM | §5.2.4             |
+-------------------------------------------------------------------+
~~~

~~~
Repudiation Threats:
+-------------------------------------------------------------------+
| ID        | Name                    | Risk   | Reference          |
+-------------------------------------------------------------------+
| TM-R-001  | Action Repudiation      | LOW    | §5.3.1             |
| TM-R-002  | Oracle Decision Repud.  | V.LOW  | §5.3.2             |
| TM-R-003  | Sponsorship Repudiation | LOW    | §5.3.3             |
+-------------------------------------------------------------------+
~~~

~~~
Information Disclosure Threats:
+-------------------------------------------------------------------+
| ID        | Name                    | Risk   | Reference          |
+-------------------------------------------------------------------+
| TM-I-001  | Trust Score Disclosure  | MEDIUM | §5.4.1             |
| TM-I-002  | Trajectory Disclosure   | MEDIUM | §5.4.2             |
| TM-I-003  | Sensor Data Disclosure  | LOW    | §5.4.3             |
| TM-I-004  | Key Disclosure          | LOW    | §5.4.4             |
+-------------------------------------------------------------------+
~~~

~~~
Denial of Service Threats:
+-------------------------------------------------------------------+
| ID        | Name                    | Risk   | Reference          |
+-------------------------------------------------------------------+
| TM-D-001  | Trust Oracle DoS        | MEDIUM | §5.5.1             |
| TM-D-002  | Sensor Flooding         | MEDIUM | §5.5.2             |
| TM-D-003  | Flight Recorder DoS     | MEDIUM | §5.5.3             |
| TM-D-004  | Federation DoS          | LOW    | §5.5.4             |
+-------------------------------------------------------------------+
~~~

~~~
Elevation of Privilege Threats:
+-------------------------------------------------------------------+
| ID        | Name                    | Risk   | Reference          |
+-------------------------------------------------------------------+
| TM-E-001  | Trust Score Manipulation| MEDIUM | §5.6.1             |
| TM-E-002  | Tier Boundary Bypass    | LOW    | §5.6.2             |
| TM-E-003  | Admin Privilege Abuse   | MEDIUM | §5.6.3             |
| TM-E-004  | Soul Constraint Bypass  | LOW    | §5.6.4             |
+-------------------------------------------------------------------+
~~~

# Mitigation Mapping

Mapping of mitigations to KTP specifications:

~~~
+-------------------------------------------------------------------+
| Mitigation              | Specification     | Section            |
+-------------------------------------------------------------------+
| Threshold signatures    | KTP-CRYPTO        | §4.3               |
| HSM key storage         | KTP-CRYPTO        | §9                 |
| Key rotation            | KTP-CRYPTO        | §8.4               |
| TLS transport           | KTP-TRANSPORT     | §5                 |
| Rate limiting           | KTP-TRANSPORT     | §14                |
| Sensor authentication   | KTP-SENSORS       | §6                 |
| Outlier detection       | KTP-SENSORS       | §2.3               |
| Risk domain aggregation | KTP-SENSORS       | §2.3               |
| Baseline drift detection| KTP-PROBLEMS      | §6                 |
| Trajectory chaining     | KTP-IDENTITY      | §4                 |
| Oracle co-signatures    | KTP-IDENTITY      | §4.3               |
| Identity proofing       | KTP-IDENTITY      | §7                 |
| Flight Recorder chain   | KTP-AUDIT         | §4                 |
| Append-only storage     | KTP-AUDIT         | §5                 |
| External anchoring      | KTP-AUDIT         | §6                 |
| PEP enforcement         | KTP-ENFORCE       | §4                 |
| Trust tiers             | KTP-ENFORCE       | §5                 |
| No override mechanism   | KTP-ENFORCE       | §7                 |
| Governance recursion    | KTP-HUMAN         | §5.4               |
| Admin Trust Scores      | KTP-HUMAN         | §3                 |
| Federation Trust Factor | KTP-FEDERATION    | §5                 |
| Zone discovery signing  | KTP-FEDERATION    | §4                 |
+-------------------------------------------------------------------+
~~~
