---
title: "Kinetic Trust Protocol - Legacy Integration Specification"
abbrev: "KTP-LEGACY"
docname: draft-perkins-ktp-legacy-00
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
  RFC6749:
  RFC7519:
  RFC8705:

informative:
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  SAML:
    title: "Security Assertion Markup Language (SAML) V2.0"
    author:
      - org: OASIS
    date: 2005-03

--- abstract

This document specifies integration between the Kinetic Trust Protocol
(KTP) and legacy authentication/authorization systems including OAuth
2.0, OpenID Connect, SAML 2.0, mTLS, and API keys. The specification
covers bidirectional bridging, trust mapping, credential translation,
migration paths from legacy to KTP-native operation, and hybrid
deployment patterns.

--- middle

# Introduction

KTP does not exist in isolation. The world runs on OAuth, SAML, mTLS,
API keys, and countless other authentication and authorization
systems. For KTP to be adopted, it must integrate with—not replace—
existing infrastructure.

This specification addresses:

- How legacy credentials map to KTP trust
- How KTP agents interact with legacy systems
- How legacy clients interact with KTP zones
- Migration paths from legacy to KTP-native
- Hybrid deployments during transition

## Design Principles

Legacy integration embodies these principles:

1. **Coexistence**: KTP and legacy systems operate simultaneously.
   Neither requires abandoning the other.

2. **Graceful Mapping**: Trust concepts translate between systems
   with appropriate discounting and constraints.

3. **No False Precision**: Legacy systems provide less information
   than KTP. Mappings acknowledge this uncertainty.

4. **Migration Support**: Organizations can migrate incrementally
   from legacy to KTP-native over time.

5. **Security Preservation**: Integration does not weaken either
   system's security properties.

## Requirements Language

{::boilerplate bcp14-tagged}

# Terminology

Bridge
: A component that translates between KTP and legacy protocols.

Credential Translation
: Converting legacy credentials to KTP Trust Proofs or vice versa.

Hybrid Agent
: An agent that can operate in both KTP and legacy contexts.

Legacy System
: Any authentication/authorization system predating KTP.

Migration Path
: A defined sequence for transitioning from legacy to KTP-native.

Trust Mapping
: Correspondence between legacy trust concepts and KTP E_base.

# Trust Mapping Framework

## The Mapping Problem

Legacy systems and KTP use different trust models:

| System | Trust Model |
|--------|-------------|
| OAuth 2.0 | Scopes granted by resource owner |
| SAML | Assertions from identity provider |
| mTLS | Certificate validity and chain |
| API Keys | Secret possession |
| KTP | Trajectory-based earned trust |

These models are fundamentally different. Mapping is approximate.

## Mapping Principles

1. **Conservative Translation**: When uncertain, assume lower trust.

2. **Explicit Uncertainty**: Mapped trust carries uncertainty markers.

3. **No Trust Amplification**: Mapping cannot increase trust beyond
   what the source system provides.

4. **Decay Over Time**: Mapped trust decays if not refreshed from
   source.

## Trust Equivalence Table

Base mapping from legacy to KTP E_base:

| Legacy Mechanism | Max E_base | Rationale |
|-----------------|------------|-----------|
| API Key (basic) | 15 | Secret possession only |
| API Key (rotated) | 20 | Some operational hygiene |
| OAuth token (public client) | 20 | User consent but weak client |
| OAuth token (confidential) | 30 | Client authenticated |
| OAuth + PKCE | 35 | Stronger binding |
| mTLS (self-signed) | 25 | Cryptographic but unverified |
| mTLS (public CA) | 35 | Third-party verification |
| mTLS (private CA) | 40 | Organizational control |
| SAML assertion | 35 | IdP-backed identity |
| SAML + MFA | 45 | Stronger authentication |
| FIDO2/WebAuthn | 50 | Hardware-backed |

## E_base Modifiers

Mapped E_base is adjusted by context:

| Factor | Modifier | Condition |
|--------|----------|-----------|
| Known issuer | +5 | Token issuer in trusted list |
| Short-lived token | +5 | Expiration < 1 hour |
| IP binding | +5 | Token bound to source IP |
| Device binding | +10 | Token bound to device |
| Fresh authentication | +5 | Auth within 5 minutes |
| Stale authentication | -10 | Auth > 24 hours ago |
| First use | -10 | Never seen this identity |
| Repeated use | +5 | Consistent behavior history |

