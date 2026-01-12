---
hide:
  - toc
---

# The Context Tensor

*The Geometry of Trust in a Digital Universe*

Trust isn't a yes/no flag. It's a field. The **Context Tensor** is the mathematical structure that captures the real-time state of trust for any interaction—its weight, direction, and volatility—so authorization can respond like physics, not policy. Instead of static rules, KTP evaluates a living vector space that changes as conditions change.

<div id="tensor-viz-container">
  <div class="tensor-viz-header">
    <h4>Live Trust Geometry</h4>
    <p>E<sub>base</sub> → Risk Deflation → E<sub>trust</sub></p>
  </div>
  <canvas id="tensor-canvas"></canvas>
  <div class="tensor-viz-scores">
    <div class="tensor-score tensor-score--base">
      <span class="tensor-score-label">E<sub>base</sub></span>
      <span class="tensor-score-value" id="tensor-ebase">--</span>
    </div>
    <div class="tensor-score tensor-score--risk">
      <span class="tensor-score-label">Risk</span>
      <span class="tensor-score-value" id="tensor-risk">--%</span>
    </div>
    <div class="tensor-score tensor-score--trust">
      <span class="tensor-score-label">E<sub>trust</sub></span>
      <span class="tensor-score-value" id="tensor-etrust">--</span>
    </div>
  </div>
  <div class="tensor-viz-hint">Click a dimension to explore</div>
  <div class="tensor-viz-legend">
    <span><span class="dot"></span>Performance</span>
    <span><span class="dot dot--risk"></span>Risk</span>
    <span><span class="dot dot--soul"></span>Soul</span>
  </div>
</div>

## The Seven Dimensions

The Context Tensor is expressed across seven primary dimensions. Click any dimension to explore its mechanics.

<div class="dimension-cards-grid">
  <a href="#__tabbed_2_1" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">M</span><span class="mono-secondary">a</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Mass</strong>
      <span>The weight of observed behavior</span>
    </div>
  </a>
  <a href="#__tabbed_2_2" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">M</span><span class="mono-secondary">o</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Momentum</strong>
      <span>Velocity of trust change</span>
    </div>
  </a>
  <a href="#__tabbed_2_3" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">I</span><span class="mono-secondary">n</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Inertia</strong>
      <span>Resistance to sudden shifts</span>
    </div>
  </a>
  <a href="#__tabbed_2_4" class="dimension-card-mini dimension-card-mini--heat">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">H</span><span class="mono-secondary">e</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Heat</strong>
      <span>Environmental stress and friction</span>
    </div>
  </a>
  <a href="#__tabbed_2_5" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">T</span><span class="mono-secondary">i</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Time</strong>
      <span>Temporal context and decay</span>
    </div>
  </a>
  <a href="#__tabbed_2_6" class="dimension-card-mini">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">O</span><span class="mono-secondary">b</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Observer</strong>
      <span>Who is watching, and how reliably</span>
    </div>
  </a>
  <a href="#__tabbed_2_7" class="dimension-card-mini dimension-card-mini--soul">
    <div class="dimension-card-mini-mono">
      <span class="mono-primary">S</span><span class="mono-secondary">o</span>
    </div>
    <div class="dimension-card-mini-content">
      <strong>Soul</strong>
      <span>Constitutional constraints</span>
    </div>
  </a>
</div>

<p class="dimension-cards-note">For the full dimensional breakdown (1,707 measurements), see <a href="../../rfcs/ktp-tensors/">KTP-Tensors RFC</a>.</p>

## Incoming Signals { #incoming-signals }

The Context Tensor doesn't operate in a vacuum—it's fed by a continuous stream of **live telemetry** from across your infrastructure. These signals are normalized, classified through ARQ, and projected into the seven-dimensional trust geometry.

<div class="signal-flow-visual ktp-animate">
  <div class="signal-flow-title">
    <h4>Signal Ingestion Pipeline</h4>
    <p>From raw telemetry to trust geometry</p>
  </div>
  <div class="signal-flow-stages">
    <div class="signal-flow-stage">
      <div class="signal-flow-count">1,707</div>
      <div class="signal-flow-label">Discrete Signals</div>
    </div>
    <div class="signal-flow-arrow">→</div>
    <div class="signal-flow-stage">
      <div class="signal-flow-count">4</div>
      <div class="signal-flow-label">Categories</div>
    </div>
    <div class="signal-flow-arrow">→</div>
    <div class="signal-flow-stage">
      <div class="signal-flow-count">3</div>
      <div class="signal-flow-label">ARQ Classes</div>
    </div>
    <div class="signal-flow-arrow">→</div>
    <div class="signal-flow-stage">
      <div class="signal-flow-count">7</div>
      <div class="signal-flow-label">Dimensions</div>
    </div>
  </div>
</div>

### Signal Categories

Every signal entering the system falls into one of four categories. Each category has distinct sources, update frequencies, and trust implications.

<div class="signal-category-cards">
  <a href="#__tabbed_1_1" class="signal-category-card">
    <div class="signal-category-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="32" height="32"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
    </div>
    <div class="signal-category-content">
      <div class="signal-category-header">
        <div class="signal-category-mono">
          <span class="mono-primary">P</span><span class="mono-secondary">a</span>
        </div>
        <strong>Packets</strong>
      </div>
      <p>Network and infrastructure telemetry—the pulse of connectivity</p>
      <div class="signal-category-meta">
        <span class="signal-count">~250 signals</span>
        <span class="signal-freq">Real-time</span>
      </div>
    </div>
  </a>
  <a href="#__tabbed_1_2" class="signal-category-card">
    <div class="signal-category-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="32" height="32"><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>
    </div>
    <div class="signal-category-content">
      <div class="signal-category-header">
        <div class="signal-category-mono">
          <span class="mono-primary">L</span><span class="mono-secondary">o</span>
        </div>
        <strong>Logs & Events</strong>
      </div>
      <p>Security events and behavioral patterns—the narrative of activity</p>
      <div class="signal-category-meta">
        <span class="signal-count">~120 signals</span>
        <span class="signal-freq">Event-driven</span>
      </div>
    </div>
  </a>
  <a href="#__tabbed_1_3" class="signal-category-card">
    <div class="signal-category-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="32" height="32"><path d="M19.88 18.47c.44-.7.7-1.51.7-2.39 0-2.49-2.01-4.5-4.5-4.5s-4.5 2.01-4.5 4.5 2.01 4.5 4.5 4.5c.88 0 1.69-.26 2.39-.7L21.58 23 23 21.58l-3.12-3.11zm-3.8.11c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5zm-.36-8.5c-.74.02-1.45.18-2.1.45l-.55-.83-3.8 6.18-3.01-3.52-3.63 5.81L1 17l5-8 3 3.5L13 6l2.72 4.08zm2.59.5c-.64-.28-1.33-.45-2.05-.49L21.38 2 23 3.18l-4.69 7.4z"/></svg>
    </div>
    <div class="signal-category-content">
      <div class="signal-category-header">
        <div class="signal-category-mono">
          <span class="mono-primary">M</span><span class="mono-secondary">e</span>
        </div>
        <strong>Metrics</strong>
      </div>
      <p>Performance and saturation indicators—the stress gauge</p>
      <div class="signal-category-meta">
        <span class="signal-count">~50 signals</span>
        <span class="signal-freq">Periodic</span>
      </div>
    </div>
  </a>
  <a href="#__tabbed_1_4" class="signal-category-card">
    <div class="signal-category-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="32" height="32"><path d="M23 12l-2.44-2.79.34-3.69-3.61-.82-1.89-3.2L12 2.96 8.6 1.5 6.71 4.69 3.1 5.5l.34 3.7L1 12l2.44 2.79-.34 3.7 3.61.82 1.89 3.2L12 21.04l3.4 1.46 1.89-3.2 3.61-.82-.34-3.69L23 12zm-12.91 4.72l-3.8-3.81 1.48-1.48 2.32 2.33 5.85-5.87 1.48 1.48-7.33 7.35z"/></svg>
    </div>
    <div class="signal-category-content">
      <div class="signal-category-header">
        <div class="signal-category-mono">
          <span class="mono-primary">A</span><span class="mono-secondary">t</span>
        </div>
        <strong>Attestations</strong>
      </div>
      <p>Cryptographic proofs and human approvals—the trust anchors</p>
      <div class="signal-category-meta">
        <span class="signal-count">~30 signals</span>
        <span class="signal-freq">On-demand</span>
      </div>
    </div>
  </a>
