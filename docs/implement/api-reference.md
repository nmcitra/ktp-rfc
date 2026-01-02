# API Reference

*Complete KTP Protocol API Documentation*

---

This reference documents all KTP REST, gRPC, and WebSocket APIs. For integration guidance, see the [Developer Guide](developer-guide.md).

## Base URLs

```
Production:   https://oracle.{zone-id}.ktp
Development:  https://oracle-dev.{zone-id}.ktp
Local:        http://localhost:8080
```

## Authentication

All API requests require mTLS (mutual TLS) authentication with valid agent credentials.

```http
GET /api/v1/trust-proof
Host: oracle.yourzone.ktp
X-KTP-Agent-ID: agent:service-alpha
X-KTP-Zone-ID: blue:production
Authorization: Bearer {jwt-token}
```

---

## Trust Oracle API

### Request Trust Proof

Request a cryptographically signed trust proof for an agent.

=== "REST"
    ```http
    POST /api/v1/trust-proof
    Content-Type: application/json
    
    {
      "agent_id": "agent:service-alpha",
      "action": "database:read",
      "resource": "users-table",
      "context": {
        "ip_address": "10.0.1.42",
        "session_age": 3600
      }
    }
    ```
    
    **Response (200 OK)**:
    ```json
    {
      "proof_id": "proof-uuid-12345",
      "agent_id": "agent:service-alpha",
      "trust_score": 72,
      "tier": "analyst",
      "e_base": 85,
      "e_trust": 72,
      "risk_factor": 0.15,
      "issued_at": "2026-01-02T14:30:00Z",
      "expires_at": "2026-01-02T14:30:30Z",
      "signature": "base64-encoded-signature",
      "oracle_quorum": ["oracle-1", "oracle-2", "oracle-3"]
    }
    ```

=== "gRPC"
    ```protobuf
    service TrustOracle {
      rpc RequestProof(TrustProofRequest) returns (TrustProof);
    }
    
    message TrustProofRequest {
      string agent_id = 1;
      string action = 2;
      string resource = 3;
      map<string, string> context = 4;
    }
    
    message TrustProof {
      string proof_id = 1;
      string agent_id = 2;
      int32 trust_score = 3;
      string tier = 4;
      int32 e_base = 5;
      int32 e_trust = 6;
      float risk_factor = 7;
      google.protobuf.Timestamp issued_at = 8;
      google.protobuf.Timestamp expires_at = 9;
      bytes signature = 10;
      repeated string oracle_quorum = 11;
    }
    ```

**Parameters**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Unique agent identifier |
| `action` | string | Yes | Action type (e.g., `database:read`) |
| `resource` | string | Yes | Target resource identifier |
| `context` | object | No | Additional context for risk calculation |

**Response Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `proof_id` | string | Unique proof identifier |
| `trust_score` | integer | Effective trust score ($E_{trust}$), 0-100 |
| `tier` | string | Trust tier: `observer`, `analyst`, `operator`, `architect`, `god-mode` |
| `e_base` | integer | Base trust score, 0-100 |
| `risk_factor` | float | Environmental risk factor ($R$), 0.0-1.0 |
| `expires_at` | timestamp | Proof expiration (typically 30 seconds) |
| `signature` | string | Cryptographic signature from Oracle quorum |

**Error Codes**:

| Code | Meaning |
|------|---------|
| `400` | Invalid request parameters |
| `401` | Authentication failed |
| `403` | Agent not authorized for this zone |
| `429` | Rate limit exceeded |
| `503` | Oracle quorum unavailable |

---

### Verify Trust Proof

Verify the authenticity and validity of a trust proof.

=== "REST"
    ```http
    POST /api/v1/trust-proof/verify
    Content-Type: application/json
    
    {
      "proof_id": "proof-uuid-12345",
      "signature": "base64-encoded-signature",
      "agent_id": "agent:service-alpha"
    }
    ```
    
    **Response (200 OK)**:
    ```json
    {
      "valid": true,
      "reason": null,
      "signature_valid": true,
      "not_expired": true,
      "agent_match": true
    }
    ```

