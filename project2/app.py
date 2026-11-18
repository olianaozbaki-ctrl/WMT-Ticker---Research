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
    signal = result["dgs10_signal"]
    st.subheader("DGS10 point-in-time signal")
    if signal["available"]:
        st.metric("10-year Treasury yield", f"{signal['value_percent']:.2f}%")
        st.write(f"Observation: {signal['observation_date']} · Available: {signal['availability_date']} · Decision date: {signal['decision_date']}")
        st.write(signal["interpretation"])
        st.caption(signal["action"])
    else:
        st.warning(signal["interpretation"])
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

    st.subheader("Interactive stress testing")
    st.caption(
        f"Stress calculations use market observations through "
        f"{result['stress_matrix']['market_data_as_of']} ({result['stress_matrix']['market_return_observations']} monthly returns), "
        f"available by the historical signal decision date {result['stress_matrix']['decision_date']}. "
        "The DGS10 row is historical validation evidence, not a current quote."
    )
    if not result["stress_matrix"]["return_hurdle_cpi"]["point_in_time_valid_for_decision_date"]:
        st.error("Stress decision stop: the CPI hurdle was not point-in-time valid for the DGS10 decision date. Numerical optimizer feasibility below is conditional only.")
    stress_rows = result["stress_matrix"]["scenarios"]
    selected_stress = st.multiselect("Scenarios", [row["scenario"] for row in stress_rows], default=[row["scenario"] for row in stress_rows])
    st.dataframe([{ "Scenario": row["scenario"], "Type": row["category"], "Estimation window": row["window"], "Status": row["status"], "Weights": row["weights"], "Gross return": row["annual_expected_return"], "Net return": row["net_expected_return"], "Volatility": row["annual_volatility"], "Turnover": row["turnover"], "Cost": row["cost_rate"], "Optimizer feasible": row["feasible"], "Rule verdicts": row["mandate_verdicts"] } for row in stress_rows if row["scenario"] in selected_stress], use_container_width=True, hide_index=True)
    comparison_rows = []
    for scenario in stress_rows:
        if scenario["scenario"] not in selected_stress:
            continue
        for item in scenario["portfolio_comparisons"]:
            comparison_rows.append({"Scenario": scenario["scenario"], "Portfolio": item["portfolio"], "Weights": item["weights"], "Gross return": item["annual_expected_return"], "Net return": item["net_expected_return"], "Volatility": item["annual_volatility"], "Turnover from hypothetical equal weight": item["turnover_from_hypothetical_equal_weight"], "Cost": item["cost_rate"], "Optimizer feasible": item["optimizer_feasible"], "Mandate verdicts": item["mandate_verdicts"]})
    st.dataframe(comparison_rows, use_container_width=True, hide_index=True)

    st.subheader("Phase 4A investment decision support")
    decision = result["decision_support"]
    decision_output_path = PROJECT_ROOT / "outputs" / "phase4a_decision_support.md"
    if decision_output_path.exists():
        st.download_button(
            "Download generated Phase 4A decision support",
            data=decision_output_path.read_text(encoding="utf-8"),
            file_name="phase4a_decision_support.md",
            mime="text/markdown",
        )
    st.warning(
        f"Candidate disposition for your review: {decision['candidate_disposition_for_student_review']}. "
        f"{decision['candidate_action']} This is decision support, not a final investment judgment."
    )
    cpi_status = decision["point_in_time_cpi"]
    st.error(
        f"Historical point-in-time stop: decision {cpi_status['decision_date']}; "
        f"September CPI availability {cpi_status['current_cpi_availability_date']}; "
        f"admissible: {cpi_status['admissible_for_stress_decision']}. The hurdle used in the existing stress run is not valid for this decision date."
    )
    st.write("**Full window versus 36 months:**")
    window_rows = []
    for group in decision["portfolio_comparisons"]:
        for item in group["portfolios"]:
            window_rows.append({"Estimation window": group["scenario"], "Portfolio": item["portfolio"], "Weights": item["weights"], "Gross expected return": item["annual_expected_return"], "Net expected return": item["net_expected_return"], "Volatility": item["annual_volatility"], "Mandate verdicts": item["mandate_verdicts"]})
    st.dataframe(window_rows, use_container_width=True, hide_index=True)
    st.write("**Model-feasible stress envelope (diagnostic only):**")
    envelope = decision["modeled_feasible_stress_envelope"]
    st.dataframe([{"Ticker": ticker, "Minimum": bounds["minimum"], "Maximum": bounds["maximum"]} for ticker,bounds in envelope["weights_by_ticker"].items()], use_container_width=True, hide_index=True)
    st.caption("Not an authorization range. Full-window versus 36-month estimates change the BIL allocation materially, and critical mandate evidence remains incomplete.")
    with st.expander("Decision rules and evidence requirements"):
        st.dataframe([{"Outcome": row["outcome"], "Decision rule": row["rule"]} for row in decision["decision_framework"]], use_container_width=True, hide_index=True)
        st.dataframe([{"Requirement": row["requirement"], "Status": row["status"], "Evidence and next requirement": row["available_evidence"] + " Needed: " + row["needed"], "Sources": ", ".join(source["title"] + ": " + source.get("url", source.get("repository_path", "")) for source in row["sources"])} for row in decision["evidence_requirements"]], use_container_width=True, hide_index=True)
    st.write("**Monitoring triggers and stop conditions**")
    st.dataframe([{"Trigger": row["trigger"], "Response": row["response"]} for row in decision["monitoring_triggers_and_stop_conditions"]], use_container_width=True, hide_index=True)
    st.write("**Decisions requiring your or the committee's approval**")
    for item in decision["committee_decisions_requested"]:
        st.write(f"- {item}")
    st.write("**Conditions that change the candidate disposition**")
    st.dataframe([{"Current outcome": row["current_outcome"], "Change to": row["change_to"], "Condition": row["condition"]} for row in decision["reversal_conditions"]], use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
