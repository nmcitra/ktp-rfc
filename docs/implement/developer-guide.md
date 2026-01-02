# Developer Guide

*From Zero to Production-Ready KTP Integration*

---

This guide walks you through integrating the Kinetic Trust Protocol into your application, from initial setup to production deployment.

## Prerequisites

Before you begin, ensure you have:

- [ ] Basic understanding of [KTP Core Concepts](../learn/core-concepts.md)
- [ ] Access to a KTP Blue Zone (or local test environment)
- [ ] Development environment for your chosen language (Python 3.9+, Node.js 18+, Rust 1.70+, or Go 1.21+)
- [ ] Familiarity with REST APIs and basic cryptography concepts

---

## Part 1: Environment Setup

### Step 1: Install the SDK

=== "Python"
    ```bash
    pip install ktp-sdk
    # Or with specific extras
    pip install ktp-sdk[async,crypto]
    ```

=== "JavaScript/TypeScript"
    ```bash
    npm install @ktp/sdk
    # Or with yarn
    yarn add @ktp/sdk
    ```

=== "Rust"
    ```toml
    [dependencies]
    ktp-sdk = "0.1.0"
    tokio = { version = "1.0", features = ["full"] }
    ```

=== "Go"
    ```bash
    go get github.com/ktp-protocol/ktp-go
    ```

### Step 2: Configure Your Connection

Create a configuration file to connect to your KTP zone:

=== "Python"
    ```python
    # config.py
    KTP_CONFIG = {
        "zone_url": "https://oracle.yourzone.ktp",
        "zone_id": "blue:production",
        "agent_id": "agent:service-alpha",
        "credentials": {
            "key_file": "/path/to/private-key.pem",
            "cert_file": "/path/to/certificate.pem"
        },
        "timeout": 5.0,  # seconds
        "retry_policy": {
            "max_attempts": 3,
            "backoff": "exponential"
        }
    }
    ```

=== "JavaScript"
    ```javascript
    // config.js
    export const ktpConfig = {
      zoneUrl: 'https://oracle.yourzone.ktp',
      zoneId: 'blue:production',
      agentId: 'agent:service-alpha',
      credentials: {
        keyFile: '/path/to/private-key.pem',
        certFile: '/path/to/certificate.pem'
      },
      timeout: 5000, // milliseconds
      retryPolicy: {
        maxAttempts: 3,
        backoff: 'exponential'
      }
    };
    ```

### Step 3: Verify Connection

Test your connection to the KTP Oracle:

=== "Python"
    ```python
    from ktp import TrustOracle
    from config import KTP_CONFIG
    
    oracle = TrustOracle(KTP_CONFIG)
    
    # Ping the oracle
    if oracle.ping():
        print("✓ Connected to KTP Oracle")
        print(f"Zone: {oracle.zone_info.name}")
        print(f"Trust Level: {oracle.zone_info.level}")
    else:
        print("✗ Connection failed")
    ```

=== "JavaScript"
    ```javascript
    import { TrustOracle } from '@ktp/sdk';
    import { ktpConfig } from './config.js';
    
    const oracle = new TrustOracle(ktpConfig);
    
    // Ping the oracle
    const connected = await oracle.ping();
    if (connected) {
      console.log('✓ Connected to KTP Oracle');
      const info = await oracle.getZoneInfo();
      console.log(`Zone: ${info.name}`);
      console.log(`Trust Level: ${info.level}`);
    } else {
      console.log('✗ Connection failed');
    }
    ```

---

## Part 2: Agent Registration

### Step 4: Create Your Agent Identity

Every entity in KTP is an **Agent** with a unique identity and capabilities:

=== "Python"
    ```python
    from ktp import Agent, Capability
    
    agent = Agent(
        id="agent:service-alpha",
        name="Alpha Microservice",
        capabilities=[
            Capability.READ_DATA,
            Capability.WRITE_LOGS,
            Capability.EXECUTE_QUERY
        ],
        metadata={
            "version": "1.2.3",
            "environment": "production",
            "owner": "team-backend"
        }
    )
    
    # Register with the Oracle
    registration = oracle.register_agent(agent)
    print(f"Agent registered: {registration.agent_id}")
    print(f"Initial trust score: {registration.trust_score}")
    ```

