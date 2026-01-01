Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


          Kinetic Trust Protocol (KTP) - Enforcement Layer Specification

Abstract

   This document specifies the Enforcement Layer for the Kinetic Trust
   Protocol (KTP). The Enforcement Layer is responsible for intercepting
   agent actions, evaluating them against Trust Proofs, and executing
   the Silent Veto when environmental constraints are violated.

   The specification covers Policy Enforcement Points (PEPs), Trust
   Tiers with graduated capability levels, Adaptive Dormancy for
   graceful degradation, and integration patterns for common
   infrastructure components.

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
       1.1.  Enforcement Philosophy  . . . . . . . . . . . . . . . .  2
       1.2.  Requirements Language . . . . . . . . . . . . . . . . .  3
   2.  Terminology . . . . . . . . . . . . . . . . . . . . . . . . .  3
   3.  Architecture Overview . . . . . . . . . . . . . . . . . . . .  4
       3.1.  Enforcement Flow  . . . . . . . . . . . . . . . . . . .  5
       3.2.  Component Roles . . . . . . . . . . . . . . . . . . . .  6
   4.  Policy Enforcement Points (PEPs)  . . . . . . . . . . . . . .  7
       4.1.  PEP Requirements  . . . . . . . . . . . . . . . . . . .  7
       4.2.  PEP Deployment Patterns . . . . . . . . . . . . . . . .  8
       4.3.  API Gateway Integration . . . . . . . . . . . . . . . . 10
       4.4.  Service Mesh Integration  . . . . . . . . . . . . . . . 12
       4.5.  IAM Provider Integration  . . . . . . . . . . . . . . . 14
       4.6.  Database Proxy Integration  . . . . . . . . . . . . . . 16
   5.  Trust Tiers . . . . . . . . . . . . . . . . . . . . . . . . . 18
       5.1.  Tier Definitions  . . . . . . . . . . . . . . . . . . . 18
       5.2.  Capability Matrices . . . . . . . . . . . . . . . . . . 20
       5.3.  Tier Transitions  . . . . . . . . . . . . . . . . . . . 22
       5.4.  Custom Tier Configuration . . . . . . . . . . . . . . . 23
   6.  Action Risk Classification  . . . . . . . . . . . . . . . . . 24
       6.1.  Standard Action Classes . . . . . . . . . . . . . . . . 24
       6.2.  Risk Score Assignment . . . . . . . . . . . . . . . . . 26
       6.3.  Dynamic Risk Adjustment . . . . . . . . . . . . . . . . 27
   7.  Silent Veto Mechanics . . . . . . . . . . . . . . . . . . . . 28
       7.1.  Veto Evaluation Order . . . . . . . . . . . . . . . . . 28
       7.2.  Veto Response Codes . . . . . . . . . . . . . . . . . . 29
       7.3.  Veto Notification . . . . . . . . . . . . . . . . . . . 30
   8.  Adaptive Dormancy . . . . . . . . . . . . . . . . . . . . . . 31
       8.1.  Dormancy Triggers . . . . . . . . . . . . . . . . . . . 31
       8.2.  Graceful Degradation  . . . . . . . . . . . . . . . . . 32
       8.3.  Recovery Procedures . . . . . . . . . . . . . . . . . . 34
       8.4.  Hibernation Mode  . . . . . . . . . . . . . . . . . . . 35
   9.  Mass Ceiling and Anti-Accumulation  . . . . . . . . . . . . . 36
       9.1.  The Accumulation Problem  . . . . . . . . . . . . . . . 36
       9.2.  Mass Ceiling  . . . . . . . . . . . . . . . . . . . . . 37
       9.3.  Mitosis Protocol  . . . . . . . . . . . . . . . . . . . 38
       9.4.  Systemic Risk Assessment  . . . . . . . . . . . . . . . 39
       9.5.  Progressive Trust Taxation  . . . . . . . . . . . . . . 40
       9.6.  Anti-Accumulation in Federation . . . . . . . . . . . . 41
   10. Latency Requirements  . . . . . . . . . . . . . . . . . . . . 42
   11. Security Considerations . . . . . . . . . . . . . . . . . . . 43
   12. References  . . . . . . . . . . . . . . . . . . . . . . . . . 44
   Authors' Addresses  . . . . . . . . . . . . . . . . . . . . . . . 45


