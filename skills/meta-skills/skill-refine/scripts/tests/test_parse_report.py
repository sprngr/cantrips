import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = SCRIPT_DIR / "parse_report.py"
SCHEMA_PATH = SCRIPT_DIR.parent / "assets" / "report-schema.json"

SPEC = importlib.util.spec_from_file_location("parse_report", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load module spec from {MODULE_PATH}")
parse_report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(parse_report)


class ParseReportTests(unittest.TestCase):
    def test_extract_json_unescapes_html_entities(self):
        html_text = (
            "<html><body><pre>"
            "{&quot;spec&quot;:{&quot;checks&quot;:[{&quot;check&quot;:&quot;c1&quot;,&quot;pass&quot;:false,&quot;detail&quot;:&quot;bad &#39;quote&#39; &amp; value&quot;}]},"
            "&quot;best_practices&quot;:{&quot;warnings&quot;:[]},"
            "&quot;structure&quot;:{&quot;warnings&quot;:[]},"
            "&quot;fixes&quot;:[]}"
            "</pre></body></html>"
        )

        data = parse_report.extract_json_from_html(html_text)
        self.assertIsInstance(data, dict)
        findings = parse_report.flatten_findings(data, parse_report.detect_report_type(data))
        self.assertEqual(len(findings), 1)
        self.assertIn("bad 'quote' & value", findings[0]["detail"])

    def test_main_fails_on_invalid_utf8_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "report.html"
            report.write_bytes(b"<pre>{\xff}</pre>")

            result = subprocess.run(
                ["python3", str(MODULE_PATH), str(report)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)

    def test_schema_accepts_skill_check_plus_minus_grade_and_int_structure_score(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            "target_path": "skills/squash",
            "audit_date": "2026-05-30",
            "grade": "A-",
            "spec": {
                "score": 27,
                "total": 27,
                "checks": [{"check": "name_present", "pass": True, "detail": "ok"}],
            },
            "best_practices": {
                "score": 25,
                "total": 26,
                "warnings": ["minor warning"],
            },
            "has_evals": True,
            "structure": {
                "score": 6,
                "found": ["SKILL.md"],
                "warnings": [],
            },
            "fixes": [{"priority": "low", "description": "polish"}],
        }

        jsonschema.Draft7Validator(schema).validate(sample)

    def test_schema_accepts_eval_iteration_string_and_integer_eval_id(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            "iteration": "iteration-5",
            "report_date": "2026-05-30",
            "eval_count": 1,
            "with_skill": {
                "pass_rate": 1.0,
                "stddev": 0.0,
                "samples": 1,
                "tokens": 100,
                "time": 0.1,
            },
            "without_skill": {
                "pass_rate": 0.0,
                "stddev": 0.0,
                "samples": 1,
                "tokens": 20,
                "time": 0.0,
            },
            "delta": {"pass_rate": 1.0, "tokens": 80, "time": 0.1},
            "evals": [
                {
                    "id": 1,
                    "pass_rate": 1.0,
                    "assertions": [{"id": "1.1", "pass": True, "evidence": "ok"}],
                }
            ],
            "patterns": [{"type": "skill-dependent", "count": 1, "action": "keep"}],
            "fixes": [{"priority": "medium", "description": "telemetry"}],
        }

        jsonschema.Draft7Validator(schema).validate(sample)


if __name__ == "__main__":
    unittest.main()
