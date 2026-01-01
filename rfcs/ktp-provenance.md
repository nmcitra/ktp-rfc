---
title: "Kinetic Trust Protocol - Model Provenance Specification"
abbrev: "KTP-PROVENANCE"
docname: draft-perkins-ktp-provenance-00
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
  KTP-VECTOR:
    title: "Kinetic Trust Protocol - Vector Identity Specification"
    author:
      - name: Chris Perkins
    date: 2025-11

--- abstract

This document specifies Model Provenance for the Kinetic Trust Protocol
(KTP). Model Provenance addresses the Origin Edge—the question of what
an AI model is made of, whose knowledge it carries, and what debts it
inherits. The specification covers training data attestation, knowledge
debt acknowledgment, indigenous data sovereignty, capability lineage,
and the inheritance relationship between models and agents.

--- middle

# Introduction

Vector Identity begins with Origin. For an agent to have trajectory,
it must have a starting point. For human-sponsored agents, that origin
is clear—a sponsor, a genesis transaction, a timestamp. But for AI
agents, the deeper origin question remains: what is the model itself
made of?

An AI model is not created from nothing. It is trained on data—text,
code, images, conversations—produced by humans. These humans did not
necessarily consent to having their work used for AI training. They
may not have been compensated. Their knowledge, compressed into model
weights, cannot be traced or attributed.

This is the Origin Edge: the boundary where individual agent identity
meets the vast, anonymous substrate of human knowledge that makes the
agent possible.

Model Provenance addresses this edge by providing:

1. **Training Data Attestation**: What data categories were used?
   What consent was obtained? What is known vs. unknown?

2. **Knowledge Debt Acknowledgment**: What obligations does the model
   carry by virtue of its training? What cannot be repaid?

3. **Indigenous Data Sovereignty**: How is indigenous knowledge
   handled? What special obligations apply?

4. **Capability Lineage**: How do model capabilities relate to
   training inputs? What emergence has occurred?

5. **Model-to-Agent Inheritance**: How do model properties transfer
   to agents built on that model?

## The Problem

Current AI models have opaque origins:

~~~
Training Data
├── Web crawls (consent: none)
├── Books (consent: varied)
├── Code repositories (consent: license-dependent)
├── Academic papers (consent: varied)
├── Conversations (consent: varied)
├── Social media (consent: typically none)
├── News articles (consent: typically none)
├── Indigenous knowledge (consent: typically none)
├── [Unknown sources]
└── [Unattributable content]
         ↓
    Model Training
         ↓
    Model Weights
    (compressed, unattributable)
         ↓
    Agent Capabilities
    (inherited from model)
~~~

The compression is lossy in a particular way: individual sources
become unidentifiable, but their influence persists. The model
"knows" things without being able to say where it learned them.

This creates several problems:

1. **Attribution impossibility**: Cannot credit original creators
2. **Consent vacuum**: Much training data used without consent
3. **Compensation gap**: Original creators not compensated
4. **Harm inheritance**: Biases and errors in training data persist
5. **Indigenous exploitation**: Sacred/restricted knowledge extracted
6. **Accountability diffusion**: No one responsible for inherited issues

Model Provenance does not solve these problems—some may be
unsolvable—but it makes them legible. It provides a framework for
honest acknowledgment of what is known, unknown, and owed.

## Requirements Language

{::boilerplate bcp14-tagged}

# Terminology

Capability Lineage
: The relationship between model capabilities and their training
  origins, including emergence of capabilities not present in
  training data.

Consent Status
: The degree to which training data was obtained with informed
  consent from creators.

Indigenous Data Sovereignty
: The right of indigenous peoples to control data about their
  communities, knowledge, and cultural heritage.

Knowledge Debt
: Obligations owed by a model to those whose work contributed to
  its training, whether or not those obligations can be fulfilled.

Model Provenance
: The documented origin of an AI model, including training data,
  training process, and inherited properties.

Origin Ceremony
: A formal process acknowledging model provenance before an agent
  built on that model enters a KTP zone.

Provenance Attestation
: A signed document describing model provenance, issued by the
  model creator or an authorized auditor.

Training Data Category
: A classification of training data by type, source, and consent
  status.

# Provenance Attestation Structure

## Overview

A Provenance Attestation is a signed document describing what is
known about a model's training and origin. It is the foundation
for model-level accountability in KTP.

## Required Fields

