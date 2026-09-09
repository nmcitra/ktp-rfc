#!/usr/bin/env python3
"""Executable v3 trajectory encoding and signature reference (not an authorizer).

Checks real JWS signatures and exact canonical payload coverage. Trust anchors,
consensus certificates, freshness, revocation, durable cutover and single-use
migration storage must be independently implemented. Callers MUST NOT obtain
trusted arguments from the candidate record. Dependencies are pinned in CI.
"""
import base64
import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, ed448, utils
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parent.parent
VERSION = 'ktp-trajectory-v3'
AGENT_TYPE = 'ktp-trajectory-agent-v3'
ORACLE_TYPE = 'ktp-trajectory-oracle-v3'
MIGRATION_TYPE = 'ktp-trajectory-migration-v3'
READINESS_TYPE = 'ktp-readiness-attestation-v1'
READINESS_DECISION_TYPE = 'ktp-readiness-decision-v1'
PRIVACY_EVIDENCE_TYPE = 'ktp-privacy-evidence-v1'
SIGNATURE_PURPOSES = (AGENT_TYPE, ORACLE_TYPE, MIGRATION_TYPE,
                      READINESS_TYPE, READINESS_DECISION_TYPE, PRIVACY_EVIDENCE_TYPE)
MAX_INTEGER = 2**53 - 1
DERIVED = {'agent_signature', 'oracle_attestation', 'record_hash'}
# Orders of the NIST curves; low-s follows KTP-CRYPTO's malleability rule.
ORDERS = {
    'ES256': int('ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551', 16),
    'ES384': int('ffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973', 16),
}


class InvalidRecord(ValueError):
    """Malformed, mismatched, unsupported, or unauthenticated input."""


def json_value(value, active=None):
    """Reject Python-only values, unsafe integers, nonfinite values and cycles."""
    active = set() if active is None else active
    if value is None or type(value) is bool:
        return
    if type(value) is str:
        try:
            value.encode('utf-8', errors='strict')
        except UnicodeError as error:
            raise InvalidRecord('invalid Unicode scalar') from error
        return
    if type(value) is int:
        if abs(value) > MAX_INTEGER:
            raise InvalidRecord('integer exceeds exact interoperable range')
        return
    if type(value) is float:
        if not math.isfinite(value):
            raise InvalidRecord('nonfinite number')
        if value.is_integer() and abs(value) > MAX_INTEGER:
            raise InvalidRecord('integer-valued number exceeds exact interoperable range')
        return
    if type(value) not in (dict, list) or id(value) in active:
        raise InvalidRecord('non-JSON value or cycle')
    active.add(id(value))
    try:
        if type(value) is dict:
            for key, child in value.items():
                if type(key) is not str:
                    raise InvalidRecord('object names must be strings')
                json_value(key, active)
                json_value(child, active)
        else:
            for child in value:
                json_value(child, active)
    finally:
        active.remove(id(value))


def canonical(value):
    try:
        json_value(value)
        return rfc8785.dumps(value)
    except (rfc8785.CanonicalizationError, RecursionError) as error:
        raise InvalidRecord('cannot canonicalize JSON') from error


def strict_loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InvalidRecord('duplicate object name')
            result[key] = value
        return result

    def nonfinite(_):
        raise InvalidRecord('nonfinite JSON constant')

    try:
        if isinstance(raw, bytes):
            raw = raw.decode('utf-8', errors='strict')
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)
        canonical(value)
        return value
    except (ValueError, TypeError, UnicodeError, RecursionError) as error:
        raise InvalidRecord(str(error)) from error


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def unb64(text):
    if type(text) is not str or not re.fullmatch(r'[A-Za-z0-9_-]+', text):
        raise InvalidRecord('invalid unpadded base64url')
    try:
        result = base64.urlsafe_b64decode(text + '=' * (-len(text) % 4))
    except ValueError as error:
        raise InvalidRecord('invalid base64url length') from error
    if b64(result) != text:
        raise InvalidRecord('noncanonical base64url')
    return result


def digest_bytes(data, level):
    if type(level) is not int or level not in (1, 2, 3):
        raise InvalidRecord('unsupported trusted conformance level')
    algorithm = 'sha384' if level == 3 else 'sha256'
    return algorithm + ':' + hashlib.new(algorithm, data).hexdigest()


def digest(value, level):
    return digest_bytes(canonical(value), level)


