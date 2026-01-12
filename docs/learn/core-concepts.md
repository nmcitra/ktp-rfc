# Core Concepts

Digital Physics is not a metaphor—it's an engineering discipline. This page explains the fundamental concepts that make KTP work.

---

## Digital Physics

<div class="ktp-animate">

Traditional security treats cyberspace as a lawless frontier requiring policies to impose order. KTP takes a different view: digital environments can have *physics*—fundamental constraints that govern what's possible, not just what's permitted.

</div>

<div class="concept-compare ktp-animate">
  <div class="concept-card concept-card--policy">
    <div class="concept-card-header">
      <div class="concept-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/></svg>
      </div>
      <strong>Policy-Based</strong>
    </div>
    <ul>
      <li>Human-speed enforcement</li>
      <li>Depends on interpretation</li>
      <li>Easily circumvented</li>
      <li>Says "you shouldn't"</li>
    </ul>
  </div>
  <div class="concept-card concept-card--physics">
    <div class="concept-card-header">
      <div class="concept-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M12,11A1,1 0 0,1 13,12A1,1 0 0,1 12,13A1,1 0 0,1 11,12A1,1 0 0,1 12,11M4.22,4.22C5.65,2.79 8.75,3.43 12,5.56C15.25,3.43 18.35,2.79 19.78,4.22C21.21,5.65 20.57,8.75 18.44,12C20.57,15.25 21.21,18.35 19.78,19.78C18.35,21.21 15.25,20.57 12,18.44C8.75,20.57 5.65,21.21 4.22,19.78C2.79,18.35 3.43,15.25 5.56,12C3.43,8.75 2.79,5.65 4.22,4.22M15.54,8.46C16.15,9.08 16.71,9.71 17.23,10.34C18.61,8.21 19.11,6.38 18.36,5.64C17.62,4.89 15.79,5.39 13.66,6.77C14.29,7.29 14.92,7.85 15.54,8.46M8.46,15.54C7.85,14.92 7.29,14.29 6.77,13.66C5.39,15.79 4.89,17.62 5.64,18.36C6.38,19.11 8.21,18.61 10.34,17.23C9.71,16.71 9.08,16.15 8.46,15.54M5.64,5.64C4.89,6.38 5.39,8.21 6.77,10.34C7.29,9.71 7.85,9.08 8.46,8.46C9.08,7.85 9.71,7.29 10.34,6.77C8.21,5.39 6.38,4.89 5.64,5.64M9.88,14.12C10.58,14.82 11.3,15.46 12,16.03C12.7,15.46 13.42,14.82 14.12,14.12C14.82,13.42 15.46,12.7 16.03,12C15.46,11.3 14.82,10.58 14.12,9.88C13.42,9.18 12.7,8.54 12,7.97C11.3,8.54 10.58,9.18 9.88,9.88C9.18,10.58 8.54,11.3 7.97,12C8.54,12.7 9.18,13.42 9.88,14.12M18.36,18.36C19.11,17.62 18.61,15.79 17.23,13.66C16.71,14.29 16.15,14.92 15.54,15.54C14.92,16.15 14.29,16.71 13.66,17.23C15.79,18.61 17.62,19.11 18.36,18.36Z"/></svg>
      </div>
      <strong>Physics-Based</strong>
    </div>
    <ul>
      <li>Machine-speed enforcement</li>
      <li>Mathematically consistent</li>
      <li>Cannot be circumvented</li>
      <li>Says "you can't"</li>
    </ul>
  </div>
</div>

!!! abstract "The Physics Principle"
    In physical reality, you don't need a policy against exceeding the speed of light. Physics makes it impossible. Digital Physics creates analogous constraints for autonomous agents.(1)
    { .annotate }

    1. :material-star-four-points-circle: The distinction between policy-based and physics-based security is foundational to KTP. See [KTP-CORE](../rfcs/ktp-core.md) Section 1.2, "The Physics-Based Solution."

---

## The Zeroth Law

<div class="ktp-animate">

At the heart of KTP is a single, inviolable constraint:

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

!!! warning "Supremacy"
    The Zeroth Law cannot be suspended, overridden, or circumvented by any mechanism, credential, or authority. It applies equally to all agents regardless of lineage, generation, or purpose.(1)
    { .annotate }

    1. :material-star-four-points-circle: The Zeroth Law's supremacy is established in [Constitution](constitution.md) Article I, Section 2, and specified in [KTP-CORE](../rfcs/ktp-core.md) Section 4.

### What It Means

- **A (Autonomy)**: The intrinsic risk of the action an agent wants to take
- **E (Environment)**: The current Trust Score—the environment's capacity to absorb risk

