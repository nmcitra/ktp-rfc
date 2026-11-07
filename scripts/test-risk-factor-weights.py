#!/usr/bin/env python3
"""Regression gate for the five deployment Risk Factor weights (F04).

Runs the real declaration checker, its CLI, and the Draft 2020-12 schema.
Install jsonschema==4.26.0, then run:
    python3 scripts/test-risk-factor-weights.py

The schema checks each weight and the five-factor shape. The declaration
checker additionally requires the exact sum of Fraction(str(weight)) to be
one, using the numeric values produced by the existing JSON parser. These
tests do not claim to preserve original JSON number tokens. The arithmetic
tests check the published weighted-risk formula, not a runtime authorizer.

It also pins the v3 identifiers of the Risk Factors and Trust Proof schemas
and the byte-preserved v2 files their v2 identifiers still name, and checks
that the demand-input vectors' R and E_trust are exact on their own inputs.
"""

import copy
import hashlib
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
from urllib.parse import urljoin

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


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


# name, all five weights, checker valid. All values in this table are strict
# finite JSON numbers in (0, 1], so the schema intentionally accepts them.
SUM_CASES = [
    ("embedded-example", BASE_WEIGHTS, True),
    ("skewed-valid", [0.96, 0.01, 0.01, 0.01, 0.01], True),
    ("decimal-valid", [0.1, 0.2, 0.3, 0.25, 0.15], True),
    ("original-small-total", [0.01] * 5, False),
    ("all-maximum", [1] * 5, False),
    ("near-unit-deficit", [math.nextafter(BASE_WEIGHTS[0], 0)]
     + BASE_WEIGHTS[1:], False),
    ("near-unit-excess", [math.nextafter(BASE_WEIGHTS[0], math.inf)]
     + BASE_WEIGHTS[1:], False),
    ("five-rounded-fifths", [0.2] * 5, True),
    ("five-rounded-thirds", [0.3333333333333333] * 3 + [0.0000000000000001] * 2, False),
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
                f'"weight": {BASE_WEIGHTS[0]}', '"weight": 1e400', 1))
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



