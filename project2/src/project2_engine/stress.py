"""Reproducible, explicit-stop portfolio stress matrix."""

from __future__ import annotations

from datetime import date
from statistics import mean
from typing import Any

from .calculations import net_expected_return, one_way_turnover, portfolio_expected_return, portfolio_variance, portfolio_volatility, transaction_cost_rate
from .mandate import validate_mandate
from .models import AssetDefinition
from .optimizer import minimum_volatility_grid


def _correlation_stress(covariance: dict[str, dict[str, float]], blend: float = 0.5) -> dict[str, dict[str, float]]:
    """Blend a valid correlation matrix with a valid equicorrelation matrix."""
    if not 0.0 <= blend <= 1.0:
        raise ValueError("blend must be between zero and one")
    names = tuple(covariance)
    vols = {name: covariance[name][name] ** 0.5 for name in names}
    correlations = {name: {} for name in names}
    for first in names:
        for second in names:
            correlations[first][second] = covariance[first][second] / (vols[first] * vols[second]) if vols[first] and vols[second] else float(first == second)
    # Equicorrelation rho=0.75 is PSD for n=4 (rho >= -1/(n-1)); convex blends preserve PSD.
    rho = 0.75
    result = {name: {} for name in names}
    for first in names:
        for second in names:
            target = 1.0 if first == second else rho
            corr = (1.0 - blend) * correlations[first][second] + blend * target
            result[first][second] = corr * vols[first] * vols[second]
    # Retain the financial engine's full symmetry and PSD validation.
    portfolio_variance({name: 1.0 / len(names) for name in names}, result)
    return result


