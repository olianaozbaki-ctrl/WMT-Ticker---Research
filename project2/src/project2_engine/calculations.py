"""Unit-explicit, deterministic portfolio calculations."""

from math import isfinite, sqrt
from typing import Mapping


TOLERANCE = 1e-12


def _require_finite_mapping(values: Mapping[str, float], label: str) -> None:
    if not values:
        raise ValueError(f"{label} cannot be empty")
    for name, value in values.items():
        if not isinstance(value, (int, float)) or not isfinite(value):
            raise ValueError(f"{label}[{name!r}] must be finite")


def weight_total(weights: Mapping[str, float]) -> float:
    """Return the sum of decimal portfolio weights."""
    _require_finite_mapping(weights, "weights")
    return float(sum(weights.values()))


def portfolio_expected_return(
    weights: Mapping[str, float], expected_returns: Mapping[str, float]
) -> float:
    """Return weighted annual expected return; all inputs are decimal rates."""
    _require_finite_mapping(weights, "weights")
    _require_finite_mapping(expected_returns, "expected_returns")
    if set(weights) != set(expected_returns):
        raise ValueError("weights and expected_returns must contain the same assets")
    return float(sum(weights[name] * expected_returns[name] for name in weights))


def portfolio_variance(
    weights: Mapping[str, float], covariance: Mapping[str, Mapping[str, float]]
) -> float:
    """Return annual portfolio variance after structural covariance checks."""
    _require_finite_mapping(weights, "weights")
    names = set(weights)
    if set(covariance) != names:
        raise ValueError("covariance rows must match the portfolio assets")

    ordered_names = list(weights)
    for first in names:
        if set(covariance[first]) != names:
            raise ValueError(f"covariance columns for {first!r} do not match assets")
        for second in names:
            value = covariance[first][second]
            if not isinstance(value, (int, float)) or not isfinite(value):
                raise ValueError("covariance values must be finite")
            if abs(value - covariance[second][first]) > TOLERANCE:
                raise ValueError("covariance matrix must be symmetric")

    # LDL decomposition checks positive semidefiniteness without adding a
    # numerical-library dependency. A zero pivot is allowed only when its
    # remaining cross-covariances are also zero after prior factors.
    dimension = len(ordered_names)
    lower = [[0.0] * dimension for _ in range(dimension)]
    diagonal = [0.0] * dimension
    for row in range(dimension):
        lower[row][row] = 1.0
        pivot = covariance[ordered_names[row]][ordered_names[row]] - sum(
            lower[row][prior] ** 2 * diagonal[prior] for prior in range(row)
        )
        if pivot < -TOLERANCE:
            raise ValueError("covariance matrix must be positive semidefinite")
        diagonal[row] = max(0.0, pivot)
        for later in range(row + 1, dimension):
            residual = covariance[ordered_names[later]][ordered_names[row]] - sum(
                lower[later][prior]
                * lower[row][prior]
                * diagonal[prior]
                for prior in range(row)
            )
            if diagonal[row] > TOLERANCE:
                lower[later][row] = residual / diagonal[row]
            elif abs(residual) > TOLERANCE:
                raise ValueError("covariance matrix must be positive semidefinite")

    variance = float(
        sum(
            weights[first] * weights[second] * covariance[first][second]
            for first in ordered_names
            for second in ordered_names
        )
    )
    if variance < -TOLERANCE:
        raise ValueError("portfolio variance is negative; covariance is invalid")
    return max(0.0, variance)


def portfolio_volatility(
    weights: Mapping[str, float], covariance: Mapping[str, Mapping[str, float]]
) -> float:
    """Return annualized standard deviation from an annual covariance matrix."""
    return sqrt(portfolio_variance(weights, covariance))


def one_way_turnover(
    current_weights: Mapping[str, float], target_weights: Mapping[str, float]
) -> float:
    """Return one-way turnover: half the sum of absolute weight changes."""
    _require_finite_mapping(current_weights, "current_weights")
    _require_finite_mapping(target_weights, "target_weights")
    names = set(current_weights) | set(target_weights)
    return 0.5 * sum(
        abs(target_weights.get(name, 0.0) - current_weights.get(name, 0.0))
        for name in names
    )


def transaction_cost_rate(turnover: float, transaction_cost_bps: float) -> float:
    """Return portfolio cost as a decimal rate for one rebalance."""
    if not isfinite(turnover) or not 0 <= turnover <= 1:
        raise ValueError("turnover must be a decimal rate between 0 and 1")
    if not isfinite(transaction_cost_bps) or transaction_cost_bps < 0:
        raise ValueError("transaction_cost_bps must be nonnegative")
    return turnover * transaction_cost_bps / 10_000


def net_expected_return(
    gross_expected_return: float, turnover: float, transaction_cost_bps: float
) -> float:
    """Deduct the modeled one-rebalance trading cost from expected return."""
    if not isfinite(gross_expected_return):
        raise ValueError("gross_expected_return must be finite")
    return gross_expected_return - transaction_cost_rate(turnover, transaction_cost_bps)
