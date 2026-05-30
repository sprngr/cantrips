import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = SCRIPT_DIR / "parse_report.py"

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


if __name__ == "__main__":
    unittest.main()
