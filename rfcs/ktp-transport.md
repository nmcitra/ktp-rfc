# KTP-Transport — Transport Specification

*The connective tissue of Digital Physics*

---

> **Design Principle**: Without standardized transport, implementations cannot interoperate. KTP transport builds on standard protocols—HTTP/2, gRPC, WebSocket—not custom wire formats.

---

## At a Glance

| Property | Value |
|----------|-------|
| **Status** | :material-check-circle:{ .stable } Stable |
| **Version** | 0.1 |
| **Dependencies** | [KTP-Core](ktp-core.md), [KTP-Crypto](ktp-crypto.md) |
| **Required By** | All KTP network implementations |

---

## Design Principles

<div class="grid cards" markdown>

-   :material-protocol:{ .lg .middle } **Standard Protocols**

    ---
    
    Build on HTTP/2, gRPC, WebSocket—leverage existing infrastructure and tooling.

-   :material-format-list-bulleted:{ .lg .middle } **Multiple Formats**

    ---
    
    Support JSON (readability), CBOR (efficiency), Protocol Buffers (performance).

-   :material-speedometer:{ .lg .middle } **Low Latency**

    ---
    
    Trust Score updates propagate in milliseconds. Design for real-time, not batch.

-   :material-layers:{ .lg .middle } **Defense in Depth**

    ---
    
    TLS mandatory. Application-layer signatures provide additional protection.

-   :material-shield-alert:{ .lg .middle } **Graceful Degradation**

    ---
    
    Network failures should not cause security failures. **Fail closed** when Oracle unreachable.

</div>

---

## Communication Patterns

KTP uses four communication patterns:

``` mermaid
flowchart LR
    subgraph Patterns
        RR["📥 Request-Response<br/>(HTTP/gRPC)"]
        ST["📡 Streaming<br/>(WebSocket/gRPC)"]
        PU["📤 Push<br/>(SSE/WebSocket)"]
        AS["📋 Async Submission<br/>(HTTP POST)"]
    end
    
    RR --> TP["Trust Proof requests"]
    ST --> RT["Real-time updates"]
    PU --> EM["Emergency broadcasts"]
    AS --> FR["Flight Recorder entries"]
```

| Pattern | Protocol | Use Cases |
|---------|----------|-----------|
| **Request-Response** | HTTP/gRPC | Trust Proof requests, Agent registration |
| **Streaming** | WebSocket/gRPC | Real-time Trust Score, Sensor feeds |
| **Push** | SSE/WebSocket | Trust Proof invalidation, Key revocation |
| **Async Submission** | HTTP POST | Flight Recorder, Batch sensor data |

---

## Protocol Stack

``` mermaid
flowchart TB
    subgraph Stack["KTP Protocol Stack"]
        A["KTP Messages<br/>(Application)"]
        S["JSON / CBOR / Protobuf<br/>(Serialization)"]
        R["gRPC / REST<br/>(RPC Framework)"]
        H["HTTP/2 / WebSocket<br/>(Session)"]
        T["TLS 1.3<br/>(Security)"]
        N["TCP / IPv4 / IPv6<br/>(Network)"]
    end
    
    A --> S --> R --> H --> T --> N
```

=== "Minimum Viable"
    
    **JSON** over **REST** over **HTTP/2** over **TLS 1.3**
    
    - Easy to implement
    - Human-readable
    - Standard tooling

=== "High Performance"
    
    **Protocol Buffers** over **gRPC** over **HTTP/2** over **TLS 1.3**
    
    Plus **WebSocket** for real-time updates
    
    - Strongly typed
    - Code generation
    - ~50% smaller payloads

---

## Port Assignments

| Service | Port | Protocol | TLS |
|---------|------|----------|-----|
| Trust Oracle API | 8443 | HTTPS | Required |
| Trust Oracle gRPC | 8444 | gRPC | Required |
| PEP Authorization | 8445 | gRPC | Required |
| Sensor Aggregator | 8446 | HTTPS/gRPC | Required |
| Flight Recorder | 8447 | HTTPS | Required |
| Federation Gateway | 8448 | HTTPS/gRPC | Required |
| WebSocket (updates) | 8449 | WSS | Required |

!!! danger "No Unencrypted Transport"
    All ports use TLS. **Unencrypted transport is NOT permitted.**

---

## Message Serialization

