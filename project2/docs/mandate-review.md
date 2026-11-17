# Meridian Mandate Review Before Phase 2

This review compares the approved Project 2 modeling decisions with the authoritative language in `../Lab_13.md`. Original policy and modeling assumptions are deliberately separate. No investment result is reported.

| Decision | Lab 13 comparison | Conflict assessment | Treatment |
|---|---|---|---|
| Minimize annualized volatility subject to return and constraints | S10 says the objective is missing; the CIO question expressly contrasts maximizing return with minimizing risk while meeting the objective. | No contradiction, but it adds a modeling choice not present in the original policy. | Approved Project 2 modeling assumption; original S10 remains preserved. |
| BIL reserve eligible; IEF not automatically reserve eligible | S3 permits cash or eligible government securities but does not classify ETFs. | No contradiction; this is an instrument-classification decision. | BIL counts toward reserve; IEF is a Treasury-bond holding only. ETF liquidity remains unverified. |
| Do not invent current holdings | S7 imposes a turnover limit but Lab 13 supplies no actual starting portfolio. | No conflict. | Actual holdings remain unavailable. Equal weight is labeled hypothetical and may be used only to illustrate turnover mechanics. |
| Illustrative transaction costs with sensitivity | S2 requires an after-cost objective but supplies no cost estimate. | No conflict; a number is necessary for modeling but cannot be represented as observed. | Base 10 bps one-way, stressed at 0/10/25 bps, all labeled illustrative. |
| CPIAUCSL with point-in-time availability | S2 names CPI but no series or publication convention. | No conflict; series selection and availability control are modeling conventions. | Year-over-year CPIAUCSL from the ALFRED vintage available on the decision date; record observation and availability dates for both inputs. |
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

CPIAUCSL is a monthly, seasonally adjusted CPI-U index. FRED identifies year-over-year percent change as a common inflation measure. For Project 2, each CPI input must retain both its observation date and the date it became available. ALFRED vintage dates identify when values were released or revised. An observation is inadmissible when its availability date is after the portfolio decision date.

Sources: [FRED CPIAUCSL series](https://fred.stlouisfed.org/series/CPIAUCSL), [FRED observations API](https://fred.stlouisfed.org/docs/api/fred/series_observations.html), and [FRED vintage-date definition](https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html).

## Remaining policy ambiguity

`Lab_13.md` states the 8% issuer rule but does not list exemptions. The existing Lab 13 checker and the official common case exempt cash, the U.S. Treasury, and diversified funds. The configuration retains those case exemptions but flags confirmation as unresolved because the Markdown mandate is authoritative for this project.
