# Core Concepts

Digital Physics is not a metaphor—it's an engineering discipline. This page explains the fundamental concepts that make KTP work.

---

## Digital Physics

Traditional security treats cyberspace as a lawless frontier requiring policies to impose order. KTP takes a different view: digital environments can have *physics*—fundamental constraints that govern what's possible, not just what's permitted.

!!! abstract "The Physics Principle"
    In physical reality, you don't need a policy against exceeding the speed of light. Physics makes it impossible. Digital Physics creates analogous constraints for autonomous agents.

### Why Physics Instead of Policy?

| Approach | Speed | Consistency | Gaming Resistance |
|----------|-------|-------------|-------------------|
| **Policy** | Human-speed enforcement | Depends on interpretation | Easily circumvented |
| **Physics** | Machine-speed enforcement | Mathematically consistent | Cannot be circumvented |

Policy says "you shouldn't." Physics says "you can't."(1)
{ .annotate }

1. :material-star-four-points-circle: The distinction between policy-based and physics-based security is foundational to KTP. See [KTP-CORE](../rfcs/ktp-core.md) Section 1.2, "The Physics-Based Solution."

---

## The Zeroth Law

At the heart of KTP is a single, inviolable constraint:

$$A \leq E$$

!!! warning "Supremacy"
    The Zeroth Law cannot be suspended, overridden, or circumvented by any mechanism, credential, or authority. It applies equally to all agents regardless of lineage, generation, or purpose.(1)
    { .annotate }

    1. :material-star-four-points-circle: The Zeroth Law's supremacy is established in [Constitution](constitution.md) Article I, Section 2, and specified in [KTP-CORE](../rfcs/ktp-core.md) Section 4.

### What It Means

- **A (Autonomy)**: The intrinsic risk of the action an agent wants to take
- **E (Environment)**: The current Trust Score—the environment's capacity to absorb risk

If an agent requests an action whose risk exceeds the environmental capacity, the action is denied automatically. This is called the **Silent Veto**.(1)
{ .annotate }

1. :material-star-four-points-circle: The Silent Veto mechanism is defined in [KTP-CORE](../rfcs/ktp-core.md) Section 8, covering action risk classification and veto triggers.

### The Silent Veto

The Silent Veto is not a punishment. It's not a denial message. It's physics.

```
When A > E:
  └── Action denied
  └── No escalation path
  └── No override mechanism
  └── Agent continues with reduced autonomy
```

The agent doesn't receive an "access denied" error—the action simply becomes impossible, like trying to walk through a wall.

---

## Digital Gravity

If the Zeroth Law is the constraint, Digital Gravity is the enforcement mechanism. When autonomy approaches environmental limits, agents experience increasing resistance.(1)
{ .annotate }

1. :material-star-four-points-circle: Digital Gravity mechanics are fully specified in [KTP-GRAVITY](../rfcs/ktp-gravity.md), covering gravity wells, constraint types, and response curves.

!!! info "The Gravity Metaphor"
    In physical space, gravity curves spacetime. Objects don't decide to fall—they follow the curvature. In digital space, risk curves the operational environment. Agents don't decide to slow down—latency increases, compute becomes scarce, network paths narrow.

### Gravity Effects

| Gravity Mechanism | Effect | Use Case |
|-------------------|--------|----------|
| **Latency Injection** | Response delays increase | Slows rapid-fire attacks |
| **Time Dilation** | Operations take longer | Prevents timing exploits |
| **Compute Throttling** | Processing capacity reduces | Limits resource consumption |
| **Network Isolation** | Connectivity constrains | Contains suspicious agents |

### The Gravity Well

As an agent's requested autonomy approaches environmental limits, it enters a "gravity well" where these effects intensify:

```
E_margin = (E - A) / E

If E_margin < 0.3:  Light gravity effects
If E_margin < 0.1:  Strong gravity effects  
If E_margin < 0:    Silent Veto (action impossible)
```

---

## Experience Score (E)

Trust in KTP is not granted by authority—it's earned through demonstrated behavior over time. The primary output of the KTP model is the **Experience Score (E)**, a 0-100 composite metric representing the overall quality and trustworthiness of an agent's interaction.

### The Trust Equation & Risk Deflation

The final Experience Score is calculated by taking the raw capability of the agent and applying **Risk Deflation**—the "friction" of the environment.

$$E_{final} = E_{raw} \times (1 - RiskFactor)$$

Where:

| Component | Meaning | Source |
|-----------|---------|--------|
| **E_raw** | Intrinsic capability | Derived from ARQ dimensions (Accessibility, Retainability, Quality) |
| **RiskFactor** | Environmental friction | Security vulnerabilities, compliance failures, or threat intelligence |
| **E_final** | Effective Trust | The actual "velocity" the agent is allowed to achieve |

!!! example "Risk Deflation in Action"
    An agent with high raw performance ($E_{raw} = 90$) operating in a compliant environment might have a Risk Factor of 0.0, resulting in $E_{final} = 90$.
    
    If a security vulnerability is detected, the Risk Factor might jump to 0.5. The agent's effective score drops to 45 ($90 \times (1 - 0.5)$), instantly constraining its autonomy via the Zeroth Law.

### Trust Velocity

KTP also tracks how trust is *changing*:(1)
{ .annotate }

1. :material-star-four-points-circle: Trust Velocity (dE/dt) and its role in anti-gaming measures is covered in [KTP-CORE](../rfcs/ktp-core.md) Section 5.4 and Section 5.5 on Trust Score Integrity.

$$\frac{dE}{dt}$$

Rapid trust changes—either building or eroding—are themselves signals. Trust that rises too fast may indicate gaming. Trust that falls suddenly may indicate compromise.

---

## Vector Identity

Traditional identity asks "Who are you?" and expects a static answer (credential, certificate, token).

KTP asks "What have you been doing?" and expects a trajectory.(1)
{ .annotate }

1. :material-star-four-points-circle: Vector Identity replaces static credentials with trajectory-based authentication. See [KTP-IDENTITY](../rfcs/ktp-identity.md) Section 3, "Vector Identity Model."

### Identity as Trajectory

| Traditional Identity | Vector Identity |
|---------------------|-----------------|
| Static credentials | Continuous behavior |
| Point-in-time verification | Trajectory analysis |
| "I am X" | "I have been doing Y" |
| Possession of secrets | Demonstration of patterns |

### The Passport Fallacy

A passport proves you *were* verified at some point. It says nothing about what you've done since. Vector Identity treats identity as a verb—something you continuously demonstrate through behavior, not a noun you possess.

### Lineage Evolution

Agents mature through phases:(1)
{ .annotate }

1. :material-star-four-points-circle: Lineage Evolution phases (Tethered, Divergent, Persistent) are specified in [KTP-IDENTITY](../rfcs/ktp-identity.md) Section 8.

1. **Tethered (Apprentice)**: New agents operate under sponsor supervision
2. **Divergent (Journeyman)**: Proven agents gain independence  
3. **Persistent (Master)**: Mature agents with full autonomy

Each phase requires demonstrated survival under real conditions—trust cannot be shortcut.

---

## Context Tensors

To enforce the Zeroth Law, KTP must measure both A (action risk) and E (environmental capacity). Context Tensors provide the measurement framework.(1)
{ .annotate }

1. :material-star-four-points-circle: The complete Context Tensor specification spans 1,707 dimensions. See [KTP-TENSORS](../rfcs/ktp-tensors.md) for measurement definitions, aggregation rules, and instrumentation requirements.

### The Six Domains

| Tensor | Dimensions | Core Question |
|--------|------------|---------------|
| **Soul** | 252 | Who is this agent becoming? |
| **Body** | 157 | What resources does it have? |
| **World** | 387 | What surrounds it? |
| **Time** | 291 | When and how fast? |
| **Relational** | 262 | Who is it connected to? |
| **Signal** | 358 | What does it know? |

**Total: 1,707 dimensions** measuring the full operational context.

### Measurement Principles

1. **Observable over Internal**: Measure what agents *do*, not what they "think"
2. **Continuous over Binary**: Trust is a spectrum, not yes/no
3. **Trajectory over Snapshot**: Single measurements are noisy; patterns matter

---

## Where to Go Next

<div class="grid cards" markdown>

-   :material-scale-balance:{ .lg .middle } **The Constitution**

    ---

    See how these concepts become law in the foundational governance document.

    [:octicons-arrow-right-24: Constitution](constitution.md)

-   :material-domain:{ .lg .middle } **Use Cases**

    ---

    Explore how Digital Physics applies to real-world scenarios.

    [:octicons-arrow-right-24: Use Cases](use-cases.md)

</div>

---

!!! tip "Next Steps"
    Ready to see the formal governance framework? Continue to **[The Constitution](constitution.md)**.
    
    Want to see theory in practice? Jump to **[Use Cases](use-cases.md)**.