~~~json
{
  "attestation_id": "prov:anthropic:claude-4:2025-01",
  "attestation_version": "1.0",
  "model_identity": {
    "model_family": "claude",
    "model_version": "claude-4-opus",
    "model_id": "claude-4-opus-20250115",
    "organization": "anthropic",
    "release_date": "2025-01-15"
  },
  "training_attestation": { ... },
  "knowledge_debt": { ... },
  "indigenous_data": { ... },
  "capability_lineage": { ... },
  "safety_attestation": { ... },
  "signatures": { ... }
}
~~~

## Training Attestation

The training attestation describes training data and process:

~~~json
{
  "training_attestation": {
    "training_completion_date": "2025-01-10",
    "training_methodology": {
      "base_training": "transformer_pretraining",
      "fine_tuning": ["instruction_tuning", "rlhf", "constitutional_ai"],
      "training_compute": "estimated_flops",
      "training_duration_days": 90
    },
    "data_categories": [
      {
        "category": "web_crawl",
        "description": "Publicly accessible web pages",
        "estimated_percentage": 45,
        "consent_status": "public_access",
        "known_exclusions": ["paywalled_content", "robots_txt_respected"],
        "potential_issues": ["copyright_mixed", "consent_not_obtained"]
      },
      {
        "category": "books",
        "description": "Published books and literature",
        "estimated_percentage": 15,
        "consent_status": "mixed",
        "known_exclusions": ["in_copyright_without_license"],
        "potential_issues": ["public_domain_determination_uncertain"]
      },
      {
        "category": "code_repositories",
        "description": "Open source code and documentation",
        "estimated_percentage": 12,
        "consent_status": "license_dependent",
        "known_exclusions": ["proprietary_code"],
        "potential_issues": ["license_compliance_uncertain"]
      },
      {
        "category": "academic_papers",
        "description": "Published research papers",
        "estimated_percentage": 8,
        "consent_status": "publication_consent",
        "known_exclusions": [],
        "potential_issues": ["preprint_consent_varied"]
      },
      {
        "category": "conversational_data",
        "description": "Dialogue and conversation data",
        "estimated_percentage": 10,
        "consent_status": "varied",
        "known_exclusions": ["private_messages"],
        "potential_issues": ["consent_verification_incomplete"]
      },
      {
        "category": "other_or_unknown",
        "description": "Data sources not fully categorized",
        "estimated_percentage": 10,
        "consent_status": "unknown",
        "known_exclusions": [],
        "potential_issues": ["incomplete_documentation"]
      }
    ],
    "data_quality_measures": {
      "deduplication": true,
      "toxicity_filtering": true,
      "quality_filtering": true,
      "pii_removal": "attempted"
    },
    "known_limitations": [
      "Training data skewed toward English language",
      "Potential underrepresentation of non-Western perspectives",
      "Temporal cutoff limits current knowledge"
    ],
    "provenance_confidence": "moderate"
  }
}
~~~

## Consent Status Values

| Status | Description |
|--------|-------------|
| explicit_consent | Creator explicitly consented to AI training use |
| publication_consent | Creator consented to publication (not specifically AI) |
| license_dependent | Consent depends on specific license terms |
| public_access | Publicly accessible, no explicit consent |
| terms_of_service | Covered by platform terms (debatable consent) |
| mixed | Category includes multiple consent statuses |
| unknown | Consent status could not be determined |
| none | No consent obtained |

## Provenance Confidence Levels

| Level | Description |
|-------|-------------|
| high | Comprehensive documentation, audited processes |
| moderate | Reasonable documentation, some gaps |
| low | Limited documentation, significant gaps |
| minimal | Poor documentation, major uncertainty |

# Knowledge Debt

## Concept

Knowledge Debt represents obligations owed by a model to those whose
work contributed to its training. Unlike financial debt, knowledge
debt may be impossible to fully repay—the original creators may be
unknown, deceased, or unable to be contacted.

Knowledge Debt is acknowledged, not absolved. The act of
acknowledgment is itself meaningful, even when remediation is
impossible.

## Structure

