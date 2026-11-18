# Meridian Foundation Decision Memo — Final Project 2 Recommendation

**AI use:** OpenAI Codex assisted with architecture, implementation, tests, data-pipeline design, and documentation; Google Gemini supplied an independently reconciled validation response. The analysis and investment decision remain the student's responsibility.

**Educational project only; not investment advice.**

## Recommendation

**HOLD funded deployment. Do not adopt the process, allocate capital, rebalance Meridian's portfolio, authorize a funded pilot, or authorize an allocation range on the current evidence.** Continue evidence collection; a paper-only rehearsal may be considered only if the committee separately approves its scope.

This is a process recommendation to the Meridian Foundation CIO and investment committee, not a recommendation to buy or sell BIL, IEF, LQD, or VT.

## Evidence as of October 5, 2026

Market-price inputs end September 30 and contain 59 monthly returns. The corrected CPI input uses the BLS August release published September 11: `334.980 / 323.976 − 1 = 3.3965%`. The project's arithmetic CPI + 4% proxy is 7.3965%.

| Portfolio | Weights: BIL / IEF / LQD / VT | Gross return | Illustrative net return | Volatility |
|---|---|---:|---:|---:|
| Equal weight | 25% / 25% / 25% / 25% | 3.0128% | 3.0128% | 7.5482% |
| 60/40 reference | 0% / 0% / 40% / 60% | 6.2591% | 6.2091% | 12.3335% |
| Constrained minimum volatility | 48% / 0% / 0% / 52% | 7.5017% | 7.4517% | 7.8242% |

The modeled portfolio clears the return proxy by only 5.51 basis points. “Net” deducts one illustrative 10 bps one-way transition charge from hypothetical equal-weight holdings; it is not an observed or recurring Meridian cost. Historical arithmetic means are estimates, not forecasts or proof of rolling five-year compounded performance.

## Mandate status

| Rule | Current treatment and implication |
|---|---|
| S1 — seven-year horizon; annual rebalance | Modeled horizon and frequency pass, but implementation feasibility is not established. |
| S2 — CPI + 4% after costs over rolling five years | Arithmetic proxy only; full rule is `NOT_TESTABLE`. The 5.51 bp margin is not rolling five-year proof. |
| S3 — twelve months of distributions in cash/eligible government securities | Modeled 3% floor passes with 48% BIL; BIL eligibility remains a committee-review assumption. |
| S4 — 60/40 reference | Used only for comparison. Its modeled reserve failure does not make it the proposed portfolio. |
| S5 — no borrowing, short selling, or derivatives | Passes in the long-only ETF construction; no constraint is relaxed. |
| S6 — maximum 8% per issuer | `NOT_TESTABLE`; exemptions, ETF look-through, and dated issuer aggregation require CIO direction and evidence. |
| S7 — maximum 25% annual turnover without approval | `NOT_TESTABLE` without actual holdings. The hypothetical equal-weight case is infeasible at the cap but is not an actual Meridian verdict. |
| S8 — at least 90% redeemable within five business days | `NOT_TESTABLE`; no position-sized sale and settlement study is available. |
| S9 — avoid annual losses greater than 10% | `UNRESOLVED`; measurement and breach response are undefined, so no guarantee is claimed. |
| S10 — objective unspecified | Minimum volatility subject to the return proxy is a modeling assumption requiring CIO approval. |

No candidate portfolio has verified full-mandate compliance.

## Sensitivity, range, and principal risks

The 36-month window selects 80% BIL / 20% VT rather than 48% / 52%, a 32 percentage-point BIL shift. Feasible modeled stresses span BIL 21–80% and VT 20–79%, with IEF and LQD at 0%. This is a **diagnostic envelope, not an authorization range**: it is unstable across estimation windows and depends on incomplete mandate evidence.

A declared −25% VT / unchanged-BIL diagnostic produces approximately −11.24% gross for the 48% / 52% mix. It reinforces the need for an S9 ruling but is not a forecast, VaR estimate, or compliance test. Other decision-critical gaps are actual holdings, execution costs, position-sized liquidity, issuer treatment/exposure, the additive-versus-compounded CPI convention, and recurring annual cost treatment.

The analysis corrected an earlier look-ahead error: September 2026 CPI was released October 14, after the decision date. The current run uses August CPI available September 11, excludes October 30 prices, and uses DGS10 dated October 2 and available October 5. The failed input and correction remain in the validation record.

## Monitoring and reversal conditions

- Stop if a required CPI, market, or signal observation was unavailable by the decision boundary; never substitute a later release.
- Stop and report the failure if optimization is infeasible, covariance validation fails, or a mandatory constraint cannot be evaluated; never silently relax a rule.
- Block funding if confirmed issuer exposure exceeds 8%, actual turnover exceeds 25% without approval, or position-sized five-day liquidity fails the 90% requirement.
- Reconsider a conditional pilot only after actual holdings and costs are supplied; S6 and S8 are verified; S9 and S10 are approved; and pilot size, duration, review cadence, and abort conditions are defined.
- Change HOLD to REJECT if a hard mandate violation is verified and no approved remedy exists.

## Committee action requested

Accept HOLD, decline funded deployment and an allocation range, and direct staff to obtain the missing holdings, cost, liquidity, issuer, CPI-convention, and S9 evidence. The complete framework and triggers are in the [generated decision-support report](../outputs/phase4a_decision_support.md); AI use, the Locked Changed-Input Record, cold run, and independent validation are in [validation-and-ai-use.md](validation-and-ai-use.md).
