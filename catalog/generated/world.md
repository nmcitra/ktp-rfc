<!-- GENERATED from catalog/world.json by scripts/gen-catalog-tables.py. Do not edit. -->

### Optical & Visual — `world.optical` (16 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.optical.illuminance` | Ambient illuminance | float | 0-200000 lx | D |   |
| `world.optical.luminance` | Scene luminance | float | 0-inf cd/m2 | D |   |
| `world.optical.color_temperature` | Correlated color temp | float | 1000-40000 K | D |   |
| `world.optical.ultraviolet_irradiance` | UV irradiance | float | 0-inf W/m2 | D |   |
| `world.optical.infrared_irradiance` | IR irradiance | float | 0-inf W/m2 | D |   |
| `world.optical.contrast_ratio` | Scene contrast ratio | float | 1-inf | D |   |
| `world.optical.saturation_fraction` | Pixel saturation fraction | float | 0-1 | D |   |
| `world.optical.glare_index` | Unified glare rating | float | 0-40 | D |   |
| `world.optical.flicker_frequency` | Light flicker frequency | float | 0-inf Hz | D |   |
| `world.optical.flicker_modulation` | Flicker modulation | float | 0-1 | D | determined |
| `world.optical.occlusion_fraction` | Scene occlusion | float | 0-1 | D |   |
| `world.optical.image_signal_noise_ratio` | Image signal-noise ratio | float | -inf-inf dB | D |   |
| `world.optical.optical_flow` | Optical flow magnitude | float | 0-inf px/s | D |   |
| `world.optical.scene_change_rate` | Scene change rate | float | 0-inf changes/min | D |   |
| `world.optical.camera_availability` | Camera availability | float | 0-1 | N |   |
| `world.optical.frame_latency` | Camera frame latency | duration | 0-inf ms | D |   |

### Spatial Awareness — `world.spatial` (22 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.spatial.latitude` | Position latitude | float | -90-90 deg | D |   |
| `world.spatial.longitude` | Position longitude | float | -180-180 deg | D |   |
| `world.spatial.altitude` | Position altitude | float | -12000-100000 m | D |   |
| `world.spatial.horizontal_error` | Horizontal position error | float | 0-inf m | D |   |
| `world.spatial.vertical_error` | Vertical position error | float | 0-inf m | D |   |
| `world.spatial.heading` | Heading | float | 0-360 deg | D |   |
| `world.spatial.floor_level` | Indoor floor level | int | -100-1000 | D |   |
| `world.spatial.position_source` | Position fix source | enum | — | S |   |
| `world.spatial.map_age` | Map observation age | duration | 0-inf s | D |   |
| `world.spatial.mapped_area` | Mapped area | float | 0-inf m2 | D |   |
| `world.spatial.map_resolution` | Map cell resolution | float | 0-inf m/cell | D |   |
| `world.spatial.map_completeness` | Map completeness | float | 0-1 | D |   |
| `world.spatial.localization_confidence` | Localization confidence | float | 0-1 | D | synthetic |
| `world.spatial.geofence_distance` | Nearest geofence distance | float | 0-inf m | S |   |
| `world.spatial.geofence_inside` | Inside configured geofence | bool | — | S |   |
| `world.spatial.nearest_obstacle` | Nearest obstacle distance | float | 0-inf m | D |   |
| `world.spatial.obstacle_density` | Obstacle density | float | 0-inf objects/m2 | D |   |
| `world.spatial.free_space_fraction` | Free-space fraction | float | 0-1 | D |   |
| `world.spatial.traversable_area` | Traversable area | float | 0-inf m2 | D |   |
| `world.spatial.route_clearance` | Minimum route clearance | float | 0-inf m | D |   |
| `world.spatial.occupancy_resolution` | Occupancy-grid resolution | float | 0-inf m/cell | D |   |
| `world.spatial.occupancy_age` | Occupancy-map age | duration | 0-inf s | D |   |