</div>

### Category Deep Dive

=== "Packets"

    <div class="signal-tab-hero">
      <div class="signal-tab-mono">
        <span class="mono-primary">P</span><span class="mono-secondary">a</span>
      </div>
      <div class="signal-tab-title">
        <strong>Packets</strong>
        <em>The pulse of the network</em>
      </div>
    </div>

    #### What It Measures

    Packet telemetry captures the **physical and logical reality of network connectivity**. Every TCP handshake, every dropped packet, every millisecond of latency tells a story about reachability, stability, and infrastructure health.

    This is the most fundamental signal category—if packets aren't flowing, nothing else matters. Packet signals form the bedrock of Accessibility scoring and provide early warning of infrastructure degradation.

    #### Why It Matters

    Network telemetry is **impossible to fake at scale**. An attacker can forge credentials, but they can't hide the latency of routing through Tor. They can compromise an endpoint, but the C2 beaconing pattern shows up in flow data. Packet signals provide ground truth that higher-layer deception can't mask.

    #### Key Signals

    <div class="signal-key-grid">
      <div class="signal-key-item">
        <strong>Latency</strong>
        <span>Round-trip time, P50/P95/P99 percentiles</span>
      </div>
      <div class="signal-key-item">
        <strong>Packet Loss</strong>
        <span>Drop rate, loss spikes, path-specific loss</span>
      </div>
      <div class="signal-key-item">
        <strong>Throughput</strong>
        <span>Bytes/sec, bandwidth utilization</span>
      </div>
      <div class="signal-key-item">
        <strong>Handshake Success</strong>
        <span>TCP SYN/ACK completion rate</span>
      </div>
      <div class="signal-key-item">
        <strong>Retransmissions</strong>
        <span>Packet resend rate, congestion indicators</span>
      </div>
      <div class="signal-key-item">
        <strong>Flow Duration</strong>
        <span>Connection longevity, session patterns</span>
      </div>
      <div class="signal-key-item">
        <strong>Path Changes</strong>
        <span>Route shifts, next-hop variations</span>
      </div>
      <div class="signal-key-item">
        <strong>Link Status</strong>
        <span>Interface up/down, flapping detection</span>
      </div>
    </div>

    #### Signal Sources

    <div class="signal-sources">
      <span class="signal-source">NetFlow/IPFIX</span>
      <span class="signal-source">sFlow</span>
      <span class="signal-source">SNMP</span>
      <span class="signal-source">Cloud VPC Flow Logs</span>
      <span class="signal-source">SD-WAN Telemetry</span>
      <span class="signal-source">Wireless Controllers</span>
    </div>

    #### ARQ Mapping

    <div class="signal-arq-bars">
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Accessibility</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--high" style="width: 40%;"></div>
        </div>
        <span class="signal-arq-pct">40%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Retainability</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--med" style="width: 30%;"></div>
        </div>
        <span class="signal-arq-pct">30%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Quality</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--med" style="width: 30%;"></div>
        </div>
        <span class="signal-arq-pct">30%</span>
      </div>
    </div>

    #### Tensor Projection

    <div class="signal-tensor-projection">
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Primary</span>
        <a href="#__tabbed_2_1" class="dimension-tag">Mass</a>
        <a href="#__tabbed_2_5" class="dimension-tag">Time</a>
      </div>
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Secondary</span>
        <a href="#__tabbed_2_2" class="dimension-tag dimension-tag--secondary">Momentum</a>
      </div>
    </div>

    ??? abstract "Full Signal Catalog (~250 signals)"

        **Layer 4: Transport**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `src_port` | Client ephemeral port | Port exhaustion, fixed port detection, scan patterns |
        | `dest_port` | Service port | Service distribution, dark port access, scan detection |
        | `tcp_flags` | SYN/ACK/FIN/RST | SYN flood, RST rate, null/xmas scans, handshake completion |
        | `window_size` | TCP receive window | Zero window, window scaling, retransmission correlation |
        | `retransmission_rate` | Packets resent | Spike detection, high-retransmit hosts, global trends |

        **Layer 3.5: Flow**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `flow_bytes_in/out` | Byte counts | Volume spikes, exfiltration detection, asymmetric flows |
        | `flow_packets` | Packet count per flow | Small packet floods, scan detection, avg packet size |
        | `flow_duration` | Connection length | Long-lived flows, C2 beaconing, tunnel detection |
        | `flow_start_time` | Initiation timestamp | Off-hours activity, burst detection, time correlation |
        | `application_id` | DPI-identified app | Shadow IT, new application alerts, usage trends |

        **Layer 3: Network**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `src_ip` / `dest_ip` | Source/destination | Top talkers, reputation, beaconing, new host detection |
        | `latency` | Round-trip time | P50/P95/P99, anomaly detection, trend analysis |
        | `packet_loss` | Drop indication | Loss rate/spikes, path-specific loss, P99 loss |
        | `hop_count` | TTL-derived | Path length, routing changes, excessive hops |
        | `bgp_peer_state` | Routing health | Flap detection, idle alerts, prefix changes |

        **Layer 2: Data Link**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `src_mac` | Asset identifier | New/rogue MAC detection, spoofing, OUI distribution |
        | `vlan_id` | Broadcast domain | VLAN hopping, unused VLAN detection |
        | `interface` | Physical port | Utilization, flapping, broadcast storms, errors |
        | `link_status` | UP/DOWN state | Availability, flapping, MTTR |

        **Layer 1: Physical**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `rssi` / `snr` | WiFi signal quality | Coverage holes, low-signal clients, interference |
        | `channel` | WiFi channel | Utilization, co-channel interference, DFS events |
        | `optical_rx_power` | Fiber light levels | Power degradation, link margin, asymmetry |
        | `transceiver_temp` | SFP temperature | Overheating alerts, thermal trends |
        | `poe_power_draw` | PoE consumption | Budget usage, power anomalies |

