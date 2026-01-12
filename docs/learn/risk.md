# Risk & Deflation

*How threats, vulnerabilities, and violations reduce your effective trust*

<div class="ktp-animate" markdown>

Trust in KTP isn't just earned through good behavior—it's actively **deflated by risk**. The system applies risk as a multiplicative friction coefficient, ensuring that operational excellence cannot mask underlying vulnerabilities.(1)
{ .annotate }

1. :material-star-four-points-circle: Risk deflation mechanics are specified in [KTP-CORE](../rfcs/ktp-core.md) Section 5.3, "Risk Factor Calculation."

</div>

---

## The Deflation Formula

<div class="ktp-animate" markdown>

Your effective trust is always less than or equal to your base performance:

</div>

<div class="risk-deflation-hero ktp-animate">
  <div class="risk-equation">
    <div class="risk-equation-part risk-equation-raw">
      <span class="risk-label">Base Trust</span>
      <span class="risk-value">E_base</span>
    </div>
    <span class="risk-equation-operator">×</span>
    <div class="risk-equation-part risk-equation-factor">
      <span class="risk-label">Risk Factor</span>
      <span class="risk-value">∏(1 - Rᵢ)</span>
    </div>
    <span class="risk-equation-operator">=</span>
    <div class="risk-equation-part risk-equation-final">
      <span class="risk-label">Effective Trust</span>
      <span class="risk-value">E_trust</span>
    </div>
  </div>
  <p class="risk-equation-caption">Multiple risks compound—they don't simply add</p>
</div>

---

## Risk Categories

<div class="ktp-animate" markdown>

KTP recognizes four distinct risk categories, each measured and applied independently:(1)
{ .annotate }

1. :material-star-four-points-circle: Risk category taxonomy aligns with the Context Tensor dimensions. See [KTP-TENSORS](../rfcs/ktp-tensors.md) Section 4, "Heat Dimension."

</div>

<div class="risk-category-cards ktp-animate">
  <div class="risk-category-card risk-category-card--security">
    <div class="risk-category-card-header">
      <div class="risk-category-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,7C13.4,7 14.8,8.1 14.8,9.5V11C15.4,11 16,11.6 16,12.3V15.8C16,16.4 15.4,17 14.7,17H9.2C8.6,17 8,16.4 8,15.7V12.2C8,11.6 8.6,11 9.2,11V9.5C9.2,8.1 10.6,7 12,7M12,8.2C11.2,8.2 10.5,8.7 10.5,9.5V11H13.5V9.5C13.5,8.7 12.8,8.2 12,8.2Z"/></svg>
      </div>
      <strong>Security Risk</strong>
    </div>
    <p>Vulnerabilities and active threats that expose the system to compromise.</p>
    <ul>
      <li>Unpatched CVEs (High)</li>
      <li>Exposed credentials (Critical)</li>
      <li>Active threat indicators (Critical)</li>
      <li>Missing encryption (High)</li>
    </ul>
  </div>
  <div class="risk-category-card risk-category-card--compliance">
    <div class="risk-category-card-header">
      <div class="risk-category-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20M9,13V19H7V13H9M15,15V19H13V15H15M11,11V19H17V11H11Z"/></svg>
      </div>
      <strong>Compliance Risk</strong>
    </div>
    <p>Regulatory and policy violations that create legal or governance exposure.</p>
    <ul>
      <li>Regulatory violations (High)</li>
      <li>Audit failures (Medium)</li>
      <li>Expired certifications (Low)</li>
      <li>Data residency violations (High)</li>
    </ul>
  </div>
  <div class="risk-category-card risk-category-card--behavioral">
    <div class="risk-category-card-header">
      <div class="risk-category-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z"/></svg>
      </div>
      <strong>Behavioral Risk</strong>
    </div>
    <p>Anomalous patterns that deviate from established baselines.</p>
    <ul>
      <li>Sudden capability changes (Medium)</li>
      <li>Baseline deviation (Variable)</li>
      <li>Unusual access patterns (Medium)</li>
      <li>Timing anomalies (Low)</li>
    </ul>
  </div>
  <div class="risk-category-card risk-category-card--operational">
    <div class="risk-category-card-header">
      <div class="risk-category-card-icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M4,1H20A1,1 0 0,1 21,2V6A1,1 0 0,1 20,7H4A1,1 0 0,1 3,6V2A1,1 0 0,1 4,1M4,9H20A1,1 0 0,1 21,10V14A1,1 0 0,1 20,15H4A1,1 0 0,1 3,14V10A1,1 0 0,1 4,9M4,17H20A1,1 0 0,1 21,18V22A1,1 0 0,1 20,23H4A1,1 0 0,1 3,22V18A1,1 0 0,1 4,17M9,5H10V3H9V5M9,13H10V11H9V13M9,21H10V19H9V21M5,3V5H7V3H5M5,11V13H7V11H5M5,19V21H7V19H5Z"/></svg>
      </div>
      <strong>Operational Risk</strong>
    </div>
    <p>Infrastructure and reliability concerns that affect availability.</p>
    <ul>
      <li>Single points of failure (Medium)</li>
      <li>Insufficient redundancy (Low)</li>
      <li>Capacity exhaustion (Medium)</li>
      <li>Dependency vulnerabilities (High)</li>
    </ul>
  </div>
