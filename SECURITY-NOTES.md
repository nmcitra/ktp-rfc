# Security notes

Defects found in a published version, recorded here as soon as they are found
rather than held until the release that corrects them.

This file is not a release artifact. It carries no DOI, it is not archived, and
it is not part of any tag. Published tags are never moved
(see [VERSIONING.md](VERSIONING.md)); this is how a defect in one becomes
readable before the next one ships.

Each note states what is wrong, which versions carry it, what to do in the
meantime, and where it is corrected.

---

## SN-001 — `ktp-sensors` §6.1 publishes a staleness default that §6.2 contradicts

**Affects:** v1.0.0, v1.0.1 (`v1.0.1-provenance`)
**Component:** `rfcs-txt/ktp-sensors.txt`, §6.1 "Freshness Requirements"
**Found:** 2026-08-13 · **Corrected in:** v2.0.0 *Gödel*
**Tracking:** [nmcitra/ktp-rfc#80](https://github.com/nmcitra/ktp-rfc/issues/80)

### What is wrong

§6.1 publishes a table whose Stale Behavior for the Mass and Inertia dimensions
is **"Use last known"**. Eleven lines later, §6.2 specifies the opposite for the
same condition — a dimension with no available feeds takes the maximum stress
value of 1.0.

A feed that has stopped answering is both stale and unavailable, so both rules
apply and they disagree. §6.1 gives those two dimensions no terminal state at
all: past the maximum stale age, the last known value is held indefinitely, and
nothing escalates.

### Why it matters

§7.1 of the same document names the attack:

> Attackers may attempt to suppress attack indicators to lower R, then strike
> when Trust Scores rise.

Holding the last known value is what makes that attack durable. A suppressed
feed keeps contributing whatever it last reported, for as long as it stays
suppressed. Whoever can freeze a feed also chooses the moment at which it
freezes, so the held value is selected by the adversary rather than by the
environment — it is neither a conservative reading nor a current one.

### What to do on v1.0.x

**Follow §6.2, not §6.1.** Treat a feed whose most recent observation has passed
its `stale_threshold_ms` as unavailable, and apply §6.2's failure ladder to it.
Do not substitute the last known value for an observation that has expired.

Deployments setting `default_on_failure` in a sensor configuration should
satisfy themselves that the value is conservative for their weighting. The
published schema does not enforce it.

### How it is corrected

v2.0.0 removes the Stale Behavior column. Staleness is a property of the
individual feed rather than of the Risk Factor it contributes to; an observation
past its declared threshold is unavailable, and §6.2 governs from there.
`ktp-core` §5.2 states, normatively, that every Risk Factor term is a stress
term and that the substitute for an unobserved term is 1.0.

The correction removes a permitted behavior, which makes it a MAJOR change under
this repository's versioning policy. There is no patch release that can carry
it, which is why this note exists instead of a `v1.0.2`.

---

## SN-002 — `sensor-config.json` validates a configuration that scores an unmonitored environment as risk-free

**Affects:** v1.0.0, v1.0.1 (`v1.0.1-provenance`)
**Component:** `schemas/sensor-config.json` (`docs/schemas/` in the affected
versions), `default_on_failure`
**Found:** 2026-08-13 · **Corrected in:** v2.0.0 *Gödel*
**Tracking:** [nmcitra/ktp-rfc#80](https://github.com/nmcitra/ktp-rfc/issues/80)

### What is wrong

The published schema declares:

```json
"default_on_failure": {
  "type": "number",
  "minimum": 0,
  "maximum": 1,
  "description": "Value to use if all feeds fail (conservative default)"
}
```

The description says "conservative". The constraint permits `0`. Nothing in the
schema makes the description binding, and the field is optional, so a
configuration may also omit it and leave the failure value undefined.

### Why it matters

`R` is a sum of stress terms, and `E_trust` is deflated by it. A dimension
substituting `0` when its feeds fail contributes no stress at all, so **turning
sensors off raises the trust score**. That is a one-line configuration change,
it validates against the published schema, and it inverts the direction the
Risk Factor exists to enforce.

### What to do on v1.0.x

Set `default_on_failure` explicitly on every non-veto dimension, at a value that
is conservative for your weighting. Do not leave it undeclared. Treat `0` as
unavailable rather than as permitted.

For a veto-aggregated dimension, unavailable feeds mean no clearance was
returned. The veto stands.

### How it is corrected

v2.0.0 floors the field at 0.5 — the value `ktp-core` §5.2 glosses as moderate
stress, against `0` for perfect conditions — defaults it to 1, requires it on
every dimension that is not veto-aggregated, and pins it to 1 where aggregation
is `any_veto`. `ktp-core` §5.2 states the underlying rule normatively: the
substitute for a term that cannot be observed is 1.0, and zero measures perfect
conditions rather than unknown ones.

### Also corrected, and found while fixing the above

The schema's own second example — the sovereignty feed configuration — has
**never validated against the schema that publishes it**. Its feeds declare
`refresh_interval_ms: 0` and `stale_threshold_ms: 0` to mean *queried on
demand*, and the schema set minimums of 100 and 1000 with no slot for that
sentinel. v2.0.0 admits `0` explicitly and says what it means. No behavior
depended on this; it is recorded because a schema that rejects its own example
is not a schema anyone has run.

---

## SN-003 — `ktp-enforce` §9.1 states the v1 Hibernation threshold (50) against a tier table that says 22

**Affects:** v2.0.0 (`v2.0.0`)
**Component:** `rfcs-txt/ktp-enforce.txt` and `rfcs-md/ktp-enforce.md`, §9.1 "Hibernation Mode"; source `rfc-src/ktp-enforce.md`
**Found:** 2026-09-03, reported by Mike Storm · **Corrected in:** v2.0.1
**Tracking:** the v2.0.1 release; the reporter's public filing is pending and will be linked here when it lands

### What is wrong

§9.1 opens:

> Hibernation is the most extreme dormancy state, entered when E_trust falls below 50.

The tier table in §5.1 gives Hibernation as `< 22`, the §5.1.5 heading reads
"Hibernation Mode (E_trust < 22)", and the migration table at the end of the
document records the move from `< 50` to `< 22`. v2.0.0 moved the tier
thresholds from 95 · 85 · 70 · 50 to 85 · 72 · 58 · 22, and this sentence was
missed.

### Why it matters

In v2 the Observer tier is `>= 22, < 58`. An implementation that gates on §9.1
hibernates every agent between 22 and 50 — agents the tier table says hold
Observer capability. That band is where an agent recovering from degraded
conditions sits, so the effect is that recovering agents are held
heartbeat-only and cannot climb out by acting.

The failure is silent. Both values are plausible, the migration table is
correct, and the document reads as self-consistent unless §5.1.5 and §9.1 are
read together — a reader who checks the migration table concludes the change
landed.

### What to do on v2.0.0

Gate Hibernation on the tier table: `E_trust < 22`. The tier table and §5.1.5
are the normative statements; the §9.1 sentence is an erratum. Nothing else in
the tag carries a surviving v1 threshold in normative prose — every other
95 · 85 · 70 · 50 occurrence (`ktp-enforce`, `ktp-core`, `ktp-conformance`) is a
two-column v1→v2 migration table and is correct as written.

### How it is corrected

v2.0.1 changes the sentence to "below 22". No other change to the set.
