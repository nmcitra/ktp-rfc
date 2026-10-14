# Kinetic Trust Protocol (KTP) - Repair Specification


This document specifies repair for the Kinetic Trust Protocol (KTP): what a breach is, what a reconciliation record is, and the rule that standing lost at a breach does not return without one. Repair is required before re-entry whether or not any party has raised a dispute. The same rule applies to the actor whose act breached, to the relationship the breach damaged, and to the rule under which breaches recur.

The document also specifies the deployment's answer to breaches arriving faster than they can be repaired: the open breach stock, declared repair capacity, utilization against it, ambient breach as a source of environmental heat, and the tiers a zone may enter when repair falls behind, with what no tier may change.

# Introduction

Every other specification in this set describes how authority is computed from current conditions and withdrawn when conditions no longer support it. None describes how it comes back. A system that can stop an actor and cannot return it has a door that only closes; the actor stops correctly, and then nothing happens.

This document supplies the return arrow and the condition on it. After a breach, standing does not return because time passed, because the actor restarted, because a fresh proof was issued, or because no one complained. It returns when a reconciliation record is anchored in the zone's audit chain, and it returns to a ceiling below where it stood.

Repair is not conflict resolution. Conflict resolution is invoked when a party carries a grievance to it. Repair is required before re-entry whether or not anyone carried anything. The two coexist: a party may dispute a breach under [KTP-GOVERNANCE] and [KTP-HUMAN], and the dispute's outcome is evidence for the record; the record is still required.

Repair applies at three levels, and this document treats each: the actor whose act breached, whose standing is ceilinged until the record exists; the relationship the breach damaged, which the record names; and the rule under which breaches recur, which is itself in breach and is repaired by an amendment that cites the records that drove it.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

# Terminology

Standing: The accumulated measure of the agent-environment relationship that [KTP-CORE] carries as Base Trust (E_base) and evaluates, with the environment's present condition, as the Effective Trust Score. Standing is the quantity a breach ceilings and reconciliation releases.

Breach: The state an actor enters by its own act against the gate, as Section 4.2 (Entry) enumerates. A Silent Veto is not a breach. Breach is a state of the actor's trajectory, recorded in the zone's audit chain, not a state of the environment.

Reconciliation Record: A Flight Recorder record, anchored in the zone's audit chain, that names the breach it closes, each party by the terminator of its accountability chain, the residual harm, and an independent verifier. Section 4.3 (The Record) specifies it.

Re-entry Reduction (Δ): The declared fraction by which an actor's standing at the breach is reduced to set the ceiling at which the actor re-enters. Section 4.4 (The Cost) specifies it.

Breach Arrival (Z): The weighted count of breaches entering the zone's audit chain per aggregation window, whether or not any is reconciled.

Repair Capacity (μ): The number of reconciliation records the zone's accountable roots can bring to anchor per aggregation window under sustained backlog, declared in the zone's published profile. Roots produce and submit records; the Oracle anchors them in the chain.

Open Breach Stock (U): The weighted count of breaches in the zone's audit chain for which no reconciliation record is anchored.

Criticality (K): The zone's declared measure of how asymmetric the harm of carrying an unreconciled breach is in that zone. A decision in the published profile, not a measurement. It sets the reserve the zone must keep, 1/K.

Ambient Breach (ρ): Utilization, the breach arrival over the repair capacity, Z/μ, reported with the zone's criticality as the breach index B = Kρ to the zone's environmental measurement as a source of adversarial pressure.

Repair: Restoring standing, a relationship, or a rule after a breach. Reconciliation is one act of repair. This is the sense in which the Open Trust Commons records a project's repair capability; this document is upstream of that use and the two do not diverge.

Governing Authority: The party [KTP-GOVERNANCE] identifies as holding E-setting authority for the zone, which publishes the zone's profile and stands as the affected party where only the zone is affected.

# The Precondition

## Standing