=== "JavaScript"
    ```javascript
    import { Agent, Capability } from '@ktp/sdk';
    
    const agent = new Agent({
      id: 'agent:service-alpha',
      name: 'Alpha Microservice',
      capabilities: [
        Capability.READ_DATA,
        Capability.WRITE_LOGS,
        Capability.EXECUTE_QUERY
      ],
      metadata: {
        version: '1.2.3',
        environment: 'production',
        owner: 'team-backend'
      }
    });
    
    // Register with the Oracle
    const registration = await oracle.registerAgent(agent);
    console.log(`Agent registered: ${registration.agentId}`);
    console.log(`Initial trust score: ${registration.trustScore}`);
    ```

!!! tip "Agent Naming Convention"
    Use the format `agent:<service-name>` for microservices or `agent:<user-id>` for user-facing agents.

---

## Part 3: Trust Proof Workflow

### Step 5: Request a Trust Proof

Before performing any action, your agent must request a **Trust Proof** from the Oracle:

=== "Python"
    ```python
    from ktp import TrustProofRequest
    
    # Request a proof
    proof_request = TrustProofRequest(
        agent_id=agent.id,
        action="database:read",
        resource="users-table",
        context={
            "ip_address": "10.0.1.42",
            "session_age": 3600,  # seconds
            "previous_actions": 127
        }
    )
    
    proof = oracle.request_proof(proof_request)
    
    print(f"Trust Score: {proof.score}")
    print(f"Tier: {proof.tier}")  # observer, analyst, operator, etc.
    print(f"Valid Until: {proof.expires_at}")
    print(f"Signature: {proof.signature[:32]}...")
    ```

=== "JavaScript"
    ```javascript
    import { TrustProofRequest } from '@ktp/sdk';
    
    // Request a proof
    const proofRequest = new TrustProofRequest({
      agentId: agent.id,
      action: 'database:read',
      resource: 'users-table',
      context: {
        ipAddress: '10.0.1.42',
        sessionAge: 3600, // seconds
        previousActions: 127
      }
    });
    
    const proof = await oracle.requestProof(proofRequest);
    
    console.log(`Trust Score: ${proof.score}`);
    console.log(`Tier: ${proof.tier}`);
    console.log(`Valid Until: ${proof.expiresAt}`);
    console.log(`Signature: ${proof.signature.substring(0, 32)}...`);
    ```

### Step 6: Verify and Enforce

At your **Policy Enforcement Point** (PEP), verify the proof and enforce the $A \leq E$ constraint:

=== "Python"
    ```python
    from ktp import PolicyEnforcementPoint, Action
    
    pep = PolicyEnforcementPoint(oracle)
    
    # Define the action
    action = Action(
        type="database:read",
        resource="users-table",
        risk_level=45  # Analyst tier required (≥40)
    )
    
    # Enforce the decision
    decision = pep.enforce(proof, action)
    
    if decision.allowed:
        print("✓ Action authorized")
        result = execute_database_read()
    else:
        print(f"✗ Action denied: {decision.reason}")
        log_denial(agent.id, action, decision.reason)
    ```

=== "JavaScript"
    ```javascript
    import { PolicyEnforcementPoint, Action } from '@ktp/sdk';
    
    const pep = new PolicyEnforcementPoint(oracle);
    
    // Define the action
    const action = new Action({
      type: 'database:read',
      resource: 'users-table',
      riskLevel: 45  // Analyst tier required (≥40)
    });
    
    // Enforce the decision
    const decision = await pep.enforce(proof, action);
    
    if (decision.allowed) {
      console.log('✓ Action authorized');
      const result = await executeDatabaseRead();
    } else {
      console.log(`✗ Action denied: ${decision.reason}`);
      await logDenial(agent.id, action, decision.reason);
    }
    ```

---

## Part 4: Context Tensor Integration

### Step 7: Configure Sensors

KTP's trust decisions are based on **Context Tensors**—real-time environmental measurements:

