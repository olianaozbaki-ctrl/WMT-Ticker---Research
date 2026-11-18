"""Configuration invariants for the documented Meridian mandate."""

import copy
import unittest
from pathlib import Path

from project2_engine.config import load_mandate, validate_mandate_config


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MandateConfigurationTests(unittest.TestCase):
    def test_phase_1_configuration_loads(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        self.assertEqual(mandate["horizon_years"], 7)
        self.assertEqual(mandate["reserve"]["minimum_weight"], 0.03)
        self.assertEqual(
            mandate["cpi"]["original_modeling_assumption"]["series_id"],
            "CPIAUCSL",
        )
        self.assertEqual(
            set(mandate["original_policy"]["statements"]),
            {f"S{number}" for number in range(1, 11)},
        )

    def test_executed_cpi_methodology_and_dates_are_explicit(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        cpi = mandate["cpi"]
        executed = cpi["executed_analysis_methodology"]

        self.assertEqual(
            executed["series_label"],
            "CPI-U all items, U.S. city average, not seasonally adjusted",
        )
        self.assertEqual(executed["provider"], "U.S. Bureau of Labor Statistics")
        self.assertEqual(executed["seasonal_adjustment"], "not_seasonally_adjusted")
        self.assertEqual(executed["current_observation_date"], "2026-08-01")
        self.assertEqual(executed["prior_year_observation_date"], "2025-08-01")
        self.assertEqual(executed["availability_date"], "2026-09-11")
        self.assertEqual(executed["decision_date"], "2026-10-05")
        self.assertTrue(executed["point_in_time_verified"])
        self.assertFalse(executed["alfred_vintage_verified"])
        self.assertEqual(
            executed["status"],
            "executed_project_2_methodology_pending_cio_approval",
        )

    def test_cpi_methodology_approval_remains_unresolved(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        self.assertEqual(
            mandate["cpi"]["methodology_approval_status"],
            "unresolved_pending_cio_approval",
        )
        unresolved = {
            item["id"]: item["question"]
            for item in mandate["unresolved_decisions"]
        }
        self.assertIn("U3", unresolved)
        self.assertIn("executed October 5, 2026 CPI methodology", unresolved["U3"])
        self.assertIn("non-seasonally adjusted CPI-U", unresolved["U3"])
        self.assertIn("CPIAUCSL/ALFRED", unresolved["U3"])

    def test_reserve_minimum_must_reconcile_to_cash_need(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        invalid = copy.deepcopy(mandate)
        invalid["reserve"]["minimum_weight"] = 0.04
        with self.assertRaisesRegex(ValueError, "reserve.minimum_weight"):
            validate_mandate_config(invalid)

    def test_hypothetical_start_is_labeled_and_balanced(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        start = mandate["turnover"]["illustrative_starting_allocation"]
        self.assertIn("Hypothetical", start["label"])
        self.assertAlmostEqual(sum(start["weights"].values()), 1.0)
        self.assertEqual(
            mandate["turnover"]["actual_starting_holdings_status"], "unavailable"
        )

    def test_reserve_classification_is_explicit(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        universe = {item["ticker"]: item for item in mandate["project_universe"]}
        self.assertIs(universe["BIL"]["reserve_eligible"], True)
        self.assertIs(universe["IEF"]["reserve_eligible"], False)
        self.assertIsNone(universe["BIL"]["liquidity_business_days"])
        self.assertIsNone(universe["IEF"]["liquidity_business_days"])

    def test_s9_remains_unresolved_and_outside_hard_constraints(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        self.assertEqual(
            mandate["risk"]["loss_rule_status"],
            "unresolved_unverifiable_promise_not_a_hard_constraint",
        )

    def test_illustrative_cost_has_declared_sensitivity(self):
        mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        costs = mandate["costs"]
        self.assertEqual(costs["transaction_cost_bps"], 10.0)
        self.assertEqual(costs["sensitivity_bps"], [0.0, 10.0, 25.0])
        self.assertIn("Illustrative", costs["transaction_cost_label"])


if __name__ == "__main__":
    unittest.main()
