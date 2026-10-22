"""Interactive portfolio stability check for the Meridian training case."""

from hashlib import sha256
from io import BytesIO

import streamlit as st

from portfolio import (
    CORRELATIONS,
    OBJECTIVE_RETURN,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimate_from_price_csv,
    search_lowest_risk_mix,
)


def default_reserve_assets(asset_names):
    """Return sensible checkbox defaults for Meridian and its ETF equivalents."""
    return {
        name
        for name in asset_names
        if name in RESERVE_ELIGIBLE or name.upper() in {"BIL", "IEF"}
    }


def show_mix(result):
    """Render one search result."""
    if result is None:
        st.warning("No mix meets the objective and reserve minimum.")
        return

    for asset, weight in result["weights"].items():
        st.write(f"{asset}: **{weight:.2%}**")
    st.metric("Expected return", f"{result['expected_return']:.2%}")
    st.metric("Volatility", f"{result['volatility']:.2%}")
    st.metric(
        "Reserve-eligible weight",
        f"{result['reserve_eligible_weight']:.2%}",
    )


st.set_page_config(page_title="Portfolio Stability", layout="wide")
st.title("Portfolio Stability")
st.caption("Built with AI help, a learning demonstration, not investment advice.")

objective = st.sidebar.number_input(
    "Objective return",
    min_value=0.0,
    max_value=100.0,
    value=OBJECTIVE_RETURN * 100,
    step=0.1,
    format="%.1f",
) / 100
reserve_minimum = st.sidebar.number_input(
    "Reserve minimum",
    min_value=0.0,
    max_value=100.0,
    value=3.0,
    step=1.0,
    format="%.1f",
) / 100
uploaded_file = st.sidebar.file_uploader("Upload prices.csv", type="csv")
use_last_36 = st.sidebar.toggle("Use only the last 36 monthly returns")

if uploaded_file is None:
    loaded_sleeves = {name: values.copy() for name, values in SLEEVES.items()}
    loaded_correlations = {
        name: values.copy() for name, values in CORRELATIONS.items()
    }
    current_sleeves = {name: values.copy() for name, values in SLEEVES.items()}
    current_correlations = {
        name: values.copy() for name, values in CORRELATIONS.items()
    }
    source_label = "Meridian inputs"
    estimate_signature = "meridian"
else:
    uploaded_bytes = uploaded_file.getvalue()
    try:
        loaded_sleeves, loaded_correlations = estimate_from_price_csv(
            BytesIO(uploaded_bytes), last_36_months=False
        )
        current_sleeves, current_correlations = estimate_from_price_csv(
            BytesIO(uploaded_bytes), last_36_months=use_last_36
        )
    except (UnicodeDecodeError, ValueError) as error:
        st.error(f"Could not read prices.csv: {error}")
        st.stop()
    source_label = "CSV inputs on all months"
    estimate_signature = f"{sha256(uploaded_bytes).hexdigest()}:{use_last_36}"

asset_names = list(current_sleeves)
default_reserves = default_reserve_assets(asset_names)
estimates_changed = st.session_state.get("_estimate_signature") != estimate_signature
if estimates_changed:
    st.session_state["_estimate_signature"] = estimate_signature

st.subheader("Expected-return estimates")
edited_sleeves = {name: values.copy() for name, values in current_sleeves.items()}
return_columns = st.columns(min(len(asset_names), 4))
for index, name in enumerate(asset_names):
    with return_columns[index % len(return_columns)]:
        return_key = f"return_{name}"
        if estimates_changed or return_key not in st.session_state:
            st.session_state[return_key] = (
                current_sleeves[name]["expected_return"] * 100
            )
        edited_sleeves[name]["expected_return"] = st.number_input(
            name,
            step=0.1,
            format="%.2f",
            key=return_key,
        ) / 100

st.subheader("Reserve eligibility")
reserve_columns = st.columns(min(len(asset_names), 4))
selected_reserves = set()
for index, name in enumerate(asset_names):
    with reserve_columns[index % len(reserve_columns)]:
        if st.checkbox(
            name,
            value=name in default_reserves,
            key=f"reserve_{name}",
        ):
            selected_reserves.add(name)

current_result = search_lowest_risk_mix(
    edited_sleeves,
    current_correlations,
    objective_return=objective,
    reserve_minimum=reserve_minimum,
    reserve_eligible=selected_reserves,
)
loaded_result = search_lowest_risk_mix(
    loaded_sleeves,
    loaded_correlations,
    objective_return=objective,
    reserve_minimum=reserve_minimum,
    reserve_eligible=selected_reserves,
)

st.divider()
current_column, loaded_column = st.columns(2)
with current_column:
    st.subheader("Lowest-risk mix")
    show_mix(current_result)
with loaded_column:
    st.subheader(f"As loaded — {source_label}")
    show_mix(loaded_result)

if current_result is not None and loaded_result is not None:
    largest_change = max(
        abs(current_result["weights"][name] - loaded_result["weights"][name])
        for name in asset_names
    )
    st.metric("Largest weight change", f"{largest_change * 100:.0f} points")