### The Silent Veto

<div class="concept-pipeline ktp-animate">
  <div class="concept-pipeline-title">
    <h4>The Silent Veto</h4>
    <p>When A > E</p>
  </div>
  <div class="concept-pipeline-step">
    <span class="concept-pipeline-step-label">Agent Request</span>
    <span class="concept-pipeline-step-sub">Action with risk level A</span>
  </div>
  <span class="concept-pipeline-arrow">→</span>
  <div class="concept-pipeline-step">
    <span class="concept-pipeline-step-label">Zeroth Law Check</span>
    <span class="concept-pipeline-step-sub">Compare A to E</span>
  </div>
  <span class="concept-pipeline-arrow">→</span>
  <div class="concept-pipeline-branch">
    <div class="concept-pipeline-step concept-pipeline-step--allow">
      <span class="concept-pipeline-step-label">A ≤ E</span>
      <span class="concept-pipeline-step-sub">Allowed</span>
    </div>
    <div class="concept-pipeline-step concept-pipeline-step--deny">
      <span class="concept-pipeline-step-label">A > E</span>
      <span class="concept-pipeline-step-sub">Impossible</span>
    </div>
  </div>
</div>

The Silent Veto is not a punishment or denial message—it's physics. The agent doesn't receive an "access denied" error—the action simply becomes impossible, like trying to walk through a wall.(1)
{ .annotate }

1. :material-star-four-points-circle: The Silent Veto mechanism is defined in [KTP-CORE](../rfcs/ktp-core.md) Section 8, covering action risk classification and veto triggers.

---

## Digital Gravity

<div class="ktp-animate" markdown>

If the Zeroth Law is the constraint, Digital Gravity is the enforcement mechanism. When autonomy approaches environmental limits, agents experience increasing resistance.(1)
{ .annotate }

1. :material-star-four-points-circle: Digital Gravity mechanics are fully specified in [KTP-GRAVITY](../rfcs/ktp-gravity.md), covering gravity wells, constraint types, and response curves.

</div>

!!! info "The Gravity Metaphor"
    In physical space, gravity curves spacetime. Objects don't decide to fall—they follow the curvature. In digital space, risk curves the operational environment. Agents don't decide to slow down—latency increases, compute becomes scarce, network paths narrow.

### Gravity Mechanisms

<div class="gravity-cards ktp-animate">
  <div class="gravity-card">
    <div class="gravity-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z"/></svg>
    </div>
    <div class="gravity-card-content">
      <strong>Latency Injection</strong>
      <span>Response delays increase, slowing rapid-fire attacks</span>
    </div>
  </div>
  <div class="gravity-card">
    <div class="gravity-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M6,2H18V8H18V8L14,12L18,16V16H18V22H6V16H6V16L10,12L6,8V8H6V2M16,16.5L12,12.5L8,16.5V20H16V16.5M12,11.5L16,7.5V4H8V7.5L12,11.5Z"/></svg>
    </div>
    <div class="gravity-card-content">
      <strong>Time Dilation</strong>
      <span>Operations take longer, preventing timing exploits</span>
    </div>
  </div>
  <div class="gravity-card">
    <div class="gravity-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12,16A3,3 0 0,1 9,13C9,11.88 9.61,10.9 10.5,10.39L20.21,4.77L14.68,14.35C14.18,15.33 13.17,16 12,16M12,3C13.81,3 15.5,3.5 16.97,4.32L14.87,5.53C14,5.19 13,5 12,5A8,8 0 0,0 4,13C4,15.21 4.89,17.21 6.34,18.65H6.35C6.74,19.04 6.74,19.67 6.35,20.06C5.96,20.45 5.32,20.45 4.93,20.07V20.07C3.12,18.26 2,15.76 2,13A10,10 0 0,1 12,3M22,13C22,15.76 20.88,18.26 19.07,20.07V20.07C18.68,20.45 18.05,20.45 17.66,20.06C17.27,19.67 17.27,19.04 17.66,18.65V18.65C19.11,17.2 20,15.21 20,13C20,12 19.81,11 19.46,10.1L20.67,8C21.5,9.5 22,11.18 22,13Z"/></svg>
    </div>
    <div class="gravity-card-content">
      <strong>Compute Throttling</strong>
      <span>Processing capacity reduces, limiting resource consumption</span>
    </div>
  </div>
  <div class="gravity-card">
    <div class="gravity-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M4,1C2.89,1 2,1.89 2,3V7C2,8.11 2.89,9 4,9H1V11H13V9H10C11.11,9 12,8.11 12,7V3C12,1.89 11.11,1 10,1H4M4,3H10V7H4V3M3,13V18L3,20H10V18H5V13H3M14,13C12.89,13 12,13.89 12,15V19C12,20.11 12.89,21 14,21H11V23H23V21H20C21.11,21 22,20.11 22,19V15C22,13.89 21.11,13 20,13H14M14,15H20V19H14V15Z"/></svg>
    </div>
    <div class="gravity-card-content">
      <strong>Network Isolation</strong>
      <span>Connectivity constrains, containing suspicious agents</span>
    </div>
  </div>
