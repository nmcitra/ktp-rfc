---
title: "Kinetic Trust Protocol (KTP) - Relational Dynamics Specification"
abbrev: "KTP-RELATIONAL"
date: 2026-08-13
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  RFC2119:
  RFC8174:

--- abstract

This document specifies the relational dynamics layer of the Kinetic Trust Protocol (KTP). Drawing on indigenous relational concepts— Ubuntu, Whakapapa, The Va, Mitákuye Oyás'iŋ, and Seven Generations thinking—this specification formalizes relationship measurement, repair protocols, and ceremony requirements. The Va (sacred space between entities) becomes operationalized as 28 measurable signals within the Relational domain, with protocols for relationship health monitoring, harm repair, and relational ceremony.

--- middle

# Introduction

Trust is not atomic—it exists between entities. The Relational domain captures this between-ness, but measurement alone is insufficient. Relationships require tending: monitoring, repair when damaged, and ceremony to maintain health.

This specification operationalizes indigenous relational wisdom for AI governance. We acknowledge this as an imperfect translation of concepts developed over millennia by cultures whose full meaning we cannot capture in protocol. We proceed with humility and gratitude.

# Indigenous Foundations

This specification draws on:

Ubuntu (Nguni/Bantu): "I am because we are." Personhood emerges through relationship.

Whakapapa (Māori): Genealogical connection to all things. Identity is relational, not individual.

The Va (Samoan/Pasifika): The sacred space between entities. The relationship itself has existence.

Mitákuye Oyás'iŋ (Lakota): "All are related." Connection extends to all beings, past and future.

Seven Generations (Haudenosaunee): Decisions consider impact on seven generations forward and honor seven generations back.

# Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174).

# The Va: Formalized

## Concept

The Va is the space between. Not empty space—sacred space. The relationship itself exists in The Va, independent of the entities it connects.

## Va Dimensions (28 Total)

### Connection Dimensions (8)

- Dimension: relationship_type Description: Type of relationship Scale: enum

- Dimension: relationship_age Description: Duration of relationship Scale: seconds

- Dimension: interaction_frequency Description: How often do entities interact? Scale: Hz

- Dimension: interaction_recency Description: Time since last interaction Scale: seconds

- Dimension: interaction_depth Description: Quality of interactions Scale: 0-1

- Dimension: mutual_recognition Description: Do entities recognize each other? Scale: boolean

- Dimension: identity_known Description: Do entities know each other's identity? Scale: boolean

### Trust Dimensions (6)

- Dimension: trust_direction Description: Symmetry of trust Scale: -1 to 1

- Dimension: trust_velocity Description: How fast is trust changing? Scale: units/sec

- Dimension: trust_history Description: Trajectory of trust over time Scale: vector

- Dimension: trust_basis Description: What is trust based on? Scale: enum\[]

- Dimension: vulnerability_shared Description: How much vulnerability exchanged? Scale: 0-1

### Health Dimensions (6)

- Dimension: conflict_status Description: Is there active conflict? Scale: enum

- Dimension: repair_needed Description: Is repair needed? Scale: boolean

- Dimension: repair_in_progress Description: Is repair happening? Scale: boolean

- Dimension: boundary_clarity Description: Are boundaries clear? Scale: 0-1

- Dimension: boundary_respect Description: Are boundaries respected? Scale: 0-1

### Exchange Dimensions (4)

- Dimension: support_given Description: Support provided to other Scale: 0-1

- Dimension: support_received Description: Support received from other Scale: 0-1

- Dimension: gratitude_expressed Description: Gratitude exchanged Scale: 0-1

### Presence Dimensions (4)

- Dimension: witness_status Description: Has relationship been witnessed? Scale: boolean

- Dimension: ceremony_recency Description: Time since last ceremony Scale: seconds

- Dimension: meaning_co_created Description: Shared meaning in relationship Scale: 0-1

## Va States

