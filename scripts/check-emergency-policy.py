#!/usr/bin/env python3
"""Validate an emergency policy declaration, not its authorization.

The actual Draft 2020-12 schema constrains shape. Additional checks enforce
finite JSON values, individually unique custodian identities, count-relative
thresholds, unique action identifiers, and predecessor syntax. A candidate's
valid shape never proves incumbent approval or permits activation/execution.

Install jsonschema==4.26.0 in an isolated environment, then run:
    python3 scripts/check-emergency-policy.py --policy <policy.json>
Exit 1 on malformed input or any declaration failure.
"""

import argparse
import json
import math
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schemas/emergency-policy.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)
VALID_MESSAGE = ("declaration valid; approval, signatures, activation, and "
                 "runtime enforcement are not verified")


def _json_failures(value, path="$", active=None):
    """Reject Python-only values and nonfinite parser results before schema use."""
    if active is None:
        active = set()
    if value is None or type(value) in (str, bool, int):
        return []
    if type(value) is float:
        return [] if math.isfinite(value) else [f"{path}: number must be finite"]
    if type(value) not in (dict, list):
        return [f"{path}: value is not a JSON type"]
    identity = id(value)
    if identity in active:
        return [f"{path}: cyclic value is not JSON"]
    active.add(identity)
    failures = []
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                failures.append(f"{path}: object keys must be strings")
            else:
                failures.extend(_json_failures(item, f"{path}.{key}", active))
    else:
        for index, item in enumerate(value):
            failures.extend(_json_failures(item, f"{path}[{index}]", active))
    active.remove(identity)
    return failures


def check(policy):
    """Return declaration failures without modifying or approving the policy."""
    failures = _json_failures(policy)
    if failures:
        return failures
    for error in VALIDATOR.iter_errors(policy):
        path = "$" + "".join(f"[{part}]" if isinstance(part, int)
                             else f".{part}" for part in error.absolute_path)
        failures.append(f"{path}: {error.message}")
    if failures:
        return failures

    roster = policy["custodians"]
    count = len(roster)
    for field in ("principal_id", "key_id", "control_domain"):
        values = [custodian[field] for custodian in roster]
        if len(set(values)) != count:
            failures.append(f"custodians: {field} must be unique for each custodian")

    # Integer arithmetic avoids rounding 90% below the next whole custodian.
    minimum_approvals = max(3, (9 * count + 9) // 10)
    threshold = policy["change_control"]["approval_threshold"]
    if not minimum_approvals <= threshold <= count:
        failures.append("change_control.approval_threshold: must be between "
                        f"{minimum_approvals} and {count} for the full roster")
    if policy["activation"]["threshold"] > count:
        failures.append("activation.threshold: exceeds the full custodian roster")

    action_ids = [action["action_id"] for action in policy["actions"]]
    if len(set(action_ids)) != len(action_ids):
        failures.append("actions: action_id must be unique")
    # This relation is also expressed in the schema; no chain state is read.
    if (policy["version"] == 1) != (policy["predecessor_digest"] is None):
        failures.append("predecessor_digest: null if and only if version is 1")
    return failures


def _reject_constant(token):
    raise ValueError(f"non-JSON numeric constant: {token}")


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object member: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", required=True, type=Path)
    args = parser.parse_args()
    try:
        policy = json.loads(args.policy.read_text(encoding="utf-8"),
                            parse_constant=_reject_constant,
                            object_pairs_hook=_unique_object)
        failures = check(policy)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        print(f"Invalid emergency policy: {error}", file=sys.stderr)
        return 1
    if failures:
        for failure in failures:
            print(f"Invalid emergency policy: {failure}", file=sys.stderr)
        return 1
    print(VALID_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
