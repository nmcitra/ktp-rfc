
Kinetic Trust Protocol                                      C. Perkins
Specification Draft                                           NMCITRA
Version: 0.1                                             November 2025


               Kinetic Trust Protocol (KTP) - Human Integration

                    Humans, Agents, and System Ethics

===============================================================================

   "The question is not whether machines should have ethics.
    The question is whether the systems we build should."

===============================================================================

Abstract

   This document specifies how humans participate in the Kinetic Trust
   Protocol: as agents subject to physics-based constraints, as
   operators of KTP infrastructure, and as the ultimate source of
   system legitimacy.

   The specification addresses human-agent collaboration, the question
   of human override, accessibility requirements, and transparency
   obligations.

   Section 10 addresses the ethics of the system itself—not whether
   agents should have ethics (irrelevant in a physics-based model),
   but whether the constraints imposed by KTP are just, and who bears
   responsibility when physics prevents beneficial action.

   This section is marked DRAFT and invites expert debate.

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

   1.  Introduction  . . . . . . . . . . . . . . . . . . . . . . . .  3
       1.1.  The Human Question . . . . . . . . . . . . . . . . . . .  3
       1.2.  Scope  . . . . . . . . . . . . . . . . . . . . . . . . .  4
   2.  Terminology  . . . . . . . . . . . . . . . . . . . . . . . . .  5
   3.  Humans as Agents . . . . . . . . . . . . . . . . . . . . . . .  6
       3.1.  Human Agent Identity . . . . . . . . . . . . . . . . . .  6
       3.2.  Human Trust Scores . . . . . . . . . . . . . . . . . . .  8
       3.3.  Human Trajectories . . . . . . . . . . . . . . . . . . . 10
       3.4.  Human Tier Transitions . . . . . . . . . . . . . . . . . 11
   4.  Human-Agent Collaboration  . . . . . . . . . . . . . . . . . . 13
       4.1.  Delegation Patterns  . . . . . . . . . . . . . . . . . . 13
       4.2.  Supervision Models . . . . . . . . . . . . . . . . . . . 15
       4.3.  Capability Inheritance . . . . . . . . . . . . . . . . . 16
       4.4.  Accountability Chains  . . . . . . . . . . . . . . . . . 17
   5.  The Override Question  . . . . . . . . . . . . . . . . . . . . 19
       5.1.  Why No Override  . . . . . . . . . . . . . . . . . . . . 19
       5.2.  What Humans Can Do . . . . . . . . . . . . . . . . . . . 21
       5.3.  Emergency Procedures . . . . . . . . . . . . . . . . . . 22
       5.4.  The Governance Recursion . . . . . . . . . . . . . . . . 24
   6.  Accessibility  . . . . . . . . . . . . . . . . . . . . . . . . 25
       6.1.  Understanding Trust Scores . . . . . . . . . . . . . . . 25
       6.2.  Contesting Decisions . . . . . . . . . . . . . . . . . . 26
       6.3.  Remediation Pathways . . . . . . . . . . . . . . . . . . 27
   7.  Transparency . . . . . . . . . . . . . . . . . . . . . . . . . 29
       7.1.  Decision Explanation . . . . . . . . . . . . . . . . . . 29
       7.2.  Environmental Visibility . . . . . . . . . . . . . . . . 30
       7.3.  Audit Access . . . . . . . . . . . . . . . . . . . . . . 31
   8.  Human Factors  . . . . . . . . . . . . . . . . . . . . . . . . 32
       8.1.  Cognitive Load . . . . . . . . . . . . . . . . . . . . . 32
       8.2.  Trust Calibration  . . . . . . . . . . . . . . . . . . . 33
       8.3.  Adaptation and Training  . . . . . . . . . . . . . . . . 34
   9.  Security Considerations  . . . . . . . . . . . . . . . . . . . 35
   10. System Ethics (DRAFT)  . . . . . . . . . . . . . . . . . . . . 36
       10.1. The Obsolescence of Agent Ethics . . . . . . . . . . . . 36
       10.2. The Silent Veto Problem  . . . . . . . . . . . . . . . . 38
       10.3. Responsibility Attribution . . . . . . . . . . . . . . . 40
       10.4. Force Majeure vs. Negligence . . . . . . . . . . . . . . 42
       10.5. The Justice of Constraints . . . . . . . . . . . . . . . 44
       10.6. Open Questions . . . . . . . . . . . . . . . . . . . . . 46
   11. References . . . . . . . . . . . . . . . . . . . . . . . . . . 47
   Authors' Addresses . . . . . . . . . . . . . . . . . . . . . . . . 48


===============================================================================
                    PART I: HUMANS IN THE SYSTEM
===============================================================================

1.  Introduction

