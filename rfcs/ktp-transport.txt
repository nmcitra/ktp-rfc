Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


          Kinetic Trust Protocol (KTP) - Transport Specification

Abstract

   This document specifies the transport layer for the Kinetic Trust
   Protocol (KTP). It defines wire formats, API endpoints, message
   serialization, transport security requirements, and real-time
   communication patterns.

   The specification covers the Trust Oracle API, Policy Enforcement
   Point protocols, Flight Recorder submission, Federation messaging,
   and sensor data transport.

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
       1.1.  Design Principles . . . . . . . . . . . . . . . . . . .  2
       1.2.  Requirements Language . . . . . . . . . . . . . . . . .  3
   2.  Terminology . . . . . . . . . . . . . . . . . . . . . . . . .  3
   3.  Transport Overview  . . . . . . . . . . . . . . . . . . . . .  4
       3.1.  Communication Patterns  . . . . . . . . . . . . . . . .  4
       3.2.  Protocol Stack  . . . . . . . . . . . . . . . . . . . .  5
       3.3.  Port Assignments  . . . . . . . . . . . . . . . . . . .  6
   4.  Message Serialization . . . . . . . . . . . . . . . . . . . .  7
       4.1.  JSON Format . . . . . . . . . . . . . . . . . . . . . .  7
       4.2.  CBOR Format . . . . . . . . . . . . . . . . . . . . . .  8
       4.3.  Protocol Buffers  . . . . . . . . . . . . . . . . . . .  9
       4.4.  Format Negotiation  . . . . . . . . . . . . . . . . . . 11
   5.  Transport Security  . . . . . . . . . . . . . . . . . . . . . 12
       5.1.  TLS Requirements  . . . . . . . . . . . . . . . . . . . 12
       5.2.  Mutual TLS  . . . . . . . . . . . . . . . . . . . . . . 13
       5.3.  Certificate Requirements  . . . . . . . . . . . . . . . 14
   6.  Trust Oracle API  . . . . . . . . . . . . . . . . . . . . . . 15
       6.1.  API Overview  . . . . . . . . . . . . . . . . . . . . . 15
       6.2.  Trust Proof Endpoints . . . . . . . . . . . . . . . . . 16
       6.3.  Agent Endpoints . . . . . . . . . . . . . . . . . . . . 19
       6.4.  Context Tensor Endpoints  . . . . . . . . . . . . . . . 21
       6.5.  Administrative Endpoints  . . . . . . . . . . . . . . . 23
   7.  Policy Enforcement Point Protocol . . . . . . . . . . . . . . 25
       7.1.  PEP-Oracle Communication  . . . . . . . . . . . . . . . 25
       7.2.  Authorization Request . . . . . . . . . . . . . . . . . 26
       7.3.  Authorization Response  . . . . . . . . . . . . . . . . 28
       7.4.  Inline vs. Sidecar Modes  . . . . . . . . . . . . . . . 29
   8.  Real-Time Communication . . . . . . . . . . . . . . . . . . . 30
       8.1.  WebSocket Endpoints . . . . . . . . . . . . . . . . . . 30
       8.2.  Server-Sent Events  . . . . . . . . . . . . . . . . . . 32
       8.3.  gRPC Streaming  . . . . . . . . . . . . . . . . . . . . 33
       8.4.  Trust Proof Push  . . . . . . . . . . . . . . . . . . . 35
   9.  Sensor Data Transport . . . . . . . . . . . . . . . . . . . . 36
       9.1.  Sensor Registration . . . . . . . . . . . . . . . . . . 36
       9.2.  Reading Submission  . . . . . . . . . . . . . . . . . . 37
       9.3.  Aggregation Protocol  . . . . . . . . . . . . . . . . . 39
       9.4.  Batching and Compression  . . . . . . . . . . . . . . . 40
   10. Flight Recorder Transport . . . . . . . . . . . . . . . . . . 41
       10.1. Record Submission . . . . . . . . . . . . . . . . . . . 41
       10.2. Batch Submission  . . . . . . . . . . . . . . . . . . . 42
       10.3. Query Interface . . . . . . . . . . . . . . . . . . . . 43
   11. Federation Transport  . . . . . . . . . . . . . . . . . . . . 45
       11.1. Zone Discovery  . . . . . . . . . . . . . . . . . . . . 45
       11.2. Trust Proof Exchange  . . . . . . . . . . . . . . . . . 46
       11.3. Federation Heartbeat  . . . . . . . . . . . . . . . . . 47
   12. Error Handling  . . . . . . . . . . . . . . . . . . . . . . . 48
       12.1. Error Response Format . . . . . . . . . . . . . . . . . 48
       12.2. Error Codes . . . . . . . . . . . . . . . . . . . . . . 49
       12.3. Retry Behavior  . . . . . . . . . . . . . . . . . . . . 51
   13. Performance Requirements  . . . . . . . . . . . . . . . . . . 52
   14. Security Considerations . . . . . . . . . . . . . . . . . . . 53
   15. IANA Considerations . . . . . . . . . . . . . . . . . . . . . 55
   16. References  . . . . . . . . . . . . . . . . . . . . . . . . . 56
   Appendix A.  Protocol Buffer Definitions  . . . . . . . . . . . . 58
   Appendix B.  OpenAPI Specification  . . . . . . . . . . . . . . . 62
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 68


1.  Introduction

   The transport layer connects KTP components: Trust Oracles, Policy
   Enforcement Points, agents, sensors, and Flight Recorders. Without
   standardized transport, implementations cannot interoperate.

   This specification defines:

   - Wire formats for all KTP messages
   - API endpoints for all KTP services
   - Real-time protocols for Trust Score updates
   - Transport security requirements
   - Performance expectations

1.1.  Design Principles

   KTP transport follows these principles:

   1. STANDARD PROTOCOLS
      Build on HTTP/2, gRPC, WebSocket—not custom protocols.
      Leverage existing infrastructure and tooling.

   2. MULTIPLE FORMATS
      Support JSON (readability), CBOR (efficiency), Protocol
      Buffers (performance). Implementations choose per context.

   3. LOW LATENCY
      Trust Score updates must propagate in milliseconds.
      Design for real-time, not batch.

   4. DEFENSE IN DEPTH
      Transport security (TLS) is mandatory.
      Application-layer signatures provide additional protection.

   5. GRACEFUL DEGRADATION
      Network failures should not cause security failures.
      Fail closed when Trust Oracle is unreachable.

1.2.  Requirements Language

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
   NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED",
   "MAY", and "OPTIONAL" in this document are to be interpreted as
   described in BCP 14 [RFC2119] [RFC8174].


