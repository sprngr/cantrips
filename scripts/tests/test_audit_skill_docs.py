import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "audit-skill-docs.py"


def run_audit(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=False,
    )


class AuditSkillDocsTests(unittest.TestCase):
    def test_fails_on_frontmatter_parse_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            bad = Path(temp_dir) / "SKILL.md"
            bad.write_text(
                "---\n"
                "name: bad\n"
                "description: Use when: \"bad colon\"\n"
                "---\n",
                encoding="utf-8",
            )

            result = run_audit("--format", "json", "--fail-on-violation", "--files", str(bad))
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["summary"]["files_with_violations"], 1)
            self.assertIn("frontmatter_parse_error", payload["violation_counts"])

    def test_fails_on_windows_style_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            bad = Path(temp_dir) / "SKILL.md"
            bad.write_text(
                "---\n"
                "name: windows-path\n"
                "description: Use when path validation needed\n"
                "---\n\n"
                "Use scripts\\helper.py for parsing.\n",
                encoding="utf-8",
            )

            result = run_audit("--format", "json", "--fail-on-violation", "--files", str(bad))
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertIn("windows_path_detected", payload["violation_counts"])

    def test_warns_on_workflow_summary_language(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill = Path(temp_dir) / "SKILL.md"
            skill.write_text(
                "---\n"
                "name: workflow-summary\n"
                "description: Use when audit needed; first parse then validate then write output\n"
                "---\n",
                encoding="utf-8",
            )

            result = run_audit("--format", "json", "--files", str(skill))
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["summary"]["files_with_violations"], 0)
            self.assertIn("description_workflow_summary", payload["warning_counts"])

    def test_warns_on_nested_reference_depth(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = root / "SKILL.md"
            ref1 = root / "reference.md"
            ref2 = root / "deep.md"

            skill.write_text(
                "---\n"
                "name: nested-ref\n"
                "description: Use when references need chaining checks\n"
                "---\n\n"
                "See [reference](reference.md).\n",
                encoding="utf-8",
            )
            ref1.write_text("See [deep](deep.md).\n", encoding="utf-8")
            ref2.write_text("Deep content\n", encoding="utf-8")

            result = run_audit("--format", "json", "--files", str(skill))
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn("nested_reference_depth", payload["warning_counts"])


if __name__ == "__main__":
    unittest.main()
