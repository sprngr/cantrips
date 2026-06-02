import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "diff-snapshot.sh"


class DiffSnapshotTests(unittest.TestCase):
    def test_handles_spaces_and_newlines_in_filenames(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            before = Path(temp_dir) / "before"
            after = Path(temp_dir) / "after"
            before.mkdir()
            after.mkdir()

            # Common unchanged
            (before / "same.txt").write_text("same\n", encoding="utf-8")
            (after / "same.txt").write_text("same\n", encoding="utf-8")

            # Modified with space in filename
            (before / "space name.txt").write_text("old\n", encoding="utf-8")
            (after / "space name.txt").write_text("new\n", encoding="utf-8")

            # Removed with newline in filename
            removed_name = "multi\nline.txt"
            (before / removed_name).write_text("gone\n", encoding="utf-8")

            # Added file
            (after / "added.txt").write_text("added\n", encoding="utf-8")

            result = subprocess.run(
                ["bash", str(SCRIPT_PATH), str(before), str(after)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("Added:    1", result.stdout)
            self.assertIn("Removed:  1", result.stdout)
            self.assertIn("Modified: 1", result.stdout)


if __name__ == "__main__":
    unittest.main()
