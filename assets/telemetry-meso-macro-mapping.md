Global Context Metrics
Throughput_sps
Meso: Immediate indicator of system load; a sudden drop suggests a service outage or blocking event.
Macro: Key performance indicator for infrastructure ROI; demonstrates the system's capacity to support business growth.

Trust_Mass
Meso: Real-time resilience score; high mass allows users to bypass friction (MFA) during low-risk activities.
Macro: Aggregate measure of workforce reliability; high average trust mass reduces security overhead costs.

Env_Friction_Risk
Meso: The 
Macro: Organizational risk appetite; adjusting this dial balances security posture against user productivity.

Accumulated_Risk
Meso: Session-level 
Macro: Long-term threat exposure; high accumulated risk across the org indicates a need for architectural security changes.

Phase
Meso: Current attack stage (e.g., Recon, Exfil); dictates which defensive playbooks are active.
Macro: Dwell time analysis; identifying which phase attackers reach most often highlights systemic vulnerabilities.

Time_Tplus
Meso: Incident timeline tracking; correlates specific log events with the exact second of an attack.
Macro: Mean Time to Detect (MTTD); tracks the organization's speed in identifying active threats.

Event_Risk_Level
Meso: Alert prioritization; Level 3 events page the SOC immediately, while Level 1s are logged for review.
Macro: Threat landscape severity; a rising average risk level indicates an increasingly hostile external environment.

Zone
Meso: Segmentation enforcement; traffic moving from 
Macro: Network architecture validation; ensures critical assets are properly isolated from public networks.

Layer 8: Identity (L8)
user_id
Meso: Individual accountability; links every action in the logs to a specific human or machine identity.
Macro: Identity lifecycle management; tracks the total active user base against licensing and HR records.

Auth_Volume_by_User
Meso: Spike detection; 100 logins in 1 minute triggers a brute-force alert.
Macro: User adoption rate; tracks the utilization of new applications or services.

Failed_Login_Rate
Meso: Account lockout trigger; >5 failures locks the account to prevent unauthorized access.
Macro: UX friction indicator; high failure rates suggest confusing login flows or password policy issues.

Concurrent_Sessions
Meso: Session hijacking indicator; simultaneous logins from NY and London trigger a 
Macro: Licensing compliance; ensures the organization isn't exceeding seat limits for SaaS tools.

New_Device_Access
Meso: Step-up auth trigger; a login from a never-before-seen laptop requires MFA.
Macro: BYOD trend analysis; measures the shift towards personal device usage in the enterprise.

role
Meso: Access control decision; 
Macro: RBAC maturity; tracks the granularity and correctness of role definitions across the org.

Privilege_Escalation
Meso: Critical alert; a standard user suddenly adding themselves to 
Macro: Insider threat monitoring; tracks the effectiveness of Least Privilege policies.

Role_Change_Frequency
Meso: Anomaly detection; a user changing roles 5 times in an hour suggests an account takeover or error.
Macro: IAM process efficiency; measures the stability of the workforce and the overhead of access requests.

Toxic_Combination
Meso: Separation of Duties (SoD) violation; a user with both 
Macro: Fraud prevention; ensures compliance with financial regulations (SOX).

Dormant_Role_Usage
Meso: Cleanup trigger; a role unused for 90 days is automatically flagged for removal.
Macro: Attack surface reduction; minimizes the number of over-privileged accounts available to attackers.

department
Meso: Contextual access; 
Macro: Cost allocation; tracks IT resource consumption by business unit.

Cross_Dept_Access
Meso: Data leakage risk; 
Macro: Collaboration patterns; visualizes how different teams interact and share data.

Dept_Outlier_Analysis
Meso: Behavioral anomaly; one user downloading 10x more data than their peers triggers an investigation.
Macro: Insider threat baseline; establishes 

Shadow_IT_by_Dept
Meso: Policy enforcement; 
Macro: Vendor risk management; identifies unvetted SaaS tools that need to be brought under governance.

geo_location
Meso: Conditional access; logins from sanctioned countries are auto-blocked.
Macro: Global footprint; visualizes where the workforce is operating to optimize CDN and edge placement.

Impossible_Travel
Meso: Access denial; login from North Korea 5 minutes after a login from Texas is auto-blocked.
Macro: Global threat landscape; identifies targeted attacks from specific geopolitical regions.

New_Country_Access
Meso: Risk scoring; first-time access from a new country adds 20 points to the risk score.
Macro: Expansion monitoring; tracks legitimate business growth into new international markets.

Geo_Velocity_Anomaly
Meso: Credential theft indicator; a user 
Macro: Remote work policy; validates that employees are working from authorized locations.

High_Risk_Country
Meso: Enhanced monitoring; all traffic from high-risk zones is subjected to full packet capture.
Macro: Geopolitical risk; aligns IT security posture with broader corporate travel and safety policies.

device_id
Meso: Asset tracking; links a specific laptop to a security incident.
Macro: Hardware lifecycle; tracks the age and distribution of the endpoint fleet.

Device_Trust_Score
Meso: Access gate; devices with a score <50 are denied access to sensitive apps.
Macro: Endpoint hygiene; measures the overall patch level and security configuration of the fleet.

New_Device_Rate
Meso: Fraud detection; a user registering 5 new devices in a day triggers a review.
Macro: Tech refresh cycle; tracks the rollout of new hardware to employees.

Jailbroken_Device
Meso: Compliance block; rooted phones are blocked from accessing corporate email.
Macro: Mobile security posture; measures the risk exposure from compromised mobile endpoints.

BYOD_Usage
Meso: Policy enforcement; personal devices are routed to a restricted guest network.
Macro: IT strategy; informs the decision to move towards or away from a BYOD model.

Layer 7: Application (L7)
http_method
Meso: Request routing; GET requests are cached, POST requests are sent to the backend.
Macro: Application architecture; analyzes the RESTfulness and design patterns of APIs.

Method_Distribution
Meso: Anomaly detection; a sudden spike in DELETE requests suggests a data destruction attack.
Macro: API usage patterns; informs capacity planning for read-heavy vs. write-heavy services.

Unusual_Method_Usage
Meso: Attack detection; using DEBUG or TRACE methods triggers a WAF block.
Macro: Security configuration; ensures production servers have dangerous HTTP methods disabled.

High_Volume_POST
Meso: DoS/Spam detection; rapid POSTs to a comment form trigger a rate limit.
Macro: Data ingestion tracking; monitors the volume of data being written to the platform.

Method_vs_Path_Anomaly
Meso: Logic flaw probe; sending a POST to a read-only image file triggers an alert.
Macro: API design consistency; ensures endpoints adhere to standard HTTP semantics.

http_status
Meso: Health check; a stream of 200 OKs indicates the service is healthy.
Macro: Reliability metric; tracks the overall availability and uptime of the application portfolio.

Error_Rate_5xx
Meso: Service health; >1% error rate triggers an automated rollback of the latest deployment.
Macro: SLA compliance; directly impacts customer satisfaction and contractual penalties.

Access_Denied_403
Meso: Reconnaissance detection; high 403s indicate an attacker scanning for vulnerable paths.
Macro: Policy effectiveness; validates that access controls are correctly restricting unauthorized users.

Not_Found_Spike_404
Meso: Broken link detection; a spike in 404s triggers a webmaster review.
Macro: SEO health; ensures the public-facing site is crawlable and user-friendly.

Success_Rate
Meso: Operational baseline; <99% success rate triggers a P2 incident.
Macro: Business performance; correlates technical success with conversion rates and revenue.

