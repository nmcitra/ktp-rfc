#!/usr/bin/env python3
"""Validate a deployment profile against the catalogue — the conformance
instrument for docs/specifications/deployment-profile.md (#108).

The JSON Schema (docs/schemas/deployment-profile.json) constrains shape; this
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
  5. envelope_thresholds — m_veto < m_allow where declared

Usage:  python3 scripts/check-declarations.py --profile <profile.json>
Exit 1 on any failure. With no --profile, self-checks against the worked
example embedded below (which doubles as documentation of the shape).
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog"
DOMAINS = ["world", "information", "time", "soul", "relational", "body"]
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
    "standing_decay_rate": 16,
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
    ids, synthetic, alias_sets = load_catalogue()

    # 1 · shape
    for key in ["profile_id", "version", "risk_factors", "soul_veto",
                "peer_share", "external_root", "standing_decay_rate"]:
        if key not in profile:
            fails.append(f"shape: required section '{key}' missing")
    rf = profile.get("risk_factors", {})
    for f in FACTORS:
        if f not in rf:
            fails.append(f"shape: risk factor '{f}' missing — the #83 arity "
                         "is six weighted inputs plus the Soul veto")
    for f in set(rf) - set(FACTORS):
        fails.append(f"shape: '{f}' is not one of the six Risk Factors")
    for f, spec in rf.items():
        if f not in FACTORS:
            continue
        for k in ("signals", "aggregation", "weight"):
            if k not in spec:
                fails.append(f"shape: {f} missing '{k}'")
        if not spec.get("aggregation", {}).get("method"):
            fails.append(f"shape: {f} aggregation has no method")
        w = spec.get("weight")
        if not (isinstance(w, (int, float)) and 0 < w <= 1):
            fails.append(f"shape: {f} weight {w!r} not in (0, 1]")
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
    d = profile.get("standing_decay_rate")
    if d is not None and not (isinstance(d, (int, float)) and 2 <= d <= 20):
        fails.append(f"shape: standing_decay_rate {d!r} not in [2, 20] (#59)")

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
    et = profile.get("envelope_thresholds")
    if et is not None:
        if not (isinstance(et.get("m_veto"), (int, float))
                and isinstance(et.get("m_allow"), (int, float))):
            fails.append("thresholds: m_veto/m_allow must both be numbers")
        elif not et["m_veto"] < et["m_allow"]:
            fails.append(f"thresholds: m_veto ({et['m_veto']}) must be "
                         f"< m_allow ({et['m_allow']}) (ktp-core 6.6)")

    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", help="profile JSON to validate; omit to "
                    "self-check the embedded example")
    args = ap.parse_args()
    if args.profile:
        profile = json.loads(Path(args.profile).read_text())
        label = args.profile
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


if __name__ == "__main__":
    main()
