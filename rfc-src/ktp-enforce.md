---
title: "Kinetic Trust Protocol (KTP) - Enforcement Layer Specification"
abbrev: "KTP-ENFORCE"
docname: draft-perkins-ktp-enforce-00
date: 2026-08-13
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  KTP-ZONES:
    title: "Kinetic Trust Protocol - Blue Zone Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-SENSORS:
    title: "Kinetic Trust Protocol - Context Signal Sensor Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  RFC2119:
  RFC8174:
informative:
  KTP-AUDIT:
    title: "Kinetic Trust Protocol - Flight Recorder Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-IDENTITY:
    title: "Kinetic Trust Protocol - Vector Identity Specification"
    author:
      - name: Chris Perkins
    date: 2025-11

--- abstract

This document specifies the Enforcement Layer for the Kinetic Trust Protocol (KTP). The Enforcement Layer is responsible for intercepting agent actions, evaluating them against Trust Proofs, and executing the Silent Veto when environmental constraints are violated.

The specification covers Policy Enforcement Points (PEPs), Trust Tiers with graduated capability levels, Adaptive Dormancy for graceful degradation, and integration patterns for common infrastructure components.

--- middle

# Introduction

The Enforcement Layer is where the constraint model becomes operational reality. While the Trust Oracle calculates what is possible, the Enforcement Layer ensures that only what is possible actually occurs.

Traditional authorization enforcement is binary: allowed or denied. KTP enforcement is graduated: actions may be allowed, denied, throttled, downgraded, or deferred based on the relationship between action risk and environmental capacity.

The graduated outcomes are one rail, and this specification names it: the prudence rail. Above the CAN question (A <= E_trust: can the environment support this action) sits a second, still amoral question — should the environment allow it now, with margin — and every graduated mechanism in this document answers it: throttling, downgrading, deferral, promotion hysteresis, the risk floor under suspicious conditions, deautomation as A approaches E_trust, and the Section 9.5 taxation trade. The rail is computed from the same measured environment as the CAN rail, and its disputes are measurement disputes: two deployments with identical sensors and identical declared parameters converge on its answers. It stays amoral only while its parameters are declared — this specification ships the mechanisms, the deployment declares the appetite, and an undeclared prudence constant is a smuggled norm. Normative judgment — ought this happen — is a different rail with a different home; see {{KTP-CORE}}'s carriage interface.

## Enforcement Philosophy

The core philosophy of KTP enforcement is:

"The environment has veto power over agent intent."

This inverts the traditional authorization model. Instead of asking "Is this agent permitted to perform this action?", KTP asks "Can this environment safely support this action right now?"

Key principles:

1. Silent Veto: Enforcement happens automatically, without human intervention. The environment constrains; it does not negotiate.

1. Graceful Degradation: When conditions degrade, agents don't fail catastrophically. They enter reduced capability modes, maintaining essential functions while shedding risky ones.

1. No Override: There is no emergency bypass. The only way to enable a high-risk action is to improve environmental conditions or reduce the action's risk classification.

1. Transparency: Every enforcement decision is logged with full context, enabling forensic reconstruction and system learning.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}}.

# Terminology

Action Risk (A): A numeric value (0-100) representing the intrinsic risk of a requested action, independent of who is requesting it.

Adaptive Dormancy: The progressive reduction of agent capabilities as environmental conditions degrade, allowing agents to "hibernate" rather than fail completely.

Capability Matrix: A mapping of Trust Tiers to permitted action classes, defining what each tier is allowed to do.

Effective Trust Score (E_trust): The current Trust Score after environmental deflation, used to determine the agent's Trust Tier.

Hibernation Mode: The most restrictive operational state, where an agent can only emit heartbeat signals and await recovery.

Policy Decision Point (PDP): The logical component that evaluates Trust Proofs and makes authorization decisions. In KTP, this is typically the Trust Oracle or a local cache.

Policy Enforcement Point (PEP): A component that intercepts agent requests and enforces PDP decisions by allowing, denying, or modifying actions.

Silent Veto: The automatic denial of an action when A > E_trust, executed without human intervention or appeal.

Soul Veto: The automatic denial of an action when sovereignty constraints are violated (S = 1), taking precedence over Trust Score evaluation.

Trust Tier: A capability level (Admin Mode, Operator Mode, Analyst Mode, Observer Mode) determined by E_trust thresholds.

# Architecture Overview

The Enforcement Layer sits between agents and protected resources, intercepting all actions and evaluating them against current environmental conditions.

~~~
+------------------------------------------------------------------+
|                         AGENT POPULATION                         |
|    [Sponsored Agents]  [Independent Agents]  [Guarantor Lineages]|
+------------------------------------------------------------------+
                                 |
                                 | Action Request
                                 v
