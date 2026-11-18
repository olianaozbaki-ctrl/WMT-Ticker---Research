# Phase 4A Investment Decision Support

Generated from the Phase 2/3B financial engine. This is candidate decision support for the student's review, not the final investment judgment.

- Evaluation date: **2026-11-18**
- Candidate disposition: **HOLD**
- Candidate action: HOLD funded deployment and do not authorize an allocation range yet; continue evidence collection and permit paper-only rehearsal if separately approved.

## Decision framework

| Outcome | Evidence gate |
|---|---|
| APPROVE | Only after every applicable hard rule has documented PASS evidence, point-in-time objective inputs are valid, actual-holdings turnover and costs are supportable, the committee accepts S10's optimization objective and S9 handling, and allocation ranges remain acceptable across approved stresses. |
| CONDITIONAL_PILOT | Only after hard legal/mandate constraints and point-in-time data gates are verified, with actual holdings, pilot size, duration, authority, monitoring cadence, and abort conditions approved in writing. A paper-only rehearsal may be considered while capital gates remain open. |
| HOLD | Use when material evidence or policy interpretation remains unknown, the estimate window produces material allocation dispersion, or feasibility depends on an inadmissible input. Do not authorize funded allocation. |
| REJECT | Use when a verified hard constraint is breached or no feasible portfolio exists under confirmed policy and evidence, with no approved remedy. A hypothetical-start infeasibility alone is not grounds to reject Meridian's actual portfolio. |

## Current approval gates

| Gate | Status |
|---|---|
| point in time cpi valid | PASS |
| actual holdings and asof known | NOT SATISFIED |
| five day liquidity verified | NOT SATISFIED |
| issuer policy and exposure verified | NOT SATISFIED |
| s9 handling approved | NOT SATISFIED |
| full mandate feasibility verified | NOT SATISFIED |
| stress range robust and approved | NOT SATISFIED |

## Decision-date and CPI check

The stress decision date is **2026-10-05**. The CPI inputs are 2025-08-01 and 2026-08-01, published 2026-09-11 and available by the decision date. BLS point-in-time source verified: **True** (this is not an ALFRED API vintage). Inflation is 3.3965%; the arithmetic CPI + 4% modeled hurdle is 7.3965%. The earlier September 2026 current-snapshot input was unavailable on October 5 and is retained in validation history as a corrected look-ahead error.

## Window sensitivity and model-only envelope

Full-window BIL allocation: 48.00%; 36-month BIL allocation: 80.00%; difference: 32.0 percentage points.

| Ticker | Minimum across modeled feasible stress solutions | Maximum |
|---|---:|---:|
| BIL | 21.00% | 80.00% |
| IEF | 0.00% | 0.00% |
| LQD | 0.00% | 0.00% |
| VT | 20.00% | 79.00% |

**Status: diagnostic only; not an authorization range.** The full-to-36-month shift, unresolved mandate evidence, and CPI measurement choice do not support a robust allocation band.

## Portfolio comparisons

Gross return uses annualized arithmetic historical estimates. Net return subtracts one modeled rebalance cost; it is not a recurring annual cost forecast or proof of the rolling five-year S2 objective. Turnover and costs use hypothetical equal-weight starting holdings, not actual Meridian holdings.

### baseline_full_window

| Portfolio | Weights (BIL / IEF / LQD / VT) | Gross return | Net return | Volatility | Turnover from hypothetical equal weight | Cost | Mandate verdicts |
|---|---|---:|---:|---:|---:|---:|---|
| Equal weight | 25.00% / 25.00% / 25.00% / 25.00% | 3.01% | 3.01% | 7.55% | 0.00% | 0.00% | weights_sum: PASS, long_only: PASS, no_borrowing: PASS, no_derivatives: PASS, reserve: PASS, liquidity: NOT_TESTABLE, issuer_limit: NOT_TESTABLE, turnover: NOT_TESTABLE, horizon: PASS, rebalance_frequency: PASS, return_objective_proxy: NOT_TESTABLE, calendar_year_loss: UNRESOLVED |
| 60/40 benchmark | 0.00% / 0.00% / 40.00% / 60.00% | 6.26% | 6.21% | 12.33% | 50.00% | 0.05% | weights_sum: PASS, long_only: PASS, no_borrowing: PASS, no_derivatives: PASS, reserve: FAIL, liquidity: NOT_TESTABLE, issuer_limit: NOT_TESTABLE, turnover: NOT_TESTABLE, horizon: PASS, rebalance_frequency: PASS, return_objective_proxy: NOT_TESTABLE, calendar_year_loss: UNRESOLVED |
| Reoptimized minimum volatility | 48.00% / 0.00% / 0.00% / 52.00% | 7.50% | 7.45% | 7.82% | 50.00% | 0.05% | weights_sum: PASS, long_only: PASS, no_borrowing: PASS, no_derivatives: PASS, reserve: PASS, liquidity: NOT_TESTABLE, issuer_limit: NOT_TESTABLE, turnover: NOT_TESTABLE, horizon: PASS, rebalance_frequency: PASS, return_objective_proxy: NOT_TESTABLE, calendar_year_loss: UNRESOLVED |
### last_36_months

