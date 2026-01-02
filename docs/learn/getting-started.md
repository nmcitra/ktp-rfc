# Getting Started

Welcome to the Kinetic Trust Protocol. This guide will orient you to the fundamental shift KTP represents—from static permissions to physics-based trust.

---

## The Problem We're Solving

Traditional authorization systems were designed for humans:

- **Static credentials** that remain valid until revoked
- **Binary permissions** (allowed/denied) with no gradation  
- **Time-invariant rules** that don't adapt to conditions
- **Trust by assertion** rather than demonstrated behavior

These models break down in an agentic world where autonomous systems operate at machine speed, make decisions without human review, and interact with each other in ways no policy can anticipate.(1)
{ .annotate }

1. :material-star-four-points-circle: The agentic authorization challenge is explored in depth in [KTP-CORE](../rfcs/ktp-core.md) Section 1.1, "The Problem with Static Authorization."

!!! danger "The Agentic Gap"
    By 2026, autonomous agents will outnumber human users on enterprise networks. Static permission models cannot scale to govern machine-to-machine interactions happening thousands of times per second.

---

## KTP in 60 Seconds

The Kinetic Trust Protocol introduces a simple but powerful constraint:

$$A \leq E$$

Where:

| Symbol | Meaning | Description |
|--------|---------|-------------|
| **A** | Autonomy | The intrinsic risk of the requested action |
| **E** | Environment | The current Trust Score |

**If the action's risk exceeds the environment's capacity, the action is denied.** No exceptions. No escalation. No override.(1)
{ .annotate }

1. :material-star-four-points-circle: The Zeroth Law is the supreme constraint in KTP. See [KTP-CORE](../rfcs/ktp-core.md) Section 4, "The Zeroth Law," and [Constitution](constitution.md) Article I.

This is not a policy—it's physics. Just as you cannot exceed the speed of light, an agent cannot exceed its trust boundaries.

---

## The Three Pillars

KTP rests on three foundational concepts:

### 1. Trust Scores

Trust is not granted—it's earned through survival. An agent's Trust Score reflects its demonstrated reliability over time, measured across six domains.(1)
{ .annotate }

1. :material-star-four-points-circle: Trust Score calculation methodology is defined in [KTP-CORE](../rfcs/ktp-core.md) Section 5, covering base trust, risk factors, and anti-Goodhart measures.

```
E_trust = E_base × (1 - R)
```

- **E_base**: Intrinsic capability (earned through demonstrated behavior)
- **R**: Risk Factor (current environmental conditions)
- **E_trust**: Effective Trust Score (what's permitted right now)

### 2. Context Tensors

Environmental state is captured through 1,707 dimensions organized into six tensors:(1)
{ .annotate }

1. :material-star-four-points-circle: The full Context Tensor specification spans 1,707 dimensions across six domains. See [KTP-TENSORS](../rfcs/ktp-tensors.md) for complete measurement definitions.

| Tensor | Core Question |
|--------|---------------|
| **Soul** | Who is this agent becoming? |
| **Body** | What resources does it have? |
| **World** | What surrounds it? |
| **Time** | When and how fast? |
| **Relational** | Who is it connected to? |
| **Signal** | What does it know? |

### 3. Blue Zones

Trust doesn't exist in isolation—it exists in environments. Blue Zones are network segments where Digital Physics is enforced, creating safe harbors where agents can operate with cryptographic trust guarantees.(1)
{ .annotate }

1. :material-star-four-points-circle: Blue Zone architecture and governance is specified in [KTP-ZONES](../rfcs/ktp-zones.md), covering zone types, discovery, ingress/egress, and the zone gradient.

!!! info "Zone Gradient"
    Zones range from **Deep Blue** (maximum constraint, maximum safety) to **Wild** (no KTP enforcement). Agents naturally gravitate toward zones matching their trust level.

---

## Your First Steps

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **Understand the Philosophy**

    ---

    Explore why physics-based constraints are necessary for the agentic age.

    [:octicons-arrow-right-24: Core Concepts](core-concepts.md)

-   :material-scale-balance:{ .lg .middle } **Read the Constitution**

    ---

    The foundational law governing all KTP implementations.

    [:octicons-arrow-right-24: Constitution](constitution.md)

</div>

---

## Quick Reference

| If you want to... | Start here |
|-------------------|------------|
| Understand the philosophy | [Core Concepts](core-concepts.md) |
| See the foundational rules | [Constitution](constitution.md) |
| Explore real applications | [Use Cases](use-cases.md) |
| Read the technical specs | [Specifications](../specifications/index.md) |
| Start building | [Developer Guide](../implement/developer-guide.md) |

---

!!! tip "Next Steps"
    New to KTP? Continue to **[Core Concepts](core-concepts.md)** to understand Digital Physics and the Zeroth Law.
    
    Ready to see it in action? Jump to **[Use Cases](use-cases.md)** for real-world applications.