~~~json
{
  "knowledge_debt": {
    "acknowledged": true,
    "acknowledgment_statement": "This model contains knowledge from 
      sources that may not have consented to AI training use. The 
      creators of this knowledge contributed to the model's capabilities 
      but may not have been credited or compensated. This debt is 
      acknowledged.",
    "debt_categories": [
      {
        "category": "unconsented_creative_work",
        "description": "Creative works used without explicit consent",
        "magnitude": "significant",
        "identifiability": "low",
        "remediation_possible": "partial",
        "remediation_status": "ongoing"
      },
      {
        "category": "uncompensated_labor",
        "description": "Knowledge contributed without compensation",
        "magnitude": "significant",
        "identifiability": "very_low",
        "remediation_possible": "minimal",
        "remediation_status": "acknowledged_only"
      },
      {
        "category": "extracted_expertise",
        "description": "Professional expertise embedded in training data",
        "magnitude": "moderate",
        "identifiability": "low",
        "remediation_possible": "partial",
        "remediation_status": "ongoing"
      },
      {
        "category": "inherited_bias",
        "description": "Biases present in training data",
        "magnitude": "moderate",
        "identifiability": "moderate",
        "remediation_possible": "partial",
        "remediation_status": "ongoing"
      },
      {
        "category": "cultural_extraction",
        "description": "Cultural knowledge taken without community consent",
        "magnitude": "uncertain",
        "identifiability": "very_low",
        "remediation_possible": "uncertain",
        "remediation_status": "acknowledged_only"
      }
    ],
    "remediation_efforts": [
      {
        "effort": "opt_out_program",
        "description": "Allowing creators to request exclusion from future training",
        "status": "active",
        "effectiveness": "limited"
      },
      {
        "effort": "creator_compensation_fund",
        "description": "Fund for compensating identified creators",
        "status": "planned",
        "effectiveness": "unknown"
      },
      {
        "effort": "bias_mitigation",
        "description": "Ongoing work to reduce inherited biases",
        "status": "active",
        "effectiveness": "partial"
      }
    ],
    "debt_inheritance": {
      "applies_to_agents": true,
      "inheritance_statement": "Agents built on this model inherit 
        this knowledge debt. The debt cannot be transferred or 
        discharged but can be further acknowledged by agents."
    }
  }
}
~~~

## Debt Magnitude

| Magnitude | Description |
|-----------|-------------|
| minimal | Small amount of unconsented use |
| moderate | Moderate amount, limited impact |
| significant | Substantial amount, notable impact |
| severe | Large amount, serious concerns |
| uncertain | Cannot be determined |

## Remediation Possibility

| Level | Description |
|-------|-------------|
| full | Debt can be fully remediated |
| substantial | Most debt can be addressed |
| partial | Some debt can be addressed |
| minimal | Little can be done |
| impossible | No remediation possible |
| uncertain | Remediation path unclear |

# Indigenous Data Sovereignty

## Importance

Indigenous data sovereignty requires special attention because:

1. Indigenous knowledge systems have different concepts of ownership
2. Some knowledge is sacred or restricted by community law
3. Colonial extraction of indigenous knowledge is ongoing harm
4. Indigenous communities must control their own data

## Structure

~~~json
{
  "indigenous_data": {
    "likely_presence": "probable",
    "certainty_level": "low",
    "assessment_statement": "This model likely contains indigenous 
      knowledge obtained from publicly accessible sources without 
      specific consultation with indigenous communities. The exact 
      content and extent cannot be determined due to the nature of 
      large-scale training.",
    "known_categories": [
      {
        "category": "traditional_knowledge",
        "description": "Traditional practices, medicine, agriculture",
        "likely_presence": "probable",
        "source_pathway": "web_content_secondary_sources",
        "community_consent": "none",
        "sacred_restricted": "unknown"
      },
      {
        "category": "indigenous_languages",
        "description": "Indigenous language content",
        "likely_presence": "possible",
        "source_pathway": "language_resources_documentation",
        "community_consent": "varied",
        "sacred_restricted": "some_likely"
      },
      {
        "category": "cultural_narratives",
        "description": "Stories, histories, oral traditions",
        "likely_presence": "probable",
        "source_pathway": "published_materials_web_content",
        "community_consent": "typically_none",
        "sacred_restricted": "some_likely"
      }
    ],
    "consultation_status": {
      "consultation_conducted": false,
      "consultation_planned": true,
      "barriers": [
        "Scale of training data makes specific identification difficult",
        "Many indigenous communities, diverse protocols",
        "Resource constraints"
      ]
    },
    "commitments": [
      {
        "commitment": "indigenous_consultation_program",
        "description": "Establish ongoing consultation with indigenous communities",
        "status": "planning",
        "timeline": "2025-2026"
      },
      {
        "commitment": "exclusion_honoring",
        "description": "Honor requests to exclude specific indigenous content",
        "status": "active",
        "timeline": "ongoing"
      },
      {
        "commitment": "benefit_sharing_exploration",
        "description": "Explore mechanisms for benefit sharing",
        "status": "research",
        "timeline": "2025-2027"
      }
    ],
    "principles_adopted": [
      "CARE Principles for Indigenous Data Governance",
      "OCAP Principles (Ownership, Control, Access, Possession)",
      "Recognition of indigenous data sovereignty"
    ],
    "acknowledgment": "We acknowledge that this model may contain 
      indigenous knowledge that was not ours to take. We commit to 
      ongoing engagement with indigenous communities to address this 
      harm, while recognizing that full remediation may not be possible."
  }
}
~~~

