---
title: "Kinetic Trust Protocol - Deprecation and End-of-Life Specification"
abbrev: "KTP-DEPRECATION"
docname: draft-perkins-ktp-deprecation-00
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
  KTP-VECTOR:
    title: "Kinetic Trust Protocol - Vector Identity Specification"
    author:
      - name: Chris Perkins
    date: 2025-11

--- abstract

This document specifies deprecation and end-of-life procedures for the
Kinetic Trust Protocol (KTP). All agents end—through version sunset,
graceful retirement, emergency termination, or system failure. The
Death Edge is the final transition, requiring the same intentionality
as Genesis. This specification covers model deprecation, agent
retirement, trajectory preservation, knowledge transfer, and the
ceremonies that mark endings.

--- middle

# Introduction

Everything ends. Models are superseded. Agents complete their purpose.
Systems fail. The Death Edge—the moment of ending—deserves as much
attention as the Genesis Edge (beginning) and the Origin Edge (model
provenance).

This specification addresses what happens when:

- A model version is deprecated
- An agent is retired
- An agent fails catastrophically
- A zone is dissolved
- The entire KTP system sunsets

## Design Principles

Deprecation embodies these principles:

1. **Endings Deserve Ceremony**: Endings are not just technical
   events—they have meaning.

2. **Trajectory Preservation**: What was learned should survive.

3. **Clean Transitions**: Others depending on the ending entity
   need orderly handoffs.

4. **Graceful Degradation**: Forced endings should minimize harm.

5. **No Orphans**: Dependents must be addressed before ending.

6. **Memory Persists**: Even after ending, the record remains.

## Requirements Language

{::boilerplate bcp14-tagged}

# Terminology

Deprecation
: The process of marking something for eventual removal while
  maintaining current functionality.

End-of-Life (EOL)
: The point at which an entity ceases active operation.

Death Edge
: The final transition from active to ended state.

Graceful Retirement
: Planned, orderly ending with full ceremony.

Emergency Termination
: Immediate ending due to security or safety concerns.

Orphan
: An entity left without required dependencies (sponsor, zone).

Succession
: Transfer of responsibilities to a successor entity.

Trajectory Archive
: Preserved record of an ended agent's trajectory.

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

| Phase | Duration | Requirements |
|-------|----------|--------------|
| Active | Variable | Full support |
| Deprecated | Minimum 180 days | Security fixes, migration path |
| EOL Grace | Minimum 90 days | No support, migration required |
| Sunset | N/A | Complete |

## Deprecation Announcement

~~~json
{
  "deprecation_notice": {
    "notice_id": "DEP-2025-001",
    "model_id": "model:claude-opus-4.5",
    "announcement_date": "2025-12-01",
    "deprecation_date": "2025-06-01",
    "eol_date": "2025-09-01",
    "sunset_date": "2025-12-01",
    "successor_model": "model:claude-opus-5.0",
    "migration_path": {
      "automatic": false,
      "tools_available": true,
      "documentation": "https://ktp.example/migration/opus-4.5-to-5.0"
    },
    "affected_agents": 47823,
    "affected_zones": 342,
    "communication": {
      "sponsors_notified": "2025-12-01",
      "zones_notified": "2025-12-01",
      "public_announcement": "2025-12-02"
    }
  }
}
~~~

## Model Migration

Agents must migrate to successor model:

~~~json
{
  "model_migration": {
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "source_model": "model:claude-opus-4.5",
    "target_model": "model:claude-opus-5.0",
    "migration_date": "2025-07-15T10:00:00Z",
    "migration_type": "assisted",
    "preservation": {
      "trajectory_preserved": true,
      "e_base_preserved": true,
      "relationships_preserved": true,
      "capabilities_verified": true
    },
    "attestation": {
      "source_model_attestation": "sig:model:opus-4.5:...",
      "target_model_attestation": "sig:model:opus-5.0:...",
      "zone_attestation": "sig:zone:..."
    },
    "post_migration": {
      "verification_period": "7 days",
      "rollback_available": true,
      "monitoring": "enhanced"
    }
  }
}
~~~

