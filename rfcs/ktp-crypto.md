# KTP-Crypto — Cryptographic Specification

*The enforcement mechanism for Digital Physics*

---

> **Design Principle**: The Zeroth Law ($A \leq E$) is meaningless without cryptographic guarantees that Trust Proofs cannot be forged, trajectories cannot be falsified, and audit records cannot be altered.

---

## At a Glance

| Property | Value |
|----------|-------|
| **Status** | :material-check-circle:{ .stable } Stable |
| **Version** | 0.1 |
| **Dependencies** | [KTP-Core](ktp-core.md) |
| **Required By** | All KTP implementations |

---

## Design Principles

KTP cryptography follows five core principles:

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } **Conservative Choices**

    ---
    
    Prefer well-studied algorithms over novel constructions. Security margins exceed minimum requirements.

-   :material-swap-horizontal:{ .lg .middle } **Cryptographic Agility**

    ---
    
    Support algorithm negotiation for future transitions. No algorithm is permanent.

-   :material-layers:{ .lg .middle } **Defense in Depth**

    ---
    
    Multiple mechanisms protect critical assets. Single compromise ≠ total compromise.

-   :material-chip:{ .lg .middle } **Hardware Roots**

    ---
    
    High-value keys protected by hardware. Software-only acceptable only for Level 1.

-   :material-atom:{ .lg .middle } **Post-Quantum Awareness**

    ---
    
    Designed for eventual quantum threat. Hybrid schemes available now; mandatory transition planned.

</div>

---

## Conformance Levels

KTP defines three levels with increasing cryptographic requirements:

=== "Level 1 (Basic)"
    
    *Development, testing, and low-risk deployments*
    
    | Category | Requirement |
    |----------|-------------|
    | **Signature** | ECDSA P-256 or EdDSA Ed25519 |
    | **Hash** | SHA-256 |
    | **Encryption** | AES-128-GCM |
    | **Key Storage** | Software keystore (HSM recommended) |
    | **Threshold** | Not required (single Oracle) |

=== "Level 2 (Standard)"
    
    *Production deployments with moderate security*
    
    | Category | Requirement |
    |----------|-------------|
    | **Signature** | ECDSA P-256 + EdDSA Ed25519 + ECDSA P-384 |
    | **Hash** | SHA-256, SHA-384, SHA3-256 |
    | **Encryption** | AES-256-GCM, ChaCha20-Poly1305 |
    | **Key Storage** | HSM **required** for Oracle keys |
    | **Threshold** | Required (min 2-of-3, recommended 3-of-5) |

=== "Level 3 (Full)"
    
    *Critical infrastructure and federation anchors*
    
    | Category | Requirement |
    |----------|-------------|
    | **Signature** | ECDSA P-384 + EdDSA Ed448 + **Hybrid PQC** |
    | **Hash** | SHA-384, SHA3-384, SHAKE256 |
    | **Encryption** | AES-256-GCM + ChaCha20-Poly1305 |
    | **Key Storage** | FIPS 140-2 Level 3 HSM, multi-person control |
    | **Threshold** | Required (min 3-of-5, recommended 5-of-7) |

---

## Signature Schemes

### ECDSA

Elliptic Curve Digital Signature Algorithm per FIPS 186-4.

| Curve | Field Size | Security | JOSE alg |
|-------|-----------|----------|----------|
| P-256 | 256 bits | 128-bit | ES256 |
| P-384 | 384 bits | 192-bit | ES384 |
| P-521 | 521 bits | 256-bit | ES512 |

!!! warning "ECDSA Requirements"
    - **MUST** use deterministic ECDSA (RFC 6979) to prevent nonce reuse
    - **MUST** validate points are on the curve
    - **MUST** reject signatures with $s > n/2$ (low-s normalization)
    - Private keys **MUST** use cryptographically secure RNG

### EdDSA

Edwards-curve Digital Signature Algorithm per RFC 8032.

| Curve | Field Size | Security | JOSE alg |
|-------|-----------|----------|----------|
| Ed25519 | 255 bits | 128-bit | EdDSA |
| Ed448 | 448 bits | 224-bit | EdDSA |

!!! success "EdDSA Advantages"
    - Deterministic by design (no nonce to leak)
    - Faster signing and verification
    - Smaller attack surface
    - Simpler implementation
    
    **EdDSA is RECOMMENDED over ECDSA for new deployments.**

### Threshold Signatures

Threshold signatures require k-of-n Oracles to cooperate, preventing single-point-of-failure:

