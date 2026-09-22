"""Five-year three-statement projection and FCFE valuation (USD millions)."""

from typing import Dict, List


YEARS = tuple(range(2026, 2031))

REVENUE_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_RATIOS = {
    2026: 0.665,
    2027: 0.655,
    2028: 0.645,
    2029: 0.645,
    2030: 0.645,
}
DEPRECIATION_RATIO = 82.4 / 3_070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365.0
FLOOR_PLAN_RATIO = 2_027.0 / 2_135.8
OTHER_WORKING_CAPITAL_RATIO = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}


def build_projection() -> List[Dict[str, float]]:
    """Build the income statement, balance sheet, and cash flow by year."""
    prior = OPENING.copy()
    projection: List[Dict[str, float]] = []

    for year in YEARS:
        revenue = prior["revenue"] * (1.0 + REVENUE_GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        cost_of_sales = revenue - gross_profit
        sga = gross_profit * SGA_RATIOS[year]
        depreciation = prior["ppe"] * DEPRECIATION_RATIO
        operating_income = gross_profit - sga - depreciation - IMPAIRMENT
        interest = (
            prior["floor_plan"] * FLOOR_PLAN_RATE
            + prior["debt"] * TERM_DEBT_RATE
            + prior["revolver"] * REVOLVER_RATE
        )
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        inventory = cost_of_sales * INVENTORY_DAYS / 365.0
        floor_plan = inventory * FLOOR_PLAN_RATIO
        ppe = prior["ppe"] + CAPEX - depreciation
        change_in_revenue = revenue - prior["revenue"]
        change_in_other_working_capital = (
            OTHER_WORKING_CAPITAL_RATIO * change_in_revenue
        )
        other_assets = (
            prior["other_assets"] + change_in_other_working_capital - IMPAIRMENT
        )
        debt_repayment = min(DEBT_REPAYMENT, prior["debt"])
        debt = prior["debt"] - debt_repayment
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - SHARE_BUYBACK

        change_in_inventory = inventory - prior["inventory"]
        change_in_floor_plan = floor_plan - prior["floor_plan"]
        fcfe = (
            net_income
            + depreciation
            + IMPAIRMENT
            - CAPEX
            - change_in_inventory
            - change_in_other_working_capital
            + change_in_floor_plan
            - debt_repayment
        )

        cash_before_revolver = prior["cash"] + fcfe - SHARE_BUYBACK
        revolver_draw = 0.0
        revolver_repayment = 0.0
        revolver = prior["revolver"]

        if cash_before_revolver < MINIMUM_CASH:
            revolver_draw = MINIMUM_CASH - cash_before_revolver
            revolver += revolver_draw
            cash = cash_before_revolver + revolver_draw
        else:
            revolver_repayment = min(
                revolver, cash_before_revolver - MINIMUM_CASH
            )
            revolver -= revolver_repayment
            cash = cash_before_revolver - revolver_repayment

        total_assets = cash + inventory + ppe + other_assets
        total_liabilities_and_equity = (
            floor_plan + debt + revolver + other_liabilities + equity
        )
        balance_gap = total_assets - total_liabilities_and_equity

        result = {
            "year": year,
            "revenue": revenue,
            "cost_of_sales": cost_of_sales,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": IMPAIRMENT,
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
            "floor_plan": floor_plan,
            "debt": debt,
            "revolver": revolver,
            "other_liabilities": other_liabilities,
            "equity": equity,
            "total_liabilities_and_equity": total_liabilities_and_equity,
            "change_in_inventory": change_in_inventory,
            "change_in_other_working_capital": change_in_other_working_capital,
            "change_in_floor_plan": change_in_floor_plan,
            "capex": CAPEX,
            "debt_repayment": debt_repayment,
            "fcfe": fcfe,
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
    """Raise an informative error if a balance or minimum-cash check fails."""
    tolerance = 1e-6
    for row in projection:
        year = int(row["year"])
        gap = row["balance_gap"]
        if abs(gap) > tolerance:
            raise ValueError(f"{year} balance-sheet gap: {gap:.6f}")

        cash_gap = row["cash"] - MINIMUM_CASH
        if cash_gap < -tolerance:
            raise ValueError(f"{year} minimum-cash gap: {cash_gap:.6f}")

        revolver_gap = REVOLVER_LIMIT - row["revolver"]
        if revolver_gap < -tolerance:
            raise ValueError(f"{year} revolver-limit gap: {revolver_gap:.6f}")


def print_table(
    title: str,
    rows: List[tuple[str, str, float]],
    projection: List[Dict[str, float]],
) -> None:
    """Print a table with line items down the page and years across."""
    label_width = max(31, max(len(label) for label, _, _ in rows))
    print(f"\n{title} (USD millions)")
    print(f"{'':<{label_width}}" + "".join(f"{year:>13}" for year in YEARS))
    print("-" * (label_width + 13 * len(YEARS)))
    for label, key, sign in rows:
        values = "".join(f"{sign * row[key]:>13,.1f}" for row in projection)
        print(f"{label:<{label_width}}{values}")


def print_projection(projection: List[Dict[str, float]]) -> None:
    income_statement = [
        ("Revenue", "revenue", 1.0),
        ("Cost of sales", "cost_of_sales", -1.0),
        ("Gross profit", "gross_profit", 1.0),
        ("SG&A", "sga", -1.0),
        ("Depreciation", "depreciation", -1.0),
        ("Impairment", "impairment", -1.0),
        ("Operating income", "operating_income", 1.0),
        ("Interest expense", "interest", -1.0),
        ("Pretax income", "pretax_income", 1.0),
        ("Tax", "tax", -1.0),
        ("Net income", "net_income", 1.0),
    ]
    balance_sheet = [
        ("Cash", "cash", 1.0),
        ("Inventory", "inventory", 1.0),
        ("PP&E", "ppe", 1.0),
        ("Other assets", "other_assets", 1.0),
        ("Total assets", "total_assets", 1.0),
        ("Floor plan", "floor_plan", 1.0),
        ("Term debt", "debt", 1.0),
        ("Revolver", "revolver", 1.0),
        ("Other liabilities", "other_liabilities", 1.0),
        ("Equity", "equity", 1.0),
        ("Total liabilities and equity", "total_liabilities_and_equity", 1.0),
    ]
    cash_flow_statement = [
        ("Net income", "net_income", 1.0),
        ("Depreciation", "depreciation", 1.0),
        ("Impairment", "impairment", 1.0),
        ("Capital spending", "capex", -1.0),
        ("Change in inventory", "change_in_inventory", -1.0),
        (
            "Change in other working capital",
            "change_in_other_working_capital",
            -1.0,
        ),
        ("Change in floor plan", "change_in_floor_plan", 1.0),
        ("Debt repayment", "debt_repayment", -1.0),
        ("Free cash flow to equity", "fcfe", 1.0),
        ("Share buyback", "buyback", -1.0),
        ("Revolver draw", "revolver_draw", 1.0),
        ("Revolver repayment", "revolver_repayment", -1.0),
        ("Net change in cash", "net_change_in_cash", 1.0),
    ]

    print_table("INCOME STATEMENT", income_statement, projection)
    print_table("BALANCE SHEET", balance_sheet, projection)
    print_table("CASH FLOW STATEMENT", cash_flow_statement, projection)

    print("\nCHECKS")
    print(f"{'':<31}" + "".join(f"{year:>13}" for year in YEARS))
    print("-" * (31 + 13 * len(YEARS)))
    print(
        f"{'Assets - liabilities - equity':<31}"
        + "".join(f"{row['balance_gap']:>13,.1f}" for row in projection)
    )
    print(
        f"{'Cash at or above minimum':<31}"
        + "".join(f"{str(row['cash_above_minimum']):>13}" for row in projection)
    )


def print_valuation(projection: List[Dict[str, float]]) -> None:
    present_value_of_fcfe = sum(
        row["fcfe"] / (1.0 + COST_OF_EQUITY) ** index
        for index, row in enumerate(projection, start=1)
    )
    final_year = projection[-1]
    terminal_cash_flow = final_year["fcfe"] + final_year["debt_repayment"]
    terminal_value = (
        terminal_cash_flow
        * (1.0 + TERMINAL_GROWTH)
        / (COST_OF_EQUITY - TERMINAL_GROWTH)
    )
    present_value_of_terminal = terminal_value / (1.0 + COST_OF_EQUITY) ** 5
    equity_value = present_value_of_fcfe + present_value_of_terminal
    value_after_2030 = present_value_of_terminal / equity_value
    value_per_share = equity_value / SHARES_OUTSTANDING

    print("\nVALUATION")
    print(f"Equity value (USD millions): {equity_value:,.2f}")
    print(f"Share of value after 2030:   {value_after_2030:.2%}")
    print(f"Value per share:             ${value_per_share:,.2f}")


def main() -> None:
    projection = build_projection()
    print_projection(projection)
    assert_balanced(projection)
    print_valuation(projection)


if __name__ == "__main__":
    main()
