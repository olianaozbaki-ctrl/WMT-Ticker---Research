# Independent Validation Package — FIN 43900 Project 2

This package contains the numerical inputs, conventions, outputs, and evidence needed for an independent review of the Meridian Foundation analysis. It does not contain or simulate an independent reviewer's response. Decimal values are shown at sufficient precision to reproduce the reported results; `0.08` means 8%.

## 1. Original Meridian Foundation investment mandate

The authoritative client wording preserved in `config/mandate.json` is:

- **S1:** The portfolio has a seven-year investment horizon and needs to be rebalanced annually.
- **S2:** The foundation wants to earn a return of CPI + 4% annually after costs over rolling five-year periods.
- **S3:** The foundation needs enough cash or eligible government securities to cover twelve months of quarterly distributions.
- **S4:** The 60% equity and 40% bond benchmark provides a reference for comparing portfolio performance rather than a required allocation.
- **S5:** The portfolio cannot use borrowing, short selling, or derivatives.
- **S6:** No single issuer can account for more than 8% of the portfolio.
- **S7:** Annual turnover cannot exceed 25% without committee approval.
- **S8:** At least 90% of the portfolio must be redeemable within five business days.
- **S9:** The foundation wants to avoid annual losses greater than 10%, but this cannot be guaranteed and the CIO has not defined how a breach would be measured or handled.
- **S10:** The CIO has not specified what the portfolio should optimize, so more information is needed before selecting the best portfolio.

Project 2 uses a $100 million portfolio, four quarterly distributions of $0.75 million, and therefore a modeled reserve floor of $3 million / $100 million = 3%. The approved modeling objective—not original S10 policy—is minimum estimated annualized volatility subject to numerical feasibility. The asset universe is BIL (reserve/cash equivalent), IEF (Treasury bonds), LQD (investment-grade corporate bonds), and VT (global equity). The model is long-only, fully invested, and uses a 1% weight grid.

The 8% issuer exemptions recorded in configuration for cash, U.S. Treasury, and diversified funds are an unconfirmed case interpretation because the quoted S6 wording contains no exemptions. They are not treated as verified mandate compliance.

## 2. Financial formulas and calculation conventions

Let `w` be target weights, `μ` annual expected returns, `Σ` the annual covariance matrix, and `w0` the illustrative starting weights.

- Simple monthly return: `r[t] = price[t] / price[t-1] - 1`.
- Annual expected asset return: `μ[i] = 12 × arithmetic mean(monthly returns[i])`.
- Annual covariance: `Σ[i,j] = 12 × sample covariance(monthly returns[i], monthly returns[j])`, using denominator `n - 1`.
- Gross portfolio expected return: `R = w'μ = Σ w[i]μ[i]`.
- Portfolio variance: `V = w'Σw = Σ_i Σ_j w[i]w[j]Σ[i,j]`.
- Annualized volatility: `σ = sqrt(V)`.
- One-way turnover: `T = 0.5 × Σ |w[i] - w0[i]|`.
- One-rebalance trading cost: `C = T × cost_bps / 10,000`.
- Illustrative after-cost expected return: `R_net = R - C`.
- Year-over-year inflation: `π = CPI_current / CPI_prior - 1`.
- Arithmetic return hurdle: `H = π + configured real_return_spread`.

The illustrative starting allocation is `w0 = [0.25, 0.25, 0.25, 0.25]` in the order BIL, IEF, LQD, VT. The base trading-cost assumption is 10 bps. These are not actual Meridian holdings or observed trading costs.

The price data use monthly last observations of Yahoo Finance adjusted close. The October 5, 2026 decision boundary leaves 60 prices from 2021-10-29 through 2026-09-30 and 59 monthly returns. Expected returns are historical arithmetic estimates, not forecasts.

### Return-hurdle inputs

- CPI source: archived BLS August 2026 CPI-U, U.S. city average, not seasonally adjusted, Table 1.
- Prior index: 323.976 for 2025-08-01.
- Current index: 334.980 for 2026-08-01.
- Release/availability date for both values: 2026-09-11.
- Decision date: 2026-10-05.
- Inflation: `334.980 / 323.976 - 1 = 0.033965478924364856`.
- Active configured spread: `0.04`.
- Baseline hurdle: `0.033965478924364856 + 0.04 = 0.07396547892436486`.

