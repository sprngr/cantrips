import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "import-plan.sh"


def run_import(plan_path: str | None = None) -> subprocess.CompletedProcess[str]:
    command = ["bash", str(SCRIPT_PATH)]
    if plan_path is not None:
        command.append(plan_path)
    return subprocess.run(command, capture_output=True, text=True, check=False)


class ImportPlanScriptTests(unittest.TestCase):
    def test_missing_arg_returns_usage_exit_code(self):
        result = run_import()
        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage:", result.stderr)

    def test_output_is_json_with_special_characters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            plan_file = Path(temp_dir) / ".skill-plan.yaml"
            plan_file.write_text(
                """
intent: "line1\nline2 = keep"
scope: single
mechanism: reasoning
context_assets:
  - templates
  - checklists
target_path: "skills/forge/"
tier: A
workflow_notes:
  - "first = thing"
  - "second: item"
turns:
  - turn: 1
    question: "q"
    answer: "a"
completed: true
""".lstrip(),
                encoding="utf-8",
            )

            result = run_import(str(plan_file))
            self.assertEqual(result.returncode, 0, msg=result.stderr)

            payload = json.loads(result.stdout)
            self.assertEqual(payload["scope"], "single")
            self.assertEqual(payload["mechanism"], "reasoning")
            self.assertTrue(payload["completed"])
            self.assertIn("line2 = keep", payload["intent"])
            self.assertIn("first = thing", payload.get("workflow_notes", ""))

    def test_incomplete_plan_keeps_exit_code_four(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            plan_file = Path(temp_dir) / ".skill-plan.yaml"
            plan_file.write_text(
                """
intent: "test"
scope: single
mechanism: reasoning
context_assets: none
target_path: "skills/forge/"
tier: A
completed: false
""".lstrip(),
                encoding="utf-8",
            )

            result = run_import(str(plan_file))
            self.assertEqual(result.returncode, 4)
            self.assertIn("completed must be true", result.stderr)


if __name__ == "__main__":
    unittest.main()