1.1.  The Human Question

   "Where do humans fit in all this?"

   This is invariably the first question asked about KTP. The protocol
   describes agents with Trust Scores, trajectories, lineages—language
   borrowed from physics and biology. It specifies autonomous operation
   under environmental constraints, Silent Vetoes that cannot be
   overridden, physics that doesn't negotiate.

   But humans built these systems. Humans operate them. Humans are
   affected by them. Where do humans fit?

   The answer is nuanced:

   1. Humans are agents within the system
      - Human actions are subject to A <= E_trust
      - Humans have Trust Scores, trajectories, tiers
      - The physics applies to humans too

   2. Humans are operators of the system
      - Humans deploy and configure KTP infrastructure
      - Humans tune sensors and weights
      - Humans respond to incidents

   3. Humans are NOT exempt from the system
      - No human override of the Zeroth Law
      - Administrators are agents within their administration
      - The governance recursion applies

   4. Humans are the source of system legitimacy
      - Humans choose to deploy KTP
      - Humans define zone boundaries
      - Humans can exit zones (opt out)
      - Consent is foundational

   This document specifies how these roles work in practice.

1.2.  Scope

   This document addresses:

   - How humans are represented as agents
   - How humans collaborate with non-human agents
   - What humans can and cannot do (the override question)
   - How the system must be accessible to humans
   - What transparency obligations exist
   - Ethical questions about the system itself

   This document does NOT address:

   - Agent ethics (obsolete in physics-based model; see Section 10.1)
   - AI alignment (different problem domain)
   - Sentience or consciousness (not relevant to KTP)


2.  Terminology

   Human Agent:
      A human user represented as an agent within KTP, with Trust
      Score, trajectory, and tier like any other agent.

   Delegation:
      A human authorizing a non-human agent to act with some portion
      of the human's Trust Score as backing.

   Supervision:
      A human monitoring and potentially intervening in non-human
      agent operations, within the constraints of physics.

   Override:
      An attempt to bypass the Zeroth Law (A <= E_trust). Not
      permitted in KTP.

   Adjustment:
      Legitimate modification of KTP parameters (sensor weights,
      action risk, zone configuration) by authorized humans.

   Remediation:
      The process by which a human (or agent) improves conditions
      to enable previously-vetoed actions.

   Governance Recursion:
      The principle that administrators are agents within the system
      they administer, subject to the same physics.

   System Ethics:
      Ethical questions about the design of KTP itself, as distinct
      from questions about agent behavior within KTP.


3.  Humans as Agents

3.1.  Human Agent Identity

   Humans are represented as agents with the same identity structures
   as non-human agents, with accommodations for human characteristics.

3.1.1.  Identity Structure

      {
        "agent_type": "human",
        "agent_id": "human:org:alice.smith",
        "identity_source": {
          "type": "federated",
          "provider": "okta",
          "subject": "alice.smith@example.com",
          "verified": "2025-11-25T10:00:00Z"
        },
        "lineage": {
          "type": "human",
          "generation": null,
          "sponsor": null,
          "tenure_start": "2022-03-15T00:00:00Z"
        },
        "trajectory": {
          "chain_hash": "sha256:abc...",
          "entries": 15247,
          "resilience_events": 3
        }
      }

   Key differences from non-human agents:

   - Lineage: Humans do not have generations or sponsors in the
     traditional sense. Tenure replaces generation as maturity signal.

   - Identity source: Human identity typically federated from existing
     IdP (Okta, Azure AD, etc.) rather than self-generated.

   - Trajectory: Human trajectories may span longer periods and
     include different action types than automated agents.

3.1.2.  Identity Binding

   Human agent identity binds to:

   - Primary authentication (SSO, MFA)
   - Device attestation (optional but recommended)
   - Location context (optional, privacy-sensitive)
   - Session continuity (for web/app interactions)

   The binding is designed to be:

   - Strong enough to prevent impersonation
   - Flexible enough for normal human behavior
   - Private enough to respect human dignity


3.2.  Human Trust Scores

   Humans have Trust Scores calculated similarly to other agents:

      E_trust = E_base × (1 - R)

   Where E_base reflects the human's demonstrated reliability and
   R reflects current environmental risk.

3.2.1.  Human E_base Calculation

   Human E_base factors:

   +------------------------+--------+--------------------------------+
   | Factor                 | Weight | Description                    |
   +------------------------+--------+--------------------------------+
   | Organizational tenure  | 0.20   | Time with organization         |
   | Role seniority         | 0.15   | Position level                 |
   | Training completion    | 0.15   | Security/compliance training   |
   | Historical reliability | 0.25   | Past behavior record           |
   | Incident history       | 0.15   | Past security incidents        |
   | Peer attestation       | 0.10   | Colleague vouching             |
   +------------------------+--------+--------------------------------+

   Example calculation:

      Tenure: 3 years (score: 0.75)
      Role: Senior Engineer (score: 0.70)
      Training: Complete (score: 1.00)
      History: Clean (score: 0.90)
      Incidents: One minor (score: 0.80)
      Peers: Two attestations (score: 0.85)

      E_base = (0.20×75 + 0.15×70 + 0.15×100 + 0.25×90 +
                0.15×80 + 0.10×85)
             = 15 + 10.5 + 15 + 22.5 + 12 + 8.5
             = 83.5

