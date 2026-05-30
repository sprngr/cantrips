import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "aggregate_benchmark.py"
SPEC = importlib.util.spec_from_file_location("aggregate_benchmark", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load module spec from {SCRIPT_PATH}")
aggregate_benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(aggregate_benchmark)


class AggregateBenchmarkTests(unittest.TestCase):
    def test_load_json_files_supports_recursive_glob(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = Path(temp_dir) / "eval-1" / "with_skill"
            nested_dir.mkdir(parents=True)
            grading_file = nested_dir / "grading.json"
            grading_file.write_text('{"summary": {"passed": 1, "total": 1}}', encoding="utf-8")

            pattern = str(Path(temp_dir) / "**" / "grading.json")
            loaded = aggregate_benchmark.load_json_files(pattern)

            self.assertEqual(len(loaded), 1)
            self.assertEqual(loaded[0]["summary"]["total"], 1)

    def test_main_counts_nested_eval_directories(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            iter_dir = Path(temp_dir) / "iteration-1"
            eval_dir = iter_dir / "eval-alpha-1"

            with_skill = eval_dir / "with_skill"
            without_skill = eval_dir / "without_skill"
            with_skill.mkdir(parents=True)
            without_skill.mkdir(parents=True)

            with (with_skill / "grading.json").open("w", encoding="utf-8") as f:
                json.dump({"summary": {"passed": 1, "total": 1}}, f)
            with (without_skill / "grading.json").open("w", encoding="utf-8") as f:
                json.dump({"summary": {"passed": 0, "total": 1}}, f)

            with (with_skill / "timing.json").open("w", encoding="utf-8") as f:
                json.dump({"total_tokens": 100, "duration_ms": 1000}, f)
            with (without_skill / "timing.json").open("w", encoding="utf-8") as f:
                json.dump({"total_tokens": 80, "duration_ms": 900}, f)

            old_argv = aggregate_benchmark.sys.argv
            try:
                aggregate_benchmark.sys.argv = ["aggregate_benchmark.py", str(iter_dir)]
                aggregate_benchmark.main()
            finally:
                aggregate_benchmark.sys.argv = old_argv

            with (iter_dir / "benchmark.json").open(encoding="utf-8") as f:
                benchmark = json.load(f)

            self.assertEqual(benchmark["eval_count"], 1)
            self.assertEqual(benchmark["run_summary"]["with_skill"]["pass_rate"]["samples"], 1)


if __name__ == "__main__":
    unittest.main()
