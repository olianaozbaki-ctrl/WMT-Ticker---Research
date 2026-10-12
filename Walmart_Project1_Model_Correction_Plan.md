# Walmart Project 1 — Model Correction Plan

**Purpose:** Prioritize the `FAIL` and `NEEDS REVIEW` findings in `Walmart_Project1_Independent_Source_Check.md` according to their effect on Walmart Project 1 V2 value per share.

**Scope:** Planning only. No model, input, validation file, or prior evidence file was changed.

## How to read the classifications

- **MUST FIX:** Resolve before presenting V2 as a final September 23, 2026 fair value. This classification includes confirmed errors and unresolved choices capable of materially changing FCFF, the equity bridge, or the share denominator.
- **SHOULD FIX:** Important to model credibility or potentially material, but can be addressed with a documented sensitivity if primary evidence cannot support a unique correction.
- **DOCUMENT AS LIMITATION:** No supported adjustment is currently available, or likely effect is secondary after the higher-priority corrections. Do not silently estimate a number.

`MUST FIX` does not automatically mean the current number is proven wrong. The “finding type” column distinguishes confirmed errors from unresolved policy or classification questions.

At the current provisional 8,022 million-share denominator, a $1,000 million change in enterprise-to-equity bridge value changes value per share by approximately **$0.1247**. This is a scale reference only, not a proposed adjustment.

## Priority summary

| Priority | Issue | Finding type | Classification | Primary valuation channel |
|---:|---|---|---|---|
| 1 | Valuation-date diluted share count | **Confirmed definition/date error** | **MUST FIX** | Per-share denominator |
| 2 | Total revenue versus net-sales margin basis | **Confirmed formula/filing-definition mismatch** | **MUST FIX** | Revenue, gross profit, EBIT, FCFF, terminal value |
| 3 | D&A definition and fixed-asset roll-forward | **Confirmed source/definition mismatch** | **MUST FIX** | EBIT, taxes, FCFF, PP&E, terminal value |
| 4 | Valuation-date cash and debt bridge | **Confirmed date mismatch; measurement policy unresolved** | **MUST FIX** | Direct equity-value adjustment |
| 5 | Finance-lease convention | **Unresolved policy and consistency risk** | **MUST FIX** | EBIT/FCFF and direct bridge claim |
| 6 | Operating working-capital perimeter | **Unresolved classification risk** | **SHOULD FIX** | Annual FCFF and terminal value; possible bridge reclassification |
| 7 | FY2026-to-FY2027 operating-income bridge | **Missing reconciliation, not a proven numerical error** | **SHOULD FIX** | Forecast credibility and normalization |
| 8 | Capex basis and maintenance/growth split | **Forecast assumption requiring support** | **SHOULD FIX** | Annual FCFF, depreciation, terminal reinvestment |
| 9 | Operating-lease forecast treatment | **Unresolved forecast-policy choice** | **SHOULD FIX** | EBIT, FCFF, invested capital, possible debt adjustment |
| 10 | Nonoperating assets and NCI | **Unresolved bridge classification and measurement** | **SHOULD FIX** | Direct equity-value additions/deductions |
| 11 | Cash-tax and tax-balance consistency | **Unresolved forecast simplification** | **SHOULD FIX** | NOPAT, FCFF, balance-sheet articulation |
| 12 | Residual mixed balances held constant | **Known limitation with incomplete disclosure** | **DOCUMENT AS LIMITATION** | Secondary forecast and terminal-value risk |

## Detailed correction plan

### 1. Replace the historical weighted-average share denominator

**Classification: MUST FIX — confirmed error for valuation use.**

1. **What is wrong:** The 8,022 million figure is correctly reported, but it is the average diluted share count used to calculate FY2026 EPS. A DCF divides equity value by equity claims outstanding at the valuation date. An annual average and a September 23 point-in-time count are different definitions.
2. **Model input or formula:** `project1_fcff_v2.py` uses `DILUTED_SHARES_M = 8_022.0`; `per_share = equity_value / DILUTED_SHARES_M`.
3. **Potential value-per-share effect:** This changes value per share directly and inversely. A lower defensible valuation-date diluted count raises value per share; a higher count lowers it. Enterprise and equity value are unchanged. The direction cannot be selected until spot shares and dilution are measured consistently.
4. **SEC evidence needed:** The FY2026 10-K Note 2 confirms that 8,022 million is weighted-average diluted shares. Obtain the closest pre-valuation-date Form 10-Q cover-page shares outstanding, the statement-of-equity repurchase and issuance activity, and share-compensation disclosures for options, restricted stock, and performance awards. If SEC filings do not report an exact September 23 count, document a roll-forward from the latest filed spot count and calculate award dilution using a stated method and September 23 market price.
5. **Correction action:** Replace 8,022 million only after building a dated basic-plus-dilution schedule. Preserve 8,022 million as a historical EPS cross-check, not the valuation denominator.