### Atmospheric & Weather — `world.weather` (24 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.weather.air_temperature` | Air temperature | float | -100-70 C | D |   |
| `world.weather.relative_humidity` | Relative humidity | float | 0-100 % | D |   |
| `world.weather.air_pressure` | Barometric pressure | float | 300-1100 hPa | D |   |
| `world.weather.dew_point` | Dew-point temperature | float | -100-70 C | D |   |
| `world.weather.wet_bulb_temperature` | Wet-bulb temperature | float | -100-70 C | D |   |
| `world.weather.apparent_temperature` | Apparent temperature | float | -150-100 C | D |   |
| `world.weather.wind_speed` | Sustained wind speed | float | 0-200 m/s | D |   |
| `world.weather.wind_gust` | Peak wind gust | float | 0-150 m/s | D |   |
| `world.weather.wind_direction` | Wind direction | float | 0-360 deg | D |   |
| `world.weather.precipitation_rate` | Precipitation rate | float | 0-inf mm/h | D |   |
| `world.weather.precipitation_type` | Precipitation type | enum | — | D |   |
| `world.weather.daily_precipitation` | Daily precipitation | float | 0-inf mm | D |   |
| `world.weather.visibility` | Meteorological visibility | float | 0-inf m | D |   |
| `world.weather.cloud_cover` | Cloud cover | float | 0-100 % | D |   |
| `world.weather.cloud_base_height` | Cloud-base height | float | 0-inf m | D |   |
| `world.weather.solar_irradiance` | Solar irradiance | float | 0-1500 W/m2 | D |   |
| `world.weather.lightning_distance` | Nearest lightning distance | float | 0-inf km | D |   |
| `world.weather.lightning_rate` | Lightning strike rate | float | 0-inf strikes/min | D |   |
| `world.weather.storm_distance` | Nearest storm distance | float | 0-inf km | D |   |
| `world.weather.storm_cell_speed` | Storm-cell speed | float | 0-150 m/s | D |   |
| `world.weather.hail_diameter` | Maximum hail diameter | float | 0-inf mm | D |   |
| `world.weather.snow_depth` | Snow depth | float | 0-inf cm | D |   |
| `world.weather.icing_probability` | Icing probability | float | 0-1 | D | synthetic |
| `world.weather.weather_alert_level` | Weather alert level | enum | — | P |   |

### Acoustic Environment — `world.acoustic` (14 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.acoustic.equivalent_sound_level` | Equivalent sound level | float | 0-194 dBA | D |   |
| `world.acoustic.peak_sound_level` | Peak sound level | float | 0-194 dB SPL | D |   |
| `world.acoustic.noise_floor` | Acoustic noise floor | float | 0-194 dB SPL | D |   |
| `world.acoustic.dominant_frequency` | Dominant frequency | float | 0-inf Hz | D |   |
| `world.acoustic.spectral_centroid` | Spectral centroid | float | 0-inf Hz | D |   |
| `world.acoustic.low_frequency_level` | Low-frequency level | float | 0-194 dB SPL | D |   |
| `world.acoustic.ultrasonic_level` | Ultrasonic level | float | 0-194 dB SPL | D |   |
| `world.acoustic.signal_noise_ratio` | Acoustic signal-noise ratio | float | -inf-inf dB | D |   |
| `world.acoustic.reverberation_time` | Reverberation time | duration | 0-inf s | D |   |
| `world.acoustic.impulse_rate` | Acoustic impulse rate | float | 0-inf events/min | D |   |
| `world.acoustic.alarm_tone_present` | Alarm tone present | bool | — | D |   |
| `world.acoustic.speech_fraction` | Speech activity | float | 0-1 | D | [P] |
| `world.acoustic.sound_source_count` | Resolved sound-source count | int | 0-inf | N |   |
| `world.acoustic.dominant_source_bearing` | Dominant source bearing | float | 0-360 deg | D |   |

### Human Presence & Behavior — `world.presence` (28 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.presence.person_count` | Person count | int | 0-inf | N | [P] |
| `world.presence.person_count_uncertainty` | Count uncertainty | float | 0-inf persons | N | [P] |
| `world.presence.occupancy_density` | Occupancy density | float | 0-inf persons/m2 | N | [P] |
| `world.presence.occupancy_capacity_ratio` | Occupancy capacity ratio | float | 0-inf | N | [P] |
| `world.presence.occupied_zone_count` | Occupied zone count | int | 0-inf | N | [P] |
| `world.presence.ingress_rate` | Ingress rate | float | 0-inf persons/min | N | [P] |
| `world.presence.egress_rate` | Egress rate | float | 0-inf persons/min | N | [P] |
| `world.presence.mean_travel_speed` | Mean travel speed | float | 0-15 m/s | N | [P] |
| `world.presence.speed_standard_deviation` | Speed variation | float | 0-inf m/s | N | [P] |
| `world.presence.direction_entropy` | Movement direction entropy | float | 0-inf bit | N | [P] |
| `world.presence.flow_coherence` | Flow coherence | float | 0-1 | N | [P] synthetic |
| `world.presence.stationary_fraction` | Stationary fraction | float | 0-1 | N | [P] |
| `world.presence.running_fraction` | Running fraction | float | 0-1 | N | [P] |
| `world.presence.counterflow_fraction` | Counterflow fraction | float | 0-1 | N | [P] |
| `world.presence.mean_dwell_time` | Mean dwell time | duration | 0-inf s | N | [P] |
| `world.presence.occupancy_persistence` | Continuous occupancy | duration | 0-inf s | N | [P] |
| `world.presence.queue_length` | Queue length | int | 0-inf | N | [P] |
| `world.presence.queue_growth_rate` | Queue growth rate | float | -inf-inf persons/min | N | [P] |
| `world.presence.mean_wait_time` | Mean queue wait | duration | 0-inf s | N | [P] |
| `world.presence.mean_spacing` | Mean interpersonal spacing | float | 0-inf m | N | [P] |
| `world.presence.minimum_spacing` | Minimum interpersonal spacing | float | 0-inf m | N | [P] |
| `world.presence.group_count` | Observed group count | int | 0-inf | N | [P] |
| `world.presence.mean_group_size` | Mean group size | float | 0-inf persons | N | [P] |
| `world.presence.restricted_zone_person_count` | People in restricted zones | int | 0-inf | N | [P] |
| `world.presence.unauthorized_person_count` | Unauthorized person count | int | 0-inf | N | [P] |
| `world.presence.fall_rate` | Detected fall rate | float | 0-inf events/min | N | [P] |
| `world.presence.abrupt_motion_rate` | Abrupt motion rate | float | 0-inf events/min | N | [P] |
| `world.presence.help_request_rate` | Help-request rate | float | 0-inf events/min | N | [P] |

