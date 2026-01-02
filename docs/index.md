---
hide:
  - toc
---

# Kinetic Trust Protocol

*An Internet Governed by Digital Physics, Not Policy*

<div class="hero" markdown>

**What if authorization wasn't a gate, but a gravity well?**

For decades, we've built digital walls. We grant permissions, check credentials, and enforce policies. It is a system of rigid gates and brittle rules.

KTP proposes a different universe. One where trust is mass, risk is friction, and authorization is the natural result of an agent moving through an environment. 

This is not a new policy. It is a new physics.

</div>

---

## The Zeroth Law

<div class="zeroth-law" markdown>

$$A \leq E$$

**Autonomy cannot exceed environmental stability.**

This is the foundational constraint. Not a rule to be enforced—a law that enforces itself. When an agent's requested action (A) exceeds what the environment can absorb (E), the action simply does not occur.

No exception handler. No override flag. No emergency bypass.

Physics.

</div>

---

## The Problem We Solve

Three assumptions poison every authorization system ever built:

<div class="problem-grid" markdown>

**The Passport Fallacy**
:   Possession of a credential equals proof of identity. It does not. Credentials are stolen, shared, and forged. The passport proves nothing about the traveler.

**The Static Fallacy**
:   Permissions verified at time T remain valid at T+1. They do not. The world changes between authentication and action. The gap is where attacks live.

**The Vacuum Fallacy**
:   Digital systems operate independent of physical reality. They do not. Every CPU runs on silicon, in a building, drawing power, generating heat. The physical world votes.

</div>

In the age of autonomous agents operating at machine-speed, all three assumptions fail catastrophically.

---

## The Model

KTP introduces physics where policy once stood.

| Concept | Physics Equivalent | Meaning |
|:--------|:-------------------|:--------|
| **Trust** | Mass | Earned through survival, not granted by fiat |
| **Risk** | Friction | Environmental pressure that constrains movement |
| **Authorization** | Motion | The result of mass overcoming friction |
| **Identity** | Trajectory | A vector through time, not a static credential |

---

## The Trust Equation

<div class="equation-block" markdown>

$$E_{trust} = E_{base} \times (1 - R)$$

| Variable | Range | Meaning |
|:---------|:------|:--------|
| $E_{base}$ | 0–100 | Intrinsic capability, earned through trajectory |
| $R$ | 0–1 | Risk factor from the Context Tensor |
| $E_{trust}$ | 0–100 | What the environment actually allows |

An agent with $E_{base} = 87$ in an environment where $R = 0.52$ has an effective trust of **42**.

Same agent. Different environment. Different physics.

</div>

---

## The Context Tensor

Seven dimensions of environmental reality, measured in real-time:

| Dimension | Symbol | Measures | Example Sensors |
|:----------|:------:|:---------|:----------------|
| **Mass** | M | Physical & computational density | CO₂ levels, badge counts, device density |
| **Momentum** | P | Data flow velocity | Transactions/sec, bandwidth saturation |
| **Heat** | H | Adversarial pressure | WAF blocks, anomaly rates, threat feeds |
| **Time** | T | Moment criticality | Event countdowns, maintenance windows |
| **Inertia** | I | Blast radius | Topology centrality, dependency depth |
| **Observer** | O | Who is watching | VIP presence, regulatory jurisdiction |
| **Soul** | S | Sacred boundaries | TK Labels, OCAP, sacred land geofences |

The first six dimensions contribute weighted values to the Risk Factor.

**Soul** is different. Soul is binary. When sovereignty constraints are violated, the action is forbidden—regardless of trust score. This is the **Silent Veto**.

---

## Trust Tiers

Agents evolve through three lifecycle stages:

<div class="grid cards" markdown>

-   :material-link-variant:{ .lg .middle } __Tethered__

    ---

    **$E_{base}$: 0–33**

    New or untested. Operating under a sponsor's trust. The sponsor stakes their own reputation. Accountability without requiring pre-existing history.

-   :material-chart-timeline:{ .lg .middle } __Divergent__

    ---

    **$E_{base}$: 34–66**

    Proven through survival. Moderate autonomy earned. No longer dependent on a sponsor, not yet capable of sponsoring others.

-   :material-shield-check:{ .lg .middle } __Persistent__

    ---

    **$E_{base}$: 67–100**

    Demonstrated resilience under stress. Can sponsor new agents. Carries enough mass to shape the environment itself.

</div>

---

## Blue Zones

Network segments where Digital Physics is enforced. Safe harbors on the internet.

