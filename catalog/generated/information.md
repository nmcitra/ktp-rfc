<!-- GENERATED from catalog/information.json by scripts/gen-catalog-tables.py. Do not edit. -->

### Attention Currents — `information.attention` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.attention.active_audience` | Active audience | int | 0-inf | N | [P] |
| `information.attention.impression_rate` | Impression rate | float | 0-inf impressions/s | N | [P] |
| `information.attention.engagement_rate` | Engagement share | float | 0-1 | N | [P] |
| `information.attention.topic_hhi` | Topic concentration | float | 0-1 | N | [P] determined |
| `information.attention.topic_entropy` | Topic diversity | float | 0-inf bits | N | [P] |
| `information.attention.top_topic_share` | Leading-topic share | float | 0-1 | N | [P] |
| `information.attention.top_source_share` | Leading-source attention | float | 0-1 | N | [P] |
| `information.attention.trend_velocity` | Trend share velocity | float | -1-1 share/h | N | [P] |
| `information.attention.trend_acceleration` | Trend share acceleration | float | -2-2 share/h^2 | N | [P] |
| `information.attention.trend_half_life` | Trend half-life | duration | 0-inf s | N | [P] |
| `information.attention.novelty_share` | Novel-topic share | float | 0-1 | N | [P] |
| `information.attention.mean_repeat_exposure` | Mean repeat exposure | float | 0-inf exposures/person | N | [P] |
| `information.attention.exposure_gini` | Exposure inequality | float | 0-1 | N | [P] determined |
| `information.attention.mean_dwell_time` | Mean dwell time | duration | 0-inf s | N | [P] |
| `information.attention.p95_dwell_time` | P95 dwell time | duration | 0-inf s | N | [P] |
| `information.attention.focus_switch_rate` | Focus-switch rate | float | 0-inf switches/min | N | [P] |
| `information.attention.median_scroll_speed` | Median scroll speed | float | 0-inf viewports/s | N | [P] |
| `information.attention.completion_rate` | Content completion | float | 0-1 | N | [P] |
| `information.attention.search_share` | Search-led attention | float | 0-1 | N | [P] |
| `information.attention.recommendation_share` | Recommendation-led attention | float | 0-1 | N | [P] |
| `information.attention.notification_share` | Notification-led attention | float | 0-1 | N | [P] |
| `information.attention.cross_platform_overlap` | Cross-platform overlap | float | 0-1 | N | [P] |
| `information.attention.region_entropy` | Audience-region diversity | float | 0-inf bits | N | [P] |
| `information.attention.time_to_threshold` | Time to trend threshold | duration | 0-inf s | N | [P] |

### Narrative Currents — `information.narrative` (28 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.narrative.cluster_count` | Narrative cluster count | int | 0-inf | N | [P] |
| `information.narrative.dominant_share` | Dominant narrative share | float | 0-1 | N | [P] |
| `information.narrative.counter_share` | Counter-narrative share | float | 0-1 | N | [P] |
| `information.narrative.cluster_hhi` | Narrative concentration | float | 0-1 | N | [P] determined |
| `information.narrative.cluster_entropy` | Narrative diversity | float | 0-inf bits | N | [P] |
| `information.narrative.cluster_silhouette` | Cluster separation | float | -1-1 | N | [P] |
| `information.narrative.internal_coherence` | Within-narrative coherence | float | 0-1 | N | [P] synthetic |
| `information.narrative.mean_intercluster_distance` | Mean intercluster distance | float | 0-2 cosine distance | N | [P] |
| `information.narrative.emergence_rate` | Narrative emergence | float | 0-inf narratives/day | N | [P] |
| `information.narrative.retirement_rate` | Narrative retirement | float | 0-inf narratives/day | N | [P] |
| `information.narrative.narrative_half_life` | Narrative half-life | duration | 0-inf s | N | [P] |
| `information.narrative.semantic_drift` | Semantic drift | float | 0-2 cosine distance/day | N | [P] |
| `information.narrative.variant_branching` | Variant branching | float | 0-inf variants/narrative | N | [P] |
| `information.narrative.claim_reuse` | Claim reuse share | float | 0-1 | N | [P] |
| `information.narrative.phrase_reuse` | Phrase reuse share | float | 0-1 | N | [P] |
| `information.narrative.frame_entropy` | Framing diversity | float | 0-inf bits | N | [P] |
| `information.narrative.causal_frame_share` | Causal-frame share | float | 0-1 | N | [P] |
| `information.narrative.moral_frame_share` | Moral-frame share | float | 0-1 | N | [P] |
| `information.narrative.identity_frame_share` | Identity-frame share | float | 0-1 | N | [P] |
| `information.narrative.threat_frame_share` | Threat-frame share | float | 0-1 | N | [P] |
| `information.narrative.solution_frame_share` | Solution-frame share | float | 0-1 | N | [P] |
| `information.narrative.blame_hhi` | Blame-target concentration | float | 0-1 | N | [P] determined |
| `information.narrative.actor_role_stability` | Actor-role stability | float | 0-1 | N | [P] synthetic |
| `information.narrative.cross_language_alignment` | Cross-language alignment | float | 0-1 | N | [P] synthetic |
| `information.narrative.cross_platform_alignment` | Cross-platform alignment | float | 0-1 | N | [P] synthetic |
| `information.narrative.counter_latency` | Counter-narrative latency | duration | 0-inf s | N | [P] |
| `information.narrative.bridge_share` | Bridge-narrative share | float | 0-1 | N | [P] |
| `information.narrative.action_divergence` | Proposed-action divergence | float | 0-2 cosine distance | N | [P] |