### Vehicle & Traffic — `world.traffic` (18 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.traffic.active_vehicle_count` | Active vehicle count | int | 0-inf | N |   |
| `world.traffic.traffic_density` | Traffic density | float | 0-inf vehicles/km | N |   |
| `world.traffic.vehicle_flow_rate` | Vehicle flow rate | float | 0-inf vehicles/min | N |   |
| `world.traffic.mean_speed` | Mean vehicle speed | float | 0-inf km/h | N |   |
| `world.traffic.p85_speed` | 85th-percentile speed | float | 0-inf km/h | N |   |
| `world.traffic.speed_variance` | Vehicle speed variance | float | 0-inf (km/h)^2 | N |   |
| `world.traffic.stopped_vehicle_count` | Stopped vehicle count | int | 0-inf | N |   |
| `world.traffic.vehicle_queue_length` | Traffic queue length | int | 0-inf vehicles | N |   |
| `world.traffic.mean_queue_delay` | Mean traffic delay | duration | 0-inf s | N |   |
| `world.traffic.lane_occupancy` | Lane occupancy | float | 0-1 | N |   |
| `world.traffic.mean_headway` | Mean vehicle headway | duration | 0-inf s | N |   |
| `world.traffic.minimum_time_gap` | Minimum time gap | duration | 0-inf s | N |   |
| `world.traffic.congestion_index` | Congestion index | float | 0-1 | N | synthetic |
| `world.traffic.active_incident_count` | Active traffic incidents | int | 0-inf | A |   |
| `world.traffic.emergency_vehicle_count` | Emergency vehicle count | int | 0-inf | N |   |
| `world.traffic.wrong_way_rate` | Wrong-way event rate | float | 0-inf events/min | N |   |
| `world.traffic.signal_phase` | Traffic signal phase | enum | — | S |   |
| `world.traffic.signal_phase_remaining` | Signal phase remaining | duration | 0-inf s | S |   |