=== "gRPC"
    ```protobuf
    service TrustOracle {
      rpc VerifyProof(VerifyProofRequest) returns (VerifyProofResponse);
    }
    
    message VerifyProofRequest {
      string proof_id = 1;
      bytes signature = 2;
      string agent_id = 3;
    }
    
    message VerifyProofResponse {
      bool valid = 1;
      string reason = 2;
      bool signature_valid = 3;
      bool not_expired = 4;
      bool agent_match = 5;
    }
    ```

---

### Get Agent Trust Score

Retrieve the current trust score for an agent.

```http
GET /api/v1/agent/{agent_id}/trust-score

Response (200 OK):
{
  "agent_id": "agent:service-alpha",
  "trust_score": 72,
  "tier": "analyst",
  "e_base": 85,
  "risk_factor": 0.15,
  "last_updated": "2026-01-02T14:30:00Z",
  "trajectory_hash": "sha256:abc123..."
}
```

---

## Agent Registry API

### Register Agent

Register a new agent with the KTP zone.

```http
POST /api/v1/agents
Content-Type: application/json

{
  "agent_id": "agent:service-alpha",
  "name": "Alpha Microservice",
  "capabilities": ["read:data", "write:logs"],
  "metadata": {
    "version": "1.2.3",
    "environment": "production"
  },
  "sponsor": "agent:team-backend"
}

Response (201 Created):
{
  "agent_id": "agent:service-alpha",
  "registered_at": "2026-01-02T14:00:00Z",
  "initial_trust_score": 40,
  "tier": "analyst",
  "genesis_block": "hash:genesis-abc123"
}
```

---

### Update Agent Metadata

```http
PATCH /api/v1/agents/{agent_id}
Content-Type: application/json

{
  "metadata": {
    "version": "1.2.4"
  }
}

Response (200 OK):
{
  "agent_id": "agent:service-alpha",
  "updated_at": "2026-01-02T15:00:00Z"
}
```

---

### Deregister Agent

```http
DELETE /api/v1/agents/{agent_id}

Response (204 No Content)
```

---

## Context Tensor API

### Submit Sensor Data

Submit real-time context data to the Oracle.

```http
POST /api/v1/context-tensor
Content-Type: application/json

{
  "agent_id": "agent:service-alpha",
  "dimensions": {
    "body.hardware.cpu": 0.45,
    "body.hardware.memory": 0.67,
    "world.network.latency": 0.12
  },
  "timestamp": "2026-01-02T14:30:00Z"
}

Response (202 Accepted):
{
  "tensor_id": "tensor-uuid-67890",
  "accepted_dimensions": 3,
  "rejected_dimensions": 0
}
```

---

### Get Context Tensor

Retrieve the current context tensor for an agent.

```http
GET /api/v1/context-tensor/{agent_id}

Response (200 OK):
{
  "agent_id": "agent:service-alpha",
  "dimensions": {
    "soul": { "value": 0.05, "weight": 3.0 },
    "body": { "value": 0.56, "weight": 1.0 },
    "world": { "value": 0.23, "weight": 1.5 },
    "time": { "value": 0.10, "weight": 1.0 },
    "relational": { "value": 0.15, "weight": 1.2 },
    "signal": { "value": 0.18, "weight": 1.0 }
  },
  "risk_factor": 0.15,
  "last_updated": "2026-01-02T14:30:00Z"
}
```

---

## Policy Enforcement API

### Enforce Decision

Make an authorization decision based on a trust proof.

```http
POST /api/v1/enforce
Content-Type: application/json

{
  "proof_id": "proof-uuid-12345",
  "action": {
    "type": "database:read",
    "resource": "users-table",
    "risk_level": 45
  }
}

Response (200 OK):
{
  "decision": "allow",
  "reason": "trust_score >= risk_level (72 >= 45)",
  "audit_id": "audit-uuid-99999",
  "recorded_at": "2026-01-02T14:30:01Z"
}
```

**Decision Values**:
- `allow`: Action permitted
- `deny`: Action denied (trust insufficient)
- `veto`: Silent veto (Soul constraint triggered)

---

## Audit API (Flight Recorder)

### Query Audit Logs

```http
GET /api/v1/audit/logs?agent_id={agent_id}&from={timestamp}&to={timestamp}

Response (200 OK):
{
  "total": 1247,
  "logs": [
    {
      "record_id": "audit-uuid-99999",
      "timestamp": "2026-01-02T14:30:01Z",
      "agent_id": "agent:service-alpha",
      "action": "database:read",
      "decision": "allow",
      "trust_score": 72,
      "risk_level": 45,
      "chain_hash": "sha256:prev-abc123"
    }
  ]
}
```