1.  Introduction

   The Enforcement Layer is where Digital Physics becomes operational
   reality. While the Trust Oracle calculates what is possible, the
   Enforcement Layer ensures that only what is possible actually occurs.

   Traditional authorization enforcement is binary: allowed or denied.
   KTP enforcement is graduated: actions may be allowed, denied, 
   throttled, downgraded, or deferred based on the relationship between
   action risk and environmental capacity.

1.1.  Enforcement Philosophy

   The core philosophy of KTP enforcement is:

   "The environment has veto power over agent intent."

   This inverts the traditional authorization model. Instead of asking
   "Is this agent permitted to perform this action?", KTP asks "Can
   this environment safely support this action right now?"

   Key principles:

   1. Silent Veto: Enforcement happens automatically, without human
      intervention. The environment constrains; it does not negotiate.

   2. Graceful Degradation: When conditions degrade, agents don't fail
      catastrophically. They enter reduced capability modes, maintaining
      essential functions while shedding risky ones.

   3. No Override: There is no emergency bypass. The only way to enable
      a high-risk action is to improve environmental conditions or
      reduce the action's risk classification.

   4. Transparency: Every enforcement decision is logged with full
      context, enabling forensic reconstruction and system learning.

1.2.  Requirements Language

   The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
   "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
   "OPTIONAL" in this document are to be interpreted as described in
   BCP 14 [RFC2119] [RFC8174].


2.  Terminology

   Action Risk (A):
      A numeric value (0-100) representing the intrinsic risk of a
      requested action, independent of who is requesting it.

   Adaptive Dormancy:
      The progressive reduction of agent capabilities as environmental
      conditions degrade, allowing agents to "hibernate" rather than
      fail completely.

   Capability Matrix:
      A mapping of Trust Tiers to permitted action classes, defining
      what each tier is allowed to do.

   Effective Trust Score (E_trust):
      The current Trust Score after environmental deflation, used to
      determine the agent's Trust Tier.

   Hibernation Mode:
      The most restrictive operational state, where an agent can only
      emit heartbeat signals and await recovery.

   Policy Decision Point (PDP):
      The logical component that evaluates Trust Proofs and makes
      authorization decisions. In KTP, this is typically the Trust
      Oracle or a local cache.

   Policy Enforcement Point (PEP):
      A component that intercepts agent requests and enforces PDP
      decisions by allowing, denying, or modifying actions.

   Silent Veto:
      The automatic denial of an action when A > E_trust, executed
      without human intervention or appeal.

   Soul Veto:
      The automatic denial of an action when sovereignty constraints
      are violated (S = 1), taking precedence over Trust Score
      evaluation.

   Trust Tier:
      A capability level (God Mode, Operator Mode, Analyst Mode,
      Observer Mode) determined by E_trust thresholds.


3.  Architecture Overview

   The Enforcement Layer sits between agents and protected resources,
   intercepting all actions and evaluating them against current
   environmental conditions.

   +------------------------------------------------------------------+
   |                         AGENT POPULATION                         |
   |    [Tethered Agents]  [Divergent Agents]  [Persistent Lineages]  |
   +------------------------------------------------------------------+
                                   |
                                   | Action Request
                                   v
   +------------------------------------------------------------------+
   |                      ENFORCEMENT LAYER                           |
   |  +------------------------------------------------------------+  |
   |  |                 Policy Enforcement Points                   |  |
   |  |  +----------+  +----------+  +----------+  +----------+    |  |
   |  |  | API GW   |  | Service  |  |   IAM    |  |    DB    |    |  |
   |  |  |   PEP    |  | Mesh PEP |  |   PEP    |  |   PEP    |    |  |
   |  |  +----------+  +----------+  +----------+  +----------+    |  |
   |  +------------------------------------------------------------+  |
   |                              |                                   |
   |                              | Trust Proof Validation            |
   |                              v                                   |
   |  +------------------------------------------------------------+  |
   |  |              Policy Decision Point (PDP)                    |  |
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
   |    [APIs]  [Databases]  [Services]  [Infrastructure]            |
   +------------------------------------------------------------------+

   Figure 1: Enforcement Layer Architecture