=== "Python"
    ```python
    from ktp import ContextSensor, SensorFeed
    
    # Create sensor feeds
    cpu_sensor = SensorFeed(
        dimension="body.hardware.cpu",
        source="local://system/cpu",
        weight=1.0,
        refresh_interval_ms=5000
    )
    
    memory_sensor = SensorFeed(
        dimension="body.hardware.memory",
        source="local://system/memory",
        weight=1.0,
        refresh_interval_ms=5000
    )
    
    network_sensor = SensorFeed(
        dimension="world.network.latency",
        source="prometheus://metrics/network_latency",
        weight=0.8,
        refresh_interval_ms=10000
    )
    
    # Register sensors
    sensor = ContextSensor(oracle)
    sensor.register_feeds([cpu_sensor, memory_sensor, network_sensor])
    
    # Start streaming context data
    sensor.start()
    print("✓ Context sensors active")
    ```

=== "JavaScript"
    ```javascript
    import { ContextSensor, SensorFeed } from '@ktp/sdk';
    
    // Create sensor feeds
    const cpuSensor = new SensorFeed({
      dimension: 'body.hardware.cpu',
      source: 'local://system/cpu',
      weight: 1.0,
      refreshIntervalMs: 5000
    });
    
    const memorySensor = new SensorFeed({
      dimension: 'body.hardware.memory',
      source: 'local://system/memory',
      weight: 1.0,
      refreshIntervalMs: 5000
    });
    
    const networkSensor = new SensorFeed({
      dimension: 'world.network.latency',
      source: 'prometheus://metrics/network_latency',
      weight: 0.8,
      refreshIntervalMs: 10000
    });
    
    // Register sensors
    const sensor = new ContextSensor(oracle);
    await sensor.registerFeeds([cpuSensor, memorySensor, networkSensor]);
    
    // Start streaming context data
    await sensor.start();
    console.log('✓ Context sensors active');
    ```

---

## Part 5: Real-Time Trust Updates

### Step 8: Subscribe to Trust Score Changes

For long-running processes, subscribe to real-time trust updates via WebSocket:

=== "Python"
    ```python
    from ktp import TrustStream
    
    stream = TrustStream(oracle, agent_id=agent.id)
    
    @stream.on_score_change
    def handle_score_change(event):
        print(f"Trust score changed: {event.old_score} → {event.new_score}")
        print(f"Reason: {event.reason}")
        
        if event.new_score < 40:  # Dropped below Analyst tier
            print("⚠ Trust degraded - reducing autonomy")
            throttle_operations()
    
    @stream.on_veto
    def handle_veto(event):
        print(f"🛑 SILENT VETO: {event.reason}")
        emergency_shutdown()
    
    stream.connect()
    ```

=== "JavaScript"
    ```javascript
    import { TrustStream } from '@ktp/sdk';
    
    const stream = new TrustStream(oracle, { agentId: agent.id });
    
    stream.onScoreChange((event) => {
      console.log(`Trust score changed: ${event.oldScore} → ${event.newScore}`);
      console.log(`Reason: ${event.reason}`);
      
      if (event.newScore < 40) {  // Dropped below Analyst tier
        console.log('⚠ Trust degraded - reducing autonomy');
        throttleOperations();
      }
    });
    
    stream.onVeto((event) => {
      console.log(`🛑 SILENT VETO: ${event.reason}`);
      emergencyShutdown();
    });
    
    await stream.connect();
    ```

---

## Part 6: Error Handling

### Step 9: Implement Robust Error Handling

=== "Python"
    ```python
    from ktp import (
        TrustProofExpiredError,
        InsufficientTrustError,
        OracleUnreachableError,
        SoulVetoError
    )
    
    try:
        proof = oracle.request_proof(proof_request)
        decision = pep.enforce(proof, action)
        
        if decision.allowed:
            result = execute_action()
        else:
            handle_denial(decision)
            
    except TrustProofExpiredError:
        # Proof expired - request a new one
        proof = oracle.request_proof(proof_request)
        retry_enforcement(proof, action)
        
    except InsufficientTrustError as e:
        # Trust score too low
        log_error(f"Insufficient trust: {e.score} < {e.required}")
        notify_operator(agent.id, "Trust degradation")
        
    except OracleUnreachableError:
        # Network failure - fail closed
        log_error("Oracle unreachable - denying action")
        deny_action(action)
        
    except SoulVetoError as e:
        # Hard veto from Soul constraint
        log_critical(f"SOUL VETO: {e.reason}")
        emergency_shutdown()
        alert_security_team(agent.id, e.reason)
    ```