### Source Ecosystem — `information.source` (26 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.source.active_source_count` | Active source count | int | 0-inf | N |   |
| `information.source.entry_rate` | Source entry rate | float | 0-inf sources/day | N |   |
| `information.source.exit_rate` | Source exit rate | float | 0-inf sources/day | N |   |
| `information.source.output_hhi` | Source-output concentration | float | 0-1 | N | determined |
| `information.source.ownership_hhi` | Ownership concentration | float | 0-1 | N | determined |
| `information.source.funding_hhi` | Funding concentration | float | 0-1 | N | determined |
| `information.source.upstream_feed_hhi` | Upstream-feed concentration | float | 0-1 | N | determined |
| `information.source.type_entropy` | Source-type diversity | float | 0-inf bits | N |   |
| `information.source.region_entropy` | Source-region diversity | float | 0-inf bits | N |   |
| `information.source.language_entropy` | Source-language diversity | float | 0-inf bits | N |   |
| `information.source.jurisdiction_entropy` | Jurisdiction diversity | float | 0-inf bits | N |   |
| `information.source.ownership_independent_share` | Ownership-independent share | float | 0-1 | N |   |
| `information.source.local_share` | Local-source share | float | 0-1 | N |   |
| `information.source.state_controlled_share` | State-controlled share | float | 0-1 | N |   |
| `information.source.anonymous_origin_share` | Anonymous-origin share | float | 0-1 | N | [P] |
| `information.source.credentialed_share` | Credentialed-source share | float | 0-1 | N | [P] |
| `information.source.adjudicated_accuracy` | Adjudicated source accuracy | float | 0-1 | A | [P] |
| `information.source.ownership_disclosure_coverage` | Ownership-disclosure coverage | float | 0-1 | N |   |
| `information.source.funding_disclosure_coverage` | Funding-disclosure coverage | float | 0-1 | N |   |
| `information.source.conflict_disclosure_coverage` | Conflict-disclosure coverage | float | 0-1 | N |   |
| `information.source.editorial_policy_coverage` | Editorial-policy coverage | float | 0-1 | N |   |
| `information.source.syndication_share` | Syndicated-content share | float | 0-1 | N |   |
| `information.source.uptime` | Source availability | float | 0-1 | N |   |
| `information.source.open_access_share` | Open-access share | float | 0-1 | N |   |
| `information.source.machine_access_share` | Machine-accessible share | float | 0-1 | N |   |
| `information.source.contactability_coverage` | Public contact coverage | float | 0-1 | N |   |

