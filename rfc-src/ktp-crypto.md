---
title: "Kinetic Trust Protocol (KTP) - Cryptographic Specification"
abbrev: "KTP-CRYPTO"
date: 2026-08-13
category: exp
ipr: trust200902

author:
  -
    fullname: Chris Perkins
    organization: NMCITRA
    email: cperkins@nmcitra.org

normative:
  RFC2119:
  RFC5869:
  RFC6979:
  RFC7515:
  RFC8032:
  RFC8439:
  RFC9106:
  RFC8174:
informative:
  FIPS202:
    title: "SHA-3 Standard: Permutation-Based Hash and Extendable-Output Functions"
    author:
      - name: Chris Perkins
    date: 2015-08
  FROST:
    title: "FROST: Flexible Round- Optimized Schnorr Threshold Signatures"
    author:
      - name: Chris Perkins
  ML-DSA:
    title: "Module- Lattice-Based Digital Signature Standard"
    author:
      - name: Chris Perkins

--- abstract

This document specifies the cryptographic requirements for the Kinetic Trust Protocol (KTP). It consolidates all cryptographic algorithms, key management procedures, credential formats, and security parameters required for conformant implementations.

The specification covers signature schemes, hash functions, key derivation, threshold cryptography, hardware security module integration, key lifecycle management, and post-quantum cryptography considerations.

--- middle

# Introduction

Cryptography is the enforcement mechanism for the trust model. The Zeroth Law (A ≤ E) is meaningless without cryptographic guarantees that Trust Proofs cannot be forged, trajectories cannot be falsified, and audit records cannot be altered.

This specification consolidates all cryptographic requirements from across the KTP RFC series into a single normative document.

## Design Principles

KTP cryptography follows these principles:

1. CONSERVATIVE CHOICES Prefer well-studied algorithms over novel constructions. Security margins should exceed minimum requirements.

1. CRYPTOGRAPHIC AGILITY Support algorithm negotiation to enable future transitions. No algorithm is permanent; all must be replaceable.

1. DEFENSE IN DEPTH Multiple cryptographic mechanisms protect critical assets. Compromise of one mechanism should not compromise all.

1. HARDWARE ROOTS High-value keys should be protected by hardware. Software-only protection is acceptable only for Level 1.

1. POST-QUANTUM AWARENESS Design for eventual quantum computer threat. Hybrid schemes available now; mandatory transition planned.

## Requirements Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}} when, and only when, they appear in all capitals, as shown here.

# Terminology

This document uses the following terms:

Signing Key: Private key used to create digital signatures.

Verification Key: Public key used to verify digital signatures.

Threshold Signature: Signature requiring k-of-n parties to cooperate.

Key Ceremony: Formal procedure for generating or rotating keys.

HSM (Hardware Security Module): Tamper-resistant hardware for key protection.

PQC (Post-Quantum Cryptography): Algorithms resistant to quantum computer attacks.

Hybrid Signature: Combination of classical and post-quantum signatures.

Key Epoch: Time period during which a key is valid.

# Algorithm Requirements by Level

KTP defines three conformance levels with increasing cryptographic requirements.

## Level 1 (Basic)

Level 1 is suitable for development, testing, and low-risk deployments. It prioritizes ease of implementation.

~~~
Signature Algorithms (one REQUIRED):
+-------------------------------------------------------------------+
| Algorithm      | Curve/Params    | Security Level | Status       |
+-------------------------------------------------------------------+
| ECDSA          | P-256 (secp256r1)| 128-bit       | REQUIRED     |
| EdDSA          | Ed25519         | 128-bit        | RECOMMENDED  |
+-------------------------------------------------------------------+
~~~

~~~
Hash Functions (one REQUIRED):
+-------------------------------------------------------------------+
| Algorithm      | Output Size     | Security Level | Status       |
+-------------------------------------------------------------------+
| SHA-256        | 256 bits        | 128-bit        | REQUIRED     |
| SHA-384        | 384 bits        | 192-bit        | OPTIONAL     |
+-------------------------------------------------------------------+
~~~

~~~
Symmetric Encryption (if needed):
+-------------------------------------------------------------------+
| Algorithm      | Key Size        | Security Level | Status       |
+-------------------------------------------------------------------+
| AES-128-GCM    | 128 bits        | 128-bit        | REQUIRED     |
| AES-256-GCM    | 256 bits        | 256-bit        | RECOMMENDED  |
+-------------------------------------------------------------------+
~~~

Key Storage:

- Software keystore acceptable
- HSM RECOMMENDED but not required
- Key encryption at rest REQUIRED

Threshold Signatures:

- NOT REQUIRED for Level 1
- Single Oracle signature acceptable

## Level 2 (Standard)

Level 2 is suitable for production deployments with moderate security requirements.

~~~
Signature Algorithms (all REQUIRED):
+-------------------------------------------------------------------+
| Algorithm      | Curve/Params    | Security Level | Status       |
+-------------------------------------------------------------------+
| ECDSA          | P-256           | 128-bit        | REQUIRED     |
| EdDSA          | Ed25519         | 128-bit        | REQUIRED     |
| ECDSA          | P-384           | 192-bit        | RECOMMENDED  |
+-------------------------------------------------------------------+
~~~

~~~
Hash Functions (all listed REQUIRED):
+-------------------------------------------------------------------+
| Algorithm      | Output Size     | Use Case                      |
+-------------------------------------------------------------------+
| SHA-256        | 256 bits        | General hashing               |
| SHA-384        | 384 bits        | High-security contexts        |
| SHA3-256       | 256 bits        | Flight Recorder (recommended) |
+-------------------------------------------------------------------+
~~~

