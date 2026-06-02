import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "grade_assertions.py"
SPEC = importlib.util.spec_from_file_location("grade_assertions", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load module spec from {SCRIPT_PATH}")
grade_assertions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(grade_assertions)


class GradeAssertionsTests(unittest.TestCase):
    def test_classify_prefers_contains_over_count_keywords(self):
        self.assertEqual(
            grade_assertions.classify_assertion("Output contains 'ready'"),
            "contains",
        )
        self.assertEqual(
            grade_assertions.classify_assertion("Result has 'summary' label"),
            "contains",
        )

    def test_classify_count_keywords_still_route_to_count(self):
        self.assertEqual(
            grade_assertions.classify_assertion("Produces at least 3 files"),
            "count",
        )

    def test_check_contains_fails_when_target_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "output.txt"
            output_file.write_text("alpha beta gamma", encoding="utf-8")

            passed, evidence = grade_assertions.check_contains(
                "Output contains 'delta'",
                temp_dir,
            )

            self.assertFalse(passed)
            self.assertIn("not found", evidence)

    def test_check_contains_fails_without_quoted_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "output.txt"
            output_file.write_text("alpha beta gamma", encoding="utf-8")

            passed, evidence = grade_assertions.check_contains(
                "Output contains delta",
                temp_dir,
            )

            self.assertFalse(passed)
            self.assertIn("No quoted target", evidence)

    def test_check_contains_passes_when_target_present(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "output.txt"
            output_file.write_text("final report includes summary block", encoding="utf-8")

            passed, evidence = grade_assertions.check_contains(
                "Output contains 'summary block'",
                temp_dir,
            )

            self.assertTrue(passed)
            self.assertIn("found", evidence)


if __name__ == "__main__":
    unittest.main()