+------------------------------------------------------------------+
|                      ENFORCEMENT LAYER                           |
|  +------------------------------------------------------------+  |
|  |                 Policy Enforcement Points                  |  |
|  |  +----------+  +----------+  +----------+  +----------+    |  |
|  |  | API GW   |  | Service  |  |   IAM    |  |    DB    |    |  |
|  |  |   PEP    |  | Mesh PEP |  |   PEP    |  |   PEP    |    |  |
|  |  +----------+  +----------+  +----------+  +----------+    |  |
|  +------------------------------------------------------------+  |
|                              |                                   |
|                              | Trust Proof Validation            |
|                              v                                   |
|  +------------------------------------------------------------+  |
|  |              Policy Decision Point (PDP)                   |  |
|  |   - Soul Veto Check                                        |  |
|  |   - Trust Tier Determination                               |  |
|  |   - Action Risk Evaluation                                 |  |
|  |   - A <= E_trust Verification                              |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
                                 |
                                 | Allowed Actions Only
                                 v
+------------------------------------------------------------------+
|                      PROTECTED RESOURCES                         |
|    [APIs]  [Databases]  [Services]  [Infrastructure]             |
+------------------------------------------------------------------+
~~~

Figure 1: Enforcement Layer Architecture

## Enforcement Flow

The standard enforcement flow for every action:

1. Agent submits action request with Trust Proof

1. PEP intercepts request

1. PEP validates Trust Proof signature and expiration

1. PEP extracts Soul constraint status

1. IF S = 1: - supervision = silent_veto, reason SOVEREIGNTY_CONSTRAINT - Log to Flight Recorder - STOP

1. PEP determines agent's Trust Tier from E_trust

1. PEP looks up Action Risk (A) for requested action

1. IF A > E_trust: - supervision = silent_veto, reason TRUST_INSUFFICIENT (Silent Veto) - Log to Flight Recorder - STOP

1. IF action not permitted for Trust Tier: - supervision = silent_veto, reason TIER_RESTRICTION - Log to Flight Recorder - STOP

1. RETURN the decision result - supervision and tightenedConstraints - per {{KTP-CORE}} Section 6.6; the action proceeds under the tightened envelope, at the returned supervision level

1. Log success to Flight Recorder

1. Return response to agent with refreshed Trust Proof

## Component Roles

Trust Oracle:

- Calculates E_trust from E_base and the Risk Factor inputs
- Signs Trust Proofs
- Maintains Proof of Resilience ledger
- Provides PDP functionality (may be distributed)

Policy Enforcement Point (PEP):

- Intercepts all agent requests
- Validates Trust Proof signatures
- Enforces Soul Veto
- Enforces Silent Veto (A <= E_trust)
- Enforces Trust Tier restrictions
- Logs all decisions to Flight Recorder

Flight Recorder:

- Receives all enforcement decisions
- Stores immutable audit trail
- Provides forensic query interface
- See {{KTP-AUDIT}} for full specification

# Policy Enforcement Points (PEPs)

## PEP Requirements

Every KTP-compliant PEP MUST:

1. Intercept all agent requests before they reach protected resources

1. Require a valid Trust Proof for every request (no Trust Proof = deny by default)

1. Validate Trust Proof signature against known Trust Oracle keys

1. Reject expired Trust Proofs (exp < current time)

1. Evaluate Soul constraint before Trust Score

1. Evaluate A <= E_trust for every action

1. Enforce Trust Tier capability restrictions

1. Log every decision (allow, deny, reason) to Flight Recorder

1. Return appropriate error responses with KTP headers

1. Support Trust Proof refresh/forwarding for downstream services

PEPs SHOULD:

1. Cache Trust Oracle public keys with appropriate TTL

1. Implement rate limiting based on Trust Tier

1. Support graceful degradation when Trust Oracle is unreachable

1. Provide metrics for monitoring (decisions/sec, veto rate, etc.)

PEPs MAY:

1. Implement local Trust Proof validation without Oracle round-trip

1. Support Trust Proof upgrade (request new proof mid-transaction)

1. Implement predictive warnings based on Trust Velocity

## PEP Deployment Patterns

PEPs can be deployed in several patterns depending on architecture:

Pattern 1: Gateway PEP (Perimeter)

~~~
   All traffic enters through a single enforcement point at the
   network perimeter. Simple but creates a single point of failure.
~~~

~~~
   +--------+     +--------+     +------------------+
   | Agent  |---->| Gateway|---->| Internal Services|
   +--------+     |  PEP   |     +------------------+
                  +--------+
~~~

Pattern 2: Sidecar PEP (Service Mesh)

~~~
   Each service has its own PEP running as a sidecar container.
   Distributed enforcement with consistent policy.
~~~

~~~
   +--------+     +--------+--------+     +--------+--------+
   | Agent  |---->| PEP    | Svc A  |---->| PEP    | Svc B  |
   +--------+     +--------+--------+     +--------+--------+
~~~

Pattern 3: Library PEP (Embedded)

~~~
   PEP logic embedded directly in application code via SDK.
   Lowest latency but requires application changes.
~~~

