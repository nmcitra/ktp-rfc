# Getting Started

<div class="ktp-animate" markdown>

Welcome to the Kinetic Trust Protocol—a way to move from static permissions to physics-based trust so autonomous agents can act safely, measurably, and at speed. Digital systems are now kinetic, and we need the environment—not human optimism—to be the final authority.

</div>

---

## The Problem We're Solving

<div class="ktp-animate" markdown>

Traditional authorization systems were designed for humans, not autonomous agents operating at machine speed.(1)
{ .annotate }

1. :material-star-four-points-circle: The agentic authorization challenge is explored in depth in [KTP-CORE](../rfcs/ktp-core.md) Section 1.1, "The Problem with Static Authorization."

</div>

<div class="problem-cards ktp-animate">
  <div class="problem-card">
    <div class="problem-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M7,14A2,2 0 0,1 5,12A2,2 0 0,1 7,10A2,2 0 0,1 9,12A2,2 0 0,1 7,14M12.65,10C11.83,7.67 9.61,6 7,6A6,6 0 0,0 1,12A6,6 0 0,0 7,18C9.61,18 11.83,16.33 12.65,14H17V18H21V14H23V10H12.65Z"/></svg>
    </div>
    <div class="problem-card-content">
      <strong>Static Credentials</strong>
      <span>Remain valid until manually revoked</span>
    </div>
  </div>
  <div class="problem-card">
    <div class="problem-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6Z"/></svg>
    </div>
    <div class="problem-card-content">
      <strong>Binary Permissions</strong>
      <span>Allowed or denied, no gradation</span>
    </div>
  </div>
  <div class="problem-card">
    <div class="problem-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg>
    </div>
    <div class="problem-card-content">
      <strong>Time-Invariant Rules</strong>
      <span>Don't adapt to changing conditions</span>
    </div>
  </div>
  <div class="problem-card">
    <div class="problem-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,5A3,3 0 0,1 15,8A3,3 0 0,1 12,11A3,3 0 0,1 9,8A3,3 0 0,1 12,5M17.13,17C15.92,18.85 14.11,20.24 12,20.92C9.89,20.24 8.08,18.85 6.87,17C6.53,16.5 6.24,16 6,15.47C6,13.82 8.71,12.47 12,12.47C15.29,12.47 18,13.79 18,15.47C17.76,16 17.47,16.5 17.13,17Z"/></svg>
    </div>
    <div class="problem-card-content">
      <strong>Trust by Assertion</strong>
      <span>Not demonstrated behavior</span>
    </div>
  </div>
</div>

!!! danger "The Agentic Gap"
    <span style="font-variant: small-caps; font-weight: 700; color: #e84f4f;">By the end of 2026, autonomous agents will outnumber human users on many enterprise networks. Static permission models cannot scale to govern machine-to-machine interactions happening thousands of times per second.</span>

---

## KTP in 60 Seconds

<div class="ktp-animate" markdown>

The Kinetic Trust Protocol introduces a simple but powerful constraint:(1)
{ .annotate }

1. :material-star-four-points-circle: The Zeroth Law is the supreme constraint in KTP. See [KTP-CORE](../rfcs/ktp-core.md) Section 4, "The Zeroth Law," and [Constitution](constitution.md) Article I.

</div>

<div class="concept-equation ktp-animate">
  <div class="concept-equation-formula">
    <div class="concept-equation-part">
      <span class="concept-equation-symbol">A</span>
      <span class="concept-equation-label">Autonomy</span>
    </div>
    <span class="concept-equation-operator">≤</span>
    <div class="concept-equation-part">
      <span class="concept-equation-symbol">E</span>
      <span class="concept-equation-label">Environment</span>
    </div>
  </div>
  <p class="concept-equation-caption">Action risk must never exceed environmental capacity</p>
</div>

<div class="ktp-animate" markdown>

**A** is the intrinsic risk of the requested action. **E** is the current Trust Score. If the action's risk exceeds the environment's capacity, the action is denied. No exceptions. No escalation. No override.

This is not a policy—it's physics. Just as you cannot exceed the speed of light, an agent cannot exceed its trust boundaries.

</div>

---

## The Three Pillars

<div class="ktp-animate" markdown>

KTP rests on three foundational concepts:

</div>

### 1. Trust Scores

<div class="ktp-animate" markdown>

Trust is not granted—it's earned through survival. An agent's Trust Score reflects its demonstrated reliability over time.(1)
{ .annotate }

1. :material-star-four-points-circle: Trust Score calculation methodology is defined in [KTP-CORE](../rfcs/ktp-core.md) Section 5, covering base trust, risk factors, and anti-Goodhart measures.

</div>

<div class="concept-pipeline ktp-animate">
  <div class="concept-pipeline-title">
    <h4>Risk Deflation</h4>
    <p>E_trust = E_base × (1 - R)</p>
  </div>
  <div class="concept-pipeline-step">
    <span class="concept-pipeline-step-label">E_base</span>
    <span class="concept-pipeline-step-sub">Earned capability</span>
  </div>
  <span class="concept-pipeline-arrow">→</span>
  <div class="concept-pipeline-step concept-pipeline-step--deny">
    <span class="concept-pipeline-step-label">Risk (R)</span>
    <span class="concept-pipeline-step-sub">Environmental friction</span>
  </div>
  <span class="concept-pipeline-arrow">→</span>
  <div class="concept-pipeline-step concept-pipeline-step--allow">
    <span class="concept-pipeline-step-label">E_trust</span>
    <span class="concept-pipeline-step-sub">What's permitted now</span>
  </div>
</div>

### 2. Context Tensors

<div class="ktp-animate" markdown>

Environmental state is captured through 1,707 measurements organized into seven dimensions:(1)
{ .annotate }