```
┌─────────────────────────────────────────────────────┐
│                     BLUE ZONE                       │
│                                                     │
│   Trust Oracle Mesh                                 │
│   ├── Oracle 1 ←→ Oracle 2 ←→ Oracle 3             │
│   └── Threshold signatures, quorum consensus        │
│                                                     │
│   Context Tensor Sensors                            │
│   └── [M] [P] [H] [T] [I] [O] [S]                  │
│                                                     │
│   Policy Enforcement Points                         │
│   └── API Gateway │ Service Mesh │ IAM │ DB Proxy  │
│                                                     │
│   Agent Population                                  │
│   └── Tethered → Divergent → Persistent            │
│                                                     │
│   Flight Recorder                                   │
│   └── Immutable audit log of decision geometry     │
│                                                     │
└─────────────────────────────────────────────────────┘
                         ↕
                   [ZONE GATEWAY]
                         ↕
┌─────────────────────────────────────────────────────┐
│                  WILD INTERNET                      │
│        Static credentials. Binary permissions.      │
│              Hope as a security strategy.           │
└─────────────────────────────────────────────────────┘
```

---

## What Makes This Different

<div class="innovations" markdown>

**Vector Identity**
:   You are not what you hold. You are where you've been and how you moved.

**Proof of Resilience**
:   Trust is earned through survival under stress, not granted by authority. An agent that has weathered storms carries more weight than one with a pristine but untested history.

**Sponsorship Model**
:   New agents enter through sponsorship. A sponsor stakes their own trust, creating accountability without requiring pre-existing reputation.

**The Silent Veto**
:   When sovereignty constraints are violated, the action is denied. Not as punishment—as physics.

**Indigenous Data Sovereignty**
:   The Soul dimension operationalizes TK Labels, OCAP/CARE principles, and sacred land protections as immutable constraints. These are not policy exceptions. They are cosmological constants.

**Honest Uncertainty**
:   [KTP-PROBLEMS](rfcs/ktp-problems.md) documents what we don't know how to solve. We invite collaboration rather than claim false completeness.

</div>

---

## Specification

| Domain | RFCs |
|:-------|:-----|
| **Foundation** | [Constitution](constitution.md) · [KTP-CORE](rfcs/ktp-core.md) · [KTP-IDENTITY](rfcs/ktp-identity.md) |
| **Measurement** | [KTP-SENSORS](rfcs/ktp-sensors.md) · [KTP-ENFORCE](rfcs/ktp-enforce.md) · [KTP-AUDIT](rfcs/ktp-audit.md) |
| **Boundaries** | [KTP-ZONES](rfcs/ktp-zones.md) · [KTP-FEDERATION](rfcs/ktp-federation.md) |
| **Infrastructure** | [KTP-CRYPTO](rfcs/ktp-crypto.md) · [KTP-TRANSPORT](rfcs/ktp-transport.md) · [KTP-THREAT-MODEL](rfcs/ktp-threat-model.md) |
| **Operations** | [KTP-RECOVERY](rfcs/ktp-recovery.md) · [KTP-MIGRATION](rfcs/ktp-migration.md) |
| **Governance** | [KTP-HUMAN](rfcs/ktp-human.md) · [KTP-GOVERNANCE](rfcs/ktp-governance.md) · [KTP-PRIVACY](rfcs/ktp-privacy.md) · [KTP-CONFORMANCE](rfcs/ktp-conformance.md) |
| **Special Topics** | [KTP-CELESTIAL](rfcs/ktp-celestial.md) · [KTP-PROBLEMS](rfcs/ktp-problems.md) |

---

## Status

| Metric | Value |
|:-------|:------|
| Version | 0.1 (Draft) |
| RFCs | 19 specifications |
| Lines | ~15,000 |
| License | Apache 2.0 |

**Status**: Draft Specification — NMCITRA  
**Date**: November 2025

These documents have not been submitted to the IETF and do not represent Internet Standards.

---

<div class="closing" markdown>

> *"We cannot command Nature except by obeying her."*  
> — Francis Bacon, 1620

The age of autonomous agents is here. The question is not whether we can control them with words.

The question is whether we can create physics they cannot violate.

</div>

---

<div class="footer-meta" markdown>

**Author**: Chris Perkins — New Mexico Cyber Intelligence & Threat Response Alliance (NMCITRA)

[Glossary](glossary.md) · [Constitution](constitution.md) · [Contributing](https://github.com/nmcitra/ktp-rfc/blob/main/CONTRIBUTING.md) · [License](https://github.com/nmcitra/ktp-rfc/blob/main/LICENSE)

</div>
