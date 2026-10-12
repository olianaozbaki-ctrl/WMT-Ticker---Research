"""Diagnostic Walmart Project 1 five-year three-statement pro forma V3.

V3 separates net sales from membership and other income, reconciles opening
D&A to the FY2026 filing, and rolls finance-lease assets and liabilities under
a financing convention. USD millions. Results remain provisional because
several forecast and valuation-date inputs are not available in SEC filings.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List


YEARS = (2027, 2028, 2029, 2030, 2031)
TOLERANCE = 1e-6

# Existing V2 operating assumptions preserved unless the definition required a
# correction. The same growth path is provisionally applied to both revenue
# streams because no separate source-backed forecast is available.
NET_SALES_GROWTH = {2027: 0.043, 2028: 0.042, 2029: 0.040, 2030: 0.038, 2031: 0.035}
MEMBERSHIP_OTHER_GROWTH = deepcopy(NET_SALES_GROWTH)
GROSS_MARGIN_ON_NET_SALES = {
    2027: 0.2500,
    2028: 0.2510,
    2029: 0.2520,
    2030: 0.2525,
    2031: 0.2530,
}

# Cash operating expense is applied to gross profit plus membership/other
# income. This aligns the income-statement definitions while preserving the V2
# ratio path. The ratios remain forecast assumptions.
CASH_OPEX_TO_OPERATING_GROSS_PROFIT = {
    2027: 0.752,
    2028: 0.750,
    2029: 0.748,
    2030: 0.746,
    2031: 0.745,
}

CAPEX = {2027: 26_000.0, 2028: 28_000.0, 2029: 29_000.0, 2030: 30_000.0, 2031: 31_000.0}
CASH_TAX_RATE = 0.245
DEBT_REPAYMENT = {2027: 3_542.0, 2028: 3_237.0, 2029: 3_389.0, 2030: 2_143.0, 2031: 2_600.0}
DEBT_RATE = 0.045
FINANCE_LEASE_RATE = 0.057
DIVIDENDS = {2027: 8_000.0, 2028: 8_240.0, 2029: 8_487.2, 2030: 8_741.8, 2031: 9_004.1}
SHARE_BUYBACK = 0.0
MINIMUM_CASH = 8_000.0
REVOLVER_LIMIT = 15_000.0
REVOLVER_RATE = 0.050

# FY2026 source-backed D&A reconciliation. Reported total D&A was $14,203M;
# reported finance-lease ROU amortization was $888M. The residual $13,315M
# includes PP&E depreciation and intangible amortization, which the filing does
# not fully split. Using net PP&E as its forecast driver remains provisional.
FY2026_REPORTED_D_AND_A = 14_203.0
FY2026_FINANCE_LEASE_AMORTIZATION = 888.0
FY2026_NONLEASE_D_AND_A = FY2026_REPORTED_D_AND_A - FY2026_FINANCE_LEASE_AMORTIZATION

# FY2026 finance-lease additions and principal are used as explicit flat
# forecast assumptions because no supported FY2027-FY2031 schedule is available.
FINANCE_LEASE_ADDITIONS = {year: 703.0 for year in YEARS}
FINANCE_LEASE_PRINCIPAL = {year: 891.0 for year in YEARS}

OPENING: Dict[str, float] = {
    "net_sales": 706_413.0,
    "membership_other_income": 6_750.0,
    "revenue": 713_163.0,
    "cash": 10_727.0,
    "receivables": 11_172.0,
    "inventory": 58_851.0,
    "prepaid_and_other_excluded": 4_124.0,
    "ppe": 136_083.0,
    "operating_lease_rou_excluded": 14_750.0,
    "finance_lease_rou": 6_123.0,
    "goodwill_excluded": 28_735.0,
    "other_long_term_assets_excluded": 14_103.0,
    "accounts_payable": 63_061.0,
    "accrued_wages_and_benefits": 7_878.0,
    "self_insurance": 5_525.0,
    "accrued_non_income_taxes": 4_110.0,
    "deferred_gift_card_revenue": 2_941.0,
    "other_accrued_liabilities_excluded": 10_733.0,
    "accrued_income_taxes_excluded": 596.0,
    "debt": 44_762.0,
    "operating_lease_obligations_excluded": 15_572.0,
    "finance_lease_obligations": 6_761.0,
    "deferred_income_taxes_and_other_excluded": 16_549.0,
    "redeemable_nci_excluded": 293.0,
    "revolver": 0.0,
    "equity": 105_887.0,
}

NONLEASE_D_AND_A_TO_OPENING_PPE = FY2026_NONLEASE_D_AND_A / OPENING["ppe"]
FINANCE_LEASE_AMORTIZATION_TO_OPENING_ROU = (
    FY2026_FINANCE_LEASE_AMORTIZATION / OPENING["finance_lease_rou"]
)

OPERATING_ASSET_KEYS = ("receivables", "inventory")
OPERATING_LIABILITY_KEYS = (
    "accounts_payable",
    "accrued_wages_and_benefits",
    "self_insurance",
    "accrued_non_income_taxes",
    "deferred_gift_card_revenue",
)
EXCLUDED_ASSET_KEYS = (
    "prepaid_and_other_excluded",
    "operating_lease_rou_excluded",
    "goodwill_excluded",
    "other_long_term_assets_excluded",
)
EXCLUDED_LIABILITY_KEYS = (
    "other_accrued_liabilities_excluded",
    "accrued_income_taxes_excluded",
    "operating_lease_obligations_excluded",
    "deferred_income_taxes_and_other_excluded",
    "redeemable_nci_excluded",
)

FY2026_REPORTED_COST_OF_SALES = 535_395.0
INVENTORY_DAYS = OPENING["inventory"] / FY2026_REPORTED_COST_OF_SALES * 365.0
ACCOUNTS_PAYABLE_DAYS = OPENING["accounts_payable"] / FY2026_REPORTED_COST_OF_SALES * 365.0
RECEIVABLES_TO_REVENUE = OPENING["receivables"] / OPENING["revenue"]
OPERATING_ACCRUALS_TO_REVENUE = {
    key: OPENING[key] / OPENING["revenue"]
    for key in OPERATING_LIABILITY_KEYS
    if key != "accounts_payable"
}

BASE_INPUTS: Dict[str, Any] = {
    "net_sales_growth": deepcopy(NET_SALES_GROWTH),
    "membership_other_growth": deepcopy(MEMBERSHIP_OTHER_GROWTH),
    "gross_margin_on_net_sales": deepcopy(GROSS_MARGIN_ON_NET_SALES),
    "cash_opex_to_operating_gross_profit": deepcopy(CASH_OPEX_TO_OPERATING_GROSS_PROFIT),
    "nonlease_d_and_a_to_opening_ppe": NONLEASE_D_AND_A_TO_OPENING_PPE,
    "finance_lease_amortization_to_opening_rou": FINANCE_LEASE_AMORTIZATION_TO_OPENING_ROU,
    "finance_lease_additions": deepcopy(FINANCE_LEASE_ADDITIONS),
    "finance_lease_principal": deepcopy(FINANCE_LEASE_PRINCIPAL),
    "enforce_fy2026_d_and_a_reconciliation": True,
    "capex": deepcopy(CAPEX),
    "cash_tax_rate": CASH_TAX_RATE,
    "debt_repayment": deepcopy(DEBT_REPAYMENT),
    "debt_rate": DEBT_RATE,
    "finance_lease_rate": FINANCE_LEASE_RATE,
    "dividends": deepcopy(DIVIDENDS),
    "share_buyback": SHARE_BUYBACK,
    "minimum_cash": MINIMUM_CASH,
    "revolver_limit": REVOLVER_LIMIT,
    "revolver_rate": REVOLVER_RATE,
    "inventory_days": INVENTORY_DAYS,
    "accounts_payable_days": ACCOUNTS_PAYABLE_DAYS,
    "receivables_to_revenue": RECEIVABLES_TO_REVENUE,
    "operating_accruals_to_revenue": deepcopy(OPERATING_ACCRUALS_TO_REVENUE),
    "opening": deepcopy(OPENING),
}


def operating_nwc(row: Dict[str, float]) -> float:
    return sum(row[key] for key in OPERATING_ASSET_KEYS) - sum(
        row[key] for key in OPERATING_LIABILITY_KEYS
    )


def total_assets(row: Dict[str, float]) -> float:
    return (
        row["cash"]
        + row["receivables"]
        + row["inventory"]
        + row["ppe"]
        + row["finance_lease_rou"]
        + sum(row[key] for key in EXCLUDED_ASSET_KEYS)
    )


def total_claims(row: Dict[str, float]) -> float:
    return (
        sum(row[key] for key in OPERATING_LIABILITY_KEYS)
        + sum(row[key] for key in EXCLUDED_LIABILITY_KEYS)
        + row["debt"]
        + row["finance_lease_obligations"]
        + row["revolver"]
        + row["equity"]
    )


def validate_opening(inputs: Dict[str, Any]) -> None:
    opening = inputs["opening"]
    if abs(total_assets(opening) - 284_668.0) > TOLERANCE:
        raise ValueError("FY2026 opening assets do not reconcile to $284,668M")
    if abs(total_claims(opening) - 284_668.0) > TOLERANCE:
        raise ValueError("FY2026 opening claims do not reconcile to $284,668M")
    if abs(opening["net_sales"] + opening["membership_other_income"] - opening["revenue"]) > TOLERANCE:
        raise ValueError("FY2026 revenue components do not reconcile")
    if abs(operating_nwc(opening) - (-13_492.0)) > TOLERANCE:
        raise ValueError("FY2026 opening operating NWC does not reconcile")
    opening_d_and_a = (
        opening["ppe"] * inputs["nonlease_d_and_a_to_opening_ppe"]
        + opening["finance_lease_rou"]
        * inputs["finance_lease_amortization_to_opening_rou"]
    )
    if (
        inputs.get("enforce_fy2026_d_and_a_reconciliation", True)
        and abs(opening_d_and_a - FY2026_REPORTED_D_AND_A) > TOLERANCE
    ):
        raise ValueError("FY2026 D&A calibration does not reconcile to $14,203M")


def build_projection(inputs: Dict[str, Any] | None = None) -> List[Dict[str, float]]:
    run = deepcopy(BASE_INPUTS if inputs is None else inputs)
    validate_opening(run)
    prior = deepcopy(run["opening"])
    projection: List[Dict[str, float]] = []

    for year in YEARS:
        net_sales = prior["net_sales"] * (1.0 + run["net_sales_growth"][year])
        membership_other_income = prior["membership_other_income"] * (
            1.0 + run["membership_other_growth"][year]
        )
        revenue = net_sales + membership_other_income
        gross_profit = net_sales * run["gross_margin_on_net_sales"][year]
        cost_of_sales = net_sales - gross_profit
        operating_gross_profit = gross_profit + membership_other_income
        cash_opex = (
            operating_gross_profit
            * run["cash_opex_to_operating_gross_profit"][year]
        )
        nonlease_d_and_a = prior["ppe"] * run["nonlease_d_and_a_to_opening_ppe"]
        finance_lease_amortization = min(
            prior["finance_lease_rou"],
            prior["finance_lease_rou"]
            * run["finance_lease_amortization_to_opening_rou"],
        )
        total_d_and_a = nonlease_d_and_a + finance_lease_amortization
        ebit = operating_gross_profit - cash_opex - total_d_and_a
        interest = (
            prior["debt"] * run["debt_rate"]
            + prior["finance_lease_obligations"] * run["finance_lease_rate"]
            + prior["revolver"] * run["revolver_rate"]
        )
        pretax_income = ebit - interest
        income_tax = max(0.0, pretax_income) * run["cash_tax_rate"]
        net_income = pretax_income - income_tax

        receivables = revenue * run["receivables_to_revenue"]
        inventory = cost_of_sales * run["inventory_days"] / 365.0
        accounts_payable = cost_of_sales * run["accounts_payable_days"] / 365.0
        operating_accruals = {
            key: revenue * ratio
            for key, ratio in run["operating_accruals_to_revenue"].items()
        }
        capex = run["capex"][year]
        ppe = prior["ppe"] + capex - nonlease_d_and_a
        debt_repayment = min(run["debt_repayment"][year], prior["debt"])
        debt = prior["debt"] - debt_repayment

        lease_additions = run["finance_lease_additions"][year]
        lease_principal = min(
            run["finance_lease_principal"][year],
            prior["finance_lease_obligations"] + lease_additions,
        )
        finance_lease_rou = (
            prior["finance_lease_rou"]
            + lease_additions
            - finance_lease_amortization
        )
        finance_lease_obligations = (
            prior["finance_lease_obligations"] + lease_additions - lease_principal
        )

        row: Dict[str, float] = {
            "year": float(year),
            "net_sales": net_sales,
            "membership_other_income": membership_other_income,
            "revenue": revenue,
            "cost_of_sales": cost_of_sales,
            "gross_profit": gross_profit,
            "operating_gross_profit": operating_gross_profit,
            "cash_opex": cash_opex,
            "nonlease_d_and_a": nonlease_d_and_a,
            "finance_lease_amortization": finance_lease_amortization,
            "depreciation": total_d_and_a,
            "operating_income": ebit,
            "interest": interest,
            "pretax_income": pretax_income,
            "income_tax": income_tax,
            "net_income": net_income,
            "receivables": receivables,
            "inventory": inventory,
            "accounts_payable": accounts_payable,
            "ppe": ppe,
            "debt": debt,
            "finance_lease_rou": finance_lease_rou,
            "finance_lease_obligations": finance_lease_obligations,
            "finance_lease_additions": lease_additions,
            "finance_lease_principal": lease_principal,
        }
        row.update(operating_accruals)
        for key in EXCLUDED_ASSET_KEYS + EXCLUDED_LIABILITY_KEYS:
            row[key] = prior[key]

        opening_onwc = operating_nwc(prior)
        closing_onwc = operating_nwc(row)
        change_operating_nwc = closing_onwc - opening_onwc
        fcfe_before_distributions = (
            net_income
            + total_d_and_a
            - capex
            - change_operating_nwc
            - debt_repayment
            - lease_principal
        )
        dividends = run["dividends"][year]
        buyback = run["share_buyback"]
        cash_before_revolver = prior["cash"] + fcfe_before_distributions - dividends - buyback
        revolver = prior["revolver"]
        revolver_draw = 0.0
        revolver_repayment = 0.0
        if cash_before_revolver < run["minimum_cash"]:
            revolver_draw = run["minimum_cash"] - cash_before_revolver
            revolver += revolver_draw
            cash = run["minimum_cash"]
        else:
            revolver_repayment = min(revolver, cash_before_revolver - run["minimum_cash"])
            revolver -= revolver_repayment
            cash = cash_before_revolver - revolver_repayment

        row["cash"] = cash
        row["revolver"] = revolver
        row["equity"] = prior["equity"] + net_income - dividends - buyback
        row["operating_nwc"] = closing_onwc
        row["change_operating_nwc"] = change_operating_nwc
        row["capex"] = capex
        row["debt_repayment"] = debt_repayment
        row["fcfe_before_distributions"] = fcfe_before_distributions
        row["dividends"] = dividends
        row["buyback"] = buyback
        row["revolver_draw"] = revolver_draw
        row["revolver_repayment"] = revolver_repayment
        row["net_change_in_cash"] = cash - prior["cash"]
        row["total_assets"] = total_assets(row)
        row["total_liabilities_and_equity"] = total_claims(row)
        row["balance_gap"] = row["total_assets"] - row["total_liabilities_and_equity"]
        projection.append(row)
        prior = row

    return projection


def accounting_check_summary(
    projection: List[Dict[str, float]],
    inputs: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    run = BASE_INPUTS if inputs is None else inputs
    validate_opening(run)
    prior = run["opening"]
    issues: List[str] = []
    cash_gaps: List[float] = []
    debt_gaps: List[float] = []
    lease_gaps: List[float] = []
    for row in projection:
        year = int(row["year"])
        if abs(row["balance_gap"]) > TOLERANCE:
            issues.append(f"FY{year} balance-sheet gap {row['balance_gap']:.6f}")
        expected_cash = (
            prior["cash"]
            + row["fcfe_before_distributions"]
            - row["dividends"]
            - row["buyback"]
            + row["revolver_draw"]
            - row["revolver_repayment"]
        )
        cash_gap = row["cash"] - expected_cash
        cash_gaps.append(abs(cash_gap))
        if abs(cash_gap) > TOLERANCE:
            issues.append(f"FY{year} cash-flow articulation gap {cash_gap:.6f}")
        expected_debt = prior["debt"] - row["debt_repayment"]
        debt_gap = row["debt"] - expected_debt
        debt_gaps.append(abs(debt_gap))
        if abs(debt_gap) > TOLERANCE:
            issues.append(f"FY{year} debt roll-forward gap {debt_gap:.6f}")
        expected_lease = (
            prior["finance_lease_obligations"]
            + row["finance_lease_additions"]
            - row["finance_lease_principal"]
        )
        lease_gap = row["finance_lease_obligations"] - expected_lease
        lease_gaps.append(abs(lease_gap))
        if abs(lease_gap) > TOLERANCE:
            issues.append(f"FY{year} finance-lease roll-forward gap {lease_gap:.6f}")
        if row["cash"] < -TOLERANCE:
            issues.append(f"FY{year} negative cash")
        if row["cash"] < run["minimum_cash"] - TOLERANCE:
            issues.append(f"FY{year} cash below minimum")
        if row["revolver"] > run["revolver_limit"] + TOLERANCE:
            issues.append(f"FY{year} revolver above limit")
        for key in EXCLUDED_ASSET_KEYS + EXCLUDED_LIABILITY_KEYS:
            if abs(row[key] - prior[key]) > TOLERANCE:
                issues.append(f"FY{year} excluded balance changed without support: {key}")
        prior = row
    return {
        "valid": not issues,
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "max_abs_balance_gap": max(abs(row["balance_gap"]) for row in projection),
        "max_abs_cash_flow_gap": max(cash_gaps),
        "max_abs_debt_roll_forward_gap": max(debt_gaps),
        "max_abs_lease_roll_forward_gap": max(lease_gaps),
        "minimum_cash": min(row["cash"] for row in projection),
        "maximum_revolver": max(row["revolver"] for row in projection),
    }


def assert_balanced(projection: List[Dict[str, float]], inputs: Dict[str, Any] | None = None) -> None:
    checks = accounting_check_summary(projection, inputs)
    if not checks["valid"]:
        raise ValueError(checks["issues"][0])


def main() -> None:
    projection = build_projection()
    checks = accounting_check_summary(projection)
    print("WALMART PROJECT 1 PRO FORMA V3 -- DIAGNOSTIC, NOT FINAL")
    print("USD millions; net sales and membership/other income modeled separately.")
    print("Year   Net sales   Other income      EBIT      D&A    Lease debt      Cash   Balance gap")
    for row in projection:
        print(
            f"{int(row['year'])}  {row['net_sales']:10,.1f}  {row['membership_other_income']:12,.1f}"
            f"  {row['operating_income']:9,.1f}  {row['depreciation']:8,.1f}"
            f"  {row['finance_lease_obligations']:10,.1f}  {row['cash']:9,.1f}"
            f"  {row['balance_gap']:11,.6f}"
        )
    print(
        f"Checks: {checks['status']} | balance {checks['max_abs_balance_gap']:.6f}"
        f" | cash flow {checks['max_abs_cash_flow_gap']:.6f}"
        f" | debt roll {checks['max_abs_debt_roll_forward_gap']:.6f}"
        f" | lease roll {checks['max_abs_lease_roll_forward_gap']:.6f}"
        f" | minimum cash ${checks['minimum_cash']:,.1f}M"
        f" | maximum revolver ${checks['maximum_revolver']:,.1f}M"
    )
    if checks["issues"]:
        print("Issues: " + "; ".join(checks["issues"]))


if __name__ == "__main__":
    main()