3.1.  Enforcement Flow

   The standard enforcement flow for every action:

   1. Agent submits action request with Trust Proof

   2. PEP intercepts request

   3. PEP validates Trust Proof signature and expiration

   4. PEP extracts Soul constraint status (S)

   5. IF S = 1:
      - DENY with SOVEREIGNTY_CONSTRAINT
      - Log to Flight Recorder
      - STOP

   6. PEP determines agent's Trust Tier from E_trust

   7. PEP looks up Action Risk (A) for requested action

   8. IF A > E_trust:
      - DENY with TRUST_INSUFFICIENT (Silent Veto)
      - Log to Flight Recorder
      - STOP

   9. IF action not permitted for Trust Tier:
      - DENY with TIER_RESTRICTION
      - Log to Flight Recorder
      - STOP

   10. ALLOW action to proceed

   11. Log success to Flight Recorder

   12. Return response to agent with refreshed Trust Proof


3.2.  Component Roles

   Trust Oracle:
      - Calculates E_trust from E_base and Context Tensor
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
      - See [KTP-AUDIT] for full specification


4.  Policy Enforcement Points (PEPs)

4.1.  PEP Requirements

   Every KTP-compliant PEP MUST:

   1. Intercept all agent requests before they reach protected resources

   2. Require a valid Trust Proof for every request (no Trust Proof =
      deny by default)

   3. Validate Trust Proof signature against known Trust Oracle keys

   4. Reject expired Trust Proofs (exp < current time)

   5. Evaluate Soul constraint before Trust Score

   6. Evaluate A <= E_trust for every action

   7. Enforce Trust Tier capability restrictions

   8. Log every decision (allow, deny, reason) to Flight Recorder

   9. Return appropriate error responses with KTP headers

   10. Support Trust Proof refresh/forwarding for downstream services

   PEPs SHOULD:

   1. Cache Trust Oracle public keys with appropriate TTL

   2. Implement rate limiting based on Trust Tier

   3. Support graceful degradation when Trust Oracle is unreachable

   4. Provide metrics for monitoring (decisions/sec, veto rate, etc.)

   PEPs MAY:

   1. Implement local Trust Proof validation without Oracle round-trip

   2. Support Trust Proof upgrade (request new proof mid-transaction)

   3. Implement predictive warnings based on Trust Velocity


4.2.  PEP Deployment Patterns

   PEPs can be deployed in several patterns depending on architecture:

   Pattern 1: Gateway PEP (Perimeter)

      All traffic enters through a single enforcement point at the
      network perimeter. Simple but creates a single point of failure.

      +--------+     +--------+     +------------------+
      | Agent  |---->| Gateway|---->| Internal Services|
      +--------+     |  PEP   |     +------------------+
                     +--------+

   Pattern 2: Sidecar PEP (Service Mesh)

      Each service has its own PEP running as a sidecar container.
      Distributed enforcement with consistent policy.

      +--------+     +--------+--------+     +--------+--------+
      | Agent  |---->| PEP    | Svc A  |---->| PEP    | Svc B  |
      +--------+     +--------+--------+     +--------+--------+

   Pattern 3: Library PEP (Embedded)

      PEP logic embedded directly in application code via SDK.
      Lowest latency but requires application changes.

      +--------+     +------------------------+
      | Agent  |---->| Service with           |
      +--------+     | embedded PEP library   |
                     +------------------------+

   Pattern 4: Hybrid (Defense in Depth)

      Multiple PEP layers for defense in depth. Recommended for
      high-security deployments.

      +--------+     +--------+     +--------+--------+
      | Agent  |---->| Gateway|---->| Sidecar| Service|
      +--------+     |  PEP   |     |  PEP   |        |
                     +--------+     +--------+--------+


4.3.  API Gateway Integration

   API Gateways are natural PEP deployment points as they already
   intercept and process all API traffic.

   4.3.1. Kong Integration

   Kong plugin configuration:

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

   4.3.2. AWS API Gateway Integration

   Lambda authorizer implementation:

      - Extract Trust Proof from Authorization header
      - Validate signature against Trust Oracle public key
      - Check expiration
      - Evaluate Soul veto
      - Look up action risk for method + path
      - Compare A <= E_trust
      - Return IAM policy document (Allow/Deny)
      - Log to CloudWatch / Flight Recorder

   4.3.3. Envoy Integration

   External authorization filter:

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


