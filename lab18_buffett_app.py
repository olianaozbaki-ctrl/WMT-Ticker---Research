"""Streamlit interface for the FIN 43900 Lab 18 Buffett skill."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
SKILL_SCRIPTS = ROOT / ".codex" / "skills" / "warren-buffett-investing" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from sec_buffett import (  # noqa: E402
    CHECK_LABELS,
    EdgarError,
    fetch_analysis,
    make_user_agent,
    money_millions,
    percent,
    unsupported_memo_numbers,
    write_json,
)


OUTPUT_DIR = ROOT / "lab18_output"


def chart_frame(analysis: dict) -> pd.DataFrame:
    records = []
    for row in analysis["rows"]:
        records.extend(
            [
                {
                    "Fiscal year end": row["fiscal_year_end"],
                    "Measure": "Owner earnings",
                    "USD millions": (
                        None
                        if row["owner_earnings"]["value"] is None
                        else row["owner_earnings"]["value"] / 1_000_000
                    ),
                },
                {
                    "Fiscal year end": row["fiscal_year_end"],
                    "Measure": "Net income",
                    "USD millions": (
                        None
                        if row["net_income"]["value"] is None
                        else row["net_income"]["value"] / 1_000_000
                    ),
                },
            ]
        )
    return pd.DataFrame(records)


def financial_table(analysis: dict) -> pd.DataFrame:
    records = []
    for row in analysis["rows"]:
        record = {"Fiscal year end": row["fiscal_year_end"]}
        for field, label in (
            ("revenue", "Revenue"),
            ("net_income", "Net income"),
            ("operating_cash_flow", "Operating cash flow"),
            ("capital_spending", "Capital spending"),
            ("equity", "Equity"),
        ):
            record[f"{label} ($m)"] = money_millions(row[field]["value"])
            record[f"{label} tag"] = row[field]["tag"] or "not found"
        record["ROE"] = percent(row["roe"]["value"])
        record["ROE tag"] = row["roe"]["tag"] or "not found"
        record["Owner earnings ($m)"] = money_millions(
            row["owner_earnings"]["value"]
        )
        record["Owner earnings tag"] = (
            row["owner_earnings"]["tag"] or "not found"
        )
        records.append(record)
    return pd.DataFrame(records)


st.set_page_config(page_title="Lab 18 Buffett Skill", layout="wide")
st.title("Warren Buffett Business-Quality Review")
st.caption(
    "Data from SEC EDGAR; built with AI help, a learning demonstration, "
    "not investment advice."
)

with st.expander("SEC EDGAR contact (used only in the request header)", expanded=False):
    sec_name = st.text_input(
        "Name", value=os.environ.get("SEC_EDGAR_NAME", ""), autocomplete="off"
    )
    sec_email = st.text_input(
        "Email", value=os.environ.get("SEC_EDGAR_EMAIL", ""), autocomplete="off"
    )
    st.caption("These values are not written to the output files.")

ticker = st.text_input("Ticker", value="COST").strip().upper()
analyze = st.button("Analyze five fiscal years", type="primary")

if analyze:
    try:
        user_agent = make_user_agent(sec_name, sec_email)
        with st.spinner("Retrieving SEC company facts and running Python checks..."):
            analysis = fetch_analysis(ticker, user_agent)
        st.session_state["analysis"] = analysis
        st.session_state["ticker"] = ticker
        write_json(OUTPUT_DIR / f"{ticker}_buffett_data.json", analysis)
    except (EdgarError, OSError, ValueError) as exc:
        st.error(str(exc))

analysis = st.session_state.get("analysis")
if analysis and st.session_state.get("ticker") == ticker:
    st.subheader(f"{analysis['company_name']} ({analysis['ticker']})")

    chart = chart_frame(analysis)
    if chart.empty or chart["USD millions"].isna().all():
        st.warning("Owner earnings and net income were not found for the chart.")
    else:
        st.line_chart(
            chart,
            x="Fiscal year end",
            y="USD millions",
            color="Measure",
        )

    st.subheader("Five-year financial table")
    st.caption("Financial statement values are USD millions; scroll right for tags.")
    st.dataframe(financial_table(analysis), hide_index=True, width="stretch")

    st.subheader("Buffett checks (computed in Python)")
    for key, label in CHECK_LABELS.items():
        result = analysis["checks"][key]
        icon = {"pass": "✅", "fail": "❌", "not known": "❓"}[result]
        st.write(f"{icon} **{label}:** {result}")

    st.subheader("Saved Buffett-style memo")
    memo_path = OUTPUT_DIR / f"{ticker}_buffett_memo.md"
    if memo_path.exists():
        memo = memo_path.read_text(encoding="utf-8")
        st.markdown(memo)
        unsupported = unsupported_memo_numbers(memo, analysis)
        if unsupported:
            st.error(
                "Numbers in the memo that the script did not produce: "
                + ", ".join(f"`{number}`" for number in unsupported)
            )
        else:
            st.success("Memo number check: no unsupported numbers found.")
    else:
        st.info(
            f"No saved memo yet. Use the `$warren-buffett-investing` skill to create "
            f"`lab18_output/{ticker}_buffett_memo.md`, then rerun the app."
        )