This is contemporaneous BLS release evidence, not an archived ALFRED API response. The mandate does not specify seasonal adjustment; use of not-seasonally-adjusted CPI-U is a modeling choice.

## 3. Historical asset return estimates and covariance matrix

All values below are annual decimals estimated from the 59 aligned monthly returns.

| Asset | Annual expected return | Annual volatility |
|---|---:|---:|
| BIL | 0.036574092957393 | 0.004909125086091 |
| IEF | -0.017289318829315 | 0.077183603953953 |
| LQD | -0.009276409995894 | 0.098685579212193 |
| VT | 0.110502349532508 | 0.149240274841163 |

Annual covariance matrix, ordered BIL, IEF, LQD, VT:

|  | BIL | IEF | LQD | VT |
|---|---:|---:|---:|---:|
| **BIL** | 0.000024099509111 | 0.000079949482539 | 0.000135567750462 | 0.000187851122512 |
| **IEF** | 0.000079949482539 | 0.005957308719321 | 0.007120211533952 | 0.007320358348576 |
| **LQD** | 0.000135567750462 | 0.007120211533952 | 0.009738843544446 | 0.011740069564072 |
| **VT** | 0.000187851122512 | 0.007320358348576 | 0.011740069564072 | 0.022272659634666 |

## 4. Baseline portfolio allocations and results

All turnover and cost figures use the hypothetical equal-weight starting allocation and 10 bps cost.

| Portfolio | BIL | IEF | LQD | VT | Gross return | Turnover | Cost | Net return | Volatility | Verified full mandate feasible |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Equal weight | 0.25 | 0.25 | 0.25 | 0.25 | 0.030127678416173 | 0.00 | 0.00000 | 0.030127678416173 | 0.075482169670959 | No |
| 60/40 benchmark | 0.00 | 0.00 | 0.40 | 0.60 | 0.062590845721147 | 0.50 | 0.00050 | 0.062090845721147 | 0.123335338919329 | No |
| Constrained minimum volatility | 0.48 | 0.00 | 0.00 | 0.52 | 0.075016786376453 | 0.50 | 0.00050 | 0.074516786376453 | 0.078242283788695 | No |

Recalculation example for the optimized portfolio:

- Gross return: `0.48(0.036574092957393) + 0.52(0.110502349532508) = 0.075016786376453`.
- Turnover: `0.5 × (|0.48-0.25| + |0-0.25| + |0-0.25| + |0.52-0.25|) = 0.50`.
- Cost: `0.50 × 10 / 10,000 = 0.00050`.
- Net return: `0.075016786376453 - 0.00050 = 0.074516786376453`.
- Volatility: `sqrt(w'Σw) = 0.078242283788695` using the covariance matrix above.
- Hurdle slack: `0.074516786376453 - 0.073965478924365 = 0.000551307452088`, or about 5.51 bps.

The optimizer evaluated 176,851 grid combinations; 6,594 cleared the supported numerical constraints. “Provisional feasible” does not mean full mandate compliance.

## 5. Stress-test results

The reported row is the reoptimized minimum-volatility portfolio for each scenario. Weights are ordered BIL / IEF / LQD / VT.