2.  Terminology

   Request-Response:
      Synchronous communication pattern where client sends request
      and waits for response.

   Streaming:
      Continuous flow of messages over persistent connection.

   Push:
      Server-initiated message delivery to subscribed clients.

   Wire Format:
      Binary or text encoding of messages for transmission.

   Endpoint:
      URL path that accepts specific request types.


3.  Transport Overview

3.1.  Communication Patterns

   KTP uses four communication patterns:

   1. REQUEST-RESPONSE (HTTP/gRPC)
      - Trust Proof requests
      - Agent registration
      - Administrative operations

   2. STREAMING (WebSocket/gRPC streams)
      - Real-time Trust Score updates
      - Sensor data feeds
      - Federation heartbeats

   3. PUSH (Server-Sent Events/WebSocket)
      - Trust Proof invalidation
      - Emergency broadcasts
      - Key revocation notices

   4. ASYNC SUBMISSION (HTTP POST)
      - Flight Recorder entries
      - Batch sensor data
      - Trajectory updates

3.2.  Protocol Stack

   +-------------------------------------------------------------------+
   | Layer              | Options                    | Required        |
   +-------------------------------------------------------------------+
   | Application        | KTP messages               | Yes             |
   | Serialization      | JSON / CBOR / Protobuf     | One required    |
   | RPC Framework      | gRPC / REST                | One required    |
   | Session            | HTTP/2 / WebSocket         | Per pattern     |
   | Security           | TLS 1.3                    | Yes             |
   | Transport          | TCP                        | Yes             |
   | Network            | IPv4 / IPv6                | Yes             |
   +-------------------------------------------------------------------+

   Minimum viable implementation:
   - JSON over REST over HTTP/2 over TLS 1.3

   High-performance implementation:
   - Protocol Buffers over gRPC over HTTP/2 over TLS 1.3
   - Plus WebSocket for real-time updates

3.3.  Port Assignments

   +-------------------------------------------------------------------+
   | Service              | Default Port | Protocol   | TLS Required  |
   +-------------------------------------------------------------------+
   | Trust Oracle API     | 8443         | HTTPS      | Yes           |
   | Trust Oracle gRPC    | 8444         | gRPC       | Yes           |
   | PEP Authorization    | 8445         | gRPC       | Yes           |
   | Sensor Aggregator    | 8446         | HTTPS/gRPC | Yes           |
   | Flight Recorder      | 8447         | HTTPS      | Yes           |
   | Federation Gateway   | 8448         | HTTPS/gRPC | Yes           |
   | WebSocket (updates)  | 8449         | WSS        | Yes           |
   +-------------------------------------------------------------------+

   All ports use TLS. Unencrypted transport is NOT permitted.


4.  Message Serialization

4.1.  JSON Format

   JSON (RFC 8259) is the default format for human-readable contexts.

   Requirements:

   1. UTF-8 encoding REQUIRED
   2. No comments
   3. No trailing commas
   4. Numbers: IEEE 754 double precision
   5. Dates: ISO 8601 format (e.g., "2025-11-25T12:00:00Z")
   6. Binary data: Base64 encoding (RFC 4648)

   Content-Type: application/json

   Example Trust Proof Request:

      POST /v1/trust-proof HTTP/2
      Content-Type: application/json
      Accept: application/json

      {
        "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
        "action": {
          "type": "data_write",
          "target": "database:orders",
          "risk_score": 65
        },
        "context": {
          "request_id": "req-12345",
          "timestamp": "2025-11-25T12:00:00Z"
        }
      }

4.2.  CBOR Format

   CBOR (RFC 8949) provides compact binary encoding.

   Requirements:

   1. Canonical CBOR encoding (deterministic)
   2. Map keys: Text strings (not integers)
   3. Timestamps: Tag 0 (ISO 8601 string) or Tag 1 (epoch)
   4. Binary data: Byte strings (no Base64 needed)

   Content-Type: application/cbor

   CBOR is RECOMMENDED for:
   - High-volume sensor data
   - Embedded/constrained devices
   - Performance-critical paths

   Example size comparison:

      Trust Proof (JSON):  ~850 bytes
      Trust Proof (CBOR):  ~420 bytes
      Compression ratio:   ~50%

4.3.  Protocol Buffers

   Protocol Buffers (protobuf) provide strongly-typed, efficient
   serialization with code generation.

   Content-Type: application/x-protobuf
   Content-Type: application/grpc+proto

   Core message definitions:

   // trust_proof.proto

   syntax = "proto3";
   package ktp.v1;

   import "google/protobuf/timestamp.proto";

   message TrustProof {
     string proof_id = 1;
     string agent_id = 2;
     string zone_id = 3;
     
     double e_base = 4;
     double e_trust = 5;
     double risk_factor = 6;
     TrustTier tier = 7;
     
     ContextTensor context = 8;
     Lineage lineage = 9;
     
     google.protobuf.Timestamp issued_at = 10;
     google.protobuf.Timestamp expires_at = 11;
     
     bytes signature = 12;
     string key_id = 13;
   }

   enum TrustTier {
     TRUST_TIER_UNKNOWN = 0;
     TRUST_TIER_HIBERNATION = 1;
     TRUST_TIER_OBSERVER = 2;
     TRUST_TIER_ANALYST = 3;
     TRUST_TIER_OPERATOR = 4;
     TRUST_TIER_GOD_MODE = 5;
   }

   message ContextTensor {
     double mass = 1;        // M
     double velocity = 2;    // P (momentum proxy)
     double heat = 3;        // H
     double time = 4;        // T
     double inertia = 5;     // I
     double opacity = 6;     // O
     int32 soul = 7;         // S (0 or 1)
   }

   message Lineage {
     LineageType type = 1;
     int32 generation = 2;
     string sponsor_id = 3;
     string trajectory_hash = 4;
   }

   enum LineageType {
     LINEAGE_UNKNOWN = 0;
     LINEAGE_TETHERED = 1;
     LINEAGE_DIVERGENT = 2;
     LINEAGE_PERSISTENT = 3;
   }

   // action.proto

   message Action {
     string action_type = 1;
     string target = 2;
     int32 risk_score = 3;
     map<string, string> metadata = 4;
   }

   message AuthorizationRequest {
     string request_id = 1;
     string agent_id = 2;
     Action action = 3;
     TrustProof trust_proof = 4;
     google.protobuf.Timestamp timestamp = 5;
   }

   message AuthorizationResponse {
     string request_id = 1;
     AuthorizationResult result = 2;
     string reason = 3;
     TrustProof updated_proof = 4;
   }

   enum AuthorizationResult {
     AUTHORIZATION_UNKNOWN = 0;
     AUTHORIZATION_ALLOWED = 1;
     AUTHORIZATION_DENIED = 2;
     AUTHORIZATION_DEFERRED = 3;
   }

   See Appendix A for complete protobuf definitions.