### Amplification Patterns — `information.amplification` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.amplification.reshare_rate` | Reshare rate | float | 0-inf events/s | N | [P] |
| `information.amplification.unique_amplifiers` | Unique amplifiers | int | 0-inf | N | [P] |
| `information.amplification.impression_multiplier` | Impression multiplier | float | 0-inf ratio | N | [P] |
| `information.amplification.exposure_reproduction` | Exposure reproduction | float | 0-inf exposures/account | N | [P] |
| `information.amplification.cascade_depth` | Cascade depth | int | 0-inf | N | [P] |
| `information.amplification.cascade_width` | Cascade width | int | 0-inf | N | [P] |
| `information.amplification.branching_factor` | Cascade branching | float | 0-inf children/node | N | [P] |
| `information.amplification.time_to_peak` | Time to peak | duration | 0-inf s | N | [P] |
| `information.amplification.cascade_half_life` | Cascade half-life | duration | 0-inf s | N | [P] |
| `information.amplification.organic_share` | Organic amplification | float | 0-1 | N | [P] |
| `information.amplification.paid_share` | Paid amplification | float | 0-1 | N |   |
| `information.amplification.algorithmic_boost_share` | Algorithmic-boost share | float | 0-1 | N |   |
| `information.amplification.automated_share` | Automated amplification | float | 0-1 | N |   |
| `information.amplification.coordinated_share` | Coordinated amplification | float | 0-1 | N | [P] |
| `information.amplification.influencer_share` | Influencer amplification | float | 0-1 | N | [P] |
| `information.amplification.amplifier_hhi` | Amplifier concentration | float | 0-1 | N | [P] determined |
| `information.amplification.platform_jump_rate` | Cross-platform jumps | float | 0-inf jumps/h | N | [P] |
| `information.amplification.platform_jump_latency` | Cross-platform latency | duration | 0-inf s | N | [P] |
| `information.amplification.duplicate_share` | Duplicate-post share | float | 0-1 | N | [P] |
| `information.amplification.synchronized_share` | Synchronized-post share | float | 0-1 | N | [P] |
| `information.amplification.interarrival_cv` | Amplification burstiness | float | 0-inf CV | N | [P] |
| `information.amplification.hop_velocity` | Propagation velocity | float | 0-inf hops/h | N | [P] |
| `information.amplification.boost_action_rate` | Platform boost rate | float | 0-inf actions/s | N |   |
| `information.amplification.downrank_action_rate` | Platform downrank rate | float | 0-inf actions/s | N |   |

### Synthetic Content — `information.synthetic` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.synthetic.generated_text_share` | Generated-text share | float | 0-1 | N |   |
| `information.synthetic.generated_image_share` | Generated-image share | float | 0-1 | N |   |
| `information.synthetic.generated_audio_share` | Generated-audio share | float | 0-1 | N |   |
| `information.synthetic.generated_video_share` | Generated-video share | float | 0-1 | N |   |
| `information.synthetic.generated_code_share` | Generated-code share | float | 0-1 | N |   |
| `information.synthetic.cloned_voice_share` | Cloned-voice share | float | 0-1 | N | [P] |
| `information.synthetic.face_swap_share` | Face-swap share | float | 0-1 | N | [P] |
| `information.synthetic.synthetic_avatar_share` | Synthetic-avatar share | float | 0-1 | N | [P] |
| `information.synthetic.synthetic_account_share` | Synthetic-account share | float | 0-1 | N | [P] |
| `information.synthetic.autonomous_post_share` | Autonomous-post share | float | 0-1 | N | [P] |
| `information.synthetic.disclosed_generation_share` | Generation-disclosed share | float | 0-1 | N |   |
| `information.synthetic.hybrid_content_share` | Hybrid human-AI share | float | 0-1 | N | [P] |
| `information.synthetic.watermarked_media_share` | Provenance-watermarked share | float | 0-1 | N |   |
| `information.synthetic.generator_family_count` | Generator family count | int | 0-inf | N |   |
| `information.synthetic.generator_hhi` | Generator concentration | float | 0-1 | N | determined |
| `information.synthetic.attribution_success` | Generator-attribution success | float | 0-1 | N |   |
| `information.synthetic.detection_confidence` | Mean detection confidence | float | 0-1 | N | synthetic |
| `information.synthetic.detector_disagreement` | Detector disagreement | float | 0-1 | N |   |
| `information.synthetic.modality_mismatch_rate` | Cross-modal mismatch | float | 0-1 | N |   |
| `information.synthetic.temporal_artifact_rate` | Temporal artifacts | float | 0-inf artifacts/1k frames | N |   |
| `information.synthetic.biometric_mismatch_rate` | Biometric mismatch | float | 0-1 | N | [P] |
| `information.synthetic.template_reuse_rate` | Template-reuse share | float | 0-1 | N |   |

