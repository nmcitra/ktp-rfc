#!/usr/bin/env python3
"""Real-signature and semantic regressions for the readiness prerequisite.

The ordinary proof is an opaque signed fixture standing for an independently
verified authorization result. These tests do not implement a full ordinary
authorizer, assessor, registry, durable status store or execution fence.
"""
import copy
from dataclasses import replace
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

from cryptography.hazmat.primitives.asymmetric import ec, ed25519, ed448
from jsonschema import Draft202012Validator

import readiness as r
from trajectory_signatures import (
    AGENT_TYPE, InvalidRecord, KeyBinding, READINESS_TYPE,
    READINESS_DECISION_TYPE, b64, canonical, digest, sign_jws, strict_loads, unb64,
)

ROOT = Path(__file__).resolve().parent.parent
NOW = 1000


def key(algorithm, level):
    if algorithm == 'ES256':
        return ec.generate_private_key(ec.SECP256R1())
    if algorithm == 'ES384':
        return ec.generate_private_key(ec.SECP384R1())
    return ed448.Ed448PrivateKey.generate() if level == 3 else ed25519.Ed25519PrivateKey.generate()


def seal(value, private, binding, level):
    value['signature'] = sign_jws(r.payload(value), private,
        key_id=binding.key_id, algorithm=binding.algorithm,
        purpose=binding.purpose, level=level)


def fixture(level=2, algorithm='EdDSA'):
    d = lambda label: digest({'test_only': label}, level)
    assessor_private, issuer_private = key(algorithm, level), key(algorithm, level)
    assessor = KeyBinding('assessor-key', 'assessor-1', algorithm,
                          READINESS_TYPE, assessor_private.public_key(), 'zone-1')
    issuer = KeyBinding('issuer-key', 'oracle-1', algorithm,
                        READINESS_DECISION_TYPE, issuer_private.public_key(), 'zone-1')
    subject = {'agent_id': 'agent-1', 'lineage_id': 'lineage-1',
               **{name + '_digest': d(name) for name in
                  ('software', 'model', 'configuration', 'toolchain', 'permissions')}}
    scope = {'zone_id': 'zone-1', 'resource_id': 'service-1',
             'environment_digest': d('environment'), 'parameters_digest': d('restart-bounds')}
    profile = {'profile_version': 'ktp-readiness-profile-v1', 'profile_id': 'service-readiness',
               'version': 2, 'conformance_level': level,
               'assessor_registry_digest': d('registry'), 'operations': [{
                   'operation_id': 'restart-service', 'scope': copy.deepcopy(scope),
                   'assessment_spec_digest': d('assessment-spec'), 'max_age_seconds': 300,
                   'required_checks': ['rollback', 'permission-check'],
                   'assessor_ids': ['assessor-1']}]}
    request = {'request_id': 'request-1', 'subject': copy.deepcopy(subject),
               'operation_id': 'restart-service', 'scope': copy.deepcopy(scope),
               'deployment_profile_digest': d('deployment'),
               'readiness_profile_digest': digest(profile, level)}
    challenge = {'challenge_id': 'challenge-1', 'nonce': b64(bytes(range(32))), 'issued_at': 900}
    attestation = {'attestation_version': 'ktp-readiness-attestation-v1',
        'attestation_id': 'assessment-1', 'subject': subject,
        'deployment_profile_digest': d('deployment'),
        'readiness_profile_digest': digest(profile, level), 'readiness_epoch': 3,
        'operation_id': 'restart-service', 'scope': scope, 'challenge': challenge,
        'assessment_spec_digest': d('assessment-spec'), 'checks': [
            {'check_id': 'rollback', 'observed_at': 920, 'evidence_digest': d('rollback-result')},
            {'check_id': 'permission-check', 'observed_at': 930, 'evidence_digest': d('permission-result')}],
        'assessed_at': 940, 'issued_at': 945, 'expires_at': 1220,
        'assessor_id': 'assessor-1', 'outcome': 'passed'}
    seal(attestation, assessor_private, assessor, level)
    state = r.TrustedState(profile['profile_id'], digest(profile, level), d('deployment'),
        d('registry'), 2, 3, digest(attestation, level), copy.deepcopy(challenge),
        NOW, 'active', 800, 2000, 800, 2000)
    # Opaque signed fixture for the external ordinary-proof verifier boundary.
    external_key = ed25519.Ed25519PrivateKey.generate()
    proof_body = {'iat': 998, 'exp': 1008, 'request_digest': r.request_digest(request, level)}
    head = {'alg': 'EdDSA', 'kid': 'external-proof-fixture', 'typ': 'JWT'}
    signing = b64(canonical(head)) + '.' + b64(canonical(proof_body))
    signature = external_key.sign(signing.encode('ascii'))
    external_key.public_key().verify(signature, signing.encode('ascii'))
    token = signing + '.' + b64(signature)
    proof = r.VerifiedOrdinaryProof(token, r.request_digest(request, level), 998, 1008)
    evidence = r.verify_readiness(attestation, profile, request, state=state,
                                  assessor=assessor, now=NOW, level=level)
    decision = r.decision_body(evidence, proof, issuer_id='oracle-1',
                               issuer_valid_until=state.issuer_valid_until, now=NOW, level=level)
    seal(decision, issuer_private, issuer, level)
    return dict(level=level, profile=profile, request=request, attestation=attestation,
                state=state, assessor=assessor, issuer=issuer, proof=proof,
                decision=decision, assessor_private=assessor_private, issuer_private=issuer_private)


