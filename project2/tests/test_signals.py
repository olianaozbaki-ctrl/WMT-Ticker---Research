import tempfile
import unittest
from pathlib import Path

from project2_engine.signals import load_dgs10_signal


ROOT = Path(__file__).resolve().parents[1]


class DGS10SignalTests(unittest.TestCase):
    def test_selects_latest_observation_available_by_decision_date(self):
        result = load_dgs10_signal(ROOT / "data" / "dgs10_pit.csv", "2026-10-05")
        self.assertTrue(result["available"])
        self.assertEqual(result["observation_date"], "2026-10-02")
        self.assertEqual(result["availability_date"], "2026-10-05")
        self.assertEqual(result["value_percent"], 5.28)

    def test_future_availability_is_excluded(self):
        result = load_dgs10_signal(ROOT / "data" / "dgs10_pit.csv", "2026-10-04")
        self.assertEqual(result["observation_date"], "2026-09-29")
        self.assertEqual(result["value_percent"], 5.26)

    def test_unavailable_observation_returns_safe_status(self):
        result = load_dgs10_signal(ROOT / "data" / "dgs10_pit.csv", "2026-01-01")
        self.assertFalse(result["available"])
        self.assertIsNone(result["value_percent"])


if __name__ == "__main__":
    unittest.main()
