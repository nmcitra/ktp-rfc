#!/usr/bin/env python3
"""Checker regressions for the supplier declaration schema in this checkout."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("declarations", Path(__file__).with_name("check-declarations.py"))
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)

class DemandDeclarations(unittest.TestCase):
    def test_example_conforms(self):
        from jsonschema import Draft202012Validator, FormatChecker
        Draft202012Validator(D.PROFILE_SCHEMA, format_checker=FormatChecker()).validate(D.EXAMPLE)
        self.assertEqual(D.check(D.EXAMPLE), [])

    @unittest.skipUnless("supplier_profile" in D.PROFILE_SCHEMA.get("$defs", {}).get("demand_input", {}).get("required", []), "supplier contract not present in this schema")
    def test_supplier_metadata_rejected_when_missing_or_invalid(self):
        mutations = [
            lambda row: row.pop("supplier_profile"),
            lambda row: row["supplier_profile"].update(digest="sha256:bad"),
            lambda row: row["supplier_profile"].update(id="relative/path"),
            lambda row: row["freshness"].update(max_age_seconds=True),
            lambda row: row["freshness"].update(max_age_seconds=0),
            lambda row: row["freshness"].update(clock="local"),
            lambda row: row.update(authoritative_location="request"),
            lambda row: row.update(signals=[]),
            lambda row: row.update(weight=0.5),
            lambda row: row.update(supplier="requester"),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                profile = copy.deepcopy(D.EXAMPLE)
                mutate(profile["demand_inputs"]["moment_criticality"])
                self.assertTrue(D.check(profile))

if __name__ == "__main__":
    unittest.main()
