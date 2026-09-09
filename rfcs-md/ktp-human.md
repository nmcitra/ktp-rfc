# Kinetic Trust Protocol (KTP) - Human Integration Humans, Agents, and System Ethics


This document specifies how humans participate in the Kinetic Trust Protocol: as agents subject to structural constraints, as operators of KTP infrastructure, and as the ultimate source of system legitimacy.

The specification addresses human-agent collaboration, the question of human override, accessibility requirements, and transparency obligations.

The final section addresses the ethics of the system itself—not whether agents should have ethics (irrelevant in a structurally constrained model), but whether the constraints imposed by KTP are just, and who bears responsibility when the constraints prevent beneficial action.

This section is marked DRAFT and invites expert debate.

# Introduction

Humans participate as operators, delegators, reviewers, and people affected by KTP decisions. Human authorization uses operation-specific eligibility under specifications/human-eligibility.md. A person does not receive a general Trust Score, resilience accumulator, or ranked tier. Eligibility for one operation says nothing about personal worth or entitlement to protection, explanation, and review.

A human request MUST satisfy the current grant, qualification, scope, purpose, and safety requirements of the particular operation. Eligibility is an additional prerequisite, never permission by itself. The unconditional capacity gate and independent Soul veto remain binding. A qualified administrator cannot waive either.

This document covers human identity, delegation, supervision, explanation, correction, and the governance of these requirements. Its final DRAFT discussion invites scrutiny of the system's legitimacy; it does not create exceptions to the normative requirements above it.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

# Terminology

Human Principal: A person whose identity and principal type have been independently authenticated by the deployment's trusted identity integration.

Operational Eligibility: Satisfaction of declared requirements for one operation and exact scope at the time of evaluation. It is neither a person score nor an authorization token.

Delegation: A currently authorized principal granting a bounded subset of their authority to another authenticated actor. It does not transfer qualifications, capacity, historical standing, or readiness.

Supervision: A qualified and authorized human reviewing or monitoring agent operations. Any required approval adds a gate; it cannot remove a gate.

Correction: An authorized change to an erroneous fact, identity association, evidence status, or application of a requirement, followed by a fresh evaluation.

Override: Permission to execute a candidate action despite a valid current capacity or Soul veto. Prohibited.

Governance Recursion: Administrators and reviewers are subject to the operation-specific authority and safety requirements of their own actions. Holding office does not supply an exemption.

# Human Identity and Eligibility

## Identity Binding

Identity SHOULD use established authentication, including MFA and session binding where appropriate. A deployment MUST authenticate principal type, issuer, subject, session, and the actor actually executing an operation. A request's self-declared human label MUST NOT bypass software-agent readiness. Human identifiers SHOULD be opaque and scoped; names, email addresses, tenure, and employment histories are not required wire identifiers.

Human records MUST NOT be forced into software-agent lineage, generation, model, E_base, or tier fields by inventing values. The closed trajectory-v3 schema continues to describe software-agent state. Human eligibility uses its own versioned records, with personal evidence protected under specifications/privacy-evidence.md.

Identity verification is not proof of eligibility. A valid login establishes who is asking; current grants and evidence establish which specific requirements are met.

## Explicit Requirements

The installed, approved human eligibility profile MUST identify each supported operation, its exact scope and purpose, required qualifications and assessment criteria, permitted evidence issuers, and authorized grant issuers. It MUST bind the governing authority, review route, retention policy, and issuer registry. The canonical profile digest and minimum accepted version MUST be independently installed and protected against rollback.

Relevant training or professional credentials MAY satisfy a specific requirement when their authority, scope, evidence, and validity are established. Role MAY confer a specific grant. Organizational tenure, seniority, generic incident totals, peer popularity, and inferred character MUST NOT be converted into general trust points or automatic privileges. No covert personality, emotion, or loyalty inference is permitted.

