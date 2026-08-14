# Context Signals — Meta

The quality of the measurement itself. Every other domain measures the world;
this one measures the instruments — how often the catalogue is resampled, how
old the observations feeding a decision are, and how far apart in time the
readings combined into one aggregate actually sit.

Adopted under **nmcitra/ktp-rfc-tracker#18** (ruled 2026-08-13). It measures the
environment's *observability*, which is E-side, so no category question arises:
a meta signal is a fact about the environment as seen, not a property of the
action requested.

**Authored in waves, and this file holds wave 1.** The ruling's sequence is
`refresh` → coverage and staleness → tamper and cross-sensor disagreement. Only
`refresh` is here. The two later waves append as further groups; nothing in this
file's shape has to change to take them.

## The discipline — evidence, never verdict

The ruling's design constraint, verbatim:

> **author signals that measure the evidence, never signals that assert a
> verdict.** No signal may state that a source *is* spoofed. Signals measure
> divergence, gaps, and provenance; adjudication happens above them.

This is not a house style. It is `catalog/index.md` §4's fifth clause applied
one layer up. That clause says a deployment MUST NOT declare itself the issuing
authority of a value it scored against its own criteria — self-measurement is
not the defect, self-adjudication is. The meta domain measures itself by
construction, so it is the one domain where that failure is available on every
row, and the constraint is what keeps it from becoming self-certification.

Concretely, in this group: `interval_ratio` reports observed ÷ declared and
never says *late*; `receipt_skew` reports a signed difference and never says
*wrong clock*; `missed_polls` counts polls that returned nothing and never
attributes a cause. A row that consulted `stale_threshold_ms` in order to
*decide* would be a verdict; `declared_stale_threshold` reads the threshold and
reports it, which is evidence.

## Measurement conventions

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement envelope (#79),
§4 the five observation classes and what each class makes MUST (#87), §5 label
sets (#68), §6 ranges and normalization, §7 aliases. Nothing in this section
overrides any of them.

What this section supplies is the binding: which observation class each Meta
group takes, and which of its rows take a different one. Two of the five
classes are present — N 14 · S 3, totalling 17.

```text
  refresh         N   declared_interval, declared_stale_threshold,
                      timestamp_source S
```

**Why only two classes, and why one of the absences is a ruling.** There is no
class D: no instrument samples a physical quantity here. There is no class P:
Meta reads no third party's number. There is no class **A**, and that is the
one worth stating — class A requires a record made by a party *outside* the
measurement, and Meta is the measurement. A class-A row in this domain would be
§4's fifth-clause laundering in its purest form.

**Class N here.** The population is the set of feeds declared to populate the
signal, per the deployment profile's `feeds[].populates` — the feed-to-signal
mapping opened by nmcitra/ktp-rfc#106. The accumulation interval and its reset
semantics are the aggregator's observation window. A feed is counted only if it
has both answered and returned a current observation, which is
`[KTP-SENSORS]` §6.2's definition and is not re-derived here.

**Class S here.** `declared_interval` and `declared_stale_threshold` are read
from the feed's `refresh_interval_ms` and `stale_threshold_ms` in
`[KTP-SENSORS]` §2.2 / `sensor-config.json`. `timestamp_source` is read from the
feed declaration. All three take an as-of timestamp and a validity horizon in
place of an observation window, per §4.

**What the declared rows are for.** `[KTP-SENSORS]` §6.1 requires every feed to
declare a refresh interval and a staleness threshold, defaulting the second to
five times the first. Nothing in the catalogue could see either. These rows give
the declarations catalogue identifiers, so what a deployment *claims* about its
own cadence and what it *achieves* become two rows that can be compared —
`interval_ratio` is that comparison, and it is the reason the declared side is
in this wave rather than left on the wire.

**`meta.refresh.sample_count` is the denominator row.** `[KTP-TRANSPORT]` §9.3
already carries `sample_count` per host per window, and it had no catalogue
identifier, so nothing in the catalogue could be aggregated from it or declared
under the D2 bridge. It is named to match the wire field deliberately. It is
also the row that lets §4's sixth clause be satisfied rather than asserted: a
signal reporting a rate over zero observations reports **unknown, not zero**,
and this is the count that distinguishes the two.

**Three age statistics, three questions.** `observation_age` is per signal — the
age of the most recent observation among the feeds populating it.
`observation_age_median` and `observation_age_max` are over the observation set
assembled for one authorization decision: the first says whether the set is
broadly fresh, the second gives the age of the aggregate, since a decision is
only as fresh as its stalest input. `age_span` is max minus min — not how old
but how *spread*, which is the quantity the temporal-alignment bridge law (D2's
open follow-on) has to reconcile and which nothing in the catalogue could
previously compute. `rate_span` is the same question asked of the declarations
rather than the readings: slowest declared interval divided by fastest, over a
Risk Factor's declared subset.

**Undefined denominators, named rather than discovered later.** A feed
declaring `refresh_interval_ms: 0` is queried on demand at decision time and has
no cadence, so `interval_ratio` has no denominator for it and reports unknown,
not zero — §4's sixth clause, in the one place in this group where the
undefined case is structural rather than a failure. `on_demand_feeds` counts
those feeds and `on_demand_latency` times their queries, so the on-demand path
is measured rather than silently excluded.

**Bare 0-1 ranges: none.** Every row in this domain is a time, a count, or a
ratio whose two terms are themselves real quantities, so no row falls under §6's
declaration obligation and none carries a `zero_one` sort. This was an outcome
of the ranges discipline rather than a goal, and it is recorded because a
later wave adding a coverage *fraction* will be the first meta row that does
carry it.

**Label sets.** `timestamp_source` assigns each feed's observations to a
category — the source's own stamp, the aggregator's receipt time, or none — and
is therefore subject to §5: the deployment profile declares the label set it
populates, or the row MUST NOT be used in a Risk Factor aggregation. The value
matters because without it `observation_age` is not interpretable: an age
computed from a receipt time and an age computed from a source stamp are not
the same measurement.

**Aliases.** No row here joins an alias set. Two were checked and are recorded
as distinct rather than merged: `meta.refresh.receipt_skew` is a feed's own
timestamp against local receipt, where `time.sync.clock_offset` is the local
clock against a time reference — different subjects, and the clock-quality
quantity is not re-emitted here. `meta.refresh.sample_count` is deliberately not
named `observation_count`, which `time.history` already uses for the agent's
operational history.

**Privacy.** No Meta signal carries the `[P]` mark. Whether signals that
measure the instruments fall under the mark at all is open under
nmcitra/ktp-rfc#67, which owns the rule and has not stated it.

## What the later waves take

Wave 2 is coverage and staleness. Wave 3 is tamper indicators and cross-sensor
disagreement, with provenance, calibration and uncertainty alongside them. Each
appends a group to `catalog/meta.json` and a line to the group-assignment block
above.

The boundary this wave holds, so a later run does not have to re-derive it: **a
refresh row reports a time, a count, or a ratio of two rates. A row reporting a
fraction of the declared set — or one that has to consult a policy threshold in
order to decide — is wave 2.** `declared_stale_threshold` reads the threshold
and reports it, which is why it is here; a row that applied it would not be.

**The regress is open and this wave does not reach it.** tracker#18 asks who
measures the Meta domain's own coverage, and the answer terminates at a declared
attestation root or not at all. Every row in this wave is computable by the
aggregator from its own ingest log and its own configuration, so the question
does not bite on refresh. It bites on coverage.


## Signals

The tables below are generated from the canonical JSON (`catalog/meta.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/meta.md"
