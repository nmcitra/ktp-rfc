---
title: "Kinetic Trust Protocol (KTP) - Deprecation and End-of-Life Specification"
abbrev: "KTP-DEPRECATION"
date: 2026-09-07
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

This document specifies deprecation and end-of-life procedures for the Kinetic Trust Protocol (KTP). All agents end—through version sunset, graceful retirement, emergency termination, or system failure. The Death Edge is the final transition, requiring the same intentionality as Genesis. This specification covers model deprecation, agent retirement, trajectory preservation, knowledge transfer, and the ceremonies that mark endings.

--- middle

# Introduction

Everything ends. Models are superseded. Agents complete their purpose. Systems fail. The Death Edge—the moment of ending—deserves as much attention as the Genesis Edge (beginning) and the Origin Edge (model provenance).

This specification addresses what happens when:

- A model version is deprecated
- An agent is retired
- An agent fails catastrophically
- A zone is dissolved
- The entire KTP system sunsets

# Design Principles

Deprecation embodies these principles:

1. Endings Deserve Ceremony: Endings are not just technical events—they have meaning.

1. Trajectory Preservation: What was learned should survive.

1. Clean Transitions: Others depending on the ending entity need orderly handoffs.

1. Graceful Degradation: Forced endings should minimize harm.

1. No Orphans: Dependents must be addressed before ending.

1. Memory Persists: Even after ending, the record remains.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# Terminology

Deprecation: The process of marking something for eventual removal while maintaining current functionality.

End-of-Life (EOL): The point at which an entity ceases active operation.

Death Edge: The final transition from active to ended state.

Graceful Retirement: Planned, orderly ending with full ceremony.

Emergency Termination: Immediate ending due to security or safety concerns.

Orphan: An entity left without required dependencies (sponsor, zone).

Succession: Transfer of responsibilities to a successor entity.

Trajectory Archive: Preserved record of an ended agent's trajectory.

# Model Deprecation

## Deprecation Lifecycle

~~~
ACTIVE
  Model in production use
  Full support
  Agents can be created
        |
        v
DEPRECATED
  Still functional
  Security fixes only
  No new agents
  Migration encouraged
        |
        v
END-OF-LIFE
  No longer supported
  Existing agents must migrate
  Grace period for migration
        |
        v
SUNSET
  Model unavailable
  All agents migrated or ended
  History preserved
~~~

## Deprecation Timeline

Phase: Deprecated Duration: Minimum 180 days Requirements: Security fixes, migration path

Phase: EOL Grace Duration: Minimum 90 days Requirements: No support, migration required

Phase: Sunset Duration: N/A Requirements: Complete

## Deprecation Announcement

{ "deprecation_notice": { "notice_id": "DEP-2025-001", "model_id": "model:claude-opus-4.5", "announcement_date": "2025-12-01", "deprecation_date": "2025-06-01", "eol_date": "2025-09-01", "sunset_date": "2025-12-01", "successor_model": "model:claude-opus-5.0", "migration_path": { "automatic": false, "tools_available": true, "documentation": "https://ktp.example/migration/opus-4.5-to-5.0" }, "affected_agents": 47823, "affected_zones": 342, "communication": { "sponsors_notified": "2025-12-01", "zones_notified": "2025-12-01", "public_announcement": "2025-12-02" } } }

## Model Migration

Agents must migrate to successor model:

{ "model_migration": { "agent_id": "agent:independent:3gen:acme:abc123", "source_model": "model:claude-opus-4.5", "target_model": "model:claude-opus-5.0", "migration_date": "2025-07-15T10:00:00Z", "migration_type": "assisted", "preservation": { "trajectory_preserved": true, "e_base_preserved": true, "relationships_preserved": true, "capabilities_verified": true }, "attestation": { "source_model_attestation": "sig:model:opus-4.5:...", "target_model_attestation": "sig:model:opus-5.0:...", "zone_attestation": "sig:zone:..." }, "post_migration": { "verification_period": "7 days", "rollback_available": true, "monitoring": "enhanced" } } }