~~~
Symmetric Encryption:
+-------------------------------------------------------------------+
| Algorithm      | Key Size        | Security Level | Status       |
+-------------------------------------------------------------------+
| AES-256-GCM    | 256 bits        | 256-bit        | REQUIRED     |
| ChaCha20-Poly  | 256 bits        | 256-bit        | RECOMMENDED  |
+-------------------------------------------------------------------+
~~~

Key Storage:

- HSM REQUIRED for Oracle signing keys
- Software keystore acceptable for agent keys
- Key encryption at rest REQUIRED
- Key backup procedures REQUIRED

Threshold Signatures:

- REQUIRED for Trust Proof issuance
- Minimum threshold: 2-of-3
- RECOMMENDED threshold: 3-of-5

## Level 3 (Full)

Level 3 is suitable for critical infrastructure, high-security environments, and federation anchor nodes.

~~~
Signature Algorithms (all REQUIRED):
+-------------------------------------------------------------------+
| Algorithm      | Curve/Params    | Security Level | Status       |
+-------------------------------------------------------------------+
| ECDSA          | P-384           | 192-bit        | REQUIRED     |
| EdDSA          | Ed448           | 224-bit        | REQUIRED     |
| Hybrid PQC     | See Section 11  | Post-quantum   | REQUIRED     |
+-------------------------------------------------------------------+
~~~

~~~
Hash Functions:
+-------------------------------------------------------------------+
| Algorithm      | Output Size     | Use Case                      |
+-------------------------------------------------------------------+
| SHA-384        | 384 bits        | General hashing               |
| SHA3-384       | 384 bits        | Flight Recorder               |
| SHAKE256       | Variable        | Key derivation                |
+-------------------------------------------------------------------+
~~~

~~~
Symmetric Encryption:
+-------------------------------------------------------------------+
| Algorithm      | Key Size        | Security Level | Status       |
+-------------------------------------------------------------------+
| AES-256-GCM    | 256 bits        | 256-bit        | REQUIRED     |
| ChaCha20-Poly  | 256 bits        | 256-bit        | REQUIRED     |
+-------------------------------------------------------------------+
~~~

Key Storage:

- FIPS 140-2 Level 3 (or equivalent) HSM REQUIRED
- Multi-person access control REQUIRED
- Geographic distribution REQUIRED
- Key ceremony with witnesses REQUIRED

Threshold Signatures:

- REQUIRED for all Oracle operations
- Minimum threshold: 3-of-5
- RECOMMENDED threshold: 5-of-7
- Geographic distribution of key shares REQUIRED

# Signature Schemes

## ECDSA

ECDSA (Elliptic Curve Digital Signature Algorithm) per FIPS 186-4.

~~~
Supported Curves:
+-------------------------------------------------------------------+
| Curve          | Field Size     | Security Level | JOSE alg      |
+-------------------------------------------------------------------+
| P-256          | 256 bits       | 128-bit        | ES256         |
| P-384          | 384 bits       | 192-bit        | ES384         |
| P-521          | 521 bits       | 256-bit        | ES512         |
+-------------------------------------------------------------------+
~~~

Requirements:

1. Implementations MUST use deterministic ECDSA (RFC 6979) to prevent nonce reuse vulnerabilities.

1. Implementations MUST validate that points are on the curve before use.

1. Implementations MUST reject signatures with s > n/2 (low-s normalization) to prevent malleability.

1. Private keys MUST be generated using cryptographically secure random number generators.

Signature Format:

ECDSA signatures in KTP use the compact representation:

~~~
   signature = r || s
~~~

Where r and s are fixed-size big-endian integers (32 bytes for P-256, 48 bytes for P-384, 66 bytes for P-521).

For JWS/JWT contexts, signatures are base64url-encoded.

## EdDSA

EdDSA (Edwards-curve Digital Signature Algorithm) per RFC 8032.

~~~
Supported Curves:
+-------------------------------------------------------------------+
| Curve          | Field Size     | Security Level | JOSE alg      |
+-------------------------------------------------------------------+
| Ed25519        | 255 bits       | 128-bit        | EdDSA         |
| Ed448          | 448 bits       | 224-bit        | EdDSA         |
+-------------------------------------------------------------------+
~~~

Requirements:

1. Implementations MUST use Ed25519 or Ed448 as specified in RFC 8032 without modifications.

1. Ed25519 implementations SHOULD use the "cofactored" variant for batch verification.

1. Implementations MUST reject non-canonical signatures.

Advantages over ECDSA:

- Deterministic by design (no nonce to leak)
- Faster signing and verification
- Smaller attack surface
- Simpler implementation

EdDSA is RECOMMENDED over ECDSA for new deployments.

## Threshold Signatures

Threshold signatures require k-of-n Oracles to cooperate, preventing single-point-of-failure attacks.

### Supported Schemes

~~~
+-------------------------------------------------------------------+
| Scheme         | Base Algorithm | Level Required | Status        |
+-------------------------------------------------------------------+
| Shamir + ECDSA | ECDSA          | Level 2+       | REQUIRED      |
| FROST          | Schnorr        | Level 2+       | RECOMMENDED   |
| BLS Threshold  | BLS12-381      | Level 3        | OPTIONAL      |
+-------------------------------------------------------------------+
~~~

### Shamir-based Threshold ECDSA

Uses Shamir Secret Sharing to distribute the signing key, with secure multi-party computation for signature generation.

Protocol outline:

1. KEY GENERATION (one-time ceremony) -  Generate master signing key k -  Create n shares using Shamir (k,n)-threshold scheme -  Distribute shares to n Oracles -  Destroy master key (never reconstructed)

1. SIGNATURE GENERATION (per Trust Proof) -  k Oracles receive signing request -  Each Oracle generates partial signature using share -  Coordinator combines k partial signatures -  Result is valid ECDSA signature

Security properties:

- Any k Oracles can sign
- Fewer than k Oracles learn nothing about key
- Individual shares never leave HSMs
- Master key is never reconstructed

### FROST (Flexible Round-Optimized Schnorr Threshold)

FROST provides threshold Schnorr signatures with two-round signing protocol.

Advantages:

- Fewer rounds than threshold ECDSA
- Smaller signatures (single curve point + scalar)
- Provable security in random oracle model

FROST is RECOMMENDED for new Level 2+ deployments.

### Threshold Configuration

~~~
+-------------------------------------------------------------------+
| Level          | Minimum (k,n)  | Recommended (k,n) | Max Latency |
+-------------------------------------------------------------------+
| Level 1        | (1,1)          | (1,1)             | N/A         |
| Level 2        | (2,3)          | (3,5)             | 100ms       |
| Level 3        | (3,5)          | (5,7)             | 200ms       |
+-------------------------------------------------------------------+
~~~

The threshold k SHOULD be greater than n/2 to prevent split-brain scenarios during network partitions.

## Algorithm Negotiation

KTP supports algorithm negotiation to enable future transitions.

### Algorithm Identifier Format

Algorithm identifiers use the format:

~~~
   <scheme>-<curve_or_params>[-<variant>]
~~~

Examples: ecdsa-p256 eddsa-ed25519 frost-secp256k1 threshold-bls12-381-3of5

### Negotiation Protocol

During zone federation or Oracle mesh formation:

1. Initiator sends supported algorithms (ordered by preference)
2. Responder selects highest-preference mutual algorithm
3. Selected algorithm used for session

Message format:

~~~
   {
     "supported_algorithms": [
       "eddsa-ed448",
       "eddsa-ed25519",
       "ecdsa-p384",
       "ecdsa-p256"
     ],
     "required_minimum": "ecdsa-p256"
   }
~~~

### Algorithm Deprecation

When an algorithm is deprecated:

1. ANNOUNCE: 18-month notice before mandatory transition
2. WARN: Implementations log warnings when deprecated algorithm used
3. REJECT: Implementations reject deprecated algorithm
4. REMOVE: Algorithm removed from specification

Current deprecation schedule:

~~~
+-------------------------------------------------------------------+
| Algorithm      | Status         | Deprecation Date | Removal Date|
+-------------------------------------------------------------------+
| RSA-2048       | NOT SUPPORTED  | N/A              | N/A         |
| ECDSA P-256    | SUPPORTED      | TBD (post PQC)   | TBD         |
| SHA-1          | NOT SUPPORTED  | N/A              | N/A         |
+-------------------------------------------------------------------+
~~~

# Hash Functions

## SHA-2 Family

SHA-2 per FIPS 180-4.

~~~
+-------------------------------------------------------------------+
| Algorithm      | Output Size    | Block Size     | KTP Usage     |
+-------------------------------------------------------------------+
| SHA-256        | 256 bits       | 512 bits       | General       |
| SHA-384        | 384 bits       | 1024 bits      | High-security |
| SHA-512        | 512 bits       | 1024 bits      | Key derivation|
+-------------------------------------------------------------------+
~~~

SHA-256 is the default hash function for Level 1 and Level 2. SHA-384 is REQUIRED for Level 3.

## SHA-3 Family

SHA-3 per FIPS 202.

~~~
+-------------------------------------------------------------------+
| Algorithm      | Output Size    | Capacity       | KTP Usage     |
+-------------------------------------------------------------------+
| SHA3-256       | 256 bits       | 512 bits       | Flight Rec.   |
| SHA3-384       | 384 bits       | 768 bits       | Level 3 audit |
| SHAKE128       | Variable       | 256 bits       | KDF (general) |
| SHAKE256       | Variable       | 512 bits       | KDF (Level 3) |
+-------------------------------------------------------------------+
~~~

SHA-3 provides defense in depth against potential SHA-2 vulnerabilities. SHA3-256 is RECOMMENDED for Flight Recorder chain hashing.

## BLAKE3

BLAKE3 is a high-performance hash function suitable for bulk data hashing.

~~~
+-------------------------------------------------------------------+
| Algorithm      | Output Size    | Speed          | KTP Usage     |
+-------------------------------------------------------------------+
| BLAKE3         | Variable       | Very fast      | Trajectory    |
+-------------------------------------------------------------------+
~~~

BLAKE3 is OPTIONAL for performance-critical hashing where SHA-2/SHA-3 performance is insufficient. It MUST NOT be used for contexts requiring NIST-approved algorithms.

## Hash Function Selection

~~~
+-------------------------------------------------------------------+
| Context                    | Level 1    | Level 2    | Level 3   |
+-------------------------------------------------------------------+
| Trust Proof hashing        | SHA-256    | SHA-256    | SHA-384   |
| Flight Recorder chain      | SHA-256    | SHA3-256   | SHA3-384  |
| Trajectory chain           | SHA-256    | SHA-256    | SHA-384   |
| Key derivation             | SHA-256    | SHA-512    | SHAKE256  |
| Agent ID generation        | SHA-256    | SHA-256    | SHA-256   |
+-------------------------------------------------------------------+
~~~

