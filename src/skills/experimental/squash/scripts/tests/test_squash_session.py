import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "squash-session.sh"


def run_session(
    *args: str,
    stdin_text: str | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    return subprocess.run(
        ["bash", str(SCRIPT_PATH), *args],
        input=stdin_text,
        capture_output=True,
        text=True,
        check=False,
        env=merged_env,
    )


def parse_saved_path(stdout: str) -> str:
    line = stdout.strip()
    prefix = "saved: "
    if not line.startswith(prefix):
        raise AssertionError(f"Missing saved label. stdout={stdout!r}")
    return line[len(prefix) :]


class SquashSessionScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not SCRIPT_PATH.exists():
            raise RuntimeError(f"Missing script: {SCRIPT_PATH}")

    def test_usage_rejects_too_many_args(self):
        result = run_session("a", "b", "c")
        self.assertEqual(result.returncode, 64)
        self.assertIn("Usage:", result.stderr)

    def test_rejects_empty_output_path_when_provided(self):
        result = run_session("")
        self.assertEqual(result.returncode, 64)
        self.assertIn("output-path cannot be empty", result.stderr)

    def test_rejects_missing_input_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "handoff.md"
            result = run_session(str(output_file), str(Path(temp_dir) / "missing.md"))
            self.assertEqual(result.returncode, 66)
            self.assertIn("input-file not found", result.stderr)

    def test_uses_explicit_output_path_and_saved_label(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_file = Path(temp_dir) / "handoff.md"
            result = run_session(str(output_file), stdin_text="This is really just ready.")

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(parse_saved_path(result.stdout), str(output_file))
            self.assertTrue(output_file.exists())

    def test_uses_temp_dir_when_output_path_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_session(
                stdin_text="This is really just ready.",
                env={"TMPDIR": temp_dir},
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            saved_path = Path(parse_saved_path(result.stdout))
            self.assertTrue(saved_path.exists())
            self.assertEqual(saved_path.parent, Path(temp_dir))
            self.assertRegex(saved_path.name, r"^handoff-\d{8}-\d{6}-[A-Za-z0-9]{6}\.md$")

    def test_accepts_input_file_and_output_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "source.md"
            output_file = Path(temp_dir) / "handoff.md"
            input_file.write_text("This is really just ready.", encoding="utf-8")

            result = run_session(str(output_file), str(input_file))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual(parse_saved_path(result.stdout), str(output_file))
            self.assertEqual(output_file.read_text(encoding="utf-8").strip(), "This is ready.")


if __name__ == "__main__":
    unittest.main()
