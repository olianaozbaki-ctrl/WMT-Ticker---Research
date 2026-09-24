"""Walmart five-year three-statement projection and FCFE valuation.

Amounts are USD millions except per-share data.  This is a course model, not
investment advice.  Historical sources and assumption rationales are recorded
in Walmart_Lab_10_Proforma.md.
"""

from __future__ import annotations

import sys
from typing import Dict, List


YEARS = (2027, 2028, 2029, 2030, 2031)

# Forecast assumptions: guidance where available, otherwise labelled judgment.
REVENUE_GROWTH = {
    2027: 0.043,
    2028: 0.042,
    2029: 0.040,
    2030: 0.038,
    2031: 0.035,
}
GROSS_MARGIN = {
    2027: 0.2500,
    2028: 0.2510,
    2029: 0.2520,
    2030: 0.2525,
    2031: 0.2530,
}
CASH_SGA_TO_GROSS_PROFIT = {
    2027: 0.752,
    2028: 0.750,
    2029: 0.748,
    2030: 0.746,
    2031: 0.745,
}
DEPRECIATION_TO_OPENING_PPE = 0.106
CAPEX = {
    2027: 26_000.0,
    2028: 28_000.0,
    2029: 29_000.0,
    2030: 30_000.0,
    2031: 31_000.0,
}
TAX_RATE = 0.245
INVENTORY_DAYS = 40.2
ACCOUNTS_PAYABLE_DAYS = 42.8
OTHER_ASSETS_TO_REVENUE = 79_007.0 / 713_163.0
OTHER_LIABILITIES_TO_REVENUE = 64_197.0 / 713_163.0
DEBT_REPAYMENT = {
    2027: 3_542.0,
    2028: 3_237.0,
    2029: 3_389.0,
    2030: 2_143.0,
    2031: 2_600.0,
}
DEBT_RATE = 0.045
FINANCE_LEASE_RATE = 0.057
DIVIDENDS = {
    2027: 8_000.0,
    2028: 8_240.0,
    2029: 8_487.2,
    2030: 8_741.8,
    2031: 9_004.1,
}
# Judgment: suspend discretionary repurchases in the base case because forecast
# FCFE first funds dividends and scheduled debt maturities.  Repurchases are a
# review trigger, not a source of value in this model.
SHARE_BUYBACK = 0.0
MINIMUM_CASH = 8_000.0
REVOLVER_LIMIT = 15_000.0
REVOLVER_RATE = 0.050
COST_OF_EQUITY = 0.0685
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 7_969.0

# Walmart FY2026 closing balance sheet.  Aggregated lines preserve the reported
# total while keeping the classroom model readable.
OPENING = {
    "revenue": 713_163.0,
    "cash": 10_727.0,
    "inventory": 58_851.0,
    "ppe": 136_083.0,
    "other_assets": 79_007.0,
    "accounts_payable": 63_061.0,
    "debt": 44_762.0,
    "finance_leases": 6_761.0,
    "revolver": 0.0,
    "other_liabilities": 64_197.0,
    "equity": 105_887.0,
}