class RiskFactorsSchemaIdentityTests(unittest.TestCase):
    """The five-input objects take v3 identifiers; the published v2 bytes stay
    where citations of the v2 identifiers land."""

    LEGACY = {
        "risk-factors-legacy-v2.json": (
            "a2f497489b94e727398278794389e6fbae0a44c851f19a1e5d1daafc1daa16e0",
            "/v2/risk-factors.json"),
        "trust-proof-legacy-v2.json": (
            "41d5dd2506893094d41e21193cf95eed396dc99b8d32d7264f50ea1a7972d4e0",
            "/v2/trust-proof.json"),
        "sensor-config-legacy-v2.json": (
            "a9f70585fc9ba85334f972dc8dbccb9dfa0446cb18ce3d8b79cadf5d59f3ad22",
            "/v2/sensor-config.json"),
    }

    @classmethod
    def setUpClass(cls):
        cls.schemas = {path.name: json.loads(path.read_text())
                       for path in sorted((ROOT / "schemas").glob("*.json"))}
        cls.registry = Registry().with_resources(
            (schema["$id"], Resource.from_contents(schema))
            for schema in cls.schemas.values())
        cls.five = cls.schemas["risk-factors.json"]["examples"][0]
        cls.six = cls.schemas["risk-factors-legacy-v2.json"]["examples"][0]

    def risk_factors_ref(self, name):
        """Resolve the one reference a schema makes to a Risk Factors object."""
        found = []

        def walk(node):
            if isinstance(node, dict):
                ref = node.get("$ref")
                if isinstance(ref, str) and ref.endswith("risk-factors.json"):
                    found.append(ref)
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(self.schemas[name])
        self.assertEqual(1, len(found), name)
        return urljoin(self.schemas[name]["$id"], found[0])

    def accepts(self, ref, instance):
        validator = Draft202012Validator({"$ref": ref}, registry=self.registry)
        return validator.is_valid(instance)

    def test_legacy_files_are_the_published_bytes(self):
        for name, (digest, suffix) in self.LEGACY.items():
            with self.subTest(schema=name):
                data = (ROOT / "schemas" / name).read_bytes()
                self.assertEqual(digest, hashlib.sha256(data).hexdigest())
                self.assertTrue(json.loads(data)["$id"].endswith(suffix))

    def test_active_schemas_carry_v3_identifiers(self):
        risk = self.schemas["risk-factors.json"]
        self.assertTrue(risk["$id"].endswith("/v3/risk-factors.json"))
        self.assertEqual(sorted(FACTORS), sorted(risk["required"]))
        self.assertTrue(self.schemas["trust-proof.json"]["$id"]
                        .endswith("/v3/trust-proof.json"))
        sensors = self.schemas["sensor-config.json"]
        self.assertTrue(sensors["$id"].endswith("/v3/sensor-config.json"))
        self.assertEqual(sorted(FACTORS + ["soul"]),
                         sorted(sensors["properties"]["dimension"]["enum"]))

    def test_each_reference_resolves_to_its_own_version(self):
        cases = {
            "trust-proof.json": "five",
            "transaction-record.json": "five",
            "trust-proof-legacy-v2.json": "six",
            "transaction-record-legacy-v2.json": "six",
        }
        for name, shape in cases.items():
            with self.subTest(schema=name):
                ref = self.risk_factors_ref(name)
                self.assertEqual(shape == "five", self.accepts(ref, self.five))
                self.assertEqual(shape == "six", self.accepts(ref, self.six))

    # The preserved v2 bytes are what v2.1.0 published, defects included.
    PUBLISHED_EXAMPLE_DEFECTS = {
        "trust-proof-legacy-v2.json": "v2.1.0 published resilience_hash examples "
                                      "with 60 hex digits against a 64-digit pattern",
    }

    def references(self, node):
        if isinstance(node, dict):
            if isinstance(node.get("$ref"), str):
                yield node["$ref"]
            for value in node.values():
                yield from self.references(value)
        elif isinstance(node, list):
            for value in node:
                yield from self.references(value)

    def test_every_reference_resolves(self):
        for name, schema in self.schemas.items():
            resolver = self.registry.resolver(base_uri=schema["$id"])
            for ref in self.references(schema):
                with self.subTest(schema=name, ref=ref):
                    resolver.lookup(ref)

    def test_every_example_validates(self):
        for name, schema in self.schemas.items():
            if name in self.PUBLISHED_EXAMPLE_DEFECTS:
                continue
            validator = Draft202012Validator(schema, registry=self.registry)
            for index, example in enumerate(schema.get("examples", [])):
                with self.subTest(schema=name, example=index):
                    self.assertEqual([], [error.message for error in
                                          validator.iter_errors(example)])



class DemandVectorArithmeticTests(unittest.TestCase):
    """The demand-input vectors that show R and E_trust carry exactly what
    Core's formulas give on their own inputs, with nothing rounded."""

    @classmethod
    def setUpClass(cls):
        path = ROOT / "specifications/conformance/demand-input-v1.json"
        suite = json.loads(path.read_text(), parse_float=Fraction)
        cls.vectors = {vector["id"].split("-")[0]: vector
                       for vector in suite["vectors"]}

    def test_kickoff_risk_and_trust_are_exact(self):
        given = self.vectors["DI10"]["given"]
        expect = self.vectors["DI10"]["expect"]
        risk = sum(given["weights"][name] * given["normalized_inputs"][name]
                   for name in FACTORS)
        self.assertEqual(sorted(FACTORS), sorted(given["weights"]))
        self.assertEqual(risk, expect["R"])
        self.assertEqual(given["E_base"] * (1 - risk), expect["E_trust"])

    def test_declared_supplier_case_matches_the_kickoff(self):
        given = self.vectors["DI01"]["given"]
        expect = self.vectors["DI01"]["expect"]
        self.assertEqual(self.vectors["DI10"]["expect"]["R"], given["R"])
        self.assertEqual(given["R"], expect["R"])
        self.assertEqual(given["E_base"] * (1 - given["R"]), expect["E_trust"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