3.2.2.  Human Trust Score Volatility

   Human Trust Scores should be LESS volatile than automated agent
   scores:

   - Humans cannot refresh credentials every 10 seconds
   - Human behavior is inherently variable
   - Frequent tier transitions are disruptive to human work

   Recommended dampening:

   - Minimum 5-minute averaging window for human R calculation
   - Hysteresis of ±5 points at tier boundaries
   - Alert human before tier demotion (where possible)

3.2.3.  Privacy Considerations

   Human Trust Scores raise privacy concerns not present for
   automated agents:

   - Trust Score MAY be visible to the human themselves
   - Trust Score SHOULD NOT be visible to peers by default
   - Trust Score MAY be visible to direct management
   - Trust Score MUST be available for legitimate audit
   - Trust Score MUST NOT be used for purposes beyond authorization

   The goal is authorization, not surveillance.


3.3.  Human Trajectories

   Human trajectories record authorization decisions over time,
   forming the basis for Proof of Resilience.

3.3.1.  What Gets Recorded

   For human agents, record:

   - Authorization decisions (allow/deny)
   - Action type and risk level
   - Environmental context at time of action
   - Trust Score at time of action
   - Outcome (if determinable)

   Do NOT record:

   - Content of communications
   - Detailed activity logs beyond authorization
   - Location beyond zone-level
   - Personal information not needed for authorization

3.3.2.  Trajectory Interpretation

   Human trajectories differ from automated agents:

   - Longer time scales (careers, not microseconds)
   - More variable patterns (humans have bad days)
   - Context-dependent (humans respond to life events)
   - Privacy-protected (less detail appropriate)

   Interpretation should account for human nature without excusing
   genuinely problematic patterns.


3.4.  Human Tier Transitions

   Humans transition between tiers like other agents, but with
   accommodations for human factors.

3.4.1.  Tier Boundaries for Humans

   The standard tier boundaries apply:

   - God Mode: E_trust >= 95 (rare for humans)
   - Operator Mode: E_trust >= 85
   - Analyst Mode: E_trust >= 70
   - Observer Mode: E_trust >= 50
   - Hibernation: E_trust < 50

   However, most humans operate in Analyst or Operator mode for
   daily work. God Mode should be exceptional.

3.4.2.  Demotion Notification

   When a human is demoted, the system SHOULD:

   1. Notify the human of demotion (if safe to do so)
   2. Explain the contributing factors
   3. Provide remediation guidance
   4. Offer escalation path

   The system SHOULD NOT:

   - Demote without explanation
   - Make demotion public to peers
   - Prevent the human from seeking help

3.4.3.  Promotion Path

   Humans can improve their Trust Score through:

   - Time (continued reliable operation)
   - Training (completing security courses)
   - Attestation (peer vouching)
   - Remediation (addressing identified issues)
   - Environmental improvement (lower R)

   Unlike automated agents, humans cannot simply "wait for the
   environment to recover." Humans can take active steps.


===============================================================================
                    PART II: COLLABORATION AND CONTROL
===============================================================================

4.  Human-Agent Collaboration

4.1.  Delegation Patterns

   Humans routinely delegate tasks to automated agents. KTP provides
   structured delegation with trust constraints.

4.1.1.  Delegation Structure

      {
        "delegation_id": "del-abc-123",
        "delegator": "human:org:alice.smith",
        "delegate": "agent:bot:data-processor",
        "scope": {
          "actions": ["read_data", "transform_data", "write_report"],
          "max_action_risk": 50,
          "resources": ["dataset:sales-q3", "report:quarterly"],
          "time_bound": {
            "start": "2025-11-25T09:00:00Z",
            "end": "2025-11-25T17:00:00Z"
          }
        },
        "trust_constraints": {
          "max_e_trust": 65,
          "cannot_exceed_delegator": true,
          "revocable": true
        }
      }

   Key principles:

   - Delegate cannot exceed delegator's Trust Score
   - Delegation is scoped (actions, resources, time)
   - Delegation is revocable
   - Delegator remains accountable

4.1.2.  Trust Ceiling

   A delegated agent's effective Trust Score is bounded by:

      E_trust_delegate <= min(E_trust_delegator, delegation_max)

   If Alice (E_trust = 78) delegates to a bot with max_e_trust = 65:
      Bot's E_trust ceiling = min(78, 65) = 65

   If Alice's Trust Score drops to 60:
      Bot's E_trust ceiling = min(60, 65) = 60

   The delegate cannot exceed the delegator.