### Infrastructure State — `world.infrastructure` (32 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.infrastructure.structural_vibration_rms` | Structural vibration RMS | float | 0-inf mm/s | D |   |
| `world.infrastructure.structural_strain` | Structural strain | float | -inf-inf microstrain | D |   |
| `world.infrastructure.structural_tilt` | Structural tilt | float | -90-90 deg | D |   |
| `world.infrastructure.maximum_crack_width` | Maximum crack width | float | 0-inf mm | D |   |
| `world.infrastructure.floor_load` | Floor load | float | 0-inf kg/m2 | D |   |
| `world.infrastructure.roof_load` | Roof load | float | 0-inf kg/m2 | D |   |
| `world.infrastructure.foundation_settlement` | Foundation settlement | float | 0-inf mm | D |   |
| `world.infrastructure.door_open_fraction` | Open-door fraction | float | 0-1 | N |   |
| `world.infrastructure.door_fault_count` | Door fault count | int | 0-inf | N |   |
| `world.infrastructure.elevator_availability` | Elevator availability | float | 0-1 | N |   |
| `world.infrastructure.elevator_fault_count` | Elevator fault count | int | 0-inf | N |   |
| `world.infrastructure.escalator_availability` | Escalator availability | float | 0-1 | N |   |
| `world.infrastructure.hvac_availability` | HVAC availability | float | 0-1 | N |   |
| `world.infrastructure.supply_air_temperature` | Supply-air temperature | float | -50-100 C | D |   |
| `world.infrastructure.return_air_temperature` | Return-air temperature | float | -50-100 C | D |   |
| `world.infrastructure.ventilation_rate` | Ventilation flow rate | float | 0-inf L/s | D |   |
| `world.infrastructure.filter_pressure_drop` | Filter pressure drop | float | 0-inf Pa | D |   |
| `world.infrastructure.water_pressure` | Water pressure | float | 0-inf kPa | D |   |
| `world.infrastructure.water_flow_rate` | Water flow rate | float | 0-inf L/s | D |   |
| `world.infrastructure.water_leak_rate` | Water leak rate | float | 0-inf L/min | D |   |
| `world.infrastructure.water_storage_level` | Water storage level | float | 0-100 % | D |   |
| `world.infrastructure.wastewater_level` | Wastewater level | float | 0-100 % | D |   |
| `world.infrastructure.sewer_backflow_detected` | Sewer backflow detected | bool | — | A |   |
| `world.infrastructure.gas_pressure` | Gas-line pressure | float | 0-inf kPa | D |   |
| `world.infrastructure.gas_leak_alarm` | Gas leak alarm | bool | — | A |   |
| `world.infrastructure.fire_alarm_state` | Fire alarm state | enum | — | A |   |
| `world.infrastructure.sprinkler_pressure` | Sprinkler pressure | float | 0-inf kPa | D |   |
| `world.infrastructure.smoke_control_state` | Smoke-control state | enum | — | A |   |
| `world.infrastructure.emergency_lighting_fraction` | Emergency lighting fraction | float | 0-1 | N |   |
| `world.infrastructure.sump_pump_availability` | Sump-pump availability | float | 0-1 | N |   |
| `world.infrastructure.asset_fault_count` | Infrastructure fault count | int | 0-inf | N |   |
| `world.infrastructure.overdue_maintenance_count` | Overdue maintenance count | int | 0-inf | N |   |

### Network & Connectivity — `world.network` (26 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.network.interface_count` | Network interface count | int | 0-inf | N |   |
| `world.network.active_link_count` | Active link count | int | 0-inf | N |   |
| `world.network.link_availability` | Link availability | float | 0-1 | N |   |
| `world.network.aggregate_capacity` | Aggregate link capacity | float | 0-inf Mbps | N |   |
| `world.network.available_bandwidth` | Available bandwidth | float | 0-inf Mbps | N |   |
| `world.network.receive_throughput` | Receive throughput | float | 0-inf bit/s | N |   |
| `world.network.transmit_throughput` | Transmit throughput | float | 0-inf bit/s | N |   |
| `world.network.packet_loss` | Packet loss | float | 0-1 | N |   |
| `world.network.round_trip_latency` | Round-trip latency | duration | 0-inf ms | N |   |
| `world.network.jitter` | Packet-delay variation | duration | 0-inf ms | N |   |
| `world.network.retransmission_rate` | Retransmission rate | float | 0-inf packets/s | N |   |
| `world.network.frame_error_rate` | Frame error rate | float | 0-inf frames/s | N |   |
| `world.network.signal_strength` | Radio signal strength | float | -200-100 dBm | D |   |
| `world.network.signal_noise_ratio` | Radio signal-noise ratio | float | -inf-inf dB | D |   |
| `world.network.channel_utilization` | Channel utilization | float | 0-100 % | N |   |
| `world.network.wifi_access_point_count` | Visible WiFi access points | int | 0-inf | N |   |
| `world.network.cellular_cell_count` | Visible cellular cells | int | 0-inf | N |   |
| `world.network.iot_device_count` | Observed IoT device count | int | 0-inf | N |   |
| `world.network.unknown_device_count` | Unknown device count | int | 0-inf | N |   |
| `world.network.address_conflict_count` | Address conflict count | int | 0-inf | N |   |
| `world.network.route_change_rate` | Route change rate | float | 0-inf changes/min | N |   |
| `world.network.dns_success_rate` | DNS resolution success | float | 0-1 | N |   |
| `world.network.dhcp_lease_utilization` | DHCP lease utilization | float | 0-1 | N |   |
| `world.network.time_sync_error` | Time synchronization error | duration | -inf-inf ms | N |   |
| `world.network.path_mtu` | Path maximum transmission unit | int | 68-65535 B | N |   |
| `world.network.captive_portal_detected` | Captive portal detected | bool | — | S |   |

