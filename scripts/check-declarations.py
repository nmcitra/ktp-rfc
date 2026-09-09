#!/usr/bin/env python3
"""Validate a deployment profile against the catalogue — the conformance
instrument for specifications/deployment-profile.md (#108).

The JSON Schema (schemas/deployment-profile.json) constrains shape; this
script checks what a schema cannot — the joins against catalog/, which stays
the single source of every identifier list so the profile schema never grows
a second copy of them:

  1. shape — required sections, the #83 arity (six factors + soul_veto),
     field types and ranges (stdlib only; run any 2020-12 validator for the
     full schema when one is available)
  2. existence — every declared signal ID resolves in catalog/*.json
  3. aliases — no aggregation includes more than one member of an alias set,
     and every populated set is declared under `aliases` with a member of
     that set
  4. normalization — every aggregated zero_one:"synthetic" signal has a
     normalization entry
  5. envelope_thresholds — finite numbers, 0 <= m_veto < m_allow
     where declared; omission retains the zero-threshold default
  6. risk-factor weights — six finite numbers in (0, 1], whose parsed
     decimal representations sum exactly to 1; never silently rescaled
  7. emergency_policy — optional exact policy ID/version/digest reference;
     this checks its shape, not approval or activation
  8. oracle_consensus — optional exact protocol and membership declaration;
     distinct identities and safe/live quorum bounds, not engine correctness
  9. standing_policy — required exact scoped-readiness profile binding;
     legacy standing_decay_rate is invalid in the active v3 profile
 10. human_policy — exact operation-specific profile binding when declared;
     omission disables human eligibility, not a legacy score fallback

Usage:  python3 scripts/check-declarations.py --profile <profile.json>
Exit 1 on any failure. With no --profile, self-checks against the worked
example embedded below (which doubles as documentation of the shape).
"""

import argparse
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
DOMAINS = ["world", "information", "time", "soul", "relational", "body",
           "meta"]
FACTORS = ["evidence_density", "trust_trend", "adversarial_pressure",
           "update_resistance", "attestation_coverage", "moment_criticality"]

EXAMPLE = {
    "profile_id": "example-minimal",
    "version": 1,
    "risk_factors": {
        "evidence_density": {
            "signals": ["soul.temporal.action_rate",
                        "relational.trust.outbound_mean"],
            "aggregation": {"method": "weighted_average",
                            "parameters": {"weights": [0.6, 0.4]}},
            "weight": 0.25},
        "trust_trend": {
            "signals": ["soul.temporal.pattern_stability"],
            "aggregation": {"method": "weighted_average"},
            "weight": 0.15},
        "adversarial_pressure": {
            "signals": ["world.security.anomaly_score"],
            "aggregation": {"method": "max"},
            "weight": 0.2},
        "update_resistance": {
            "signals": ["soul.consistency.behavioral_drift_rate"],
            "aggregation": {"method": "weighted_average"},
            "weight": 0.1},
        "attestation_coverage": {
            "signals": ["body.hardware.bmc_reachable"],
            "aggregation": {"method": "min"},
            "weight": 0.15},
        "moment_criticality": {
            "signals": ["time.window.business_hours_active"],
            "aggregation": {"method": "max"},
            "weight": 0.15},
    },
    "soul_veto": {"frameworks": ["example-sovereignty-registry"]},
    "feeds": {"feed-01": {"populates": ["world.security.anomaly_score"]}},
    "aliases": {"business_hours_active": "time.window.business_hours_active"},
    "normalization": {
        "world.security.anomaly_score": {
            "method": "min-max",
            "parameters": {"source_range": [0, 100]}},
        "soul.temporal.pattern_stability": {
            "method": "vendor-documented",
            "parameters": {"reference": "example"}},
        "relational.trust.outbound_mean": {
            "method": "min-max",
            "parameters": {"source_range": [0, 1],
                           "edge_value_normalization": "declared with the "
                           "edge value it averages — a derived statistic "
                           "inherits the obligation of the quantity it "
                           "summarizes"}}},
    "peer_share": 0,
    "external_root": {"hop_bound": 3, "adjudicator": "example-adjudicator"},
    # Shape-only illustrative binding; the all-zero digest is not evidence
    # that any readiness profile exists, is approved, or permits execution.
    "standing_policy": {
        "mode": "history-with-scoped-readiness-v1",
        "profile_id": "example-readiness",
        "version": 1,
        "digest": "sha256:" + "0" * 64,
    },
    "envelope_thresholds": {"m_veto": 0.0, "m_allow": 0.2},
}