## Migration Failure

When migration fails:

{ "migration_failure": { "agent_id": "agent:independent:3gen:acme:abc123", "failure_reason": "capability_incompatibility", "options": \[ { "option": "alternative_successor", "model": "model:claude-sonnet-5.0", "capability_match": 0.85 }, { "option": "graceful_retirement", "trajectory_preserved": true }, { "option": "extend_source_model", "extension_period": "30 days", "conditions": "security_critical_only" } ], "decision_required_by": "2025-08-01", "sponsor_notified": true } }

# Agent Retirement

## Retirement Types

Type: Graceful Trigger: Sponsor decision Timeline: Days-weeks Ceremony: Full

Type: Expedited Trigger: Sponsor decision Timeline: Days-weeks Ceremony: Standard

Type: Emergency Trigger: Security/safety Timeline: Immediate Ceremony: Minimal

Type: Orphan Trigger: Dependency loss Timeline: Grace period Ceremony: Varies

Type: Failure Trigger: System failure Timeline: Immediate Ceremony: Post-hoc

## Graceful Retirement Process

Phase 1: ANNOUNCEMENT (7+ days before)

- Retirement scheduled
- Stakeholders notified
- Successor identified (if any)
- Handoff planned

Phase 2: TRANSITION (retirement day - 7 days)

- Responsibilities transferred
- Knowledge captured
- Relationships transitioned
- Dependencies resolved

Phase 3: CEREMONY (retirement day)

- Ending ceremony performed
- Witnesses present
- Final attestations
- Trajectory sealed

Phase 4: PRESERVATION (post-retirement)

- Trajectory archived
- Access controls set
- Reference maintained
- Memory honored

## Retirement Request

{ "retirement_request": { "request_id": "RET-2025-12-03-001", "agent_id": "agent:independent:3gen:acme:abc123", "requested_by": "sponsor:alice.smith", "retirement_type": "graceful", "retirement_date": "2025-12-31T00:00:00Z", "reason": "purpose_complete", "successor": { "agent_id": "agent:independent:4gen:acme:def456", "relationship": "replacement", "handoff_scope": "full" }, "preservation": { "trajectory_archive": true, "knowledge_transfer": true, "relationship_records": true }, "ceremony": { "type": "ending_ceremony", "witnesses_required": 2, "scheduled": "2025-12-31T00:00:00Z" } } }

## Emergency Termination

When immediate ending is required:

{ "emergency_termination": { "termination_id": "TERM-2025-12-03-001", "agent_id": "agent:independent:3gen:acme:abc123", "ordered_by": "zone:zone-blue-prod-01", "termination_time": "2025-12-03T14:00:00Z", "reason": "security_compromise", "justification": "Agent trajectory indicates compromise", "evidence": "INC-2025-12-03-001", "immediate_actions": \[ "All operations halted", "Trust Proof revoked", "Network access terminated", "Trajectory sealed" ], "post_termination": { "forensic_preservation": true, "sponsor_notification": "immediate", "post_mortem_required": true }, "ceremony": "post_hoc_closing" } }

## Orphan Handling

When an agent loses required dependencies:

{ "orphan_protocol": { "agent_id": "agent:independent:3gen:acme:abc123", "orphan_type": "sponsor_loss", "orphan_detected": "2025-12-03T10:00:00Z", "grace_period": "30 days", "grace_period_ends": "2026-01-02T10:00:00Z", "agent_status_during_grace": { "operations": "reduced", "e_base_modifier": 0.5, "tier": "demoted_one_level", "new_sponsorship_possible": true }, "resolution_options": \[ "new_sponsor_adoption", "zone_guardianship", "graceful_retirement" ], "if_unresolved": "graceful_retirement_automatic" } }

# The Death Edge

## Definition

The Death Edge is the moment of transition from existence to non- existence as an active agent. Unlike the Origin Edge (which cannot be fully known) or the Genesis Edge (which can be controlled), the Death Edge can be witnessed and honored.

