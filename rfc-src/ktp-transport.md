---
title: "Kinetic Trust Protocol (KTP) - Transport Specification"
abbrev: "KTP-TRANSPORT"
date: 2026-10-12
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  RFC2119:
  RFC7515:
  RFC8259:
  RFC8446:
  RFC8949:
  KTP-AUDIT:
    title: "Kinetic Trust Protocol - Flight Recorder"
    author:
      - name: Chris Perkins
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
  KTP-SENSORS:
    title: "Kinetic Trust Protocol - Context Signal Sensor Specification"
    author:
      - name: Chris Perkins
  RFC8174:
informative:
  GRPC:
    title: "gRPC: A high-performance, open-source universal RPC framework"
    author:
      - name: Chris Perkins
  PROTOBUF:
    title: "Protocol Buffers"
    author:
      - name: Chris Perkins

--- abstract

This document specifies the transport layer for the Kinetic Trust Protocol (KTP). It defines wire formats, API endpoints, message serialization, transport security requirements, and real-time communication patterns.

The specification covers the Trust Oracle API, Policy Enforcement Point protocols, Flight Recorder submission, Federation messaging, and sensor data transport.

--- middle

# Introduction

The transport layer connects KTP components: Trust Oracles, Policy Enforcement Points, agents, sensors, and Flight Recorders. Without standardized transport, implementations cannot interoperate.

This specification defines:

- Wire formats for all KTP messages
- API endpoints for all KTP services
- Real-time protocols for Trust Score updates
- Transport security requirements
- Performance expectations

## Design Principles

KTP transport follows these principles:

1. STANDARD PROTOCOLS Build on HTTP/2, gRPC, WebSocket—not custom protocols. Leverage existing infrastructure and tooling.

1. CANONICAL BASE Native v3 uses JSON and exact signed JWS artifacts. Alternative encodings require a separately published, versioned interoperability profile; an implementation preference cannot select a different semantic model.

1. LOW LATENCY Trust Score updates must propagate in milliseconds. Design for real-time, not batch.

1. DEFENSE IN DEPTH Transport security (TLS) is mandatory. Application-layer signatures provide additional protection.

1. GRACEFUL DEGRADATION Network failures should not cause security failures. Fail closed when Trust Oracle is unreachable.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}}.

# Terminology

Request-Response: Synchronous communication pattern where client sends request and waits for response.

Streaming: Continuous flow of messages over persistent connection.

Push: Server-initiated message delivery to subscribed clients.

Wire Format: Binary or text encoding of messages for transmission.

Endpoint: URL path that accepts specific request types.

# Transport Overview

## Communication Patterns

KTP uses four communication patterns:

1. REQUEST-RESPONSE (HTTP/gRPC) -  Trust Proof requests -  Agent registration -  Administrative operations

1. STREAMING (WebSocket/gRPC streams) -  Real-time Trust Score updates -  Sensor data feeds -  Federation heartbeats

1. PUSH (Server-Sent Events/WebSocket) -  Trust Proof invalidation -  Emergency broadcasts -  Key revocation notices

1. ASYNC SUBMISSION (HTTP POST) -  Flight Recorder entries -  Batch sensor data -  Trajectory updates

## Protocol Stack

~~~
+---------------+------------------------+--------------+
| Layer         | Options                | Required     |
+---------------+------------------------+--------------+
| Application   | KTP messages           | Yes          |
| Serialization | JSON / exact JWS       | Required     |
| API binding   | HTTP JSON/JWS base     | Required     |
| Session       | HTTP/2 / WebSocket     | Per pattern  |
| Security      | TLS 1.3                | Yes          |
| Transport     | TCP                    | Yes          |
| Network       | IPv4 / IPv6            | Yes          |
+---------------+------------------------+--------------+
~~~

Minimum viable implementation:

- JSON over REST over HTTP/2 over TLS 1.3

Alternative performance encodings and streaming bindings are not substitutes
for the base profile. Their use for native artifacts requires the separately
published profiles described in specifications/native-transport.md.

## Port Assignments

~~~
+---------------------+--------------+------------+--------------+
| Service             | Default Port | Protocol   | TLS Required |
+---------------------+--------------+------------+--------------+
| Trust Oracle API    | 8443         | HTTPS      | Yes          |
| Trust Oracle gRPC   | 8444         | gRPC       | Yes          |
| PEP Authorization   | 8445         | gRPC       | Yes          |
| Sensor Aggregator   | 8446         | HTTPS/gRPC | Yes          |
| Flight Recorder     | 8447         | HTTPS      | Yes          |
| Federation Gateway  | 8448         | HTTPS/gRPC | Yes          |
| WebSocket (updates) | 8449         | WSS        | Yes          |
+---------------------+--------------+------------+--------------+
~~~

All ports use TLS. Unencrypted transport is NOT permitted. The gRPC entries
are historical port conventions, not native-v3 message profiles or requirements
to implement a protobuf service. A port number does not negotiate an encoding.

# Message Serialization