4.4.  Service Mesh Integration

   Service meshes provide ideal infrastructure for KTP enforcement
   as they already implement mutual TLS, traffic management, and
   observability.

   4.4.1. Istio Integration

   KTP can be integrated with Istio via:

   1. Custom AuthorizationPolicy that calls KTP PEP
   2. WASM plugin for Envoy sidecars
   3. External authorization service

   AuthorizationPolicy example:

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

   4.4.2. Linkerd Integration

   Linkerd integration via policy controller:

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


4.5.  IAM Provider Integration

   Identity and Access Management providers can incorporate KTP
   enforcement into their token issuance and validation flows.

   4.5.1. OAuth 2.0 / OIDC Integration

   KTP Trust Proofs can be embedded in OAuth tokens:

   1. Resource Owner requests access token
   2. Authorization Server validates identity
   3. Authorization Server requests Trust Proof from Trust Oracle
   4. Trust Proof embedded in access token claims
   5. Resource Server validates Trust Proof during token validation
   6. Enforcement based on E_trust and action risk

   Token claims extension:

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

   4.5.2. SAML Integration

   Trust Proof can be included as SAML AttributeStatement:

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


4.6.  Database Proxy Integration

   Database proxies can enforce KTP at the data layer, providing
   fine-grained control over data access based on Trust Score.

   4.6.1. Query Classification

   Database operations are classified by risk:

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

   4.6.2. Row-Level Enforcement

   Trust Score can be used for row-level security:

      CREATE POLICY ktp_row_security ON sensitive_data
        USING (
          sensitivity_level <= current_setting('ktp.e_trust')::int / 10
        );

   This allows access to data with sensitivity_level <= E_trust/10.
   An agent with E_trust = 72 can access rows with sensitivity <= 7.


5.  Trust Tiers

5.1.  Tier Definitions

   Trust Tiers provide graduated capability levels based on E_trust
   thresholds. The standard tiers are:

   +---------------+----------+--------------------------------------+
   | Tier          | E_trust  | Description                          |
   +---------------+----------+--------------------------------------+
   | God Mode      | >= 95    | Full infrastructure control          |
   | Operator Mode | >= 85    | Service management, config changes   |
   | Analyst Mode  | >= 70    | Data query, read-only operations     |
   | Observer Mode | >= 50    | Logging, monitoring, heartbeat       |
   | Hibernation   | < 50     | Heartbeat only, await recovery       |
   +---------------+----------+--------------------------------------+

   5.1.1. God Mode (E_trust >= 95)

   The highest capability tier. Reserved for critical infrastructure
   operations that require maximum trust.

   Permitted actions:
   - Create, modify, destroy infrastructure components
   - Deploy code to production
   - Modify security configurations
   - Access all data regardless of classification
   - Grant/revoke permissions for other agents

   Requirements:
   - Persistent lineage (generation 6+)
   - Extensive Proof of Resilience
   - Stable environmental conditions (R < 0.05)

   5.1.2. Operator Mode (E_trust >= 85)

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

   5.1.3. Analyst Mode (E_trust >= 70)

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

   5.1.4. Observer Mode (E_trust >= 50)

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

   5.1.5. Hibernation Mode (E_trust < 50)

   Emergency survival mode when environmental conditions are severe.

   Permitted actions:
   - Emit heartbeat signal only
   - Await Trust Score recovery

   Restricted actions:
   - All actions except heartbeat are blocked


5.2.  Capability Matrices

   The Capability Matrix maps Trust Tiers to Action Risk thresholds:

   +---------------+-------------+----------------------------------+
   | Tier          | Max A       | Permitted Action Classes         |
   +---------------+-------------+----------------------------------+
   | God Mode      | 100         | All actions                      |
   | Operator Mode | 85          | Read, Write, Execute (safe)      |
   | Analyst Mode  | 60          | Read (all), Write (append only)  |
   | Observer Mode | 30          | Read (public), Emit logs         |
   | Hibernation   | 5           | Heartbeat only                   |
   +---------------+-------------+----------------------------------+

   Note: Even if Tier permits an action class, the A <= E_trust check
   still applies. An Operator Mode agent (E_trust = 87) cannot perform
   an action with A = 90, even though the tier theoretically permits
   actions up to A = 85.


