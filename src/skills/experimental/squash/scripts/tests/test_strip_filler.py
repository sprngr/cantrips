import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "strip-filler.sh"


def run_strip(*args: str, stdin_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SCRIPT_PATH), *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        check=False,
    )


class StripFillerScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not SCRIPT_PATH.exists():
            raise RuntimeError(f"Missing script: {SCRIPT_PATH}")

    def test_usage_rejects_multiple_args(self):
        result = run_strip("a.txt", "b.txt")
        self.assertEqual(result.returncode, 64)
        self.assertIn("Usage:", result.stderr)

    def test_removes_single_fillers_from_stdin(self):
        result = run_strip(stdin_text="This is really just useful.")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "This is useful.")

    def test_removes_phrase_fillers_from_file_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "input.txt"
            input_file.write_text("It is kind of slow but sort of stable.", encoding="utf-8")

            result = run_strip(str(input_file))
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(result.stdout.strip(), "It is slow but stable.")

    def test_keeps_non_filler_words(self):
        result = run_strip(stdin_text="Justification and sorting stay.")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "Justification and sorting stay.")

    def test_keeps_kind_when_not_phrase(self):
        result = run_strip(stdin_text="This kind behavior stays.")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "This kind behavior stays.")

    def test_preserves_fence_marker_lines(self):
        text = "```python\n```\nThis is really clear."
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "```python\n```\nThis is clear.")

    def test_collapses_excess_blank_lines(self):
        result = run_strip(stdin_text="One.\n\n\nTwo.")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.strip(), "One.\n\nTwo.")

    def test_preserves_indentation_on_following_lines(self):
        result = run_strip(stdin_text="Header\n  This is really useful.")
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.rstrip("\n"), "Header\n  This is useful.")

    def test_preserves_absolute_and_relative_paths(self):
        text = (
            "Path: /mnt/f/workspace/cantrips/skills/experimental/squash/SKILL.md\n"
            "Rel: skills/experimental/squash/scripts/strip-filler.sh"
        )
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(result.stdout.rstrip("\n"), text)

    def test_preserves_urls(self):
        text = "Doc: https://www.nltk.org/index.html is really useful."
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "Doc: https://www.nltk.org/index.html is useful.",
        )

    def test_preserves_inline_code_spans(self):
        text = "Run `bash scripts/squash-session.sh output/handoff.md` really now."
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "Run `bash scripts/squash-session.sh output/handoff.md` now.",
        )

    def test_preserves_fenced_code_block_content(self):
        text = "```md\n/mnt/f/workspace/file.md\nreally keep this\n```\nreally done"
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "```md\n/mnt/f/workspace/file.md\nreally keep this\n```\ndone",
        )

    def test_preserves_hyphenated_compounds_globally(self):
        text = "Use POS-based flow and self-tests for state-of-the-art utf-8 output."
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "Use POS-based flow and self-tests for state-of-the-art utf-8 output.",
        )

    def test_keeps_math_range_spacing_unmerged(self):
        text = "Compute x - y in range 1 - 2 and keep it really clear."
        result = run_strip(stdin_text=text)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertEqual(
            result.stdout.strip(),
            "Compute x - y in range 1 - 2 and keep it clear.",
        )


if __name__ == "__main__":
    unittest.main()