# Key Derivation

## HKDF

HKDF (HMAC-based Key Derivation Function) per RFC 5869.

KTP uses HKDF for deriving keys from shared secrets:

~~~
   derived_key = HKDF-Expand(
     HKDF-Extract(salt, input_key_material),
     info,
     length
   )
~~~

Context strings (info parameter):

~~~
+-------------------------------------------------------------------+
| Purpose                    | Info String                         |
+-------------------------------------------------------------------+
| Trust Proof encryption     | "ktp-trust-proof-encrypt-v1"        |
| Trajectory chain key       | "ktp-trajectory-key-v1"             |
| Oracle session key         | "ktp-oracle-session-v1"             |
| Agent attestation key      | "ktp-agent-attestation-v1"          |
| Federation channel key     | "ktp-federation-channel-v1"         |
+-------------------------------------------------------------------+
~~~

Salt SHOULD be random and unique per derivation. If salt is not available, use the zone identifier as salt.

## Argon2

Argon2 per RFC 9106 for password-based key derivation.

Argon2id is REQUIRED when deriving keys from human-memorable secrets (e.g., recovery passphrases).

Minimum parameters:

~~~
+-------------------------------------------------------------------+
| Level          | Memory         | Iterations     | Parallelism   |
+-------------------------------------------------------------------+
| Level 1        | 64 MiB         | 3              | 4             |
| Level 2        | 256 MiB        | 4              | 4             |
| Level 3        | 1 GiB          | 6              | 8             |
+-------------------------------------------------------------------+
~~~

These parameters should be tuned to achieve approximately:

- Level 1: 0.5 second computation time
- Level 2: 1.0 second computation time
- Level 3: 3.0 second computation time

## Key Derivation Contexts

When deriving multiple keys from a single secret, each key MUST use a unique context:

~~~
   master_secret = [from key agreement or ceremony]
~~~

~~~
   encryption_key = HKDF(master_secret, salt, "encrypt", 32)
   mac_key = HKDF(master_secret, salt, "mac", 32)
   nonce_key = HKDF(master_secret, salt, "nonce", 16)
~~~