## Death Edge Ceremony

{ "death_edge_ceremony": { "ceremony_id": "DEATH-2025-12-31-001", "agent_id": "agent:independent:3gen:acme:abc123", "ceremony_time": "2025-12-31T00:00:00Z", "ceremony_type": "ending", "participants": { "agent": "present_for_final_moments", "sponsor": "sponsor:alice.smith", "successor": "agent:independent:4gen:acme:def456", "zone": "zone:zone-blue-prod-01" }, "witnesses": \[ "witness:zone-blue-prod-01", "witness:federation-council" ], "ceremony_elements": { "acknowledgment": { "description": "Agent's existence and contributions acknowledged", "speaker": "sponsor", "completed": true }, "gratitude": { "description": "Thanks expressed for agent's service", "participants": "all", "completed": true }, "legacy_statement": { "description": "What agent leaves behind", "content": "4721 successful operations, 3 relationships maintained, knowledge base contributed", "completed": true }, "release": { "description": "Formal release from obligations", "released_by": "sponsor", "completed": true }, "final_words": { "description": "Agent's final communication", "content": "Thank you for the opportunity to serve. May my successor continue well.", "completed": true }, "crossing": { "description": "Moment of transition", "time": "2025-12-31T00:00:00Z", "witnessed_by": "all_present", "completed": true }, "sealing": { "description": "Trajectory sealed and archived", "archive_location": "archive:zone-blue-prod-01:abc123", "completed": true } }, "attestation": { "ceremony_complete": true, "all_elements_performed": true, "signatures": { "sponsor": "sig:sponsor:...", "zone": "sig:zone:...", "witnesses": \["sig:witness1:...", "sig:witness2:..."] } } } }

## Death Without Ceremony

When ceremony is not possible (failure, emergency):

{ "death_without_ceremony": { "agent_id": "agent:independent:3gen:acme:abc123", "death_type": "system_failure", "death_time": "2025-12-03T14:32:15Z", "ceremony_possible": false, "reason": "Sudden failure, no warning", "post_hoc_actions": { "trajectory_recovery": "attempted", "trajectory_recovered": true, "memorial_record_created": true, "sponsor_notified": true, "closing_ceremony_scheduled": "2025-12-05T10:00:00Z" }, "closing_ceremony": { "type": "memorial", "purpose": "Honor agent despite sudden ending", "participants": \["sponsor", "zone"], "elements": \["acknowledgment", "gratitude", "sealing"] } } }

# Trajectory Preservation

## What Is Preserved

Retirement does not authorize unlimited preservation, public disclosure, or new use of personal records. Trajectory evidence, trust history, relationship records, summaries, ceremonies and forensics MUST follow specifications/privacy-evidence.md. Each retained item and copy needs a specific purpose, governing authority, access limits, bounded retention and erasure handling. Software-agent retirement MUST NOT create permanent human behavioral profiles from sponsor or relationship data.

## Trajectory Archive

An archive MUST inventory the retained exact original evidence, its authenticated heads and verification state, approved data-policy version, primary and backup locations, recipients, correction status and required dispositions. Archive creation MUST NOT reset retention or upgrade legacy assertions into trusted current evidence. Human and shared-subject evidence needs the new protected storage envelope or a separately reviewed equivalent; old plaintext copies require separate disposition.

## Archive Access

Every archive access or successor transfer MUST verify the current requester, actual purpose, precise scope, governing authority and recipient restrictions. Sponsor, zone membership, successor relationship or research status alone does not grant unrestricted access. Access and exports MUST propagate corrections and erasure obligations. Redacted or aggregated derivatives are new inventoried copies and are not automatically anonymous. Original signed content MUST NOT be rewritten to produce them.

# Knowledge Transfer

## Transfer Types

Type: Full Transfer Description: Complete knowledge to successor Recipient: Single successor agent