</div>

---

## Experience Score (E)

<div class="ktp-animate" markdown>

Trust in KTP is not granted by authority—it's earned through demonstrated behavior over time. The primary output of the KTP model is the **Experience Score (E_trust)**, a live 0–100 meter of how much autonomy an agent has actually earned.

</div>

### The Trust Equation

<div class="concept-pipeline ktp-animate">
  <div class="concept-pipeline-title">
    <h4>Risk Deflation</h4>
    <p>E_trust = E_base × (1 - R)</p>
  </div>
  <div class="concept-pipeline-step">
    <span class="concept-pipeline-step-label">E_base</span>
    <span class="concept-pipeline-step-sub">Raw performance score</span>
  </div>
  <span class="concept-pipeline-arrow">→</span>
  <div class="concept-pipeline-step concept-pipeline-step--deny">
    <span class="concept-pipeline-step-label">Risk (R)</span>
    <span class="concept-pipeline-step-sub">Environmental friction</span>
  </div>
  <span class="concept-pipeline-arrow">→</span>
  <div class="concept-pipeline-step concept-pipeline-step--allow">
    <span class="concept-pipeline-step-label">E_trust</span>
    <span class="concept-pipeline-step-sub">Effective trust score</span>
  </div>
</div>

What drives Risk Deflation up:

- Open vulnerabilities or failed controls (patch gaps, weak TLS, bad secrets)
- Adversarial signals (DDoS indicators, anomaly spikes, tampering)
- Contextual pressure (regulated data, high-stakes phase, critical audience)

!!! example "Risk Deflation in Action"
    **Clean environment:** An agent scores 90 on base performance. With no risk factors (R = 0), its effective trust stays at 90.

    **Vulnerability detected:** A security issue appears, pushing R to 0.5. The agent's effective trust instantly drops to 45—half its original score. The Zeroth Law now blocks any action requiring trust above 45.

### Trust Velocity

KTP also tracks how trust is *changing*:(1)
{ .annotate }

1. :material-star-four-points-circle: Trust Velocity (dE/dt) and its role in anti-gaming measures is covered in [KTP-CORE](../rfcs/ktp-core.md) Section 5.4 and Section 5.5 on Trust Score Integrity.

$$\frac{dE}{dt}$$

Rapid trust changes—either building or eroding—are themselves signals. Trust that rises too fast may indicate gaming. Trust that falls suddenly may indicate compromise.

---

## Vector Identity

<div class="ktp-animate" markdown>

Traditional identity asks "Who are you?" and expects a static answer (credential, certificate, token).

KTP asks "What have you been doing?" and expects a trajectory.(1)
{ .annotate }

1. :material-star-four-points-circle: Vector Identity replaces static credentials with trajectory-based authentication. See [KTP-IDENTITY](../rfcs/ktp-identity.md) Section 3, "Vector Identity Model."

</div>

<div class="concept-compare ktp-animate">
  <div class="concept-card concept-card--policy">
    <div class="concept-card-header">
      <div class="concept-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M2,3V9H4.95L6.95,15H6V21H12V16.41L17.41,11H22V5H16V9.57L10.59,15H9.06L7.06,9H8V3M4,5H6V7H4M18,7H20V9H18M8,17H10V19H8"/></svg>
      </div>
      <strong>Traditional Identity</strong>
    </div>
    <ul>
      <li>Static credentials</li>
      <li>Point-in-time verification</li>
      <li>"I am X"</li>
      <li>Possession of secrets</li>
    </ul>
  </div>
  <div class="concept-card concept-card--physics">
    <div class="concept-card-header">
      <div class="concept-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M15,16L11,20H21V16H15M14.91,4.5L6.91,12.5L9.91,15.5L17.91,7.5L14.91,4.5M4.12,21.46L2.59,19.92L4.12,18.39L5.66,19.92L4.12,21.46M9.91,7.5L11.45,5.96L10.5,5L9.91,5.59L8.32,4L9.91,2.41L11.45,3.96L13.91,1.5L16.91,4.5L14.45,6.96L16,8.5L14.45,10.04L13.5,9.09L9.91,12.68L9.91,7.5Z"/></svg>
      </div>
      <strong>Vector Identity</strong>
    </div>
    <ul>
      <li>Continuous behavior</li>
      <li>Trajectory analysis</li>
      <li>"I have been doing Y"</li>
      <li>Demonstration of patterns</li>
    </ul>
  </div>