5.3.  Tier Transitions

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

   To prevent oscillation at tier boundaries, implementations MAY
   implement hysteresis:

   - Promotion requires E_trust >= threshold + 2
   - Demotion requires E_trust < threshold - 2

   This creates a 4-point buffer zone that prevents rapid tier
   switching when E_trust fluctuates near boundaries.


5.4.  Custom Tier Configuration

   Implementations MAY define custom tiers for domain-specific needs:

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


6.  Action Risk Classification

6.1.  Standard Action Classes

   The standard action classification taxonomy:

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


6.2.  Risk Score Assignment

   Action risk scores should be assigned based on:

   1. Reversibility: Can the action be undone?
      - Fully reversible: Lower A
      - Partially reversible: Medium A
      - Irreversible: Higher A

   2. Blast Radius: How many systems/users are affected?
      - Single record: Lower A
      - Single service: Medium A
      - Multiple services: Higher A
      - Entire system: Highest A

   3. Data Sensitivity: What type of data is involved?
      - Public data: Lower A
      - Internal data: Medium A
      - PII/PHI: Higher A
      - Credentials/keys: Highest A

   4. Regulatory Impact: Are there compliance implications?
      - No regulatory data: Baseline A
      - GDPR/CCPA data: +10 A
      - HIPAA/PCI data: +20 A
      - Classified data: +30 A


6.3.  Dynamic Risk Adjustment

   Action risk may be dynamically adjusted based on context:

   6.3.1. Target-Based Adjustment

   The same action has different risk based on target:

      DELETE /api/users/test-account    A = 50 (test environment)
      DELETE /api/users/production      A = 85 (production data)

   6.3.2. Volume-Based Adjustment

   Bulk operations carry higher risk:

      DELETE /api/records/1             A = 70 (single record)
      DELETE /api/records?all=true      A = 95 (bulk delete)

   6.3.3. Time-Based Adjustment

   Risk increases during critical periods:

      Base A = 60
      During maintenance window: A = 60 (no adjustment)
      During peak hours: A = 70 (+10)
      During live event: A = 80 (+20)


7.  Silent Veto Mechanics

7.1.  Veto Evaluation Order

   Enforcement follows a strict evaluation order:

   1. Trust Proof Validation
      - Signature valid?
      - Not expired?
      - If NO: DENY with INVALID_TRUST_PROOF

   2. Soul Veto (Sovereignty Check)
      - S = 1?
      - If YES: DENY with SOVEREIGNTY_CONSTRAINT

   3. Trust Tier Eligibility
      - Is action class permitted for tier?
      - If NO: DENY with TIER_RESTRICTION

   4. Zeroth Law (A <= E_trust)
      - Is A <= E_trust?
      - If NO: DENY with TRUST_INSUFFICIENT

   5. Custom Policy (Optional)
      - Any additional policy constraints?
      - If violated: DENY with POLICY_VIOLATION

   6. ALLOW

   This order ensures that sovereignty constraints are always
   evaluated first, followed by physics-based constraints, followed
   by tier restrictions, followed by any custom policies.


7.2.  Veto Response Codes

   HTTP response codes for KTP enforcement:

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

   Response body format:

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


7.3.  Veto Notification

   When a veto occurs, the PEP SHOULD notify relevant parties:

   1. Agent: Receives error response with details

   2. Flight Recorder: Receives full decision context

   3. Monitoring: Metrics updated (veto counter, by type)

   4. Alerting (optional): If veto rate exceeds threshold

   Agents SHOULD implement veto handling:

   - Parse veto response to understand reason
   - If TRUST_INSUFFICIENT: Reduce activity, wait for recovery
   - If SOVEREIGNTY_CONSTRAINT: Do not retry, seek remediation
   - If TIER_RESTRICTION: Request tier upgrade path
   - Log veto for own records


8.  Adaptive Dormancy

   Adaptive Dormancy is the mechanism by which agents gracefully
   reduce their activity as environmental conditions degrade,
   rather than failing catastrophically.

8.1.  Dormancy Triggers

   Dormancy is triggered by:

   1. Tier Demotion: When E_trust drops below tier threshold

   2. Velocity Warning: When dE/dt indicates rapid degradation

   3. Direct Signal: When Trust Oracle issues dormancy advisory

   4. Peer Signal: When peer agents report entering dormancy

   Dormancy is NOT a failure state. It is a survival strategy.
   An agent in dormancy is conserving resources and protecting
   the environment from actions it can no longer safely perform.