### 2. Separate net sales from membership and other income

**Classification: MUST FIX — confirmed formula/definition mismatch.**

1. **What is wrong:** Walmart reports $706,413 million of net sales and $6,750 million of membership and other income within $713,163 million of total revenue. V2 applies one gross-margin percentage to total revenue and then defines cost of sales as total revenue less gross profit. This is not the filing's net-sales/cost-of-sales presentation.
2. **Model input or formula:** `OPENING["revenue"] = 713_163.0`; forecast `gross_profit = revenue * gross_margin`; forecast `cost_of_sales = revenue - gross_profit`; inventory and AP are projected from that cost-of-sales amount.
3. **Potential value-per-share effect:** The formula affects gross profit, EBIT, taxes, inventory, AP, FCFF, and terminal value. The direction is not known without separate forecasts: treating higher-margin membership or other income like merchandise sales could overstate cost of sales or misstate margin, but recalibrated margin assumptions could offset part of the effect.
4. **SEC evidence needed:** FY2026 Consolidated Statements of Income for net sales, membership and other income, cost of sales, and operating expenses; MD&A and segment disclosures describing membership, advertising, marketplace, and other higher-margin activities; subsequent 10-Q revenue and margin disclosures.
5. **Correction action:** Forecast net sales and membership/other income separately, calculate merchandise cost of sales against net sales, and connect inventory/AP drivers to the appropriate cost base. If a single blended approach is retained, demonstrate that its gross profit and working-capital results reconcile to a separated version.

### 3. Rebuild D&A from consistent asset classes

**Classification: MUST FIX — confirmed source/definition mismatch.**

1. **What is wrong:** V2 has no FY2026 D&A input and forecasts FY2027 depreciation as 10.6% of $136,083 million of opening net PP&E. Walmart's $14,203 million reported D&A includes PP&E, finance-lease assets, and intangible assets. The modeled amount and reported amount are not the same period or definition.
2. **Model input or formula:** `DEPRECIATION_TO_OPENING_PPE = 0.106`; `depreciation = prior["ppe"] * depreciation_to_opening_ppe`; `ppe = prior["ppe"] + capex - depreciation`; EBIT subtracts this depreciation and FCFF adds it back after tax.
3. **Potential value-per-share effect:** D&A changes EBIT, tax shields, FCFF, the PP&E roll-forward, and later depreciation. Because D&A is both deducted in EBIT and added back in FCFF, changing it does not affect FCFF dollar-for-dollar; tax and asset-roll-forward effects remain. Direction is therefore not supportable until the corrected asset schedule is built.
4. **SEC evidence needed:** FY2026 cash-flow-statement D&A of $14,203 million; gross and net PP&E and accumulated depreciation; Note 6 finance-lease ROU asset and $888 million amortization; identifiable-intangible balances and amortization disclosures; FY2026 and interim capex and asset-disposal evidence.
5. **Correction action:** Create separate PP&E depreciation, finance-lease ROU amortization, and intangible-amortization schedules. Tie their FY2026 total to reported D&A and roll each asset class independently through FY2031.

### 4. Rebuild cash and debt at the valuation date

**Classification: MUST FIX — confirmed date mismatch; final measurement remains unresolved.**

