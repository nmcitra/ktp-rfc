#!/usr/bin/env python3
"""Regression gate for the six deployment Risk Factor weights (F04).

Runs the real declaration checker, its CLI, and the Draft 2020-12 schema.
Install jsonschema==4.26.0, then run:
    python3 scripts/test-risk-factor-weights.py

The schema checks each weight and the six-factor shape. The declaration
checker additionally requires the exact sum of Fraction(str(weight)) to be
one, using the numeric values produced by the existing JSON parser. These
tests do not claim to preserve original JSON number tokens. The arithmetic
tests check the published weighted-risk formula, not a runtime authorizer.
"""

import copy
import importlib.util
import itertools
import json
import math
import re
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
CHECKER_PATH = ROOT / "scripts/check-declarations.py"
SPEC = importlib.util.spec_from_file_location("check_declarations", CHECKER_PATH)
DECLARATIONS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DECLARATIONS)
FACTORS = DECLARATIONS.FACTORS
SCHEMA = json.loads((ROOT / "schemas/deployment-profile.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
BASE_WEIGHTS = [DECLARATIONS.EXAMPLE["risk_factors"][name]["weight"]
                for name in FACTORS]


def profile_with(weights):
    profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
    for name, weight in zip(FACTORS, weights, strict=True):
        profile["risk_factors"][name]["weight"] = weight
    return profile


def published_profiles():
    """Read only the named profiles in the two domain-weight sections."""
    profiles = []
    sections = (
        ("ktp-core.md", "## Domain Weights", "## Risk Factor Modularity", 5),
        ("ktp-sensors.md", "# Domain Weight Profiles",
         "# Sensor Quality and Validation", 6),
    )
    for filename, start, end, expected_count in sections:
        source = (ROOT / "rfc-src" / filename).read_text()
        section = source.split(start + "\n", 1)[1].split(end + "\n", 1)[0]
        named = []
        for line in section.splitlines():
            if "evidence_density=" not in line:
                continue
            label, _, _ = line.partition(":")
            pairs = re.findall(r"([a-z_]+)=([0-9]+(?:\.[0-9]+)?)", line)
            if len(pairs) != len(FACTORS) or set(dict(pairs)) != set(FACTORS):
                raise AssertionError(f"Incomplete profile: {filename}: {label}")
            values = {key: float(value) for key, value in pairs}
            named.append((f"{filename}: {label}",
                          [values[name] for name in FACTORS]))
        if len(named) != expected_count:
            raise AssertionError(f"Expected {expected_count} profiles in {filename}; "
                                 f"found {len(named)}")
        profiles.extend(named)
        if filename == "ktp-sensors.md":
            custom = [block for block in section.split("~~~")[1::2]
                      if '"profile_id": "custom-retail"' in block]
            if len(custom) != 1:
                raise AssertionError("Expected one Sensors custom-retail profile")
            weights = json.loads(custom[0])["weights"]
            if set(weights) != set(FACTORS):
                raise AssertionError("Incomplete custom-retail profile")
            profiles.append(("ktp-sensors.md: custom-retail",
                             [weights[name] for name in FACTORS]))
    return profiles


# name, all six weights, checker valid. All values in this table are strict
# finite JSON numbers in (0, 1], so the schema intentionally accepts them.
SUM_CASES = [
    ("embedded-example", BASE_WEIGHTS, True),
    ("skewed-valid", [0.95, 0.01, 0.01, 0.01, 0.01, 0.01], True),
    ("decimal-valid", [0.1, 0.2, 0.3, 0.15, 0.15, 0.1], True),
    ("original-small-total", [0.01] * 6, False),
    ("all-maximum", [1] * 6, False),
    ("near-unit-deficit", [math.nextafter(BASE_WEIGHTS[0], 0)]
     + BASE_WEIGHTS[1:], False),
    ("near-unit-excess", [math.nextafter(BASE_WEIGHTS[0], math.inf)]
     + BASE_WEIGHTS[1:], False),
    ("six-rounded-sixths", [0.16666666666666666] * 6, False),
    ("balanced-rounded-sixths", [0.16666666666666666] * 5
     + [0.1666666666666667], True),
]


def malformed_profiles():
    for value in (None, [], "profile", 1, True):
        yield f"root-{type(value).__name__}", value
    for value in (None, [], "factors", 1, True):
        profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
        profile["risk_factors"] = value
        yield f"risk-factors-{type(value).__name__}", profile
    for value in (None, [], "factor", 1, True):
        profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
        profile["risk_factors"][FACTORS[0]] = value
        yield f"factor-{type(value).__name__}", profile
    profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
    profile.pop("risk_factors")
    yield "missing-risk-factors", profile
    for name in FACTORS:
        profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
        del profile["risk_factors"][name]
        yield f"missing-{name}", profile
        profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
        del profile["risk_factors"][name]["weight"]
        yield f"missing-weight-{name}", profile
    for value in (None, copy.deepcopy(DECLARATIONS.EXAMPLE["risk_factors"][FACTORS[0]])):
        profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
        profile["risk_factors"]["unknown_factor"] = value
        yield f"extra-factor-{type(value).__name__}", profile


class RiskFactorWeightTests(unittest.TestCase):
    def check_unchanged(self, profile):
        # JSON-compatible caller objects, including Python's nonstandard
        # NaN/Infinity values, must remain byte-for-byte serializable as before.
        before = json.dumps(profile, sort_keys=True)
        try:
            return DECLARATIONS.check(profile)
        finally:
            self.assertEqual(json.dumps(profile, sort_keys=True), before)

    def test_schema_definition(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_exact_sum_contract(self):
        for name, weights, expected_valid in SUM_CASES:
            with self.subTest(case=name):
                profile = json.loads(json.dumps(profile_with(weights), allow_nan=False))
                failures = self.check_unchanged(profile)
                self.assertEqual(not failures, expected_valid, failures)

    def test_schema_intentionally_does_not_enforce_sum(self):
        for name, weights, _ in SUM_CASES:
            with self.subTest(case=name):
                errors = list(VALIDATOR.iter_errors(profile_with(weights)))
                self.assertFalse(errors, [error.message for error in errors])

    def test_published_profiles_remain_valid(self):
        profiles = published_profiles()
        self.assertEqual(len(profiles), 12)  # Core 5; Sensors 6 named + 1 custom.
        for name, weights in profiles:
            with self.subTest(profile=name):
                profile = profile_with(weights)
                self.assertFalse(self.check_unchanged(profile))
                self.assertTrue(VALIDATOR.is_valid(profile))

    def test_invalid_weight_types_and_bounds(self):
        for factor in FACTORS:
            for value in (0, -0.0, -0.1, 1.01, 10 ** 400,
                          True, False, "0.25", None, [], {}):
                with self.subTest(factor=factor, value=repr(value)):
                    profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
                    profile["risk_factors"][factor]["weight"] = value
                    self.assertTrue(self.check_unchanged(profile))
                    self.assertFalse(VALIDATOR.is_valid(profile))

    def test_checker_rejects_nonfinite_weights(self):
        # JSON Schema does not reliably reject every non-JSON NaN/Infinity
        # value admitted by a language parser, so test the checker directly.
        for factor in FACTORS:
            for token in ("NaN", "Infinity", "-Infinity", "1e400", "-1e400"):
                with self.subTest(factor=factor, token=token):
                    profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
                    profile["risk_factors"][factor]["weight"] = json.loads(token)
                    self.assertTrue(self.check_unchanged(profile))

    def test_malformed_shapes_fail_without_mutation_or_crash(self):
        for name, profile in malformed_profiles():
            with self.subTest(case=name):
                self.assertTrue(self.check_unchanged(profile))
                self.assertFalse(VALIDATOR.is_valid(profile))

    def test_cli_exit_codes(self):
        cases = [(name, profile_with(weights), valid)
                 for name, weights, valid in SUM_CASES]
        cases.extend((name, profile, False) for name, profile in malformed_profiles())
        for value in (True, False, "0.25", None, [], {}, math.nan, math.inf, -math.inf):
            profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
            profile["risk_factors"][FACTORS[0]]["weight"] = value
            cases.append((f"weight-{value!r}", profile, False))
        with tempfile.TemporaryDirectory(prefix="ktp-weight-regressions-") as tempdir:
            path = Path(tempdir) / "profile.json"
            for name, profile, valid in cases:
                with self.subTest(case=name):
                    path.write_text(json.dumps(profile))
                    result = subprocess.run(
                        [sys.executable, str(CHECKER_PATH), "--profile", str(path)],
                        capture_output=True, text=True, check=False)
                    self.assertEqual(result.returncode, 0 if valid else 1,
                                     result.stdout + result.stderr)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertIn("declarations valid" if valid else
                                  "DECLARATIONS INVALID", result.stdout)
            # Exercise exponent overflow through the CLI's existing parser.
            path.write_text(json.dumps(profile_with(BASE_WEIGHTS)).replace(
                '"weight": 0.25', '"weight": 1e400', 1))
            result = subprocess.run(
                [sys.executable, str(CHECKER_PATH), "--profile", str(path)],
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertIn("DECLARATIONS INVALID", result.stdout)

    def test_accepted_weights_bound_risk_and_preserve_monotonicity(self):
        # Exact-decimal arithmetic for the published R=sum(w_i*s_i) and
        # E=base*(1-R) formulas. No decision result is simulated here.
        profiles = [(name, weights) for name, weights, valid in SUM_CASES if valid]
        profiles.extend(published_profiles())
        stresses = list(itertools.product((Fraction(0), Fraction(1, 2), Fraction(1)),
                                          repeat=len(FACTORS)))
        for name, values in profiles:
            with self.subTest(profile=name):
                self.assertFalse(self.check_unchanged(profile_with(values)))
                weights = [Fraction(str(value)) for value in values]
                self.assertEqual(sum(weights), 1)
                self.assertEqual(sum(weight * 0 for weight in weights), 0)
                self.assertEqual(sum(weight * 1 for weight in weights), 1)
                for stress in stresses:
                    risk = sum(weight * value for weight, value in zip(weights, stress))
                    self.assertGreaterEqual(risk, 0)
                    self.assertLessEqual(risk, 1)
                    for index, value in enumerate(stress):
                        increased_risk = risk + weights[index] * (1 - value)
                        for base in (Fraction(0), Fraction(50), Fraction(100)):
                            self.assertLessEqual(base * (1 - increased_risk),
                                                 base * (1 - risk))


if __name__ == "__main__":
    unittest.main(verbosity=2)
