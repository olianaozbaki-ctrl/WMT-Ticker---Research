# Phase 2 Executed Results

Generated directly by `python scripts/generate_phase2_results.py`; values were not manually transcribed.

- Analysis date: **2026-11-18**
- Source retrieval date: **2026-11-17**
- Market-data as-of date: **2026-10-30**
- Price observations: **61 monthly adjusted closes**
- Return observations: **60 monthly simple returns**
- Provisional CPI year-over-year: **3.72%**
- Provisional after-cost hurdle: **7.72%**
- ALFRED vintage verified: **False**
- DGS10 point-in-time signal: **5.28%** (observation 2026-10-02; available 2026-10-05; decision 2026-10-05)

## Portfolio comparison

| Portfolio | BIL | IEF | LQD | VT | Expected return | Volatility | Reserve | Illustrative turnover | Illustrative cost | Verified mandate feasible |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Equal weight | 25.00% | 25.00% | 25.00% | 25.00% | 3.18% | 7.49% | 25.00% | 0.00% | 0.00% | False |
| 60/40 benchmark | 0.00% | 0.00% | 40.00% | 60.00% | 6.16% | 12.23% | 0.00% | 50.00% | 0.05% | False |
| Constrained minimum volatility | 40.00% | 0.00% | 0.00% | 60.00% | 7.79% | 8.95% | 40.00% | 50.00% | 0.05% | False |

## Rule-level verdicts

### Equal weight

| Rule | Verdict | Measured | Limit | Explanation |
|---|---|---:|---:|---|
| Weights sum to 100% | PASS | 1.000000 | 1.000000 | Portfolio weights must be fully invested and use decimal units. |
| No short sales | PASS | 0.250000 | 0.000000 | Every direct portfolio weight must be nonnegative. |
| No borrowing | PASS | 0.000000 | 0.000000 | Borrowing is prohibited by the mandate. |
| No derivatives | PASS | 0.000000 | 0.000000 | Direct derivative use is prohibited by the mandate. |
| Twelve-month distribution reserve | PASS | 0.250000 | 0.030000 | Approved reserve-eligible assets must cover four quarterly distributions. |
| Five-business-day liquidity | NOT_TESTABLE | — | — | Liquidity evidence is missing for: BIL, IEF, LQD, VT |
| Maximum nonexempt issuer exposure | NOT_TESTABLE | — | — | Issuer metadata is missing for: BIL, IEF, LQD, VT |
| Annual turnover limit | NOT_TESTABLE | — | — | Current weights and their as-of date are required for turnover. |
| Seven-year investment horizon | PASS | 7.000000 | 7.000000 | The proposed process must be evaluated for the stated mandate horizon. |
| Annual rebalancing | PASS | 1.000000 | 1.000000 | The Meridian mandate specifies annual rebalancing. |
| CPI + 4% after-cost expected-return proxy | NOT_TESTABLE | — | — | Expected returns, CPI, current weights, and transaction cost are all required. Passing this proxy will not prove the rolling five-year realized objective. |
| Calendar-year loss threshold | UNRESOLVED | — | -0.100000 | The -10% statement lacks an approved measurement and breach rule. It is monitored and escalated, never reported as a guaranteed pass. |

### 60/40 benchmark

| Rule | Verdict | Measured | Limit | Explanation |
|---|---|---:|---:|---|
| Weights sum to 100% | PASS | 1.000000 | 1.000000 | Portfolio weights must be fully invested and use decimal units. |
| No short sales | PASS | 0.000000 | 0.000000 | Every direct portfolio weight must be nonnegative. |
| No borrowing | PASS | 0.000000 | 0.000000 | Borrowing is prohibited by the mandate. |
| No derivatives | PASS | 0.000000 | 0.000000 | Direct derivative use is prohibited by the mandate. |
| Twelve-month distribution reserve | FAIL | 0.000000 | 0.030000 | Approved reserve-eligible assets must cover four quarterly distributions. |
| Five-business-day liquidity | NOT_TESTABLE | — | — | Liquidity evidence is missing for: LQD, VT |
| Maximum nonexempt issuer exposure | NOT_TESTABLE | — | — | Issuer metadata is missing for: LQD, VT |
| Annual turnover limit | NOT_TESTABLE | — | — | Current weights and their as-of date are required for turnover. |
| Seven-year investment horizon | PASS | 7.000000 | 7.000000 | The proposed process must be evaluated for the stated mandate horizon. |
| Annual rebalancing | PASS | 1.000000 | 1.000000 | The Meridian mandate specifies annual rebalancing. |
| CPI + 4% after-cost expected-return proxy | NOT_TESTABLE | — | — | Expected returns, CPI, current weights, and transaction cost are all required. Passing this proxy will not prove the rolling five-year realized objective. |
| Calendar-year loss threshold | UNRESOLVED | — | -0.100000 | The -10% statement lacks an approved measurement and breach rule. It is monitored and escalated, never reported as a guaranteed pass. |

