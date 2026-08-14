<!-- GENERATED from catalog/body.json by scripts/gen-catalog-tables.py. Do not edit. -->

### Power — missing dimension — `body.power` (16 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.power.amperage` | Current draw | float | 0-inf A | D |   |
| `body.power.wattage` | Power consumption | float | 0-inf W | D |   |
| `body.power.efficiency` | Power efficiency | float | 0-1 | D |   |
| `body.power.power_source` | Source type | enum | — | S |   |
| `body.power.battery_level` | Charge level | float | 0-1 | D |   |
| `body.power.battery_health` | Battery condition | float | 0-1 | D |   |
| `body.power.power_stability` | Supply stability | float | 0-1 | D | synthetic |
| `body.power.backup_available` | Backup power | bool | — | S |   |
| `body.power.time_on_battery` | Battery duration | duration | 0-inf | D |   |
| `body.power.charge_rate` | Charging speed | float | 0-inf | D |   |
| `body.power.discharge_rate` | Drain speed | float | 0-inf | D |   |
| `body.power.power_budget` | Allocated power | float | 0-inf W | S |   |
| `body.power.power_utilization` | Budget usage | float | 0-1 | D |   |
| `body.power.thermal_throttle_power` | Throttled power | bool | — | D |   |
| `body.power.power_anomaly` | Unusual patterns | float | 0-1 | D | synthetic |
| `body.power.voltage` | Input voltage | float | 0-inf V | D |   |

### Thermal — missing dimension — `body.thermal` (14 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.thermal.gpu_temp` | GPU temperature | float | 0-150 C | D |   |
| `body.thermal.memory_temp` | Memory temperature | float | 0-100 C | D |   |
| `body.thermal.storage_temp` | Storage temp | float | 0-100 C | D |   |
| `body.thermal.ambient_temp` | Ambient temp | float | -40-60 C | D |   |
| `body.thermal.cooling_capacity` | Cooling headroom | float | 0-1 | D |   |
| `body.thermal.fan_speed` | Fan RPM | int | 0-inf | D |   |
| `body.thermal.thermal_throttle` | Throttle active | bool | — | D |   |
| `body.thermal.thermal_trend` | Temp direction | float | -inf-inf | D |   |
| `body.thermal.heat_dissipation` | Heat removal rate | float | 0-inf W | D |   |
| `body.thermal.thermal_headroom` | Degrees to limit | float | 0-inf C | D |   |
| `body.thermal.cooling_efficiency` | Cooling effective. | float | 0-1 | D | synthetic |
| `body.thermal.hotspot_delta` | Hotspot vs average | float | 0-inf C | D |   |
| `body.thermal.thermal_stability` | Temp consistency | float | 0-1 | D | synthetic |
| `body.thermal.cpu_temp` | CPU temperature | float | -40-150 C | D |   |

### Compute — arithmetic completion — `body.compute` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.compute.cpu_frequency` | Clock speed | float | 0-inf Hz | D |   |
| `body.compute.cpu_throttle` | Throttle active | bool | — | D |   |
| `body.compute.core_count_available` | Usable cores | int | 0-inf | N |   |
| `body.compute.core_count_utilized` | Used cores | int | 0-inf | N |   |
| `body.compute.thread_count` | Active threads | int | 0-inf | N |   |
| `body.compute.context_switches` | Switches/sec | int | 0-inf | N |   |
| `body.compute.gpu_utilization` | GPU usage | float | 0-1 | N |   |
| `body.compute.gpu_memory_used` | GPU memory | float | 0-1 | N |   |
| `body.compute.inference_rate` | Inferences/sec | float | 0-inf | N |   |
| `body.compute.batch_size` | Batch processing | int | 0-inf | N |   |
| `body.compute.queue_depth` | Pending work | int | 0-inf | N |   |
| `body.compute.queue_wait_time` | Queue latency | duration | 0-inf | N |   |
| `body.compute.processing_latency` | Processing time | duration | 0-inf | N |   |
| `body.compute.compute_budget` | Allocated compute | float | 0-inf | S |   |
| `body.compute.compute_utilization` | Budget usage | float | 0-1 | N |   |
| `body.compute.compute_efficiency` | Work per resource | float | 0-1 | N | synthetic |
| `body.compute.scheduler_fairness` | Fair scheduling | float | 0-1 | N | synthetic |
| `body.compute.preemption_rate` | Interruption rate | float | 0-1 | N |   |
| `body.compute.starvation_risk` | Resource starvation | float | 0-1 | N | synthetic |
| `body.compute.compute_headroom` | Capacity remaining | float | 0-1 | N |   |
| `body.compute.burst_capacity` | Burst available | float | 0-1 | N |   |
| `body.compute.cpu_steal_ratio` | CPU steal ratio | float | 0-1 | N |   |