</div>

---

## How Risks Compound

<div class="ktp-animate" markdown>

Risks multiply rather than add. This prevents agents from offsetting severe risks with excellence elsewhere.

</div>

<div class="risk-compound ktp-animate">
  <div class="risk-compound-title">
    <h4>Compounding Example</h4>
    <p>Three risks, one result</p>
  </div>
  <div class="risk-factor-row">
    <span class="risk-factor-label">Security</span>
    <div class="risk-factor-bar-container">
      <div class="risk-factor-bar risk-factor-bar--security" style="width: 25%"></div>
    </div>
    <span class="risk-factor-value">25%</span>
  </div>
  <div class="risk-factor-row">
    <span class="risk-factor-label">Compliance</span>
    <div class="risk-factor-bar-container">
      <div class="risk-factor-bar risk-factor-bar--compliance" style="width: 10%"></div>
    </div>
    <span class="risk-factor-value">10%</span>
  </div>
  <div class="risk-factor-row">
    <span class="risk-factor-label">Behavioral</span>
    <div class="risk-factor-bar-container">
      <div class="risk-factor-bar risk-factor-bar--behavioral" style="width: 5%"></div>
    </div>
    <span class="risk-factor-value">5%</span>
  </div>
  <div class="risk-compound-result">
    <span class="risk-compound-result-label">Total Deflation</span>
    <span class="risk-compound-result-value">36%</span>
  </div>
  <div class="risk-compound-formula">0.75 × 0.90 × 0.95 = 0.64</div>
</div>

!!! warning "Why Multiplication Matters"
    If risks simply added (25% + 10% + 5% = 40%), an agent could game the system by achieving excellence in one area to offset failures elsewhere. Multiplication ensures that **every risk category matters**—you can't hide a critical vulnerability behind perfect compliance.

---

## Risk Thresholds

<div class="ktp-animate" markdown>

Different trust tiers have different risk tolerances. As risk increases, agents are automatically demoted to lower-privilege tiers:(1)
{ .annotate }

1. :material-star-four-points-circle: Trust tier definitions and transitions are specified in [KTP-CORE](../rfcs/ktp-core.md) Section 6, "Trust Tiers."

</div>

<div class="risk-tiers ktp-animate">
  <div class="risk-tier risk-tier--god">
    <div class="risk-tier-badge">≤5%</div>
    <div class="risk-tier-content">
      <strong>God Mode</strong>
      <span>Immediate demotion if exceeded</span>
    </div>
  </div>
  <div class="risk-tier risk-tier--operator">
    <div class="risk-tier-badge">≤15%</div>
    <div class="risk-tier-content">
      <strong>Operator</strong>
      <span>Warning, restricted actions</span>
    </div>
  </div>
  <div class="risk-tier risk-tier--analyst">
    <div class="risk-tier-badge">≤30%</div>
    <div class="risk-tier-content">
      <strong>Analyst</strong>
      <span>Degraded permissions</span>
    </div>
  </div>
  <div class="risk-tier risk-tier--observer">
    <div class="risk-tier-badge">≤50%</div>
    <div class="risk-tier-content">
      <strong>Observer</strong>
      <span>Read-only enforcement</span>
    </div>
  </div>
  <div class="risk-tier risk-tier--hibernation">
    <div class="risk-tier-badge">>50%</div>
    <div class="risk-tier-content">
      <strong>Hibernation</strong>
      <span>Dormant, no actions permitted</span>
    </div>
  </div>
