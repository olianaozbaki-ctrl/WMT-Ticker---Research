"""Deterministic known-answer tests; fixtures are not investment results."""

import math
import unittest

from project2_engine.calculations import (
    net_expected_return,
    one_way_turnover,
    portfolio_expected_return,
    portfolio_volatility,
    transaction_cost_rate,
    weight_total,
)


class CalculationKnownAnswers(unittest.TestCase):
    def test_weight_total(self):
        self.assertAlmostEqual(weight_total({"A": 0.60, "B": 0.40}), 1.0)

    def test_expected_return(self):
        result = portfolio_expected_return(
            {"A": 0.60, "B": 0.40}, {"A": 0.08, "B": 0.04}
        )
        self.assertAlmostEqual(result, 0.064)

    def test_volatility_includes_covariance(self):
        weights = {"A": 0.50, "B": 0.50}
        covariance = {
            "A": {"A": 0.01, "B": 0.005},
            "B": {"A": 0.005, "B": 0.04},
        }
        self.assertAlmostEqual(
            portfolio_volatility(weights, covariance), math.sqrt(0.015)
        )

    def test_one_way_turnover(self):
        current = {"A": 0.50, "B": 0.50}
        target = {"A": 0.60, "B": 0.40}
        self.assertAlmostEqual(one_way_turnover(current, target), 0.10)

    def test_transaction_cost_in_basis_points(self):
        self.assertAlmostEqual(transaction_cost_rate(0.10, 20.0), 0.0002)
        self.assertAlmostEqual(net_expected_return(0.064, 0.10, 20.0), 0.0638)

    def test_illustrative_cost_sensitivity_is_monotonic(self):
        gross_return = 0.07
        turnover = 0.20
        net_returns = [
            net_expected_return(gross_return, turnover, cost_bps)
            for cost_bps in (0.0, 10.0, 25.0)
        ]
        self.assertGreater(net_returns[0], net_returns[1])
        self.assertGreater(net_returns[1], net_returns[2])

    def test_negative_variance_is_rejected(self):
        weights = {"A": 0.50, "B": 0.50}
        invalid = {
            "A": {"A": 0.01, "B": -0.05},
            "B": {"A": -0.05, "B": 0.01},
        }
        with self.assertRaisesRegex(ValueError, "positive semidefinite"):
            portfolio_volatility(weights, invalid)


if __name__ == "__main__":
    unittest.main()