4.1.3.  Delegation Chains

   Delegation can chain: Human → Agent A → Agent B

   Trust ceiling propagates:

      E_trust_B <= min(E_trust_A, E_trust_human, delegation_max_A,
                       delegation_max_B)

   Long chains rapidly constrain capability, which is intentional.

4.2.  Supervision Models

   Humans may supervise automated agents at various levels:

4.2.1.  Active Supervision

   Human reviews and approves each significant action:

   - Agent proposes action
   - Human reviews proposal
   - Human approves or rejects
   - Agent executes if approved

   Appropriate for: High-risk actions, learning phase, sensitive data

   Trust implication: Agent operates at human's tier (human is
   effectively the actor)

4.2.2.  Passive Supervision

   Human monitors but does not approve each action:

   - Agent operates autonomously
   - Human receives activity summary
   - Human can intervene if needed
   - Human reviews outcomes periodically

   Appropriate for: Routine operations, established agents, lower risk

   Trust implication: Agent operates at own tier, human provides
   oversight but not direct control

4.2.3.  Exceptional Supervision

   Human is notified only for anomalies:

   - Agent operates fully autonomously
   - Agent self-monitors for anomalies
   - Human alerted only on exceptions
   - Human investigates alerts

   Appropriate for: Mature agents, stable environments, high volume

   Trust implication: Agent fully autonomous, human as backstop

4.3.  Capability Inheritance

   When humans and agents collaborate, capabilities combine:

4.3.1.  Human Providing Context

   A human may provide environmental context that affects agent
   capability:

   - Human's presence may lower Observer dimension
   - Human attestation may boost agent's E_base temporarily
   - Human supervision may allow higher-risk actions

   Example: Agent requests action with A = 70, has E_trust = 65.
   Human (E_trust = 85) actively supervises and co-signs.
   Combined E_trust for supervised action = min(85, 65+15) = 80.
   Action permitted.

4.3.2.  Agent Extending Human

   An agent may extend human capabilities within constraints:

   - Agent operates faster than human could
   - Agent processes more data than human could
   - Agent maintains consistency human might not
   - BUT agent cannot exceed human's authority

4.4.  Accountability Chains

   When humans delegate to agents, accountability flows:

4.4.1.  Accountability Principle

   The delegating human remains accountable for:

   - Appropriate scope of delegation
   - Appropriate choice of delegate
   - Monitoring of delegated activity
   - Responding to problems

   The delegate agent is accountable for:

   - Operating within delegated scope
   - Maintaining own trajectory
   - Reporting issues to delegator
   - Not exceeding authority

4.4.2.  Incident Attribution

   When a delegated agent causes an incident:

   1. Agent directly responsible for action
   2. Human responsible for delegation decision
   3. Organization responsible for system design

   Flight Recorder captures full chain for forensic analysis.


5.  The Override Question

5.1.  Why No Override

   "But what if a human needs to override the system?"

   This question reveals a misunderstanding of KTP's nature. The
   Zeroth Law is not a policy that can be suspended. It is physics.
   Asking for override is like asking to override gravity.

5.1.1.  The Physics Argument

   KTP models trust as environmental capacity. When A > E_trust,
   the environment cannot safely absorb the action's risk. Allowing
   the action doesn't change this reality; it just proceeds without
   the environment's support.

   An override would be saying: "I know the environment cannot
   support this action, but do it anyway." This is precisely how
   incidents happen.