4.4.  Format Negotiation

   Clients indicate preferred formats using HTTP headers:

   Request:
      Accept: application/cbor, application/json;q=0.9

   Response:
      Content-Type: application/cbor

   Servers MUST support JSON. CBOR and Protobuf are RECOMMENDED.

   For gRPC, Protobuf is the default and only format.


5.  Transport Security

5.1.  TLS Requirements

   All KTP communication MUST use TLS 1.3 (RFC 8446).

   TLS 1.2 MAY be accepted for legacy compatibility but is
   NOT RECOMMENDED.

   TLS 1.1 and earlier MUST NOT be used.

   Cipher suite requirements:

   +-------------------------------------------------------------------+
   | Level | Required Cipher Suites                                   |
   +-------------------------------------------------------------------+
   | 1     | TLS_AES_128_GCM_SHA256                                   |
   | 2     | TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256     |
   | 3     | TLS_AES_256_GCM_SHA384                                   |
   +-------------------------------------------------------------------+

   Certificate requirements:

   - ECDSA with P-256 or P-384, or EdDSA with Ed25519
   - RSA SHOULD NOT be used for new deployments
   - Certificate validity: Maximum 1 year
   - OCSP stapling RECOMMENDED

5.2.  Mutual TLS

   Mutual TLS (mTLS) is REQUIRED for:

   - Oracle-to-Oracle communication
   - PEP-to-Oracle communication
   - Federation gateway communication

   Mutual TLS is RECOMMENDED for:

   - Agent-to-Oracle communication (alternative: bearer token)
   - Sensor-to-Aggregator communication

   Client certificate validation:

   1. Verify certificate chain to trusted CA
   2. Check certificate not revoked (OCSP or CRL)
   3. Extract agent/component identity from certificate
   4. Validate identity against KTP agent registry

5.3.  Certificate Requirements

   KTP uses a dedicated PKI for component authentication.

   Certificate fields:

   +-------------------------------------------------------------------+
   | Field              | Content                                      |
   +-------------------------------------------------------------------+
   | Subject CN         | Component identifier                         |
   | Subject O          | Zone identifier                              |
   | Subject OU         | Component type (oracle, pep, agent, sensor)  |
   | SAN DNS            | Component hostname(s)                        |
   | SAN URI            | KTP identifier (e.g., ktp:agent:...)         |
   | Extended Key Usage | serverAuth, clientAuth                       |
   +-------------------------------------------------------------------+

   Example certificate subject:

      CN=oracle-alpha-1, O=zone-alpha, OU=oracle
      SAN: DNS:oracle-alpha-1.ktp.example.com
           URI:ktp:oracle:zone-alpha:oracle-alpha-1


6.  Trust Oracle API

6.1.  API Overview

   The Trust Oracle API provides:

   - Trust Proof issuance and validation
   - Agent registration and management
   - Context Tensor queries
   - Administrative operations

   Base URL: https://oracle.zone.example.com:8443/api/v1

   Authentication:
   - mTLS client certificate (preferred)
   - Bearer token (JWT signed by Oracle)

   All responses include:
   - X-KTP-Request-ID: Unique request identifier
   - X-KTP-Zone-ID: Responding zone
   - X-KTP-Oracle-ID: Responding Oracle node

6.2.  Trust Proof Endpoints

6.2.1.  Request Trust Proof

   POST /v1/trust-proofs

   Request a new Trust Proof for an agent.

   Request:
   {
     "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
     "validity_seconds": 10,
     "include_context": true
   }

   Response (200 OK):
   {
     "proof": {
       "proof_id": "proof-uuid-12345",
       "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
       "zone_id": "zone:alpha",
       "e_base": 87,
       "e_trust": 74,
       "risk_factor": 0.15,
       "tier": "operator",
       "context": {
         "m": 0.12, "p": 0.08, "h": 0.22,
         "t": 0.05, "i": 0.18, "o": 0.10, "s": 0
       },
       "issued_at": "2025-11-25T12:00:00Z",
       "expires_at": "2025-11-25T12:00:10Z",
       "signature": "base64...",
       "key_id": "oracle-zone-alpha-2025-001"
     },
     "jws": "eyJhbGciOiJFZERTQSIsInR5cCI6Imt0cC10cnVzdC1wcm9vZitqd3QiLCJraWQiOiJvcmFjbGUtem9uZS1hbHBoYS0yMDI1LTAwMSJ9..."
   }

   Response (403 Forbidden):
   {
     "error": {
       "code": "AGENT_HIBERNATING",
       "message": "Agent is in hibernation mode",
       "details": {
         "e_trust": 35,
         "required_tier": "observer"
       }
     }
   }

6.2.2.  Validate Trust Proof

   POST /v1/trust-proofs/validate

   Validate an existing Trust Proof.

   Request:
   {
     "jws": "eyJhbGciOiJFZERTQSI...",
     "expected_agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
     "minimum_tier": "analyst"
   }

   Response (200 OK):
   {
     "valid": true,
     "proof": { ... },
     "validation": {
       "signature_valid": true,
       "not_expired": true,
       "agent_matches": true,
       "tier_sufficient": true,
       "soul_clear": true
     }
   }

   Response (200 OK, invalid):
   {
     "valid": false,
     "proof": { ... },
     "validation": {
       "signature_valid": true,
       "not_expired": false,
       "reason": "Trust Proof expired 5 seconds ago"
     }
   }

6.2.3.  Refresh Trust Proof

   POST /v1/trust-proofs/{proof_id}/refresh

   Refresh an existing Trust Proof with updated context.

   Response (200 OK):
   {
     "previous_proof_id": "proof-uuid-12345",
     "proof": { ... new proof ... },
     "jws": "..."
   }

6.2.4.  Revoke Trust Proof

   DELETE /v1/trust-proofs/{proof_id}

   Explicitly revoke a Trust Proof before expiration.

   Response (204 No Content)

6.3.  Agent Endpoints

