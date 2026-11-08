#!/usr/bin/env python3
"""Source checks render in isolation and propagate gate failures."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("source_checks", Path(__file__).with_name("check-source.py"))

class SourceChecks(unittest.TestCase):
    def exercise(self, gate_status, render_status=0, incomplete_venv=False):
        module = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / "scripts").mkdir()
            (root / "rfcs-md").mkdir()
            generated = root / "rfcs-md/example.md"
            generated.write_text("stale")
            (root / "scripts/gen-rfcs-md.py").write_text(
                "from pathlib import Path\nPath('rfcs-md/example.md').write_text('fresh')\n"
                f"raise SystemExit({render_status})\n")
            (root / "scripts/check-all.sh").write_text(
                "test \"$(cat rfcs-md/example.md)\" = fresh || exit 99\n"
                f"exit {gate_status}\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            if incomplete_venv:
                python = root / ".venv/bin/python3"
                python.parent.mkdir(parents=True)
                python.write_text("#!/bin/sh\nexit 1\n")
                python.chmod(0o755)
                script = root / "scripts/check-all.sh"
                script.write_text("test ! -L .venv || exit 98\n" + script.read_text())
            self.assertEqual(module.check_source(root), render_status or gate_status)
            self.assertEqual(generated.read_text(), "stale")

    def test_render_is_used_without_changing_checkout(self):
        self.exercise(0)

    def test_gate_failure_propagates_without_changing_checkout(self):
        self.exercise(7)

    def test_render_failure_propagates_without_changing_checkout(self):
        self.exercise(0, render_status=9)

    def test_incomplete_environment_is_not_shared(self):
        self.exercise(0, incomplete_venv=True)

if __name__ == "__main__":
    unittest.main()