### Truth Conditions — `information.truth` (28 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.truth.verification_success` | Claim verification success | float | 0-1 | N |   |
| `information.truth.fact_check_coverage` | Fact-check coverage | float | 0-1 | N |   |
| `information.truth.fact_check_agreement` | Fact-check verdict agreement | float | 0-1 | A | [P] |
| `information.truth.misinformation_volume` | Misinformation volume | float | 0-inf items/s | N |   |
| `information.truth.misinformation_velocity` | Misinformation spread | float | 0-inf exposures/s | N |   |
| `information.truth.disinformation_volume` | Disinformation volume | float | 0-inf items/s | N |   |
| `information.truth.disinformation_sophistication` | Disinformation sophistication | float | 0-1 | N | synthetic |
| `information.truth.epistemic_pollution` | Polluted-exposure share | float | 0-1 | N |   |
| `information.truth.uncertainty_acknowledged` | Uncertainty-disclosure share | float | 0-1 | N |   |
| `information.truth.overconfidence_rate` | Overconfidence share | float | 0-1 | N | [P] |
| `information.truth.citation_rate` | Citation density | float | 0-inf citations/claim | N |   |
| `information.truth.citation_quality` | Citation quality | float | 0-1 | N | synthetic |
| `information.truth.primary_source_usage` | Primary-source use | float | 0-1 | N |   |
| `information.truth.rumor_prevalence` | Rumor prevalence | float | 0-1 | N | [P] |
| `information.truth.correction_rate` | Identified-error correction | float | 0-1 | A |   |
| `information.truth.correction_reach` | Correction reach | float | 0-1 | N | [P] |
| `information.truth.retraction_rate` | Retraction share | float | 0-1 | A |   |
| `information.truth.consensus_level` | Consensus-backed claims | float | 0-1 | A | [P] |
| `information.truth.contested_claim_rate` | Contested-claim share | float | 0-1 | N | [P] |
| `information.truth.expert_agreement` | Mean expert agreement | float | 0-1 | A | [P] |
| `information.truth.mean_evidence_quality` | Mean evidence quality | float | 0-1 | N | synthetic |
| `information.truth.logical_consistency` | Logical consistency | float | 0-1 | N |   |
| `information.truth.contradiction_rate` | Contradiction share | float | 0-1 | N |   |
| `information.truth.nuance_preservation` | Nuance retention | float | 0-1 | N | synthetic |
| `information.truth.false_balance` | False-balance share | float | 0-1 | N |   |
| `information.truth.context_preservation` | Context retention | float | 0-1 | N | synthetic |
| `information.truth.manipulation_resistance` | Manipulation test pass rate | float | 0-1 | N |   |
| `information.truth.replication_success` | Independent replication success | float | 0-1 | N |   |

### Emotional Weather — `information.emotion` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.emotion.anger_expression_share` | Anger-expression share | float | 0-1 | N | [P] |
| `information.emotion.fear_expression_share` | Fear-expression share | float | 0-1 | N | [P] |
| `information.emotion.hope_expression_share` | Hope-expression share | float | 0-1 | N | [P] |
| `information.emotion.sadness_expression_share` | Sadness-expression share | float | 0-1 | N | [P] |
| `information.emotion.joy_expression_share` | Joy-expression share | float | 0-1 | N | [P] |
| `information.emotion.disgust_expression_share` | Disgust-expression share | float | 0-1 | N | [P] |
| `information.emotion.anxiety_expression_share` | Anxiety-expression share | float | 0-1 | N | [P] |
| `information.emotion.exhaustion_expression_share` | Exhaustion-expression share | float | 0-1 | N | [P] |
| `information.emotion.grief_expression_share` | Grief-expression share | float | 0-1 | N | [P] |
| `information.emotion.compassion_expression_share` | Compassion-expression share | float | 0-1 | N | [P] |
| `information.emotion.shame_expression_share` | Shame-expression share | float | 0-1 | N | [P] |
| `information.emotion.contempt_expression_share` | Contempt-expression share | float | 0-1 | N | [P] |
| `information.emotion.mean_expressed_valence` | Mean expressed valence | float | -1-1 | N | [P] |
| `information.emotion.mean_expressed_arousal` | Mean expressed arousal | float | 0-1 | N | [P] synthetic |
| `information.emotion.valence_volatility` | Valence volatility | float | 0-1 SD | N | [P] |
| `information.emotion.post_exposure_valence_shift` | Post-exposure valence shift | float | -2-2 score | N | [P] |
| `information.emotion.arousal_increase_share` | Arousal-increase share | float | 0-1 | N | [P] |
| `information.emotion.median_recovery_time` | Median emotional recovery | duration | 0-inf s | N | [P] |
| `information.emotion.p95_negative_streak` | P95 negative-expression streak | duration | 0-inf s | N | [P] |
| `information.emotion.reaction_incongruence` | Incongruent-reaction share | float | 0-1 | N | [P] |
| `information.emotion.toxicity_share` | Toxic-content share | float | 0-1 | N | [P] |
| `information.emotion.threat_language_density` | Threat-language density | float | 0-inf occurrences/1k tokens | N | [P] |
| `information.emotion.support_language_density` | Support-language density | float | 0-inf occurrences/1k tokens | N | [P] |
| `information.emotion.emotion_entropy` | Emotion diversity | float | 0-inf bits | N | [P] |

