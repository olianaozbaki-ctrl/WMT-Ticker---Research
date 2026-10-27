"""Apply a point-in-time provenance gate to a monthly data table."""

from datetime import date


# Editable inputs ------------------------------------------------------------

DECISION_DATE = "2026-03-31"

TABLE = [
    {"row": 1, "ticker": "AAA", "month": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3, "ticker": "AAA", "month": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4, "ticker": "AAA", "month": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5, "ticker": "BBB", "month": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7, "ticker": "BBB", "month": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8, "ticker": "BBB", "month": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9, "ticker": "CCC", "month": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "", "month": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month": "2026-02", "published_on": "2026-03-10", "index": 111.0},
]


def parse_date(value):
    """Convert an ISO date string to a date."""
    return date.fromisoformat(value)


def row_numbers(rows):
    """Format removed row numbers for the funnel."""
    return ", ".join(str(row["row"]) for row in rows) or "none"


def remove_missing_tickers(rows):
    """Rule 1: quarantine rows whose ticker is blank."""
    removed = [row for row in rows if not row["ticker"].strip()]
    kept = [row for row in rows if row["ticker"].strip()]
    return kept, removed


def remove_exact_duplicates(rows):
    """Rule 2: keep the first row when all data fields match exactly."""
    seen = set()
    kept = []
    removed = []

    for row in rows:
        signature = (
            row["ticker"],
            row["month"],
            row["published_on"],
            row["index"],
        )
        if signature in seen:
            removed.append(row)
        else:
            seen.add(signature)
            kept.append(row)

    return kept, removed


def remove_late_publications(rows, decision_date):
    """Rule 3: exclude information published after the decision date."""
    cutoff = parse_date(decision_date)
    removed = [row for row in rows if parse_date(row["published_on"]) > cutoff]
    kept = [row for row in rows if parse_date(row["published_on"]) <= cutoff]
    return kept, removed


def keep_latest_vintages(rows):
    """Rule 4: keep the latest publication for each ticker and month."""
    latest = {}
    removed = []

    for row in rows:
        key = (row["ticker"], row["month"])
        prior = latest.get(key)
        if prior is None or parse_date(row["published_on"]) > parse_date(
            prior["published_on"]
        ):
            if prior is not None:
                removed.append(prior)
            latest[key] = row
        else:
            removed.append(row)

    kept = sorted(latest.values(), key=lambda row: row["row"])
    removed.sort(key=lambda row: row["row"])
    return kept, removed


def build_latest_panel(rows):
    """Create a panel using the latest publication regardless of its date."""
    valid_rows, _ = remove_missing_tickers(rows)
    unique_rows, _ = remove_exact_duplicates(valid_rows)
    panel, _ = keep_latest_vintages(unique_rows)
    return panel


def calculate_signals(panel):
    """Calculate each ticker's latest month-over-month percentage change."""
    by_ticker = {}
    for row in panel:
        by_ticker.setdefault(row["ticker"], []).append(row)

    signals = {}
    for ticker, rows in by_ticker.items():
        ordered = sorted(rows, key=lambda row: row["month"])
        if len(ordered) < 2:
            signals[ticker] = None
            continue
        previous, latest = ordered[-2:]
        percent_change = (latest["index"] / previous["index"] - 1) * 100
        signals[ticker] = (latest["month"], percent_change)
    return signals


def print_funnel(steps, panel):
    print(f"ROW FUNNEL (decision date: {DECISION_DATE})")
    for label, removed in steps:
        print(f"{label}: removed {len(removed)} row(s) [{row_numbers(removed)}]")
    print(f"As-of panel: {len(panel)} row(s) [{row_numbers(panel)}]")


def print_panel(panel):
    print("\nAS-OF PANEL")
    print("Row  Ticker  Month    Published on  Index")
    for row in panel:
        print(
            f"{row['row']:>3}  {row['ticker']:<6}  {row['month']}  "
            f"{row['published_on']}    {row['index']:.1f}"
        )


def print_signals(title, signals):
    print(f"\n{title}")
    for ticker in sorted(signals):
        signal = signals[ticker]
        if signal is None:
            print(f"{ticker}: unavailable (fewer than two months)")
        else:
            month, percent_change = signal
            month_name = date.fromisoformat(f"{month}-01").strftime("%B %Y")
            print(f"{ticker}: {percent_change:+.2f}% ({month_name})")


def main():
    current = TABLE
    steps = []

    current, removed = remove_missing_tickers(current)
    steps.append(("1. Quarantined: no ticker", removed))

    current, removed = remove_exact_duplicates(current)
    steps.append(("2. Exact duplicate", removed))

    current, removed = remove_late_publications(current, DECISION_DATE)
    steps.append((f"3. Published after {DECISION_DATE}", removed))

    asof_panel, removed = keep_latest_vintages(current)
    steps.append(("4. Older vintage replaced by revision", removed))

    naive_panel = build_latest_panel(TABLE)

    print_funnel(steps, asof_panel)
    print_panel(asof_panel)
    print_signals("AS-OF SIGNALS", calculate_signals(asof_panel))
    print_signals(
        "NAIVE SIGNALS (publication date ignored)",
        calculate_signals(naive_panel),
    )


if __name__ == "__main__":
    main()