~~~
   +--------+     +------------------------+
   | Agent  |---->| Service with           |
   +--------+     | embedded PEP library   |
                  +------------------------+
~~~

Pattern 4: Hybrid (Defense in Depth)

~~~
   Multiple PEP layers for defense in depth. Recommended for
   high-security deployments.
~~~

~~~
   +--------+     +--------+     +--------+--------+
   | Agent  |---->| Gateway|---->| Sidecar| Service|
   +--------+     |  PEP   |     |  PEP   |        |
                  +--------+     +--------+--------+
~~~

## API Gateway Integration

API Gateways are natural PEP deployment points as they already intercept and process all API traffic.

4.3.1. Kong Integration

Kong plugin configuration:

~~~
   plugins:
     - name: ktp-enforcement
       config:
         trust_oracle_url: "https://oracle.example.com"
         oracle_public_keys:
           - kid: "oracle-key-1"
             algorithm: "ES256"
             key: "-----BEGIN PUBLIC KEY-----..."
         action_risk_map:
           "GET:/api/public/*": 10
           "GET:/api/private/*": 30
           "POST:/api/data/*": 50
           "DELETE:/api/*": 85
         default_action_risk: 50
         require_trust_proof: true
         trust_proof_header: "X-Trust-Proof"
         flight_recorder_url: "https://recorder.example.com"
~~~

4.3.2. AWS API Gateway Integration

Lambda authorizer implementation:

~~~
   - Extract Trust Proof from Authorization header
   - Validate signature against Trust Oracle public key
   - Check expiration
   - Evaluate Soul veto
   - Look up action risk for method + path
   - Compare A <= E_trust
   - Return IAM policy document (Allow/Deny)
   - Log to CloudWatch / Flight Recorder
~~~

4.3.3. Envoy Integration

External authorization filter:

~~~
   http_filters:
     - name: envoy.filters.http.ext_authz
       typed_config:
         "@type": type.googleapis.com/envoy.extensions.filters
                  .http.ext_authz.v3.ExtAuthz
         grpc_service:
           envoy_grpc:
             cluster_name: ktp-authz-service
         transport_api_version: V3
         with_request_body:
           max_request_bytes: 1024
           allow_partial_message: false
~~~

## Service Mesh Integration

Service meshes provide ideal infrastructure for KTP enforcement as they already implement mutual TLS, traffic management, and observability.

4.4.1. Istio Integration

KTP can be integrated with Istio via:

1. Custom AuthorizationPolicy that calls KTP PEP
2. WASM plugin for Envoy sidecars
3. External authorization service

AuthorizationPolicy example:

~~~
   apiVersion: security.istio.io/v1beta1
   kind: AuthorizationPolicy
   metadata:
     name: ktp-enforcement
     namespace: production
   spec:
     selector:
       matchLabels:
         app: protected-service
     action: CUSTOM
     provider:
       name: ktp-ext-authz
     rules:
       - to:
           - operation:
               paths: ["/*"]
~~~

4.4.2. Linkerd Integration

Linkerd integration via policy controller:

~~~
   apiVersion: policy.linkerd.io/v1beta1
   kind: AuthorizationPolicy
   metadata:
     name: ktp-enforcement
     namespace: production
   spec:
     targetRef:
       group: core
       kind: Server
       name: protected-server
     requiredAuthenticationRefs:
       - name: ktp-authn
         kind: MeshTLSAuthentication
         group: policy.linkerd.io
~~~

## IAM Provider Integration

Identity and Access Management providers can incorporate KTP enforcement into their token issuance and validation flows.

4.5.1. OAuth 2.0 / OIDC Integration

KTP Trust Proofs can be embedded in OAuth tokens:

1. Resource Owner requests access token
2. Authorization Server validates identity
3. Authorization Server requests Trust Proof from Trust Oracle
4. Trust Proof embedded in access token claims
5. Resource Server validates Trust Proof during token validation
6. Enforcement based on E_trust and action risk

Token claims extension:

~~~
   {
     "iss": "https://auth.example.com",
     "sub": "agent:7gen:optimized:a1b2c3d4",
     "aud": "https://api.example.com",
     "exp": 1699900600,
     "iat": 1699900000,
     "ktp": {
       "trust_proof": "eyJhbGciOiJFUzI1NiIs...",
       "e_trust": 72,
       "tier": "analyst",
       "soul_clear": true
     }
   }
~~~

4.5.2. SAML Integration

Trust Proof can be included as SAML AttributeStatement:

~~~
   <saml:AttributeStatement>
     <saml:Attribute Name="ktp:trust_proof">
       <saml:AttributeValue>eyJhbGciOiJFUzI1NiIs...
       </saml:AttributeValue>
     </saml:Attribute>
     <saml:Attribute Name="ktp:e_trust">
       <saml:AttributeValue>72</saml:AttributeValue>
     </saml:Attribute>
     <saml:Attribute Name="ktp:tier">
       <saml:AttributeValue>analyst</saml:AttributeValue>
     </saml:Attribute>
   </saml:AttributeStatement>
