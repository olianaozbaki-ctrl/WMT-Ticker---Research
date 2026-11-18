"""Data-integrity tests for the frozen Phase 2 inputs."""

import csv
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from project2_engine.data import estimate_from_monthly_prices, load_cpi_yoy, load_monthly_prices


ROOT = Path(__file__).resolve().parents[1]


class MarketDataIntegrityTests(unittest.TestCase):
    def test_frozen_price_panel_is_complete_and_dated(self):
        dates, prices = load_monthly_prices(ROOT / "data" / "prices_monthly.csv")
        self.assertEqual(len(dates), 61)
        self.assertEqual(dates[0].isoformat(), "2021-10-29")
        self.assertEqual(dates[-1].isoformat(), "2026-10-30")
        self.assertEqual(set(prices), {"BIL", "IEF", "LQD", "VT"})
        self.assertTrue(all(len(series) == 61 for series in prices.values()))

    def test_provenance_reconciles_to_price_panel(self):
        provenance = json.loads(
            (ROOT / "data" / "market_data_provenance.json").read_text()
        )
        self.assertEqual(provenance["price_data"]["aligned_rows"], 61)
        self.assertEqual(provenance["price_data"]["aligned_missing_values"], 0)
        self.assertFalse(provenance["cpi_data"]["alfred_vintage_verified"])
        self.assertNotIn("RETRIEVAL_DATE", (ROOT / "scripts" / "fetch_market_data.py").read_text())
        self.assertEqual(
            provenance["retrieval_date"],
            provenance["source_retrieved_at_utc"][:10],
        )
        self.assertIn(
            provenance["source_retrieval_timestamp_precision"],
            {"second", "date_only_legacy_snapshot"},
        )
        datetime.fromisoformat(provenance["source_retrieved_at_utc"])
        datetime.fromisoformat(provenance["processed_at_utc"])
        self.assertLessEqual(
            provenance["price_data"]["as_of_date"], provenance["retrieval_date"]
        )
        for ticker in ("BIL", "IEF", "LQD", "VT"):
            self.assertEqual(
                provenance["price_data"]["tickers"][ticker]["raw_missing_adjusted_close"], 0
            )

    def test_missing_price_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.csv"
            path.write_text("observation_date,A\n2026-01-31,1\n2026-02-28,\n")
            with self.assertRaisesRegex(ValueError, "missing value"):
                load_monthly_prices(path)

    def test_estimates_use_sixty_monthly_returns(self):
        result = estimate_from_monthly_prices(ROOT / "data" / "prices_monthly.csv")
        self.assertTrue(all(len(values) == 60 for values in result.monthly_returns.values()))
        self.assertAlmostEqual(
            result.annual_covariance["VT"]["LQD"],
            result.annual_covariance["LQD"]["VT"],
        )

    def test_latest_valid_cpi_pair_is_computed_and_october_is_missing(self):
        value = load_cpi_yoy(
            ROOT / "data" / "cpi_snapshot.csv", "2026-09-01", "2025-09-01"
        )
        self.assertAlmostEqual(value, 336.298 / 324.245 - 1.0)
        with self.assertRaisesRegex(ValueError, "both requested"):
            load_cpi_yoy(
                ROOT / "data" / "cpi_snapshot.csv", "2026-10-01", "2025-10-01"
            )


if __name__ == "__main__":
    unittest.main()