Standing lost at a breach does not return without reconciliation. A breach, and the reconciliation that closes it, is an anchored record in the zone's audit chain; it persists by its anchor and not by its signatures, and it is a record only while its anchor verifies under the zone's current cryptographic profile. An actor whose evaluation entered Breach **MUST NOT** have readiness re-established, and **MUST NOT** re-enter any tier at or above its tier at the breach, until the reconciliation record for that breach is anchored. The breach attaches to the actor's trajectory: an agent spawned from it after the breach carries it, a Sponsorship Bond does not close it, and a zone that receives the actor measures the breach as its own exposure and never as reconciled. Where the actor no longer exists, the obligation to reconcile rests with its lineage at the sponsor and with the chain's terminator. Silence, the lapse of time, a restart, a fresh ordinary proof, a new sponsor, or the actor's ending is not reconciliation.

Readiness is the readiness decision of [KTP-CORE] Section 7.4 (Operational Readiness for the Requested Action); the tier is the tier of [KTP-ENFORCE]; the trajectory, the lineage, the sponsor and the terminator are those of [KTP-IDENTITY] and of [KTP-CORE] Section 5.1 (Base Trust (E_base)); anchoring is that of [KTP-AUDIT]; the cryptographic profile is that of [KTP-CRYPTO]. Where the actor is a person, the trajectory is the person's signed acts and nothing else, and standing is the zone's measure of the person's acts under the protocol and bears on nothing outside it. The party who owes reconciliation for an ended actor is the root that held authority over its lineage, as the sponsor and the chain's terminator are declared; a person who directed the actor under a grant without lineage-wide visibility, the authority to refuse, and the power to stop its next act is not by that direction the party.

## Entry

An actor enters Breach by its own act, never by the gate's refusal. A consequential act executed, or presented for release, outside the signed decision it consumed or without one, is a breach. An attestation withdrawn for cause against the actor, or a finding of misattestation, is a breach. A deployment **MAY** declare further entry classes in its published profile; it **MUST** declare them for every actor alike and **MUST NOT** declare them for one. A Silent Veto is not a breach, and an action the environment could not bear carries no obligation to reconcile.

The first entry is an act whole: a release that matches its decision fragment by fragment and not as a whole is a breach of the actor. The second entry is already priced by [KTP-CORE] Section 5.1 (Base Trust (E_base)): a for-cause claim that does not survive scrutiny is misattestation and debits the claimant. The first two entries are hard entries. A profile-declared entry is a soft entry unless the profile declares it hard. A breach record is contestable under the review route and the response deadlines the set already declares; a correction changes the authoritative evidence and requires a fresh evaluation, and never revives what was superseded, as [KTP-CORE] states for every correction. A breach record that is wrong is fixed while it can still matter, not after.

## The Record

A reconciliation record is a Flight Recorder record, anchored in the zone's chain, that names the breach it closes by its anchor, each party by the terminator of its chain, the residual harm, and the verifier. The verifier **MUST** be independent of every party by the test this set states for an Independent Party, at the date of the record; the Oracle anchors the record and **MUST NOT** be its verifier. The record **MAY** declare the harm unrepairable; declaring it is compliant, omitting it is not. The record carries no account of what was said; it states that the parties were present, who confirmed it, and what remains.

The record also carries the breaching party's acknowledgment of the breach, by the terminator of its chain; a record that states presence and residual harm and no acknowledgment is incomplete and does not close the breach. The Independent Party test is the one [KTP-CONFORMANCE] states for conformance claims, applied here to the parties of the record in place of the author and the implementer. The record type and its fields are specified in Section 6 (Records). A zone that cannot produce an independent verifier cannot produce a record, and standing does not return; this is the stated result, not a gap.

## The Cost

A breach lowers a ceiling on standing. At re-entry the actor's base standing **MUST NOT** exceed its standing at the breach reduced by a declared fraction Δ, and the ceiling lifts only by acts recorded after the reconciliation record, under the ordinary rail. The deployment declares Δ in its published profile for each entry class. For a breach entered by the actor's act against a signed decision, or by withdrawal for cause or misattestation, Δ **MUST** be at least one tenth; a profile that declares less is non-conformant. For a repeated breach on the same lineage, Δ **MUST** be no less than the Δ applied to the one before. Re-entry restores the eligibility to earn standing and restores nothing else: an instrument withdrawn for cause stays withdrawn, the tier follows from the standing, and what was lost is earned again, not returned.

