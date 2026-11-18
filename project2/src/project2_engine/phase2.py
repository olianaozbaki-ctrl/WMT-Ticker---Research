"""End-to-end Phase 2 analysis assembled from the tested engine."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .calculations import (
    net_expected_return,
    one_way_turnover,
    portfolio_expected_return,
    portfolio_volatility,
    transaction_cost_rate,
)
from .config import load_mandate
from .data import estimate_from_monthly_prices, load_cpi_yoy
from .mandate import validate_mandate
from .models import AssetDefinition
from .optimizer import maximum_net_return_grid, minimum_volatility_grid
from .signals import load_dgs10_signal
from .stress import build_stress_matrix


TICKERS = ("BIL", "IEF", "LQD", "VT")


def _assets(mandate: Mapping[str, Any]) -> dict[str, AssetDefinition]:
    universe = {item["ticker"]: item for item in mandate["project_universe"]}
    return {
        ticker: AssetDefinition(
            ticker,
            None,
            universe[ticker]["liquidity_business_days"],
            universe[ticker]["reserve_eligible"],
        )
        for ticker in TICKERS
    }


def _rule_dict(rule: Any) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "label": rule.label,
        "status": rule.status.value,
        "measured_value": rule.measured_value,
        "limit_value": rule.limit_value,
        "units": rule.units,
        "explanation": rule.explanation,
        "required_for_feasibility": rule.required_for_feasibility,
    }


def run_phase2(project_root: Path | str) -> dict[str, Any]:
    """Run the frozen Phase 2 analysis and return JSON-serializable results."""
    root = Path(project_root)
    mandate = load_mandate(root / "config" / "mandate.json")
    estimates = estimate_from_monthly_prices(root / "data" / "prices_monthly.csv")
    provenance = json.loads(
        (root / "data" / "market_data_provenance.json").read_text(encoding="utf-8")
    )
    signal = load_dgs10_signal(root / "data" / "dgs10_pit.csv", "2026-10-05")
    cpi_yoy = load_cpi_yoy(
        root / "data" / "cpi_snapshot.csv", "2026-09-01", "2025-09-01"
    )
    stress = build_stress_matrix(mandate, estimates, cpi_yoy, signal)
    hurdle = cpi_yoy + mandate["objective"]["real_return_spread"]
    illustrative_current = mandate["turnover"]["illustrative_starting_allocation"]["weights"]
    cost_bps = mandate["costs"]["transaction_cost_bps"]

    equal = {ticker: 0.25 for ticker in TICKERS}
    benchmark = {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60}
    optimization = minimum_volatility_grid(
        estimates.annual_expected_returns,
        estimates.annual_covariance,
        minimum_return=hurdle,
        reserve_assets={"BIL"},
        minimum_reserve=mandate["reserve"]["minimum_weight"],
        current_weights=illustrative_current,
        maximum_turnover=None,
        transaction_cost_bps=cost_bps,
        step=0.01,
    )
    hypothetical_turnover_check = minimum_volatility_grid(
        estimates.annual_expected_returns,
        estimates.annual_covariance,
        minimum_return=hurdle,
        reserve_assets={"BIL"},
        minimum_reserve=mandate["reserve"]["minimum_weight"],
        current_weights=illustrative_current,
        maximum_turnover=mandate["turnover"]["maximum"],
        transaction_cost_bps=cost_bps,
        step=0.01,
    )
    hypothetical_maximum_return = maximum_net_return_grid(
        estimates.annual_expected_returns,
        reserve_assets={"BIL"},
        minimum_reserve=mandate["reserve"]["minimum_weight"],
        current_weights=illustrative_current,
        maximum_turnover=mandate["turnover"]["maximum"],
        transaction_cost_bps=cost_bps,
        step=0.01,
    )
    portfolios: list[tuple[str, str, dict[str, float]]] = [
        ("Equal weight", "baseline", equal),
        ("60/40 benchmark", "baseline", benchmark),
    ]
    if optimization.weights is not None:
        portfolios.append(
            ("Constrained minimum volatility", "provisional_model_portfolio", optimization.weights)
        )

    assets = _assets(mandate)
    results = []
    for name, kind, weights in portfolios:
        turnover = one_way_turnover(illustrative_current, weights)
        gross = portfolio_expected_return(weights, estimates.annual_expected_returns)
        cost = transaction_cost_rate(turnover, cost_bps)
        report = validate_mandate(
            weights,
            assets,
            mandate,
            expected_returns=estimates.annual_expected_returns,
            current_weights=None,
            transaction_cost_bps=cost_bps,
            cpi_yoy=cpi_yoy,
            investment_horizon_years=7,
            rebalance_interval_years=1,
        )
        results.append(
            {
                "name": name,
                "kind": kind,
                "weights": weights,
                "annual_expected_return": gross,
                "annual_volatility": portfolio_volatility(weights, estimates.annual_covariance),
                "reserve_allocation": weights["BIL"],
                "illustrative_turnover_from_equal_weight": turnover,
                "illustrative_transaction_cost_rate": cost,
                "illustrative_net_expected_return": net_expected_return(gross, turnover, cost_bps),
                "liquidity_status": "NOT_TESTABLE",
                "verified_mandate_feasible": report.model_feasible,
                "rules": [_rule_dict(rule) for rule in report.results],
            }
        )

    return {
        "phase": 2,
        "generated_by": "scripts/generate_phase2_results.py",
        "analysis_date": datetime.now(timezone.utc).date().isoformat(),
        "source_retrieval_date": provenance["retrieval_date"],
        "source_retrieved_at_utc": provenance.get("source_retrieved_at_utc"),
        "data_processed_at_utc": provenance.get("processed_at_utc"),
        "market_data_as_of": provenance["price_data"]["as_of_date"],
        "price_observations": provenance["price_data"]["aligned_rows"],
        "monthly_return_observations": len(estimates.observation_dates) - 1,
        "annual_expected_returns_by_asset": estimates.annual_expected_returns,
        "cpi_yoy": cpi_yoy,
        "provisional_after_cost_hurdle": hurdle,
        "cpi_vintage_verified": provenance["cpi_data"]["alfred_vintage_verified"],
        "dgs10_signal": signal,
        "stress_matrix": stress,
        "optimization": {
            "provisional_feasible_on_supported_model_inputs": optimization.feasible,
            "full_mandate_feasible": False,
            "reason": optimization.reason,
            "grid_step": optimization.grid_step,
            "combinations_evaluated": optimization.combinations_evaluated,
            "feasible_combinations": optimization.feasible_combinations,
            "constraints_enforced": [
                "long-only",
                "weights sum to 100%",
                "BIL reserve at least 3%",
                "provisional CPI + 4% after illustrative one-way trading cost",
            ],
            "constraints_not_claimed_as_verified": [
                "turnover: actual Meridian holdings and as-of date unavailable",
                "liquidity: independent five-business-day evidence unavailable",
                "CPI vintage: current FRED snapshot is not an ALFRED-vintage verification",
                "issuer exposure: diversified-fund exemption and look-through treatment are unverified",
            ],
            "hypothetical_turnover_cap_stop_condition": {
                "starting_holdings": "Hypothetical equal weight; not actual Meridian holdings",
                "maximum_turnover": mandate["turnover"]["maximum"],
                "feasible": hypothetical_turnover_check.feasible,
                "reason": hypothetical_turnover_check.reason,
                "combinations_evaluated": hypothetical_turnover_check.combinations_evaluated,
                "feasible_combinations": hypothetical_turnover_check.feasible_combinations,
                "maximum_net_expected_return": hypothetical_maximum_return.net_expected_return,
                "maximum_return_weights": hypothetical_maximum_return.weights,
                "return_hurdle": hurdle,
                "return_shortfall": (
                    None
                    if hypothetical_maximum_return.net_expected_return is None
                    else hurdle - hypothetical_maximum_return.net_expected_return
                ),
            },
        },
        "portfolios": results,
        "limitations": [
            "Historical arithmetic means are estimates, not forecasts or promised returns.",
            "Turnover and transaction costs use a hypothetical equal-weight starting allocation and illustrative 10 bps cost; neither is actual Meridian evidence.",
            "ETF five-business-day liquidity remains unverified, so no portfolio is reported as fully mandate-compliant.",
            "The CPI hurdle uses a current FRED snapshot; ALFRED vintage verification remains outstanding.",
            "The 1% grid solution is discrete and may differ from a continuous optimum.",
        ],
    }