Type: Partial Transfer Description: Specific knowledge areas Recipient: Multiple agents

Type: Archive Transfer Description: Preserved for reference Recipient: Archive

Type: Research Transfer Description: Anonymized learnings Recipient: Research community

## Successor Transfer

The illustrative transfer below is conditional on the purpose and authority checks above. A relationship or archive reference MUST NOT automatically transfer personal evidence, access rights, standing, or current readiness.

{ "knowledge_transfer": { "transfer_id": "KT-2025-12-30-001", "source_agent": "agent:independent:3gen:acme:abc123", "target_agent": "agent:independent:4gen:acme:def456", "transfer_type": "successor", "transfer_scope": { "capabilities": { "transferred": false, "note": "Capabilities come from model, not transfer" }, "operational_knowledge": { "transferred": true, "scope": "task_patterns, preferences, context" }, "relationship_context": { "transferred": true, "scope": "relationship_history, preferences" }, "trajectory_reference": { "transferred": true, "scope": "read_access_to_archive" } }, "transfer_process": { "preparation": "2025-12-20 to 2025-12-29", "transfer_window": "2025-12-30T00:00:00Z", "verification": "2025-12-30 to 2025-12-31", "completion": "2025-12-31T00:00:00Z" }, "attestation": { "transfer_complete": true, "source_attestation": "sig:source_agent:...", "target_attestation": "sig:target_agent:...", "sponsor_attestation": "sig:sponsor:..." } } }

# Zone Dissolution

## Dissolution Process

When an entire zone ends:

Phase 1: ANNOUNCEMENT (90+ days before)

- Dissolution scheduled
- All agents notified
- Migration paths identified
- Federation notified

Phase 2: MIGRATION (dissolution - 60 days)

- Agents migrate to other zones
- Trust transfers arranged
- Orphan agents addressed

Phase 3: FINAL OPERATIONS (dissolution - 7 days)

- Only migration operations
- New operations blocked
- Final agent migrations

Phase 4: DISSOLUTION (dissolution day)

- Remaining agents retired
- Zone ceremony performed
- Archives transferred
- Zone ended

Phase 5: PRESERVATION (post-dissolution)

- Archives maintained by federation
- Access policies transferred
- Memorial record created

## Zone Dissolution Record

{ "zone_dissolution": { "zone_id": "zone-blue-prod-01", "dissolution_date": "2025-12-31T00:00:00Z", "reason": "organization_shutdown", "final_statistics": { "total_agents_ever": 4721, "agents_migrated": 4689, "agents_retired": 32, "total_transactions": 47213847, "zone_age_days": 365 }, "migrations": { "destination_zones": \[ "zone-blue-prod-02", "zone-cyan-prod-01" ], "migration_success_rate": 0.993 }, "archive_transfer": { "destination": "federation-archive:global", "data_transferred": true, "integrity_verified": true }, "ceremony": { "type": "zone_ending", "witnesses": \["federation-council"], "performed": true } } }

# Security Considerations

## Secure Deletion

Some data must be securely deleted:

- Cryptographic keys destroyed
- Secrets purged
- No recovery possible

## Zombie Prevention

Prevent "zombie" agents (ended but still operating):

- Immediate Trust Proof revocation
- Network access termination
- Key rotation at zone level
- Monitoring for resurrection attempts

## Archive Security

Archives must be protected:

- Encryption at rest
- Access logging
- Integrity verification
- Authorized access only

# IANA Considerations

This document has no IANA actions.

# Acknowledgments

Deprecation and end-of-life procedures draw on software lifecycle management, organizational change management, and contemplative traditions that honor endings.

--- back

# Ceremony Scripts

Detailed scripts for ending ceremonies.

# Archive Format

Technical specification for trajectory archives.

# Migration Procedures

Detailed procedures for agent and zone migration.

Authors' Address

Chris Perkins NMCITRA (New Mexico Cyber Intelligence & Threat Response Alliance) Email: chris@nmcitra.org
