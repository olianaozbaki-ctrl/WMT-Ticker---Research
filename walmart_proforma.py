"""Walmart five-year three-statement projection and FCFE valuation.

Amounts are USD millions except per-share data.  This is a course model, not
investment advice.  Historical sources and assumption rationales are recorded
in Walmart_Lab_10_Proforma.md.
"""

from __future__ import annotations

from copy import deepcopy
import sys
from typing import Any, Dict, List


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


# One immutable-by-convention source for every independent base input. Each
# projection and sensitivity case receives a deep copy so no run can
# contaminate a later run.
BASE_INPUTS: Dict[str, Any] = {
    "revenue_growth": deepcopy(REVENUE_GROWTH),
    "gross_margin": deepcopy(GROSS_MARGIN),
    "cash_sga_to_gross_profit": deepcopy(CASH_SGA_TO_GROSS_PROFIT),
    "depreciation_to_opening_ppe": DEPRECIATION_TO_OPENING_PPE,
    "capex": deepcopy(CAPEX),
    "tax_rate": TAX_RATE,
    "inventory_days": INVENTORY_DAYS,
    "accounts_payable_days": ACCOUNTS_PAYABLE_DAYS,
    "other_assets_to_revenue": OTHER_ASSETS_TO_REVENUE,
    "other_liabilities_to_revenue": OTHER_LIABILITIES_TO_REVENUE,
    "debt_repayment": deepcopy(DEBT_REPAYMENT),
    "debt_rate": DEBT_RATE,
    "finance_lease_rate": FINANCE_LEASE_RATE,
    "dividends": deepcopy(DIVIDENDS),
    "share_buyback": SHARE_BUYBACK,
    "minimum_cash": MINIMUM_CASH,
    "revolver_limit": REVOLVER_LIMIT,
    "revolver_rate": REVOLVER_RATE,
    "cost_of_equity": COST_OF_EQUITY,
    "terminal_growth": TERMINAL_GROWTH,
    "shares_outstanding": SHARES_OUTSTANDING,
    "opening": deepcopy(OPENING),
}