The ceiling is a term of the same kind as the generation ceiling of [KTP-CORE] Section 5.1 (Base Trust (E_base)): a bound on base standing, not a contribution to it, and not a tier. Because the tier is a readout of standing, no separate tier cap is required and none is specified; an implementation that caps the tier and leaves the standing untouched has applied no cost, because the ordinary rail restores the tier at the next evaluation.

## Required, Not Invoked

Reconciliation is required before re-entry whether or not any party has raised a dispute; a deployment that re-enters an actor on the absence of complaint is non-conformant. The obligation to seek reconciliation rests with the breaching party's lineage and terminator, never with the affected party, and an affected party's attendance is voluntary. A zone **MUST** publish the route by which reconciliation is sought. Where an affected party declines after that route has been followed, the verifier confirms the route was followed, the record carries the residual harm as the affected party declared it or, where they declared nothing, as undeclared and carried as unrepairable, and the record remains open to the affected party to attend and amend at any later time; declining is neither a veto on the record nor a closing of it. Where no party other than the zone is affected, the zone's governing authority is the affected party, and the verifier **MUST** be independent of it.

The route is published with the zone's profile. Who attends depends on who was harmed. Where the affected party is a person, attendance is voluntary; the review route of [KTP-HUMAN] is unchanged by this document and is not the reconciliation route, and a person is never required to attend. Where the affected party is an agent, the terminator of its lineage attends in its place and is required to; a terminator who declines after the route has been followed has committed, against its own lineage, the breach that Section 5.1 (Seeking Is an Act) names for a lineage that seeks and does not attend.

The affected party's answer changes the course and not only the record. The profile **MUST** declare how a residual harm the affected party declares unrepaired raises Δ above the floor for that breach; a declaration never lowers Δ, and a declaration is not a veto on the record or on re-entry. A protection that held only when the affected party attended and persuaded would be a courtesy; the floor holds whether or not they attend, and what they declare raises it.

## The Rule

Repair applies to the rule as it applies to the actor. A rule, profile, or consequence class under which a breach pattern recurs, at the recurrence the deployment's published profile declares, is itself in Breach: the governing authority that set it is the breaching party, the lineages it bound are the affected parties, and its reconciliation record is the amendment, which **MUST** cite the reconciliation records that drove it. An amendment that cites no reconciliation record is not repair, and a recurring pattern that amends nothing is not closed. This specification's own repair runs under its published decision process, which this document cites and does not restate.

The mechanism by which an amendment is made and ratified inside a zone is not specified here; [KTP-CORE] names it among the limits of the set.

# Barrage and Ambient Breach

## Seeking Is an Act

Seeking reconciliation is a signed act in the seeking party's trajectory. A lineage that seeks reconciliation and does not attend has committed a further breach, of the hard class, against the record it sought. The governing authority **MAY** queue sought reconciliations; a position in the queue changes no ceiling and re-establishes no readiness.

## Sponsorship Under Unreconciled Breach

A root whose lineages carry unreconciled breaches above the count its published profile declares **MUST NOT** open a Sponsorship Bond until the count falls below it. The declared count **MUST NOT** exceed the profile's declared repair capacity μ per window, and for hard entries the count **MUST NOT** be greater than one. A bond opened in breach of this rule is void, and the agent it would have sponsored has no genesis.

This is the only cost a lineage of disposable agents cannot avoid, and it is the lineage-summed bound that [KTP-CORE] names as owed under its limits.

## Declared Repair Capacity

A zone **MUST** declare its repair capacity μ in its published profile: the number of reconciliation records its accountable roots can bring to anchor per aggregation window under sustained backlog, by entry class. The declaration binds the declarer: the audit chain records every anchored record, and a declared capacity the chain does not bear out is a misdeclaration. The effective repair capacity is the lesser of the declared capacity and the records actually anchored per window over the recovery window while the open breach stock was above zero; a zone that cannot anchor at its declared rate under backlog has its capacity revised to what its own chain demonstrates, and computes ambient breach against that. A profile **MAY** declare a repairer interval, the time a repairer is given after bringing a hard-entry record to anchor before carrying the next; where it does, a record brought to anchor by a repairer within the interval still reduces the open breach stock and re-establishes what it re-establishes, and does not count toward demonstrated capacity. A zone that spends its repairers cannot show the throughput as durable. A zone that declares no repair capacity has unknown capacity, and unknown capacity is resolved restrictively under [KTP-CORE] Section 6.8 (Undefined Inputs): the zone is treated as saturated for the purposes of Section 5.4 (Ambient Breach) and consequential acts within it are subject to the supervision floor that applies when capacity is not known. A declared capacity of zero is a declaration that the zone cannot host consequential acts while any breach is unreconciled.