def build_stress_matrix(mandate: dict[str, Any], estimates: Any, cpi_yoy: float, signal: dict[str, Any]) -> dict[str, Any]:
    names = estimates.tickers
    decision_date = date.fromisoformat(signal["decision_date"])
    # Price returns are dated by their ending month. Exclude any return whose
    # observation endpoint is after the signal decision date.
    eligible_endpoints = tuple(d for d in estimates.observation_dates[1:] if d <= decision_date)
    if len(eligible_endpoints) < 2:
        raise ValueError("stress decision boundary leaves too few returns to estimate covariance")
    n_eligible = len(eligible_endpoints)
    aligned_returns = {k: tuple(v[:n_eligible]) for k, v in estimates.monthly_returns.items()}
    full_r, full_c = _estimates_from_returns(aligned_returns)
    short_r, short_c = estimates_for_window_from_returns(aligned_returns, 36)
    market_as_of = eligible_endpoints[-1].isoformat()
    hurdle = cpi_yoy + mandate["objective"]["real_return_spread"]
    reserve_floor = mandate["reserve"]["minimum_weight"]
    base = {"BIL": .25, "IEF": .25, "LQD": .25, "VT": .25}
    assets = {ticker: AssetDefinition(ticker, None, None, mandate["project_universe"][i]["reserve_eligible"]) for i, ticker in enumerate(names)}
    scenarios: list[dict[str, Any]] = []

    def run(label: str, returns: dict[str, float], covariance: dict[str, dict[str, float]], cost: float, reserve_min: float, turn_cap: float | None, window: str, category: str, signal_available: bool = True) -> None:
        opt = minimum_volatility_grid(returns, covariance, minimum_return=hurdle, reserve_assets={"BIL"}, minimum_reserve=reserve_min, current_weights=base, maximum_turnover=turn_cap, transaction_cost_bps=cost, step=.01)
        weights = opt.weights
        comparisons = []
        comparison_weights = {
            "Equal weight": base,
            "60/40 benchmark": {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60},
        }
        if weights is not None:
            comparison_weights["Reoptimized minimum volatility"] = weights
        for portfolio_name, portfolio_weights in comparison_weights.items():
            portfolio_turnover = one_way_turnover(base, portfolio_weights)
            gross_return = portfolio_expected_return(portfolio_weights, returns)
            report = validate_mandate(portfolio_weights, assets, mandate, expected_returns=returns, current_weights=None, transaction_cost_bps=cost, cpi_yoy=cpi_yoy, investment_horizon_years=7, rebalance_interval_years=1)
            comparisons.append({"portfolio":portfolio_name,"weights":portfolio_weights,"annual_expected_return":gross_return,"net_expected_return":net_expected_return(gross_return,portfolio_turnover,cost),"annual_volatility":portfolio_volatility(portfolio_weights,covariance),"turnover_from_hypothetical_equal_weight":portfolio_turnover,"cost_rate":transaction_cost_rate(portfolio_turnover,cost),"optimizer_feasible":portfolio_name != "Reoptimized minimum volatility" or opt.feasible,"mandate_verdicts":{r.rule_id:r.status.value for r in report.results}})
        if weights is None:
            comparisons.append({"portfolio":"Reoptimized minimum volatility","weights":None,"annual_expected_return":None,"net_expected_return":None,"annual_volatility":None,"turnover_from_hypothetical_equal_weight":None,"cost_rate":None,"optimizer_feasible":False,"mandate_verdicts":{},"stop_reason":opt.reason})
            scenarios.append({"scenario":label,"category":category,"window":window,"status":"STOP_INFEASIBLE","reason":opt.reason,"combinations_evaluated":opt.combinations_evaluated,"weights":None,"annual_expected_return":None,"net_expected_return":None,"annual_volatility":None,"turnover":None,"cost_rate":None,"feasible":False,"mandate_verdicts":{},"portfolio_comparisons":comparisons,"signal_available":signal_available})
            return
        turnover = one_way_turnover(base, weights)
        gross = portfolio_expected_return(weights, returns)
        report = validate_mandate(weights, assets, mandate, expected_returns=returns, current_weights=None, transaction_cost_bps=cost, cpi_yoy=cpi_yoy, investment_horizon_years=7, rebalance_interval_years=1)
        scenarios.append({"scenario":label,"category":category,"window":window,"status":"PROVISIONAL_FEASIBLE","reason":"All scenario optimizer constraints passed; full mandate evidence remains incomplete.","combinations_evaluated":opt.combinations_evaluated,"weights":weights,"annual_expected_return":gross,"net_expected_return":net_expected_return(gross,turnover,cost),"annual_volatility":portfolio_volatility(weights,covariance),"turnover":turnover,"cost_rate":transaction_cost_rate(turnover,cost),"feasible":True,"mandate_verdicts":{r.rule_id:r.status.value for r in report.results},"portfolio_comparisons":comparisons,"signal_available":signal_available})

    full_window = f"full aligned window ({n_eligible} monthly returns)"
    short_window = "36 monthly returns"
    run("baseline_full_window",dict(full_r),full_c,10,reserve_floor,None,full_window,"baseline")
    run("return_estimates_minus_2pp",{k:v-.02 for k,v in full_r.items()},full_c,10,reserve_floor,None,full_window,"expected_return")
    run("return_estimates_plus_2pp",{k:v+.02 for k,v in full_r.items()},full_c,10,reserve_floor,None,full_window,"expected_return")
    run("last_36_months",short_r,short_c,10,reserve_floor,None,short_window,"window")
    for cost in (0,25): run(f"transaction_cost_{cost}bps",dict(full_r),full_c,cost,reserve_floor,None,full_window,"cost")
    run("reserve_minimum_10pct",dict(full_r),full_c,10,.10,None,full_window,"constraint")
    run("turnover_cap_25pct_hypothetical",dict(full_r),full_c,10,reserve_floor,.25,full_window,"constraint")
    run("volatility_plus_25pct",dict(full_r),{k:{j:v*1.5625 for j,v in row.items()} for k,row in full_c.items()},10,reserve_floor,None,full_window,"risk")
    run("correlations_psd_convex_blend_50pct",dict(full_r),_correlation_stress(full_c),10,reserve_floor,None,full_window,"risk")
    run("signal_available_review_only",dict(full_r),full_c,10,reserve_floor,None,full_window,"signal",bool(signal.get("available")))
    run("signal_unavailable_no_tilt",dict(full_r),full_c,10,reserve_floor,None,full_window,"signal",False)
    return {"decision_date":signal["decision_date"],"market_data_as_of":market_as_of,"market_return_observations":n_eligible,"signal_observation_date":signal["observation_date"],"signal_availability_date":signal["availability_date"],"signal_boundary_consistent":market_as_of <= signal["decision_date"] and signal["observation_date"] <= signal["decision_date"] and signal["availability_date"] <= signal["decision_date"],"assumptions":"Each numerical scenario is a modeling stress. Historical asset returns/covariance are altered mechanically; none is a forecast or verified market shock. Market returns are restricted to observation endpoints available on the signal decision date. No signal scenario changes weights because the approved signal role is review-only.","scenarios":scenarios}


def estimates_for_window(estimates: Any, months: int) -> tuple[dict[str,float],dict[str,dict[str,float]]]:
    return estimates_for_window_from_returns(estimates.monthly_returns, months)


def estimates_for_window_from_returns(monthly_returns: dict[str, tuple[float, ...]], months: int) -> tuple[dict[str,float],dict[str,dict[str,float]]]:
    if months < 2 or any(len(v) < months for v in monthly_returns.values()):
        raise ValueError("window must contain at least two available monthly returns")
    returns={k:tuple(v[-months:]) for k,v in monthly_returns.items()}
    return _estimates_from_returns(returns)


def _estimates_from_returns(returns: dict[str, tuple[float, ...]]) -> tuple[dict[str,float],dict[str,dict[str,float]]]:
    sample_size = len(next(iter(returns.values())))
    if sample_size < 2 or any(len(v) != sample_size for v in returns.values()):
        raise ValueError("aligned returns must have equal lengths of at least two")
    means={k:mean(v) for k,v in returns.items()}
    cov={a:{} for a in returns}
    for a in returns:
        for b in returns:
            cov[a][b]=sum((x-means[a])*(y-means[b]) for x,y in zip(returns[a],returns[b]))/(sample_size-1)*12
    return {k:v*12 for k,v in means.items()},cov
