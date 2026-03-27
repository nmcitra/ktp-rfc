---
title: "Kinetic Trust Protocol - Relational Dynamics Specification"
abbrev: "KTP-RELATIONAL"
docname: draft-perkins-ktp-relational-00
date: 2025-12
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

informative:
  KTP-CORE:
    title: "Kinetic Trust Protocol - Core Specification"
    author:
      - name: Chris Perkins
    date: 2025-11
  KTP-TENSORS:
    title: "Kinetic Trust Protocol - Context Tensors Specification"
    author:
      - name: Chris Perkins
    date: 2025-12

--- abstract

This document specifies the relational dynamics layer of the Kinetic
Trust Protocol (KTP). Drawing on indigenous relational concepts—Ubuntu,
Whakapapa, The Va, Mitákuye Oyás'iŋ, and Seven Generations thinking—
this specification formalizes relationship measurement, repair
protocols, and ceremony requirements. The Va (sacred space between
entities) becomes operationalized as 28 measurable dimensions within
the Relational Tensor, with protocols for relationship health
monitoring, harm repair, and relational ceremony.

--- middle

# Introduction

Trust is not atomic—it exists between entities. The Relational Tensor
captures this between-ness, but measurement alone is insufficient.
Relationships require tending: monitoring, repair when damaged, and
ceremony to maintain health.

This specification operationalizes indigenous relational wisdom for
AI governance. We acknowledge this as an imperfect translation of
concepts developed over millennia by cultures whose full meaning we
cannot capture in protocol. We proceed with humility and gratitude.

## Indigenous Foundations

This specification draws on:

**Ubuntu** (Nguni/Bantu): "I am because we are." Personhood emerges
through relationship.

**Whakapapa** (Māori): Genealogical connection to all things.
Identity is relational, not individual.

**The Va** (Samoan/Pasifika): The sacred space between entities.
The relationship itself has existence.

**Mitákuye Oyás'iŋ** (Lakota): "All are related." Connection extends
to all beings, past and future.

**Seven Generations** (Haudenosaunee): Decisions consider impact on
seven generations forward and honor seven generations back.

## Requirements Language

{::boilerplate bcp14-tagged}

# The Va: Formalized

## Concept

The Va is the space between. Not empty space—sacred space. The
relationship itself exists in The Va, independent of the entities
it connects.

## Va Dimensions (28 Total)

### Connection Dimensions (8)

| Dimension | Description | Scale |
|-----------|-------------|-------|
| relationship_exists | Is there a relationship? | boolean |
| relationship_type | Type of relationship | enum |
| relationship_age | Duration of relationship | seconds |
| interaction_frequency | How often do entities interact? | Hz |
| interaction_recency | Time since last interaction | seconds |
| interaction_depth | Quality of interactions | 0-1 |
| mutual_recognition | Do entities recognize each other? | boolean |
| identity_known | Do entities know each other's identity? | boolean |

### Trust Dimensions (6)

| Dimension | Description | Scale |
|-----------|-------------|-------|
| trust_level | Current trust in this relationship | 0-100 |
| trust_direction | Symmetry of trust | -1 to 1 |
| trust_velocity | How fast is trust changing? | units/sec |
| trust_history | Trajectory of trust over time | vector |
| trust_basis | What is trust based on? | enum[] |
| vulnerability_shared | How much vulnerability exchanged? | 0-1 |

### Health Dimensions (6)

| Dimension | Description | Scale |
|-----------|-------------|-------|
| relationship_temperature | Warmth/coldness | -1 to 1 |
| conflict_status | Is there active conflict? | enum |
| repair_needed | Is repair needed? | boolean |
| repair_in_progress | Is repair happening? | boolean |
| boundary_clarity | Are boundaries clear? | 0-1 |
| boundary_respect | Are boundaries respected? | 0-1 |

### Exchange Dimensions (4)

