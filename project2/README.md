# Meridian Foundation Investment Management Application

**AI use:** OpenAI Codex assisted with Phases 1–4A architecture, implementation, tests, data-pipeline design, decision-support research, and documentation. The student owns the analysis and investment decision.

**Educational project only; not investment advice.**

## Decision and intended user

This application supports the Meridian Foundation CIO and investment committee in deciding whether to reject, pilot, or adopt a constrained ETF allocation process. It compares two baselines with a provisional constrained minimum-volatility portfolio and supplies a Phase 4A evidence-gated decision framework; it does **not** make the student's final investment judgment. See the [official Project 2 brief](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/projects/project-2-investment-management-application.md).

## Run from a clean checkout

Requires Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/generate_phase2_results.py
PYTHONPATH=src python -m streamlit run app.py --server.fileWatcherType poll
```

Run the command from the `project2/` directory using the same `python` environment in which the requirements were installed. The `PYTHONPATH=src` prefix makes the local `project2_engine` package importable without relying on a prior editable install.

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
- CPI decision-date input: BLS archived August 2026 CPI-U, not seasonally adjusted, 334.980 (observation 2026-08-01) versus August 2025 323.976 (2025-08-01), released 2026-09-11. The October 5, 2026 CPI + 4% hurdle is 7.3965%. This is contemporaneous BLS release evidence, not an ALFRED API vintage or seasonally adjusted CPIAUCSL.
- Point-in-time signal: DGS10 at 5.28% for October 2, 2026, available October 5, 2026, evaluated as known on October 5. These dates/value come from the documented Lab 17 ALFRED validation. The signal is a review trigger only and does not automatically change portfolio weights.

## Executed Phase 2 result

| Portfolio | Weights (BIL / IEF / LQD / VT) | Expected return | Volatility | Reserve |
|---|---|---:|---:|---:|
| Equal weight | 25% / 25% / 25% / 25% | 3.01% | 7.55% | 25% |
| 60/40 benchmark | 0% / 0% / 40% / 60% | 6.26% | 12.33% | 0% |
| Provisional constrained minimum volatility | 48% / 0% / 0% / 52% | 7.50% | 7.82% | 48% |

These figures are generated in [outputs/phase2_results.md](outputs/phase2_results.md). Historical expected return is an estimate, not a forecast or promise.

## Repository map

- `app.py` — Streamlit comparison and individual rule verdicts.
- `config/mandate.json` — exact S1–S10 policy plus separately labeled modeling assumptions.
- `data/raw/` — preserved Yahoo responses.
- `data/prices_monthly.csv` — aligned adjusted-price panel.
- `data/market_data_provenance.json` — source, dates, units, adjustment, missingness, and transformations.
- `src/project2_engine/` — calculations, loaders, optimizer, mandate checker, stress analysis, and decision support.
- `scripts/` — reproducible data refresh and visible-output generation.
- `tests/` — known-answer, integrity, feasible/infeasible optimizer, baseline, and rule-verdict tests.
- `outputs/` — code-generated Phase 2/3B and Phase 4A JSON and Markdown results.

## Known limitations and approvals needed

- No actual Meridian holdings or holdings as-of date were supplied. Displayed turnover and costs are explicitly illustrative from a hypothetical equal-weight start; the mandate turnover verdict remains `NOT_TESTABLE`.
- If hypothetical equal weight were treated as the starting portfolio, enforcing the 25% turnover cap makes the provisional return hurdle infeasible. This is a sensitivity stop condition, not an actual-holdings verdict.
- No independent evidence establishes five-business-day liquidation and settlement for the ETFs. Liquidity remains `NOT_TESTABLE`.
- The 10 bps one-way cost is illustrative, not observed Meridian execution evidence.
- The point-in-time CPI pair is documented from the contemporaneous BLS August 2026 release; no ALFRED API vintage is archived. The current CPIAUCSL snapshot remains preserved as legacy data and is not used in the October 5 calculation.
- The 1% grid solution is discrete and sensitive to historical expected-return estimates.
- ETF issuer exposure, the diversified-fund exemption, and look-through treatment are unverified; issuer compliance remains `NOT_TESTABLE`.
- S9 remains `UNRESOLVED`; no loss guarantee is claimed.
- Phase 3B adds reproducible allocation stresses and an interactive comparison. Final recommendation, allocation ranges, monitoring triggers, clean-user cold run, and Locked Changed-Input Record remain deferred. The reserved changed-input scenario has not been run.

## Phase 3B stress testing

The code-generated stress matrix is included in `outputs/phase2_results.json` and `outputs/phase2_results.md`. It covers expected-return shifts of ±2 percentage points, the full decision-date-aligned historical window and 36 monthly returns, 0/10/25 bps one-way costs, a 10% reserve floor and hypothetical 25% turnover cap, 25% higher volatility, PSD-preserving correlation stress, and available/unavailable DGS10 cases. The Streamlit section compares equal weight, the 60/40 benchmark, and the reoptimized portfolio for selected scenarios.

The DGS10 decision date is 2026-10-05 (observation 2026-10-02; available 2026-10-05). All market-return calculations stop at 2026-09-30, the latest month-end observation available by the decision date (59 monthly returns); the 2026-10-30 price observation is excluded from portfolio baselines, optimization, stress tests, and decision support. DGS10 is a historical review-only signal, not a current quote.

Corrected aligned-window reoptimization: 48% BIL / 52% VT, 7.5017% gross and 7.4517% net expected annual return, 7.8242% annual volatility. The 36-month case selects 80% BIL / 20% VT, 7.5422% gross / 7.4872% net, and 2.3730% volatility. All baseline and scenario portfolio metrics and mandate verdicts are in the output files. The hypothetical 25% turnover cap produces `STOP_INFEASIBLE`; no constraint is relaxed. Turnover and transaction costs use an explicitly hypothetical equal-weight start, not actual Meridian holdings. Optimizer feasibility is provisional and is not full mandate compliance.

Correlation stress blends the historical correlation matrix 50% with a valid four-asset equicorrelation matrix (off-diagonal 0.75) and retains original volatilities. This convex blend preserves PSD; covariance validation remains enabled. Stress outcomes are historical-sample sensitivity results, not forecasts or observed market shocks.

## Phase 4A investment decision support

The application and [generated decision report](outputs/phase4a_decision_support.md) provide an evidence-gated framework for `APPROVE`, `CONDITIONAL_PILOT`, `HOLD`, or `REJECT`. The candidate disposition is **HOLD funded deployment** for student/committee review, not a final investment judgment. The tested model-feasible allocation envelope is BIL 21–80%, IEF 0%, LQD 0%, VT 20–79%; it is explicitly **not an authorization range**. Full-window versus 36-month optimization changes BIL from 48% to 80% (32 percentage points), and the mandate defines no tolerance for this variation.

The initial Phase 3B calculation used September 2026 CPI, released after the 2026-10-05 decision date. That look-ahead error is retained as validation history in `docs/validation-and-ai-use.md`. The corrected run uses the August 2026 BLS archived release, filters every ETF-price calculation through 2026-09-30, and retains the DGS10 observation dated 2026-10-02 and available 2026-10-05. The optimized allocation is 48% BIL / 52% VT; the 36-month result is 80% BIL / 20% VT. The remaining 32 percentage-point BIL window difference and unresolved mandate evidence support a HOLD for review, not an authorized allocation.

The 90%/five-business-day liquidity test, 8% issuer interpretation and exposure, actual holdings/turnover, observed costs, and S9 breach handling remain unresolved or unverified. Public fund pages publish holdings and trading indicators, but those do not establish portfolio-specific five-day sale and settlement capacity at Meridian's trade size. No funded pilot is supported by the current evidence; paper-only rehearsal may be considered separately.
