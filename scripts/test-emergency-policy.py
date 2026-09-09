#!/usr/bin/env python3
"""Regression gate for emergency policy declaration validation.

Exercises the actual schema, declaration checker, and CLI. The outage vectors
are normative downstream requirements; this repository has no authorizer,
signature verifier, approval registry, trusted clock, or incident state store.
These tests do not execute or claim to verify those runtime requirements.

Install jsonschema==4.26.0 in an isolated environment, then run:
    python3 scripts/test-emergency-policy.py
"""

import copy
import importlib.util
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/check-emergency-policy.py"
SPEC = importlib.util.spec_from_file_location("check_emergency_policy", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
DECLARATION_SPEC = importlib.util.spec_from_file_location(
    "check_declarations", ROOT / "scripts/check-declarations.py")
DECLARATIONS = importlib.util.module_from_spec(DECLARATION_SPEC)
DECLARATION_SPEC.loader.exec_module(DECLARATIONS)
DEPLOYMENT_SCHEMA = json.loads((ROOT / "schemas/deployment-profile.json").read_text())
DEPLOYMENT_VALIDATOR = Draft202012Validator(DEPLOYMENT_SCHEMA)
DIGEST = "sha256:" + "a" * 64
DIGEST384 = "sha384:" + "b" * 96


def example(count=3):
    """A shape-valid test declaration, without any actual approval or keys."""
    return {
        "policy_id": "example-containment", "version": 1,
        "zone_id": "example-zone", "predecessor_digest": None,
        "custodians": [
            {"principal_id": f"person-{index}", "key_id": f"key-{index}",
             "control_domain": f"custody-domain-{index}"}
            for index in range(count)],
        "change_control": {"approval_threshold": max(3, (9 * count + 9) // 10),
                           "notice_days": 90, "ratification_days": 14,
                           "external_review_required": True},
        "activation": {"threshold": 2, "max_duration_seconds": 14400,
                       "automatic_renewal": False},
        "actions": [{"action_id": "close-isolation-valve",
                     "subject": "safety-controller-1",
                     "resource": "valve:coolant-isolation-1",
                     "operation": "set-state",
                     "parameters": {"state": "closed", "verify": True,
                                    "retry_delay": 0, "annotation": None},
                     "max_executions": 1,
                     "evaluation_profile_digest": DIGEST}],
        "logging": {"durable_before_execution": True},
    }


def replace(path, value, policy=None):
    candidate = copy.deepcopy(example() if policy is None else policy)
    target = candidate
    for member in path[:-1]:
        target = target[member]
    target[path[-1]] = value
    return candidate


class EmergencyPolicyTests(unittest.TestCase):
    def assert_rejected(self, policy, schema=True):
        self.assertTrue(CHECKER.check(policy))
        if schema:
            self.assertFalse(CHECKER.VALIDATOR.is_valid(policy))

    def run_cli(self, contents):
        with tempfile.TemporaryDirectory(prefix="ktp-emergency-test-") as temp:
            path = Path(temp) / "policy.json"
            path.write_text(contents, encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), "--policy", str(path)],
                                  capture_output=True, text=True, check=False)

    def test_schema_definition_and_valid_declarations(self):
        Draft202012Validator.check_schema(CHECKER.SCHEMA)
        for count in (3, 5, 10, 11):
            for version in (1, 2, 10):
                with self.subTest(count=count, version=version):
                    policy = example(count)
                    policy["version"] = version
                    policy["predecessor_digest"] = None if version == 1 else DIGEST
                    json.dumps(policy, allow_nan=False)
                    self.assertTrue(CHECKER.VALIDATOR.is_valid(policy))
                    self.assertEqual(CHECKER.check(policy), [])

    def test_change_threshold_uses_entire_roster(self):
        for count, minimum in ((3, 3), (5, 5), (10, 9), (11, 10)):
            for threshold in range(0, count + 2):
                with self.subTest(count=count, threshold=threshold):
                    policy = replace(("change_control", "approval_threshold"),
                                     threshold, example(count))
                    self.assertEqual(not CHECKER.check(policy),
                                     minimum <= threshold <= count)
        # These configurations have schema-valid shape, but fail cross-count checks.
        self.assertTrue(CHECKER.VALIDATOR.is_valid(
            replace(("change_control", "approval_threshold"), 4, example(5))))
        self.assert_rejected(replace(("change_control", "approval_threshold"),
                                     4, example(5)), schema=False)

    def test_activation_requires_two_and_cannot_exceed_roster(self):
        for count in (3, 5, 10):
            for threshold in (0, 1, 2, count, count + 1):
                with self.subTest(count=count, threshold=threshold):
                    policy = replace(("activation", "threshold"), threshold, example(count))
                    self.assertEqual(not CHECKER.check(policy), 2 <= threshold <= count)

    def test_tampered_roster_recomputes_count_bounds(self):
        added = example(3)
        added["custodians"].append(example(4)["custodians"][-1])
        self.assert_rejected(added, schema=False)
        removed = example(5)
        removed["custodians"].pop()
        self.assert_rejected(removed, schema=False)
        # Replacing all names is shape-valid. Incumbent approval and history
        # must be enforced by a downstream verifier, not inferred from names.
        replaced = example()
        for custodian in replaced["custodians"]:
            for field in custodian:
                custodian[field] = "replacement-" + custodian[field]
        self.assertEqual(CHECKER.check(replaced), [])

    def test_custodian_and_action_uniqueness(self):
        self.assert_rejected(replace(("custodians",), example()["custodians"][:2]))
        for field in ("principal_id", "key_id", "control_domain"):
            with self.subTest(field=field):
                policy = example()
                policy["custodians"][1][field] = policy["custodians"][0][field]
                self.assert_rejected(policy, schema=False)
        policy = example()
        duplicate = copy.deepcopy(policy["actions"][0])
        duplicate["resource"] = "different-resource"
        policy["actions"].append(duplicate)
        self.assert_rejected(policy, schema=False)

    def test_predecessor_and_digest_syntax(self):
        self.assert_rejected(replace(("predecessor_digest",), DIGEST))
        self.assert_rejected(replace(("version",), 2))
        for digest in (DIGEST, DIGEST384):
            policy = replace(("version",), 2)
            policy["predecessor_digest"] = digest
            policy["actions"][0]["evaluation_profile_digest"] = digest
            with self.subTest(valid_digest=digest):
                self.assertTrue(CHECKER.VALIDATOR.is_valid(policy))
                self.assertEqual(CHECKER.check(policy), [])
        for value in ("", "sha256:abc", "sha256:" + "A" * 64,
                      DIGEST + "\n", " " + DIGEST, "sha512:" + "a" * 64,
                      "sha384:" + "B" * 96, "sha384:" + "b" * 95,
                      "sha384:" + "b" * 97, DIGEST384 + "\n",
                      " " + DIGEST384, "sha256:" + "b" * 96, None):
            with self.subTest(digest=value):
                self.assert_rejected(replace(
                    ("actions", 0, "evaluation_profile_digest"), value))
                policy = replace(("version",), 2)
                policy["predecessor_digest"] = value
                self.assert_rejected(policy)

    def test_change_control_and_activation_floors(self):
        invalid = [
            (("change_control", "notice_days"), 89),
            (("change_control", "ratification_days"), 13),
            (("change_control", "external_review_required"), False),
            (("change_control", "external_review_required"), 1),
            (("activation", "max_duration_seconds"), 0),
            (("activation", "max_duration_seconds"), 14401),
            (("activation", "automatic_renewal"), True),
            (("activation", "automatic_renewal"), 0),
            (("logging", "durable_before_execution"), False),
            (("logging", "durable_before_execution"), 1),
            (("actions", 0, "max_executions"), 0),
        ]
        for path, value in invalid:
            with self.subTest(path=path):
                self.assert_rejected(replace(path, value))
        for duration in (1, 14400):
            self.assertFalse(CHECKER.check(replace(
                ("activation", "max_duration_seconds"), duration)))

    def test_numeric_controls_reject_boolean_string_fraction_and_null(self):
        paths = [("version",), ("change_control", "approval_threshold"),
                 ("change_control", "notice_days"),
                 ("change_control", "ratification_days"),
                 ("activation", "threshold"),
                 ("activation", "max_duration_seconds"),
                 ("actions", 0, "max_executions")]
        for path in paths:
            for value in (True, False, "3", None, 2.5, -1):
                with self.subTest(path=path, value=value):
                    self.assert_rejected(replace(path, value))

    def test_finite_json_values_and_python_boundary(self):
        paths = [("version",), ("change_control", "approval_threshold"),
                 ("activation", "max_duration_seconds"),
                 ("actions", 0, "parameters", "retry_delay")]
        for path in paths:
            for value in (math.nan, math.inf, -math.inf):
                with self.subTest(path=path, value=repr(value)):
                    self.assert_rejected(replace(path, value), schema=False)
        for value in ((), {"nested": object()}, {1: "non-string key"}):
            self.assertTrue(CHECKER.check(value))
        cyclic = {}
        cyclic["cycle"] = cyclic
        self.assertTrue(CHECKER.check(cyclic))

    def test_literals_and_parameter_map(self):
        paths = [("policy_id",), ("zone_id",),
                 ("custodians", 0, "principal_id"),
                 ("custodians", 0, "key_id"),
                 ("custodians", 0, "control_domain"),
                 ("actions", 0, "action_id"), ("actions", 0, "subject"),
                 ("actions", 0, "resource"), ("actions", 0, "operation")]
        for path in paths:
            for value in ("", " ", "\n", "name\n", "name space", "*",
                          "name?", "[name]", "{name}"):
                with self.subTest(path=path, value=repr(value)):
                    self.assert_rejected(replace(path, value))
        for parameters in ({"nested": {}}, {"nested": []}, {"*": "value"},
                           {"": "value"}, {"bad name": "value"}):
            self.assert_rejected(replace(("actions", 0, "parameters"), parameters))
        # Empty maps and literal scalar values are allowed; runtime exact
        # matching must still deny any parameter absent from the map.
        for parameters in ({}, {"s": "literal * text", "n": 1.25,
                                "b": False, "z": None}):
            self.assertFalse(CHECKER.check(replace(
                ("actions", 0, "parameters"), parameters)))

    def test_required_fields_and_closed_objects(self):
        paths = [(), ("custodians", 0), ("change_control",),
                 ("activation",), ("actions", 0), ("logging",)]
        for path in paths:
            policy = example()
            target = policy
            for part in path:
                target = target[part]
            for name in list(target):
                candidate = copy.deepcopy(policy)
                selected = candidate
                for part in path:
                    selected = selected[part]
                del selected[name]
                with self.subTest(path=path, removed=name):
                    self.assert_rejected(candidate)
            target["approved"] = True
            with self.subTest(path=path, extra="approved"):
                self.assert_rejected(policy)
        for value in ([], {}, None, True, "policy"):
            self.assert_rejected(value)
        self.assert_rejected(replace(("actions",), []))

    def test_checker_does_not_mutate_or_rescale(self):
        for policy in (example(), replace(("change_control", "approval_threshold"), 3,
                                          example(10))):
            before = copy.deepcopy(policy)
            CHECKER.check(policy)
            self.assertEqual(policy, before)

    def test_cli_success_is_limited_to_declaration(self):
        result = self.run_cli(json.dumps(example()))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), CHECKER.VALID_MESSAGE)
        self.assertEqual(result.stderr, "")

    def test_cli_rejects_bad_json_duplicate_members_and_nonfinite_values(self):
        for contents in ("{", '{"policy_id":"one","policy_id":"two"}',
                         json.dumps(example()).replace('"threshold": 2',
                                                       '"threshold": 1, "threshold": 2'),
                         json.dumps(replace(("activation", "threshold"), 1)),
                         json.dumps(example()).replace('"retry_delay": 0',
                                                       '"retry_delay": 1e400'),
                         json.dumps(example()).replace('"retry_delay": 0',
                                                       '"retry_delay": NaN')):
            with self.subTest(contents=contents[:80]):
                result = self.run_cli(contents)
                self.assertEqual(result.returncode, 1)
                self.assertIn("Invalid emergency policy:", result.stderr)
                self.assertNotIn(CHECKER.VALID_MESSAGE, result.stdout)
                self.assertNotIn("Traceback", result.stderr)
        result = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True,
                                text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--policy", result.stderr)

    def test_deployment_binding_is_optional_and_shape_only(self):
        Draft202012Validator.check_schema(DEPLOYMENT_SCHEMA)
        profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
        self.assertNotIn("emergency_policy", profile)
        self.assertFalse(DECLARATIONS.check(profile))
        self.assertTrue(DEPLOYMENT_VALIDATOR.is_valid(profile))
        for digest in (DIGEST, DIGEST384):
            profile["emergency_policy"] = {
                "policy_id": "example-containment", "version": 1, "digest": digest}
            before = copy.deepcopy(profile)
            with self.subTest(digest=digest):
                self.assertFalse(DECLARATIONS.check(profile))
                self.assertTrue(DEPLOYMENT_VALIDATOR.is_valid(profile))
                self.assertEqual(profile, before)
        # No policy is loaded here. Acceptance validates only the reference,
        # never approval, digest agreement with a payload, or activation.

    def test_deployment_binding_rejects_malformed_references(self):
        valid = {"policy_id": "example-containment", "version": 1, "digest": DIGEST}
        cases = [None, [], True, "policy", {}, {**valid, "approved": True}]
        cases.extend({key: value for key, value in valid.items() if key != removed}
                     for removed in valid)
        for field, values in (
                ("policy_id", ["", " ", "name\n", "name space", "*", "x?", "[x]", "{x}"]),
                ("version", [True, False, None, "1", 0, -1, 1.5]),
                ("digest", [None, "", "sha256:a", "sha256:" + "A" * 64,
                            DIGEST + "\n", " " + DIGEST,
                            "sha384:" + "B" * 96, "sha384:" + "b" * 95,
                            "sha384:" + "b" * 97, DIGEST384 + "\n",
                            " " + DIGEST384, "sha256:" + "b" * 96])):
            cases.extend({**valid, field: value} for value in values)
        for reference in cases:
            with self.subTest(reference=reference):
                profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
                profile["emergency_policy"] = reference
                self.assertTrue(DECLARATIONS.check(profile))
                self.assertFalse(DEPLOYMENT_VALIDATOR.is_valid(profile))
        for value in (math.nan, math.inf, -math.inf):
            profile = copy.deepcopy(DECLARATIONS.EXAMPLE)
            profile["emergency_policy"] = {**valid, "version": value}
            self.assertTrue(DECLARATIONS.check(profile))

    def test_downstream_vectors_are_requirements_not_runtime_execution(self):
        suite = json.loads(
            (ROOT / "specifications/conformance/outage-safety-v1.json").read_text(),
            parse_constant=CHECKER._reject_constant,
            object_pairs_hook=CHECKER._unique_object)
        self.assertEqual(suite["suite"], "outage-safety-v1")
        self.assertEqual(suite["kind"], "normative-downstream-requirements")
        vectors = suite["vectors"]
        self.assertTrue(vectors)
        self.assertEqual(len(vectors), len({vector["id"] for vector in vectors}))
        for vector in vectors:
            self.assertEqual(set(vector), {"id", "given", "expect", "reason"})
            self.assertTrue(vector["given"])
            self.assertTrue(vector["expect"])
            self.assertTrue(vector["reason"])
        json.dumps(suite, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
