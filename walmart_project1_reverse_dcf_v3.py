"""Walmart Project 1 V3 reverse DCF diagnostics.

This additive analysis imports the unchanged V3 engines. It solves two separate
one-driver cases against Walmart's September 23, 2026 closing price. Results are
diagnostic and do not modify or calibrate the V3 base model.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable, Dict, Tuple

import project1_fcff_v3 as dcf
import walmart_project1_proforma_v3 as proforma


MARKET_PRICE = 110.53
MARKET_PRICE_DATE = "2026-09-23"
PRICE_SOURCE = "https://stockanalysis.com/stocks/wmt/history/"
PRICE_CROSS_CHECK = "https://chartexchange.com/symbol/nasdaq-wmt/historical/"
SOLVER_TOLERANCE = 1e-10
MAX_ITERATIONS = 200


def value_inputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Run the unchanged V3 statements, FCFF schedule, and valuation."""
    case = dcf.forecast(inputs)
    schedule = dcf.fcff_schedule(case["rows"], case["inputs"])
    valuation = dcf.value(schedule) if case["checks"]["valid"] else None
    return {**case, "schedule": schedule, "valuation": valuation}


def revenue_growth_case(additive_shift: float) -> Dict[str, Any]:
    """Shift both V3 revenue-stream growth paths by the same decimal amount."""
    inputs = deepcopy(proforma.BASE_INPUTS)
    for year in proforma.YEARS:
        inputs["net_sales_growth"][year] += additive_shift
        inputs["membership_other_growth"][year] += additive_shift
    return value_inputs(inputs)


def operating_efficiency_case(expense_ratio_reduction: float) -> Dict[str, Any]:
    """Reduce cash opex / operating gross profit by equal percentage points."""
    inputs = deepcopy(proforma.BASE_INPUTS)
    for year in proforma.YEARS:
        inputs["cash_opex_to_operating_gross_profit"][year] -= expense_ratio_reduction
        if not 0.0 < inputs["cash_opex_to_operating_gross_profit"][year] < 1.0:
            raise ValueError("Solved cash operating-expense ratio left the valid range")
    return value_inputs(inputs)


def solve(
    case_builder: Callable[[float], Dict[str, Any]],
    lower: float,
    upper: float,
) -> Tuple[float, Dict[str, Any]]:
    """Bisection solve for the driver that reproduces MARKET_PRICE."""
    low_case = case_builder(lower)
    high_case = case_builder(upper)
    if not low_case["checks"]["valid"] or not high_case["checks"]["valid"]:
        raise ValueError("A solver endpoint failed the unchanged V3 controls")
    low_value = low_case["valuation"]["per_share"]
    high_value = high_case["valuation"]["per_share"]
    if not low_value <= MARKET_PRICE <= high_value:
        raise ValueError("Solver interval does not bracket the market price")

    midpoint = lower
    result = low_case
    for _ in range(MAX_ITERATIONS):
        midpoint = (lower + upper) / 2.0
        result = case_builder(midpoint)
        if not result["checks"]["valid"]:
            raise ValueError("Solved case failed the unchanged V3 controls")
        difference = result["valuation"]["per_share"] - MARKET_PRICE
        if abs(difference) <= SOLVER_TOLERANCE:
            break
        if difference < 0.0:
            lower = midpoint
        else:
            upper = midpoint
    else:
        raise RuntimeError("Reverse-DCF solver did not converge")
    return midpoint, result


def validation_summary(case: Dict[str, Any]) -> Dict[str, Any]:
    dcf_checks = dcf.dcf_check_summary(case)
    reproduced_price = case["valuation"]["per_share"]
    issues = list(case["checks"]["issues"]) + list(dcf_checks["issues"])
    if abs(reproduced_price - MARKET_PRICE) > 1e-6:
        issues.append("Solved case did not reproduce the sourced market price")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "price_error": reproduced_price - MARKET_PRICE,
    }


def run_analysis() -> Dict[str, Any]:
    base = dcf.diagnostic_case()
    growth_shift, growth = solve(revenue_growth_case, 0.0, 0.25)
    efficiency_shift, efficiency = solve(operating_efficiency_case, 0.0, 0.25)
    results = {
        "base": base,
        "growth_shift": growth_shift,
        "growth": growth,
        "growth_validation": validation_summary(growth),
        "efficiency_shift": efficiency_shift,
        "efficiency": efficiency,
        "efficiency_validation": validation_summary(efficiency),
    }
    if not base["checks"]["valid"]:
        raise ValueError("Imported V3 base case failed its controls")
    if dcf.dcf_check_summary(base)["status"] != "PASS":
        raise ValueError("Imported V3 base DCF failed its controls")
    if results["growth_validation"]["status"] != "PASS":
        raise ValueError(results["growth_validation"])
    if results["efficiency_validation"]["status"] != "PASS":
        raise ValueError(results["efficiency_validation"])
    return results


def _print_case(label: str, case: Dict[str, Any]) -> None:
    valuation = case["valuation"]
    print(f"\n{label}")
    print("Year  Revenue      EBIT   EBIT margin      FCFF      Cash  Revolver")
    for row, fcff_row in zip(case["rows"], case["schedule"]):
        print(
            f"{int(row['year'])}  {row['revenue']:9,.1f}  {row['operating_income']:9,.1f}"
            f"  {row['operating_income'] / row['revenue']:10.4%}"
            f"  {fcff_row['fcff']:9,.1f}  {row['cash']:9,.1f}  {row['revolver']:8,.1f}"
        )
    print(
        f"EV ${valuation['enterprise_value']:,.3f}M | equity ${valuation['equity_value']:,.3f}M"
        f" | price ${valuation['per_share']:.8f} | terminal share {valuation['terminal_share']:.2%}"
    )


def main() -> None:
    result = run_analysis()
    growth_rates = [
        result["growth"]["inputs"]["net_sales_growth"][year]
        for year in proforma.YEARS
    ]
    expense_ratios = [
        result["efficiency"]["inputs"]["cash_opex_to_operating_gross_profit"][year]
        for year in proforma.YEARS
    ]
    print("WALMART PROJECT 1 V3 REVERSE DCF -- DIAGNOSTIC, NOT FINAL")
    print(f"Market close ${MARKET_PRICE:.2f} on {MARKET_PRICE_DATE}")
    print(f"V3 base ${result['base']['valuation']['per_share']:.8f}")
    print(f"Growth-path additive shift: {result['growth_shift']:.8%}")
    print("Solved growth path: " + ", ".join(f"{value:.4%}" for value in growth_rates))
    print(f"Cash-opex ratio reduction: {result['efficiency_shift']:.8%}")
    print("Solved cash-opex ratios: " + ", ".join(f"{value:.4%}" for value in expense_ratios))
    _print_case("REVENUE-GROWTH SOLVE", result["growth"])
    _print_case("OPERATING-EFFICIENCY SOLVE", result["efficiency"])
    print(
        "\nValidation: growth solve " + result["growth_validation"]["status"]
        + " | efficiency solve " + result["efficiency_validation"]["status"]
        + " | unchanged V3 statement and DCF controls PASS"
    )


if __name__ == "__main__":
    main()