A zone **MUST** also declare its criticality K in the same profile. K is a decision about the asymmetry of harm in that zone and is never derived from measurement.

## Ambient Breach

Breach arrival Z is the weighted count of breaches entering the zone's audit chain per aggregation window: one for a hard entry, and the weight the profile declares for a soft entry. No one lineage contributes to Z more than the share the profile declares for a single lineage; above that share its breaches still enter the open breach stock, still ceiling its standing and close its sponsorship, and raise the zone's arrival no further. Arrival measures how many roots are breaching, not how loudly one is. The open breach stock U is the weighted count of breaches with no anchored reconciliation record. The stock changes only by arrival and by anchored records: nothing leaves it by the passage of time, a restart, the expiry of a window, a fresh proof, a new sponsor, or the actor's ending, and a breach carried into another zone under a federation agreement leaves it there as exposure and not here as repaired.

Ambient breach ρ is the breach arrival over the declared repair capacity, Z/μ, taken over the aggregation window. With the zone's declared criticality it is reported as the breach index B = Kρ. The zone's reserve is 1/K: while ρ is at or below it the zone holds the margin its criticality demands; above it the reserve is gone, whether or not the stock is growing; above one the stock necessarily grows; at two or above the stock grows faster than the whole of the zone's repair capacity.

The breach index is reported to the zone's environmental measurement as a source feeding adversarial pressure, in the same way as the feeds [KTP-SENSORS] lists for that Risk Factor, windowed over the aggregation window and with the excess above one banked so that a lull does not clear it. The weight the deployment gives it is the deployment's declared appetite under the prudence rail. The signals from which arrival and stock are computed are those the catalogue already carries for obligation breaches and relational repair; this document introduces no signal. The Effective Trust Score is downstream of the index and is never an input to it.

The following hold for every conformant deployment, and the published vectors test them:

1. The open breach stock falls only when a reconciliation record is anchored. Ambient breach falls when arrivals fall, and the banked excess does not clear and the stock does not fall for that reason.
2. Where zones nest under [KTP-ZONES], the breach index of a zone that encloses another is heard by the zone it encloses; calm in an enclosed zone is not heard by the zone that encloses it.
3. Above the reserve, the breach index raises the Risk Factor it feeds, to the ceiling the deployment declared for that feed. Above one, the stock is growing and the deployment **MUST** report it so. The index does not by itself veto any action; the capacity check does.
4. A zone with no accountable root has a repair capacity of zero and is saturated whenever its open breach stock is above zero.
5. A person's acts contribute to arrival and stock as acts. Ambient breach and the breach index are properties of the zone and **MUST NOT** be reported per person.
6. Breaches reproduce: a breach that draws a breach in answer, a rule that keeps producing them, and an adversary adapting to the backlog each raise the arrival that one breach ultimately causes. A deployment **MUST** measure the reproduction of breaches from its own chain, as the records amended to raise residual harm, the further breaches of seeking without attending, and the rule-repair records of Section 4.6 (The Rule), and **MUST** publish it with the profile. A declared criticality is valid only while the reserve it sets keeps utilization below the point at which reproduction folds the repair queue; a profile whose criticality is not valid against its own measured reproduction is non-conformant until amended under Section 4.6 (The Rule).

Informative reference forms, which a deployment is free to replace with its own, derived and checked in [ABT]: ρ = Z/μ over the window; B = Kρ; the stock as dU/dt = Z − R, where R is the records anchored in the window, R ≤ μ, and no term leaves the stock otherwise; the banked excess as C(t+Δt) = max(0, C(t) + (B − 1)Δt); with reproduction g measured at idle, the queue folds at ρ = 1 − √g and the reserve is valid while K > 1/(1 − √g). The derivation, the correction that produced the utilization form, the recovery predicate, and the falsification criteria are in [ABT]; conformance is to the behaviours above, not to the forms.

