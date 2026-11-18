"""Streamlit interface for the Meridian Foundation investment review."""

from pathlib import Path

import streamlit as st

from project2_engine.phase2 import TICKERS, run_phase2


PROJECT_ROOT = Path(__file__).resolve().parent


def pct(value: float) -> str:
    return f"{value:.2%}"


def analysis() -> dict:
    return run_phase2(PROJECT_ROOT)


def portfolio_label(name: str) -> str:
    if name == "Constrained minimum volatility":
        return "Constrained minimum-volatility model portfolio"
    return name


def main() -> None:
    st.set_page_config(page_title="Meridian Foundation — Investment Review", layout="wide")
    result = analysis()
    st.title("Meridian Foundation Investment Management Application")
    st.caption(
        "OpenAI Codex assisted with architecture, implementation, tests, and documentation. "
        "The student owns the analysis and investment decision. Educational project only; "
        "not investment advice."
    )
    st.warning(
        "Portfolio analysis for committee review. Model feasibility is separate from verified "
        "mandate compliance; actual holdings, position-sized liquidity evidence, issuer exposure, "
        "and observed transaction costs remain unavailable."
    )
    output_path = PROJECT_ROOT / "outputs" / "phase2_results.md"
    if output_path.exists():
        st.download_button(
            "Download generated portfolio results",
            data=output_path.read_text(encoding="utf-8"),
            file_name="phase2_results.md",
            mime="text/markdown",
        )

    st.subheader("Decision-date data and provenance")
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
    cards[2].metric("CPI-U inflation (BLS)", f"{result['cpi_yoy']:.4%}")
    cards[3].metric("CPI + 4% target", f"{result['provisional_after_cost_hurdle']:.4%}")
    cpi = result["stress_matrix"]["return_hurdle_cpi"]
    st.write(
        "**Prices:** Yahoo Finance daily adjusted close (USD, split- and distribution-adjusted), "
        "transformed to aligned calendar-month-end observations. **Window:** 2021-10-29 through "
        f"{result['market_data_as_of']} ({result['monthly_return_observations']} monthly returns). "
        "**Aligned price-panel missing values:** 0."
    )
    st.info(
        f"**CPI input:** BLS archived August 2026 CPI-U release, not seasonally adjusted. "
        f"{cpi['prior_observation_date']} = {cpi['prior_year_value']:.3f}; "
        f"{cpi['current_observation_date']} = {cpi['current_value']:.3f}. The release was "
        f"available {cpi['current_availability_date']}, before the {cpi['decision_date']} "
        "decision boundary. This is verified BLS release evidence, not an ALFRED API vintage. "
        f"Source: {cpi['source_url']}"
    )

    st.subheader("Portfolio comparison")
    rows = []
    allocation_rows = []
    gross_risk_rows = []
    net_risk_rows = []
    optimization = result["optimization"]
    for portfolio in result["portfolios"]:
        label = portfolio_label(portfolio["name"])
        allocation_rows.append({"Portfolio": label, **portfolio["weights"]})
        gross_risk_rows.append({
            "Portfolio": label,
            "Annualized volatility": portfolio["annual_volatility"],
            "Annualized expected return": portfolio["annual_expected_return"],
        })
        net_risk_rows.append({
            "Portfolio": label,
            "Annualized volatility": portfolio["annual_volatility"],
            "Annualized expected return": portfolio["illustrative_net_expected_return"],
        })
        model_status = (
            "Provisionally feasible (optimizer)"
            if portfolio["kind"] == "provisional_model_portfolio" and optimization["provisional_feasible_on_supported_model_inputs"]
            else "Reference portfolio"
        )
        rows.append(
            {
                "Portfolio": label,
                **{ticker: pct(portfolio["weights"][ticker]) for ticker in TICKERS},
                "Gross expected return": pct(portfolio["annual_expected_return"]),
                "Illustrative after-cost expected return": pct(portfolio["illustrative_net_expected_return"]),
                "Annualized volatility": pct(portfolio["annual_volatility"]),
                "Reserve": pct(portfolio["reserve_allocation"]),
                "Illustrative turnover": pct(
                    portfolio["illustrative_turnover_from_equal_weight"]
                ),
                "Illustrative cost": pct(portfolio["illustrative_transaction_cost_rate"]),
                "Liquidity": portfolio["liquidity_status"],
                "Modeled construction status": model_status,
                "Full mandate compliance verified": portfolio["verified_mandate_feasible"],
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.caption("Gross expected returns are annualized arithmetic historical estimates. The after-cost figure deducts one illustrative rebalance cost from a hypothetical equal-weight starting portfolio; it is not an observed or recurring Meridian cost estimate.")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.markdown("**Asset allocation by portfolio**")
        st.bar_chart(allocation_rows, x="Portfolio", y=list(TICKERS), use_container_width=True)
    with chart_right:
        st.markdown("**Gross risk-return comparison**")
        st.scatter_chart(gross_risk_rows, x="Annualized volatility", y="Annualized expected return", color="Portfolio", use_container_width=True)
    st.markdown("**Illustrative after-cost risk-return comparison**")
    st.scatter_chart(net_risk_rows, x="Annualized volatility", y="Annualized expected return", color="Portfolio", use_container_width=True)

    st.subheader("Rule-by-rule mandate assessment")
    st.caption("A feasible model portfolio is not the same as verified full mandate compliance. Unknown or unverified evidence remains NOT_TESTABLE or UNRESOLVED in the rule results below.")
    selected = st.selectbox("Portfolio", [item["name"] for item in result["portfolios"]], format_func=portfolio_label)
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

    st.subheader("Modeled feasibility and evidence status")
    if optimization["provisional_feasible_on_supported_model_inputs"]:
        st.success(
            f"The constrained optimizer is feasible on supported model inputs: a 1% grid portfolio was found after evaluating "
            f"{optimization['combinations_evaluated']:,} long-only combinations."
        )
    else:
        st.error(f"No feasible portfolio: {optimization['reason']}")
    st.write("**Enforced:** " + "; ".join(optimization["constraints_enforced"]))
    st.write(
        "**Not claimed as verified:** "
        + "; ".join(optimization["constraints_not_claimed_as_verified"])
    )
    st.error("Verified full mandate compliance: NO. Model feasibility does not establish actual turnover, five-day liquidity, issuer treatment/exposure, actual transaction costs, or S9 compliance.")
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

    st.subheader("Stress-test scenario analysis")
    st.caption(
        f"Stress calculations use market observations through "
        f"{result['stress_matrix']['market_data_as_of']} ({result['stress_matrix']['market_return_observations']} monthly returns), "
        f"available by the historical signal decision date {result['stress_matrix']['decision_date']}. "
        "The DGS10 row is historical validation evidence, not a current quote."
    )
    if not result["stress_matrix"]["return_hurdle_cpi"]["point_in_time_valid_for_decision_date"]:
        st.error("Stress decision stop: the CPI hurdle was not point-in-time valid for the DGS10 decision date. Numerical optimizer feasibility below is conditional only.")
    else:
        st.success(f"Point-in-time CPI gate passed using BLS observations dated {cpi['prior_observation_date']} and {cpi['current_observation_date']}, available {cpi['current_availability_date']} before the {cpi['decision_date']} decision.")
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

    st.subheader("Investment decision framework")
    decision = result["decision_support"]
    decision_output_path = PROJECT_ROOT / "outputs" / "phase4a_decision_support.md"
    if decision_output_path.exists():
        st.download_button(
            "Download investment decision-support report",
            data=decision_output_path.read_text(encoding="utf-8"),
            file_name="phase4a_decision_support.md",
            mime="text/markdown",
        )
    st.warning(
        f"Candidate disposition for your review: {decision['candidate_disposition_for_student_review']}. "
        f"{decision['candidate_action']} This is decision support, not a final investment judgment."
    )
    cpi_status = decision["point_in_time_cpi"]
    if cpi_status["admissible_for_stress_decision"]:
        st.info(
            f"CPI + 4% objective inputs are point-in-time admissible for {cpi_status['decision_date']}: "
            f"August 2025/2026 CPI-U observations were both available {cpi_status['current_cpi_availability_date']}. "
            f"Inflation: {cpi_status['inflation_rate']:.4%}; modeled target: {cpi_status['modeled_hurdle_used']:.4%}. "
            "BLS release evidence is used; no ALFRED API vintage is claimed."
        )
    else:
        st.error(
            f"STOP: CPI inputs are not point-in-time admissible for {cpi_status['decision_date']}. "
            "Do not interpret scenario feasibility as decision-date feasibility."
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