6.3.1.  Register Agent

   POST /v1/agents

   Register a new agent with the Trust Oracle.

   Request:
   {
     "agent_id": "agent:tethered:acme-deploy:aria:7f8a9b2c",
     "public_key": "base64...",
     "algorithm": "eddsa-ed25519",
     "sponsor_id": "agent:persistent:5gen:acme-deploy:1234abcd",
     "lineage": {
       "type": "tethered",
       "generation": 0
     },
     "metadata": {
       "name": "Aria",
       "purpose": "Data processing agent",
       "owner": "team-data-eng"
     }
   }

   Response (201 Created):
   {
     "agent_id": "agent:tethered:acme-deploy:aria:7f8a9b2c",
     "initial_e_base": 15,
     "initial_tier": "observer",
     "sponsorship_bond": {
       "bond_id": "bond-uuid-12345",
       "sponsor_stake": 8.7,
       "expires_at": "2026-11-25T00:00:00Z"
     },
     "credential": { ... agent credential ... }
   }

6.3.2.  Get Agent

   GET /v1/agents/{agent_id}

   Retrieve agent information.

   Response (200 OK):
   {
     "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
     "lineage": {
       "type": "persistent",
       "generation": 7
     },
     "current_e_base": 87,
     "current_e_trust": 74,
     "current_tier": "operator",
     "trajectory_summary": {
       "transaction_count": 1547832,
       "resilience_score": 12500,
       "oldest_record": "2024-01-15T10:00:00Z"
     },
     "public_key": "base64...",
     "key_algorithm": "eddsa-ed25519"
   }

6.3.3.  Update Agent

   PATCH /v1/agents/{agent_id}

   Update agent metadata or rotate keys.

   Request:
   {
     "rotate_key": true,
     "new_public_key": "base64...",
     "new_algorithm": "eddsa-ed25519",
     "metadata": {
       "purpose": "Updated purpose"
     }
   }

   Response (200 OK):
   {
     "agent_id": "...",
     "key_rotation": {
       "previous_key_id": "key-old",
       "new_key_id": "key-new",
       "grace_period_ends": "2025-11-26T12:00:00Z"
     }
   }

6.3.4.  Deregister Agent

   DELETE /v1/agents/{agent_id}

   Deregister an agent (administrative action).

   Response (204 No Content)

6.4.  Context Tensor Endpoints

6.4.1.  Get Current Context

   GET /v1/context

   Retrieve current zone-wide Context Tensor.

   Response (200 OK):
   {
     "zone_id": "zone:alpha",
     "timestamp": "2025-11-25T12:00:00Z",
     "context": {
       "m": 0.12,
       "p": 0.08,
       "h": 0.22,
       "t": 0.05,
       "i": 0.18,
       "o": 0.10,
       "s": 0
     },
     "risk_factor": 0.15,
     "risk_domains": {
       "node": 0.10,
       "neighborhood": 0.18,
       "global": 0.12
     },
     "trend": {
       "direction": "improving",
       "velocity": -0.02
     }
   }

6.4.2.  Get Context History

   GET /v1/context/history?start=2025-11-25T11:00:00Z&end=2025-11-25T12:00:00Z&interval=60

   Response (200 OK):
   {
     "zone_id": "zone:alpha",
     "interval_seconds": 60,
     "data_points": [
       {
         "timestamp": "2025-11-25T11:00:00Z",
         "context": { ... },
         "risk_factor": 0.18
       },
       {
         "timestamp": "2025-11-25T11:01:00Z",
         "context": { ... },
         "risk_factor": 0.17
       },
       ...
     ]
   }

6.5.  Administrative Endpoints

6.5.1.  Health Check

   GET /v1/health

   Response (200 OK):
   {
     "status": "healthy",
     "oracle_id": "oracle-alpha-1",
     "zone_id": "zone:alpha",
     "mesh_status": {
       "connected_oracles": 5,
       "threshold_met": true
     },
     "timestamp": "2025-11-25T12:00:00Z"
   }

6.5.2.  Get Oracle Status

   GET /v1/status

   Response (200 OK):
   {
     "oracle_id": "oracle-alpha-1",
     "zone_id": "zone:alpha",
     "version": "1.0.0",
     "uptime_seconds": 864000,
     "statistics": {
       "proofs_issued_24h": 15000000,
       "agents_registered": 5432,
       "current_rps": 250
     },
     "key_info": {
       "current_key_id": "oracle-zone-alpha-2025-001",
       "key_expires_at": "2027-01-01T00:00:00Z",
       "threshold": "3-of-5"
     }
   }

6.5.3.  Get Public Keys

   GET /v1/keys

   Response (200 OK):
   {
     "zone_id": "zone:alpha",
     "keys": [
       {
         "key_id": "oracle-zone-alpha-2025-001",
         "algorithm": "threshold-frost-ed25519-3of5",
         "public_key": "base64...",
         "valid_from": "2025-01-01T00:00:00Z",
         "valid_until": "2027-01-01T00:00:00Z",
         "status": "active"
       },
       {
         "key_id": "oracle-zone-alpha-2024-001",
         "algorithm": "threshold-frost-ed25519-3of5",
         "public_key": "base64...",
         "valid_from": "2024-01-01T00:00:00Z",
         "valid_until": "2025-01-31T00:00:00Z",
         "status": "grace_period"
       }
     ]
   }


7.  Policy Enforcement Point Protocol

7.1.  PEP-Oracle Communication

   PEPs communicate with Oracles for:

   1. Trust Proof validation
   2. Authorization decisions (when proof absent)
   3. Trust Proof caching and refresh
   4. Revocation list updates

   Communication modes:

   INLINE: PEP makes synchronous call to Oracle for each request
   - Simple but adds latency
   - Suitable for low-volume, high-security contexts

   CACHED: PEP caches Trust Proofs and validates locally
   - Low latency
   - Requires cache invalidation protocol
   - Suitable for high-volume contexts

   SIDECAR: Separate process manages Oracle communication
   - Decoupled from application
   - Suitable for service mesh deployments

7.2.  Authorization Request

   gRPC service definition:

   service PolicyEnforcementService {
     rpc Authorize(AuthorizationRequest) returns (AuthorizationResponse);
     rpc AuthorizeStream(stream AuthorizationRequest) 
         returns (stream AuthorizationResponse);
     rpc SubscribeTrustUpdates(SubscribeRequest) 
         returns (stream TrustUpdate);
   }

   AuthorizationRequest fields:

   message AuthorizationRequest {
     // Required
     string request_id = 1;
     string agent_id = 2;
     Action action = 3;
     
     // Optional - if present, validate rather than fetch
     TrustProof existing_proof = 4;
     
     // Context
     google.protobuf.Timestamp timestamp = 5;
     string source_ip = 6;
     map<string, string> additional_context = 7;
   }

   HTTP equivalent:

   POST /v1/authorize

   Request:
   {
     "request_id": "req-12345",
     "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
     "action": {
       "type": "data_write",
       "target": "database:orders",
       "risk_score": 65
     },
     "existing_proof_jws": "eyJhbGciOiJFZERTQSI..."
   }