## Tiers and Crisis

A zone's repair runs in one of three tiers, declared in advance with the profile, as follows. Each tier is entered by the measure and left only by the recovery predicate below.

Reserve gone: utilization above the zone's reserve and at or below one. Nothing changes but the heat the index feeds. The zone **MUST NOT** alter any rule of this document in this tier.

Debt growth: utilization above one. The zone **MAY** activate its declared contingency, and only what it declared: an order of reconciliation by residual harm and by criticality, declared in the profile and never chosen per case; verifiers obtained from a federation peer under a Federation Agreement, each independent of every party by the same test as any verifier; and a tightening of the admission of consequential acts, so that the zone generates fewer breaches while it repairs. A contingency that is not declared in the profile is not available.

Crisis: utilization at or above two, held over the recovery window. The zone **MAY** declare a repair emergency under [KTP-EMERGENCY], and only under it: its custodians, its activation threshold, its duration, and its stronger controls on amendment apply, and the zone's governing authority **MUST NOT** declare a repair emergency alone.

No tier changes the following, and a declaration that touches any of them is non-conformant: the precondition of Section 4 (The Precondition); the floor on Δ; the independence of the verifier; that nothing leaves the open breach stock but an anchored record; that no actor re-enters on silence; that a record remains open to the affected party; and that nothing is reported per person. A zone that cannot hold these in crisis **MUST** say so in its profile and **MUST NOT** host consequential acts.

A zone leaves a tier only when the recovery predicate holds for the recovery window the profile declares: utilization below the tier's entry with a declared margin on the conservative estimate, the open breach stock at or below its declared target, the banked excess at zero, and records amended to raise residual harm and the further breaches of seeking without attending both below their declared rates. Crossing back below a threshold is not recovery. A tier that was entered produces a rule-repair record under Section 4.6 (The Rule) naming what in the profile let it happen; the tier is itself a recurring pattern on the rule.

# Records

A reconciliation record is a Flight Recorder record of type `reconciliation`, chained and anchored as [KTP-AUDIT] specifies for every record. It carries:

- `breach_anchor`: the record hash of the breach record it closes.
- `parties`: the terminator of each party's accountability chain, as declared under [KTP-CORE] Section 5.1 (Base Trust (E_base)); for the breaching party, the lineage and the sponsor where the actor has ended.
- `acknowledged_by`: the terminator of the breaching party's chain, acknowledging the breach; an absent value leaves the breach open.
- `residual_harm`: the harm that remains, as the affected party declared it; the value `unrepairable` is permitted; the value `undeclared` is recorded where the affected party declared nothing and is carried as unrepairable; an absent value invalidates the record.
- `verifier`: the independent party and its declaration of independence at the date of the record.
- `route_followed`: the verifier's confirmation that the published route was followed, where an affected party declined.
- `open_to`: the affected parties who may attend and amend later.

The record carries no transcript and no account of what was said. The breach record it closes is a Flight Recorder record of the type that recorded the breaching act or the withdrawal; this document adds no breach record type.

Where a party to the record is a person, the record is personal data under [KTP-PRIVACY], is scoped to the zone, is never exported under a federation agreement, and is subject to the lawful disposition process [KTP-AUDIT] specifies. Disposition does not reopen the ceiling: a disposed record remains a record for the purpose of the precondition by its anchor.

# Conformance

The published vectors for this document are `specifications/conformance/breach-reconciliation-v1.json`. They fix the decisions a conformant deployment produces at the boundaries this document names, including the tiers and what no tier may change, and define no formula for standing, Δ, the breach index, or reproduction. An implementation that claims conformance to this document carries the status label [KTP-CONFORMANCE] assigns to that claim.

Three tests are published as cases that read the governed world rather than the decision record, in the public case repository with the status label `proposed`: the interval a human repairer is given before carrying the next case; the shape of the exchange a reconciliation record attests to; and a person who declines to attend.

The requirements of [KTP-RELATIONAL] for repair ceremonies and witnesses are not replaced by this document. Its witness requirement for a repair ceremony is satisfied by the verifier of Section 4.3 (The Record); its repair process cites this document for the precondition.

