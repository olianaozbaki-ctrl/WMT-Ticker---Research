"""Causal Walmart V3 scenarios; imports the unchanged V3 model engines.

All scenarios are diagnostics, not final valuations. The downside case is
allowed to fail liquidity controls so the financing constraint remains visible.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

import project1_fcff_v3 as dcf
import walmart_project1_proforma_v3 as proforma


SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Downside": {
        "cause": "Weaker consumer demand, competitive price pressure, slower digital/membership growth, and less favorable supplier terms.",
        "growth_shift": -0.005,
        "gross_margin_shift": -0.001,
        "opex_ratio_shift": 0.002,
        "capex_shift_m": 0.0,
        "inventory_days_shift": 1.0,
        "ap_days_shift": -0.5,
        "receivables_ratio_shift": 0.0005,
        "financing_policy": "Retain V3 debt repayments, dividends, lease additions/principal, minimum cash, and revolver limit; no financing rescue assumed.",
    },
    "Base": {
        "cause": "Current V3 operating forecast and financing policy, with no driver changes.",
        "growth_shift": 0.0,
        "gross_margin_shift": 0.0,
        "opex_ratio_shift": 0.0,
        "capex_shift_m": 0.0,
        "inventory_days_shift": 0.0,
        "ap_days_shift": 0.0,
        "receivables_ratio_shift": 0.0,
        "financing_policy": "Unchanged V3 debt repayments, dividends, lease additions/principal, minimum cash, and revolver limit.",
    },
    "Upside": {
        "cause": "Stronger digital/advertising and membership mix, resilient demand, productivity gains, and better inventory/supplier execution.",
        "growth_shift": 0.010,
        "gross_margin_shift": 0.0025,
        "opex_ratio_shift": -0.005,
        "capex_shift_m": 1_500.0,
        "inventory_days_shift": -3.0,
        "ap_days_shift": 2.0,
        "receivables_ratio_shift": -0.001,
        "financing_policy": "Retain V3 debt repayments, dividends, lease additions/principal, minimum cash, and revolver limit; incremental capex is funded from operating cash unless the model draws the revolver.",
    },
}


def scenario_inputs(name: str) -> Dict[str, Any]:
    scenario = SCENARIOS[name]
    inputs = deepcopy(proforma.BASE_INPUTS)
    for year in proforma.YEARS:
        inputs["net_sales_growth"][year] += scenario["growth_shift"]
        inputs["membership_other_growth"][year] += scenario["growth_shift"]
        inputs["gross_margin_on_net_sales"][year] += scenario["gross_margin_shift"]
        inputs["cash_opex_to_operating_gross_profit"][year] += scenario["opex_ratio_shift"]
        inputs["capex"][year] += scenario["capex_shift_m"]
    inputs["inventory_days"] += scenario["inventory_days_shift"]
    inputs["accounts_payable_days"] += scenario["ap_days_shift"]
    inputs["receivables_to_revenue"] += scenario["receivables_ratio_shift"]
    return inputs


def run_scenario(name: str) -> Dict[str, Any]:
    inputs = scenario_inputs(name)
    rows = proforma.build_projection(inputs)
    statement_checks = proforma.accounting_check_summary(rows, inputs)
    schedule = dcf.fcff_schedule(rows, inputs)

    # Calculate even for an infeasible downside to show its mechanical DCF,
    # but never present that value as financeable or fair value.
    valuation = dcf.value(schedule)
    bridge_rebuild = (
        valuation["enterprise_value"]
        + valuation["cash"]
        + valuation["nonoperating_investments"]
        - valuation["debt"]
        - valuation["finance_leases"]
        - valuation["nci"]
    )
    dcf_issues: List[str] = []
    if not (0.0 <= dcf.TERMINAL_GROWTH < dcf.WACC < 1.0):
        dcf_issues.append("WACC/terminal-growth boundary failed")
    if len(schedule) != 5:
        dcf_issues.append("FCFF forecast horizon is not five years")
    if abs(valuation["equity_value"] - bridge_rebuild) > dcf.TOLERANCE:
        dcf_issues.append("Enterprise-to-equity bridge arithmetic failed")
    if abs(valuation["per_share"] - valuation["equity_value"] / valuation["shares"]) > dcf.TOLERANCE:
        dcf_issues.append("Per-share arithmetic failed")

    return {
        "name": name,
        "inputs": inputs,
        "rows": rows,
        "schedule": schedule,
        "statement_checks": statement_checks,
        "dcf_issues": dcf_issues,
        "dcf_status": "PASS" if not dcf_issues else "FAIL",
        "valuation": valuation,
        "feasible": statement_checks["valid"] and not dcf_issues,
    }


def run_all() -> Dict[str, Any]:
    results = {name: run_scenario(name) for name in SCENARIOS}
    # Baseline controls should pass, and the upper case should remain financeable.
    for name in ("Base", "Upside"):
        if not results[name]["feasible"]:
            raise AssertionError(f"{name} unexpectedly failed: {results[name]['statement_checks']['issues']} {results[name]['dcf_issues']}")
    # Downside is intentionally not forced to pass. Its exact financing failure
    # is printed and documented as infeasible rather than repaired with a plug.
    return results


def print_case(result: Dict[str, Any]) -> None:
    name = result["name"]
    checks = result["statement_checks"]
    value = result["valuation"]
    print(f"\n{name.upper()} — {'FEASIBLE' if result['feasible'] else 'INFEASIBLE'}")
    print(f"Cause: {SCENARIOS[name]['cause']}")
    print("Year Revenue     EBIT      CapEx  Change ONWC      FCFF     Cash  Debt  Lease debt Revolver")
    for row, fcff in zip(result["rows"], result["schedule"]):
        print(
            f"{int(row['year'])} {row['revenue']:9,.1f} {row['operating_income']:9,.1f}"
            f" {row['capex']:9,.1f} {row['change_operating_nwc']:11,.1f}"
            f" {fcff['fcff']:9,.1f} {row['cash']:8,.1f} {row['debt']:7,.1f}"
            f" {row['finance_lease_obligations']:10,.1f} {row['revolver']:8,.1f}"
        )
    print(
        f"EV ${value['enterprise_value']:,.3f}M | equity ${value['equity_value']:,.3f}M"
        f" | ${value['per_share']:.4f}/share | terminal share {value['terminal_share']:.2%}"
    )
    print(
        f"Balance {checks['max_abs_balance_gap']:.8f}M | cash-flow {checks['max_abs_cash_flow_gap']:.8f}M"
        f" | debt roll {checks['max_abs_debt_roll_forward_gap']:.8f}M"
        f" | finance-lease roll {checks['max_abs_lease_roll_forward_gap']:.8f}M"
        f" | min cash ${checks['minimum_cash']:,.1f}M"
        f" | max revolver ${checks['maximum_revolver']:,.1f}M"
        f" | statement controls {checks['status']} | DCF checks {result['dcf_status']}"
    )
    for issue in checks["issues"]:
        print(f"STATEMENT FAIL: {issue}")
    for issue in result["dcf_issues"]:
        print(f"DCF FAIL: {issue}")


def main() -> None:
    results = run_all()
    print("WALMART PROJECT 1 V3 CAUSAL SCENARIOS — DIAGNOSTIC, NOT FINAL")
    print("WACC 7.00% | terminal growth 2.50% | V3 provisional bridge and August 26 basic shares")
    for name in SCENARIOS:
        print_case(results[name])
    print("\nScenario feasibility does not verify source assumptions or valuation-date inputs.")


if __name__ == "__main__":
    main()