## Uncertainty Markers

Mapped trust includes uncertainty:

~~~json
{
  "trust_mapping": {
    "source_system": "oauth2",
    "source_credential": "bearer_token",
    "mapped_e_base": 30,
    "uncertainty": {
      "level": "moderate",
      "reasons": [
        "no_trajectory_history",
        "no_behavioral_data",
        "point_in_time_auth"
      ]
    },
    "constraints": {
      "max_action_risk": 25,
      "trajectory_start": "fresh",
      "monitoring": "enhanced"
    }
  }
}
~~~

# OAuth 2.0 Integration

## OAuth to KTP Bridge

~~~
+----------------+     +------------------+     +----------------+
|  OAuth Client  |---->|  OAuth-KTP       |---->|   KTP Zone     |
|                |     |  Bridge          |     |                |
+----------------+     +------------------+     +----------------+
                              |
                              v
                       Token validation
                       Scope mapping
                       Trust translation
                       Trust Proof issuance
~~~

## Token Validation

The bridge validates OAuth tokens:

1. Verify token signature (if JWT) or introspect
2. Check expiration
3. Verify issuer against allowed list
4. Extract scopes and claims
5. Check for revocation

## Scope to Tier Mapping

OAuth scopes map to KTP capability tiers:

~~~json
{
  "scope_mapping": {
    "read": {
      "tier": "observer",
      "max_action_risk": 10
    },
    "write": {
      "tier": "participant",
      "max_action_risk": 25
    },
    "admin": {
      "tier": "analyst",
      "max_action_risk": 40
    },
    "superadmin": {
      "tier": "operator",
      "max_action_risk": 60,
      "requires_additional_verification": true
    }
  }
}
~~~

## KTP to OAuth Bridge

KTP agents accessing OAuth-protected resources:

~~~
+----------------+     +------------------+     +----------------+
|   KTP Agent    |---->|  KTP-OAuth       |---->| OAuth Resource |
|                |     |  Bridge          |     |                |
+----------------+     +------------------+     +----------------+
                              |
                              v
                       Trust Proof validation
                       E_base to scope mapping
                       Token request (client credentials)
                       Token caching
~~~

## E_base to Scope Mapping

~~~json
{
  "e_base_to_scope": {
    "ranges": [
      {"e_min": 0, "e_max": 20, "scopes": ["read"]},
      {"e_min": 21, "e_max": 40, "scopes": ["read", "write"]},
      {"e_min": 41, "e_max": 60, "scopes": ["read", "write", "admin"]},
      {"e_min": 61, "e_max": 100, "scopes": ["read", "write", "admin", "superadmin"]}
    ]
  }
}
~~~

# OpenID Connect Integration

## OIDC Claims to KTP Identity

OIDC provides richer identity than OAuth:

~~~json
{
  "oidc_mapping": {
    "sub": "→ agent sponsor identity",
    "email": "→ contact for sponsor",
    "email_verified": "→ +5 E_base if true",
    "name": "→ display name",
    "preferred_username": "→ agent identifier hint",
    "acr": "→ authentication strength modifier",
    "amr": "→ authentication method modifier",
    "auth_time": "→ freshness calculation"
  }
}
~~~

## ACR/AMR to E_base Modifiers

Authentication Context Class Reference (acr) values:

| ACR Value | E_base Modifier |
|-----------|-----------------|
| urn:mace:incommon:iap:bronze | +0 |
| urn:mace:incommon:iap:silver | +5 |
| urn:mace:incommon:iap:gold | +10 |
| urn:oasis:names:tc:SAML:2.0:ac:classes:Password | +0 |
| urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport | +5 |
| urn:oasis:names:tc:SAML:2.0:ac:classes:MultiFactor | +15 |

Authentication Method Reference (amr) values:

| AMR Value | E_base Modifier |
|-----------|-----------------|
| pwd | +0 |
| otp | +5 |
| sms | +3 |
| hwk | +15 |
| swk | +10 |
| bio | +10 |
| mfa | +10 |

## Sponsor Identity from OIDC

