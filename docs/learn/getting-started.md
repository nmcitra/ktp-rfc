# Getting Started

Welcome to the Kinetic Trust Protocol—a way to move from static permissions to physics-based trust so autonomous agents can act safely, measurably, and at speed. We do this because digital systems are now kinetic, and we need the environment—not human optimism—to be the final authority.

We get from today’s brittle controls to a resilient future by refusing to skip fundamentals: rigorous data analytics, asking sharper questions, aligning incentives and culture, and avoiding complacency or false certainty about inherently unpredictable systems. This guide maps that path.

---

## The Problem We're Solving

We’re enamored with the hard problem and honest about its risks: don’t take trust for granted, interrogate the data, and recognize that incentives and culture shape outcomes as much as code. Traditional authorization systems were designed for humans:

- **Static credentials** that remain valid until revoked
- **Binary permissions** (allowed/denied) with no gradation  
- **Time-invariant rules** that don't adapt to conditions
- **Trust by assertion** rather than demonstrated behavior

These models break down in an agentic world where autonomous systems operate at machine speed, make decisions without human review, and interact with each other in ways no policy can anticipate—or fully predict.(1)
{ .annotate }

1. :material-star-four-points-circle: The agentic authorization challenge is explored in depth in [KTP-CORE](../rfcs/ktp-core.md) Section 1.1, "The Problem with Static Authorization."

!!! danger "The Agentic Gap"
    <span style="font-variant: small-caps; font-weight: 700; color: #e84f4f;">By the end of 2026, autonomous agents will outnumber human users on many enterprise networks. Static permission models cannot scale to govern machine-to-machine interactions happening thousands of times per second.</span>

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

$$
E_{\text{trust}} = E_{\text{base}} \times (1 - R)
$$