=== "JavaScript"
    ```javascript
    import {
      TrustProofExpiredError,
      InsufficientTrustError,
      OracleUnreachableError,
      SoulVetoError
    } from '@ktp/sdk';
    
    try {
      const proof = await oracle.requestProof(proofRequest);
      const decision = await pep.enforce(proof, action);
      
      if (decision.allowed) {
        const result = await executeAction();
      } else {
        await handleDenial(decision);
      }
      
    } catch (error) {
      if (error instanceof TrustProofExpiredError) {
        // Proof expired - request a new one
        const proof = await oracle.requestProof(proofRequest);
        await retryEnforcement(proof, action);
        
      } else if (error instanceof InsufficientTrustError) {
        // Trust score too low
        await logError(`Insufficient trust: ${error.score} < ${error.required}`);
        await notifyOperator(agent.id, 'Trust degradation');
        
      } else if (error instanceof OracleUnreachableError) {
        // Network failure - fail closed
        await logError('Oracle unreachable - denying action');
        await denyAction(action);
        
      } else if (error instanceof SoulVetoError) {
        // Hard veto from Soul constraint
        await logCritical(`SOUL VETO: ${error.reason}`);
        await emergencyShutdown();
        await alertSecurityTeam(agent.id, error.reason);
      }
    }
    ```

---

## Part 7: Testing

### Step 10: Run Conformance Tests

Before production deployment, validate your implementation:

```bash
# Run the official KTP test suite
ktp-test --level basic --config config.yaml

# Output:
# ✓ Connection to Oracle (5/5 tests passed)
# ✓ Agent Registration (3/3 tests passed)
# ✓ Trust Proof Workflow (8/8 tests passed)
# ✓ Context Tensor Integration (4/4 tests passed)
# ⚠ Stress Test (2/3 tests passed - latency spike under load)
#
# Result: PASSED (22/23 tests)
# Conformance Level: Basic ✓
```

---

## Part 8: Production Deployment

### Step 11: Production Checklist

Before going live, verify:

- [ ] **Security**
    - [ ] Private keys stored in HSM or secure vault
    - [ ] mTLS enabled for Oracle communication
    - [ ] Audit logging configured
    - [ ] Security review completed

- [ ] **Reliability**
    - [ ] Oracle mesh has ≥3 nodes (for Standard level)
    - [ ] Failover and retry logic tested
    - [ ] Monitoring and alerting configured
    - [ ] Backup Oracle endpoints configured

- [ ] **Performance**
    - [ ] Trust proof caching implemented
    - [ ] Latency impact measured (<10ms target)
    - [ ] Load testing completed
    - [ ] Context sensor overhead acceptable

- [ ] **Compliance**
    - [ ] [Conformance tests](../rfcs/ktp-conformance.md) passed
    - [ ] [Threat model](../rfcs/ktp-threat-model.md) reviewed
    - [ ] Privacy impact assessment completed
    - [ ] Runbook for incident response

---

## Next Steps

Now that you have a working KTP integration:

- **Explore the [API Reference](api-reference.md)** for advanced features
- **Review [Examples](examples.md)** for integration patterns
- **Check out [SDKs & Libraries](sdks-and-libraries.md)** for language-specific tools
- **Read [KTP-Migration](../rfcs/ktp-migration.md)** for guidance on migrating legacy systems

---

## Related Specifications

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **[KTP-Core](../rfcs/ktp-core.md)**

    ---

    The foundational protocol and the Zeroth Law ($A \leq E$).

-   :material-cube-outline:{ .lg .middle } **[KTP-Tensors](../rfcs/ktp-tensors.md)**

    ---

    Complete Context Tensor specification (1,707 dimensions).

-   :material-lan:{ .lg .middle } **[KTP-Transport](../rfcs/ktp-transport.md)**

    ---

    Network protocols for KTP communication.

-   :material-shield-check:{ .lg .middle } **[KTP-Conformance](../rfcs/ktp-conformance.md)**

    ---

    Testing requirements and certification procedures.

</div>
