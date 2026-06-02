import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
VALIDATE_SCRIPT = SCRIPTS_DIR / "validate-structure.sh"
COMPARE_SCRIPT = SCRIPTS_DIR / "compare-structure.sh"


def run_bash_script(script_path: Path, arg: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(script_path), arg],
        capture_output=True,
        text=True,
        check=False,
    )


def check_map(result: subprocess.CompletedProcess[str]) -> dict[str, dict]:
    checks = json.loads(result.stdout)
    return {item["check"]: item for item in checks}


class SkillCheckScriptTests(unittest.TestCase):
    def test_validate_detects_unclosed_frontmatter(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "bad-frontmatter"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\nname: bad-frontmatter\ndescription: test\n",
                encoding="utf-8",
            )

            result = run_bash_script(VALIDATE_SCRIPT, str(skill_dir))
            self.assertEqual(result.returncode, 0)

            checks = json.loads(result.stdout)
            frontmatter_close = next(c for c in checks if c["check"] == "frontmatter_closes")
            self.assertFalse(frontmatter_close["pass"])

    def test_validate_requires_use_when_phrase(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "missing-use-when"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: missing-use-when\n"
                "description: Valid grammar but no trigger phrase\n"
                "---\n",
                encoding="utf-8",
            )

            result = run_bash_script(VALIDATE_SCRIPT, str(skill_dir))
            self.assertEqual(result.returncode, 0)

            checks = check_map(result)
            self.assertIn("description_use_when", checks)
            self.assertFalse(checks["description_use_when"]["pass"])

    def test_validate_detects_windows_style_paths_in_body(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "windows-path"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: windows-path\n"
                "description: Use when validating path style in docs\n"
                "---\n\n"
                "Run script at scripts\\helper.py\n",
                encoding="utf-8",
            )

            result = run_bash_script(VALIDATE_SCRIPT, str(skill_dir))
            self.assertEqual(result.returncode, 0)

            checks = check_map(result)
            self.assertIn("no_windows_paths", checks)
            self.assertFalse(checks["no_windows_paths"]["pass"])

    def test_validate_handles_multiline_description_with_quoted_examples(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "quoted-description"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: quoted-description\n"
                "description: >\n"
                "  Build tutorial outputs. Use when: \"teach me X\", \"show me X\",\n"
                "  or \"walk me through\" appears in request context.\n"
                "---\n",
                encoding="utf-8",
            )

            result = run_bash_script(VALIDATE_SCRIPT, str(skill_dir))
            self.assertEqual(result.returncode, 0)

            checks = check_map(result)
            self.assertTrue(checks["frontmatter_parse"]["pass"])
            self.assertTrue(checks["description_use_when"]["pass"])
            self.assertTrue(checks["description_third_person"]["pass"])

    def test_validate_output_json_handles_quoted_path(self):
        with tempfile.TemporaryDirectory(prefix='skill"quoted-') as temp_dir:
            skill_dir = Path(temp_dir)
            (skill_dir / "SKILL.md").write_text(
                "---\nname: test-skill\ndescription: test\n---\n",
                encoding="utf-8",
            )

            result = run_bash_script(VALIDATE_SCRIPT, str(skill_dir))
            self.assertEqual(result.returncode, 0)

            checks = json.loads(result.stdout)
            exists_check = next(c for c in checks if c["check"] == "SKILL.md_exists")
            self.assertIn(str(skill_dir), exists_check["detail"])

    @unittest.skipUnless(shutil.which("jq"), "jq required for compare-structure.sh")
    def test_compare_error_json_escapes_path(self):
        missing_path = '/tmp/not-a-dir-"quoted"'

        result = run_bash_script(COMPARE_SCRIPT, missing_path)
        self.assertEqual(result.returncode, 1)

        error_payload = json.loads(result.stdout)
        self.assertEqual(error_payload["error"], f"{missing_path} is not a directory")

    @unittest.skipUnless(shutil.which("jq"), "jq required for compare-structure.sh")
    def test_compare_score_penalizes_warning(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_dir = Path(temp_dir) / "score-check"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\nname: score-check\ndescription: test\n---\n",
                encoding="utf-8",
            )

            # Found optional dirs present, but no evals dir should produce warning.
            (skill_dir / "scripts").mkdir()
            (skill_dir / "references").mkdir()
            (skill_dir / "assets").mkdir()

            result = run_bash_script(COMPARE_SCRIPT, str(skill_dir))
            self.assertEqual(result.returncode, 0)

            payload = json.loads(result.stdout)
            self.assertEqual(payload["structure_score"], 3)
            self.assertTrue(any("No evals/ directory found" in w for w in payload["warnings"]))


if __name__ == "__main__":
    unittest.main()
