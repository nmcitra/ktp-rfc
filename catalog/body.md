# Context Signals — Body

The supplied arithmetic exposes a third missing row. Power reaches 16 with one addition, Thermal reaches 14 with one addition, but `21 + 16 + 14 + 105 = 156`. The source specification labels Compute as 22 dimensions while listing only 21, so Body cannot reach 157 without a Compute completion. I add `body.compute.cpu_steal_ratio`; no Additional Body group is inflated to conceal the discrepancy.

## Measurement conventions

The catalogue-wide declaration rules are not restated here. They are stated
once in `catalog/index.md`, which governs: §3 the measurement
envelope (#79), §4 the five observation classes and what each class makes MUST
(#87), §5 label sets (#68), §6 ranges and normalization, §7 aliases. Nothing
in this section overrides any of them.

What this section supplies is the binding: which observation class each Body
group takes, and which of its rows take a different one.

Group assignments. A group's class is the default for its rows; the named
exceptions take the class given. Four of the five classes are present —
N 90 · D 40 · S 22 · A 5, totalling 157. There is no class P: Body reads no
third party's number.

```text
  power           D   power_source, backup_available, power_budget S
  thermal         D   —
  compute         N   cpu_frequency, cpu_throttle D; compute_budget S
  memory          N   ram_capacity, commit_limit, swap_capacity,
                      storage_capacity S; endurance_remaining D
  network         N   default_route_present, tunnel_state S
  hardware        N   active_alarms, post_result, firmware_integrity A;
                      reset_reason, firmware_update_age S
  orchestration   N   desired_instances, maximum_instances,
                      cpu_quota_available, memory_quota_available,
                      autoscaler_state, workload_phase S
  facility        D   smoke_alarm, water_leak_alarm A; cooling_redundancy N;
                      utility_feed_state, access_control_state S
  clock           D   reference_count, backward_step_events, last_sync_age N;
                      sync_state, reference_source S
  entropy         N   —
```

The binding covers all 157 Body rows, not only the 108 authored here. The
`power`, `thermal` and `compute` exceptions name published v1.0.x rows that
this file completes rather than restates; their identifiers are the repaired
forms in `IDENTIFIER-PASS-BODY.md`, authoritative under nmcitra/ktp-rfc#69.

Capacity, quota and budget rows are class S and not class N. A configured
limit is not a counted set; it is read from an allocation, with an as-of
timestamp and a validity horizon in place of an observation window. Declaring
a population for it would be the laundering front matter §4 prohibits for
class D, in a different costume.

Class A's *unknown, not zero* clause is load-bearing in `hardware` and
`facility`. `body.hardware.active_alarms` reading zero because the management
controller is unreachable is not a quiet platform, and
`body.hardware.bmc_reachable` is the row that separates the two cases.

Bare 0-1 ranges. Twelve of the rows carried in this file take a bare 0-1.
Eleven are ratios with a real denominator and satisfy the catalogue rule by
declaring that denominator as their population; no normalization function
exists for them and none is to be invented: compute.cpu_steal_ratio,
memory.inode_free_ratio, memory.endurance_remaining, memory.cache_hit_ratio,
network.endpoint_reachability, network.packet_loss, network.retransmit_ratio,
network.dns_failure_ratio, network.connection_failure_ratio,
network.conntrack_utilization, network.port_utilization. One is a synthetic
score with no natural denominator and MUST declare a normalization function in
the deployment profile: entropy.filesystem_fragmentation, which different
filesystems define incompatibly and which is not comparable across them
without one. None is fully determined.

The published Power, Thermal and Compute rows that this file completes rather
than restates carry eighteen more, and they split the same way. Eleven
ratios: power.efficiency, power.battery_level, power.battery_health,
power.power_utilization, thermal.cooling_capacity, compute.gpu_utilization,
compute.gpu_memory_used, compute.compute_utilization, compute.preemption_rate,
compute.compute_headroom, compute.burst_capacity. Seven synthetic scores that
MUST declare a normalization function: power.power_stability,
power.power_anomaly, thermal.cooling_efficiency, thermal.thermal_stability,
compute.compute_efficiency, compute.scheduler_fairness,
compute.starvation_risk. Their identifiers are the repaired forms recorded in
`IDENTIFIER-PASS-BODY.md`, authoritative under nmcitra/ktp-rfc#69.

Where a ratio's denominator is gated by a predicate — required, operational,
usable, degraded — the predicate is a label set and is declared under the
catalogue-wide label-set rule, not here.

```text
  [ HOLD — the [P] paragraph is not written. The [P] rule has never been
    stated (nmcitra/ktp-rfc#67, open). No Body signal carries the mark; the
    hole is kept so the six domain files agree in shape. ]
```


## Signals

The tables below are generated from the canonical JSON (`catalog/body.json`) by `scripts/gen-catalog-tables.py`. The JSON is source (D5, #66); do not edit the tables.

--8<-- "catalog/generated/body.md"