| Scenario | Input change | Weights | Gross return | Net return | Volatility | Turnover | Cost | Status |
|---|---|---|---:|---:|---:|---:|---:|---|
| Baseline full window | 59 returns; 10 bps; 3% reserve | 0.48 / 0 / 0 / 0.52 | 0.075016786376453 | 0.074516786376453 | 0.078242283788695 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |
| Returns −2 pp | Subtract 0.02 from every asset return estimate | 0.21 / 0 / 0 / 0.79 | 0.074977415651734 | 0.074437415651734 | 0.118168348845180 | 0.54 | 0.00054 | PROVISIONAL_FEASIBLE |
| Returns +2 pp | Add 0.02 to every asset return estimate | 0.75 / 0 / 0 / 0.25 | 0.075056157101172 | 0.074556157101172 | 0.038419283855681 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |
| Last 36 months | Re-estimate returns and covariance from last 36 returns | 0.80 / 0 / 0 / 0.20 | 0.075422063715400 | 0.074872063715400 | 0.023730013378740 | 0.55 | 0.00055 | PROVISIONAL_FEASIBLE |
| Cost 0 bps | Set one-way cost to 0 bps | 0.49 / 0 / 0 / 0.51 | 0.074277503810702 | 0.074277503810702 | 0.076764529921999 | 0.50 | 0.00000 | PROVISIONAL_FEASIBLE |
| Cost 25 bps | Set one-way cost to 25 bps | 0.47 / 0 / 0 / 0.53 | 0.075756068942204 | 0.074506068942204 | 0.079720142386825 | 0.50 | 0.00125 | PROVISIONAL_FEASIBLE |
| Reserve minimum 10% | Raise BIL floor from 3% to 10% | 0.48 / 0 / 0 / 0.52 | 0.075016786376453 | 0.074516786376453 | 0.078242283788695 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |
| Turnover cap 25% | Enforce 25% cap from hypothetical equal weight | — | — | — | — | — | — | STOP_INFEASIBLE |
| Volatility +25% | Multiply each asset volatility by 1.25; covariance by 1.5625 | 0.48 / 0 / 0 / 0.52 | 0.075016786376453 | 0.074516786376453 | 0.097802854735869 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |
| Correlation stress | 50% convex blend of baseline correlations with four-asset equicorrelation 0.75 | 0.48 / 0 / 0 / 0.52 | 0.075016786376453 | 0.074516786376453 | 0.078816986660495 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |
| Signal available | DGS10 is review-only; no allocation tilt | 0.48 / 0 / 0 / 0.52 | 0.075016786376453 | 0.074516786376453 | 0.078242283788695 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |
| Signal unavailable | No automatic allocation tilt | 0.48 / 0 / 0 / 0.52 | 0.075016786376453 | 0.074516786376453 | 0.078242283788695 | 0.50 | 0.00050 | PROVISIONAL_FEASIBLE |

The 25% turnover-cap search found no grid portfolio that also met the return hurdle. The highest net return inside that hypothetical cap was `0.061825595506629` at weights BIL 0.25, IEF 0, LQD 0.25, VT 0.50, leaving a baseline shortfall of `0.012139883417736`.

The signal fixture is DGS10 at 5.28%, observation date 2026-10-02 and availability date 2026-10-05. Its approved role is review-only, so it does not change weights or return estimates.

### Additional numerical inputs for stress recalculation

The last-36-month annual expected returns are:

| BIL | IEF | LQD | VT |
|---:|---:|---:|---:|
| 0.043659700035992 | 0.030695485342755 | 0.048428351351312 | 0.202471518433034 |

Last-36-month annual covariance matrix:

|  | BIL | IEF | LQD | VT |
|---|---:|---:|---:|---:|
| **BIL** | 0.000004557491044 | 0.000023820928485 | 0.000039296793121 | 0.000036879903778 |
| **IEF** | 0.000023820928485 | 0.004435778304735 | 0.004874289322416 | 0.004293261912157 |
| **LQD** | 0.000039296793121 | 0.004874289322416 | 0.006119049104841 | 0.006298068356248 |
| **VT** | 0.000036879903778 | 0.004293261912157 | 0.006298068356248 | 0.013709879286958 |

Correlation-stress annual covariance matrix:

|  | BIL | IEF | LQD | VT |
|---|---:|---:|---:|---:|
| **BIL** | 0.000024099509111 | 0.000182063728671 | 0.000249456319936 | 0.000368665252660 |
| **IEF** | 0.000182063728671 | 0.005957308719321 | 0.006416446515181 | 0.007979767524533 |
| **LQD** | 0.000249456319936 | 0.006416446515181 | 0.009738843544446 | 0.011392983393719 |
| **VT** | 0.000368665252660 | 0.007979767524533 | 0.011392983393719 | 0.022272659634666 |

## 6. Locked Changed-Input test

The human-authored pre-run prediction was committed at `1fd3c8ba1895424dcea5a0c1eb76f4934f09f346`. The locked run changed only `objective.real_return_spread` from 0.04 to 0.05 and then restored the active configuration. The original artifacts remain under `outputs/locked-changed-input-test-1fd3c8b/`; their SHA-256 manifests verify.

