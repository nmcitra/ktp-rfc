#!/usr/bin/env python3
"""Regression gate for consequential-action evidence schema vectors.

This validates only the proposed record's JSON shape. It does not verify a
signature, authorize an action, establish protected-path coverage, or prove a
target effect.
"""

import copy
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