~~~

## Database Proxy Integration

Database proxies can enforce KTP at the data layer, providing fine- grained control over data access based on Trust Score.

4.6.1. Query Classification

Database operations are classified by risk:

~~~
   +----------------------+-----+--------------------------------+
   | Operation            | A   | Description                    |
   +----------------------+-----+--------------------------------+
   | SELECT (public)      | 10  | Read public/non-sensitive data |
   | SELECT (private)     | 30  | Read private/PII data          |
   | SELECT (sensitive)   | 50  | Read credentials, keys, PHI    |
   | INSERT               | 40  | Create new records             |
   | UPDATE               | 60  | Modify existing records        |
   | DELETE               | 75  | Remove records                 |
   | TRUNCATE             | 85  | Remove all records from table  |
   | DROP                 | 95  | Destroy database objects       |
   | GRANT/REVOKE         | 90  | Modify permissions             |
   +----------------------+-----+--------------------------------+
~~~

4.6.2. Row-Level Enforcement

Trust Score can be used for row-level security:

~~~
   CREATE POLICY ktp_row_security ON sensitive_data
     USING (
       sensitivity_level <= current_setting('ktp.e_trust')::int / 10
     );
~~~

This allows access to data with sensitivity_level <= E_trust/10. An agent with E_trust = 72 can access rows with sensitivity <= 7.

# Trust Tiers

## Tier Definitions

Trust Tiers provide graduated capability levels based on E_trust thresholds. The standard tiers are:

~~~
+---------------+----------+--------------------------------------+
| Tier          | E_trust  | Description                          |
+---------------+----------+--------------------------------------+
| Admin Mode    | >= 85    | Full infrastructure control          |
| Operator Mode | >= 72    | Service management, config changes   |
| Analyst Mode  | >= 58    | Data query, read-only operations     |
| Observer Mode | >= 22    | Logging, monitoring, heartbeat       |
| Hibernation   | < 22     | Heartbeat only, await recovery       |
+---------------+----------+--------------------------------------+
~~~

5.1.1. Admin Mode (E_trust >= 85)

The highest capability tier. Reserved for critical infrastructure operations that require maximum trust.

Permitted actions:

- Create, modify, destroy infrastructure components
- Deploy code to production
- Modify security configurations
- Access all data regardless of classification
- Grant/revoke permissions for other agents

Admin Mode is available only in zones whose Mass Ceiling is at least 95 (the zone ceilings of Section 9.2): the threshold is derived from that ceiling at the tier's declared R budget, and a zone with a lower ceiling cannot deliver it at any generation. An operator planning toward Admin Mode in such a zone is planning toward a tier the zone does not offer.

Requirements:

- Guarantor lineage (generation 7+)
- Extensive Proof of Resilience
- Stable environmental conditions (R < 0.10)

5.1.2. Operator Mode (E_trust >= 72)

Standard operational capability for routine service management.

Permitted actions:

- Restart services
- Scale deployments up/down
- Read configuration files
- Access internal APIs
- Modify non-sensitive data

Restricted actions:

- Cannot deploy new code
- Cannot modify security settings
- Cannot access credentials or keys

5.1.3. Analyst Mode (E_trust >= 58)

Read-heavy capability tier for data analysis and investigation.

Permitted actions:

- Query databases (read-only)
- Access logs and metrics
- Generate reports
- Call read-only APIs

Restricted actions:

- Cannot write to production data
- Cannot restart services
- Cannot access credentials

5.1.4. Observer Mode (E_trust >= 22)

Minimal capability tier for monitoring and logging.

Permitted actions:

- Emit logs and metrics
- Send heartbeat signals
- Read own state
- Request Trust Proof refresh

Restricted actions:

- Cannot read external data
- Cannot call APIs
- Cannot perform any writes

5.1.5. Hibernation Mode (E_trust < 22)

Emergency survival mode when environmental conditions are severe.

Permitted actions:

- Emit heartbeat signal only
- Await Trust Score recovery

Restricted actions:

- All actions except heartbeat are blocked

## Capability Matrices

The Capability Matrix maps Trust Tiers to permitted action classes:

~~~
+---------------+----------------------------------+
| Tier          | Permitted Action Classes         |
+---------------+----------------------------------+
| Admin Mode    | All actions                      |
| Operator Mode | Read, Write, Execute (safe)      |
| Analyst Mode  | Read (all), Write (append only)  |
| Observer Mode | Read (public), Emit logs         |
| Hibernation   | Heartbeat only                   |
+---------------+----------------------------------+
~~~

A tier permits action classes; it does not carry a numeric action-risk cap of its own. The numeric bound is the Zeroth Law: A <= E_trust, evaluated per action against the agent's current score. An earlier revision carried a Max A column beside the classes — a second numeric bound keyed to the tier thresholds, which drifted when the thresholds moved and could only ever restate, more coarsely, what A <= E_trust already enforces exactly. One fact stated twice diverges; the environment's bound is the bound.