### Geophysical — `world.geophysical` (18 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.geophysical.peak_ground_acceleration` | Peak ground acceleration | float | 0-inf m/s2 | D |   |
| `world.geophysical.peak_ground_velocity` | Peak ground velocity | float | 0-inf mm/s | D |   |
| `world.geophysical.ground_displacement` | Ground displacement | float | 0-inf mm | D |   |
| `world.geophysical.earthquake_magnitude` | Earthquake magnitude | float | -2-10 Mw | P |   |
| `world.geophysical.epicenter_distance` | Epicenter distance | float | 0-inf km | P |   |
| `world.geophysical.terrain_elevation` | Terrain elevation | float | -11000-9000 m | S |   |
| `world.geophysical.terrain_slope` | Terrain slope | float | 0-90 deg | S |   |
| `world.geophysical.terrain_roughness` | Terrain roughness RMS | float | 0-inf m | S |   |
| `world.geophysical.soil_moisture` | Soil moisture | float | 0-100 % | D |   |
| `world.geophysical.soil_temperature` | Soil temperature | float | -100-100 C | D |   |
| `world.geophysical.soil_shear_strength` | Soil shear strength | float | 0-inf kPa | D |   |
| `world.geophysical.vertical_ground_rate` | Vertical ground-motion rate | float | -inf-inf mm/yr | D |   |
| `world.geophysical.landslide_displacement` | Landslide displacement | float | 0-inf mm | D |   |
| `world.geophysical.groundwater_depth` | Groundwater depth | float | 0-inf m | D |   |
| `world.geophysical.surface_water_level` | Surface-water level | float | -inf-inf m datum | D |   |
| `world.geophysical.stream_flow` | Stream flow rate | float | 0-inf m3/s | D |   |
| `world.geophysical.flood_depth` | Flood depth | float | 0-inf m | D |   |
| `world.geophysical.significant_wave_height` | Significant wave height | float | 0-inf m | D |   |

### Chemical & Biological — `world.chemical` (16 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.chemical.co2` | Carbon dioxide | float | 0-inf ppm | D |   |
| `world.chemical.co` | Carbon monoxide | float | 0-inf ppm | D |   |
| `world.chemical.no2` | Nitrogen dioxide | float | 0-inf ppb | D |   |
| `world.chemical.so2` | Sulfur dioxide | float | 0-inf ppb | D |   |
| `world.chemical.ozone` | Ozone concentration | float | 0-inf ppb | D |   |
| `world.chemical.total_voc` | Total volatile organics | float | 0-inf ppb | D |   |
| `world.chemical.pm1` | PM1 concentration | float | 0-inf ug/m3 | D |   |
| `world.chemical.pm2_5` | PM2.5 concentration | float | 0-inf ug/m3 | D |   |
| `world.chemical.pm10` | PM10 concentration | float | 0-inf ug/m3 | D |   |
| `world.chemical.oxygen` | Oxygen concentration | float | 0-100 % | D |   |
| `world.chemical.methane` | Methane concentration | float | 0-inf ppm | D |   |
| `world.chemical.hydrogen_sulfide` | Hydrogen sulfide | float | 0-inf ppm | D |   |
| `world.chemical.radiation_dose_rate` | Radiation dose rate | float | 0-inf uSv/h | D |   |
| `world.chemical.bioaerosol_concentration` | Bioaerosol concentration | float | 0-inf particles/m3 | D |   |
| `world.chemical.pollen_concentration` | Pollen concentration | float | 0-inf grains/m3 | D |   |
| `world.chemical.pathogen_marker_load` | Pathogen marker load | float | 0-inf copies/m3 | D |   |

### Energy Flows — `world.energy` (14 signals, class D)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.energy.grid_frequency` | Grid frequency | float | 0-100 Hz | D |   |
| `world.energy.supply_voltage_rms` | Supply voltage RMS | float | 0-inf V | D |   |
| `world.energy.voltage_unbalance` | Voltage unbalance | float | 0-inf % | D |   |
| `world.energy.supply_current_rms` | Supply current RMS | float | 0-inf A | D |   |
| `world.energy.load_power` | Load active power | float | 0-inf W | D |   |
| `world.energy.reactive_power` | Reactive power | float | -inf-inf var | D |   |
| `world.energy.power_factor` | Power factor | float | -1-1 | D |   |
| `world.energy.harmonic_distortion` | Total harmonic distortion | float | 0-inf % | D |   |
| `world.energy.power_ramp_rate` | Power ramp rate | float | -inf-inf W/s | D |   |
| `world.energy.grid_exchange_power` | Grid import/export power | float | -inf-inf W | D |   |
| `world.energy.local_generation_power` | Local generation power | float | 0-inf W | D |   |
| `world.energy.storage_state_of_charge` | Storage state of charge | float | 0-1 | D |   |
| `world.energy.grid_connected` | Grid connection state | bool | — | S |   |
| `world.energy.outage_duration` | Current outage duration | duration | 0-inf s | D |   |