=== "JSON"
    
    Default format for human-readable contexts.
    
    **Content-Type**: `application/json`
    
    | Requirement | Specification |
    |-------------|---------------|
    | Encoding | UTF-8 |
    | Numbers | IEEE 754 double |
    | Dates | ISO 8601 (`2025-11-25T12:00:00Z`) |
    | Binary | Base64 (RFC 4648) |
    
    ??? example "JSON Trust Proof Request"
        ```json
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
        ```

=== "CBOR"
    
    Compact binary encoding for high-volume contexts.
    
    **Content-Type**: `application/cbor`
    
    | Trust Proof | Size |
    |-------------|------|
    | JSON | ~850 bytes |
    | CBOR | ~420 bytes |
    | **Savings** | **~50%** |
    
    RECOMMENDED for:
    
    - High-volume sensor data
    - Embedded/constrained devices
    - Performance-critical paths

=== "Protocol Buffers"
    
    Strongly-typed with code generation.
    
    **Content-Type**: `application/x-protobuf` or `application/grpc+proto`
    
    ??? example "Proto Definition"
        ```protobuf
        syntax = "proto3";
        package ktp.v1;
        
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
        ```

### Format Negotiation

```http
Accept: application/cbor, application/json;q=0.9
```

Servers **MUST** support JSON. CBOR and Protobuf are RECOMMENDED.

---

## Transport Security

### TLS Requirements

!!! warning "TLS 1.3 Required"
    All KTP communication **MUST** use TLS 1.3 (RFC 8446).
    
    - TLS 1.2 MAY be accepted for legacy (NOT RECOMMENDED)
    - TLS 1.1 and earlier **MUST NOT** be used

| Level | Required Cipher Suites |
|-------|------------------------|
| Level 1 | `TLS_AES_128_GCM_SHA256` |
| Level 2 | `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256` |
| Level 3 | `TLS_AES_256_GCM_SHA384` |

### Mutual TLS

| Communication | mTLS |
|---------------|------|
| Oracle ↔ Oracle | **Required** |
| PEP ↔ Oracle | **Required** |
| Federation Gateway | **Required** |
| Agent ↔ Oracle | Recommended |
| Sensor ↔ Aggregator | Recommended |

---

## Trust Oracle API

### Endpoints Overview

``` mermaid
flowchart LR
    subgraph Oracle["Trust Oracle API (8443)"]
        TP["/v1/trust-proof"]
        AG["/v1/agents"]
        CT["/v1/context"]
        AD["/v1/admin"]
    end
    
    A["Agent"] --> TP
    P["PEP"] --> TP
    S["Sensors"] --> CT
    O["Operator"] --> AD
```

### Trust Proof Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/trust-proof/request` | Request new Trust Proof |
| `GET` | `/v1/trust-proof/{proof_id}` | Retrieve existing proof |
| `POST` | `/v1/trust-proof/validate` | Validate proof signature |
| `POST` | `/v1/trust-proof/refresh` | Refresh expiring proof |

??? example "Trust Proof Request"
    ```http
    POST /v1/trust-proof/request HTTP/2
    Content-Type: application/json
    Authorization: Bearer <agent_token>
    
    {
      "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
      "action": {
        "type": "data_write",
        "target": "database:orders",
        "risk_score": 65
      }
    }
    ```
    
    **Response**:
    ```json
    {
      "proof_id": "tp-2025-11-25-abc123",
      "e_base": 87,
      "e_trust": 73.95,
      "risk_factor": 0.15,
      "tier": "operator",
      "expires_at": "2025-11-25T12:01:00Z",
      "signature": "base64..."
    }
    ```

### Agent Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/agents/register` | Register new agent |
| `GET` | `/v1/agents/{agent_id}` | Get agent details |
| `GET` | `/v1/agents/{agent_id}/trajectory` | Get trajectory chain |
| `POST` | `/v1/agents/{agent_id}/sponsor` | Create sponsorship bond |

---

## Real-Time Communication

### WebSocket Updates

Connect to `wss://oracle:8449/v1/ws` for real-time Trust Score updates:

``` mermaid
sequenceDiagram
    participant A as Agent
    participant W as WebSocket
    participant O as Oracle
    
    A->>W: Connect (auth token)
    W->>O: Subscribe agent_id
    loop Every update
        O->>W: Trust Score change
        W->>A: Push notification
    end
```

??? example "WebSocket Message"
    ```json
    {
      "type": "trust_update",
      "agent_id": "agent:persistent:7gen:optimized:a1b2c3d4",
      "e_trust": 68.5,
      "previous_e_trust": 73.95,
      "delta": -5.45,
      "reason": "environmental_stress",
      "timestamp": "2025-11-25T12:00:30Z"
    }
    ```

