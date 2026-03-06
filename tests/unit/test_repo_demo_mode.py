from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestRepoDemoMode(unittest.TestCase):
    def test_problem_statement_present(self) -> None:
        content = (REPO_ROOT / "05-problem-statement.txt").read_text(encoding="utf-8")
        self.assertIn("Top 3 pain points", content)

    def test_migrations_present(self) -> None:
        ups = sorted((REPO_ROOT / "migrations").glob("*.up.sql"))
        self.assertGreaterEqual(len(ups), 3)

    def test_gitops_validation_runs(self) -> None:
        subprocess.run([sys.executable, "scripts/gitops_validate.py"], cwd=str(REPO_ROOT), check=True)

    def test_notice_present(self) -> None:
        notice = (REPO_ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("CloudForgeLabs", notice)
        self.assertIn("Freddy D. Alvarez", notice)

