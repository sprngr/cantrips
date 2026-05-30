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

    def test_extract_prefers_machine_report_over_other_pre_blocks(self):
        html_text = (
            "<html><body>"
            "<pre>{\"noise\":true}</pre>"
            "<details id='machine-report'><summary>x</summary><pre>{\"skill\":\"s\",\"iteration\":\"iteration-1\",\"report_date\":\"2026-05-30\",\"eval_count\":1,\"with_skill\":{\"pass_rate\":1,\"stddev\":0,\"samples\":1,\"tokens\":10,\"time\":0.1},\"without_skill\":{\"pass_rate\":0,\"stddev\":0,\"samples\":1,\"tokens\":1,\"time\":0.01}}</pre></details>"
            "</body></html>"
        )

        data, mode = parse_report.extract_json_with_mode(html_text)
        self.assertEqual(mode, "machine")
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get("skill"), "s")

    def test_extract_falls_back_when_machine_report_missing(self):
        html_text = (
            "<html><body>"
            "<pre>not-json</pre>"
            "<pre>{\"skill\":\"s\",\"iteration\":\"iteration-2\",\"report_date\":\"2026-05-30\",\"eval_count\":1,\"with_skill\":{\"pass_rate\":1,\"stddev\":0,\"samples\":1,\"tokens\":10,\"time\":0.1},\"without_skill\":{\"pass_rate\":0,\"stddev\":0,\"samples\":1,\"tokens\":1,\"time\":0.01}}</pre>"
            "</body></html>"
        )

        data, mode = parse_report.extract_json_with_mode(html_text)
        self.assertEqual(mode, "fallback")
        self.assertIsInstance(data, dict)
        self.assertEqual(data.get("iteration"), "iteration-2")

    def test_main_outputs_extraction_mode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "report.html"
            report.write_text(
                "<html><body><pre>{\"skill\":\"s\",\"iteration\":\"iteration-3\",\"report_date\":\"2026-05-30\",\"eval_count\":1,\"with_skill\":{\"pass_rate\":1,\"stddev\":0,\"samples\":1,\"tokens\":10,\"time\":0.1},\"without_skill\":{\"pass_rate\":0,\"stddev\":0,\"samples\":1,\"tokens\":1,\"time\":0.01}}</pre></body></html>",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(MODULE_PATH), str(report)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn("extraction_mode", payload)
            self.assertEqual(payload["extraction_mode"], "fallback")

    def test_main_rejects_skill_check_when_not_from_machine_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "report.html"
            # skill-check-like payload but only generic <pre>, no machine-report details block
            report.write_text(
                "<html><body><pre>{\"skill\":\"demo\",\"target_path\":\"skills/demo\",\"audit_date\":\"2026-05-30\",\"grade\":\"A\",\"spec\":{\"score\":1,\"total\":1,\"checks\":[{\"check\":\"c\",\"pass\":true,\"detail\":\"ok\"}]},\"best_practices\":{\"score\":1,\"total\":1,\"warnings\":[]},\"structure\":{\"score\":1,\"found\":[],\"warnings\":[]}}</pre></body></html>",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(MODULE_PATH), str(report)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertIn("error", payload)
            self.assertEqual(payload.get("report_type"), "skill-check")
            self.assertEqual(payload.get("extraction_mode"), "fallback")

    def test_main_accepts_skill_check_from_machine_block(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "report.html"
            report.write_text(
                "<html><body><details id='machine-report'><summary>x</summary><pre>{\"skill\":\"demo\",\"target_path\":\"skills/demo\",\"audit_date\":\"2026-05-30\",\"grade\":\"A\",\"spec\":{\"score\":1,\"total\":1,\"checks\":[{\"check\":\"c\",\"pass\":true,\"detail\":\"ok\"}]},\"best_practices\":{\"score\":1,\"total\":1,\"warnings\":[]},\"structure\":{\"score\":1,\"found\":[],\"warnings\":[]}}</pre></details></body></html>",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["python3", str(MODULE_PATH), str(report)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload.get("report_type"), "skill-check")
            self.assertEqual(payload.get("extraction_mode"), "machine")

    def test_schema_rejects_skill_check_missing_required_top_level_field(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            # target_path intentionally missing
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
                "warnings": [],
            },
            "structure": {
                "score": 6,
                "found": ["SKILL.md"],
                "warnings": [],
            },
        }

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft7Validator(schema).validate(sample)

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

    def test_schema_rejects_skill_check_missing_check_detail(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            "target_path": "skills/experimental/squash",
            "audit_date": "2026-05-30",
            "grade": "A-",
            "spec": {
                "score": 27,
                "total": 27,
                # detail missing by design
                "checks": [{"check": "name_present", "pass": True}],
            },
            "best_practices": {
                "score": 25,
                "total": 26,
                "warnings": [],
            },
            "structure": {
                "score": 6,
                "found": ["SKILL.md"],
                "warnings": [],
            },
            "fixes": [{"priority": "low", "description": "polish"}],
        }

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft7Validator(schema).validate(sample)

    def test_schema_rejects_skill_check_missing_best_practice_warnings(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            "target_path": "skills/experimental/squash",
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
                # warnings missing by design
            },
            "structure": {
                "score": 6,
                "found": ["SKILL.md"],
                "warnings": [],
            },
            "fixes": [{"priority": "low", "description": "polish"}],
        }

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft7Validator(schema).validate(sample)

    def test_schema_rejects_skill_check_fix_missing_required_fields(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            "target_path": "skills/experimental/squash",
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
                "warnings": [],
            },
            "structure": {
                "score": 6,
                "found": ["SKILL.md"],
                "warnings": [],
            },
            # missing description by design
            "fixes": [{"priority": "low"}],
        }

        with self.assertRaises(jsonschema.ValidationError):
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

    def test_schema_rejects_eval_iteration_integer(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")

        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        sample = {
            "skill": "squash",
            "iteration": 5,
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
        }

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft7Validator(schema).validate(sample)

    def test_schema_rejects_missing_metric_keys(self):
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
                # missing required "time"
            },
            "without_skill": {
                "pass_rate": 0.0,
                "stddev": 0.0,
                "samples": 1,
                "tokens": 20,
                "time": 0.0,
            },
        }

        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft7Validator(schema).validate(sample)


if __name__ == "__main__":
    unittest.main()