### Memory & Storage — `body.memory` (24 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.memory.ram_capacity` | Physical RAM | int | 0-inf B | S |   |
| `body.memory.ram_available` | Available RAM | int | 0-inf B | N |   |
| `body.memory.commit_limit` | Commit limit | int | 0-inf B | S |   |
| `body.memory.committed_bytes` | Committed memory | int | 0-inf B | N |   |
| `body.memory.swap_capacity` | Swap capacity | int | 0-inf B | S |   |
| `body.memory.swap_used` | Swap used | int | 0-inf B | N |   |
| `body.memory.page_fault_rate` | Page fault rate | float | 0-inf faults/s | N |   |
| `body.memory.major_fault_rate` | Major fault rate | float | 0-inf faults/s | N |   |
| `body.memory.pressure_state` | Memory pressure | enum | — | N |   |
| `body.memory.oom_kill_events` | OOM kills | int | 0-inf | N |   |
| `body.memory.ecc_corrected_errors` | Corrected ECC errors | int | 0-inf | N |   |
| `body.memory.ecc_uncorrected_errors` | Uncorrected ECC errors | int | 0-inf | N |   |
| `body.memory.storage_capacity` | Storage capacity | int | 0-inf B | S |   |
| `body.memory.storage_free` | Free storage | int | 0-inf B | N |   |
| `body.memory.read_throughput` | Read throughput | float | 0-inf B/s | N |   |
| `body.memory.write_throughput` | Write throughput | float | 0-inf B/s | N |   |
| `body.memory.read_latency` | Read latency | duration | 0-inf ms | N |   |
| `body.memory.write_latency` | Write latency | duration | 0-inf ms | N |   |
| `body.memory.io_queue_depth` | I/O queue depth | int | 0-inf | N |   |
| `body.memory.io_errors` | I/O errors | int | 0-inf | N |   |
| `body.memory.readonly_mounts` | Read-only mounts | int | 0-inf | N |   |
| `body.memory.inode_free_ratio` | Free inode ratio | float | 0-1 | N |   |
| `body.memory.endurance_remaining` | Write endurance left | float | 0-1 | D |   |
| `body.memory.cache_hit_ratio` | Cache hit ratio | float | 0-1 | N |   |

### Network Connectivity — `body.network` (22 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.network.interface_count` | Network interfaces | int | 0-inf | N |   |
| `body.network.operational_interfaces` | Operational interfaces | int | 0-inf | N |   |
| `body.network.default_route_present` | Default route present | bool | — | S |   |
| `body.network.endpoint_reachability` | Required endpoint reachability | float | 0-1 | N |   |
| `body.network.reference_rtt` | Reference RTT | duration | 0-inf ms | N |   |
| `body.network.reference_jitter` | Reference jitter | duration | 0-inf ms | N |   |
| `body.network.packet_loss` | Reference packet loss | float | 0-1 | N |   |
| `body.network.egress_bandwidth` | Available egress bandwidth | float | 0-inf bit/s | N |   |
| `body.network.ingress_bandwidth` | Available ingress bandwidth | float | 0-inf bit/s | N |   |
| `body.network.transmit_rate` | Transmit rate | float | 0-inf bit/s | N |   |
| `body.network.receive_rate` | Receive rate | float | 0-inf bit/s | N |   |
| `body.network.retransmit_ratio` | Transport retransmit ratio | float | 0-1 | N |   |
| `body.network.dns_latency` | DNS resolution latency | duration | 0-inf ms | N |   |
| `body.network.dns_failure_ratio` | DNS failure ratio | float | 0-1 | N |   |
| `body.network.connection_failure_ratio` | Connection failure ratio | float | 0-1 | N |   |
| `body.network.active_connections` | Active connections | int | 0-inf | N |   |
| `body.network.conntrack_utilization` | Conntrack utilization | float | 0-1 | N |   |
| `body.network.port_utilization` | Ephemeral port utilization | float | 0-1 | N |   |
| `body.network.route_change_events` | Route changes | int | 0-inf | N |   |
| `body.network.link_flap_events` | Link flaps | int | 0-inf | N |   |
| `body.network.tunnel_state` | Secure tunnel state | enum | — | S |   |
| `body.network.endpoint_contact_age` | Required endpoint contact age | duration | 0-inf s | N |   |

