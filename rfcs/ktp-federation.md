---
title: KTP-Federation - Trust Federation Specification
description: Enabling portable trust and reputation across the network of Blue Zones.
---

# KTP-Federation: Trust Federation Specification

> "Without federation, each zone is an island. With federation, trust becomes a portable asset that compounds across the network."

---

## At a Glance

| Property | Value |
|----------|-------|
| **Status** | :material-progress-clock:{ .draft } Draft |
| **Version** | 0.1 |
| **Dependencies** | [KTP-Core](ktp-core.md), [KTP-Identity](ktp-identity.md), [KTP-Zones](ktp-zones.md) |
| **Required By** | [KTP-Governance](ktp-governance.md), [KTP-Migration](ktp-migration.md) |

---

## The Problem
In a fragmented network, an agent must rebuild its reputation from zero every time it enters a new environment. This creates friction and disincentivizes long-term good behavior. Conversely, bad actors can "zone hop" to escape the consequences of their actions.

## The Solution: Trust Federation
KTP-Federation allows [**Blue Zones**](ktp-zones.md) to establish formal trust relationships. This enables:
1.  **Portable Reputation**: An agent's history in Zone A carries weight in Zone B.
2.  **Global Accountability**: Negative actions in one zone propagate to others.
3.  **Sovereignty**: Each zone retains full control over its own policies while participating in the network.

### Federation Models

=== "Bilateral"
    **Direct Partnership.**
    Two zones agree to trust each other directly. Simple and effective for close partners.
    
    ```mermaid
    graph LR
        A[Zone A] <-->|Trust 0.9| B[Zone B]
    ```

=== "Hub & Spoke"
    **Centralized Trust.**
    A central "Hub" zone acts as a trust anchor for multiple "Spoke" zones. Efficient for corporate or government hierarchies.
    
    ```mermaid
    graph TD
        H[Hub Zone]
        S1[Spoke 1]
        S2[Spoke 2]
        S3[Spoke 3]
        
        H <-->|1.0| S1
        H <-->|1.0| S2
        H <-->|0.8| S3
        S1 -.->|Via Hub| S2
    ```

=== "Mesh"
    **Decentralized Network.**
    Many zones with direct relationships to each other. No central authority. Trust is calculated via pathfinding.
    
    ```mermaid
    graph LR
        A[Zone A] --- B[Zone B]
        B --- C[Zone C]
        C --- A
        A --- D[Zone D]
        D --- B
    ```

---

## Trust Factor Calculation
When an agent moves from Zone A to Zone B, its effective trust is modified by the **Trust Factor ($T_f$)** between the zones.

$$E_{effective} = E_{base} \times T_f$$

Where:
*   $E_{base}$ is the agent's earned trust in its home zone.
*   $T_f$ is the negotiated trust level between the zones (0.0 to 1.0).

### Trust Propagation
Trust events propagate across the federation network:

*   **Forward Propagation**: Positive actions increase reputation in federated zones.
*   **Backward Propagation**: Negative actions (violations) decrease reputation in previously visited zones.

!!! warning "Transitivity Limits"
    Trust is not infinitely transitive. If Zone A trusts Zone B, and Zone B trusts Zone C, Zone A does **not** automatically trust Zone C unless explicitly configured.

---

## Federation Agreement

A formal JSON contract specifying trust factors, expiration dates, and dispute resolution protocols.

- **Cross-Zone Attestation:** Cryptographic proofs co-signed by multiple Zone Authorities.
- **Trust Decay:** External reputation decays unless reinforced by local good behavior.
- **Dispute Resolution:** Protocols for handling disagreements between zones.

## Related Specifications

??? info "Related Specifications"
    - [KTP-Core](ktp-core.md): Trust physics that federation relies on.
    - [KTP-Identity](ktp-identity.md): Portable identity and reputation signals.
    - [KTP-Zones](ktp-zones.md): Zone boundaries and trust domains.
    - [KTP-Governance](ktp-governance.md): Negotiation and oversight frameworks.
    - [KTP-Migration](ktp-migration.md): Trust portability during zone transitions.

---

## Official RFC Document

??? note "View Complete RFC Text (ktp-federation.txt)"
    ```text
    --8<-- "rfcs-txt/ktp-federation.txt"
    ```