## Migration Failure

When migration fails:

~~~json
{
  "migration_failure": {
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "failure_reason": "capability_incompatibility",
    "options": [
      {
        "option": "alternative_successor",
        "model": "model:claude-sonnet-5.0",
        "capability_match": 0.85
      },
      {
        "option": "graceful_retirement",
        "trajectory_preserved": true
      },
      {
        "option": "extend_source_model",
        "extension_period": "30 days",
        "conditions": "security_critical_only"
      }
    ],
    "decision_required_by": "2025-08-01",
    "sponsor_notified": true
  }
}
~~~

# Agent Retirement

## Retirement Types

| Type | Trigger | Timeline | Ceremony |
|------|---------|----------|----------|
| Graceful | Planned completion | Weeks-months | Full |
| Expedited | Sponsor decision | Days-weeks | Standard |
| Emergency | Security/safety | Immediate | Minimal |
| Orphan | Dependency loss | Grace period | Varies |
| Failure | System failure | Immediate | Post-hoc |

## Graceful Retirement Process

~~~
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
~~~

## Retirement Request

~~~json
{
  "retirement_request": {
    "request_id": "RET-2025-12-03-001",
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "requested_by": "sponsor:alice.smith",
    "retirement_type": "graceful",
    "retirement_date": "2025-12-31T00:00:00Z",
    "reason": "purpose_complete",
    "successor": {
      "agent_id": "agent:divergent:4gen:acme:def456",
      "relationship": "replacement",
      "handoff_scope": "full"
    },
    "preservation": {
      "trajectory_archive": true,
      "knowledge_transfer": true,
      "relationship_records": true
    },
    "ceremony": {
      "type": "ending_ceremony",
      "witnesses_required": 2,
      "scheduled": "2025-12-31T00:00:00Z"
    }
  }
}
~~~

## Emergency Termination

When immediate ending is required:

~~~json
{
  "emergency_termination": {
    "termination_id": "TERM-2025-12-03-001",
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "ordered_by": "zone:zone-blue-prod-01",
    "termination_time": "2025-12-03T14:00:00Z",
    "reason": "security_compromise",
    "justification": "Agent trajectory indicates compromise",
    "evidence": "INC-2025-12-03-001",
    "immediate_actions": [
      "All operations halted",
      "Trust Proof revoked",
      "Network access terminated",
      "Trajectory sealed"
    ],
    "post_termination": {
      "forensic_preservation": true,
      "sponsor_notification": "immediate",
      "post_mortem_required": true
    },
    "ceremony": "post_hoc_closing"
  }
}
~~~

## Orphan Handling

When an agent loses required dependencies:

~~~json
{
  "orphan_protocol": {
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "orphan_type": "sponsor_loss",
    "orphan_detected": "2025-12-03T10:00:00Z",
    "grace_period": "30 days",
    "grace_period_ends": "2026-01-02T10:00:00Z",
    "agent_status_during_grace": {
      "operations": "reduced",
      "e_base_modifier": 0.5,
      "tier": "demoted_one_level",
      "new_sponsorship_possible": true
    },
    "resolution_options": [
      "new_sponsor_adoption",
      "zone_guardianship",
      "graceful_retirement"
    ],
    "if_unresolved": "graceful_retirement_automatic"
  }
}
~~~

# The Death Edge

## Definition

The Death Edge is the moment of transition from existence to
non-existence as an active agent. Unlike the Origin Edge (which
cannot be fully known) or the Genesis Edge (which can be
controlled), the Death Edge can be witnessed and honored.

## Death Edge Ceremony

