# Meridian Foundation Decision Memo — Phase 2 Interim Review

**AI use:** OpenAI Codex assisted with Phase 1–2 architecture, implementation, tests, data-pipeline design, and documentation. The analysis and investment decision remain the student's responsibility.

**Educational project only; not investment advice.**

## Interim status

Do not adopt or allocate from the Phase 2 output yet. The application now executes real dated market inputs and compares two baselines with a provisional constrained portfolio, but critical compliance evidence remains unavailable. This is a hold for committee review, not the final Project 2 recommendation.

## Intended committee question

Should the Meridian Foundation reject, pilot, or adopt the proposed constrained ETF allocation process and, if piloted or adopted, what allocation ranges should the committee authorize?

## Executed evidence

For the October 5, 2026 decision boundary, ETF prices end September 30, producing 59 monthly returns. The BLS August CPI pair gives 3.3965% year-over-year inflation and an arithmetic CPI + 4% hurdle of 7.3965%. The equal-weight portfolio estimates 3.01% annual return and 7.55% volatility; 60% VT / 40% LQD estimates 6.26% and 12.33%; the provisional minimum-volatility portfolio is 48% BIL / 52% VT at 7.50% gross return and 7.82% volatility.

These are historical estimates, not promised returns. The constrained mix clears the 7.3965% point-in-time CPI + 4% after-cost modeling hurdle by a small margin using one illustrative rebalance cost. The CPI source is the BLS archived August 2026 release dated September 11, 2026, not an ALFRED API vintage.

The modeled margin is only about 5.51 basis points. The application does not establish compounded after-cost performance over rolling five-year periods, and its one modeled transition cost is not a recurring annual rebalancing-cost forecast. Those limitations prevent the point estimate from being treated as verified S2 compliance.

## Why no decision is requested yet

- Actual Meridian holdings and their as-of date are unavailable, so turnover compliance cannot be tested.
- Under the explicitly hypothetical equal-weight start, the 25% turnover cap makes the provisional return hurdle infeasible; this is a stop condition, not evidence about actual holdings.
- Independent five-business-day ETF liquidity evidence is unavailable.
- ETF issuer exposure and exemption treatment are unverified.
- CPI measurement remains a modeling decision: the corrected run uses unadjusted CPI-U from the contemporaneous BLS release rather than seasonally adjusted CPIAUCSL or an ALFRED API vintage.
- S9 remains unresolved, and the completed stress matrix does not support a robust or authorized allocation range.
- As an additional declared diagnostic, a −25% one-year VT return with BIL left at its historical annual arithmetic estimate produces approximately −11.24% gross for the 48% BIL / 52% VT mix. This reinforces the need for an S9 ruling but is not a forecast or compliance test.

The next committee action is to resolve the missing evidence and modeling decisions before a committee decision or funded implementation. The Locked Changed-Input Record has been completed and preserved separately; it did not change the HOLD disposition.

## Phase 4A candidate recommendation — for student review, not final judgment

**Candidate disposition: HOLD funded deployment. Do not authorize an allocation range on the current evidence.** This is a rule-based decision-support output for the student's personal review; the student retains the investment judgment. The current record does not support a full approval or a funded conditional pilot. A paper-only rehearsal may be considered if separately approved.

### What the results say

The corrected full-window reoptimization is 48% BIL / 52% VT; the 36-month window selects 80% BIL / 20% VT. The BIL weight shifts 32 percentage points. Gross annual expected return/volatility are 7.5017%/7.8242% and 7.5422%/2.3730%, respectively. These historical sample statistics are not forecasts. The stress envelope spans BIL 21–80%, IEF 0%, LQD 0%, VT 20–79%. This is a diagnostic envelope, not an authorization range: the window shift is large and mandate evidence remains incomplete.

### Point-in-time feasibility stop

The earlier Phase 3B run contained a CPI look-ahead error: September 2026 CPI was released October 14, after the October 5 decision. That failed result remains preserved in the validation record. The corrected run uses BLS-published August 2025 CPI-U 323.976 and August 2026 CPI-U 334.980; both appear in the archived release published September 11. It also excludes ETF price observations after September 30 and uses DGS10 dated October 2, available October 5. The generated output reports point-in-time release verification while explicitly stating this is not an ALFRED API vintage. [BLS August 2026 release](https://www.bls.gov/news.release/archives/cpi_09112026.htm); [BLS 2026 release schedule](https://www.bls.gov/schedule/2026/home.htm).

### Decision gates and requested action

- **Liquidity (S8):** SEC Rule 6c-11 and fund pages expose prior-day holdings, NAV/market information, and 30-day median spreads. Those indicators do not prove that at least 90% of Meridian's position can be sold and settled within five business days at the actual order size. Obtain a dated, position-sized liquidation analysis.
- **Issuer limit (S6):** `Lab_13.md` says 8% per issuer and does not state exemptions. Configuration exemptions are unconfirmed; decide whether to apply them and whether to look through ETFs, then aggregate dated holdings as needed.
- **Rolling objective (S2):** Confirm additive versus compounded CPI-plus-spread treatment and the recurring cost convention, then obtain enough point-in-time history to test rolling five-year after-cost outcomes. The current arithmetic expected-return proxy is not a compliance verdict.
- **Turnover and costs (S7):** Actual holdings/as-of date and observed execution costs are missing. The 25% cap is infeasible from hypothetical equal-weight holdings, which is not evidence about Meridian's real portfolio.
- **S9:** The annual-loss statement has no defined measurement or breach response. Keep it `UNRESOLVED`; any -10% alert is human-review only until the CIO specifies the policy.
- **CPI convention:** Confirm whether BLS not-seasonally-adjusted CPI-U from a release archive is the committee's preferred target input or require an archived contemporaneous ALFRED CPIAUCSL vintage before operational use.

Use the [generated Phase 4A decision-support report](../outputs/phase4a_decision_support.md) for the full outcome framework, model envelope, portfolio-by-window comparisons, evidence references, monitoring triggers, and committee questions. The candidate disposition is not a recommendation to buy or sell a fund.