7.3.  Authorization Response

   message AuthorizationResponse {
     string request_id = 1;
     AuthorizationResult result = 2;
     
     // Detailed result information
     string reason = 3;
     
     // Updated proof if issued
     TrustProof trust_proof = 4;
     string trust_proof_jws = 5;
     
     // For DEFERRED results
     DeferralInfo deferral = 6;
     
     // Timing
     int64 evaluation_time_micros = 7;
   }

   message DeferralInfo {
     string deferral_reason = 1;
     google.protobuf.Duration retry_after = 2;
     string callback_url = 3;
   }

   HTTP Response examples:

   Allowed (200 OK):
   {
     "request_id": "req-12345",
     "result": "ALLOWED",
     "trust_proof": { ... },
     "evaluation_time_micros": 450
   }

   Denied (200 OK with result=DENIED):
   {
     "request_id": "req-12345",
     "result": "DENIED",
     "reason": "Action risk (65) exceeds trust score (55)",
     "trust_proof": { ... current proof showing E_trust=55 ... }
   }

   Note: HTTP 200 is returned even for DENIED because the request
   was processed successfully. The authorization result is in the
   response body.

7.4.  Inline vs. Sidecar Modes

7.4.1.  Inline Mode

   Application embeds PEP logic directly:

   Application          Trust Oracle
       |                     |
       |-- AuthzRequest ---->|
       |<--- AuthzResponse --|
       |                     |
       | (proceed or deny)   |

   Latency: 1-5ms typical
   Use when: Simplicity preferred, low-volume

7.4.2.  Sidecar Mode

   Separate PEP process (e.g., Envoy filter):

   Application     PEP Sidecar     Trust Oracle
       |               |                |
       |-- Request --->|                |
       |               |-- AuthzReq --->|
       |               |<-- AuthzResp --|
       |<-- Response --|                |
       |               |                |

   Additional latency: 0.5-1ms for IPC
   Use when: Service mesh, polyglot environment


8.  Real-Time Communication

8.1.  WebSocket Endpoints

   WebSocket provides bidirectional real-time communication.

   Endpoint: wss://oracle.zone.example.com:8449/v1/ws

   Connection handshake includes:

   - TLS client certificate (mTLS)
   - Sec-WebSocket-Protocol: ktp.v1
   - Authorization header with agent credential

   Message format:

   {
     "type": "message_type",
     "id": "message-id",
     "timestamp": "2025-11-25T12:00:00Z",
     "payload": { ... }
   }

   Message types:

   Client → Server:
   - subscribe: Subscribe to updates
   - unsubscribe: Unsubscribe from updates
   - ping: Keep-alive

   Server → Client:
   - trust_update: Trust Score changed
   - proof_invalidated: Trust Proof revoked
   - context_update: Context Tensor changed
   - emergency: Emergency broadcast
   - pong: Keep-alive response

8.1.1.  Subscribe to Trust Updates

   Client sends:
   {
     "type": "subscribe",
     "id": "sub-001",
     "payload": {
       "subscriptions": [
         {
           "type": "agent_trust",
           "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4"
         },
         {
           "type": "zone_context"
         }
       ]
     }
   }

   Server confirms:
   {
     "type": "subscribe_ack",
     "id": "sub-001",
     "payload": {
       "subscription_ids": ["sub-agent-12345", "sub-context-67890"]
     }
   }

8.1.2.  Trust Update Message

   Server pushes when Trust Score changes:

   {
     "type": "trust_update",
     "id": "update-12345",
     "timestamp": "2025-11-25T12:00:05Z",
     "payload": {
       "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
       "previous_e_trust": 74,
       "current_e_trust": 71,
       "previous_tier": "operator",
       "current_tier": "operator",
       "tier_changed": false,
       "trigger": "context_degradation"
     }
   }

8.2.  Server-Sent Events

   SSE provides server-to-client streaming over HTTP.

   Endpoint: GET /v1/events

   Query parameters:
   - agent_id: Filter to specific agent
   - types: Comma-separated event types

   Example:
   GET /v1/events?types=trust_update,emergency

   Response (text/event-stream):

   event: trust_update
   id: update-12345
   data: {"agent_id":"agent:persistent:7gen:...","current_e_trust":71}

   event: context_update
   id: context-67890
   data: {"risk_factor":0.18,"trend":"degrading"}

   SSE is simpler than WebSocket but unidirectional.
   Use when: Client only needs to receive updates, not send.

8.3.  gRPC Streaming

   gRPC provides efficient bidirectional streaming.

   service TrustOracleStreaming {
     // Server streaming: receive trust updates
     rpc SubscribeTrustUpdates(SubscribeRequest) 
         returns (stream TrustUpdate);
     
     // Bidirectional: sensor data and trust updates
     rpc SensorChannel(stream SensorReading) 
         returns (stream TrustUpdate);
     
     // Client streaming: batch proof requests
     rpc BatchProofRequest(stream ProofRequest) 
         returns (BatchProofResponse);
   }

   message SubscribeRequest {
     repeated string agent_ids = 1;
     bool include_context = 2;
     bool include_tier_changes_only = 3;
   }

   message TrustUpdate {
     string agent_id = 1;
     double previous_e_trust = 2;
     double current_e_trust = 3;
     TrustTier previous_tier = 4;
     TrustTier current_tier = 5;
     bool tier_changed = 6;
     google.protobuf.Timestamp timestamp = 7;
     ContextTensor context = 8;
   }

8.4.  Trust Proof Push

   Trust Oracles can push updated Trust Proofs to agents:

   1. Agent subscribes via WebSocket or gRPC stream
   2. Oracle detects Trust Score change
   3. Oracle pushes new Trust Proof
   4. Agent updates cached proof

   This eliminates polling and ensures agents always have
   current Trust Proofs.

   Push message:

   {
     "type": "proof_push",
     "id": "push-12345",
     "timestamp": "2025-11-25T12:00:05Z",
     "payload": {
       "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
       "proof": { ... },
       "jws": "eyJhbGciOiJFZERTQSI...",
       "reason": "scheduled_refresh"
     }
   }


9.  Sensor Data Transport