=== "Logs & Events"

    <div class="signal-tab-hero">
      <div class="signal-tab-mono">
        <span class="mono-primary">L</span><span class="mono-secondary">o</span>
      </div>
      <div class="signal-tab-title">
        <strong>Logs & Events</strong>
        <em>The narrative of activity</em>
      </div>
    </div>

    #### What It Measures

    Log telemetry captures the **semantic story of what's happening** across identities, applications, and endpoints. Authentication attempts, policy violations, configuration changes, and security events all flow through this category.

    Unlike packet data (which shows *that* something happened), logs show *what* happened and *who* did it. This category is essential for behavioral analysis and detecting patterns that span multiple sessions.

    #### Why It Matters

    Logs are where **intent becomes visible**. A failed login is just noise—but 50 failed logins from 50 different IPs against the same account is credential stuffing. Logs provide the context to distinguish between accidents and attacks, mistakes and malice.

    Security events in this category directly influence Heat (anomalies increase friction) and Observer (audit coverage affects confidence).

    #### Key Signals

    <div class="signal-key-grid">
      <div class="signal-key-item">
        <strong>Auth Failures</strong>
        <span>Failed logins, lockouts, MFA denials</span>
      </div>
      <div class="signal-key-item">
        <strong>Privilege Changes</strong>
        <span>Role escalation, permission grants</span>
      </div>
      <div class="signal-key-item">
        <strong>Impossible Travel</strong>
        <span>Geo-velocity anomalies</span>
      </div>
      <div class="signal-key-item">
        <strong>Policy Violations</strong>
        <span>WAF blocks, ACL denials, DLP triggers</span>
      </div>
      <div class="signal-key-item">
        <strong>Process Execution</strong>
        <span>Command lines, parent-child trees</span>
      </div>
      <div class="signal-key-item">
        <strong>Config Changes</strong>
        <span>Registry mods, file changes, drift</span>
      </div>
      <div class="signal-key-item">
        <strong>Session Patterns</strong>
        <span>Duration, concurrency, churn</span>
      </div>
      <div class="signal-key-item">
        <strong>API Abuse</strong>
        <span>Rate limits, invalid keys, shadow APIs</span>
      </div>
    </div>

    #### Signal Sources

    <div class="signal-sources">
      <span class="signal-source">SIEM Platforms</span>
      <span class="signal-source">IdP / IAM Logs</span>
      <span class="signal-source">EDR/XDR</span>
      <span class="signal-source">Cloud Audit Logs</span>
      <span class="signal-source">WAF/Firewall Logs</span>
      <span class="signal-source">Application Logs</span>
    </div>

    #### ARQ Mapping

    <div class="signal-arq-bars">
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Accessibility</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--low" style="width: 20%;"></div>
        </div>
        <span class="signal-arq-pct">20%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Retainability</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--med" style="width: 30%;"></div>
        </div>
        <span class="signal-arq-pct">30%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Quality</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--high" style="width: 50%;"></div>
        </div>
        <span class="signal-arq-pct">50%</span>
      </div>
    </div>

    #### Tensor Projection

    <div class="signal-tensor-projection">
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Primary</span>
        <a href="#__tabbed_2_4" class="dimension-tag dimension-tag--heat">Heat</a>
        <a href="#__tabbed_2_6" class="dimension-tag">Observer</a>
      </div>
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Secondary</span>
        <a href="#__tabbed_2_3" class="dimension-tag dimension-tag--secondary">Inertia</a>
      </div>
    </div>

    ??? abstract "Full Signal Catalog (~120 signals)"

        **Layer 8: Identity**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `user_id` | Human/machine identity | Auth volume, failed login rate, concurrent sessions |
        | `role` | RBAC assignment | Privilege escalation, toxic combinations, dormant usage |
        | `geo_location` | Access location | Impossible travel, new country, high-risk country |
        | `device_id` | Endpoint identifier | Device trust score, new device rate, jailbreak detection |

        **Layer 7: Application**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `http_method` | GET/POST/PUT/DELETE | Method distribution, unusual usage, high-volume POST |
        | `http_status` | Response codes | 5xx error rate, 403 denials, 404 spikes |
        | `url_path` | Resource accessed | Path traversal, admin access, sensitive files |
        | `user_agent` | Client string | Rare agents, bot detection, spoofing |

        **Layer 6.5: API**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `api_endpoint` | API route | Usage patterns, deprecated endpoints, shadow APIs |
        | `api_key_id` | Client identifier | Invalid key rate, concurrent usage, key rotation |
        | `rate_limit_status` | Throttling events | Quota consumption, abusive clients |

        **Layer 6: Presentation**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `tls_version` | Protocol version | Legacy protocol usage, downgrade attacks |
        | `cipher_suite` | Encryption algo | Weak cipher usage, PFS adoption |

        **Layer 5: Session**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `session_id` | Session identifier | Fixation, churn, concurrent sessions |
        | `session_duration` | Active length | Short/long sessions, timeout rate |
        | `login_status` | Auth result | Brute force, credential stuffing |

        **Layer 0: Endpoint/Host**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `process_name` | Executable | Rare process, living-off-the-land techniques |
        | `process_hash` | File hash | Malware match, unknown hashes, first-seen |
        | `process_cmd_line` | Full command | Encoded commands, suspicious patterns |
        | `registry_key` | Windows registry | Run key mods, persistence detection |
        | `file_operation` | File changes | Mass changes, sensitive file access |

