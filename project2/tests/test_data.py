"""Data-integrity tests for the frozen Phase 2 inputs."""

import csv
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from project2_engine.data import estimate_from_monthly_prices, load_cpi_yoy, load_monthly_prices, load_point_in_time_cpi


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

    def test_cpi_pair_is_point_in_time_verified_and_matches_bls_release(self):
        value, metadata = load_point_in_time_cpi(ROOT / "data" / "cpi_pit_2026-10-05.csv", "2026-10-05")
        self.assertAlmostEqual(value, 334.980 / 323.976 - 1.0)
        self.assertEqual(metadata["availability_date"], "2026-09-11")
        self.assertEqual(metadata["vintage_date"], "2026-10-05")
        self.assertEqual(metadata["provider"], "U.S. Bureau of Labor Statistics")
        self.assertFalse(metadata["alfred_vintage_verified"])

    def test_cpi_csv_must_match_published_values(self):
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "cpi.csv"
            csv_path.write_text("observation_date,CPI-U\n2025-08-01,323.976\n2026-08-01,335.000\n")
            metadata = json.loads((ROOT / "data" / "cpi_pit_2026-10-05.json").read_text())
            (Path(directory) / "cpi.json").write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "do not match"):
                load_point_in_time_cpi(csv_path, "2026-10-05")

    def test_cpi_loader_rejects_post_decision_vintage_or_availability(self):
        with self.assertRaisesRegex(ValueError, "vintage does not match"):
            load_point_in_time_cpi(ROOT / "data" / "cpi_pit_2026-10-05.csv", "2026-10-15")
        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "cpi.csv"
            csv_path.write_text((ROOT / "data" / "cpi_pit_2026-10-05.csv").read_text())
            metadata_path = Path(directory) / "cpi.json"
            metadata = json.loads((ROOT / "data" / "cpi_pit_2026-10-05.json").read_text())
            metadata["prior_year_availability_date"] = "2026-10-06"
            metadata_path.write_text(json.dumps(metadata))
            with self.assertRaisesRegex(ValueError, "unavailable"):
                load_point_in_time_cpi(csv_path, "2026-10-05")

    def test_decision_boundary_excludes_future_market_prices(self):
        full = estimate_from_monthly_prices(ROOT / "data" / "prices_monthly.csv")
        pit = estimate_from_monthly_prices(ROOT / "data" / "prices_monthly.csv", as_of_date="2026-10-05")
        self.assertEqual(full.observation_dates[-1].isoformat(), "2026-10-30")
        self.assertEqual(pit.observation_dates[-1].isoformat(), "2026-09-30")
        self.assertEqual(len(pit.monthly_returns["VT"]), 59)

    def test_legacy_current_cpi_snapshot_is_not_used_for_pit_target(self):
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
