# SDKs & Libraries

*Official and Community Tools for KTP Integration*

---

Choose from our official SDKs or explore community-maintained libraries to integrate KTP into your application.

## Official SDKs

### Python SDK

The most mature and feature-complete SDK, recommended for backend services and data science applications.

=== "Installation"
    ```bash
    # Basic installation
    pip install ktp-sdk
    
    # With async support
    pip install ktp-sdk[async]
    
    # With cryptography extras
    pip install ktp-sdk[crypto]
    
    # Full installation
    pip install ktp-sdk[all]
    ```

=== "Quick Start"
    ```python
    from ktp import TrustOracle, Agent, TrustProofRequest
    
    # Initialize Oracle connection
    oracle = TrustOracle(
        zone_url="https://oracle.yourzone.ktp",
        zone_id="blue:production",
        credentials="/path/to/cert.pem"
    )
    
    # Register your agent
    agent = Agent(
        id="agent:myservice",
        capabilities=["read:data", "write:logs"]
    )
    oracle.register_agent(agent)
    
    # Request trust proof
    proof = oracle.request_proof(TrustProofRequest(
        agent_id=agent.id,
        action="data:read",
        resource="database:users"
    ))
    
    print(f"Trust Score: {proof.score}")
    ```

=== "Features"
    - ✅ REST and gRPC support
    - ✅ Async/await with `asyncio`
    - ✅ WebSocket streaming
    - ✅ Automatic proof caching
    - ✅ Circuit breaker pattern
    - ✅ Comprehensive type hints
    - ✅ Django and Flask integrations

