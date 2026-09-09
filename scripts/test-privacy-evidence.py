#!/usr/bin/env python3
"""Real AEAD/signature tests; not evidence that deployed copies were erased."""
import copy
from dataclasses import replace
import unittest

from cryptography.hazmat.primitives.asymmetric import ec, ed25519, ed448

import privacy_evidence as p
from trajectory_signatures import (
    AGENT_TYPE, InvalidRecord, KeyBinding, PRIVACY_EVIDENCE_TYPE,
    b64, canonical, digest, sign_jws, verify_jws,
)


def fixture(level=2, algorithm='EdDSA'):
    if algorithm == 'ES256':
        signer = ec.generate_private_key(ec.SECP256R1())
    elif algorithm == 'ES384':
        signer = ec.generate_private_key(ec.SECP384R1())
    else:
        signer = ed448.Ed448PrivateKey.generate() if level == 3 else ed25519.Ed25519PrivateKey.generate()
    binding = KeyBinding('archive-key', 'archive-issuer', algorithm,
                         PRIVACY_EVIDENCE_TYPE, signer.public_key(), 'zone-1')
    meta = {'envelope_id': 'opaque-entry-1', 'zone_id': 'zone-1', 'chain_id': 'archive-1',
            'sequence': 1, 'previous_hash': None, 'purpose_id': 'authorization-review',
            'privacy_policy_digest': digest({'policy': 'bounded-review'}, level),
            'created_at': 100, 'delete_after': 200, 'issuer_id': 'archive-issuer'}
    # Deliberately preserve noncanonical whitespace and UTF-8 bytes, like an
    # original signed artifact whose exact representation must not be rewritten.
    original = b'{ "subject" : "Alice", "evidence" : "caf\xc3\xa9" }\n'
    envelope, key = p.seal_evidence(original, meta, signer, key_id=binding.key_id,
                                  algorithm=algorithm, level=level)
    expected = p.ExpectedEnvelope('zone-1', 'archive-1', 1, None, envelope['record_hash'],
        'authorization-review', meta['privacy_policy_digest'], 'archive-issuer', level, 50, 150)
    return envelope, key, binding, expected, original, signer, meta


def resign(envelope, signer, binding, level):
    envelope['signature'] = sign_jws(p.body(envelope), signer, key_id=binding.key_id,
        algorithm=binding.algorithm, purpose=binding.purpose, level=level)
    envelope['record_hash'] = p.record_digest(envelope, level)