8.2.  Graceful Degradation

   When entering a lower tier, agents SHOULD:

   1. Complete in-flight operations if possible within timeout

   2. Release resources not needed for new tier

   3. Cancel scheduled operations that exceed new tier

   4. Notify dependent systems of capability reduction

   5. Enter reduced activity loop

   Degradation sequence example:

      E_trust drops from 88 to 68 (Operator → Analyst)

      Agent actions:
      1. Complete pending write operation (2 seconds)
      2. Cancel scheduled deployment (no longer permitted)
      3. Release infrastructure locks
      4. Notify orchestrator: "capability reduced to analyst"
      5. Enter read-only mode
      6. Continue monitoring for recovery


8.3.  Recovery Procedures

   When E_trust recovers above a tier threshold:

   1. Agent detects tier promotion via Trust Proof

   2. Agent verifies recovery is stable (E_trust maintained
      for minimum duration, e.g., 30 seconds)

   3. Agent gradually re-enables capabilities

   4. Agent resumes normal operations

   Recovery SHOULD be gradual to avoid oscillation:

      E_trust recovers from 68 to 88 (Analyst → Operator)

      Agent actions:
      1. Detect promotion in Trust Proof
      2. Wait 30 seconds to confirm stability
      3. Re-enable write capabilities
      4. Wait 30 seconds
      5. Re-enable service management capabilities
      6. Resume normal operations
      7. Notify orchestrator: "capability restored to operator"


8.4.  Hibernation Mode

   Hibernation is the most extreme dormancy state, entered when
   E_trust falls below 50.

   In Hibernation:
   - Agent performs NO operations except heartbeat
   - Heartbeat interval increases to conserve resources
   - Agent awaits external signal or Trust Score recovery
   - All state is preserved for potential recovery

   Heartbeat signal in hibernation:

      {
        "type": "heartbeat",
        "agent_id": "agent:7gen:optimized:a1b2c3d4",
        "state": "hibernating",
        "e_trust": 35,
        "hibernation_duration_seconds": 3600,
        "awaiting": "trust_recovery",
        "timestamp": "2025-11-25T12:00:00Z"
      }

   Hibernation exit requires:
   - E_trust >= 55 (with hysteresis buffer)
   - Sustained for minimum 60 seconds
   - No Soul veto active


9.  Mass Ceiling and Anti-Accumulation

   An agent that accumulates excessive trust becomes a systemic risk.
   Like a star that grows too massive, it can collapse catastrophically
   or distort the environment around it.

   This section specifies constraints to prevent dangerous mass
   accumulation.

9.1.  The Accumulation Problem

   Without constraints, agents can accumulate trust indefinitely:

   - Long tenure → high E_base
   - Many attestations → high resilience score
   - Critical role → high dependency

   This creates "too big to fail" agents:

   - Their failure would cascade across the system
   - They cannot be easily replaced or demoted
   - They may crowd out other agents
   - They accumulate disproportionate authority

   The physics metaphor: a star that exceeds the Chandrasekhar limit
   cannot remain stable. It must either shed mass or collapse.

9.2.  Mass Ceiling

   Every zone MUST define a Mass Ceiling: the maximum E_base any
   single agent may hold.

   Recommended ceilings by zone type:

   +------------+---------------+--------------------------------+
   | Zone Type  | Mass Ceiling  | Rationale                      |
   +------------+---------------+--------------------------------+
   | Deep Blue  | 95            | Critical systems need margin   |
   | Blue       | 92            | Production requires headroom   |
   | Cyan       | 90            | General operations             |
   | Green      | 95            | Minimal enforcement anyway     |
   +------------+---------------+--------------------------------+

   When an agent's E_base would exceed the ceiling:

   1. E_base is capped at ceiling (excess trust does not accumulate)
   2. Agent is flagged for mass review
   3. Options presented: mitosis, redistribution, or acceptance