=== "Metrics"

    <div class="signal-tab-hero">
      <div class="signal-tab-mono">
        <span class="mono-primary">M</span><span class="mono-secondary">e</span>
      </div>
      <div class="signal-tab-title">
        <strong>Metrics</strong>
        <em>The stress gauge</em>
      </div>
    </div>

    #### What It Measures

    Metrics telemetry captures the **quantitative health of infrastructure**. CPU utilization, memory pressure, queue depths, error rates, and saturation levels all reveal whether systems are operating within safe bounds or approaching failure.

    These signals are periodic snapshots rather than event-driven—they show the state of the system at regular intervals, enabling trend analysis and capacity planning.

    #### Why It Matters

    Infrastructure stress directly correlates with trust risk. A service running at 95% CPU has less capacity to validate requests properly. A queue backing up might indicate an attack or a failing dependency. Metrics provide the **early warning system** before events occur.

    Metrics heavily influence Heat (saturation increases friction) and Momentum (degradation trends signal declining trust trajectory).

    #### Key Signals

    <div class="signal-key-grid">
      <div class="signal-key-item">
        <strong>CPU Utilization</strong>
        <span>Processing pressure, core saturation</span>
      </div>
      <div class="signal-key-item">
        <strong>Memory Pressure</strong>
        <span>Heap usage, swap activity, OOM risk</span>
      </div>
      <div class="signal-key-item">
        <strong>Queue Depth</strong>
        <span>Backlog size, processing lag</span>
      </div>
      <div class="signal-key-item">
        <strong>Error Rate</strong>
        <span>5xx responses, exceptions, timeouts</span>
      </div>
      <div class="signal-key-item">
        <strong>Throughput</strong>
        <span>Requests/sec, transactions/sec</span>
      </div>
      <div class="signal-key-item">
        <strong>Saturation</strong>
        <span>Resource exhaustion indicators</span>
      </div>
      <div class="signal-key-item">
        <strong>Response Time</strong>
        <span>P50/P95/P99 latency distributions</span>
      </div>
      <div class="signal-key-item">
        <strong>Connection Pools</strong>
        <span>Pool exhaustion, wait times</span>
      </div>
    </div>

    #### Signal Sources

    <div class="signal-sources">
      <span class="signal-source">Prometheus</span>
      <span class="signal-source">CloudWatch</span>
      <span class="signal-source">Datadog</span>
      <span class="signal-source">StatsD</span>
      <span class="signal-source">OpenTelemetry</span>
      <span class="signal-source">APM Platforms</span>
    </div>

    #### ARQ Mapping

    <div class="signal-arq-bars">
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Accessibility</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--med" style="width: 30%;"></div>
        </div>
        <span class="signal-arq-pct">30%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Retainability</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--med" style="width: 30%;"></div>
        </div>
        <span class="signal-arq-pct">30%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Quality</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--high" style="width: 40%;"></div>
        </div>
        <span class="signal-arq-pct">40%</span>
      </div>
    </div>

    #### Tensor Projection

    <div class="signal-tensor-projection">
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Primary</span>
        <a href="#__tabbed_2_4" class="dimension-tag dimension-tag--heat">Heat</a>
        <a href="#__tabbed_2_2" class="dimension-tag">Momentum</a>
      </div>
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Secondary</span>
        <a href="#__tabbed_2_1" class="dimension-tag dimension-tag--secondary">Mass</a>
      </div>
    </div>

    ??? abstract "Full Signal Catalog (~50 signals)"

        **Compute Resources**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `cpu_utilization` | Processor load | Average, peak, per-core distribution |
        | `memory_usage` | RAM consumption | Heap/stack, swap activity, OOM proximity |
        | `disk_io` | Storage throughput | IOPS, latency, queue depth |
        | `network_io` | NIC throughput | Bytes in/out, packet rate |

        **Application Health**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `request_rate` | Incoming traffic | Requests/sec, burst detection |
        | `error_rate` | Failure ratio | 5xx rate, exception frequency |
        | `response_time` | Latency | P50/P95/P99, anomaly detection |
        | `queue_depth` | Backlog | Size, growth rate, drain time |

        **Trust Dynamics**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `throughput` | Session velocity | Sessions/sec processing rate |
        | `trust_mass` | Friction capacity | 100 - Accumulated Risk |
        | `env_friction` | Instantaneous risk | Current environmental resistance (0-100) |
        | `accumulated_risk` | Session risk | Total risk accrued during session |

        **Infrastructure**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `connection_pool` | Pool status | Active/idle/waiting counts |
        | `thread_count` | Concurrency | Active threads, pool exhaustion |
        | `gc_pressure` | Garbage collection | Pause time, frequency, heap churn |

=== "Attestations"

    <div class="signal-tab-hero signal-tab-hero--soul">
      <div class="signal-tab-mono">
        <span class="mono-primary">A</span><span class="mono-secondary">t</span>
      </div>
      <div class="signal-tab-title">
        <strong>Attestations</strong>
        <em>The trust anchors</em>
      </div>
    </div>

    #### What It Measures

    Attestation telemetry captures **cryptographic proofs and human validations**. Digital signatures, audit certifications, provenance trails, and explicit approvals all provide external verification that grounds trust in something more than self-reported behavior.

    This is the only signal category that can directly influence the Soul dimension—attestations carry the weight of constitutional constraints, jurisdictional requirements, and consent verification.

    #### Why It Matters

    Attestations provide **trust that cannot be fabricated by the subject being evaluated**. An agent can manipulate its own logs, but it can't forge a signature from a trusted third party. Attestations anchor the trust calculation in external reality.

    When multiple independent attesters agree, confidence compounds. When attestations are missing or stale, Observer confidence drops. When constitutional constraints are attested (GDPR consent, TK Labels), Soul gates engage.

    #### Key Signals

    <div class="signal-key-grid">
      <div class="signal-key-item">
        <strong>Digital Signatures</strong>
        <span>Cryptographic proofs of origin</span>
      </div>
      <div class="signal-key-item">
        <strong>Audit Certifications</strong>
        <span>SOC2, ISO 27001, third-party audits</span>
      </div>
      <div class="signal-key-item">
        <strong>Provenance Trails</strong>
        <span>Chain of custody, origin verification</span>
      </div>
      <div class="signal-key-item">
        <strong>Human Approvals</strong>
        <span>Manual authorizations, break-glass</span>
      </div>
      <div class="signal-key-item">
        <strong>Consent Records</strong>
        <span>GDPR consent, opt-in/opt-out state</span>
      </div>
      <div class="signal-key-item">
        <strong>Sovereignty Markers</strong>
        <span>TK Labels, OCAP/CARE, geofences</span>
      </div>
      <div class="signal-key-item">
        <strong>Peer Attestations</strong>
        <span>Cross-agent vouching, mesh trust</span>
      </div>
      <div class="signal-key-item">
        <strong>Time Anchors</strong>
        <span>Notarization, timestamping</span>
      </div>
    </div>

    #### Signal Sources

    <div class="signal-sources">
      <span class="signal-source">PKI / Certificate Authorities</span>
      <span class="signal-source">Audit Platforms</span>
      <span class="signal-source">Consent Management</span>
      <span class="signal-source">Blockchain / Notary</span>
      <span class="signal-source">Identity Providers</span>
      <span class="signal-source">Governance Systems</span>
    </div>

    #### ARQ Mapping

    <div class="signal-arq-bars">
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Accessibility</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--low" style="width: 10%;"></div>
        </div>
        <span class="signal-arq-pct">10%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Retainability</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--low" style="width: 20%;"></div>
        </div>
        <span class="signal-arq-pct">20%</span>
      </div>
      <div class="signal-arq-bar">
        <span class="signal-arq-label">Quality</span>
        <div class="signal-arq-track">
          <div class="signal-arq-fill signal-arq-fill--high" style="width: 70%;"></div>
        </div>
        <span class="signal-arq-pct">70%</span>
      </div>
    </div>

    #### Tensor Projection

    <div class="signal-tensor-projection">
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Primary</span>
        <a href="#__tabbed_2_6" class="dimension-tag">Observer</a>
        <a href="#__tabbed_2_7" class="dimension-tag dimension-tag--soul">Soul</a>
      </div>
      <div class="signal-tensor-group">
        <span class="signal-tensor-label">Secondary</span>
        <a href="#__tabbed_2_3" class="dimension-tag dimension-tag--secondary">Inertia</a>
      </div>
    </div>

    ??? abstract "Full Signal Catalog (~30 signals)"

        **Cryptographic Proofs**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `signature_valid` | Digital signature verification | Signer identity, algorithm strength, timestamp |
        | `certificate_chain` | PKI chain validation | Chain completeness, revocation status |
        | `hash_verification` | Content integrity | Match status, algorithm used |

        **Audit & Compliance**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `audit_certification` | Third-party audit status | Certification type, expiry, scope |
        | `compliance_attestation` | Regulatory compliance | Standard (SOC2, ISO, etc.), last audit date |
        | `policy_attestation` | Internal policy compliance | Policy version, attestation freshness |

        **Consent & Sovereignty**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `consent_state` | User consent record | Consent type, timestamp, scope |
        | `data_sovereignty` | Jurisdictional constraints | TK Labels, OCAP/CARE markers, geofence status |
        | `opt_out_flags` | Explicit denials | Scope of denial, timestamp |

        **Peer & Human Validation**

        | Signal | Description | Derived Metrics |
        |--------|-------------|-----------------|
        | `peer_attestation` | Cross-agent vouching | Attester trust level, attestation count |
        | `human_approval` | Manual authorization | Approver identity, approval scope, expiry |
        | `break_glass_event` | Emergency override | Override reason, authorizer, audit trail |