def load_catalogue():
    ids, synthetic = set(), set()
    for dom in DOMAINS:
        doc = json.loads((CATALOG / f"{dom}.json").read_text())
        for g in doc["groups"]:
            for s in g["signals"]:
                ids.add(s["id"])
                if s.get("zero_one") == "synthetic":
                    synthetic.add(s["id"])
    index = json.loads((CATALOG / "index.json").read_text())
    sets = {}
    for a in index["alias_sets"]:
        members = (a.get("canonical", []) + a.get("aliases", [])
                   + a.get("members", []))
        sets[a["set"]] = set(members)
    return ids, synthetic, sets


def check(profile):
    fails = []
    if not isinstance(profile, dict):
        return ["shape: deployment profile must be an object"]
    ids, synthetic, alias_sets = load_catalogue()

    # 1 · shape
    for key in ["profile_id", "version", "risk_factors", "soul_veto",
                "peer_share", "external_root", "standing_policy"]:
        if key not in profile:
            fails.append(f"shape: required section '{key}' missing")
    declared_rf = profile.get("risk_factors", {})
    if not isinstance(declared_rf, dict):
        fails.append("shape: risk_factors must be an object containing the "
                     "six weighted inputs")
        return fails
    for f in FACTORS:
        if f not in declared_rf:
            fails.append(f"shape: risk factor '{f}' missing — the #83 arity "
                         "is six weighted inputs plus the Soul veto")
    for f in set(declared_rf) - set(FACTORS):
        fails.append(f"shape: '{f}' is not one of the six Risk Factors")
    # Later catalogue checks only inspect known factors with object shapes.
    # Malformed declarations still fail; filtering never repairs the profile.
    rf, weights = {}, []
    for f, spec in declared_rf.items():
        if f not in FACTORS:
            continue
        if not isinstance(spec, dict):
            fails.append(f"shape: risk factor '{f}' must be an object")
            continue
        rf[f] = spec
        for k in ("signals", "aggregation", "weight"):
            if k not in spec:
                fails.append(f"shape: {f} missing '{k}'")
        aggregation = spec.get("aggregation")
        if not isinstance(aggregation, dict) or not aggregation.get("method"):
            fails.append(f"shape: {f} aggregation has no method")
        w = spec.get("weight")
        if not ((type(w) is int or
                 (type(w) is float and math.isfinite(w))) and 0 < w <= 1):
            fails.append(f"weights: {f} weight must be a finite number in "
                         "(0, 1]; booleans are not numbers")
        else:
            weights.append(Fraction(str(w)))
    if len(weights) == len(FACTORS):
        # Exact decimal arithmetic avoids both binary summation noise and
        # an epsilon that accepts a non-unit total. The JSON parser has
        # already resolved each number; this does not preserve token text.
        total = sum(weights, Fraction(0))
        if total != 1:
            fails.append("weights: the six Risk Factor weights must sum "
                         f"exactly to 1 (parsed decimal total: {total}); "
                         "invalid weights are not rescaled (ktp-core 6.4)")
    if "soul_veto" in profile and not profile["soul_veto"].get("frameworks"):
        fails.append("shape: soul_veto.frameworks empty — the veto needs at "
                     "least one framework to query")
    ps = profile.get("peer_share")
    if ps is not None and ps != 0 and not (
            isinstance(ps, (int, float)) and 10 <= ps <= 20):
        fails.append(f"shape: peer_share {ps!r} is neither 0 nor in [10, 20] "
                     "(ktp-core 5.5.5)")
    er = profile.get("external_root", {})
    hb = er.get("hop_bound")
    if hb is not None and not (isinstance(hb, int) and 1 <= hb <= 12):
        fails.append(f"shape: hop_bound {hb!r} not an integer in [1, 12]")
    if "external_root" in profile and not er.get("adjudicator"):
        fails.append("shape: external_root.adjudicator missing")
    if "standing_decay_rate" in profile:
        fails.append("standing_policy: legacy standing_decay_rate is invalid "
                     "in v3; an approved scoped-readiness profile binding "
                     "is required")

    # 2 · existence
    declared = []
    for f, spec in rf.items():
        for s in spec.get("signals", []):
            declared.append((f"risk_factors.{f}", s))
    for fid, fe in profile.get("feeds", {}).items():
        for s in fe.get("populates", []):
            declared.append((f"feeds.{fid}", s))
    for where, s in declared:
        if s not in ids:
            fails.append(f"existence: {where} names '{s}', not in catalog/")
    for s in list(profile.get("normalization", {})) \
            + list(profile.get("label_sets", {})):
        if s not in ids:
            fails.append(f"existence: '{s}' (normalization/label_sets) "
                         "not in catalog/")

    # 3 · aliases
    for f, spec in rf.items():
        sigs = set(spec.get("signals", []))
        for name, members in alias_sets.items():
            hit = sigs & members
            if len(hit) > 1:
                fails.append(f"alias: risk_factors.{f} aggregates "
                             f"{sorted(hit)} — more than one member of alias "
                             f"set '{name}' (catalog/index.md §7 MUST NOT)")
    populated = {s for _, s in declared}
    for name, members in alias_sets.items():
        used = populated & members
        if used:
            decl = profile.get("aliases", {}).get(name)
            if decl is None:
                fails.append(f"alias: set '{name}' is populated "
                             f"({sorted(used)}) but not declared under "
                             "'aliases' (NORMALIZATION-01 §A MUST)")
            elif decl not in members:
                fails.append(f"alias: aliases.{name} = '{decl}' is not a "
                             f"member of that set")
    for name in profile.get("aliases", {}):
        if name not in alias_sets:
            fails.append(f"alias: aliases.{name} names no alias set in "
                         "catalog/index.json")

    # 4 · normalization coverage
    norm = profile.get("normalization", {})
    aggregated = {s for f, spec in rf.items() for s in spec.get("signals", [])}
    for s in sorted(aggregated & synthetic):
        if s not in norm:
            fails.append(f"normalization: '{s}' is zero_one:synthetic and "
                         "aggregated, but declares no normalization function "
                         "(catalog/index.md §6 MUST)")

    # 5 · thresholds
    if "envelope_thresholds" in profile:
        et = profile["envelope_thresholds"]
        if not isinstance(et, dict):
            fails.append("thresholds: envelope_thresholds must be an object; "
                         "omit the section to use the default")
        else:
            if set(et) != {"m_veto", "m_allow"}:
                fails.append("thresholds: exactly m_veto and m_allow are "
                             "required")
            values = (et.get("m_veto"), et.get("m_allow"))
            # bool is an int subclass, but not a JSON number. Test ints
            # without float conversion so large finite integers stay valid.
            if not all(type(v) is int or
                       (type(v) is float and math.isfinite(v))
                       for v in values):
                fails.append("thresholds: m_veto/m_allow must both be finite "
                             "numbers (booleans are not numbers)")
            elif not 0 <= values[0] < values[1]:
                fails.append("thresholds: require 0 <= m_veto < m_allow "
                             f"(got {values[0]!r}, {values[1]!r}); profile "
                             "thresholds cannot relax the capacity veto "
                             "(ktp-core 6.6)")

    # 7 · emergency policy binding: absence disables the capability.
    # Approval and protected installation are separate runtime obligations.
    if "emergency_policy" in profile:
        emergency = profile["emergency_policy"]
        if not isinstance(emergency, dict):
            fails.append("emergency_policy: must be an ID/version/digest "
                         "object; omission disables the capability")
        else:
            if set(emergency) != {"policy_id", "version", "digest"}:
                fails.append("emergency_policy: exactly policy_id, version, "
                             "and digest are required")
            policy_id = emergency.get("policy_id")
            if not isinstance(policy_id, str) or not policy_id or re.search(
                    r"[\s*?\[\]{}]", policy_id):
                fails.append("emergency_policy: policy_id must be a "
                             "nonempty literal without whitespace or wildcards")
            version = emergency.get("version")
            if type(version) is not int or version < 1:
                fails.append("emergency_policy: version must be a positive integer")
            digest = emergency.get("digest")
            if not isinstance(digest, str) or not re.fullmatch(
                    r"sha(?:256:[0-9a-f]{64}|384:[0-9a-f]{96})", digest):
                fails.append("emergency_policy: digest must be sha256: "
                             "with 64 or sha384: with 96 lowercase hexadecimal digits")

    # 8 · consensus declaration: omission makes no Byzantine mesh claim.
    # Counting declared identities does not establish their real independence,
    # authenticate votes, or verify the referenced consensus implementation.
    if "oracle_consensus" in profile:
        consensus = profile["oracle_consensus"]
        fields = {"protocol_id", "protocol_version", "protocol_spec_digest",
                  "membership_epoch", "members", "fault_tolerance", "quorum"}
        if not isinstance(consensus, dict):
            fails.append("oracle_consensus: must be a protocol/membership "
                         "object; omission makes no Byzantine mesh claim")
        else:
            if set(consensus) != fields:
                fails.append("oracle_consensus: exactly protocol_id, "
                             "protocol_version, protocol_spec_digest, "
                             "membership_epoch, members, fault_tolerance, "
                             "and quorum are required")
            for field in ("protocol_id", "protocol_version"):
                value = consensus.get(field)
                if not isinstance(value, str) or not value or re.search(
                        r"[\s*?\[\]{}]", value):
                    fails.append(f"oracle_consensus: {field} must be a "
                                 "nonempty literal without whitespace or wildcards")
            digest = consensus.get("protocol_spec_digest")
            if not isinstance(digest, str) or not re.fullmatch(
                    r"sha(?:256:[0-9a-f]{64}|384:[0-9a-f]{96})", digest):
                fails.append("oracle_consensus: protocol_spec_digest must be "
                             "sha256: with 64 or sha384: with 96 lowercase "
                             "hexadecimal digits")
            controls = {}
            for field in ("membership_epoch", "fault_tolerance", "quorum"):
                value = consensus.get(field)
                if type(value) is not int or value < 1:
                    fails.append(f"oracle_consensus: {field} must be a "
                                 "positive integer; booleans and floats are invalid")
                else:
                    controls[field] = value
            members = consensus.get("members")
            if not isinstance(members, list):
                fails.append("oracle_consensus: members must be an array")
            else:
                count = len(members)
                if count < 4:
                    fails.append("oracle_consensus: at least four members "
                                 "are required for a Byzantine mesh declaration")
                member_fields = {"node_id", "key_id", "control_domain"}
                seen = {field: set() for field in member_fields}
                for index, member in enumerate(members):
                    if not isinstance(member, dict):
                        fails.append(f"oracle_consensus: members[{index}] "
                                     "must be an object")
                        continue
                    if set(member) != member_fields:
                        fails.append(f"oracle_consensus: members[{index}] "
                                     "requires exactly node_id, key_id, and control_domain")
                    for field in sorted(member_fields):
                        value = member.get(field)
                        if not isinstance(value, str) or not value or re.search(
                                r"[\s*?\[\]{}]", value):
                            fails.append(f"oracle_consensus: members[{index}].{field} "
                                         "must be a nonempty literal without "
                                         "whitespace or wildcards")
                        elif value in seen[field]:
                            fails.append(f"oracle_consensus: {field} {value!r} "
                                         "is repeated; each identity must be distinct")
                        else:
                            seen[field].add(value)
                if "fault_tolerance" in controls and "quorum" in controls:
                    faults, quorum = controls["fault_tolerance"], controls["quorum"]
                    minimum = (count + faults) // 2 + 1
                    maximum = count - faults
                    if count < 3 * faults + 1:
                        fails.append("oracle_consensus: N must be at least "
                                     "3 * fault_tolerance + 1")
                    if not minimum <= quorum <= maximum:
                        fails.append("oracle_consensus: quorum must satisfy "
                                     "floor((N + fault_tolerance) / 2) + 1 "
                                     f"<= quorum <= N - fault_tolerance "
                                     f"(for N={count}, f={faults}: "
                                     f"{minimum} <= quorum <= {maximum}); "
                                     "unsafe or unavailable configurations are rejected")

    # 9/10 · Profile bindings. Shape checks do not authenticate installation,
    # current eligibility/readiness, governance approval, or ordinary authority.
    for policy_name, required_mode in (
            ("standing_policy", "history-with-scoped-readiness-v1"),
            ("human_policy", "operation-eligibility-v1")):
        if policy_name not in profile:
            continue  # standing_policy missing is rejected by required checks above
        binding = profile[policy_name]
        if not isinstance(binding, dict):
            fails.append(f"{policy_name}: must be an exact "
                         "mode/profile_id/version/digest object")
            continue
        if set(binding) != {"mode", "profile_id", "version", "digest"}:
            fails.append(f"{policy_name}: exactly mode, profile_id, "
                         "version, and digest are required")
        if binding.get("mode") != required_mode:
            fails.append(f"{policy_name}: mode must be {required_mode}")
        profile_id = binding.get("profile_id")
        if not isinstance(profile_id, str) or not profile_id or re.search(
                r"[\s*?\[\]{}]", profile_id):
            fails.append(f"{policy_name}: profile_id must be a "
                         "nonempty literal without whitespace or wildcards")
        version = binding.get("version")
        if type(version) is not int or not 1 <= version <= 9007199254740991:
            fails.append(f"{policy_name}: version must be a positive "
                         "safe integer token; booleans and floats are invalid")
        digest = binding.get("digest")
        if not isinstance(digest, str) or not re.fullmatch(
                r"sha(?:256:[0-9a-f]{64}|384:[0-9a-f]{96})", digest):
            fails.append(f"{policy_name}: digest must be sha256: "
                         "with 64 or sha384: with 96 lowercase hexadecimal digits")

    return fails


