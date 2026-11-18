"""Known-answer tests for portfolio construction and constrained search."""

import unittest

from project2_engine.optimizer import maximum_net_return_grid, minimum_volatility_grid


class OptimizerTests(unittest.TestCase):
    def setUp(self):
        self.returns = {"Reserve": 0.02, "Risk": 0.10}
        self.covariance = {
            "Reserve": {"Reserve": 0.0001, "Risk": 0.0},
            "Risk": {"Reserve": 0.0, "Risk": 0.04},
        }

    def test_feasible_case_meets_return_and_reserve(self):
        result = minimum_volatility_grid(
            self.returns,
            self.covariance,
            minimum_return=0.06,
            reserve_assets={"Reserve"},
            minimum_reserve=0.10,
            current_weights={"Reserve": 0.50, "Risk": 0.50},
            maximum_turnover=0.50,
            step=0.10,
        )
        self.assertTrue(result.feasible)
        self.assertEqual(result.weights, {"Reserve": 0.5, "Risk": 0.5})

    def test_infeasible_case_is_explicit(self):
        result = minimum_volatility_grid(
            self.returns,
            self.covariance,
            minimum_return=0.20,
            reserve_assets={"Reserve"},
            minimum_reserve=0.10,
            current_weights=None,
            maximum_turnover=None,
            step=0.10,
        )
        self.assertFalse(result.feasible)
        self.assertIsNone(result.weights)
        self.assertIn("no grid portfolio", result.reason)

    def test_turnover_constraint_without_holdings_is_rejected(self):
        result = minimum_volatility_grid(
            self.returns,
            self.covariance,
            minimum_return=0.05,
            reserve_assets={"Reserve"},
            minimum_reserve=0.10,
            current_weights=None,
            maximum_turnover=0.25,
            step=0.10,
        )
        self.assertFalse(result.feasible)
        self.assertEqual(result.reason, "turnover constraint requires current weights")

    def test_maximum_return_respects_turnover_boundary(self):
        result = maximum_net_return_grid(
            self.returns,
            reserve_assets={"Reserve"},
            minimum_reserve=0.10,
            current_weights={"Reserve": 0.50, "Risk": 0.50},
            maximum_turnover=0.10,
            transaction_cost_bps=10.0,
            step=0.10,
        )
        self.assertEqual(result.weights, {"Reserve": 0.4, "Risk": 0.6})
        self.assertAlmostEqual(result.net_expected_return, 0.0679)


if __name__ == "__main__":
    unittest.main()
