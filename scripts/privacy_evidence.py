#!/usr/bin/env python3
"""Authenticated encrypted evidence reference; not a key store or authorizer.

Each seal generates a fresh data key and nonce. Callers must persist keys and
anchors safely, authorize decryption, enforce retention, and implement erasure.
Verifying an outer envelope says nothing about the truth of its inner evidence.
"""
import json
import secrets
from dataclasses import dataclass
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from jsonschema import Draft202012Validator

from trajectory_signatures import (
    InvalidRecord, PRIVACY_EVIDENCE_TYPE, b64, canonical, digest,
    sign_jws, unb64, verify_jws,
)

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / 'schemas/privacy-evidence-envelope.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
FORMAT = 'ktp-privacy-evidence-v1'


def body(envelope):
    return {k: v for k, v in envelope.items() if k not in ('signature', 'record_hash')}


def associated_data(envelope):
    header = {k: v for k, v in body(envelope).items() if k != 'encryption'}
    header['encryption'] = {k: v for k, v in envelope['encryption'].items()
                            if k != 'ciphertext'}
    return canonical(header)


def record_digest(envelope, level):
    return digest({k: v for k, v in envelope.items() if k != 'record_hash'}, level)


def validate_envelope(envelope):
    canonical(envelope)
    errors = list(VALIDATOR.iter_errors(envelope))
    if errors:
        raise InvalidRecord('privacy envelope schema: ' + errors[0].message)
    for name in ('sequence', 'conformance_level', 'created_at', 'delete_after'):
        if type(envelope[name]) is not int:
            raise InvalidRecord(name + ' must be an integer token')
    if envelope['created_at'] >= envelope['delete_after']:
        raise InvalidRecord('retention deadline must follow creation')
    if (envelope['sequence'] == 1) != (envelope['previous_hash'] is None):
        raise InvalidRecord('only genesis may have no predecessor')
    prefix = 'sha384:' if envelope['conformance_level'] == 3 else 'sha256:'
    for name in ('privacy_policy_digest', 'record_hash', 'previous_hash'):
        value = envelope[name]
        if value is not None and not value.startswith(prefix):
            raise InvalidRecord('digest strength differs from profile')
    if len(unb64(envelope['encryption']['nonce'])) != 12:
        raise InvalidRecord('AES-GCM nonce must have 96 bits')
    if len(unb64(envelope['encryption']['ciphertext'])) <= 16:
        raise InvalidRecord('ciphertext must include nonempty evidence and tag')


@dataclass(frozen=True)
class ExpectedEnvelope:
    """Independently authenticated archive anchor and installed policy context.

    Construction is not authentication. Policy validity and lawful retention
    must be established outside this helper, including justified holds.
    """
    zone_id: str
    chain_id: str
    sequence: int
    previous_hash: object
    record_hash: str
    purpose_id: str
    privacy_policy_digest: str
    issuer_id: str
    level: int
    key_valid_from: int
    key_valid_until: int


def seal_evidence(plaintext, metadata, private_key, *, key_id, algorithm, level):
    """Return a new envelope and raw data key; never rewrites the plaintext.

    The caller must not log the returned data key. This reference does not
    perform production key wrapping, secure memory zeroization, or erasure.
    """
    if type(plaintext) is not bytes or not plaintext:
        raise InvalidRecord('nonempty exact evidence bytes required')
    if type(metadata) is not dict or set(metadata) != {
        'envelope_id', 'zone_id', 'chain_id', 'sequence', 'previous_hash',
        'purpose_id', 'privacy_policy_digest', 'created_at', 'delete_after', 'issuer_id',
    }:
        raise InvalidRecord('exact privacy metadata fields required')
    envelope = dict(metadata, format=FORMAT, conformance_level=level,
                    encryption={'algorithm': 'A256GCM', 'key_ref': b64(secrets.token_bytes(24)),
                                'nonce': b64(secrets.token_bytes(12)), 'ciphertext': b64(bytes(17))},
                    signature='e30.e30.AA', record_hash=digest({}, level))
    validate_envelope(envelope)
    data_key = AESGCM.generate_key(bit_length=256)
    envelope['encryption']['ciphertext'] = b64(AESGCM(data_key).encrypt(
        unb64(envelope['encryption']['nonce']), plaintext, associated_data(envelope)))
    envelope['signature'] = sign_jws(body(envelope), private_key, key_id=key_id,
        algorithm=algorithm, purpose=PRIVACY_EVIDENCE_TYPE, level=level)
    envelope['record_hash'] = record_digest(envelope, level)
    validate_envelope(envelope)
    return envelope, data_key


def verify_envelope(envelope, binding, expected, *, now):
    """Verify outer integrity and archive anchor without needing a data key.

    A valid result is deliberately 'outer_integrity_only'; neither decryption,
    original signatures, erasure, authority nor chain consensus is established.
    Historical verification may occur after deletion deadline; retaining the
    object beyond that deadline requires separate authority, never this result.
    """
    validate_envelope(envelope)
    for value in (now, expected.level, expected.sequence, expected.key_valid_from,
                  expected.key_valid_until):
        if type(value) is not int or value < 0 or value > 2**53 - 1:
            raise InvalidRecord('invalid trusted integer')
    for name in ('zone_id', 'chain_id', 'sequence', 'previous_hash', 'record_hash',
                 'purpose_id', 'privacy_policy_digest', 'issuer_id'):
        if envelope[name] != getattr(expected, name):
            raise InvalidRecord('envelope differs from independently anchored ' + name)
    if envelope['conformance_level'] != expected.level:
        raise InvalidRecord('trusted level mismatch')
    if (binding.purpose != PRIVACY_EVIDENCE_TYPE or binding.subject != expected.issuer_id
            or binding.zone_id != expected.zone_id):
        raise InvalidRecord('privacy evidence key role, issuer or zone mismatch')
    if not expected.key_valid_from <= envelope['created_at'] < expected.key_valid_until:
        raise InvalidRecord('signer not valid at envelope creation')
    if envelope['created_at'] > now:
        raise InvalidRecord('future envelope')
    verify_jws(envelope['signature'], body(envelope), binding, level=expected.level)
    if record_digest(envelope, expected.level) != expected.record_hash:
        raise InvalidRecord('completed envelope digest mismatch')
    return 'outer_integrity_only'


def open_evidence(envelope, data_key, binding, expected, *, now):
    """Verify the envelope then decrypt; caller must separately authorize access.

    Exact recovered bytes still require their original format/signature checks.
    This helper cannot grant access or verify destruction of other key copies.
    """
    verify_envelope(envelope, binding, expected, now=now)
    if type(data_key) is not bytes or len(data_key) != 32:
        raise InvalidRecord('256-bit data key required')
    if now >= envelope['delete_after']:
        raise InvalidRecord('expired evidence: do not decrypt without a new authorized retention record')
    try:
        return AESGCM(data_key).decrypt(unb64(envelope['encryption']['nonce']),
            unb64(envelope['encryption']['ciphertext']), associated_data(envelope))
    except InvalidTag as error:
        raise InvalidRecord('evidence key or ciphertext authentication failed') from error
