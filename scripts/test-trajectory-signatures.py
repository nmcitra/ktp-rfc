#!/usr/bin/env python3
"""Real-cryptography regressions for the v3 trajectory reference.

Uses only deliberately fixed, public test-key material. Published fixtures carry
public keys, never private credentials. Tests exercise schema validation, JCS,
Ed25519/Ed448/P-256/P-384 JWS, exact signed payloads and supplied trust bindings.
They do not implement or certify consensus, a head store, migration consumption,
state revalidation, key custody, revocation, or an authorization engine.

Dependencies: cryptography==50.0.1, rfc8785==0.1.4, jsonschema==4.26.0.
Run: python3 scripts/test-trajectory-signatures.py
"""

import copy
import hashlib
import json
import math
import struct
import sys
import unittest
from dataclasses import replace
from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, ed448, utils
from jsonschema import Draft202012Validator
import rfc8785

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import trajectory_signatures as TS

FIXTURE_PATH = ROOT / 'specifications/conformance/trajectory-signatures-v3.json'
LEGACY_HASH = 'd0649fd4d7c77eb85243b37f115b48adf145cbcfd4d8b43cff912d8014fc0f12'
ZONE = 'zone-test'
AGENT = 'agent-test'
ORACLE = 'oracle-test'
CHAIN = 'chain-test-v3'


def test_key(kind, role):
    """Known test-only keys; never use these reproducible values operationally."""
    byte = {'agent': 17, 'oracle': 34, 'migration': 51, 'other': 68}[role]
    if kind == 'Ed25519':
        return ed25519.Ed25519PrivateKey.from_private_bytes(bytes([byte]) * 32)
    if kind == 'Ed448':
        return ed448.Ed448PrivateKey.from_private_bytes(bytes([byte]) * 57)
    curve = ec.SECP256R1() if kind == 'ES256' else ec.SECP384R1()
    return ec.derive_private_key(byte, curve)


def binding(kind, role):
    purpose = {'agent': TS.AGENT_TYPE, 'oracle': TS.ORACLE_TYPE,
               'migration': TS.MIGRATION_TYPE}[role]
    subject = {'agent': AGENT, 'oracle': ORACLE, 'migration': 'migration-authority-test'}[role]
    return TS.KeyBinding(key_id=f'{role}-test-{kind}', subject=subject,
                         algorithm=kind if kind.startswith('ES') else 'EdDSA',
                         purpose=purpose, public_key=test_key(kind, role).public_key(),
                         zone_id=ZONE)


def profile_digest(level):
    return TS.digest({'profile_id': 'test-only-evaluation', 'version': 1}, level)


def unsigned_record(level=2, predecessor=None):
    state = {'e_base': 20, 'e_trust': 18, 'location': ZONE, 'tier': 'observer',
             'lineage': 'sponsored', 'generation': 0}
    sequence = 0 if predecessor is None else predecessor['sequence'] + 1
    return {
        'record_version': TS.VERSION, 'record_id': f'record-test-{sequence}',
        'agent_id': AGENT, 'zone_id': ZONE, 'chain_id': CHAIN,
        'sequence': sequence, 'timestamp': f'2026-09-06T12:00:0{sequence}Z',
        'previous_hash': None if predecessor is None else predecessor['record_hash'],
        'previous_state': None if predecessor is None else copy.deepcopy(predecessor['current_state']),
        'current_state': state,
        'action': {'action_type': 'GENESIS' if sequence == 0 else 'READ',
                   'action_risk': 0 if sequence == 0 else 5,
                   'target': None if sequence == 0 else '/service/test-report',
                   'result': 'success',
                   'details': {'records_accessed': sequence, 'classification': 'test-only',
                               'nested': {'enabled': True, 'labels': ['alpha', 'β'],
                                          'optional': None, 'fraction': 0.25}}},
        'friction': 0.1, 'velocity': 0 if sequence == 0 else 2.5,
        'conformance_level': level, 'evaluation_profile_digest': profile_digest(level),
        'migration_checkpoint': None,
        'oracle_attestation': {
            'oracle_id': ORACLE, 'attestation_time': f'2026-09-06T12:00:0{sequence}.500000Z',
            'risk_factors': {field: 0.1 for field in TS.RISK_SCHEMA['required']}},
    }


def sign_record(record, kind='Ed25519'):
    record = copy.deepcopy(record)
    level = record['conformance_level']
    agent, oracle = binding(kind, 'agent'), binding(kind, 'oracle')
    record['agent_signature'] = TS.sign_jws(
        TS.body(record), test_key(kind, 'agent'), key_id=agent.key_id,
        algorithm=agent.algorithm, purpose=agent.purpose, level=level)
    record['oracle_attestation']['oracle_signature'] = TS.sign_jws(
        TS.oracle_payload(record), test_key(kind, 'oracle'), key_id=oracle.key_id,
        algorithm=oracle.algorithm, purpose=oracle.purpose, level=level)
    record['record_hash'] = TS.record_digest(record)
    return record