@dataclass(frozen=True)
class KeyBinding:
    """Previously authenticated key/role/subject binding, never candidate data."""
    key_id: str
    subject: str
    algorithm: str
    purpose: str
    public_key: object
    zone_id: str


def literal(value):
    if type(value) is not str or not value or re.search(r'[\s*?\[\]{}]', value):
        raise InvalidRecord('expected nonempty literal identifier')


def check_key(key, algorithm, level):
    if hasattr(key, 'public_key'):
        key = key.public_key()
    if algorithm in ('ES256', 'ES384'):
        curve = ec.SECP256R1 if algorithm == 'ES256' else ec.SECP384R1
        valid = isinstance(key, ec.EllipticCurvePublicKey) and isinstance(key.curve, curve)
        if level == 3 and algorithm != 'ES384':
            valid = False
    elif algorithm == 'EdDSA':
        valid = isinstance(key, (ed25519.Ed25519PublicKey, ed448.Ed448PublicKey))
        if level == 3 and not isinstance(key, ed448.Ed448PublicKey):
            valid = False
    else:
        valid = False
    if not valid:
        raise InvalidRecord('key, algorithm, or trusted strength mismatch')
    return key


def sign_jws(payload, private_key, *, key_id, algorithm, purpose, level):
    """Reference signing for conformance fixtures; contains no key management."""
    digest_bytes(b'', level)
    literal(key_id)
    check_key(private_key, algorithm, level)
    if purpose not in SIGNATURE_PURPOSES:
        raise InvalidRecord('unknown signature purpose')
    header = {'alg': algorithm, 'kid': key_id, 'typ': purpose}
    message = (b64(canonical(header)) + '.' + b64(canonical(payload))).encode('ascii')
    if algorithm in ORDERS:
        hash_alg = hashes.SHA256() if algorithm == 'ES256' else hashes.SHA384()
        r, s = utils.decode_dss_signature(private_key.sign(message, ec.ECDSA(hash_alg)))
        s = min(s, ORDERS[algorithm] - s)
        size = 32 if algorithm == 'ES256' else 48
        signature = r.to_bytes(size, 'big') + s.to_bytes(size, 'big')
    else:
        signature = private_key.sign(message)
    return message.decode('ascii') + '.' + b64(signature)