### Temporal & Cyclical — `world.cyclical` (18 signals, class S)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.cyclical.local_timestamp` | Local timestamp | timestamp | — | S |   |
| `world.cyclical.utc_offset` | UTC offset | float | -14-14 h | S |   |
| `world.cyclical.day_of_week` | Local day of week | enum | — | S |   |
| `world.cyclical.day_of_year` | Local day of year | int | 1-366 | S |   |
| `world.cyclical.local_hour` | Local civil hour | float | 0-24 h | S |   |
| `world.cyclical.daylight_present` | Daylight present | bool | — | S |   |
| `world.cyclical.solar_elevation` | Solar elevation | float | -90-90 deg | S |   |
| `world.cyclical.solar_azimuth` | Solar azimuth | float | 0-360 deg | S |   |
| `world.cyclical.daylight_duration` | Daily daylight duration | duration | 0-24 h | S |   |
| `world.cyclical.lunar_phase` | Lunar phase fraction | float | 0-1 | S | determined |
| `world.cyclical.season` | Local season | enum | — | S |   |
| `world.cyclical.daylight_saving_active` | Daylight-saving active | bool | — | S |   |
| `world.cyclical.business_hours_active` | Configured business hours | bool | — | S |   |
| `world.cyclical.holiday_state` | Holiday calendar state | enum | — | S |   |
| `world.cyclical.scheduled_event_count` | Scheduled activity count | int | 0-inf | N |   |
| `world.cyclical.dominant_period` | Dominant observed period | duration | 0-inf s | N |   |
| `world.cyclical.periodicity_strength` | Periodicity strength | float | 0-1 | N | synthetic |
| `world.cyclical.cycle_deviation` | Cycle baseline deviation | float | 0-inf SD | N |   |

### Economic Indicators — `world.economic` (22 signals, class P)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.economic.electricity_price` | Electricity spot price | float | -inf-inf USD/MWh | P |   |
| `world.economic.natural_gas_price` | Natural gas spot price | float | -inf-inf USD/MMBtu | P |   |
| `world.economic.fuel_price` | Transport fuel price | float | 0-inf USD/L | P |   |
| `world.economic.water_price` | Water unit price | float | 0-inf USD/m3 | P |   |
| `world.economic.compute_price` | Compute unit price | float | 0-inf USD/core-h | P |   |
| `world.economic.storage_price` | Storage unit price | float | 0-inf USD/GB-month | P |   |
| `world.economic.bandwidth_price` | Bandwidth unit price | float | 0-inf USD/GB | P |   |
| `world.economic.carbon_price` | Carbon unit price | float | 0-inf USD/tCO2e | P |   |
| `world.economic.consumer_price_index` | Consumer price index | float | 0-inf index | P |   |
| `world.economic.inflation_rate` | Inflation rate | float | -inf-inf %/yr | P |   |
| `world.economic.exchange_rate` | Configured exchange rate | float | 0-inf quote/base | P |   |
| `world.economic.policy_rate` | Policy interest rate | float | -inf-inf %/yr | P |   |
| `world.economic.market_volatility` | Market volatility | float | 0-inf %/yr | P |   |
| `world.economic.bid_ask_spread` | Bid-ask spread | float | 0-inf bp | P |   |
| `world.economic.market_depth` | Quoted market depth | float | 0-inf USD | P |   |
| `world.economic.transaction_success_rate` | Transaction success rate | float | 0-1 | N |   |
| `world.economic.settlement_latency` | Settlement latency | duration | 0-inf s | N |   |
| `world.economic.active_supplier_count` | Active supplier count | int | 0-inf | N |   |
| `world.economic.supplier_concentration` | Supplier concentration | float | 0-1 | N | synthetic |
| `world.economic.inventory_cover` | Inventory coverage | duration | 0-inf d | N |   |
| `world.economic.procurement_lead_time` | Procurement lead time | duration | 0-inf d | N |   |
| `world.economic.demand_forecast_error` | Demand forecast error | float | 0-inf % | N |   |

