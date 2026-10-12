# Walmart Project 1 — Final Valuation Assumptions Review

**Proposed valuation date:** September 23, 2026  
**Status:** Decision support for the V3 diagnostic model. This review does not select a final investment conclusion and does not convert provisional inputs into verified facts.  
**Units:** USD millions except per-share amounts, percentages, and stated share counts.

## Scope and current V3 result

This review uses the unchanged V3 forecast and enterprise-to-equity bridge in `walmart_project1_proforma_v3.py` and `project1_fcff_v3.py`. The current V3 output is:

| Measure | V3 result |
|---|---:|
| Present value of explicit FCFF | $60,185.789 |
| Present value of terminal value | $274,669.788 |
| Enterprise value | $334,855.577 |
| Cash added | $11,529.000 |
| Debt subtracted | $(47,746.000) |
| Finance leases subtracted | $(6,832.000) |
| NCI subtracted | $0.000 |
| Nonoperating investments added | $0.000 |
| Provisional common equity value | $291,806.577 |
| Share denominator | 7,933.746241 million |
| Value per share | **$36.780427** |
| Terminal-value share of enterprise value | **82.03%** |

The $36.78 output is value per **August 26 basic share**, not a verified September 23 diluted value. It remains a diagnostic result.

## Source hierarchy