## Tier Transitions

Agents transition between tiers as E_trust changes:

Tier Promotion (E_trust increases):

- Happens automatically when E_trust crosses threshold
- No delay or approval required
- Expanded capabilities immediately available
- Logged to Flight Recorder

Tier Demotion (E_trust decreases):

- Happens automatically when E_trust crosses threshold
- In-flight operations may be interrupted
- Agent should implement graceful capability shedding
- Logged to Flight Recorder with context

Hysteresis (optional):

To prevent oscillation at tier boundaries, implementations MAY implement hysteresis:

- Promotion requires E_trust >= threshold + 2
- Demotion requires E_trust < threshold - 2

This creates a 4-point buffer zone that prevents rapid tier switching when E_trust fluctuates near boundaries.

## Custom Tier Configuration

Implementations MAY define custom tiers for domain-specific needs:

~~~
   {
     "tiers": [
       {
         "name": "emergency_responder",
         "e_trust_min": 60,
         "e_trust_max": 80,
         "max_action_risk": 75,
         "permitted_actions": [
           "read:*",
           "write:emergency_logs",
           "execute:emergency_procedures"
         ],
         "restricted_actions": [
           "delete:*",
           "admin:*"
         ],
         "description": "Emergency response operations"
       }
     ]
   }
~~~

# Action Risk Classification

## Standard Action Classes

The standard action classification taxonomy:

~~~
+----------------------+-----+--------------------------------------+
| Action Class         | A   | Description                          |
+----------------------+-----+--------------------------------------+
| Heartbeat            | 5   | Agent alive signal                   |
| Read (public)        | 10  | Read publicly accessible data        |
| Read (internal)      | 20  | Read internal/company data           |
| Read (private)       | 30  | Read PII, personal data              |
| Read (sensitive)     | 40  | Read credentials, keys, PHI          |
| Write (logs)         | 25  | Emit logs, metrics, events           |
| Write (append)       | 40  | Add new records, no modification     |
| Write (modify)       | 50  | Modify existing records              |
| Write (sensitive)    | 65  | Modify sensitive data                |
| Execute (safe)       | 60  | Run pre-approved operations          |
| Execute (unsafe)     | 75  | Run arbitrary code                   |
| Delete (recoverable) | 70  | Delete with backup/undo available    |
| Delete (permanent)   | 85  | Delete without recovery              |
| Admin (config)       | 80  | Change system configuration          |
| Admin (security)     | 90  | Modify security settings             |
| Admin (infra)        | 95  | Modify infrastructure                |
+----------------------+-----+--------------------------------------+
~~~

## Risk Score Assignment

Action risk scores should be assigned based on:

1. Reversibility: Can the action be undone? - Fully reversible: Lower A - Partially reversible: Medium A - Irreversible: Higher A

1. Blast Radius: How many systems/users are affected? - Single record: Lower A - Single service: Medium A - Multiple services: Higher A - Entire system: Highest A

1. Data Sensitivity: What type of data is involved? - Public data: Lower A - Internal data: Medium A - PII/PHI: Higher A - Credentials/keys: Highest A

1. Regulatory Impact: Are there compliance implications? - No regulatory data: Baseline A - GDPR/CCPA data: +10 A - HIPAA/PCI data: +20 A - Classified data: +30 A

## Dynamic Risk Adjustment

Action risk may be dynamically adjusted based on context:

6.3.1. Target-Based Adjustment

The same action has different risk based on target:

~~~
   DELETE /api/users/test-account    A = 50 (test environment)
   DELETE /api/users/production      A = 85 (production data)
~~~

6.3.2. Volume-Based Adjustment

Bulk operations carry higher risk:

~~~
   DELETE /api/records/1             A = 70 (single record)
   DELETE /api/records?all=true      A = 95 (bulk delete)
~~~

6.3.3. Time-Based Adjustment

Risk increases during critical periods:

~~~
   Base A = 60
   During maintenance window: A = 60 (no adjustment)
   During peak hours: A = 70 (+10)
   During live event: A = 80 (+20)
~~~

# Silent Veto Mechanics

## Veto Evaluation Order

Enforcement follows a strict evaluation order:

1. Trust Proof Validation - Signature valid? - Not expired? - If NO: supervision = silent_veto, reason INVALID_TRUST_PROOF

1. Soul Veto (Sovereignty Check) - S = 1? - If YES: supervision = silent_veto, reason SOVEREIGNTY_CONSTRAINT

1. Trust Tier Eligibility - Is action class permitted for tier? - If NO: supervision = silent_veto, reason TIER_RESTRICTION

1. Zeroth Law (A <= E_trust) - Is A <= E_trust? - If NO: supervision = silent_veto, reason TRUST_INSUFFICIENT

