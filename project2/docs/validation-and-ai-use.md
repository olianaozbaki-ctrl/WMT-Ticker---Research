# Validation and AI Use — Working Record

**AI use:** OpenAI Codex was used on 2026-11-17 for Phase 1 architecture, Python implementation, documentation, and deterministic test scaffolding. Its suggestions are subject to student review and financial validation. The analysis and investment decision remain the student's responsibility.

**Educational project only; not investment advice.**

## Phase 1 validation scope

The deterministic tests use synthetic, explicitly constructed inputs with known answers. They validate formulas and rule behavior; they are not Meridian investment results and do not validate the market data, forecasts, signal, or final recommendation.

Tests cover:

- weight totals;
- weighted expected return;
- covariance-based volatility;
- one-way turnover;
- basis-point transaction costs;
- rule-level mandate pass, fail, not-testable, and unresolved outcomes;
- conservative feasibility when required evidence is missing.

## Evidence status after Phase 2

- No clean-user cold run has been performed.
- Visible executed Phase 2 output exists in `outputs/phase2_results.md` and `outputs/phase2_results.json`; it is provisional and not a final recommendation.
- No external data values have been independently reverified for Project 2.
- No final recommendation or allocation range exists.
- No holdout, outcome analysis, or stress matrix has been run.

## Locked Changed-Input Record

**Not created in Phase 1.** The human-authored AI-off prediction must be written and committed before the selected changed-input run. It must not be drafted or reconstructed by AI after the run.

## Mandate finalization update — 2026-11-17

Codex assisted with reconciling eight user-approved Project 2 modeling decisions against `Lab_13.md`, updating the machine-readable configuration, and extending deterministic configuration tests. No portfolio optimization, stress result, recommendation, or Locked Changed-Input run was performed.

## Phase 2 implementation and validation — 2026-11-17

Codex assisted with the external-data pipeline, deterministic portfolio optimizer, Streamlit comparison, test suite, and generated output. The student must review and own every financial interpretation before Phase 3.

### Data evidence

- Yahoo Finance chart endpoint: daily adjusted close for BIL, IEF, LQD, and VT; raw JSON preserved.
- Retrieval date: 2026-11-17. Aligned observation window: 2021-10-29 through 2026-10-30.
- Transformation: last nonmissing adjusted close per calendar month; common-month intersection; latest 61 prices; 60 simple monthly returns.
- Missingness: zero raw adjusted-close nulls for each ticker and zero aligned nulls.
- FRED CPIAUCSL current snapshot: September 2025 324.245 and September 2026 336.298; year-over-year change 3.7173%.
- CPI availability evidence: September 2025 released 2025-10-24 and September 2026 released 2026-10-14. The analysis date is later than both.
- October 2026 year-over-year CPI is not computed because the October 2025 all-items index was not published.
- ALFRED vintage verification remains incomplete; the CPI proxy is provisional and is never labeled verified compliance.

Full field-level provenance is in `data/market_data_provenance.json`.

### Tests executed

Command: `PYTHONPATH=src python -m unittest discover -s tests -v`

Result: **35 tests passed in 3.934 seconds; 0 failed; 0 skipped; OK.** Coverage includes the headless Streamlit app, formulas, mandate configuration, data completeness and missing-value rejection, generated retrieval metadata, output-path consistency, 60-return estimation, CPI missingness, feasible and infeasible optimization, turnover-boundary failure, baseline reconciliation, enforced optimizer constraints, precision evidence, and rule-level `NOT_TESTABLE`/`UNRESOLVED` handling.

### Executed result and disposition

`python scripts/generate_phase2_results.py` generated three portfolios in `outputs/phase2_results.json` and `outputs/phase2_results.md`. The model produced 40% BIL / 60% VT as the lowest-volatility 1% grid mix meeting the provisional after-cost hurdle. It is **not** reported as verified mandate-feasible because actual holdings, independent liquidity and issuer evidence, and ALFRED vintage verification are missing.

### Turnover stop condition

Actual Meridian holdings remain unavailable, so actual turnover is `NOT_TESTABLE`. As an explicitly hypothetical sensitivity, treating equal weight as the starting portfolio and enforcing the 25% turnover cap produces no feasible 1% grid portfolio. The highest net expected return within that hypothetical cap is 6.0614%, versus the provisional 7.7173% hurdle, a 1.6558 percentage-point shortfall. No constraint was relaxed.

### Optimizer precision check

The production exhaustive 1% grid was compared with an exhaustive 0.5% grid and SciPy SLSQP continuous variance minimization from four starting points using identical long-only, full-investment, reserve, provisional after-cost return, and illustrative-cost inputs.

- 1% grid: 40.0000% BIL / 60.0000% VT; net return 7.7449%; volatility 8.9550%.
- 0.5% grid: unchanged at 40.0000% BIL / 60.0000% VT.
- Continuous SLSQP: 40.4022% BIL / 59.5978% VT; net return 7.7173%; volatility 8.8958%.
- Maximum weight difference: 0.4022 percentage points.
- Volatility difference: 0.0591 percentage points.

The 1% grid is sufficiently accurate for Phase 2 comparison. The generated output preserves full-precision values, solver status, iteration count, grid counts, and constraint slack.

No stress run, allocation range, committee recommendation, or Locked Changed-Input Record was created in Phase 2.
