<!-- GENERATED from catalog/relational.json by scripts/gen-catalog-tables.py. Do not edit. -->

### The Va (Space Between) — `relational.va` (28 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.va.relationship_type` | Relationship type | enum | — | S |   |
| `relational.va.history_length` | Relationship age | duration | 0-inf s | N |   |
| `relational.va.interaction_rate` | Interaction rate | float | 0-inf events/s | N |   |
| `relational.va.interaction_recency` | Interaction recency | duration | 0-inf s | N |   |
| `relational.va.clarity` | Mutual clarity | float | 0-1 | N | synthetic |
| `relational.va.temperature` | Relational temperature | float | -1-1 | N | [P] |
| `relational.va.trust_level` | Mutual trust | float | 0-1 | N | synthetic |
| `relational.va.reciprocity_balance` | Reciprocity balance | float | -1-1 | N |   |
| `relational.va.repair_needed` | Repair required | bool | — | N |   |
| `relational.va.repair_in_progress` | Repair active | bool | — | N |   |
| `relational.va.ceremony_recency` | Ceremony recency | duration | 0-inf s | N |   |
| `relational.va.conflict_active` | Conflict active | bool | — | N |   |
| `relational.va.conflict_count` | Conflict count | int | 0-inf | N |   |
| `relational.va.resolution_rate` | Conflict resolution rate | float | 0-1 | N |   |
| `relational.va.boundary_clarity` | Boundary clarity | float | 0-1 | N | synthetic |
| `relational.va.boundary_respect` | Boundary respect | float | 0-1 | N |   |
| `relational.va.vulnerability_exchange` | Vulnerability exchange | float | 0-1 | N | [P] synthetic |
| `relational.va.support_given_rate` | Support given rate | float | 0-inf events/s | N |   |
| `relational.va.support_received_rate` | Support received rate | float | 0-inf events/s | N |   |
| `relational.va.presence_quality` | Presence quality | float | 0-1 | N | synthetic |
| `relational.va.witnessed` | Relationship witnessed | bool | — | A |   |
| `relational.va.growth_gain` | Joint growth gain | float | -1-1 | N |   |
| `relational.va.drift_rate` | Relational drift rate | float | 0-inf 1/s | N |   |
| `relational.va.gratitude_given_rate` | Gratitude given | float | 0-inf events/s | N | [P] |
| `relational.va.gratitude_received_rate` | Gratitude received | float | 0-inf events/s | N | [P] |
| `relational.va.shared_joy_rate` | Shared joy rate | float | 0-inf events/s | N | [P] |
| `relational.va.shared_grief_rate` | Shared grief rate | float | 0-inf events/s | N | [P] |
| `relational.va.meaning_overlap` | Shared-meaning overlap | float | 0-1 | N | [P] synthetic |

### Connection Topology — `relational.topology` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.topology.peer_count` | Direct peer count | int | 0-inf | N |   |
| `relational.topology.inbound_degree` | Inbound degree | int | 0-inf | N |   |
| `relational.topology.outbound_degree` | Outbound degree | int | 0-inf | N |   |
| `relational.topology.weighted_degree` | Weighted degree | float | 0-inf | N |   |
| `relational.topology.component_size` | Component size | int | 0-inf | N |   |
| `relational.topology.ego_component_count` | Ego component count | int | 0-inf | N |   |
| `relational.topology.root_path_length` | Root path length | int | 0-inf hops | N |   |
| `relational.topology.mean_peer_distance` | Mean peer distance | float | 0-inf hops | N |   |
| `relational.topology.betweenness` | Betweenness centrality | float | 0-1 | N |   |
| `relational.topology.closeness` | Closeness centrality | float | 0-1 | N |   |
| `relational.topology.eigenvector` | Eigenvector centrality | float | 0-1 | N |   |
| `relational.topology.pagerank` | PageRank score | float | 0-1 | N |   |
| `relational.topology.clustering` | Clustering coefficient | float | 0-1 | N |   |
| `relational.topology.bridge_count` | Bridge edge count | int | 0-inf | N |   |
| `relational.topology.articulation_point` | Articulation point | bool | — | N |   |
| `relational.topology.neighbor_density` | Neighbor edge density | float | 0-1 | N |   |
| `relational.topology.degree_correlation` | Neighbor degree correlation | float | -1-1 | N |   |
| `relational.topology.edge_reciprocity` | Directed edge reciprocity | float | 0-1 | N |   |
| `relational.topology.edge_churn_rate` | Edge churn rate | float | 0-inf edges/s | N |   |
| `relational.topology.isolation_duration` | Isolation duration | duration | 0-inf s | N |   |
| `relational.topology.single_path_risk` | Single-path dependency | bool | — | N |   |
| `relational.topology.snapshot_age` | Topology snapshot age | duration | 0-inf s | N |   |