1. Custom Policy (Optional) - Any additional policy constraints? - If violated: supervision = silent_veto, reason POLICY_VIOLATION

1. RETURN the decision result - supervision and tightenedConstraints - per {{KTP-CORE}} Section 6.6

This order ensures that sovereignty constraints are always evaluated first, followed by environment-derived constraints, followed by tier restrictions, followed by any custom policies.

## Veto Response Codes

HTTP response codes for KTP enforcement:

~~~
+------+---------------------------+--------------------------------+
| Code | KTP Error                 | Description                    |
+------+---------------------------+--------------------------------+
| 401  | MISSING_TRUST_PROOF       | No Trust Proof provided        |
| 401  | INVALID_TRUST_PROOF       | Signature invalid or expired   |
| 403  | SOVEREIGNTY_CONSTRAINT    | Soul veto (S = 1)              |
| 403  | TRUST_INSUFFICIENT        | A > E_trust (Silent Veto)      |
| 403  | TIER_RESTRICTION          | Action not permitted for tier  |
| 403  | POLICY_VIOLATION          | Custom policy constraint       |
| 429  | RATE_LIMITED              | Trust-based rate limit hit     |
| 503  | ORACLE_UNAVAILABLE        | Cannot validate Trust Proof    |
+------+---------------------------+--------------------------------+
~~~

Response body format:

~~~
   {
     "error": "TRUST_INSUFFICIENT",
     "message": "Action risk exceeds current trust",
     "details": {
       "action": "DELETE /api/users/12345",
       "action_risk": 85,
       "e_trust": 72,
       "tier": "analyst",
       "de_dt": -1.5,
       "soul_clear": true
     },
     "retry_after": null,
     "request_id": "req-uuid-12345"
   }
~~~

## Veto Notification

When a veto occurs, the PEP SHOULD notify relevant parties:

1. Agent: Receives error response with details

1. Flight Recorder: Receives full decision context

1. Monitoring: Metrics updated (veto counter, by type)

1. Alerting (optional): If veto rate exceeds threshold

Agents SHOULD implement veto handling:

- Parse veto response to understand reason
- If TRUST_INSUFFICIENT: Reduce activity, wait for recovery
- If SOVEREIGNTY_CONSTRAINT: Do not retry, seek remediation
- If TIER_RESTRICTION: Request tier upgrade path
- Log veto for own records

# Adaptive Dormancy

Adaptive Dormancy is the mechanism by which agents gracefully reduce their activity as environmental conditions degrade, rather than failing catastrophically.

## Dormancy Triggers

Dormancy is triggered by:

1. Tier Demotion: When E_trust drops below tier threshold

1. Velocity Warning: When dE/dt indicates rapid degradation

1. Direct Signal: When Trust Oracle issues dormancy advisory

1. Peer Signal: When peer agents report entering dormancy

Dormancy is NOT a failure state. It is a survival strategy. An agent in dormancy is conserving resources and protecting the environment from actions it can no longer safely perform.

## Graceful Degradation

When entering a lower tier, agents SHOULD:

1. Complete in-flight operations if possible within timeout

1. Release resources not needed for new tier

1. Cancel scheduled operations that exceed new tier

1. Notify dependent systems of capability reduction

1. Enter reduced activity loop

Degradation sequence example:

~~~
   E_trust drops from 88 to 68 (Operator -> Analyst)
~~~

~~~
   Agent actions:
   1. Complete pending write operation (2 seconds)
   2. Cancel scheduled deployment (no longer permitted)
   3. Release infrastructure locks
   4. Notify orchestrator: "capability reduced to analyst"
   5. Enter read-only mode
   6. Continue monitoring for recovery
~~~

## Recovery Procedures

When E_trust recovers above a tier threshold:

1. Agent detects tier promotion via Trust Proof

1. Agent verifies recovery is stable (E_trust maintained for minimum duration, e.g., 30 seconds)

1. Agent gradually re-enables capabilities

1. Agent resumes normal operations

Recovery SHOULD be gradual to avoid oscillation:

~~~
   E_trust recovers from 68 to 88 (Analyst -> Operator)
~~~

~~~
   Agent actions:
   1. Detect promotion in Trust Proof
   2. Wait 30 seconds to confirm stability
   3. Re-enable write capabilities
   4. Wait 30 seconds
   5. Re-enable service management capabilities
   6. Resume normal operations
   7. Notify orchestrator: "capability restored to operator"
~~~

## Hibernation Mode

Hibernation is the most extreme dormancy state, entered when E_trust falls below 50.

In Hibernation:

- Agent performs NO operations except heartbeat
- Heartbeat interval increases to conserve resources
- Agent awaits external signal or Trust Score recovery
- All state is preserved for potential recovery

Heartbeat signal in hibernation:

~~~
   {
     "type": "heartbeat",
     "agent_id": "agent:7gen:optimized:a1b2c3d4",
     "state": "hibernating",
     "e_trust": 35,
     "hibernation_duration_seconds": 3600,
     "awaiting": "trust_recovery",
     "timestamp": "2025-11-25T12:00:00Z"
   }