1. **What is wrong:** The $10,727 million cash addition and $44,762 million debt deduction are confirmed January 31 balances, but the proposed valuation date is September 23. The model also assumes all cash is excess and uses debt carrying value without completing a valuation-date market-value assessment.
2. **Model input or formula:** `CASH_M = 10_727.0`; `BORROWINGS_M = 44_762.0`; `equity_value = enterprise_value + cash - borrowings - lease_claim`.
3. **Potential value-per-share effect:** Bridge changes pass one-for-one into equity value. Less excess cash lowers value; more excess cash raises it. More debt lowers value; less debt raises it. At the current share denominator, each $1 billion net bridge change is about $0.1247 per share, before correcting the denominator.
4. **SEC evidence needed:** July 2026 Form 10-Q balance sheet and debt notes, subsequent borrowing/repayment disclosures, restricted-cash information, subsidiary cash and transfer restrictions, and any SEC-filed events between July 31 and September 23. For debt, obtain instrument-level principal/carrying value and available fair-value disclosures; do not add maturity-table amounts to the same balance-sheet debt.
5. **Correction action:** Roll cash and debt to September 23 or use the closest supported date with a transparent limitation. Define minimum operating cash and excess cash. Choose carrying or market debt consistently with the WACC capital weights and provide a sensitivity where market evidence is incomplete.

### 5. Select and implement one finance-lease convention

**Classification: MUST FIX — unresolved, but capable of material double counting.**

1. **What is wrong:** The $6,761 million liability is correctly sourced. The unresolved issue is treatment: V2 subtracts it from enterprise value and models lease interest below EBIT, while holding the $6,123 million ROU asset and liability constant and not separately tracing ROU amortization or principal. This can omit costs or count the same financing burden twice.
2. **Model input or formula:** `FINANCE_LEASES_M = 6_761.0`; `INCLUDE_FINANCE_LEASES_IN_BRIDGE = True`; finance-lease interest enters pretax income; the ROU asset is `finance_lease_rou_excluded`; the obligation is held constant.
3. **Potential value-per-share effect:** The direct liability is large enough to affect the bridge materially, but simply adding back $6,761 million is not a valid alternative unless EBIT, FCFF, assets, and WACC are recast consistently. Direction is indeterminate until the entire convention is changed together.
4. **SEC evidence needed:** Note 6 current/noncurrent liabilities, ROU assets, amortization, interest, principal payments, new ROU assets obtained, and maturity schedules; the latest 10-Q lease balances and activity.
5. **Correction action:** Under a financing convention, exclude finance-lease interest and principal from FCFF, include operating asset benefits and appropriate amortization in EBIT, roll the asset/liability, and subtract the valuation-date liability. Under an operating convention, recast all related expenses and do not also deduct the same claim. Document a double-counting check.

### 6. Refine the operating working-capital perimeter

**Classification: SHOULD FIX — several classifications remain unproven, not confirmed errors.**

1. **What is wrong:** V2 includes all $11,172 million of receivables as operating even though the line contains tax and real-estate amounts. It includes all $63,061 million of AP even though $5,989 million is supplier finance. It excludes all $4,124 million of prepaids and all $10,733 million of other accrued liabilities even though both contain operating items. These are transparent choices, but none is a complete operating/nonoperating split.
2. **Model input or formula:** `OPERATING_ASSET_KEYS`, `OPERATING_LIABILITY_KEYS`, `operating_nwc()`, `receivables_to_revenue`, `inventory_days`, `accounts_payable_days`, and `operating_accruals_to_revenue`; FCFF subtracts `change_operating_nwc`.
3. **Potential value-per-share effect:** Reclassification changes annual FCFF and terminal FCFF. Supplier finance can also move from operating NWC to the equity bridge; changing only one side could create an omission or double count. The direction depends on opening classifications and forecast changes, so no adjustment should be assumed.
4. **SEC evidence needed:** Receivables accounting-policy detail, Note 4 accrued-liability composition, supplier-finance balance and cash-flow disclosures, prepaids/other detail, and subsequent 10-Q balances. Obtain enough history to test whether the selected drivers are stable.
5. **Correction action:** Build a classification matrix for each account: operating NWC, financing claim, tax, investment, or excluded residual. Reforecast only supported operating components. For unresolved portions, run explicit high/low classification sensitivities rather than forcing a split.

### 7. Add a FY2026-to-FY2027 EBIT bridge

**Classification: SHOULD FIX — missing control, not a proven numerical error.**

1. **What is wrong:** Reported FY2026 EBIT is $29,825 million, but V2 begins with a derived FY2027 EBIT of $31,692.601 million. The model does not show how sales, membership/other income, margin, expense leverage, D&A, or normalization explain the change.
2. **Model input or formula:** FY2027 `revenue_growth`, `gross_margin`, `cash_sga_to_gross_profit`, and `depreciation_to_opening_ppe`; `operating_income = gross_profit - cash_sga - depreciation`.
3. **Potential value-per-share effect:** The bridge itself does not change valuation. It can reveal unsupported margin or expense assumptions that change all five EBIT and FCFF forecasts and terminal value.
4. **SEC evidence needed:** FY2026 income statement and MD&A; disclosed self-insurance claims pressure, PhonePe compensation, and other operating items; FY2027 guidance and subsequent 10-Q operating results.
5. **Correction action:** Produce a numerical bridge from $29,825 million to FY2027 EBIT. Separate reported facts, normalizations, growth/mix, gross margin, operating expenses, and D&A. Do not normalize an item merely because it is unusual.

