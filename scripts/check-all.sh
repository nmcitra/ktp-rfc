#!/usr/bin/env bash
# Run every gate CI runs, in the same order, from a clean checkout.
# This is the one command to run before opening a pull request.
# Mirrors .github/workflows/rfc-sync.yml (job: gates) and repo-hygiene.yml.
#
# The conformance tests need three packages. CI installs them into its runner;
# locally this script installs them into a throwaway .venv/ in the repo root
# (ignored by git and by the hygiene check), never into the system Python.
set -euo pipefail
cd "$(dirname "$0")/.."

step() { printf '\n== %s\n' "$1"; }

step "Vocabulary";                       python3 scripts/check-vocabulary.py
step "Parity (rfcs-md/ generation)";     python3 scripts/check-parity.py
step "Repo hygiene";                     python3 scripts/check-repo-hygiene.py
step "Declarations";                     python3 scripts/check-declarations.py

step "Conformance test dependencies"
PY=python3
if ! python3 -c 'import jsonschema, cryptography, rfc8785' 2>/dev/null; then
  [ -x .venv/bin/python3 ] || python3 -m venv .venv
  PY=.venv/bin/python3
  "$PY" -c 'import jsonschema, cryptography, rfc8785' 2>/dev/null \
    || "$PY" -m pip install --quiet jsonschema==4.26.0 cryptography==50.0.1 rfc8785==0.1.4
  echo "using .venv/"
fi

step "Capacity threshold regressions";   "$PY" scripts/test-envelope-thresholds.py
step "Risk Factor weight regressions";   "$PY" scripts/test-risk-factor-weights.py
step "Emergency policy regressions";     "$PY" scripts/test-emergency-policy.py
step "Oracle consensus regressions";     "$PY" scripts/test-oracle-consensus.py
step "Trajectory signature regressions"; "$PY" scripts/test-trajectory-signatures.py
step "Operational readiness regressions"; "$PY" scripts/test-readiness.py
step "Human eligibility regressions";    "$PY" scripts/test-human-eligibility.py
step "Privacy evidence regressions";     "$PY" scripts/test-privacy-evidence.py
step "Catalogue tables";                 python3 scripts/gen-catalog-tables.py --check

printf '\nAll gates green.\n'
