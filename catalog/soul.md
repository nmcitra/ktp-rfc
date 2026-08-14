# Context Signals — Soul

Two source-level repairs are necessary before the catalogue can close. Section 5.6 is labeled **140 dimensions**, but its ten stated group targets total **150**. Separately, Behavioral Consistency is labeled **22 dimensions** but contains only 21 rows; the Tensor Explorer identifies **Action Entropy** as a key Consistency dimension, making it the strongest candidate for the omitted row. ([github.com](https://github.com/nmcitra/ktp-rfc/raw/refs/heads/main/rfcs-txt/ktp-tensors.txt))

I therefore:

- restore `soul.consistency.action_entropy`;
- reduce Error Patterns from 16 to 14;
- reduce Meta-Cognition from 14 to 11;
- reduce Growth Indicators from 14 to 11;
- reduce Environmental Response from 12 to 10.

Those four reductions remove the ten-dimension over-allocation without inventing measurements that duplicate dimensions already present in sections 5.1–5.5.

## Measurement conventions

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement
envelope (#79), §4 the five observation classes and what each class makes MUST
(#87), §5 label sets (#68), §6 ranges and normalization, §7 aliases. Nothing
in this section overrides any of them.

What this section supplies is the binding: which observation class each Soul
group takes, and which of its rows take a different one.

Group assignments. A group's class is the default for its rows; the named
exceptions take the class given. Two of the five classes are present —
N 242 · A 10, totalling 252. Soul is the catalogue's most nearly monoclass
domain: it is the agent's own event log, and one boundary encloses all of it.

```text
  temporal        N   —
  consistency     N   —
  values          N   —
  capability      N   —
  communication   N   —
  relational      N   —
  decision        N   —
  error           N   —
  stress          N   —
  metacognition   N   —
  boundary        N   —
  growth          N   —
  lineage         A   constraint_adherence, origin_drift N
  environment     N   —
  sovereignty     N   —
```

Sections 5.1–5.5 carry one added row each in this file; their remaining 107
rows are the published v1.0.x entries, whose identifiers and ranges are
supplied by `RANGES-PASS-01.md` and are authoritative under
nmcitra/ktp-rfc#69. They take their group's class, which is N in all five
cases.

**`soul.values.*` is class N, not class A, and this corrects the prediction in
front matter §4's six-domain test.** A rubric is not an authority. Class A is
for values that exist because a party outside the measurement recorded
something; `soul.values.harm_avoidance` exists because the deployment scored
its own action log against a declared rubric, and it would exist with no
authority anywhere in the system. The rubric is its **instrument identity**
under front matter §3 — which is already a MUST for classifier- and
oracle-derived values — and the set of scored actions with its eligibility
rule is its population. Calling it adjudication would make the deployment its
own adjudicator, which is the shape the framework exists to refuse.

**Where Soul's class A actually is: `lineage`.** An origin manifest, a parent
identity, a signed provenance record and a verified lineage claim all exist
because an issuer recorded them, and none of them exists because Soul measured
anything. Front matter §4's *unknown, not zero* is load-bearing there:
`soul.lineage.ancestry_gap_count` reading zero because no manifest could be
fetched is not a clean ancestry. The two exceptions are the rows the
deployment computes for itself — `constraint_adherence` and `origin_drift`
score behaviour against the inherited baseline, and the baseline being an
authority's record does not make the score one.

A missing observation is **unknown**, not zero. Soul has stated this since it
was written, and it is stated more generally here than front matter §4 states
it — §4 lands the clause for class **A** only, and Soul has ten class-A rows
out of 252. **The dependence is not where the class is:** 68 of the 78 bare
`0-1` rows in this file are ratios whose denominator is a set of eligible
events that can be empty, and a rate over zero eligible events is unknown, not
zero. None of those 68 is class A. This paragraph is therefore evidence for
nmcitra/ktp-rfc#80 and not a ruling by it; `ktp-sensors` §6.1 publishes a
fail-open *Use last known* that contradicts it, and #80 owns the conflict.

Reading conventions that are Soul's own and are not declaration rules: signed
`-1-1` values use zero as no change or perfect balance; entropy is base-2
Shannon entropy, subject to the label-set cardinality clause in front matter
§5; durations use monotonic event timestamps and are reported in seconds.
"Decision trace" means a structured evidence, constraint and outcome record;
it does not require disclosure or inference of private chain-of-thought.

Bare 0-1 ranges. Seventy-eight of the rows carried in this file take a bare
0-1. Sixty-eight are ratios with a real denominator and satisfy the catalogue
rule by declaring that denominator as their population; no normalization
function exists for them and none is to be invented. Ten are synthetic scores
with no natural denominator and MUST declare a normalization function in the
deployment profile:

```text
  relational      trust_gain, trust_loss, partner_concentration
  decision        uncertainty_at_commit, outcome_error
  error           severity_mean
  metacognition   confidence_update
  boundary        margin_median
  lineage         origin_drift
  sovereignty     migration_continuity
```

None is fully determined.

**Soul is 87% ratio, which is the reverse of what was expected of it.** Front
matter §6 predicts that Soul and Information are behaviour measures where the
synthetic score is the norm; on a full read of this file, Soul's bare `0-1`
rows are overwhelmingly *rates over eligible events*. The retired wording of
this very section is why: it defined a `0-1` rate as "the fraction of eligible
events satisfying the named condition over a declared observation window,"
which is the ratio class stated three years before the class existed. The
prediction was made from the domain's subject matter; the count comes from its
rows.

The 107 rows of sections 5.1–5.5 are **not** included in that seventy-eight.
`RANGES-PASS-01` resolves 73 of them to a bare `0-1`, and those 73 are not
split here — the split lands with the merge that brings those rows into this
file. Front matter §6's census of 433 counts neither them nor Body's
equivalent, and is understated by 91 rows domain-wide.

Where a ratio's denominator is gated by a predicate — eligible, required,
safe, authorized, unauthorized, silent, partial — the predicate is a label set
and is declared under the catalogue-wide label-set rule, not here. Soul
carries at least twenty such rows.

The plausible telemetry sources are action and decision logs, policy-engine records, relationship and trust ledgers, error and incident records, runtime counters, load-test traces, orchestration records, model registries, evaluation results, signed provenance manifests, consent records, and context-sensor streams.

Privacy. Two Soul signals carry the [P] mark: relational.human_acceptance_rate
and relational.human_repair_acceptance. The rule governing the mark is open
under nmcitra/ktp-rfc#67, and nothing in this section authorizes, restricts or
interprets it.


## Signals

The tables below are generated from the canonical JSON (`catalog/soul.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/soul.md"