def build_projection() -> List[Dict[str, float]]:
    """Build linked income statements, balance sheets, and cash flows."""
    prior = OPENING.copy()
    projection: List[Dict[str, float]] = []

    for year in YEARS:
        revenue = prior["revenue"] * (1.0 + REVENUE_GROWTH[year])
        gross_profit = revenue * GROSS_MARGIN[year]
        cost_of_sales = revenue - gross_profit
        cash_sga = gross_profit * CASH_SGA_TO_GROSS_PROFIT[year]
        depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
        operating_income = gross_profit - cash_sga - depreciation
        interest = (
            prior["debt"] * DEBT_RATE
            + prior["finance_leases"] * FINANCE_LEASE_RATE
            + prior["revolver"] * REVOLVER_RATE
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = cost_of_sales * INVENTORY_DAYS / 365.0
        accounts_payable = cost_of_sales * ACCOUNTS_PAYABLE_DAYS / 365.0
        ppe = prior["ppe"] + CAPEX[year] - depreciation
        other_assets = revenue * OTHER_ASSETS_TO_REVENUE
        other_liabilities = revenue * OTHER_LIABILITIES_TO_REVENUE
        debt_repayment = min(DEBT_REPAYMENT[year], prior["debt"])
        debt = prior["debt"] - debt_repayment
        finance_leases = prior["finance_leases"]
        equity = prior["equity"] + net_income - DIVIDENDS[year] - SHARE_BUYBACK

        change_in_inventory = inventory - prior["inventory"]
        change_in_other_assets = other_assets - prior["other_assets"]
        change_in_accounts_payable = accounts_payable - prior["accounts_payable"]
        change_in_other_liabilities = other_liabilities - prior["other_liabilities"]

        # FCFE is before discretionary dividends and buybacks.  Every modeled
        # non-cash balance-sheet change appears once in this bridge.
        fcfe = (
            net_income
            + depreciation
            - CAPEX[year]
            - change_in_inventory
            - change_in_other_assets
            + change_in_accounts_payable
            + change_in_other_liabilities
            - debt_repayment
        )

        cash_before_revolver = (
            prior["cash"] + fcfe - DIVIDENDS[year] - SHARE_BUYBACK
        )
        revolver_draw = 0.0
        revolver_repayment = 0.0
        revolver = prior["revolver"]

        if cash_before_revolver < MINIMUM_CASH:
            revolver_draw = MINIMUM_CASH - cash_before_revolver
            revolver += revolver_draw
            cash = MINIMUM_CASH
        else:
            revolver_repayment = min(
                revolver, cash_before_revolver - MINIMUM_CASH
            )
            revolver -= revolver_repayment
            cash = cash_before_revolver - revolver_repayment

        total_assets = cash + inventory + ppe + other_assets
        total_liabilities_and_equity = (
            accounts_payable
            + debt
            + finance_leases
            + revolver
            + other_liabilities
            + equity
        )
        balance_gap = total_assets - total_liabilities_and_equity

        result = {
            "year": float(year),
            "revenue": revenue,
            "cost_of_sales": cost_of_sales,
            "gross_profit": gross_profit,
            "cash_sga": cash_sga,
            "depreciation": depreciation,
            "operating_income": operating_income,
            "interest": interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
            "cash": cash,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": total_assets,
            "accounts_payable": accounts_payable,
            "debt": debt,
            "finance_leases": finance_leases,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "total_liabilities_and_equity": total_liabilities_and_equity,
            "change_in_inventory": change_in_inventory,
            "change_in_other_assets": change_in_other_assets,
            "change_in_accounts_payable": change_in_accounts_payable,
            "change_in_other_liabilities": change_in_other_liabilities,
            "capex": CAPEX[year],
            "debt_repayment": debt_repayment,
            "fcfe": fcfe,
            "dividends": DIVIDENDS[year],
            "buyback": SHARE_BUYBACK,
            "revolver_draw": revolver_draw,
            "revolver_repayment": revolver_repayment,
            "net_change_in_cash": cash - prior["cash"],
            "balance_gap": balance_gap,
            "cash_above_minimum": cash >= MINIMUM_CASH,
        }
        projection.append(result)
        prior = result

    return projection


def assert_balanced(projection: List[Dict[str, float]]) -> None:
    """Refuse to value a projection whose balance or liquidity checks fail."""
    tolerance = 1e-6
    for row in projection:
        year = int(row["year"])
        if abs(row["balance_gap"]) > tolerance:
            raise ValueError(
                f"FY{year}E balance-sheet gap: {row['balance_gap']:.6f}"
            )
        if row["cash"] < MINIMUM_CASH - tolerance:
            raise ValueError(
                f"FY{year}E cash is below the minimum by "
                f"{MINIMUM_CASH - row['cash']:.6f}"
            )
        if row["revolver"] > REVOLVER_LIMIT + tolerance:
            raise ValueError(
                f"FY{year}E revolver exceeds its limit by "
                f"{row['revolver'] - REVOLVER_LIMIT:.6f}"
            )


def print_table(
    title: str,
    rows: List[tuple[str, str, float]],
    projection: List[Dict[str, float]],
) -> None:
    label_width = max(34, max(len(label) for label, _, _ in rows))
    print(f"\n{title} (USD millions)")
    print(f"{'':<{label_width}}" + "".join(f"FY{year}E".rjust(14) for year in YEARS))
    print("-" * (label_width + 14 * len(YEARS)))
    for label, key, sign in rows:
        values = "".join(f"{sign * row[key]:>14,.1f}" for row in projection)
        print(f"{label:<{label_width}}{values}")


def print_projection(projection: List[Dict[str, float]]) -> None:
    income_statement = [
        ("Revenue", "revenue", 1.0),
        ("Cost of sales", "cost_of_sales", -1.0),
        ("Gross profit", "gross_profit", 1.0),
        ("Cash SG&A", "cash_sga", -1.0),
        ("Depreciation and amortization", "depreciation", -1.0),
        ("Operating income", "operating_income", 1.0),
        ("Interest expense", "interest", -1.0),
        ("Pretax income", "pretax_income", 1.0),
        ("Income tax", "tax", -1.0),
        ("Net income", "net_income", 1.0),
    ]
    balance_sheet = [
        ("Cash", "cash", 1.0),
        ("Inventory", "inventory", 1.0),
        ("Property and equipment, net", "ppe", 1.0),
        ("Other assets", "other_assets", 1.0),
        ("Total assets", "total_assets", 1.0),
        ("Accounts payable", "accounts_payable", 1.0),
        ("Borrowings and long-term debt", "debt", 1.0),
        ("Finance lease obligations", "finance_leases", 1.0),
        ("Revolver", "revolver", 1.0),
        ("Other liabilities", "other_liabilities", 1.0),
        ("Total equity", "equity", 1.0),
        ("Total liabilities and equity", "total_liabilities_and_equity", 1.0),
    ]
    cash_flow_statement = [
        ("Net income", "net_income", 1.0),
        ("Depreciation and amortization", "depreciation", 1.0),
        ("Capital expenditures", "capex", -1.0),
        ("Change in inventory", "change_in_inventory", -1.0),
        ("Change in other assets", "change_in_other_assets", -1.0),
        ("Change in accounts payable", "change_in_accounts_payable", 1.0),
        ("Change in other liabilities", "change_in_other_liabilities", 1.0),
        ("Debt repayment", "debt_repayment", -1.0),
        ("Free cash flow to equity", "fcfe", 1.0),
        ("Dividends", "dividends", -1.0),
        ("Share repurchases", "buyback", -1.0),
        ("Revolver draw", "revolver_draw", 1.0),
        ("Revolver repayment", "revolver_repayment", -1.0),
        ("Net change in cash", "net_change_in_cash", 1.0),
    ]

    print_table("INCOME STATEMENT", income_statement, projection)
    print_table("BALANCE SHEET", balance_sheet, projection)
    print_table("CASH FLOW STATEMENT", cash_flow_statement, projection)

    print("\nCHECKS")
    print(f"{'':<34}" + "".join(f"FY{year}E".rjust(14) for year in YEARS))
    print("-" * (34 + 14 * len(YEARS)))
    print(
        f"{'Assets - liabilities - equity':<34}"
        + "".join(f"{row['balance_gap']:>14,.1f}" for row in projection)
    )
    print(
        f"{'Cash at or above minimum':<34}"
        + "".join(f"{str(row['cash_above_minimum']):>14}" for row in projection)
    )


def calculate_valuation(projection: List[Dict[str, float]]) -> Dict[str, float]:
    if TERMINAL_GROWTH >= COST_OF_EQUITY:
        raise ValueError("Terminal growth must be below the cost of equity.")
    present_value_of_fcfe = sum(
        row["fcfe"] / (1.0 + COST_OF_EQUITY) ** index
        for index, row in enumerate(projection, start=1)
    )
    final_year = projection[-1]
    normalized_terminal_fcfe = final_year["fcfe"] + final_year["debt_repayment"]
    terminal_value = (
        normalized_terminal_fcfe
        * (1.0 + TERMINAL_GROWTH)
        / (COST_OF_EQUITY - TERMINAL_GROWTH)
    )
    present_value_of_terminal = terminal_value / (1.0 + COST_OF_EQUITY) ** 5
    equity_value = present_value_of_fcfe + present_value_of_terminal
    return {
        "pv_fcfe": present_value_of_fcfe,
        "pv_terminal": present_value_of_terminal,
        "equity_value": equity_value,
        "terminal_share": present_value_of_terminal / equity_value,
        "value_per_share": equity_value / SHARES_OUTSTANDING,
    }


def print_valuation(projection: List[Dict[str, float]]) -> None:
    valuation = calculate_valuation(projection)
    print("\nVALUATION")
    print(f"PV of five explicit FCFE (USD millions): {valuation['pv_fcfe']:,.2f}")
    print(f"PV of terminal value (USD millions):     {valuation['pv_terminal']:,.2f}")
    print(f"Equity value (USD millions):             {valuation['equity_value']:,.2f}")
    print(f"Share of value after FY2031:             {valuation['terminal_share']:.2%}")
    print(f"Value per share:                         ${valuation['value_per_share']:,.2f}")


def main() -> None:
    projection = build_projection()
    if "--break-check" in sys.argv:
        projection[0]["cash"] = OPENING["cash"]
        projection[0]["total_assets"] = (
            projection[0]["cash"]
            + projection[0]["inventory"]
            + projection[0]["ppe"]
            + projection[0]["other_assets"]
        )
        projection[0]["balance_gap"] = (
            projection[0]["total_assets"]
            - projection[0]["total_liabilities_and_equity"]
        )
    print_projection(projection)
    assert_balanced(projection)
    print_valuation(projection)


if __name__ == "__main__":
    main()