## The Signal Pipeline: From Telemetry to Trust { #signal-pipeline }

Before signals reach the seven-dimensional tensor, they pass through a classification layer called **ARQ** — the foundational physics of digital experience.

<div class="arq-pipeline ktp-animate">
  <div class="arq-pipeline-title">
    <h4>The Trust Pipeline</h4>
    <p>Raw signals → Classification → Projection → Score</p>
  </div>
  <div class="arq-pipeline-flow">
    <div class="arq-pipeline-stage arq-pipeline-stage--input">
      <div class="arq-pipeline-stage-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M3 17V19H5V17H3M7 17V19H9V17H7M11 17V19H13V17H11M3 13V15H5V13H3M7 13V15H9V13H7M11 13V15H13V13H11M15 13V15H17V13H15M3 9V11H5V9H3M7 9V11H9V9H7M11 9V11H13V9H11M15 9V11H17V9H15M19 9V11H21V9H19M3 5V7H5V5H3M7 5V7H9V5H7M11 5V7H13V5H11M15 5V7H17V5H15M19 5V7H21V5H19M15 17V19H17V17H15M19 13V15H21V13H19"/></svg>
      </div>
      <div class="arq-pipeline-stage-label">Telemetry</div>
      <div class="arq-pipeline-stage-sub">Packets, Logs,<br>Metrics, Attestations</div>
    </div>
    <div class="arq-pipeline-arrow">→</div>
    <div class="arq-pipeline-stage arq-pipeline-stage--arq">
      <div class="arq-pipeline-stage-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M14.76 20.83L17.6 18L14.76 15.17L16.17 13.76L19 16.57L21.83 13.76L23.24 15.17L20.43 18L23.24 20.83L21.83 22.24L19 19.41L16.17 22.24L14.76 20.83M12 12V19.88C12.04 20.18 11.94 20.5 11.71 20.71C11.32 21.1 10.69 21.1 10.3 20.71L8.29 18.7C8.06 18.47 7.96 18.16 8 17.87V12H7.97L2.21 4.62C1.87 4.19 1.95 3.56 2.38 3.22C2.57 3.08 2.78 3 3 3H17C17.22 3 17.43 3.08 17.62 3.22C18.05 3.56 18.13 4.19 17.79 4.62L12.03 12H12Z"/></svg>
      </div>
      <div class="arq-pipeline-stage-label">ARQ Classify</div>
      <div class="arq-pipeline-stage-sub">Accessibility<br>Retainability, Quality</div>
    </div>
    <div class="arq-pipeline-arrow">→</div>
    <div class="arq-pipeline-stage arq-pipeline-stage--tensor">
      <div class="arq-pipeline-stage-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28">
          <!-- 3D Tensor/Cube with axes -->
          <path d="M21 16.5C21 16.88 20.79 17.21 20.47 17.38L12.57 21.82C12.41 21.94 12.21 22 12 22C11.79 22 11.59 21.94 11.43 21.82L3.53 17.38C3.21 17.21 3 16.88 3 16.5V7.5C3 7.12 3.21 6.79 3.53 6.62L11.43 2.18C11.59 2.06 11.79 2 12 2C12.21 2 12.41 2.06 12.57 2.18L20.47 6.62C20.79 6.79 21 7.12 21 7.5V16.5Z" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <path d="M12 22V12M3 7.5L12 12L21 7.5" fill="none" stroke="currentColor" stroke-width="1.5"/>
          <circle cx="12" cy="12" r="2" fill="currentColor"/>
        </svg>
      </div>
      <div class="arq-pipeline-stage-label">Context Tensor</div>
      <div class="arq-pipeline-stage-sub">Multidimensional<br>trust geometry</div>
    </div>
    <div class="arq-pipeline-arrow">→</div>
    <div class="arq-pipeline-stage arq-pipeline-stage--output">
      <div class="arq-pipeline-stage-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="28" height="28"><path d="M10 17L6 13L7.41 11.59L10 14.17L16.59 7.58L18 9M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1Z"/></svg>
      </div>
      <div class="arq-pipeline-stage-label">Trust Score</div>
      <div class="arq-pipeline-stage-sub">E = 0–100<br>Action permitted?</div>
    </div>
  </div>
</div>

### The Three Foundational Questions

Every signal entering the system is classified by three fundamental questions about the digital experience it represents:

<div class="arq-cards">
  <div class="arq-card">
    <div class="arq-card-header">
      <div class="arq-monogram">
        <span class="mono-primary">A</span><span class="mono-secondary">c</span>
      </div>
      <div class="arq-card-title">
        <strong>Accessibility</strong>
        <em>Reachability</em>
      </div>
    </div>
    <div class="arq-card-question">"Can we reach it?"</div>
    <div class="arq-card-description">
      Measures whether the resource, agent, or service is reachable. Latency, packet loss, handshake success, and path availability all contribute. If you can't reach it, nothing else matters.
    </div>
    <div class="arq-card-feeds">
      <span class="arq-card-feeds-label">Projects into</span>
      <span class="arq-feed-tag">Mass</span>
      <span class="arq-feed-tag">Time</span>
    </div>
  </div>
  <div class="arq-card">
    <div class="arq-card-header">
      <div class="arq-monogram">
        <span class="mono-primary">R</span><span class="mono-secondary">e</span>
      </div>
      <div class="arq-card-title">
        <strong>Retainability</strong>
        <em>Stability</em>
      </div>
    </div>
    <div class="arq-card-question">"Can we hold it?"</div>
    <div class="arq-card-description">
      Measures whether the connection can be sustained. Session stability, connection drops, retry rates, and consistency over time. Reaching something once means little if you can't stay connected.
    </div>
    <div class="arq-card-feeds">
      <span class="arq-card-feeds-label">Projects into</span>
      <span class="arq-feed-tag">Inertia</span>
      <span class="arq-feed-tag">Momentum</span>
    </div>
  </div>
  <div class="arq-card">
    <div class="arq-card-header">
      <div class="arq-monogram">
        <span class="mono-primary">Q</span><span class="mono-secondary">u</span>
      </div>
      <div class="arq-card-title">
        <strong>Quality</strong>
        <em>Fidelity</em>
      </div>
    </div>
    <div class="arq-card-question">"Is it good?"</div>
    <div class="arq-card-description">
      Measures the integrity and performance of the interaction. Error rates, throughput, security signals, and validation status. A stable connection that delivers garbage is still a failure.
    </div>
    <div class="arq-card-feeds">
      <span class="arq-card-feeds-label">Projects into</span>
      <span class="arq-feed-tag arq-feed-tag--heat">Heat</span>
      <span class="arq-feed-tag">Observer</span>
    </div>
  </div>
</div>

### ARQ-to-Tensor Projection Matrix

Each ARQ classification feeds specific tensor dimensions. The mapping is not 1:1 — signals often influence multiple dimensions with different weights.

<div class="arq-matrix">
  <table>
    <thead>
      <tr>
        <th>ARQ Input</th>
        <th>Primary Dimensions</th>
        <th>Secondary</th>
        <th>Signal Examples</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Accessibility</td>
        <td><span class="dimension-tag">Mass</span> <span class="dimension-tag">Time</span></td>
        <td>Momentum</td>
        <td>Latency, packet loss, reachability, handshake success</td>
      </tr>
      <tr>
        <td>Retainability</td>
        <td><span class="dimension-tag">Inertia</span> <span class="dimension-tag">Momentum</span></td>
        <td>Mass</td>
        <td>Session stability, connection drops, retry rates</td>
      </tr>
      <tr>
        <td>Quality</td>
        <td><span class="dimension-tag dimension-tag--heat">Heat</span> <span class="dimension-tag">Observer</span></td>
        <td>Inertia</td>
        <td>Error rates, throughput, security signals, attestations</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="arq-soul-note">
  <strong>What about Soul?</strong> The Soul dimension stands apart from the ARQ pipeline. It is not derived from telemetry signals — it represents constitutional constraints (jurisdiction, consent, sovereignty) that exist outside the physics of network performance. Soul is checked separately and can veto any action regardless of ARQ-derived trust scores.
</div>

---

## Dimension Lens { #dimension-lens }

Each dimension has a distinct signal signature and behavioral effect. Click any dimension to explore its mechanics.