### Security & Threat — `world.security` (28 signals, class A)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.security.active_alert_count` | Active security alerts | int | 0-inf | A |   |
| `world.security.critical_alert_fraction` | Critical alert fraction | float | 0-1 | A |   |
| `world.security.alert_rate` | Security alert rate | float | 0-inf alerts/min | A |   |
| `world.security.oldest_alert_age` | Oldest alert age | duration | 0-inf s | A |   |
| `world.security.anomaly_score` | Environment anomaly score | float | 0-1 | A | synthetic |
| `world.security.anomalous_host_count` | Anomalous host count | int | 0-inf | N |   |
| `world.security.intrusion_alert_count` | Active intrusion alerts | int | 0-inf | A |   |
| `world.security.malware_alert_count` | Active malware alerts | int | 0-inf | A |   |
| `world.security.exploit_attempt_rate` | Exploit attempt rate | float | 0-inf events/min | A |   |
| `world.security.authentication_failure_rate` | Authentication failure rate | float | 0-inf events/min | A |   |
| `world.security.authorization_denial_rate` | Authorization denial rate | float | 0-inf events/min | A |   |
| `world.security.privilege_escalation_rate` | Privilege escalation rate | float | 0-inf events/min | A |   |
| `world.security.exfiltration_rate` | Suspected exfiltration rate | float | 0-inf B/s | A |   |
| `world.security.command_control_endpoint_count` | Command-control endpoints | int | 0-inf | A |   |
| `world.security.malicious_ip_count` | Malicious IP count | int | 0-inf | P |   |
| `world.security.vulnerable_asset_count` | Vulnerable asset count | int | 0-inf | N |   |
| `world.security.exposed_service_count` | Externally exposed services | int | 0-inf | N |   |
| `world.security.oldest_patch_age` | Oldest missing-patch age | duration | 0-inf d | N |   |
| `world.security.threat_intelligence_match_count` | Threat-intelligence matches | int | 0-inf | P |   |
| `world.security.perimeter_breach_rate` | Perimeter breach rate | float | 0-inf events/min | A |   |
| `world.security.forced_entry_alarm_count` | Active forced-entry alarms | int | 0-inf | A |   |
| `world.security.tamper_alarm_count` | Active tamper alarms | int | 0-inf | A |   |
| `world.security.unattended_object_count` | Unattended object count | int | 0-inf | A |   |
| `world.security.access_control_fault_count` | Access-control fault count | int | 0-inf | A |   |
| `world.security.surveillance_coverage_fraction` | Surveillance coverage | float | 0-1 | A |   |
| `world.security.open_incident_count` | Open security incidents | int | 0-inf | A |   |
| `world.security.containment_fraction` | Incident containment fraction | float | 0-1 | A |   |
| `world.security.control_health_fraction` | Security control health | float | 0-1 | A | synthetic |

### Emergency & Response — `world.emergency` (18 signals, class A)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.emergency.emergency_level` | Emergency severity level | enum | — | A |   |
| `world.emergency.active_incident_count` | Active emergency incidents | int | 0-inf | A |   |
| `world.emergency.current_alert_age` | Current emergency alert age | duration | 0-inf s | A |   |
| `world.emergency.warning_channel_coverage` | Warning channel coverage | float | 0-1 | A |   |
| `world.emergency.evacuation_order` | Evacuation order active | bool | — | A |   |
| `world.emergency.shelter_order` | Shelter-in-place active | bool | — | A |   |
| `world.emergency.evacuation_zone_area` | Evacuation zone area | float | 0-inf km2 | A |   |
| `world.emergency.evacuation_route_availability` | Evacuation route availability | float | 0-1 | A |   |
| `world.emergency.responder_unit_count` | Available responder units | int | 0-inf | N |   |
| `world.emergency.nearest_responder_eta` | Nearest responder ETA | duration | 0-inf s | N |   |
| `world.emergency.dispatch_latency` | Dispatch latency | duration | 0-inf s | N |   |
| `world.emergency.incident_command_active` | Incident command active | bool | — | A |   |
| `world.emergency.injury_count` | Reported injury count | int | 0-inf | A | [P] |
| `world.emergency.unaccounted_person_count` | Unaccounted person count | int | 0-inf | A | [P] |
| `world.emergency.hospital_demand_ratio` | Hospital demand ratio | float | 0-inf | A | [P] |
| `world.emergency.shelter_demand_ratio` | Shelter demand ratio | float | 0-inf | A | [P] |
| `world.emergency.emergency_supply_endurance` | Emergency supply endurance | duration | 0-inf d | N |   |
| `world.emergency.recovery_progress_fraction` | Recovery progress | float | 0-1 | A | synthetic |

### Regulatory & Compliance — `world.regulatory` (16 signals, class S)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.regulatory.jurisdiction_count` | Applicable jurisdiction count | int | 0-inf | S |   |
| `world.regulatory.primary_jurisdiction` | Primary jurisdiction code | string | — | S |   |
| `world.regulatory.jurisdiction_conflict_count` | Jurisdiction conflict count | int | 0-inf | S |   |
| `world.regulatory.applicable_requirement_count` | Applicable requirement count | int | 0-inf | S |   |
| `world.regulatory.assessment_age` | Compliance assessment age | duration | 0-inf d | A |   |
| `world.regulatory.unmet_requirement_count` | Unmet requirement count | int | 0-inf | A |   |
| `world.regulatory.weighted_compliance_score` | Weighted compliance score | float | 0-1 | A | synthetic |
| `world.regulatory.active_exception_count` | Active exception count | int | 0-inf | A |   |
| `world.regulatory.next_exception_expiry` | Next exception expiry | timestamp | — | S |   |
| `world.regulatory.permit_valid` | Required permit valid | bool | — | S |   |
| `world.regulatory.license_valid` | Required license valid | bool | — | S |   |
| `world.regulatory.data_residency_zone` | Required data residency | enum | — | S |   |
| `world.regulatory.cross_border_allowed` | Cross-border transfer allowed | bool | — | S |   |
| `world.regulatory.maximum_retention_period` | Maximum retention period | duration | 0-inf d | S |   |
| `world.regulatory.consent_required` | Consent required | bool | — | S |   |
| `world.regulatory.consent_coverage_fraction` | Valid consent coverage | float | 0-1 | N | [P] |