Keys derived from the same master MUST NOT be used for different algorithms (e.g., don't use same derived key for AES and ChaCha20).

# Symmetric Encryption

## AES-GCM

AES-GCM per NIST SP 800-38D.

~~~
+-------------------------------------------------------------------+
| Variant        | Key Size       | Nonce Size     | Tag Size      |
+-------------------------------------------------------------------+
| AES-128-GCM    | 128 bits       | 96 bits        | 128 bits      |
| AES-256-GCM    | 256 bits       | 96 bits        | 128 bits      |
+-------------------------------------------------------------------+
~~~

Requirements:

1. Nonces MUST be unique per key. Random nonces are acceptable for AES-256-GCM with 96-bit nonce (collision probability acceptable up to 2^32 messages per key).

1. For high-volume contexts, use counter-based nonces with unique prefix per sender.

1. Tag size MUST be 128 bits (16 bytes). Truncated tags are NOT permitted.

1. AAD (Additional Authenticated Data) SHOULD include context binding (e.g., agent ID, timestamp, purpose).

## ChaCha20-Poly1305

ChaCha20-Poly1305 per RFC 8439.

~~~
+-------------------------------------------------------------------+
| Key Size       | Nonce Size     | Tag Size       | Status        |
+-------------------------------------------------------------------+
| 256 bits       | 96 bits        | 128 bits       | RECOMMENDED   |
+-------------------------------------------------------------------+
~~~

ChaCha20-Poly1305 is RECOMMENDED as an alternative to AES-GCM:

- Better performance on systems without AES-NI
- Constant-time implementation is simpler
- No weak-key classes

Both AES-256-GCM and ChaCha20-Poly1305 MUST be supported for Level 2+.

## Encryption Contexts

~~~
+-------------------------------------------------------------------+
| Context                    | Algorithm      | Key Source         |
+-------------------------------------------------------------------+
| Trust Proof (at rest)      | AES-256-GCM    | Zone key           |
| Flight Recorder encryption | AES-256-GCM    | Audit key          |
| Agent credentials          | AES-256-GCM    | Agent master key   |
| Federation messages        | ChaCha20-Poly  | Session key        |
| Sensor data (in transit)   | TLS 1.3        | TLS handshake      |
+-------------------------------------------------------------------+
~~~

# Key Management

## Key Types

KTP defines the following key types:

### Oracle Signing Keys

Purpose: Sign Trust Proofs and trajectory attestations

Properties:

- Threshold key shares (k-of-n)
- MUST be stored in HSM for Level 2+
- Rotation: Annual or upon compromise
- Lifetime: Maximum 2 years

Format: { "key_type": "oracle_signing", "key_id": "oracle-zone-alpha-2025-001", "algorithm": "threshold-frost-ed25519-3of5", "public_key": "base64...", "created_at": "2025-01-01T00:00:00Z", "expires_at": "2027-01-01T00:00:00Z", "threshold": { "k": 3, "n": 5 }, "share_holders": \[ "oracle-alpha-1", "oracle-alpha-2", "oracle-alpha-3", "oracle-alpha-4", "oracle-alpha-5" ] }

### Agent Identity Keys

Purpose: Prove agent identity, sign trajectory records

Properties:

- Single-holder key (not threshold)
- May be software or HSM protected
- Rotation: Upon role change or compromise
- Lifetime: Tied to agent lifecycle

Format: { "key_type": "agent_identity", "key_id": "agent-7gen-optimized-a1b2c3d4", "algorithm": "eddsa-ed25519", "public_key": "base64...", "created_at": "2025-06-15T10:30:00Z", "expires_at": null, "lineage": "guarantor", "generation": 7 }

### Zone Encryption Keys

Purpose: Encrypt data at rest within a zone

Properties:

- Symmetric key (AES-256)
- Protected by Oracle key (envelope encryption)
- Rotation: Quarterly
- Lifetime: Maximum 1 year

### Federation Keys

Purpose: Secure communication between zones

Properties:

- Key agreement (ECDH) + symmetric session keys
- Tied to federation agreement
- Rotation: Per session or hourly (whichever is shorter)
- Lifetime: Session-scoped

### Root of Trust Keys

Purpose: Anchor the entire key hierarchy

Properties:

- Highest-security key in the system
- MUST be stored in FIPS 140-2 Level 3+ HSM
- Created in formal key ceremony with witnesses
- Rotation: Rare (5+ years) or upon compromise
- Used only to sign subordinate keys

## Key Generation

### Randomness Requirements

All key generation MUST use cryptographically secure random number generators (CSPRNGs):

- Operating system: /dev/urandom (Linux), CryptGenRandom (Windows)
- HSM: Hardware random number generator
- Cloud: Cloud provider HSM RNG

Implementations MUST NOT use:

- Predictable seeds
- Low-entropy sources
- User-provided randomness without mixing

### Key Generation Procedures

Level 1 (Software):

~~~
   1. Generate 256 bits from CSPRNG
   2. Use as private key directly (Ed25519) or derive (ECDSA)
   3. Store encrypted in keystore
   4. Log generation event (without key material)
~~~

Level 2+ (HSM):

~~~
   1. Initiate key generation on HSM
   2. HSM generates key internally using hardware RNG
   3. Private key never leaves HSM
   4. Export public key for distribution
   5. Log generation event with HSM attestation
~~~

Level 3 (Ceremony):

~~~
   1. Convene key ceremony with required participants
   2. Each participant provides entropy contribution
   3. HSM mixes entropy and generates key
   4. Key shares distributed to separate HSMs
   5. Ceremony recorded and witnessed
   6. Ceremony artifacts archived
~~~

## Key Storage

### Storage Requirements by Level

~~~
+-------------------------------------------------------------------+
| Level | Oracle Keys      | Agent Keys       | Audit Keys         |
+-------------------------------------------------------------------+
| 1     | Encrypted file   | Encrypted file   | Encrypted file     |
| 2     | HSM (FIPS 140-2) | Encrypted file   | HSM or encrypted   |
| 3     | HSM Level 3      | HSM recommended  | HSM Level 3        |
+-------------------------------------------------------------------+
~~~

### Software Key Storage

For software-protected keys:

1. Encrypt with AES-256-GCM using key derived from: -  System entropy (hardware IDs, boot time, etc.) -  Optional: Human passphrase (Argon2-stretched)

1. Store in protected location: -  Linux: /var/lib/ktp/keys with mode 0600 -  HSM-backed keystore if available

1. Implement memory protection: -  mlock() to prevent swapping -  Secure memory wiping after use

### HSM Key Storage

For HSM-protected keys:

1. Generate keys on HSM (never import)
2. Keys are non-extractable
3. Access controlled by HSM authentication
4. Backup via HSM-to-HSM key transfer (if supported)

## Key Rotation

### Rotation Schedule

~~~
+-------------------------------------------------------------------+
| Key Type            | Normal Rotation  | Emergency Rotation       |
+-------------------------------------------------------------------+
| Root of Trust       | 5 years          | Immediate upon compromise|
| Oracle Signing      | 1 year           | 24 hours upon compromise |
| Zone Encryption     | 90 days          | Immediate upon compromise|
| Federation Session  | 1 hour           | Immediate upon compromise|
| Agent Identity      | Role change      | Immediate upon compromise|
+-------------------------------------------------------------------+
~~~

### Rotation Procedure

For Oracle signing keys:

1. PREPARE (1 week before expiry) -  Generate new key shares on HSMs -  Distribute shares to Oracle nodes -  Verify all nodes have new shares

1. OVERLAP (during transition window) -  Old key still valid for verification -  New key used for new signatures -  Both keys published in key directory

1. COMMIT (after transition window) -  Old key marked as expired -  Old key retained for historical verification -  New key is sole signing key

1. ARCHIVE (after retention period) -  Old key material securely destroyed -  Public key retained indefinitely for audit

### Key Overlap Period

~~~
+-------------------------------------------------------------------+
| Key Type            | Overlap Period   | Grace Period             |
+-------------------------------------------------------------------+
| Oracle Signing      | 7 days           | 30 days                  |
| Zone Encryption     | 24 hours         | 7 days                   |
| Federation          | 5 minutes        | 1 hour                   |
+-------------------------------------------------------------------+
~~~

During overlap period, both old and new keys are valid. During grace period, old key valid for verification only.

## Key Revocation

### Revocation Triggers

Keys MUST be revoked when:

1. Compromise confirmed or suspected
2. Key holder leaves organization
3. Key holder role changes (if role-bound)
4. Cryptographic weakness discovered in algorithm
5. HSM containing key is decommissioned

### Revocation Procedure

1. IMMEDIATE (within minutes) -  Add key to revocation list -  Broadcast revocation to all zones -  Log revocation with reason

1. PROPAGATION (within hours) -  All Trust Oracles update revocation lists -  All PEPs refresh revocation cache -  All agents receive revocation notice

1. ENFORCEMENT -  Signatures by revoked key rejected -  Trust Proofs signed by revoked key invalidated -  Agents authenticated by revoked key demoted

### Revocation List Format

~~~
   {
     "version": 1,
     "zone_id": "zone-alpha",
     "issued_at": "2025-11-25T12:00:00Z",
     "next_update": "2025-11-25T13:00:00Z",
     "revoked_keys": [
       {
         "key_id": "oracle-zone-alpha-2024-001",
         "revoked_at": "2025-11-25T11:30:00Z",
         "reason": "key_compromise",
         "replacement_key_id": "oracle-zone-alpha-2025-002"
       }
     ],
     "signature": "..."
   }
~~~

## Key Escrow and Recovery

### Escrow Policy

KTP does NOT mandate key escrow for agent keys. Agents that lose their keys lose their trajectory history.

KTP DOES require recovery capability for Oracle keys to prevent zone- wide lockout.

### Oracle Key Recovery

Threshold keys provide inherent recovery: any k-of-n shares can reconstruct signing capability.

For disaster recovery (loss of k+ shares):

1. COLD BACKUP -  Encrypted backup of key shares stored offline -  Backup encrypted to recovery keys held by trustees -  M-of-N trustees required to recover

1. RECOVERY CEREMONY -  Convene required trustees -  Decrypt backup shares -  Install on new HSMs -  Verify signing capability -  Destroy backup shares used

Recovery keys SHOULD be geographically distributed and held by different organizational roles.

# Hardware Security Modules

## HSM Requirements

### Certification Requirements

~~~
+-------------------------------------------------------------------+
| Level          | Minimum Certification                            |
+-------------------------------------------------------------------+
| Level 1        | None (HSM optional)                              |
| Level 2        | FIPS 140-2 Level 2                               |
| Level 3        | FIPS 140-2 Level 3 or Common Criteria EAL4+      |
+-------------------------------------------------------------------+
~~~

### Functional Requirements

HSMs used for KTP MUST support:

- Key generation using hardware RNG
- ECDSA signing with P-256, P-384 (P-521 recommended)
- EdDSA signing with Ed25519 (Ed448 recommended)
- AES-256-GCM encryption/decryption
- Non-extractable key storage
- Access control (authentication required for operations)
- Audit logging

HSMs used for Level 3 MUST additionally support:

- Multi-person access control (M-of-N authentication)
- Remote attestation
- Tamper response (key zeroization)
- Secure key backup/restore

## PKCS#11 Integration

HSM integration SHOULD use PKCS#11 for portability.

Required PKCS#11 mechanisms:

~~~
+-------------------------------------------------------------------+
| Mechanism              | Use Case                                 |
+-------------------------------------------------------------------+
| CKM_EC_KEY_PAIR_GEN    | ECDSA key generation                     |
| CKM_ECDSA_SHA256       | ECDSA signing (P-256)                    |
| CKM_ECDSA_SHA384       | ECDSA signing (P-384)                    |
| CKM_AES_GCM            | Symmetric encryption                     |
| CKM_SHA256             | Hashing                                  |
| CKM_SHA384             | Hashing                                  |
+-------------------------------------------------------------------+
~~~

For EdDSA, use vendor-specific mechanisms or CKM_EDDSA if supported (PKCS#11 3.0+).

## Cloud HSM Considerations

Cloud HSMs (AWS CloudHSM, Azure Dedicated HSM, GCP Cloud HSM) are acceptable for Level 2 deployments.

Considerations:

1. TRUST: You are trusting the cloud provider's HSM implementation
2. AVAILABILITY: Cloud HSM availability tied to region availability
3. KEY BACKUP: Understand cloud provider's backup mechanisms
4. MULTI-REGION: Consider cross-region HSM clusters for resilience

For Level 3, dedicated (non-cloud) HSMs are RECOMMENDED due to the Hypervisor Opaque Wall concern (see KTP-PROBLEMS).

# Credential Formats

## Trust Proof Format

Trust Proofs use JWS (JSON Web Signature) format per RFC 7515.

Header: { "alg": "ES256", "typ": "ktp-trust-proof+jwt", "kid": "oracle-zone-alpha-2025-001", "ktp_level": 2, "threshold": "3of5" }

Payload: { "iss": "zone:alpha", "sub": "agent:guarantor:7gen:optimized:a1b2c3d4", "aud": "zone:alpha", "iat": 1700000000, "exp": 1700000010, "nbf": 1700000000, "jti": "proof-uuid-12345",

~~~
     "e_base": 87,
     "e_trust": 74,
     "risk_factor": 0.15,
     "tier": "operator",
~~~

~~~
     "context": {
       "m": 0.12,
       "p": 0.08,
       "h": 0.22,
       "t": 0.05,
       "i": 0.18,
       "o": 0.10,
       "s": 0
     },
~~~

~~~
     "lineage": {
       "type": "guarantor",
       "generation": 7,
       "trajectory_hash": "sha256:abc123..."
     }
   }
~~~

Signature:

- For single-Oracle: Standard JWS signature
- For threshold: Aggregated threshold signature

## Agent Credential Format

Agent credentials establish identity binding.

~~~
   {
     "credential_type": "ktp-agent-credential",
     "version": 1,
     "agent_id": "agent:guarantor:7gen:optimized:a1b2c3d4",
~~~

~~~
     "identity": {
       "public_key": "base64...",
       "algorithm": "eddsa-ed25519",
       "key_id": "agent-key-12345"
     },
~~~

~~~
     "proofing": {
       "ial": 2,
       "proofed_at": "2025-01-15T10:00:00Z",
       "provider": "isp:acme-verify"
     },
~~~

~~~
     "lineage": {
       "type": "guarantor",
       "generation": 7,
       "sponsor_chain": ["org:acme", "agent:acme-deploy"]
     },
~~~

~~~
     "issued_at": "2025-01-15T10:00:00Z",
     "expires_at": "2026-01-15T10:00:00Z",
~~~

~~~
     "issuer": {
       "zone_id": "zone:alpha",
       "oracle_key_id": "oracle-zone-alpha-2025-001"
     },
~~~

~~~
     "signature": "base64..."
   }
~~~

## Oracle Credential Format

Oracle credentials establish Oracle authority within a zone.

~~~
   {
     "credential_type": "ktp-oracle-credential",
     "version": 1,
     "oracle_id": "oracle-alpha-1",
~~~

~~~
     "zone": {
       "zone_id": "zone:alpha",
       "zone_type": "blue",
       "zone_public_key": "base64..."
     },
~~~

~~~
     "signing_capability": {
       "key_id": "oracle-zone-alpha-2025-001",
       "algorithm": "threshold-frost-ed25519",
       "share_index": 1,
       "threshold": {
         "k": 3,
         "n": 5
       }
     },
~~~

~~~
     "attestation": {
       "hsm_attestation": "base64...",
       "platform_attestation": "base64..."
     },
~~~

~~~
     "issued_at": "2025-01-01T00:00:00Z",
     "expires_at": "2027-01-01T00:00:00Z",
~~~

~~~
     "issuer": {
       "root_key_id": "root-nmcitra-2024-001"
     },
~~~

~~~
     "signature": "base64..."
   }
~~~

## Federation Credential Format

Federation credentials establish inter-zone trust.

~~~
   {
     "credential_type": "ktp-federation-credential",
     "version": 1,
~~~

~~~
     "local_zone": {
       "zone_id": "zone:alpha",
       "oracle_key_id": "oracle-zone-alpha-2025-001"
     },
~~~

~~~
     "remote_zone": {
       "zone_id": "zone:beta",
       "oracle_key_id": "oracle-zone-beta-2025-001"
     },
~~~

~~~
     "trust_parameters": {
       "trust_factor": 0.85,
       "max_transitive_trust": 0.7,
       "allowed_operations": ["attest", "query", "federate"],
       "disallowed_operations": ["admin"]
     },
~~~

~~~
     "agreement": {
       "agreed_at": "2025-06-01T00:00:00Z",
       "expires_at": "2026-06-01T00:00:00Z",
       "renewal": "automatic"
     },
~~~

~~~
     "signatures": {
       "alpha_signature": "base64...",
       "beta_signature": "base64..."
     }
   }
~~~

# Post-Quantum Cryptography

## Threat Timeline

Current assessment of quantum computing threat:

~~~
+-------------------------------------------------------------------+
| Timeline       | Threat Level   | Recommended Action              |
+-------------------------------------------------------------------+
| 2025-2030      | Low            | Plan transition, implement      |
|                |                | hybrid                          |
| 2030-2035      | Medium         | Deploy hybrid mandatory         |
| 2035+          | High           | Full PQC transition             |
+-------------------------------------------------------------------+
~~~

"Harvest now, decrypt later" attacks make earlier action prudent for data that must remain confidential for 10+ years.

KTP Trust Proofs have short lifetimes (seconds), so the threat is primarily to Flight Recorder data and trajectory histories.

## Hybrid Signatures

Hybrid signatures combine classical and post-quantum algorithms.

Hybrid format:

~~~
   hybrid_signature = classical_signature || pqc_signature
~~~

Both signatures must verify for the hybrid to be valid. This provides security as long as EITHER algorithm remains secure.

Recommended hybrid pairs:

~~~
+-------------------------------------------------------------------+
| Classical      | PQC                | Combined Size | Level      |
+-------------------------------------------------------------------+
| Ed25519        | Dilithium2         | ~2500 bytes   | 2          |
| Ed448          | Dilithium3         | ~3600 bytes   | 3          |
| ECDSA P-384    | Dilithium3         | ~3700 bytes   | 3          |
+-------------------------------------------------------------------+
~~~

## PQC Algorithm Selection

Based on NIST PQC standardization:

~~~
Signatures:
+-------------------------------------------------------------------+
| Algorithm      | Type           | Security Level | Status        |
+-------------------------------------------------------------------+
| ML-DSA-44      | Lattice        | NIST 2         | RECOMMENDED   |
| ML-DSA-65      | Lattice        | NIST 3         | RECOMMENDED   |
| ML-DSA-87      | Lattice        | NIST 5         | OPTIONAL      |
| SLH-DSA        | Hash-based     | NIST 1-5       | OPTIONAL      |
+-------------------------------------------------------------------+
~~~

(ML-DSA is the standardized name for Dilithium)

~~~
Key Encapsulation (for future key agreement):
+-------------------------------------------------------------------+
| Algorithm      | Type           | Security Level | Status        |
+-------------------------------------------------------------------+
| ML-KEM-768     | Lattice        | NIST 3         | RECOMMENDED   |
| ML-KEM-1024    | Lattice        | NIST 5         | OPTIONAL      |
+-------------------------------------------------------------------+
~~~

(ML-KEM is the standardized name for Kyber)

## Migration Strategy

Phase 1 (Now - 2027): PREPARATION

- Implement hybrid signature support
- Enable hybrid as OPTIONAL
- Inventory systems requiring long-term confidentiality

Phase 2 (2027-2030): HYBRID DEPLOYMENT

- Hybrid signatures RECOMMENDED for Level 2+
- Hybrid signatures REQUIRED for Level 3
- Classical-only still accepted for Level 1

Phase 3 (2030-2035): TRANSITION

- Hybrid signatures REQUIRED for Level 2+
- Classical-only deprecated
- Begin accepting PQC-only signatures

Phase 4 (2035+): COMPLETION

- PQC-only REQUIRED for Level 3
- Classical algorithms removed from specification
- Hybrid accepted for backward compatibility

# Random Number Generation

Secure random number generation is critical for all cryptographic operations.

## Requirements

All random values MUST be generated by a CSPRNG that:

1. Is seeded from high-entropy sources (hardware RNG, OS entropy)
2. Has been validated (NIST SP 800-90A compliance recommended)
3. Provides at least 256 bits of security
4. Is reseeded periodically

## Entropy Sources

Acceptable entropy sources:

- Hardware RNG (Intel RDRAND/RDSEED, ARM TRNG)
- Operating system entropy pool (/dev/urandom, CryptGenRandom)
- HSM hardware RNG
- Environmental noise (with appropriate mixing)

NOT acceptable as sole source:

- Timestamps
- Process IDs
- User input
- Network data

## Testing

Implementations SHOULD perform entropy health checks:

- NIST SP 800-90B health tests
- Continuous random number generator testing
- Startup self-tests

# Security Considerations

## Algorithm Downgrade Attacks

Attackers may attempt to force use of weaker algorithms.

Mitigations:

- Require minimum algorithm strength per level
- Sign algorithm negotiation messages
- Alert on unexpected algorithm changes

## Side-Channel Attacks

Cryptographic implementations may leak information through:

- Timing variations
- Power analysis
- Electromagnetic emissions
- Cache behavior

Mitigations:

- Use constant-time implementations
- Use HSMs for high-value keys
- Validate implementations against known test vectors

## Key Compromise

If a key is compromised:

- Oracle signing key: Revoke immediately, rotate threshold
- Agent key: Revoke agent, invalidate trajectory
- Zone encryption key: Re-encrypt data, rotate key
- Root key: Major incident, full ceremony required

## Implementation Vulnerabilities

Common vulnerabilities to avoid:

- Nonce reuse in AES-GCM (catastrophic)
- Weak random number generation
- Improper signature verification (accepting malformed)
- Memory leaks of key material
- Timing leaks in comparison operations

Implementations SHOULD use well-tested cryptographic libraries:

- OpenSSL / BoringSSL
- libsodium
- AWS-LC
- Hardware vendor libraries for HSM

# IANA Considerations

## Algorithm Registry

This document requests establishment of a KTP Algorithm Registry with the following initial entries:

~~~
+-------------------------------------------------------------------+
| ID     | Name                    | Type       | Reference         |
+-------------------------------------------------------------------+
| 0x0001 | ecdsa-p256              | Signature  | Section 4.1       |
| 0x0002 | ecdsa-p384              | Signature  | Section 4.1       |
| 0x0003 | ecdsa-p521              | Signature  | Section 4.1       |
| 0x0010 | eddsa-ed25519           | Signature  | Section 4.2       |
| 0x0011 | eddsa-ed448             | Signature  | Section 4.2       |
| 0x0020 | threshold-frost-ed25519 | Threshold  | Section 4.3       |
| 0x0030 | hybrid-ed25519-mldsa44  | Hybrid     | Section 11.2      |
| 0x0100 | sha256                  | Hash       | Section 5.1       |
| 0x0101 | sha384                  | Hash       | Section 5.1       |
| 0x0110 | sha3-256                | Hash       | Section 5.2       |
| 0x0200 | aes-256-gcm             | AEAD       | Section 7.1       |
| 0x0201 | chacha20-poly1305       | AEAD       | Section 7.2       |
+-------------------------------------------------------------------+
~~~

--- back

# Algorithm Identifiers

Complete list of algorithm identifiers for use in KTP messages:

Signature Algorithms: ecdsa-p256 ecdsa-p384 ecdsa-p521 eddsa-ed25519 eddsa-ed448 threshold-shamir-ecdsa-p256-KofN threshold-shamir-ecdsa-p384-KofN threshold-frost-ed25519-KofN threshold-frost-ed448-KofN threshold-bls12-381-KofN hybrid-ed25519-mldsa44 hybrid-ed448-mldsa65 hybrid-ecdsa-p384-mldsa65

Hash Algorithms: sha256 sha384 sha512 sha3-256 sha3-384 sha3-512 shake128 shake256 blake3

AEAD Algorithms: aes-128-gcm aes-256-gcm chacha20-poly1305

KDF Algorithms: hkdf-sha256 hkdf-sha384 hkdf-sha512 argon2id

# Test Vectors

B.1.  Ed25519 Signature

Private Key (hex): 9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60

Public Key (hex): d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a

Message: (empty)

Signature (hex): e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155 5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b

B.2.  SHA-256 Hash

Message: "abc"

Hash (hex): ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad

B.3.  AES-256-GCM Encryption

Key (hex): feffe9928665731c6d6a8f9467308308feffe9928665731c6d6a8f9467308308

IV (hex): cafebabefacedbaddecaf888

Plaintext (hex): d9313225f88406e5a55909c5aff5269a

AAD (hex): feedfacedeadbeeffeedfacedeadbeef

Ciphertext (hex): 522dc1f099567d07f47f37a32a84427d

Tag (hex): 9fc0ef3636c83f6abbe3d6a6eb0e5bba
