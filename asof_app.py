"""Show current and point-in-time FRED interest-rate observations."""

from datetime import date
from io import StringIO
import re
from urllib.parse import urlencode

import certifi
import pandas as pd
import requests
import streamlit as st


SERIES_NAMES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year mortgage rate",
}
DEFAULT_SERIES = list(SERIES_NAMES)
FRED_GRAPH_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"
ALFRED_GRAPH_URL = "https://alfred.stlouisfed.org/graph/alfredgraph.csv"
SERIES_ID_PATTERN = re.compile(r"^[A-Z0-9_.-]+$")


def _read_fred_csv(url):
    """Make one HTTP request and normalize a FRED/ALFRED graph CSV."""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "FIN43900-learning-app/1.0"},
            timeout=30,
            verify=certifi.where(),
        )
        response.raise_for_status()
    except requests.exceptions.SSLError as error:
        raise ValueError(
            "SSL certificate verification failed while using the certifi CA bundle; "
            "update certifi or install this Python's macOS certificates"
        ) from error
    except requests.exceptions.Timeout as error:
        raise ValueError("download timed out") from error
    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else "unknown"
        raise ValueError(f"download returned HTTP {status}") from error
    except requests.exceptions.RequestException as error:
        raise ValueError(f"download failed: {error}") from error

    try:
        raw = pd.read_csv(StringIO(response.content.decode("utf-8-sig")), na_values=["."])
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as error:
        raise ValueError("download was not a valid FRED CSV") from error

    if raw.shape[1] < 2:
        raise ValueError("download did not contain a date and value column")

    dates = pd.to_datetime(raw.iloc[:, 0], errors="coerce")
    values = pd.to_numeric(raw.iloc[:, 1], errors="coerce")
    frame = pd.DataFrame({"date": dates, "value": values}).dropna(subset=["date"])
    if frame.empty:
        raise ValueError("download contained no valid observation dates")

    return (
        frame.drop_duplicates(subset="date", keep="last")
        .sort_values("date")
        .reset_index(drop=True)
    )


def normalize_series_id(series_id):
    """Return a safe, normalized FRED series ID or raise ValueError."""
    normalized = series_id.strip().upper()
    if not normalized or not SERIES_ID_PATTERN.fullmatch(normalized):
        raise ValueError("use only letters, numbers, periods, underscores, or hyphens")
    return normalized


@st.cache_data(ttl=3600, show_spinner=False)
def download_current_values(series_id):
    """Download the series as FRED reports it today."""
    series_id = normalize_series_id(series_id)
    url = f"{FRED_GRAPH_URL}?{urlencode({'id': series_id})}"
    return _read_fred_csv(url)


@st.cache_data(ttl=3600, show_spinner=False)
def download_as_known_values(series_id, vintage_date):
    """Download the ALFRED vintage that was available on vintage_date."""
    series_id = normalize_series_id(series_id)
    vintage_date = date.fromisoformat(str(vintage_date)).isoformat()
    query = urlencode({"id": series_id, "vintage_date": vintage_date})
    return _read_fred_csv(f"{ALFRED_GRAPH_URL}?{query}")


def last_observation(frame):
    """Return the last nonmissing observation as (date, value), or None."""
    available = frame.dropna(subset=["value"])
    if available.empty:
        return None
    row = available.iloc[-1]
    return row["date"], float(row["value"])


def compare_vintages(current, as_known):
    """Count observations added after the vintage endpoint and later revisions."""
    known_last = last_observation(as_known)
    if known_last is None:
        return int(current["value"].notna().sum()), 0

    last_known_date = known_last[0]
    later_count = int(
        ((current["date"] > last_known_date) & current["value"].notna()).sum()
    )

    paired = current.merge(as_known, on="date", how="inner", suffixes=("_today", "_then"))
    paired = paired.dropna(subset=["value_today", "value_then"])
    revised_count = int(
        ((paired["value_today"] - paired["value_then"]).abs() > 1e-12).sum()
    )
    return later_count, revised_count


def format_date(timestamp):
    """Format a pandas timestamp for display."""
    return timestamp.strftime("%Y-%m-%d")


def format_value(value):
    """Format a value without discarding meaningful precision."""
    return f"{value:,.6f}".rstrip("0").rstrip(".")


def main():
    """Render the Streamlit application."""
    st.set_page_config(page_title="FRED Point-in-Time Rates", layout="wide")
    st.title("FRED Point-in-Time Rates")
    st.caption(
        "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, "
        f"downloaded {date.today().isoformat()}; built with AI help, a learning "
        "demonstration, not investment advice."
    )

    selected = st.sidebar.multiselect(
        "Series",
        options=DEFAULT_SERIES,
        default=DEFAULT_SERIES,
        format_func=lambda series_id: f"{series_id} — {SERIES_NAMES[series_id]}",
    )
    other_series = st.sidebar.text_input("Add another FRED series ID").strip()
    start_date = st.sidebar.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.sidebar.date_input(
        "As known on",
        value=date.today(),
        max_value=date.today(),
    )

    series_ids = list(selected)
    if other_series:
        candidate = other_series.upper()
        if candidate not in series_ids:
            series_ids.append(candidate)

    if not series_ids:
        st.info("Select a series or enter another FRED series ID.")
        return

    summary_rows = []
    for series_id in series_ids:
        display_name = SERIES_NAMES.get(series_id, series_id)
        st.subheader(f"{series_id} — {display_name}")

        try:
            safe_id = normalize_series_id(series_id)
            with st.spinner(f"Downloading {safe_id} from FRED and ALFRED..."):
                current = download_current_values(safe_id)
                as_known = download_as_known_values(
                    safe_id, as_known_on.isoformat()
                )
        except ValueError as error:
            st.error(f"Could not load {series_id}: {error}")
            continue

        chart_data = current.loc[
            (current["date"].dt.date >= start_date) & current["value"].notna(),
            ["date", "value"],
        ].set_index("date")
        if chart_data.empty:
            st.warning(
                f"No current observations are available on or after {start_date}."
            )
        else:
            st.line_chart(chart_data, y="value", x_label="Date", y_label="Value")

        known_last = last_observation(as_known)
        current_last = last_observation(current)
        if known_last is None:
            st.write(f"No observation was available as known on **{as_known_on}**.")
        else:
            st.write(
                f"Last observation known on **{as_known_on}**: "
                f"**{format_date(known_last[0])} — "
                f"{format_value(known_last[1])}**"
            )

        later_count, revised_count = compare_vintages(current, as_known)
        summary_rows.append(
            {
                "Series": f"https://fred.stlouisfed.org/series/{safe_id}",
                "ID": safe_id,
                "Last date known then": (
                    format_date(known_last[0]) if known_last else "Unavailable"
                ),
                "Value known then": (
                    format_value(known_last[1]) if known_last else "Unavailable"
                ),
                "Last date today": (
                    format_date(current_last[0]) if current_last else "Unavailable"
                ),
                "Value today": (
                    format_value(current_last[1]) if current_last else "Unavailable"
                ),
                "Values added afterward": later_count,
                "Values revised since": revised_count,
            }
        )

    st.divider()
    st.subheader("Point-in-time comparison")
    if summary_rows:
        st.dataframe(
            pd.DataFrame(summary_rows),
            hide_index=True,
            use_container_width=True,
            column_config={
                "Series": st.column_config.LinkColumn(
                    "FRED page", display_text="Open series"
                )
            },
        )
    else:
        st.warning("No selected series could be loaded.")


if __name__ == "__main__":
    main()
