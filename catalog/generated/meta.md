<!-- GENERATED from catalog/meta.json by scripts/gen-catalog-tables.py. Do not edit. -->

### Refresh & Observation Age — `meta.refresh` (17 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `meta.refresh.declared_interval` | Declared refresh interval | duration | 0-inf ms | S |   |
| `meta.refresh.declared_stale_threshold` | Declared staleness threshold | duration | 0-inf ms | S |   |
| `meta.refresh.timestamp_source` | Observation timestamp source | enum | — | S |   |
| `meta.refresh.on_demand_feeds` | On-demand feeds | int | 0-inf | N |   |
| `meta.refresh.rate_span` | Declared rate span | float | 1-inf | N |   |
| `meta.refresh.sample_interval` | Observed sample interval | duration | 0-inf ms | N |   |
| `meta.refresh.interval_ratio` | Observed-to-declared interval ratio | float | 0-inf | N |   |
| `meta.refresh.interval_jitter` | Sample interval jitter | duration | 0-inf ms | N |   |
| `meta.refresh.longest_gap` | Longest observation gap | duration | 0-inf ms | N |   |
| `meta.refresh.missed_polls` | Missed polls | int | 0-inf | N |   |
| `meta.refresh.sample_count` | Observations in window | int | 0-inf | N |   |
| `meta.refresh.observation_age` | Observation age | duration | 0-inf ms | N |   |
| `meta.refresh.observation_age_median` | Median observation age | duration | 0-inf ms | N |   |
| `meta.refresh.observation_age_max` | Oldest observation age | duration | 0-inf ms | N |   |
| `meta.refresh.age_span` | Observation age span | duration | 0-inf ms | N |   |
| `meta.refresh.receipt_skew` | Source-to-receipt skew | float | -inf-inf ms | N |   |
| `meta.refresh.on_demand_latency` | On-demand query latency | duration | 0-inf ms | N |   |

