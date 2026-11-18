"""Download and preserve the dated Phase 2 market-data inputs.

Run from project2/: ``python scripts/fetch_market_data.py``.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
TICKERS = ("BIL", "IEF", "LQD", "VT")
PERIOD1 = 1633046400  # 2021-10-01 00:00:00 UTC
PERIOD2 = 1793491200  # 2026-11-01 00:00:00 UTC, exclusive
YAHOO_TEMPLATE = (
    "https://query2.finance.yahoo.com/v8/finance/chart/{ticker}"
    f"?period1={PERIOD1}&period2={PERIOD2}&interval=1d"
    "&events=div%2Csplits&includeAdjustedClose=true"
)
FRED_URL = (
    "https://fred.stlouisfed.org/graph/fredgraph.csv"
    "?id=CPIAUCSL&cosd=2025-09-01&coed=2026-09-01"
)


def _get(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    refresh = "--refresh" in sys.argv[1:]
    process_timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    provenance_path = DATA / "market_data_provenance.json"
    existing_provenance = (
        json.loads(provenance_path.read_text(encoding="utf-8"))
        if provenance_path.exists()
        else {}
    )
    prior_source_timestamp = existing_provenance.get(
        "source_retrieved_at_utc", existing_provenance.get("retrieval_date")
    )
    downloaded_source = False
    monthly_by_ticker: dict[str, dict[str, tuple[str, float]]] = {}
    ticker_audit: dict[str, dict[str, object]] = {}

    for ticker in TICKERS:
        url = YAHOO_TEMPLATE.format(ticker=ticker)
        raw_path = RAW / f"yahoo_{ticker}.json"
        if refresh or not raw_path.exists():
            payload = _get(url)
            raw_path.write_bytes(payload)
            downloaded_source = True
        else:
            payload = raw_path.read_bytes()
        chart = json.loads(payload)["chart"]
        if chart.get("error") or not chart.get("result"):
            raise RuntimeError(f"Yahoo returned no result for {ticker}: {chart.get('error')}")
        result = chart["result"][0]
        timestamps = result["timestamp"]
        adjusted = result["indicators"]["adjclose"][0]["adjclose"]
        if len(timestamps) != len(adjusted):
            raise RuntimeError(f"timestamp/value length mismatch for {ticker}")

        monthly: dict[str, tuple[str, float]] = {}
        missing = 0
        valid_dates: list[str] = []
        for stamp, value in zip(timestamps, adjusted):
            observation = datetime.fromtimestamp(stamp, tz=timezone.utc).date().isoformat()
            if value is None:
                missing += 1
                continue
            valid_dates.append(observation)
            monthly[observation[:7]] = (observation, float(value))
        monthly_by_ticker[ticker] = monthly
        ticker_audit[ticker] = {
            "source_url": url,
            "currency": result["meta"].get("currency"),
            "exchange": result["meta"].get("fullExchangeName"),
            "raw_rows": len(timestamps),
            "raw_missing_adjusted_close": missing,
            "first_daily_observation": valid_dates[0],
            "last_daily_observation": valid_dates[-1],
            "monthly_observations_before_alignment": len(monthly),
        }

    common_months = sorted(set.intersection(*(set(values) for values in monthly_by_ticker.values())))
    if len(common_months) < 61:
        raise RuntimeError(f"expected at least 61 common monthly prices, found {len(common_months)}")
    common_months = common_months[-61:]

    output_rows = []
    for month in common_months:
        dates = {monthly_by_ticker[ticker][month][0] for ticker in TICKERS}
        if len(dates) != 1:
            raise RuntimeError(f"month-end dates do not align for {month}: {sorted(dates)}")
        row = {"observation_date": dates.pop()}
        row.update(
            {
                ticker: f"{monthly_by_ticker[ticker][month][1]:.6f}"
                for ticker in TICKERS
            }
        )
        output_rows.append(row)

    with (DATA / "prices_monthly.csv").open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=("observation_date", *TICKERS))
        writer.writeheader()
        writer.writerows(output_rows)

    cpi_path = DATA / "cpi_snapshot.csv"
    if refresh or not cpi_path.exists():
        cpi_payload = _get(FRED_URL)
        cpi_path.write_bytes(cpi_payload)
        downloaded_source = True
    else:
        cpi_payload = cpi_path.read_bytes()
    source_timestamp = (
        process_timestamp if downloaded_source else prior_source_timestamp
    )
    if source_timestamp is None:
        raise RuntimeError(
            "cached source files lack retrieval metadata; rerun with --refresh"
        )
    source_retrieval_date = source_timestamp[:10]
    source_timestamp_precision = (
        "second"
        if downloaded_source
        else existing_provenance.get(
            "source_retrieval_timestamp_precision", "date_only_legacy_snapshot"
        )
    )
    provenance = {
        "retrieval_date": source_retrieval_date,
        "source_retrieved_at_utc": source_timestamp,
        "source_retrieval_timestamp_precision": source_timestamp_precision,
        "processed_at_utc": process_timestamp,
        "price_data": {
            "provider": "Yahoo Finance chart endpoint",
            "provider_adjustment_definition": "Adjusted close includes applicable splits and dividend distributions.",
            "provider_definition_url": "https://help.yahoo.com/kb/SLN28256.html",
            "units": "USD per ETF share, back-adjusted by provider",
            "requested_interval": "daily",
            "transformation": "Select the last nonmissing adjusted close in each calendar month, intersect months across all tickers, retain the latest 61 prices to produce 60 simple monthly returns.",
            "aligned_rows": len(output_rows),
            "first_observation": output_rows[0]["observation_date"],
            "as_of_date": output_rows[-1]["observation_date"],
            "aligned_missing_values": 0,
            "tickers": ticker_audit,
        },
        "cpi_data": {
            "series": "CPIAUCSL",
            "provider": "FRED, source U.S. Bureau of Labor Statistics",
            "source_url": FRED_URL,
            "units": "Index 1982-1984=100, seasonally adjusted",
            "current_observation_date": "2026-09-01",
            "current_availability_date": "2026-10-14",
            "prior_year_observation_date": "2025-09-01",
            "prior_year_availability_date": "2025-10-24",
            "decision_date": process_timestamp[:10],
            "vintage_date": None,
            "alfred_vintage_verified": False,
            "status": "Provisional current FRED snapshot; not verified against an ALFRED vintage.",
            "missing_data_note": "October 2026 cannot be compared year over year because BLS did not publish the October 2025 all-items index.",
            "release_sources": [
                "https://www.bls.gov/news.release/archives/cpi_10142026.htm",
                "https://www.bls.gov/schedule/2025/10_sched.htm",
                "https://www.bls.gov/bls/news-release/cpi.htm",
            ],
        },
    }
    provenance_path.write_text(
        json.dumps(provenance, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Wrote {len(output_rows)} aligned monthly prices through "
        f"{output_rows[-1]['observation_date']} for {', '.join(TICKERS)}."
    )


if __name__ == "__main__":
    main()