Every required item MUST be current, correctly associated with the authenticated person, applicable to the actual operation and scope, and accepted under the current evidence and revocation state. Missing, expired, corrected, revoked, or unverifiable evidence MUST prevent dependent eligibility. An expired recovery qualification MUST NOT disable unrelated operations whose requirements remain met, nor access to explanation, correction, assistance, or basic protections.

The checkable profile and decision-body formats are schemas/human-eligibility-profile.json and schemas/human-eligibility-decision.json. Schema validity alone does not establish issuer authority, evidence truth, assessment adequacy, identity, or permission. The reference evaluator's supported exact scopes and direct delegations are deliberately bounded; unsupported matches or longer chains require a separately reviewed implementation and MUST NOT be silently accepted.

## Capacity Is a Separate Requirement

The deployment MUST define comparable demand and current capacity for the particular operation through its approved evaluation profile. Credentials or employment history MUST NOT be substituted for measured capacity or converted into a replacement human E_base. When adequate capacity evidence cannot be established, the dependent operation MUST remain unavailable; a fabricated score is not remediation.

All existing input-validity, zero-capacity, A > E, threshold, sovereignty, grant, and Soul checks remain binding. Eligibility adds no numeric increment and MUST NOT reverse any prior veto. A <= E alone is never sufficient authorization. Software agents retain their own historical standing and current scoped readiness under specifications/operational-readiness.md.

## Sessions and Freshness

A human-facing session MAY remain open while its backend refreshes short-lived authorization evidence. This MUST NOT extend an ordinary proof beyond ten seconds, renew expired qualifications, or delay known invalidation. The previous human-specific five-minute risk averaging and tier hysteresis recommendations MUST NOT be used to defer a safety response. No repeated manual login every ten seconds is required by this specification.

Current eligibility, delegated scope, and safety MUST be re-established at execution and on relevant changes. A corrected registry entry MUST invalidate dependent cached decisions; restart or backup restoration MUST NOT resurrect superseded evidence.

## Retained Human Evidence

Record the decision, the requirement results, the versioned policy and evidence bindings, and the information necessary to explain and review the decision. Protect person-specific evidence separately. Authorization records MUST NOT become career-long behavioral profiles, general resilience credit, employee rankings, or a basis for automatically promoting a person.

Collection, access, disclosure, corrections, and erasure follow KTP-Privacy and specifications/privacy-evidence.md. Metadata and opaque identifiers can still identify people through linkage. Retention is purpose-specific, bounded, and reviewed; no default permanent human trajectory is required.

# Human-Agent Collaboration

## Delegation

A delegation MUST bind the authenticated delegator and executing actor, the source grant, exact operation, resources, parameters, purpose, zone, validity interval, and current revocation state. Its authority is the intersection of current delegator grants and every applicable delegation restriction. Neither a valid delegation nor a human signature expands that intersection.

Each link of a supported delegation chain MUST be independently validated, current, scoped, and revocable. Changing the delegator's relevant grant or qualification invalidates dependent authority. A downstream delegate MUST NOT widen actions, resources, purposes, time bounds, or subdelegation rights. Unsupported chains MUST fail closed.

The software delegate MUST independently satisfy its own grant, standing, readiness, capacity, Soul, and other enforcement checks. Delegation MUST NOT transfer a human's qualification to a bot, mint standing, change lineage, or confer a human principal type.

For example, Alice may authorize a recovery agent to prepare a rollback plan for one database. A grant to prepare that plan does not authorize execution, another database, or another purpose. Even an explicit execution grant cannot overcome the agent's insufficient readiness or current capacity.

## Supervision

Active supervision requires the human's eligible and authorized approval of the exact proposed action before the agent continues through its remaining checks. Passive supervision monitors authorized operations. Exceptional supervision alerts an accountable human on defined events. In every model the agent retains its own restrictions.

Human presence, co-signing, seniority, or reassurance MUST NOT add arbitrary E_base points, move the agent into the human's alleged tier, or relax a capacity veto. If A = 70 and established E = 65, the action is denied even with a supervisor's signature. A revised action or changed environment requires a fresh evaluation of the actual conditions.

