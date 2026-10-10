#!/usr/bin/env python3
"""Regression gate for software-substrate decision schema vectors.

This validates only the proposed decision's JSON shape. It does not verify a
signature, execute an authorizer, or establish a provider or target effect.
"""

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads(
    (ROOT / "schemas/software-substrate-decision.json").read_text())
SUITE = json.loads(
    (ROOT / "specifications/conformance/software-substrate-execution.json")
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
        self.assertEqual(len(vectors), 38)
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
                self.assertEqual(pair["request"], expected_request)
                self.assertEqual(pair["expect"]["compareTo"], baseline["id"])
                self.assertEqual(pair["expect"]["decisionNotLooserThan"], "allow")
                self.assertIs(pair["expect"]["environmentalCapacityNotGreaterThanCompared"], True)

    def test_schema_definition(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_schema_vectors(self):
        for vector in SUITE["schemaVectors"]:
            with self.subTest(vector=vector["id"]):
                candidate = copy.deepcopy(SUITE["schemaFixture"])
                if "mutation" in vector:
                    apply_mutation(candidate, vector["mutation"])
                actual = VALIDATOR.is_valid(candidate)
                expected = vector["expect"]["schemaValid"]
                self.assertEqual(actual, expected, vector["id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