### Constrained minimum volatility

| Rule | Verdict | Measured | Limit | Explanation |
|---|---|---:|---:|---|
| Weights sum to 100% | PASS | 1.000000 | 1.000000 | Portfolio weights must be fully invested and use decimal units. |
| No short sales | PASS | 0.000000 | 0.000000 | Every direct portfolio weight must be nonnegative. |
| No borrowing | PASS | 0.000000 | 0.000000 | Borrowing is prohibited by the mandate. |
| No derivatives | PASS | 0.000000 | 0.000000 | Direct derivative use is prohibited by the mandate. |
| Twelve-month distribution reserve | PASS | 0.400000 | 0.030000 | Approved reserve-eligible assets must cover four quarterly distributions. |
| Five-business-day liquidity | NOT_TESTABLE | — | — | Liquidity evidence is missing for: BIL, VT |
| Maximum nonexempt issuer exposure | NOT_TESTABLE | — | — | Issuer metadata is missing for: BIL, VT |
| Annual turnover limit | NOT_TESTABLE | — | — | Current weights and their as-of date are required for turnover. |
| Seven-year investment horizon | PASS | 7.000000 | 7.000000 | The proposed process must be evaluated for the stated mandate horizon. |
| Annual rebalancing | PASS | 1.000000 | 1.000000 | The Meridian mandate specifies annual rebalancing. |
| CPI + 4% after-cost expected-return proxy | NOT_TESTABLE | — | — | Expected returns, CPI, current weights, and transaction cost are all required. Passing this proxy will not prove the rolling five-year realized objective. |
| Calendar-year loss threshold | UNRESOLVED | — | -0.100000 | The -10% statement lacks an approved measurement and breach rule. It is monitored and escalated, never reported as a guaranteed pass. |

## Feasibility boundary and stop condition

- Provisional optimizer feasible on supported model inputs: **True**
- Full mandate feasible: **False**
- Starting holdings for turnover sensitivity: **Hypothetical equal weight; not actual Meridian holdings**
- Feasible if the hypothetical start were subject to the 25.00% turnover cap: **False**
- Maximum net expected return under that hypothetical cap: **6.06%**
- Provisional return hurdle: **7.72%**
- Shortfall: **1.66%**

Because actual Meridian holdings and their as-of date are unavailable, this is a hypothetical stop-condition test, not an actual turnover verdict. Actual turnover remains NOT_TESTABLE.

## Optimizer precision validation

Production exhaustive 1% grid compared with exhaustive 0.5% grid and SciPy SLSQP continuous variance minimization from four starting points; all use identical long-only, full-investment, reserve, provisional after-cost return, and illustrative-cost inputs.

| Method | BIL | IEF | LQD | VT | Net return | Volatility |
|---|---:|---:|---:|---:|---:|---:|
| Production 1% grid | 40.00% | 0.00% | 0.00% | 60.00% | 7.74% | 8.95% |
| Finer 0.5% grid | 40.00% | 0.00% | 0.00% | 60.00% | 7.74% | 8.95% |
| Continuous SLSQP | 40.40% | 0.00% | 0.00% | 59.60% | 7.72% | 8.90% |

Maximum production-grid weight difference versus continuous: **0.4022 percentage points**.
Production-grid volatility gap versus continuous: **0.0591 percentage points**.
Conclusion: **The 1% grid is sufficiently accurate for Phase 2 comparison.**

## Limitations

- Historical arithmetic means are estimates, not forecasts or promised returns.
- Turnover and transaction costs use a hypothetical equal-weight starting allocation and illustrative 10 bps cost; neither is actual Meridian evidence.
- ETF five-business-day liquidity remains unverified, so no portfolio is reported as fully mandate-compliant.
- The CPI hurdle uses a current FRED snapshot; ALFRED vintage verification remains outstanding.
- The 1% grid solution is discrete and may differ from a continuous optimum.

## DGS10 point-in-time signal

{
  "available": true,
  "series_id": "DGS10",
  "source": "Board of Governors of the Federal Reserve System, H.15, via FRED/ALFRED",
  "source_url": "https://fred.stlouisfed.org/series/DGS10",
  "decision_date": "2026-10-05",
  "observation_date": "2026-10-02",
  "availability_date": "2026-10-05",
  "value_percent": 5.28,
  "units": "percent, not seasonally adjusted",
  "interpretation": "10-year Treasury constant-maturity yield; descriptive macro regime indicator, not a return forecast.",
  "action": "Modeling assumption: use as a review trigger only; do not alter weights automatically. Rerun rates-sensitive valuation and approved stresses when elevated or materially changed."
}