``` mermaid
flowchart LR
    subgraph Oracles["Oracle Mesh (5 nodes)"]
        O1["Oracle 1<br/>Share 1"]
        O2["Oracle 2<br/>Share 2"]
        O3["Oracle 3<br/>Share 3"]
        O4["Oracle 4<br/>Share 4"]
        O5["Oracle 5<br/>Share 5"]
    end
    
    O1 --> C["Coordinator"]
    O2 --> C
    O3 --> C
    
    C --> S["✅ Valid Signature<br/>(3-of-5)"]
```

| Scheme | Base Algorithm | Level Required |
|--------|---------------|----------------|
| **Shamir + ECDSA** | ECDSA | Level 2+ |
| **FROST** | Schnorr | Level 2+ (recommended) |
| **BLS Threshold** | BLS12-381 | Level 3 |

??? info "Threshold Configuration by Level"
    
    | Level | Minimum (k,n) | Recommended (k,n) | Max Latency |
    |-------|---------------|-------------------|-------------|
    | Level 1 | (1,1) | (1,1) | N/A |
    | Level 2 | (2,3) | (3,5) | 100ms |
    | Level 3 | (3,5) | (5,7) | 200ms |
    
    Threshold $k$ SHOULD be greater than $n/2$ to prevent split-brain scenarios.

---

## Hash Functions

### Selection by Context

| Context | Level 1 | Level 2 | Level 3 |
|---------|---------|---------|---------|
| Trust Proof hashing | SHA-256 | SHA-256 | SHA-384 |
| Flight Recorder chain | SHA-256 | SHA3-256 | SHA3-384 |
| Trajectory chain | SHA-256 | SHA-256 | SHA-384 |
| Key derivation | SHA-256 | SHA-512 | SHAKE256 |

??? abstract "Hash Function Details"
    
    **SHA-2 Family** (FIPS 180-4):
    
    | Algorithm | Output | Block | Usage |
    |-----------|--------|-------|-------|
    | SHA-256 | 256 bits | 512 bits | General |
    | SHA-384 | 384 bits | 1024 bits | High-security |
    | SHA-512 | 512 bits | 1024 bits | Key derivation |
    
    **SHA-3 Family** (FIPS 202):
    
    | Algorithm | Output | Usage |
    |-----------|--------|-------|
    | SHA3-256 | 256 bits | Flight Recorder |
    | SHA3-384 | 384 bits | Level 3 audit |
    | SHAKE256 | Variable | KDF (Level 3) |
    
    SHA-3 provides defense in depth against potential SHA-2 vulnerabilities.

---

## Symmetric Encryption

### AES-GCM

AES-GCM per NIST SP 800-38D:

| Variant | Key Size | Nonce | Tag |
|---------|----------|-------|-----|
| AES-128-GCM | 128 bits | 96 bits | 128 bits |
| AES-256-GCM | 256 bits | 96 bits | 128 bits |

### ChaCha20-Poly1305

ChaCha20-Poly1305 per RFC 8439:

| Key Size | Nonce | Tag |
|----------|-------|-----|
| 256 bits | 96 bits | 128 bits |

!!! tip "ChaCha20 Advantages"
    - Better performance on systems without AES-NI
    - Constant-time implementation is simpler
    - No weak-key classes
    
    Both **AES-256-GCM** and **ChaCha20-Poly1305** MUST be supported for Level 2+.

### Encryption Contexts

| Context | Algorithm | Key Source |
|---------|-----------|------------|
| Trust Proof (at rest) | AES-256-GCM | Zone key |
| Flight Recorder | AES-256-GCM | Audit key |
| Agent credentials | AES-256-GCM | Agent master key |
| Federation messages | ChaCha20-Poly1305 | Session key |
| Sensor data (in transit) | TLS 1.3 | TLS handshake |

---

## Key Management

### Key Types

``` mermaid
flowchart TB
    subgraph Oracle["Oracle Keys"]
        OS["🔐 Signing Keys<br/>(Threshold, HSM)"]
        OE["🔒 Encryption Keys"]
    end
    
    subgraph Agent["Agent Keys"]
        AS["✍️ Agent Signing"]
        AI["🆔 Identity Keys"]
    end
    
    subgraph Zone["Zone Keys"]
        ZM["🏛️ Zone Master"]
        ZF["🌐 Federation Keys"]
    end
    
    ZM --> OS
    ZM --> ZF
    OS --> AS
```

??? example "Oracle Signing Key Format"
    ```json
    {
      "key_type": "oracle_signing",
      "key_id": "oracle-zone-alpha-2025-001",
      "algorithm": "threshold-frost-ed25519-3of5",
      "public_key": "base64...",
      "created_at": "2025-01-01T00:00:00Z",
      "expires_at": "2027-01-01T00:00:00Z",
      "rotation_policy": "annual"
    }
    ```

