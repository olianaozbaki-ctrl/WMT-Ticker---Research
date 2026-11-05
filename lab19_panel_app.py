"""Streamlit interface for the FIN 43900 Lab 19 investor panel."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from lab19_panel import (
    BUFFETT_CHECK_LABELS,
    BURRY_CHECK_LABELS,
    WOOD_CHECK_LABELS,
    audit_all_memos,
    build_memos,
    fetch_panel_analysis,
    money_millions,
    ratio,
    write_json,
    write_memos,
)
from sec_buffett import EdgarError, make_user_agent, percent


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "lab19_output"


def financial_table(analysis: dict) -> pd.DataFrame:
    records = []
    for row in analysis["rows"]:
        records.append(
            {
                "Fiscal year end": row["fiscal_year_end"],
                "Revenue ($m)": money_millions(row["revenue"]["value"]),
                "Net income ($m)": money_millions(row["net_income"]["value"]),
                "Operating cash flow ($m)": money_millions(
                    row["operating_cash_flow"]["value"]
                ),
                "Capital spending ($m)": money_millions(
                    row["capital_spending"]["value"]
                ),
                "Equity ($m)": money_millions(row["equity"]["value"]),
                "ROE": percent(row["roe"]["value"]),
                "Owner earnings ($m)": money_millions(
                    row["owner_earnings"]["value"]
                ),
                "Reported R&D ($m)": money_millions(
                    row["research_and_development"]["value"]
                ),
                "Liabilities ($m)": money_millions(
                    row["liabilities"]["value"]
                ),
                "Liabilities / equity": ratio(
                    row["liabilities_to_equity"]["value"]
                ),
            }
        )
    return pd.DataFrame(records)


def panel_table(analysis: dict) -> pd.DataFrame:
    labels = {
        "Buffett": BUFFETT_CHECK_LABELS,
        "Wood": WOOD_CHECK_LABELS,
        "Burry": BURRY_CHECK_LABELS,
    }
    records = []
    for investor in ("Buffett", "Wood", "Burry"):
        for key, label in labels[investor].items():
            records.append(
                {
                    "Investor": investor,
                    "Check": label,
                    "Result": analysis["panel_checks"][investor][key],
                }
            )
    return pd.DataFrame(records)


def save_analysis_and_memos(analysis: dict) -> dict[str, str]:
    memos = build_memos(analysis)
    ticker = analysis["ticker"]
    write_json(OUTPUT_DIR / f"{ticker}_panel_data.json", analysis)
    write_memos(OUTPUT_DIR, ticker, memos)
    return memos


st.set_page_config(page_title="Lab 19 Investor Panel", layout="wide")
st.title("Buffett, Wood, and Burry Investor Panel")
st.caption(
    "Data from SEC EDGAR; built with AI help, a learning demonstration, "
    "not investment advice."
)
st.caption(
    "Wood's checks are a transparent course operational interpretation, "
    "not official ARK Invest rules."
)

with st.expander("SEC EDGAR contact (used only in the request header)"):
    sec_name = st.text_input(
        "Name", value=os.environ.get("SEC_EDGAR_NAME", ""), autocomplete="off"
    )
    sec_email = st.text_input(
        "Email", value=os.environ.get("SEC_EDGAR_EMAIL", ""), autocomplete="off"
    )
    st.caption("These values are never written to an output file.")

ticker = st.text_input("Ticker", value="COST").strip().upper()

left, right = st.columns(2)
with left:
    analyze = st.button("Analyze five fiscal years", type="primary")
with right:
    load_saved = st.button("Load saved Costco validation")

if analyze:
    try:
        user_agent = make_user_agent(sec_name, sec_email)
        with st.spinner("Retrieving SEC facts and running all checks..."):
            analysis = fetch_panel_analysis(ticker, user_agent)
        memos = save_analysis_and_memos(analysis)
        st.session_state["lab19_analysis"] = analysis
        st.session_state["lab19_memos"] = memos
    except (EdgarError, OSError, ValueError) as exc:
        st.error(str(exc))

if load_saved:
    saved_path = OUTPUT_DIR / "COST_panel_data.json"
    try:
        analysis = json.loads(saved_path.read_text(encoding="utf-8"))
        memos = build_memos(analysis)
        st.session_state["lab19_analysis"] = analysis
        st.session_state["lab19_memos"] = memos
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        st.error(f"Could not load the saved Costco validation: {exc}")

analysis = st.session_state.get("lab19_analysis")
memos = st.session_state.get("lab19_memos")

if analysis:
    st.subheader(f"{analysis['company_name']} ({analysis['ticker']})")
    st.caption(analysis["wood_framework_note"])

    st.subheader("Five-year SEC financial facts")
    st.dataframe(
        financial_table(analysis),
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Investor-by-check panel")
    st.dataframe(
        panel_table(analysis),
        hide_index=True,
        use_container_width=True,
    )

    verdict_columns = st.columns(3)
    for column, investor in zip(
        verdict_columns, ("Buffett", "Wood", "Burry")
    ):
        with column:
            st.metric(f"{investor} verdict", analysis["verdicts"][investor])

    st.subheader("Independent investor memos")
    memo_columns = st.columns(3)
    for column, investor in zip(memo_columns, ("Buffett", "Wood", "Burry")):
        with column:
            st.markdown(memos[investor])

    st.subheader("Unprinted-number check across all memos")
    audit = audit_all_memos(memos, analysis)
    unsupported = {
        investor: numbers for investor, numbers in audit.items() if numbers
    }
    if unsupported:
        for investor, numbers in unsupported.items():
            st.error(
                f"{investor} memo numbers not printed by the script: "
                + ", ".join(f"`{number}`" for number in numbers)
            )
    else:
        st.success("All three memos passed the unprinted-number check.")
