# Walmart Project 1 — Independent Source and Definition Check

**Scope:** Walmart Project 1 V2 FY2026 opening inputs and the related FCFF and enterprise-to-equity uses. No model or input was changed.

**Units:** USD millions except per-share amounts, ratios, days, and share counts. Walmart's statements are presented in millions except per-share data.

## Primary evidence and review standard

- [Walmart FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), fiscal year ended January 31, 2026, filed March 13, 2026, accession 0000104169-26-000055.
- [SEC filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/0000104169-26-000055-index.html).
- [Official SEC XBRL company facts for Walmart](https://data.sec.gov/api/xbrl/companyfacts/CIK0000104169.json). The facts cited below were filtered to the same FY2026 10-K accession, filing date, and fiscal period.

Status definitions:

- **PASS:** value, units, reporting period/date, and definition match the filing for the stated model use.
- **FAIL:** the model use has a material date or definition conflict with the filing measure.
- **NEEDS REVIEW:** the amount ties or is a transparent forecast assumption, but classification, period, scope, or valuation treatment is not sufficiently like-for-like for final use.

A numerical tie alone does not earn PASS.

## Priority input conclusions

| Input | Value and units used in V2 | FY2026 filing value | Exact filing locator and primary link | Date and definition comparison | Status and explanation |
|---|---:|---:|---|---|---|
| Revenue | **$713,163M** FY2026 opening revenue | **$713,163M total revenues**: $706,413M net sales plus $6,750M membership and other income | Item 8, Consolidated Statements of Income, p. 52; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, and `OtherIncome` | The value and FY2026 period match. The definition does not remain consistent in forecasting: V2 applies gross margin to total revenue, while Walmart's reported gross profit/cost of sales relationship is based on net sales, with membership and other income reported separately. | **NEEDS REVIEW.** The opening value is confirmed, but the forecast margin denominator blends unlike revenue components. |
| Operating income | No FY2026 opening EBIT input. FY2027 EBIT is derived as **$31,692.601M** | **$29,825M** for FY2026 | Item 8, Consolidated Statements of Income, p. 52; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `OperatingIncomeLoss` | The dates do not match: reported FY2026 versus modeled FY2027. The model amount is built from forecast total revenue, gross margin, cash SG&A, and modeled depreciation, not carried from the filing. | **NEEDS REVIEW.** No historical-to-forecast EBIT bridge exists; $31,692.601M must not be described as a sourced FY2026 value. |
| Cash and cash equivalents — opening balance | **$10,727M** at January 31, 2026 | **$10,727M** cash and cash equivalents | Item 8, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `CashAndCashEquivalentsAtCarryingValue` | Date, value, and balance-sheet definition match for the opening balance. The filing separately reports $11,321M of cash, cash equivalents, restricted cash and restricted cash equivalents, so the two cash measures must not be conflated. | **PASS** for the FY2026 opening balance. |
| Cash in equity bridge | **+$10,727M** | Same reported balance, **$10,727M** | Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) | The amount is dated January 31, not the proposed September 23, 2026 valuation date. The filing does not identify the full balance as excess, unrestricted, transferable cash available to common equity holders. | **NEEDS REVIEW.** Source amount is confirmed; full-add treatment and valuation date are not. |
| Short-term and long-term borrowings — FY2026 opening | **$44,762M** total debt | $6,596M short-term borrowings + $3,542M current long-term debt + $34,624M noncurrent long-term debt = **$44,762M** | Item 8, Consolidated Balance Sheets, p. 54; Note 5, “Short-term Borrowings and Long-term Debt,” pp. 65–67; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `ShortTermBorrowings`, `LongTermDebtCurrent`, and `LongTermDebtNoncurrent` | Date and carrying-value definition match the opening debt balance. Finance leases are reported separately and are not duplicated in this sum. | **PASS** for the January 31 carrying-value opening balance. |
| Borrowings in equity bridge | **−$44,762M** | Same January 31 carrying-value sum | Consolidated Balance Sheets and Note 5; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) | Carrying value is not market value and is not dated September 23. Note 7 reports a separate $36,777M fair value for $38,166M of long-term-debt carrying value; that is an alternative measure, not an additional liability. | **NEEDS REVIEW.** The arithmetic is complete, but the date and valuation convention are not final. |
| Finance lease liabilities | **$6,761M** opening liability and bridge deduction | $856M current + $5,905M noncurrent = **$6,761M** | Consolidated Balance Sheets, p. 54; Note 6, “Leases,” pp. 67–69; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `FinanceLeaseLiability`, `FinanceLeaseLiabilityCurrent`, and `FinanceLeaseLiabilityNoncurrent` | The January 31 value and liability definition match. The filing also reports a $6,123M finance-lease ROU asset, $888M amortization, and $383M interest. V2 subtracts the liability, models interest below EBIT, holds the liability and ROU asset constant, and does not separately trace principal or ROU amortization through FCFF. | **NEEDS REVIEW.** The source amount passes, but the lease convention is not fully reconciled and is dated January 31. |
| Diluted weighted-average shares | **8,022M** used as the valuation denominator | **8,022M FY2026 diluted weighted-average shares** = 7,983M basic + 39M dilutive awards | Item 8, Note 2, “Net Income Per Common Share,” p. 63; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `WeightedAverageNumberOfDilutedSharesOutstanding`, `WeightedAverageNumberOfSharesOutstandingBasic`, and `WeightedAverageNumberDilutedSharesOutstandingAdjustment` | The amount and FY2026 earnings-period definition match the filing. They do **not** match a period-end or September 23 diluted equity-claim count. Weighted-average shares measure earnings allocation during FY2026, not claims outstanding at the valuation date. | **FAIL** for valuation-denominator use. The historical filing fact is correct, but its definition and date are wrong for a point-in-time DCF denominator. |
| Depreciation and amortization | No FY2026 expense input. V2 forecasts FY2027 depreciation as **10.6% × $136,083M opening net PP&E = $14,424.798M** | **$14,203M** FY2026 depreciation and amortization | Item 8, Consolidated Statements of Cash Flows, p. 56; Note 6 for finance-lease amortization; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `DepreciationAmortizationAndAccretionNet` and `FinanceLeaseRightOfUseAssetAmortization` | Date and definition do not match. Reported D&A includes property and equipment, finance-lease property, and intangible assets; V2 applies one assumed rate only to ending net PP&E and does not separately trace $888M of reported finance-lease ROU amortization. | **FAIL** as a source/definition match. The FY2027 amount is a model assumption, not the FY2026 filing amount. |
| Capital expenditures | FY2027 forecast **$26,000M**; no FY2026 capex input | **$26,642M** FY2026 payments to acquire property and equipment | Item 8, Consolidated Statements of Cash Flows, p. 56; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `PaymentsToAcquirePropertyPlantAndEquipment` | Both are cash capex concepts, but the periods and amounts differ. The $26,000M is a FY2027 forecast assumption, $642M below FY2026, not a filing fact. | **NEEDS REVIEW.** Correctly label as forecast and document its guidance/maintenance-versus-growth basis before final use. |
| Net PP&E opening balance | **$136,083M** | **$136,083M** property and equipment, net | Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `PropertyPlantAndEquipmentNet` | January 31 value and definition match. Operating- and finance-lease ROU assets are shown separately in both the filing and V2. | **PASS** for the opening balance; this does not validate the 10.6% depreciation rate. |
| Cost of sales used for historical working-capital days | **$535,395M** | **$535,395M** FY2026 cost of sales/cost of revenue | Consolidated Statements of Income, p. 52; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `CostOfRevenue` | The historical amount and period match. V2 correctly derives 40.1211 inventory days and 42.9912 AP days from it. Forecast cost of sales, however, is defined as total modeled revenue less modeled gross profit, while the filing's cost of sales is linked to net sales. | **NEEDS REVIEW.** Historical arithmetic passes; forecast denominator consistency does not. |

