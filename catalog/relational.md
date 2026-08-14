# Context Signals — Relational

Normalization note: the current 9.3 table claims 28 dimensions but displays 27 rows, several with truncated identifiers. The catalogue below normalizes that group rather than carrying the defect forward: `stagnation_risk` is removed as a derived duplicate of growth and drift, while the separately specified `relationship_type` and `interaction_recency` observables restore a defensible count of 28.

## Measurement conventions

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement
envelope (#79), §4 the five observation classes and what each class makes MUST
(#87), §5 label sets (#68), §6 ranges and normalization, §7 aliases. Nothing
in this section overrides any of them.

What this section supplies is the binding: which observation class each
Relational group takes, and which of its rows take a different one.

Group assignments. A group's class is the default for its rows; the named
exceptions take the class given. Three of the five classes are present —
N 210 · A 22 · S 6, totalling 238. There is no class D, because Relational
observes no physical quantity, and no class P, because it reads no third
party's number.

```text
  va             N   relationship_type S; witnessed A
  topology       N   —
  trust          N   —
  obligation     N   covenant_count, covenant_validity A
  communication  N   —
  repair         N   incident_count, incident_rate, peak_severity,
                     cumulative_severity, affected_count, unresolved_count,
                     recurrence_count, verified, accountability_assigned,
                     closure_consent A; appeal_available S
  power          A   revocation_latency, unilateral_fraction,
                     resource_control_share, data_access_share,
                     decision_weight_share, sovereignty_coverage,
                     authority_conflict_count, veto_balance N;
                     jurisdiction_count, exit_available S
  context        N   —
  presence       N   —
  cocreation     N   —
  dynamics       N   —
  generations    N   forecast_horizon S
  place          N   bound_place_count S; community_consent A
```

A rubric is not an authority. Class A is for values that exist because a party
outside the measurement recorded something — an authority issued a delegation,
a human granted consent, a witness attested, an incident was opened against a
record. A score the deployment computes by applying its own rubric or
classifier is class N with an inferred membership rule, and the rubric is its
**instrument identity** under front matter §3, not an adjudication. This is
the line that puts `relational.va.trust_level` in N and
`relational.va.witnessed` in A, and it is the line front matter §4's
six-domain test will have to hold or revise for `soul.values.*`.

Class A's *unknown, not zero* clause is load-bearing throughout `power`,
`repair` and `place`. `relational.place.community_consent` is the case front
matter §4 already names: no consent record is not consent. The same reading
governs `power.consent_current`, `repair.closure_consent` and
`repair.accountability_assigned` — an unassigned accountability and an
unavailable record are different states and MUST be distinguishable.

Projected values. Three `generations` rows describe periods that have not
happened and have no observation window: descendant_impact_peak,
far_uncertainty, reversibility_horizon. They are held in class N against the
record set their scenario model runs over, and marked here rather than
reclassified. Front matter §4 names PROJECTED as a candidate sixth class and
declines to add it, because nmcitra/ktp-rfc#73 and #74 own that question.
`generations.forecast_horizon` is a declared parameter of that model, not a
projection, and is class S.

Bare 0-1 ranges. Eighty Relational signals carry a bare 0-1. Fifty-five are
ratios with a real denominator and satisfy the catalogue rule by declaring
that denominator as their population; no normalization function exists for
them and none is to be invented. Twenty-five are synthetic scores with no
natural denominator and MUST declare a normalization function in the
deployment profile:

```text
  va             clarity, trust_level, boundary_clarity,
                 vulnerability_exchange, presence_quality, meaning_overlap
  trust          outbound_mean, inbound_mean, outbound_minimum,
                 inbound_minimum, asymmetry, chain_minimum, chain_product,
                 sponsor_stake, concentration
  obligation     failure_coupling, exit_cost
  repair         peak_severity, residual_impact
  presence       witness_independence
  cocreation     capability_gain, role_complementarity
  dynamics       fragmentation_score
  generations    descendant_impact_peak, far_uncertainty
```

None is fully determined.

`trust` is the whole group and that is the finding, not an accident of
counting. Every bare `0-1` in Trust Flow is a statistic over the trust edge
value, and the trust edge value is itself a synthetic score. **A derived
statistic inherits the normalization obligation of the quantity it
summarizes** — the same shape as #68's ruling that a derived signal inherits
its label set's cardinality. Declaring a normalization function for
`outbound_mean` without declaring one for the edge value it averages
satisfies the letter of the rule and none of it.

`topology`'s seven are the opposite case and are ratios, including the four
centralities. Their denominator is the graph: declare the node set, its
membership rule, edge direction and weighting, and the value is determined.
The algorithm's own parameters — PageRank's damping factor, weighted versus
unweighted betweenness — are instrument identity under front matter §3. They
are not a normalization function and MUST NOT be declared as one.

Where a ratio's denominator is gated by a predicate — critical, optional,
overdue, valid, encrypted, authenticated, dissenting — the predicate is a
label set and is declared under the catalogue-wide label-set rule, not here.
Relational carries at least fourteen such rows.

Privacy. Nineteen Relational signals carry the [P] mark. The rule governing
the mark is open under nmcitra/ktp-rfc#67, and nothing in this section
authorizes, restricts or interprets it.


## Signals

The tables below are generated from the canonical JSON (`catalog/relational.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/relational.md"
