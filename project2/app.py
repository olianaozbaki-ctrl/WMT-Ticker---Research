"""Phase 1 Streamlit shell for the Meridian Foundation application."""

from pathlib import Path

import streamlit as st

from project2_engine.config import load_mandate


PROJECT_ROOT = Path(__file__).resolve().parent
MANDATE_PATH = PROJECT_ROOT / "config" / "mandate.json"


def main() -> None:
    """Display the approved mandate and unresolved Phase 1 policy decisions."""
    mandate = load_mandate(MANDATE_PATH)

    st.set_page_config(page_title="Meridian Foundation — Phase 1", layout="wide")
    st.title("Meridian Foundation Investment Management Application")
    st.caption(
        "Built with OpenAI Codex assistance for software architecture and testing. "
        "The analysis and investment decision remain the student's responsibility. "
        "Educational project only; not investment advice."
    )
    st.warning(
        "Phase 1 foundation only: no final portfolio, validation claim, or committee "
        "recommendation is presented."
    )

    st.subheader("Committee decision")
    st.write(mandate["decision_context"]["committee_question"])

    objective = mandate["objective"]
    left, right = st.columns(2)
    with left:
        st.subheader("Mandate")
        st.write(f"**Horizon:** {mandate['horizon_years']} years")
        st.write(f"**Rebalancing:** {mandate['rebalance_frequency']}")
        st.write(
            "**Objective:** CPI + "
            f"{objective['real_return_spread']:.1%} after costs over rolling "
            f"{objective['measurement_window_years']}-year periods"
        )
        st.write(f"**Benchmark:** {mandate['benchmark']['description']}")
    with right:
        st.subheader("Hard limits")
        st.write(
            f"**Reserve:** {mandate['reserve']['minimum_weight']:.1%} in approved "
            "reserve-eligible assets"
        )
        st.write(
            f"**Liquidity:** at least {mandate['liquidity']['minimum_weight']:.1%} "
            f"within {mandate['liquidity']['maximum_business_days']} business days"
        )
        st.write(
            f"**Issuer limit:** {mandate['issuer_limit']['maximum_weight']:.1%}, "
            "subject to documented exemptions"
        )
        st.write(f"**Turnover limit:** {mandate['turnover']['maximum']:.1%} annually")

    st.subheader("Unresolved decisions")
    for item in mandate["unresolved_decisions"]:
        st.write(f"- **{item['id']}** — {item['question']}")


if __name__ == "__main__":
    main()