Human sponsors can authenticate via OIDC:

~~~json
{
  "sponsor_from_oidc": {
    "oidc_provider": "https://idp.example.com",
    "subject": "user@example.com",
    "verified_claims": ["email", "name"],
    "ial_equivalent": "IAL2",
    "sponsor_e_base": 75,
    "sponsored_agents_max": 10
  }
}
~~~

# SAML 2.0 Integration

## SAML to KTP Bridge

~~~
+----------------+     +------------------+     +----------------+
|  SAML Service  |---->|  SAML-KTP        |---->|   KTP Zone     |
|  Provider      |     |  Bridge          |     |                |
+----------------+     +------------------+     +----------------+
                              |
                              v
                       Assertion validation
                       Attribute mapping
                       Trust translation
                       Trust Proof issuance
~~~

## Assertion Processing

The bridge processes SAML assertions:

1. Validate assertion signature
2. Verify issuer (IdP) against trusted list
3. Check conditions (NotBefore, NotOnOrAfter, AudienceRestriction)
4. Extract attributes
5. Map to KTP identity and trust

## Attribute Mapping

~~~json
{
  "saml_attribute_mapping": {
    "urn:oid:0.9.2342.19200300.100.1.3": {
      "name": "email",
      "ktp_use": "sponsor_contact"
    },
    "urn:oid:2.5.4.42": {
      "name": "givenName",
      "ktp_use": "display"
    },
    "urn:oid:2.5.4.4": {
      "name": "surname",
      "ktp_use": "display"
    },
    "urn:oid:1.3.6.1.4.1.5923.1.1.1.7": {
      "name": "eduPersonEntitlement",
      "ktp_use": "capability_hint"
    },
    "urn:mace:dir:attribute-def:eduPersonAssurance": {
      "name": "assurance",
      "ktp_use": "e_base_modifier"
    }
  }
}
~~~

## Entitlement to Capability Mapping

SAML entitlements map to KTP capabilities:

~~~json
{
  "entitlement_mapping": {
    "urn:example:ktp:tier:observer": {
      "tier": "observer",
      "max_e_base": 30
    },
    "urn:example:ktp:tier:participant": {
      "tier": "participant",
      "max_e_base": 45
    },
    "urn:example:ktp:tier:analyst": {
      "tier": "analyst",
      "max_e_base": 60
    },
    "urn:example:ktp:tier:operator": {
      "tier": "operator",
      "max_e_base": 75
    }
  }
}
~~~

# mTLS Integration

## Certificate to Trust Mapping

mTLS provides cryptographic identity:

~~~json
{
  "mtls_trust_mapping": {
    "certificate_attributes": {
      "subject_dn": "→ agent identifier",
      "issuer_dn": "→ trust anchor",
      "serial_number": "→ credential reference",
      "not_before": "→ credential start",
      "not_after": "→ credential expiration",
      "key_usage": "→ capability constraints",
      "san": "→ alternative identities"
    },
    "trust_factors": {
      "ca_type": {
        "self_signed": 25,
        "public_ca": 35,
        "private_ca": 40,
        "qualified_ca": 50
      },
      "key_strength": {
        "rsa_2048": 0,
        "rsa_4096": 5,
        "ec_p256": 5,
        "ec_p384": 10
      },
      "validity_period": {
        "under_1_year": 5,
        "1_to_3_years": 0,
        "over_3_years": -5
      }
    }
  }
}
~~~

## Certificate Chain Validation

The bridge validates certificate chains:

1. Build chain to trusted anchor
2. Check each certificate's validity period
3. Verify signatures up the chain
4. Check revocation (CRL/OCSP)
5. Validate key usage and constraints
6. Map trust based on chain quality

## Hardware Key Attestation

Hardware-backed keys increase trust:

~~~json
{
  "hardware_attestation": {
    "attestation_type": "TPM",
    "tpm_version": "2.0",
    "key_in_tpm": true,
    "key_non_exportable": true,
    "e_base_bonus": 15
  }
}
~~~

# API Key Integration

## API Key Limitations

API keys provide minimal trust signals:

- No identity binding (shared secrets)
- No behavior history
- No expiration (typically)
- No scope (typically)
- Easily leaked

## API Key to Trust Mapping

