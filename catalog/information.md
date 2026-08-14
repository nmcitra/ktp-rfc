# Context Signals — Information

The information environment the agent reads and acts in.

MEASUREMENT CONVENTIONS

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement
envelope (#79), §4 the five observation classes and what each class makes MUST
(#87), §5 label sets (#68), §6 ranges and normalization, §7 aliases. Nothing
in this section overrides any of them. The three declaration bullets this
section used to carry — population/corpus/platform-set/window, and model
identifier/version/threshold/sample-count for classifier-derived values — were
the front matter's §3 in a fourth wording and are withdrawn under
nmcitra/ktp-rfc#96.

What this section supplies is the binding: which observation class each
Information group takes, and which of its rows take a different one.

Group assignments. A group's class is the default for its rows; the named
exceptions take the class given. Three of the five classes are present —
N 316 · A 17 · P 3, totalling 336. There is no class D: Information observes
no physical quantity.

  attention      N   —
  narrative      N   —
  source         N   adjudicated_accuracy A
  amplification  N   —
  synthetic      N   —
  truth          N   fact_check_agreement, expert_agreement, consensus_level,
                     retraction_rate, correction_rate A
  emotion        N   —
  tribal         N   —
  platform       N   moderation_action_rate, moderation_reversal_rate,
                     appeal_latency, enforcement_consistency,
                     policy_change_rate, policy_notice_lead_time,
                     ranking_change_rate, personalization_features A
  info_ops       N   attributed_actor_count, state_linked_share,
                     attribution_confidence A
  temporal       N   —
  epistemic      N   investigative_capacity, literacy_program_reach,
                     peer_review_rate P
  sensemaking    N   —
  integrity      N   —
  trauma         N   —
  meaning        N   —

Information is not uniformly class N, and front matter §4's six-domain test
predicted that it was. Seventeen rows are class A and three are class P. The
seventeen are the rows that exist because somebody else adjudicated
something — a platform moderated, a fact-checker ruled, a publisher retracted,
an analyst attributed a campaign. The deployment reads a verdict it did not
make, and the A slots are the ones that say whose verdict, under which
criteria, at which version.

The A/P boundary in `platform` is a deployment fact, not a catalogue fact.
Moderation counts read live from a platform API are class A. The same numbers
taken from a quarterly transparency report are class P, and then the
publication lag is MUST and the platform's population MUST NOT be restated as
the deployment's own. A deployment declares which it did.

Class A's *unknown, not zero* clause is load-bearing throughout. Zero
moderation actions because the endpoint stopped answering is not an unmoderated
platform, and no attribution is not an absent actor.

Bare 0-1 ranges. One hundred and ninety-five Information signals carry a bare
0-1 — 58% of the domain, and the largest concentration in the catalogue. They
split three ways.

  158  ratios with a real denominator. Satisfied by declaring that
       denominator as their population; no normalization function exists for
       them and none is to be invented. Every `_share`, every `_coverage`,
       every `_rate` computed over the declared corpus is here.

   15  fully determined. HHI, Gini and Brier name their own formula, so once
       the distribution's population is declared the value follows and there
       is nothing left to normalize: attention.topic_hhi,
       attention.exposure_gini, narrative.cluster_hhi, narrative.blame_hhi,
       source.output_hhi, source.ownership_hhi, source.funding_hhi,
       source.upstream_feed_hhi, amplification.amplifier_hhi,
       synthetic.generator_hhi, tribal.group_size_gini,
       platform.audience_hhi, platform.traffic_hhi,
       sensemaking.participation_gini, sensemaking.forecast_brier.

   22  synthetic scores with no natural denominator, which MUST declare a
       normalization function in the deployment profile:
       narrative.internal_coherence, narrative.actor_role_stability,
       narrative.cross_language_alignment, narrative.cross_platform_alignment,
       synthetic.detection_confidence, truth.disinformation_sophistication,
       truth.citation_quality, truth.mean_evidence_quality,
       truth.nuance_preservation, truth.context_preservation,
       emotion.mean_expressed_arousal, tribal.within_group_similarity,
       tribal.intergroup_hostility, platform.enforcement_consistency,
       info_ops.timing_synchrony, info_ops.attribution_confidence,
       temporal.diurnal_strength, temporal.weekly_strength,
       sensemaking.calibration_error, meaning.purpose_clarity,
       meaning.meaning_self_report, meaning.authenticity_self_report.

Eighty-one per cent of Information's bare `0-1` rows are ratios, which is the
reverse of what front matter §6 predicts for this domain. The prediction was
made from the subject matter — content and behaviour, therefore synthetic. The
rows say otherwise: a content measure is almost always a share of a corpus,
and a share of a declared corpus has a denominator.

One of this section's original five bullets is kept, because it is not a
declaration rule and it is what makes those fifteen rows determinate: **HHI,
Gini, entropy, cosine-distance, coefficient-of-variation and Brier values use
the formula named in the Name or Range column.**

Where a ratio's denominator is gated by a predicate — organic, coordinated,
credentialed, state-controlled, synthetic, toxic, graphic, contested — the
predicate is a label set and is declared under the catalogue-wide label-set
rule, not here. Information is where that rule bites hardest: ninety-five of
its bare `0-1` rows are named `_share` or `_coverage`, and every one of them
names a category whose membership has to be declared before the numerator
means anything. The twelve emotion-expression shares depend on a declared
emotion label set whose reference identifier is still open under
nmcitra/ktp-rfc#68.

Privacy. Two hundred and six Information signals carry the [P] mark — more than
the rest of the catalogue combined, and 61% of this domain. This file once
carried the catalogue's only written [P] paragraph: "It does not authorize
collection. Consent, minimization, aggregation, sovereignty, and retention
controls remain mandatory." That wording was authored here rather than ruled
anywhere, and it is withdrawn to nmcitra/ktp-rfc#67 as evidence rather than kept
as a sixth wording. Nothing in this section authorizes, restricts or interprets
the mark.

The covert-inference prohibition. This file once carried a clause that is
preserved here verbatim and unapplied:

> Emotional, trauma, and meaning self-report rows MUST NOT be populated by
> covert inference of an individual's private mental state.

It is a real normative clause, it sits outside the measurement envelope in
`catalog/index.md` §3, and it is not obviously Information-only.
nmcitra/ktp-rfc#67 owns whether it is a catalogue-wide rule or the [P] rule
under another name. #96 raised it without ruling it.


## Signals

The tables below are generated from the canonical JSON (`catalog/information.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/information.md"