### Key Lifecycle

| Phase | Action | Requirements |
|-------|--------|--------------|
| **Generation** | Create key material | HSM ceremony for Level 2+ |
| **Distribution** | Share to authorized parties | Threshold splitting |
| **Rotation** | Replace with new key | 18-month max lifetime |
| **Revocation** | Invalidate compromised key | Immediate propagation |

### Key Derivation

**HKDF** (RFC 5869) for deriving keys from shared secrets:

| Purpose | Info String |
|---------|-------------|
| Trust Proof encryption | `ktp-trust-proof-encrypt-v1` |
| Trajectory chain key | `ktp-trajectory-key-v1` |
| Oracle session key | `ktp-oracle-session-v1` |
| Federation channel key | `ktp-federation-channel-v1` |

**Argon2id** (RFC 9106) for password-based key derivation:

| Level | Memory | Iterations | Time |
|-------|--------|------------|------|
| Level 1 | 64 MiB | 3 | ~0.5s |
| Level 2 | 256 MiB | 4 | ~1.0s |
| Level 3 | 1 GiB | 6 | ~3.0s |

---

## Hardware Security Modules

### Requirements by Level

| Level | HSM Requirement |
|-------|-----------------|
| Level 1 | Recommended, not required |
| Level 2 | **Required** for Oracle signing keys |
| Level 3 | FIPS 140-2 Level 3 HSM, multi-person control, geographic distribution |

### Integration

``` mermaid
flowchart LR
    A["Trust Oracle"] --> P["PKCS#11 API"]
    P --> H["HSM"]
    H --> K["🔐 Key Material<br/>(never leaves HSM)"]
```

!!! danger "Key Protection"
    For Level 2+, Oracle signing keys **MUST**:
    
    - Be generated inside the HSM
    - Never be exported in plaintext
    - Require multi-factor authentication
    - Support threshold operations

---

## Post-Quantum Cryptography

### Threat Timeline

!!! warning "Quantum Threat"
    Current estimates suggest cryptographically relevant quantum computers may exist within 10-15 years. KTP implements hybrid schemes **now** to protect long-lived data.

### Hybrid Signatures

Level 3 requires **hybrid signatures** combining classical and post-quantum algorithms:

| Component | Algorithm | Purpose |
|-----------|-----------|---------|
| Classical | ECDSA P-384 or EdDSA Ed448 | Current security |
| Post-Quantum | ML-DSA (Dilithium) | Future security |

``` mermaid
flowchart LR
    M["Message"] --> C["Classical Sign<br/>(EdDSA)"]
    M --> Q["PQC Sign<br/>(ML-DSA)"]
    C --> H["Hybrid Signature"]
    Q --> H
```

### Migration Strategy

| Phase | Timeline | Action |
|-------|----------|--------|
| **Prepare** | Now | Hybrid schemes available, optional |
| **Recommend** | 2027 | Hybrid recommended for Level 3 |
| **Require** | 2030 | Hybrid mandatory for Level 2+ |
| **Classical-only** | 2035 | No longer permitted |

---

## Algorithm Deprecation

When algorithms are deprecated:

1. **ANNOUNCE** — 18-month notice before mandatory transition
2. **WARN** — Log warnings when deprecated algorithm used
3. **REJECT** — Reject deprecated algorithm
4. **REMOVE** — Remove from specification

| Algorithm | Status | Notes |
|-----------|--------|-------|
| RSA-2048 | ❌ NOT SUPPORTED | Never permitted |
| SHA-1 | ❌ NOT SUPPORTED | Never permitted |
| ECDSA P-256 | ✅ SUPPORTED | Deprecation TBD (post PQC) |
| EdDSA Ed25519 | ✅ SUPPORTED | Long-term support |

---

## Related Specifications

??? info "Related Specifications"
    - [KTP-Core](ktp-core.md): Trust physics that cryptography enforces.
    - [KTP-Identity](ktp-identity.md): Identity chains and cryptographic lineage.
    - [KTP-Transport](ktp-transport.md): Secure transport and proof propagation.
    - [KTP-Federation](ktp-federation.md): Cross-zone cryptographic trust.
    - [KTP-Conformance](ktp-conformance.md): Compliance requirements for algorithms.

---

## Official RFC Document

!!! abstract "IETF Submission Format"
    The text below is the canonical RFC specification intended for IETF submission. It contains the complete, authoritative technical specification.

??? note "View Complete RFC Text (ktp-crypto.txt)"
    ```
    --8<-- "rfcs/ktp-crypto.txt"
    ```