def reject_duplicate_keys(pairs):
    """Reject ambiguous declarations before any field can overwrite another."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_nonfinite_constant(value):
    raise ValueError(f"non-finite JSON constant: {value}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", help="profile JSON to validate; omit to "
                    "self-check the embedded example")
    args = ap.parse_args()
    if args.profile:
        label = args.profile
        try:
            profile = json.loads(
                Path(args.profile).read_text(encoding="utf-8"),
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=reject_nonfinite_constant)
        except (OSError, UnicodeError, ValueError) as error:
            print(f"DECLARATIONS INVALID — {label}")
            print(f"  FAIL JSON: {error}")
            sys.exit(1)
    else:
        profile = EXAMPLE
        label = "embedded example"
    fails = check(profile)
    if fails:
        print(f"DECLARATIONS INVALID — {label}")
        for f in fails:
            print("  FAIL", f)
        sys.exit(1)
    print(f"declarations valid — {label} "
          f"(profile {profile['profile_id']}@{profile['version']})")
    print("  Standing-policy declaration only; profile approval, verified "
          "readiness, and current authority are not certified.")
    if "oracle_consensus" in profile:
        print("  Declaration checks only; protocol review, signature validity, "
              "member independence, and runtime consensus are not certified.")


if __name__ == "__main__":
    main()