| Portfolio | Weights (BIL / IEF / LQD / VT) | Gross return | Net return | Volatility | Turnover from hypothetical equal weight | Cost | Mandate verdicts |
|---|---|---:|---:|---:|---:|---:|---|
| Equal weight | 25.00% / 25.00% / 25.00% / 25.00% | 8.13% | 8.13% | 5.88% | 0.00% | 0.00% | weights_sum: PASS, long_only: PASS, no_borrowing: PASS, no_derivatives: PASS, reserve: PASS, liquidity: NOT_TESTABLE, issuer_limit: NOT_TESTABLE, turnover: NOT_TESTABLE, horizon: PASS, rebalance_frequency: PASS, return_objective_proxy: NOT_TESTABLE, calendar_year_loss: UNRESOLVED |
| 60/40 benchmark | 0.00% / 0.00% / 40.00% / 60.00% | 14.09% | 14.04% | 9.45% | 50.00% | 0.05% | weights_sum: PASS, long_only: PASS, no_borrowing: PASS, no_derivatives: PASS, reserve: FAIL, liquidity: NOT_TESTABLE, issuer_limit: NOT_TESTABLE, turnover: NOT_TESTABLE, horizon: PASS, rebalance_frequency: PASS, return_objective_proxy: NOT_TESTABLE, calendar_year_loss: UNRESOLVED |
| Reoptimized minimum volatility | 80.00% / 0.00% / 0.00% / 20.00% | 7.54% | 7.49% | 2.37% | 55.00% | 0.06% | weights_sum: PASS, long_only: PASS, no_borrowing: PASS, no_derivatives: PASS, reserve: PASS, liquidity: NOT_TESTABLE, issuer_limit: NOT_TESTABLE, turnover: NOT_TESTABLE, horizon: PASS, rebalance_frequency: PASS, return_objective_proxy: NOT_TESTABLE, calendar_year_loss: UNRESOLVED |

## Hypothetical turnover-cap stop

Status: **STOP_INFEASIBLE**; feasible: **False** under the 25.00% turnover cap from the explicitly hypothetical equal-weight start. Actual Meridian holdings are not inferred. Reason: no grid portfolio satisfies every supplied constraint.

## Evidence requirements

