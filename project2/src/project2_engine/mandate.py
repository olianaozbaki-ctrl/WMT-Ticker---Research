"""Rule-level Meridian mandate validation with no silent passes."""

from dataclasses import dataclass
from math import isclose
from typing import Any, Mapping, Optional

from .calculations import (
    net_expected_return,
    one_way_turnover,
    portfolio_expected_return,
    weight_total,
)
from .models import AssetDefinition, RuleResult, RuleStatus


WEIGHT_TOLERANCE = 1e-9


@dataclass(frozen=True)
class ValidationReport:
    """Complete rule list and a conservative model-feasibility conclusion."""

    results: tuple[RuleResult, ...]

    @property
    def model_feasible(self) -> bool:
        required = [result for result in self.results if result.required_for_feasibility]
        return bool(required) and all(result.status is RuleStatus.PASS for result in required)

    def by_id(self) -> dict[str, RuleResult]:
        return {result.rule_id: result for result in self.results}


def _result(
    rule_id: str,
    label: str,
    passed: bool,
    measured: Optional[float],
    limit: Optional[float],
    units: str,
    explanation: str,
    required: bool = True,
) -> RuleResult:
    return RuleResult(
        rule_id=rule_id,
        label=label,
        status=RuleStatus.PASS if passed else RuleStatus.FAIL,
        measured_value=measured,
        limit_value=limit,
        units=units,
        explanation=explanation,
        required_for_feasibility=required,
    )


def _untestable(
    rule_id: str, label: str, explanation: str, required: bool = True
) -> RuleResult:
    return RuleResult(
        rule_id=rule_id,
        label=label,
        status=RuleStatus.NOT_TESTABLE,
        measured_value=None,
        limit_value=None,
        units="",
        explanation=explanation,
        required_for_feasibility=required,
    )