## Working-capital and related classification check

V2 defines operating NWC as receivables plus inventory less accounts payable and four identified operating accruals. It excludes cash, prepaids/other, leases, goodwill, other long-term assets, taxes, debt, NCI, and mixed/noncurrent balances. The following table tests both the reported amount and the model's classification.

| V2 balance and treatment | Model value | Filing value and locator | Date/definition assessment | Status |
|---|---:|---|---|---|
| Receivables, net — included as operating | **$11,172M** | **$11,172M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `ReceivablesNetCurrent` | Amount/date match. The filing says the line includes customer and supplier receivables but also tax and real-estate receivables. The $4,900M tagged accounts-receivable subset is not the same as the full $11,172M balance-sheet line. Treating all $11,172M as operating is not independently supported. | **NEEDS REVIEW** |
| Inventory — included as operating | **$58,851M** | **$58,851M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `InventoryNet` | Amount, date, current-asset definition, and operating classification match. Future constant days remain a forecast assumption, not a filing fact. | **PASS** |
| Accounts payable — included as operating | **$63,061M** | **$63,061M**, Consolidated Balance Sheets, p. 54; supplier-finance disclosure; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `AccountsPayableCurrent` and `SupplierFinanceProgramObligation` | Amount/date match. The line includes **$5,989M** of supplier-finance obligations that Walmart presents in AP and operating cash flow. Presentation is confirmed, but valuation classification as operating versus financing remains a policy question. | **NEEDS REVIEW** |
| Accrued wages and benefits — included as operating | **$7,878M** | **$7,878M**, Note 4, “Accrued Liabilities”; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `EmployeeRelatedLiabilitiesCurrent` | Amount/date and employee-related current operating-liability definition match. | **PASS** |
| Self-insurance — included as operating | **$5,525M** | **$5,525M**, Note 4; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `SelfInsuranceReserveCurrent` | Amount/date and reserve definition match an operating accrual. The reserve balance is not the same measure as FY2026 claims expense or the approximately $900M expense increase. | **PASS** for the opening balance; future revenue scaling is an assumption. |
| Accrued non-income taxes — included as operating | **$4,110M** | **$4,110M**, Note 4; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `AccrualForTaxesOtherThanIncomeTaxesCurrent` | Amount/date and non-income-tax operating-accrual definition match. | **PASS** |
| Deferred gift-card revenue — included as operating | **$2,941M** | **$2,941M**, Note 4, “Accrued Liabilities”; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) | Amount/date and deferred-revenue definition match. The future constant revenue ratio is a model assumption. | **PASS** for the opening balance. |
| Prepaid expenses and other — excluded and held constant | **$4,124M** | **$4,124M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `PrepaidExpenseAndOtherAssetsCurrent` | Amount/date match. The label is mixed; excluding the entire line avoids inventing a split but omits any operating prepaid portion from NWC. | **NEEDS REVIEW** |
| Other accrued liabilities — excluded and held constant | **$10,733M** | **$10,733M**, Note 4; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `OtherAccruedLiabilitiesCurrent` | Amount/date match. The filing description includes deferred membership revenue and supply-chain, advertising, maintenance, and utilities accruals, as well as interest. Full exclusion removes operating items together with financial items. | **NEEDS REVIEW** |
| Accrued income taxes — excluded | **$596M** | **$596M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `AccruedIncomeTaxesCurrent` | Amount/date match. Exclusion from operating NWC can be consistent with a separately modeled cash-tax convention, but V2 assumes tax expense equals cash operating tax and does not roll the tax payable. | **NEEDS REVIEW** |
| Operating-lease ROU asset — excluded and held constant | **$14,750M** | **$14,750M**, Consolidated Balance Sheets and Note 6; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `OperatingLeaseRightOfUseAsset` | Amount/date and lease-asset definition match; exclusion from ordinary NWC is appropriate. Holding the asset and related obligation constant without a lease roll-forward is not an economic forecast. | **NEEDS REVIEW** |
| Operating-lease obligations — excluded and held constant | **$15,572M** | $1,631M current + $13,941M noncurrent = **$15,572M**, Consolidated Balance Sheets and Note 6; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `OperatingLeaseLiability` | Amount/date match. V2 retains operating treatment and does not subtract this claim in the bridge, but the forecast lacks a complete rent/ROU/liability roll-forward. | **NEEDS REVIEW** |
| Finance-lease ROU asset — excluded and held constant | **$6,123M** | **$6,123M**, Consolidated Balance Sheets and Note 6; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `FinanceLeaseRightOfUseAsset` | Amount/date match. It is correctly excluded from ordinary NWC, but holding it flat while subtracting the liability and forecasting PP&E-based depreciation leaves the asset/amortization convention incomplete. | **NEEDS REVIEW** |
| Goodwill — excluded and held constant | **$28,735M** | **$28,735M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `Goodwill` | Amount/date match. Goodwill is not current working capital; exclusion from NWC is definitionally appropriate. | **PASS** for NWC classification. |
| Other long-term assets — excluded and held constant | **$14,103M** | **$14,103M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `OtherAssetsNoncurrent` | Amount/date match. The line includes investments, deferred-tax assets, intangibles, and unresolved operating/nonoperating assets. Exclusion from current NWC is appropriate, but holding it flat and omitting verified nonoperating assets from the bridge are separate unresolved choices. | **NEEDS REVIEW** |
| Deferred income taxes and other liabilities — excluded and held constant | **$16,549M** | **$16,549M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `DeferredIncomeTaxesAndOtherLiabilitiesNoncurrent` | Amount/date match. The mixed line is not current operating NWC, but the model does not forecast its tax, derivative, indemnity, or other components. | **NEEDS REVIEW** |
| Redeemable NCI — excluded and held constant | **$293M** | **$293M**, Consolidated Balance Sheets, p. 54; [10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm); SEC XBRL `RedeemableNoncontrollingInterestEquityCarryingAmount` | Amount/date match and NCI is not operating NWC. The provisional DCF bridge does not separately subtract a market value for redeemable or nonredeemable NCI. | **NEEDS REVIEW** |

