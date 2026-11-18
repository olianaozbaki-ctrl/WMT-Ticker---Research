"""Deterministic constrained minimum-volatility search."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .calculations import (
    net_expected_return,
    one_way_turnover,
    portfolio_expected_return,
    portfolio_variance,
)


@dataclass(frozen=True)
class OptimizationResult:
    feasible: bool
    weights: dict[str, float] | None
    combinations_evaluated: int
    feasible_combinations: int
    reason: str
    grid_step: float


@dataclass(frozen=True)
class MaximumReturnResult:
    weights: dict[str, float] | None
    net_expected_return: float | None
    combinations_evaluated: int
    grid_step: float


def maximum_net_return_grid(
    expected_returns: Mapping[str, float],
    *,
    reserve_assets: set[str],
    minimum_reserve: float,
    current_weights: Mapping[str, float],
    maximum_turnover: float,
    transaction_cost_bps: float,
    step: float = 0.01,
) -> MaximumReturnResult:
    """Return the highest after-cost return satisfying reserve and turnover limits."""
    names = tuple(expected_returns)
    units_float = 1.0 / step
    units = round(units_float)
    if len(names) < 2 or abs(units - units_float) > 1e-9 or units <= 0:
        raise ValueError("step must divide 1.0 exactly and at least two assets are required")
    best_weights: dict[str, float] | None = None
    best_return: float | None = None
    evaluated = 0

    def visit(prefix: list[int], remaining: int) -> None:
        nonlocal best_weights, best_return, evaluated
        if len(prefix) == len(names) - 1:
            allocation = prefix + [remaining]
            evaluated += 1
            weights = {name: value / units for name, value in zip(names, allocation)}
            if sum(weights.get(name, 0.0) for name in reserve_assets) + 1e-12 < minimum_reserve:
                return
            turnover = one_way_turnover(current_weights, weights)
            if turnover > maximum_turnover + 1e-12:
                return
            net_return = net_expected_return(
                portfolio_expected_return(weights, expected_returns),
                turnover,
                transaction_cost_bps,
            )
            if best_return is None or net_return > best_return:
                best_weights, best_return = weights, net_return
            return
        for value in range(remaining + 1):
            visit(prefix + [value], remaining - value)

    visit([], units)
    return MaximumReturnResult(best_weights, best_return, evaluated, step)


def minimum_volatility_grid(
    expected_returns: Mapping[str, float],
    covariance: Mapping[str, Mapping[str, float]],
    *,
    minimum_return: float,
    reserve_assets: set[str],
    minimum_reserve: float,
    current_weights: Mapping[str, float] | None,
    maximum_turnover: float | None,
    transaction_cost_bps: float = 0.0,
    step: float = 0.01,
) -> OptimizationResult:
    """Search all long-only, fully invested grid portfolios without relaxing constraints."""
    names = tuple(expected_returns)
    if set(covariance) != set(names):
        raise ValueError("covariance assets must match expected returns")
    units_float = 1.0 / step
    units = round(units_float)
    if len(names) < 2 or abs(units - units_float) > 1e-9 or units <= 0:
        raise ValueError("step must divide 1.0 exactly and at least two assets are required")
    if current_weights is None and maximum_turnover is not None:
        return OptimizationResult(
            False, None, 0, 0, "turnover constraint requires current weights", step
        )

    best: dict[str, float] | None = None
    best_variance: float | None = None
    evaluated = 0
    feasible = 0

    def visit(prefix: list[int], remaining: int) -> None:
        nonlocal best, best_variance, evaluated, feasible
        if len(prefix) == len(names) - 1:
            allocation = prefix + [remaining]
            evaluated += 1
            weights = {name: value / units for name, value in zip(names, allocation)}
            if sum(weights.get(name, 0.0) for name in reserve_assets) + 1e-12 < minimum_reserve:
                return
            turnover = (
                one_way_turnover(current_weights, weights)
                if current_weights is not None
                else 0.0
            )
            if maximum_turnover is not None and current_weights is not None:
                if turnover > maximum_turnover + 1e-12:
                    return
            gross_return = portfolio_expected_return(weights, expected_returns)
            if (
                net_expected_return(gross_return, turnover, transaction_cost_bps)
                + 1e-12
                < minimum_return
            ):
                return
            feasible += 1
            variance = portfolio_variance(weights, covariance)
            if best_variance is None or variance < best_variance - 1e-15:
                best, best_variance = weights, variance
            return
        for value in range(remaining + 1):
            visit(prefix + [value], remaining - value)

    visit([], units)
    if best is None:
        return OptimizationResult(
            False,
            None,
            evaluated,
            0,
            "no grid portfolio satisfies every supplied constraint",
            step,
        )
    return OptimizationResult(True, best, evaluated, feasible, "feasible", step)