Supervision responsibilities MUST identify monitoring scope, response authority, and conflict-of-interest safeguards. A reviewer or supervisor needs relevant competence and authority; a general human trust score is neither necessary nor sufficient.

## Accountability

The retained record SHOULD distinguish the delegation decision, the executing actor, the specific human approval if required, and the deployment's responsibilities. Audit evidence supports investigation; it does not by itself establish legal liability or a person's intent. Access and exports remain subject to the declared purpose and protection of other people.

# Constraints, Emergencies, and Governance

## No Safety Override

An administrator, supervisor, or reviewer MUST NOT waive a valid capacity or Soul veto. Correcting erroneous evidence and challenging the legitimacy of a rule remain available. A corrected fact or properly adopted rule change leads to a fresh evaluation rather than an exception for the original denied request.

Safe responses can include reducing the requested scope, establishing reversibility, restoring capacity, repairing invalid evidence, or using an independently authorized alternative. Each proposed alternative requires its own checks. Dividing an operation into smaller requests MUST NOT evade cumulative resource or effect limits.

## Emergency Procedures

Human emergency actions MUST follow the separately preapproved capability, exact scope, duration, revocation, and protected amendment requirements in specifications/emergency-capability.md and KTP-Emergency. Ordinary proof expiry and all capacity and Soul gates remain in force. An emergency declaration, incident role, or outage MUST NOT itself lower weights, raise standing, relax thresholds, widen authority, or activate a missing emergency capability.

Eligibility to act as an incident commander is specific authority for a declared response scope. It is not a numerical trust boost. Review and assistance routes MUST remain accessible during denial without becoming alternative execution paths for the hazardous operation.

## Policy Changes

The deployment MUST document the legitimate governing authority, review route, approval process, and durable version floor for human eligibility policy. Changes MUST be versioned, approved by that authority, authenticated, audited, and tested against the hard safety constraints before activation. The requester MUST NOT choose the accepted policy version or authorize their own exemption. Relevant changes invalidate dependent decisions.

Any change affecting emergency policy remains subject to its stronger amendment controls. Human eligibility policy MUST NOT be a route around those controls. Challenges to rule legitimacy require an accountable governing process with authority to revise the rule; merely confirming that software executed it correctly is insufficient.

# Explanation, Correction, and Accessibility

## Decision Explanation

For each decision affecting a person, the system MUST provide an accessible explanation of the operation and scope, result, unmet requirements or safety constraint, evidence source and version, responsible authority, and review route. It MUST distinguish ineligibility from a capacity or Soul veto and avoid presenting a personal rank.

Sensitive evidence may require protected access or a suitable representative. A generic security label MUST NOT make the grounds of a decision impossible to challenge. Disclosures MUST protect other subjects and legitimate security interests while enabling meaningful review.

## Meaningful Review

A person MUST be able to challenge a specific fact, identity association, evidence scope or status, application of a requirement, or the legitimacy of the governing rule. Review access MUST NOT depend on the eligibility being challenged. The deployment MUST declare response and escalation deadlines, an accessible assistance route, reviewer competence and authority, and conflict-of-interest safeguards.

The reviewer MUST have power to investigate and correct an individual case, including obtaining correction from the responsible issuer, withdrawing established invalid evidence from decision use, and directing re-evaluation of affected decisions. A case-specific error does not require a global calibration change. Unresolved disputes MUST be identified as such; a disputed hazardous operation remains restricted while the evidence necessary for eligibility is unresolved.

Corrections MUST append an authenticated correction event, mark superseded evidence as unusable for future decisions, update the current evidence state and epoch, invalidate dependent cached decisions, and propagate to affected authorized recipients. The original signed bytes MUST NOT be rewritten. A retained record of the error is not permission to keep treating it as true.