class PrivacyEvidenceTests(unittest.TestCase):
    def test_original_real_signature_survives_exact_encrypted_roundtrip(self):
        _, _, binding, expected, _, signer, meta = fixture()
        inner_signer = ed25519.Ed25519PrivateKey.generate()
        inner_binding = KeyBinding('original-key', 'original-agent', 'EdDSA',
                                   AGENT_TYPE, inner_signer.public_key(), 'zone-1')
        original_body = {'subject': 'Alice', 'claim': 'qualification-association'}
        # A real typed inner signature proves byte preservation here; this is
        # not a full trajectory fixture or a claim that this assertion is true.
        original = sign_jws(original_body, inner_signer, key_id='original-key',
                           algorithm='EdDSA', purpose=AGENT_TYPE, level=2)
        envelope, key = p.seal_evidence(original.encode('ascii'), meta, signer,
            key_id=binding.key_id, algorithm=binding.algorithm, level=2)
        expected = replace(expected, record_hash=envelope['record_hash'])
        recovered = p.open_evidence(envelope, key, binding, expected, now=110)
        self.assertEqual(recovered, original.encode('ascii'))
        verify_jws(recovered.decode('ascii'), original_body, inner_binding, level=2)
        with self.assertRaises(InvalidRecord):
            verify_jws(recovered.decode('ascii'), dict(original_body, subject='Bob'),
                       inner_binding, level=2)

    def test_real_aead_and_supported_signatures_roundtrip_exact_bytes(self):
        for level, algorithm in [(1, 'ES256'), (1, 'ES384'), (1, 'EdDSA'),
                                  (2, 'ES256'), (2, 'ES384'), (2, 'EdDSA'),
                                  (3, 'ES384'), (3, 'EdDSA')]:
            with self.subTest(level=level, algorithm=algorithm):
                e, k, b, x, original, *_ = fixture(level, algorithm)
                self.assertEqual(p.open_evidence(e, k, b, x, now=110), original)
                self.assertNotIn(b'Alice', canonical(e))

    def test_new_seal_uses_new_data_key_nonce_and_reference(self):
        e, key, b, x, raw, private, meta = fixture()
        second, other = p.seal_evidence(raw, meta, private, key_id=b.key_id,
                                       algorithm=b.algorithm, level=2)
        self.assertNotEqual(key, other)
        for field in ('key_ref', 'nonce', 'ciphertext'):
            self.assertNotEqual(e['encryption'][field], second['encryption'][field])

    def test_outer_integrity_remains_verifiable_without_plaintext_key(self):
        e, _, b, x, *_ = fixture()
        self.assertEqual(p.verify_envelope(e, b, x, now=110), 'outer_integrity_only')
        with self.assertRaises(InvalidRecord):
            p.open_evidence(e, None, b, x, now=110)

    def test_wrong_subject_compartment_key_cannot_decrypt(self):
        e, _, b, x, *_ = fixture()
        _, other, *_ = fixture()
        with self.assertRaises(InvalidRecord):
            p.open_evidence(e, other, b, x, now=110)

    def test_every_header_and_ciphertext_mutation_rejected(self):
        e, _, b, x, *_ = fixture()
        for field in p.body(e):
            candidate = copy.deepcopy(e)
            if field == 'encryption':
                candidate[field]['ciphertext'] = b64(b'changed-ciphertext-with-tag')
            elif field == 'previous_hash':
                candidate[field] = digest({'other': True}, 2)
            elif type(candidate[field]) is int:
                candidate[field] += 1
            else:
                candidate[field] += '-changed'
            with self.subTest(field=field), self.assertRaises(InvalidRecord):
                p.verify_envelope(candidate, b, x, now=110)

    def test_plaintext_redaction_cannot_replace_ciphertext(self):
        e, _, b, x, *_ = fixture()
        e['encryption']['ciphertext'] = b64(b'[REDACTED] and imaginary authentication tag')
        with self.assertRaises(InvalidRecord):
            p.verify_envelope(e, b, x, now=110)

    def test_recomputed_outer_hash_does_not_repair_signature(self):
        e, _, b, x, *_ = fixture()
        e['encryption']['key_ref'] = 'other-key'
        e['record_hash'] = p.record_digest(e, 2)
        with self.assertRaises(InvalidRecord):
            p.verify_envelope(e, b, replace(x, record_hash=e['record_hash']), now=110)

    def test_resigning_changed_purpose_does_not_repair_aead_binding(self):
        e, k, b, x, _, private, _ = fixture()
        e['purpose_id'] = 'employee-ranking'
        resign(e, private, b, 2)
        x = replace(x, purpose_id=e['purpose_id'], record_hash=e['record_hash'])
        self.assertEqual(p.verify_envelope(e, b, x, now=110), 'outer_integrity_only')
        with self.assertRaises(InvalidRecord):
            p.open_evidence(e, k, b, x, now=110)

    def test_role_zone_and_issuer_substitution_rejected(self):
        e, _, b, x, *_ = fixture()
        for changed in (replace(b, purpose=AGENT_TYPE), replace(b, zone_id='other-zone'),
                        replace(b, subject='other-issuer')):
            with self.subTest(binding=changed), self.assertRaises(InvalidRecord):
                p.verify_envelope(e, changed, x, now=110)

    def test_reanchoring_without_trusted_anchor_rejected(self):
        e, _, b, x, _, signer, _ = fixture()
        e['chain_id'] = 'new-clean-history'
        resign(e, signer, b, 2)
        with self.assertRaises(InvalidRecord):
            p.verify_envelope(e, b, x, now=110)

    def test_retention_boundary_does_not_grant_decryption(self):
        e, k, b, x, raw, *_ = fixture()
        self.assertEqual(p.open_evidence(e, k, b, x, now=199), raw)
        with self.assertRaises(InvalidRecord):
            p.open_evidence(e, k, b, x, now=200)
        self.assertEqual(p.verify_envelope(e, b, x, now=200), 'outer_integrity_only')

    def test_invalid_creation_and_key_validity_rejected(self):
        e, _, b, x, *_ = fixture()
        for at, expected in ((99, x), (110, replace(x, key_valid_from=101)),
                             (110, replace(x, key_valid_until=100))):
            with self.subTest(at=at), self.assertRaises(InvalidRecord):
                p.verify_envelope(e, b, expected, now=at)

    def test_unsafe_boolean_float_and_unknown_metadata_rejected(self):
        e, _, b, x, raw, private, meta = fixture()
        for bad in (True, 1.0, 2**53):
            candidate = dict(meta, sequence=bad)
            with self.subTest(value=bad), self.assertRaises(InvalidRecord):
                p.seal_evidence(raw, candidate, private, key_id=b.key_id, algorithm=b.algorithm, level=2)
        with self.assertRaises(InvalidRecord):
            p.seal_evidence(raw, dict(meta, name='Alice'), private, key_id=b.key_id, algorithm=b.algorithm, level=2)

    def test_genesis_and_predecessor_rules(self):
        e, _, b, x, raw, private, meta = fixture()
        with self.assertRaises(InvalidRecord):
            p.seal_evidence(raw, dict(meta, sequence=2), private, key_id=b.key_id, algorithm=b.algorithm, level=2)
        next_meta = dict(meta, sequence=2, previous_hash=e['record_hash'], envelope_id='entry-2')
        second, _ = p.seal_evidence(raw, next_meta, private, key_id=b.key_id, algorithm=b.algorithm, level=2)
        nx = replace(x, sequence=2, previous_hash=e['record_hash'], record_hash=second['record_hash'])
        self.assertEqual(p.verify_envelope(second, b, nx, now=110), 'outer_integrity_only')

    def test_level_three_cannot_use_weak_digest_or_signing_key(self):
        e, _, b, x, raw, private, meta = fixture(3)
        with self.assertRaises(InvalidRecord):
            p.seal_evidence(raw, dict(meta, privacy_policy_digest=digest({}, 2)), private,
                            key_id=b.key_id, algorithm=b.algorithm, level=3)
        with self.assertRaises(InvalidRecord):
            fixture(3, 'ES256')

    def test_truncated_tag_and_noncanonical_base64_rejected(self):
        e, _, b, x, *_ = fixture()
        for ciphertext in (b64(bytes(16)), e['encryption']['ciphertext'] + '='):
            bad = copy.deepcopy(e)
            bad['encryption']['ciphertext'] = ciphertext
            with self.assertRaises(InvalidRecord):
                p.verify_envelope(bad, b, x, now=110)


if __name__ == '__main__':
    unittest.main()
