#!/usr/bin/env python3
"""Validate source-only PRs using freshly rendered Markdown in a temporary tree.

Copies tracked working files (including staged additions and local edits), not
untracked files. The original checkout and committed generated views are never
written. Use check-all.sh --release for strict committed-artifact parity before
a tag, after the maintainer regenerates the release documents.
"""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile


def check_source(root):
    paths = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "-z"], text=True).split("\0")
    with tempfile.TemporaryDirectory(prefix="ktp-source-checks-") as temp:
        target = Path(temp)
        for name in filter(None, paths):
            source = root / name
            destination = target / name
            if not source.exists() and not source.is_symlink():
                continue  # Respect tracked working-tree deletions.
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_symlink():
                destination.symlink_to(os.readlink(source))
            else:
                shutil.copy2(source, destination)
        # Hygiene uses the tracked inventory. Stage before generating so newly
        # rendered outputs do not conceal deleted or forbidden tracked files.
        subprocess.run(["git", "init", "-q", str(target)], check=True)
        subprocess.run(["git", "-C", str(target), "add", "--force", "."], check=True)
        # Reuse an already complete environment read-only. If it lacks a new
        # dependency, check-all creates a disposable environment in this tree.
        python = root / ".venv/bin/python3"
        if python.exists() and subprocess.run(
                [str(python), "-c", "import jsonschema, cryptography, rfc8785"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            (target / ".venv").symlink_to((root / ".venv").resolve())
        rendered = subprocess.run(
            [sys.executable, "scripts/gen-rfcs-md.py"], cwd=target)
        if rendered.returncode:
            return rendered.returncode
        return subprocess.run(
            ["bash", "scripts/check-all.sh", "--release"], cwd=target).returncode


if __name__ == "__main__":
    sys.exit(check_source(Path(__file__).resolve().parent.parent))
