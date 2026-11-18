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

The human-authored pre-run prediction was committed before execution in `1fd3c8ba1895424dcea5a0c1eb76f4934f09f346`. It remains exactly as committed in the Pre-Run Record of `docs/locked-changed-input-record.md`; Codex did not draft or reconstruct it after the run.

The locked script `scripts/run_locked_test.sh` changed only `objective.real_return_spread` from 0.04 to 0.05 for the reserved run, generated the reports, copied the evidence, and restored the tracked configuration and normal output files. The preserved baseline and changed-input SHA-256 manifests both verify. The artifact timestamps show baseline preservation at 11:58:43 PM EST, changed-input report generation at 11:58:58 PM EST, and completion of the changed-input checksum evidence at 11:59:03 PM EST on November 17, 2026. They do not prove an exact command-start timestamp. The script's repository path resolution was made portable after the run; the locked outputs were not regenerated or modified.

The locked artifacts are preserved without modification under `outputs/locked-changed-input-test-1fd3c8b/`. Numerical comparison of the saved JSON confirms the hurdle changed from 7.3965478924% to 8.3965478924%; the selected weights changed from 48% BIL / 52% VT to 35% BIL / 65% VT; after-cost expected return changed from 7.4516786376% to 8.4127459731%; and annualized volatility changed from 7.8242283789% to 9.7460880081%. The disposition stayed HOLD, full mandate feasibility stayed false, and the hypothetical 25% turnover-constrained optimization stayed infeasible.

Codex assisted only with post-run evidence reconciliation, documentation, diagnosis, and the reporting-label correction after the locked execution. The saved changed-input artifacts exposed that numerical calculations used 5% while generated labels still said CPI + 4%. Configuration-derived labels now use `objective.real_return_spread`; quoted original client wording remains CPI + 4% where explicitly identified as original policy. Regression tests cover 4%, 5%, and fractional-spread formatting plus mandate and decision-report propagation. The active `config/mandate.json` remains at 0.04.

Completion validation on November 18, 2026 used `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`: **58 tests passed in 49.729 seconds; 0 failed; 0 skipped; OK.** Both locked artifact checksum manifests were also reverified after the reporting correction, and the normal active-configuration reports were regenerated without rerunning the locked changed-input script.

## Mandate finalization update — 2026-11-17

Codex assisted with reconciling eight user-approved Project 2 modeling decisions against `Lab_13.md`, updating the machine-readable configuration, and extending deterministic configuration tests. No portfolio optimization, stress result, recommendation, or Locked Changed-Input run was performed.

## Corrected point-in-time CPI and decision-date market inputs — 2026-11-17

The preceding Phase 3B/Phase 4A run used September 2026 CPI for a historical decision dated October 5, even though September CPI was not released until October 14. That was a genuine look-ahead error. The incorrect run, the test that exposed the mismatch, and the correction are retained here as validation and AI-use evidence; generated portfolio results below and in `outputs/` use the corrected inputs.

