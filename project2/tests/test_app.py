"""Headless execution test for the Streamlit application."""

import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class StreamlitAppTests(unittest.TestCase):
    def test_app_executes_and_dashboard_controls_are_usable(self):
        app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=20)
        self.assertEqual(list(app.exception), [])
        self.assertEqual(
            app.title[0].value,
            "Meridian Foundation Investment Management Application",
        )
        self.assertGreaterEqual(len(app.dataframe), 4)
        downloads = app.get("download_button")
        self.assertEqual(len(downloads), 2)
        self.assertTrue(all(button.proto.url for button in downloads))

        # The widget's stored values remain engine IDs; its visible labels use
        # the concise committee-facing format_func strings.
        app.selectbox[0].select("60/40 Benchmark").run(timeout=30)
        self.assertEqual(app.selectbox[0].value, "60/40 Benchmark")
        self.assertEqual(list(app.exception), [])

        app.multiselect[0].set_value(["baseline_full_window"]).run(timeout=30)
        self.assertEqual(app.multiselect[0].value, ["baseline_full_window"])
        self.assertEqual(list(app.exception), [])


if __name__ == "__main__":
    unittest.main()
