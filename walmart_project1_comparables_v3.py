"""Walmart Project 1 comparable-company valuation and triangulation.

Inputs are manually transcribed dated observations documented in the companion
evidence report. This file performs arithmetic only; it does not fetch or alter
market or filing data and does not modify any V2/V3 model.
"""
from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Any, Dict, List

import project1_fcff_v3 as dcf


VALUATION_DATE = "2026-09-23"


@dataclass(frozen=True)
class Peer:
    name: str
    ticker: str
    price: float
    price_date: str
    basic_shares_m: float
    share_date: str
    cash_m: float
    investments_m: float
    debt_claims_m: float
    bridge_date: str
    ttm_ebit_m: float
    ttm_diluted_eps: float
    earnings_date: str
    qualification: str


PEERS = (
    Peer(
        name="Target Corporation",
        ticker="TGT",
        price=156.26,
        price_date=VALUATION_DATE,
        basic_shares_m=454.296736,
        share_date="2026-08-21",
        cash_m=5_411.0,
        investments_m=0.0,
        debt_claims_m=15_357.0,
        bridge_date="2026-08-01",
        ttm_ebit_m=6_024.0,
        ttm_diluted_eps=9.64,
        earnings_date="TTM ended 2026-08-01",
        qualification="Primary broadline omnichannel peer",
    ),
    Peer(
        name="Costco Wholesale Corporation",
        ticker="COST",
        price=904.70,
        price_date=VALUATION_DATE,
        basic_shares_m=443.478804,
        share_date="2026-05-27",
        cash_m=18_946.0,
        investments_m=1_050.0,
        debt_claims_m=5_766.0,
        bridge_date="2026-05-10",
        ttm_ebit_m=11_225.0,
        ttm_diluted_eps=19.88,
        earnings_date="TTM ended 2026-05-10",
        qualification="Qualified membership-warehouse peer",
    ),
)

# Walmart TTM metrics available before September 23. EBIT is FY2026 operating
# income plus FY2027 H1 less FY2026 H1. EPS uses the same roll-forward.
WALMART_TTM_EBIT_M = 29_825.0 + 16_876.0 - 14_421.0
WALMART_TTM_DILUTED_EPS = 2.73 + 1.46 - 1.43


def peer_metrics(peer: Peer) -> Dict[str, Any]:
    meaningful_ev = peer.ttm_ebit_m > 0.0
    meaningful_pe = peer.ttm_diluted_eps > 0.0
    market_cap = peer.price * peer.basic_shares_m
    enterprise_value = (
        market_cap
        + peer.debt_claims_m
        - peer.cash_m
        - peer.investments_m
    )
    if abs(
        enterprise_value
        - (market_cap + peer.debt_claims_m - peer.cash_m - peer.investments_m)
    ) > 1e-9:
        raise AssertionError(f"{peer.ticker} EV arithmetic failed")
    return {
        "peer": peer,
        "market_cap": market_cap,
        "enterprise_value": enterprise_value,
        "ev_ebit": enterprise_value / peer.ttm_ebit_m if meaningful_ev else None,
        "pe": peer.price / peer.ttm_diluted_eps if meaningful_pe else None,
        "ev_meaningful": meaningful_ev,
        "pe_meaningful": meaningful_pe,
    }


def apply_to_walmart(metrics: Dict[str, Any]) -> Dict[str, float | None]:
    ev_multiple = metrics["ev_ebit"]
    pe_multiple = metrics["pe"]
    implied_ev = ev_multiple * WALMART_TTM_EBIT_M if ev_multiple is not None else None
    implied_equity = (
        implied_ev
        + dcf.BRIDGE_CASH_M
        + dcf.BRIDGE_NONOPERATING_INVESTMENTS_M
        - dcf.BRIDGE_DEBT_FAIR_VALUE_PROXY_M
        - dcf.BRIDGE_FINANCE_LEASES_M
        - dcf.BRIDGE_NCI_M
        if implied_ev is not None
        else None
    )
    implied_equity_without_separate_finance_lease_claim = (
        implied_ev
        + dcf.BRIDGE_CASH_M
        + dcf.BRIDGE_NONOPERATING_INVESTMENTS_M
        - dcf.BRIDGE_DEBT_FAIR_VALUE_PROXY_M
        - dcf.BRIDGE_NCI_M
        if implied_ev is not None
        else None
    )
    return {
        "ev_ebit_value_per_share": (
            implied_equity / dcf.PROVISIONAL_BASIC_SHARES_M
            if implied_equity is not None
            else None
        ),
        "ev_ebit_value_per_share_without_finance_lease_claim": (
            implied_equity_without_separate_finance_lease_claim
            / dcf.PROVISIONAL_BASIC_SHARES_M
            if implied_equity_without_separate_finance_lease_claim is not None
            else None
        ),
        "pe_value_per_share": (
            pe_multiple * WALMART_TTM_DILUTED_EPS
            if pe_multiple is not None
            else None
        ),
        "implied_enterprise_value": implied_ev,
        "implied_equity_value": implied_equity,
    }