- [Walmart FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), fiscal year ended January 31, 2026, filed March 13, 2026.
- [Walmart FY2027 second-quarter Form 10-Q](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm), period ended July 31, 2026, filed August 28, 2026.
- [U.S. Treasury daily par yield curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&type=daily_treasury_yield_curve), September 23, 2026.
- [Kroll September 2026 cost-of-capital recommendation](https://edge.sitecorecloud.io/krollllc17bf0-kroll6fee-proda464-0e9b/media/cost-of-capital/kroll-cost-of-capital-recommendations-updated-to-use-spot-risk-free-rates-september-2026.pdf), published September 10, 2026.
- [ICE BofA AA U.S. Corporate Index Effective Yield](https://fred.stlouisfed.org/series/BAMLC0A2CAAEY), September 23, 2026 observation.

“Verified” below means that a value and definition are confirmed in the cited source. It does not mean that a historical accounting balance is the correct September 23 valuation adjustment.

## Assumption decisions

### 1. WACC

| Item | Assessment |
|---|---|
| Current V3 value | **7.00%** |
| Exact definition | Discount rate applied to consolidated, nominal USD FCFF before debt and finance-lease financing cash flows. |
| Current status | **PROVISIONAL.** It is a model choice, not a sourced September 23 market observation. |
| Source evidence | September 23 ten-year Treasury yield **5.11%** (verified market observation); beta **0.55** (unverified assumption; dated reported estimates in the evidence file range from 0.39 to 0.66); Kroll U.S. ERP **5.00%** effective September 2 (verified published recommendation); pretax debt proxy **5.54%–5.66%** (unverified as Walmart-specific); tax rate **24.50%** (provisional); estimated weights **94.8364% equity / 5.1636% debt** using mixed-date inputs. |
| Evidence-based calculation | Using 5.11%, 0.55, 5.00%, 5.66%, 24.50%, and the estimated weights produces **7.6748%**. The arithmetic is verified; the combined estimate is illustrative because beta, debt yield, tax convention, weights, and the Kroll risk-free maturity pairing remain unresolved. |
| Recommended decision range | Use **7.00%–7.67% as a disclosed working range**, not a verified final range. Retain 7.00% only as the V3 continuity case and use 7.6748% as the dated-evidence illustration. Do not use the preliminary 6.6774% as the September 23 central case because it contains the unsupported 4.10% risk-free assumption. Select a point only after resolving the beta methodology and the risk-free/ERP pairing. |

At 2.50% terminal growth and with all other V3 inputs fixed:

| WACC | Value per share | Change from V3 |
|---:|---:|---:|
| 6.6774% preliminary case | $40.090425 | +$3.309997 |
| **7.0000% V3** | **$36.780427** | — |
| 7.6748% dated-evidence illustration | $31.192800 | −$5.587627 |

This sensitivity is mechanical. It does not validate any of the three rates.

### 2. Terminal growth

| Item | Assessment |
|---|---|
| Current V3 value | **2.50%** |
| Exact definition | Perpetual nominal growth rate applied to FY2031 FCFF to calculate terminal value. |
| Primary support | Prior Project 1 modeling judgment described it as a long-run nominal-growth anchor. No Walmart filing reports a terminal-growth rate, and the reviewed evidence does not contain a dated market observation that independently verifies 2.50%. |
| Current status | **PROVISIONAL valuation assumption.** |
| Recommended decision range | Retain **2.50% as the working midpoint** and disclose **2.00%–3.00%** sensitivity. A final choice must be reconciled to mature Walmart revenue growth, margins, reinvestment, and return on invested capital; `g < WACC` is necessary but not sufficient. |

At 7.00% WACC and with all other V3 inputs fixed:

| Terminal growth | Value per share | Change from V3 |
|---:|---:|---:|
| 2.00% | $33.166391 | −$3.614036 |
| **2.50% V3** | **$36.780427** | — |
| 3.00% | $41.297973 | +$4.517545 |

Because terminal value is 82.03% of V3 enterprise value, this assumption is highly material.

### 3. Valuation-date share count

| Item | Assessment |
|---|---|
| Current V3 value | **7,933.746241 million shares** |
| Primary source and date | Form 10-Q cover, filed August 28, 2026: **7,933,746,241 common shares outstanding on August 26, 2026**. |
| Exact definition | Basic common shares actually outstanding on a point-in-time date. It is not a weighted-average count and contains no valuation-date treasury-stock or if-converted dilution. |
| Current status | **VERIFIED filing fact; PROVISIONAL valuation denominator.** It is 28 days before September 23 and is not diluted. |
| Recommended treatment | Begin with the August 26 count, then add only award-specific September 23 dilution supported by outstanding awards, vesting/performance terms, exercise prices, and the September 23 share price. Until that work is complete, show **7,933.746241–8,022 million** only as a transparent denominator sensitivity; it is not a verified valuation-date range. The upper figure is the FY2026 weighted-average diluted EPS denominator, not a spot count. |

Holding V3 equity value constant, 7,933.746241 million shares gives $36.780427 per share; 8,022 million gives **$36.375789**, or **$0.404639 less**. A 1% increase in the denominator would reduce value by approximately **$0.3642 per share**, holding equity value fixed.

### 4. Cash

| Item | Assessment |
|---|---|
| Current V3 value | **$11,529** added to enterprise value |
| Primary source and date | July 31 Form 10-Q, Condensed Consolidated Balance Sheet; period ended July 31, 2026. |
| Exact definition | Total reported **cash and cash equivalents**, not “excess cash.” |
| Current status | **VERIFIED accounting balance; PROVISIONAL bridge treatment and date.** The filing does not establish that the full balance is distributable to Walmart common shareholders. |
| Recommended treatment | Add only cash demonstrated to be excess after operating liquidity, jurisdictional restrictions, transfer costs, and NCI ownership. Pending that analysis, present **$0–$11,529** as a conservative bridge sensitivity, not as a forecast of September 23 cash. The upper end is total July 31 cash; the lower end avoids claiming unsupported excess cash. |

Each $1,000 change in cash changes equity value by $1,000 and value per share by approximately **$0.126044**. Adding no cash would reduce V3 value to **$35.327268**, a **$1.453160** decrease. The $11,529 V3 treatment is therefore the upper end of the stated cash sensitivity.

### 5. Debt

| Item | Assessment |
|---|---|
| Current V3 value | **$47,746** subtracted |
| Primary source and date | July 31 Form 10-Q: $10,479 short-term borrowings and $39,932 long-term debt including current maturities; the filing reports long-term-debt fair value of $37,267. |
| Exact V3 definition | Short-term borrowings at carrying value, which Walmart says approximates fair value because of short maturities, plus disclosed fair value of long-term debt: $10,479 + $37,267 = $47,746. Finance leases are excluded and subtracted separately. |
| Current status | **Source-backed mixed-measure proxy; PROVISIONAL for September 23.** It is a July 31 observation, not a same-day instrument-level market value. |
| Recommended treatment | Use the same-date market value of interest-bearing borrowings when available. Until then, disclose **$47,746 fair-value proxy to $50,411 carrying value** as two July 31 measurement conventions, not as a bound on September 23 debt. Keep the debt definition consistent with WACC capital weights and do not add current maturities a second time. |

Using $50,411 instead of $47,746 would lower equity value by $2,665 and value per share by **$0.335907**, to **$36.444520**.

### 6. Finance leases

| Item | Assessment |
|---|---|
| Current V3 value | **$6,832** subtracted |
| Primary source and date | July 31 Form 10-Q balance-sheet finance-lease obligations: $880 current plus $5,952 long-term. |
| Exact definition | Carrying amount of current and long-term finance-lease liabilities. It is excluded from the $47,746 debt proxy. |
| Current status | **VERIFIED July 31 accounting balance; PROVISIONAL September 23 bridge amount.** No separate market value is reported. |
| Recommended treatment | Continue subtracting the latest $6,832 carrying amount provisionally under V3's financing convention, but update it to September 23 if a defensible roll-forward or later filing evidence becomes available. Do not subtract it if lease principal and full lease payments are also deducted as operating FCFF. V3 avoids that duplication by treating principal and interest as financing flows and lease additions as economic capex. |

Each $1,000 change in the finance-lease claim changes value per share by approximately **$0.126044** in the opposite direction. Omitting the claim would increase value by **$0.861132 per share**, but omission is not recommended under V3's financing convention. Using the January 31 balance of $6,761 instead would increase value by only **$0.008949 per share**; that comparison measures date selection, not economic correctness.

### 7. Noncontrolling interests

| Item | Assessment |
|---|---|
| Current V3 value | **$0** subtracted |
| Primary source and date | July 31 Form 10-Q reports $293 redeemable NCI and $6,268 nonredeemable NCI, or **$6,561 combined book amount**. |
| Exact definition | Accounting carrying amounts for equity claims in consolidated subsidiaries not owned by Walmart common shareholders. They are not a reported market value. |
| Current status | The reported $6,561 book amount is **VERIFIED**; the V3 zero and any September 23 market-value adjustment are **PROVISIONAL/UNVERIFIED**. Zero is not evidence that NCI is immaterial. |
| Recommended treatment | Because V3 values consolidated FCFF, subtract an NCI claim unless the minority share of subsidiary FCFF has first been removed. Use **$6,561 only as an explicitly provisional book-value proxy or sensitivity**, while obtaining a September 23 ownership and market-value analysis. Reconcile subsidiary cash and investments so the minority claim is not counted twice. |

Subtracting the $6,561 book proxy would reduce V3 value by **$0.826974 per share**, to **$35.953454**. This illustrates materiality; it does not verify book value as fair value.

### 8. Nonoperating investments

| Item | Assessment |
|---|---|
| Current V3 value | **$0** added |
| Primary source and date | July 31 Form 10-Q recurring fair-value table reports $860 Level 1 equity, $2,781 Level 2 equity, and $1,226 Level 3 debt investments, totaling **$4,867**. |
| Exact definition | Investments included in the filing's recurring fair-value table; this is not necessarily the complete population of nonoperating investments or the amount attributable to Walmart common shareholders. |
| Current status | The $4,867 table total is **VERIFIED**; its September 23 value, ownership allocation, operating classification, and bridge eligibility are **UNVERIFIED**. |
| Recommended treatment | Retain zero until the investments and related income are removed consistently from operating assets, operating NWC, and FCFF. Then add only the September 23 value attributable to Walmart common shareholders. Mechanically adding $4,867 today could double count value already embedded in the forecast. |

If $4,867 were eligible and added without any offsetting FCFF change, value would rise by approximately **$0.613455 per share**. This is a materiality illustration, not a recommended adjustment.

## Valuation-date reconciliation

| Element | Date currently represented | September 23 consistency |
|---|---|---|
| Stated valuation date | September 23, 2026 | Matches the proposed Project 1 date. |
| DCF timing | Five annual FY2027–FY2031 FCFF amounts discounted as full annual periods | **PROVISIONAL.** The code contains no September 23 stub-period or fiscal-year timing adjustment, so its discount timing is an annual-period convention rather than an exact date-based DCF. |
| Risk-free rate used in V3 | V3 uses a 7.00% aggregate WACC; no component date is encoded | The evidence file has a September 23 Treasury observation, but V3 WACC does not incorporate a finalized component build. |
| Share count | August 26, 2026 | Verified basic count, 28 days early; September 23 dilution unverified. |
| Cash, debt, finance leases, and NCI evidence | July 31, 2026 | Latest pre-date filing balances, 54 days early; not September 23 market values. |
| Equity price used for WACC weights | September 23, 2026 closing price of $110.53 | Date matches, but the paired share count and debt measure are earlier. |
| Opening operating statements | FY2026 ended January 31, 2026 | Historical forecast base, not a bridge date; later operating results are not incorporated into V3. |

Accordingly, V3 should be described as a **September 23 valuation framework using the latest reviewed pre-date filed bridge observations**, not as a fully same-date valuation. The final memo should either obtain valuation-date data or state the mixed-date convention prominently.

## WACC and terminal-growth sensitivity

The table below reruns the unchanged V3 FCFF and bridge. Entries are value per August 26 basic share; parentheses show change from the $36.780427 V3 base.

| WACC \ Terminal growth | 2.00% | 2.50% | 3.00% |
|---:|---:|---:|---:|
| 6.50% | $37.5354 (+$0.7550) | $42.1384 (+$5.3580) | $48.0565 (+$11.2761) |
| **7.00%** | $33.1664 (−$3.6140) | **$36.7804 ($0.0000)** | $41.2980 (+$4.5175) |
| 7.50% | $29.5930 (−$7.1875) | $32.4953 (−$4.2852) | $36.0425 (−$0.7379) |

All nine cases satisfy `WACC > terminal growth`. They are valuation sensitivity cases, not a final fair-value range. The 6.50% row is below the documented working WACC range and is included only to show curvature around V3.

## Recommended memo presentation

The investment memo should present at least two explicitly provisional valuation cases rather than one final point:

1. **V3 continuity case:** 7.00% WACC, 2.50% terminal growth, and the current bridge, yielding $36.780427 per August 26 basic share.
2. **Dated-evidence discount-rate case:** 7.6748% illustrative WACC with the same 2.50% terminal growth and bridge, yielding $31.192800 per August 26 basic share.

Neither case is a final September 23 diluted fair value. Bridge alternatives for excess cash, debt convention, NCI, investments, and dilution should be shown separately so their effects are not hidden inside the discount-rate sensitivity.

## Source verification still required before the investment memo

1. **WACC:** choose and document a reproducible beta methodology; pair the risk-free maturity with the selected ERP convention; obtain Walmart-specific September 23 bond yields; support the marginal tax rate; and rebuild weights using consistent debt and lease definitions.
2. **Share denominator:** obtain September 23 common shares outstanding and award-level dilution under a documented treasury-stock or if-converted method.
3. **Cash:** identify September 23 cash and the portion genuinely excess after operating, jurisdictional, transfer, tax, and NCI constraints.
4. **Debt:** obtain September 23 market values for short- and long-term borrowings using the same debt perimeter as WACC.
5. **Finance leases:** obtain or roll forward the September 23 liability and confirm that lease additions, amortization, interest, principal, FCFF, invested capital, and the bridge follow one convention.
6. **NCI:** determine the market value and ownership scope of redeemable and nonredeemable NCI and reconcile NCI-controlled cash and investments.
7. **Nonoperating investments:** identify security-level September 23 values, ownership, and related income; remove eligible investments from operating FCFF before adding them in the bridge.
8. **Terminal economics and timing:** support mature growth with reinvestment and return assumptions, and decide whether an exact September 23 stub-period DCF is required.

Until these items are resolved, the V3 output and all sensitivity results remain **diagnostic and provisional**, not a final investment recommendation.