### Trust Flow — `relational.trust` (26 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.trust.outbound_mean` | Mean trust given | float | 0-1 | N | synthetic |
| `relational.trust.inbound_mean` | Mean trust received | float | 0-1 | N | synthetic |
| `relational.trust.outbound_minimum` | Minimum trust given | float | 0-1 | N | synthetic |
| `relational.trust.inbound_minimum` | Minimum trust received | float | 0-1 | N | synthetic |
| `relational.trust.outbound_variance` | Trust-given variance | float | 0-0.25 | N |   |
| `relational.trust.inbound_variance` | Trust-received variance | float | 0-0.25 | N |   |
| `relational.trust.net_balance` | Net trust balance | float | -1-1 | N |   |
| `relational.trust.asymmetry` | Trust asymmetry | float | 0-1 | N | synthetic |
| `relational.trust.outbound_velocity` | Trust-given velocity | float | -inf-inf 1/s | N |   |
| `relational.trust.inbound_velocity` | Trust-received velocity | float | -inf-inf 1/s | N |   |
| `relational.trust.grant_rate` | Trust grant rate | float | 0-inf events/s | N |   |
| `relational.trust.revocation_rate` | Trust revocation rate | float | 0-inf events/s | N |   |
| `relational.trust.decay_half_life` | Trust decay half-life | duration | 0-inf s | N |   |
| `relational.trust.edge_age_mean` | Mean trust-edge age | duration | 0-inf s | N |   |
| `relational.trust.trusted_edge_count` | Trusted edge count | int | 0-inf | N |   |
| `relational.trust.distrust_edge_count` | Distrust edge count | int | 0-inf | N |   |
| `relational.trust.dormant_edge_count` | Dormant trust-edge count | int | 0-inf | N |   |
| `relational.trust.chain_length` | Trust chain length | int | 0-inf hops | N |   |
| `relational.trust.chain_minimum` | Trust chain minimum | float | 0-1 | N | synthetic |
| `relational.trust.chain_product` | Trust chain product | float | 0-1 | N | synthetic |
| `relational.trust.sponsor_stake` | Sponsor trust at stake | float | 0-1 | N | synthetic |
| `relational.trust.sponsor_count` | Active sponsor count | int | 0-inf | N |   |
| `relational.trust.concentration` | Trust-source concentration | float | 0-1 | N | synthetic |
| `relational.trust.source_diversity` | Independent trust sources | int | 0-inf | N |   |
| `relational.trust.volatility` | Trust-flow volatility | float | 0-inf 1/s | N |   |
| `relational.trust.recovery_time` | Trust recovery time | duration | 0-inf s | N |   |

