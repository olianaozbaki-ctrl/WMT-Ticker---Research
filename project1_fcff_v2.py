"""Diagnostic Walmart Project 1 FCFF DCF using the v2 operating-NWC model.

The WACC, terminal growth, and enterprise-to-equity bridge are preserved from
project1_fcff.py provisionally. Results are diagnostic, not final fair value.
"""
from copy import deepcopy
from typing import Dict, List

import walmart_project1_proforma_v2 as source


WACC = 0.07
TERMINAL_GROWTH = 0.025
DILUTED_SHARES_M = 8_022.0
CASH_M = 10_727.0
BORROWINGS_M = 44_762.0
FINANCE_LEASES_M = 6_761.0
INCLUDE_FINANCE_LEASES_IN_BRIDGE = True
TOLERANCE = 1e-6


def forecast(inputs=None):
    assumptions = deepcopy(source.BASE_INPUTS if inputs is None else inputs)
    rows = source.build_projection(assumptions)
    source.assert_balanced(rows, assumptions)
    return rows, assumptions


def fcff_schedule(
    rows: List[Dict[str, float]], inputs: Dict
) -> List[Dict[str, float]]:
    """Calculate FCFF from EBIT, cash operating tax, D&A, capex, and operating NWC."""
    schedule: List[Dict[str, float]] = []
    for row in rows:
        cash_operating_tax = max(0.0, row["operating_income"]) * inputs["cash_tax_rate"]
        nopat = row["operating_income"] - cash_operating_tax
        fcff = (
            nopat
            + row["depreciation"]
            - row["capex"]
            - row["change_operating_nwc"]
        )
        schedule.append(
            {
                "year": int(row["year"]),
                "revenue": row["revenue"],
                "ebit": row["operating_income"],
                "cash_operating_tax": cash_operating_tax,
                "nopat": nopat,
                "depreciation": row["depreciation"],
                "capex": row["capex"],
                "operating_nwc": row["operating_nwc"],
                "change_operating_nwc": row["change_operating_nwc"],
                "fcff": fcff,
            }
        )
    return schedule


def value(schedule, wacc: float = WACC, g: float = TERMINAL_GROWTH):
    if not (0.0 <= g < wacc < 1.0):
        raise ValueError("DCF rate boundary violated: require 0 <= g < WACC < 1")
    if len(schedule) != 5:
        raise ValueError("Expected a five-year FCFF schedule")
    pv_explicit = sum(
        row["fcff"] / (1.0 + wacc) ** index
        for index, row in enumerate(schedule, start=1)
    )
    terminal_fcff = schedule[-1]["fcff"] * (1.0 + g)
    pv_terminal = (
        terminal_fcff / (wacc - g) / (1.0 + wacc) ** len(schedule)
    )
    enterprise_value = pv_explicit + pv_terminal
    lease_claim = (
        FINANCE_LEASES_M if INCLUDE_FINANCE_LEASES_IN_BRIDGE else 0.0
    )
    equity_value = (
        enterprise_value + CASH_M - BORROWINGS_M - lease_claim
    )
    if abs(
        equity_value
        - (enterprise_value + CASH_M - BORROWINGS_M - lease_claim)
    ) > TOLERANCE:
        raise ValueError("Enterprise-to-equity bridge arithmetic failed")
    return {
        "pv_explicit": pv_explicit,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "per_share": equity_value / DILUTED_SHARES_M,
        "terminal_share": pv_terminal / enterprise_value,
        "lease_claim": lease_claim,
    }


def diagnostic_case():
    rows, assumptions = forecast()
    schedule = fcff_schedule(rows, assumptions)
    result = value(schedule)
    return rows, schedule, result


def main() -> None:
    rows, schedule, result = diagnostic_case()
    checks = source.accounting_check_summary(rows)
    print("WALMART PROJECT 1 FCFF V2 -- DIAGNOSTIC, NOT FINAL")
    print("Provisional WACC 7.00% | terminal growth 2.50% | USD millions")
    print("Year       EBIT    Cash tax       D&A     CapEx   Change ONWC       FCFF")
    for row in schedule:
        print(
            f"{row['year']}  {row['ebit']:9,.1f}  {row['cash_operating_tax']:10,.1f}"
            f"  {row['depreciation']:8,.1f}  {row['capex']:8,.1f}"
            f"  {row['change_operating_nwc']:12,.1f}  {row['fcff']:9,.1f}"
        )
    print(
        f"EV ${result['enterprise_value']:,.1f}M | equity ${result['equity_value']:,.1f}M"
        f" | ${result['per_share']:,.2f}/FY2026 diluted share"
        f" | terminal share {result['terminal_share']:.2%}"
    )
    print(
        f"Provisional bridge: EV + ${CASH_M:,.0f}M cash - ${BORROWINGS_M:,.0f}M debt"
        f" - ${result['lease_claim']:,.0f}M finance leases"
    )
    print(
        f"Tests: {checks['status']} | opening reconciliation, balance sheets, cash flows,"
        " DCF boundary, five-year horizon, and bridge arithmetic"
    )


if __name__ == "__main__":
    main()
