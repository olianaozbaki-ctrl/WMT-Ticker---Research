# Phase 2 Data

- `raw/yahoo_{ticker}.json` preserves the downloaded daily Yahoo Finance chart response for BIL, IEF, LQD, and VT.
- `prices_monthly.csv` contains 61 aligned calendar-month-end adjusted closes in USD from 2021-10-29 through 2026-10-30.
- `cpi_snapshot.csv` preserves the current FRED CPIAUCSL snapshot used for the provisional September 2026 year-over-year calculation. October 2025 is blank because it was not published.
- `market_data_provenance.json` separately records the market observation boundary, preserved source-retrieval date/precision, current processing timestamp, provider URLs, units, adjustment definition, missingness, transformations, CPI availability dates, and the unverified ALFRED-vintage status.

These are real downloaded observations, not synthetic fixtures. Synthetic data appear only in known-answer tests.