### Dependency & Obligation — `relational.obligation` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.obligation.upstream_count` | Direct dependency count | int | 0-inf | N |   |
| `relational.obligation.downstream_count` | Direct dependent count | int | 0-inf | N |   |
| `relational.obligation.critical_count` | Critical dependency count | int | 0-inf | N |   |
| `relational.obligation.optional_count` | Optional dependency count | int | 0-inf | N |   |
| `relational.obligation.chain_depth` | Dependency chain depth | int | 0-inf hops | N |   |
| `relational.obligation.blast_radius` | Dependent blast radius | int | 0-inf | N |   |
| `relational.obligation.availability_overlap` | Availability-window overlap | float | 0-1 | N |   |
| `relational.obligation.failure_coupling` | Failure coupling | float | 0-1 | N | synthetic |
| `relational.obligation.substitute_count` | Available substitute count | int | 0-inf | N |   |
| `relational.obligation.substitution_latency` | Substitution latency | duration | 0-inf s | N |   |
| `relational.obligation.exit_cost` | Dependency exit cost | float | 0-1 | N | synthetic |
| `relational.obligation.lock_in_ratio` | No-substitute ratio | float | 0-1 | N |   |
| `relational.obligation.outstanding_count` | Outstanding obligation count | int | 0-inf | N |   |
| `relational.obligation.overdue_count` | Overdue obligation count | int | 0-inf | N |   |
| `relational.obligation.balance` | Obligation balance | float | -1-1 | N |   |
| `relational.obligation.fulfillment_rate` | Obligation fulfillment rate | float | 0-1 | N |   |
| `relational.obligation.breach_count` | Obligation breach count | int | 0-inf | N |   |
| `relational.obligation.oldest_overdue_age` | Oldest overdue age | duration | 0-inf s | N |   |
| `relational.obligation.next_due` | Next obligation due | timestamp | — | N |   |
| `relational.obligation.covenant_count` | Active covenant count | int | 0-inf | A |   |
| `relational.obligation.covenant_validity` | Valid covenant fraction | float | 0-1 | A |   |
| `relational.obligation.collateral_at_risk` | Collateral fraction at risk | float | 0-1 | N |   |
| `relational.obligation.mutual_dependency` | Mutual dependency ratio | float | 0-1 | N |   |
| `relational.obligation.provenance_coverage` | Obligation provenance coverage | float | 0-1 | N |   |

### Communication Patterns — `relational.communication` (20 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.communication.send_rate` | Message send rate | float | 0-inf messages/s | N |   |
| `relational.communication.receive_rate` | Message receive rate | float | 0-inf messages/s | N |   |
| `relational.communication.turn_balance` | Communication turn balance | float | -1-1 | N |   |
| `relational.communication.delivery_success` | Delivery success rate | float | 0-1 | N |   |
| `relational.communication.acknowledgment_rate` | Acknowledgment rate | float | 0-1 | N |   |
| `relational.communication.response_latency` | Response latency | duration | 0-inf s | N |   |
| `relational.communication.delivery_latency` | Delivery latency | duration | 0-inf s | N |   |
| `relational.communication.latency_jitter` | Latency jitter | duration | 0-inf s | N |   |
| `relational.communication.loss_rate` | Message loss rate | float | 0-1 | N |   |
| `relational.communication.duplicate_rate` | Duplicate message rate | float | 0-1 | N |   |
| `relational.communication.retry_rate` | Retry rate | float | 0-inf retries/s | N |   |
| `relational.communication.channel_count` | Active channel count | int | 0-inf | N |   |
| `relational.communication.encrypted_fraction` | Encrypted message fraction | float | 0-1 | N |   |
| `relational.communication.authenticated_fraction` | Authenticated message fraction | float | 0-1 | N |   |
| `relational.communication.message_size_mean` | Mean message size | float | 0-inf bytes | N |   |
| `relational.communication.vocabulary_size` | Observed vocabulary size | int | 0-inf | N |   |
| `relational.communication.vocabulary_overlap` | Vocabulary overlap | float | 0-1 | N |   |
| `relational.communication.clarification_rate` | Clarification request rate | float | 0-1 | N |   |
| `relational.communication.contradiction_rate` | Message contradiction rate | float | 0-1 | N |   |
| `relational.communication.human_origin_fraction` | Human-origin message fraction | float | 0-1 | N | [P] |