### Tribal Dynamics — `information.tribal` (20 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.tribal.community_count` | Detected communities | int | 0-inf | N | [P] |
| `information.tribal.network_modularity` | Network modularity | float | -1-1 | N | [P] |
| `information.tribal.identity_assortativity` | Identity assortativity | float | -1-1 | N | [P] |
| `information.tribal.echo_chamber_share` | Echo-chamber share | float | 0-1 | N | [P] |
| `information.tribal.cross_group_edge_share` | Cross-group edges | float | 0-1 | N | [P] |
| `information.tribal.cross_group_reply_share` | Cross-group replies | float | 0-1 | N | [P] |
| `information.tribal.cross_cutting_exposure` | Cross-cutting exposure | float | 0-1 | N | [P] |
| `information.tribal.bridge_account_share` | Bridge-account share | float | 0-1 | N | [P] |
| `information.tribal.bridge_edge_share` | Bridge-edge share | float | 0-1 | N | [P] |
| `information.tribal.within_group_similarity` | Within-group similarity | float | 0-1 | N | [P] synthetic |
| `information.tribal.between_group_distance` | Between-group distance | float | 0-2 cosine distance | N | [P] |
| `information.tribal.group_size_gini` | Group-size inequality | float | 0-1 | N | [P] determined |
| `information.tribal.identity_term_density` | Identity-term density | float | 0-inf occurrences/1k tokens | N | [P] |
| `information.tribal.outgroup_mention_density` | Out-group mentions | float | 0-inf occurrences/1k tokens | N | [P] |
| `information.tribal.dehumanization_share` | Dehumanizing-content share | float | 0-1 | N | [P] |
| `information.tribal.loyalty_signal_share` | Loyalty-signal share | float | 0-1 | N | [P] |
| `information.tribal.boundary_policing_share` | Boundary-policing share | float | 0-1 | N | [P] |
| `information.tribal.defection_penalty_share` | Defection-penalty share | float | 0-1 | N | [P] |
| `information.tribal.group_switch_rate` | Group-switch rate | float | 0-inf transitions/1k accounts/day | N | [P] |
| `information.tribal.intergroup_hostility` | Intergroup hostility | float | 0-1 | N | [P] synthetic |

### Platform Dynamics — `information.platform` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.platform.active_platform_count` | Active platform count | int | 0-inf | N |   |
| `information.platform.audience_hhi` | Audience concentration | float | 0-1 | N | [P] determined |
| `information.platform.traffic_hhi` | Traffic concentration | float | 0-1 | N | determined |
| `information.platform.top_platform_share` | Leading-platform audience | float | 0-1 | N | [P] |
| `information.platform.switch_rate` | Platform-switch rate | float | 0-inf transitions/1k users/day | N | [P] |
| `information.platform.cross_post_share` | Cross-posting share | float | 0-1 | N | [P] |
| `information.platform.api_uptime` | API availability | float | 0-1 | N |   |
| `information.platform.api_latency` | API latency | duration | 0-inf s | N |   |
| `information.platform.api_error_rate` | API error share | float | 0-1 | N |   |
| `information.platform.moderation_action_rate` | Moderation action rate | float | 0-inf actions/s | A | [P] |
| `information.platform.moderation_reversal_rate` | Moderation reversal share | float | 0-1 | A | [P] |
| `information.platform.appeal_latency` | Appeal latency | duration | 0-inf s | A | [P] |
| `information.platform.policy_change_rate` | Policy change rate | float | 0-inf changes/day | A |   |
| `information.platform.policy_notice_lead_time` | Policy notice lead time | duration | 0-inf s | A |   |
| `information.platform.ranking_change_rate` | Ranking-system change rate | float | 0-inf changes/day | A |   |
| `information.platform.personalization_features` | Personalization inputs | int | 0-inf | A | [P] |
| `information.platform.portability_success` | Portability success share | float | 0-1 | N |   |
| `information.platform.enforcement_consistency` | Enforcement consistency | float | 0-1 | A | [P] synthetic |