---

### Get Decision Geometry

Retrieve detailed decision context for forensics.

```http
GET /api/v1/audit/{record_id}/geometry

Response (200 OK):
{
  "record_id": "audit-uuid-99999",
  "timestamp": "2026-01-02T14:30:01Z",
  "agent": {
    "id": "agent:service-alpha",
    "e_base": 85,
    "e_trust": 72,
    "tier": "analyst"
  },
  "environment": {
    "context_tensor": { "m": 0.56, "p": 0.23, "h": 0.10 },
    "risk_factor": 0.15
  },
  "decision": {
    "outcome": "allow",
    "reason": "trust_score >= risk_level",
    "constraint": null
  }
}
```

---

## WebSocket API (Real-Time)

### Subscribe to Trust Updates

```javascript
const ws = new WebSocket('wss://oracle.yourzone.ktp/api/v1/stream');

ws.send(JSON.stringify({
  type: 'subscribe',
  agent_id: 'agent:service-alpha',
  events: ['trust_score', 'veto', 'zone_alert']
}));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'trust_score':
      console.log(`Score: ${data.old_score} → ${data.new_score}`);
      break;
    case 'veto':
      console.log(`VETO: ${data.reason}`);
      break;
    case 'zone_alert':
      console.log(`ALERT: ${data.message}`);
      break;
  }
};
```

**Event Types**:

| Type | Description |
|------|-------------|
| `trust_score` | Trust score changed |
| `veto` | Silent veto triggered |
| `tier_change` | Trust tier changed |
| `zone_alert` | Zone-wide security alert |
| `proof_invalidated` | Trust proof was invalidated |

---

## Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/trust-proof` | 100 requests | per second |
| `/trust-proof/verify` | 1000 requests | per second |
| `/context-tensor` | 10 requests | per second |
| `/audit/logs` | 10 requests | per minute |

Exceeding rate limits returns `429 Too Many Requests`.

---

## Data Models

### Trust Proof Schema

```json
{
  "proof_id": "string (uuid)",
  "agent_id": "string",
  "trust_score": "integer (0-100)",
  "tier": "enum(observer|analyst|operator|architect|god-mode)",
  "e_base": "integer (0-100)",
  "e_trust": "integer (0-100)",
  "risk_factor": "float (0.0-1.0)",
  "issued_at": "timestamp (ISO 8601)",
  "expires_at": "timestamp (ISO 8601)",
  "signature": "string (base64)",
  "oracle_quorum": "array[string]"
}
```

### Context Tensor Schema

```json
{
  "agent_id": "string",
  "dimensions": {
    "soul": { "value": "float", "weight": "float" },
    "body": { "value": "float", "weight": "float" },
    "world": { "value": "float", "weight": "float" },
    "time": { "value": "float", "weight": "float" },
    "relational": { "value": "float", "weight": "float" },
    "signal": { "value": "float", "weight": "float" }
  },
  "risk_factor": "float (0.0-1.0)",
  "last_updated": "timestamp (ISO 8601)"
}
```

---

## SDK Code Generation

Generate client code from our OpenAPI spec:

```bash
# Download the OpenAPI spec
curl -O https://oracle.yourzone.ktp/api/v1/openapi.json

# Generate Python client
openapi-generator-cli generate \
  -i openapi.json \
  -g python \
  -o ./ktp-client-python

# Generate TypeScript client
openapi-generator-cli generate \
  -i openapi.json \
  -g typescript-fetch \
  -o ./ktp-client-ts
```

Or use our official SDKs from [SDKs & Libraries](sdks-and-libraries.md).

---

## Related Resources

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **[Developer Guide](developer-guide.md)**

    ---

    Step-by-step integration tutorial.

-   :material-code-tags:{ .lg .middle } **[Examples](examples.md)**

    ---

    Working code samples for all endpoints.

-   :material-lan:{ .lg .middle } **[KTP-Transport](../rfcs/ktp-transport.md)**

    ---

    Protocol specification and transport details.

-   :material-shield-lock:{ .lg .middle } **[KTP-Crypto](../rfcs/ktp-crypto.md)**

    ---

    Cryptographic primitives and signature schemes.

</div>
