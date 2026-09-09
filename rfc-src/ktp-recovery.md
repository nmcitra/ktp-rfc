---
title: "Kinetic Trust Protocol (KTP) - Recovery Specification"
abbrev: "KTP-RECOVERY"
date: 2026-09-06
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

This document specifies disaster recovery, backup, restoration, and failure handling procedures for Kinetic Trust Protocol (KTP) deployments. It addresses Oracle mesh failures, zone recovery, federation partition handling, and data restoration procedures.

Security systems must be resilient. This specification ensures KTP deployments can recover from failures without compromising security properties.

--- middle

# Introduction

"Everything fails, all the time." - Werner Vogels

KTP systems protect critical operations. When components fail, the system must either continue operating safely or recover quickly. This specification defines how.

Recovery objectives:

1. SECURITY PRESERVATION Recovery must not compromise security properties. "Fail secure" takes precedence over "fail available."

1. DATA INTEGRITY Recovered state must be consistent and verifiable. No silent data corruption or loss.

1. MINIMAL DISRUPTION Recovery should be as fast as possible while meeting objectives 1 and 2.

1. AUDITABILITY All recovery actions must be logged and attributable.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

# Recovery Principles

PRINCIPLE 1: FAIL CLOSED An undefined input MUST NOT resolve toward permission. It resolves toward the more restrictive outcome available at that decision point (\[KTP-CORE] Section 6.7). Where recovery offers a graded outcome, that is the more supervised level, not a denial; deny where nothing more restrictive short of denial exists. A system that fails open is worse than a system that fails closed. Availability loss is recoverable; security breach may not be.

PRINCIPLE 2: NO SINGLE POINT OF FAILURE Every critical component should have redundancy. Threshold cryptography for Oracles. Multiple Flight Recorders. Distributed sensors.

PRINCIPLE 3: DEFENSE IN DEPTH FOR RECOVERY Backup your backups. Verify your verifications. Test your tests. Recovery procedures themselves can fail.

PRINCIPLE 4: SECURITY DURING RECOVERY Recovery mode is an attractive attack window. Maintain authentication, authorization, and audit during recovery.

PRINCIPLE 5: KNOWN-GOOD STATE Recovery should restore to a known-good state, not just "last state." Compromised state should not be restored.

Consensus recovery MUST additionally preserve previously cast votes, locks, committed history, and authenticated membership under `specifications/oracle-consensus.md`. The backup recovery-point objectives below do not permit loss or rollback of that safety state followed by renewed voting. An older known-good snapshot requires verified recovery evidence; if safety cannot be established, the affected identity remains fenced.

Recovery timing does not set authorization lifetime. Every ordinary Trust Proof MUST satisfy 0 < exp - iat <= 10 seconds and iat <= current_time < exp. Future-issued proofs and proofs at or beyond expiration MUST be rejected. Invalid or unverifiable timestamps or current time MUST fail closed under KTP-Core. An outage, existing session, queued request, low-risk classification, key grace period, or recovery objective MUST NOT extend that lifetime. Clock rollback MUST NOT restore or prolong an expired permission; if current validity cannot be established, the proof MUST NOT authorize an action.

Recovery Time Objectives (RTO):

~~~
+----------------------+----------+------------+------------+
| Component            | Level 1  | Level 2    | Level 3    |
+----------------------+----------+------------+------------+
| Single Oracle node   | 1 hour   | 15 minutes | 5 minutes  |
| Oracle mesh (quorum) | 4 hours  | 1 hour     | 15 minutes |
| Flight Recorder      | 24 hours | 4 hours    | 1 hour     |
| Federation gateway   | 4 hours  | 1 hour     | 15 minutes |
| Full zone            | 24 hours | 8 hours    | 2 hours    |
+----------------------+----------+------------+------------+
~~~

Recovery Point Objectives (RPO):

~~~
+--------------------+----------+------------+---------------+
| Data Type          | Level 1  | Level 2    | Level 3       |
+--------------------+----------+------------+---------------+
| Trust Score state  | 1 hour   | 15 minutes | 1 minute      |
| Trajectory records | 24 hours | 1 hour     | 15 minutes    |
| Flight Recorder    | 1 hour   | 15 minutes | 0 (real-time) |
| Configuration      | 24 hours | 4 hours    | 1 hour        |
+--------------------+----------+------------+---------------+
~~~

# Failure Modes

## Oracle Node Failure

Definition: Single Oracle node becomes unavailable while remaining nodes continue operating.

### Detection

