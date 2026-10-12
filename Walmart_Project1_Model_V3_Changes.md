# Walmart Project 1 — V3 Model Changes and V2 Reconciliation

**Status:** Diagnostic V3 model only. V3 is not a final valuation or investment recommendation. The exact September 23, 2026 diluted share count, excess cash, debt value, and finance-lease balance are not available in the reviewed SEC filings.

**New files:** `walmart_project1_proforma_v3.py`, `project1_fcff_v3.py`, and this change log.

**Preserved historical evidence:** V2 remains unchanged at **$35.674421 per FY2026 diluted weighted-average share**, displayed as **$35.67**. No V2 model, original validation file, lab, Edition A file, or `Walmart_Project1_Locked_Changed_Input_Record.md` was modified.

## Primary sources and dates

- Walmart FY2026 Form 10-K, fiscal year ended January 31, 2026, filed March 13, 2026: [primary filing](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) and [filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/0000104169-26-000055-index.html).
- Walmart FY2027 second-quarter Form 10-Q, period ended July 31, 2026, filed August 28, 2026: [primary filing](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) and [filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/0000104169-26-000154-index.html).
- The 10-Q cover reports **7,933,746,241** common shares outstanding on **August 26, 2026**. This is the latest exact filed count before September 23, but it is basic, not diluted, and is 28 days earlier than the proposed valuation date.

All monetary figures below are USD millions unless stated otherwise.

## Five priority corrections

### 1. Share denominator

| Topic | V2 | V3 diagnostic treatment |
|---|---|---|
| Input/formula | `DILUTED_SHARES_M = 8,022`; equity value divided by FY2026 diluted weighted-average shares | Equity value divided by **7,933.746241 million August 26 basic spot shares** |
| SEC evidence | FY2026 10-K Note 2: 7,983 million basic weighted-average shares + 39 million dilutive awards = 8,022 million | August 28 Form 10-Q cover: 7,933,746,241 shares outstanding on August 26 |
| Reporting date | Fiscal year ended January 31, 2026 | August 26, 2026 |
| Status | Confirmed filing fact, but wrong definition for a valuation-date denominator | **Source-backed basic spot count; PROVISIONAL.** Exact September 23 shares and award-specific dilution remain unverified. |
| Sequential valuation impact | — | **+$0.404639 per share** after all operating and bridge changes; no equity-value change |

V3 reports **value per August 26 basic share**, not value per September 23 diluted share. No unsupported dilution estimate is added. This addresses the known weighted-average/spot error without pretending the remaining dilution evidence exists.

### 2. Revenue, net sales, cost of sales, and gross margin

| Topic | V2 | V3 diagnostic treatment |
|---|---|---|
| Opening input | One `revenue = $713,163` | `net_sales = $706,413` plus `membership_other_income = $6,750`, reconciling to total revenue $713,163 |
| Gross profit | `total revenue × gross margin` | `net sales × gross margin on net sales` |
| Cost of sales | `total revenue − gross profit` | `net sales − gross profit` |
| Other income and cash operating expense | Membership/other income is blended into revenue; cash SG&A is a percentage of modeled gross profit | Membership/other income is added after merchandise gross profit; cash operating expense is applied to gross profit plus membership/other income |
| Working-capital link | Inventory and AP days applied to cost of sales derived from total revenue | Inventory and AP days applied to cost of sales derived from net sales |

**Evidence:** FY2026 10-K Consolidated Statements of Income reports $706,413 net sales, $6,750 membership and other income, $713,163 total revenue, and $535,395 cost of sales for the year ended January 31, 2026.

**Status:** The formula correction is **CONFIRMED**. V3 preserves the V2 annual growth, margin, and cash-operating-expense ratio paths; applying the same growth rate to both revenue streams remains **PROVISIONAL** because no separate FY2027–FY2031 source-backed paths are available.

**Sequential valuation impact:** enterprise and equity value increase **$23,496.417**, and value per V2 share increases **$2.928997**. This large result reflects the corrected treatment of membership/other income and the related cost-of-sales and working-capital formulas. It is not a target-calibrated adjustment.

### 3. D&A and finance-lease amortization

| Topic | V2 | V3 diagnostic treatment |
|---|---|---|
| Formula | `10.6% × opening net PP&E`; FY2027 D&A $14,424.798 | Opening calibration: $13,315 nonlease D&A proxy + $888 finance-lease ROU amortization = **$14,203 reported total D&A** |
| Asset linkage | All modeled depreciation reduces PP&E; finance-lease ROU asset is held constant | Nonlease D&A reduces PP&E; finance-lease amortization reduces the finance-lease ROU asset separately |
| Source | 10.6% is a model assumption | FY2026 cash-flow-statement D&A $14,203 and Note 6 finance-lease ROU amortization $888 |