### Information Operations — `information.info_ops` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.info_ops.active_campaign_count` | Active campaign count | int | 0-inf | N |   |
| `information.info_ops.attributed_actor_count` | Attributed actor count | int | 0-inf | A |   |
| `information.info_ops.state_linked_share` | State-linked campaign share | float | 0-1 | A |   |
| `information.info_ops.coordinated_account_count` | Coordinated accounts | int | 0-inf | N | [P] |
| `information.info_ops.coordinated_cluster_count` | Coordinated clusters | int | 0-inf | N | [P] |
| `information.info_ops.campaign_output_rate` | Campaign output rate | float | 0-inf items/s | N |   |
| `information.info_ops.target_topic_count` | Targeted topic count | int | 0-inf | N |   |
| `information.info_ops.target_region_count` | Targeted region count | int | 0-inf | N | [P] |
| `information.info_ops.target_language_count` | Targeted language count | int | 0-inf | N | [P] |
| `information.info_ops.persona_reuse_rate` | Persona reuse | float | 0-1 | N | [P] |
| `information.info_ops.infrastructure_reuse` | Infrastructure reuse | float | 0-1 | N |   |
| `information.info_ops.registration_burst` | Domain-registration burst | float | 0-inf domains/h | N |   |
| `information.info_ops.timing_synchrony` | Posting synchrony | float | 0-1 | N | [P] synthetic |
| `information.info_ops.narrative_seeding_rate` | Narrative seeding rate | float | 0-inf narratives/day | N |   |
| `information.info_ops.propaganda_marker_density` | Propaganda-marker density | float | 0-inf occurrences/1k items | N | [P] |
| `information.info_ops.laundering_depth` | Information-laundering depth | int | 0-inf | N |   |
| `information.info_ops.attribution_confidence` | Attribution confidence | float | 0-1 | A | synthetic |
| `information.info_ops.reach_share` | Operation reach | float | 0-1 | N | [P] |
| `information.info_ops.engagement_share` | Operation engagement | float | 0-1 | N | [P] |
| `information.info_ops.takedown_latency` | Takedown latency | duration | 0-inf s | N |   |
| `information.info_ops.reconstitution_rate` | Asset reconstitution share | float | 0-1 | N |   |
| `information.info_ops.evasion_success_rate` | Countermeasure-evasion share | float | 0-1 | N |   |

### Temporal Patterns — `information.temporal` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.temporal.arrival_rate` | Content arrival rate | float | 0-inf items/s | N |   |
| `information.temporal.p95_arrival_gap` | P95 arrival gap | duration | 0-inf s | N |   |
| `information.temporal.arrival_burstiness` | Arrival burstiness | float | 0-inf CV | N |   |
| `information.temporal.diurnal_strength` | Diurnal periodicity | float | 0-1 | N | [P] synthetic |
| `information.temporal.weekly_strength` | Weekly periodicity | float | 0-1 | N | [P] synthetic |
| `information.temporal.event_publication_latency` | Event-publication latency | duration | 0-inf s | N |   |
| `information.temporal.publication_index_latency` | Publication-index latency | duration | 0-inf s | N |   |
| `information.temporal.median_update_interval` | Median content-update interval | duration | 0-inf s | N |   |
| `information.temporal.median_correction_latency` | Median correction latency | duration | 0-inf s | N |   |
| `information.temporal.median_retraction_latency` | Median retraction latency | duration | 0-inf s | N |   |
| `information.temporal.median_news_cycle_duration` | Median news-cycle duration | duration | 0-inf s | N | [P] |
| `information.temporal.median_recurrence_interval` | Median narrative recurrence | duration | 0-inf s | N | [P] |
| `information.temporal.resurfaced_share` | Resurfaced-content share | float | 0-1 | N | [P] |
| `information.temporal.historical_reference_density` | Historical-reference density | float | 0-inf references/1k items | N | [P] |
| `information.temporal.median_reference_lookback` | Median reference lookback | duration | 0-inf s | N | [P] |
| `information.temporal.archive_retrieval_success` | Archive retrieval success | float | 0-1 | N |   |
| `information.temporal.timestamp_anomaly_rate` | Timestamp anomaly share | float | 0-1 | N |   |
| `information.temporal.stale_content_share` | Stale-content share | float | 0-1 | N |   |

