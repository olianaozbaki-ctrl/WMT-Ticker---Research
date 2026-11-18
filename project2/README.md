# Meridian Foundation Investment Management Application

**AI use:** OpenAI Codex assisted with Phase 1–2 architecture, implementation, tests, data-pipeline design, and documentation. The student owns the analysis and investment decision.

**Educational project only; not investment advice.**

## Decision and intended user

This application supports the Meridian Foundation CIO and investment committee in deciding whether to reject, pilot, or adopt a constrained ETF allocation process. Phase 2 compares two baselines with a provisional constrained minimum-volatility portfolio; it does **not** make the final committee recommendation.

## Run from a clean checkout

Requires Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/generate_phase2_results.py
python -m streamlit run app.py
```

The committed input snapshot reproduces the analysis offline. To refresh external data deliberately, run `python scripts/fetch_market_data.py --refresh`. Refreshing changes the evidence boundary and may change results; preserve and review the new raw responses and provenance.

## Phase 2 method

- Universe: BIL, IEF, LQD, and VT.
- Price source: Yahoo Finance chart endpoint, retrieved 2026-11-17.
- Price unit: USD adjusted close per ETF share; Yahoo states adjusted close incorporates applicable splits and distributions.
- Window: 61 aligned calendar-month-end prices from 2021-10-29 through 2026-10-30, producing 60 monthly simple returns.
- Missing values: zero in the raw adjusted-close fields and aligned panel.
- Estimates: monthly arithmetic mean × 12; sample monthly covariance × 12; portfolio volatility is the square root of annual portfolio variance.
- Equal-weight baseline: 25% each.
- 60/40 benchmark: 60% VT global equity and 40% LQD investment-grade bonds; BIL and IEF are 0%.
- Optimizer: deterministic 1%-weight grid, long-only, fully invested, BIL reserve at least 3%, and provisional CPI + 4% after illustrative trading cost. It never relaxes a supplied constraint.
- CPI signal: September 2026 CPIAUCSL divided by September 2025 CPIAUCSL minus one. October is not used because the October 2025 all-items CPI was not published.
- Point-in-time signal: DGS10 at 5.28% for October 2, 2026, available October 5, 2026, evaluated as known on October 5. These dates/value come from the documented Lab 17 ALFRED validation. The signal is a review trigger only and does not automatically change portfolio weights.

## Executed Phase 2 result

| Portfolio | Weights (BIL / IEF / LQD / VT) | Expected return | Volatility | Reserve |
|---|---|---:|---:|---:|
| Equal weight | 25% / 25% / 25% / 25% | 3.18% | 7.49% | 25% |
| 60/40 benchmark | 0% / 0% / 40% / 60% | 6.16% | 12.23% | 0% |
| Provisional constrained minimum volatility | 40% / 0% / 0% / 60% | 7.79% | 8.95% | 40% |

These figures are generated in [outputs/phase2_results.md](outputs/phase2_results.md). Historical expected return is an estimate, not a forecast or promise.

## Repository map

- `app.py` — Streamlit comparison and individual rule verdicts.
- `config/mandate.json` — exact S1–S10 policy plus separately labeled modeling assumptions.
- `data/raw/` — preserved Yahoo responses.
- `data/prices_monthly.csv` — aligned adjusted-price panel.
- `data/market_data_provenance.json` — source, dates, units, adjustment, missingness, and transformations.
- `src/project2_engine/` — calculations, loaders, optimizer, mandate checker, and Phase 2 orchestration.
- `scripts/` — reproducible data refresh and visible-output generation.
- `tests/` — known-answer, integrity, feasible/infeasible optimizer, baseline, and rule-verdict tests.
- `outputs/` — code-generated JSON and Markdown results.

## Known limitations and approvals needed

- No actual Meridian holdings or holdings as-of date were supplied. Displayed turnover and costs are explicitly illustrative from a hypothetical equal-weight start; the mandate turnover verdict remains `NOT_TESTABLE`.
- If hypothetical equal weight were treated as the starting portfolio, enforcing the 25% turnover cap makes the provisional return hurdle infeasible. This is a sensitivity stop condition, not an actual-holdings verdict.
- No independent evidence establishes five-business-day liquidation and settlement for the ETFs. Liquidity remains `NOT_TESTABLE`.
- The 10 bps one-way cost is illustrative, not observed Meridian execution evidence.
- The CPI values are a current FRED snapshot with documented release dates, but the required ALFRED vintage has not been verified.
- The 1% grid solution is discrete and sensitive to historical expected-return estimates.
- ETF issuer exposure, the diversified-fund exemption, and look-through treatment are unverified; issuer compliance remains `NOT_TESTABLE`.
- S9 remains `UNRESOLVED`; no loss guarantee is claimed.
- Allocation ranges, stress runs, final recommendation, monitoring triggers, cold run, and Locked Changed-Input Record are intentionally deferred beyond Phase 2.