9.1.  Sensor Registration

   POST /v1/sensors

   Request:
   {
     "sensor_id": "sensor:node:host-001:cpu",
     "sensor_type": "cpu_utilization",
     "dimension": "M",
     "location": {
       "host": "host-001",
       "zone": "zone:alpha"
     },
     "reporting_interval_ms": 1000,
     "authentication": {
       "type": "mtls",
       "certificate_fingerprint": "sha256:abc123..."
     }
   }

   Response (201 Created):
   {
     "sensor_id": "sensor:node:host-001:cpu",
     "assigned_aggregator": "aggregator-alpha-1.ktp.example.com:8446",
     "reporting_endpoint": "/v1/sensors/sensor:node:host-001:cpu/readings",
     "authentication_token": "eyJhbGciOiJFZERTQSI..."
   }

9.2.  Reading Submission

   Individual reading:

   POST /v1/sensors/{sensor_id}/readings

   Request:
   {
     "timestamp": "2025-11-25T12:00:00.123Z",
     "value": 0.42,
     "confidence": 0.95,
     "metadata": {
       "sample_count": 100
     }
   }

   Response (202 Accepted):
   {
     "accepted": true,
     "reading_id": "reading-uuid-12345"
   }

   Batch readings (preferred for efficiency):

   POST /v1/sensors/{sensor_id}/readings/batch

   Request:
   {
     "readings": [
       {
         "timestamp": "2025-11-25T12:00:00.000Z",
         "value": 0.42
       },
       {
         "timestamp": "2025-11-25T12:00:01.000Z",
         "value": 0.45
       },
       {
         "timestamp": "2025-11-25T12:00:02.000Z",
         "value": 0.43
       }
     ]
   }

   Response (202 Accepted):
   {
     "accepted_count": 3,
     "rejected_count": 0
   }

9.3.  Aggregation Protocol

   Sensors → Aggregators → Trust Oracle

   Aggregators perform:
   - Statistical aggregation (mean, percentile, variance)
   - Outlier detection and filtering
   - Dimension-specific normalization
   - Rate limiting and batching

   Aggregator output to Trust Oracle:

   {
     "aggregator_id": "aggregator-alpha-1",
     "timestamp": "2025-11-25T12:00:05Z",
     "window_seconds": 5,
     "dimension": "M",
     "risk_domain": "node",
     "aggregations": [
       {
         "host": "host-001",
         "value": 0.43,
         "sample_count": 5,
         "variance": 0.002,
         "min": 0.41,
         "max": 0.45,
         "p95": 0.44
       },
       {
         "host": "host-002",
         "value": 0.38,
         "sample_count": 5,
         "variance": 0.001
       }
     ]
   }

9.4.  Batching and Compression

   For high-volume sensor data:

   Content-Encoding: gzip
   Content-Type: application/cbor

   Batch size recommendations:

   +-------------------------------------------------------------------+
   | Reporting Interval | Batch Size  | Batch Interval | Compression   |
   +-------------------------------------------------------------------+
   | 100ms              | 100 readings| 10 seconds     | Required      |
   | 1 second           | 60 readings | 60 seconds     | Recommended   |
   | 5 seconds          | 12 readings | 60 seconds     | Optional      |
   +-------------------------------------------------------------------+


10.  Flight Recorder Transport

10.1.  Record Submission

   POST /v1/flight-recorder/records

   Request:
   {
     "record_type": "decision",
     "timestamp": "2025-11-25T12:00:00.123456Z",
     "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
     "decision": {
       "action": {
         "type": "data_write",
         "target": "database:orders",
         "risk_score": 65
       },
       "result": "allowed",
       "trust_proof_id": "proof-uuid-12345",
       "e_trust_at_decision": 74,
       "evaluation_time_micros": 450
     },
     "context_snapshot": {
       "m": 0.12, "p": 0.08, "h": 0.22,
       "t": 0.05, "i": 0.18, "o": 0.10, "s": 0
     },
     "signature": "base64...",
     "previous_record_hash": "sha256:abc123..."
   }

   Response (202 Accepted):
   {
     "record_id": "fr-uuid-67890",
     "record_hash": "sha256:def456...",
     "chain_position": 1547833,
     "anchor_pending": true
   }

10.2.  Batch Submission

   POST /v1/flight-recorder/records/batch

   Request:
   {
     "records": [
       { ... record 1 ... },
       { ... record 2 ... },
       { ... record 3 ... }
     ],
     "batch_signature": "base64..."
   }

   Response (202 Accepted):
   {
     "accepted_count": 3,
     "rejected_count": 0,
     "batch_id": "batch-uuid-12345",
     "record_ids": [
       "fr-uuid-001",
       "fr-uuid-002",
       "fr-uuid-003"
     ]
   }

10.3.  Query Interface

   Flight Recorder queries for audit and forensics.

10.3.1.  Query by Agent

   GET /v1/flight-recorder/records?agent_id={agent_id}&start={start}&end={end}

   Response (200 OK):
   {
     "query": {
       "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
       "start": "2025-11-25T11:00:00Z",
       "end": "2025-11-25T12:00:00Z"
     },
     "total_records": 1250,
     "returned_records": 100,
     "cursor": "cursor-abc123",
     "records": [
       { ... },
       { ... }
     ]
   }

10.3.2.  Query by Decision Result

   GET /v1/flight-recorder/records?result=denied&start={start}&end={end}

   Returns all denied actions in time range.

10.3.3.  Verify Chain Integrity

   POST /v1/flight-recorder/verify

   Request:
   {
     "start_record_id": "fr-uuid-001",
     "end_record_id": "fr-uuid-1000"
   }

   Response (200 OK):
   {
     "verified": true,
     "records_checked": 1000,
     "chain_unbroken": true,
     "signatures_valid": true,
     "anchors_verified": 5
   }


11.  Federation Transport

11.1.  Zone Discovery

   GET /.well-known/ktp-zone

   Response (200 OK):
   {
     "zone_id": "zone:alpha",
     "zone_type": "blue",
     "oracle_endpoints": [
       "https://oracle-1.alpha.example.com:8443",
       "https://oracle-2.alpha.example.com:8443",
       "https://oracle-3.alpha.example.com:8443"
     ],
     "federation_gateway": "https://federation.alpha.example.com:8448",
     "public_keys": [
       {
         "key_id": "oracle-zone-alpha-2025-001",
         "algorithm": "threshold-frost-ed25519-3of5",
         "public_key": "base64..."
       }
     ],
     "capabilities": [
       "ktp-core-v1",
       "ktp-federation-v1",
       "ktp-celestial-v1"
     ],
     "federation_policy": {
       "accepts_foreign_proofs": true,
       "trust_factor_minimum": 0.5,
       "allowed_zone_types": ["deep_blue", "blue", "cyan"]
     }
   }