9.3.  Mitosis Protocol

   When an agent exceeds mass ceiling or approaches systemic risk
   threshold, it may undergo Mitosis: controlled division into
   multiple smaller agents.

   Mitosis process:

   1. Agent (or operator) initiates mitosis request
   2. Trust Oracle evaluates agent's responsibilities
   3. Trust Oracle proposes division plan:
      - Which capabilities go to which child agent
      - How E_base is distributed
      - Dependency migration plan
   4. Operator approves division plan
   5. Child agents created with allocated E_base
   6. Dependencies migrated to appropriate children
   7. Parent agent retired or reduced

   E_base distribution in mitosis:

      E_base_child_1 + E_base_child_2 + ... <= E_base_parent

   Trust is conserved but may have overhead losses (children start
   slightly lower than parent's allocation due to newness).

   Example:

      Parent agent: E_base = 92 (at ceiling)
      Division: 3 children

      Child A (data operations): E_base = 45
      Child B (compute operations): E_base = 35
      Child C (admin operations): E_base = 40
      Total: 120, but capped to 92 with proportional reduction

      Actual allocation:
      Child A: 45 * (92/120) = 34.5 → 34
      Child B: 35 * (92/120) = 26.8 → 27
      Child C: 40 * (92/120) = 30.6 → 31
      Total: 92

9.4.  Systemic Risk Assessment

   Beyond individual mass ceiling, zones MUST assess systemic risk
   from agent concentration.

   Concentration metrics:

   1. Single Agent Dependency (SAD):
      What percentage of critical paths depend on one agent?
      Threshold: No agent should be on > 30% of critical paths

   2. Mass Concentration Index (MCI):
      What percentage of total zone trust is held by top N agents?
      Threshold: Top 5 agents should hold < 40% of total trust

   3. Failure Blast Radius (FBR):
      If this agent fails, how many others are affected?
      Threshold: No agent should have FBR > 20% of zone population

   When thresholds are exceeded:

   - Alert zone operators
   - Flag agents for mitosis review
   - Increase monitoring on concentrated agents
   - Consider architectural changes to reduce dependency

9.5.  Progressive Trust Taxation

   To discourage excessive accumulation, zones MAY implement
   progressive trust taxation: diminishing returns at high E_base.

   Formula:

      effective_E_base = E_base                        if E_base <= 70
      effective_E_base = 70 + 0.8*(E_base - 70)        if E_base <= 85
      effective_E_base = 82 + 0.5*(E_base - 85)        if E_base <= 95
      effective_E_base = 87 + 0.2*(E_base - 95)        if E_base > 95

   Example with taxation:

      Nominal E_base = 98
      Effective E_base = 70 + 0.8*(85-70) + 0.5*(95-85) + 0.2*(98-95)
                       = 70 + 12 + 5 + 0.6
                       = 87.6

   This does not prevent high-trust agents from existing, but it
   reduces the advantage of extreme accumulation, encouraging
   distribution of responsibilities.

9.6.  Anti-Accumulation in Federation

   Federated zones MUST coordinate on mass ceiling enforcement:

   - An agent at ceiling in Zone A should not accumulate freely in Zone B
   - Cross-zone mass is aggregated for ceiling calculation
   - Mitosis may span zones (child agents in different zones)

   Federation mass coordination:

      {
        "agent_id": "agent:persistent:mega-service",
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


10.  Latency Requirements

   Enforcement must be fast enough to not impede legitimate operations
   while thorough enough to maintain security.

   Target latency budget:

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

   To achieve these targets:

   1. Cache Trust Oracle public keys locally
   2. Cache action risk mappings locally
   3. Use async logging to Flight Recorder
   4. Pre-compute tier from E_trust
   5. Use efficient data structures (hash maps, not linear search)


11. Security Considerations

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


12. References

12.1.  Normative References

   [KTP-CORE]
              Perkins, C., "Kinetic Trust Protocol - Core
              Specification", NMCITRA, November 2025.

   [KTP-SENSORS]
              Perkins, C., "Kinetic Trust Protocol - Context Tensor
              Sensor Specification", NMCITRA, November 2025.

   [RFC2119]  Bradner, S., "Key words for use in RFCs to Indicate
              Requirement Levels", BCP 14, RFC 2119, March 1997.

12.2.  Informative References

   [KTP-AUDIT]
              Perkins, C., "Kinetic Trust Protocol - Flight Recorder
              Specification", NMCITRA, November 2025.

   [KTP-IDENTITY]
              Perkins, C., "Kinetic Trust Protocol - Vector Identity
              Specification", NMCITRA, November 2025.


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