**Package Info**:
- **Latest Version**: 0.1.0
- **Python**: ≥3.9
- **License**: Apache 2.0
- **Repository**: [github.com/ktp-protocol/ktp-python](https://github.com/ktp-protocol/ktp-python)
- **Documentation**: [docs.ktp.dev/python](https://docs.ktp.dev/python)

---

### JavaScript/TypeScript SDK

Full-featured SDK for Node.js backends and browser-based applications.

=== "Installation"
    ```bash
    # npm
    npm install @ktp/sdk
    
    # yarn
    yarn add @ktp/sdk
    
    # pnpm
    pnpm add @ktp/sdk
    ```

=== "Quick Start"
    ```typescript
    import { TrustOracle, Agent, TrustProofRequest } from '@ktp/sdk';
    
    // Initialize Oracle connection
    const oracle = new TrustOracle({
      zoneUrl: 'https://oracle.yourzone.ktp',
      zoneId: 'blue:production',
      credentials: '/path/to/cert.pem'
    });
    
    // Register your agent
    const agent = new Agent({
      id: 'agent:myservice',
      capabilities: ['read:data', 'write:logs']
    });
    await oracle.registerAgent(agent);
    
    // Request trust proof
    const proof = await oracle.requestProof({
      agentId: agent.id,
      action: 'data:read',
      resource: 'database:users'
    });
    
    console.log(`Trust Score: ${proof.score}`);
    ```

=== "Features"
    - ✅ Full TypeScript support
    - ✅ Promise-based async API
    - ✅ WebSocket streaming
    - ✅ React hooks (`useKTP`, `useTrustScore`)
    - ✅ Express.js middleware
    - ✅ Next.js integration
    - ✅ Browser and Node.js compatible

**Package Info**:
- **Latest Version**: 0.1.0
- **Node.js**: ≥18.0
- **TypeScript**: ≥5.0
- **License**: Apache 2.0
- **Repository**: [github.com/ktp-protocol/ktp-js](https://github.com/ktp-protocol/ktp-js)
- **Documentation**: [docs.ktp.dev/js](https://docs.ktp.dev/js)

---

### Rust SDK

High-performance SDK for systems programming and embedded applications.

=== "Installation"
    ```toml
    [dependencies]
    ktp-sdk = "0.1.0"
    tokio = { version = "1.0", features = ["full"] }
    ```

=== "Quick Start"
    ```rust
    use ktp_sdk::{TrustOracle, Agent, TrustProofRequest};
    
    #[tokio::main]
    async fn main() -> Result<(), Box<dyn std::error::Error>> {
        // Initialize Oracle connection
        let oracle = TrustOracle::new(
            "https://oracle.yourzone.ktp",
            "blue:production",
            "/path/to/cert.pem"
        ).await?;
        
        // Register agent
        let agent = Agent::new("agent:myservice")
            .with_capabilities(vec!["read:data", "write:logs"]);
        oracle.register_agent(&agent).await?;
        
        // Request trust proof
        let proof = oracle.request_proof(TrustProofRequest {
            agent_id: agent.id,
            action: "data:read".into(),
            resource: "database:users".into(),
            ..Default::default()
        }).await?;
        
        println!("Trust Score: {}", proof.score);
        
        Ok(())
    }
    ```

=== "Features"
    - ✅ Zero-copy serialization
    - ✅ Async runtime (Tokio)
    - ✅ gRPC support (Tonic)
    - ✅ WebAssembly compatible
    - ✅ No unsafe code
    - ✅ Comprehensive error types
    - ✅ HTTP/2 connection pooling

**Package Info**:
- **Latest Version**: 0.1.0
- **Rust**: ≥1.70
- **License**: Apache 2.0
- **Repository**: [github.com/ktp-protocol/ktp-rust](https://github.com/ktp-protocol/ktp-rust)
- **Documentation**: [docs.rs/ktp-sdk](https://docs.rs/ktp-sdk)

---

### Go SDK

Lightweight SDK for microservices and cloud-native applications.

=== "Installation"
    ```bash
    go get github.com/ktp-protocol/ktp-go
    ```

=== "Quick Start"
    ```go
    package main
    
    import (
        "context"
        "fmt"
        "log"
        
        "github.com/ktp-protocol/ktp-go"
    )
    
    func main() {
        // Initialize Oracle connection
        oracle, err := ktp.NewTrustOracle(
            "https://oracle.yourzone.ktp",
            ktp.WithZoneID("blue:production"),
            ktp.WithCredentials("/path/to/cert.pem"),
        )
        if err != nil {
            log.Fatal(err)
        }
        defer oracle.Close()
        
        // Register agent
        agent := &ktp.Agent{
            ID:           "agent:myservice",
            Capabilities: []string{"read:data", "write:logs"},
        }
        if err := oracle.RegisterAgent(context.Background(), agent); err != nil {
            log.Fatal(err)
        }
        
        // Request trust proof
        proof, err := oracle.RequestProof(context.Background(), &ktp.TrustProofRequest{
            AgentID:  agent.ID,
            Action:   "data:read",
            Resource: "database:users",
        })
        if err != nil {
            log.Fatal(err)
        }
        
        fmt.Printf("Trust Score: %d\n", proof.Score)
    }
    ```

=== "Features"
    - ✅ Standard library `context` support
    - ✅ gRPC and HTTP/2
    - ✅ Connection pooling
    - ✅ Structured logging (slog)
    - ✅ Graceful shutdown
    - ✅ Metrics (Prometheus)
    - ✅ Zero dependencies (core)

**Package Info**:
- **Latest Version**: 0.1.0
- **Go**: ≥1.21
- **License**: Apache 2.0
- **Repository**: [github.com/ktp-protocol/ktp-go](https://github.com/ktp-protocol/ktp-go)
- **Documentation**: [pkg.go.dev/github.com/ktp-protocol/ktp-go](https://pkg.go.dev/github.com/ktp-protocol/ktp-go)

---

## Language Support Matrix

| Feature | Python | JS/TS | Rust | Go | Java | C# |
|---------|:------:|:-----:|:----:|:--:|:----:|:--:|
| **REST API** | ✅ | ✅ | ✅ | ✅ | 🚧 | 🚧 |
| **gRPC** | ✅ | ✅ | ✅ | ✅ | 🚧 | 🚧 |
| **WebSocket** | ✅ | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **Async/Await** | ✅ | ✅ | ✅ | ✅ | 🚧 | 🚧 |
| **Type Safety** | ⚠️ | ✅ | ✅ | ⚠️ | 🚧 | 🚧 |
| **Browser Support** | ❌ | ✅ | ⚠️ | ❌ | ❌ | ❌ |
| **Proof Caching** | ✅ | ✅ | ✅ | ✅ | 🚧 | 🚧 |

**Legend**: ✅ Fully Supported | ⚠️ Partial Support | 🚧 In Development | ❌ Not Supported

---

## Community Libraries

### Java SDK (Community)

Maintained by [@ktp-community](https://github.com/ktp-community)

```xml
<!-- Maven -->
<dependency>
    <groupId>dev.ktp</groupId>
    <artifactId>ktp-sdk</artifactId>
    <version>0.1.0-beta</version>
</dependency>
```

```java
// Quick example
TrustOracle oracle = TrustOracle.builder()
    .zoneUrl("https://oracle.yourzone.ktp")
    .zoneId("blue:production")
    .build();

TrustProof proof = oracle.requestProof(
    TrustProofRequest.builder()
        .agentId("agent:myservice")
        .action("data:read")
        .build()
);

System.out.println("Trust Score: " + proof.getScore());
```

**Status**: Beta | [Repository](https://github.com/ktp-community/ktp-java)

---

### C# SDK (Community)

Maintained by [@ktp-dotnet](https://github.com/ktp-dotnet)

```bash
dotnet add package KTP.SDK
```

```csharp
// Quick example
var oracle = new TrustOracle(
    zoneUrl: "https://oracle.yourzone.ktp",
    zoneId: "blue:production"
);

var proof = await oracle.RequestProofAsync(new TrustProofRequest
{
    AgentId = "agent:myservice",
    Action = "data:read",
    Resource = "database:users"
});

Console.WriteLine($"Trust Score: {proof.Score}");
```

**Status**: Beta | [Repository](https://github.com/ktp-dotnet/ktp-sdk)

---

## Framework Integrations

### Django

```python
# settings.py
INSTALLED_APPS = [
    ...
    'ktp.contrib.django',
]

KTP_CONFIG = {
    'ZONE_URL': 'https://oracle.yourzone.ktp',
    'ZONE_ID': 'blue:production',
    'MIN_TRUST_SCORE': 40,
}

# views.py
from ktp.contrib.django import require_trust

@require_trust(min_score=60)
def protected_view(request):
    trust_score = request.ktp.trust_score
    return JsonResponse({'trust_score': trust_score})
```

---

### Express.js

```javascript
import express from 'express';
import { ktpMiddleware } from '@ktp/express';

const app = express();

app.use(ktpMiddleware({
  zoneUrl: 'https://oracle.yourzone.ktp',
  zoneId: 'blue:production',
  minTrustScore: 40
}));

app.get('/api/data', (req, res) => {
  res.json({
    data: 'protected',
    trustScore: req.ktp.trustScore
  });
});
```

---

### FastAPI

```python
from fastapi import FastAPI, Depends
from ktp.contrib.fastapi import KTPAuth

app = FastAPI()
ktp_auth = KTPAuth(zone_url="https://oracle.yourzone.ktp")

@app.get("/api/data")
async def get_data(proof = Depends(ktp_auth.require(min_score=40))):
    return {"trust_score": proof.score}
```

---

## Tools & Utilities

### KTP CLI

Command-line tool for testing and debugging KTP integrations.

```bash
# Installation
pip install ktp-cli

# Connect to Oracle
ktp connect https://oracle.yourzone.ktp

# Register agent
ktp agent register agent:test --capabilities read:data,write:logs

# Request proof
ktp proof request agent:test --action data:read

# Watch trust score
ktp watch agent:test
```

**Repository**: [github.com/ktp-protocol/ktp-cli](https://github.com/ktp-protocol/ktp-cli)

---

### OpenAPI Generator Templates

Generate client SDKs from our OpenAPI specification.

```bash
# Download spec
curl -O https://oracle.yourzone.ktp/api/v1/openapi.json

# Generate clients
openapi-generator-cli generate \
  -i openapi.json \
  -g python \
  -o ./ktp-client-python \
  --additional-properties=packageName=ktp_client

# Available generators
openapi-generator-cli list
# python, javascript, typescript-fetch, rust, go, java, csharp, php, ruby, swift
```

---

### Protocol Buffers Definitions

For gRPC integration:

```bash
# Clone the repo
git clone https://github.com/ktp-protocol/proto

# Generate code
protoc --go_out=. --go-grpc_out=. proto/ktp/v1/*.proto
```

**Repository**: [github.com/ktp-protocol/proto](https://github.com/ktp-protocol/proto)

---

## Migration Guides

### From OAuth 2.0

```python
# Before (OAuth)
from oauthlib.oauth2 import BackendApplicationClient
client = BackendApplicationClient(client_id='your-client-id')

# After (KTP)
from ktp import TrustOracle, Agent
oracle = TrustOracle(zone_url="https://oracle.yourzone.ktp")
agent = Agent(id="agent:your-service")
```

See [KTP-Migration RFC](../rfcs/ktp-migration.md) for detailed guidance.

---

## Contributing

Want to contribute to KTP SDKs?

1. Check out our [Contribution Guidelines](https://github.com/ktp-protocol/ktp-python/blob/main/CONTRIBUTING.md)
2. Join the [Developer Slack](https://ktp-dev.slack.com)
3. Review [open issues](https://github.com/ktp-protocol/ktp-python/issues)

---

## Support & Resources

!!! tip "Need Help?"
    - **SDK Issues**: Open an issue on the respective GitHub repository
    - **Feature Requests**: [RFC Discussion Board](https://github.com/nmcitra/ktp-rfc/discussions)
    - **Security**: Email security@ktp.example
    - **Community**: [Discord](https://discord.gg/ktp) | [Slack](https://ktp-dev.slack.com)

---

## Related Resources

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **[Developer Guide](developer-guide.md)**

    ---

    Step-by-step integration tutorial.

-   :material-api:{ .lg .middle } **[API Reference](api-reference.md)**

    ---

    Complete API documentation.

-   :material-code-tags:{ .lg .middle } **[Examples](examples.md)**

    ---

    Working code samples for all SDKs.

-   :material-lan:{ .lg .middle } **[KTP-Transport](../rfcs/ktp-transport.md)**

    ---

    Protocol specification and wire formats.

</div>