- Authoritative source: BLS archived [August 2026 CPI release](https://www.bls.gov/news.release/archives/cpi_09112026.htm), published September 11, 2026. Table 1 reports CPI-U not seasonally adjusted at 323.976 for August 2025 and 334.980 for August 2026 (1982-84=100). Both observations were available by the October 5 decision. This is direct point-in-time BLS release evidence, not a claim that an ALFRED API vintage was retrieved.
- Corrected year-over-year inflation: `334.980 / 323.976 - 1 = 3.3965478924%`. The project’s arithmetic CPI + 4% convention gives a 7.3965478924% target. CPI seasonal adjustment is not specified by S2; using BLS NSA CPI-U is a modeling choice that should be reviewed.
- The price panel used for *all* baseline, optimizer, stress, and decision-support results is filtered through September 30, 2026, the last month-end observation before October 5. It contains 60 month-end prices and 59 monthly returns. October 30 prices remain in the preserved source panel but are excluded from these decision-date estimates. DGS10 uses observation October 2, available October 5. The common boundary is October 5 decision date, with market return data no later than September 30 and signal observation/availability no later than October 5.
- Corrected portfolios: equal weight estimates 3.0128% return / 7.5482% volatility; 60% VT / 40% LQD estimates 6.2591% / 12.3335%; minimum-volatility optimizer selects 48% BIL / 52% VT with 7.5017% gross return, 7.4517% net after the illustrative 10 bps one-way transaction charge, and 7.8242% volatility. All are historical/model outputs, not forecasts or verified full mandate compliance.
- Stress outcomes: full-window optimizer is 48% BIL / 52% VT (7.5017% gross return, 7.8242% volatility); 36-month is 80% BIL / 20% VT (7.5422%, 2.3730%). BIL changes 32 percentage points. Across feasible reoptimized stresses, the diagnostic envelope is BIL 21–80%, IEF 0%, LQD 0%, VT 20–79%. Hypothetical equal-weight starting holdings under a 25% turnover cap remain `STOP_INFEASIBLE`; this says nothing about actual Meridian holdings.
- Precision check: exhaustive 1% grid 48% BIL / 52% VT, net return 7.4517%, volatility 7.8242%; exhaustive 0.5% grid 48.5% / 51.5%, net 7.4147%, volatility 7.7503%; continuous SLSQP 48.7457% / 51.2543%, net 7.3965%, volatility 7.7140%. The maximum production-grid weight difference is 0.7457 percentage points and volatility gap 0.1102 points. Solver is successful; this is retained as numerical comparison evidence, not proof of financial robustness.
- CPI source/measurement choice aside, actual holdings, position-sized ETF liquidity, issuer exemptions and look-through, actual transaction costs, and S9 remain unresolved or unverified. Issuer is `NOT_TESTABLE`, never PASS. Candidate disposition remains HOLD for student/committee review and is not a final decision.

The result generator writes the corresponding JSON and Markdown directly from the engine. The previous September CPI snapshots remain preserved as historical evidence but are not inputs to the corrected October 5 analysis.

## Phase 2 implementation and validation — original run (historical record; superseded for October 5 decision analysis)

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

## Phase 4A — investment decision support and AI-output checks (corrected numbers below)

The generated decision-support artifacts are `outputs/phase4a_decision_support.json` and `outputs/phase4a_decision_support.md`; reproduce them and the Phase 2/3B outputs with `python scripts/generate_phase2_results.py`. `app.py` displays the decision framework, portfolio/window comparison, diagnostic allocation envelope, evidence gates, monitoring triggers, and approval questions. Its current candidate disposition is **HOLD funded deployment**, for the student's review; it is not a final investment judgment.

### Result interpretation and range

The numbers in this initial Phase 4A report were generated before the CPI and common-boundary correction and are retained only as an audit trail. The current numbers are in “Corrected point-in-time CPI and decision-date market inputs” above and in regenerated output files.

### Point-in-time CPI finding

The prior CPI look-ahead issue and its correction are documented above. The subsequent correction uses the BLS archived release and retains BLS versus ALFRED provenance distinction.

### Diligence evidence review

- **ETF liquidity (S8):** The [SEC Rule 6c-11 guide](https://www.sec.gov/investment/exchange-traded-funds-small-entity-compliance-guide) describes public prior-day holdings, NAV/market and premium/discount information, and 30-day median bid-ask spread disclosures. Official provider pages publish trading/holdings information for [BIL](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil), [IEF](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf), [LQD](https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf), and [VT](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf). Those fields are diligence evidence, not proof that 90% of a $100 million portfolio exposure can be sold and settled within five business days at its actual order size. No dated order-size liquidation study is loaded; liquidity stays `NOT_TESTABLE`.
- **Issuer exemptions (S6):** The accessible `Lab_13.md` says “No single issuer can account for more than 8%” and states no exemption. Configuration includes cash, Treasury, and diversified-fund exemptions as an unconfirmed modeling interpretation. SEC-required ETF holdings disclosure can enable a look-through analysis, but neither the policy interpretation nor dated issuer aggregation is verified. S6 remains `NOT_TESTABLE` pending CIO confirmation and holdings evidence.
- **CPI vintage (S2):** The original run's September 2026 input was look-ahead. Corrected analysis uses the BLS August 2026 archived release for both August year-over-year observations; no ALFRED API vintage is claimed. The BLS-versus-ALFRED and seasonal-adjustment conventions remain review items.
- **S9:** The client-authored `Lab_13.md` describes the >10% annual-loss goal as an unverifiable promise without breach measurement or handling. No external source can decide this client policy. It remains `UNRESOLVED`; -10% is a human-review alert only, not an automatic stop or guarantee.

### Phase 3B correlation-stress failure and correction

The initial AI-assisted correlation stress multiplied each historical pairwise correlation by 1.25 and clipped values independently. Pairwise-valid values do not ensure a positive-semidefinite matrix; the existing covariance validator rejected the resulting covariance and the test suite exposed the error. That first method was rejected. The corrected stress forms a 50% convex combination of the original valid correlation matrix and a valid four-asset equicorrelation matrix (off-diagonal 0.75), then restores the original volatilities. A convex combination of PSD matrices is PSD. Covariance symmetry/PSD validation remains enabled; regression tests check the stressed covariance and verify a deliberately invalid covariance is still rejected. This preserves the failed AI output, the validation evidence, and the reason for accepting the correction.

The later Locked Changed-Input run is documented above and in `docs/locked-changed-input-record.md`. Its reserved artifacts remain separate from the normal generated outputs. This work does not alter previous labs or Project 1.

### Earlier CPI error and correction audit trail

The initial Phase 3B/4A result used September 2026 CPI for the October 5 decision, despite the October 14 release date. During this correction, the BLS August release was verified: it publishes the August 2025 and August 2026 CPI-U observations in Table 1, with release date September 11, before the decision boundary. The model now uses those exact published values and validates the vintage and availability dates in a regression test. It also applies the decision boundary before the estimate step for all portfolio calculations. A second change replaced a precision-test cutoff of 0.5 percentage points with a 1.0-point bound matching the production grid step; the actual gap is 0.7457 points and the volatility difference is separately checked. This records both the original AI-assisted mistake and the test-driven correction rather than presenting only the corrected result.

The corrected CPI target uses unadjusted CPI-U because S2 specifies CPI but does not specify seasonal adjustment. The user/committee should decide whether that convention is acceptable or require the archived ALFRED CPIAUCSL series. This unresolved measurement choice limits the result's policy interpretation.

### Final corrected regression run

Command: `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`.

Result: **55 passed, 0 failed, 0 skipped**. Coverage includes point-in-time CPI source/value/availability enforcement, future market-price exclusion, DGS10 boundary handling, portfolio calculations, feasible and infeasible optimization, stress/covariance validation, mandate verdicts, decision support, and the headless Streamlit application.

### Phase 4A regression suite

Command: `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`. The 50-test Phase 4A run above is historical. The corrected full-suite run and count are recorded in the final “Corrected point-in-time CPI” audit trail after validation.

## Phase 3B — stress matrix and current verification

The current Phase 3B implementation supersedes the earlier Phase 2 statement that no stress matrix had been run. Results are generated directly by `python scripts/generate_phase2_results.py` and stored in both `outputs/phase2_results.json` and `outputs/phase2_results.md`. The Streamlit stress section compares equal weight, 60/40, and reoptimized allocations with weights, gross/net expected annual return, annual volatility, hypothetical turnover, cost, optimizer status, and individual rule verdicts.

The signal fixture is historical, not live. Its decision date is 2026-10-05; current results use monthly return endpoints through 2026-09-30 (59 returns). The signal observation is 2026-10-02, available 2026-10-05. October 30 prices are excluded from portfolio, stress, and decision-support calculations.

### Executed stress outcomes

- Corrected aligned-window baseline: 48% BIL / 52% VT; gross annual expected return 7.5017%, net 7.4517%, volatility 7.8242%; 50% one-way turnover from the hypothetical equal-weight start and 0.05% cost at illustrative 10 bps.
- The 36-return window selects 80% BIL / 20% VT; gross return 7.5422%, net 7.4872%, volatility 2.3730%; turnover 55%, cost 0.055%.
- Parallel expected-return shifts of -2 pp and +2 pp produce 21%/79% and 75%/25% BIL/VT, respectively; output files show the metrics and rules for each portfolio.
- At 0, 10 and 25 bps, the generated output records the corrected reoptimized allocations and costs for each; see `outputs/phase2_results.md` and `.json`.
- Raising the reserve floor to 10% leaves the selected 48%/52% allocation unchanged. A hypothetical 25% turnover cap returns `STOP_INFEASIBLE`; no constraint is weakened.
- Scaling volatilities by 1.25 raises corrected aligned-baseline volatility to 9.7803%. The PSD-preserving correlation stress gives 7.8817% volatility for the optimized portfolio. Covariance validation remains active, and regression tests reject a non-PSD matrix.
- Signal-available and signal-unavailable cases return the same allocations because DGS10 is a review-only modeling trigger and does not automatically tilt weights.

Every scenario also evaluates the equal-weight and 60/40 reference portfolios. Optimizer feasibility is reported separately from rule verdicts and is never called full mandate compliance. Turnover and costs are sensitivity estimates from hypothetical equal-weight holdings. Actual holdings, ETF liquidity, CPI vintage, issuer exemptions/look-through exposure and S9 evidence remain unavailable or unresolved. These historical-sample sensitivities are not forecasts or independently verified shocks.

### Regression suite

Command: `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`. Phase 3B verification: **44 tests passed, 0 failed, 0 skipped**. It includes all earlier Phase 1/2/3A tests, the headless Streamlit test, stress scenario and three-portfolio comparisons, the hypothetical turnover stop, point-in-time boundary alignment, PSD-preserving correlation stress, and rejection of invalid covariance. The prior 32-test run did not cover all discovered test modules; the current explicit `test*.py` discovery runs all 44.
