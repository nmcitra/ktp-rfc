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
        self.assertEqual(len(vectors), 52)
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
        vectors = {v["id"][:3]: v for v in SUITE["vectors"]}
        def verify(jws):
            h, p, signature = jws.split(".")
            decode = lambda value: base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
            raw = decode(signature)
            der = utils.encode_dss_signature(int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
            key.verify(der, (h + "." + p).encode(), ec.ECDSA(hashes.SHA256()))
            return json.loads(decode(p))
        digest = lambda value: "sha256:" + hashlib.sha256(value).hexdigest()
        for name in ("S05", "S07", "S08", "S12"):
            with self.subTest(vector=name):
                c = vectors[name]["request"]["softwareContext"]
                inputs = c["cryptographicInputs"]
                verify(inputs["ordinaryProof"])
                if name == "S12":
                    with self.assertRaises(InvalidSignature):
                        verify(inputs["signedDecision"])
                    continue
                decision = verify(inputs["signedDecision"])
                request_matches = decision["request_digest"] == digest(rfc8785.dumps(inputs["actualRequestBinding"]))
                proof_matches = decision["proof_digest"] == digest(inputs["ordinaryProof"].encode("ascii"))
                self.assertEqual(request_matches, name == "S08")
                self.assertEqual(proof_matches, name != "S08")

    def test_wire_times_and_review_controls(self):
        vectors = {v["id"][:3]: v for v in SUITE["vectors"]}
        for vector in vectors.values():
            c = vector["request"]["softwareContext"]
            for field in ("nowMs", "observedAtMs", "maxAgeMs", "proofIssuedAtMs", "proofExpiresAtMs", "decisionExpiresAtMs"):
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