### Harm & Repair — `relational.repair` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.repair.incident_count` | Harm incident count | int | 0-inf | A |   |
| `relational.repair.incident_rate` | Harm incident rate | float | 0-inf events/s | A |   |
| `relational.repair.peak_severity` | Peak harm severity | float | 0-1 | A | synthetic |
| `relational.repair.cumulative_severity` | Cumulative harm severity | float | 0-inf score | A |   |
| `relational.repair.affected_count` | Affected entity count | int | 0-inf | A |   |
| `relational.repair.unresolved_count` | Unresolved harm count | int | 0-inf | A |   |
| `relational.repair.recurrence_count` | Post-repair recurrence count | int | 0-inf | A |   |
| `relational.repair.detection_latency` | Harm detection latency | duration | 0-inf s | N |   |
| `relational.repair.acknowledgment_latency` | Harm acknowledgment latency | duration | 0-inf s | N |   |
| `relational.repair.repair_start_latency` | Repair start latency | duration | 0-inf s | N |   |
| `relational.repair.repair_duration` | Repair duration | duration | 0-inf s | N |   |
| `relational.repair.completion_rate` | Repair completion rate | float | 0-1 | N |   |
| `relational.repair.restitution_progress` | Restitution progress | float | 0-1 | N |   |
| `relational.repair.rollback_success` | Rollback success rate | float | 0-1 | N |   |
| `relational.repair.residual_impact` | Residual harm impact | float | 0-1 | N | synthetic |
| `relational.repair.verified` | Repair independently verified | bool | — | A |   |
| `relational.repair.accountability_assigned` | Accountability assigned | bool | — | A |   |
| `relational.repair.owner_count` | Repair owner count | int | 0-inf | N |   |
| `relational.repair.witness_count` | Repair witness count | int | 0-inf | N |   |
| `relational.repair.prevention_coverage` | Prevention control coverage | float | 0-1 | N |   |
| `relational.repair.closure_consent` | Affected-party closure consent | bool | — | A | [P] |
| `relational.repair.appeal_available` | Repair appeal available | bool | — | S |   |

### Power & Sovereignty — `relational.power` (18 signals, class A)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.power.authority_source` | Authority source | enum | — | A |   |
| `relational.power.authority_scope_count` | Authorized action classes | int | 0-inf | A |   |
| `relational.power.delegation_depth` | Delegation depth | int | 0-inf hops | A |   |
| `relational.power.delegation_fanout` | Delegation fanout | int | 0-inf | A |   |
| `relational.power.authority_age` | Authority age | duration | 0-inf s | A |   |
| `relational.power.authority_expiry` | Authority expiry | timestamp | — | A |   |
| `relational.power.revocation_latency` | Authority revocation latency | duration | 0-inf s | N |   |
| `relational.power.unilateral_fraction` | Unilateral action fraction | float | 0-1 | N |   |
| `relational.power.veto_balance` | Veto-power balance | float | -1-1 | N |   |
| `relational.power.resource_control_share` | Resource control share | float | 0-1 | N |   |
| `relational.power.data_access_share` | Data access share | float | 0-1 | N |   |
| `relational.power.decision_weight_share` | Decision weight share | float | 0-1 | N |   |
| `relational.power.consent_required` | Human consent required | bool | — | A | [P] |
| `relational.power.consent_current` | Human consent current | bool | — | A | [P] |
| `relational.power.sovereignty_coverage` | Sovereignty label coverage | float | 0-1 | N |   |
| `relational.power.jurisdiction_count` | Applicable jurisdiction count | int | 0-inf | S |   |
| `relational.power.authority_conflict_count` | Authority conflict count | int | 0-inf | N |   |
| `relational.power.exit_available` | Human exit available | bool | — | S | [P] |