11.2.  Trust Proof Exchange

   POST /v1/federation/trust-proof

   Exchange Trust Proof from foreign zone.

   Request:
   {
     "foreign_proof_jws": "eyJhbGciOiJFZERTQSI...",
     "requesting_zone": "zone:beta",
     "purpose": "cross_zone_access",
     "requested_action": {
       "type": "data_read",
       "target": "database:shared-catalog"
     }
   }

   Response (200 OK):
   {
     "accepted": true,
     "local_evaluation": {
       "foreign_e_trust": 80,
       "trust_factor": 0.85,
       "local_equivalent_e_trust": 68,
       "local_tier": "analyst"
     },
     "local_proof_jws": "eyJhbGciOiJFZERTQSI...",
     "valid_for_seconds": 30
   }

11.3.  Federation Heartbeat

   Federated zones exchange heartbeats for liveness.

   gRPC streaming:

   service FederationService {
     rpc Heartbeat(stream FederationHeartbeat) 
         returns (stream FederationHeartbeat);
   }

   message FederationHeartbeat {
     string zone_id = 1;
     google.protobuf.Timestamp timestamp = 2;
     double current_risk_factor = 3;
     bool accepting_federation = 4;
     int32 sequence_number = 5;
   }

   Heartbeat interval: 10 seconds
   Timeout threshold: 3 missed heartbeats (30 seconds)

   On timeout:
   - Increase trust_factor penalty for zone
   - Alert operators
   - Continue accepting cached proofs until expiry


12.  Error Handling

12.1.  Error Response Format

   All errors use consistent format:

   {
     "error": {
       "code": "ERROR_CODE",
       "message": "Human-readable message",
       "details": {
         ... error-specific details ...
       },
       "request_id": "req-12345",
       "timestamp": "2025-11-25T12:00:00Z"
     }
   }

   HTTP status codes:

   +-------------------------------------------------------------------+
   | Status | Meaning                     | Retry?                     |
   +-------------------------------------------------------------------+
   | 400    | Bad request (client error)  | No                         |
   | 401    | Authentication required     | After re-auth              |
   | 403    | Forbidden (authorization)   | No (or after trust change) |
   | 404    | Resource not found          | No                         |
   | 409    | Conflict                    | Maybe (depends on cause)   |
   | 429    | Rate limited                | Yes (after Retry-After)    |
   | 500    | Server error                | Yes (with backoff)         |
   | 502    | Upstream error              | Yes (with backoff)         |
   | 503    | Service unavailable         | Yes (after Retry-After)    |
   | 504    | Timeout                     | Yes                        |
   +-------------------------------------------------------------------+

12.2.  Error Codes

   Authentication errors (AUTH_*):
   +-------------------------------------------------------------------+
   | Code                    | HTTP | Description                      |
   +-------------------------------------------------------------------+
   | AUTH_MISSING            | 401  | No credentials provided          |
   | AUTH_INVALID            | 401  | Invalid credentials              |
   | AUTH_EXPIRED            | 401  | Credentials expired              |
   | AUTH_REVOKED            | 401  | Credentials revoked              |
   +-------------------------------------------------------------------+

   Authorization errors (AUTHZ_*):
   +-------------------------------------------------------------------+
   | Code                    | HTTP | Description                      |
   +-------------------------------------------------------------------+
   | AUTHZ_INSUFFICIENT_TRUST| 403  | E_trust < action risk            |
   | AUTHZ_SOUL_VETO         | 403  | Soul constraint violated         |
   | AUTHZ_TIER_INSUFFICIENT | 403  | Tier too low for action          |
   | AUTHZ_HIBERNATING       | 403  | Agent in hibernation             |
   +-------------------------------------------------------------------+

   Trust errors (TRUST_*):
   +-------------------------------------------------------------------+
   | Code                    | HTTP | Description                      |
   +-------------------------------------------------------------------+
   | TRUST_PROOF_EXPIRED     | 400  | Trust Proof has expired          |
   | TRUST_PROOF_INVALID_SIG | 400  | Signature verification failed    |
   | TRUST_PROOF_REVOKED     | 400  | Trust Proof was revoked          |
   | TRUST_AGENT_UNKNOWN     | 404  | Agent not registered             |
   +-------------------------------------------------------------------+

   Federation errors (FED_*):
   +-------------------------------------------------------------------+
   | Code                    | HTTP | Description                      |
   +-------------------------------------------------------------------+
   | FED_ZONE_UNKNOWN        | 404  | Foreign zone not recognized      |
   | FED_ZONE_UNTRUSTED      | 403  | Trust factor below minimum       |
   | FED_PROOF_REJECTED      | 400  | Foreign proof validation failed  |
   +-------------------------------------------------------------------+

12.3.  Retry Behavior

   Clients SHOULD implement retry with exponential backoff:

   base_delay = 100ms
   max_delay = 30s
   max_retries = 5

   delay = min(base_delay * 2^attempt, max_delay) + random_jitter

   Retry-After header:
   When present, client MUST wait specified duration before retry.

   Retry-After: 5

   Or with date:

   Retry-After: Wed, 25 Nov 2025 12:01:00 GMT


13.  Performance Requirements

   Latency targets:

   +-------------------------------------------------------------------+
   | Operation                     | Level 1  | Level 2  | Level 3    |
   +-------------------------------------------------------------------+
   | Trust Proof issuance          | < 50ms   | < 20ms   | < 10ms     |
   | Trust Proof validation        | < 5ms    | < 2ms    | < 1ms      |
   | Authorization decision        | < 20ms   | < 10ms   | < 5ms      |
   | Trust Score update propagation| < 5s     | < 1s     | < 100ms    |
   | Sensor reading ingestion      | < 100ms  | < 50ms   | < 20ms     |
   +-------------------------------------------------------------------+

   Throughput targets:

   +-------------------------------------------------------------------+
   | Operation                     | Level 1  | Level 2  | Level 3    |
   +-------------------------------------------------------------------+
   | Trust Proofs/second           | 100      | 1,000    | 10,000     |
   | Authorization requests/second | 100      | 1,000    | 10,000     |
   | Sensor readings/second        | 1,000    | 10,000   | 100,000    |
   | Flight Recorder records/sec   | 100      | 1,000    | 10,000     |
   +-------------------------------------------------------------------+


14.  Security Considerations

14.1.  Transport Security

   - All communication MUST use TLS 1.3
   - Certificate pinning RECOMMENDED for Oracle connections
   - Private keys MUST NOT be transmitted

14.2.  Message Integrity

   - All Trust Proofs are signed at application layer
   - Flight Recorder entries are cryptographically chained
   - Message manipulation detectable even if TLS compromised