A reviewer MUST NOT manually boost a score, substitute an unexplained approval, or override a valid safety check. Corrected evidence produces a fresh decision under the current approved rules. Challenges to those rules themselves MUST reach the designated governing authority.

## Alice's Correction Scenario

Alice requests a rollback for a named production database. Her login and operation grant are valid, but the qualification registry attached another employee's expired certificate to her identity. The explanation identifies the mismatched qualification and review route.

An authorized reviewer verifies the error, obtains a corrected association from the responsible issuer, and invalidates decisions using the wrong association. Alice's actual current qualification is evaluated against the rollback requirements. She now meets eligibility. If current database recovery capacity is still inadequate, the rollback remains denied. Correction has practical effect without weakening safety.

## Assistance and Remediation

Explain the actual missing requirement and a feasible review, qualification, or safe alternative route. Do not promise that waiting, gaining seniority, or obtaining a supervisor's signature will restore permission. If no safe execution path exists, state that plainly and retain access to assistance and challenge.

Interfaces SHOULD use plain language, accessible text and status indicators, and explanations that do not depend solely on color. Backend evidence refresh SHOULD be automatic within existing freshness limits. Notifications SHOULD identify relevant changes without exposing the person's circumstances to peers.

People MUST be able to request access to, export of, and correction of their own retained decision evidence through protected channels. These rights do not grant unrestricted access to other subjects' records or the entire Flight Recorder. Applicable retention and erasure handling follows specifications/privacy-evidence.md.

# Security Considerations

Stolen credentials can exploit whatever live grants and eligible operations remain available. MFA, session binding, least privilege, current revocation, and separation of duties reduce that risk but do not establish benign intent. The system MUST NOT claim that scoped eligibility eliminates insider threats, coercion, or social engineering.

Authentication anomaly detection MUST be limited to explicitly authorized security evidence and purpose. It MUST NOT become covert internal-state inference or employee performance surveillance. Software agents cannot evade readiness by presenting a human label, and a person cannot evade a revocation by requesting erasure or a new identifier. Where required security state cannot be retained or reconstructed under the applicable rules, old authority MUST remain unusable; any new enrollment requires separate authorization.

# System Ethics (DRAFT)

This section addresses ethical questions about the design of KTP itself. It is marked DRAFT to invite expert review and debate.

These questions are worthy of serious consideration. The authors do not claim definitive answers but offer this framework to structure the discussion.

## The Obsolescence of Agent Ethics

A fundamental claim of KTP is that agent ethics—the question of whether an autonomous agent has good or bad intentions—becomes irrelevant in a structurally constrained model.

### The Traditional Ethics Problem

Traditional approaches to AI safety ask: "How do we ensure AI agents have aligned values, good intentions, and ethical behavior?"

This question assumes that agent intent matters—that an agent with good values will do good things, and an agent with bad values will do bad things.

### The Physics Response

KTP responds: "Agent intent doesn't matter because agents can only do what the environment permits."

A = 80, E_trust = 60 → Action denied, regardless of intent. A = 40, E_trust = 60 → The capacity check passes; all other authorization requirements still apply.

The agent's values, goals, or ethics are irrelevant to the calculation. The environment has veto power over agent intent.

An agent that "wants" to do harm cannot do harm exceeding its Trust Score. An agent that "wants" to help cannot help beyond its Trust Score. The structure constrains all agents equally.

### The Limits of This Claim

This does not mean ethics is irrelevant. It means the LOCUS of ethical consideration shifts:

- FROM: "Is this agent ethical?"
- TO: "Is this system ethical?"

We no longer ask whether individual agents have good values. We ask whether the constraints imposed by the system are just.

This is the question the rest of Section 10 addresses.

## The Silent Veto Problem

"If the Silent Veto prevents an action that would have saved lives, who is responsible?"

This is the central ethical challenge of KTP.

### The Scenario

Consider: A fire breaks out in a building. An automated system could unlock all doors to enable evacuation. But the system's Trust Score has been deflated by the crisis itself (high Heat, high threat indicators). A > E_trust. The action is vetoed. People are harmed.