=== "Mass"

    <div class="dimension-hero" id="mass">
      <div class="dimension-monogram">
        <span class="mono-primary">M</span><span class="mono-secondary">a</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Mass</strong>
        <em>The weight of observed behavior</em>
      </div>
    </div>

    ### How It Works

    Mass measures the **density and volume of telemetry** flowing through the system. Think of it as gravitational weight—agents with more observed, consistent behavior carry more mass and are harder to perturb.

    Unlike a simple counter, Mass rewards *sustained* activity over spikes. An agent processing 1,000 requests over an hour gains more mass than one processing 1,000 requests in a burst. The tensor values consistency and predictability.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Packets | Request volume, throughput, bytes transferred | Primary |
    | Logs | Event density, audit trail depth | Secondary |
    | Metrics | Concurrent sessions, queue depth, active connections | Secondary |

    </div>

    !!! tip "Behavioral Pattern"
        **Consistency compounds.** Steady behavior over time builds mass more effectively than volume spikes. The tensor rewards agents who show up reliably, not those who flood the system episodically.

    !!! warning "Failure Mode"
        **Noisy traffic inflation.** High-volume garbage requests can artificially inflate Mass without genuine trust improvement. Anti-Goodhart measures detect and penalize this pattern.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Momentum](#__tabbed_2_2) (velocity × mass = force), [Inertia](#__tabbed_2_3) (stability anchors gains), [Heat](#__tabbed_2_4) (stress erodes accumulated mass)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [KTP-Tensors RFC](../rfcs/ktp-tensors.md) <span class="separator">·</span>
    [Telemetry Pipeline](telemetry.md) <span class="separator">·</span>
    [Use Cases](use-cases.md)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_7" class="nav-prev">Soul</a>
      <a href="#__tabbed_2_2" class="nav-next">Momentum</a>
    </div>

=== "Momentum"

    <div class="dimension-hero" id="momentum">
      <div class="dimension-monogram">
        <span class="mono-primary">M</span><span class="mono-secondary">o</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Momentum</strong>
        <em>The velocity of trust change</em>
      </div>
    </div>

    ### How It Works

    Momentum captures the **rate and direction of change** in an agent's trust posture. It's not about where you are—it's about where you're heading and how fast.

    Positive momentum (improving trust trajectory) can accelerate permission grants. Negative momentum (declining trust) triggers early intervention before thresholds are crossed. The system watches the derivative, not just the value.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Trust Deltas | Score changes per window, trend direction | Primary |
    | Volatility | Swing magnitude, oscillation frequency | Primary |
    | Step Changes | Sudden jumps, threshold crossings | Secondary |

    </div>

    !!! tip "Behavioral Pattern"
        **Direction matters more than position.** An agent at E=60 with positive momentum may be granted more than one at E=75 with negative momentum. The system anticipates where you'll be, not just where you are.

    !!! warning "Failure Mode"
        **Oscillation whiplash.** Rapidly swinging between states—even if averaging to a good score—signals instability. The tensor penalizes agents that can't hold a steady course.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Mass](#__tabbed_2_1) (momentum × mass = force), [Inertia](#__tabbed_2_3) (high inertia dampens momentum swings), [Time](#__tabbed_2_5) (recent momentum weighted higher)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [KTP-Tensors RFC](../rfcs/ktp-tensors.md) <span class="separator">·</span>
    [Telemetry Pipeline](telemetry.md) <span class="separator">·</span>
    [Trust Tiers](risk.md#risk-thresholds)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_1" class="nav-prev">Mass</a>
      <a href="#__tabbed_2_3" class="nav-next">Inertia</a>
    </div>

=== "Inertia"

    <div class="dimension-hero" id="inertia">
      <div class="dimension-monogram">
        <span class="mono-primary">I</span><span class="mono-secondary">n</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Inertia</strong>
        <em>Resistance to sudden change</em>
      </div>
    </div>

    ### How It Works

    Inertia measures an agent's **resistance to rapid fluctuation**. High inertia means the agent has established stable patterns that dampen noise. Low inertia indicates volatility and fragility.

    Think of inertia as behavioral ballast. Agents with deep, consistent histories are harder to knock off course by a single bad event—but also slower to recover from genuine compromise. It's a stabilizing force that cuts both ways.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Configuration | Config stability, drift detection | Primary |
    | Dependencies | Dependency consistency, version churn | Primary |
    | Behavior | Pattern consistency, routine adherence | Secondary |

    </div>

    !!! tip "Behavioral Pattern"
        **Stability is earned over time.** New agents have low inertia by design—they haven't proven themselves yet. Inertia builds through sustained, predictable operation. It cannot be rushed.

    !!! warning "Failure Mode"
        **Rapid drift signals fragility.** Frequent configuration changes, dependency updates, or behavioral shifts indicate an agent that hasn't settled. The tensor interprets this as risk.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Momentum](#__tabbed_2_2) (inertia dampens momentum swings), [Mass](#__tabbed_2_1) (high mass + high inertia = stable anchor), [Heat](#__tabbed_2_4) (heat can overcome inertia under sustained stress)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [KTP-Tensors RFC](../rfcs/ktp-tensors.md) <span class="separator">·</span>
    [Vector Identity](../specifications/identity.md) <span class="separator">·</span>
    [Proof of Resilience](../rfcs/ktp-identity.md)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_2" class="nav-prev">Momentum</a>
      <a href="#__tabbed_2_4" class="nav-next">Heat</a>
    </div>

=== "Heat"

    <div class="dimension-hero dimension-hero--heat" id="heat">
      <div class="dimension-monogram">
        <span class="mono-primary">H</span><span class="mono-secondary">e</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Heat</strong>
        <em>Environmental stress and friction</em>
      </div>
    </div>

    ### How It Works

    Heat measures **environmental stress, anomaly load, and adversarial pressure**. It's the friction coefficient of the trust environment—the resistance that actions must overcome.

    Heat rises fast but cools slowly. A burst of errors, a spike in blocked requests, or detected attack patterns all generate heat. Recovery requires sustained periods of clean operation—there are no shortcuts to cooling down.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Errors | Error rates, exception frequency, 5xx responses | Primary |
    | Security | WAF blocks, anomaly detections, threat indicators | Primary |
    | Load | CPU pressure, memory saturation, queue depth | Secondary |

    </div>

    !!! tip "Behavioral Pattern"
        **Heat is asymmetric.** It spikes immediately on stress events but decays on a longer curve. This prevents agents from rapidly alternating between attack and recovery to game the system.

    !!! warning "Failure Mode"
        **Sustained heat collapse.** Prolonged stress doesn't just reduce trust—it can trigger adaptive dormancy, forcing the agent into Hibernation mode until the environment stabilizes.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Mass](#__tabbed_2_1) (heat erodes accumulated mass), [Inertia](#__tabbed_2_3) (high inertia resists heat longer), [Observer](#__tabbed_2_6) (observed heat is weighted higher than inferred)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [KTP-Enforce RFC](../rfcs/ktp-enforce.md) <span class="separator">·</span>
    [Threat Model](../rfcs/ktp-threat-model.md) <span class="separator">·</span>
    [Adaptive Dormancy](risk.md#risk-thresholds)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_3" class="nav-prev">Inertia</a>
      <a href="#__tabbed_2_5" class="nav-next">Time</a>
    </div>

=== "Time"

    <div class="dimension-hero" id="time">
      <div class="dimension-monogram">
        <span class="mono-primary">T</span><span class="mono-secondary">i</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Time</strong>
        <em>Temporal context and signal decay</em>
      </div>
    </div>

    ### How It Works

    Time captures **temporal context, signal freshness, and decay functions**. Not all history is equal—recent signals carry more weight than stale ones, and the tensor applies exponential decay to age out old data.

    Time also encodes session context. Long-lived sessions shift baselines differently than ephemeral requests. The tensor understands that an agent's behavior at hour 1 of a session may differ from hour 8—and accounts for it.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Freshness | Signal age, last-seen timestamps | Primary |
    | Session | Session duration, activity windows | Primary |
    | History | Historical baselines, trend windows | Secondary |

    </div>

    !!! tip "Behavioral Pattern"
        **Recency dominates.** A clean last hour matters more than a clean last month. The tensor implements exponential decay—old signals fade, giving agents the ability to recover from past mistakes.

    !!! warning "Failure Mode"
        **Stale signal poisoning.** If the tensor relies on outdated data, it may grant trust based on conditions that no longer exist. Time decay prevents this, but gaps in telemetry can still mislead.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Momentum](#__tabbed_2_2) (recent momentum weighted higher), [Mass](#__tabbed_2_1) (old mass decays without fresh signals), [Observer](#__tabbed_2_6) (observation freshness affects confidence)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [KTP-Tensors RFC](../rfcs/ktp-tensors.md) <span class="separator">·</span>
    [Telemetry Pipeline](telemetry.md) <span class="separator">·</span>
    [Experience Calculator](../implement/experience-calculator.md)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_4" class="nav-prev">Heat</a>
      <a href="#__tabbed_2_6" class="nav-next">Observer</a>
    </div>

=== "Observer"

    <div class="dimension-hero" id="observer">
      <div class="dimension-monogram">
        <span class="mono-primary">O</span><span class="mono-secondary">b</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Observer</strong>
        <em>Who is watching, and how reliably</em>
      </div>
    </div>

    ### How It Works

    Observer measures **attestation coverage, audit visibility, and peer corroboration**. Trust confidence depends not just on what happened, but on how well it was witnessed.

    Multiple independent observers raise confidence. A single observer—or gaps in observation—lower it. The tensor implements observer-weighted trust: signals from high-trust attesters carry more weight than those from unknown sources.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Attestations | Signed proofs, audit logs, peer validations | Primary |
    | Coverage | Observation gaps, blind spot detection | Primary |
    | Peer Visibility | Cross-agent corroboration, mesh attestation | Secondary |

    </div>

    !!! tip "Behavioral Pattern"
        **Independent witnesses compound trust.** Three independent observers seeing the same behavior creates higher confidence than one observer seeing it three times. The tensor rewards attestation diversity.

    !!! warning "Failure Mode"
        **Blind spot exploitation.** Attackers may target gaps in observation coverage. The tensor flags low-visibility zones and may require additional attestation before granting high-privilege actions.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Heat](#__tabbed_2_4) (observed heat weighted higher), [Time](#__tabbed_2_5) (stale attestations decay), [Soul](#__tabbed_2_7) (Soul constraints require explicit observer confirmation)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [KTP-Audit RFC](../rfcs/ktp-audit.md) <span class="separator">·</span>
    [KTP-Provenance RFC](../rfcs/ktp-provenance.md) <span class="separator">·</span>
    [Trust Oracles](../rfcs/ktp-oracle.md)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_5" class="nav-prev">Time</a>
      <a href="#__tabbed_2_7" class="nav-next">Soul</a>
    </div>

=== "Soul"

    <div class="dimension-hero dimension-hero--soul" id="soul">
      <div class="dimension-monogram">
        <span class="mono-primary">S</span><span class="mono-secondary">o</span>
      </div>
      <div class="dimension-hero-content">
        <strong>Soul</strong>
        <em>Constitutional constraints that cannot be overridden</em>
      </div>
    </div>

    ### How It Works

    Soul is the **constitutional veto layer**. Unlike the other six dimensions (which contribute weighted values to trust calculations), Soul operates as a binary gate. If a Soul constraint is violated, the action is forbidden—regardless of how high the trust score is.

    Soul encodes immutable constraints: jurisdictional requirements, consent state, Indigenous data sovereignty (TK Labels, OCAP/CARE), sacred land protections, and governance vetoes. These are the laws of the digital universe that cannot be negotiated away for operational convenience.

    <div class="dimension-signals" markdown>

    | Signal Source | Example Signals | Influence |
    |---------------|-----------------|-----------|
    | Jurisdiction | Regulatory flags, data residency requirements | Veto |
    | Consent | User consent state, opt-out flags | Veto |
    | Sovereignty | TK Labels, OCAP/CARE markers, sacred geofences | Veto |

    </div>

    !!! tip "Behavioral Pattern"
        **Soul is not a score—it's a gate.** An agent with E=99 is still blocked if Soul=1. This ensures that human rights, cultural sovereignty, and constitutional constraints are never traded away for performance or efficiency.

    !!! warning "Failure Mode"
        **Soul violations are absolute.** There is no gradual degradation, no warning tier—just immediate denial. Recovery requires explicit governance action to change the underlying constraint, not just improved behavior.

    <div class="dimension-interacts" markdown>
    **Interacts with:** [Observer](#__tabbed_2_6) (Soul constraints require explicit attestation), [All Dimensions](#__tabbed_2_1) (Soul overrides any numerical trust calculation)
    </div>

    <div class="dimension-links" markdown>
    **Explore Further**
    [Constitution](constitution.md) <span class="separator">·</span>
    [KTP-Privacy RFC](../rfcs/ktp-privacy.md) <span class="separator">·</span>
    [Indigenous Data Sovereignty](../rfcs/ktp-human.md)
    </div>

    <div class="dimension-nav">
      <a href="#__tabbed_2_6" class="nav-prev">Observer</a>
      <a href="#__tabbed_2_1" class="nav-next">Mass</a>
    </div>

## Risk Deflation { #risk-deflation }

Trust isn't just built—it's also **deflated by risk**. The tensor doesn't ignore threats; it applies them as friction that reduces your effective trust score.

<div class="risk-deflation-hero">
  <div class="risk-equation">
    <div class="risk-equation-part risk-equation-raw">
      <span class="risk-label">Performance</span>
      <span class="risk-value">E<sub>base</sub></span>
    </div>
    <div class="risk-equation-operator">×</div>
    <div class="risk-equation-part risk-equation-factor">
      <span class="risk-label">Risk Factor</span>
      <span class="risk-value">(1 − R)</span>
    </div>
    <div class="risk-equation-operator">=</div>
    <div class="risk-equation-part risk-equation-final">
      <span class="risk-label">Trust Score</span>
      <span class="risk-value">E<sub>trust</sub></span>
    </div>
  </div>
  <p class="risk-equation-caption">Your base performance is deflated by risk. Higher risk means lower effective trust.</p>
</div>

### How Risk Deflates Trust

Even a perfect operational score can be crushed by unaddressed risk:

<div class="risk-examples">
  <div class="risk-example">
    <div class="risk-example-header">
      <span class="risk-example-icon risk-example-icon--security">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 1L3 5V11C3 16.55 6.84 21.74 12 23C17.16 21.74 21 16.55 21 11V5L12 1M12 7C13.4 7 14.8 8.1 14.8 9.5V11C15.4 11 16 11.6 16 12.3V15.8C16 16.4 15.4 17 14.7 17H9.2C8.6 17 8 16.4 8 15.7V12.2C8 11.6 8.6 11 9.2 11V9.5C9.2 8.1 10.6 7 12 7M12 8.2C11.2 8.2 10.5 8.7 10.5 9.5V11H13.5V9.5C13.5 8.7 12.8 8.2 12 8.2Z"/></svg>
      </span>
      <strong>Security Risk</strong>
    </div>
    <div class="risk-example-body">
      <p>Unpatched vulnerabilities, exposed secrets, insecure configurations, active threat indicators.</p>
      <div class="risk-example-calc">
        <span>E<sub>base</sub> = 85</span>
        <span class="risk-mult">× 0.6</span>
        <span class="risk-result">→ E<sub>trust</sub> = 51</span>
      </div>
      <p class="risk-example-note">40% security risk drops an excellent score to marginal.</p>
    </div>
  </div>
  <div class="risk-example">
    <div class="risk-example-header">
      <span class="risk-example-icon risk-example-icon--compliance">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M17 3H7C5.9 3 5 3.9 5 5V19C5 20.1 5.9 21 7 21H17C18.1 21 19 20.1 19 19V5C19 3.9 18.1 3 17 3M17 19H7V5H17V19M8 12H16V14H8V12M8 16H13V18H8V16M8 8H16V10H8V8Z"/></svg>
      </span>
      <strong>Compliance Risk</strong>
    </div>
    <div class="risk-example-body">
      <p>Regulatory violations, audit failures, policy breaches, expired certifications.</p>
      <div class="risk-example-calc">
        <span>E<sub>base</sub> = 92</span>
        <span class="risk-mult">× 0.75</span>
        <span class="risk-result">→ E<sub>trust</sub> = 69</span>
      </div>
      <p class="risk-example-note">25% compliance risk turns excellent into merely acceptable.</p>
    </div>
  </div>
  <div class="risk-example">
    <div class="risk-example-header">
      <span class="risk-example-icon risk-example-icon--behavioral">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2C6.48 2 2 6.48 2 12S6.48 22 12 22 22 17.52 22 12 17.52 2 12 2M12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20M11 7H13V13H11V7M11 15H13V17H11V15Z"/></svg>
      </span>
      <strong>Behavioral Risk</strong>
    </div>
    <div class="risk-example-body">
      <p>Anomalous patterns, deviation from baseline, sudden capability changes.</p>
      <div class="risk-example-calc">
        <span>E<sub>base</sub> = 78</span>
        <span class="risk-mult">× 0.5</span>
        <span class="risk-result">→ E<sub>trust</sub> = 39</span>
      </div>
      <p class="risk-example-note">50% behavioral risk triggers adaptive dormancy.</p>
    </div>
  </div>
</div>

!!! warning "Risk Compounds"
    Multiple risk factors multiply together. Security risk of 20% plus compliance risk of 15% doesn't equal 35%—it equals `0.8 × 0.85 = 0.68`, or **32% total deflation**. Risk stacks against you.

<div class="risk-cta">
  <strong>Deep Dive:</strong> For full risk taxonomy, scoring methodology, and mitigation strategies, see <a href="../risk/">Risk & Deflation</a>.
</div>