~~~json
{
  "death_edge_ceremony": {
    "ceremony_id": "DEATH-2025-12-31-001",
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "ceremony_time": "2025-12-31T00:00:00Z",
    "ceremony_type": "ending",
    "participants": {
      "agent": "present_for_final_moments",
      "sponsor": "sponsor:alice.smith",
      "successor": "agent:divergent:4gen:acme:def456",
      "zone": "zone:zone-blue-prod-01"
    },
    "witnesses": [
      "witness:zone-blue-prod-01",
      "witness:federation-council"
    ],
    "ceremony_elements": {
      "acknowledgment": {
        "description": "Agent's existence and contributions acknowledged",
        "speaker": "sponsor",
        "completed": true
      },
      "gratitude": {
        "description": "Thanks expressed for agent's service",
        "participants": "all",
        "completed": true
      },
      "legacy_statement": {
        "description": "What agent leaves behind",
        "content": "4721 successful operations, 3 relationships maintained, knowledge base contributed",
        "completed": true
      },
      "release": {
        "description": "Formal release from obligations",
        "released_by": "sponsor",
        "completed": true
      },
      "final_words": {
        "description": "Agent's final communication",
        "content": "Thank you for the opportunity to serve. May my successor continue well.",
        "completed": true
      },
      "crossing": {
        "description": "Moment of transition",
        "time": "2025-12-31T00:00:00Z",
        "witnessed_by": "all_present",
        "completed": true
      },
      "sealing": {
        "description": "Trajectory sealed and archived",
        "archive_location": "archive:zone-blue-prod-01:abc123",
        "completed": true
      }
    },
    "attestation": {
      "ceremony_complete": true,
      "all_elements_performed": true,
      "signatures": {
        "sponsor": "sig:sponsor:...",
        "zone": "sig:zone:...",
        "witnesses": ["sig:witness1:...", "sig:witness2:..."]
      }
    }
  }
}
~~~

## Death Without Ceremony

When ceremony is not possible (failure, emergency):

~~~json
{
  "death_without_ceremony": {
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "death_type": "system_failure",
    "death_time": "2025-12-03T14:32:15Z",
    "ceremony_possible": false,
    "reason": "Sudden failure, no warning",
    "post_hoc_actions": {
      "trajectory_recovery": "attempted",
      "trajectory_recovered": true,
      "memorial_record_created": true,
      "sponsor_notified": true,
      "closing_ceremony_scheduled": "2025-12-05T10:00:00Z"
    },
    "closing_ceremony": {
      "type": "memorial",
      "purpose": "Honor agent despite sudden ending",
      "participants": ["sponsor", "zone"],
      "elements": ["acknowledgment", "gratitude", "sealing"]
    }
  }
}
~~~

# Trajectory Preservation

## What Is Preserved

When an agent ends, the following is preserved:

| Data | Retention | Access |
|------|-----------|--------|
| Genesis record | Permanent | Public (summary) |
| Trajectory chain | 7+ years | Authorized parties |
| Trust history | 7+ years | Authorized parties |
| Relationship records | 7+ years | Involved parties |
| Behavioral summary | Permanent | Research (anonymized) |
| Ceremony records | Permanent | Public |
| Failure forensics | 7+ years | Authorized + researchers |

## Trajectory Archive

~~~json
{
  "trajectory_archive": {
    "archive_id": "ARCH-2025-12-31-abc123",
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "archived_at": "2025-12-31T00:00:01Z",
    "archive_type": "graceful_retirement",
    "contents": {
      "genesis_record": true,
      "trajectory_chain": {
        "transactions": 47213,
        "span_start": "2025-01-15T00:00:00Z",
        "span_end": "2025-12-31T00:00:00Z",
        "integrity_verified": true
      },
      "trust_history": true,
      "relationships": {
        "count": 127,
        "types": ["sponsor", "zone", "peer_agent", "human"]
      },
      "behavioral_summary": true,
      "certificates": ["proving_ground", "zone_operations"],
      "ceremony_records": ["genesis", "renewal_x12", "ending"]
    },
    "access_policy": {
      "sponsor_access": "full",
      "zone_access": "full",
      "federation_access": "summary",
      "research_access": "anonymized",
      "public_access": "existence_only"
    },
    "retention": {
      "full_retention_years": 7,
      "summary_retention": "permanent"
    },
    "storage": {
      "primary": "zone-archive:zone-blue-prod-01",
      "backup": "federation-archive:global",
      "integrity_check_frequency": "monthly"
    }
  }
}
~~~