def readiness(f, now=NOW):
    return r.verify_readiness(f['attestation'], f['profile'], f['request'],
                              state=f['state'], assessor=f['assessor'], now=now, level=f['level'])


def decision(f, now=NOW):
    return r.verify_decision(f['decision'], f['attestation'], f['profile'], f['request'], f['proof'],
        state=f['state'], assessor=f['assessor'], issuer=f['issuer'], now=now, level=f['level'])


def reseal_attestation(f):
    seal(f['attestation'], f['assessor_private'], f['assessor'], f['level'])
    f['state'] = replace(f['state'], active_attestation_digest=digest(f['attestation'], f['level']))


def leaves(value, prefix=()):
    if isinstance(value, dict):
        for name, child in value.items():
            yield from leaves(child, prefix + (name,))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            yield from leaves(child, prefix + (i,))
    else:
        yield prefix


def mutate(value, path):
    target = value
    for member in path[:-1]:
        target = target[member]
    old = target[path[-1]]
    target[path[-1]] = old + 1 if type(old) is int else old + '-tampered'


class ReadinessTests(unittest.TestCase):
    def setUp(self):
        self.f = fixture()

    def test_schemas_are_valid_and_fixture_passes(self):
        for kind, validator in r.VALIDATORS.items():
            Draft202012Validator.check_schema(validator.schema)
            self.assertTrue(validator.is_valid(self.f[kind]))
        result = decision(self.f)
        self.assertEqual(result.request_digest, r.request_digest(self.f['request'], 2))
        self.assertFalse(hasattr(result, 'standing'))
        self.assertFalse(hasattr(result, 'allow'))

    def test_supported_algorithms_and_levels(self):
        for level, alg in ((1, 'EdDSA'), (1, 'ES256'), (1, 'ES384'),
                           (2, 'EdDSA'), (2, 'ES256'), (2, 'ES384'),
                           (3, 'EdDSA'), (3, 'ES384')):
            with self.subTest(level=level, algorithm=alg):
                decision(fixture(level, alg))

    def test_every_attestation_leaf_is_authenticated(self):
        for path in leaves(r.payload(self.f['attestation'])):
            f = fixture()
            mutate(f['attestation'], path)
            # Recompute the storage digest to isolate signature and semantic checks.
            f['state'] = replace(f['state'], active_attestation_digest=digest(f['attestation'], 2))
            with self.subTest(path=path), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_every_decision_leaf_is_authenticated(self):
        for path in leaves(r.payload(self.f['decision'])):
            f = fixture()
            mutate(f['decision'], path)
            with self.subTest(path=path), self.assertRaises(InvalidRecord):
                decision(f)

    def test_corrupt_signatures_fail_even_with_recomputed_storage_digest(self):
        for target in ('attestation', 'decision'):
            f = fixture()
            parts = f[target]['signature'].split('.')
            signature = bytearray(unb64(parts[2]))
            signature[0] ^= 1
            parts[2] = b64(bytes(signature))
            f[target]['signature'] = '.'.join(parts)
            if target == 'attestation':
                f['state'] = replace(f['state'], active_attestation_digest=digest(f[target], 2))
            with self.subTest(target=target), self.assertRaises(InvalidRecord):
                decision(f)

    def test_trajectory_signatures_cover_complete_readiness_sidecar(self):
        # This exercises signed carrier coverage, not complete execution/lineage
        # conformance between the two independent test fixture contexts.
        module_spec = importlib.util.spec_from_file_location(
            'trajectory_fixture_helpers', ROOT/'scripts/test-trajectory-signatures.py')
        fixtures = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(fixtures)
        record = fixtures.unsigned_record()
        record['action']['details']['readiness'] = copy.deepcopy(self.f['decision'])
        signed = fixtures.sign_record(record)
        fixtures.verify(signed)
        signed['action']['details']['readiness']['expires_at'] += 1
        signed['record_hash'] = fixtures.TS.record_digest(signed)
        with self.assertRaises(InvalidRecord):
            fixtures.verify(signed)
        signed = fixtures.sign_record(record)
        for purpose in (READINESS_TYPE, READINESS_DECISION_TYPE):
            with self.subTest(purpose=purpose), self.assertRaises(InvalidRecord):
                fixtures.TS.verify_record(signed,
                    replace(fixtures.binding('Ed25519', 'agent'), purpose=purpose),
                    fixtures.binding('Ed25519', 'oracle'), **fixtures.trusted_context())

    def test_lifecycle_requirements_have_unique_ids_and_explicit_scope(self):
        suite = json.loads((ROOT/'specifications/conformance/readiness-lifecycle-v1.json').read_text())
        self.assertEqual('normative-downstream-runtime-requirements', suite['kind'])
        ids = [case['id'] for case in suite['vectors']]
        self.assertEqual(len(ids), len(set(ids)))
        for case in suite['vectors']:
            self.assertEqual({'id', 'given', 'when', 'expected'}, set(case))
            self.assertTrue(all(type(value) is str and value for value in case.values()))

    def test_all_request_configuration_and_scope_substitutions_fail(self):
        for path in leaves(self.f['request']):
            f = fixture()
            mutate(f['request'], path)
            with self.subTest(path=path), self.assertRaises(InvalidRecord):
                decision(f)

    def test_unmapped_operation_does_not_skip_readiness(self):
        f = self.f
        f['request']['operation_id'] = f['attestation']['operation_id'] = 'delete-database'
        reseal_attestation(f)
        with self.assertRaises(InvalidRecord):
            readiness(f)

    def test_assessment_expiration_boundary(self):
        f = self.f
        f['state'] = replace(f['state'], checked_at=1219)
        readiness(f, 1219)
        f['state'] = replace(f['state'], checked_at=1220)
        with self.assertRaises(InvalidRecord):
            readiness(f, 1220)

    def test_fresh_signature_does_not_refresh_old_assessment(self):
        f = self.f
        f['attestation']['issued_at'] = 1219
        f['attestation']['expires_at'] = 1519
        reseal_attestation(f)
        f['state'] = replace(f['state'], checked_at=1220)
        with self.assertRaises(InvalidRecord):
            readiness(f, 1220)

    def test_oldest_required_check_controls_expiration(self):
        f = self.f
        f['attestation']['expires_at'] = 1221
        reseal_attestation(f)
        with self.assertRaises(InvalidRecord):
            readiness(f)

    def test_challenge_issuance_observation_and_completion_order(self):
        mutations = [('issued_at', 1001), ('assessed_at', 925), ('issued_at', 939)]
        for field, value in mutations:
            f = fixture()
            f['attestation'][field] = value
            reseal_attestation(f)
            with self.subTest(field=field, value=value), self.assertRaises(InvalidRecord):
                readiness(f)
        f = fixture()
        f['attestation']['checks'][0]['observed_at'] = 899
        reseal_attestation(f)
        with self.assertRaises(InvalidRecord):
            readiness(f)

    def test_challenge_binding_and_encoding_failures(self):
        for nonce in (b64(bytes(reversed(range(32)))), b64(bytes(range(31))),
                      b64(bytes(range(32))) + '='):
            f = fixture()
            f['attestation']['challenge']['nonce'] = nonce
            reseal_attestation(f)
            with self.subTest(nonce=nonce), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_missing_duplicate_and_unrequired_checks_fail(self):
        for kind in ('missing', 'duplicate', 'unrequired'):
            f = fixture()
            checks = f['attestation']['checks']
            if kind == 'missing': checks.pop()
            elif kind == 'duplicate': checks.append(copy.deepcopy(checks[0]))
            else: checks[0]['check_id'] = 'heartbeat'
            reseal_attestation(f)
            with self.subTest(kind=kind), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_failed_and_inconclusive_assessments_cannot_be_certificates(self):
        for outcome in ('failed', 'inconclusive', 'unknown', None, True):
            f = fixture()
            f['attestation']['outcome'] = outcome
            reseal_attestation(f)
            with self.subTest(outcome=outcome), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_assessor_role_zone_identity_and_key_must_match(self):
        for field, value in (('purpose', READINESS_DECISION_TYPE), ('purpose', AGENT_TYPE),
                             ('zone_id', 'zone-2'), ('subject', 'self-appointed-assessor'),
                             ('public_key', ed25519.Ed25519PrivateKey.generate().public_key())):
            f = fixture()
            f['assessor'] = replace(f['assessor'], **{field: value})
            with self.subTest(field=field), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_current_restrictions_win_over_unexpired_evidence(self):
        for status in ('revoked', 'suspended', 'unestablished', 'unknown', 'unavailable', None, True):
            f = fixture()
            f['state'] = replace(f['state'], status=status)
            with self.subTest(status=status), self.assertRaises(InvalidRecord):
                decision(f)

    def test_current_status_cannot_be_cached_or_future_dated(self):
        for at in (NOW-1, NOW+1, None, True, float(NOW)):
            f = fixture()
            f['state'] = replace(f['state'], checked_at=at)
            with self.subTest(at=at), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_stale_epoch_profile_floor_and_active_digest_fail(self):
        for changes in ({'readiness_epoch': 4}, {'minimum_profile_version': 3},
                        {'active_attestation_digest': digest({'old': 'history'}, 2)}):
            f = fixture()
            f['state'] = replace(f['state'], **changes)
            with self.subTest(changes=changes), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_profile_or_registry_substitution_fails(self):
        for field in ('profile_digest', 'deployment_profile_digest', 'assessor_registry_digest'):
            f = fixture()
            f['state'] = replace(f['state'], **{field: digest({'substitute': field}, 2)})
            with self.subTest(field=field), self.assertRaises(InvalidRecord):
                readiness(f)
        f = fixture()
        f['profile']['operations'][0]['max_age_seconds'] *= 100
        with self.assertRaises(InvalidRecord):
            readiness(f)

    def test_key_expiration_limits_assessment_and_decision(self):
        for changes in ({'assessor_valid_until': NOW}, {'assessor_valid_until': 1219},
                        {'issuer_valid_until': NOW}, {'issuer_valid_until': 1007},
                        {'assessor_valid_from': 946}, {'issuer_valid_from': 1001}):
            f = fixture()
            f['state'] = replace(f['state'], **changes)
            with self.subTest(changes=changes), self.assertRaises(InvalidRecord):
                decision(f)

    def test_proof_cannot_outlive_readiness_even_with_shorter_sidecar(self):
        f = self.f
        f['attestation']['expires_at'] = 1005
        reseal_attestation(f)
        evidence = readiness(f)
        with self.assertRaises(InvalidRecord):
            r.decision_body(evidence, f['proof'], issuer_id='oracle-1',
                             issuer_valid_until=2000, now=NOW, level=2)
        f['decision']['attestation_digest'] = digest(f['attestation'], 2)
        f['decision']['expires_at'] = 1005
        seal(f['decision'], f['issuer_private'], f['issuer'], 2)
        with self.assertRaises(InvalidRecord):
            decision(f)

    def test_ordinary_proof_expiry_and_ten_second_maximum(self):
        for iat, exp in ((998, 1009), (1001, 1008), (998, NOW), (998, 998), (998, 997)):
            f = fixture()
            f['proof'] = replace(f['proof'], issued_at=iat, expires_at=exp)
            with self.subTest(iat=iat, exp=exp), self.assertRaises(InvalidRecord):
                decision(f)
        f = fixture()
        f['state'] = replace(f['state'], checked_at=1008)
        with self.assertRaises(InvalidRecord):
            decision(f, 1008)

    def test_ordinary_proof_bytes_and_request_are_bound(self):
        for changes in ({'token': self.f['proof'].token + 'A'},
                        {'request_digest': digest({'different': 'request'}, 2)}):
            f = fixture()
            f['proof'] = replace(f['proof'], **changes)
            with self.subTest(changes=changes), self.assertRaises(InvalidRecord):
                decision(f)

    def test_decision_cannot_extend_or_predate_proof(self):
        for field, value in (('expires_at', 1009), ('evaluated_at', 997),
                             ('evaluated_at', 1001), ('expires_at', NOW)):
            f = fixture()
            f['decision'][field] = value
            seal(f['decision'], f['issuer_private'], f['issuer'], 2)
            with self.subTest(field=field, value=value), self.assertRaises(InvalidRecord):
                decision(f)

    def test_decision_issuer_role_and_zone_are_separate(self):
        for field, value in (('purpose', READINESS_TYPE), ('subject', 'assessor-1'),
                             ('zone_id', 'zone-2')):
            f = fixture()
            f['issuer'] = replace(f['issuer'], **{field: value})
            with self.subTest(field=field), self.assertRaises(InvalidRecord):
                decision(f)

    def test_float_boolean_unsafe_and_nonfinite_controls_fail(self):
        for value in (True, 2.0, 0, -1, 2**53, float('nan'), float('inf')):
            f = fixture()
            f['profile']['version'] = value
            with self.subTest(value=value), self.assertRaises(InvalidRecord):
                readiness(f)
        for field in ('assessed_at', 'issued_at', 'expires_at', 'readiness_epoch'):
            f = fixture()
            f['attestation'][field] = float(f['attestation'][field])
            with self.subTest(field=field), self.assertRaises(InvalidRecord):
                readiness(f)

    def test_unknown_fields_at_all_object_levels_fail(self):
        paths = [('profile',), ('profile','operations',0), ('profile','operations',0,'scope'),
                 ('attestation',), ('attestation','subject'), ('attestation','scope'),
                 ('attestation','challenge'), ('attestation','checks',0), ('decision',)]
        for path in paths:
            f = fixture()
            target = f
            for part in path: target = target[part]
            target['extra'] = 'unsigned-extension'
            with self.subTest(path=path), self.assertRaises(InvalidRecord):
                decision(f)

    def test_level_three_rejects_digest_and_key_downgrades(self):
        f = fixture(3)
        f['attestation']['checks'][0]['evidence_digest'] = digest({'weak': 'digest'}, 2)
        reseal_attestation(f)
        with self.assertRaises(InvalidRecord): readiness(f)
        f = fixture(3)
        f['assessor'] = replace(f['assessor'], public_key=ed25519.Ed25519PrivateKey.generate().public_key())
        with self.assertRaises(InvalidRecord): readiness(f)

    def test_duplicate_operation_definitions_fail(self):
        f = self.f
        f['profile']['operations'].append(copy.deepcopy(f['profile']['operations'][0]))
        with self.assertRaises(InvalidRecord): readiness(f)

    def test_duplicate_json_and_unrepresentable_values_fail(self):
        for raw in ('{"expires_at":1,"expires_at":2}', '{"x":NaN}', '{"x":9007199254740992}'):
            with self.subTest(raw=raw), self.assertRaises(InvalidRecord): strict_loads(raw)

    def test_repeated_verification_does_not_modify_evidence_or_profiles(self):
        f = self.f
        before = {name: canonical(f[name]) for name in ('attestation','profile','decision','request')}
        first = decision(f)
        for _ in range(3): self.assertEqual(first, decision(f))
        for name, data in before.items(): self.assertEqual(data, canonical(f[name]))

    def test_readiness_never_lowers_existing_supervision(self):
        f = self.f
        args = (f['decision'], f['attestation'], f['profile'], f['request'], f['proof'])
        kwargs = dict(state=f['state'], assessor=f['assessor'], issuer=f['issuer'], now=NOW, level=2)
        for prior in sorted(r.SUPERVISION):
            self.assertEqual(prior, r.restrict_decision(prior, *args, **kwargs))
        kwargs['state'] = replace(f['state'], status='revoked')
        for prior in sorted(r.SUPERVISION):
            self.assertEqual('silent_veto', r.restrict_decision(prior, *args, **kwargs))

    def test_migration_and_legacy_profile_are_explicit(self):
        legacy = (ROOT/'schemas/deployment-profile-legacy-v2.json').read_bytes()
        self.assertEqual(hashlib.sha256(legacy).hexdigest(),
                         'c0087dc3662b8ef1988f7d612a779ca38f2b771454a45fc33abaaed6f2ebb3f2')
        original = json.loads(legacy)
        self.assertTrue(original['$id'].endswith('/v2/deployment-profile.json'))
        active = json.loads((ROOT/'schemas/deployment-profile.json').read_text())
        self.assertTrue(active['$id'].endswith('/v3/deployment-profile.json'))
        module_spec = importlib.util.spec_from_file_location('readiness_declarations', ROOT/'scripts/check-declarations.py')
        checker = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(checker)
        validator = Draft202012Validator(active)
        self.assertEqual([], checker.check(copy.deepcopy(checker.EXAMPLE)))
        self.assertTrue(validator.is_valid(checker.EXAMPLE))
        for mode in ('missing', 'legacy', 'both', 'null', 'bad-version', 'unknown-field'):
            p = copy.deepcopy(checker.EXAMPLE)
            if mode in ('missing','legacy'): p.pop('standing_policy')
            if mode in ('legacy','both'): p['standing_decay_rate'] = 16
            if mode == 'null': p['standing_policy'] = None
            if mode == 'bad-version': p['standing_policy']['version'] = True
            if mode == 'unknown-field': p['standing_policy']['override'] = True
            with self.subTest(mode=mode):
                self.assertTrue(checker.check(p))
                self.assertFalse(validator.is_valid(p))

    def test_decision_construction_requires_current_verification(self):
        evidence = readiness(self.f)
        with self.assertRaises(InvalidRecord):
            r.decision_body(evidence, self.f['proof'], issuer_id='oracle-1',
                             issuer_valid_until=2000, now=NOW+1, level=2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