### Shared Context — `relational.context` (16 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.context.shared_history_span` | Shared history span | duration | 0-inf s | N |   |
| `relational.context.common_event_count` | Common event count | int | 0-inf | N |   |
| `relational.context.goal_overlap` | Declared goal overlap | float | 0-1 | N |   |
| `relational.context.constraint_overlap` | Constraint-set overlap | float | 0-1 | N |   |
| `relational.context.policy_match` | Policy version match | bool | — | N |   |
| `relational.context.schema_match` | Schema version match | bool | — | N |   |
| `relational.context.ontology_overlap` | Ontology overlap | float | 0-1 | N |   |
| `relational.context.state_hash_match` | Shared-state hash match | bool | — | N |   |
| `relational.context.snapshot_age_gap` | Context snapshot age gap | duration | 0-inf s | N |   |
| `relational.context.assumption_conflicts` | Assumption conflict count | int | 0-inf | N |   |
| `relational.context.fact_overlap` | Known-fact overlap | float | 0-1 | N |   |
| `relational.context.uncertainty_overlap` | Uncertainty-set overlap | float | 0-1 | N |   |
| `relational.context.role_coverage` | Shared role-map coverage | float | 0-1 | N |   |
| `relational.context.plan_revision_age` | Shared-plan revision age | duration | 0-inf s | N |   |
| `relational.context.provenance_coverage` | Shared-context provenance | float | 0-1 | N |   |
| `relational.context.staleness` | Shared-context staleness | duration | 0-inf s | N |   |

### Presence & Attention — `relational.presence` (14 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.presence.copresence_duration` | Current co-presence duration | duration | 0-inf s | N |   |
| `relational.presence.copresence_ratio` | Co-presence time fraction | float | 0-1 | N |   |
| `relational.presence.availability_ratio` | Mutual availability fraction | float | 0-1 | N |   |
| `relational.presence.presence_gap` | Time since confirmed presence | duration | 0-inf s | N |   |
| `relational.presence.continuity_break_count` | Presence continuity breaks | int | 0-inf | N |   |
| `relational.presence.handoff_gap` | Presence handoff gap | duration | 0-inf s | N |   |
| `relational.presence.attention_response_rate` | Attention response rate | float | 0-1 | N |   |
| `relational.presence.active_attention_fraction` | Active attention fraction | float | 0-1 | N | [P] |
| `relational.presence.foreground_fraction` | Foreground interaction fraction | float | 0-1 | N | [P] |
| `relational.presence.interruption_rate` | Interruption rate | float | 0-inf events/s | N | [P] |
| `relational.presence.human_observer_count` | Human observer count | int | 0-inf | N | [P] |
| `relational.presence.machine_witness_count` | Machine witness count | int | 0-inf | N |   |
| `relational.presence.witness_independence` | Witness independence | float | 0-1 | N | synthetic |
| `relational.presence.witness_quorum` | Witness quorum met | bool | — | N |   |

### Emergence & Co-creation — `relational.cocreation` (12 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.cocreation.joint_artifact_count` | Joint artifact count | int | 0-inf | N |   |
| `relational.cocreation.active_artifact_count` | Active joint artifacts | int | 0-inf | N |   |
| `relational.cocreation.coauthor_fraction` | Co-authored output fraction | float | 0-1 | N |   |
| `relational.cocreation.success_rate` | Joint task success rate | float | 0-1 | N |   |
| `relational.cocreation.synergy_gain` | Joint synergy gain | float | -1-1 | N |   |
| `relational.cocreation.error_reduction` | Joint error reduction | float | -1-1 | N |   |
| `relational.cocreation.coordination_time` | Coordination time per task | duration | 0-inf s | N |   |
| `relational.cocreation.novel_output_rate` | Novel joint output rate | float | 0-inf artifacts/s | N |   |
| `relational.cocreation.capability_gain` | Joint capability gain | float | 0-1 | N | synthetic |
| `relational.cocreation.adaptation_rate` | Mutual adaptation rate | float | 0-inf updates/s | N |   |
| `relational.cocreation.role_complementarity` | Role complementarity | float | 0-1 | N | synthetic |
| `relational.cocreation.artifact_survival` | Joint artifact survival | duration | 0-inf s | N |   |