| Measure | Baseline spread 0.04 | Changed spread 0.05 |
|---|---:|---:|
| Inflation | 0.033965478924365 | 0.033965478924365 |
| Return hurdle | 0.073965478924365 | 0.083965478924365 |
| Optimized weights, BIL / IEF / LQD / VT | 0.48 / 0 / 0 / 0.52 | 0.35 / 0 / 0 / 0.65 |
| Gross expected return | 0.075016786376453 | 0.084627459731218 |
| Illustrative turnover | 0.50 | 0.50 |
| Illustrative cost | 0.00050 | 0.00050 |
| After-cost expected return | 0.074516786376453 | 0.084127459731218 |
| Annualized volatility | 0.078242283788695 | 0.097460880081473 |
| Candidate disposition | HOLD | HOLD |
| Full mandate feasibility verified | No | No |
| Feasible with hypothetical 25% turnover cap | No | No |
| Maximum net return inside hypothetical cap | 0.061825595506629 | 0.061825595506629 |
| Shortfall inside hypothetical cap | 0.012139883417736 | 0.022139883417736 |

The higher hurdle shifted the grid solution toward VT and raised expected return and volatility, but it did not resolve missing mandate evidence. The locked changed-input reports display a stale “CPI + 4%” label beside the correctly calculated 8.3965% hurdle; this preserved defect is reporting evidence, not a numerical optimization failure. Later application and report generation code derives modeled labels from configuration. The locked artifacts themselves were not modified.

## 7. Candidate disposition and evidence

Candidate disposition: **HOLD funded deployment and do not authorize an allocation range yet.** Continue evidence collection; a paper-only rehearsal may be considered only if separately approved.

| Approval gate | Current state |
|---|---|
| Point-in-time CPI valid for decision date | Yes |
| Actual holdings and as-of date known | No |
| Five-business-day liquidity verified | No |
| Issuer policy interpretation and exposure verified | No |
| S9 measurement and handling approved | No |
| Full mandate feasibility verified | No |
| Stress range robust and committee-approved | No |

Supporting evidence for HOLD:

- The numerical optimizer is only provisionally feasible; liquidity, issuer exposure, and actual-turnover rules remain `NOT_TESTABLE`, while S9 remains `UNRESOLVED`.
- The hypothetical 25% turnover constraint is infeasible, but actual Meridian holdings are unavailable, so this is not an actual turnover verdict.
- Estimation-window sensitivity is material: BIL changes from 48% in the 59-return window to 80% in the 36-return window, a 32 percentage-point difference.
- The stress envelope is diagnostic, not an authorized allocation range.
- The baseline optimized net return clears the modeled hurdle by only about 5.51 bps.
- Historical mean returns are estimates, not forecasts or guaranteed rolling five-year outcomes.

## 8. Remaining financial limitations

- Actual Meridian holdings and their as-of date are unavailable; actual turnover and trading cost cannot be calculated.
- The 10 bps transaction-cost assumption and equal-weight starting portfolio are illustrative only.
- No dated, position-sized evidence proves that at least 90% of a $100 million portfolio can be sold and settled within five business days.
- S6 exemptions and ETF look-through/issuer aggregation treatment require CIO confirmation and dated holdings evidence.
- S9 lacks an approved measurement period, return definition, and breach response; it cannot be encoded as a hard rule or claimed as passed.
- The BLS point-in-time CPI release is verified, but no underlying ALFRED API vintage was archived, and the mandate does not resolve seasonal adjustment.
- The optimizer uses historical arithmetic means, annual sample covariance, and a discrete 1% grid. Results are sensitive to the estimation window.
- A single modeled rebalance cost is not proof of recurring annual after-cost performance.
- The application does not calculate a probability of achieving the rolling five-year objective.
- No full mandate compliance, approved allocation range, or final investment authorization is established.

## Reproduction references and implementation status

- Active results: `outputs/phase2_results.json` and `outputs/phase4a_decision_support.json`.
- Frozen prices: `data/prices_monthly.csv`.
- Point-in-time CPI: `data/cpi_pit_2026-10-05.csv` and its JSON provenance file.
- Mandate: `config/mandate.json`.
- Formula implementation: `src/project2_engine/calculations.py`.
- Stress definitions: `src/project2_engine/stress.py`.
- Locked evidence: `outputs/locked-changed-input-test-1fd3c8b/`.
- Previous implementation test result: **58 tests passed, 0 failed, 0 skipped**.
- Previous implementation commit: `d3ceae0101e58077f85eaf1127fe41fc9f4af753`.