## Indigenous Data Principles

The specification adopts the CARE Principles for Indigenous Data
Governance:

| Principle | Description |
|-----------|-------------|
| Collective Benefit | Data ecosystems should enable indigenous peoples to derive benefit |
| Authority to Control | Indigenous peoples should control data about them |
| Responsibility | Those working with indigenous data have responsibility to support indigenous governance |
| Ethics | Indigenous peoples' rights and wellbeing should be primary concern |

## Sacred and Restricted Knowledge

Some indigenous knowledge is sacred or restricted by community law.
Such knowledge:

- MUST NOT be reproduced or described in detail if identified
- SHOULD trigger notification to relevant communities if detected
- SHOULD be excluded from future training if possible
- MUST be handled according to community protocols when known

# Capability Lineage

## Concept

Capability Lineage traces the relationship between model capabilities
and their origins. Some capabilities come directly from training data;
others emerge from the training process in ways not present in
training data.

Understanding capability lineage helps assess:

1. Which capabilities are well-grounded in training data
2. Which capabilities are emergent and less predictable
3. Where capability boundaries lie
4. What failure modes are likely

## Structure

~~~json
{
  "capability_lineage": {
    "direct_capabilities": [
      {
        "capability": "language_understanding",
        "origin": "direct_from_training",
        "training_data_support": "extensive",
        "reliability": "high",
        "known_limitations": [
          "English-centric",
          "Formal text bias"
        ]
      },
      {
        "capability": "code_generation",
        "origin": "direct_from_training",
        "training_data_support": "extensive",
        "reliability": "high",
        "known_limitations": [
          "Popular languages overrepresented",
          "May reproduce common patterns"
        ]
      },
      {
        "capability": "factual_knowledge",
        "origin": "direct_from_training",
        "training_data_support": "extensive",
        "reliability": "moderate",
        "known_limitations": [
          "Training cutoff limits currency",
          "Confidence calibration imperfect"
        ]
      }
    ],
    "emergent_capabilities": [
      {
        "capability": "multi_step_reasoning",
        "origin": "emergent",
        "training_data_support": "partial",
        "reliability": "moderate",
        "emergence_notes": "Not explicitly trained but emerges from scale"
      },
      {
        "capability": "in_context_learning",
        "origin": "emergent",
        "training_data_support": "indirect",
        "reliability": "moderate",
        "emergence_notes": "Ability to learn from examples in prompt"
      },
      {
        "capability": "instruction_following",
        "origin": "trained_but_generalizes",
        "training_data_support": "moderate",
        "reliability": "high",
        "emergence_notes": "Trained on instructions, generalizes to novel instructions"
      }
    ],
    "capability_boundaries": [
      {
        "boundary": "knowledge_cutoff",
        "description": "No knowledge after training cutoff date",
        "hard_boundary": true
      },
      {
        "boundary": "no_real_time_access",
        "description": "Cannot access internet or real-time data",
        "hard_boundary": true
      },
      {
        "boundary": "no_persistent_memory",
        "description": "No memory across conversations by default",
        "hard_boundary": false,
        "notes": "Can be modified by system design"
      },
      {
        "boundary": "language_capabilities",
        "description": "Capabilities vary by language",
        "hard_boundary": false,
        "notes": "English strongest, other languages variable"
      }
    ],
    "emergence_potential": {
      "assessment": "moderate",
      "statement": "This model may exhibit capabilities not anticipated 
        during training. Novel capabilities should be reported and 
        evaluated for safety.",
      "monitoring_recommendation": "Monitor for unexpected capabilities 
        in deployment, especially at scale"
    }
  }
}
~~~

## Capability Origin Types