### Opening operating-NWC arithmetic

The V2 defined balance is arithmetically correct using its selected lines:

```text
Receivables                                      $11,172
+ Inventory                                       58,851
− Accounts payable                               (63,061)
− Accrued wages and benefits                      (7,878)
− Self-insurance                                  (5,525)
− Accrued non-income taxes                        (4,110)
− Deferred gift-card revenue                      (2,941)
                                                 --------
Defined operating NWC                           $(13,492)
```

This is a model-defined subtotal, not a Walmart-reported measure. The arithmetic passes; the receivables and supplier-finance classifications remain unresolved, and the total excludes operating components that may be embedded in prepaids and other accrued liabilities.

## Confirmed filing facts versus model assumptions

### Confirmed filing facts

- FY2026 total revenue $713,163M and operating income $29,825M.
- January 31 cash $10,727M; carrying-value borrowings $44,762M; finance-lease liability $6,761M.
- FY2026 diluted weighted-average shares 8,022M.
- FY2026 D&A $14,203M and cash capex $26,642M.
- The individually listed January 31 balance-sheet and Note 4 working-capital amounts above.

### Model assumptions or valuation policies—not filing facts

- Revenue growth, gross margins, cash SG&A ratios, 10.6% depreciation rate, FY2027–FY2031 capex, 24.5% cash-tax proxy, and constant working-capital ratios/days.
- Treating total revenue as the gross-margin base.
- Treating all $10,727M as nonoperating/excess cash.
- Using January 31 carrying-value debt and finance leases in a September 23 bridge.
- Using FY2026 weighted-average diluted shares as a point-in-time valuation denominator.
- Holding mixed, lease, tax, NCI, and other excluded balances constant.

