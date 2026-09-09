#!/usr/bin/env python3
"""Regression gate for the capacity contract's deployment thresholds (F03).

Runs the repository's declaration checker and actual Draft 2020-12 schema.
Install jsonschema==4.26.0 in an isolated environment, then run:
    python3 scripts/test-envelope-thresholds.py

The arithmetic property checks the published threshold bands. The downstream
decision vectors describe requirements for an authorizer; this repository has
no authorizer implementation, and these tests do not claim to execute one.
"""

import copy
import importlib.util
import json
import math
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "check_declarations", ROOT / "scripts/check-declarations.py")
DECLARATIONS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DECLARATIONS)
SCHEMA = json.loads((ROOT / "schemas/deployment-profile.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
OMITTED = object()

# name, explicit threshold section (or omission), checker valid, schema valid.
# Cross-property ordering is a semantic check, not a JSON Schema constraint.
FINITE_CASES = [
    ("omitted-default", OMITTED, True, True),
    ("ordinary", {"m_veto": 0, "m_allow": 0.2}, True, True),
    ("positive-veto", {"m_veto": 0.1, "m_allow": 0.5}, True, True),
    ("integer-numbers", {"m_veto": 0, "m_allow": 1}, True, True),
    ("conservative-above-one", {"m_veto": 2, "m_allow": 3}, True, True),
    ("negative-original-counterexample", {"m_veto": -1, "m_allow": -0.5}, False, False),
    ("negative-veto", {"m_veto": -0.1, "m_allow": 0.2}, False, False),
    ("negative-allow", {"m_veto": 0, "m_allow": -0.1}, False, False),
    ("explicit-zero-pair", {"m_veto": 0, "m_allow": 0}, False, False),
    ("equal-positive-pair", {"m_veto": 0.2, "m_allow": 0.2}, False, True),
    ("reversed-positive-pair", {"m_veto": 0.5, "m_allow": 0.2}, False, True),
    ("null-section", None, False, False),
    ("empty-object", {}, False, False),
    ("missing-veto", {"m_allow": 0.2}, False, False),
    ("missing-allow", {"m_veto": 0}, False, False),
    ("extra-field", {"m_veto": 0, "m_allow": 0.2, "override": True}, False, False),
    ("array-section", [0, 0.2], False, False),
    ("string-section", "default", False, False),
    ("numeric-section", 1, False, False),
    ("boolean-section", False, False, False),
    ("null-veto", {"m_veto": None, "m_allow": 0.2}, False, False),
    ("null-allow", {"m_veto": 0, "m_allow": None}, False, False),
    ("boolean-veto", {"m_veto": False, "m_allow": 0.2}, False, False),
    ("boolean-allow", {"m_veto": 0, "m_allow": True}, False, False),
    ("string-veto", {"m_veto": "0", "m_allow": 0.2}, False, False),
    ("string-allow", {"m_veto": 0, "m_allow": "0.2"}, False, False),
]


def profile_with(thresholds=OMITTED):
    profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
    profile.pop("envelope_thresholds", None)
    if thresholds is not OMITTED:
        profile["envelope_thresholds"] = copy.deepcopy(thresholds)
    return profile


class EnvelopeThresholdTests(unittest.TestCase):
    def test_schema_definition(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_checker_finite_json_cases(self):
        for name, thresholds, checker_valid, _ in FINITE_CASES:
            with self.subTest(case=name):
                # Strict serialization also proves these are finite JSON cases.
                profile = json.loads(json.dumps(profile_with(thresholds), allow_nan=False))
                failures = DECLARATIONS.check(profile)
                self.assertEqual(not failures, checker_valid, failures)

    def test_schema_finite_json_cases(self):
        for name, thresholds, _, schema_valid in FINITE_CASES:
            with self.subTest(case=name):
                profile = json.loads(json.dumps(profile_with(thresholds), allow_nan=False))
                errors = list(VALIDATOR.iter_errors(profile))
                self.assertEqual(not errors, schema_valid,
                                 [error.message for error in errors])

    def test_checker_rejects_nonfinite_python_thresholds(self):
        # NaN and infinities are not JSON numbers. Python callers can still
        # supply them, so the checker must not accept them as thresholds.
        for field in ("m_veto", "m_allow"):
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(field=field, value=repr(value)):
                    thresholds = {"m_veto": 0, "m_allow": 0.2}
                    thresholds[field] = value
                    self.assertTrue(DECLARATIONS.check(profile_with(thresholds)))

    def test_checker_rejects_nonfinite_parser_results(self):
        # Python's parser accepts nonstandard constants, and finite-looking
        # exponent text can overflow its float representation. JSON Schema's
        # number type alone cannot reliably catch those resulting values.
        for field in ("m_veto", "m_allow"):
            for token in ("NaN", "Infinity", "-Infinity", "1e400", "-1e400"):
                with self.subTest(field=field, token=token):
                    thresholds = {"m_veto": 0, "m_allow": 0.2}
                    thresholds[field] = json.loads(token)
                    self.assertTrue(DECLARATIONS.check(profile_with(thresholds)))

    def test_accepted_threshold_bands_exclude_over_capacity(self):
        # Property-style arithmetic check, not a second authorizer. For every
        # accepted sampled profile and A > E > 0, the published margin cannot
        # satisfy either the stable or supervision band's inequalities.
        threshold_pairs = [(0, 0)]  # Omitted section's existing binary default.
        for veto in (0, 0.01, 0.2, 0.9, 1, 2, 100):
            for gap in (0.001, 0.2, 1, 10):
                thresholds = {"m_veto": veto, "m_allow": veto + gap}
                profile = profile_with(thresholds)
                self.assertFalse(DECLARATIONS.check(profile))
                self.assertTrue(VALIDATOR.is_valid(profile))
                threshold_pairs.append((veto, veto + gap))
        for veto, allow in threshold_pairs:
            for capacity in (1e-12, 0.1, 1, 50, 1e6, 1e12):
                demands = [math.nextafter(capacity, math.inf)]
                demands.extend(capacity * ratio for ratio in (1.001, 1.2, 2, 1000))
                for demand in demands:
                    with self.subTest(veto=veto, allow=allow, A=demand, E=capacity):
                        self.assertGreater(demand, capacity)
                        margin = 1 - demand / capacity
                        self.assertLessEqual(margin, veto)
                        self.assertFalse(margin >= allow)
                        self.assertFalse(veto < margin < allow)

    def test_downstream_vector_file_is_strict_json(self):
        # This checks the fixture container only. It deliberately does not
        # calculate or assert authorizer decisions from a test-only evaluator.
        def reject_constant(token):
            raise ValueError(f"Non-JSON numeric constant: {token}")

        suite = json.loads(
            (ROOT / "specifications/conformance/capacity-gate-v1.json").read_text(),
            parse_constant=reject_constant)
        vectors = suite["vectors"]
        self.assertEqual(len({vector["id"] for vector in vectors}), len(vectors))
        self.assertTrue(vectors)
        json.dumps(suite, allow_nan=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
