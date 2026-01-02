---
title: KTP-Audit - Flight Recorder Specification
description: The immutable memory of the KTP system, recording every decision, veto, and state change.
---

# KTP-Audit: Flight Recorder Specification

> "The invisible success problem: when security works, nothing happens. The Flight Recorder makes the invisible visible."

---

## At a Glance

| Property | Value |
|----------|-------|
| **Status** | :material-progress-clock:{ .draft } Draft |
| **Version** | 0.1 |
| **Dependencies** | [KTP-Core](ktp-core.md), [KTP-Transport](ktp-transport.md) |
| **Required By** | [KTP-Governance](ktp-governance.md), [KTP-Conformance](ktp-conformance.md) |

---

## The Problem
Traditional logs are often incomplete, mutable, or unstructured. When an incident occurs (or is prevented), it is difficult to reconstruct exactly *why* a decision was made. Was it a policy error? A sensor failure? A malicious agent?

## The Solution: The Flight Recorder
KTP-Audit defines a system for recording **Decision Geometry**—a multi-dimensional snapshot of the agent, the environment, and the logic used at the exact moment of a decision. These records are cryptographically chained to ensure immutability.

### Decision Geometry

```json
{
  "record_id": "dr-uuid-12345",
  "timestamp": "2025-11-25T14:32:07.123Z",
  "chain": {
    "previous_hash": "sha256:abc123...",
    "sequence_number": 1847392
  },
  "agent": {
    "id": "agent:7gen:optimized:a1b2c3d4",
    "e_base": 87,
    "e_trust": 42,
    "tier": "analyst"
  },
  "environment": {
    "context_tensor": { "m": 0.45, "p": 0.78, "h": 0.82 },
    "risk_factor": 0.523
  },
  "decision": {
    "outcome": "DENY",
    "reason": "silent_veto",
    "constraint": "soul_violation"
  }
}
```

---

## Record Types

=== "Authorization Decision"
    **The Core Record.**
    Logged every time an agent requests an action. Captures the $A \leq E$ calculation.
    
    *   **Use Case**: "Why was Agent X blocked from accessing the database?"

=== "Trust Score Change"
    **State Transition.**
    Logged when an agent's $E_{base}$ or $E_{trust}$ changes significantly.
    
    *   **Use Case**: "Why did Agent Y drop from Operator to Analyst tier?"

=== "Soul Veto"
    **Critical Event.**
    Logged when the Soul constraint triggers a hard stop.
    
    *   **Use Case**: "Investigate potential rogue agent behavior."

=== "System Event"
    **Infrastructure Health.**
    Logged when sensors fail, Oracles partition, or keys rotate.
    
    *   **Use Case**: "Diagnose the root cause of the zone outage."

---

## Storage Architecture

```mermaid
graph TD
    subgraph Hot [Hot Storage (Redis/Memcached)]
        R1[Recent Logs (1h)]
    end
    
    subgraph Warm [Warm Storage (Elasticsearch)]
        R2[Searchable Logs (30d)]
    end
    
    subgraph Cold [Cold Storage (S3/Glacier)]
        R3[Archived Logs (7y)]
    end

---

## Related Specifications

<div class="grid cards" markdown>

-   :material-book-open-variant:{ .lg .middle } **[KTP-Core](ktp-core.md)**

    ---

    The foundational protocol and the Zeroth Law ($A \leq E$).

-   :material-shield-check:{ .lg .middle } **[KTP-Conformance](ktp-conformance.md)**

    ---

    Defining the three levels of KTP compliance and certification.

-   :material-scale-balance:{ .lg .middle } **[KTP-Governance](ktp-governance.md)**

    ---

    The human-in-the-loop and algorithmic governance framework.

-   :material-lan:{ .lg .middle } **[KTP-Transport](ktp-transport.md)**

    ---

    The secure messaging and transport layer for KTP signals.

</div>
    end

    Oracle -->|Stream| Hot
    Hot -->|Batch| Warm
    Warm -->|Archive| Cold
```

---

## Forensic Reconstruction
Because the Flight Recorder captures the full **Environmental Snapshot**, investigators can "replay" a decision.

1.  **Load Snapshot**: Restore the exact state of the Context Tensor from the record.
2.  **Re-run Logic**: Feed the agent's request into the policy engine.
3.  **Verify Outcome**: Confirm that the decision matches the log.

This capability is critical for proving that the system behaved correctly during a security incident.

---

## Core Components

<div class="grid cards" markdown>

-   **Cryptographic Chaining**
    ---
    Each record includes the hash of the previous record, creating a tamper-evident blockchain-like structure.

-   **Counterfactual Analysis**
    ---
    Records can include "what-if" data: "If the risk factor had been 0.1 lower, this action would have been allowed."

-   **Compliance Export**
    ---
    Standardized formats for exporting logs to external auditors or SIEM systems.

-   **Liability Attribution**
    ---
    Using the logs to determine if a failure was due to human negligence, agent error, or environmental force majeure.

</div>

---

## Related Specifications

<div class="grid cards" markdown>

-   [**KTP-Threat Model**](ktp-threat-model.md)
    ---
    The threats that the Flight Recorder helps investigate.

-   [**KTP-Tensors**](ktp-tensors.md)
    ---
    The environmental data captured in every record.

-   [**KTP-Identity**](ktp-identity.md)
    ---
    The agent identity tracked across records.

-   [**KTP-Recovery**](ktp-recovery.md)
    ---
    How to use logs to reconstruct state after a failure.

</div>

---

## Official RFC Document

??? abstract "KTP-RFC-016: KTP-Audit (Raw Text)"

    ```text
    --8<-- "rfcs/ktp-audit.txt"
    ```

    *(Note: The raw text above is the authoritative technical specification. This page provides a user-friendly interface for that content.)*
