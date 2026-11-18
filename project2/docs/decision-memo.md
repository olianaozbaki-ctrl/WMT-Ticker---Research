# Meridian Foundation Decision Memo — Phase 2 Interim Review

**AI use:** OpenAI Codex assisted with Phase 1–2 architecture, implementation, tests, data-pipeline design, and documentation. The analysis and investment decision remain the student's responsibility.

**Educational project only; not investment advice.**

## Interim status

Do not adopt or allocate from the Phase 2 output yet. The application now executes real dated market inputs and compares two baselines with a provisional constrained portfolio, but critical compliance evidence remains unavailable. This is a hold for committee review, not the final Project 2 recommendation.

## Intended committee question

Should the Meridian Foundation reject, pilot, or adopt the proposed constrained ETF allocation process and, if piloted or adopted, what allocation ranges should the committee authorize?

## Executed evidence

As of 2026-10-30, five years of monthly adjusted-price data produce a 40% BIL / 60% VT provisional minimum-volatility grid portfolio. Its historical annualized arithmetic expected return is 7.79% and volatility is 8.95%. The equal-weight baseline estimates 3.18% return and 7.49% volatility; the 60% VT / 40% LQD benchmark estimates 6.16% return and 12.23% volatility.

These are historical estimates, not promised returns. The constrained mix clears the provisional 7.72% CPI + 4% after-cost modeling hurdle, but that check relies on a current FRED snapshot and an illustrative cost assumption.

## Why no decision is requested yet

- Actual Meridian holdings and their as-of date are unavailable, so turnover compliance cannot be tested.
- Under the explicitly hypothetical equal-weight start, the 25% turnover cap makes the provisional return hurdle infeasible; this is a stop condition, not evidence about actual holdings.
- Independent five-business-day ETF liquidity evidence is unavailable.
- ETF issuer exposure and exemption treatment are unverified.
- The CPI inputs have release-date support but not the required ALFRED-vintage verification.
- S9 remains unresolved, and no stress matrix or allocation range has been completed.

The next committee action is to resolve the missing evidence and modeling decisions before a committee decision or funded implementation. No Locked Changed-Input Record has been run.

## Phase 4A candidate recommendation — for student review, not final judgment

**Candidate disposition: HOLD funded deployment. Do not authorize an allocation range on the current evidence.** This is a rule-based decision-support output for the student's personal review; the student retains the investment judgment. The current record does not support a full approval or a funded conditional pilot. A paper-only rehearsal may be considered if separately approved.

### What the results say

The Phase 3B full signal-aligned history selects 44% BIL / 56% VT; the 36-month window selects 78% BIL / 22% VT. The BIL weight shifts 34 percentage points, with full-window/36-month model estimates of 7.7974%/7.8598% gross annual expected return and 8.4154%/2.6057% annual volatility, respectively. These historical means and volatilities describe the selected samples; they are not forecasts. The feasible stress solutions span BIL 17–78%, IEF 0%, LQD 0%, VT 22–83%. This is a diagnostic envelope, not a defensible authorization range: the estimation-window shift is large, the policy sets no stability tolerance, and the hurdle/evidence gates below fail.

### Point-in-time feasibility stop

The historical signal/stress decision date is October 5, 2026. The optimizer used the September 2026 CPI observation, whose availability in the project provenance is October 14, 2026. The BLS archived release confirms that September CPI was embargoed until October 14 at 8:30 a.m. ET. Therefore the CPI + 4% hurdle used by that historical stress calculation was not known on October 5. Its optimizer `PROVISIONAL_FEASIBLE` status is numerical feasibility on the supplied input, not point-in-time feasibility. FRED documents vintage-date/realtime retrieval, but this project does not contain the required ALFRED CPI vintage. No substitute value is inferred. [BLS release](https://www.bls.gov/news.release/archives/cpi_10142026.htm); [FRED observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html).

### Decision gates and requested action

- **Liquidity (S8):** SEC Rule 6c-11 and fund pages expose prior-day holdings, NAV/market information, and 30-day median spreads. Those indicators do not prove that at least 90% of Meridian's position can be sold and settled within five business days at the actual order size. Obtain a dated, position-sized liquidation analysis.
- **Issuer limit (S6):** `Lab_13.md` says 8% per issuer and does not state exemptions. Configuration exemptions are unconfirmed; decide whether to apply them and whether to look through ETFs, then aggregate dated holdings as needed.
- **Turnover and costs (S7):** Actual holdings/as-of date and observed execution costs are missing. The 25% cap is infeasible from hypothetical equal-weight holdings, which is not evidence about Meridian's real portfolio.
- **S9:** The annual-loss statement has no defined measurement or breach response. Keep it `UNRESOLVED`; any -10% alert is human-review only until the CIO specifies the policy.
- **CPI/decision date:** Choose the date that governs the next stress run and obtain both CPI inputs from the correct ALFRED vintage. For the October 5 date, do not use September CPI released October 14.

Use the [generated Phase 4A decision-support report](../outputs/phase4a_decision_support.md) for the full outcome framework, model envelope, portfolio-by-window comparisons, evidence references, monitoring triggers, and committee questions. The candidate disposition is not a recommendation to buy or sell a fund.