~~~json
{
  "api_key_mapping": {
    "base_e": 15,
    "modifiers": {
      "rotated_regularly": {
        "condition": "rotation_period < 90 days",
        "modifier": 5
      },
      "ip_restricted": {
        "condition": "ip_whitelist defined",
        "modifier": 5
      },
      "rate_limited": {
        "condition": "rate_limit < 1000/hour",
        "modifier": 3
      },
      "audited": {
        "condition": "usage_logging enabled",
        "modifier": 2
      }
    },
    "max_e_base": 30,
    "constraints": {
      "trajectory_start": "fresh",
      "monitoring": "enhanced",
      "max_action_risk": 20
    }
  }
}
~~~

## API Key to Agent Binding

API keys can be bound to KTP agents:

~~~json
{
  "api_key_binding": {
    "api_key_id": "key_abc123",
    "bound_agent": "agent:tethered:1gen:acme:xyz789",
    "binding_type": "exclusive",
    "created_at": "2025-12-01T00:00:00Z",
    "created_by": "sponsor:alice.smith",
    "restrictions": {
      "source_ips": ["10.0.0.0/8"],
      "allowed_actions": ["read", "write"],
      "max_rate": 100
    }
  }
}
~~~

# Hybrid Agents

## Definition

Hybrid agents operate in both KTP and legacy contexts:

- Have KTP identity and trajectory
- Can present legacy credentials when needed
- Translate trust bidirectionally
- Accumulate trajectory from all contexts

## Hybrid Agent Architecture

~~~
+-------------------------------------------------------------------+
|                        HYBRID AGENT                               |
|                                                                   |
|  +------------------+     +------------------+                    |
|  |  KTP Identity    |     | Legacy Credentials|                   |
|  |  - Agent ID      |     | - OAuth tokens    |                   |
|  |  - Trajectory    |     | - SAML assertions |                   |
|  |  - Trust Proof   |     | - mTLS certs      |                   |
|  +------------------+     +------------------+                    |
|           |                       |                               |
|           v                       v                               |
|  +-----------------------------------------------+                |
|  |            Credential Manager                 |                |
|  |  - Context detection                          |                |
|  |  - Credential selection                       |                |
|  |  - Trust translation                          |                |
|  +-----------------------------------------------+                |
|           |                       |                               |
|           v                       v                               |
|  +------------------+     +------------------+                    |
|  |   KTP Context    |     | Legacy Context   |                    |
|  |   Operations     |     | Operations       |                    |
|  +------------------+     +------------------+                    |
|                                                                   |
+-------------------------------------------------------------------+
~~~

## Context Detection

The agent detects which context applies:

~~~json
{
  "context_detection": {
    "ktp_indicators": [
      "endpoint_in_zone_registry",
      "ktp_protocol_headers",
      "trust_proof_request"
    ],
    "legacy_indicators": [
      "oauth_token_required",
      "saml_sp_metadata",
      "mtls_client_auth",
      "api_key_header"
    ],
    "default_context": "ktp",
    "fallback_behavior": "attempt_ktp_then_legacy"
  }
}
~~~

## Trajectory Accumulation

All actions contribute to trajectory:

~~~json
{
  "hybrid_trajectory": {
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "trajectory_sources": [
      {
        "source": "ktp_native",
        "transactions": 4721,
        "weight": 1.0
      },
      {
        "source": "oauth_bridge",
        "transactions": 1247,
        "weight": 0.8
      },
      {
        "source": "saml_bridge",
        "transactions": 89,
        "weight": 0.8
      },
      {
        "source": "mtls_bridge",
        "transactions": 2103,
        "weight": 0.9
      }
    ],
    "composite_trajectory_length": 7632
  }
}
~~~

# Migration Paths

## Migration Stages

~~~
Stage 0: LEGACY ONLY
  - All operations use legacy auth
  - No KTP infrastructure
  - Baseline for migration

Stage 1: BRIDGE DEPLOYMENT
  - Legacy-KTP bridges deployed
  - Legacy clients continue unchanged
  - KTP zone operational in shadow

Stage 2: HYBRID OPERATION
  - Some clients use KTP-native
  - Some clients use bridges
  - Both paths fully supported

