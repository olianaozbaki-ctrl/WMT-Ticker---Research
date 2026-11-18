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

## Phase 3A — DGS10 signal

The point-in-time signal uses the Lab 17 documented ALFRED check: DGS10 observation 2026-10-02, availability 2026-10-05, value 5.28%, evaluated for decision date 2026-10-05. The prior verified row is September 29 at 5.26%, available September 30. Source: Board of Governors H.15 via FRED/ALFRED; units are percent, not seasonally adjusted. `data/dgs10_pit.csv` preserves only those documented rows. The loader filters by both observation and availability date and returns unavailable when no eligible observation exists.

Signal interpretation and process effect are modeling assumptions: treat the yield as a descriptive macro regime review trigger, not a return forecast; it prompts a review of rates-sensitive valuation and approved stress scenarios but does not automatically tilt allocations. No CPI/portfolio outputs are changed by the signal. This date-specific educational fixture is not a live current quote.

## Phase 4A — investment decision support and AI-output checks

The generated decision-support artifacts are `outputs/phase4a_decision_support.json` and `outputs/phase4a_decision_support.md`; reproduce them and the Phase 2/3B outputs with `python scripts/generate_phase2_results.py`. `app.py` displays the decision framework, portfolio/window comparison, diagnostic allocation envelope, evidence gates, monitoring triggers, and approval questions. Its current candidate disposition is **HOLD funded deployment**, for the student's review; it is not a final investment judgment.

### Result interpretation and range

In the point-in-time-aligned stress output, the full-window reoptimization is 44% BIL / 56% VT, while the 36-month reoptimization is 78% BIL / 22% VT. BIL shifts 34 percentage points; annual volatility is 8.4154% versus 2.6057%, respectively. Across all model-feasible reoptimized stress cases, the envelope is BIL 17–78%, IEF 0%, LQD 0%, VT 22–83%. It is **not** an approved or robust range: the window dispersion is large, there is no committee-approved tolerance for stability, and actual turnover, liquidity, costs, issuer treatment, and S9 are unresolved.

### Point-in-time CPI finding