Native v3 MUST support the proposed `ktp-json-jws-v1` base profile in
[Native JSON/JWS Transport](../specifications/native-transport.md). Its `v1`
versions this transport profile, not KTP semantics or an HTTP API. The installed
immutable KTP release identifies the owning artifact contracts. All base
requests and results MUST satisfy those contracts and the matching schemas;
Transport does not define parallel copies of their fields.

Trust Proofs remain exact signed compact JWS bytes. A decoded map, translated
message or re-encoded payload MUST NOT replace them. Ordinary requests and
associations follow request-binding.md; portable evaluation and its signed
boundary carrier follow decision-geometry.md. HTTP status, content negotiation,
a transport label and a valid proof alone never supply execution permission.

The v2.1 protobuf, abbreviated OpenAPI, flat proof and authorization enum are
legacy only. Their definitions remain at the immutable release and in the
migration references, not as native-v3 examples in this specification.

## JSON Format

JSON (RFC 8259) is the required base format for JSON artifacts.

UTF-8, strict parsing, finite numeric bounds, duplicate-member rejection and
canonical bytes follow each owning artifact contract. In particular, signed
claims use their specified NumericDate fields and binary fields use their
specified encodings; generic ISO dates or Base64 conventions MUST NOT override
an artifact schema. Content-Type is application/json for JSON bodies and
application/ktp-trust-proof+jwt for a bare canonical Trust Proof. A signed
Decision Geometry carrier is a compact JWS with its own protected purpose,
not a JSON copy of its claims. The base profile defines its carriage below.

Complete positive and negative artifact examples are the owning signed proof,
request-binding and Decision Geometry suites. Ellipses or decoded REST summaries
are not alternative complete wire examples.

## CBOR Format

CBOR does not define an alternative native-v3 proof, ordinary request or
evaluation format in this specification. A binary encoding MUST NOT rewrite
signed JWS bytes or silently translate the canonical artifacts. Native artifact
use requires a separately versioned mapping profile with complete artifacts
and interoperability vectors. Independent sensor telemetry encodings remain
subject to their own sensor contract; they do not authorize an action.

## Protocol Buffers