def verify_jws(token, expected_payload, binding, *, level):
    digest_bytes(b'', level)
    literal(binding.key_id)
    literal(binding.subject)
    literal(binding.zone_id)
    if binding.purpose not in SIGNATURE_PURPOSES:
        raise InvalidRecord('unknown trusted signature purpose')
    if type(token) is not str:
        raise InvalidRecord('signature must be compact JWS')
    pieces = token.split('.')
    if len(pieces) != 3:
        raise InvalidRecord('signature must have three segments')
    header_raw, payload_raw, signature = map(unb64, pieces)
    header = strict_loads(header_raw)
    expected_header = {'alg': binding.algorithm, 'kid': binding.key_id, 'typ': binding.purpose}
    if header != expected_header or canonical(header) != header_raw:
        raise InvalidRecord('protected header does not match trusted binding')
    if canonical(expected_payload) != payload_raw:
        raise InvalidRecord('signed payload does not match complete canonical content')
    key = check_key(binding.public_key, binding.algorithm, level)
    message = (pieces[0] + '.' + pieces[1]).encode('ascii')
    try:
        if binding.algorithm in ORDERS:
            size = 32 if binding.algorithm == 'ES256' else 48
            if len(signature) != size * 2:
                raise InvalidRecord('invalid raw ECDSA signature length')
            r, s = int.from_bytes(signature[:size], 'big'), int.from_bytes(signature[size:], 'big')
            if not (0 < r < ORDERS[binding.algorithm] and 0 < s <= ORDERS[binding.algorithm] // 2):
                raise InvalidRecord('invalid or non-low-s ECDSA signature')
            hash_alg = hashes.SHA256() if binding.algorithm == 'ES256' else hashes.SHA384()
            key.verify(utils.encode_dss_signature(r, s), message, ec.ECDSA(hash_alg))
        else:
            key.verify(signature, message)
    except (InvalidSignature, ValueError) as error:
        raise InvalidRecord('signature verification failed') from error


def body(record):
    return {key: value for key, value in record.items() if key not in DERIVED}


def oracle_payload(record):
    return {'record_body': body(record), 'agent_signature': record['agent_signature'],
            'attestation': {key: value for key, value in record['oracle_attestation'].items()
                            if key != 'oracle_signature'}}


def record_digest(record):
    return digest({key: value for key, value in record.items() if key != 'record_hash'},
                  record['conformance_level'])


def commit_intent(record):
    return digest({'purpose': 'ktp-trajectory-commit-v3', 'payload': oracle_payload(record)},
                  record['conformance_level'])


SCHEMA = json.loads((ROOT / 'schemas/transaction-record.json').read_text())
RISK_SCHEMA = json.loads((ROOT / 'schemas/risk-factors.json').read_text())
REGISTRY = Registry().with_resource(RISK_SCHEMA['$id'], Resource.from_contents(RISK_SCHEMA))
VALIDATOR = Draft202012Validator(SCHEMA, registry=REGISTRY, format_checker=FormatChecker())
STATE_VALIDATOR = Draft202012Validator({'$defs': SCHEMA['$defs'], '$ref': '#/$defs/agentState'})


def validate_record(record):
    canonical(record)
    errors = list(VALIDATOR.iter_errors(record))
    if errors:
        raise InvalidRecord('record schema: ' + errors[0].message)
    for state in (record['previous_state'], record['current_state']):
        if state is not None and type(state['generation']) is not int:
            raise InvalidRecord('generation must be an integer token')
    if type(record['sequence']) is not int or type(record['conformance_level']) is not int:
        raise InvalidRecord('sequence and level must be integer tokens')
    if instant(record['oracle_attestation']['attestation_time']) < instant(record['timestamp']):
        raise InvalidRecord('attestation predates event')


def instant(text):
    if type(text) is not str or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z', text):
        raise InvalidRecord('expected UTC timestamp with at most microsecond precision')
    try:
        return datetime.fromisoformat(text.replace('Z', '+00:00'))
    except ValueError as error:
        raise InvalidRecord('invalid timestamp') from error


def verify_record(record, agent, oracle, *, trusted_level, trusted_profile_digest,
                  expected_agent, expected_zone, expected_chain):
    """Verify integrity and supplied identity/profile bindings, never authority."""
    validate_record(record)
    if agent.zone_id != expected_zone or oracle.zone_id != expected_zone:
        raise InvalidRecord('key is not authorized in expected zone')
    if (record['agent_id'], record['zone_id'], record['chain_id'], record['conformance_level'],
        record['evaluation_profile_digest']) != (
            expected_agent, expected_zone, expected_chain, trusted_level, trusted_profile_digest):
        raise InvalidRecord('record does not match trusted deployment/chain')
    if agent.subject != expected_agent or agent.purpose != AGENT_TYPE:
        raise InvalidRecord('agent key role/subject mismatch')
    if oracle.subject != record['oracle_attestation']['oracle_id'] or oracle.purpose != ORACLE_TYPE:
        raise InvalidRecord('Oracle key role/subject mismatch')
    verify_jws(record['agent_signature'], body(record), agent, level=trusted_level)
    verify_jws(record['oracle_attestation']['oracle_signature'], oracle_payload(record), oracle,
               level=trusted_level)
    if record['record_hash'] != record_digest(record):
        raise InvalidRecord('completed record hash mismatch')
    # Deliberately no boolean ALLOW: this result is integrity evidence only.
    return {'record_hash': record['record_hash'], 'commit_intent': commit_intent(record)}


def head_binding(record):
    return {key: record[key] for key in ('record_version', 'agent_id', 'zone_id', 'chain_id',
                                       'sequence', 'previous_hash', 'record_hash')} | {
        'commit_intent': commit_intent(record)}


def verify_head_binding(record, authenticated_head):
    """Compare an externally authenticated immutable head and recompute its hash.

    The caller must also run verify_record with trusted keys. This comparison
    does not authenticate the head evidence or independently verify signatures.
    """
    validate_record(record)
    if record['record_hash'] != record_digest(record):
        raise InvalidRecord('completed record hash mismatch before head comparison')
    canonical(authenticated_head)
    if canonical(head_binding(record)) != canonical(authenticated_head):
        raise InvalidRecord('record does not match independently authenticated final head')


MIGRATION_FIELDS = {'checkpoint_version', 'checkpoint_id', 'agent_id', 'zone_id', 'issued_at',
                    'expires_at', 'legacy_chain_id', 'legacy_sequence', 'legacy_record_hash',
                    'legacy_archive_digest', 'new_chain_id', 'new_genesis_record_id',
                    'new_genesis_timestamp', 'conformance_level', 'evaluation_profile_digest',
                    'approved_state', 'revalidation_evidence_digest'}


def verify_migration(checkpoint, token, authority, record, *, trusted_level,
                     trusted_checkpoint_digest, trusted_revalidated_state, trusted_now):
    """Verify an approved migration's signed binding, not approval or single-use storage.

    trusted_* inputs must come from independent commissioning/verification. The
    caller must separately run verify_record with trusted agent/Oracle keys,
    atomically reserve the lineage transition, and anchor the final genesis
    through the reviewed protocol before authority can carry forward. This
    function checks the checkpoint signature, not the record signatures.
    """
    canonical(checkpoint)
    validate_record(record)
    if type(checkpoint) is not dict or set(checkpoint) != MIGRATION_FIELDS:
        raise InvalidRecord('migration checkpoint shape mismatch')
    state = checkpoint['approved_state']
    if not STATE_VALIDATOR.is_valid(state) or type(state['generation']) is not int:
        raise InvalidRecord('migration approved state must satisfy the state schema and integer controls')
    if checkpoint['checkpoint_version'] != MIGRATION_TYPE or authority.purpose != MIGRATION_TYPE:
        raise InvalidRecord('migration version or authority role mismatch')
    if authority.zone_id != record['zone_id']:
        raise InvalidRecord('migration authority is not authorized for target zone')
    for field in MIGRATION_FIELDS - {'legacy_sequence', 'conformance_level', 'approved_state'}:
        if type(checkpoint[field]) is not str or not checkpoint[field]:
            raise InvalidRecord('migration string field missing')
    for field in ('legacy_sequence', 'conformance_level'):
        if type(checkpoint[field]) is not int:
            raise InvalidRecord('migration integer field invalid')
    for field in ('checkpoint_id', 'agent_id', 'zone_id', 'legacy_chain_id',
                  'new_chain_id', 'new_genesis_record_id'):
        literal(checkpoint[field])
    if not 0 <= checkpoint['legacy_sequence'] <= MAX_INTEGER:
        raise InvalidRecord('legacy sequence invalid')
    for field in ('legacy_record_hash', 'legacy_archive_digest', 'evaluation_profile_digest',
                  'revalidation_evidence_digest'):
        if not re.fullmatch(r'sha(?:256:[0-9a-f]{64}|384:[0-9a-f]{96})', checkpoint[field]):
            raise InvalidRecord('migration digest invalid')
    if trusted_level == 3 and any(not checkpoint[field].startswith('sha384:') for field in (
            'legacy_archive_digest', 'evaluation_profile_digest', 'revalidation_evidence_digest')):
        raise InvalidRecord('migration evidence digest downgrade')
    if checkpoint['legacy_chain_id'] == checkpoint['new_chain_id']:
        raise InvalidRecord('migration requires a distinct new chain')
    if not (instant(checkpoint['issued_at']) <= instant(trusted_now) < instant(checkpoint['expires_at'])):
        raise InvalidRecord('migration checkpoint not currently valid')
    verify_jws(token, checkpoint, authority, level=trusted_level)
    actual_digest = digest_bytes(token.encode('ascii'), trusted_level)
    if actual_digest != trusted_checkpoint_digest or record['migration_checkpoint'] != actual_digest:
        raise InvalidRecord('migration checkpoint is not the independently approved one')
    if record['sequence'] != 0 or record['previous_hash'] is not None or record['previous_state'] is not None:
        raise InvalidRecord('migration must initialize a new chain')
    mappings = {'agent_id': 'agent_id', 'zone_id': 'zone_id', 'new_chain_id': 'chain_id',
                'new_genesis_record_id': 'record_id', 'new_genesis_timestamp': 'timestamp',
                'conformance_level': 'conformance_level',
                'evaluation_profile_digest': 'evaluation_profile_digest'}
    if record['record_version'] != VERSION or checkpoint['conformance_level'] != trusted_level:
        raise InvalidRecord('migration format or strength mismatch')
    if any(canonical(checkpoint[k]) != canonical(record[v]) for k, v in mappings.items()):
        raise InvalidRecord('migration target mismatch')
    if canonical(checkpoint['approved_state']) != canonical(trusted_revalidated_state) or canonical(
            record['current_state']) != canonical(trusted_revalidated_state):
        raise InvalidRecord('migration must use independently revalidated state')