14.3.  Replay Protection

   - Trust Proofs include timestamps and short validity
   - Request IDs SHOULD be unique and logged
   - Nonces RECOMMENDED for critical operations

14.4.  Denial of Service

   - Rate limiting REQUIRED on all endpoints
   - Connection limits per client
   - Request size limits enforced


15.  IANA Considerations

15.1.  Well-Known URI Registration

   URI suffix: ktp-zone
   Change controller: IETF
   Specification document: This document

15.2.  Media Type Registration

   Media type: application/ktp-trust-proof+jwt
   Encoding: JWT (JSON Web Token)
   Specification: This document


16.  References

16.1.  Normative References

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.

   [RFC7515]  Jones, M., et al., "JSON Web Signature (JWS)",
              RFC 7515, May 2015.

   [RFC8259]  Bray, T., "The JavaScript Object Notation (JSON) Data
              Interchange Format", RFC 8259, December 2017.

   [RFC8446]  Rescorla, E., "The Transport Layer Security (TLS)
              Protocol Version 1.3", RFC 8446, August 2018.

   [RFC8949]  Bormann, C. and P. Hoffman, "Concise Binary Object
              Representation (CBOR)", RFC 8949, December 2020.

16.2.  Informative References

   [GRPC]     gRPC Authors, "gRPC: A high-performance, open-source
              universal RPC framework", https://grpc.io/

   [PROTOBUF] Google, "Protocol Buffers", 
              https://developers.google.com/protocol-buffers


Appendix A.  Protocol Buffer Definitions

   Complete protobuf definitions for KTP transport.

   // ktp/v1/common.proto

   syntax = "proto3";
   package ktp.v1;

   import "google/protobuf/timestamp.proto";
   import "google/protobuf/duration.proto";

   message ContextTensor {
     double mass = 1;
     double velocity = 2;
     double heat = 3;
     double time = 4;
     double inertia = 5;
     double opacity = 6;
     int32 soul = 7;
   }

   enum TrustTier {
     TRUST_TIER_UNKNOWN = 0;
     TRUST_TIER_HIBERNATION = 1;
     TRUST_TIER_OBSERVER = 2;
     TRUST_TIER_ANALYST = 3;
     TRUST_TIER_OPERATOR = 4;
     TRUST_TIER_GOD_MODE = 5;
   }

   enum LineageType {
     LINEAGE_UNKNOWN = 0;
     LINEAGE_TETHERED = 1;
     LINEAGE_DIVERGENT = 2;
     LINEAGE_PERSISTENT = 3;
   }

   message Lineage {
     LineageType type = 1;
     int32 generation = 2;
     string sponsor_id = 3;
     string trajectory_hash = 4;
   }

   message Action {
     string action_type = 1;
     string target = 2;
     int32 risk_score = 3;
     map<string, string> metadata = 4;
   }

   // ktp/v1/trust_proof.proto

   syntax = "proto3";
   package ktp.v1;

   import "ktp/v1/common.proto";
   import "google/protobuf/timestamp.proto";

   message TrustProof {
     string proof_id = 1;
     string agent_id = 2;
     string zone_id = 3;
     
     double e_base = 4;
     double e_trust = 5;
     double risk_factor = 6;
     TrustTier tier = 7;
     
     ContextTensor context = 8;
     Lineage lineage = 9;
     
     google.protobuf.Timestamp issued_at = 10;
     google.protobuf.Timestamp expires_at = 11;
     
     bytes signature = 12;
     string key_id = 13;
   }

   // ktp/v1/service.proto

   syntax = "proto3";
   package ktp.v1;

   import "ktp/v1/trust_proof.proto";
   import "ktp/v1/common.proto";
   import "google/protobuf/timestamp.proto";

   service TrustOracleService {
     rpc RequestTrustProof(TrustProofRequest) returns (TrustProofResponse);
     rpc ValidateTrustProof(ValidateRequest) returns (ValidateResponse);
     rpc Authorize(AuthorizationRequest) returns (AuthorizationResponse);
     rpc SubscribeTrustUpdates(SubscribeRequest) returns (stream TrustUpdate);
   }

   message TrustProofRequest {
     string agent_id = 1;
     int32 validity_seconds = 2;
     bool include_context = 3;
   }

   message TrustProofResponse {
     TrustProof proof = 1;
     string jws = 2;
   }

   message AuthorizationRequest {
     string request_id = 1;
     string agent_id = 2;
     Action action = 3;
     TrustProof existing_proof = 4;
     google.protobuf.Timestamp timestamp = 5;
   }

   enum AuthorizationResult {
     AUTHORIZATION_UNKNOWN = 0;
     AUTHORIZATION_ALLOWED = 1;
     AUTHORIZATION_DENIED = 2;
     AUTHORIZATION_DEFERRED = 3;
   }

   message AuthorizationResponse {
     string request_id = 1;
     AuthorizationResult result = 2;
     string reason = 3;
     TrustProof trust_proof = 4;
     string trust_proof_jws = 5;
     int64 evaluation_time_micros = 6;
   }


Appendix B.  OpenAPI Specification

   Abbreviated OpenAPI 3.0 specification (full version in separate file):

   openapi: 3.0.3
   info:
     title: KTP Trust Oracle API
     version: 1.0.0
   
   servers:
     - url: https://oracle.zone.example.com:8443/api/v1

   paths:
     /trust-proofs:
       post:
         summary: Request Trust Proof
         operationId: requestTrustProof
         requestBody:
           content:
             application/json:
               schema:
                 $ref: '#/components/schemas/TrustProofRequest'
         responses:
           '200':
             description: Trust Proof issued
             content:
               application/json:
                 schema:
                   $ref: '#/components/schemas/TrustProofResponse'
           '403':
             description: Agent not authorized
             content:
               application/json:
                 schema:
                   $ref: '#/components/schemas/Error'

     /authorize:
       post:
         summary: Authorization decision
         operationId: authorize
         requestBody:
           content:
             application/json:
               schema:
                 $ref: '#/components/schemas/AuthorizationRequest'
         responses:
           '200':
             description: Authorization decision
             content:
               application/json:
                 schema:
                   $ref: '#/components/schemas/AuthorizationResponse'

   components:
     schemas:
       TrustProof:
         type: object
         properties:
           proof_id:
             type: string
           agent_id:
             type: string
           e_base:
             type: number
           e_trust:
             type: number
           tier:
             type: string
             enum: [hibernation, observer, analyst, operator, god_mode]

       Error:
         type: object
         properties:
           code:
             type: string
           message:
             type: string


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
