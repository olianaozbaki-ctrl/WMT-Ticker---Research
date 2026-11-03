"""Offline behavior tests for the deterministic Lab 18 calculations."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sys.path.insert(
    0,
    str(ROOT / ".codex" / "skills" / "warren-buffett-investing" / "scripts"),
)

from sec_buffett import (  # noqa: E402
    buffett_checks,
    select_value,
    unsupported_memo_numbers,
)


class Lab18Tests(unittest.TestCase):
    def test_tag_priority_beats_fallback_and_latest_same_period_wins(self):
        facts = {
            "facts": {
                "us-gaap": {
                    "RevenueFromContractWithCustomerExcludingAssessedTax": {
                        "units": {
                            "USD": [
                                {
                                    "start": "2024-01-01",
                                    "end": "2024-12-31",
                                    "val": 100,
                                    "form": "10-K",
                                    "filed": "2025-02-01",
                                    "accn": "old",
                                },
                                {
                                    "start": "2024-01-01",
                                    "end": "2024-12-31",
                                    "val": 110,
                                    "form": "10-K",
                                    "filed": "2026-02-01",
                                    "accn": "new",
                                },
                            ]
                        }
                    },
                    "Revenues": {
                        "units": {
                            "USD": [
                                {
                                    "start": "2024-01-01",
                                    "end": "2024-12-31",
                                    "val": 999,
                                    "form": "10-K",
                                    "filed": "2027-02-01",
                                    "accn": "fallback",
                                }
                            ]
                        }
                    },
                }
            }
        }
        chosen = select_value(facts, "revenue", "2024-12-31")
        self.assertEqual(chosen["value"], 110)
        self.assertEqual(
            chosen["tag"], "RevenueFromContractWithCustomerExcludingAssessedTax"
        )

    def test_missing_check_input_is_not_known(self):
        rows = [
            {"roe": {"value": 0.20}, "owner_earnings": {"value": 10}}
            for _ in range(5)
        ]
        rows[2]["owner_earnings"]["value"] = None
        checks = buffett_checks(rows)
        self.assertEqual(checks["roe_15_every_year"], "pass")
        self.assertEqual(
            checks["positive_owner_earnings_every_year"], "not known"
        )
        self.assertEqual(checks["owner_earnings_growth"], "not known")

    def test_hand_typed_roe_is_flagged(self):
        analysis = {
            "ticker": "TEST",
            "rows": [],
            "checks": {
                "roe_15_every_year": "not known",
                "positive_owner_earnings_every_year": "not known",
                "owner_earnings_growth": "not known",
            },
        }
        self.assertEqual(
            unsupported_memo_numbers("ROE was 40.0%.", analysis), ["40.0%"]
        )

    def test_unprinted_date_is_flagged_as_a_whole_value(self):
        analysis = {
            "ticker": "TEST",
            "rows": [],
            "checks": {
                "roe_15_every_year": "not known",
                "positive_owner_earnings_every_year": "not known",
                "owner_earnings_growth": "not known",
            },
        }
        self.assertEqual(
            unsupported_memo_numbers("As of 2099-01-01.", analysis),
            ["2099-01-01"],
        )


if __name__ == "__main__":
    unittest.main()