def validate_mandate(
    weights: Mapping[str, float],
    assets: Mapping[str, AssetDefinition],
    mandate: Mapping[str, Any],
    *,
    expected_returns: Optional[Mapping[str, float]] = None,
    current_weights: Optional[Mapping[str, float]] = None,
    transaction_cost_bps: Optional[float] = None,
    cpi_yoy: Optional[float] = None,
    investment_horizon_years: Optional[float] = None,
    rebalance_interval_years: Optional[float] = None,
    uses_borrowing: bool = False,
    uses_derivatives: bool = False,
) -> ValidationReport:
    """Evaluate every documented Meridian rule and return individual verdicts."""
    unknown_assets = set(weights) - set(assets)
    if unknown_assets:
        raise ValueError(f"asset metadata missing for: {sorted(unknown_assets)}")

    results: list[RuleResult] = []
    total = weight_total(weights)
    results.append(
        _result(
            "weights_sum",
            "Weights sum to 100%",
            isclose(total, 1.0, abs_tol=WEIGHT_TOLERANCE),
            total,
            1.0,
            "decimal weight",
            "Portfolio weights must be fully invested and use decimal units.",
        )
    )

    minimum_weight = min(weights.values())
    results.append(
        _result(
            "long_only",
            "No short sales",
            minimum_weight >= -WEIGHT_TOLERANCE,
            minimum_weight,
            0.0,
            "decimal weight",
            "Every direct portfolio weight must be nonnegative.",
        )
    )
    results.append(
        _result(
            "no_borrowing",
            "No borrowing",
            not uses_borrowing,
            float(uses_borrowing),
            0.0,
            "Boolean indicator",
            "Borrowing is prohibited by the mandate.",
        )
    )
    results.append(
        _result(
            "no_derivatives",
            "No derivatives",
            not uses_derivatives,
            float(uses_derivatives),
            0.0,
            "Boolean indicator",
            "Direct derivative use is prohibited by the mandate.",
        )
    )

    reserve_unknown = [
        name
        for name, weight in weights.items()
        if weight > WEIGHT_TOLERANCE and assets[name].reserve_eligible is None
    ]
    if reserve_unknown:
        results.append(
            _untestable(
                "reserve",
                "Twelve-month distribution reserve",
                "Reserve eligibility is unresolved for: " + ", ".join(reserve_unknown),
            )
        )
    else:
        reserve_weight = sum(
            weight
            for name, weight in weights.items()
            if assets[name].reserve_eligible is True
        )
        reserve_limit = mandate["reserve"]["minimum_weight"]
        results.append(
            _result(
                "reserve",
                "Twelve-month distribution reserve",
                reserve_weight + WEIGHT_TOLERANCE >= reserve_limit,
                reserve_weight,
                reserve_limit,
                "decimal weight",
                "Approved reserve-eligible assets must cover four quarterly distributions.",
            )
        )

    liquidity_unknown = [
        name
        for name, weight in weights.items()
        if weight > WEIGHT_TOLERANCE and assets[name].liquidity_business_days is None
    ]
    if liquidity_unknown:
        results.append(
            _untestable(
                "liquidity",
                "Five-business-day liquidity",
                "Liquidity evidence is missing for: " + ", ".join(liquidity_unknown),
            )
        )
    else:
        window = mandate["liquidity"]["maximum_business_days"]
        liquid_weight = sum(
            weight
            for name, weight in weights.items()
            if assets[name].liquidity_business_days is not None
            and assets[name].liquidity_business_days <= window
        )
        liquid_limit = mandate["liquidity"]["minimum_weight"]
        results.append(
            _result(
                "liquidity",
                "Five-business-day liquidity",
                liquid_weight + WEIGHT_TOLERANCE >= liquid_limit,
                liquid_weight,
                liquid_limit,
                "decimal weight",
                "Only assets with documented liquidity within the mandate window count.",
            )
        )

    missing_issuers = [
        name
        for name, weight in weights.items()
        if weight > WEIGHT_TOLERANCE and not assets[name].issuer
    ]
    if missing_issuers:
        results.append(
            _untestable(
                "issuer_limit",
                "Maximum nonexempt issuer exposure",
                "Issuer metadata is missing for: " + ", ".join(missing_issuers),
            )
        )
    else:
        exempt = set(mandate["issuer_limit"]["exempt_issuers"])
        issuer_weights: dict[str, float] = {}
        for name, weight in weights.items():
            issuer = assets[name].issuer
            if issuer is not None and issuer not in exempt:
                issuer_weights[issuer] = issuer_weights.get(issuer, 0.0) + weight
        largest = max(issuer_weights.values(), default=0.0)
        issuer_limit = mandate["issuer_limit"]["maximum_weight"]
        results.append(
            _result(
                "issuer_limit",
                "Maximum nonexempt issuer exposure",
                largest <= issuer_limit + WEIGHT_TOLERANCE,
                largest,
                issuer_limit,
                "decimal weight",
                "All securities from the same nonexempt issuer are aggregated.",
            )
        )

    turnover_value: Optional[float] = None
    if current_weights is None:
        results.append(
            _untestable(
                "turnover",
                "Annual turnover limit",
                "Current weights and their as-of date are required for turnover.",
            )
        )
    else:
        current_total = weight_total(current_weights)
        if not isclose(current_total, 1.0, abs_tol=WEIGHT_TOLERANCE):
            raise ValueError("current weights must sum to 100% before turnover is tested")
        if min(current_weights.values()) < -WEIGHT_TOLERANCE:
            raise ValueError("current weights cannot be negative")
        turnover_value = one_way_turnover(current_weights, weights)
        turnover_limit = mandate["turnover"]["maximum"]
        results.append(
            _result(
                "turnover",
                "Annual turnover limit",
                turnover_value <= turnover_limit + WEIGHT_TOLERANCE,
                turnover_value,
                turnover_limit,
                "decimal turnover",
                "Turnover equals half the sum of absolute target-minus-current weights.",
            )
        )

    if investment_horizon_years is None:
        results.append(
            _untestable(
                "horizon",
                "Seven-year investment horizon",
                "The proposed process horizon was not supplied.",
            )
        )
    else:
        horizon = mandate["horizon_years"]
        results.append(
            _result(
                "horizon",
                "Seven-year investment horizon",
                investment_horizon_years == horizon,
                investment_horizon_years,
                horizon,
                "years",
                "The proposed process must be evaluated for the stated mandate horizon.",
            )
        )

    if rebalance_interval_years is None:
        results.append(
            _untestable(
                "rebalance_frequency",
                "Annual rebalancing",
                "The proposed rebalancing interval was not supplied.",
            )
        )
    else:
        results.append(
            _result(
                "rebalance_frequency",
                "Annual rebalancing",
                isclose(rebalance_interval_years, 1.0, abs_tol=WEIGHT_TOLERANCE),
                rebalance_interval_years,
                1.0,
                "years",
                "The Meridian mandate specifies annual rebalancing.",
            )
        )

    objective_inputs_available = all(
        value is not None
        for value in (expected_returns, current_weights, transaction_cost_bps, cpi_yoy)
    )
    if not objective_inputs_available:
        results.append(
            _untestable(
                "return_objective_proxy",
                "CPI + 4% after-cost expected-return proxy",
                "Expected returns, CPI, current weights, and transaction cost are all required. "
                "Passing this proxy will not prove the rolling five-year realized objective.",
            )
        )
    else:
        assert expected_returns is not None
        assert turnover_value is not None
        assert transaction_cost_bps is not None
        assert cpi_yoy is not None
        gross_return = portfolio_expected_return(weights, expected_returns)
        net_return = net_expected_return(
            gross_return, turnover_value, transaction_cost_bps
        )
        hurdle = cpi_yoy + mandate["objective"]["real_return_spread"]
        results.append(
            _result(
                "return_objective_proxy",
                "CPI + 4% after-cost expected-return proxy",
                net_return + WEIGHT_TOLERANCE >= hurdle,
                net_return,
                hurdle,
                "annual decimal return",
                "This is a forward-looking feasibility proxy, not proof of rolling five-year performance.",
            )
        )

    results.append(
        RuleResult(
            rule_id="calendar_year_loss",
            label="Calendar-year loss threshold",
            status=RuleStatus.UNRESOLVED,
            measured_value=None,
            limit_value=mandate["risk"]["loss_threshold"],
            units="annual decimal return",
            explanation=(
                "The -10% statement lacks an approved measurement and breach rule. "
                "It is monitored and escalated, never reported as a guaranteed pass."
            ),
            required_for_feasibility=False,
        )
    )

    return ValidationReport(tuple(results))
