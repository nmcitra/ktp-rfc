#!/usr/bin/env python3
"""Regression gate for consequential-action evidence schema vectors.

This checks fixture integrity, a synthetic signature, and schema shape. It does
not authorize an action, establish protected-path coverage, or prove a target
effect.
"""

import copy
import base64
import re

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
    (ROOT / "schemas/consequential-action-evidence.json").read_text())
SUITE = json.loads(
    (ROOT / "specifications/conformance/consequential-action-execution-v1.json")
    .read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def apply_mutation(value, mutation):
    """Apply one isolated schema-vector mutation to a JSON-compatible value."""
    operation = mutation["operation"]
    if operation not in {"set", "remove"}:
        raise ValueError(f"unsupported mutation operation: {operation}")
    target = value
    for member in mutation["path"][:-1]:
        target = target[member]
    leaf = mutation["path"][-1]
    if operation == "set":
        target[leaf] = mutation["value"]
    else:
        del target[leaf]


def verify_non_dispatch_fixture(request):
    """Check only this suite's synthetic observer contract, not a live source."""
    def decode(segment):
        if not re.fullmatch(r"[A-Za-z0-9_-]+", segment):
            raise ValueError("noncanonical base64url")
        value = base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4))
        if base64.urlsafe_b64encode(value).rstrip(b"=").decode() != segment:
            raise ValueError("noncanonical base64url")
        return value

    header, payload, signature = request["nonDispatchRecordJws"].split(".")
    observer = SUITE["nonDispatchFixtureObserver"]
    if decode(header) != rfc8785.dumps(observer["protectedHeader"]):
        raise ValueError("unexpected observer header")
    raw = decode(signature)
    if len(raw) != 64:
        raise ValueError("wrong ES256 signature length")
    r, scalar_s = int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")
    order = int("ffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551", 16)
    if not 0 < r < order or not 0 < scalar_s <= order // 2:
        raise ValueError("noncanonical ECDSA scalars")
    key = serialization.load_pem_public_key(SUITE["nonDispatchFixturePublicKeyPem"].encode())
    key.verify(utils.encode_dss_signature(r, scalar_s),
               (header + "." + payload).encode(), ec.ECDSA(hashes.SHA256()))
    record = request["nonDispatchRecord"]
    if decode(payload) != rfc8785.dumps(record):
        raise ValueError("record/payload mismatch")
    expected = {
        "source_id": observer["sourceId"],
        "statement": "no_dispatch",
        "request_id": request["requestId"],
        "protected_path_coverage": request["protectedPath"],
        "interval_start": request["intervalStart"],
        "interval_end": request["intervalEnd"],
    }
    if record != expected:
        raise ValueError("non-dispatch binding mismatch")
    return record


class ConsequentialActionEvidenceTests(unittest.TestCase):
    def test_contract_fixture_integrity(self):
        vectors = SUITE["vectors"]
        self.assertTrue(vectors)
        self.assertEqual(len(vectors), len({v["id"] for v in vectors}))
        required = {"allow", "expired_queue", "scope_change", "destination_change",
                    "target_version_change", "same_id_replay", "same_id_changed_body",
                    "shared_budget", "recorder_failure", "crash_before_dispatch",
                    "crash_after_dispatch", "lost_reply", "unknown_effect", "restart"}
        self.assertTrue(required <= {v["case"] for v in vectors})
        for vector in vectors:
            with self.subTest(vector=vector["id"]):
                self.assertIsInstance(vector["request"], dict)
                self.assertTrue(vector["request"])
                self.assertIsInstance(vector["expect"], dict)
                self.assertTrue(vector["expect"])

    def test_non_dispatch_fixture_signature_and_binding_controls(self):
        vectors = {v["id"]: v for v in SUITE["vectors"]}
        verify_non_dispatch_fixture(vectors["E17"]["request"])
        for name in ("E28", "E29"):
            with self.subTest(vector=name):
                with self.assertRaises((ValueError, InvalidSignature)):
                    verify_non_dispatch_fixture(vectors[name]["request"])
                self.assertEqual(vectors[name]["expect"]["evidenceState"], "unknown")

    def test_evidence_expectations_have_authentication_inputs(self):
        for vector in SUITE["vectors"]:
            with self.subTest(vector=vector["id"]):
                request = {**SUITE["requestBaseline"], **vector["request"]}
                state = vector["expect"].get("evidenceState")
                if state == "dispatched":
                    self.assertTrue(request["dispatchAuthenticated"])
                elif state == "withheld":
                    if "nonDispatchRecordJws" in request:
                        verify_non_dispatch_fixture(request)
                    else:
                        self.assertTrue(request["nonDispatchAuthenticated"])
                elif state == "effect_confirmed":
                    self.assertTrue(request["targetEffectAuthenticated"])
                elif state == "no_effect":
                    self.assertTrue(request["dispatchAuthenticated"])
                    self.assertTrue(request["targetNoEffectAuthenticated"])

    def test_second_request_fits_an_exact_authenticated_remainder(self):
        request = next(v["request"] for v in SUITE["vectors"] if v["id"] == "E27")
        self.assertEqual(request["authenticatedRemainingBudgetUnits"],
                         request["scopeLimit"] - request["firstReservation"])
        self.assertLessEqual(request["secondConservativeReservation"],
                             request["authenticatedRemainingBudgetUnits"])
        self.assertGreaterEqual(request["secondConservativeReservation"],
                                request["secondRequested"])

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

    def test_rejects_unsupported_mutation_operations(self):
        for vector in SUITE["mutationValidationVectors"]:
            with self.subTest(vector=vector["id"]):
                candidate = copy.deepcopy(SUITE["schemaFixture"])
                with self.assertRaises(ValueError):
                    apply_mutation(candidate, vector["mutation"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