The filing does not fully separate PP&E depreciation from intangible amortization inside the residual $13,315. V3 therefore forecasts the residual from opening net PP&E as an explicit proxy. The opening total is source-reconciled, while the asset-class split and future rates remain **PROVISIONAL**.

**Sequential valuation impact:** enterprise and equity value decrease **$2,786.362**, and value per V2 share decreases **$0.347340** after the revenue correction.

### 4. Valuation-date cash, debt, and finance-lease bridge

| Bridge item | V2 input | V3 input | Source date and definition | Status | Sequential impact |
|---|---:|---:|---|---|---:|
| Cash | +$10,727 | **+$11,529** | July 31 Form 10-Q cash and cash equivalents | Source-backed later date, but full cash is not verified excess cash and is not September 23 | +$802 equity; **+$0.099975/share** |
| Debt | −$44,762 carrying value | **−$47,746 fair-value proxy** | July 31: $10,479 short-term borrowings, whose carrying value approximates fair value, plus $37,267 disclosed long-term-debt fair value | Source-backed later-date proxy; not September 23 and not an instrument-level same-day market value | −$2,984 equity; **−$0.371977/share** |
| Finance leases | −$6,761 | **−$6,832** | July 31 Form 10-Q carrying amount | Source-backed later date; not September 23 market value | −$71 equity; **−$0.008851/share** |

The V3 bridge is:

```text
Enterprise value                                      $334,855.577
+ July 31 cash                                          11,529.000
− July 31 debt fair-value proxy                        (47,746.000)
− July 31 finance-lease obligations                     (6,832.000)
− NCI adjustment retained provisionally at zero                  —
+ Nonoperating-investment adjustment retained at zero            —
                                                      ------------
Provisional common equity value                       $291,806.577
```

NCI and nonoperating-investment adjustments remain zero only because V2 included no such bridge amounts and no supported September 23 market values are available. Zero is **not** evidence that the claims or assets are immaterial.

### 5. Consistent finance-lease convention

V3 applies a financing convention throughout:

- Finance-lease ROU amortization is included in EBIT and total D&A.
- Total D&A is added back in FCFF.
- New finance-lease ROU assets are treated as economic lease capex and deducted in FCFF.
- Finance-lease interest remains below EBIT and is excluded from FCFF.
- Finance-lease principal is a financing cash flow: it reduces cash and the lease liability but does not reduce FCFF.
- The closing finance-lease liability is rolled as opening liability + new lease additions − principal.
- The provisional July 31 finance-lease claim is subtracted once in the enterprise-to-equity bridge.

**Source-backed opening facts:** January 31 finance-lease liability $6,761; ROU asset $6,123; FY2026 ROU amortization $888; interest $383; new ROU assets $703; and principal payments $891, from the FY2026 10-K Note 6 and cash-flow disclosures.

**Provisional forecast assumptions:** V3 holds new lease additions at $703 and principal payments at $891 in each forecast year because no supported FY2027–FY2031 schedule is available. The liability declines by $188 per year under those assumptions.

**Sequential operating valuation impact:** enterprise and equity value decrease **$12,830.682**, and value per V2 share decreases **$1.599437** after the D&A correction. The separate July 31 bridge update then reduces equity value by $71 and value per V2 share by $0.008851.

## V3 five-year diagnostic forecast

| Year | Net sales | Membership/other income | EBIT | Total D&A | Finance-lease liability | FCFF |
|---:|---:|---:|---:|---:|---:|---:|
| 2027 | $736,788.8 | $7,040.2 | $33,223.9 | $14,203.0 | $6,573.0 | $13,118.4 |
| 2028 | 767,733.9 | 7,335.9 | 34,592.0 | 15,417.3 | 6,385.0 | 13,414.3 |
| 2029 | 798,443.2 | 7,629.4 | 35,917.1 | 16,709.8 | 6,197.0 | 14,702.3 |
| 2030 | 828,784.1 | 7,919.3 | 37,190.8 | 17,974.7 | 6,009.0 | 15,924.7 |
| 2031 | 857,791.5 | 8,196.5 | 38,215.8 | 19,214.7 | 5,821.0 | 16,912.9 |

FCFF is calculated as:

```text
FCFF = EBIT
     − assumed cash operating tax
     + total D&A
     − cash PP&E capex
     − new finance-lease ROU assets
     − change in defined operating NWC
```

Finance-lease interest and principal do not enter FCFF under the selected financing convention.

## V2-to-V3 sequential valuation reconciliation

The impacts below are sequential and order-dependent. Each row changes the stated item after all preceding rows; they should not be interpreted as independent sensitivities.