### 8. Support capex and terminal reinvestment

**Classification: SHOULD FIX — forecast assumption, not a confirmed error.**

1. **What is wrong:** The FY2027 $26,000 million capex assumption is not the reported FY2026 $26,642 million. That is acceptable for a forecast, but the model does not separate maintenance from growth spending or connect spending to asset productivity and terminal growth.
2. **Model input or formula:** `CAPEX` for FY2027–FY2031; PP&E roll-forward; FCFF deducts annual capex; terminal value capitalizes FY2031 FCFF.
3. **Potential value-per-share effect:** Higher capex lowers near-term FCFF but may support later growth and depreciation; lower capex does the reverse. An unsupported terminal capex level can materially overstate or understate terminal FCFF.
4. **SEC evidence needed:** FY2026 cash-flow capex, MD&A capital-allocation guidance, PP&E additions/disposals, store and supply-chain investment disclosures, later 10-Q capex, and any maintenance/growth description Walmart provides.
5. **Correction action:** Document annual capex by purpose where evidence supports it, link additions to depreciation and revenue capacity, and test whether terminal capex and D&A are consistent with 2.5% terminal growth.

### 9. Complete operating-lease forecasting

**Classification: SHOULD FIX — unresolved policy choice, not a confirmed bridge error.**

1. **What is wrong:** V2 excludes and holds constant the $14,750 million operating-lease ROU asset and $15,572 million liability. Exclusion from ordinary NWC is reasonable, but a flat asset/liability with no complete rent and renewal roll-forward is not an economic forecast.
2. **Model input or formula:** `operating_lease_rou_excluded`, `operating_lease_obligations_excluded`, excluded-balance constancy checks, cash SG&A, and the absence of an operating-lease bridge deduction.
3. **Potential value-per-share effect:** Retaining operating treatment versus capitalizing leases changes EBIT, FCFF timing, invested capital, debt, WACC, and the equity bridge. Direction is not knowable from the liability alone.
4. **SEC evidence needed:** Note 6 operating-lease cost, payments, ROU additions, current/noncurrent liabilities, maturity schedule, discount rate, and subsequent 10-Q updates.
5. **Correction action:** Either maintain operating treatment with a supported lease-expense/cash-payment forecast or capitalize leases and recast every affected valuation component. Do not subtract operating leases while leaving full lease costs in FCFF.

### 10. Reconcile nonoperating investments and NCI

**Classification: SHOULD FIX — unresolved bridge items, not proven omissions at market value.**

1. **What is wrong:** Other long-term assets contain investments and other mixed assets, while V2 holds them flat and adds no separate nonoperating investment value. Redeemable NCI of $293 million is excluded from NWC, and nonredeemable NCI remains within consolidated equity, but the DCF bridge deducts neither at a supported market value.
2. **Model input or formula:** `other_long_term_assets_excluded`, `redeemable_nci_excluded`, total equity/opening claims, and the bridge formula in `project1_fcff_v2.py`, which adjusts only cash, borrowings, and finance leases.
3. **Potential value-per-share effect:** Adding genuinely nonoperating investments increases equity value; subtracting NCI claims decreases it. If an investment or subsidiary cash flow remains in FCFF, adding its asset value again would overstate value. Direction and amount require a perimeter reconciliation.
4. **SEC evidence needed:** Note 7 investment balances and fair values; subsidiary ownership and PhonePe disclosures; redeemable and nonredeemable NCI balances, income attribution, redemption terms, and subsequent ownership changes; latest 10-Q values.
5. **Correction action:** Map each investment and subsidiary to consolidated FCFF. Add only assets excluded from enterprise value and subtract only equity claims not already captured, using a supported valuation-date measure. Where market value cannot be established, disclose carrying-value sensitivities without calling them final.

### 11. Align cash taxes with tax balances

