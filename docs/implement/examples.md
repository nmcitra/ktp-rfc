# Examples

*Working Code Samples and Integration Patterns*

---

This page provides production-ready code examples for common KTP integration scenarios. All examples are available in the [KTP Examples Repository](https://github.com/ktp-protocol/examples).

## Quick Navigation

<div class="grid cards" markdown>

-   :material-api:{ .lg .middle } **API Gateway Integration**

    ---

    Add KTP authorization to Nginx, Envoy, or Kong.

    [:octicons-arrow-right-24: Jump to section](#api-gateway-integration)

-   :material-application:{ .lg .middle } **Web Framework Middleware**

    ---

    Express.js, FastAPI, and Flask integration examples.

    [:octicons-arrow-right-24: Jump to section](#web-framework-middleware)

-   :material-database:{ .lg .middle } **Database Access Control**

    ---

    Enforce trust-based queries with PostgreSQL and MongoDB.

    [:octicons-arrow-right-24: Jump to section](#database-access-control)

-   :material-robot:{ .lg .middle } **Autonomous Agent Swarms**

    ---

    Build trust-constrained multi-agent systems.

    [:octicons-arrow-right-24: Jump to section](#autonomous-agent-swarms)

</div>

---

## API Gateway Integration

### Nginx with KTP Module

```nginx
# /etc/nginx/conf.d/ktp.conf

upstream ktp_oracle {
    server oracle-1.yourzone.ktp:443;
    server oracle-2.yourzone.ktp:443;
    server oracle-3.yourzone.ktp:443;
}

server {
    listen 443 ssl http2;
    server_name api.yourcompany.com;
    
    # KTP Module Configuration
    ktp_enabled on;
    ktp_oracle_url https://oracle.yourzone.ktp;
    ktp_zone_id blue:production;
    ktp_min_trust_score 40;  # Analyst tier
    ktp_proof_cache_ttl 20s;
    
    location /api/v1/users {
        # Require Operator tier (≥60) for user management
        ktp_action "user:management";
        ktp_min_trust_score 60;
        
        proxy_pass http://backend;
        proxy_set_header X-KTP-Agent-ID $ktp_agent_id;
        proxy_set_header X-KTP-Trust-Score $ktp_trust_score;
    }
    
    location /api/v1/data {
        # Standard Analyst tier (≥40) for data reads
        ktp_action "data:read";
        
        proxy_pass http://backend;
    }
}
```

### Envoy with KTP Filter

```yaml
# envoy.yaml

static_resources:
  listeners:
  - name: main_listener
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 8080
    filter_chains:
    - filters:
      - name: envoy.filters.network.http_connection_manager
        typed_config:
          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
          http_filters:
          
          # KTP Authorization Filter
          - name: envoy.filters.http.ktp_auth
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.ktp_auth.v3.KTPAuth
              oracle_cluster: ktp_oracle
              zone_id: "blue:production"
              min_trust_score: 40
              proof_cache_ttl: 20s
              
          - name: envoy.filters.http.router
            typed_config:
              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
              
  clusters:
  - name: ktp_oracle
    type: STRICT_DNS
    lb_policy: ROUND_ROBIN
    load_assignment:
      cluster_name: ktp_oracle
      endpoints:
      - lb_endpoints:
        - endpoint:
            address:
              socket_address:
                address: oracle.yourzone.ktp
                port_value: 443
    transport_socket:
      name: envoy.transport_sockets.tls
      typed_config:
        "@type": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext
```

---

## Web Framework Middleware

### Express.js (Node.js)

```javascript
// middleware/ktp-auth.js

const { TrustOracle, PolicyEnforcementPoint } = require('@ktp/sdk');

const oracle = new TrustOracle({
  zoneUrl: process.env.KTP_ORACLE_URL,
  zoneId: process.env.KTP_ZONE_ID
});

const pep = new PolicyEnforcementPoint(oracle);

/**
 * KTP Authorization Middleware
 * @param {number} minTrustScore - Minimum required trust score
 */
function ktpAuth(minTrustScore = 40) {
  return async (req, res, next) => {
    try {
      // Extract agent ID from header or JWT
      const agentId = req.headers['x-ktp-agent-id'] || req.user?.agentId;
      
      if (!agentId) {
        return res.status(401).json({ error: 'Missing agent ID' });
      }
      
      // Request trust proof
      const proof = await oracle.requestProof({
        agentId,
        action: `${req.method.toLowerCase()}:${req.path}`,
        resource: req.path,
        context: {
          ipAddress: req.ip,
          userAgent: req.headers['user-agent'],
          sessionAge: req.session?.age || 0
        }
      });
      
      // Enforce decision
      const decision = await pep.enforce(proof, {
        type: `${req.method.toLowerCase()}:${req.path}`,
        riskLevel: minTrustScore
      });
      
      if (!decision.allowed) {
        return res.status(403).json({
          error: 'Insufficient trust',
          reason: decision.reason,
          trustScore: proof.score,
          required: minTrustScore
        });
      }
      
      // Add trust info to request
      req.ktp = {
        proof,
        trustScore: proof.score,
        tier: proof.tier
      };
      
      next();
      
    } catch (error) {
      console.error('KTP Auth Error:', error);
      // Fail closed - deny on error
      return res.status(503).json({ error: 'Authorization service unavailable' });
    }
  };
}

module.exports = { ktpAuth };
```

**Usage**:

```javascript
// app.js

const express = require('express');
const { ktpAuth } = require('./middleware/ktp-auth');

const app = express();

// Public route - no KTP required
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// Protected route - Analyst tier required (≥40)
app.get('/api/data', ktpAuth(40), (req, res) => {
  res.json({
    data: 'sensitive information',
    trustScore: req.ktp.trustScore
  });
});

// High-security route - Operator tier required (≥60)
app.post('/api/users', ktpAuth(60), (req, res) => {
  // Create user logic
  res.json({ created: true });
});

app.listen(3000, () => {
  console.log('Server running with KTP authorization');
});
```

---

### FastAPI (Python)

```python
# middleware/ktp_auth.py

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ktp import TrustOracle, PolicyEnforcementPoint, TrustProofRequest, Action
import os

oracle = TrustOracle({
    "zone_url": os.getenv("KTP_ORACLE_URL"),
    "zone_id": os.getenv("KTP_ZONE_ID")
})

pep = PolicyEnforcementPoint(oracle)
security = HTTPBearer()

async def require_trust(
    min_score: int = 40,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    request: Request = None
):
    """
    Dependency for KTP authorization.
    
    Args:
        min_score: Minimum required trust score
        credentials: Bearer token containing agent ID
        request: FastAPI request object
    
    Raises:
        HTTPException: If trust is insufficient
    """
    try:
        # Extract agent ID from token
        agent_id = credentials.credentials  # Or decode JWT
        
        # Request trust proof
        proof = oracle.request_proof(TrustProofRequest(
            agent_id=agent_id,
            action=f"{request.method.lower()}:{request.url.path}",
            resource=request.url.path,
            context={
                "ip_address": request.client.host,
                "user_agent": request.headers.get("user-agent"),
                "method": request.method
            }
        ))
        
        # Enforce decision
        decision = pep.enforce(proof, Action(
            type=f"{request.method.lower()}:{request.url.path}",
            risk_level=min_score
        ))
        
        if not decision.allowed:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Insufficient trust",
                    "reason": decision.reason,
                    "trust_score": proof.score,
                    "required": min_score
                }
            )
        
        return proof
        
    except Exception as e:
        # Fail closed
        raise HTTPException(
            status_code=503,
            detail="Authorization service unavailable"
        )
```

**Usage**:

```python
# main.py

from fastapi import FastAPI, Depends
from middleware.ktp_auth import require_trust

app = FastAPI()

@app.get("/health")
async def health():
    """Public endpoint"""
    return {"status": "ok"}

@app.get("/api/data")
async def get_data(proof = Depends(lambda: require_trust(min_score=40))):
    """Protected endpoint - Analyst tier required"""
    return {
        "data": "sensitive information",
        "trust_score": proof.score,
        "tier": proof.tier
    }

@app.post("/api/users")
async def create_user(proof = Depends(lambda: require_trust(min_score=60))):
    """High-security endpoint - Operator tier required"""
    return {"created": True}
```

---

## Database Access Control

### PostgreSQL with KTP Row-Level Security

```python
# db/ktp_postgres.py

import psycopg2
from ktp import TrustOracle, PolicyEnforcementPoint
from contextlib import contextmanager

class KTPDatabase:
    """PostgreSQL wrapper with KTP enforcement"""
    
    def __init__(self, oracle: TrustOracle, db_config: dict):
        self.oracle = oracle
        self.pep = PolicyEnforcementPoint(oracle)
        self.conn = psycopg2.connect(**db_config)
        self._setup_rls()
    
    def _setup_rls(self):
        """Enable Row-Level Security with KTP"""
        with self.conn.cursor() as cur:
            # Enable RLS
            cur.execute("""
                ALTER TABLE users ENABLE ROW LEVEL SECURITY;
                
                -- Policy: Only agents with Operator tier (≥60) can see all users
                CREATE POLICY ktp_users_select ON users
                    FOR SELECT
                    USING (
                        current_setting('ktp.trust_score')::int >= 60
                        OR user_id = current_setting('ktp.agent_id')
                    );
                
                -- Policy: Only Architect tier (≥80) can modify users
                CREATE POLICY ktp_users_modify ON users
                    FOR UPDATE
                    USING (current_setting('ktp.trust_score')::int >= 80);
            """)
            self.conn.commit()
    
    @contextmanager
    def query(self, agent_id: str, action: str):
        """Execute query with KTP context"""
        
        # Get trust proof
        proof = self.oracle.request_proof({
            "agent_id": agent_id,
            "action": action,
            "resource": "database:users"
        })
        
        # Set session variables for RLS
        with self.conn.cursor() as cur:
            cur.execute("SET ktp.agent_id = %s", (agent_id,))
            cur.execute("SET ktp.trust_score = %s", (proof.score,))
            
            yield cur
            
            self.conn.commit()

# Usage
db = KTPDatabase(oracle, {"dbname": "mydb", "user": "postgres"})

with db.query(agent_id="agent:service-alpha", action="database:read") as cur:
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    # Will only return rows allowed by KTP policy
```

---

## Autonomous Agent Swarms

### Multi-Agent Coordination with KTP

```python
# agents/swarm.py

from ktp import TrustOracle, Agent, TrustStream
from typing import List, Callable
import asyncio

class KTPAgentSwarm:
    """Coordinate multiple agents with KTP constraints"""
    
    def __init__(self, oracle: TrustOracle):
        self.oracle = oracle
        self.agents: List[Agent] = []
        self.streams: dict = {}
    
    async def add_agent(self, agent: Agent):
        """Register agent and subscribe to trust updates"""
        
        # Register with Oracle
        registration = self.oracle.register_agent(agent)
        self.agents.append(agent)
        
        # Subscribe to trust updates
        stream = TrustStream(self.oracle, agent_id=agent.id)
        
        @stream.on_score_change
        def handle_score_change(event):
            print(f"[{agent.id}] Trust: {event.old_score} → {event.new_score}")
            
            # Adjust agent autonomy based on trust
            if event.new_score < 40:
                self.throttle_agent(agent.id)
            elif event.new_score >= 60:
                self.boost_agent(agent.id)
        
        @stream.on_veto
        def handle_veto(event):
            print(f"[{agent.id}] VETO: {event.reason}")
            self.halt_agent(agent.id)
        
        await stream.connect()
        self.streams[agent.id] = stream
    
    async def execute_task(
        self,
        task: dict,
        min_trust: int = 40
    ):
        """Execute task with highest-trust available agent"""
        
        # Get eligible agents
        eligible = []
        for agent in self.agents:
            proof = self.oracle.request_proof({
                "agent_id": agent.id,
                "action": task["type"],
                "resource": task.get("resource", "unknown")
            })
            
            if proof.score >= min_trust:
                eligible.append((agent, proof.score))
        
        if not eligible:
            raise Exception(f"No agent has sufficient trust (≥{min_trust})")
        
        # Select highest-trust agent
        best_agent, score = max(eligible, key=lambda x: x[1])
        
        print(f"Assigning task to {best_agent.id} (trust: {score})")
        return await self.run_task(best_agent, task)
    
    async def run_task(self, agent: Agent, task: dict):
        """Execute task with monitoring"""
        # Implementation specific to your use case
        pass
    
    def throttle_agent(self, agent_id: str):
        """Reduce agent autonomy"""
        print(f"Throttling {agent_id}")
    
    def boost_agent(self, agent_id: str):
        """Increase agent autonomy"""
        print(f"Boosting {agent_id}")
    
    def halt_agent(self, agent_id: str):
        """Emergency stop"""
        print(f"HALTING {agent_id}")

# Usage
oracle = TrustOracle({"zone_url": "https://oracle.yourzone.ktp"})
swarm = KTPAgentSwarm(oracle)

# Create agents
agent1 = Agent(id="agent:worker-1", capabilities=["compute", "analyze"])
agent2 = Agent(id="agent:worker-2", capabilities=["compute", "analyze"])

await swarm.add_agent(agent1)
await swarm.add_agent(agent2)

# Execute tasks
task = {
    "type": "data:analysis",
    "resource": "dataset-abc",
    "payload": {"query": "SELECT * FROM data"}
}

result = await swarm.execute_task(task, min_trust=40)
```

---

## Integration Patterns

### Circuit Breaker with KTP

```python
from ktp import TrustOracle, OracleUnreachableError
import time

class KTPCircuitBreaker:
    """Circuit breaker for KTP Oracle calls"""
    
    def __init__(self, oracle: TrustOracle, threshold: int = 5, timeout: int = 60):
        self.oracle = oracle
        self.failure_count = 0
        self.threshold = threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    def request_proof(self, proof_request):
        """Request proof with circuit breaker logic"""
        
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                # Fail fast
                raise Exception("Circuit breaker OPEN - Oracle unreachable")
        
        try:
            proof = self.oracle.request_proof(proof_request)
            
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            
            return proof
            
        except OracleUnreachableError:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.threshold:
                self.state = "open"
                print("Circuit breaker OPEN")
            
            raise
```

---

## Testing Examples

### Unit Test with Mock Oracle

```python
# tests/test_ktp_auth.py

import pytest
from unittest.mock import Mock, patch
from ktp import TrustProof

@pytest.fixture
def mock_oracle():
    """Mock KTP Oracle for testing"""
    oracle = Mock()
    
    # Mock trust proof response
    oracle.request_proof.return_value = TrustProof(
        proof_id="test-proof-123",
        agent_id="agent:test",
        trust_score=72,
        tier="analyst",
        e_base=85,
        e_trust=72,
        risk_factor=0.15
    )
    
    return oracle

def test_sufficient_trust(mock_oracle):
    """Test authorization with sufficient trust"""
    from your_app import authorize_action
    
    result = authorize_action(
        oracle=mock_oracle,
        agent_id="agent:test",
        action="data:read",
        min_trust=40
    )
    
    assert result.allowed == True
    assert result.trust_score == 72

def test_insufficient_trust(mock_oracle):
    """Test authorization with insufficient trust"""
    # Override mock for this test
    mock_oracle.request_proof.return_value.trust_score = 30
    
    result = authorize_action(
        oracle=mock_oracle,
        agent_id="agent:test",
        action="data:write",
        min_trust=60
    )
    
    assert result.allowed == False
```

---

## More Examples

Browse the complete example collection:

- **[Kubernetes Admission Controller](https://github.com/ktp-protocol/examples/tree/main/k8s-admission)**
- **[Service Mesh Integration (Istio)](https://github.com/ktp-protocol/examples/tree/main/istio)**
- **[Lambda Function Authorization (AWS)](https://github.com/ktp-protocol/examples/tree/main/aws-lambda)**
- **[CI/CD Pipeline Integration](https://github.com/ktp-protocol/examples/tree/main/cicd)**
- **[Real-time Monitoring Dashboard](https://github.com/ktp-protocol/examples/tree/main/monitoring)**

---

## Related Resources

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **[Developer Guide](developer-guide.md)**

    ---

    Step-by-step integration tutorial.

-   :material-api:{ .lg .middle } **[API Reference](api-reference.md)**

    ---

    Complete API documentation.

-   :material-package-variant:{ .lg .middle } **[SDKs & Libraries](sdks-and-libraries.md)**

    ---

    Official client libraries and tools.

-   :material-github:{ .lg .middle } **[Examples Repository](https://github.com/ktp-protocol/examples)**

    ---

    Full source code for all examples.

</div>