### Digital Environment — `world.digital` (39 signals, class N)

| ID | Name | Type | Range | Class | Notes |
|---|---|---|---|---|---|
| `world.digital.cloud_provider_count` | Cloud provider count | int | 0-inf | N |   |
| `world.digital.configured_region_count` | Configured region count | int | 0-inf | N |   |
| `world.digital.healthy_region_fraction` | Healthy region fraction | float | 0-1 | N |   |
| `world.digital.availability_zone_count` | Availability-zone count | int | 0-inf | N |   |
| `world.digital.healthy_zone_fraction` | Healthy zone fraction | float | 0-1 | N |   |
| `world.digital.resource_quota_utilization` | Resource quota utilization | float | 0-1 | N |   |
| `world.digital.compute_instance_count` | Compute instance count | int | 0-inf | N |   |
| `world.digital.healthy_instance_fraction` | Healthy instance fraction | float | 0-1 | N |   |
| `world.digital.cpu_utilization` | Compute CPU utilization | float | 0-100 % | N |   |
| `world.digital.memory_utilization` | Compute memory utilization | float | 0-100 % | N |   |
| `world.digital.disk_utilization` | Instance disk utilization | float | 0-100 % | N |   |
| `world.digital.gpu_utilization` | Compute GPU utilization | float | 0-100 % | N |   |
| `world.digital.running_container_count` | Running container count | int | 0-inf | N |   |
| `world.digital.container_restart_rate` | Container restart rate | float | 0-inf restarts/min | N |   |
| `world.digital.serverless_throttle_rate` | Serverless throttle rate | float | 0-inf events/min | N |   |
| `world.digital.monitored_service_count` | Monitored service count | int | 0-inf | N |   |
| `world.digital.service_availability` | Service availability | float | 0-1 | N |   |
| `world.digital.request_rate` | Service request rate | float | 0-inf requests/s | N |   |
| `world.digital.error_fraction` | Service error fraction | float | 0-1 | N |   |
| `world.digital.latency_p50` | Service latency p50 | duration | 0-inf ms | N |   |
| `world.digital.latency_p95` | Service latency p95 | duration | 0-inf ms | N |   |
| `world.digital.latency_p99` | Service latency p99 | duration | 0-inf ms | N |   |
| `world.digital.healthy_dependency_fraction` | Healthy dependency fraction | float | 0-1 | N |   |
| `world.digital.dependency_failure_rate` | Dependency failure rate | float | 0-inf events/min | N |   |
| `world.digital.queue_depth` | Message queue depth | int | 0-inf | N |   |
| `world.digital.oldest_message_age` | Oldest queued-message age | duration | 0-inf s | N |   |
| `world.digital.consumer_lag` | Message consumer lag | int | 0-inf messages | N |   |
| `world.digital.database_connection_utilization` | Database connection utilization | float | 0-1 | N |   |
| `world.digital.database_replica_lag` | Database replica lag | duration | 0-inf s | N |   |
| `world.digital.managed_storage_capacity` | Managed storage capacity | float | 0-inf GB | N |   |
| `world.digital.storage_free_fraction` | Managed storage free fraction | float | 0-1 | N |   |
| `world.digital.newest_data_age` | Newest data age | duration | 0-inf s | N |   |
| `world.digital.schema_drift_count` | Schema drift count | int | 0-inf | N |   |
| `world.digital.successful_backup_age` | Newest successful backup age | duration | 0-inf s | N |   |
| `world.digital.deployment_age` | Current deployment age | duration | 0-inf s | N |   |
| `world.digital.deployment_failure_rate` | Deployment failure rate | float | 0-inf failures/d | N |   |
| `world.digital.rollback_available` | Rollback artifact available | bool | — | S |   |
| `world.digital.configuration_drift_count` | Configuration drift count | int | 0-inf | N |   |
| `world.digital.next_certificate_expiry` | Next certificate expiry | timestamp | — | S |   |