~~~

Hibernation exit requires:

- E_trust >= 24 (the Observer floor of 22 plus the Section 5.3 promotion buffer)
- Sustained for minimum 60 seconds
- No Soul veto active

# Mass Ceiling and Anti-Accumulation

An agent that accumulates excessive trust becomes a systemic risk. Like a star that grows too massive, it can collapse catastrophically or distort the environment around it.

This section specifies constraints to prevent dangerous mass accumulation.

## The Accumulation Problem

Without constraints, agents can accumulate trust indefinitely:

- Long tenure -> high E_base
- Many attestations -> high resilience score
- Critical role -> high dependency

This creates "too big to fail" agents:

- Their failure would cascade across the system
- They cannot be easily replaced or demoted
- They may crowd out other agents
- They accumulate disproportionate authority

The astrophysical analogy (informative): a star that exceeds the Chandrasekhar limit cannot remain stable. It must either shed mass or collapse.

## Mass Ceiling

Every zone MUST define a Mass Ceiling: the maximum E_base any single agent may hold.

Recommended ceilings by zone type:

~~~
+------------+---------------+--------------------------------+
| Zone Type  | Mass Ceiling  | Rationale                      |
+------------+---------------+--------------------------------+
| Deep Blue  | 95            | Critical systems need margin   |
| Blue       | 92            | Production requires headroom   |
| Cyan       | 90            | General operations             |
| Green      | 95            | Minimal enforcement anyway     |
+------------+---------------+--------------------------------+
~~~

When an agent's E_base would exceed the ceiling:

1. E_base is capped at ceiling (excess trust does not accumulate)
2. Agent is flagged for mass review
3. Options presented: mitosis, redistribution, or acceptance

## Mitosis Protocol

When an agent exceeds mass ceiling or approaches systemic risk threshold, it may undergo Mitosis: controlled division into multiple smaller agents.

Mitosis process:

1. Agent (or operator) initiates mitosis request
2. Trust Oracle evaluates agent's responsibilities
3. Trust Oracle proposes division plan: - Which capabilities go to which child agent - How E_base is distributed - Dependency migration plan
4. Operator approves division plan
5. Child agents created with allocated E_base
6. Dependencies migrated to appropriate children
7. Parent agent retired or reduced

E_base distribution in mitosis:

~~~
   E_base_child_1 + E_base_child_2 + ... <= E_base_parent
~~~

