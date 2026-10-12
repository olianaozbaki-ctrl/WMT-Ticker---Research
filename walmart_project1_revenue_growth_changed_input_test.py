"""Isolated Walmart Project 1 V2 revenue-growth changed-input test.

The test runs the original base case and a case that reduces only FY2027-
FY2031 revenue growth by exactly one percentage point per year. It does not
modify either underlying model or the locked pre-run prediction record.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

import project1_fcff_v2 as dcf
import walmart_project1_proforma_v2 as proforma


EXPECTED_BASE_GROWTH = {
    2027: 0.043,
    2028: 0.042,
    2029: 0.040,
    2030: 0.038,
    2031: 0.035,
}
CHANGED_GROWTH = {
    2027: 0.033,
    2028: 0.032,
    2029: 0.030,
    2030: 0.028,
    2031: 0.025,
}
REPORTED_BASELINE_PER_SHARE = 35.67


def changed_inputs() -> Dict[str, Any]:
    """Change only the revenue-growth schedule and prove input isolation."""
    source_snapshot = deepcopy(proforma.BASE_INPUTS)
    if source_snapshot["revenue_growth"] != EXPECTED_BASE_GROWTH:
        raise ValueError(
            "Base revenue growth no longer matches the locked test specification"
        )

    changed = deepcopy(source_snapshot)
    changed["revenue_growth"] = deepcopy(CHANGED_GROWTH)

    for key, base_value in source_snapshot.items():
        if key != "revenue_growth" and changed[key] != base_value:
            raise ValueError(f"Unauthorized independent-input change: {key}")
    if any(
        abs(changed["revenue_growth"][year] - (base_rate - 0.01)) > 1e-12
        for year, base_rate in EXPECTED_BASE_GROWTH.items()
    ):
        raise ValueError("Revenue-growth change is not exactly one percentage point")
    if proforma.BASE_INPUTS != source_snapshot:
        raise ValueError("Underlying v2 base inputs were mutated")
    return changed


def run_case(inputs: Dict[str, Any]) -> Dict[str, Any]:
    rows = proforma.build_projection(inputs)
    checks = proforma.accounting_check_summary(rows, inputs)
    schedule = dcf.fcff_schedule(rows, inputs)
    valuation = (
        dcf.value(schedule, dcf.WACC, dcf.TERMINAL_GROWTH)
        if checks["valid"]
        else None
    )
    return {
        "rows": rows,
        "checks": checks,
        "schedule": schedule,
        "valuation": valuation,
    }


def run_test() -> Dict[str, Any]:
    base_inputs = deepcopy(proforma.BASE_INPUTS)
    changed = changed_inputs()
    base = run_case(base_inputs)
    changed_case = run_case(changed)
    return {"base": base, "changed": changed_case, "changed_inputs": changed}


def _case_summary(label: str, case: Dict[str, Any]) -> None:
    checks = case["checks"]
    print(
        f"{label} controls: {checks['status']} | max balance gap "
        f"{checks['max_abs_balance_gap']:.6f}M | minimum cash "
        f"${checks['minimum_cash']:,.1f}M | maximum revolver "
        f"${checks['maximum_revolver']:,.1f}M"
    )
    if checks["issues"]:
        print(f"{label} failures: " + "; ".join(checks["issues"]))
    else:
        print(f"{label} failures: none")


def _signed_money(value: float, decimals: int) -> str:
    sign = "+" if value >= 0.0 else "-"
    return f"{sign}${abs(value):,.{decimals}f}"


def main() -> None:
    result = run_test()
    base = result["base"]
    changed = result["changed"]
    base_value = base["valuation"]
    changed_value = changed["valuation"]

    print("WALMART PROJECT 1 V2 -- REVENUE-GROWTH CHANGED-INPUT TEST")
    print("Diagnostic output; not a final valuation or investment recommendation")
    print(
        "Fixed valuation inputs: WACC 7.00% | terminal growth 2.50% | "
        "cash $10,727M | borrowings $44,762M | finance leases $6,761M | "
        "diluted shares 8,022M"
    )
    print("Independent-input isolation: PASS -- only revenue_growth changed")
    print("Year   Base growth   Changed growth   Change")
    for year in proforma.YEARS:
        base_rate = EXPECTED_BASE_GROWTH[year]
        changed_rate = result["changed_inputs"]["revenue_growth"][year]
        print(
            f"{year}       {base_rate:6.2%}           {changed_rate:6.2%}    "
            f"{changed_rate - base_rate:+.2%}"
        )

    print("\nYear      Base FCFF   Changed FCFF    FCFF change")
    for base_row, changed_row in zip(base["schedule"], changed["schedule"]):
        difference = changed_row["fcff"] - base_row["fcff"]
        print(
            f"{base_row['year']}  ${base_row['fcff']:11,.3f}M"
            f"  ${changed_row['fcff']:11,.3f}M  "
            f"{_signed_money(difference, 3):>12}M"
        )

    _case_summary("Base", base)
    _case_summary("Changed-input", changed)

    if base_value is None or changed_value is None:
        print("Valuation: not presented because at least one case failed model controls")
        return

    difference_from_reported = (
        changed_value["per_share"] - REPORTED_BASELINE_PER_SHARE
    )
    difference_from_actual = changed_value["per_share"] - base_value["per_share"]
    print("\nValuation results")
    print(
        f"Base: EV ${base_value['enterprise_value']:,.3f}M | "
        f"equity ${base_value['equity_value']:,.3f}M | "
        f"${base_value['per_share']:.6f}/share | terminal share "
        f"{base_value['terminal_share']:.6%}"
    )
    print(
        f"Changed-input: EV ${changed_value['enterprise_value']:,.3f}M | "
        f"equity ${changed_value['equity_value']:,.3f}M | "
        f"${changed_value['per_share']:.6f}/share | terminal share "
        f"{changed_value['terminal_share']:.6%}"
    )
    print(
        f"Changed-input difference from reported $35.67 baseline: "
        f"{_signed_money(difference_from_reported, 6)}/share"
    )
    print(
        f"Changed-input difference from unrounded actual base "
        f"(${base_value['per_share']:.6f}): "
        f"{_signed_money(difference_from_actual, 6)}/share"
    )


if __name__ == "__main__":
    main()
