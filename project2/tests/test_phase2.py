"""Integration tests for baselines, visible metrics, and rule verdicts."""

import json
import unittest
from pathlib import Path

from project2_engine.phase2 import run_phase2


ROOT = Path(__file__).resolve().parents[1]


class Phase2IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_phase2(ROOT)
        cls.portfolios = {item["name"]: item for item in cls.result["portfolios"]}

    def test_three_portfolios_are_constructed(self):
        self.assertEqual(
            set(self.portfolios),
            {"Equal weight", "60/40 benchmark", "Constrained minimum volatility"},
        )
        self.assertEqual(
            self.portfolios["60/40 benchmark"]["weights"],
            {"BIL": 0.0, "IEF": 0.0, "LQD": 0.4, "VT": 0.6},
        )

    def test_baseline_calculations_reconcile(self):
        equal = self.portfolios["Equal weight"]
        asset_returns = self.result["annual_expected_returns_by_asset"]
        self.assertAlmostEqual(
            equal["annual_expected_return"], sum(asset_returns.values()) / 4.0
        )
        self.assertAlmostEqual(equal["reserve_allocation"], 0.25)
        self.assertAlmostEqual(equal["illustrative_turnover_from_equal_weight"], 0.0)

    def test_optimizer_output_meets_enforced_model_constraints(self):
        optimized = self.portfolios["Constrained minimum volatility"]
        self.assertGreaterEqual(optimized["weights"]["BIL"], 0.03)
        self.assertGreaterEqual(
            optimized["illustrative_net_expected_return"],
            self.result["provisional_after_cost_hurdle"] - 1e-12,
        )

    def test_hypothetical_turnover_cap_is_visible_and_infeasible(self):
        stop = self.result["optimization"][
            "hypothetical_turnover_cap_stop_condition"
        ]
        self.assertFalse(stop["feasible"])
        self.assertEqual(stop["maximum_turnover"], 0.25)
        self.assertIn("Hypothetical", stop["starting_holdings"])
        self.assertGreater(stop["return_shortfall"], 0.0)
        self.assertFalse(self.result["optimization"]["full_mandate_feasible"])

    def test_unknown_evidence_is_not_reported_as_compliance(self):
        for portfolio in self.portfolios.values():
            rules = {item["rule_id"]: item["status"] for item in portfolio["rules"]}
            self.assertEqual(rules["liquidity"], "NOT_TESTABLE")
            self.assertEqual(rules["issuer_limit"], "NOT_TESTABLE")
            self.assertEqual(rules["turnover"], "NOT_TESTABLE")
            self.assertEqual(rules["calendar_year_loss"], "UNRESOLVED")
            self.assertFalse(portfolio["verified_mandate_feasible"])

    def test_corrected_output_paths_and_precision_evidence_exist(self):
        self.assertTrue((ROOT / "outputs" / "phase2_results.md").is_file())
        self.assertFalse((ROOT / "outputs" / "phase2-results.md").exists())
        precision = json.loads(
            (ROOT / "outputs" / "phase2_results.json").read_text()
        )["optimizer_precision_validation"]
        self.assertLess(
            precision["maximum_weight_difference_percentage_points"], 0.5
        )
        self.assertTrue(precision["continuous_slsqp"]["success"])


if __name__ == "__main__":
    unittest.main()