Phase 3B aligned monthly equity/bond return endpoints and the DGS10 fixture to October 5, 2026, but it passed a September 2026 CPI value into the return hurdle. Project provenance records that CPI observation as available October 14; the BLS archived release confirms September CPI was embargoed until October 14, 2026 at 8:30 a.m. ET. Thus the numerical `PROVISIONAL_FEASIBLE` stress label means only that the supplied grid constraints were satisfied; it does not establish point-in-time feasibility on October 5. The ALFRED API supports querying observations by `vintage_dates` or real-time period, but no matching vintage is present locally. We do not backfill or infer an August-vintage value. The historical stress feasibility and candidate ranges remain diagnostics pending a correct vintage rerun. Sources: [BLS archived release](https://www.bls.gov/news.release/archives/cpi_10142026.htm), [FRED observations/vintage API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html), [FRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html).

### Diligence evidence review

- **ETF liquidity (S8):** The [SEC Rule 6c-11 guide](https://www.sec.gov/investment/exchange-traded-funds-small-entity-compliance-guide) describes public prior-day holdings, NAV/market and premium/discount information, and 30-day median bid-ask spread disclosures. Official provider pages publish trading/holdings information for [BIL](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil), [IEF](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf), [LQD](https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf), and [VT](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf). Those fields are diligence evidence, not proof that 90% of a $100 million portfolio exposure can be sold and settled within five business days at its actual order size. No dated order-size liquidation study is loaded; liquidity stays `NOT_TESTABLE`.
- **Issuer exemptions (S6):** The accessible `Lab_13.md` says “No single issuer can account for more than 8%” and states no exemption. Configuration includes cash, Treasury, and diversified-fund exemptions as an unconfirmed modeling interpretation. SEC-required ETF holdings disclosure can enable a look-through analysis, but neither the policy interpretation nor dated issuer aggregation is verified. S6 remains `NOT_TESTABLE` pending CIO confirmation and holdings evidence.
- **CPI vintage (S2):** The project stores a current FRED snapshot with September 2026 available October 14 and no ALFRED vintage date. BLS's [2026 release schedule](https://www.bls.gov/schedule/2026/home.htm) also shows August CPI released September 11, before the October 5 decision; however, the local file lacks the prior-year August observation and no vintage pair is verified. No replacement inflation rate is reported.
- **S9:** The client-authored `Lab_13.md` describes the >10% annual-loss goal as an unverifiable promise without breach measurement or handling. No external source can decide this client policy. It remains `UNRESOLVED`; -10% is a human-review alert only, not an automatic stop or guarantee.

### Phase 3B correlation-stress failure and correction

The initial AI-assisted correlation stress multiplied each historical pairwise correlation by 1.25 and clipped values independently. Pairwise-valid values do not ensure a positive-semidefinite matrix; the existing covariance validator rejected the resulting covariance and the test suite exposed the error. That first method was rejected. The corrected stress forms a 50% convex combination of the original valid correlation matrix and a valid four-asset equicorrelation matrix (off-diagonal 0.75), then restores the original volatilities. A convex combination of PSD matrices is PSD. Covariance symmetry/PSD validation remains enabled; regression tests check the stressed covariance and verify a deliberately invalid covariance is still rejected. This preserves the failed AI output, the validation evidence, and the reason for accepting the correction.

The Locked Changed-Input Record has **not** been executed, and its reserved scenario result is not included here. This work does not alter previous labs or Project 1.

### Phase 4A regression suite

Command: `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`. Final Phase 4A run: **50 tests passed, 0 failed, 0 skipped** in 32.300 seconds. This includes all prior Phase 1–3B tests plus decision-support tests for the four decision outcomes, CPI look-ahead stop, window/range dispersion, evidence/trigger reporting, and generated artifacts. The Phase 3B result now also has a regression test proving the CPI hurdle is explicitly marked invalid at the October 5 decision date. The headless Streamlit application test passes.

## Phase 3B — stress matrix and current verification

The current Phase 3B implementation supersedes the earlier Phase 2 statement that no stress matrix had been run. Results are generated directly by `python scripts/generate_phase2_results.py` and stored in both `outputs/phase2_results.json` and `outputs/phase2_results.md`. The Streamlit stress section compares equal weight, 60/40, and reoptimized allocations with weights, gross/net expected annual return, annual volatility, hypothetical turnover, cost, optimizer status, and individual rule verdicts.

The signal fixture is historical, not live. Its decision date is 2026-10-05; stresses use monthly return endpoints no later than the decision date (through 2026-09-30, 59 returns). The signal observation is 2026-10-02, available 2026-10-05. Full-panel Phase 2 results remain through 2026-10-30 and are not used as the market boundary for these signal-linked stress runs.

### Executed stress outcomes

- Aligned-window baseline: 44% BIL / 56% VT; gross annual expected return 7.7974%, net 7.7474%, volatility 8.4154%; 50% one-way turnover from the hypothetical equal-weight start and 0.05% cost at illustrative 10 bps.
- The 36-return window selects 78% BIL / 22% VT; gross return 7.8598%, net 7.8068%, volatility 2.6057%; turnover 53%, cost 0.053%.
- Parallel expected-return shifts of -2 pp and +2 pp produce 17%/83% and 71%/29% BIL/VT, respectively; output files show the metrics and rules for each portfolio.
- At 0, 10 and 25 bps, reoptimized allocations are 45%/55%, 44%/56% and 43%/57% BIL/VT; costs are 0%, 0.05% and 0.125% of NAV.
- Raising the reserve floor to 10% leaves the selected 44%/56% allocation unchanged. A hypothetical 25% turnover cap returns `STOP_INFEASIBLE`; no constraint is weakened.
- Scaling volatilities by 1.25 raises aligned-baseline volatility to 10.5193%. Correlations are stressed by a 50% convex blend with a valid equicorrelation matrix (off-diagonal 0.75), retaining the original volatilities; resulting portfolio volatility is 8.4682%. Covariance validation remains active, and regression tests reject a non-PSD matrix.
- Signal-available and signal-unavailable cases return the same allocations because DGS10 is a review-only modeling trigger and does not automatically tilt weights.

Every scenario also evaluates the equal-weight and 60/40 reference portfolios. Optimizer feasibility is reported separately from rule verdicts and is never called full mandate compliance. Turnover and costs are sensitivity estimates from hypothetical equal-weight holdings. Actual holdings, ETF liquidity, CPI vintage, issuer exemptions/look-through exposure and S9 evidence remain unavailable or unresolved. These historical-sample sensitivities are not forecasts or independently verified shocks.

### Regression suite

Command: `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`. Phase 3B verification: **44 tests passed, 0 failed, 0 skipped**. It includes all earlier Phase 1/2/3A tests, the headless Streamlit test, stress scenario and three-portfolio comparisons, the hypothetical turnover stop, point-in-time boundary alignment, PSD-preserving correlation stress, and rejection of invalid covariance. The prior 32-test run did not cover all discovered test modules; the current explicit `test*.py` discovery runs all 44.
