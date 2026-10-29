# Lab 17 – Point-in-Time Audit

## D – The Question

Was each number in the selected series knowable on the day I would have traded on it, and may Project 2 use it?

The point-in-time test separates an observation's measurement date from the date when the value became available. This prevents a backtest from using later publications or revisions.

**Selected rate:** DGS10 (10-Year Treasury Yield).

DGS10 is relevant to Walmart because Treasury yields influence the risk-free rate used in estimating its cost of capital. Higher yields can increase the discount rate and reduce the present value of forecast cash flows.

**Sample partner reason (not an actual conversation):** DGS10 provides a market-based reference for the long-term risk-free rate, so it can materially affect the discount rate used to value Walmart.

## R – The Data

The app uses live data from the Federal Reserve Bank of St. Louis. FRED supplies each series as it appears today, while ALFRED supplies the historical vintage available on a selected date. The default series are BAA, FEDFUNDS, DGS10, and MORTGAGE30US; another valid FRED series ID can be entered in the sidebar.

| Series | Measure | Frequency | Source |
|---|---|---|---|
| BAA | Moody's Baa corporate bond yield | Monthly | [FRED](https://fred.stlouisfed.org/series/BAA) |
| FEDFUNDS | Effective federal funds rate | Monthly | [FRED](https://fred.stlouisfed.org/series/FEDFUNDS) |
| DGS10 | 10-year Treasury yield | Daily | [FRED](https://fred.stlouisfed.org/series/DGS10) |
| MORTGAGE30US | 30-year fixed mortgage rate | Weekly | [FRED](https://fred.stlouisfed.org/series/MORTGAGE30US) |

## I – The App

The Streamlit application is available in [`asof_app.py`](asof_app.py). It downloads current values from FRED and point-in-time values from ALFRED in separate functions and caches each result for one hour. The sidebar controls the selected series, optional additional series ID, chart start date, and as-known-on date.

For each series, the app charts current values from the selected start date and reports the last observation available in the selected ALFRED vintage. The comparison table shows the last value known then, the latest value today, the number of later observations, and the number of overlapping observations whose values changed. An invalid or unavailable series produces an error for that series without stopping the rest of the page.

## V – Known-Answer Validation

### Test 1: October 5, 2026

With **As known on** set to October 5, 2026, all four results matched the instructor's expected values.

| Series | Last observation known then | Value | Result |
|---|---|---:|---|
| BAA | September 1, 2026 | 6.47 | Match |
| FEDFUNDS | September 1, 2026 | 3.75 | Match |
| DGS10 | October 2, 2026 | 5.28 | Match |
| MORTGAGE30US | October 1, 2026 | 7.28 | Match |

### Test 2: PAYEMS on January 15, 2025

For PAYEMS, the last observation available as of January 15, 2025 was December 1, 2024, with a value of **159,536**. Compared with the current series, the app reported **381 revised observations** on shared dates and **21 additional observations** after the historical endpoint. These results confirm that the point-in-time download is not simply reading current FRED data twice.

The latest current PAYEMS observation, **159,044 in September 2026**, is a different observation and should not be confused with the revised December 2024 value.

## E – Your Series

### DGS10 Data Card

| Field | Entry |
|---|---|
| Series ID and name | DGS10 – 10-Year Treasury Constant Maturity Rate |
| Source | Board of Governors of the Federal Reserve System, H.15 Selected Interest Rates, via [FRED](https://fred.stlouisfed.org/series/DGS10) |
| What it measures | The market yield on U.S. Treasury securities at a 10-year constant maturity, interpolated from the daily Treasury yield curve and quoted on an investment basis |
| Units | Percent, not seasonally adjusted |
| Frequency | Daily on business days |
| Publication lag | The H.15 release is posted Monday through Friday at 4:15 p.m. An observation normally appears in the next business day's release, subject to holidays and Federal Reserve closures. |
| Revision behavior | FRED states that the data are subject to revision. In these two app tests, no overlapping historical observations were revised. |
| Download date | October 29, 2026 |

DGS10 is relevant to Walmart because the 10-year Treasury yield is a long-term risk-free-rate reference in the cost of equity and a baseline for borrowing costs. A higher DGS10 can increase Walmart's estimated cost of capital and discount rate, reducing the present value of forecast cash flows if other assumptions remain unchanged.

### Point-in-Time Comparison

| As-known-on date | Latest known observation | Value | Additional observations in today's data | Revised observations |
|---|---|---:|---:|---:|
| September 30, 2026 | September 29, 2026 | 5.26% | 19 | 0 |
| October 29, 2026 | October 27, 2026 | 4.99% | 0 | 0 |

After September 30, 19 new dated observations became available in today's data. None of the historical observations appearing in both datasets changed value. The 5.26% and 4.99% figures belong to different observation dates, so their difference is a movement in the rate rather than a revision to the September 29 observation.

### Three Historical Observation Checks

These values were independently corroborated using FRED-derived historical data and then verified directly against the [official FRED CSV](https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=2026-09-25&coed=2026-09-29) on October 29, 2026.

| Observation date | Reported value | Official FRED CSV check |
|---|---:|---|
| September 25, 2026 | 5.17% | Match |
| September 28, 2026 | 5.24% | Match |
| September 29, 2026 | 5.26% | Match |

## V – Fresh Eyes and Partner Attack

### Code Explanation

The historical download function retrieves ALFRED data using a selected vintage date. The app then compares the historical observations with current FRED data to determine which observations were available and whether values changed.

| Code step | Explanation |
|---|---|
| `@st.cache_data(ttl=3600, show_spinner=False)` | Caches the downloaded result for one hour so the same request is not repeated on every Streamlit rerun. |
| `def download_as_known_values(series_id, vintage_date):` | Accepts a FRED series ID and the date representing what was known then. |
| `series_id = normalize_series_id(series_id)` | Removes extra spaces, converts the ID to uppercase, and rejects unsupported characters. |
| `vintage_date = date.fromisoformat(str(vintage_date)).isoformat()` | Checks that the selected date is valid and formats it as `YYYY-MM-DD`. |
| `query = urlencode({"id": series_id, "vintage_date": vintage_date})` | Safely builds the URL parameters for the series and vintage date. |
| `return _read_fred_csv(f"{ALFRED_GRAPH_URL}?{query}")` | Sends the ALFRED URL to the shared CSV reader, which downloads, cleans, sorts, and returns the historical observations. |

### Sample Partner Attack

The following is a sample attack, not an actual completed partner exchange.

**Sample Partner Question:** How can we confirm that DGS10 values were available on the decision date and were not revised afterward?

**Sample Least-Trusted Field:** Publication lag, because the observation date does not necessarily indicate when the data became available to investors.

**Sample Response:** The September 30, 2026 test showed that the latest available DGS10 observation was September 29 at 5.26%. The application identified 19 additional observations and zero revisions when compared with October 29.

## E – Project 2 Decision

**Decision: ADMIT DGS10.**

**Reason:** DGS10 is relevant to Walmart's valuation, and the application found no revisions among the overlapping historical observations tested.

**Point-in-Time Rule:** Only use observations that were available by the decision date, retrieved from the appropriate ALFRED vintage. Respect the publication lag.

**Condition:** Reconsider the decision if additional testing identifies revisions, publication delays, or missing observations that could affect the analysis.

## Reflection

DGS10 has a publication lag, meaning an observation may not be available on its measurement date. My September 30, 2026 test showed that September 29 was the latest available observation at 5.26%. The application identified 19 additional observations and zero revisions among overlapping values. Using today's dataset in a historical backtest could introduce information that investors did not have at the time, resulting in look-ahead bias.