def trusted_context(level=2):
    return {'trusted_level': level, 'trusted_profile_digest': profile_digest(level),
            'expected_agent': AGENT, 'expected_zone': ZONE, 'expected_chain': CHAIN}


def verify(record, kind='Ed25519', **overrides):
    context = trusted_context(record['conformance_level'])
    context.update(overrides)
    return TS.verify_record(record, binding(kind, 'agent'), binding(kind, 'oracle'), **context)


def leaves(value, path=()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaves(child, path + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from leaves(child, path + (index,))
    else:
        yield path, value


def changed(value):
    if value is None:
        return 'changed-null'
    if type(value) is bool:
        return not value
    if isinstance(value, str):
        return value + '-changed'
    return value + 1


def set_path(value, path, replacement):
    candidate = copy.deepcopy(value)
    target = candidate
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    return candidate


def raw_ed_jws(header_bytes, payload_bytes, role='agent'):
    """Sign intentionally hostile wire encodings with a real test Ed25519 key."""
    message = (TS.b64(header_bytes) + '.' + TS.b64(payload_bytes)).encode('ascii')
    return message.decode('ascii') + '.' + TS.b64(test_key('Ed25519', role).sign(message))


def public_binding(key):
    return {'key_id': key.key_id, 'subject': key.subject, 'algorithm': key.algorithm,
            'purpose': key.purpose, 'zone_id': key.zone_id,
            'public_key_spki_der_base64url': TS.b64(key.public_key.public_bytes(
                serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo))}


def load_public_binding(value):
    return TS.KeyBinding(key_id=value['key_id'], subject=value['subject'],
                         algorithm=value['algorithm'], purpose=value['purpose'],
                         zone_id=value['zone_id'], public_key=serialization.load_der_public_key(
                             TS.unb64(value['public_key_spki_der_base64url'])))


def fixture_document():
    """Explicit fixture construction, never invoked by the test runner."""
    genesis = sign_record(unsigned_record())
    successor = sign_record(unsigned_record(predecessor=genesis))
    cases = []
    for record, label in ((genesis, 'genesis'), (successor, 'successor')):
        cases.append({
            'id': f'ed25519-level2-{label}', 'record': record,
            'trusted_context': trusted_context(),
            'agent_binding': public_binding(binding('Ed25519', 'agent')),
            'oracle_binding': public_binding(binding('Ed25519', 'oracle')),
            'expected': {
                'agent_payload_utf8': TS.canonical(TS.body(record)).decode('utf-8'),
                'agent_signing_input_ascii': '.'.join(record['agent_signature'].split('.')[:2]),
                'oracle_payload_utf8': TS.canonical(TS.oracle_payload(record)).decode('utf-8'),
                'oracle_signing_input_ascii': '.'.join(record['oracle_attestation']['oracle_signature'].split('.')[:2]),
                'record_hash': record['record_hash'], 'commit_intent': TS.commit_intent(record),
                'final_head_binding': TS.head_binding(record),
            },
        })
    return {
        'suite': 'trajectory-signatures-v3',
        'kind': 'executable-public-key-cryptographic-fixtures',
        'specification': 'specifications/trajectory-signatures.md',
        'note': ('These fixed public test keys and signatures exercise record integrity only. '
                 'The keys have no operational authority. No private keys are stored here. '
                 'Expected payloads, signing inputs, final hashes and intent digests are fixed '
                 'known answers. Tests also generate real Ed448, ES256 and ES384 cases. '
                 'The separate trajectory-lifecycle-v3.json specifies downstream consensus, '
                 'unique-head, migration registry and recovery obligations; those services '
                 'are not executed by this fixture.'),
        'canonicalization_reference': 'https://www.rfc-editor.org/rfc/rfc8785.html',
        'cases': cases,
    }


def migration_case(level=2):
    kind = 'Ed448' if level == 3 else 'Ed25519'
    record = unsigned_record(level)
    checkpoint = {
        'checkpoint_version': TS.MIGRATION_TYPE, 'checkpoint_id': 'migration-test-1',
        'agent_id': AGENT, 'zone_id': ZONE,
        'issued_at': '2026-09-06T11:00:00Z', 'expires_at': '2026-09-06T13:00:00Z',
        'legacy_chain_id': 'chain-test-legacy', 'legacy_sequence': 7,
        'legacy_record_hash': 'sha256:' + 'a' * 64,
        'legacy_archive_digest': TS.digest_bytes(b'test-only archived evidence', level),
        'new_chain_id': CHAIN, 'new_genesis_record_id': record['record_id'],
        'new_genesis_timestamp': record['timestamp'], 'conformance_level': level,
        'evaluation_profile_digest': profile_digest(level),
        'approved_state': copy.deepcopy(record['current_state']),
        'revalidation_evidence_digest': TS.digest_bytes(b'test-only independent revalidation', level),
    }
    authority = binding(kind, 'migration')
    token = TS.sign_jws(checkpoint, test_key(kind, 'migration'), key_id=authority.key_id,
                        algorithm=authority.algorithm, purpose=authority.purpose, level=level)
    checkpoint_digest = TS.digest_bytes(token.encode('ascii'), level)
    record['migration_checkpoint'] = checkpoint_digest
    record = sign_record(record, kind)
    trusted = {'trusted_level': level, 'trusted_checkpoint_digest': checkpoint_digest,
               'trusted_revalidated_state': copy.deepcopy(checkpoint['approved_state']),
               'trusted_now': '2026-09-06T12:00:00Z'}
    return checkpoint, token, authority, record, trusted


class TrajectorySignatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures = TS.strict_loads(FIXTURE_PATH.read_bytes())
        cls.genesis = sign_record(unsigned_record())
        cls.record = sign_record(unsigned_record(predecessor=cls.genesis))

    def test_published_fixtures_verify_real_signatures_and_known_payloads(self):
        for case in self.fixtures['cases']:
            with self.subTest(case=case['id']):
                record, expected = case['record'], case['expected']
                agent = load_public_binding(case['agent_binding'])
                oracle = load_public_binding(case['oracle_binding'])
                result = TS.verify_record(record, agent, oracle, **case['trusted_context'])
                self.assertEqual(result, {key: expected[key] for key in ('record_hash', 'commit_intent')})
                self.assertEqual(TS.canonical(TS.body(record)), expected['agent_payload_utf8'].encode())
                self.assertEqual(TS.canonical(TS.oracle_payload(record)), expected['oracle_payload_utf8'].encode())
                for token, role in ((record['agent_signature'], 'agent'),
                                    (record['oracle_attestation']['oracle_signature'], 'oracle')):
                    self.assertEqual('.'.join(token.split('.')[:2]), expected[f'{role}_signing_input_ascii'])
                TS.verify_head_binding(record, expected['final_head_binding'])
                # Independent hash construction checks the fixture's expected
                # completed record and intent domains, not only schema shape.
                completed = {k: v for k, v in record.items() if k != 'record_hash'}
                self.assertEqual('sha256:' + hashlib.sha256(TS.canonical(completed)).hexdigest(), expected['record_hash'])
                proposed = {'purpose': 'ktp-trajectory-commit-v3', 'payload': TS.oracle_payload(record)}
                self.assertEqual('sha256:' + hashlib.sha256(TS.canonical(proposed)).hexdigest(), expected['commit_intent'])

    def test_fixture_genesis_and_successor_have_exact_continuity(self):
        first, second = [case['record'] for case in self.fixtures['cases']]
        self.assertEqual(first['sequence'], 0)
        self.assertIsNone(first['previous_hash'])
        self.assertIsNone(first['previous_state'])
        self.assertEqual(second['sequence'], first['sequence'] + 1)
        self.assertEqual(second['previous_hash'], first['record_hash'])
        self.assertEqual(second['previous_state'], first['current_state'])
        self.assertGreater(TS.instant(second['timestamp']), TS.instant(first['timestamp']))
        self.assertEqual(second['chain_id'], first['chain_id'])

    def test_all_supported_curves_and_trusted_levels(self):
        for level in (1, 2, 3):
            for kind in ('Ed25519', 'Ed448', 'ES256', 'ES384'):
                if level == 3 and kind in ('Ed25519', 'ES256'):
                    continue
                with self.subTest(level=level, kind=kind):
                    record = sign_record(unsigned_record(level), kind)
                    result = verify(record, kind)
                    self.assertEqual(result['record_hash'], record['record_hash'])
                    self.assertTrue(record['record_hash'].startswith('sha384:' if level == 3 else 'sha256:'))
                    self.assertNotIn('allow', result)

    def test_every_body_leaf_is_covered_by_real_agent_signature(self):
        count = 0
        for path, value in leaves(TS.body(self.record)):
            with self.subTest(path=path):
                altered = set_path(self.record, path, changed(value))
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(self.record['agent_signature'], TS.body(altered), binding('Ed25519', 'agent'), level=2)
                with self.assertRaises(TS.InvalidRecord):
                    verify(altered)
                count += 1
        self.assertGreaterEqual(count, 35)

    def test_all_attestation_leaves_are_covered_by_real_oracle_signature(self):
        attestation = {k: v for k, v in self.record['oracle_attestation'].items() if k != 'oracle_signature'}
        paths = list(leaves(attestation))
        self.assertEqual(len(paths), 8)
        for path, value in paths:
            with self.subTest(path=path):
                altered = set_path(self.record, ('oracle_attestation',) + path, changed(value))
                TS.verify_jws(altered['agent_signature'], TS.body(altered), binding('Ed25519', 'agent'), level=2)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(self.record['oracle_attestation']['oracle_signature'], TS.oracle_payload(altered), binding('Ed25519', 'oracle'), level=2)
                with self.assertRaises(TS.InvalidRecord):
                    verify(altered)

    def test_changed_valid_agent_envelope_invalidates_oracle_signature(self):
        record = sign_record(unsigned_record(), 'ES256')
        agent = binding('ES256', 'agent')
        replacement = TS.sign_jws(TS.body(record), test_key('ES256', 'agent'),
                                  key_id=agent.key_id, algorithm=agent.algorithm,
                                  purpose=agent.purpose, level=2)
        self.assertNotEqual(replacement, record['agent_signature'])
        TS.verify_jws(replacement, TS.body(record), agent, level=2)
        record['agent_signature'] = replacement
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_jws(record['oracle_attestation']['oracle_signature'], TS.oracle_payload(record), binding('ES256', 'oracle'), level=2)

    def test_unknown_fields_cannot_be_unsigned_extensions(self):
        for path in ((), ('action',), ('current_state',), ('previous_state',),
                     ('oracle_attestation',), ('oracle_attestation', 'risk_factors')):
            with self.subTest(path=path):
                altered = copy.deepcopy(self.record)
                target = altered
                for key in path:
                    target = target[key]
                target['new_authority'] = True
                with self.assertRaises(TS.InvalidRecord):
                    TS.validate_record(altered)
        altered = set_path(self.record, ('action', 'details', 'unsigned_extension'), {'can_write': True})
        self.assertTrue(TS.VALIDATOR.is_valid(altered))
        with self.assertRaises(TS.InvalidRecord):
            verify(altered)

    def test_completed_hash_cannot_be_replaced_or_recomputed_to_hide_body_mutation(self):
        altered = copy.deepcopy(self.record)
        altered['record_hash'] = 'sha256:' + '0' * 64
        with self.assertRaisesRegex(TS.InvalidRecord, 'hash mismatch'):
            verify(altered)
        altered = set_path(self.record, ('current_state', 'e_base'), 90)
        altered['record_hash'] = TS.record_digest(altered)
        with self.assertRaises(TS.InvalidRecord):
            verify(altered)

    def test_legacy_selective_projection_misses_state_that_v3_authenticates(self):
        def legacy_projection(record, oracle=False):
            # Test-only field projection of the pre-v3 documented preimages.
            # It does not invent an archived wire encoding or verify old data.
            values = [record[k] for k in ('record_id', 'action', 'previous_hash', 'timestamp')]
            if oracle:
                values += [record['agent_signature'], record['oracle_attestation']['risk_factors']]
            return TS.canonical(values)
        altered = set_path(self.record, ('current_state', 'e_base'), 90)
        for oracle in (False, True):
            self.assertEqual(legacy_projection(self.record, oracle), legacy_projection(altered, oracle))
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_jws(self.record['agent_signature'], TS.body(altered), binding('Ed25519', 'agent'), level=2)
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_jws(self.record['oracle_attestation']['oracle_signature'], TS.oracle_payload(altered), binding('Ed25519', 'oracle'), level=2)

    def test_equivalent_outer_json_formatting_and_key_order_keep_signatures_valid(self):
        def reversed_objects(value):
            if isinstance(value, dict):
                return {k: reversed_objects(v) for k, v in reversed(list(value.items()))}
            if isinstance(value, list):
                return [reversed_objects(v) for v in value]
            return value
        formatted = json.dumps(reversed_objects(self.record), ensure_ascii=True, indent=3)
        parsed = TS.strict_loads(formatted)
        self.assertEqual(verify(parsed), verify(self.record))
        self.assertEqual(TS.canonical(parsed), TS.canonical(self.record))

    def test_rfc8785_utf16_property_order_and_array_order(self):
        # RFC 8785 section 3.2.3 keys, with numeric labels to expose order.
        sample = {'\u20ac': 5, '\r': 1, '\ufb33': 7, '1': 2,
                  '\U0001f600': 6, '\u0080': 3, '\u00f6': 4}
        expected_keys = ['\r', '1', '\u0080', '\u00f6', '\u20ac', '\U0001f600', '\ufb33']
        result = TS.strict_loads(TS.canonical(sample))
        self.assertEqual(list(result), expected_keys)
        self.assertEqual(list(result.values()), list(range(1, 8)))
        nested = TS.strict_loads(TS.canonical({'array': [sample, {'z': 1, 'a': 2}, 0]}))
        self.assertEqual(list(nested['array'][0]), expected_keys)
        self.assertEqual(list(nested['array'][1]), ['a', 'z'])
        self.assertEqual(nested['array'][2], 0)

    def test_rfc8785_published_binary64_number_vectors(self):
        # Selected IEEE-754 known answers from RFC 8785 Appendix B.
        cases = {
            '0000000000000000': '0', '8000000000000000': '0',
            '0000000000000001': '5e-324', '8000000000000001': '-5e-324',
            '7fefffffffffffff': '1.7976931348623157e+308',
            'ffefffffffffffff': '-1.7976931348623157e+308',
            '44b52d02c7e14af5': '9.999999999999997e+22',
            '44b52d02c7e14af6': '1e+23',
            '44b52d02c7e14af7': '1.0000000000000001e+23',
            '3eb0c6f7a0b5ed8c': '9.999999999999997e-7',
            '3eb0c6f7a0b5ed8d': '0.000001',
            '41b3de4355555555': '333333333.3333333',
            'becbf647612f3696': '-0.0000033333333333333333',
            '43143ff3c1cb0959': '1424953923781206.2',
        }
        for bits, expected in cases.items():
            with self.subTest(bits=bits):
                value = struct.unpack('>d', bytes.fromhex(bits))[0]
                self.assertEqual(rfc8785.dumps(value), expected.encode())
                # The published JCS numeric model is wider than v3's exact
                # integer profile. Exercise its backing library's vectors,
                # then require the reference helper's stricter boundary.
                if value.is_integer() and abs(value) > TS.MAX_INTEGER:
                    with self.assertRaises(TS.InvalidRecord):
                        TS.canonical(value)
                else:
                    self.assertEqual(TS.canonical(value), expected.encode())
        self.assertEqual(TS.canonical({'n': -0.0}), b'{"n":0}')

    def test_unicode_is_preserved_without_normalization(self):
        self.assertNotEqual(TS.canonical({'x': '\u00e9'}), TS.canonical({'x': 'e\u0301'}))
        for value in ('\ud800', '\udfff', {'\ud800': 'x'}, {'x': '\udfff'}):
            with self.subTest(value=repr(value)):
                with self.assertRaises(TS.InvalidRecord):
                    TS.canonical(value)

    def test_strict_json_rejects_duplicates_nonfinite_unsafe_and_non_json_values(self):
        for raw in ('{"x":1,"x":2}', '{"nested":{"x":1,"x":2}}',
                    '{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}',
                    '{"x":1e309}', '{"x":9007199254740992}',
                    '{"x":-9007199254740992}', '"\\ud800"', b'"\xff"', '{'):
            with self.subTest(raw=raw):
                with self.assertRaises(TS.InvalidRecord):
                    TS.strict_loads(raw)
        cycle = {}; cycle['self'] = cycle
        for value in (math.nan, math.inf, -math.inf, 2**53, -(2**53),
                      9007199254740992.0, 9007199254740993.0, 9.007199254740993e15,
                      (), {1: 'x'}, {'x': object()}, cycle):
            with self.subTest(value=repr(value)):
                with self.assertRaises(TS.InvalidRecord):
                    TS.canonical(value)
        for raw in ('9007199254740992.0', '9007199254740993.0', '9.007199254740993e15'):
            with self.assertRaises(TS.InvalidRecord):
                TS.strict_loads(raw)
            self.assertEqual(TS.strict_loads(json.dumps(raw)), raw)

    def test_integer_controls_and_chain_schema_boundaries(self):
        paths = [('sequence',), ('conformance_level',),
                 ('current_state', 'generation'), ('previous_state', 'generation')]
        for path in paths:
            for value in (True, 1.0, -1, 2**53):
                with self.subTest(path=path, value=value):
                    with self.assertRaises(TS.InvalidRecord):
                        TS.validate_record(set_path(self.record, path, value))
        for path in (('previous_hash',), ('previous_state',)):
            with self.assertRaises(TS.InvalidRecord):
                TS.validate_record(set_path(self.record, path, None))
        with self.assertRaises(TS.InvalidRecord):
            TS.validate_record(set_path(self.genesis, ('previous_hash',), self.record['record_hash']))
        with self.assertRaises(TS.InvalidRecord):
            TS.validate_record(set_path(self.record, ('migration_checkpoint',), self.record['record_hash']))

    def test_compact_jws_rejects_padding_junk_and_noncanonical_base64(self):
        token = self.record['agent_signature']
        pieces = token.split('.')
        bad_tokens = [token + '=', token + '\n', token + '.extra', '.'.join(pieces[:2]),
                      '.' + token, pieces[0] + '..' + pieces[2], None, 1,
                      pieces[0] + '=.' + pieces[1] + '.' + pieces[2]]
        for candidate in bad_tokens:
            with self.subTest(candidate=str(candidate)[:30]):
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(candidate, TS.body(self.record), binding('Ed25519', 'agent'), level=2)
        for value in ('AB', 'A', 'AA=', 'AA\n', '+A', '/A', ''):
            with self.subTest(base64=value):
                with self.assertRaises(TS.InvalidRecord):
                    TS.unb64(value)

    def test_real_signatures_with_forbidden_headers_are_rejected(self):
        key = binding('Ed25519', 'agent')
        header = {'alg': key.algorithm, 'kid': key.key_id, 'typ': key.purpose}
        payload = TS.canonical(TS.body(self.record))
        bad_headers = [dict(header, alg='none'), dict(header, alg='HS256'),
                       dict(header, typ=TS.ORACLE_TYPE), dict(header, kid='attacker-key'),
                       dict(header, jwk={'kty': 'OKP'}), dict(header, jku='https://example.invalid/key'),
                       dict(header, crit=['b64']), dict(header, b64=False), dict(header, zip='DEF')]
        for candidate in bad_headers:
            with self.subTest(header=candidate):
                token = raw_ed_jws(TS.canonical(candidate), payload)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(token, TS.body(self.record), key, level=2)
        duplicate = ('{"alg":"none","alg":"EdDSA","kid":"' + key.key_id + '","typ":"' + key.purpose + '"}').encode()
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_jws(raw_ed_jws(duplicate, payload), TS.body(self.record), key, level=2)
        for key_id in ('', ' ', 'key*', None, True, 3):
            with self.subTest(malformed_key_id=key_id):
                with self.assertRaises(TS.InvalidRecord):
                    TS.sign_jws(TS.body(self.record), test_key('Ed25519', 'agent'),
                                key_id=key_id, algorithm=key.algorithm,
                                purpose=key.purpose, level=2)
                malformed = dict(header, kid=key_id)
                token = raw_ed_jws(TS.canonical(malformed), payload)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(token, TS.body(self.record), replace(key, key_id=key_id), level=2)
        for purpose in ('', 'unregistered-purpose'):
            token = raw_ed_jws(TS.canonical(dict(header, typ=purpose)), payload)
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_jws(token, TS.body(self.record), replace(key, purpose=purpose), level=2)

    def test_noncanonical_but_cryptographically_signed_header_or_payload_is_rejected(self):
        key = binding('Ed25519', 'agent')
        header = {'alg': key.algorithm, 'kid': key.key_id, 'typ': key.purpose}
        for header_bytes, payload_bytes in (
                (json.dumps(header, indent=2).encode(), TS.canonical(TS.body(self.record))),
                (TS.canonical(header), json.dumps(TS.body(self.record), indent=2).encode())):
            token = raw_ed_jws(header_bytes, payload_bytes)
            # The underlying key verifies these bytes; rejection must come
            # from the required canonical envelope/payload contract.
            first, second, signature = token.split('.')
            key.public_key.verify(TS.unb64(signature), (first + '.' + second).encode())
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_jws(token, TS.body(self.record), key, level=2)

    def test_wrong_subject_zone_role_key_and_curve_bindings_fail(self):
        agent, oracle = binding('Ed25519', 'agent'), binding('Ed25519', 'oracle')
        for altered_agent in (replace(agent, subject='another-agent'),
                              replace(agent, zone_id='another-zone'),
                              replace(agent, purpose=TS.ORACLE_TYPE),
                              replace(agent, public_key=test_key('Ed25519', 'other').public_key())):
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_record(self.record, altered_agent, oracle, **trusted_context())
        for altered_oracle in (replace(oracle, subject='another-oracle'),
                               replace(oracle, zone_id='another-zone'),
                               replace(oracle, purpose=TS.AGENT_TYPE),
                               replace(oracle, public_key=test_key('Ed25519', 'other').public_key())):
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_record(self.record, agent, altered_oracle, **trusted_context())
        with self.assertRaises(TS.InvalidRecord):
            TS.check_key(test_key('ES384', 'agent'), 'ES256', 2)
        with self.assertRaises(TS.InvalidRecord):
            TS.check_key(test_key('ES256', 'agent'), 'ES384', 2)

    def test_candidate_cannot_choose_expected_identity_profile_or_strength(self):
        for field, value in (('expected_agent', 'attacker-agent'), ('expected_zone', 'another-zone'),
                             ('expected_chain', 'another-chain'), ('trusted_profile_digest', 'sha256:' + '0' * 64),
                             ('trusted_level', 3), ('trusted_profile_digest', None), ('expected_chain', None)):
            with self.subTest(field=field):
                with self.assertRaises(TS.InvalidRecord):
                    verify(self.record, **{field: value})
        for kind in ('Ed25519', 'ES256'):
            with self.subTest(kind=kind):
                key = binding(kind, 'agent')
                token = TS.sign_jws({'x': 1}, test_key(kind, 'agent'), key_id=key.key_id,
                                    algorithm=key.algorithm, purpose=key.purpose, level=2)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(token, {'x': 1}, key, level=3)

    def test_ecdsa_raw_width_and_low_s_are_enforced(self):
        for kind, level, size in (('ES256', 2, 32), ('ES384', 3, 48)):
            with self.subTest(kind=kind):
                record = sign_record(unsigned_record(level), kind)
                key = binding(kind, 'agent')
                pieces = record['agent_signature'].split('.')
                raw = TS.unb64(pieces[2])
                self.assertEqual(len(raw), 2 * size)
                r, s = int.from_bytes(raw[:size], 'big'), int.from_bytes(raw[size:], 'big')
                self.assertLessEqual(s, TS.ORDERS[kind] // 2)
                high_s = TS.ORDERS[kind] - s
                key.public_key.verify(
                    utils.encode_dss_signature(r, high_s),
                    '.'.join(pieces[:2]).encode(),
                    ec.ECDSA(hashes.SHA256() if kind == 'ES256' else hashes.SHA384()))
                for signature in (r.to_bytes(size, 'big') + high_s.to_bytes(size, 'big'),
                                  utils.encode_dss_signature(r, s), raw[:-1]):
                    token = '.'.join(pieces[:2]) + '.' + TS.b64(signature)
                    with self.assertRaises(TS.InvalidRecord):
                        TS.verify_jws(token, TS.body(record), key, level=level)

    def test_distinct_valid_oracle_signatures_need_distinct_final_head_anchors(self):
        record = sign_record(unsigned_record(), 'ES256')
        alternate = copy.deepcopy(record)
        oracle = binding('ES256', 'oracle')
        alternate['oracle_attestation']['oracle_signature'] = TS.sign_jws(
            TS.oracle_payload(record), test_key('ES256', 'oracle'), key_id=oracle.key_id,
            algorithm=oracle.algorithm, purpose=oracle.purpose, level=2)
        alternate['record_hash'] = TS.record_digest(alternate)
        verify(record, 'ES256'); verify(alternate, 'ES256')
        self.assertEqual(TS.commit_intent(record), TS.commit_intent(alternate))
        self.assertNotEqual(record['record_hash'], alternate['record_hash'])
        selected_head = TS.head_binding(record)
        TS.verify_head_binding(record, selected_head)
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_head_binding(alternate, selected_head)

    def test_missing_or_substituted_final_head_is_rejected(self):
        head = TS.head_binding(self.record)
        for supplied in (None, {}, {'record_hash': self.record['record_hash']}):
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_head_binding(self.record, supplied)
        for field, value in head.items():
            with self.subTest(field=field):
                changed_head = dict(head); changed_head[field] = changed(value)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_head_binding(self.record, changed_head)
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_head_binding(self.record, dict(head, committed=True))
        corrupted = copy.deepcopy(self.record)
        parts = corrupted['oracle_attestation']['oracle_signature'].split('.')
        signature = bytearray(TS.unb64(parts[2])); signature[0] ^= 1
        corrupted['oracle_attestation']['oracle_signature'] = '.'.join(parts[:2]) + '.' + TS.b64(signature)
        with self.assertRaises(TS.InvalidRecord):
            verify(corrupted)
        # Retaining the selected original hash and head cannot conceal the
        # changed envelope, even before separate public-key verification.
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_head_binding(corrupted, head)

    def test_migration_real_signatures_and_independently_supplied_state(self):
        for level in (2, 3):
            with self.subTest(level=level):
                checkpoint, token, authority, record, trusted = migration_case(level)
                self.assertEqual(set(checkpoint), TS.MIGRATION_FIELDS)
                TS.verify_migration(checkpoint, token, authority, record, **trusted)
                verify(record, 'Ed448' if level == 3 else 'Ed25519')
                self.assertNotEqual(checkpoint['legacy_chain_id'], record['chain_id'])
                self.assertTrue(checkpoint['legacy_record_hash'].startswith('sha256:'))
                self.assertTrue(record['migration_checkpoint'].startswith('sha384:' if level == 3 else 'sha256:'))

    def test_every_migration_checkpoint_leaf_is_cryptographically_bound(self):
        checkpoint, token, authority, record, trusted = migration_case()
        count = 0
        for path, value in leaves(checkpoint):
            with self.subTest(path=path):
                candidate = set_path(checkpoint, path, changed(value))
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_jws(token, candidate, authority, level=2)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_migration(candidate, token, authority, record, **trusted)
                count += 1
        self.assertGreaterEqual(count, 22)

    def test_fresh_migration_signature_cannot_replace_the_pinned_checkpoint(self):
        checkpoint, token, authority, record, trusted = migration_case()
        candidate = dict(checkpoint, checkpoint_id='candidate-chosen-checkpoint')
        new_token = TS.sign_jws(candidate, test_key('Ed25519', 'migration'), key_id=authority.key_id,
                                algorithm=authority.algorithm, purpose=authority.purpose, level=2)
        new_record = copy.deepcopy(record)
        new_record['migration_checkpoint'] = TS.digest_bytes(new_token.encode(), 2)
        with self.assertRaisesRegex(TS.InvalidRecord, 'independently approved'):
            TS.verify_migration(candidate, new_token, authority, new_record, **trusted)
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_migration(checkpoint, token, authority, record,
                                **dict(trusted, trusted_checkpoint_digest=None))

    def test_migration_requires_external_revalidated_state(self):
        checkpoint, token, authority, record, trusted = migration_case()
        for state in (None, {}, dict(trusted['trusted_revalidated_state'], e_base=90)):
            with self.subTest(state=state):
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_migration(checkpoint, token, authority, record,
                                        **dict(trusted, trusted_revalidated_state=state))
        altered = set_path(record, ('current_state', 'e_base'), 90)
        altered = sign_record(altered)
        verify(altered)
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_migration(checkpoint, token, authority, altered, **trusted)
        floating_generation = set_path(checkpoint, ('approved_state', 'generation'), 0.0)
        # JCS encodes 0 and 0.0 alike. The mandatory integer-token boundary
        # must reject this input even though its signature bytes still match.
        TS.verify_jws(token, floating_generation, authority, level=2)
        with self.assertRaises(TS.InvalidRecord):
            TS.verify_migration(floating_generation, token, authority, record, **trusted)

    def test_migration_target_and_new_chain_bindings_are_exact(self):
        checkpoint, token, authority, record, trusted = migration_case()
        for field in ('agent_id', 'zone_id', 'chain_id', 'record_id', 'timestamp',
                      'conformance_level', 'evaluation_profile_digest', 'record_version'):
            with self.subTest(field=field):
                candidate = dict(record); candidate[field] = changed(candidate[field])
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_migration(checkpoint, token, authority, candidate, **trusted)
        for field, value in (('sequence', 1), ('previous_hash', record['record_hash']),
                             ('previous_state', record['current_state'])):
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_migration(checkpoint, token, authority, dict(record, **{field: value}), **trusted)

    def test_migration_time_and_authority_boundaries(self):
        checkpoint, token, authority, record, trusted = migration_case()
        for now in (checkpoint['issued_at'], '2026-09-06T12:59:59.999999Z'):
            TS.verify_migration(checkpoint, token, authority, record, **dict(trusted, trusted_now=now))
        for now in ('2026-09-06T10:59:59Z', checkpoint['expires_at'],
                    '2026-09-06T13:00:01Z', None, 'not-a-time'):
            with self.subTest(now=now):
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_migration(checkpoint, token, authority, record, **dict(trusted, trusted_now=now))
        for wrong in (replace(authority, zone_id='another-zone'),
                      replace(authority, purpose=TS.AGENT_TYPE),
                      replace(authority, public_key=test_key('Ed25519', 'other').public_key())):
            with self.assertRaises(TS.InvalidRecord):
                TS.verify_migration(checkpoint, token, wrong, record, **trusted)

    def test_level3_migration_rejects_weaker_new_evidence_digests(self):
        checkpoint, token, authority, record, trusted = migration_case(3)
        for field in ('legacy_archive_digest', 'evaluation_profile_digest', 'revalidation_evidence_digest'):
            with self.subTest(field=field):
                candidate = dict(checkpoint); candidate[field] = 'sha256:' + 'a' * 64
                replacement = TS.sign_jws(candidate, test_key('Ed448', 'migration'), key_id=authority.key_id,
                                          algorithm=authority.algorithm, purpose=authority.purpose, level=3)
                with self.assertRaises(TS.InvalidRecord):
                    TS.verify_migration(candidate, replacement, authority, record, **trusted)

    def test_legacy_archive_unchanged_and_unversioned_record_rejected(self):
        path = ROOT / 'schemas/transaction-record-legacy-v2.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), LEGACY_HASH)
        archive = json.loads(path.read_text())
        self.assertEqual(archive['$id'], 'https://kinetic-trust-protocol.net/specs/schemas/v2/transaction-record.json')
        with self.assertRaises(TS.InvalidRecord):
            TS.validate_record(archive['examples'][0])
        candidate = copy.deepcopy(self.record); del candidate['record_version']
        with self.assertRaises(TS.InvalidRecord):
            verify(candidate)

    def test_schema_definition_and_timestamp_validation(self):
        Draft202012Validator.check_schema(TS.SCHEMA)
        for stamp in ('2026-09-06T12:00:01Z', '2026-09-06T12:00:01.1Z',
                      '2026-09-06T12:00:01.123456Z'):
            candidate = set_path(self.record, ('timestamp',), stamp)
            TS.validate_record(candidate)
        for stamp in ('2026-02-30T12:00:01Z', '2026-09-06T12:00:60Z',
                      '2026-09-06T12:00:01.1234567Z', '2026-09-06T12:00:01+00:00',
                      '2026-09-06t12:00:01z', '2026-09-06T12:00:01Z\n'):
            with self.subTest(timestamp=stamp):
                with self.assertRaises(TS.InvalidRecord):
                    TS.validate_record(set_path(self.record, ('timestamp',), stamp))
        with self.assertRaises(TS.InvalidRecord):
            TS.validate_record(set_path(self.record, ('oracle_attestation', 'attestation_time'), '2026-09-06T11:59:59Z'))

    def test_verification_does_not_mutate_record_or_supplied_bindings(self):
        original = copy.deepcopy(self.record)
        verify(self.record)
        self.assertEqual(self.record, original)
        head = TS.head_binding(self.record); original_head = copy.deepcopy(head)
        TS.verify_head_binding(self.record, head)
        self.assertEqual(head, original_head)
        checkpoint, token, authority, record, trusted = migration_case()
        snapshots = copy.deepcopy((checkpoint, record, trusted))
        TS.verify_migration(checkpoint, token, authority, record, **trusted)
        self.assertEqual((checkpoint, record, trusted), snapshots)


if __name__ == '__main__':
    unittest.main(verbosity=2)