</div>

---

## Mitigation Strategies

<div class="ktp-animate" markdown>

Risk can be reduced through four primary strategies:

</div>

<div class="mitigation-cards ktp-animate">
  <div class="mitigation-card">
    <div class="mitigation-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M13.78 15.3L19.78 21.3L21.89 19.14L15.89 13.14L13.78 15.3M17.5 10.1C17.11 10.1 16.69 10.05 16.36 9.91L4.97 21.25L2.86 19.14L10.27 11.74L8.5 9.96L7.78 10.66L6.33 9.25V12.11L5.63 12.81L2.11 9.25L2.81 8.55H5.62L4.22 7.14L7.78 3.58C8.95 2.41 10.83 2.41 12 3.58L9.89 5.74L11.27 7.11L10.57 7.81L12.38 9.63L14.54 7.46C14.39 7.14 14.34 6.72 14.34 6.33C14.34 4.54 15.76 3.11 17.5 3.11C18.09 3.11 18.61 3.25 19.08 3.53L16.41 6.2L17.91 7.7L20.58 5.03C20.86 5.5 21 6 21 6.63C21 8.34 19.58 9.76 17.84 9.76L17.5 10.1Z"/></svg>
    </div>
    <div class="mitigation-card-content">
      <strong>Remediation</strong>
      <span>Fix the underlying issue—patch, rotate credentials, reconfigure</span>
    </div>
  </div>
  <div class="mitigation-card">
    <div class="mitigation-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M23,12L20.56,9.22L20.9,5.54L17.29,4.72L15.4,1.54L12,3L8.6,1.54L6.71,4.72L3.1,5.53L3.44,9.21L1,12L3.44,14.78L3.1,18.47L6.71,19.29L8.6,22.47L12,21L15.4,22.46L17.29,19.28L20.9,18.46L20.56,14.78L23,12M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z"/></svg>
    </div>
    <div class="mitigation-card-content">
      <strong>Attestation</strong>
      <span>Third-party verification that risk is addressed</span>
    </div>
  </div>
  <div class="mitigation-card">
    <div class="mitigation-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2C17.5 2 22 6.5 22 12S17.5 22 12 22 2 17.5 2 12 6.5 2 12 2M12 4C10.1 4 8.4 4.6 7.1 5.7L18.3 16.9C19.3 15.5 20 13.8 20 12C20 7.6 16.4 4 12 4M16.9 18.3L5.7 7.1C4.6 8.4 4 10.1 4 12C4 16.4 7.6 20 12 20C13.9 20 15.6 19.4 16.9 18.3Z"/></svg>
    </div>
    <div class="mitigation-card-content">
      <strong>Isolation</strong>
      <span>Contain blast radius through segmentation</span>
    </div>
  </div>
  <div class="mitigation-card">
    <div class="mitigation-card-icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"/></svg>
    </div>
    <div class="mitigation-card-content">
      <strong>Monitoring</strong>
      <span>Increased observation to detect exploitation</span>
    </div>
  </div>
</div>

---

## Related

<div class="grid cards ktp-animate" markdown>

-   :material-cube-outline:{ .lg .middle } **Context Tensor**

    ---

    See how risk is measured through the Heat dimension.

    [:octicons-arrow-right-24: Context Tensor](context-tensor.md#__tabbed_2_4)

-   :material-chart-timeline-variant:{ .lg .middle } **Telemetry**

    ---

    Understand how risk signals flow through the pipeline.

    [:octicons-arrow-right-24: Telemetry](telemetry.md)

-   :material-book-open-variant:{ .lg .middle } **Core Concepts**

    ---

    Learn about trust tiers and the Zeroth Law.

    [:octicons-arrow-right-24: Core Concepts](core-concepts.md)

</div>