url_path
Meso: Traffic routing; requests to /api/* are routed to the API gateway.
Macro: Content strategy; analyzes which pages or features are most popular with users.

Path_Traversal_Attempt
Meso: Exploit block; ../../etc/passwd in the URL triggers an immediate IP ban.
Macro: Vulnerability management; highlights code that needs input validation fixes.

Admin_Page_Access
Meso: High-risk monitoring; access to /admin triggers a log entry and potential alert.
Macro: Attack surface reduction; drives the decision to hide or VPN-gate administrative interfaces.

Sensitive_File_Access
Meso: Data leak prevention; access to backup.sql triggers a critical alert.
Macro: Information classification; validates that sensitive assets are stored in secure locations.

High_Cardinality_Paths
Meso: Scraper detection; a user hitting 10,000 unique product pages is blocked.
Macro: Bot management; measures the impact of automated traffic on infrastructure costs.

user_agent
Meso: Client identification; serves mobile-optimized content to iPhone users.
Macro: Browser support strategy; decides which legacy browsers (e.g., IE11) to deprecate.

Rare_User_Agent
Meso: Bot detection; a UA string like Python-urllib/3.8 triggers a challenge.
Macro: Threat intelligence; identifies custom tools used by specific threat actors.

Bot_Scraper_Detection
Meso: Traffic shaping; known bots are rate-limited to prevent server overload.
Macro: Competitive intelligence protection; prevents rivals from scraping pricing data.

Outdated_Browser
Meso: Security warning; users on Chrome 50 are warned to update.
Macro: Vulnerability exposure; measures the risk of client-side exploits across the user base.

UA_Spoofing
Meso: Evasion detection; a Linux machine claiming to be an iPhone is flagged.
Macro: Fraud analysis; identifies sophisticated actors trying to mask their identity.

referer
Meso: Traffic source tracking; identifies where a user came from (e.g., Google, email).
Macro: Marketing attribution; measures the ROI of different ad campaigns.

Empty_Referer
Meso: Suspicious traffic; direct access to deep links triggers a fraud check.
Macro: Privacy trend; tracks the increase in users utilizing privacy tools that strip headers.

Cross_Site_Scripting
Meso: Input sanitization failure; a script tag in a comment field triggers a content filter.
Macro: Application security posture; drives the prioritization of bug bounty programs.

External_Referer
Meso: Hotlinking protection; blocks other sites from embedding your images.
Macro: Brand monitoring; identifies external sites linking to your content (positive or negative).

cookie_id
Meso: Session tracking; maintains user state across page loads.
Macro: Privacy compliance; ensures cookie usage aligns with GDPR/CCPA consent.

Cookie_Replay
Meso: Session hijacking; a cookie used from a different IP triggers a session reset.
Macro: Authentication security; validates the effectiveness of token binding technologies.

Cookie_Theft
Meso: Malware alert; detection of a cookie database access triggers an endpoint scan.
Macro: Incident response; drives the need for shorter session lifetimes.

Missing_Secure_Flag
Meso: Compliance violation; cookies sent over HTTP are flagged for remediation.
Macro: Security best practices; ensures all sensitive cookies are protected in transit.

Session_Fixation
Meso: Account takeover; a user reusing a pre-auth session ID triggers a forced logout.
Macro: Identity architecture; validates the robustness of the session management framework.

Layer 6.5: API (L6.5)
api_endpoint
Meso: Service routing; directs calls to the appropriate microservice.
Macro: API catalog; maintains an inventory of all available programmatic interfaces.

Endpoint_Usage
Meso: Resource allocation; high traffic to /v1/search triggers auto-scaling for that specific service.
Macro: Feature adoption; tracks which API capabilities are driving business value.

Deprecated_Endpoint
Meso: Developer warning; returns a 
Macro: Technical debt; tracks the progress of migrating clients to newer API versions.

Shadow_API
Meso: Security gap; traffic to an undocumented endpoint (/v1/test_admin) triggers an alert.
Macro: Governance gap; highlights unauthorized development or legacy endpoints that need decommissioning.

Endpoint_Latency
Meso: Performance bottleneck; slow response times trigger a database optimization review.
Macro: Developer experience; ensures the API is performant enough for third-party integrations.

api_key_id
Meso: Client authentication; validates the caller has permission to access the API.
Macro: Partner management; tracks the usage and billing for different API consumers.

Key_Usage_Volume
Meso: Quota enforcement; a partner exceeding their daily limit is throttled.
Macro: Revenue forecasting; predicts API usage tiers and potential overage charges.

Invalid_Key_Rate
Meso: Misconfiguration detection; high failures suggest a broken client integration.
Macro: Security scanning; identifies actors attempting to guess valid API keys.

Key_Rotation
Meso: Security hygiene; forces clients to update keys every 90 days.
Macro: Compliance audit; proves that credential management policies are being followed.

Concurrent_Key_Use
Meso: Key sharing detection; the same key used from 50 IPs simultaneously triggers a block.
Macro: License enforcement; prevents customers from sharing a single API account.

response_size
Meso: Bandwidth management; compresses large JSON responses to save data.
Macro: Infrastructure cost; correlates payload sizes with egress bandwidth bills.

Payload_Size_Avg
Meso: Optimization target; identifies bloated responses that slow down mobile apps.
Macro: Data efficiency; drives API design improvements (e.g., GraphQL) to fetch only needed data.

Data_Exfiltration
Meso: DLP trigger; a 5GB response from a 
Macro: Intellectual property protection; monitors the flow of sensitive data leaving the organization.

Large_Payload
Meso: DoS risk; a request body >10MB is rejected to prevent memory exhaustion.
Macro: System stability; ensures the API is robust against malformed or excessive inputs.

Zero_Byte_Response
Meso: Bug detection; empty responses suggest a silent failure in the backend.
Macro: Quality assurance; tracks the reliability of API data delivery.

rate_limit_status
Meso: DoS protection; a client hitting the limit is temporarily IP-banned.
Macro: API monetization; identifies customers who need to be upsold to a higher tier plan.

Throttled_Requests
Meso: Client feedback; returns a Retry-After header to well-behaved clients.
Macro: Capacity planning; high throttling indicates a need to increase infrastructure limits.

Quota_Consumption
Meso: Resource protection; prevents a single tenant from consuming all available resources.
Macro: Fair use policy; ensures equitable access to shared API infrastructure.

Abusive_Client
Meso: Ban trigger; a client hitting limits 100x in a row is permanently blocked.
Macro: Platform integrity; protects the ecosystem from malicious or poorly written integrations.

Layer 6: Presentation (L6)
tls_version
Meso: Connection security; a client negotiating TLS 1.0 is rejected.
Macro: Compliance standard; ensures alignment with PCI-DSS requirements (no SSL/early TLS).

Legacy_Protocol
Meso: Deprecation warning; logs usage of SSLv3 to identify impacted clients.
Macro: Modernization roadmap; tracks the elimination of obsolete cryptographic standards.

TLS_1_3_Adoption
Meso: Performance boost; faster handshakes improve initial page load times.
Macro: Security leadership; demonstrates commitment to using the latest secure protocols.

Downgrade_Attack
Meso: MITM detection; a forced downgrade to plaintext triggers a connection reset.
Macro: Network integrity; validates that active defenses against interception are working.

cipher_suite
Meso: Encryption strength; ensures the session uses strong algorithms (e.g., AES-256).
Macro: Risk management; balances security requirements with client compatibility.

Weak_Cipher_Usage
Meso: Encryption downgrade; a request for RC4 is blocked to prevent interception.
Macro: Cryptographic agility; measures the organization's readiness for post-quantum standards.

Cipher_Distribution
Meso: Configuration audit; verifies that the server prefers the strongest available ciphers.
Macro: Industry alignment; ensures the crypto profile matches current best practices (NIST).

PFS_Usage
Meso: Privacy assurance; ensures past sessions can't be decrypted if the key is stolen later.
Macro: Data confidentiality; critical for protecting long-term sensitive communications.

content_type
Meso: Parsing logic; tells the browser how to render the data (JSON vs. HTML).
Macro: Interoperability; ensures APIs are returning data in expected formats.

MIME_Type_Mismatch
Meso: Malware delivery; a file named invoice.pdf with application/x-dosexec content is quarantined.
Macro: Content security policy; enforces strict data type validation across the enterprise.

Executable_Download
Meso: Security block; downloading .exe files is restricted to admin users.
Macro: Endpoint protection; reduces the risk of drive-by downloads and malware infection.

Unexpected_Content
Meso: Anomaly detection; an image upload containing PHP code is rejected.
Macro: Web security; prevents file upload vulnerabilities (webshells).

encoding
Meso: Data integrity; ensures characters are displayed correctly (UTF-8).
Macro: Globalization; supports the localization of applications for international markets.

Compression_Ratio
Meso: Bandwidth optimization; high compression (GZIP/Brotli) speeds up delivery.
Macro: Infrastructure efficiency; reduces CDN costs and improves user experience.

Double_Encoding
Meso: WAF evasion; %252E (double encoded dot) triggers a security block.
Macro: Attack signature tuning; improves the detection of sophisticated evasion techniques.

Malformed_Encoding
Meso: Error handling; invalid byte sequences trigger a 400 Bad Request.
Macro: Robustness testing; ensures the application handles fuzzing and bad input gracefully.

Layer 5: Session (L5)
session_id
Meso: User tracking; correlates multiple requests into a single user journey.
Macro: Audit trail; provides a unique key to reconstruct user activity for forensics.

Session_Count
Meso: Load monitoring; total active sessions tracks server memory usage.
Macro: Business activity; correlates with daily active users (DAU).

Session_Churn
Meso: UX issue; high churn suggests users are getting logged out unexpectedly.
Macro: Application stability; measures the reliability of the session persistence layer.

session_duration
Meso: Timeout enforcement; a session active for >24 hours is forced to re-authenticate.
Macro: Productivity vs. Security; balancing long session convenience against the risk of unattended access.

Avg_Session_Length
Meso: Engagement metric; longer sessions imply deeper user engagement.
Macro: Product value; indicates how 

Short_Sessions
Meso: Bot behavior; 1-second sessions suggest a crawler or health check.
Macro: Traffic quality; filters out non-human traffic from analytics reports.

Long_Sessions
Meso: Security risk; sessions >8 hours are flagged for re-verification.
Macro: Workflow analysis; understands how long users typically need to complete tasks.

Session_Timeout_Rate
Meso: Configuration tuning; high timeouts suggest the idle timer is too aggressive.
Macro: User frustration; balancing security requirements with usability.

login_status
Meso: Access control; determines if the user is allowed into the system.
Macro: System health; tracks the overall reliability of the authentication service.

Login_Success_Rate
Meso: Operational baseline; <99% success rate triggers a P2 incident.
Macro: Business performance; correlates technical success with conversion rates and revenue.

Brute_Force
Meso: Credential defense; 50 failed logins from one IP triggers a CAPTCHA for all users from that IP.
Macro: Threat intelligence; identifies botnet IPs to feed into the global blocklist.

Credential_Stuffing
Meso: Account protection; detects login attempts using leaked username/password pairs.
Macro: Fraud loss reduction; prevents mass account takeovers and subsequent financial fraud.

keepalive_status
Meso: Connection health; ensures the link remains open for push notifications.
Macro: Mobile experience; critical for real-time features in mobile apps.

Keepalive_Failures
Meso: Network instability; frequent failures suggest a flaky client connection.
Macro: Infrastructure reliability; identifies issues with load balancers dropping idle connections.

Zombie_Sessions
Meso: Resource leak; sessions that remain open after the user leaves consume memory.
Macro: Capacity planning; accurate sizing requires cleaning up dead sessions.

Layer 4: Transport (L4)
src_port
Meso: Connection tracking; identifies the client side of a socket pair.
Macro: NAT capacity; monitors the usage of available ports on NAT gateways.

Ephemeral_Port_Exhaustion
Meso: Connection failure; inability to open new outbound connections triggers a load balancer alert.
Macro: Infrastructure scalability; indicates a need to redesign connection pooling strategies.

Fixed_Source_Port
Meso: DNS poisoning risk; static source ports make DNS spoofing easier.
Macro: Security hardening; ensures randomization is used to prevent prediction attacks.

Port_Scan_Source
Meso: Recon detection; a single IP connecting to 100 different ports is blocked.
Macro: Threat landscape; measures the background noise of internet scanning activity.

dest_port
Meso: Service identification; traffic to port 80 is Web, port 22 is SSH.
Macro: Attack surface; tracks which services are exposed to the internet.

Service_Distribution
Meso: Traffic analysis; visualizes the mix of HTTP, DNS, and SMTP traffic.
Macro: Network planning; informs QoS policies based on application types.

Dark_Port_Access
Meso: Malware beaconing; traffic to non-standard ports (e.g., 6667) is blocked.
Macro: Firewall policy; validates that the 

Port_Scan_Dest
Meso: Targeted attack; multiple IPs scanning a specific server suggests a focused campaign.
Macro: Vulnerability management; prioritizes patching for services receiving scan attention.

High_Port_Usage
Meso: P2P detection; traffic on high-numbered ports suggests torrenting.
Macro: Compliance; ensures corporate networks aren't used for illegal file sharing.

tcp_flags
Meso: State inspection; validates the TCP handshake sequence (SYN -> SYN-ACK -> ACK).
Macro: Firewall efficiency; stateful inspection relies on tracking these flags.

SYN_Flood
Meso: DDoS mitigation; a spike in SYN packets without ACKs triggers SYN cookies.
Macro: Business continuity; ensures critical services remain available during volumetric attacks.

RST_Rate
Meso: Connection errors; high resets suggest a firewall is actively rejecting traffic.
Macro: Network health; helps diagnose application connectivity issues.

Null_Scan
Meso: Evasion attempt; packets with no flags set trigger an IDS alert.
Macro: IDS tuning; improves detection of non-standard scanning techniques.

Xmas_Scan
Meso: OS fingerprinting; packets with FIN, URG, and PSH set are blocked.
Macro: Reconnaissance defense; makes it harder for attackers to identify target OS versions.

Handshake_Completion
Meso: Connection success; measures the ratio of successful TCP setups.
Macro: User experience; failed handshakes equal failed page loads.

window_size
Meso: Flow control; a shrinking window indicates the receiver is overwhelmed.
Macro: Performance tuning; optimizing window sizes improves throughput on long-fat networks.

Zero_Window
Meso: Stalled connection; the receiver pauses data transmission to clear its buffer.
Macro: Application performance; frequent zero windows indicate an under-resourced server.

Window_Scaling
Meso: High-speed transfer; enables window sizes >64KB for gigabit links.
Macro: Network modernization; ensures the stack supports modern high-bandwidth applications.

Retransmission_Correlation
Meso: Loss diagnosis; correlates retransmits with congestion events.
Macro: Root cause analysis; distinguishes between physical loss and congestion loss.

retransmission_rate
Meso: Network congestion; high retransmits trigger a rerouting of traffic to a healthy link.
Macro: User experience; directly correlates with application 

Retransmission_Spike
Meso: Incident trigger; a sudden jump to 10% loss alerts the NOC.
Macro: SLA monitoring; tracks periods of degraded network performance.

High_Retransmission_Host
Meso: Fault isolation; identifies a specific server with a bad NIC or cable.
Macro: Hardware maintenance; drives proactive replacement of failing components.

Global_Retransmission
Meso: Network-wide issue; high retransmits everywhere suggest an ISP outage.
Macro: Vendor management; holds upstream providers accountable for quality.

Layer 3.5: Flow (L3.5)
flow_bytes_in
Meso: Download tracking; measures the volume of data entering the network.
Macro: Capacity planning; ensures internet circuits are sized correctly.

Inbound_Volume
Meso: DDoS detection; a massive spike in inbound bytes triggers scrubbing.
Macro: Cost analysis; tracks data ingress costs for cloud providers.

Large_Transfer
Meso: Backup detection; a single flow moving 1TB is flagged as a backup job.
Macro: Traffic engineering; schedules large transfers for off-peak hours.

Volume_Spike
Meso: Flash crowd; sudden traffic to a marketing site triggers auto-scaling.
Macro: Event management; prepares infrastructure for product launches or announcements.

Ratio_Analysis
Meso: C2 detection; high outbound/low inbound ratio suggests exfiltration.
Macro: Threat modeling; defines 

flow_bytes_out
Meso: Upload tracking; measures data leaving the network.
Macro: Egress cost; monitors the most expensive part of cloud networking bills.

Outbound_Volume
Meso: Leak detection; a database server sending high volume to the internet is blocked.
Macro: Security posture; enforces the principle that servers should not initiate outbound connections.

Exfiltration_Detection
Meso: DLP alert; sensitive data patterns detected in outbound flows.
Macro: Risk mitigation; prevents the loss of customer PII or trade secrets.

Upload_Anomaly
Meso: Insider threat; a user uploading 50GB to Dropbox is investigated.
Macro: Policy enforcement; restricts the use of personal cloud storage on corporate devices.

Asymmetric_Flow
Meso: Routing issue; traffic leaving one path and returning another causes firewall drops.
Macro: Network design; ensures routing symmetry for stateful security devices.

flow_packets
Meso: Load measurement; packet rate (PPS) determines firewall CPU load.
Macro: Hardware sizing; ensures devices can handle the packet-per-second throughput.

Packet_Volume
Meso: DDoS type; high PPS with low bandwidth suggests a small-packet flood.
Macro: Infrastructure resilience; tests the limits of the network control plane.

Small_Packet_Flood
Meso: Attack signature; millions of 64-byte packets overwhelm routers.
Macro: Defense strategy; prioritizes hardware-based mitigation for volumetric attacks.

Packet_Size_Avg
Meso: Traffic characterization; large packets = file transfer, small packets = VoIP/Gaming.
Macro: QoS policy; optimizes queues based on the nature of the traffic.

Scan_Detection
Meso: Recon alert; a source sending 1 packet to thousands of destinations is blocked.
Macro: Threat intelligence; identifies active scanners on the internet.

flow_duration
Meso: Connection state; tracks how long a conversation lasts.
Macro: Application behavior; helps understand the persistence of different protocols.

Average_Flow_Duration
Meso: Baseline; web traffic is short, SSH/RDP is long.
Macro: Anomaly detection; deviations from the baseline indicate a change in usage.

Long_Lived_Flows
Meso: Tunnel detection; a flow active for days suggests a VPN or C2 channel.
Macro: Security audit; investigates why connections are remaining open indefinitely.

C2_Beaconing
Meso: Malware comms; short, periodic flows to a bad IP trigger an alert.
Macro: APT defense; detects the 

Tunnel_Detection
Meso: Evasion; DNS traffic with long durations suggests DNS tunneling.
Macro: Policy enforcement; blocks unauthorized VPNs and proxy tools.

flow_start_time
Meso: Temporal analysis; correlates flows with specific time-based events.
Macro: Usage patterns; identifies peak hours for capacity planning.

Flow_Start_Distribution
Meso: Boot storm; thousands of flows starting at 9 AM crashes the login server.
Macro: Infrastructure scaling; pre-warms resources before expected traffic spikes.

Off_Hours_Activity
Meso: Suspicious behavior; a backup server active at 2 PM (instead of 2 AM) is flagged.
Macro: Operational discipline; ensures scheduled tasks run within their maintenance windows.

Burst_Detection
Meso: Microburst; sub-second traffic spikes that drop packets are identified.
Macro: Buffer sizing; ensures network buffers are large enough to absorb bursts.

Time_Correlation
Meso: Forensic timeline; links a network flow to a specific log entry.
Macro: Incident reconstruction; builds a complete picture of an attack across systems.

flow_end_reason
Meso: Termination cause; did the flow end normally (FIN) or abruptly (RST)?
Macro: Network health; high rates of abnormal termination indicate underlying issues.

End_Reason_Distribution
Meso: Troubleshooting; a spike in timeouts suggests a firewall is silently dropping packets.
Macro: Reliability engineering; aims to maximize clean flow terminations.

Timeout_Flows
Meso: Zombie connections; flows that just stop talking consume state table entries.
Macro: Firewall tuning; adjusting timeout values to match application behavior.

RST_FIN_Analysis
Meso: Connection teardown; distinguishes between polite closing and forced resets.
Macro: Application quality; well-behaved apps close connections gracefully.

Forced_Closure
Meso: Security intervention; an IPS sending a RST to kill a bad connection.
Macro: Defense effectiveness; measures how often security tools are actively blocking threats.

application_id
Meso: Layer 7 visibility; identifies traffic as 
Macro: App rationalization; identifies redundant applications (e.g., Zoom vs. Teams).

App_Distribution
Meso: Bandwidth allocation; shows that 40% of WAN traffic is YouTube.
Macro: Policy enforcement; justifies the need to throttle recreational traffic.

Shadow_IT_Detection
Meso: Unauthorized app; detection of 
Macro: Risk management; brings unapproved tools into the governance process.

New_Application
Meso: Change detection; first time seeing 
Macro: Threat hunting; investigates new, unknown protocols appearing in the environment.

App_Usage_Trend
Meso: Adoption tracking; monitors the growth of a new corporate tool.
Macro: Licensing; ensures the org has enough licenses for the number of active users.

flow_direction
Meso: Traffic classification; East-West (server-to-server) vs. North-South (client-to-server).
Macro: Architecture validation; ensures traffic flows match the intended network design.

Direction_Distribution
Meso: Segmentation check; ensures Guest WiFi isn't sending traffic to the Data Center.
Macro: Zero Trust; validates that lateral movement is restricted.

Egress_Anomaly
Meso: Data leak; a database server initiating a connection to the internet is blocked.
Macro: Security posture; enforces strict egress filtering rules.

Lateral_Movement
Meso: Attack propagation; an infected laptop scanning other laptops is isolated.
Macro: Containment strategy; measures the effectiveness of micro-segmentation.

Internal_Traffic
Meso: LAN performance; monitors the health of local switching infrastructure.
Macro: Network capacity; ensures the backbone can handle internal file transfers and backups.

Layer 3: Network (L3)
src_ip
Meso: Identity attribution; maps an IP address to a specific device or user.
Macro: Asset management; tracks the usage of IP address space.

Unique_Sources
Meso: DDoS metric; a sudden jump to 100k unique sources indicates a botnet attack.
Macro: User base sizing; estimates the number of active devices on the network.

New_Source_Detection
Meso: NAC alert; a new IP appearing on a server VLAN triggers an investigation.
Macro: Change management; validates that new deployments are authorized.

Top_Talkers
Meso: Bandwidth hog; a single host consuming 80% of the link is throttled.
Macro: Cost management; identifies departments or apps driving up ISP/Cloud egress bills.

Source_Reputation
Meso: Threat blocking; traffic from a known 
Macro: Threat intelligence; leverages global data to protect the local environment.

Internal_vs_External
Meso: Perimeter monitoring; tracks the ratio of local vs. internet traffic.
Macro: Network architecture; informs decisions about DMZ placement and internet breakout.

dest_ip
Meso: Target identification; shows where traffic is going.
Macro: Dependency mapping; builds a map of external services the org relies on.

Unique_Destinations
Meso: Malware behavior; a host connecting to 1000 random IPs is likely infected.
Macro: Internet usage; understands the breadth of external sites accessed by employees.

New_Destination_Alert
Meso: C2 detection; a server connecting to a never-before-seen IP is flagged.
Macro: Threat hunting; investigates connections to newly registered domains.

Destination_Reputation
Meso: Web filtering; access to 
Macro: Acceptable use policy; enforces corporate rules on internet usage.

Beaconing_Detection
Meso: C2 identification; regular 5-minute pulses to a rare IP trigger a host isolation.
Macro: APT detection; reveals long-term, stealthy compromises that evaded perimeter defenses.

Rare_Destination_Access
Meso: Anomaly detection; traffic to a country the org does no business with is flagged.
Macro: Risk reduction; geo-blocking reduces the attack surface.

latency
Meso: Performance monitoring; measures the round-trip time (RTT) for packets.
Macro: User experience; high latency kills productivity for interactive apps.

Average_Latency
Meso: Baseline; establishes the 
Macro: SLA tracking; ensures providers are meeting their latency guarantees.

P50_Latency
Meso: Median performance; the experience of the typical user.
Macro: Quality consistency; ensures stable performance for the majority.

P95_Latency
Meso: Outlier detection; the experience of the slowest 5% of requests.
Macro: Performance optimization; targeting P95 improvements fixes the worst bottlenecks.

P99_Latency
Meso: Worst-case scenario; the extreme tail latency.
Macro: Critical app support; vital for real-time trading or voice applications.

Latency_Anomaly
Meso: Performance degradation; a 50ms jump in RTT triggers a ticket to the network team.
Macro: Digital experience; ensures remote workers have the connectivity needed to be productive.

Latency_Trend
Meso: Capacity planning; slowly increasing latency suggests a link is reaching saturation.
Macro: Infrastructure investment; justifies the need for bandwidth upgrades.

packet_loss
Meso: Link health; drops indicate a bad cable, congestion, or errors.
Macro: Application reliability; loss causes retransmits and slowness.

Loss_Rate
Meso: Quality threshold; >0.1% loss triggers an alert for VoIP circuits.
Macro: Vendor performance; holds ISPs accountable for clean circuits.

Loss_Spike
Meso: Incident trigger; a sudden burst of loss indicates a failure or attack.
Macro: Operational stability; minimizes the impact of transient network issues.

Loss_Outliers
Meso: Problem isolation; identifies specific paths or times with high loss.
Macro: Root cause analysis; helps pinpoint intermittent issues.

Loss_by_Path
Meso: Route optimization; traffic is steered away from a lossy ISP peer.
Macro: Multi-cloud strategy; ensures redundancy across different network paths.

P99_Loss
Meso: Worst-case quality; ensures even the worst connections are usable.
Macro: User equity; ensures remote users in rural areas can still work.

hop_count
Meso: Path length; measures the number of routers traffic passes through.
Macro: Routing efficiency; fewer hops usually means lower latency.

Avg_Path_Length
Meso: Topology baseline; establishes the normal distance to key services.
Macro: Network design; validates the flatness of the data center fabric.

Path_Change_Detection
Meso: Routing instability; a change in hop count suggests a route flap.
Macro: Internet weather; monitors global routing changes affecting connectivity.

Excessive_Hops
Meso: Routing loop; hop count hitting 255 means traffic is circling endlessly.
Macro: Configuration audit; identifies misconfigured routing protocols.

TTL_Expiry_Rate
Meso: Connectivity loss; packets dropping due to TTL=0 triggers a routing protocol reset.
Macro: Network stability; highlights fragile or misconfigured routing architectures.

tos_dscp
Meso: QoS tagging; ensures critical traffic is marked for priority handling.
Macro: Service assurance; guarantees voice and video quality during congestion.

QoS_Marking_Distribution
Meso: Policy audit; verifies that only authorized apps are using the 
Macro: Network fairness; prevents low-priority traffic from starving critical apps.

Voice_Traffic_Tagging
Meso: VoIP quality; ensures phone calls are tagged EF (DSCP 46).
Macro: Collaboration experience; ensures clear audio for meetings.

Mismarked_Traffic
Meso: Configuration error; YouTube traffic tagged as 
Macro: Bandwidth management; enforces the intended QoS policy.

protocol_id
Meso: Traffic mix; identifies the underlying transport (TCP, UDP, ICMP).
Macro: Protocol support; ensures firewalls pass necessary protocols (e.g., GRE for VPNs).

Protocol_Distribution
Meso: Baseline; 90% TCP, 9% UDP, 1% ICMP is typical.
Macro: Anomaly detection; a shift to 50% UDP suggests a DDoS or new streaming app.

Unusual_Protocol
Meso: Security alert; seeing protocol 47 (GRE) where none is expected suggests a rogue tunnel.
Macro: Attack surface; blocks obscure protocols not required for business.

ICMP_Volume
Meso: Recon detection; high ICMP suggests a ping sweep.
Macro: Network visibility; allows necessary troubleshooting traffic while blocking abuse.

GRE_ESP_Tunnels
Meso: VPN tracking; monitors the health of site-to-site VPN tunnels.
Macro: Secure connectivity; ensures remote sites remain connected.

icmp_type
Meso: Message analysis; distinguishes between 
Macro: Troubleshooting; 

Unreachable_Rate
Meso: Configuration error; high unreachables suggest a router has no route to a destination.
Macro: Network availability; minimizes 

Echo_Request_Volume
Meso: Ping flood; a massive spike in pings triggers a rate limit.
Macro: Monitoring overhead; ensures monitoring tools aren't generating too much noise.

ICMP_Flood_Detection
Meso: DoS defense; blocks ICMP traffic exceeding a threshold.
Macro: Infrastructure protection; prevents router CPUs from being overwhelmed.

Redirect_Messages
Meso: Routing inefficiency; redirects mean the sender is using the wrong gateway.
Macro: Network optimization; fixing the sender's routing table removes the need for redirects.

bgp_peer_state
Meso: Peering health; tracks the status of BGP sessions with ISPs.
Macro: Internet connectivity; a down peer means loss of redundancy or connectivity.

Peer_Status
Meso: Alerting; a peer going from 
Macro: Vendor reliability; tracks the stability of ISP connections.

State_Flap_Detection
Meso: Instability; a peer bouncing up and down triggers a 
Macro: Route stability; prevents unstable routes from propagating to the internet.

Idle_Peer_Alert
Meso: Configuration check; a peer configured but never established suggests a mismatch.
Macro: Redundancy verification; ensures backup paths are actually ready to take traffic.

Prefix_Count_Change
Meso: Route leak; an ISP suddenly sending 800k routes (full table) instead of 10 crashes the router.
Macro: Routing security; validates that peers are sending the expected number of routes.

Session_Uptime
Meso: Stability metric; long uptime indicates a stable connection.
Macro: Operational excellence; aims for 100% uptime on core peering sessions.

route_next_hop
Meso: Forwarding decision; determines the immediate next step for a packet.
Macro: Traffic engineering; manipulating next hops steers traffic to cheaper or faster paths.

Next_Hop_Distribution
Meso: Load balancing; ensures traffic is spread evenly across available links.
Macro: Capacity utilization; prevents one link from being saturated while others are empty.

Next_Hop_Change
Meso: Rerouting event; traffic shifting to a backup path indicates a primary failure.
Macro: Failover testing; validates that backup paths work as expected.

Black_Hole_Routes
Meso: DDoS mitigation; routing traffic for a victim IP to 
Macro: Infrastructure protection; sacrifices one victim to save the rest of the network.

Path_Symmetry
Meso: Firewall health; ensures return traffic comes back to the same stateful firewall.
Macro: Network design; simplifies troubleshooting and security policy enforcement.

tunnel_id
Meso: Interface tracking; identifies specific virtual interfaces (Tunnel0, Tunnel1).
Macro: Overlay network; manages the complexity of SD-WAN and VPN topologies.

Tunnel_Status
Meso: Connectivity check; is the VPN tunnel UP or DOWN?
Macro: Site availability; ensures branch offices can reach the data center.

Tunnel_Flap_Detection
Meso: Link quality; flapping tunnels suggest packet loss on the underlay internet link.
Macro: SD-WAN performance; triggers an automatic switch to a better path (e.g., MPLS).

Tunnel_Latency
Meso: Performance monitoring; measures the delay across the virtual path.
Macro: App performance; high tunnel latency kills VDI and VoIP sessions.

Tunnel_Throughput
Meso: Capacity planning; monitors bandwidth usage inside the tunnel.
Macro: WAN sizing; ensures the overlay network has enough underlay bandwidth.

Failover_Events
Meso: Resilience tracking; counts how often the network has to switch paths.
Macro: Link stability; frequent failovers indicate a poor quality ISP.

vpc_id
Meso: Cloud segmentation; identifies which virtual cloud (AWS VPC) traffic belongs to.
Macro: Cloud architecture; enforces isolation between Prod, Dev, and Test environments.

VPC_Traffic_Distribution
Meso: Cost allocation; tracks traffic volume per VPC for chargeback.
Macro: Cloud spend; identifies which projects are driving data transfer costs.

Cross_VPC_Traffic
Meso: Peering monitoring; tracks traffic flowing between VPCs.
Macro: Security boundaries; ensures only authorized VPCs are talking to each other.

New_VPC_Detection
Meso: Shadow IT; a new VPC appearing without approval triggers an alert.
Macro: Governance; ensures all cloud resources are created via Infrastructure as Code (IaC).

VPC_Flow_Anomaly
Meso: Threat detection; unusual traffic patterns within a VPC suggest a compromise.
Macro: Cloud security; monitors the 

security_group_id
Meso: Firewall rule; identifies the specific AWS Security Group applied to an instance.
Macro: Micro-segmentation; enforces granular access controls at the instance level.

SG_Rule_Effectiveness
Meso: Rule cleanup; identifies rules that are never hit and can be removed.
Macro: Policy hygiene; keeps the firewall policy set clean and manageable.

Overly_Permissive_SG
Meso: Risk alert; an SG allowing 0.0.0.0/0 on port 22 is flagged immediately.
Macro: Compliance; ensures no administrative ports are exposed to the public internet.

SG_Change_Detection
Meso: Audit trail; logs who changed a security group and when.
Macro: Change control; ensures all firewall changes go through the approval process.

Unused_SG_Detection
Meso: Cleanup; identifies SGs not attached to any instances.
Macro: Cloud hygiene; removes clutter from the cloud environment.

SG_Deny_Spike
Meso: Attack detection; a spike in denies indicates someone probing the instance.
Macro: Threat visibility; highlights which resources are being targeted.

Layer 2: Data Link (L2)
src_mac
Meso: Asset identification; the physical address of the network card.
Macro: Inventory management; the ultimate source of truth for what hardware is on the wire.

Unique_MACs
Meso: Capacity planning; tracks the size of the MAC address table on switches.
Macro: Network sizing; ensures subnets are sized correctly for the device count.

New_MAC_Detection
Meso: NAC enforcement; a new MAC address on a secure port triggers a 
Macro: Asset inventory; ensures the CMDB is accurate and no unauthorized hardware is on the network.

MAC_Spoofing_Detection
Meso: Security alert; seeing the same MAC on two different ports triggers a shutdown.
Macro: Zero Trust; prevents attackers from impersonating trusted devices.

OUI_Distribution
Meso: Vendor analysis; identifies the manufacturer (Apple, Dell, Cisco) of devices.
Macro: Fleet composition; tracks the mix of vendors in the environment.

Rogue_Device_Detection
Meso: Security block; a Raspberry Pi detected on a printer port is isolated.
Macro: Physical security; prevents unauthorized hardware implants.

vlan_id
Meso: Segmentation; identifies the broadcast domain (e.g., VLAN 10 = Users).
Macro: Network architecture; separates traffic types (Voice, Data, Guest) for security and performance.

VLAN_Distribution
Meso: Load balancing; ensures users are spread evenly across available VLANs.
Macro: Subnet planning; prevents VLAN exhaustion.

VLAN_Hopping_Detection
Meso: Attack detection; a device trying to tag traffic for a different VLAN is blocked.
Macro: Switch hardening; validates that ports are configured as 

Native_VLAN_Traffic
Meso: Misconfiguration; traffic on VLAN 1 (Native) is often a security risk.
Macro: Best practices; ensures the Native VLAN is unused and secured.

Unused_VLAN_Detection
Meso: Cleanup; identifies VLANs with no active ports.
Macro: Configuration hygiene; removes dead config from switches.

interface
Meso: Physical connection; identifies the specific jack (Gi0/1) a user is plugged into.
Macro: Port management; tracks available capacity on switches.

Port_Utilization
Meso: Congestion; a port hitting 90% usage drops packets.
Macro: Capacity planning; identifies when to upgrade to 10Gbps uplinks.

Port_Flapping
Meso: Physical fault; a port going Up/Down rapidly suggests a bad cable.
Macro: Maintenance; drives the replacement of faulty cabling infrastructure.

Broadcast_Storm
Meso: Network meltdown; broadcast traffic >20% triggers storm control suppression.
Macro: Network hygiene; indicates a need for better segmentation (smaller VLANs).

Port_Error_Rate
Meso: Signal quality; errors indicate duplex mismatch or bad hardware.
Macro: Link reliability; ensures clean physical layer connectivity.

Duplex_Mismatch
Meso: Performance killer; one side Half, one side Full causes massive collisions.
Macro: Configuration standard; enforces 

frame_type
Meso: Protocol analysis; Ethernet II vs. 802.3.
Macro: Legacy support; identifies old devices using non-standard framing.

Frame_Type_Distribution
Meso: Baseline; mostly Ethernet II (IP).
Macro: Anomaly detection; a spike in non-IP frames suggests a legacy app issue.

Unusual_EtherType
Meso: Protocol discovery; seeing AppleTalk or IPX suggests legacy devices.
Macro: Network modernization; identifies targets for decommissioning.

ARP_Traffic_Volume
Meso: Broadcast noise; high ARP volume slows down all hosts on the subnet.
Macro: Subnet sizing; indicates VLANs are too large (too many hosts).

IPv6_Adoption
Meso: Meso: Modernization; tracks the migration from IPv4 to IPv6.
Macro: Future proofing; ensures the network is ready for the IPv4 address exhaustion.

stp_state
Meso: Loop prevention; Forwarding vs. Blocking.
Macro: Topology stability; ensures the Spanning Tree Protocol is building a loop-free path.

Blocking_Port_Count
Meso: Redundancy check; ensures redundant links are actually in Blocking mode (standby).
Macro: Network efficiency; too many blocking ports suggests wasted cabling.

STP_Topology_Change
Meso: Network blip; a TCN causes a temporary flood of traffic while MAC tables flush.
Macro: Stability monitoring; frequent changes indicate a flapping link somewhere.

Root_Bridge_Change
Meso: Critical event; a new switch taking over as Root can crash the network.
Macro: Configuration audit; ensures the Core Switch is hard-coded as Root.

Port_State_Flap
Meso: Instability; a port cycling through STP states prevents connectivity.
Macro: Edge protection; use 

Designated_Port_Ratio
Meso: Topology map; identifies which switches are downstream.
Macro: Tree structure; validates the hierarchical design of the network.

link_status
Meso: Up/Down; is the cable plugged in?
Macro: Availability; the most basic measure of network uptime.

Link_Availability
Meso: SLA metric; % of time the link is Up.
Macro: Vendor management; holds circuit providers to their uptime contracts.

Link_Down_Events
Meso: Incident log; counts how many times a link failed.
Macro: Reliability trend; increasing down events suggests failing hardware.

Flapping_Detection
Meso: Suppression; an interface flapping 5 times in 10 seconds is error-disabled.
Macro: Stability protection; prevents a bad link from destabilizing the routing table.

Critical_Link_Monitor
Meso: Alerting; a core uplink going down pages the entire team.
Macro: Risk management; identifies single points of failure.

MTTR
Meso: Operational speed; Mean Time To Repair a down link.
Macro: Team efficiency; measures how fast the NOC resolves outages.

input_discards
Meso: Congestion; the router has no buffer memory left to store the packet.
Macro: Capacity planning; indicates the need for hardware with larger buffers.

Discard_Rate
Meso: Quality impact; discards cause TCP backoff and slow apps.
Macro: Hardware sizing; ensures devices are sized for the traffic bursts.

Discard_Spike
Meso: Microburst; a split-second traffic spike fills the buffer.
Macro: Traffic engineering; smoothing out traffic flows to prevent drops.

input_errors
Meso: Physical corruption; the packet was mangled on the wire.
Macro: Layer 1 health; the primary indicator of bad cables or optics.

Error_Rate
Meso: Threshold; >1 error per million packets triggers a check.
Macro: Maintenance; drives the schedule for fiber cleaning and cable replacement.

CRC_Error_Spike
Meso: Interference; a sudden burst of errors suggests EMI (e.g., a motor starting).
Macro: Environmental audit; checks for electrical noise sources near cabling.

Error_Trend
Meso: Meso: Degradation; errors increasing over time suggest a failing component.
Macro: Predictive maintenance; replacing parts before they fail completely.

Hardware_Failure
Meso: Component death; massive errors on all ports suggests a bad ASIC.
Macro: Lifecycle management; tracking failure rates by vendor/model.

Error_Distribution
Meso: Isolation; errors on one port vs. all ports helps pinpoint the issue.
Macro: Troubleshooting; guides the technician to the switch or the patch panel.

neighbor_mac
Meso: Discovery; identifies the device connected to the other end (LLDP/CDP).
Macro: Topology mapping; automatically draws the network diagram.

Expected_Neighbors
Meso: Validation; ensures the Core Switch is connected to the Distribution Switch.
Macro: Design compliance; verifies the cabling matches the documentation.

Neighbor_Change
Meso: Alert; a neighbor changing suggests a cable was moved.
Macro: Change control; detects unauthorized cabling changes.

Missing_Neighbor
Meso: Fault detection; a link is Up but no neighbor is seen (one-way traffic).
Macro: Protocol health; ensures discovery protocols are running everywhere.

New_Neighbor_Detection
Meso: Rogue device; a 
Macro: Security audit; prevents unauthorized switches from extending the network.

arp_status
Meso: L2-L3 mapping; resolves IP addresses to MAC addresses.
Macro: Connectivity; without ARP, IP communication is impossible.

Incomplete_ARP_Rate
Meso: Scanning detection; high incomplete ARPs suggest scanning of empty IP space.
Macro: Subnet hygiene; identifies misconfigured hosts trying to reach dead IPs.

ARP_Timeout_Spike
Meso: Performance; slow ARP responses delay connection setup.
Macro: Control plane load; high ARP load can overwhelm the router CPU.

ARP_Cache_Size
Meso: Resource usage; tracks the number of active hosts on the subnet.
Macro: Hardware limits; ensures the router's memory isn't exhausted.

Duplicate_IP_Detection
Meso: Conflict alert; two MACs claiming the same IP triggers a log.
Macro: IPAM integrity; ensures unique IP assignment (DHCP vs. Static).

Layer 1: Physical (L1)
rssi
Meso: WiFi signal strength; -65dBm is good, -80dBm is bad.
Macro: Coverage quality; ensures the office has adequate WiFi signal everywhere.

Average_RSSI
Meso: Cell health; the average experience of clients on an AP.
Macro: Site survey; validates the AP placement design.

P10_RSSI
Meso: Edge users; the experience of the users with the worst signal.
Macro: Coverage gaps; identifies dead zones that need new APs.

Low_Signal_Clients
Meso: Roaming issue; a client sticking to a far AP needs to be kicked.
Macro: Client tuning; optimizing roaming aggressiveness on laptops.

RSSI_Anomaly
Meso: Obstruction; a sudden drop suggests a new wall or metal cabinet.
Macro: Environment monitoring; detects physical changes in the building.

Coverage_Holes
Meso: Dead zone; areas with no signal < -85dBm.
Macro: Remediation; drives the installation of fill-in APs.

RSSI_Distribution
Meso: Capacity planning; ensures clients are distributed across the signal range.
Macro: Design validation; confirms the cell sizing is correct.

snr
Meso: Signal quality; Signal-to-Noise Ratio determines the max speed.
Macro: RF health; high SNR is required for high-speed WiFi (MCS rates).

Average_SNR
Meso: Performance baseline; >25dB is required for voice/video.
Macro: User experience; correlates directly with throughput.

SNR_Anomaly
Meso: Interference; a drop in SNR without a drop in RSSI means noise increased.
Macro: Spectrum analysis; identifies sources of RF pollution.

Low_SNR_Clients
Meso: Performance drag; low SNR clients consume more airtime (slow data rates).
Macro: Airtime fairness; prevents one bad client from slowing down the whole AP.

SNR_vs_Throughput
Meso: Efficiency; validates that high SNR is actually delivering high speed.
Macro: Driver optimization; identifies client devices with poor radios.

channel
Meso: Frequency slot; 2.4GHz vs 5GHz channels.
Macro: Capacity planning; 5GHz offers more channels and capacity.

Channel_Utilization
Meso: Congestion; >50% utilization means the WiFi is slow.
Macro: Density planning; high utilization drives the need for smaller cells (more APs).

Co_Channel_Interference
Meso: Self-interference; APs on the same channel hearing each other slows everyone down.
Macro: Channel planning; optimizing the channel map to minimize overlap.

Channel_Change_Rate
Meso: Instability; frequent changes suggest the AP is 
Macro: RRM tuning; adjusting the sensitivity of the auto-channel algorithm.

DFS_Event_Rate
Meso: Radar detection; AP jumping off a DFS channel due to radar.
Macro: Spectrum availability; determines if DFS channels are usable in this location.

Channel_Width
Meso: Speed vs. Reliability; 80MHz is fast but prone to noise, 20MHz is stable.
Macro: Design strategy; balancing top speed against connection stability.

data_rate
Meso: Connection speed; the negotiated PHY rate (e.g., 866Mbps).
Macro: Technology generation; tracks the adoption of WiFi 6/6E/7.

Average_Data_Rate
Meso: Cell efficiency; higher average rate = more efficient use of airtime.
Macro: Device refresh; identifies old clients dragging down the average.

P10_Data_Rate
Meso: Legacy support; the speed of the slowest clients.
Macro: Minimum bitrate; setting a floor (e.g., disable 11Mbps) to force upgrades.

Low_Rate_Clients
Meso: Airtime hogs; clients connecting at 1Mbps consume 100x more airtime than at 100Mbps.
Macro: Configuration tuning; disabling low data rates improves overall capacity.

Rate_vs_RSSI
Meso: Client health; checks if clients are selecting the best rate for their signal.
Macro: Driver validation; identifies buggy client drivers.

retry_rate
Meso: Packet loss; % of WiFi frames that had to be resent.
Macro: RF quality; high retries kill real-time apps like VoIP.

Average_Retry_Rate
Meso: Health metric; <10% is good, >20% is bad.
Macro: Environment tuning; high retries suggest hidden nodes or interference.

Retry_Spike
Meso: Transient noise; a microwave running causes a spike in retries.
Macro: User complaints; correlates 

High_Retry_APs
Meso: Problem isolation; identifies specific APs in noisy areas.
Macro: Site remediation; moving APs away from interference sources.

Retry_vs_Channel_Util
Meso: Congestion impact; distinguishes between noise-based and congestion-based retries.
Macro: Capacity management; adding more APs fixes congestion, not noise.

noise_floor
Meso: Background noise; the level of non-WiFi RF energy (-95dBm).
Macro: RF environment; a clean noise floor is essential for good WiFi.

Average_Noise_Floor
Meso: Baseline; establishes the 
Macro: Site suitability; noisy environments (factories) need different hardware.

Interference_Spike
Meso: Connectivity drop; a microwave turning on causes packet loss; AP changes channels.
Macro: Spectrum management; identifies non-WiFi devices (Bluetooth, security cameras) polluting the airwaves.

High_Noise_APs
Meso: Location issue; APs near breakrooms or elevators often see high noise.
Macro: Deployment guidelines; avoiding placement near interference sources.

Noise_Trend
Meso: Degradation; noise increasing over time suggests new equipment was installed.
Macro: Environmental control; managing the RF spectrum as a shared resource.

optical_rx_power
Meso: Fiber health; light level received by the SFP (-10dBm).
Macro: Link budget; ensures fiber runs are within distance limits.

Rx_Power_Level
Meso: Signal strength; determines if the link is stable.
Macro: Installation quality; validates fiber cleaning and termination.

Low_Power_Alert
Meso: Link failure imminent; light level dropping to -25dBm triggers a 
Macro: Physical plant health; proactive maintenance prevents costly unplanned outages.

Power_Degradation
Meso: Dirty fiber; gradual loss of light suggests dust accumulation.
Macro: Maintenance schedule; prompts regular cleaning of fiber patch panels.

Link_Margin
Meso: Safety buffer; how much light can be lost before the link drops.
Macro: Reliability engineering; designing links with adequate margin for aging.

Asymmetric_Power
Meso: Single strand issue; good Tx but bad Rx suggests one broken fiber strand.
Macro: Troubleshooting; guides the tech to check a specific connector.

transceiver_temp
Meso: Component health; temperature of the SFP module.
Macro: Environmental monitoring; high temps suggest rack cooling issues.

Average_Temperature
Meso: Baseline; establishes normal operating range.
Macro: Hardware longevity; cooler components last longer.

Overheating_Alert
Meso: Hardware risk; >70C triggers a shutdown warning.
Macro: Cooling failure; indicates a failed fan or blocked airflow.

Temperature_Trend
Meso: AC failure; rising temps across all modules suggests the room AC died.
Macro: Facility management; monitors the health of the data center environment.

Thermal_Runaway
Meso: Fire risk; rapid temp rise triggers an emergency power off.
Macro: Safety compliance; protects the facility from hardware fires.

poe_power_draw
Meso: Power delivery; Watts consumed by the attached device (AP, Phone).
Macro: Energy efficiency; tracks the power consumption of the edge network.

Power_Per_Device
Meso: Device health; a phone drawing 0W is dead.
Macro: Budgeting; estimating the power bill for the network.

Total_Budget_Usage
Meso: Switch capacity; ensures the switch has enough power for all ports.
Macro: Hardware selection; buying switches with larger power supplies for high-power APs.

Power_Anomaly
Meso: Short circuit; a sudden spike in draw triggers a port shutdown.
Macro: Safety; prevents damaged cables from causing electrical issues.

Class_Mismatch
Meso: Configuration error; a Class 4 device requesting Class 3 power.
Macro: Compatibility; ensures devices negotiate the correct power level.

Power_Trend
Meso: Load profile; tracks power usage over the day (phones sleeping at night).
Macro: Green IT; optimizing power usage to reduce carbon footprint.

fan_status
Meso: Cooling active; fan RPM and health status.
Macro: Hardware reliability; active cooling is critical for switch life.

Fan_Health
Meso: Pass/Fail; is the fan spinning?
Macro: RMA tracking; identifying models with high fan failure rates.

Fan_Failure_Alert
Meso: Critical alarm; a stopped fan triggers an immediate replacement.
Macro: Uptime risk; a switch with one fan left is a ticking time bomb.

Fan_Speed_Anomaly
Meso: Airflow blockage; fans spinning at 100% suggests the intake is blocked.
Macro: Maintenance; prompts cleaning of dust filters.

Degraded_Cooling
Meso: Warning; temp rising despite max fan speed.
Macro: Environment check; is the ambient air too hot?

psu_status
Meso: Power input; status of the Power Supply Unit.
Macro: Power redundancy; ensures dual-PSU switches have both plugged in.

PSU_Health
Meso: Pass/Fail; is the PSU providing power?
Macro: Availability; dual PSUs allow for hitless failover.

PSU_Failure
Meso: Critical alarm; loss of a PSU removes redundancy.
Macro: Site resilience; ensures the switch stays up on the remaining PSU.

Redundancy_Status
Meso: Protection level; N+1 or N+N redundancy.
Macro: Risk acceptance; running on a single PSU is a risk.

Power_Input_Voltage
Meso: Quality check; 110V vs 220V input.
Macro: Facility power; monitors the stability of the utility power.

Load_Balance
Meso: Efficiency; are both PSUs sharing the load equally?
Macro: Hardware design; ensures optimal efficiency and lifespan.

Layer 0: Endpoint/Host (L0)
process_name
Meso: Execution tracking; what is running? (e.g., chrome.exe).
Macro: Software inventory; tracks what apps are actually being used.

Process_Execution_Volume
Meso: Anomaly; a sudden spawn of 1000 processes suggests a fork bomb.
Macro: Performance profiling; identifies resource-intensive applications.

Rare_Process_Detection
Meso: Malware execution; a process named svchost.exe running from C:\Temp is killed.
Macro: Threat hunting; identifies novel malware variants before signatures are available.

Process_Spawn_Rate
Meso: Behavior analysis; rapid spawning is typical of malware unpacking.
Macro: Heuristic tuning; adjusting thresholds to reduce false positives.

Living_Off_the_Land
Meso: Stealth attack; PowerShell downloading a file triggers an EDR alert.
Macro: Attack surface reduction; drives policies to restrict the use of admin tools by standard users.

process_hash
Meso: Integrity check; unique fingerprint (SHA256) of the binary.
Macro: Whitelisting; ensuring only approved binaries can run.

Known_Malware_Match
Meso: Blocking; hash matches a VirusTotal entry, execution is denied.
Macro: Threat landscape; tracks the prevalence of commodity malware.

Unknown_Hash_Detection
Meso: Zero-day risk; a never-before-seen binary triggers sandbox analysis.
Macro: Innovation vs. Risk; balancing developer freedom with strict execution control.

Hash_Diversity
Meso: Polymorphism; seeing 100 variants of the same file name suggests polymorphic malware.
Macro: Defense evasion; attackers changing hashes to bypass static signatures.

First_Seen_Hash
Meso: Alerting; new code appearing in the environment is flagged.
Macro: Change management; correlates new binaries with software deployments.

parent_process
Meso: Context; who started this? (e.g., Word spawning PowerShell).
Macro: Attack chain; visualizes the sequence of events in an exploit.

Process_Tree_Anomaly
Meso: Exploit detection; Outlook spawning cmd.exe is blocked.
Macro: Behavioral rules; defining 

Suspicious_Spawning
Meso: Persistence; a scheduled task spawning a temp file.
Macro: EDR efficacy; validates that behavioral rules are catching attacks.

Injection_Detection
Meso: Memory defense; one process writing to another's memory is blocked.
Macro: Advanced defense; protecting against fileless malware.

Execution_Chain_Length
Meso: Complexity; long chains (A->B->C->D) are suspicious.
Macro: Forensic depth; ensures logs capture the full history.

process_cmd_line
Meso: Intent analysis; arguments passed to the process (e.g., -Enc).
Macro: Visibility; command lines reveal what the attacker was trying to do.

Encoded_Command
Meso: Obfuscation; Base64 strings in command lines trigger alerts.
Macro: Policy; blocking the use of encoded commands by default.

Long_Command_Line
Meso: Evasion; extremely long commands try to buffer overflow logging tools.
Macro: Tool robustness; ensures security tools can handle large inputs.

Suspicious_Patterns
Meso: Signature match; IEX(New-Object Net.WebClient) is blocked.
Macro: Threat intelligence; updating patterns based on new TTPs.

PowerShell_Cmdlets
Meso: Usage tracking; monitors use of Invoke-WebRequest or Mimikatz.
Macro: Scripting governance; restricting PowerShell to signed scripts only.

registry_key
Meso: Configuration; Windows settings database.
Macro: System state; monitors changes to the OS configuration.

Run_Key_Modifications
Meso: Persistence; adding an entry to CurrentVersion\Run triggers an alert.
Macro: Baseline enforcement; keeping startup items clean.

Service_Registry_Changes
Meso: Privilege escalation; modifying a service binary path.
Macro: System hardening; locking down service permissions.

Persistence_Detection
Meso: Hunting; looking for hidden autostart locations (WMI, Scheduled Tasks).
Macro: Dwell time reduction; finding backdoors before they are used.

Unusual_Key_Access
Meso: Credential theft; reading LSA secrets keys is blocked.
Macro: OS security; protecting critical system secrets.

file_operation
Meso: Disk activity; creating, reading, or deleting files.
Macro: Data protection; monitoring access to sensitive documents.

File_Operations_Volume
Meso: Ransomware; rapid encryption/renaming of thousands of files triggers a kill switch.
Macro: Backup strategy; high change rates impact backup windows.

Mass_File_Changes
Meso: Bulk change detection; a spike in file writes indicates mass edits or encryption.
Macro: Data integrity; measures exposure to destructive file operations.

Shadow_Copy_Deletion
Meso: Recovery evasion; deleting shadow copies triggers an immediate ransomware alert.
Macro: Resilience posture; ensures recovery safeguards remain intact.

network_connection_local
Meso: Host network context; tracks local sockets for suspicious connections.
Macro: Endpoint visibility; strengthens correlation between host and network telemetry.

Outbound_Connections
Meso: Exfiltration signal; unusual outbound spikes trigger DLP checks.
Macro: Egress governance; validates that endpoints are not leaking data.

Rare_Destination
Meso: Anomaly detection; connections to uncommon IPs/domains raise risk.
Macro: Threat exposure; highlights emerging destinations outside normal business traffic.

Port_Anomaly
Meso: Policy violation; unexpected ports in use trigger a block or review.
Macro: Baseline hygiene; enforces standard port usage across endpoints.

usb_device_id
Meso: Device accountability; ties USB activity to a specific device fingerprint.
Macro: Peripheral governance; tracks removable media across the fleet.

USB_Insert_Volume
Meso: Insider risk; bursts of USB insertions trigger monitoring.
Macro: Control effectiveness; measures policy compliance around removable media.

Unknown_USB_Device
Meso: Threat alert; unrecognized USB devices prompt isolation.
Macro: Hardware assurance; prevents unmanaged devices from entering the environment.

USB_Write_Volume
Meso: Data leakage; large USB writes trigger an alert.
Macro: IP protection; reduces offline data theft risks.

After_Hours_USB
Meso: Timing anomaly; USB activity outside working hours flags review.
Macro: Insider threat; detects off-hours data movement patterns.

Accessibility (A)

Retainability (R)

Quality (Q)