| Step | Enterprise value | Equity value | Per-share output | Change in EV | Change in equity | Sequential per-share impact |
|---|---:|---:|---:|---:|---:|---:|
| Historical V2 | $326,976.203 | $286,180.203 | **$35.674421** per FY2026 diluted weighted-average share | — | — | — |
| Correct revenue/net-sales formula | 350,472.621 | 309,676.621 | 38.603418 | +$23,496.417 | +$23,496.417 | **+$2.928997** |
| Reconcile D&A and asset rolls | 347,686.259 | 306,890.259 | 38.256078 | −2,786.362 | −2,786.362 | **−$0.347340** |
| Apply finance-lease forecast convention | 334,855.577 | 294,059.577 | 36.656641 | −12,830.682 | −12,830.682 | **−$1.599437** |
| Substitute July 31 cash proxy | 334,855.577 | 294,861.577 | 36.756616 | — | +802.000 | **+$0.099975** |
| Substitute July 31 debt fair-value proxy | 334,855.577 | 291,877.577 | 36.384639 | — | −2,984.000 | **−$0.371977** |
| Substitute July 31 finance leases | 334,855.577 | 291,806.577 | 36.375789 | — | −71.000 | **−$0.008851** |
| Substitute August 26 basic spot shares | 334,855.577 | 291,806.577 | **$36.780427 per basic share** | — | — | **+$0.404639** |

Total mechanical change from historical V2 to the V3 diagnostic proxy:

- Enterprise value: **+$7,879.373**.
- Equity value: **+$5,626.373**.
- Per-share output: **+$1.106007**, from $35.674421 on a historical weighted-average diluted denominator to $36.780427 on an August 26 basic spot denominator.

The total per-share comparison mixes denominator definitions by design to show the full V2-to-V3 transition. It is not evidence that $36.78 is a corrected September 23 diluted fair value.

## Validation results

| Check | Result |
|---|---|
| FY2026 opening assets reconcile to $284,668 | **PASS** |
| FY2026 opening claims and equity reconcile to $284,668 | **PASS** |
| Opening net sales + membership/other income = total revenue | **PASS** |
| Opening D&A proxy reconciles to reported $14,203 | **PASS** |
| Five annual balance sheets articulate | **PASS** — maximum absolute gap below $0.000001M |
| Five annual cash flows reconcile to balance-sheet cash | **PASS** — maximum absolute gap $0.000000M |
| Debt roll-forward | **PASS** — maximum absolute gap $0.000000M |
| Finance-lease liability roll-forward | **PASS** — maximum absolute gap $0.000000M |
| Nonnegative cash | **PASS** — minimum cash $10,303.6M |
| Minimum-cash requirement and revolver limit | **PASS** — maximum revolver $0.0M |
| Five-year FCFF horizon | **PASS** |
| WACC exceeds terminal growth | **PASS** — 7.00% > 2.50% |
| Enterprise-to-equity bridge arithmetic | **PASS** |
| Failed checks suppressed | **NO** — no check failed in the executed V3 base diagnostic |

## V3 diagnostic valuation

| Output | V3 result |
|---|---:|
| Present value of explicit FCFF | $60,185.8M |
| Present value of terminal value | $274,669.8M |
| Enterprise value | **$334,855.6M** |
| Provisional common equity value | **$291,806.6M** |
| Value per August 26 basic share | **$36.780427** |
| Terminal-value share | **82.03%** |

The WACC remains the provisional 7.00% and terminal growth remains 2.50%. V3 does not claim that either is final.

## Unresolved limitations

1. **Exact valuation-date dilution:** September 23 common shares and award-level dilution are unverified. The $36.78 output uses August 26 basic shares and therefore is not a final diluted value.
2. **Bridge dates:** cash, debt, and finance leases are July 31 observations, not September 23 observations.
3. **Excess cash:** V3 adds all $11,529 cash. Required operating cash, transfer restrictions, taxes, and NCI ownership are unresolved.
4. **Debt measurement:** $47,746 is a July 31 proxy combining short-term carrying value with long-term fair value. It is not a same-day September 23 instrument-level market value.
5. **D&A split:** $13,315 nonlease D&A includes unresolved PP&E depreciation and intangible amortization. Forecasting it from PP&E is provisional.
6. **Finance-lease forecast:** flat annual additions of $703 and principal of $891 use FY2026 historical amounts as assumptions, not management forecasts.
7. **Revenue-stream forecasts:** net sales and membership/other income use the same V2 growth path because separate supported forecasts were unavailable.
8. **Operating working capital:** V3 retains the V2 perimeter. Receivables, supplier finance within AP, prepaids, and other accrued liabilities remain unresolved.
9. **Operating leases:** operating-lease ROU assets and obligations remain excluded and held constant without a complete lease forecast.
10. **NCI and investments:** the bridge retains zero adjustments because supported September 23 market values and ownership allocations are unavailable. Zero does not mean immaterial.
11. **Taxes and capex:** the 24.5% cash-tax proxy and FY2027–FY2031 capex remain provisional V2 assumptions.
12. **Terminal-value concentration:** 82.03% of enterprise value comes from terminal value, making unresolved terminal margins, reinvestment, and lease assumptions material.

V3 improves definition consistency and passes its mechanical controls, but these unresolved facts must be reviewed before the model is used in a final investment memo.