</div>

### The Passport Fallacy

A passport proves you *were* verified at some point. It says nothing about what you've done since. Vector Identity treats identity as a verb—something you continuously demonstrate through behavior, not a noun you possess.

### Lineage Evolution

<div class="lineage-timeline ktp-animate">
  <div class="lineage-phase lineage-phase--tethered">
    <div class="lineage-mono">T</div>
    <div class="lineage-content">
      <strong>Tethered</strong>
      <em>Apprentice</em>
      <span>New agents operate under sponsor supervision</span>
    </div>
  </div>
  <div class="lineage-phase lineage-phase--divergent">
    <div class="lineage-mono">D</div>
    <div class="lineage-content">
      <strong>Divergent</strong>
      <em>Journeyman</em>
      <span>Proven agents gain independence</span>
    </div>
  </div>
  <div class="lineage-phase lineage-phase--persistent">
    <div class="lineage-mono">P</div>
    <div class="lineage-content">
      <strong>Persistent</strong>
      <em>Master</em>
      <span>Mature agents with full autonomy</span>
    </div>
  </div>
</div>

Each phase requires demonstrated survival under real conditions—trust cannot be shortcut.(1)
{ .annotate }

1. :material-star-four-points-circle: Lineage Evolution phases (Tethered, Divergent, Persistent) are specified in [KTP-IDENTITY](../rfcs/ktp-identity.md) Section 8.

---

## Context Tensors

<div class="ktp-animate" markdown>

To enforce the Zeroth Law, KTP must measure both A (action risk) and E (environmental capacity). Context Tensors provide the measurement framework.(1)
{ .annotate }

1. :material-star-four-points-circle: The complete Context Tensor specification spans 1,707 dimensions. See [KTP-TENSORS](../rfcs/ktp-tensors.md) for measurement definitions, aggregation rules, and instrumentation requirements.

</div>

### The Seven Dimensions

<div class="dimension-table-simple ktp-animate" markdown>

| Dimension | What It Measures | Explore |
|-----------|------------------|---------|
| **Mass** | Telemetry density and volume | [Deep dive →](context-tensor.md#__tabbed_2_1) |
| **Momentum** | Direction and velocity of change | [Deep dive →](context-tensor.md#__tabbed_2_2) |
| **Inertia** | Resistance to rapid shifts | [Deep dive →](context-tensor.md#__tabbed_2_3) |
| **Heat** | Environmental stress and anomaly load | [Deep dive →](context-tensor.md#__tabbed_2_4) |
| **Time** | Temporal context and decay | [Deep dive →](context-tensor.md#__tabbed_2_5) |
| **Observer** | Attestation coverage and visibility | [Deep dive →](context-tensor.md#__tabbed_2_6) |
| **Soul** | Constitutional constraints (vetoes) | [Deep dive →](context-tensor.md#__tabbed_2_7) |

</div>

!!! tip "Dimension Interaction"
    These dimensions don't operate in isolation. For example, high **Heat** combined with low **Inertia** creates rapid trust collapse, while high **Mass** with stable **Momentum** indicates a healthy, predictable system.

### Measurement Principles

<div class="principles-list ktp-animate">
  <div class="principle-item">
    <strong>Observable over Internal</strong>
    <span>Measure what agents <em>do</em>, not what they "think"</span>
  </div>
  <div class="principle-item">
    <strong>Continuous over Binary</strong>
    <span>Trust is a spectrum, not yes/no</span>
  </div>
  <div class="principle-item">
    <strong>Trajectory over Snapshot</strong>
    <span>Single measurements are noisy; patterns matter</span>
  </div>
</div>

---

## Where to Go Next

<div class="grid cards ktp-animate" markdown>

-   :material-scale-balance:{ .lg .middle } **The Constitution**

    ---

    See how these concepts become law in the foundational governance document.

    [:octicons-arrow-right-24: Constitution](constitution.md)

-   :material-cube-outline:{ .lg .middle } **Context Tensor**

    ---

    Explore the 7-dimensional trust geometry with interactive visualization.

    [:octicons-arrow-right-24: Context Tensor](context-tensor.md)

-   :material-domain:{ .lg .middle } **Use Cases**

    ---

    See how Digital Physics applies to real-world scenarios.

    [:octicons-arrow-right-24: Use Cases](use-cases.md)

</div>
