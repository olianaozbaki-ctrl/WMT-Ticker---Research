# Meridian Mandate Review Before Phase 2

This review compares the approved Project 2 modeling decisions with the authoritative language in `../Lab_13.md`. Original policy and modeling assumptions are deliberately separate. No investment result is reported.

| Decision | Lab 13 comparison | Conflict assessment | Treatment |
|---|---|---|---|
| Minimize annualized volatility subject to return and constraints | S10 says the objective is missing; the CIO question expressly contrasts maximizing return with minimizing risk while meeting the objective. | No contradiction, but it adds a modeling choice not present in the original policy. | Approved Project 2 modeling assumption; original S10 remains preserved. |
| BIL reserve eligible; IEF not automatically reserve eligible | S3 permits cash or eligible government securities but does not classify ETFs. | No contradiction; this is an instrument-classification decision. | BIL counts toward reserve; IEF is a Treasury-bond holding only. ETF liquidity remains unverified. |
| Do not invent current holdings | S7 imposes a turnover limit but Lab 13 supplies no actual starting portfolio. | No conflict. | Actual holdings remain unavailable. Equal weight is labeled hypothetical and may be used only to illustrate turnover mechanics. |
| Illustrative transaction costs with sensitivity | S2 requires an after-cost objective but supplies no cost estimate. | No conflict; a number is necessary for modeling but cannot be represented as observed. | Base 10 bps one-way, stressed at 0/10/25 bps, all labeled illustrative. |
| CPI-U with point-in-time availability | S2 names CPI but no series or publication convention. | CPI measure and availability convention are modeling choices. | This run uses the BLS archived August 2026 CPI-U release available by October 5, with matching August year-over-year observations; it does not claim ALFRED API vintage verification. |
| Preserve S9 meaning | S9 is explicitly an unverifiable promise with no breach measurement or handling. | Turning it into a hard stop would conflict with Lab 13. | Always `UNRESOLVED`, excluded from feasibility, with no automatic prohibition. |
| Do not assume ETF liquidity | S8 requires 90% redeemable within five business days but does not verify the selected ETFs. | No conflict. | All ETF liquidity fields remain unknown until independently evidenced. |
| Derive ranges after optimization and stress | Lab 13 specifies no allocation ranges. | No conflict. | No range exists before accepted optimization and estimate/window/cost/constraint stresses. |

## Original policy versus modeling assumptions

The exact S1-S10 language is preserved in `config/mandate.json` under `original_policy`. The following are Project 2 modeling assumptions rather than client policy:

- minimum annualized volatility as the optimization objective;
- CPIAUCSL and the year-over-year/vintage convention;
- BIL reserve eligibility and IEF reserve ineligibility;
- one-way turnover as half the sum of absolute trades;
- hypothetical equal-weight starting weights when actual holdings are unavailable; and
- the illustrative 10 bps cost with 0/10/25 bps sensitivity.

## CPI provenance rule

CPI is a monthly index and the mandate does not specify seasonal adjustment. The corrected October 5 historical run uses BLS CPI-U not seasonally adjusted, 334.980 for August 2026 and 323.976 for August 2025. Both were published in the archived August 2026 release on September 11, 2026. Inflation is 3.3965%; the model adds the 4% real-return spread arithmetically for a 7.3965% hurdle. This release is point-in-time evidence from BLS, not an ALFRED API vintage. Any observation unavailable by the decision date is inadmissible.

Sources: [FRED CPIAUCSL series](https://fred.stlouisfed.org/series/CPIAUCSL), [FRED observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html), and [FRED vintage-date definition](https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html).

## Remaining policy ambiguity

`Lab_13.md` states the 8% issuer rule but does not list exemptions. `config/mandate.json` retains cash, U.S. Treasury, and diversified-fund exemptions as a prior case assumption, but the accessible authoritative Markdown does not substantiate it. The exemption and look-through treatment require CIO confirmation; issuer status remains `NOT_TESTABLE` in the meantime.