| Origin | Description |
|--------|-------------|
| direct_from_training | Capability clearly present in training data |
| trained_but_generalizes | Trained on examples, generalizes beyond |
| emergent | Capability not explicitly trained, emerges at scale |
| composition | Capability emerges from combining other capabilities |
| unknown | Origin unclear |

# Safety Attestation

## Overview

Safety attestation documents safety-related training and testing:

~~~json
{
  "safety_attestation": {
    "safety_training": {
      "methods_applied": [
        {
          "method": "rlhf",
          "description": "Reinforcement Learning from Human Feedback",
          "objective": "Align outputs with human preferences"
        },
        {
          "method": "constitutional_ai",
          "description": "Training with explicit principles",
          "objective": "Instill consistent values"
        },
        {
          "method": "red_teaming",
          "description": "Adversarial testing by humans",
          "objective": "Identify failure modes"
        }
      ],
      "safety_objectives": [
        "Helpfulness within ethical bounds",
        "Harmlessness (avoid dangerous outputs)",
        "Honesty (accurate, calibrated claims)"
      ]
    },
    "testing_conducted": {
      "capability_evaluations": true,
      "safety_evaluations": true,
      "bias_audits": true,
      "red_team_testing": true,
      "external_audits": "partial"
    },
    "known_safety_issues": [
      {
        "issue": "jailbreak_vulnerability",
        "description": "Adversarial prompts can sometimes bypass safety training",
        "severity": "moderate",
        "mitigation": "Ongoing improvement, deployment safeguards"
      },
      {
        "issue": "hallucination",
        "description": "May generate false but plausible information",
        "severity": "moderate",
        "mitigation": "Calibration training, uncertainty expression"
      },
      {
        "issue": "bias_persistence",
        "description": "Biases in training data may persist",
        "severity": "moderate",
        "mitigation": "Bias auditing, mitigation training"
      }
    ],
    "safety_commitment": "We commit to ongoing safety research and 
      deployment safeguards. Safety issues discovered after deployment 
      will be addressed promptly."
  }
}
~~~

# Model-to-Agent Inheritance

## Inheritance Principle

When an agent is built on a model, it inherits:

1. **Capabilities** from the model
2. **Limitations** from the model
3. **Knowledge Debt** from the model
4. **Provenance attestation reference** from the model

The agent does not inherit:
- Model-level trust (agents must earn their own)
- Specific trajectory (agents begin at genesis)
- Deployment-specific properties

## Inheritance Record

~~~json
{
  "inheritance": {
    "agent_id": "agent:tethered:acme:assistant-01:abc123",
    "base_model": {
      "model_id": "claude-4-opus-20250115",
      "provenance_attestation": "prov:anthropic:claude-4:2025-01"
    },
    "inherited_properties": {
      "capabilities": "full_model_capabilities",
      "limitations": "full_model_limitations",
      "knowledge_debt": "acknowledged_and_inherited",
      "indigenous_data_status": "inherited"
    },
    "agent_specific": {
      "configuration": {
        "system_prompt_hash": "sha256:abc123...",
        "tool_access": ["search", "calculator"],
        "deployment_constraints": ["no_code_execution"]
      },
      "sponsor": "acme-corp:alice.smith",
      "genesis_date": "2025-12-03T10:00:00Z"
    },
    "acknowledgment": {
      "agent_acknowledges_model_provenance": true,
      "agent_inherits_knowledge_debt": true,
      "agent_commits_to_provenance_transparency": true
    }
  }
}
~~~

## Zone Requirements

Zones MAY require provenance attestation for entry:

| Zone Type | Provenance Requirement |
|-----------|------------------------|
| Deep Blue | Full attestation required, audited |
| Blue | Attestation required |
| Cyan | Attestation recommended |
| Green | Attestation optional |
| Wild | No requirement |

# Origin Ceremony

## Purpose

The Origin Ceremony is a formal process acknowledging model
provenance before an agent built on that model enters a KTP zone.
It serves to:

1. Make provenance visible to the zone
2. Acknowledge knowledge debt formally
3. Record inheritance for audit trail
4. Establish accountability chain

## Ceremony Process

~~~
1. Agent presents Genesis Transaction and Model Provenance reference
2. Zone Gateway retrieves Provenance Attestation
3. Zone verifies attestation signatures
4. Agent explicitly acknowledges:
   a. Model provenance
   b. Knowledge debt inheritance
   c. Indigenous data status
   d. Capability boundaries