- Heartbeat failure (3 consecutive missed, 30 seconds)
- Threshold signing failure (node doesn't contribute)
- Health check endpoint returns error or timeout
- Network unreachability

### Impact Assessment

Impact depends separately on the consensus quorum and the signing threshold. The normative contract is `specifications/oracle-consensus.md`:

- The default five-member mesh, tolerating one Byzantine member, requires four distinct members for protected state decisions. One unavailable member leaves enough participants; two unavailable or withholding members pause those decisions.
- A seven-member mesh tolerating two Byzantine members requires at least five participants for protected decisions, under a protocol reviewed for those parameters.
- Three shares of a five-share signing key can still produce a signature when two holders are unavailable. This does not establish a safe consensus decision or authorize a standing update. A two-of-three signing arrangement likewise supplies no one-Byzantine-member consensus guarantee.

Progress also requires mutually communicating participants and the selected protocol's leader-change and timing conditions. Health checks and possession of enough key shares alone do not establish availability. Single-node proof issuance, where permitted by KTP-ORACLE, still requires verified committed standing and every ordinary validity check; it cannot create a new mesh decision.

### Automatic Response

1. DETECT: Monitoring detects node failure
2. ISOLATE: Stop routing work to the unavailable node; retain the authenticated membership, fault budget, and quorum denominator
3. ALERT: Notify operations team
4. CONTINUE: Remaining nodes proceed only where the established consensus and signing requirements can both be met
5. REDISTRIBUTE: Rebalance load across healthy nodes

### Manual Recovery

1. DIAGNOSE: Determine failure cause -  Hardware failure -> Replace hardware -  Software crash -> Analyze, restart or redeploy -  Network issue -> Resolve network problem -  Compromise suspected -> Initiate incident response

1. RESTORE: Return node to operation -  Restart service if software issue -  Redeploy to new hardware if hardware issue -  Restore durable voting and lock state, then verify committed checkpoint and membership evidence under `specifications/oracle-consensus.md`. A backup or a healthy peer's assertion alone is insufficient. If prior voting state cannot be recovered safely, fence the identity until the selected protocol's reviewed recovery procedure makes rejoining safe.

1. VERIFY: Confirm proper operation -  Health check passes -  Authenticated membership and key epochs match -  Prior locks cannot be forgotten or rolled back -  Committed state and transition evidence verify before voting or signing resumes

1. REINTEGRATE: Add back to rotation -  Gradually increase traffic -  Monitor for issues -  Restore full participation

### Key Share Considerations

Oracle node has threshold key share. If node is compromised:

- DO NOT restore node with same key share
- Initiate key rotation procedure (KTP-CRYPTO Section 8.4)
- Generate new key shares for all nodes
- Revoked or compromised keys MUST NOT gain authority through a grace period. Key replacement and any membership transition require the authenticated, committed transition controls in `specifications/oracle-consensus.md` and the applicable KTP-CRYPTO rules.

If node failure is NOT compromise:

- Key share can be restored from backup
- Or regenerated from other shares (if supported)
- HSM attestation should verify integrity

## Oracle Mesh Partition

Definition: Oracle mesh communication separates or delays groups so that they cannot all exchange consensus messages. A compromised member may still communicate selectively with both sides. A group may proceed only with the established quorum and valid protocol evidence; reachable membership MUST NOT replace authenticated membership.

### Detection

- Threshold signing fails (insufficient participants)
- Nodes report partial connectivity
- Network monitoring shows partition

### Impact

CRITICAL: Protected state changes pause wherever a valid consensus quorum cannot be obtained.

- No new consensus-dependent standing, trajectory, genesis, or configuration decision may be inferred from a minority or a signing threshold alone
- Proof issuance stops wherever its own signing, committed-state verification, or other validity requirements cannot be met; consensus loss is not permission to issue from an uncommitted fork
- Existing proofs continue until expiration
- PEPs enforce each proof's original expiration while entering degraded mode
- Operations requiring new proofs fail

### Degradation Behavior

During a partition, PEPs MUST apply the following rules regardless of outage duration:

1. UNEXPIRED PROOF - A cached proof MAY be evaluated only while its original lifetime and all other authorization conditions remain valid. Queuing a refresh request grants no extension.

1. EXPIRED OR UNVERIFIABLE PROOF - Deny new ordinary actions, including actions in existing sessions and actions classified as low risk. Continuing actions MUST obtain a fresh valid proof or cease ordinary operation through a previously declared, bounded safe transition. Such a transition MUST NOT continue the original task or introduce new discretionary actions; independently authorized emergency actions use the separate path below.

1. SEPARATE EMERGENCY CAPABILITY - Evaluate an explicitly matched, independently authorized emergency capability only under `specifications/emergency-capability.md`. If it is absent or unverifiable, deny. Neither a partition nor emergency mode permits a lower signing quorum, a stale ordinary proof, or a widened policy. Alert administrators.

### Resolution

1. IDENTIFY partition cause -  Network failure between sites -  BGP issue, firewall misconfiguration -  DDoS attack on network links

1. RESOLVE network issue -  Work with network team -  Activate backup network paths -  Engage ISP if external

1. VERIFY state after healing -  Authenticate membership and committed checkpoints, recover missing records, and preserve the selected protocol's locks and view-change evidence. Uncommitted proposals may be abandoned only by that protocol's safe rules. Two conflicting committed records for the same position constitute a safety incident: preserve evidence, fence the affected state, and investigate. Operators MUST NOT select a winner by timestamp, longest local log, or administrator preference and resume signing.

### Prevention

- Geographic diversity but network redundancy
- Multiple network paths between Oracle sites
- Monitoring of network health
- Regular partition testing

## Total Oracle Loss

Definition: All Oracle nodes fail or are unreachable. No threshold signing is possible.

This is the most severe failure mode.

### Detection

- All health checks fail
- No nodes respond to signing requests
- Monitoring shows all nodes down

### Impact

CRITICAL: Zone is effectively offline for new trust decisions

- No new Trust Proofs
- Existing proofs expire within seconds
- Ordinary permissions cease at each proof's original expiration
- The zone MAY evaluate a separately authorized emergency capability

### Emergency Mode Operation

When total Oracle loss is detected, ordinary Trust Proof expiration remains mandatory. Entering emergency mode grants no authority.

1. An emergency action MUST be independently authorized by a capability established before the incident and MUST match its named action, subject, resource, activation conditions, limits, and validity under `specifications/emergency-capability.md`. The PEP MUST verify that capability independently of the unavailable ordinary Oracle path. Absent or unverifiable authorization means denial.

1. Life-safety and infrastructure maintenance labels are not exceptions. Emergency actions remain subject to applicable Soul constraints, the capacity veto, and the companion's audit requirements. Loss of the evidence needed to establish those conditions MUST NOT resolve toward permission.

1. During the outage, operators MUST NOT create or widen emergency authority, extend its validity, relax approval requirements, or reduce signing quorums. Restriction and revocation follow the companion's controls. A human invocation or incident declaration cannot override these boundaries.

1. Alert the incident team and activate the declared recovery procedures. Key restoration, when necessary, requires the applicable key ceremony; restoration of infrastructure alone does not establish permission to resume ordinary actions.

### Recovery from Total Loss

SCENARIO A: Infrastructure failure (all nodes down but intact)

1. Restore infrastructure (network, power, hardware)
2. Restart Oracle nodes
3. Nodes recover state from local storage
4. Verify threshold signing works
5. Exit emergency mode

SCENARIO B: Data loss (nodes destroyed)

1. Provision new Oracle infrastructure
2. Restore from backup: -  Configuration from backup -  State from backup -  Key shares from secure backup (if available)
3. If key shares not recoverable: -  Initiate key recovery ceremony -  Recover from trustee-held shares
4. Verify and reintegrate

SCENARIO C: Suspected compromise (all nodes potentially hostile)

1. DO NOT restore from current backups (may be compromised)
2. Activate incident response
3. Rebuild from known-good golden images
4. Key ceremony to generate new keys
5. Re-enroll all agents (may be required)
6. Forensic investigation of compromise

## Flight Recorder Failure

Definition: Flight Recorder becomes unavailable or corrupted.

### Detection

- Write failures from components
- Read failures for queries
- Integrity check failures
- Storage exhaustion

### Impact

MEDIUM-HIGH: Audit trail may have gaps

- New decisions may not be recorded
- Historical queries fail
- Compliance impact
- Forensic capability degraded

Note: Flight Recorder failure does NOT stop Trust Proof issuance. Operations can continue, but without audit.

### Degradation Behavior

1. LOCAL BUFFERING -  Components buffer audit records locally -  Typical buffer: 1 hour of records -  Buffer overflow: oldest records dropped (with count)

1. SECONDARY FLIGHT RECORDER -  If configured, switch to secondary -  Primary failure logged

1. ALERTING -  Immediate alert on Flight Recorder failure -  Escalating alerts as buffer fills

### Recovery

1. Restore Flight Recorder service
2. Flush buffered records from components
3. Verify chain integrity -  Chain will have gap marker if records lost -  Gap is itself recorded and auditable
4. Investigate cause of failure

### Chain Gap Handling

If records were lost during failure:

{ "record_type": "chain_gap", "gap_start": "2025-11-25T10:00:00Z", "gap_end": "2025-11-25T10:15:00Z", "estimated_records_lost": 1500, "cause": "flight_recorder_failure", "recovery_action": "restored_from_backup", "signature": "..." }

Gap records are signed by Oracle and become part of permanent audit trail.

## Sensor Aggregator Failure

Definition: Sensor aggregator becomes unavailable.

### Impact

MEDIUM: Context Signal updates degraded

- Sensors cannot deliver readings
- Risk Factor inputs use stale data
- Risk Factor calculation affected

### Degradation Behavior

1. SENSOR BUFFERING -  Sensors buffer readings locally -  Typical buffer: 5 minutes

1. STALE DATA MARKING - Oracle MUST mark stale inputs and resolve inputs beyond their declared freshness under \[KTP-CORE] Sections 5.2 and 6.7. An unobserved Risk Factor term uses the conservative substitute 1.0; it MUST NOT be reused as a current measurement or defaulted toward permission. If no valid risk calculation is possible, no authorizing result may be issued.

1. FAILOVER -  Sensors switch to backup aggregator (if configured)

### Recovery

1. Restore aggregator service
2. Sensors flush buffered readings
3. Context Signals return to real-time
4. Trust Scores normalize

## Federation Gateway Failure

Definition: Federation gateway becomes unavailable.

### Impact

MEDIUM: Cross-zone trust affected

- Cannot accept foreign Trust Proofs
- Cannot issue cross-zone attestations
- Federation heartbeat fails
- Partner zones see this zone as degraded

### Degradation Behavior

1. CACHED FOREIGN PROOFS - Evaluate cached foreign proofs only within their original validity, including 0 < exp - iat <= 10 seconds and iat <= current_time < exp. Invalid or unverifiable timestamps or current time mean denial. Existing sessions and outages provide no extension. No new foreign proofs are accepted through the failed gateway.

1. LOCAL OPERATION -  Zone operates independently -  Local agents unaffected -  Cross-zone agents cannot operate

1. PARTNER NOTIFICATION -  Heartbeat failure notifies partners -  Partners reduce trust factor for this zone

### Recovery

1. Restore federation gateway
2. Re-establish federation connections
3. Resume heartbeat
4. Trust factor gradually recovers

## Zone-Wide Failure

Definition: Entire zone becomes unavailable (natural disaster, massive infrastructure failure, coordinated attack).

### Impact

CRITICAL: All zone operations cease

- All agents in zone cannot operate
- All protected resources inaccessible
- Federation partners lose connection

### Recovery Options

OPTION A: Restore in place

- Rebuild infrastructure at same location
- Restore from backups
- Resume operations

OPTION B: Failover to DR site

- Activate disaster recovery site
- Restore from replicated data
- Update DNS/routing to DR site
- Resume operations at DR

OPTION C: Migrate to partner zone (temporary)

- Federated partner accepts refugees
- Agents operate with reduced trust (foreign zone penalty)
- Temporary until primary zone restored

### DR Site Requirements

For Level 3 deployments, DR site MUST:

- Be geographically separate (>100 miles recommended)
- Have independent power and network
- Maintain synchronized state (RPO per Section 2)
- Have HSMs with key shares
- Be tested quarterly

# Backup Procedures

## What to Back Up

### Critical (MUST back up)

ORACLE SIGNING KEY SHARES

- Threshold key shares for Trust Proof signing
- Backup encrypted to recovery keys
- Stored with trustees (not with Oracle)
- Recovery requires M-of-N trustees

ZONE CONFIGURATION

- Security policies, thresholds, weights
- Soul constraints
- Trust Tier boundaries
- Federation agreements

FLIGHT RECORDER DATA

- All audit records
- Chain hashes
- External anchor references

### Important (SHOULD back up)

AGENT REGISTRY

- Registered agents
- Public keys
- Lineage information
- Current E_base (can be recalculated)

TRAJECTORY CHAINS

- Agent transaction history
- Proof of Resilience records
- (Large; may use differential backups)

SENSOR CONFIGURATION

- Sensor registrations
- Aggregator mappings
- Baseline calibrations

### Reconstructible (MAY back up)

TRUST SCORES

- Current E_trust values
- Can be recalculated from E_base and the Risk Factor inputs

CONTEXT SIGNALS

- Current sensor readings
- Will be refreshed by live sensors

CACHED TRUST PROOFS

- Short-lived, will be re-issued

## Backup Frequency

~~~
+-------------------+-------------------+----------------------+
| Data Type         | Backup Frequency  | Retention            |
+-------------------+-------------------+----------------------+
| Key shares        | On change only    | Forever              |
| Configuration     | On change + daily | 1 year               |
| Flight Recorder   | Continuous/hourly | Per policy (7 years) |
| Agent Registry    | Daily             | 90 days              |
| Trajectory Chains | Daily incremental | 1 year full, 7 incr  |
| Sensor Config     | Daily             | 90 days              |
+-------------------+-------------------+----------------------+
~~~

## Backup Security

ENCRYPTION

- All backups encrypted at rest
- Encryption key separate from backed-up keys
- Key shares backed up to different location than data

ACCESS CONTROL

- Backup access requires authentication
- Restore requires multi-person authorization (Level 2+)
- All access logged

INTEGRITY

- Backups include cryptographic checksums
- Verify integrity before restore
- Detect tampering

ISOLATION

- Backups stored separately from production
- Air-gapped for highest security (Level 3)
- Ransomware cannot reach backups

## Backup Verification

VERIFICATION SCHEDULE

- Automated integrity check: Daily
- Restore test to isolated environment: Monthly
- Full DR test: Quarterly (Level 2+), Monthly (Level 3)

VERIFICATION PROCEDURES

1. Verify backup file integrity (checksums)
2. Verify backup completeness (all expected files)
3. Restore to isolated environment
4. Verify restored system functions
5. Verify restored data matches source
6. Document results

# Restoration Procedures

## Oracle Restoration

### Single Node Restoration

Prerequisites:

- Healthy Oracle mesh (other nodes operational)
- Backup of node configuration
- Key share (from backup or ceremony)

Procedure:

1. PROVISION infrastructure -  Deploy new VM/hardware -  Install Oracle software -  Configure network

1. RESTORE configuration -  Apply configuration from backup -  Verify configuration matches zone

1. RESTORE key share -  If HSM available: Import key share -  If HSM destroyed: Recover from trustee backup

1. SYNC state -  Connect to healthy nodes -  Sync current Trust Score state -  Sync recent trajectory updates

1. VERIFY operation -  Run health checks -  Participate in test signing -  Verify state matches other nodes

1. REINTEGRATE -  Add to load balancer -  Enable full traffic

### Full Mesh Restoration

Prerequisites:

- New infrastructure for all nodes
- Configuration backups
- Key shares (from trustees or ceremony)
- State backups

Procedure:

1. PROVISION all infrastructure -  Deploy all Oracle nodes -  Configure network between nodes

1. RESTORE configuration to all nodes -  Same configuration on all nodes

1. KEY RECOVERY CEREMONY -  Convene required trustees -  Recover threshold key shares -  Install shares in HSMs

1. RESTORE state -  Restore Agent Registry from backup -  Restore trajectory data from backup -  Restore last known Trust Scores

1. VERIFY threshold signing -  Attempt to sign test message -  Verify k-of-n nodes can sign

1. RESUME operations -  Enable PEP connections -  Issue Trust Proofs -  Monitor closely

## Key Recovery

### Key Recovery Prerequisites

Key recovery requires:

- M-of-N trustees (typically 3-of-5 or 5-of-7)
- Trustees have recovery key shares
- Secure environment for ceremony
- New HSMs to receive recovered keys

Trustees should be:

- Geographically distributed
- Organizationally independent
- Personally reliable
- Reachable in emergency

### Key Recovery Ceremony

PHASE 1: CONVENE

1. Incident commander declares key recovery needed
2. Contact trustees (secure channel)
3. Schedule ceremony (virtual or in-person)
4. Prepare secure environment

PHASE 2: AUTHENTICATE

1. Verify trustee identity (multi-factor)
2. Verify ceremony authorization
3. Record ceremony (video + transcript)
4. Witnesses present (if required)

PHASE 3: RECOVER

1. Each trustee decrypts their recovery share
2. Shares combined in secure environment
3. Master key material reconstructed
4. New threshold shares generated
5. Shares installed in HSMs
6. Master key material destroyed (never stored)

PHASE 4: VERIFY

1. Test threshold signing
2. Verify all nodes can participate
3. Issue test Trust Proof
4. Verify signature validates

PHASE 5: DOCUMENT

1. Record ceremony completion
2. Update key inventory
3. Notify stakeholders
4. Archive ceremony recording (secure)

### Key Recovery Security

- Recovery environment: Air-gapped if possible
- No photography except official recording
- All attendees logged
- Ceremony room swept for bugs (Level 3)
- Shares transmitted encrypted, never in clear

## State Reconstruction

If state backups are unavailable or suspect:

### Agent Registry Reconstruction

If backup unavailable:

1. Agents must re-register
2. Identity proofing re-verified
3. Sponsor relationships re-established
4. E_base starts from initial value (not historical)

Impact: Agents lose accumulated trust. Significant operational disruption. Use backup restoration if at all possible.

### Trust Score Reconstruction

Recovery MUST use the current Core calculation:

~~~
E_trust = E_base * (1 - R)
~~~

Before issuing an authorizing result, the Oracle MUST authenticate the recovered standing and establish that it remains current. Restoration MUST preserve the original expiry, withdrawal and revocation state of external attestations, all applicable ceilings, and the validity of supporting evidence. A backup timestamp or recovery event MUST NOT renew any of them.

Recovery MUST retain valid historical PoR without subtracting points solely for elapsed time or inactivity. It MUST preserve authenticated corrections to invalid claims. That retained history does not establish operational readiness: before an affected operation resumes, establish the current assessment and matched decision under specifications/operational-readiness.md for the exact recovered code/model/configuration/toolchain/permissions and actual operation.

The installed standing policy, independently approved readiness criteria, authorized assessor and issuer bindings, readiness epoch, evidence revocations, and policy/version floor MUST survive restart and restore. A stale backup, archived v2 profile, old epoch, retained signature, or heartbeat MUST NOT roll back those controls or renew expired evidence. If their authenticated current state cannot be established, keep the affected operation unavailable. Assessment or remediation requires its separately authorized safe route and does not override any current safety veto or earn standing credits.

R MUST be calculated from currently valid observations and the declared valid weights, with undefined terms handled under \[KTP-CORE] Sections 5.2 and 6.7. A missing observation uses the specified restrictive handling; a failed calculation MUST NOT be replaced with a fabricated score. If E_base is unknown or its current validity cannot be established, the Oracle MUST NOT invent standing from a lineage default. Fresh enrollment or re-attestation may establish new standing through its normal authorization procedure.

If the required inputs cannot yield a valid current E_trust, recovery MUST NOT issue an authorizing result. A separately authorized emergency capability, if present, is evaluated under `specifications/emergency-capability.md`; it does not reconstruct or extend ordinary trust.

### Trajectory Reconstruction

Trajectory chains are cryptographically linked. If chain is broken:

1. Recover as much chain as possible from backup
2. Mark gap in chain
3. Resume new authoritative records only after recovering an authenticated head and continuity, or completing the separately authorized migration procedure below
4. Agent's E_base calculation notes gap

Gaps in trajectory reduce trust (unverifiable history).

For consensus-protected trajectory records, marking a gap MUST NOT authorize inventing a predecessor, reusing a committed position, or discarding a committed successor. Reconstruction MUST establish the authenticated committed head and continuity evidence required by `specifications/oracle-consensus.md` before new co-signing. If that evidence is unavailable, the affected history remains fenced; a lower trust score alone does not repair consensus safety.

For v3 records, recovery MUST apply specifications/trajectory-signatures.md: reconstruct and verify both complete canonical JWS payloads, the final signed-envelope hash, and the independently authenticated final-head selection. A stored record_hash, an intent certificate, a valid signature pair, or an internally consistent suffix alone does not establish the current authoritative head. Recovery MUST preserve the selected final hash even where another valid ECDSA envelope exists for the same committed intent. The restored trusted version/algorithm/profile floor, key state, and head evidence MUST be authenticated independently of the candidate records.

Legacy v2 records MUST be restored as their original archival bytes, not reserialized or automatically promoted into active v3 records. An authorized transition to a new v3 chain requires an independently signed migration checkpoint binding the legacy head/archive, independently revalidated carried state, and the approved target chain/genesis/profile. The new genesis includes the checkpoint digest before it is signed; its final envelope is anchored separately afterward. The checkpoint MUST NOT depend on that final genesis hash. Recovery MUST retain the durable v3 format floor and the single-use lineage succession, so an old backup cannot reactivate v2 authority, reuse a checkpoint, or start a second successor. Membership changes additionally require the joint-transition evidence in specifications/oracle-consensus.md. Without this evidence, keep the affected lineage fenced.

## Trajectory Recovery

Trajectory data may be large. Recovery strategies:

FULL RESTORE

- Restore complete trajectory from backup
- Slowest but most complete
- Use for complete zone recovery

POINT-IN-TIME RESTORE

- Restore trajectory to specific point
- Useful if recent data corrupted
- Records after restore point lost

Point-in-time restoration is not permission to forget later consensus decisions. Before renewed voting or signing, recover and verify the committed suffix and relevant locks, or complete the selected protocol's reviewed recovery procedure. The earlier snapshot alone cannot authorize a new branch of the same history.

DIFFERENTIAL RESTORE

- Restore base + incremental backups
- Faster than full restore
- Standard approach for routine recovery

# Graceful Degradation

## Degradation Levels

KTP defines four degradation levels:

LEVEL 0: NORMAL

- All components operational
- Full functionality
- Standard Trust Score calculation

LEVEL 1: DEGRADED

- Some redundancy lost
- Full functionality maintained
- Increased monitoring
- Example: 1 Oracle node down (but quorum intact)

LEVEL 2: IMPAIRED

- Some functionality reduced
- Core security maintained
- Non-critical features disabled
- Example: Sensor aggregator down (stale Context Signals)

LEVEL 3: EMERGENCY

- Critical functionality only
- Fail-closed for non-essential
- Human intervention required
- Example: Oracle mesh partitioned

LEVEL 4: OFFLINE

- Zone non-operational
- All requests denied
- Recovery in progress
- Example: Total Oracle loss

## Automatic Failover

### Oracle Failover

- Automatic only while the established quorum and protocol conditions permit progress
- Leader replacement follows the reviewed view-change procedure and carries prior decision evidence
- A timeout, restart, or removal from routing does not reduce membership or reset locks

### Flight Recorder Failover

- Automatic switch to secondary (if configured)
- Local buffering during transition
- Alert on primary failure

### Sensor Aggregator Failover

- Sensors automatically retry backup aggregator
- Oracle uses stale data with marking
- Automatic when aggregator returns

### Federation Failover

- Automatic failover to backup gateway
- Partners notified via heartbeat
- Automatic reconnection on recovery

## Manual Intervention

Some situations require manual intervention:

- Total Oracle loss
- Suspected compromise
- Key recovery
- DR site activation
- Configuration rollback

Manual procedures are documented in Appendix A.

# Testing and Validation

## Recovery Testing Requirements

~~~
+----------------------+-----------+-------------+-----------+
| Test Type            | Level 1   | Level 2     | Level 3   |
+----------------------+-----------+-------------+-----------+
| Backup verification  | Monthly   | Weekly      | Daily     |
| Single node recovery | Quarterly | Monthly     | Monthly   |
| Mesh partition test  | Annually  | Quarterly   | Monthly   |
| Full DR test         | Annually  | Quarterly   | Monthly   |
| Key recovery drill   | Annually  | Semi-annual | Quarterly |
+----------------------+-----------+-------------+-----------+
~~~

## Test Procedures

SINGLE NODE RECOVERY TEST

1. Take one Oracle node offline (planned)
2. Verify mesh continues operating
3. Restore node from backup
4. Verify node rejoins mesh
5. Document time and issues

PARTITION TEST

1. Simulate network partition (firewall rules)
2. Verify PEPs enter degraded mode
3. Verify no Trust Proofs issued during partition
4. Heal partition
5. Verify normal operation resumes

FULL DR TEST

1. Activate DR site
2. Restore all components from backup
3. Verify full functionality
4. Measure RTO and RPO achieved
5. Fail back to primary

# Security Considerations

## Recovery as Attack Vector

Recovery procedures can be exploited:

- Attacker triggers failure to invoke recovery
- Attacker substitutes malicious backup
- Attacker compromises recovery process
- Attacker uses recovery mode to bypass controls

Mitigations:

- Authenticate all recovery actions
- Verify backup integrity before restore
- Maintain audit during recovery
- Time-limit recovery mode

## Backup Security

Backups are high-value targets:

- Contain all secrets (encrypted, but still)
- May reveal system architecture
- May enable offline attacks

Mitigations:

- Encrypt all backups
- Separate backup encryption keys
- Access control on backups
- Monitor backup access

## Key Recovery Security

Key recovery is highest-risk operation:

- Reconstitutes master key material
- Single point where key exists in full
- Attractive target for advanced attackers

Mitigations:

- Ceremony with witnesses
- Secure environment
- Immediate destruction after use
- M-of-N trustee requirement

--- back

# Recovery Runbooks

The commands below are illustrative operational steps, not authority to bypass `specifications/oracle-consensus.md`. Restoring configuration, importing shares, joining a mesh, or clearing degradation MUST verify authenticated membership epochs, durable vote/lock recovery, and committed state. Replacing an identity or changing membership requires the committed transition with the old and new quorums; a partition cannot authorize its own smaller committee.

A.1.  Runbook: Single Oracle Node Recovery

TRIGGER: Oracle node health check fails for 5 minutes

STEPS:

1. Verify failure (not monitoring false positive) $ ktp-cli oracle status --node oracle-1

1. Check if quorum maintained $ ktp-cli oracle mesh-status Expected: authenticated membership epoch, established quorum, and distinct eligible participants; the default requires four of the original five members, not a majority of healthy nodes

1. Attempt restart $ systemctl restart ktp-oracle Wait 60 seconds, check status

1. If restart fails, check logs $ journalctl -u ktp-oracle -n 100

1. If hardware issue, provision new node $ terraform apply -target=oracle-node-1

1. Restore configuration $ ktp-backup restore --target oracle-1 --type config

1. Restore key share (requires HSM access) $ ktp-hsm import-share --node oracle-1

1. Verify and reintegrate $ ktp-cli oracle join-mesh --node oracle-1 $ ktp-cli oracle verify-signing --node oracle-1

ESCALATION: If not resolved in 30 minutes, page on-call lead

A.2.  Runbook: Oracle Mesh Partition

TRIGGER: Trust Proof issuance fails, partition detected

STEPS:

1. Verify partition $ ktp-cli oracle mesh-status Expected: "Mesh partitioned, no quorum"

1. Identify partition boundaries $ ktp-cli oracle connectivity-matrix

1. Check network connectivity $ for node in oracle-{1..5}; do ping -c 1 $node && echo "$node reachable" done

1. If network issue, engage network team -  Check firewall rules -  Check BGP status -  Check physical connectivity

1. If single site isolated, verify other sites operational $ ktp-cli oracle site-status

1. When partition heals, verify mesh reforms $ ktp-cli oracle mesh-status Expected: "Mesh operational"

1. Check for state conflicts $ ktp-cli oracle state-consistency-check Conflicting committed records require fencing and incident investigation; do not proceed to normal operation

1. Resume normal operations $ ktp-cli zone set-degradation-level 0

ESCALATION: Immediate page to incident commander

A.3.  Runbook: Total Oracle Loss Recovery

TRIGGER: All Oracle nodes unreachable

STEPS:

1. Declare incident -  Page incident commander -  Activate incident response team -  Begin incident timeline

1. Assess situation -  Infrastructure failure vs. attack -  Data center status -  Network status

1. If infrastructure failure: a.  Restore infrastructure b.  Restore from backup (see A.4)

1. If suspected attack: a.  DO NOT restore from recent backups b.  Engage security team c.  Preserve evidence d.  Rebuild from golden images e.  Key recovery ceremony required

1. Activate DR site (if available) $ ktp-dr activate --site dr-west

1. Update DNS/routing to DR $ ktp-dns failover --to dr-west

1. Verify DR operational $ ktp-cli oracle mesh-status --site dr-west

1. Communicate status to stakeholders

ESCALATION: This IS the escalation

A.4.  Runbook: Restore from Backup

TRIGGER: Recovery requires backup restoration

STEPS:

1. Identify backup to restore $ ktp-backup list --type full Select most recent known-good backup

1. Verify backup integrity $ ktp-backup verify --backup-id \<id> MUST pass before proceeding

1. Provision target infrastructure $ terraform apply

1. Restore configuration $ ktp-backup restore --backup-id \<id> --type config

1. Restore state data $ ktp-backup restore --backup-id \<id> --type state

1. Restore trajectories (may take time) $ ktp-backup restore --backup-id \<id> --type trajectory

1. Key recovery (if needed) -  Contact trustees -  Schedule ceremony -  Execute per Section 5.2.2

1. Verify system operational $ ktp-cli oracle mesh-status $ ktp-cli oracle test-sign

1. Gradually restore traffic $ ktp-cli zone set-degradation-level 1 Monitor for 15 minutes $ ktp-cli zone set-degradation-level 0

A.5.  Runbook: Key Recovery Ceremony

TRIGGER: Key shares unrecoverable from backup

PREPARATION:

1. Incident commander authorizes ceremony
2. Contact M trustees (need M of N)
3. Schedule ceremony time (within RTO)
4. Prepare secure environment: -  Air-gapped machine -  New HSMs -  Recording equipment -  Witness(es)

CEREMONY:

1. Verify all participants' identity
2. Begin recording
3. Read ceremony authorization into record
4. Each trustee: a.  Connects to ceremony machine (isolated) b.  Decrypts their recovery share c.  Inputs share to recovery software d.  Disconnects
5. Recovery software reconstructs master key
6. Generate new threshold shares
7. Install shares in HSMs
8. Test threshold signing
9. Securely destroy master key material
10. End recording

POST-CEREMONY:

1. Verify all Oracle nodes operational
2. Generate new trustee recovery shares
3. Distribute to trustees
4. Archive ceremony recording
5. Update key inventory