def build_projection(
    inputs: Dict[str, Any] | None = None,
) -> List[Dict[str, float]]:
    """Build linked income statements, balance sheets, and cash flows."""
    run_inputs = deepcopy(BASE_INPUTS if inputs is None else inputs)
    prior = deepcopy(run_inputs["opening"])
    projection: List[Dict[str, float]] = []

    for year in YEARS:
        revenue = prior["revenue"] * (1.0 + run_inputs["revenue_growth"][year])
        gross_profit = revenue * run_inputs["gross_margin"][year]
        cost_of_sales = revenue - gross_profit
        cash_sga = (
            gross_profit * run_inputs["cash_sga_to_gross_profit"][year]
        )
        depreciation = (
            prior["ppe"] * run_inputs["depreciation_to_opening_ppe"]
        )
        operating_income = gross_profit - cash_sga - depreciation
        interest = (
            prior["debt"] * run_inputs["debt_rate"]
            + prior["finance_leases"] * run_inputs["finance_lease_rate"]
            + prior["revolver"] * run_inputs["revolver_rate"]
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * run_inputs["tax_rate"]
        net_income = pretax_income - tax

        inventory = cost_of_sales * run_inputs["inventory_days"] / 365.0
        accounts_payable = (
            cost_of_sales * run_inputs["accounts_payable_days"] / 365.0
        )
        ppe = prior["ppe"] + run_inputs["capex"][year] - depreciation
        other_assets = revenue * run_inputs["other_assets_to_revenue"]
        other_liabilities = revenue * run_inputs["other_liabilities_to_revenue"]
        debt_repayment = min(run_inputs["debt_repayment"][year], prior["debt"])
        debt = prior["debt"] - debt_repayment
        finance_leases = prior["finance_leases"]
        equity = (
            prior["equity"]
            + net_income
            - run_inputs["dividends"][year]
            - run_inputs["share_buyback"]
        )

        change_in_inventory = inventory - prior["inventory"]
        change_in_other_assets = other_assets - prior["other_assets"]
        change_in_accounts_payable = accounts_payable - prior["accounts_payable"]
        change_in_other_liabilities = other_liabilities - prior["other_liabilities"]

        # FCFE is before discretionary dividends and buybacks.  Every modeled
        # non-cash balance-sheet change appears once in this bridge.
        fcfe = (
            net_income
            + depreciation
            - run_inputs["capex"][year]
            - change_in_inventory
            - change_in_other_assets
            + change_in_accounts_payable
            + change_in_other_liabilities
            - debt_repayment
        )

        cash_before_revolver = (
            prior["cash"]
            + fcfe
            - run_inputs["dividends"][year]
            - run_inputs["share_buyback"]
        )
        revolver_draw = 0.0
        revolver_repayment = 0.0
        revolver = prior["revolver"]

        if cash_before_revolver < run_inputs["minimum_cash"]:
            revolver_draw = run_inputs["minimum_cash"] - cash_before_revolver
            revolver += revolver_draw
            cash = run_inputs["minimum_cash"]
        else:
            revolver_repayment = min(
                revolver, cash_before_revolver - run_inputs["minimum_cash"]
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
            "capex": run_inputs["capex"][year],
            "debt_repayment": debt_repayment,
            "fcfe": fcfe,
            "dividends": run_inputs["dividends"][year],
            "buyback": run_inputs["share_buyback"],
            "revolver_draw": revolver_draw,
            "revolver_repayment": revolver_repayment,
            "net_change_in_cash": cash - prior["cash"],
            "balance_gap": balance_gap,
            "cash_above_minimum": cash >= run_inputs["minimum_cash"],
        }
        projection.append(result)
        prior = result

    return projection


def accounting_check_summary(
    projection: List[Dict[str, float]],
    inputs: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Return visible accounting/liquidity checks without stopping the run."""
    run_inputs = BASE_INPUTS if inputs is None else inputs
    tolerance = 1e-6
    issues: List[str] = []
    for row in projection:
        year = int(row["year"])
        if abs(row["balance_gap"]) > tolerance:
            issues.append(
                f"FY{year}E balance-sheet gap: {row['balance_gap']:.6f}"
            )
        if row["cash"] < run_inputs["minimum_cash"] - tolerance:
            issues.append(
                f"FY{year}E cash below minimum: "
                f"{row['cash'] - run_inputs['minimum_cash']:.6f}"
            )
        if row["revolver"] > run_inputs["revolver_limit"] + tolerance:
            issues.append(
                f"FY{year}E revolver above limit: "
                f"{row['revolver'] - run_inputs['revolver_limit']:.6f}"
            )
    return {
        "valid": not issues,
        "status": "VALID" if not issues else "INVALID",
        "issues": issues,
        "max_abs_balance_gap": max(abs(row["balance_gap"]) for row in projection),
        "minimum_cash": min(row["cash"] for row in projection),
        "maximum_revolver": max(row["revolver"] for row in projection),
    }


def assert_balanced(
    projection: List[Dict[str, float]],
    inputs: Dict[str, Any] | None = None,
) -> None:
    """Refuse to value a projection whose balance or liquidity checks fail."""
    checks = accounting_check_summary(projection, inputs)
    if not checks["valid"]:
        raise ValueError(checks["issues"][0])


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


def calculate_valuation(
    projection: List[Dict[str, float]],
    inputs: Dict[str, Any] | None = None,
) -> Dict[str, float]:
    run_inputs = BASE_INPUTS if inputs is None else inputs
    if run_inputs["terminal_growth"] >= run_inputs["cost_of_equity"]:
        raise ValueError("Terminal growth must be below the cost of equity.")
    present_value_of_fcfe = sum(
        row["fcfe"] / (1.0 + run_inputs["cost_of_equity"]) ** index
        for index, row in enumerate(projection, start=1)
    )
    final_year = projection[-1]
    normalized_terminal_fcfe = final_year["fcfe"] + final_year["debt_repayment"]
    terminal_value = (
        normalized_terminal_fcfe
        * (1.0 + run_inputs["terminal_growth"])
        / (run_inputs["cost_of_equity"] - run_inputs["terminal_growth"])
    )
    present_value_of_terminal = terminal_value / (
        1.0 + run_inputs["cost_of_equity"]
    ) ** 5
    equity_value = present_value_of_fcfe + present_value_of_terminal
    return {
        "pv_fcfe": present_value_of_fcfe,
        "pv_terminal": present_value_of_terminal,
        "equity_value": equity_value,
        "terminal_share": present_value_of_terminal / equity_value,
        "value_per_share": equity_value / run_inputs["shares_outstanding"],
    }


def print_valuation(projection: List[Dict[str, float]]) -> None:
    valuation = calculate_valuation(projection)
    print("\nVALUATION")
    print(f"PV of five explicit FCFE (USD millions): {valuation['pv_fcfe']:,.2f}")
    print(f"PV of terminal value (USD millions):     {valuation['pv_terminal']:,.2f}")
    print(f"Equity value (USD millions):             {valuation['equity_value']:,.2f}")
    print(f"Share of value after FY2031:             {valuation['terminal_share']:.2%}")
    print(f"Value per share:                         ${valuation['value_per_share']:,.2f}")


SENSITIVITY_DRIVERS = {
    "revenue_growth": {
        "label": "Revenue growth",
        "unit": "% of prior-year revenue",
        "step": 0.010,
    },
    "cash_sga_to_revenue": {
        "label": "Cash SG&A as a percentage of revenue",
        "unit": "% of revenue",
        "step": 0.005,
    },
}


def sensitivity_input_values(
    inputs: Dict[str, Any], driver: str
) -> Dict[int, float]:
    """Return displayed driver values in decimal form for each year."""
    if driver == "revenue_growth":
        return deepcopy(inputs["revenue_growth"])
    if driver == "cash_sga_to_revenue":
        return {
            year: (
                inputs["gross_margin"][year]
                * inputs["cash_sga_to_gross_profit"][year]
            )
            for year in YEARS
        }
    raise KeyError(f"Unknown sensitivity driver: {driver}")


def apply_sensitivity_case(
    inputs: Dict[str, Any], driver: str, case: str
) -> Dict[int, float]:
    """Apply one lower/base/higher driver case to a fresh base input copy."""
    direction = {"lower": -1.0, "base": 0.0, "higher": 1.0}[case]
    step = SENSITIVITY_DRIVERS[driver]["step"]
    base_values = sensitivity_input_values(BASE_INPUTS, driver)
    case_values = {
        year: base_values[year] + direction * step for year in YEARS
    }

    if driver == "revenue_growth":
        inputs["revenue_growth"] = deepcopy(case_values)
    elif driver == "cash_sga_to_revenue":
        # The existing model stores cash SG&A as a percentage of gross profit.
        # Translate the requested revenue-based input without changing gross
        # margin or any other independent assumption.
        inputs["cash_sga_to_gross_profit"] = {
            year: case_values[year] / inputs["gross_margin"][year]
            for year in YEARS
        }
    else:
        raise KeyError(f"Unknown sensitivity driver: {driver}")
    return case_values


def run_sensitivity_case(driver: str, case: str) -> Dict[str, Any]:
    """Run one isolated case and retain its linked statements and checks."""
    inputs = deepcopy(BASE_INPUTS)
    case_values = apply_sensitivity_case(inputs, driver, case)
    projection = build_projection(inputs)
    checks = accounting_check_summary(projection, inputs)
    valuation = None
    valuation_error = None
    if checks["valid"]:
        try:
            valuation = calculate_valuation(projection, inputs)
        except ValueError as exc:
            valuation_error = str(exc)
    else:
        valuation_error = "Accounting or liquidity checks failed."
    return {
        "driver": driver,
        "case": case,
        "inputs": inputs,
        "case_values": case_values,
        "projection": projection,
        "checks": checks,
        "valuation": valuation,
        "valuation_error": valuation_error,
    }


def _signed(value: float, decimals: int = 1, currency: bool = False) -> str:
    if currency:
        sign = "+" if value >= 0.0 else "-"
        return f"{sign}${abs(value):,.{decimals}f}"
    return f"{value:+,.{decimals}f}"


def print_sensitivity_trace(driver_results: List[Dict[str, Any]]) -> None:
    """Print final-year statement detail sufficient to trace each result."""
    label = SENSITIVITY_DRIVERS[driver_results[0]["driver"]]["label"]
    print(f"\n{label.upper()} — FY2031E TRACE (USD millions)")
    print(
        f"{'':<34}"
        + "".join(result["case"].title().rjust(16) for result in driver_results)
    )
    print("-" * (34 + 16 * len(driver_results)))
    rows = [
        ("Revenue", "revenue", 1.0),
        ("Gross profit", "gross_profit", 1.0),
        ("Cash SG&A", "cash_sga", -1.0),
        ("Depreciation and amortization", "depreciation", -1.0),
        ("Operating profit", "operating_income", 1.0),
        ("Interest expense", "interest", -1.0),
        ("Income tax", "tax", -1.0),
        ("Net income", "net_income", 1.0),
        ("D&A add-back", "depreciation", 1.0),
        ("Capital expenditures", "capex", -1.0),
        ("Change in inventory", "change_in_inventory", -1.0),
        ("Change in other assets", "change_in_other_assets", -1.0),
        ("Change in accounts payable", "change_in_accounts_payable", 1.0),
        ("Change in other liabilities", "change_in_other_liabilities", 1.0),
        ("Debt repayment", "debt_repayment", -1.0),
        ("Free cash flow to equity", "fcfe", 1.0),
        ("Ending cash", "cash", 1.0),
        ("Revolver", "revolver", 1.0),
        ("Balance-sheet gap", "balance_gap", 1.0),
    ]
    for row_label, key, sign in rows:
        values = "".join(
            f"{sign * result['projection'][-1][key]:>16,.1f}"
            for result in driver_results
        )
        print(f"{row_label:<34}{values}")
    print(
        f"{'Accounting check status':<34}"
        + "".join(
            result["checks"]["status"].rjust(16)
            for result in driver_results
        )
    )


def print_sensitivity_analysis() -> None:
    """Run and report one-at-a-time sensitivities for the two set drivers."""
    print("\nONE-AT-A-TIME SENSITIVITY ANALYSIS")
    print("Each case starts from a fresh deep copy of BASE_INPUTS.")

    for driver, metadata in SENSITIVITY_DRIVERS.items():
        results = [
            run_sensitivity_case(driver, case)
            for case in ("lower", "base", "higher")
        ]
        base_result = results[1]
        base_final = base_result["projection"][-1]
        base_value = (
            base_result["valuation"]["value_per_share"]
            if base_result["valuation"] is not None
            else None
        )

        print(f"\n{metadata['label']}")
        print(f"Units: {metadata['unit']}; affected years: FY2027E–FY2031E")
        print(
            f"{'Case':<9}{'FY2027E–FY2031E actual inputs':<45}"
            f"{'FY2031E operating profit':>26}{'Change':>14}"
            f"{'FY2031E FCFE':>18}{'Change':>14}"
            f"{'Value/share':>15}{'Change':>12}{'Status':>11}"
        )
        print("-" * 164)
        for result in results:
            final = result["projection"][-1]
            input_text = ", ".join(
                f"{100.0 * result['case_values'][year]:.3f}%" for year in YEARS
            )
            operating_change = (
                final["operating_income"] - base_final["operating_income"]
            )
            fcfe_change = final["fcfe"] - base_final["fcfe"]
            if result["valuation"] is not None and base_value is not None:
                value_per_share = result["valuation"]["value_per_share"]
                value_text = f"${value_per_share:,.2f}"
                value_change = _signed(
                    value_per_share - base_value, decimals=2, currency=True
                )
            else:
                value_text = "N/A"
                value_change = "N/A"
            print(
                f"{result['case'].title():<9}{input_text:<45}"
                f"{final['operating_income']:>26,.1f}"
                f"{_signed(operating_change):>14}"
                f"{final['fcfe']:>18,.1f}{_signed(fcfe_change):>14}"
                f"{value_text:>15}{value_change:>12}"
                f"{result['checks']['status']:>11}"
            )
            if result["valuation_error"]:
                print(f"  Valuation unavailable: {result['valuation_error']}")
            for issue in result["checks"]["issues"]:
                print(f"  Check failure: {issue}")

        valid_results = [result for result in results if result["checks"]["valid"]]
        operating_values = [
            result["projection"][-1]["operating_income"]
            for result in valid_results
        ]
        fcfe_values = [
            result["projection"][-1]["fcfe"] for result in valid_results
        ]
        valuation_values = [
            result["valuation"]["value_per_share"]
            for result in valid_results
            if result["valuation"] is not None
        ]
        if operating_values:
            print(
                "Operating-profit span: "
                f"{max(operating_values) - min(operating_values):,.1f} "
                "USD millions"
            )
            print(
                "FCFE span: "
                f"{max(fcfe_values) - min(fcfe_values):,.1f} USD millions"
            )
        else:
            print("Operating-profit span: N/A (no valid runs)")
            print("FCFE span: N/A (no valid runs)")
        if valuation_values:
            print(
                "Value-per-share span: "
                f"${max(valuation_values) - min(valuation_values):,.2f}"
            )
        else:
            print("Value-per-share span: N/A")
        print_sensitivity_trace(results)

    # Explicitly restore the base inputs and rerun after every sensitivity case.
    restored_inputs = deepcopy(BASE_INPUTS)
    restored_projection = build_projection(restored_inputs)
    restored_checks = accounting_check_summary(restored_projection, restored_inputs)
    restored_valuation = None
    if restored_checks["valid"]:
        restored_valuation = calculate_valuation(
            restored_projection, restored_inputs
        )
    print("\nBASE RESTORATION RERUN")
    print(f"Status: {restored_checks['status']}")
    print(
        "FY2031E operating profit (USD millions): "
        f"{restored_projection[-1]['operating_income']:,.1f}"
    )
    print(
        "FY2031E FCFE (USD millions): "
        f"{restored_projection[-1]['fcfe']:,.1f}"
    )
    print(
        "Value per share: "
        + (
            f"${restored_valuation['value_per_share']:,.2f}"
            if restored_valuation is not None
            else "N/A"
        )
    )


def main() -> None:
    base_inputs = deepcopy(BASE_INPUTS)
    projection = build_projection(base_inputs)
    if "--break-check" in sys.argv:
        projection[0]["cash"] = base_inputs["opening"]["cash"]
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
    assert_balanced(projection, base_inputs)
    print_valuation(projection)
    if "--break-check" not in sys.argv and "--base-only" not in sys.argv:
        print_sensitivity_analysis()


if __name__ == "__main__":
    main()