- **E_base**: Intrinsic capability (earned through demonstrated behavior)
- **R**: Risk Factor (current environmental conditions)
- **E_trust**: Effective Trust Score (what's permitted right now)

### 2. Context Tensors

Environmental state is captured through 1,707 dimensions organized into six tensors:(1)
{ .annotate }

1. :material-star-four-points-circle: The full Context Tensor specification spans 1,707 dimensions across six domains. See [KTP-TENSORS](../rfcs/ktp-tensors.md) for complete measurement definitions.

| Physics Lens | Core Question | RFC Tensor Mapping | Example Signals | Why it matters |
|--------------|---------------|--------------------|-----------------|----------------|
| **Mass** | Volume and density of telemetry | Body + World | Packet rates, occupancy, RF absorption | Establishes how “heavy” the environment is; sets baseline stability. [Dive deeper →](../rfcs/ktp-tensors.md) |
| **Momentum** | Rate of change in trust | Time + Signal | Trust velocity, confidence deltas, surge patterns | Captures acceleration of trust up/down to prevent whiplash. [Dive deeper →](../rfcs/ktp-tensors.md) |
| **Inertia** | Resistance to trust fluctuation | Body + Relational | Service criticality, blast radius, dependency depth | Dampens sudden shifts for high-impact systems; enforces stability. [Dive deeper →](../rfcs/ktp-tensors.md) |
| **Heat** | Operational stress and anomaly detection | World + Signal | Error bursts, adversarial scans, resource contention | Reveals pressure that should lower autonomy or trigger dormancy. [Dive deeper →](../rfcs/ktp-tensors.md) |
| **Time** | Temporal patterns and decay | Time | Phase of event, freshness, decay curves | Governs how long trust holds and when it should decay or refresh. [Dive deeper →](../rfcs/ktp-tensors.md#time) |
| **Observer** | Perspective and vantage point | Relational + Signal | Audience, stakeholder expectations, locality | Adjusts trust by who is impacted and from where it’s measured. [Dive deeper →](../rfcs/ktp-tensors.md) |
| **Soul** | Constitutional constraints that cannot be overridden | Soul | Sovereignty labels, TK/OCAP/CARE rules | Hard vetoes enforced before any other calculation. [Dive deeper →](../rfcs/ktp-tensors.md#soul) |

### 3. Blue Zones

Trust doesn't exist in isolation—it exists in environments. Blue Zones are network segments where Digital Physics is enforced, creating safe harbors where agents can operate with cryptographic trust guarantees.(1)
{ .annotate }

1. :material-star-four-points-circle: Blue Zone architecture and governance is specified in [KTP-ZONES](../rfcs/ktp-zones.md), covering zone types, discovery, ingress/egress, and the zone gradient.

???+ info "Zone Gradient & Colors"
    Zones range from **Deep Blue** (maximum constraint, maximum safety) to **Wild** (no KTP enforcement). Agents naturally gravitate toward zones matching their trust level.

    <span style="color:#0b3d91">:material-circle:</span> <span style="color:#0b3d91; font-weight: 800; letter-spacing: 0.02em; text-transform: uppercase;">Deep Blue</span><br><span style="display:inline-block; margin-left:1.6rem;">Maximum enforcement for critical infrastructure (all Constitutional Laws, full telemetry, sub-second proofs).</span>

    <span style="color:#1e88e5">:material-circle:</span> <span style="color:#1e88e5; font-weight: 800; letter-spacing: 0.02em; text-transform: uppercase;">Blue</span><br><span style="display:inline-block; margin-left:1.6rem;">Full enforcement for enterprise and regulated workloads (trust refresh &lt;10s, labeled data Soul checks).</span>

    <span style="color:#4dd0e1">:material-circle:</span> <span style="color:#4dd0e1; font-weight: 800; letter-spacing: 0.02em; text-transform: uppercase;">Cyan</span><br><span style="display:inline-block; margin-left:1.6rem;">Partial enforcement for public APIs and early adopters (lightweight trajectory, optional Soul).</span>

    <span style="color:#7cb342">:material-circle:</span> <span style="color:#7cb342; font-weight: 800; letter-spacing: 0.02em; text-transform: uppercase;">Green</span><br><span style="display:inline-block; margin-left:1.6rem;">Minimal enforcement bridge from Wild (validate proofs if present).</span>

    <span style="color:#8a8a8a">:material-circle:</span> <span style="color:#8a8a8a; font-weight: 800; letter-spacing: 0.02em; text-transform: uppercase;">Wild</span><br><span style="display:inline-block; margin-left:1.6rem;">Legacy Internet with no KTP physics or trust portability.</span>

---

## How to Use This Site

!!! tip ":material-compass-outline: Quick reset"
    Click the site title (top left) to jump back to the hero page. The footer has shortcuts to Learn, Specs, Implement, and Community—use it as your escape hatch.

**Choose your path with these cues:**

:material-account-tie:{ .ktp-icon } **Leadership track:** Start with [Core Concepts](core-concepts.md) and [Use Cases](use-cases.md) for value narratives, then skim the [Constitution](constitution.md) and [KTP-Core](../rfcs/ktp-core.md) summaries for how physics-based trust reduces risk.

:material-school-outline:{ .ktp-icon } **Learn track:** Start with [Core Concepts](core-concepts.md) and the [Constitution](constitution.md) to see why we treat trust like physics. Then check [Use Cases](use-cases.md) for real-world examples.

:material-hammer-wrench:{ .ktp-icon } **Builder track:** Go to the [Developer Guide](../implement/developer-guide.md) and [SDKs & Libraries](../implement/sdks-and-libraries.md) for integration steps. Need payloads? See the [API Reference](../implement/api-reference.md).

:material-script-text-outline:{ .ktp-icon } **Specs/RFCs:** All formal docs live under `/rfcs/`. Each page ends with “Official RFC Document” so you can read the exact text. Use the right-hand TOC to hop between sections.

:material-eye-plus-outline:{ .ktp-icon } **Annotations & callouts:** Markers (<span class="ktp-annotate" data-note="Hover or tap to see inline notes or deep links to the relevant RFC section.">:material-star-four-points-circle:</span>) expand with extra context. Callouts like **Tip**, **Warning**, or custom labels highlight what matters most.

:material-map-marker-path:{ .ktp-icon } **Lost?** Use the footer sitemap as a mini index or jump back to the hero and pick a new lane.

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
