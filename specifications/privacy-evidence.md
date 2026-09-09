# Purpose-limited evidence, correction, and erasure

Status: normative, unreleased F11 contract, 2026-09-07. Applies to personal data
in human and software-agent records, including copied and derived evidence.

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT,
RECOMMENDED, NOT RECOMMENDED, MAY, and OPTIONAL are to be interpreted as described
in BCP 14 (RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

## 1. Declared information flows

Before collection, a deployment MUST have an approved, authenticated, versioned
data policy defining each purpose, source, subject category, authority and its
governing instrument, permitted processing, recipients, access controls,
retention trigger and bounded deadline, correction propagation, erasure process,
and responsible owner. The policy MUST include review/escalation deadlines and
any justified hold's authority, scope, access limits, end date, and review date.
Names such as "audit" or "compliance" alone do not discharge these declarations.
The evidence envelope binds the canonical policy's digest; the human profile's
retention-policy ID MUST resolve to that approved versioned policy. A deployment
MUST reject an unresolved or unauthorized declaration for dependent processing.

The policy MUST distinguish environmental measurement, specifically authorized
local content analysis, human qualification/review evidence, and minimized
exports. Permission for one does not authorize another. Sensors MUST NOT gain
general access to communications or personal behavior. Local content analysis
requires its own specific purpose, source, authority, and recipient limits.
Security evidence MUST NOT be reused for HR performance ranking, personality,
emotion, or loyalty inference. Collective data authority and individual rights
must each be established where applicable. Labeling a zone opt-in is insufficient.

Opaque identifiers, timestamps, resource references, evidence digests, and
aggregates MAY remain personal data through linkage. Deployments MUST assess
and limit that linkage; metadata is not automatically anonymous. Public anchors
SHOULD contain only suitably protected aggregate commitments. Hashing a name or
another low-entropy personal value is not sufficient protection.

## 2. New encrypted storage envelope

[privacy-evidence-envelope.json](../schemas/privacy-evidence-envelope.json)
defines `ktp-privacy-evidence-v1`, a new **storage** format. It does not replace
trajectory-v3, its signatures, consensus evidence, or the ordinary proof format.
Each envelope contains minimal contextual metadata, a separately encrypted
evidence payload, a signature over the complete envelope body, and a final hash
covering the signature. The metadata remains subject to its own retention and
access obligations and can itself require deletion.

The payload is nonempty exact evidence bytes. These may be the exact original
signed record, or a separately versioned evidence bundle whose format is
identified inside the encryption. Existing signed bytes MUST NOT be normalized,
redacted, or re-signed to imply that the original author signed revised content.
An inner record's own format, signatures, and authenticated head MUST be checked
independently before its claims are used. Encryption and a new archive signature
do not validate those claims or upgrade a legacy trajectory to v3.

The envelope's closed header contains: format, opaque envelope and chain IDs,
zone, sequence, predecessor hash, conformance level, purpose ID, approved data
policy digest, creation time, bounded deletion deadline, and issuer ID. It
contains no plaintext subject name, qualification, score, original content hash,
or free-form personal details. A chain ID or key reference still may be linkable.
Subject and retention partitioning MUST prevent one person's erasure request
from being falsely satisfied while another key still reveals their information.

The exact cryptographic construction is:

1. Generate a fresh 256-bit data-encryption key for each envelope, a fresh
   96-bit nonce, and an opaque key reference. Wrap/store the key through the
   deployment's approved key-management system, separate from the envelope.
2. Form the associated-data object from all envelope body fields except
   `encryption.ciphertext`. The body excludes only `signature` and `record_hash`.
   Encode the associated data using RFC 8785 JCS, including the format, purpose,
   policy, chain, nonce, algorithm (`A256GCM`), and key reference.
3. AES-256-GCM encrypts the exact payload bytes with that associated data.
   `ciphertext` is unpadded canonical base64url of ciphertext followed by its
   complete 128-bit authentication tag. The nonce is canonical base64url too.
4. Sign the complete body, including ciphertext, as compact JWS with protected
   `typ = ktp-privacy-evidence-v1`, `alg`, and `kid`. Use the strict canonical,
   key-binding, role, encoding, and low-s rules of
   [trajectory-signatures.md](trajectory-signatures.md). This additional role
   MUST NOT be accepted as a trajectory, readiness, or authorization role.
5. `record_hash` is the digest of the JCS completed envelope excluding only
   its own `record_hash` field. Levels 1/2 use SHA-256; Level 3 uses SHA-384,
   including predecessor and policy digests. The signed conformance level MUST
   equal the independently trusted level.

Sequence 1 has a null predecessor; every later sequence has the independently
anchored predecessor's complete hash. Times and sequence are safe integer tokens;
creation precedes deletion deadline. Verifiers MUST obtain expected chain,
position, predecessor, completed hash, purpose, policy, issuer and valid signing
key from authenticated archive state. Candidate metadata cannot provide those
expectations. The issuer must have been authorized at creation; historical
verification does not make an old record current authority. Existing consensus,
anchoring, crypto-strength and threshold/hybrid requirements remain applicable.

## 3. Corrections and permitted views

A correction is a new authenticated event. It MUST identify the superseded
evidence/version, correction authority, reason, and replacement state inside
the protected payload. It MUST update active evidence and invalidate dependent
decisions under [human-eligibility.md](human-eligibility.md). The archive MUST
distinguish an authentic past assertion from currently valid evidence.

A redacted view MAY be generated for an authorized recipient, but it is a new
derivative with its own purpose, retention, and integrity description. If signed,
its signature attests to the derivative, not the original author's endorsement.
It MUST NOT be substituted into the old signed chain. A shared record that
cannot be erased for one person without affecting others requires subject
partitioning, an authorized new derivative, or a disclosed retained exception;
destroying one of several usable keys is insufficient.

## 4. Erasure and retention accounting

Erasure MUST account for the full authorized subject/data scope through a
declared cutoff: primary copies, replicas, backups, caches, extracts, derived
records, recipient copies, every usable data-key copy and wrapping/recovery
path, and shared-subject records. An independently authenticated inventory
MUST bind the exact scope, version, objects, key relationships and recipients.
Concurrent processing MUST be fenced or included through a later inventory;
a snapshot must not allow an ongoing copy to escape the result.

The [erasure receipt schema](../schemas/privacy-erasure-receipt.json) defines
an unsigned accounting body. A deployment MUST authenticate the complete
receipt and verify its inventory and disposal evidence before relying on it.
Its `complete` status means the declared scope and cutoff were fully accounted
for and every covered copy was verifiably erased. It MUST NOT imply global
erasure beyond that inventory, a particular legal outcome, or destruction of
uncontrolled public copies. Discovery of an omitted copy requires reopening
the disposition and corrective action.

`pending` means no covered copy yet has verified erasure or an approved
retention disposition. `partial` includes approved retained exceptions even
before any erasure succeeds, and identifies unfinished copies or incomplete
inventories after verified progress. Missing recipient acknowledgements cannot
count as completed disposal. A claimed deletion, a key
name disappearing from a directory, a rotated wrapping key, or a notice sent to
a federation partner is not verified erasure. The reference binds each copy verification to the digest of exactly
`{copy_id, disposition, verification_digest}`; a crypto-erasure claim MUST NOT
be relabeled physical deletion to skip key-destruction checks.
Required destruction and recipient
acknowledgements MUST be independently bound to the actual copy/key and request.

Every retained exception MUST declare authority, precise purpose, restricted
access policy, deletion deadline, and scheduled review in its authorizing
instrument. Retained exceptions MUST remain visible; they cannot count as
erased even when justified. Passing a deadline does not transform an undeleted
copy into a deleted one. Restore procedures MUST apply erasure/correction
dispositions before restored evidence can be read or used. Archiving or copying
MUST NOT restart a retention clock. No universal seven-year or permanent
personal-data retention rule is imposed by KTP conformance level.

Revocation, accepted-format floors, and correction state MUST NOT be cleared by
erasure or identity changes. Any retained anti-rollback marker must have its own
declared purpose, access limits, authority and deadline; it may be personal data.
If required safety state cannot be retained or reconstructed under applicable
rules, old authority MUST remain unusable. Any new enrollment requires separate
authorization, not an automatic clean slate.

## 5. What verification means after erasure

While ciphertext and its minimal envelope are legitimately retained, the
outer signature and chain anchor can remain verifiable after the data key is
destroyed. A verifier MUST report **outer integrity only** when it cannot recover
and independently verify the payload. It MUST NOT report the original evidence
as reviewed, its signatures as replayed, or complete forensic reconstruction.
Destroying the key means those operations can become impossible by design.

Where the envelope itself must be deleted, continuity beyond the retained
authenticated checkpoints may also be unavailable. An authorized disposition
can explain the gap; it cannot recreate the missing signature verification.
Retention and erasure limits MUST be declared when evidence is first accepted
for an audit or conformance claim. Erased evidence cannot continue to support
an operation requiring it to be independently verified.

F08's preservation of admissible historical achievement prevents time alone
from subtracting standing. It does not mandate indefinite personal-data
retention or permit use of unavailable, corrected, or unverified evidence.
Retention while evidence is held, its integrity, current authority, and lawful
disposition are distinct requirements.

## 6. Legacy records and executable limits

Before migration, inventory existing plaintext signed records and their copies,
restrict access, identify justified retention and required erasure, and approve
the disposition. Wrapping exact legacy bytes protects the new copy; it does not
remove original plaintext from old storage, backups, exports or public replicas.
Each old copy requires separate disposition evidence. Archived published schemas
and retained record bytes MUST NOT be rewritten to disguise that limitation.

`scripts/privacy_evidence.py` implements real AES-GCM, complete-body JWS, and
completed-envelope hash checks with externally supplied archive/key expectations.
It generates a new data key on each seal, returns it to the caller, and performs
no production key wrapping, secure memory zeroization, retention scheduler,
discovery, authorization, or deletion. The reference decryptor refuses use at
or after `delete_after`; a justified extension requires separately authorized
retention and new authenticated records, not editing the old signed deadline.

`scripts/human_eligibility.py` checks receipt semantics using a supplied trusted
inventory and disposal evidence. Neither helper authenticates the discovery or
destruction process. A complete reference receipt is not a hardware or legal
certificate. Tests and runtime obligations are separated in
[human-privacy-lifecycle-v1.json](conformance/human-privacy-lifecycle-v1.json).