1. :material-star-four-points-circle: The full Context Tensor specification spans 1,707 dimensions across seven trust dimensions. See [KTP-TENSORS](../rfcs/ktp-tensors.md) for complete measurement definitions.

</div>

<div class="dimension-cards-grid ktp-animate">
  <a href="../context-tensor/#__tabbed_2_1" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">M</span><span class="mono-secondary">a</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Mass</strong>
      <span>Telemetry volume</span>
    </div>
  </a>
  <a href="../context-tensor/#__tabbed_2_2" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">M</span><span class="mono-secondary">o</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Momentum</strong>
      <span>Rate of change</span>
    </div>
  </a>
  <a href="../context-tensor/#__tabbed_2_3" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">I</span><span class="mono-secondary">n</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Inertia</strong>
      <span>Resistance to shift</span>
    </div>
  </a>
  <a href="../context-tensor/#__tabbed_2_4" class="dimension-card-mini dimension-card-mini--heat">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">H</span><span class="mono-secondary">t</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Heat</strong>
      <span>Stress & anomalies</span>
    </div>
  </a>
  <a href="../context-tensor/#__tabbed_2_5" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">T</span><span class="mono-secondary">i</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Time</strong>
      <span>Temporal decay</span>
    </div>
  </a>
  <a href="../context-tensor/#__tabbed_2_6" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">O</span><span class="mono-secondary">b</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Observer</strong>
      <span>Vantage point</span>
    </div>
  </a>
  <a href="../context-tensor/#__tabbed_2_7" class="dimension-card-mini dimension-card-mini--soul">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">S</span><span class="mono-secondary">o</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Soul</strong>
      <span>Hard vetoes</span>
    </div>
  </a>
</div>

<p class="dimension-cards-note ktp-animate">
  <a href="../context-tensor/">Explore the full Context Tensor →</a>
</p>

### 3. Blue Zones

<div class="ktp-animate" markdown>

Trust doesn't exist in isolation—it exists in environments. Blue Zones are network segments where Digital Physics is enforced, creating safe harbors where agents can operate with cryptographic trust guarantees.(1)
{ .annotate }

1. :material-star-four-points-circle: Blue Zone architecture and governance is specified in [KTP-ZONES](../rfcs/ktp-zones.md), covering zone types, discovery, ingress/egress, and the zone gradient.

</div>

???+ info "Zone Gradient"
    Zones range from maximum constraint to no enforcement. Agents naturally gravitate toward zones matching their trust level.

    <div class="zone-list">
      <div class="zone-item">
        <div class="zone-dot zone-dot--deep-blue"></div>
        <div class="zone-content">
          <span class="zone-name">Deep Blue</span>
          <span class="zone-desc">Maximum enforcement for critical infrastructure</span>
        </div>
      </div>
      <div class="zone-item">
        <div class="zone-dot zone-dot--blue"></div>
        <div class="zone-content">
          <span class="zone-name">Blue</span>
          <span class="zone-desc">Full enforcement for enterprise workloads</span>
        </div>
      </div>
      <div class="zone-item">
        <div class="zone-dot zone-dot--cyan"></div>
        <div class="zone-content">
          <span class="zone-name">Cyan</span>
          <span class="zone-desc">Partial enforcement for public APIs</span>
        </div>
      </div>
      <div class="zone-item">
        <div class="zone-dot zone-dot--green"></div>
        <div class="zone-content">
          <span class="zone-name">Green</span>
          <span class="zone-desc">Minimal enforcement bridge from Wild</span>
        </div>
      </div>
      <div class="zone-item">
        <div class="zone-dot zone-dot--wild"></div>
        <div class="zone-content">
          <span class="zone-name">Wild</span>
          <span class="zone-desc">Legacy Internet, no KTP physics</span>
        </div>
      </div>
    </div>

---

## Choose Your Path

<div class="track-cards ktp-animate">
  <a href="../core-concepts/" class="track-card">
    <div class="track-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21L19,17.18V13.18L12,17L5,13.18Z"/></svg>
    </div>
    <span class="track-card-name">Learn</span>
    <span class="track-card-desc">Core concepts & philosophy</span>
  </a>
  <a href="../use-cases/" class="track-card">
    <div class="track-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M11,16.5L18,9.5L16.59,8.09L11,13.67L7.91,10.59L6.5,12L11,16.5Z"/></svg>
    </div>
    <span class="track-card-name">Use Cases</span>
    <span class="track-card-desc">Real-world applications</span>
  </a>
  <a href="../../implement/developer-guide/" class="track-card">
    <div class="track-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M14.6,16.6L19.2,12L14.6,7.4L16,6L22,12L16,18L14.6,16.6M9.4,16.6L4.8,12L9.4,7.4L8,6L2,12L8,18L9.4,16.6Z"/></svg>
    </div>
    <span class="track-card-name">Build</span>
    <span class="track-card-desc">Developer guide & SDKs</span>
  </a>
  <a href="../../rfcs/ktp-core/" class="track-card">
    <div class="track-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/></svg>
    </div>
    <span class="track-card-name">Specs</span>
    <span class="track-card-desc">RFC documentation</span>
  </a>
</div>

---

## Your First Steps

<div class="grid cards ktp-animate" markdown>

-   :material-book-open-variant:{ .lg .middle } **Understand the Philosophy**

    ---

    Explore why physics-based constraints are necessary for the agentic age.

    [:octicons-arrow-right-24: Core Concepts](core-concepts.md)

-   :material-scale-balance:{ .lg .middle } **Read the Constitution**

    ---

    The foundational law governing all KTP implementations.

    [:octicons-arrow-right-24: Constitution](constitution.md)

</div>