| Requirement | Status | Current evidence and remaining need |
|---|---|---|
| S8 five-business-day liquidity | NOT_VERIFIED | SEC Rule 6c-11 materials and fund-provider pages disclose prior-day holdings, market/NAV information, and/or 30-day median bid-ask spread. These are useful diligence inputs, not proof that the proposed portfolio's required 90% can be sold and settled within five business days at the intended trade size. Needed: Dated holdings and executable, position-sized liquidation/settlement analysis for each proposed allocation under normal-market conditions; confirm treatment of ETF secondary-market sale versus fund redemption. Sources: [SEC ETF Rule 6c-11 compliance guide](https://www.sec.gov/investment/exchange-traded-funds-small-entity-compliance-guide), [State Street BIL product data](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil), [iShares IEF product data](https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf), [iShares LQD product data](https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf), [Vanguard VT product data](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf) |
| S6 issuer cap and exemptions | POLICY_INTERPRETATION_AND_LOOKTHROUGH_UNVERIFIED | Lab_13.md says: No single issuer can account for more than 8% of the portfolio. The machine-readable project configuration carries case-exemption assumptions, but the quoted client rule does not state them. Public daily ETF holdings disclosures can support look-through aggregation; no dated constituents or CIO ruling is loaded in this project. Needed: CIO confirmation of exemptions and look-through method; dated underlying holdings and issuer aggregation if exemptions do not apply. Sources: [SEC ETF Rule 6c-11 compliance guide (daily holdings disclosure)](https://www.sec.gov/investment/exchange-traded-funds-small-entity-compliance-guide), [Lab_13.md S6 source](../../Lab_13.md) |
| S2 CPI + 4% point-in-time hurdle | BLS_POINT_IN_TIME_RELEASE_VERIFIED | The CPI pair is 2025-08-01=323.976 and 2026-08-01=334.98 (Index 1982-84=100); release availability is 2026-09-11, before decision date 2026-10-05. Inflation is 3.3965%; the arithmetic CPI + 4% hurdle is 7.3965%. Source: https://www.bls.gov/news.release/archives/cpi_09112026.htm. This is BLS release evidence, not an ALFRED API vintage. Needed: For exact revised-series vintage reproduction, archive the underlying ALFRED response; this run relies on the contemporaneous BLS release and does not claim ALFRED API verification. Sources: [FRED observations API and vintage_dates parameter](https://fred.stlouisfed.org/docs/api/fred/series_observations.html), [FRED real-time periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html), [BLS archived August 2026 CPI release](https://www.bls.gov/news.release/archives/cpi_09112026.htm), [BLS 2026 release schedule](https://www.bls.gov/schedule/2026/home.htm) |
| S9 annual loss statement | UNRESOLVED_CLIENT_POLICY | Lab_13.md describes an annual loss greater than 10% as an unverifiable promise and does not define measurement or breach handling. No external market source can supply this client-specific policy decision. Needed: CIO definition of calendar/fiscal/rolling year, NAV or market-price total return, fee/cost treatment, and breach escalation. Until then, display a human-review alert only; do not promise or encode a loss guarantee. Sources: [Lab_13.md S9 source](../../Lab_13.md) |

## Monitoring triggers and stop conditions

- **Point-in-time CPI or required market observation unavailable, revised without a recorded vintage, or dated after the decision boundary** — STOP the decision run; do not reuse the prior hurdle as current or substitute a later release.
- **Optimizer returns infeasible, covariance validation fails, or required constraint cannot be evaluated** — STOP and report the failed rule/input. Do not relax constraints or treat unknown as PASS.
- **Verified reserve falls below the mandate's required distribution coverage** — Escalate before trading and restore the committee-approved reserve; current modeled floor is 3% only under the stated $0.75m quarterly distribution assumption.
- **Verified five-day liquid share falls below 90% or a position-sized liquidation test fails** — STOP new allocations and obtain committee-approved remediation; ETF headline volume or median spread alone is insufficient.
- **Aggregated nonexempt issuer exposure exceeds 8% under a CIO-confirmed S6 interpretation** — Block the proposed trade and obtain committee direction; no exemption is presumed.
- **Actual one-way turnover exceeds 25%** — Do not rebalance absent the committee approval explicitly required by S7; current holdings are missing, so modeled turnover is illustrative only.
- **Rolling five-year after-cost return falls below the CPI + 4% objective using admissible vintages** — Trigger committee review and rerun the analysis; this is an objective review trigger, not a guaranteed return or automatic liquidation rule.
- **DGS10 is unavailable at the decision date** — Mark the signal unavailable and proceed without an automatic portfolio tilt; obtain a fresh permitted observation before using it as a review input.
- **Calendar-year loss approaches or crosses -10%** — Human-review alert only pending CIO definition of S9. Do not represent this as a verified breach or automatic sell rule.
- **Proposed weights lie outside a subsequently committee-approved allocation range** — STOP that trade pending review. The current stress envelope is not an approved range.

## Reversal conditions

| Current outcome | Change to | Condition |
|---|---|---|
| HOLD | CONDITIONAL_PILOT | Point-in-time CPI and all required data are valid; actual holdings/costs are recorded; S3, S5, S6, S7 and S8 have documented treatment/evidence; the CIO approves S9 handling and the committee sets pilot size, authority, duration, review cadence, and abort conditions. |
| CONDITIONAL_PILOT | HOLD | Any required observation is unavailable or revised without vintage evidence, an optimizer/covariance stop occurs, a mandatory rule becomes untestable, or a pilot monitoring trigger is breached. |
| ANY | REJECT | A hard mandate violation is verified and no committee-approved exception or feasible remedy exists. Hypothetical equal-weight turnover infeasibility alone does not meet this condition. |
| CONDITIONAL_PILOT | APPROVE | Only after the committee-defined pilot review period is complete, outcomes and actual costs reconcile to the pre-approved plan, constraints remain verified, and the committee accepts a stress-supported allocation range. |

## Decisions requested from the committee

- Confirm that the archived BLS not-seasonally-adjusted CPI-U release is the preferred operational interpretation of the CPI + 4% mandate, or require a contemporaneous ALFRED CPIAUCSL vintage before adoption.
- Provide Meridian's actual holdings and holdings as-of date, plus an approved transaction-cost estimate or execution evidence.
- Confirm whether the S6 exemptions in config/mandate.json govern despite their absence from the S6 sentence in Lab_13.md; approve look-through and issuer aggregation treatment.
- Provide position-sized five-business-day sale and settlement evidence for the 90% liquidity rule.
- Define how S9 is measured and handled, and confirm the minimum-volatility objective as a modeling choice under S10.
- Decide whether the model-only stress envelope is useful for discussion; no allocation range is recommended for authorization in this report.
