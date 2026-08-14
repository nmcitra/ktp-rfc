# Context Signals — World

The physical and digital environment the agent acts in.

MEASUREMENT CONVENTIONS

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement
envelope (#79), §4 the five observation classes and what each class makes MUST
(#87), §5 label sets (#68), §6 ranges and normalization, §7 aliases. Nothing
in this section overrides any of them.

What this section supplies is the binding: which observation class each World
group takes, and which of its rows take a different one. World is the only
domain that contains all five classes, which is why the classes were authored
against it.

Group assignments. A group's class is the default for its rows; the named
exceptions take the class given. The five classes partition the domain:
N 135 · D 132 · A 45 · S 37 · P 20, totalling 369.

  optical         D   camera_availability N
  spatial         D   position_source, geofence_inside, geofence_distance S
  weather         D   weather_alert_level P
  acoustic        D   sound_source_count N
  presence        N   —
  traffic         N   signal_phase, signal_phase_remaining S;
                      active_incident_count A
  infrastructure  D   fault counts, availabilities, overdue_maintenance_count N;
                      fire_alarm_state, smoke_control_state, gas_leak_alarm,
                      sewer_backflow_detected A
  network         N   signal_strength, signal_noise_ratio D;
                      captive_portal_detected S
  geophysical     D   earthquake_magnitude, epicenter_distance P;
                      terrain_elevation, terrain_slope, terrain_roughness S
  chemical        D   —
  energy          D   grid_connected S
  cyclical        S   dominant_period, periodicity_strength, cycle_deviation,
                      scheduled_event_count N
  economic        P   active_supplier_count, supplier_concentration,
                      inventory_cover, procurement_lead_time,
                      demand_forecast_error, transaction_success_rate,
                      settlement_latency N
  security        A   malicious_ip_count, threat_intelligence_match_count P;
                      vulnerable_asset_count, exposed_service_count,
                      oldest_patch_age, anomalous_host_count N
  emergency       A   responder_unit_count, nearest_responder_eta,
                      dispatch_latency, emergency_supply_endurance N
  regulatory      S   assessment_age, unmet_requirement_count,
                      weighted_compliance_score, active_exception_count A;
                      consent_coverage_fraction N
  digital         N   rollback_available, next_certificate_expiry S

Bare 0-1 ranges. Forty-nine World signals carry a bare 0-1. Thirty-seven are
ratios with a real denominator and satisfy the catalogue rule by declaring
that denominator as their population; no normalization function exists for
them and none is to be invented. Ten are synthetic scores with no natural
denominator and MUST declare a normalization function in the deployment
profile: spatial.localization_confidence, weather.icing_probability,
presence.flow_coherence, traffic.congestion_index,
cyclical.periodicity_strength, security.anomaly_score,
security.control_health_fraction, regulatory.weighted_compliance_score,
emergency.recovery_progress_fraction, economic.supplier_concentration. Two
are fully determined and declare neither: cyclical.lunar_phase and
optical.flicker_modulation.

Where a ratio's denominator is gated by a predicate — healthy, available,
critical — the predicate is a label set and is declared under the
catalogue-wide label-set rule, not here.

Projected values. world.weather.icing_probability describes a period that has
not happened, so it has no observation window; it is held in class D against
its instrument and marked here rather than reclassified. Front matter §4 names
PROJECTED as a candidate sixth class and declines to add it, because
nmcitra/ktp-rfc#73 and #74 own that question.

Privacy. Thirty-four World signals carry the [P] mark. The rule governing the
mark is open under nmcitra/ktp-rfc#67, and nothing in this section authorizes,
restricts or interprets it.


## Signals

The tables below are generated from the canonical JSON (`catalog/world.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/world.md"
