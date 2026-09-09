#!/usr/bin/env python3
"""Regression gate for Oracle consensus declarations and quorum arithmetic.

Exercises the actual deployment schema, checker, and CLI. The set model below
enumerates possible signer intersections; it has no cryptography, network,
durable locks, view changes, or membership transition engine. It demonstrates
the old five-node counterexample and a necessary quorum property, not complete
consensus correctness or production availability.

Install jsonschema==4.26.0 in an isolated environment, then run:
    python3 scripts/test-oracle-consensus.py
"""

import copy
import importlib.util
import itertools
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/check-declarations.py"
SPEC = importlib.util.spec_from_file_location("check_declarations", SCRIPT)
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
SCHEMA = json.loads((ROOT / "schemas/deployment-profile.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
DIGEST = "sha256:" + "a" * 64
DIGEST384 = "sha384:" + "b" * 96


def example(count=5, faults=1, quorum=4):
    """A declaration fixture; the protocol and member labels are not evidence."""
    profile = copy.deepcopy(CHECKER.EXAMPLE)
    profile["oracle_consensus"] = {
        "protocol_id": "test-only-protocol-reference",
        "protocol_version": "1.0",
        "protocol_spec_digest": DIGEST,
        "membership_epoch": 1,
        "members": [
            {"node_id": f"node-{index}", "key_id": f"key-{index}",
             "control_domain": f"operator-{index}"}
            for index in range(count)],
        "fault_tolerance": faults,
        "quorum": quorum,
    }
    return profile


def replace(path, value, profile=None):
    candidate = copy.deepcopy(example() if profile is None else profile)
    target = candidate["oracle_consensus"]
    for member in path[:-1]:
        target = target[member]
    target[path[-1]] = value
    return candidate


def abstract_certificate(voters, roster, quorum):
    """Set cardinality only: inputs stand for authenticated eligible voters."""
    identities = set(voters)
    return identities <= set(roster) and len(identities) >= quorum


class OracleConsensusTests(unittest.TestCase):
    def assert_rejected(self, profile, schema=True):
        self.assertTrue(CHECKER.check(profile))
        if schema:
            self.assertFalse(VALIDATOR.is_valid(profile))

    def run_cli(self, contents):
        with tempfile.TemporaryDirectory(prefix="ktp-consensus-test-") as temp:
            path = Path(temp) / "profile.json"
            path.write_text(contents, encoding="utf-8")
            return subprocess.run([sys.executable, str(SCRIPT), "--profile", str(path)],
                                  capture_output=True, text=True, check=False)

    def test_schema_and_valid_configurations(self):
        Draft202012Validator.check_schema(SCHEMA)
        for count, faults, quorum in ((4, 1, 3), (5, 1, 4), (6, 1, 4),
                                      (6, 1, 5), (7, 2, 5)):
            for digest in (DIGEST, DIGEST384):
                with self.subTest(count=count, faults=faults, quorum=quorum,
                                  digest=digest[:7]):
                    profile = example(count, faults, quorum)
                    profile["oracle_consensus"]["protocol_spec_digest"] = digest
                    self.assertTrue(VALIDATOR.is_valid(profile))
                    self.assertEqual(CHECKER.check(profile), [])

    def test_absence_makes_no_mesh_claim_and_null_is_invalid(self):
        profile = copy.deepcopy(CHECKER.EXAMPLE)
        self.assertTrue(VALIDATOR.is_valid(profile))
        self.assertEqual(CHECKER.check(profile), [])
        for value in (None, False, "5-of-7", [], 5):
            profile["oracle_consensus"] = value
            self.assert_rejected(profile)

    def test_known_unsafe_and_unavailable_quorums(self):
        # The shapes pass JSON Schema: cross-field safety/liveness must be
        # checked by the real declaration checker, not by type validation.
        for count, faults, quorum in ((5, 1, 3), (7, 2, 4), (5, 2, 4),
                                      (4, 2, 3), (5, 1, 5), (7, 2, 6)):
            with self.subTest(count=count, faults=faults, quorum=quorum):
                profile = example(count, faults, quorum)
                self.assertTrue(VALIDATOR.is_valid(profile))
                self.assert_rejected(profile, schema=False)

    def test_member_array_and_exact_member_shapes(self):
        for members in (None, {}, "nodes", (), [], example(3)["oracle_consensus"]["members"]):
            with self.subTest(members=members):
                self.assert_rejected(replace(("members",), members))
        for member in (None, "node", [], 1, {},
                       {"node_id": "node", "key_id": "key"}):
            self.assert_rejected(replace(("members", 0), member))
        profile = example()
        profile["oracle_consensus"]["members"][0]["weight"] = 2
        self.assert_rejected(profile)

    def test_identity_uniqueness_is_per_field(self):
        for field in ("node_id", "key_id", "control_domain"):
            with self.subTest(field=field):
                profile = example()
                members = profile["oracle_consensus"]["members"]
                members[1][field] = members[0][field]
                self.assertTrue(VALIDATOR.is_valid(profile))
                self.assert_rejected(profile, schema=False)
        profile = example()
        profile["oracle_consensus"]["members"][1] = copy.deepcopy(
            profile["oracle_consensus"]["members"][0])
        self.assert_rejected(profile)

    def test_integer_controls_reject_hostile_types(self):
        for field in ("membership_epoch", "fault_tolerance", "quorum"):
            for value in (True, False, "1", None, 0, -1, 1.5, [], {}):
                with self.subTest(field=field, value=value):
                    self.assert_rejected(replace((field,), value))
            for value in (1.0, 4.0, math.nan, math.inf, -math.inf):
                with self.subTest(field=field, value=repr(value)):
                    # JSON Schema treats integral floats as integers. The
                    # stdlib checker deliberately requires integer tokens.
                    self.assert_rejected(replace((field,), value), schema=False)

    def test_literal_protocol_and_member_identifiers(self):
        paths = [("protocol_id",), ("protocol_version",),
                 ("members", 0, "node_id"), ("members", 0, "key_id"),
                 ("members", 0, "control_domain")]
        for path in paths:
            for value in ("", " ", "\n", "name\n", "name space", "name\t",
                          "*", "name?", "[name]", "{name}", 1, None, []):
                with self.subTest(path=path, value=repr(value)):
                    self.assert_rejected(replace(path, value))

    def test_digest_requires_exact_algorithm_case_and_length(self):
        for digest in (None, 1, "", "sha256:abc", "sha256:" + "A" * 64,
                       "sha256:" + "a" * 63, "sha256:" + "a" * 65,
                       "sha384:" + "B" * 96, "sha384:" + "b" * 95,
                       "sha384:" + "b" * 97, "sha512:" + "a" * 64,
                       DIGEST + "\n", DIGEST384 + "\n", " " + DIGEST):
            with self.subTest(digest=digest):
                self.assert_rejected(replace(("protocol_spec_digest",), digest))

    def test_required_fields_and_unknown_fields(self):
        for field in example()["oracle_consensus"]:
            with self.subTest(field=field):
                profile = example()
                del profile["oracle_consensus"][field]
                self.assert_rejected(profile)
        profile = example()
        profile["oracle_consensus"]["outage_quorum"] = 3
        self.assert_rejected(profile)

    def test_validation_does_not_repair_or_mutate_declarations(self):
        for profile in (example(), example(5, 1, 3)):
            original = copy.deepcopy(profile)
            CHECKER.check(profile)
            self.assertEqual(profile, original)

    def test_cli_checks_math_and_describes_its_limits(self):
        valid = self.run_cli(json.dumps(example()))
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        self.assertIn("runtime consensus are not certified", valid.stdout)
        invalid = self.run_cli(json.dumps(example(5, 1, 3)))
        self.assertEqual(invalid.returncode, 1, invalid.stdout + invalid.stderr)
        self.assertIn("oracle_consensus", invalid.stdout)
        generic = self.run_cli(json.dumps(CHECKER.EXAMPLE))
        self.assertEqual(generic.returncode, 0, generic.stdout + generic.stderr)

    def test_cli_rejects_ambiguous_and_non_json_input_cleanly(self):
        encoded = json.dumps(example())
        invalid_inputs = [
            encoded.replace('"quorum": 4', '"quorum": 3, "quorum": 4'),
            encoded.replace('"node_id": "node-0"',
                            '"node_id": "node-x", "node_id": "node-0"'),
            encoded.replace('"quorum": 4', '"quorum": NaN'),
            encoded.replace('"quorum": 4', '"quorum": Infinity'),
            encoded.replace('"quorum": 4', '"quorum": -Infinity'),
            encoded.replace('"quorum": 4', '"quorum": 1e309'),
            encoded.replace('"quorum": 4', '"quorum": 4.0'),
            '{"oracle_consensus":',
        ]
        for contents in invalid_inputs:
            with self.subTest(contents=contents[-70:]):
                result = self.run_cli(contents)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("DECLARATIONS INVALID", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_five_node_equivocation_counterexample(self):
        roster = {"A", "B", "C", "D", "X"}
        first, second = {"A", "B", "X"}, {"C", "D", "X"}
        self.assertEqual(first & second, {"X"})
        self.assertTrue(abstract_certificate(first, roster, 3))
        self.assertTrue(abstract_certificate(second, roster, 3))
        self.assertFalse(abstract_certificate(first, roster, 4))
        self.assertFalse(abstract_certificate(second, roster, 4))
        # No honest voter needs to vote for both conflicting proposals in
        # this counterexample. X alone can support each proposal.
        self.assertFalse((first - {"X"}) & (second - {"X"}))

    def test_all_small_quorum_pairs_match_checker_safety_and_availability(self):
        checked = 0
        for count in range(4, 10):
            roster = range(count)
            for quorum in range(1, count + 1):
                groups = [frozenset(group) for group in
                          itertools.combinations(roster, quorum)]
                smallest_intersection = min(
                    len(left & right) for left, right in
                    itertools.combinations_with_replacement(groups, 2))
                for faults in range(1, 4):
                    # Derive safety from actual enumerated voter sets and
                    # availability from the remaining honest voter count.
                    safe = smallest_intersection > faults
                    available = quorum <= count - faults
                    profile = example(count, faults, quorum)
                    self.assertEqual(not CHECKER.check(profile), safe and available,
                                     (count, faults, quorum, smallest_intersection))
                    checked += 1
        self.assertEqual(checked, 117)

    def test_duplicate_messages_and_unknown_voters_do_not_make_a_quorum(self):
        roster = {"A", "B", "C", "D", "X"}
        self.assertFalse(abstract_certificate(["X"] * 100, roster, 4))
        self.assertFalse(abstract_certificate(["A", "B", "X", "X"], roster, 4))
        self.assertFalse(abstract_certificate(["A", "B", "C", "outsider"], roster, 4))
        self.assertTrue(abstract_certificate(["A", "B", "C", "D"], roster, 4))

    def test_one_fault_budget_does_not_promise_two_unavailable_members(self):
        roster = {"A", "B", "C", "D", "X"}
        self.assertTrue(abstract_certificate(roster - {"X"}, roster, 4))
        self.assertFalse(abstract_certificate(roster - {"D", "X"}, roster, 4))


if __name__ == "__main__":
    unittest.main(verbosity=2)
