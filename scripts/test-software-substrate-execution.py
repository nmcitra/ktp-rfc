#!/usr/bin/env python3
"""Regression gate for software-substrate decision schema vectors.

This validates fixture integrity, synthetic signatures and JSON shape. It does
not execute an authorizer or establish a provider or target effect.
"""

import copy
import base64
import hashlib

import rfc8785
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads(
    (ROOT / "schemas/software-substrate-decision.json").read_text())
SUITE = json.loads(
    (ROOT / "specifications/conformance/software-substrate-execution-v1.json")
    .read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def apply_mutation(value, mutation):
    """Apply one isolated schema-vector mutation to a JSON-compatible value."""
    target = value
    for member in mutation["path"][:-1]:
        target = target[member]
    leaf = mutation["path"][-1]
    if mutation["operation"] == "set":
        target[leaf] = mutation["value"]
    else:
        del target[leaf]


class SoftwareSubstrateExecutionTests(unittest.TestCase):
    def test_capacity_input_pairs_are_isolated(self):
        vectors = {v["id"]: v for v in SUITE["vectors"]}
        self.assertEqual(len(vectors), 53)
        self.assertEqual(len(vectors), len(SUITE["vectors"]))
        baseline = vectors["S01-current-bound-action"]
        for name, field in (
            ("S37-repair-capacity-monotonic", "repairPathVerified"),
            ("S38-supervision-capacity-monotonic", "supervisionAvailable"),
        ):
            with self.subTest(vector=name):
                pair = vectors[name]
                expected_request = copy.deepcopy(baseline["request"])
                conditions = expected_request["softwareContext"]["conditions"]
                self.assertIs(conditions[field], True)
                conditions[field] = False
                expected_request["softwareContext"]["candidateEnvelope"]["environmentalCapacity"] = 0.8
                self.assertEqual(pair["request"], expected_request)
                self.assertEqual(pair["expect"]["compareTo"], baseline["id"])
                self.assertEqual(pair["expect"]["decisionNotLooserThan"], "allow")
                self.assertIs(pair["expect"]["environmentalCapacityNotGreaterThanCompared"], True)

    def test_real_signature_and_binding_fixtures(self):
        key = serialization.load_pem_public_key(SUITE["fixturePublicKeyPem"].encode())
        order = int("ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551", 16)

        def verify(jws, expected_type):
            h, p, signature = jws.split(".")
            def decode(value):
                raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
                self.assertEqual(base64.urlsafe_b64encode(raw).rstrip(b"=").decode(), value)
                return raw
            header = {"alg": "ES256", "kid": "fixture-only", "typ": expected_type}
            self.assertEqual(decode(h), rfc8785.dumps(header))
            raw = decode(signature)
            self.assertEqual(len(raw), 64)
            r, s = int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")
            self.assertTrue(0 < s <= order // 2)
            key.verify(utils.encode_dss_signature(r, s), (h + "." + p).encode(), ec.ECDSA(hashes.SHA256()))
            payload_bytes = decode(p)
            payload = json.loads(payload_bytes)
            self.assertEqual(payload_bytes, rfc8785.dumps(payload))
            return payload

        digest = lambda value: "sha256:" + hashlib.sha256(value).hexdigest()
        cases = [v for v in SUITE["vectors"] if v.get("stage") == "signature_binding"]
        self.assertEqual(len(cases), 5)
        self.assertTrue(any(v["expect"]["decision"] == "allow" for v in cases))
        for vector in cases:
            with self.subTest(vector=vector["id"]):
                inputs = vector["request"]["softwareContext"]["cryptographicInputs"]
                verify(inputs["ordinaryProof"], "test-ordinary-proof")
                actual = {"proofSignatureValid": True}
                try:
                    decision = verify(inputs["signedDecision"], "ktp-software-substrate-decision-v1")
                    actual["decisionSignatureValid"] = True
                except InvalidSignature:
                    actual["decisionSignatureValid"] = False
                if actual["decisionSignatureValid"]:
                    actual["requestBindingMatches"] = decision["request_digest"] == digest(rfc8785.dumps(inputs["actualRequestBinding"]))
                    actual["proofDigestMatches"] = decision["proof_digest"] == digest(inputs["ordinaryProof"].encode("ascii"))
                self.assertEqual(actual, vector["expect"]["cryptographicChecks"])

    def test_independent_freshness_and_expiry_checks(self):
        for vector in SUITE["vectors"]:
            c = vector["request"]["softwareContext"]
            expect = vector["expect"]
            with self.subTest(vector=vector["id"]):
                if "observationFresh" in expect:
                    fresh = c["observedAtMs"] <= c["nowMs"] < c["observedAtMs"] + c["maxAgeMs"]
                    self.assertEqual(fresh, expect["observationFresh"])
                if "decisionUnexpired" in expect:
                    self.assertEqual(c["nowMs"] < c["decisionExpiresAtMs"], expect["decisionUnexpired"])
                if vector.get("stage") == "observation_freshness":
                    self.assertNotIn("decisionExpiresAtMs", c)
                    self.assertNotIn("decision", expect)

    def test_wire_times_and_review_controls(self):
        vectors = {v["id"][:3]: v for v in SUITE["vectors"]}
        for vector in vectors.values():
            c = vector["request"]["softwareContext"]
            for field in ("nowMs", "observedAtMs", "maxAgeMs", "proofIssuedAtMs", "proofExpiresAtMs", "decisionExpiresAtMs"):
                if field in c:
                    self.assertEqual(c[field] % 1000, 0, (vector["id"], field))
        stable = vectors["S36"]
        self.assertFalse(stable["request"]["softwareContext"]["conditions"]["supervisionAvailable"])
        self.assertEqual(stable["expect"]["decision"], "allow")
        veto = vectors["S42"]
        self.assertFalse(veto["request"]["softwareContext"]["conditions"]["supervisionAvailable"])
        self.assertEqual(veto["expect"]["supervision"], "silent_veto")
        self.assertEqual(vectors["S35"]["expect"]["decision"], "deny")
        self.assertEqual(vectors["S40"]["expect"]["decision"], "allow")

    def test_schema_definition(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_schema_vectors(self):
        for vector in SUITE["schemaVectors"]:
            with self.subTest(vector=vector["id"]):
                candidate = copy.deepcopy(SUITE["schemaFixture"])
                if "mutation" in vector:
                    apply_mutation(candidate, vector["mutation"])
                for mutation in vector.get("mutations", []):
                    apply_mutation(candidate, mutation)
                actual = VALIDATOR.is_valid(candidate)
                expected = vector["expect"]["schemaValid"]
                self.assertEqual(actual, expected, vector["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