5.1.2.  The Incentive Argument

   If override exists, it will be used:

   - Under deadline pressure ("just this once")
   - To avoid inconvenience ("I know what I'm doing")
   - Because of authority ("I'm the VP")
   - In emergencies (where it's most dangerous)

   Every override creates precedent. The exception becomes the rule.
   Soon, the system provides theater of security without substance.

5.1.3.  The Equality Argument

   Override creates two classes: those who can override and those
   who cannot. This undermines the fundamental premise that physics
   applies equally to all agents.

   If the CEO can override, the CEO's compromised account can
   override. The attack surface expands with every override path.

5.2.  What Humans Can Do

   No override does not mean no human agency. Humans have legitimate
   paths to enable actions that would otherwise be vetoed:

5.2.1.  Improve the Environment

   If E_trust is too low because environmental risk is high, address
   the environmental risk:

   - Reduce threat level (resolve the incident)
   - Add capacity (scale resources)
   - Lower stakes (reduce blast radius)
   - Improve monitoring (reduce uncertainty)

   This is the legitimate response to "the system won't let me."
   Fix the environment, don't bypass physics.

5.2.2.  Reduce Action Risk

   If action risk A is too high, restructure the action:

   - Break into smaller steps (each with lower A)
   - Add reversibility (lower effective risk)
   - Reduce scope (fewer systems affected)
   - Add verification (catch errors before impact)

   A well-designed action often has lower risk than a hasty one.

5.2.3.  Adjust the System (Legitimately)

   Humans with appropriate Trust Scores can adjust KTP parameters:

   - Recalibrate sensor weights (if justified)
   - Reclassify action risk (if evidence supports)
   - Adjust tier boundaries (for domain-specific needs)
   - Modify zone configuration (within governance)

   These adjustments are themselves actions with risk scores.
   Adjusting the system to enable a specific action is logged and
   auditable. If the adjustment was inappropriate, accountability
   follows.

5.2.4.  Accept Constraints

   Sometimes the right answer is: "No, not right now."

   The action is too risky for current conditions. This is the
   system working correctly. Accept the constraint and wait for
   conditions to improve, or find an alternative approach.

5.3.  Emergency Procedures

   "But what about genuine emergencies?"

5.3.1.  The Emergency Paradox

   Emergencies are precisely when the Zeroth Law is most important:

   - Decisions are hasty
   - Pressure is high
   - Verification is skipped
   - Mistakes are most likely
   - Consequences are largest

   Override during emergency is maximum risk at minimum judgment.

5.3.2.  Pre-Authorized Emergency Actions

   Instead of override, pre-authorize emergency actions:

   - Define emergency procedures in advance
   - Assign appropriate action risk (may be high)
   - Require corresponding Trust Score
   - Pre-position high-trust agents for emergency response

   Example: "Break glass" action to shut down a system.
   A = 90 (high risk, major impact)
   Requires E_trust >= 90
   Pre-authorized for incident commanders
   Logged immediately to Flight Recorder

   This is not override. It is a legitimate high-risk action
   performed by an agent with sufficient trust.

5.3.3.  Emergency Trust Boost

   In genuine emergencies, environmental factors may actually
   INCREASE available trust:

   - Declared emergency lowers some risk weights
   - Incident response mode adjusts tier boundaries
   - But this is system configuration, not bypass

   The adjustment is pre-defined, automatic, and logged.

5.4.  The Governance Recursion

   Article VII of the Constitution states that administrators are
   agents within the system they administer.

5.4.1.  Administrators as Agents

   A human administrator:

   - Has a Trust Score like any agent
   - Is subject to A <= E_trust
   - Cannot configure the system beyond their authority
   - Is logged to the Flight Recorder

   If an administrator wants to make a high-risk configuration
   change, they must have sufficient Trust Score to do so.

5.4.2.  No Self-Exemption

   An administrator cannot:

   - Exempt themselves from the Zeroth Law
   - Grant themselves unlimited Trust Score
   - Create backdoors that bypass physics
   - Modify their own audit records

   The moment administrators can exempt themselves, the physics
   becomes policy, and policy can be ignored.


===============================================================================
                    PART III: HUMAN EXPERIENCE
===============================================================================

6.  Accessibility

   KTP must be accessible to the humans who operate within it.

6.1.  Understanding Trust Scores

   Humans should be able to understand their own Trust Score:

6.1.1.  Visibility Requirements

   Every human agent MUST be able to see:

   - Their current E_trust
   - Their E_base and how it's calculated
   - The current R (environmental risk)
   - Their current tier
   - Recent trajectory summary

6.1.2.  Explanation Requirements

   The system MUST explain Trust Score in plain language:

   Good:
      "Your Trust Score is 72. This is calculated from your base
       trust of 85 reduced by 15% due to current elevated threat
       conditions. You can perform Analyst-level actions."

   Bad:
      "E_trust = 72.4 (E_base=85.2, R=0.15, tier=2)"

6.2.  Contesting Decisions

   Humans must be able to contest KTP decisions:

6.2.1.  Contest Process

   1. Human requests explanation for specific denial
   2. System provides Decision Geometry from Flight Recorder
   3. Human reviews contributing factors
   4. Human can request human review if disagreement persists
   5. Human reviewer evaluates (also subject to KTP)
   6. Decision either upheld or system adjustment made

6.2.2.  Contest Limitations

   Contesting does not mean override:

   - Contest reviews whether the system worked correctly
   - If system worked correctly, denial stands
   - If system misconfigured, adjustment made (globally, not case-specific)
   - Contest is not appeal for exception

6.3.  Remediation Pathways

   When denied, humans should know how to improve:

6.3.1.  Remediation Guidance

   For each denial, provide:

   - What was denied
   - Why (Trust Score, tier, specific constraint)
   - What would be needed (E_trust >= X)
   - How to achieve it (options)

   Example:

      "Your request to deploy to production was denied.
       Required: E_trust >= 85 (Operator tier)
       Current: E_trust = 72 (Analyst tier)

       Options:
       1. Request supervision from Operator-tier colleague
       2. Wait for threat level to decrease (est. 2 hours)
       3. Deploy to staging instead (A = 60, permitted)
       4. Request Trust Score review if you believe this is error"

6.3.2.  No Dead Ends

   Every denial should offer a path forward. "No, and there's nothing
   you can do" is a system design failure.


7.  Transparency

7.1.  Decision Explanation

   Every KTP decision affecting a human must be explainable.

7.1.1.  Explanation Components

   - What: The action requested
   - Result: Allow or deny
   - Why: The specific constraint triggered
   - Context: Environmental state at time of decision
   - History: How this compares to past decisions

7.1.2.  Explanation Timeliness

   - Real-time: Immediate indication of allow/deny
   - On-demand: Detailed explanation within seconds
   - Audit: Complete forensic detail available

7.2.  Environmental Visibility

   Humans should understand the environment affecting them:

7.2.1.  Dashboard Requirements

   Provide human-readable display of:

   - Current Context Tensor state
   - Trend (improving or degrading)
   - Major contributing factors
   - Expected evolution

7.2.2.  Alert Requirements

   Notify humans proactively of:

   - Significant environmental changes
   - Impending tier transitions
   - Relevant security events
   - System status changes

7.3.  Audit Access

   Humans should be able to audit their own records:

7.3.1.  Self-Audit Rights

   Every human agent has the right to:

   - View their own trajectory
   - View decisions affecting them
   - Export their own data
   - Request correction of errors

7.3.2.  Audit Limitations

   Self-audit does not include:

   - Other agents' records
   - System-wide analytics (unless authorized)
   - Security-sensitive details
   - Unredacted Flight Recorder access


8.  Human Factors

8.1.  Cognitive Load

   KTP should minimize cognitive burden on humans:

8.1.1.  Simplification

   - Present tier rather than numeric score where possible
   - Use color coding (green/yellow/red)
   - Hide complexity unless requested
   - Default to least surprising behavior

8.1.2.  Automation

   - Auto-refresh Trust Proofs (humans shouldn't manage this)
   - Auto-select appropriate tier for context
   - Auto-explain denials
   - Auto-suggest remediation

8.2.  Trust Calibration

   Humans develop mental models of the system. These should be
   accurate:

8.2.1.  Predictability

   The system should be predictable:

   - Same conditions → same outcome
   - Gradual changes → gradual effects
   - No surprising tier transitions
   - Consistent explanations

8.2.2.  Feedback

   Provide feedback to calibrate expectations:

   - "You're approaching tier boundary"
   - "Environmental risk is elevated"
   - "This action has risk X, your limit is Y"

8.3.  Adaptation and Training

   Humans need support in adapting to KTP:

8.3.1.  Training Requirements

   All human agents should understand:

   - Basic KTP concepts (Trust Score, tiers, Zeroth Law)
   - How their role maps to KTP
   - What actions require what tier
   - How to respond to denial
   - Who to contact for help

8.3.2.  Gradual Introduction

   Migration stages (see [KTP-MIGRATION]) provide adaptation time:

   - Shadow mode: See what would happen
   - Advisory mode: Receive recommendations
   - Canary mode: Experience real constraints
   - Full mode: Operate normally


9.  Security Considerations

9.1.  Human-Specific Risks

   Credential Theft:
      Human credentials can be stolen via phishing, malware, etc.
      KTP provides defense-in-depth: stolen credential has Trust
      Score of legitimate user, limited by current environment.

   Coercion:
      Humans can be coerced to act against interest. KTP cannot
      prevent this but can limit blast radius through constraints.

   Insider Threat:
      Malicious insiders operate within their Trust Score. KTP
      ensures they cannot exceed earned capability.

   Social Engineering:
      Attackers may manipulate humans into delegation or other
      trust-related actions. Training and monitoring essential.

9.2.  Mitigations

   - MFA for human authentication
   - Device attestation for session binding
   - Behavioral analysis for anomaly detection
   - Delegation review for unusual patterns
   - Separation of duties for high-risk actions


===============================================================================
                    PART IV: SYSTEM ETHICS
===============================================================================

10.  System Ethics (DRAFT)

   This section addresses ethical questions about the design of KTP
   itself. It is marked DRAFT to invite expert review and debate.

   These questions are worthy of serious consideration. The authors
   do not claim definitive answers but offer this framework to
   structure the discussion.

10.1.  The Obsolescence of Agent Ethics

   A fundamental claim of KTP is that agent ethics—the question of
   whether an autonomous agent has good or bad intentions—becomes
   irrelevant in a physics-based model.

10.1.1.  The Traditional Ethics Problem

   Traditional approaches to AI safety ask: "How do we ensure AI
   agents have aligned values, good intentions, and ethical
   behavior?"

   This question assumes that agent intent matters—that an agent
   with good values will do good things, and an agent with bad
   values will do bad things.

10.1.2.  The Physics Response

   KTP responds: "Agent intent doesn't matter because agents can
   only do what the environment permits."

   A = 80, E_trust = 60 → Action denied, regardless of intent.
   A = 40, E_trust = 60 → Action allowed, regardless of intent.

   The agent's values, goals, or ethics are irrelevant to the
   calculation. The environment has veto power over agent intent.

   An agent that "wants" to do harm cannot do harm exceeding its
   Trust Score. An agent that "wants" to help cannot help beyond
   its Trust Score. The physics constrains all agents equally.

10.1.3.  The Limits of This Claim

   This does not mean ethics is irrelevant. It means the LOCUS of
   ethical consideration shifts:

   - FROM: "Is this agent ethical?"
   - TO: "Is this system ethical?"

   We no longer ask whether individual agents have good values.
   We ask whether the constraints imposed by the system are just.

   This is the question the rest of Section 10 addresses.

10.2.  The Silent Veto Problem

   "If the Silent Veto prevents an action that would have saved
   lives, who is responsible?"

   This is the central ethical challenge of KTP.

10.2.1.  The Scenario

   Consider: A fire breaks out in a building. An automated system
   could unlock all doors to enable evacuation. But the system's
   Trust Score has been deflated by the crisis itself (high Heat,
   high threat indicators). A > E_trust. The action is vetoed.
   People are harmed.

   The system did exactly what it was designed to do. The physics
   worked correctly. And yet harm occurred that might have been
   prevented.

   Who is responsible?

10.2.2.  Possible Positions

   Position A: The System is Not Responsible

      The system correctly evaluated that the environment could not
      safely support the action. Unlocking all doors during a crisis
      could also enable attackers, trap people in dangerous areas,
      or cause other harm. The system made a conservative judgment
      appropriate to uncertainty.

      Responsibility lies with:
      - Those who caused the fire (proximate cause)
      - Those who designed the building (safety systems)
      - Those who configured the Trust Score (calibration)
      - Not the system that correctly evaluated constraints

   Position B: The System is Partially Responsible

      The system's designers knew that conservative constraints
      would sometimes prevent beneficial actions. They chose to
      accept this tradeoff. This choice carries moral weight.

      Responsibility is shared:
      - System designers (for the tradeoff)
      - System operators (for specific configuration)
      - External actors (for the crisis itself)

   Position C: The System Should Not Make Such Decisions

      Life-safety actions should be exempt from Trust Score
      constraints. Physics should not override the preservation
      of human life.

      This position argues for carving out exceptions for
      specific action categories.

10.2.3.  The Authors' Tentative View

   We lean toward Position B with important caveats:

   1. The tradeoff is explicit and intentional
      - KTP knowingly accepts false positives (blocking beneficial
        actions) to prevent false negatives (allowing harmful actions)
      - This is a design choice with moral weight
      - Designers bear responsibility for this choice

   2. The calibration matters enormously
      - A system that vetoes life-safety actions frequently is
        miscalibrated
      - Proper configuration should make such scenarios rare
      - Operators who miscalibrate bear responsibility

   3. Position C is a slippery slope
      - Every exemption creates an attack vector
      - "Life safety" can be claimed for almost anything
      - Exemptions undermine the physics model entirely
      - We reject categorical exemptions while acknowledging the
        moral cost

   4. The alternative is worse
      - A system that can be overridden "for good reasons" will
        be overridden for bad reasons
      - The harm from a exploitable system exceeds the harm from
        occasional false positives
      - This is a tragic tradeoff, not a happy solution

10.3.  Responsibility Attribution

   When harm occurs in a KTP-governed system, how is responsibility
   attributed?

10.3.1.  The Causal Chain

   For any incident, multiple parties may bear responsibility:

   1. Proximate cause: Who or what directly caused the harm?
   2. Environmental cause: What conditions enabled the harm?
   3. Configuration cause: Was the system properly calibrated?
   4. Design cause: Does the system design create this risk?
   5. Deployment cause: Was this the right system for this context?

10.3.2.  The Flight Recorder's Role

   The Flight Recorder provides evidence for attribution:

   - What was the agent's Trust Score?
   - What was the environmental state?
   - Was the action correctly classified?
   - Did the system behave as designed?

   This enables forensic analysis distinguishing:
   - System working correctly (design responsibility)
   - System misconfigured (operator responsibility)
   - System malfunctioning (technical failure)
   - External factors (force majeure)

10.3.3.  Attribution Framework

   We propose the following framework:

   If the system ALLOWED an action that caused harm:
      - Was action risk correctly classified? (If no: calibration error)
      - Was Trust Score correctly calculated? (If no: technical error)
      - Were sensors functioning? (If no: operational error)
      - If all correct: The system permitted an action within
        constraints that still caused harm. This is residual risk
        accepted by the design.

   If the system DENIED an action that would have prevented harm:
      - Was denial correct per Zeroth Law? (If yes: design tradeoff)
      - Was action risk over-classified? (If yes: calibration error)
      - Was Trust Score incorrectly deflated? (If yes: technical error)
      - Was environment incorrectly assessed? (If yes: sensor error)

10.4.  Force Majeure vs. Negligence

   A critical distinction in responsibility attribution.

10.4.1.  Force Majeure (Environmental Force)

   The system correctly evaluated conditions and appropriately
   constrained actions. Harm resulted from external factors beyond
   the system's control.

   Characteristics:
   - System behaved as designed
   - Configuration was appropriate
   - Sensors were accurate
   - Environmental conditions genuinely degraded
   - Harm was not reasonably preventable by system

   Responsibility: External factors, not system or operators

10.4.2.  Negligence (Human Failure)

   The system was misconfigured, poorly maintained, or inappropriately
   deployed. Harm resulted from human failure to properly operate
   the system.

   Characteristics:
   - Miscalibration of risk or trust
   - Ignored sensor failures
   - Inappropriate system for context
   - Known issues unaddressed
   - Harm was preventable with proper operation

   Responsibility: Operators and/or designers

10.4.3.  The Boundary

   The boundary between force majeure and negligence is often
   contested. KTP's Flight Recorder provides evidence, but
   interpretation requires judgment.

   Key questions:
   - Was this configuration reasonable at deployment time?
   - Were warning signs ignored?
   - Is this a known limitation that was accepted?
   - Would a reasonable operator have done differently?

10.5.  The Justice of Constraints

   Are KTP's constraints just? This is perhaps the deepest question.

10.5.1.  Constraints as Enablement

   The Constitution frames constraints positively:

      "Freedom without constraint is not freedom but randomness.
       An agent is not free because it can do anything, but because
       it acts within the bounds of what the environment can safely
       support."

   Constraints enable trust. Without them, every agent is suspect.
   With them, agents can earn and accumulate trust, enabling greater
   capability over time.

10.5.2.  Constraints as Limitation

   Critics might argue:

   - Constraints limit beneficial actions
   - Trust Scores may reflect bias or history unfairly
   - The "physics" is still human-designed and value-laden
   - Those who configure constraints hold power over others

   These concerns deserve serious consideration.

10.5.3.  Addressing the Concerns

   On limiting beneficial actions:
      Yes, this is the acknowledged tradeoff. The question is whether
      the alternative (unlimited action, unlimited risk) is better.
      We argue it is not.

   On bias in Trust Scores:
      Trust Scores should be based on demonstrated behavior, not
      demographic characteristics. If a Trust Score system
      incorporates bias, it should be corrected. The physics model
      does not require bias; implementations must be vigilant.

   On human design of "physics":
      Yes, this physics is designed, not discovered. The values
      embedded in the design should be explicit, debatable, and
      adjustable through governance. The Constitution provides
      amendment procedures.

   On power of configurators:
      The Governance Recursion (Article VII) addresses this:
      configurators are agents within the system. They cannot
      exempt themselves. Their configuration actions are logged.
      They are accountable.

10.5.4.  The Consent Foundation

   Ultimately, KTP's legitimacy rests on consent:

   - Zones are opt-in (no one is forced into a Blue Zone)
   - Humans can exit (take actions outside the zone)
   - Governance is transparent (rules are published)
   - Amendment is possible (the system can evolve)

   A system of constraints is just if those subject to it have
   meaningfully consented to it and can meaningfully exit.

10.6.  Open Questions

   We do not claim to have resolved these questions. We offer them
   for ongoing discussion:

   10.6.1. Is there any action that should never be vetoed?

      If so, how do we define it without creating an exploitable
      exemption? If not, how do we accept the moral weight of
      vetoing genuinely beneficial actions?

   10.6.2. How do we handle genuine uncertainty about consequences?

      The Silent Veto prevents actions whose risk exceeds trust.
      But risk estimation is uncertain. How confident must we be
      in our risk assessment to impose constraints?

   10.6.3. Who has standing to contest system design?

      If someone is harmed by a correct system operation (Position B
      above), can they seek remedy? From whom? Through what process?

   10.6.4. How do we prevent constraint creep?

      As systems operate, there may be pressure to increase
      constraints (more conservative, more vetoes). How do we
      maintain appropriate balance?

   10.6.5. What is the right level of transparency?

      Full transparency enables gaming. Insufficient transparency
      prevents accountability. Where is the balance?

   10.6.6. Can physics-based constraints be truly neutral?

      Or do they inevitably embed the values of their designers?
      If the latter, how do we govern those values democratically?

   These questions deserve expert attention from ethicists, lawyers,
   policymakers, and affected communities. This specification is
   technical; the ethics are for society to resolve.


11.  References

11.1.  Normative References

   [KTP-CORE]
              Perkins, C., "Kinetic Trust Protocol - Core
              Specification", NMCITRA, November 2025.

   [KTP-MIGRATION]
              Perkins, C., "Kinetic Trust Protocol - Migration
              Guide", NMCITRA, November 2025.

11.2.  Informative References

   [CONSTITUTION]
              Perkins, C., "The Constitution of Digital Physics",
              NMCITRA, November 2025.


Authors' Addresses

   Chris Perkins
   New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

   Email: cperkins@nmcitra.org