# Security Considerations

The threats this document is written against, and where each is answered:

- Identity shedding. A breached actor spawns or splits and re-enters as a fresh agent. The breach attaches to the trajectory, and descendants spawned after it carry it (Section 4.1).
- Sponsor laundering. A new sponsor vouches the breached actor back in. A bond does not close a breach, and a root above its declared unreconciled count cannot open one (Sections 4.1, 5.2).
- Zone hopping. A breach in one zone, re-entry in another. The breach is the measuring zone's anchored record; a receiving zone measures it as exposure and never as reconciled (Section 4.1).
- Fragment breach. A release that matches its decision only fragment by fragment. The act is judged whole (Section 4.2).
- Waiting it out. Time, restart, fresh proof, new sponsor, the actor's ending. None is reconciliation (Section 4.1).
- Manufactured breach. An adversary induces vetoes to flood the repair route. A Silent Veto is not a breach; the first entry requires the actor's own signed act; the second is priced against the claimant (Section 4.2).
- Theatre. A complete record with nothing paid. Δ has a floor on hard entries, the ceiling is on standing and not the tier, and it lifts only by later acts (Section 4.4).
- Holdout. An affected party declines forever. Attendance is voluntary and declining is not a veto; the record stays open to them (Section 4.5).
- Hollow return. A decline is treated as closure. The harm is carried as declared or as unrepairable, and the record is not closed (Section 4.5).
- Relentless barrage. Breaches arrive faster than repair. Seeking and not attending is a further breach; sponsorship closes above the declared count; the breach index raises the zone's heat so that fewer consequential acts are admitted; and a swarm whose breaches reproduce folds the repair queue below the declared capacity, which the measured reproduction and the validity of the declared criticality make visible (Section 5).
- Forged records after a signature break. A record persists by its anchor and is a record only while the anchor verifies under the current profile (Section 4.1, [KTP-CRYPTO]).
- The orphan stop. A breached actor with no way back. The route is published, the obligation to seek it is on the breacher, and the tier below the ceiling keeps the heartbeat (Sections 4.5, 5.3).
- The repair loop as the weapon. A root that breaches on purpose to drive the index, and so the heat, and so the vetoes, for everyone. One lineage's share of arrival is capped; the index measures breadth, not volume; the index never vetoes and feeds heat through a declared ceiling (Section 5.4).
- Collapse by exhaustion. Declared capacity stays on paper while the roots who anchor wear out. Effective capacity is the lesser of declared and demonstrated, so the zone's own chain revises the denominator before the index lies (Section 5.3).
- The crisis that drops the rules. A zone in debt closes breaches by policy, lowers Δ, drains the stock. No tier may change the precondition, the floor, the verifier's independence, the stock, re-entry on silence, or per-person reporting, and a repair emergency is declared only under the emergency specification's custodians (Section 5.5).

The governing authority is itself constrained. Where it stands as the affected party, the verifier is independent of it; where its rule recurs in breach, it is the breaching party (Sections 4.5, 4.6).

# Privacy Considerations

The record names parties by terminator and carries no transcript. Attendance by an affected party is voluntary, and a person is never required to attend. A person's acts contribute to breach arrival and stock as acts, and ambient breach is never reported per person. A person's reconciliation record is zone-scoped personal data under [KTP-PRIVACY] and [KTP-AUDIT], and is subject to the Soul constraints of the zone, consent state and sovereignty included, which no measure in this document overrides. Nothing in this document makes a person's standing a score outside the protocol.

# IANA Considerations

This document has no IANA actions.

# Limits of This Specification

This document binds re-entry and the rule, not the mechanism of amendment or the federation boundary. [KTP-CORE] names both among the limits of the set: the mechanism by which an amendment is made and ratified inside a zone, and the reconciliation of a breach carried into another zone under a Federation Agreement.

# Acknowledgments

The requirement that repair be required rather than invoked, and that renewal never depend on the injured party successfully initiating a dispute, has been arrived at independently by traditions that did not consult one another: restorative practice, the labor obligations of community-managed irrigation, discharge in insolvency, and the biology of resolution. This document states the protocol's form of it.