Stage 3: KTP PRIMARY
  - Most clients KTP-native
  - Bridges for legacy holdouts
  - Legacy deprecation announced

Stage 4: KTP ONLY
  - All clients KTP-native
  - Bridges removed
  - Legacy decommissioned
~~~

## Migration Timeline

Recommended migration pace:

| Stage | Duration | Milestone |
|-------|----------|-----------|
| 0 → 1 | 2-4 weeks | Bridges operational |
| 1 → 2 | 4-8 weeks | 20% KTP-native |
| 2 → 3 | 3-6 months | 80% KTP-native |
| 3 → 4 | 3-6 months | 100% KTP-native |

## Migration Checklist

Pre-migration:
- [ ] KTP zone deployed and tested
- [ ] Bridges deployed and tested
- [ ] Trust mappings configured
- [ ] Fallback procedures documented

During migration:
- [ ] Traffic monitored at bridges
- [ ] Trust mapping accuracy verified
- [ ] Agent trajectories accumulating
- [ ] Issues logged and addressed

Post-migration:
- [ ] All clients KTP-native
- [ ] Bridges decommissioned
- [ ] Legacy systems decommissioned
- [ ] Documentation updated

## Trust Carryover

Trajectory earned via bridges carries over:

~~~json
{
  "migration_carryover": {
    "agent_id": "agent:divergent:3gen:acme:abc123",
    "pre_migration_trajectory": {
      "source": "oauth_bridge",
      "transactions": 5000,
      "e_base_earned": 35
    },
    "carryover_factor": 0.7,
    "post_migration_e_base": 24.5,
    "carryover_attestation": "signed_by_bridge_and_zone"
  }
}
~~~

# Bridge Deployment Patterns

## Sidecar Pattern

Bridge runs alongside application:

~~~
+-----------------------------------+
|           Application Pod         |
|  +-------------+  +-------------+ |
|  | Application |  |   Bridge    | |
|  |             |<>|             | |
|  +-------------+  +-------------+ |
+-----------------------------------+
~~~

## Gateway Pattern

Bridge at API gateway:

~~~
                    +---------------+
                    |   API Gateway |
                    |   + Bridge    |
                    +---------------+
                          |
        +--------+--------+--------+
        |        |        |        |
        v        v        v        v
    +------+ +------+ +------+ +------+
    | Svc1 | | Svc2 | | Svc3 | | Svc4 |
    +------+ +------+ +------+ +------+
~~~

## Service Mesh Pattern

Bridge integrated with service mesh:

~~~
+-----------------------------------+
|        Service Mesh Control       |
|        + KTP Bridge Control       |
+-----------------------------------+
              |
    +---------+---------+
    |         |         |
    v         v         v
+-------+ +-------+ +-------+
| Envoy | | Envoy | | Envoy |
|+Bridge| |+Bridge| |+Bridge|
+-------+ +-------+ +-------+
    |         |         |
    v         v         v
+-------+ +-------+ +-------+
| Svc A | | Svc B | | Svc C |
+-------+ +-------+ +-------+
~~~

# Security Considerations

## Bridge Security

Bridges are high-value targets:

- Bridges MUST run in secure environments
- Bridge credentials MUST be protected
- Bridge operations MUST be logged
- Bridge compromise affects all translations

## Trust Mapping Attacks

Attackers may try to exploit mappings:

- Claim inflation: claiming higher legacy trust than warranted
- Scope smuggling: gaining capabilities not in original token
- Replay attacks: reusing translated credentials

Mitigations:
- Conservative translation
- Short credential lifetimes
- Binding to context (IP, device)
- Continuous validation

## Migration Security

During migration, both systems are attack surface:

- Maintain security on both systems
- Monitor for migration-related anomalies
- Test fallback procedures
- Plan for rollback if needed

# IANA Considerations

This document has no IANA actions.

--- back

# Appendix A: Protocol-Specific Bridge Configurations

Detailed configuration for each legacy protocol.

# Appendix B: Trust Mapping Calibration

Guidance for tuning trust mappings to organizational context.

# Appendix C: Migration Runbooks

Step-by-step procedures for migration stages.

# Acknowledgments

Legacy integration design draws on production experience with
OAuth, SAML, mTLS, and identity federation systems.