### Hardware Health — `body.hardware` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.hardware.cpu_machine_checks` | CPU machine checks | int | 0-inf | N |   |
| `body.hardware.pcie_corrected_errors` | PCIe corrected errors | int | 0-inf | N |   |
| `body.hardware.pcie_uncorrected_errors` | PCIe uncorrected errors | int | 0-inf | N |   |
| `body.hardware.accelerator_faults` | Accelerator faults | int | 0-inf | N |   |
| `body.hardware.peripheral_resets` | Peripheral resets | int | 0-inf | N |   |
| `body.hardware.bus_timeouts` | Bus timeouts | int | 0-inf | N |   |
| `body.hardware.watchdog_resets` | Watchdog resets | int | 0-inf | N |   |
| `body.hardware.unplanned_reboots` | Unplanned reboots | int | 0-inf | N |   |
| `body.hardware.reset_reason` | Last reset reason | enum | — | S |   |
| `body.hardware.post_result` | Boot self-test result | enum | — | A |   |
| `body.hardware.bmc_reachable` | Management controller reachable | bool | — | N |   |
| `body.hardware.active_alarms` | Active platform alarms | int | 0-inf | A |   |
| `body.hardware.firmware_update_age` | Firmware update age | duration | 0-inf d | S |   |
| `body.hardware.firmware_integrity` | Firmware integrity | bool | — | A |   |
| `body.hardware.degraded_components` | Degraded components | int | 0-inf | N |   |
| `body.hardware.failed_components` | Failed components | int | 0-inf | N |   |
| `body.hardware.unavailable_sensors` | Unavailable hardware sensors | int | 0-inf | N |   |
| `body.hardware.inventory_drift` | Hardware inventory drift | bool | — | N |   |

### Orchestration & Scaling — `body.orchestration` (14 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.orchestration.control_plane_reachable` | Control plane reachable | bool | — | N |   |
| `body.orchestration.workload_phase` | Workload phase | enum | — | S |   |
| `body.orchestration.desired_instances` | Desired instances | int | 0-inf | S |   |
| `body.orchestration.ready_instances` | Ready instances | int | 0-inf | N |   |
| `body.orchestration.failed_instances` | Failed instances | int | 0-inf | N |   |
| `body.orchestration.pending_instances` | Pending instances | int | 0-inf | N |   |
| `body.orchestration.restart_events` | Restart events | int | 0-inf | N |   |
| `body.orchestration.eviction_events` | Eviction events | int | 0-inf | N |   |
| `body.orchestration.autoscaler_state` | Autoscaler state | enum | — | S |   |
| `body.orchestration.maximum_instances` | Maximum instances | int | 0-inf | S |   |
| `body.orchestration.cpu_quota_available` | Available CPU quota | float | 0-inf cores | S |   |
| `body.orchestration.memory_quota_available` | Available memory quota | int | 0-inf B | S |   |
| `body.orchestration.scheduling_latency` | Scheduling latency | duration | 0-inf ms | N |   |
| `body.orchestration.placement_constraints_met` | Placement constraints met | bool | — | N |   |

### Facility Infrastructure — `body.facility` (12 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.facility.utility_feed_state` | Utility feed state | enum | — | S |   |
| `body.facility.generator_state` | Generator state | enum | — | D |   |
| `body.facility.hvac_state` | HVAC state | enum | — | D |   |
| `body.facility.cooling_redundancy` | Cooling redundancy | int | 0-inf | N |   |
| `body.facility.relative_humidity` | Relative humidity | float | 0-100 %RH | D |   |
| `body.facility.particulate_concentration` | Airborne particulates | float | 0-inf ug/m3 | D |   |
| `body.facility.vibration_rms` | Vibration RMS | float | 0-inf mm/s | D |   |
| `body.facility.smoke_alarm` | Smoke alarm | bool | — | A |   |
| `body.facility.water_leak_alarm` | Water leak alarm | bool | — | A |   |
| `body.facility.fire_suppression_ready` | Fire suppression ready | bool | — | D |   |
| `body.facility.rack_door_open` | Rack door open | bool | — | D |   |
| `body.facility.access_control_state` | Access control state | enum | — | S |   |

### Time Synchronization — `body.clock` (8 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.clock.sync_state` | Synchronization state | enum | — | S |   |
| `body.clock.reference_source` | Reference source | enum | — | S |   |
| `body.clock.reference_count` | Usable time sources | int | 0-inf | N |   |
| `body.clock.offset_magnitude` | Clock offset (signed) | float | -inf-inf ms | D |   |
| `body.clock.uncertainty` | Clock uncertainty | float | 0-inf ms | D |   |
| `body.clock.frequency_error` | Frequency error (signed) | float | -inf-inf ppm | D |   |
| `body.clock.last_sync_age` | Last synchronization age | duration | 0-inf s | N |   |
| `body.clock.backward_step_events` | Backward clock steps | int | 0-inf | N |   |

### Entropy Indicators — `body.entropy` (7 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `body.entropy.config_drift_items` | Configuration drift items | int | 0-inf | N |   |
| `body.entropy.orphaned_allocations` | Orphaned allocations | int | 0-inf | N |   |
| `body.entropy.zombie_processes` | Zombie processes | int | 0-inf | N |   |
| `body.entropy.memory_leak_rate` | Memory leak rate | float | 0-inf B/s | N |   |
| `body.entropy.handle_leak_rate` | Handle leak rate | float | 0-inf handles/s | N |   |
| `body.entropy.filesystem_fragmentation` | Filesystem fragmentation | float | 0-1 | N | synthetic |
| `body.entropy.unhandled_error_rate` | Unhandled error rate | float | 0-inf events/s | N |   |