### Epistemic Infrastructure — `information.epistemic` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.epistemic.fact_checker_count` | Active fact-checkers | int | 0-inf | N | [P] |
| `information.epistemic.fact_check_rate` | Fact-check throughput | float | 0-inf checks/day | N |   |
| `information.epistemic.verification_backlog` | Verification backlog | int | 0-inf | N |   |
| `information.epistemic.verification_latency` | Verification latency | duration | 0-inf s | N |   |
| `information.epistemic.journalist_count` | Active journalists | int | 0-inf | N | [P] |
| `information.epistemic.expert_count` | Available experts | int | 0-inf | N | [P] |
| `information.epistemic.newsroom_count` | Active newsroom count | int | 0-inf | N |   |
| `information.epistemic.local_coverage` | Local-news coverage | float | 0-1 | N |   |
| `information.epistemic.investigative_capacity` | Investigative capacity | float | 0-inf staff-h/week | P | [P] |
| `information.epistemic.public_records_uptime` | Public-records uptime | float | 0-1 | N |   |
| `information.epistemic.public_records_latency` | Public-records latency | duration | 0-inf s | N |   |
| `information.epistemic.open_dataset_count` | Open dataset count | int | 0-inf | N |   |
| `information.epistemic.open_data_freshness` | Open-data age | duration | 0-inf s | N |   |
| `information.epistemic.search_index_coverage` | Search-index coverage | float | 0-1 | N |   |
| `information.epistemic.search_index_freshness` | Search-index age | duration | 0-inf s | N |   |
| `information.epistemic.search_result_entropy` | Search-result diversity | float | 0-inf bits | N |   |
| `information.epistemic.knowledge_graph_coverage` | Knowledge-graph coverage | float | 0-1 | N |   |
| `information.epistemic.library_archive_count` | Accessible archive count | int | 0-inf | N |   |
| `information.epistemic.archive_digitization_share` | Archive digitization | float | 0-1 | N |   |
| `information.epistemic.repository_uptime` | Research-repository uptime | float | 0-1 | N |   |
| `information.epistemic.peer_review_rate` | Peer-review throughput | float | 0-inf articles/day | P | [P] |
| `information.epistemic.retraction_registry_coverage` | Retraction-registry coverage | float | 0-1 | N |   |
| `information.epistemic.literacy_program_reach` | Media-literacy reach | float | 0-1 | P | [P] |
| `information.epistemic.commons_edit_rate` | Knowledge-commons edits | float | 0-inf edits/day | N | [P] |

### Sensemaking Capacity — `information.sensemaking` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.sensemaking.active_participants` | Active participants | int | 0-inf | N | [P] |
| `information.sensemaking.expertise_entropy` | Expertise diversity | float | 0-inf bits | N | [P] |
| `information.sensemaking.participation_gini` | Participation inequality | float | 0-1 | N | [P] determined |
| `information.sensemaking.transition_entropy` | Speaker-transition diversity | float | 0-inf bits | N | [P] |
| `information.sensemaking.question_answer_rate` | Question-answer rate | float | 0-1 | N | [P] |
| `information.sensemaking.counterargument_response` | Counterargument response rate | float | 0-1 | N | [P] |
| `information.sensemaking.dissent_visibility` | Dissent visibility | float | 0-1 | N | [P] |
| `information.sensemaking.stakeholder_coverage` | Stakeholder coverage | float | 0-1 | N | [P] |
| `information.sensemaking.argument_map_coverage` | Argument-map coverage | float | 0-1 | N | [P] |
| `information.sensemaking.synthesis_rate` | Synthesis output rate | float | 0-inf outputs/day | N | [P] |
| `information.sensemaking.synthesis_latency` | Synthesis latency | duration | 0-inf s | N | [P] |
| `information.sensemaking.unresolved_questions` | Unresolved questions | int | 0-inf | N | [P] |
| `information.sensemaking.calibration_error` | Confidence calibration error | float | 0-1 | N | [P] synthetic |
| `information.sensemaking.forecast_brier` | Forecast Brier score | float | 0-1 | N | [P] determined |
| `information.sensemaking.belief_update_rate` | Belief-update rate | float | 0-1 | N | [P] |
| `information.sensemaking.decision_reversal_rate` | Decision-reversal rate | float | 0-1 | N | [P] |
| `information.sensemaking.knowledge_gain` | Knowledge gain | float | -1-1 score | N | [P] |
| `information.sensemaking.completion_rate` | Deliberation completion | float | 0-1 | N | [P] |

