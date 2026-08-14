# Context Signals — the catalogue

*The one home for every rule that applies to more than one domain, and the
index of the seven domain files.*

Created in `worklog` under **nmcitra/ktp-rfc#95**, corrected under **#98**
against the full read in **#96**, and moved here under **#108**, which built
`catalog/` per **D5** (#66). This file is the normative half of the index;
`index.json` is its machine half.

**What governs what.** This file carries the **obligation**. A domain file
carries the **binding** — which observation class each of its groups takes,
and which rows take a different one. The canonical form of every row is JSON
(`catalog/<domain>.json`); the markdown tables are generated from it by
`scripts/gen-catalog-tables.py` and transcluded into the domain files. Where a
domain file and this file disagree, this file governs.

Every clause below is quoted from a confirmed ruling, per map #46 process
rule 1. Nothing here is authored new except §4, which #87 ruled and which had
no carrier either, and §4's class-**A** provenance clause, which #98
confirmed.

---

## 0 · Scope

**1,644 signals across seven domains.** #58 froze 1,627 across six; **tracker#18**
(ruled 2026-08-13) adopted the `meta` domain and moved the count. The freeze
follows the count-changers rather than preceding them — a ruling that adds
signals is not a violation of a frozen number, it is the reason the number gets
re-derived.

| domain | signals | file |
|---|---|---|
| `world` | 369 | `catalog/world.json` |
| `information` | 336 | `catalog/information.json` |
| `time` | 275 | `catalog/time.json` |
| `soul` | 252 | `catalog/soul.json` |
| `relational` | 238 | `catalog/relational.json` |
| `body` | 157 | `catalog/body.json` |
| `meta` | 17 | `catalog/meta.json` |
| | **1,644** | |

**`meta` is authored in waves and only the first has landed.** tracker#18's
sequence is `refresh` → coverage and staleness → tamper and cross-sensor
disagreement; `meta.refresh` is the 17 rows above. The domain's own file states
the boundary that decides which wave a row belongs to. Its governing constraint
— *author signals that measure the evidence, never signals that assert a
verdict* — is §4's fifth clause applied to the measurement system itself, and
is stated there rather than here because it binds one domain.

Under **D5** (#66) the catalogue is its own document: seven domain files plus
this index, **canonical as JSON**, markdown generated and transcluded. It
**versions with the release set**. Adding a signal is MINOR and rides the next
release; **removing or renaming a signal ID is MAJOR** — a signal ID is a
permitted value.

Built under **#108** (2026-08-13) from the landed catalogue runs, merged with
the two published completions those runs deliberately excluded: Soul's 107 v1.0.x rows (identifiers and ranges
per `RANGES-PASS-01.md`, authoritative under #69) and Body's 49 published
Power, Thermal and Compute rows (12 identifiers repaired per
`IDENTIFIER-PASS-BODY.md`, same ruling). **This directory is the catalogue;**
the landing files that fed it are retained as provenance and are not published.

The observation-class census, closed exactly on every domain:
**N 1,174 · D 211 · A 117 · S 119 · P 23 = 1,644.**

### The machine encoding

`index.json` carries the domains, counts, class census and the sixteen alias
sets. Each domain JSON carries its groups in catalogue order; per group the
declared class and per row `id`, `name`, `type`, `range`, plus:

- `class` — only where the row is a named exception to its group's class;
- `zero_one` — the three-way bare-`0-1` sort (§6): `ratio`, `synthetic`, or
  `determined`. A `synthetic` row is one that MUST declare a normalization
  function in the deployment profile;
- `p` — transcribes the `[P]` mark as published. The mark's rule is **#67's**
  (open); nothing in this encoding authorizes, restricts or interprets it.

---

## 1 · The object — D5 (#66)

| question | ruled |
|---|---|
| where | its own document, not an appendix to `ktp-signals` |
| how many files | six domain files + an index, in `catalog/` |
| which form is canonical | **JSON.** The domain `.md` is hand-authored conventions prose plus one `--8<--` include |
| cadence | with the set. Adding a signal is MINOR and rides the next release |
| removal | **MAJOR** — a signal ID is a permitted value |
| authorship disclosure | none — *ruled against the recommendation* |

The last row is not an oversight. `VERSIONING.md` defines every tier by effect
on conformance and never by authorship, so a specification is judged on whether
its requirements are checkable, not on who drafted them.

---

## 2 · Identifiers — #69, and the ID scheme

`domain.group.name` — lowercase, snake_case, dot-separated.

**Never truncated.** Shorten the *word*; never the string. The v1.0.x rendering
truncated identifiers to fit a 70-column gutter and produced 50 unresolvable
Soul entries; the tagged text remains authoritative for v1.0.x and is not being
edited.

> **NORMATIVE.** No v1.0.x truncated form is an identifier.

Reconstructions of those identifiers are **authoritative**, carried by one
provenance paragraph per corpus rather than per-row markers. This catalogue's
provenance paragraph is §0's; the reconstruction records are
`RANGES-PASS-01.md` (Soul) and `IDENTIFIER-PASS-BODY.md` (Body).

**Left open by #69, and not settled here:** whether an `Identifier repairs`
section becomes required of every domain file.

---

## 3 · The measurement envelope — #79

Confirmed recommendation, verbatim:

> **Adopt the per-signal envelope, as a consolidation rather than an invention.**
> Five of six domains already assert observation-window and population
> obligations, in five incompatible wordings, none normative, none checkable, and
> none applied to `world`. The fields that belong on the catalogue row are the
> ones that do not vary between readings: **subject/resource, population,
> denominator, observation window, instrument identity.**
>
> - **MUST** — subject, population, observation window
> - **MUST** where the value is classifier- or oracle-derived — instrument
>   identity and version
> - **MAY** — uncertainty
>
> A signal that does not declare them **MUST NOT** be used in a Risk Factor
> aggregation. Same shape as `RANGES-PASS-01`'s bare-`0-1` clause and #68's
> label-set clause: declare it, or it does not aggregate. That is checkable,
> which is #46 success criterion 3, rather than declarative.
>
> **Normalization stays in the deployment profile.** It varies per deployment;
> population does not. `RANGES-PASS-01` binds both in one sentence and the
> catalogue row takes only half — that split is now stated rather than implied.

**The envelope does not ride the wire** (#72). `risk-factors.json` (pre-rewrite: `context-tensor.json`) carries an
`evidence` hash over the observation set; the envelope stays in the aggregator's
log under a retention MUST with a stated floor. **The retention floor is a
number nobody has chosen** — #72's open item, not this file's.

---

## 4 · Observation classes — #87

The envelope in §3 is one obligation. What varies is **what fills each slot**,
and that varies by **observation class** — not by domain and not by group.

> **NORMATIVE.** Every signal belongs to exactly one observation class. A domain
> file declares the class for each of its groups and names the rows that take a
> different class. The class determines which envelope slots are MUST, which are
> `n/a`, and what satisfies them.

| | class | subject | population | window | instrument |
|---|---|---|---|---|---|
| **D** | DIRECT — one instrument samples a physical quantity | sensing location/volume + modality | **n/a** | integration/averaging interval | make/model + **calibration date and reference** |
| **N** | ENUMERATED — computed over a counted set inside a boundary | the boundary | the set + its **membership rule** | accumulation interval + **reset semantics** | MUST where membership is *inferred*, MAY where *enumerated* |
| **A** | ADJUDICATED — exists because an authority recorded it | issuing authority + its scope | the **record set** | open-set horizon or retention period | adjudication criteria + version |
| **P** | PUBLISHED — a third party's number, read | publisher's universe, **by reference** | publisher's, **by reference** | publisher's **reference period** | publisher + series id + **vintage**, and the **publication lag** |
| **S** | DERIVED STATE — read from a table, calendar, config or ephemeris | locale/config scope | **n/a** | **n/a** — as-of timestamp + validity horizon replace it | authoritative source + version |

Four clauses that do not follow from §3 and are normative in their own right:

- **D** — a single instrument observes no set. A deployment **MUST NOT** declare
  a population to satisfy the rule. A MUST that is always trivially met launders
  the obligation.
- **A** — a signal that returns no record reports **unknown, not zero**. A
  deployment **MUST** distinguish an empty record set from an unavailable one.
- **P** — the value's age is the **publication lag**, not the fetch time. And a
  deployment **MUST NOT** restate a publisher's subject or population as its own.
- **S** — there is no observation window. An as-of timestamp and a validity
  horizon are declared in its place, and both are MUST.

A fifth, added under **#98** because it decided 117 rows and was living in five
domain files instead of here:

- **A** — class A requires a record made by a **party outside the
  measurement**. A rubric or classifier the deployment runs is **instrument
  identity under §3**, not adjudication. A deployment **MUST NOT** declare
  itself the issuing authority of a value it scored against its own criteria.
  Self-*measurement* is not the defect and is not restricted; a controller may
  report its own reachability. What it may not also do is choose the criterion
  by which the report counts as passing. **The separating variable is the
  provenance of the criteria, not the provenance of the observation.**

  This is the same failure mode as the class-**D** clause above, one layer up:
  an obligation the constrained party discharges is not discharged, and a MUST
  satisfiable at will launders rather than binds. Confirmed 2026-08-12 under
  #98.

A sixth, added under **#60**, and it is **cross-class rather than per-class** —
the clause existed for **A** alone and the exposure it covers is mostly outside
**A**:

- **All classes.** A signal whose observation is **unavailable reports unknown**,
  and a deployment **MUST** distinguish *unavailable* from *empty*. **An empty
  denominator is unknown, not zero.** A signal reporting unknown **MUST NOT**
  contribute to a Risk Factor aggregation as though it had observed zero risk.

  Class **A** already carried this for record sets, and #96 measured why one
  class is not enough: **68 of `soul`'s 78 bare-`0-1` rows are ratios whose
  denominator is a set of eligible events that can be empty, and none of the 68
  is class A.** A rate over zero eligible events is not a rate of zero. The same
  reading covers a dark instrument (**D**), an unenumerable boundary (**N**), an
  unreachable publisher (**P**) and an unreadable table (**S**), which is why it
  is stated once here rather than four times — five incompatible wordings of one
  obligation is the defect #79 was opened to end.

  **This is the measurement-side half of the undefined-W rule** (round 4; #47
  scope row 4; the class rule is now `ktp-core` §6.7, per #110/#105). The other
  two layers are already normative: `ktp-sensors` §6.2 governs the **feed**, and
  `ktp-core` §5.2 governs the **Risk Factor term** (both landed under #80).
  This clause governs the **signal**, which is the layer neither of those
  reaches — **a signal can be unavailable while every feed feeding it is
  healthy**, and the 68 rows above are exactly that case. Confirmed by Chris
  2026-08-13 under #60.

### The six-domain test — run on samples, then run on every row

#87 authored the classes against `world` alone and named the test: *does the
assignment survive the other five domains?* #95 ran it by **sampling groups**
and said so. **#96 read all 1,102 rows in the five outstanding files.**

| domain | classes present | census |
|---|---|---|
| `world` | D · N · A · P · S | N 135 · D 132 · A 45 · S 37 · P 20 = 369 |
| `information` | N · A · P | N 316 · A 17 · P 3 = 336 |
| `time` | N · S · D · A | N 167 · S 51 · D 39 · A 18 = 275 |
| `relational` | N · A · S | N 210 · A 22 · S 6 = 238 |
| `soul` | N · A | N 242 · A 10 = 252 |
| `body` | N · D · S · A | N 90 · D 40 · S 22 · A 5 = 157 |
| `meta` | N · S | N 14 · S 3 = 17 |

**`meta` postdates the test and was authored under the classes rather than
tested against them** (tracker#18, 2026-08-13). It needs no sixth class either,
and one of its absences is a ruling rather than a gap: **class A cannot occur in
`meta`**, because class A requires a record made by a party outside the
measurement and `meta` *is* the measurement. A class-A meta row would be the
fifth clause's laundering in its purest form. There is no D (no instrument
samples a physical quantity) and no P (it reads no third party's number).

Catalogue-wide: **N 1,174 · D 211 · A 117 · S 119 · P 23 = 1,644.** Each census
closes on its domain total exactly, which is the check that an assignment is a
partition rather than a sketch — and the #108 build re-verifies the closure
mechanically from the JSON on every run of `108-build-catalog.py`.

No domain needs a sixth class **for signals that were observed**. Five holds,
on a full read.

**The candidate that does exist, named rather than added: PROJECTED.** A
forecast has no observation window, because the period it describes has not
happened. Its slots are an **issue time** and a **valid-for horizon**, plus the
model identity and version — structurally the same shape as **P**, minus the
third party. The roster (corrected by the #96 full read) concentrates in
`time.future` — 14 rows — with scattered members elsewhere; a floor of about 20
rows, membership moves. Its distinctive clause would be *a projected value is
not an observation and MUST NOT be aggregated as one* — which is exactly the
question **#73** and **#74** are open on. **This file does not add it.** Adding
the class would rule those tickets by writing the paragraph.

**The sharp line, recorded because it is easy to get wrong:** *scoring a
forecast is an observation; the forecast is not.*
`time.future.forecast_mae` and `information.sensemaking.forecast_brier` are
class **N** — backtests over a record set of resolved forecasts.

---

## 5 · Label sets — #68

Confirmed clause, verbatim:

> a signal whose value requires assigning observations to categories MUST
> declare, in the deployment profile, the label set it populates; a signal with
> no declared label set MUST NOT be used in a Risk Factor aggregation

And its second half, also confirmed:

> **Derived signals inherit the label set's cardinality.** `emotion_entropy`
> cannot be `0-inf bits` over a closed twelve-label set.

Fifteen `_entropy` rows carry a range that is either over an undeclared set or
carries a wrong one. That becomes checkable once the declarations exist, which
is what makes this satisfy #46 success criterion 3 rather than merely asserting
it.

**A predicate is a label set.** Where a ratio's denominator is gated by a word —
`healthy`, `available`, `critical`, `active` — that word enumerates a category
and falls under this clause, not under §6. `world` alone carries at least 13
such rows.

**Left open by #68, and not settled here:** the reference label set needs a real
identifier. `ktp-emotion-12` was a placeholder, and whether it becomes a
registry interacts with OTCS.

---

## 6 · Ranges and normalization — `RANGES-PASS-01`, as split by #79

The original clause:

> **NORMATIVE.** A signal whose range is a bare `0-1` **MUST** declare its
> normalization function and reference population in the deployment profile.
> Without both, the value is not comparable across deployments and **MUST NOT**
> be used in a Risk Factor aggregation.

**#79 split its two halves across two carriers, and that split is normative:**
**reference population → the row. Normalization function → the deployment
profile.** Population does not vary per deployment; normalization does.

**The clause over-fires as originally written, and the correction is
normative.** A bare `0-1` is not one thing. It is three:

- **ratio with a real denominator** — satisfied by declaring that denominator
  as its population. No normalization function exists for it and none is to be
  invented.
- **synthetic score with no natural denominator** — what the clause was written
  for. A signal MUST declare a normalization function **only** if it is here.
- **fully determined** — the row names its own formula (HHI, Gini, Brier,
  Michelson modulation, lunar phase), so declaring the population determines
  the value and there is nothing left to normalize. Declares neither.

**The sort is encoded on every bare-`0-1` row** as `zero_one` in the domain
JSON — 524 rows catalogue-wide:

| domain | ratio | synthetic | determined | total |
|---|---|---|---|---|
| `information` | 158 | 22 | 15 | 195 |
| `soul` | 104 | 46 | 1 | 151 |
| `relational` | 55 | 25 | 0 | 80 |
| `world` | 37 | 10 | 2 | 49 |
| `body` | 22 | 8 | 0 | 30 |
| `time` | 10 | 9 | 0 | 19 |
| | **386** | **120** | **18** | **524** |

**`meta` carries no bare-`0-1` row and is absent from the table for that
reason** — every row in it is a time, a count, or a ratio whose two terms are
themselves real quantities, so none falls under this clause. The 524 stands
unchanged against a catalogue of 1,644. This is an outcome rather than a
policy, and the first coverage *fraction* in a later `meta` wave will be the
row that ends it.

The first measurement of this table (front matter §6, #96/#98) was file-level:
433 rows, 339 · 77 · 17, with `soul`'s 73 legacy rows and `body`'s 18 named as
owed. **The #108 merge landed both.** `body`'s 18 split 11 · 7 · 0 as the
domain file's own conventions state. `soul`'s 73 split **36 · 36 · 1**,
applied under the three criteria above and emitted for review — the legacy
rows run far more
synthetic than the re-authored rows, because the v1.0.x sections are rubric
scores where the re-authored rows are event rates. Reversible pre-tag; a
flipped row is a one-field JSON edit.

---

## 7 · Aliases — #79's rule, #86's four sets, and the table

Confirmed clause, verbatim:

> a Risk Factor aggregation MUST NOT include more than one ID from an alias set

**The rule is normative and in force.** The sets it governs are declared in
`index.json` under `alias_sets` — sixteen, in two shapes:

- **duplicate** (12, from `NORMALIZATION-01` §A): a true duplicate with one
  canonical home; the aliases exist for sensor provenance. Unit actions
  applied under §G, 2026-08-11.
- **collision** (4, from **#86**, ruled 2026-08-13): *alias, not merge* —
  both rows are legitimate, non-redundant measurements of **different
  subjects** that share an observation-collision hazard. **No canonical**:
  forcing a canonical/alias split would misstate three of the four as
  preferred/demoted pairs, which is the opposite of what #86 ruled.

Under either shape, **a deployment MUST declare which ID of each set it
populates**, in the deployment profile (`NORMALIZATION-01` §A, normative).
`business_hours_active` carries #86's own open flag: if declaring its subject
shows `world.cyclical`'s row is configuration rather than observation, it
drops out of the catalogue and the set dissolves — not decided here.

**The alias table's retirement is not in force.** #79 ruled the
hand-maintained table retires because alias sets are *derivable* from declared
subject and population — and its own Inference block records derivability as
**argued, not demonstrated**. The line holds: **retire the table on a
working derivation, not on the ruling.** #86 was the live test and was decided
on the merits rather than by derivation, so the debt stands. Until a
derivation reproduces the sixteen sets from declared subject and population
alone — or is ruled impossible, in which case the table *is* the mechanism —
`alias_sets` in `index.json` is the table, and it is hand-maintained.

**Flagged, not ruled:** `information.integrity.packet_loss_rate` is an
undeclared third member of the packet-loss set (`NORMALIZATION-01` §F). It is
carried as a note on that set, not as a membership.

---

## 8 · What is not here, and who owns it

Clauses that would belong in this file if they were ruled. They are not, and
writing them here would rule them by authorship.

| | owner | state |
|---|---|---|
| **The `[P]` privacy rule** — never stated; applied by feel; the mark is transcribed as `p` in the JSON | **#67** | open, `grilling` |
| **PROJECTED as a sixth observation class** (§4) | **#73**, **#74** | open, `grilling` |
| **Statistical modifier grammar** — two conventions split by domain, 54 rows | **#91** | open, `v2.1` |
| **The reference label-set identifier** and whether it becomes a registry (§5) | **#68** *What this opens* | left open on purpose |
| **Whether `Identifier repairs` is required of every domain file** (§2) | **#69** *What this opens* | left open on purpose |
| **The retention floor** for the envelope's log (§3) | **#72** *What this opens* | a number nobody has chosen |
| **`information`'s covert-inference prohibition** — a real normative clause that is not in §3's envelope and may be the `[P]` rule under another name. Preserved verbatim and unapplied in that file | **#96** → **#67** | raised, unowned |
| **The A/P boundary where it depends on the deployment** (§4) — `information.platform`'s moderation counts are **A** read live from an API and **P** read from a quarterly transparency report, and then publication lag becomes MUST. The catalogue cannot decide it and the row cannot carry it | adjacent to **#72** | named, unowned |
| **The alias derivation** (§7) — reproduce the sixteen alias sets from declared subject and population alone, or rule it impossible | **#86** open item 2 | design work, unticketed |
| **`soul`'s legacy split review** (§6) — 73 rows classified by the merge, 36 · 36 · 1 | **#108** | applied, reviewable, reversible pre-tag |
| **`meta` waves 2 and 3** — coverage and staleness, then tamper and cross-sensor disagreement. Wave 1 (`refresh`) landed; the rest are unauthored and the boundary between them is stated in `catalog/meta.md` | **tracker#18** | ruled, sequenced, not yet authored |
| **Who measures `meta`'s own coverage** — the regress terminates at a declared attestation root or not at all. Wave 1 does not reach it; wave 2 does | **tracker#18** *What this opens* | named, unowned |

**Closed since the front matter was written:** *bringing the other five domain
files to the `world` form* — **#96**, applied 2026-08-12. *The general
missing-data rule* — **#60**, ruled into §4 as its sixth clause, 2026-08-13.
*The alias declaration shape and site* — **#101/#106**, closed into **#108**,
which built `index.json`'s two-shape encoding and the deployment profile's
declaration slot. *Encoding the three-way `0-1` split as a schema field* —
built by **#108** as `zero_one` (§6), which makes map #46 success criterion 3
script-checkable for this clause.

**No *clause* in this file changes a row count.** Every rule above is a
declaration obligation, and none of them adds or removes a signal.

**A ruling did.** **tracker#18** adopted the `meta` domain and its first wave
landed 17 signals: **1,627 → 1,644, six domains → seven.** #58's freeze was
never a bar on adopting a domain — it fixed a headline that had not been
derived from its parts, and the correction that made 1,627 true is the same
discipline that makes 1,644 true. Both numbers are re-derived mechanically from
`catalog/*.json` on every run of `scripts/gen-catalog-tables.py`, and the
class census closes exactly on all seven domains.
