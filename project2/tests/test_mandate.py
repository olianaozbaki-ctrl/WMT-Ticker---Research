"""Known-answer tests for individual Meridian mandate verdicts."""

import copy
import unittest
from pathlib import Path

from project2_engine.config import load_mandate
from project2_engine.mandate import validate_mandate
from project2_engine.models import AssetDefinition, RuleStatus


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MandateKnownAnswers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mandate = load_mandate(PROJECT_ROOT / "config" / "mandate.json")
        cls.assets = {
            "Cash": AssetDefinition("Cash", "none", 0, True),
            "Treasury": AssetDefinition(
                "Treasury", "U.S. Treasury", 1, True
            ),
            "Global fund": AssetDefinition(
                "Global fund", "diversified fund", 2, False
            ),
            "Acme stock": AssetDefinition("Acme stock", "Acme Corp", 1, False),
        }

    def complete_report(self):
        weights = {"Cash": 0.03, "Treasury": 0.47, "Global fund": 0.50}
        return validate_mandate(
            weights,
            self.assets,
            self.mandate,
            expected_returns={"Cash": 0.03, "Treasury": 0.06, "Global fund": 0.10},
            current_weights=weights,
            transaction_cost_bps=10.0,
            cpi_yoy=0.025,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        )

    def test_every_documented_rule_returns_a_verdict(self):
        expected_ids = {
            "weights_sum",
            "long_only",
            "no_borrowing",
            "no_derivatives",
            "reserve",
            "liquidity",
            "issuer_limit",
            "turnover",
            "horizon",
            "rebalance_frequency",
            "return_objective_proxy",
            "calendar_year_loss",
        }
        self.assertEqual(set(self.complete_report().by_id()), expected_ids)

    def test_complete_synthetic_case_is_model_feasible(self):
        report = self.complete_report()
        self.assertTrue(report.model_feasible)
        self.assertEqual(
            report.by_id()["calendar_year_loss"].status, RuleStatus.UNRESOLVED
        )

    def test_failures_are_rule_specific(self):
        weights = {
            "Cash": 0.00,
            "Treasury": 0.00,
            "Global fund": 0.90,
            "Acme stock": 0.10,
        }
        report = validate_mandate(
            weights,
            self.assets,
            self.mandate,
            expected_returns={name: 0.05 for name in weights},
            current_weights=weights,
            transaction_cost_bps=0.0,
            cpi_yoy=0.025,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        ).by_id()
        self.assertEqual(report["reserve"].status, RuleStatus.FAIL)
        self.assertEqual(report["issuer_limit"].status, RuleStatus.FAIL)
        self.assertEqual(report["return_objective_proxy"].status, RuleStatus.FAIL)

    def test_turnover_above_25_percent_fails(self):
        target = {"Cash": 0.03, "Treasury": 0.47, "Global fund": 0.50}
        current = {"Cash": 0.50, "Treasury": 0.00, "Global fund": 0.50}
        report = validate_mandate(
            target,
            self.assets,
            self.mandate,
            expected_returns={"Cash": 0.03, "Treasury": 0.06, "Global fund": 0.10},
            current_weights=current,
            transaction_cost_bps=10.0,
            cpi_yoy=0.025,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        ).by_id()
        self.assertAlmostEqual(report["turnover"].measured_value, 0.47)
        self.assertEqual(report["turnover"].status, RuleStatus.FAIL)

    def test_unknown_reserve_eligibility_is_not_a_pass(self):
        assets = {
            "ETF": AssetDefinition("ETF", "diversified fund", 1, None),
        }
        report = validate_mandate(
            {"ETF": 1.0},
            assets,
            self.mandate,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        )
        self.assertEqual(report.by_id()["reserve"].status, RuleStatus.NOT_TESTABLE)
        self.assertFalse(report.model_feasible)

    def test_missing_current_weights_blocks_turnover_and_objective(self):
        report = validate_mandate(
            {"Cash": 0.03, "Treasury": 0.47, "Global fund": 0.50},
            self.assets,
            self.mandate,
            expected_returns={"Cash": 0.03, "Treasury": 0.06, "Global fund": 0.10},
            transaction_cost_bps=10.0,
            cpi_yoy=0.025,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        ).by_id()
        self.assertEqual(report["turnover"].status, RuleStatus.NOT_TESTABLE)
        self.assertEqual(
            report["return_objective_proxy"].status, RuleStatus.NOT_TESTABLE
        )

    def test_return_objective_label_uses_configured_spread(self):
        mandate = copy.deepcopy(self.mandate)
        mandate["objective"]["real_return_spread"] = 0.05
        report = validate_mandate(
            {"Cash": 0.03, "Treasury": 0.47, "Global fund": 0.50},
            self.assets,
            mandate,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        ).by_id()
        self.assertEqual(
            report["return_objective_proxy"].label,
            "CPI + 5% after-cost expected-return proxy",
        )


if __name__ == "__main__":
    unittest.main()