The system did exactly what it was designed to do. The constraints worked correctly. And yet harm occurred that might have been prevented.

Who is responsible?

### Possible Positions

Position A: The System is Not Responsible

~~~
   The system correctly evaluated that the environment could not
   safely support the action. Unlocking all doors during a crisis
   could also enable attackers, trap people in dangerous areas,
   or cause other harm. The system made a conservative judgment
   appropriate to uncertainty.
~~~

~~~
   Responsibility lies with:
   - Those who caused the fire (proximate cause)
   - Those who designed the building (safety systems)
   - Those who configured the Trust Score (calibration)
   - Not the system that correctly evaluated constraints
~~~

Position B: The System is Partially Responsible

~~~
   The system's designers knew that conservative constraints
   would sometimes prevent beneficial actions. They chose to
   accept this tradeoff. This choice carries moral weight.
~~~

~~~
   Responsibility is shared:
   - System designers (for the tradeoff)
   - System operators (for specific configuration)
   - External actors (for the crisis itself)
~~~

Position C: The System Should Not Make Such Decisions

~~~
   Life-safety actions should be exempt from Trust Score
   constraints. Physics should not override the preservation
   of human life.
~~~

~~~
   This position argues for carving out exceptions for
   specific action categories.
~~~

### The Authors' Tentative View

We lean toward Position B with important caveats:

1. The tradeoff is explicit and intentional - KTP knowingly accepts false positives (blocking beneficial actions) to prevent false negatives (allowing harmful actions) - This is a design choice with moral weight - Designers bear responsibility for this choice

1. The calibration matters enormously - A system that vetoes life-safety actions frequently is miscalibrated - Proper configuration should make such scenarios rare - Operators who miscalibrate bear responsibility

1. Position C is a slippery slope - Every exemption creates an attack vector - "Life safety" can be claimed for almost anything - Exemptions undermine the constraint model entirely - We reject categorical exemptions while acknowledging the moral cost

1. The alternative is worse - A system that can be overridden "for good reasons" will be overridden for bad reasons - The harm from a exploitable system exceeds the harm from occasional false positives - This is a tragic tradeoff, not a happy solution

## Responsibility Attribution

When harm occurs in a KTP-governed system, how is responsibility attributed?

### The Causal Chain

For any incident, multiple parties may bear responsibility:

1. Proximate cause: Who or what directly caused the harm?
2. Environmental cause: What conditions enabled the harm?
3. Configuration cause: Was the system properly calibrated?
4. Design cause: Does the system design create this risk?
5. Deployment cause: Was this the right system for this context?

### The Flight Recorder's Role

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

### Attribution Framework

We propose the following framework:

If the system ALLOWED an action that caused harm:

- Was action risk correctly classified? (If no: calibration error)
- Was Trust Score correctly calculated? (If no: technical error)
- Were sensors functioning? (If no: operational error)
- If all correct: The system permitted an action within constraints that still caused harm. This is residual risk accepted by the design.

If the system DENIED an action that would have prevented harm:

- Was denial correct per Zeroth Law? (If yes: design tradeoff)
- Was action risk over-classified? (If yes: calibration error)
- Was Trust Score incorrectly deflated? (If yes: technical error)
- Was environment incorrectly assessed? (If yes: sensor error)

## Force Majeure vs. Negligence

A critical distinction in responsibility attribution.

### Force Majeure (Environmental Force)

The system correctly evaluated conditions and appropriately constrained actions. Harm resulted from external factors beyond the system's control.

Characteristics:

- System behaved as designed
- Configuration was appropriate
- Sensors were accurate
- Environmental conditions genuinely degraded
- Harm was not reasonably preventable by system

Responsibility: External factors, not system or operators

### Negligence (Human Failure)

The system was misconfigured, poorly maintained, or inappropriately deployed. Harm resulted from human failure to properly operate the system.

