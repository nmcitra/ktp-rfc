# Missing Evidence: Feed, Signal and Factor

**Proposed, unreleased missing-evidence contract.**

The key words MUST, MUST NOT, REQUIRED, SHOULD and MAY have BCP 14 meanings.

## 1. States do not impersonate observations

The factor population is the five weighted Risk Factors defined by Core.
Demand-side `moment_criticality` remains a separately declared supplied input;
it MUST NOT be configured as a sensor-factor dimension or added to the weighted
population. Its absence follows Core's demand-side rule, not a fabricated
Context Signal observation.

A feed's transport health, a signal's population and a factor's observability
are distinct. Evaluate them under the installed configuration and actual
authenticated source/evaluation context. Candidate labels cannot establish
currentness, independence, signal meaning or catalogue membership.

[Evidence State](../schemas/evidence-state.json) defines closed result shapes:

| Layer | Available branch | Unavailable branch |
| --- | --- | --- |
| Feed | current, value, observed_at_ms | unavailable, reason; no value or carried cached measurement |
| Context Signal | populated, value | unknown, reason; no value |
| Risk Factor | observable, measured/derived value in [0,1] | unobservable, reason and decision_stress = 1; no measured value |

Each result identifies input and layer. Reason is absent, unanswered, stale or
undefined. It describes the actual established condition, not an adversary's
intent or an invented observation. An invalid source/value, failed validation
or unsatisfied population rule is undefined; absence is absent; a query/feed
that returns no usable answer is unanswered; exceeded age is stale. Diagnostic
detail belongs in the owning evidence record outside the closed result.

The value field is never present in an unavailable/unknown/unobservable branch,
not even with null or 1. decision_stress is a separate **restrictive decision
reading**, never a measurement. Zero may still be a genuine current observation
or derived value when the owning signal contract establishes it. A schema cannot
establish whether an observation is true, admissible or current.

## 2. Feed currentness

A feed is current only if it is enabled, its source and observation are
authenticated/admissible, and it has returned a usable observation current under
its declared freshness rule. A healthy connection alone is insufficient. Numeric
feed measurements must be finite; categorical/other raw values must satisfy the
owning catalogue/normalization contract before use. A normalization function
for real observations cannot manufacture a value for missing evidence.

Use the installed feed refresh_interval_ms/stale_threshold_ms rules of
KTP-SENSORS 6.1, including its default threshold of five times refresh interval
and recorded justification for a longer threshold. observed_at_ms and evaluation
time use one authenticated clock basis. An observation is stale when its age
is greater than the positive threshold; equality is current. Unknown clock,
future observations or invalid timestamps are unavailable/undefined, never
current by assumption. A newly received or re-signed old observation retains
its original observation time and cannot refresh its age.

A zero threshold means no cached observation is current. An on-demand feed
requires a new authenticated response for the current evaluation, not an old
response relabeled with a fresh timestamp. A disabled required feed is absent;
disabling it MUST NOT silently remove a signal or factor requirement.

Remove default_on_failure from all active sensor configurations, including
veto configurations; numeric 1 is not an exception. The schema forbids that
member at the configuration and individual-feed levels. There is **no estimator
profile** for filling this gap. No last-known value, partial-stress default,
synthetic signal or separate estimate may impersonate an unavailable feed.
This rule does not rewrite Core's separate capacity/supervision contract;
that contract cannot be used to turn missing feed evidence into observations.

## 3. Signal population and independent continuity

The deployment's feeds mapping and the catalogue's declared population,
normalization, denominator and label-set rules determine which observations can
populate each required signal. A current observation may populate only signals
it is declared and qualified to populate. A mapping name alone cannot change
its semantic type or supply a missing denominator.

**One failed feed does not make a signal unknown if another declared independent
current feed legitimately satisfies the same complete population rule.** This
is the continuity rule. Conversely, a current backup that supplies a different
signal, only part of a required population, or a dependent copy does not meet it.
There is no fraction-of-all-feeds availability rule. Neither 49 percent nor zero
percent of a factor's feeds chooses a numeric default. Availability is checked
for each required signal and its actual population rule.

For a feed claimed as an independent redundant alternative, the installed
mapping MUST declare independence_group and independence_evidence. Groups name
source/control/failure domains; evidence references the approved assessment of
actual independence for this signal's required population. The replacing feed
must belong to a distinct independently established domain from the failed
source it replaces. Strings, endpoints, vendor names or a fresh profile version
do not prove that independence. Shared upstream/control/failure dependencies
MUST NOT be counted as separate independent support. Unknown or false claimed
independence cannot justify continuity; the signal is unknown unless other
admissible evidence satisfies its full rule.

The configuration and population rule are fixed before evaluation; a candidate
or failure cannot rewrite membership or label a dependency independent. Profile
changes require independent approval, a new version/digest and new evidence;
reconfiguration cannot retroactively change the original evaluation record.
This decision neither chooses a universal signal derivation formula nor creates
consensus/fault-bounded selection. Those mechanisms require their own contracts.