### Signal Integrity — `information.integrity` (16 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.integrity.transport_encryption` | Transport-encrypted share | float | 0-1 | N |   |
| `information.integrity.end_to_end_encryption` | End-to-end encrypted share | float | 0-1 | N |   |
| `information.integrity.signature_validation` | Valid-signature share | float | 0-1 | N |   |
| `information.integrity.hash_mismatch_rate` | Hash mismatch share | float | 0-1 | N |   |
| `information.integrity.packet_loss_rate` | Packet loss | float | 0-1 | N |   |
| `information.integrity.message_loss_rate` | Message loss | float | 0-1 | N |   |
| `information.integrity.duplicate_rate` | Message duplication | float | 0-1 | N |   |
| `information.integrity.reordering_rate` | Message reordering | float | 0-1 | N |   |
| `information.integrity.delivery_latency` | Delivery latency | duration | 0-inf s | N |   |
| `information.integrity.delivery_jitter` | Delivery jitter | duration | 0-inf s | N |   |
| `information.integrity.alert_rate` | Integrity alert rate | float | 0-inf alerts/s | N |   |
| `information.integrity.censorship_probe_failure` | Censorship-probe failure share | float | 0-1 | N |   |
| `information.integrity.throughput_ratio` | Observed/control throughput | float | 0-inf ratio | N |   |
| `information.integrity.route_diversity` | Independent path count | int | 0-inf | N |   |
| `information.integrity.mirror_count` | Reachable mirror count | int | 0-inf | N |   |
| `information.integrity.tamper_evidence_coverage` | Tamper-evidence coverage | float | 0-1 | N |   |

### Collective Trauma — `information.trauma` (14 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.trauma.active_topic_count` | Active trauma topics | int | 0-inf | N | [P] |
| `information.trauma.content_share` | Trauma-content share | float | 0-1 | N | [P] |
| `information.trauma.graphic_content_share` | Graphic-content share | float | 0-1 | N | [P] |
| `information.trauma.trigger_marker_density` | Trigger-marker density | float | 0-inf occurrences/1k items | N | [P] |
| `information.trauma.exposed_audience_share` | Exposed audience share | float | 0-1 | N | [P] |
| `information.trauma.mean_repeat_exposure` | Mean repeated exposure | float | 0-inf exposures/person | N | [P] |
| `information.trauma.unconsented_exposure` | Unconsented exposure | float | 0-1 | N | [P] |
| `information.trauma.anniversary_resurgence` | Anniversary resurgence | float | 0-inf ratio | N | [P] |
| `information.trauma.retraumatization_reports` | Retraumatization reports | float | 0-inf reports/1k exposures | N | [P] |
| `information.trauma.warning_coverage` | Content-warning coverage | float | 0-1 | N | [P] |
| `information.trauma.support_resource_coverage` | Support-resource coverage | float | 0-1 | N | [P] |
| `information.trauma.survivor_voice_share` | Self-identified survivor voice | float | 0-1 | N | [P] |
| `information.trauma.restorative_content_share` | Restorative-content share | float | 0-1 | N | [P] |
| `information.trauma.signal_recovery_time` | Signal recovery time | duration | 0-inf s | N | [P] |

### Sacred & Meaning — `information.meaning` (10 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `information.meaning.purpose_clarity` | Purpose clarity | float | 0-1 | N | [P] synthetic |
| `information.meaning.meaning_self_report` | Experienced meaning | float | 0-1 | N | [P] synthetic |
| `information.meaning.authenticity_self_report` | Experienced authenticity | float | 0-1 | N | [P] synthetic |
| `information.meaning.purpose_consistency` | Purpose-action consistency | float | 0-1 | N | [P] |
| `information.meaning.sacred_reference_density` | Sacred-reference density | float | 0-inf occurrences/1k items | N | [P] |
| `information.meaning.awe_expression_density` | Awe-expression density | float | 0-inf occurrences/1k items | N | [P] |
| `information.meaning.beauty_response_rate` | Beauty-response share | float | 0-1 | N | [P] |
| `information.meaning.ritual_participation_rate` | Ritual participation rate | float | 0-inf events/1k people/day | N | [P] |
| `information.meaning.value_conflict_share` | Value-conflict share | float | 0-1 | N | [P] |
| `information.meaning.existential_distress_rate` | Existential-distress reports | float | 0-inf reports/1k people/day | N | [P] |