Trust is conserved but may have overhead losses (children start slightly lower than parent's allocation due to newness).

Example:

~~~
   Parent agent: E_base = 92 (at ceiling)
   Division: 3 children
~~~

~~~
   Child A (data operations): E_base = 45
   Child B (compute operations): E_base = 35
   Child C (admin operations): E_base = 40
   Total: 120, but capped to 92 with proportional reduction
~~~

~~~
   Actual allocation:
   Child A: 45 * (92/120) = 34.5 -> 34
   Child B: 35 * (92/120) = 26.8 -> 27
   Child C: 40 * (92/120) = 30.6 -> 31
   Total: 92
~~~

## Systemic Risk Assessment

Beyond individual mass ceiling, zones MUST assess systemic risk from agent concentration.

Concentration metrics:

1. Single Agent Dependency (SAD): What percentage of critical paths depend on one agent? Threshold: No agent should be on > 30% of critical paths

1. Mass Concentration Index (MCI): What percentage of total zone trust is held by top N agents? Threshold: Top 5 agents should hold < 40% of total trust

1. Failure Blast Radius (FBR): If this agent fails, how many others are affected? Threshold: No agent should have FBR > 20% of zone population

When thresholds are exceeded:

- Alert zone operators
- Flag agents for mitosis review
- Increase monitoring on concentrated agents
- Consider architectural changes to reduce dependency

## Progressive Trust Taxation

To discourage excessive accumulation, zones MAY implement progressive trust taxation: diminishing returns at high E_base.

Formula:

~~~
   effective_E_base = E_base                        if E_base <= 70
   effective_E_base = 70 + 0.8*(E_base - 70)        if E_base <= 85
   effective_E_base = 82 + 0.5*(E_base - 85)        if E_base <= 95
   effective_E_base = 87 + 0.2*(E_base - 95)        if E_base > 95
~~~

Example with taxation:

~~~
   Nominal E_base = 98
   Effective E_base = 70 + 0.8*(85-70) + 0.5*(95-85) + 0.2*(98-95)
                    = 70 + 12 + 5 + 0.6
                    = 87.6
~~~

This does not prevent high-trust agents from existing, but it reduces the advantage of extreme accumulation, encouraging distribution of responsibilities.

A zone implementing progressive trust taxation does not offer Admin Mode. The taxed curve saturates at 87, which at any environmental deflation a live zone exhibits sits below the Admin threshold; this is a consequence of the curve, and it is the intended trade rather than an accident. The section's purpose is to discourage accumulation, and the top tier is accumulation. A zone that requires Admin Mode MUST NOT implement this section; a zone that implements it has chosen distribution of responsibilities over apex capability, and its capability planning MUST proceed from Operator Mode as the highest attainable tier.

## Anti-Accumulation in Federation

Federated zones MUST coordinate on mass ceiling enforcement:

- An agent at ceiling in Zone A should not accumulate freely in Zone B
- Cross-zone mass is aggregated for ceiling calculation
- Mitosis may span zones (child agents in different zones)

Federation mass coordination:

~~~
   {
     "agent_id": "agent:guarantor:mega-service",
     "zone_mass": {
       "zone-blue-prod": 88,
       "zone-blue-staging": 45,
       "zone-cyan-dev": 32
     },
     "aggregate_mass": 165,
     "federation_ceiling": 150,
     "status": "over_ceiling",
     "recommendation": "mitosis"
   }
~~~

# Latency Requirements

Enforcement must be fast enough to not impede legitimate operations while thorough enough to maintain security.

Target latency budget:

~~~
+---------------------------+------------+
| Operation                 | Target     |
+---------------------------+------------+
| Trust Proof validation    | < 1 ms     |
| Soul veto check           | < 5 ms     |
| Action risk lookup        | < 1 ms     |
| A <= E_trust evaluation   | < 0.1 ms   |
| Flight Recorder logging   | < 10 ms    |
| Total PEP overhead        | < 15 ms    |
+---------------------------+------------+
~~~

To achieve these targets:

1. Cache Trust Oracle public keys locally
2. Cache action risk mappings locally
3. Use async logging to Flight Recorder
4. Pre-compute tier from E_trust
5. Use efficient data structures (hash maps, not linear search)

# Security Considerations

11.1. PEP Bypass

Attackers may attempt to bypass PEPs entirely.

Mitigations:

- Deploy PEPs at network choke points
- Use defense in depth (multiple PEP layers)
- Monitor for traffic not passing through PEPs
- Implement network segmentation

11.2. Trust Proof Theft

Stolen Trust Proofs could be used by attackers.

Mitigations:

- Short Trust Proof lifetime (max 10 seconds)
- Bind Trust Proof to agent identity
- Bind Trust Proof to TLS session
- Monitor for Trust Proof reuse

11.3. PEP Compromise

A compromised PEP could allow unauthorized actions.

Mitigations:

- Run PEPs in hardened containers
- Implement PEP integrity monitoring
- Use multiple PEP layers (defense in depth)
- Log all PEP decisions for audit

11.4. Denial of Service

Attackers may attempt to overwhelm PEPs.

Mitigations:

- Implement rate limiting at PEP
- Scale PEPs horizontally
- Use caching to reduce Oracle load
- Implement circuit breakers

--- back

# Changes from v1

This appendix records what a v1 implementation must change to conform to
v2.0.0.  The break is deliberate and there is no dual-accept period: an
implementation reads v1 or it reads v2.

## The lineage stage names

The three lineage stages are renamed on the wire and in prose.  Numeric
protobuf values are unchanged, so only the symbol names move.

| v1 | v2.0.0 |
|----|--------|
| `tethered` | `sponsored` |
| `divergent` | `independent` |
| `persistent` | `guarantor` |

This affects agent identifier strings (`agent:<stage>:...`), the `lineage`
enum, and the protobuf `LineageType` member names.  The v1 words each carried
an unintended security reading - in jailbreak and intrusion vocabulary,
"tethered" means a compromise that dies at reboot and "persistent" is the
established word for one that survives a restart - and the three together read
as a coherent escalation narrative rather than as a maturity ladder.  Stage 3
is now named for what it can be held to rather than what it is freed of.

## The Trust Tier thresholds

| Tier | v1 | v2.0.0 |
|------|----|--------|
| Admin Mode | `E_trust >= 95` | `E_trust >= 85` |
| Operator Mode | `E_trust >= 85` | `E_trust >= 72` |
| Analyst Mode | `E_trust >= 70` | `E_trust >= 58` |
| Observer Mode | `E_trust >= 50` | `E_trust >= 22` |
| Hibernation | `E_trust < 50` | `E_trust < 22` |

The v1 set was unreachable from the v1 generation ceilings: generations 0
through 2 were capped below the lowest threshold, so an agent was in
Hibernation by lineage rather than by environment, and the top tier could not
be reached in any zone at the calm conditions the specification's own worked
example uses.  The generation ceilings are unchanged; one table moved, not two.

Two consequences travel with the change.  Hibernation exit moves from
`E_trust >= 55` to `E_trust >= 24`, because a five-point hysteresis over a
floor of 50 becomes a thirty-three-point one over a floor of 22.  And the
stable-conditions requirement for the top tier moves from `R < 0.05` to
`R < 0.10`, because 0.05 is stricter than the calm baseline the corpus
illustrates.