**Classification: SHOULD FIX — unresolved simplification, not a confirmed numerical error.**

1. **What is wrong:** V2 applies a 24.5% cash tax rate to positive EBIT while holding accrued income taxes and deferred taxes/other constant. Tax expense, cash taxes, and balance-sheet tax changes are not the same measure.
2. **Model input or formula:** `CASH_TAX_RATE = 0.245`; `cash_operating_tax = EBIT × cash_tax_rate`; `accrued_income_taxes_excluded`; `deferred_income_taxes_and_other_excluded`.
3. **Potential value-per-share effect:** A higher sustainable cash-tax rate lowers NOPAT and FCFF; a lower rate raises them. Deferred-tax and timing differences can also change cash flow without changing statutory expense in the same period.
4. **SEC evidence needed:** Income-tax note, current and deferred tax expense, cash taxes paid, credits, NOLs, uncertain tax positions, accrued income taxes, deferred-tax balances, and interim updates.
5. **Correction action:** Build a cash-tax forecast or, at minimum, reconcile the 24.5% proxy to reported current tax, cash payments, and expected discrete items. If a simple rate remains, hold tax-balance movements outside FCFF only with an explicit limitation and sensitivity.

### 12. Preserve unsupported residuals transparently

**Classification: DOCUMENT AS LIMITATION — no defensible split currently exists.**

1. **What is wrong:** Some mixed long-term assets, deferred-tax-and-other liabilities, and excluded balances cannot be separated from the available filing evidence. Holding them constant is transparent but not an economic forecast.
2. **Model input or formula:** `EXCLUDED_ASSET_KEYS`, `EXCLUDED_LIABILITY_KEYS`, and the check that these balances remain unchanged.
3. **Potential value-per-share effect:** Acquisitions, disposals, FX, derivatives, deferred taxes, impairments, and other movements could affect cash flow or the bridge. Direction and magnitude are unknown.
4. **SEC evidence needed:** Detailed footnotes and later 10-Q roll-forwards for material components. If the filing does not disaggregate a balance, no exact correction can be claimed.
5. **Correction action:** Keep the fail-loud constancy check, list every unsupported component, and run sensitivities for material residuals. Do not create balancing plugs or invented line-item splits.

## Finding-to-plan coverage

| Source-check finding | Plan item | Disposition |
|---|---:|---|
| Revenue and forecast cost-of-sales definition | 2 | MUST FIX |
| No FY2026 operating-income input | 7 | SHOULD FIX |
| Cash in equity bridge | 4 | MUST FIX |
| Borrowings in equity bridge | 4 | MUST FIX |
| Finance-lease liability and ROU asset | 3 and 5 | MUST FIX |
| Diluted weighted-average shares | 1 | MUST FIX |
| D&A | 3 | MUST FIX |
| Capex | 8 | SHOULD FIX |
| Receivables classification | 6 | SHOULD FIX |
| AP and supplier finance | 6 | SHOULD FIX |
| Prepaids and other accrued liabilities | 6 | SHOULD FIX |
| Accrued income taxes | 11 | SHOULD FIX |
| Operating-lease ROU asset and obligations | 9 | SHOULD FIX |
| Other long-term assets and investments | 10 and 12 | SHOULD FIX / DOCUMENT AS LIMITATION |
| Deferred taxes and other liabilities | 11 and 12 | SHOULD FIX / DOCUMENT AS LIMITATION |
| Redeemable and nonredeemable NCI | 10 | SHOULD FIX |

## Recommended implementation order

1. **Fix the operating model perimeter:** separate revenue definitions, rebuild D&A/assets/leases, and refine operating NWC.
2. **Re-run the five-year statements and FCFF controls:** preserve balance-sheet and cash-flow articulation and report any new financing failure.
3. **Rebuild the September 23 bridge:** cash, debt, leases, investments, and NCI under the same operating perimeter used in FCFF and WACC.
4. **Build the valuation-date diluted share count:** apply it only after equity value is finalized.
5. **Re-run scenarios and sensitivities:** distinguish parameter uncertainty from definition corrections.
6. **Update the investment memo last:** label any still-unresolved items as limitations and do not describe diagnostic outputs as final fair value.

The first five `MUST FIX` items should be resolved together because changing only one can create a new inconsistency. In particular, lease liabilities cannot be changed independently of lease expense and FCFF, and supplier finance cannot be moved from AP without addressing both operating NWC and the equity bridge.