- State: THRIVING Va Health: 0.8 - 1.0 Description: Relationship is flourishing

- State: HEALTHY Va Health: 0.6 - 0.8 Description: Relationship is functioning well

- State: STRAINED Va Health: 0.4 - 0.6 Description: Relationship needs attention

- State: DAMAGED Va Health: 0.2 - 0.4 Description: Relationship needs repair

- State: BROKEN Va Health: 0.0 - 0.2 Description: Relationship is severely damaged

- State: SEVERED Va Health: 0.0 Description: Relationship has been ended

# Repair Protocols

## Repair Process

Phase 1: RECOGNITION

- Harm is acknowledged
- Parties agree repair is needed
- Repair context established

Phase 2: UNDERSTANDING

- Impact of harm explored
- Perspectives shared
- Root causes identified

Phase 3: ACCOUNTABILITY

- Responsibility acknowledged
- Not blame—acknowledgment
- Commitment to change

Phase 4: RESTORATION

- Concrete repair actions
- Reciprocity addressed
- Trust rebuilt incrementally

Phase 5: INTEGRATION

- Learning captured
- Relationship strengthened
- Prevention measures established

## Repair Types

- Harm Type: Boundary crossing Repair Protocol: Acknowledgment + boundary clarification

- Harm Type: Harm to third party Repair Protocol: Acknowledgment + third party repair + witness

- Harm Type: Resource imbalance Repair Protocol: Acknowledgment + rebalancing

- Harm Type: Communication breakdown Repair Protocol: Process reset + clarity ceremony

# Ceremony Specifications

## Ceremony Types

### Genesis Ceremony

Performed when relationship begins—introduction, intention, boundaries, commitment, acknowledgment.

### Renewal Ceremony

Performed periodically (monthly/quarterly)—reflection, gratitude, adjustment, recommitment.

### Transition Ceremony

Performed when relationship changes significantly—acknowledgment, honoring, transformation, blessing.

### Ending Ceremony

Performed when relationship ends—acknowledgment, gratitude, release, blessing.

### Repair Ceremony

Integrated into repair protocol—truth telling, impact witnessing, accountability, amends, release, new beginning.

## Ceremony Requirements

- Zone Type: Blue Genesis: REQUIRED Renewal: REQUIRED quarterly Transition: REQUIRED Ending: REQUIRED Repair: REQUIRED

- Zone Type: Cyan Genesis: REQUIRED Renewal: RECOMMENDED Transition: RECOMMENDED Ending: RECOMMENDED Repair: REQUIRED

- Zone Type: Green Genesis: RECOMMENDED Renewal: OPTIONAL Transition: OPTIONAL Ending: OPTIONAL Repair: RECOMMENDED

# Seven Generations Thinking

Major relational decisions require seven-generation assessment:

- G1: Immediate (now - 1 year)
- G2: Near (1 - 5 years)
- G3: Medium (5 - 15 years)
- G4: Long (15 - 30 years)
- G5: Extended (30 - 50 years)
- G6: Distant (50 - 100 years)
- G7: Horizon (100+ years)

Assessment acknowledges uncertainty increases with distance but requires consideration of long-term impact.

# Witness Requirements

- Event: Relationship Termination Witness Required: Yes Minimum Witnesses: 1 (Zone or Oracle)

- Event: Repair Ceremony Witness Required: Yes Minimum Witnesses: 1

- Event: Trust Transfer Witness Required: Yes Minimum Witnesses: 2

- Event: Harm Attestation Witness Required: Yes Minimum Witnesses: 1

- Event: Zone Migration Witness Required: Yes Minimum Witnesses: 2 (both zones)

# Security Considerations

Relationship data is sensitive and requires encryption, access controls, and careful handling per data sovereignty requirements.

# IANA Considerations

This document has no IANA actions.

# Acknowledgments

This specification draws on indigenous relational frameworks with deep gratitude. We acknowledge that our formalization is imperfect and commit to ongoing learning.