### Server-Sent Events

For simpler push scenarios:

```http
GET /v1/events/trust-updates HTTP/2
Accept: text/event-stream

event: trust_update
data: {"agent_id": "...", "e_trust": 68.5}

event: veto_notification
data: {"agent_id": "...", "action": "data_delete", "reason": "insufficient_trust"}
```

---

## Policy Enforcement Point Protocol

### Authorization Flow

``` mermaid
sequenceDiagram
    autonumber
    participant A as Agent
    participant PEP as Policy Enforcement Point
    participant O as Trust Oracle
    
    A->>PEP: Action Request
    PEP->>O: Authorization Request
    O->>O: Evaluate A ≤ E_trust
    O-->>PEP: Authorization Response
    alt Allowed
        PEP-->>A: Action Proceeds
    else Denied (Silent Veto)
        PEP-->>A: Action Impossible
    end
```

### Inline vs. Sidecar Modes

=== "Inline Mode"
    
    PEP integrated directly into application:
    
    ```
    [Agent] → [App + PEP] → [Oracle]
    ```
    
    - Lower latency
    - Tighter integration
    - Language-specific SDK required

=== "Sidecar Mode"
    
    PEP as separate process (Kubernetes sidecar):
    
    ```
    [Agent] → [App] → [PEP Sidecar] → [Oracle]
    ```
    
    - Language-agnostic
    - Easier deployment
    - Slight latency overhead

---

## Sensor Data Transport

### Registration & Submission

``` mermaid
flowchart LR
    S["Sensor"] -->|Register| A["Aggregator"]
    S -->|Submit readings| A
    A -->|Aggregated data| O["Oracle"]
    O -->|Update R| CT["Context Tensor"]
```

| Endpoint | Description |
|----------|-------------|
| `POST /v1/sensors/register` | Register new sensor |
| `POST /v1/sensors/{id}/readings` | Submit readings |
| `POST /v1/sensors/batch` | Batch submission |

### Batching & Compression

For high-volume sensors:

| Parameter | Recommendation |
|-----------|----------------|
| Batch size | 100-1000 readings |
| Max latency | 5 seconds |
| Compression | gzip or zstd |
| Format | CBOR (50% smaller than JSON) |

---

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "KTP-4003",
    "message": "Trust Proof expired",
    "details": {
      "proof_id": "tp-2025-11-25-abc123",
      "expired_at": "2025-11-25T12:01:00Z"
    },
    "retry_after": 0,
    "request_id": "req-xyz789"
  }
}
```

### Error Codes

| Code | Category | Description |
|------|----------|-------------|
| KTP-4001 | Client | Invalid request format |
| KTP-4002 | Client | Agent not found |
| KTP-4003 | Client | Trust Proof expired |
| KTP-4010 | Auth | Invalid signature |
| KTP-4011 | Auth | Insufficient trust level |
| KTP-5001 | Server | Oracle unavailable |
| KTP-5002 | Server | Threshold not met |

### Retry Behavior

| Error Type | Retry | Backoff |
|------------|-------|---------|
| 4xx Client | No | — |
| 5xx Server | Yes | Exponential (1s, 2s, 4s...) |
| Network | Yes | Exponential with jitter |
| Timeout | Yes | Max 3 attempts |

!!! danger "Fail Closed"
    If the Trust Oracle is unreachable after retries, the PEP **MUST** deny the action. Never fail open.

---

## Performance Requirements

| Metric | Requirement |
|--------|-------------|
| Trust Proof latency | < 50ms (p99) |
| Authorization decision | < 10ms (p99) |
| WebSocket update delivery | < 100ms |
| Sensor batch processing | < 1s for 1000 readings |
| Federation heartbeat | Every 30s |

---

## Related Specifications

??? info "Related Specifications"
    - [KTP-Core](ktp-core.md): Trust physics carried by transport.
    - [KTP-Crypto](ktp-crypto.md): Encryption and signing requirements.
    - [KTP-Sensors](ktp-sensors.md): Telemetry payload formats.
    - [KTP-Federation](ktp-federation.md): Cross-zone transport protocols.

---

## Official RFC Document

!!! abstract "IETF Submission Format"
    The text below is the canonical RFC specification intended for IETF submission. It contains the complete, authoritative technical specification.

??? note "View Complete RFC Text (ktp-transport.txt)"
    ```
    --8<-- "rfcs/ktp-transport.txt"
    ```