A signal with no sufficient current population is unknown. A rate with an empty
eligible-event denominator is unknown even if every feed is current; do not
invent an event, zero, infinity or the previous window's value. Partial
populations count only if the **already installed** signal rule explicitly
establishes a complete valid observation from them. Missing required coverage
cannot be waived by dropping the missing part or changing its denominator.

## 4. Required factor subset

Every signal in a factor's declared subset is required. If any is unknown, the
subset cannot be populated: the factor is unobservable and takes decision_stress
1.0 under Core. Do not drop an unknown signal, rescale weights over survivors,
fill a missing input with zero or a prior value, or reduce the factor's weight
in R. An empty/missing/invalid factor declaration is not a calm observable
factor; it is unobservable and cannot support an authorizing declaration.

When every required signal is populated, use the installed factor aggregation
and normalization contract. Record the factor as observable only if it produces
a valid finite stress in [0,1]. This proposal changes no A, E or aggregation
formula. An undefined aggregate remains unobservable with decision_stress 1.

Applying the maximum stress reading MUST NOT erase unknownness. Preserve all
required-layer states and Core's restrictive uncertainty/supervision handling;
a required unobserved environment cannot become known merely because a finite
bound was applied. Where operational capacity remains unknown, the existing
capacityKnown = false floor applies; where no usable conservative comparison
exists, execution is denied. A populated backup does not automatically grant
permission or remove an unrelated veto or constraint.

## 5. Soul and per-layer attribution

Soul is evaluated on demand for every applicable sovereignty framework. An
unanswered, absent, timed-out, errored or empty framework query is UNDETERMINED
and raises S = 1 under KTP-SENSORS 4.3. Other frameworks' clear answers do not
outvote it. Prior clearances and ordinary signal redundancy do not replace
that current authoritative answer. Record the query and established failure,
not a fabricated answering authority or a positive finding of prohibited use.
If Soul stops evaluation, later factor/margin values remain uncomputed.

Preserve the existing exact undefined_inputs entry shape:

```json
{"input":"feed-a","layer":"feed","state":"unanswered"}
```

input names the actual feed, catalogue signal, factor or framework. Layer is
feed, signal, term or query; state is absent, unanswered, stale or undefined.
Do not add a score, numeric default, reason enum from another contract, or
attribution of motive to this three-field object. Each distinct evaluated
undefined input has one entry. Distinct layers never collapse into one entry.

Record an unavailable feed even when independence-backed continuity populates
the signal; do not invent signal/term entries in that successful branch. If
population fails, also record the signal with state undefined (or stale when
its own derived observation has expired) and the term with state undefined.
An empty denominator yields signal/term undefined entries even with no failed
feed. An unanswered Soul framework yields a query/unanswered entry and veto;
no later term entry is invented if evaluation never reached it. Detailed source
failure and causal links stay in the associated evidence record. Canonical
ordering, when serialized, is layer order feed, signal, term, query, then
lexicographic input identifier within each layer.

Carry these entries only in canonical Decision Geometry and the audit record,
never as additional members of the closed TrustProof payload.

These entries support the attribution work following
[Induced Conservatism](https://github.com/nmcitra/ktp-rfc/issues/146): a feed
failure, a derived unknown and a factor's restrictive reading remain separately
visible. They do not establish whether an adversary caused the uncertainty.
This proposal neither assigns blame nor changes the later attribution bounds.

## 6. Vectors, migration and limits

[missing-evidence-v1.json](conformance/missing-evidence-v1.json) publishes
configuration/outcome shape cases and complete modeled feed-to-signal-to-factor
transitions, including independent backup continuity, all-feed failure, empty
denominators, freshness boundaries, partial subsets, no inputs and unanswered
Soul. Test population/aggregation profiles are declared fixture rules, not a
universal production formula. Implementations must exercise the cases against
their actual sources, catalogue mappings and installed profiles.

Native configuration removes default_on_failure and the 50-percent dimension
fallback. Install actual independent redundancy where continuity is required;
there is no estimator migration alternative. Increment configuration/profile
versions/digests and re-evaluate from current observations. Preserve historical
v2.1 records and bytes under their release; do not rewrite old fallback numbers
into observations or hide old missingness. Explicit legacy handling cannot
provide a fallback around active native validation.

Schema and vector checks do not establish sensor truth, source independence,
population completeness, trusted clocks, actual sensor-stack interoperability
or runtime enforcement. Acquisition, retries, alerting and operator workflow
remain product responsibilities. No public reference implementation or
first-conformance claim is offered.

## Fixed-weight redundant substitution

For `weighted_average`, use the complete declared signal/collection slots and
fixed weights defined in [Sensors Feed Aggregation](../rfc-src/ktp-sensors.md#feed-aggregation).
Each slot contributes once. An independent backup supplies the same slot at the
same weight; its configured source weight cannot change that weight. With slot
weights 1 and 1, readings 0.2 and 0.4 yield 0.3 both before and after replacing
the first source by a backup reading 0.2 whose configured weight is 0.5.
Concurrent alternatives do not add a slot or change the denominator.