## Highest-risk remaining issues

1. **Share denominator — highest direct per-share risk.** The 8,022M value is correctly sourced but definitionally wrong for a September 23 point-in-time valuation. It combines an FY2026 average basic count with FY2026 treasury-stock dilution.
2. **Revenue and margin definition.** V2 forecasts gross profit on total revenue even though the filing distinguishes $706,413M net sales from $6,750M membership and other income and relates cost of sales to net sales. This can distort gross margin, EBIT, and every downstream cash flow.
3. **D&A and lease consistency.** Reported D&A covers more asset classes than the model's PP&E-only driver. Finance-lease assets, amortization, interest, principal, and liabilities are not fully rolled together, creating double-counting or omission risk.
4. **Equity-bridge date and measurement.** Cash, carrying-value borrowings, and finance leases are January 31 balances, not September 23 values. Full cash availability, debt market value, NCI, and nonoperating investment adjustments remain unresolved.
5. **Operating-NWC perimeter.** Receivables include nonoperating items; AP includes $5,989M of supplier finance; prepaids and other accrued liabilities contain operating items that V2 excludes. The current subtotal is transparent but not yet economically complete.
6. **Historical-to-forecast bridge.** No explicit FY2026 operating-income or D&A base flows into FY2027. Consequently, the first forecast year cannot be explained cleanly through volume, price/mix, margins, normalization, depreciation, and reinvestment changes.
7. **Capex definition.** FY2027 $26,000M is a forecast rather than the reported $26,642M. Maintenance versus growth capex and the resulting depreciation/returns are not separately supported.

## Corrections required before finalizing the investment memo

1. Replace the 8,022M historical average denominator with a documented September 23 basic share count plus award-specific dilution; do not mix weighted-average and period-end concepts.
2. Split the forecast into net sales and membership/other income, or demonstrate explicitly why applying one margin to total revenue produces an equivalent result.
3. Add a FY2026-to-FY2027 operating bridge beginning with $29,825M reported EBIT and $14,203M reported D&A, with every normalization and forecast change separately sourced or labeled as an assumption.
4. Build an integrated PP&E, intangible-amortization, finance-lease, and operating-lease roll-forward so EBIT, FCFF, invested capital, and bridge claims use one consistent lease convention.
5. Rebuild the valuation-date equity bridge using valuation-date cash, debt, lease, investment, and NCI evidence; define excess cash and choose carrying or market debt consistently with WACC weights.
6. Refine operating NWC by separating nonoperating receivables, evaluating supplier financing as operating versus financing, and identifying operating portions of prepaids and other accrued liabilities. Do not add or subtract an item in the bridge if it remains embedded in operating cash flow.
7. Document FY2027 capex as maintenance and growth components where support exists, and connect them to asset growth, depreciation, and terminal reinvestment.

Until these corrections are completed, the V2 model remains useful as a controlled diagnostic model, but its per-share output should not be presented as a finalized investment-memo fair value.