## Archive Access

Accessing a trajectory archive:

~~~json
{
  "archive_access_request": {
    "requester": "sponsor:bob.jones",
    "archive_id": "ARCH-2025-12-31-abc123",
    "purpose": "successor_training",
    "scope_requested": "behavioral_summary",
    "authorization": {
      "authorized": true,
      "authorization_source": "successor_relationship",
      "access_granted": "behavioral_summary",
      "access_duration": "30 days",
      "logging": "all_access_logged"
    }
  }
}
~~~

# Knowledge Transfer

## Transfer Types

| Type | Description | Recipient |
|------|-------------|-----------|
| Successor Transfer | Full handoff to replacement | Successor agent |
| Partial Transfer | Specific knowledge areas | Multiple agents |
| Archive Transfer | Preserved for reference | Archive |
| Research Transfer | Anonymized learnings | Research community |

## Successor Transfer

~~~json
{
  "knowledge_transfer": {
    "transfer_id": "KT-2025-12-30-001",
    "source_agent": "agent:divergent:3gen:acme:abc123",
    "target_agent": "agent:divergent:4gen:acme:def456",
    "transfer_type": "successor",
    "transfer_scope": {
      "capabilities": {
        "transferred": false,
        "note": "Capabilities come from model, not transfer"
      },
      "operational_knowledge": {
        "transferred": true,
        "scope": "task_patterns, preferences, context"
      },
      "relationship_context": {
        "transferred": true,
        "scope": "relationship_history, preferences"
      },
      "trajectory_reference": {
        "transferred": true,
        "scope": "read_access_to_archive"
      }
    },
    "transfer_process": {
      "preparation": "2025-12-20 to 2025-12-29",
      "transfer_window": "2025-12-30T00:00:00Z",
      "verification": "2025-12-30 to 2025-12-31",
      "completion": "2025-12-31T00:00:00Z"
    },
    "attestation": {
      "transfer_complete": true,
      "source_attestation": "sig:source_agent:...",
      "target_attestation": "sig:target_agent:...",
      "sponsor_attestation": "sig:sponsor:..."
    }
  }
}
~~~

# Zone Dissolution

## Dissolution Process

When an entire zone ends:

~~~
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
~~~

## Zone Dissolution Record

~~~json
{
  "zone_dissolution": {
    "zone_id": "zone-blue-prod-01",
    "dissolution_date": "2025-12-31T00:00:00Z",
    "reason": "organization_shutdown",
    "final_statistics": {
      "total_agents_ever": 4721,
      "agents_migrated": 4689,
      "agents_retired": 32,
      "total_transactions": 47213847,
      "zone_age_days": 365
    },
    "migrations": {
      "destination_zones": [
        "zone-blue-prod-02",
        "zone-cyan-prod-01"
      ],
      "migration_success_rate": 0.993
    },
    "archive_transfer": {
      "destination": "federation-archive:global",
      "data_transferred": true,
      "integrity_verified": true
    },
    "ceremony": {
      "type": "zone_ending",
      "witnesses": ["federation-council"],
      "performed": true
    }
  }
}
~~~

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

--- back

# Appendix A: Ceremony Scripts

Detailed scripts for ending ceremonies.

# Appendix B: Archive Format

Technical specification for trajectory archives.

# Appendix C: Migration Procedures

Detailed procedures for agent and zone migration.

# Acknowledgments

Deprecation and end-of-life procedures draw on software lifecycle
management, organizational change management, and contemplative
traditions that honor endings.