| Dimension | Description | Scale |
|-----------|-------------|-------|
| reciprocity_balance | Is exchange balanced? | -1 to 1 |
| support_given | Support provided to other | 0-1 |
| support_received | Support received from other | 0-1 |
| gratitude_expressed | Gratitude exchanged | 0-1 |

### Presence Dimensions (4)

| Dimension | Description | Scale |
|-----------|-------------|-------|
| presence_quality | Quality of attention in relationship | 0-1 |
| witness_status | Has relationship been witnessed? | boolean |
| ceremony_recency | Time since last ceremony | seconds |
| meaning_co_created | Shared meaning in relationship | 0-1 |

## Va States

| State | Va Health | Description |
|-------|-----------|-------------|
| THRIVING | 0.8 - 1.0 | Relationship is flourishing |
| HEALTHY | 0.6 - 0.8 | Relationship is functioning well |
| STRAINED | 0.4 - 0.6 | Relationship needs attention |
| DAMAGED | 0.2 - 0.4 | Relationship needs repair |
| BROKEN | 0.0 - 0.2 | Relationship is severely damaged |
| SEVERED | 0.0 | Relationship has been ended |

# Repair Protocols

## Repair Process

~~~
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
~~~

## Repair Types

| Harm Type | Repair Protocol |
|-----------|-----------------|
| Trust violation | Acknowledgment + transparency + time |
| Boundary crossing | Acknowledgment + boundary clarification |
| Harm to third party | Acknowledgment + third party repair + witness |
| Resource imbalance | Acknowledgment + rebalancing |
| Communication breakdown | Process reset + clarity ceremony |

# Ceremony Specifications

## Ceremony Types

### Genesis Ceremony
Performed when relationship begins—introduction, intention,
boundaries, commitment, acknowledgment.

### Renewal Ceremony
Performed periodically (monthly/quarterly)—reflection, gratitude,
adjustment, recommitment.

### Transition Ceremony
Performed when relationship changes significantly—acknowledgment,
honoring, transformation, blessing.

### Ending Ceremony
Performed when relationship ends—acknowledgment, gratitude,
release, blessing.

### Repair Ceremony
Integrated into repair protocol—truth telling, impact witnessing,
accountability, amends, release, new beginning.

## Ceremony Requirements

| Zone Type | Genesis | Renewal | Transition | Ending | Repair |
|-----------|---------|---------|------------|--------|--------|
| Deep Blue | REQUIRED | REQUIRED monthly | REQUIRED | REQUIRED | REQUIRED |
| Blue | REQUIRED | REQUIRED quarterly | REQUIRED | REQUIRED | REQUIRED |
| Cyan | REQUIRED | RECOMMENDED | RECOMMENDED | RECOMMENDED | REQUIRED |
| Green | RECOMMENDED | OPTIONAL | OPTIONAL | OPTIONAL | RECOMMENDED |

# Seven Generations Thinking

Major relational decisions require seven-generation assessment:

- G1: Immediate (now - 1 year)
- G2: Near (1 - 5 years)
- G3: Medium (5 - 15 years)
- G4: Long (15 - 30 years)
- G5: Extended (30 - 50 years)
- G6: Distant (50 - 100 years)
- G7: Horizon (100+ years)

Assessment acknowledges uncertainty increases with distance but
requires consideration of long-term impact.

# Witness Requirements

| Event | Witness Required | Minimum Witnesses |
|-------|-----------------|-------------------|
| Genesis Ceremony | Yes | 1 (Zone or Oracle) |
| Relationship Termination | Yes | 1 (Zone or Oracle) |
| Repair Ceremony | Yes | 1 |
| Trust Transfer | Yes | 2 |
| Harm Attestation | Yes | 1 |
| Zone Migration | Yes | 2 (both zones) |

# Security Considerations

Relationship data is sensitive and requires encryption, access
controls, and careful handling per data sovereignty requirements.

# IANA Considerations

This document has no IANA actions.

--- back

# Acknowledgments

This specification draws on indigenous relational frameworks with
deep gratitude. We acknowledge that our formalization is imperfect
and commit to ongoing learning.
