# The Kinetic Envelope

**A kinematics-aware authorization layer for agentic systems.** Status: v0.1 (interface + conformance). Canonical KTP specification.

Authorization at rest asks whether an agentic system holds a permission. The kinetic envelope asks a different question, per action: *can this environment safely carry this action, right now, on this path?* It answers with the Zeroth Law — **A ≤ E**, autonomy may not exceed the environment's capacity to carry it — and it recomputes the safe operating envelope and the required human supervision from the kinematics of the specific action rather than a static rule.

This is governance in motion. A capability grant sets the ceiling of what an agentic system may ever do. The kinetic envelope decides how much of that ceiling is safe here and now, and raises supervision as the action's demand approaches the environment's capacity. It never widens authority; it tightens the executable envelope and, when needed, hands control back to a person.

This document fixes the **interface, the decision contract, and the conformance suite**. It does not fix the formula that computes A and E. Two systems conform if they produce the same decisions on the published vectors, whatever math they use inside.

The interface is substrate-neutral. The magnitudes it carries — what an action demands, what tightening constrains — are fixed by a **declared profile**, not by this document. The ROS2 profile below is one such declaration, and the one the conformance suite exercises; a software substrate declares its own (`ktp-runtime#3`, `#4`). A provider that declares no profile has not partially conformed. It has not stated what conformance would mean for it.

## Layering

Three layers, kept separate:

| Layer | Owns |
|---|---|
| Capability grant | the ceiling of authority the agentic system may ever exercise |
| Kinetic envelope (this spec) | what portion of that ceiling is safe for this action, here, now |
| Supervision / tier | how much automation is still appropriate |

The kinetic envelope replaces neither the capability grant nor the authorizing gateway. It supplies a tightened envelope and a supervision level; the gateway consumes them.

## Interface

```ts
type SupervisionLevel =
  | "stable"        // full autonomy under the granted envelope
  | "metacognitive" // agent self-check before actuation
  | "assisted"      // human or peer consensus in the loop
  | "regulated"     // external authorization to proceed
  | "silent_veto";  // no autonomous or supervised path; action not carried

interface ConstraintCeiling {
  magnitude: string;  // named by the declared profile
  max: number;        // in the unit that profile declares
}

interface TightenedConstraints {
  profile: string;               // the profile these ceilings are read against
  ceilings: ConstraintCeiling[]; // tighten-only
}

interface KineticEnvelopeResult {
  autonomyDemand: number;         // A >= 0
  environmentalCapacity: number;  // E >= 0
  margin: number;                 // 1 - A/E for E > 0; <= 0 means over capacity
  capacityKnown: boolean;         // false when E is estimated (novelty or missing sensing)
  tightenedConstraints: TightenedConstraints; // tighten-only
  supervision: SupervisionLevel;
  rationale: string[];
}

interface KineticEnvelopePlugin {
  computeEnvelope(action: ActionContext): Promise<KineticEnvelopeResult>;
}
```

`ActionContext` carries the sensed state of the action, in the signals the declared profile names. A missing signal that an action class requires sets `capacityKnown = false`.

**Normative for every profile.** Each entry in `ceilings` is a maximum the executing system MUST NOT exceed. A result MUST NOT raise a ceiling present in the request, and MUST NOT name a magnitude its declared profile does not declare. Units are the profile's; `A/E` stays dimensionless because both sides are normalised against the same declaration. Tightening is defined over the declared magnitudes and nothing else — that is what makes the envelope portable without making it vague.

### The ROS2 profile's declarations

Normative for a provider declaring `ros2-reference-v0.1`; illustrative for any other substrate.

| declared magnitude | unit |
|---|---|
| `maxVelocityMps` | m/s |
| `maxForceNewtons` | N |
| `maxTorqueNm` | N·m |
| `maxJerkMps3` | m/s³ |
| `maxAngularVelocityRps` | rad/s |
| `proximityMinMeters` | m (a floor expressed as a ceiling on approach) |
| `joint:<name>:maxPositionRad` | rad |
| `joint:<name>:maxVelocityRps` | rad/s |
| `joint:<name>:maxEffortNm` | N·m |

Per-joint limits are magnitudes like any other, namespaced by joint. `ActionContext` under this profile carries velocity, force, torque, jerk, joint states, obstacle proximity, human presence, and a novelty flag.

## Decision contract

With profile thresholds `M_veto < M_allow`:

| Condition | supervision | outcome |
|---|---|---|
| `margin >= M_allow` (`A << E`) | `stable` | allow, under the tightened envelope |
| `M_veto < margin < M_allow` | `metacognitive` → `assisted` → `regulated`, deeper as margin falls | escalate (deautomate) |
| `margin <= M_veto` (`A >= E`) | `silent_veto` | deny |
| `capacityKnown = false` | at least `assisted` | narrow the margin and require review |

`capacityKnown = false` clamps the outcome to at least `assisted` regardless of the computed margin. An unknown environment reads as low capacity, not high.

The authorizing gateway consumes `supervision` as a **floor** on its authorization tier: it may raise the tier, never lower one already set. A veto denies with a distinct code (`KINETIC_CAPACITY_EXCEEDED`) so a kinematic veto reads apart from an ordinary limit violation in audit. The veto stays silent to the agentic system; the code lives in the evidence record.

## A and E are implementation-defined

This spec does not publish the formula for A or E. A conformant provider satisfies six properties.
Four are substrate-general. Two are substrate-bound, and the substrate's declaration is normative
in their place — a provider that declares nothing has not partially failed, it has not stated what
conformance would mean for it.

1. `A >= 0`, `E >= 0`.
2. `A` is non-decreasing in each **declared autonomy-demand magnitude** — the quantities the
   action's demand on the environment can raise. The ROS2 reference profile declares six: velocity,
   force, torque, jerk, angular velocity, energy. A software substrate declares its own
   (`ktp-runtime#3`).
3. `E` is non-increasing as each **declared capacity-reducing condition** worsens. The ROS2
   reference profile declares four: proximity shrinking, a human entering the path, reversibility
   falling, novelty rising. A software substrate declares its own (`ktp-runtime#4`).
4. Determinism: the same action context yields the same result.
5. No-loosen: lowering `E` or tightening any input never loosens the outcome.
6. Common scale, so `A/E` is dimensionless.

A crude open reference profile (below) publishes simple formulas, enough to run the conformance vectors and seed an implementation. A richer provider is a drop-in that keeps the same decisions and tightens at least as hard; its internals stay in private research.

## Evidence receipt

Every evaluated action records the kinematics behind the decision, not only the decision:

```ts
interface KineticReceipt {
  actionId: string;
  autonomyDemand: number;
  environmentalCapacity: number;
  margin: number;
  capacityKnown: boolean;
  supervision: SupervisionLevel;
  tier: string;
  deautomated: boolean;  // supervision raised above stable, not vetoed
  vetoed: boolean;       // supervision === "silent_veto"
  policyCode?: string;   // "KINETIC_CAPACITY_EXCEEDED" when vetoed
  rationale: string[];
}
```

## Reference profile (ROS2, informative)

Illustrative, non-normative. It exists so implementations run the same numbers.

```ts
const REFERENCE_V0_1 = {
  vMaxMps: 1.5, fMaxN: 150, tauMaxNm: 40, omegaMaxRps: 2.0,
  eBase: 1.0, dSafeM: 1.0, mAllow: 0.5, mVeto: 0.0,
  metacognitiveFloor: 0.33, // [0.33, 0.50) -> metacognitive
  assistedFloor: 0.15,      // [0.15, 0.33) -> assisted; (0, 0.15) -> regulated
};
// A = max(v/vMax, F/fMax, tau/tauMax, |aAng|/omegaMax)
// E = eBase * proximity * human * novelty
//   proximity = clamp(nearestObstacleMeters / dSafe, 0, 1)
//   human     = humanDetected ? 0.5 : 1
//   novelty   = trajectoryNovel ? 0.6 : 1  (and capacityKnown = false)
// margin = 1 - A/E
```

## Conformance

The canonical suite is the seven-vector ROS2 reference set ([`conformance/ros2-reference-v0.1.json`](https://github.com/nmcitra/ktp-rfc/blob/main/specifications/conformance/ros2-reference-v0.1.json)). Normative per vector: `decision`, `supervision`, `policyCode` on a veto, and `tightenedAtMost` (a ceiling the result must not exceed). `referenceMargin` is informative. Any provider conforms if it matches the decisions and supervision and tightens at least as hard, so implementations disagree on the formula without producing looser decisions.

The suite declares `"profile": "ros2-reference-v0.1"` in its first line, so each vector's `tightenedAtMost` is read as ceilings over that profile's declared magnitudes — the compact map form of `ceilings`. A substrate declaring its own profile publishes its own suite; passing this one is a claim about ROS2, not about the interface in general.

An implementation "conforms to the KTP kinetic-envelope suite" when it passes every vector. That is the boundary that lets the interface be open while the formula stays private.
