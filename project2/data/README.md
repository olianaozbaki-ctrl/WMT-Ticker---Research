# Phase 2 Data

- `raw/yahoo_{ticker}.json` preserves the downloaded daily Yahoo Finance chart response for BIL, IEF, LQD, and VT.
- `prices_monthly.csv` contains 61 aligned calendar-month-end adjusted closes in USD from 2021-10-29 through 2026-10-30.
- `cpi_snapshot.csv` preserves the later FRED CPIAUCSL snapshot involved in the original look-ahead error; the Phase 2 historical decision run does not use it.
- `cpi_pit_2026-10-05.csv` and its JSON provenance preserve the BLS-reported August 2025 and August 2026 CPI-U index levels (not seasonally adjusted), available in the archived August release on September 11, 2026. This is BLS release evidence, not an ALFRED API vintage.
- `market_data_provenance.json` records the source snapshot metadata. The analysis applies the October 5, 2026 decision boundary before estimating returns; market observations end September 30, 2026.

These are real downloaded observations, not synthetic fixtures. Synthetic data appear only in known-answer tests.