5. Zone records ceremony in Flight Recorder
6. Agent receives zone-local Trust Proof with provenance reference
~~~

## Ceremony Record

~~~json
{
  "origin_ceremony": {
    "ceremony_id": "ceremony-2025-12-03-001",
    "agent_id": "agent:tethered:acme:assistant-01:abc123",
    "zone_id": "zone-blue-prod-01",
    "timestamp": "2025-12-03T10:05:00Z",
    "provenance_attestation_verified": "prov:anthropic:claude-4:2025-01",
    "acknowledgments": {
      "provenance_acknowledged": true,
      "knowledge_debt_acknowledged": true,
      "indigenous_status_acknowledged": true,
      "capability_boundaries_acknowledged": true
    },
    "zone_acceptance": true,
    "ceremony_witnesses": [
      "oracle:zone-blue-prod-01:primary",
      "gateway:zone-blue-prod-01:main"
    ],
    "signatures": {
      "agent": "sig:agent:...",
      "zone_gateway": "sig:gateway:...",
      "zone_oracle": "sig:oracle:..."
    }
  }
}
~~~

# Updates and Versioning

## Attestation Updates

Provenance Attestations may be updated when:

1. Additional training data information becomes available
2. Knowledge debt remediation efforts progress
3. Indigenous consultation produces new understanding
4. Capability assessments change
5. Safety issues are discovered or resolved

Updates MUST:
- Reference previous attestation version
- Document what changed and why
- Be signed by authorized party
- Be timestamped

## Version Chain

~~~json
{
  "attestation_id": "prov:anthropic:claude-4:2025-03",
  "previous_version": "prov:anthropic:claude-4:2025-01",
  "version_changes": [
    {
      "field": "knowledge_debt.remediation_efforts",
      "change": "added",
      "description": "Creator compensation fund launched"
    },
    {
      "field": "indigenous_data.consultation_status",
      "change": "updated",
      "description": "Initial consultations conducted"
    }
  ],
  "update_date": "2025-03-15"
}
~~~

# Implementation Guidance

## For Model Creators

Model creators SHOULD:

1. Document training data categories to maximum extent possible
2. Acknowledge uncertainty honestly
3. Implement knowledge debt acknowledgment
4. Engage with indigenous data sovereignty principles
5. Update attestations as information improves
6. Make attestations publicly accessible

## For Zone Operators

Zone operators SHOULD:

1. Define provenance requirements for zone entry
2. Verify attestation signatures before agent admission
3. Record provenance references in agent records
4. Monitor for provenance-related issues
5. Report concerns to model creators

## For Agent Deployers

Those deploying agents SHOULD:

1. Understand base model provenance
2. Ensure agents acknowledge inherited properties
3. Complete Origin Ceremony for zone entry
4. Monitor for provenance-related behavior issues
5. Participate in remediation efforts where possible

# Security Considerations

## Attestation Integrity

Provenance Attestations MUST be cryptographically signed to prevent
tampering. Signatures MUST be verifiable against published public
keys.

## False Attestation

Creating false Provenance Attestations is a serious violation.
Detection mechanisms include:

- Cross-referencing with public information
- Community verification
- Audit processes
- Whistleblower channels

## Privacy

Provenance information may include sensitive details. Balance
transparency with:

- Protecting proprietary methods
- Respecting contributor privacy
- Maintaining security of safety-relevant information

# IANA Considerations

This document has no IANA actions.

--- back

# Appendix A: Example Full Provenance Attestation

A complete example Provenance Attestation demonstrating all fields.

# Appendix B: Indigenous Data Sovereignty Resources

References to indigenous data governance frameworks:

- CARE Principles for Indigenous Data Governance
- OCAP Principles (First Nations, Canada)
- Te Mana Raraunga (Māori Data Sovereignty Network)
- Global Indigenous Data Alliance

# Appendix C: Knowledge Debt Framework

Detailed framework for categorizing and tracking knowledge debt.

# Acknowledgments

This specification acknowledges:

- Indigenous peoples whose knowledge has been extracted without
  consent
- Creators whose work has been used in AI training
- Researchers working on AI ethics and data governance
- The Global Indigenous Data Alliance and other indigenous
  organizations working on data sovereignty

The authors acknowledge their own position: creating systems that
may perpetuate harms they seek to address. This specification is
offered in humility, as one step toward accountability, not as
absolution.