def run_analysis() -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    issues: List[str] = []
    for peer in PEERS:
        metrics = peer_metrics(peer)
        valuation = apply_to_walmart(metrics)
        if abs(metrics["market_cap"] - peer.price * peer.basic_shares_m) > 1e-9:
            issues.append(f"{peer.ticker} market-cap arithmetic failed")
        if metrics["ev_ebit"] is not None and abs(
            metrics["ev_ebit"] * peer.ttm_ebit_m - metrics["enterprise_value"]
        ) > 1e-8:
            issues.append(f"{peer.ticker} EV/EBIT arithmetic failed")
        if metrics["pe"] is not None and abs(
            metrics["pe"] * peer.ttm_diluted_eps - peer.price
        ) > 1e-8:
            issues.append(f"{peer.ticker} P/E arithmetic failed")
        if valuation["ev_ebit_value_per_share"] is not None and abs(
            valuation["ev_ebit_value_per_share"]
            - valuation["implied_equity_value"] / dcf.PROVISIONAL_BASIC_SHARES_M
        ) > 1e-9:
            issues.append(f"{peer.ticker} EV/EBIT bridge/share arithmetic failed")
        if peer.price_date != VALUATION_DATE:
            issues.append(f"{peer.ticker} price date is inconsistent")
        if not metrics["ev_meaningful"]:
            issues.append(f"{peer.ticker} EV/EBIT is not meaningful")
        if not metrics["pe_meaningful"]:
            issues.append(f"{peer.ticker} P/E is not meaningful")
        rows.append({**metrics, **valuation})

    ev_values = [row["ev_ebit_value_per_share"] for row in rows if row["ev_ebit_value_per_share"] is not None]
    pe_values = [row["pe_value_per_share"] for row in rows if row["pe_value_per_share"] is not None]
    if len(ev_values) < 2 or len(pe_values) < 2:
        issues.append("Fewer than two meaningful peer observations")

    v3 = dcf.diagnostic_case()
    if not v3["checks"]["valid"] or dcf.dcf_check_summary(v3)["status"] != "PASS":
        issues.append("Imported V3 case failed validation")

    return {
        "rows": rows,
        "ev_range": (min(ev_values), max(ev_values)) if ev_values else None,
        "pe_range": (min(pe_values), max(pe_values)) if pe_values else None,
        "ev_median": median(ev_values) if ev_values else None,
        "pe_median": median(pe_values) if pe_values else None,
        "v3_value_per_share": v3["valuation"]["per_share"],
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }


def main() -> None:
    result = run_analysis()
    print("WALMART PROJECT 1 V3 COMPARABLE VALUATION -- DIAGNOSTIC, NOT FINAL")
    print(f"Market-price date: {VALUATION_DATE}")
    print(f"Walmart TTM EBIT ${WALMART_TTM_EBIT_M:,.1f}M | TTM diluted EPS ${WALMART_TTM_DILUTED_EPS:.2f}")
    for row in result["rows"]:
        peer = row["peer"]
        print(
            f"{peer.ticker}: EV ${row['enterprise_value']:,.1f}M | EV/EBIT {row['ev_ebit']:.4f}x"
            f" | P/E {row['pe']:.4f}x | Walmart EV/EBIT value ${row['ev_ebit_value_per_share']:.2f}"
            f" | no-finance-lease bridge ${row['ev_ebit_value_per_share_without_finance_lease_claim']:.2f}"
            f" | Walmart P/E value ${row['pe_value_per_share']:.2f}"
        )
    print(
        f"EV/EBIT range ${result['ev_range'][0]:.2f}-${result['ev_range'][1]:.2f}"
        f" | P/E range ${result['pe_range'][0]:.2f}-${result['pe_range'][1]:.2f}"
    )
    print(f"Validation: {result['status']}")
    if result["issues"]:
        for issue in result["issues"]:
            print(f"FAIL: {issue}")


if __name__ == "__main__":
    main()