### Multi-Agent Dynamics — `relational.dynamics` (16 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.dynamics.active_agent_count` | Active agent count | int | 0-inf | N |   |
| `relational.dynamics.coalition_count` | Coalition count | int | 0-inf | N |   |
| `relational.dynamics.coalition_size_mean` | Mean coalition size | float | 0-inf agents | N |   |
| `relational.dynamics.coalition_churn_rate` | Coalition churn rate | float | 0-inf memberships/s | N |   |
| `relational.dynamics.coalition_overlap` | Coalition membership overlap | float | 0-1 | N |   |
| `relational.dynamics.consensus_latency` | Consensus latency | duration | 0-inf s | N |   |
| `relational.dynamics.consensus_success` | Consensus success rate | float | 0-1 | N |   |
| `relational.dynamics.dissent_fraction` | Dissenting agent fraction | float | 0-1 | N |   |
| `relational.dynamics.deadlock_count` | Deadlock count | int | 0-inf | N |   |
| `relational.dynamics.quorum_margin` | Quorum margin | float | -1-1 | N |   |
| `relational.dynamics.leader_control_share` | Leader control share | float | 0-1 | N |   |
| `relational.dynamics.byzantine_evidence_count` | Byzantine evidence count | int | 0-inf | N |   |
| `relational.dynamics.coordination_overhead` | Coordination overhead | float | 0-inf messages/decision | N |   |
| `relational.dynamics.cascade_depth` | Influence cascade depth | int | 0-inf hops | N |   |
| `relational.dynamics.behavior_correlation` | Mean behavior correlation | float | -1-1 | N |   |
| `relational.dynamics.fragmentation_score` | Group fragmentation score | float | 0-1 | N | synthetic |

### Seven Generations — `relational.generations` (12 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.generations.lineage_depth` | Recorded lineage depth | int | 0-inf generations | N |   |
| `relational.generations.history_span` | Historical record span | duration | 0-inf s | N |   |
| `relational.generations.ancestor_coverage` | Ancestor record coverage | float | 0-1 | N |   |
| `relational.generations.inherited_obligation_count` | Inherited obligation count | int | 0-inf | N |   |
| `relational.generations.inherited_harm_count` | Unresolved inherited harms | int | 0-inf | N |   |
| `relational.generations.forecast_horizon` | Impact forecast horizon | duration | 0-inf s | S |   |
| `relational.generations.horizon_coverage` | Generation horizons assessed | int | 0-7 | N |   |
| `relational.generations.future_human_groups` | Future human groups represented | int | 0-inf | N | [P] |
| `relational.generations.descendant_impact_peak` | Peak descendant impact | float | 0-1 | N | [P] synthetic |
| `relational.generations.reversibility_horizon` | Impact reversibility horizon | duration | 0-inf s | N |   |
| `relational.generations.far_uncertainty` | Furthest-horizon uncertainty | float | 0-1 | N | synthetic |
| `relational.generations.review_age` | Intergenerational review age | duration | 0-inf s | N |   |

### Relationship to Place — `relational.place` (8 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `relational.place.bound_place_count` | Declared place bindings | int | 0-inf | S |   |
| `relational.place.current_place_match` | Current place matches binding | bool | — | N |   |
| `relational.place.distance_to_place` | Distance to bound place | float | 0-inf m | N |   |
| `relational.place.colocation_duration` | Place co-location duration | duration | 0-inf s | N |   |
| `relational.place.place_dependency_count` | Place-dependent resource count | int | 0-inf | N |   |
| `relational.place.local_energy_fraction` | Local energy fraction | float | 0-1 | N |   |
| `relational.place.land_footprint` | Relationship land footprint | float | 0-inf m2 | N |   |
| `relational.place.community_consent` | Place-community consent current | bool | — | A | [P] |

