"""Diagnostic Walmart Project 1 V3 FCFF DCF and V2-to-V3 reconciliation.

V3 uses the closest SEC-filed pre-September 23 bridge observations. They are
provisional, not exact valuation-date measures. The share denominator is the
August 26 basic spot count and therefore produces a provisional value per basic
share, not a final diluted fair value.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List

import project1_fcff_v2 as v2
import walmart_project1_proforma_v3 as source


WACC = 0.0700
TERMINAL_GROWTH = 0.0250

# Closest SEC-filed facts available before the proposed September 23, 2026 date.
PROVISIONAL_BASIC_SHARES_M = 7_933.746241  # August 26, 2026; not diluted.
BRIDGE_CASH_M = 11_529.0  # July 31, 2026; total cash, not verified excess cash.
SHORT_TERM_DEBT_FAIR_VALUE_PROXY_M = 10_479.0  # Carrying value approximates fair value.
LONG_TERM_DEBT_FAIR_VALUE_M = 37_267.0  # July 31 disclosed fair value.
BRIDGE_DEBT_FAIR_VALUE_PROXY_M = (
    SHORT_TERM_DEBT_FAIR_VALUE_PROXY_M + LONG_TERM_DEBT_FAIR_VALUE_M
)
BRIDGE_FINANCE_LEASES_M = 6_832.0  # July 31, 2026 carrying value.
BRIDGE_NCI_M = 0.0  # No supported September 23 market value; unresolved, not assumed immaterial.
BRIDGE_NONOPERATING_INVESTMENTS_M = 0.0  # Unresolved; avoids unsupported addition.
TOLERANCE = 1e-6


def forecast(inputs: Dict[str, Any] | None = None) -> Dict[str, Any]:
    assumptions = deepcopy(source.BASE_INPUTS if inputs is None else inputs)
    rows = source.build_projection(assumptions)
    checks = source.accounting_check_summary(rows, assumptions)
    return {"rows": rows, "inputs": assumptions, "checks": checks}


def fcff_schedule(
    rows: List[Dict[str, float]], inputs: Dict[str, Any]
) -> List[Dict[str, float]]:
    """Calculate lease-consistent FCFF under a financing convention."""
    schedule: List[Dict[str, float]] = []
    for row in rows:
        cash_operating_tax = max(0.0, row["operating_income"]) * inputs["cash_tax_rate"]
        nopat = row["operating_income"] - cash_operating_tax
        # Finance-lease interest and principal are financing cash flows. New
        # finance-lease ROU assets are economic capex and are deducted here.
        fcff = (
            nopat
            + row["depreciation"]
            - row["capex"]
            - row["finance_lease_additions"]
            - row["change_operating_nwc"]
        )
        schedule.append(
            {
                "year": int(row["year"]),
                "revenue": row["revenue"],
                "ebit": row["operating_income"],
                "cash_operating_tax": cash_operating_tax,
                "nopat": nopat,
                "d_and_a": row["depreciation"],
                "capex": row["capex"],
                "finance_lease_additions": row["finance_lease_additions"],
                "change_operating_nwc": row["change_operating_nwc"],
                "fcff": fcff,
            }
        )
    return schedule


def value(
    schedule: List[Dict[str, float]],
    *,
    cash: float = BRIDGE_CASH_M,
    debt: float = BRIDGE_DEBT_FAIR_VALUE_PROXY_M,
    finance_leases: float = BRIDGE_FINANCE_LEASES_M,
    nci: float = BRIDGE_NCI_M,
    nonoperating_investments: float = BRIDGE_NONOPERATING_INVESTMENTS_M,
    shares: float = PROVISIONAL_BASIC_SHARES_M,
    wacc: float = WACC,
    g: float = TERMINAL_GROWTH,
) -> Dict[str, float]:
    if not (0.0 <= g < wacc < 1.0):
        raise ValueError("DCF rate boundary violated: require 0 <= g < WACC < 1")
    if len(schedule) != 5:
        raise ValueError("Expected a five-year FCFF schedule")
    if shares <= 0.0:
        raise ValueError("Share denominator must be positive")
    pv_explicit = sum(
        row["fcff"] / (1.0 + wacc) ** index
        for index, row in enumerate(schedule, start=1)
    )
    terminal_fcff = schedule[-1]["fcff"] * (1.0 + g)
    pv_terminal = terminal_fcff / (wacc - g) / (1.0 + wacc) ** len(schedule)
    enterprise_value = pv_explicit + pv_terminal
    equity_value = (
        enterprise_value
        + cash
        + nonoperating_investments
        - debt
        - finance_leases
        - nci
    )
    bridge_check = (
        enterprise_value
        + cash
        + nonoperating_investments
        - debt
        - finance_leases
        - nci
    )
    if abs(equity_value - bridge_check) > TOLERANCE:
        raise ValueError("Enterprise-to-equity bridge arithmetic failed")
    return {
        "pv_explicit": pv_explicit,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share": equity_value / shares,
        "terminal_share": pv_terminal / enterprise_value,
        "cash": cash,
        "debt": debt,
        "finance_leases": finance_leases,
        "nci": nci,
        "nonoperating_investments": nonoperating_investments,
        "shares": shares,
    }


def _revenue_only_inputs() -> Dict[str, Any]:
    """Correct revenue definitions while retaining V2 D&A/lease behavior."""
    inputs = deepcopy(source.BASE_INPUTS)
    inputs["nonlease_d_and_a_to_opening_ppe"] = 0.106
    inputs["finance_lease_amortization_to_opening_rou"] = 0.0
    inputs["finance_lease_additions"] = {year: 0.0 for year in source.YEARS}
    inputs["finance_lease_principal"] = {year: 0.0 for year in source.YEARS}
    inputs["enforce_fy2026_d_and_a_reconciliation"] = False
    return inputs


def _d_and_a_corrected_inputs() -> Dict[str, Any]:
    """Add reconciled D&A while leaving the finance-lease liability static."""
    inputs = deepcopy(source.BASE_INPUTS)
    inputs["finance_lease_additions"] = {year: 0.0 for year in source.YEARS}
    inputs["finance_lease_principal"] = {year: 0.0 for year in source.YEARS}
    return inputs


def _run_operating_case(inputs: Dict[str, Any]) -> Dict[str, Any]:
    case = forecast(inputs)
    case["schedule"] = fcff_schedule(case["rows"], case["inputs"])
    case["valuation_v2_bridge"] = (
        value(
            case["schedule"],
            cash=v2.CASH_M,
            debt=v2.BORROWINGS_M,
            finance_leases=v2.FINANCE_LEASES_M,
            shares=v2.DILUTED_SHARES_M,
        )
        if case["checks"]["valid"]
        else None
    )
    return case


def diagnostic_case() -> Dict[str, Any]:
    case = forecast()
    schedule = fcff_schedule(case["rows"], case["inputs"])
    valuation = value(schedule) if case["checks"]["valid"] else None
    return {**case, "schedule": schedule, "valuation": valuation}


def reconciliation() -> List[Dict[str, Any]]:
    """Return a sequential V2-to-V3 valuation bridge without target calibration."""
    _, v2_schedule, v2_result = v2.diagnostic_case()
    revenue_case = _run_operating_case(_revenue_only_inputs())
    d_and_a_case = _run_operating_case(_d_and_a_corrected_inputs())
    full_case = _run_operating_case(deepcopy(source.BASE_INPUTS))
    if not all(
        case["checks"]["valid"] for case in (revenue_case, d_and_a_case, full_case)
    ):
        return [{"label": "Operating reconciliation failed", "value": None, "impact": None}]

    rows: List[Dict[str, Any]] = []

    def add(label: str, result: Dict[str, float], status: str) -> None:
        prior_value = rows[-1]["value"]["per_share"] if rows else v2_result["per_share"]
        rows.append(
            {
                "label": label,
                "value": result,
                "impact": result["per_share"] - prior_value,
                "status": status,
            }
        )

    add("Revenue/net-sales formula", revenue_case["valuation_v2_bridge"], "confirmed formula correction")
    add("D&A definition and asset roll-forward", d_and_a_case["valuation_v2_bridge"], "confirmed definition correction; split remains provisional")
    add("Finance-lease forecast convention", full_case["valuation_v2_bridge"], "provisional roll-forward")

    operating_schedule = full_case["schedule"]
    cash_step = value(
        operating_schedule,
        cash=BRIDGE_CASH_M,
        debt=v2.BORROWINGS_M,
        finance_leases=v2.FINANCE_LEASES_M,
        shares=v2.DILUTED_SHARES_M,
    )
    add("July 31 cash proxy", cash_step, "source-backed date; excess-cash treatment provisional")
    debt_step = value(
        operating_schedule,
        cash=BRIDGE_CASH_M,
        debt=BRIDGE_DEBT_FAIR_VALUE_PROXY_M,
        finance_leases=v2.FINANCE_LEASES_M,
        shares=v2.DILUTED_SHARES_M,
    )
    add("July 31 debt fair-value proxy", debt_step, "source-backed date; not September 23")
    lease_step = value(
        operating_schedule,
        cash=BRIDGE_CASH_M,
        debt=BRIDGE_DEBT_FAIR_VALUE_PROXY_M,
        finance_leases=BRIDGE_FINANCE_LEASES_M,
        shares=v2.DILUTED_SHARES_M,
    )
    add("July 31 finance-lease bridge", lease_step, "source-backed date; not September 23")
    share_step = value(operating_schedule)
    add("August 26 basic spot shares", share_step, "source-backed basic count; dilution unresolved")
    return rows


def dcf_check_summary(case: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    if len(case["schedule"]) != 5:
        issues.append("FCFF horizon is not five years")
    if not 0.0 <= TERMINAL_GROWTH < WACC < 1.0:
        issues.append("DCF rate boundary failed")
    if case["valuation"] is None:
        issues.append("Valuation suppressed because statement controls failed")
    elif abs(
        case["valuation"]["equity_value"]
        - (
            case["valuation"]["enterprise_value"]
            + case["valuation"]["cash"]
            + case["valuation"]["nonoperating_investments"]
            - case["valuation"]["debt"]
            - case["valuation"]["finance_leases"]
            - case["valuation"]["nci"]
        )
    ) > TOLERANCE:
        issues.append("Bridge arithmetic failed")
    return {"status": "PASS" if not issues else "FAIL", "issues": issues}


def main() -> None:
    case = diagnostic_case()
    dcf_checks = dcf_check_summary(case)
    print("WALMART PROJECT 1 FCFF V3 -- DIAGNOSTIC, NOT FINAL")
    print("Provisional WACC 7.00% | terminal growth 2.50% | USD millions")
    print("Year       EBIT       D&A   CapEx  Lease capex   Change ONWC       FCFF")
    for row in case["schedule"]:
        print(
            f"{row['year']}  {row['ebit']:9,.1f}  {row['d_and_a']:8,.1f}"
            f"  {row['capex']:7,.1f}  {row['finance_lease_additions']:11,.1f}"
            f"  {row['change_operating_nwc']:12,.1f}  {row['fcff']:9,.1f}"
        )
    checks = case["checks"]
    print(
        f"Statement checks: {checks['status']} | balance {checks['max_abs_balance_gap']:.6f}"
        f" | cash flow {checks['max_abs_cash_flow_gap']:.6f}"
        f" | debt roll {checks['max_abs_debt_roll_forward_gap']:.6f}"
        f" | lease roll {checks['max_abs_lease_roll_forward_gap']:.6f}"
        f" | minimum cash ${checks['minimum_cash']:,.1f}M"
        f" | maximum revolver ${checks['maximum_revolver']:,.1f}M"
    )
    if checks["issues"]:
        print("Statement issues: " + "; ".join(checks["issues"]))
    print(f"DCF checks: {dcf_checks['status']}")
    if dcf_checks["issues"]:
        print("DCF issues: " + "; ".join(dcf_checks["issues"]))
    if case["valuation"] is not None:
        result = case["valuation"]
        print(
            f"V3 EV ${result['enterprise_value']:,.1f}M | equity ${result['equity_value']:,.1f}M"
            f" | provisional ${result['per_share']:,.2f}/August 26 basic share"
            f" | terminal share {result['terminal_share']:.2%}"
        )
        print(
            f"Provisional bridge: +${result['cash']:,.0f}M cash"
            f" -${result['debt']:,.0f}M debt proxy"
            f" -${result['finance_leases']:,.0f}M finance leases"
            f" -${result['nci']:,.0f}M NCI +${result['nonoperating_investments']:,.0f}M investments"
        )
    print("\nV2-TO-V3 SEQUENTIAL RECONCILIATION")
    print(f"Historical V2: ${v2.diagnostic_case()[2]['per_share']:.6f}/share")
    for row in reconciliation():
        if row["value"] is None:
            print(row["label"])
        else:
            print(
                f"{row['label']}: ${row['value']['per_share']:.6f}/share"
                f" | impact {row['impact']:+.6f} | {row['status']}"
            )


if __name__ == "__main__":
    main()