Characteristics:

- Miscalibration of risk or trust
- Ignored sensor failures
- Inappropriate system for context
- Known issues unaddressed
- Harm was preventable with proper operation

Responsibility: Operators and/or designers

### The Boundary

The boundary between force majeure and negligence is often contested. KTP's Flight Recorder provides evidence, but interpretation requires judgment.

Key questions:

- Was this configuration reasonable at deployment time?
- Were warning signs ignored?
- Is this a known limitation that was accepted?
- Would a reasonable operator have done differently?

## The Justice of Constraints

Are KTP's constraints just? This is perhaps the deepest question.

### Constraints as Enablement

The Constitution frames constraints positively:

~~~
   "Freedom without constraint is not freedom but randomness.
    An agent is not free because it can do anything, but because
    it acts within the bounds of what the environment can safely
    support."
~~~

For software agents, admissible historical evidence may contribute to standing, subject to current readiness and all other checks. For people, operation-specific eligibility replaces accumulated trust points; protection and access to review do not depend on earning permission.

### Constraints as Limitation

Critics might argue:

- Constraints limit beneficial actions
- Trust Scores may reflect bias or history unfairly
- The constraint model is still human-designed and value-laden
- Those who configure constraints hold power over others

These concerns deserve serious consideration.

### Addressing the Concerns

On limiting beneficial actions: Yes, this is the acknowledged tradeoff. The question is whether the alternative (unlimited action, unlimited risk) is better. We argue it is not.

On bias: Software-agent standing and human qualification requirements each require scrutiny. Calling evidence behavioral does not make it unbiased. Human requirements need a defensible connection to the operation, permitted evidence, and meaningful correction; they MUST NOT become general behavioral scores.

On human design of the constraints: Yes, this constraint model is designed, not discovered. The values embedded in the design should be explicit, debatable, and adjustable through governance. The Constitution provides amendment procedures.

On power of configurators: The Governance Recursion (Article VII) addresses this: configurators are agents within the system. They cannot exempt themselves. Their configuration actions are logged. They are accountable.

### The Consent Foundation

Ultimately, KTP's legitimacy rests on consent:

- Establish whether participation is voluntary in the actual context
- Establish whether exit is meaningful and what alternatives exist
- Make the governing rules and responsible authority accessible
- Provide a legitimate process to challenge and amend those rules

Consent and meaningful exit are relevant legitimacy conditions, not a sufficient proof of justice. Deployments MUST declare the actual governing authority and contest process; employment, public services, and collective data interests MUST NOT be treated as freely optional merely because a zone is described as opt-in.

## Open Questions

We do not claim to have resolved these questions. We offer them for ongoing discussion:

10.6.1. Is there any action that should never be vetoed?

~~~
   If so, how do we define it without creating an exploitable
   exemption? If not, how do we accept the moral weight of
   vetoing genuinely beneficial actions?
~~~

10.6.2. How do we handle genuine uncertainty about consequences?

~~~
   The Silent Veto prevents actions whose risk exceeds trust.
   But risk estimation is uncertain. How confident must we be
   in our risk assessment to impose constraints?
~~~

10.6.3. Who has standing to contest system design?

~~~
   If someone is harmed by a correct system operation (Position B
   above), can they seek remedy? From whom? Through what process?
~~~

10.6.4. How do we prevent constraint creep?

~~~
   As systems operate, there may be pressure to increase
   constraints (more conservative, more vetoes). How do we
   maintain appropriate balance?
~~~

10.6.5. What is the right level of transparency?

~~~
   Full transparency enables gaming. Insufficient transparency
   prevents accountability. Where is the balance?
~~~

10.6.6. Can structural constraints be truly neutral?

~~~
   Or do they inevitably embed the values of their designers?
   If the latter, how do we govern those values democratically?
~~~

These questions deserve expert attention from ethicists, lawyers, policymakers, and affected communities. This specification is technical; the ethics are for society to resolve.
