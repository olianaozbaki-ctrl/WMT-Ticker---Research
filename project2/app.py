"""Streamlit interface for the Meridian Foundation Phase 2 analysis."""

from pathlib import Path

import streamlit as st

from project2_engine.phase2 import TICKERS, run_phase2


PROJECT_ROOT = Path(__file__).resolve().parent


def pct(value: float) -> str:
    return f"{value:.2%}"


def analysis() -> dict:
    return run_phase2(PROJECT_ROOT)


def main() -> None:
    st.set_page_config(page_title="Meridian Foundation — Phase 2", layout="wide")
    result = analysis()
    st.title("Meridian Foundation Investment Management Application")
    st.caption(
        "OpenAI Codex assisted with architecture, implementation, tests, and documentation. "
        "The student owns the analysis and investment decision. Educational project only; "
        "not investment advice."
    )
    st.warning(
        "Phase 2 model comparison, not a committee recommendation. Liquidity, actual holdings, "
        "observed trading costs, and ALFRED CPI vintage verification remain unavailable."
    )
    output_path = PROJECT_ROOT / "outputs" / "phase2_results.md"
    if output_path.exists():
        st.download_button(
            "Download generated Phase 2 results",
            data=output_path.read_text(encoding="utf-8"),
            file_name="phase2_results.md",
            mime="text/markdown",
        )

    st.subheader("Data card and as-of boundary")
    cards = st.columns(4)
    cards[0].metric("Market data as of", result["market_data_as_of"])
    cards[1].metric("Monthly return observations", result["monthly_return_observations"])
    cards[2].metric("Provisional CPI YoY", pct(result["cpi_yoy"]))
    cards[3].metric("After-cost hurdle", pct(result["provisional_after_cost_hurdle"]))
    st.write(
        "**Prices:** Yahoo Finance daily adjusted close (USD, split- and distribution-adjusted), "
        "transformed to aligned calendar-month-end observations. **Window:** 2021-10-29 through "
        f"{result['market_data_as_of']}. **Missing aligned values:** 0. "
        "**CPI:** CPIAUCSL September 2026 versus September 2025 current FRED snapshot; "
        "ALFRED vintage not verified. October YoY is unavailable because October 2025 CPI was not published."
    )

    st.subheader("Side-by-side portfolio results")
    rows = []
    for portfolio in result["portfolios"]:
        rows.append(
            {
                "Portfolio": portfolio["name"],
                **{ticker: pct(portfolio["weights"][ticker]) for ticker in TICKERS},
                "Expected return": pct(portfolio["annual_expected_return"]),
                "Volatility": pct(portfolio["annual_volatility"]),
                "Reserve": pct(portfolio["reserve_allocation"]),
                "Illustrative turnover": pct(
                    portfolio["illustrative_turnover_from_equal_weight"]
                ),
                "Illustrative cost": pct(portfolio["illustrative_transaction_cost_rate"]),
                "Liquidity": portfolio["liquidity_status"],
                "Verified feasible": portfolio["verified_mandate_feasible"],
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.caption(
        "Expected returns are annualized arithmetic historical estimates. Turnover is shown only "
        "from the explicitly hypothetical equal-weight start; it is not actual Meridian turnover."
    )

    st.subheader("Individual mandate verdicts")
    selected = st.selectbox("Portfolio", [item["name"] for item in result["portfolios"]])
    portfolio = next(item for item in result["portfolios"] if item["name"] == selected)
    verdict_rows = [
        {
            "Rule": rule["label"],
            "Verdict": rule["status"],
            "Measured": rule["measured_value"],
            "Limit": rule["limit_value"],
            "Units": rule["units"],
            "Explanation": rule["explanation"],
        }
        for rule in portfolio["rules"]
    ]
    st.dataframe(verdict_rows, use_container_width=True, hide_index=True)

    st.subheader("Optimization status")
    optimization = result["optimization"]
    if optimization["provisional_feasible_on_supported_model_inputs"]:
        st.success(
            f"A provisionally feasible 1% grid portfolio was found after evaluating "
            f"{optimization['combinations_evaluated']:,} long-only combinations."
        )
    else:
        st.error(f"No feasible portfolio: {optimization['reason']}")
    st.write("**Enforced:** " + "; ".join(optimization["constraints_enforced"]))
    st.write(
        "**Not claimed as verified:** "
        + "; ".join(optimization["constraints_not_claimed_as_verified"])
    )
    st.error(
        "Full mandate feasible: False. Provisional optimization does not establish actual "
        "turnover, liquidity, issuer, or CPI-vintage compliance."
    )
    stop = optimization["hypothetical_turnover_cap_stop_condition"]
    st.subheader("Hypothetical turnover-cap stop condition")
    st.write(f"**Starting holdings:** {stop['starting_holdings']}")
    if stop["feasible"]:
        st.success("The hypothetical starting portfolio can meet the modeled constraints.")
    else:
        st.error(
            f"No portfolio meets both the {stop['maximum_turnover']:.0%} hypothetical turnover "
            f"cap and the {stop['return_hurdle']:.2%} provisional hurdle. The best net return "
            f"is {stop['maximum_net_expected_return']:.2%}, a {stop['return_shortfall']:.2%} shortfall."
        )
    st.caption(
        "This is a sensitivity using hypothetical equal-weight holdings, not evidence about "
        "actual Meridian turnover. Actual holdings remain unavailable."
    )

    st.subheader("Remaining limitations")
    for limitation in result["limitations"]:
        st.write(f"- {limitation}")


if __name__ == "__main__":
    main()