The old `ktp.v1` protobuf package is the legacy v2.1 transport profile, not a
native-v3 message definition. It is available only through the immutable
[v2.1.0 Transport source](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-transport.md#protocol-buffers).
It MUST NOT be recommended, selected, mechanically renamed or decoded as native
v3. No replacement protobuf or gRPC schema is defined by this decision.

A future profile requires its own name/version, complete machine-readable
artifacts, deterministic mapping to the owning canonical schemas, a named
builder and positive/negative interoperability vectors. It MUST preserve all
five named weighted Risk Factors, separately declared demand criticality,
Soul as an independent gate, complete exact
signed proof bytes, and supervision plus tightenedConstraints. A derived
authorization verb is not a stored normative result.

## Format Negotiation

Peers MUST establish the KTP release, named transport profile and supported
artifact contracts from authenticated configuration or explicit authenticated
negotiation before using native artifacts. The base is `ktp-json-jws-v1`; its
version is independent of API paths such as `/api/v1` or `/v1`. The complete
namespace inventory and rejection cases are in specifications/native-transport.md
and specifications/conformance/native-transport-v1.json.

HTTP Accept and Content-Type select representation, not semantic versions.
application/json does not make legacy payload members native. A bare Trust
Proof uses application/ktp-trust-proof+jwt; a bare Decision Geometry carrier
uses application/jose and its independently checked protected purpose. A JSON
wrapper, when explicitly defined by an installed binding, MUST preserve the
exact compact JWS string and all canonical request/association bytes.

An unsupported Accept selection cannot trigger legacy or protobuf fallback;
a server rejects it (406 for an unacceptable response representation, 415 for
an unsupported request media type). An ambiguous version, unknown profile or
mismatched artifact contract MUST fail before any authority is inferred.
Implementation API routing or a content-type header cannot override that gate.

# Transport Security

## TLS Requirements

All KTP communication MUST use TLS 1.3 (RFC 8446).

TLS 1.2 MAY be accepted for legacy compatibility but is NOT RECOMMENDED.

TLS 1.1 and earlier MUST NOT be used.

Cipher suite requirements:

~~~
+-------+------------------------------------------------------+
| Level | Required Cipher Suites                               |
+-------+------------------------------------------------------+
| 1     | TLS_AES_128_GCM_SHA256                               |
| 2     | TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256 |
| 3     | TLS_AES_256_GCM_SHA384                               |
+-------+------------------------------------------------------+
~~~

Certificate requirements:

- ECDSA with P-256 or P-384, or EdDSA with Ed25519
- RSA SHOULD NOT be used for new deployments
- Certificate validity: Maximum 1 year
- OCSP stapling RECOMMENDED

## Mutual TLS

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

## Certificate Requirements

KTP uses a dedicated PKI for component authentication.

Certificate fields:

~~~
+--------------------+---------------------------------------------+
| Field              | Content                                     |
+--------------------+---------------------------------------------+
| Subject CN         | Component identifier                        |
| Subject O          | Zone identifier                             |
| Subject OU         | Component type (oracle, pep, agent, sensor) |
| SAN DNS            | Component hostname(s)                       |
| SAN URI            | KTP identifier (e.g., ktp:agent:...)        |
| Extended Key Usage | serverAuth, clientAuth                      |
+--------------------+---------------------------------------------+
~~~

Example certificate subject:

~~~
   CN=oracle-alpha-1, O=zone-alpha, OU=oracle
   SAN: DNS:oracle-alpha-1.ktp.example.com
        URI:ktp:oracle:zone-alpha:oracle-alpha-1
~~~

# Trust Oracle API

## API Overview

The Trust Oracle API provides:

- Trust Proof issuance and validation
- Agent registration and management
- Context Signal queries
- Administrative operations

Base URL: https://oracle.zone.example.com:8443/api/v1

Here `v1` is the HTTP API route version only. Endpoint paths below are relative
to the deployment origin and illustrate the same API namespace; deployments
MUST publish their exact route mapping rather than concatenate `/api/v1` and
`/v1` prefixes. Neither route selects a KTP release or transport profile.
Administrative/sensor examples below are API views, not alternative proof,
ordinary-request or normative decision schemas.

Authentication:

- mTLS client certificate (preferred)
- Bearer token (JWT signed by Oracle)

All responses include:

- X-KTP-Request-ID: Unique request identifier
- X-KTP-Zone-ID: Responding zone
- X-KTP-Oracle-ID: Responding Oracle node

## Trust Proof Endpoints

### Request Trust Proof

POST /v1/trust-proofs

Request a new Trust Proof for an agent.

Request: { "agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4", "validity_seconds": 10, "include_context": true }

A native v3 response carries the exact compact JWS from
[Canonical Trust Proof Contract](../specifications/trust-proof.md). Any decoded
summary is an unauthoritative view and MUST NOT substitute for those signed
bytes. Complete response-proof examples are the canonical signed fixtures;
this section defines no alternative claims object. Request options such as
include_context MUST NOT omit a claim required by the canonical schema.

Response (403 Forbidden): { "error": { "code": "AGENT_HIBERNATING", "message": "Agent is in hibernation mode", "details": { "e_trust": 15, "required_tier": "observer" } } }

### Validate Trust Proof

POST /v1/trust-proofs/validate

Validate an existing Trust Proof.

Request: { "jws": "eyJhbGciOiJFZERTQSI...", "expected_agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4", "minimum_tier": "analyst" }

Native proof validation follows the canonical contract, Section 5. Its stable
reason and validity/gate result are distinct: a valid veto or undetermined
assertion cannot authorize execution. These proof-validation results are not
an action authorization response; request association follows
specifications/request-binding.md.

### Refresh Trust Proof

POST /v1/trust-proofs/{proof_id}/refresh

Refresh an existing Trust Proof with updated context.

A successful native refresh returns a newly issued canonical compact JWS;
it does not amend or extend the old signed proof.

### Revoke Trust Proof

DELETE /v1/trust-proofs/{proof_id}

Explicitly revoke a Trust Proof before expiration.

Response (204 No Content)

## Agent Endpoints

### Register Agent

POST /v1/agents

Register a new agent with the Trust Oracle.

Request: { "agent_id": "agent:sponsored:acme-deploy:aria:7f8a9b2c", "public_key": "base64...", "algorithm": "eddsa-ed25519", "sponsor_id": "agent:guarantor:5gen:acme-deploy:1234abcd", "lineage": { "type": "sponsored", "generation": 0 }, "metadata": { "name": "Aria", "purpose": "Data processing agent", "owner": "team- data-eng" } }

Response (201 Created): { "agent_id": "agent:sponsored:acme- deploy:aria:7f8a9b2c", "initial_e_base": 25, "initial_tier": "observer", "sponsorship_bond": { "bond_id": "bond-uuid-12345", "sponsor_stake": 8.7, "expires_at": "2026-11-25T00:00:00Z" }, "credential": { ... agent credential ... } }

### Get Agent

GET /v1/agents/{agent_id}

Retrieve agent information.

Response (200 OK): { "agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4", "lineage": { "type": "guarantor", "generation": 7 }, "current_e_base": 87, "current_e_trust": 74, "current_tier": "operator", "trajectory_summary": { "transaction_count": 1547832, "resilience_score": 12500, "oldest_record": "2024-01-15T10:00:00Z" }, "public_key": "base64...", "key_algorithm": "eddsa-ed25519" }

### Update Agent

PATCH /v1/agents/{agent_id}

Update agent metadata or rotate keys.

Request: { "rotate_key": true, "new_public_key": "base64...", "new_algorithm": "eddsa-ed25519", "metadata": { "purpose": "Updated purpose" } }

Response (200 OK): { "agent_id": "...", "key_rotation": { "previous_key_id": "key-old", "new_key_id": "key-new", "grace_period_ends": "2025-11-26T12:00:00Z" } }

### Deregister Agent

DELETE /v1/agents/{agent_id}

Deregister an agent (administrative action).

Response (204 No Content)

## Context Signal Endpoints

### Get Current Context

GET /v1/context

Retrieve current zone-wide Context Signals.

Response (200 OK): { "zone_id": "zone:alpha", "timestamp": "2025-11-25T12:00:00Z", "context": { "evidence_density": 0.12, "trust_trend": 0.08, "adversarial_pressure": 0.22, "update_resistance": 0.18, "attestation_coverage": 0.10, "soul": 0 }, "risk_factor": 0.15, "risk_domains": { "node": 0.10, "neighborhood": 0.18, "global": 0.12 }, "trend": { "direction": "improving", "velocity": -0.02 } }

### Get Context History

GET /v1/context/history?start=2025-11-25T11:00:00Z&end=2025-11-25T12: 00:00Z&interval=60

Response (200 OK): { "zone_id": "zone:alpha", "interval_seconds": 60, "data_points": \[ { "timestamp": "2025-11-25T11:00:00Z", "context": { ... }, "risk_factor": 0.18 }, { "timestamp": "2025-11-25T11:01:00Z", "context": { ... }, "risk_factor": 0.17 }, ... ] }

## Administrative Endpoints

### Health Check

GET /v1/health

Response (200 OK): { "status": "healthy", "oracle_id": "oracle- alpha-1", "zone_id": "zone:alpha", "mesh_status": { "connected_oracles": 5, "threshold_met": true }, "timestamp": "2025-11-25T12:00:00Z" }

The legacy threshold_met field reports signing-threshold availability only. Connected-node counts and a healthy status MUST NOT authorize protected-state commitments or substitute for authenticated consensus evidence. A mesh MUST establish the installed membership, decision quorum, and required protocol evidence under specifications/oracle-consensus.md. In the default N = 5, f = 1 deployment, q = 4 distinct members are required for protected-state decisions; three available signers do not satisfy that decision quorum.

### Get Oracle Status

GET /v1/status

Response (200 OK): { "oracle_id": "oracle-alpha-1", "zone_id": "zone:alpha", "version": "1.0.0", "uptime_seconds": 864000, "statistics": { "proofs_issued_24h": 15000000, "agents_registered": 5432, "current_rps": 250 }, "key_info": { "current_key_id": "oracle- zone-alpha-2025-001", "key_expires_at": "2027-01-01T00:00:00Z", "threshold": "3-of-5" } }

The key_info.threshold field and threshold values embedded in algorithm identifiers describe cryptographic signing configuration. Implementations claiming mesh agreement MUST separately make the authenticated consensus declaration and installed configuration available as required by specifications/oracle-consensus.md. Proof issuers and honest signers MUST verify applicable committed standing; consumers relying on mesh agreement MUST verify the required evidence and binding to the returned result under the selected protocol. A status response or threshold signature alone does not establish that binding. Protocol-native evidence or a protected envelope MUST bind the zone, installed configuration digest and epoch, view, phase/purpose, sequence/checkpoint position, predecessor/state, and operation or control-payload digest; the named protocol version defines the canonical encoding and evidence format.

### Get Public Keys

GET /v1/keys

Response (200 OK): { "zone_id": "zone:alpha", "keys": \[ { "key_id": "oracle-zone-alpha-2025-001", "algorithm": "threshold-frost- ed25519-3of5", "public_key": "base64...", "valid_from": "2025-01-01T00:00:00Z", "valid_until": "2027-01-01T00:00:00Z", "status": "active" }, { "key_id": "oracle-zone-alpha-2024-001", "algorithm": "threshold-frost-ed25519-3of5", "public_key": "base64...", "valid_from": "2024-01-01T00:00:00Z", "valid_until": "2025-01-31T00:00:00Z", "status": "grace_period" } ] }

# Policy Enforcement Point Protocol

## PEP-Oracle Communication

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

## Authorization Request

Native v3 ordinary software evaluation MUST use the canonical request and
association schemas of [Ordinary Request and Trust Proof Association](../specifications/request-binding.md),
with the exact complete compact Trust Proof. An authenticated adapter maps the
actual invocation into the complete canonical body; arbitrary transport
headers, omitted defaults, decoded proof summaries or caller-supplied digests
cannot change the evaluated request. The companion fixes preimages and failures
across transports. No legacy request-message or abbreviated OpenAPI sketch
is accepted as an alternative canonical request. The `/v1/authorize` route is
an API route version, not a KTP semantic version. The authenticated binding MUST
identify where the complete compact proof is carried and bind it to the actual
canonical request; an arbitrary caller-selected header is insufficient.

## Authorization Response

The normative evaluation result is supervision plus tightenedConstraints,
recorded in the canonical Decision Geometry of
[Decision Geometry](../specifications/decision-geometry.md). A local association
is an unsigned prerequisite. A decision crossing a trust boundary MUST use the
separately purpose-typed signed Decision Geometry carrier covering the complete
body, both exact request/proof digests and evaluation context.

Consumers MUST check key role, installed profile, actual invocation binding,
current validity, replay and all other restrictions before use. A bare carrier
uses application/jose; its protected purpose distinguishes it from a Trust
Proof. Neither carrier validity, an HTTP success status, a copied score nor
an ALLOWED/DENIED/DEFERRED enum is execution permission. Product-derived verbs
MUST NOT replace the normative result or remove constraints.

The legacy authorization enum, protobuf service and flat HTTP result examples
remain only at v2.1.0. No asynchronous deferral, retry, callback or execution
receipt format is introduced here.

## Inline vs. Sidecar Modes

### Inline Mode

Application embeds PEP logic directly:

Application          Trust Oracle \|                     \| \|-- AuthzRequest ---->\| \|<--- AuthzResponse --\| \|                     \| \| (proceed or deny)   \|

Latency: 1-5ms typical Use when: Simplicity preferred, low-volume

### Sidecar Mode

Separate PEP process (e.g., Envoy filter):

~~~
Application     PEP Sidecar     Trust Oracle |               |
| |-- Request --->|                | |               |-- AuthzReq
--->| |               |<-- AuthzResp --| |<-- Response --|
| |               |                |
~~~

Additional latency: 0.5-1ms for IPC Use when: Service mesh, polyglot environment

# Real-Time Communication

## WebSocket Endpoints

WebSocket provides bidirectional real-time communication.

Endpoint: wss://oracle.zone.example.com:8449/v1/ws

Connection handshake includes:

- TLS client certificate (mTLS)
- An explicitly selected, separately published native streaming profile

The old Sec-WebSocket-Protocol token `ktp.v1` denotes the legacy stream binding
and MUST NOT negotiate native v3. This decision assigns no replacement stream
subprotocol. The message/event sketches below describe notification patterns,
not a complete native streaming profile. Notifications are hints only; they
MUST NOT establish fresh authority, substitute for canonical proof/decision
validation or extend an existing proof's expiry.
- Authorization header with agent credential

Message format:

{ "type": "message_type", "id": "message-id", "timestamp": "2025-11-25T12:00:00Z", "payload": { ... } }

Message types:

Client → Server:

- subscribe: Subscribe to updates
- unsubscribe: Unsubscribe from updates
- ping: Keep-alive

Server → Client:

- trust_update: Trust Score changed
- proof_invalidated: Trust Proof revoked
- context_update: Context Signals changed
- emergency: Emergency broadcast
- pong: Keep-alive response

### Subscribe to Trust Updates

Client sends: { "type": "subscribe", "id": "sub-001", "payload": { "subscriptions": \[ { "type": "agent_trust", "agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4" }, { "type": "zone_context" } ] } }

Server confirms: { "type": "subscribe_ack", "id": "sub-001", "payload": { "subscription_ids": \["sub-agent-12345", "sub- context-67890"] } }

### Trust Update Message

Server pushes when Trust Score changes:

{ "type": "trust_update", "id": "update-12345", "timestamp": "2025-11-25T12:00:05Z", "payload": { "agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4", "previous_e_trust": 74, "current_e_trust": 73, "previous_tier": "operator", "current_tier": "operator", "tier_changed": false, "trigger": "context_degradation" } }

## Server-Sent Events

SSE provides server-to-client streaming over HTTP.

Endpoint: GET /v1/events

Query parameters:

- agent_id: Filter to specific agent
- types: Comma-separated event types

Example: GET /v1/events?types=trust_update,emergency

Response (text/event-stream):

event: trust_update id: update-12345 data: {"agent_id":"agent:guarantor:7gen:...","current_e_trust":71}

event: context_update id: context-67890 data: {"risk_factor":0.18,"trend":"degrading"}

SSE is simpler than WebSocket but unidirectional. Use when: Client only needs to receive updates, not send.

## gRPC Streaming

The v2.1 gRPC service/message definitions are legacy. A future native gRPC
streaming binding requires the separately published named profile, complete
machine-readable definitions and vectors described above. HTTP/JSON base
support is mandatory regardless of any optional future streaming support.

## Trust Proof Push

Trust Oracles can push updated Trust Proofs to agents:

1. Agent subscribes via WebSocket or gRPC stream
2. Oracle detects Trust Score change
3. Oracle pushes new Trust Proof
4. Agent updates cached proof

Delivery can be delayed, lost, duplicated or reordered. Receiving an update
MUST NOT imply current validity; consumers validate the complete newly issued
compact JWS under the canonical proof contract and cannot extend old authority.
No flat `proof` object accompanies or substitutes for those exact signed bytes.
A native push binding must define its complete envelope and authenticated
profile separately; the old abbreviated push sketch is not a native schema.

# Sensor Data Transport

## Sensor Registration

POST /v1/sensors

Request: { "sensor_id": "sensor:node:host-001:cpu", "sensor_type": "cpu_utilization", "dimension": "evidence_density", "location": { "host": "host-001", "zone": "zone:alpha" }, "reporting_interval_ms": 1000, "authentication": { "type": "mtls", "certificate_fingerprint": "sha256:abc123..." } }

Response (201 Created): { "sensor_id": "sensor:node:host-001:cpu", "assigned_aggregator": "aggregator-alpha-1.ktp.example.com:8446", "reporting_endpoint": "/v1/sensors/sensor:node:host-001:cpu/readings", "authentication_token": "eyJhbGciOiJFZERTQSI..." }

## Reading Submission

Individual reading:

POST /v1/sensors/{sensor_id}/readings

Request: { "timestamp": "2025-11-25T12:00:00.123Z", "value": 0.42, "confidence": 0.95, "metadata": { "sample_count": 100 } }

Response (202 Accepted): { "accepted": true, "reading_id": "reading- uuid-12345" }

Batch readings (preferred for efficiency):

POST /v1/sensors/{sensor_id}/readings/batch

Request: { "readings": \[ { "timestamp": "2025-11-25T12:00:00.000Z", "value": 0.42 }, { "timestamp": "2025-11-25T12:00:01.000Z", "value": 0.45 }, { "timestamp": "2025-11-25T12:00:02.000Z", "value": 0.43 } ] }

Response (202 Accepted): { "accepted_count": 3, "rejected_count": 0 }

## Aggregation Protocol

Sensors → Aggregators → Trust Oracle

Aggregators perform:

- Statistical aggregation (mean, percentile, variance)
- Outlier detection and filtering
- Dimension-specific normalization
- Rate limiting and batching

Aggregator output to Trust Oracle:

{ "aggregator_id": "aggregator-alpha-1", "timestamp": "2025-11-25T12:00:05Z", "window_seconds": 5, "dimension": "evidence_density", "risk_domain": "node", "aggregations": \[ { "host": "host-001", "value": 0.43, "sample_count": 5, "variance": 0.002, "min": 0.41, "max": 0.45, "p95": 0.44 }, { "host": "host-002", "value": 0.38, "sample_count": 5, "variance": 0.001 } ] }

### Empty and Short Windows

An aggregation window may contain no readings.  This is the aggregation boundary's instance of the rule {{KTP-CORE}} Section 5.9 states as a class: an undefined input MUST NOT resolve toward permission, and substituting a measured value for an undefined one - including zero - is prohibited.  A mean computed over an empty window is such a substitution, and it crosses the wire looking exactly like an observation.

sample_count is REQUIRED in every aggregation entry.  It is the count of readings the window actually contained, and it carries the fail-closed signal for everything else in the entry.  An aggregator MUST NOT omit it, and MUST NOT report a count it did not observe.

An aggregation entry MUST omit every statistic its window does not define.  value, min, max and p95 are undefined for a window of zero readings; variance is undefined below two.  The rule is stated over the property rather than over the current field list so that a statistic added later inherits it.

This is deliberately stronger than flagging.  A consumer that ignores sample_count and reads a flagged value gets a plausible number and no indication that it is fiction; a consumer that ignores sample_count and reads an entry with no value fails at the point of use.  Silence and absence do not separate, and the wire format should not make them look different.

A consumer MUST NOT treat an aggregation entry as an observation of the environment unless sample_count is greater than zero.  A consumer MUST NOT substitute a value for an omitted statistic - not zero, not the previous window's value, not a dimension default.  An entry with sample_count zero is a report that the environment was not observed, and it MUST be handled under {{KTP-CORE}} Section 5.9 and counted as unavailable under {{KTP-SENSORS}} Section 6.2 rather than aggregated into the Risk Factor.

An aggregator MUST emit an entry for a host whose window was empty rather than dropping the host from the array.  A dropped host and a host that reported calm conditions are indistinguishable to the Oracle, and whoever can suppress a feed also chooses the moment of suppression.

## Batching and Compression

For high-volume sensor data:

Content-Encoding: gzip Content-Type: application/json

Compression does not change the owning sensor schema or artifact semantics.

Batch size recommendations:

~~~
+--------------------+--------------+----------------+-------------+
| Reporting Interval | Batch Size   | Batch Interval | Compression |
+--------------------+--------------+----------------+-------------+
| 100ms              | 100 readings | 10 seconds     | Required    |
| 1 second           | 60 readings  | 60 seconds     | Recommended |
| 5 seconds          | 12 readings  | 60 seconds     | Optional    |
+--------------------+--------------+----------------+-------------+
~~~

# Flight Recorder Transport

## Record Submission

POST /v1/flight-recorder/records

Submit the complete canonical Decision Geometry, or its complete signed carrier
when it crosses a trust boundary, under specifications/decision-geometry.md.
Storage metadata and product-derived views belong outside the canonical body.
The old decision wrapper with a derived result verb is not the native record.
Transport acceptance acknowledges receipt only, not execution or durable audit
assurance beyond the recorder's separately established contract.

Response (202 Accepted): { "record_id": "fr-uuid-67890", "record_hash": "sha256:def456...", "chain_position": 1547833, "anchor_pending": true }

## Batch Submission

POST /v1/flight-recorder/records/batch

Request: { "records": \[ { ... record 1 ... }, { ... record 2 ... }, { ... record 3 ... } ], "batch_signature": "base64..." }

Response (202 Accepted): { "accepted_count": 3, "rejected_count": 0, "batch_id": "batch-uuid-12345", "record_ids": \[ "fr-uuid-001", "fr- uuid-002", "fr-uuid-003" ] }

## Query Interface

Flight Recorder queries for audit and forensics.

### Query by Agent

GET /v1/flight- recorder/records?agent_id={agent_id}&start={start}&end={end}

Response (200 OK): { "query": { "agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4", "start": "2025-11-25T11:00:00Z", "end": "2025-11-25T12:00:00Z" }, "total_records": 1250, "returned_records": 100, "cursor": "cursor- abc123", "records": \[ { ... }, { ... } ] }

### Query by Decision Result

GET /v1/flight-recorder/records?result=denied&start={start}&end={end}

Returns all denied actions in time range.

### Verify Chain Integrity

POST /v1/flight-recorder/verify

Request: { "start_record_id": "fr-uuid-001", "end_record_id": "fr- uuid-1000" }

Response (200 OK): { "verified": true, "records_checked": 1000, "chain_unbroken": true, "signatures_valid": true, "anchors_verified": 5 }

# Federation Transport

## Zone Discovery

GET /.well-known/ktp-zone

Discovery MUST distinguish the immutable KTP release from its advertised named
transport profiles and separately versioned capabilities. Native artifact
exchange advertises `ktp-json-jws-v1`, subject to authenticated agreement of its
owning artifact contracts. The historical capability tokens `ktp-core-v1`,
`ktp-federation-v1` and `ktp-celestial-v1` do not identify native v3 or this base
profile. A document advertising only those tokens MUST NOT trigger native
acceptance or silent fallback. Discovery hints alone are not trusted policy.

## Trust Proof Exchange

POST /v1/federation/trust-proof

Exchange Trust Proof from foreign zone.

Request: { "foreign_proof_jws": "eyJhbGciOiJFZERTQSI...", "requesting_zone": "zone:beta", "purpose": "cross_zone_access", "requested_action": { "type": "data_read", "target": "database:shared-catalog" } }

Response (200 OK): { "accepted": true, "local_evaluation": { "foreign_e_trust": 80, "trust_factor": 0.85, "local_equivalent_e_trust": 68, "local_tier": "analyst" }, "local_proof_jws": "eyJhbGciOiJFZERTQSI...", "valid_for_seconds": 10 }

The issued local ordinary proof MUST satisfy the KTP-Core ten-second maximum and iat <= current_time < exp; valid_for_seconds MUST NOT override the signed claims. At current_time = exp it is expired. Federation outages, caches, and invalid or unverifiable time MUST NOT extend ordinary authority.

## Federation Heartbeat

Federated zones exchange heartbeats for liveness.

The heartbeat is a liveness notification. The old gRPC heartbeat definition is
legacy; a native streaming profile must define its complete envelope separately.
Heartbeat data MUST NOT substitute for authenticated standing or authorization.

Heartbeat interval: 10 seconds Timeout threshold: 3 missed heartbeats (30 seconds)

On timeout: - Increase trust_factor penalty for zone - Alert operators - Continue accepting cached proofs until expiry

# Error Handling

## Error Response Format

All errors use consistent format:

{ "error": { "code": "ERROR_CODE", "message": "Human-readable message", "details": { ... error-specific details ... }, "request_id": "req-12345", "timestamp": "2025-11-25T12:00:00Z" } }

HTTP status codes:

~~~
+--------+----------------------------+----------------------------+
| Status | Meaning                    | Retry?                     |
+--------+----------------------------+----------------------------+
| 400    | Bad request (client error) | No                         |
| 401    | Authentication required    | After re-auth              |
| 403    | Forbidden (authorization)  | No (or after trust change) |
| 404    | Resource not found         | No                         |
| 409    | Conflict                   | Maybe (depends on cause)   |
| 429    | Rate limited               | Yes (after Retry-After)    |
| 500    | Server error               | Yes (with backoff)         |
| 502    | Upstream error             | Yes (with backoff)         |
| 503    | Service unavailable        | Yes (after Retry-After)    |
| 504    | Timeout                    | Yes                        |
+--------+----------------------------+----------------------------+
~~~

## Error Codes

Every code in this registry is wire-visible unless listed as evidence-only.  An evidence-only code MUST NOT appear in any response returned to the agentic system; it is recorded in the evidence record (see {{KTP-AUDIT}}) so that its cause reads apart in audit.  The wire response for a decision carrying an evidence-only code is the ordinary response for its supervision level.

~~~
Authentication errors (AUTH_*):
+--------------+------+-------------------------+
| Code         | HTTP | Description             |
+--------------+------+-------------------------+
| AUTH_MISSING | 401  | No credentials provided |
| AUTH_INVALID | 401  | Invalid credentials     |
| AUTH_EXPIRED | 401  | Credentials expired     |
| AUTH_REVOKED | 401  | Credentials revoked     |
+--------------+------+-------------------------+
~~~

~~~
Authorization errors (AUTHZ_*):
+--------------------------+------+--------------------------+
| Code                     | HTTP | Description              |
+--------------------------+------+--------------------------+
| AUTHZ_INSUFFICIENT_TRUST | 403  | E_trust < action risk    |
| AUTHZ_SOUL_VETO          | 403  | Soul constraint violated |
| AUTHZ_TIER_INSUFFICIENT  | 403  | Tier too low for action  |
| AUTHZ_HIBERNATING        | 403  | Agent in hibernation     |
+--------------------------+------+--------------------------+
~~~

~~~
Evidence-only codes (never on the wire):
+---------------------------+------+----------------------------+
| Code                      | HTTP | Description                |
+---------------------------+------+----------------------------+
| KINETIC_CAPACITY_EXCEEDED | -    | Kinematic veto [KTP-AUDIT] |
+---------------------------+------+----------------------------+
~~~

KINETIC_CAPACITY_EXCEEDED marks a kinematic veto - a silent_veto raised by the kinetic envelope - so that it reads apart from an ordinary limit violation in audit, without disclosing to the agentic system which limit vetoed it.

~~~
Trust errors (TRUST_*):
+-------------------------+------+-------------------------------+
| Code                    | HTTP | Description                   |
+-------------------------+------+-------------------------------+
| TRUST_PROOF_EXPIRED     | 400  | Trust Proof has expired       |
| TRUST_PROOF_INVALID_SIG | 400  | Signature verification failed |
| TRUST_PROOF_REVOKED     | 400  | Trust Proof was revoked       |
| TRUST_AGENT_UNKNOWN     | 404  | Agent not registered          |
+-------------------------+------+-------------------------------+
~~~

~~~
Federation errors (FED_*):
+--------------------+------+---------------------------------+
| Code               | HTTP | Description                     |
+--------------------+------+---------------------------------+
| FED_ZONE_UNKNOWN   | 404  | Foreign zone not recognized     |
| FED_ZONE_UNTRUSTED | 403  | Trust factor below minimum      |
| FED_PROOF_REJECTED | 400  | Foreign proof validation failed |
+--------------------+------+---------------------------------+
~~~

## Retry Behavior

Clients SHOULD implement retry with exponential backoff:

base_delay = 100ms max_delay = 30s max_retries = 5

delay = min(base_delay * 2^attempt, max_delay) + random_jitter

Retry-After header: When present, client MUST wait specified duration before retry.

Retry-After: 5

Or with date:

Retry-After: Wed, 25 Nov 2025 12:01:00 GMT

# Performance Requirements

Latency targets:

~~~
+--------------------------------+---------+---------+---------+
| Operation                      | Level 1 | Level 2 | Level 3 |
+--------------------------------+---------+---------+---------+
| Trust Proof issuance           | < 50ms  | < 20ms  | < 10ms  |
| Trust Proof validation         | < 5ms   | < 2ms   | < 1ms   |
| Authorization decision         | < 20ms  | < 10ms  | < 5ms   |
| Trust Score update propagation | < 5s    | < 1s    | < 100ms |
| Sensor reading ingestion       | < 100ms | < 50ms  | < 20ms  |
+--------------------------------+---------+---------+---------+
~~~

Throughput targets:

~~~
+-------------------------------+---------+---------+---------+
| Operation                     | Level 1 | Level 2 | Level 3 |
+-------------------------------+---------+---------+---------+
| Trust Proofs/second           | 100     | 1,000   | 10,000  |
| Authorization requests/second | 100     | 1,000   | 10,000  |
| Sensor readings/second        | 1,000   | 10,000  | 100,000 |
| Flight Recorder records/sec   | 100     | 1,000   | 10,000  |
+-------------------------------+---------+---------+---------+
~~~

# Security Considerations

## Transport Security

- All communication MUST use TLS 1.3 - Certificate pinning RECOMMENDED for Oracle connections - Private keys MUST NOT be transmitted

## Message Integrity

- All Trust Proofs are signed at application layer - Flight Recorder entries are cryptographically chained - Message manipulation detectable even if TLS compromised

## Replay Protection

- Trust Proofs include timestamps and short validity - Ordinary request IDs, replay domains and reservations MUST satisfy specifications/request-binding.md; logging or a nonce alone does not satisfy that contract

## Denial of Service

- Rate limiting REQUIRED on all endpoints - Connection limits per client - Request size limits enforced

# IANA Considerations

## Well-Known URI Registration

URI suffix: ktp-zone Change controller: IETF Specification document: This document

## Media Type Registration

Media type: application/ktp-trust-proof+jwt Encoding: compact JWT/JWS
Specification: specifications/trust-proof.md; this transport supplies no
alternate artifact contract.

--- back

# Protocol Buffer Definitions

The legacy definitions are preserved in the immutable
[v2.1.0 appendix](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-transport.md#protocol-buffer-definitions),
commit 15520035267546e1035aad7beea0cc3cf9ef8f2c. They are not native-v3 examples
or a recommended encoding. See specifications/native-transport.md and
MIGRATION.md for negotiated isolation and migration; no stored bytes are rewritten.

# OpenAPI Specification

The abbreviated legacy surface is preserved only in the immutable
[v2.1.0 appendix](https://github.com/nmcitra/ktp-rfc/blob/v2.1.0/rfc-src/ktp-transport.md#openapi-specification).
There is no complete native OpenAPI artifact in this decision. A future one
requires a separately named/versioned profile, complete machine-readable
artifact, deterministic canonical mapping, builder and interoperability vectors.
An API document cannot weaken the owning request, proof or result contract.
