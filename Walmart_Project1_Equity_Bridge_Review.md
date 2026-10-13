# Walmart Project 1 — Equity Bridge Review

**Status:** Review only. No model input, enterprise-to-equity bridge, or final bridge has been selected or changed.

**Proposed valuation date:** September 23, 2026. **Reporting basis reviewed:** Walmart's fiscal year ended January 31, 2026. Unless stated otherwise, dollar amounts are in **USD millions** and share counts are in **millions of shares**.

## Sources and date convention

- Walmart FY2026 Form 10-K, fiscal year ended January 31, 2026, filed March 13, 2026: [primary filing](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) and [SEC filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/0000104169-26-000055-index.html).
- Walmart FY2027 second-quarter Form 10-Q, period ended July 31, 2026, filed August 28, 2026: [primary filing](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) and [SEC filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/0000104169-26-000154-index.html). This filing was available before the proposed valuation date and is used only to identify later reported facts and date mismatches.
- Local files reviewed: `project1_fcff.py`, `walmart_project1_proforma.py`, and `Walmart_Project1_Normalization_Review.md`.

“Verified” below means traced to an original SEC filing. It does not mean that the item's valuation classification has been resolved.

## Existing bridge amounts reconciled to the FY2026 filing

| Existing model item | Model amount | Filing reconciliation at January 31, 2026 | Evidence status | Current accounting and valuation treatment |
|---|---:|---|---|---|
| Cash and cash equivalents | $10,727 | The consolidated balance sheet reports cash and cash equivalents of $10,727. | **VERIFIED filing amount** | `project1_fcff.py` adds the entire balance to enterprise value. The filing does not identify all $10,727 as excess cash, so the amount is verified but the full-add treatment is a **valuation assumption**. |
| Borrowings | $44,762 | Short-term borrowings $6,596 + long-term debt due within one year $3,542 + long-term debt $34,624 = **$44,762**. | **VERIFIED filing arithmetic** | This is a carrying-value measure and correctly excludes finance leases. The filing reports fair value of the $38,166 long-term-debt carrying amount as $36,777; short-term borrowings approximate fair value. Therefore, $44,762 is not a verified market-value debt measure. |
| Finance lease obligations | $6,761 | Current finance lease obligations $856 + long-term finance lease obligations $5,905 = **$6,761**. Note 6 independently reports net finance lease obligations of $6,761. | **VERIFIED filing arithmetic** | `project1_fcff.py` subtracts this amount separately. It is not included in the $44,762 borrowings amount, so there is no debt/finance-lease duplication in the stated bridge. Whether finance leases should be debt-like depends on a consistent FCFF lease convention, discussed below. |
| FY2026 diluted weighted-average shares | 8,022 | FY2026 basic weighted-average shares 7,983 + dilutive impact of share-based awards 39 = **8,022**. | **VERIFIED filing arithmetic** | This is an annual earnings denominator, not shares outstanding on January 31 or September 23. Using it as the DCF denominator is a **valuation assumption**. |
| FY2026 year-end shares in the pro forma | 7,969 | The statement of shareholders' equity reports 7,969 shares at January 31, 2026, rounded to the nearest million. | **VERIFIED filing amount** | `walmart_project1_proforma.py` stores 7,969 as `SHARES_OUTSTANDING`, but `project1_fcff.py` does not use it for value per share; the FCFF model uses 8,022 instead. |

The [FY2026 balance sheet and share disclosures](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) are the source for these amounts. Note 7 also reports that long-term debt is carried at cost and provides its separate fair value.

## Current bridge arithmetic

At the model's existing 7.00% WACC and 2.50% terminal-growth assumptions, `project1_fcff.py` calculates enterprise value of **$305,974.253**. The current bridge recomputes as follows:

```text
Enterprise value                                      $305,974.253
+ Cash and cash equivalents                             10,727.000
- Short-term borrowings                                 (6,596.000)
- Long-term debt due within one year                    (3,542.000)
- Long-term debt                                       (34,624.000)
- Finance lease obligations due within one year           (856.000)
- Long-term finance lease obligations                  (5,905.000)
                                                       ------------
Equity value                                           $265,178.253

Condensed bridge adjustment:
$10,727 - $44,762 - $6,761 = $(40,796)

Value per FY2026 diluted weighted-average share:
$265,178.253 / 8,022 = $33.0564
```

**Arithmetic result: PASS.** The calculation exactly matches the model. This check validates arithmetic only; it does not validate the dates, economic classifications, carrying-value convention, or share denominator.

## Restricted cash versus excess cash

### Verified filing facts

- Cash and cash equivalents were **$10,727** at January 31, 2026.
- The cash-flow statement reports **$11,321** of cash, cash equivalents, and restricted cash at year-end. The **$594** difference from balance-sheet cash is an arithmetic inference for restricted cash outside the cash-and-cash-equivalents line; the filing excerpt does not separately label that $594 as an equity-bridge asset.
- Walmart states that **approximately $3.9 billion of the $10.7 billion cash balance** may not be freely transferable to the U.S. because of local laws, other restrictions, or required noncontrolling-shareholder approval. This is a transfer restriction within the reported cash balance; it is not an additional $3.9 billion asset and is not the same disclosure as the $594 cash-flow-statement difference.
- Approximately 56% of cash and cash equivalents was held outside the U.S. Walmart states that such cash is generally used for non-U.S. liquidity needs.

Source: [FY2026 Form 10-K, cash and liquidity disclosures](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), facts as of January 31, 2026.

### Assumptions and unresolved treatment

- Adding all $10,727 assumes the entire balance is nonoperating or excess. The filing provides **no verified excess-cash amount**. The pro forma's $8,000 minimum-cash input is a model assumption, not a disclosed required-cash amount, and `project1_fcff.py` does not use it to limit the cash added in the bridge.
- Cash required for store operations, payments, working capital, liquidity buffers, foreign operations, or noncontrolling shareholders should not automatically be treated as freely distributable excess cash.
- The exact excess cash at September 23, 2026 is **UNVERIFIED**. The latest pre-valuation-date filing reports $11,529 cash and cash equivalents at July 31, 2026, not September 23.

**Double-counting control:** Do not add the $3.9 billion transfer-restricted portion separately because it is already inside $10,727. Do not mechanically deduct both NCI-related cash restrictions and the full NCI claim without confirming ownership and valuation consistency. Adding the inferred $594 restricted cash would also require proof of ownership, availability, and confirmation that it is not already represented in the model's broad `other_assets` balance.

## Borrowings and debt measurement

The model's $44,762 is a complete carrying-value sum of the three debt lines and excludes lease obligations. The maturity table and the balance-sheet current debt line describe the same debt and must not both be added. Likewise, the $36,777 fair value is an alternative measurement of the $38,166 carrying amount for long-term debt, not another liability.

A market-value bridge would need a consistent debt measurement as of the valuation date. The 10-K's January 31 evidence implies a debt fair-value cross-check of **$43,373** ($6,596 short-term borrowings, whose carrying value approximates fair value, plus $36,777 long-term-debt fair value). This is not a September 23 observation and is not selected here.

The July 31 Form 10-Q, available August 28, reports $10,479 short-term borrowings and $39,932 long-term debt at carrying value, for **$50,411**, while that long-term debt's fair value was $37,267. These later facts demonstrate that the January 31 model amount is date-mismatched to September 23; exact September 23 borrowings and fair value remain **UNVERIFIED**.

## Lease obligations

### Operating leases

The FY2026 filing reports current operating lease obligations of $1,631 and long-term operating lease obligations of $13,941, totaling **$15,572**. It also reports operating lease right-of-use assets of **$14,750** and FY2026 operating lease cost of **$2,434**. These are verified January 31 or FY2026 filing facts. Source: [FY2026 Form 10-K, Note 6](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm).

The current bridge does not subtract operating lease obligations. That treatment can be internally consistent when operating lease expense remains in operating costs and FCFF. Subtracting the liability without also recasting lease expense, operating profit, capital investment, and the discount-rate convention would count the operating lease burden once in FCFF and again in the bridge.

`walmart_project1_proforma.py` models aggregate cash SG&A rather than a separately auditable operating-rent line. Accordingly, the current operating-lease convention is **UNRESOLVED**. A final treatment requires either:

1. an operating-expense convention that leaves operating leases out of the bridge; or
2. a capitalization convention that adjusts the forecast and discount rate consistently before subtracting an operating-lease claim.

No $15,572 adjustment is selected here.

### Finance leases

The $6,761 finance lease obligation is verified and separate from borrowings. The filing also reports a $6,123 finance lease right-of-use asset, $888 of FY2026 finance-lease asset amortization, and $383 of finance-lease interest.

The model treats finance leases as financing by placing assumed finance-lease interest below operating income and subtracting the obligation in the bridge. However, it holds the obligation constant, does not separately identify finance-lease principal in FCFF, and includes the finance lease right-of-use asset within the broad opening `other_assets` total. Finance-lease amortization is not separately traceable in the forecast.

**Double-counting control:** Subtracting the finance lease liability is appropriate only if enterprise value includes the leased assets' operating benefits and FCFF does not also deduct the full financing payment as an operating expense. Conversely, subtracting the obligation after treating full lease payments as operating costs would double count it. The current $6,761 subtraction is a stated model convention, but its full forecast consistency remains **UNRESOLVED**.

## Noncontrolling interests

### Verified filing facts

At January 31, 2026, Walmart reported:

- redeemable noncontrolling interest: **$293**;
- nonredeemable noncontrolling interest: **$6,270**; and
- combined book amount: **$6,563**.

The filing also reports $377 of FY2026 consolidated net income attributable to noncontrolling interests. Walmart's PhonePe ownership declined from approximately 84% to approximately 73% during FY2026. Source: [FY2026 Form 10-K balance sheet and Note 3](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm).

The July 31 Form 10-Q reports $293 redeemable and $6,268 nonredeemable NCI, a combined book amount of **$6,561**. That later filing was available before September 23, but neither book amount is verified as market value.

### Valuation treatment and overlap

The FCFF forecast begins with consolidated revenue and operating income and does not remove earnings or cash flows attributable to noncontrolling owners. Enterprise value therefore appears to include 100% of consolidated subsidiaries. The current bridge subtracts **no NCI claim**, which may overstate value attributable to Walmart common shareholders.

A final adjustment requires the market value of relevant NCI claims, or a documented approximation, and consistent treatment of subsidiary cash and investments. Using book NCI without analysis is an assumption. Excluding NCI-controlled cash and also subtracting a full NCI value can double count the minority claim unless the two adjustments are built on the same ownership basis. The appropriate NCI bridge amount at September 23 is **UNVERIFIED**.

## Nonoperating investments

### Verified filing facts

Note 7 reports the following investments at fair value as of January 31, 2026:

| Investment class | Fair value |
|---|---:|
| Equity investments measured using Level 1 inputs | $1,037 |
| Equity investments measured using Level 2 inputs | 3,462 |
| Debt investments measured using Level 3 inputs | 1,176 |
| **Total** | **$5,675** |

These investments are primarily recorded in other long-term assets. Their fair-value changes are reported in other gains and losses below operating income; fiscal 2026 other gains and losses included a $2.1 billion gain driven primarily by these investments and other immaterial activity. Source: [FY2026 Form 10-K, Notes 1 and 7](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm).

The July 31, 2026 Form 10-Q reports $860 Level 1 equity, $2,781 Level 2 equity, and $1,226 Level 3 debt investments, totaling **$4,867**. This later total still is not a September 23 value.

### Valuation treatment and overlap

Because the DCF starts from operating income, it excludes the reported other gains and losses. That supports investigating these investments as nonoperating assets. The current bridge adds **zero** for investments, but no final omission or addition is selected here.

There is a material classification problem: the pro forma's $79,007 opening `other_assets` is the exact aggregate of reported assets other than cash, inventory, and property and equipment. It therefore includes investments, receivables, lease right-of-use assets, goodwill, and other items. `project1_fcff.py` treats changes in the entire broad `other_assets` balance as operating working capital. Simply adding $5,675 in the bridge without separating investment balances and their forecast effects could count the assets in the operating forecast and again in the bridge. The recurring-fair-value table also may not identify every asset that a valuation practitioner could classify as nonoperating.

Required before any adjustment: isolate each investment from operating assets, identify ownership attributable to NCI, remove any investment return or reinvestment effect from FCFF, and obtain a valuation-date value. The September 23 amount and final classification are **UNVERIFIED**.

## Weighted-average diluted shares versus valuation-date shares

| Measure | Shares | Observation date or period | Status and use |
|---|---:|---|---|
| FY2026 diluted weighted-average denominator used by `project1_fcff.py` | 8,022 | Fiscal year ended January 31, 2026 | **VERIFIED filing fact**; includes 39 dilutive shares under the treasury-stock method, but is not a spot count. |
| FY2026 basic weighted-average denominator | 7,983 | Fiscal year ended January 31, 2026 | **VERIFIED filing fact**; not a spot count. |
| Statement-of-equity year-end shares used by the pro forma | 7,969 | January 31, 2026 | **VERIFIED, rounded filing fact**; not used by the FCFF per-share calculation. |
| Exact Form 10-K cover count | 7,972.402501 | March 11, 2026 | **VERIFIED filing fact**. |
| Latest exact count published before the valuation date | 7,933.746241 | August 26, 2026 | **VERIFIED filing fact** in the Form 10-Q filed August 28, 2026; not a September 23 count and not diluted. |
| Exact diluted shares at September 23, 2026 | Not reported | September 23, 2026 | **UNVERIFIED**. |

Sources: [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) and [July 31, 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm).

The model denominator exceeds the latest exact pre-valuation-date outstanding count by **88.253759 million shares**, or approximately **1.10% of the model denominator**. That difference combines two effects that must not be confused: the model uses a historical annual average, and it includes dilution. Walmart also continued repurchasing shares after FY2026, while share-based awards can increase diluted shares.

Holding the current $265,178.253 equity value constant, division by the August 26 outstanding count would mechanically produce $33.4241 per share instead of $33.0564. This is only a denominator illustration, not a revised valuation: a proper September 23 denominator would require the actual spot shares plus valuation-date dilution under a documented treasury-stock or fully diluted method.

## Later filing facts available before September 23

These items show why the existing January 31 bridge is not a same-date bridge. They are not assembled into a replacement bridge.

| Item | January 31, 2026 reported amount | July 31 or August 26, 2026 reported amount | Valuation-date limitation |
|---|---:|---:|---|
| Cash and cash equivalents | $10,727 | $11,529 at July 31 | September 23 excess cash is unverified. |
| Borrowings at carrying value | $44,762 | $50,411 at July 31 | September 23 carrying and market values are unverified. |
| Finance lease obligations | $6,761 | $6,832 at July 31 | September 23 amount is unverified. |
| Combined book NCI | $6,563 | $6,561 at July 31 | Book value is not verified market value. |
| Investments in recurring fair-value table | $5,675 | $4,867 at July 31 | September 23 value and full nonoperating scope are unverified. |
| Common shares outstanding | 7,969 rounded at January 31 | 7,933.746241 exact at August 26 | September 23 spot and diluted counts are unverified. |

## Verified facts versus valuation assumptions

### Verified from original filings

- The January 31 balance-sheet amounts and arithmetic for $10,727 cash, $44,762 borrowings, $6,761 finance lease obligations, and the reported lease and NCI balances.
- The 8,022 FY2026 diluted weighted-average share calculation.
- The January 31 investment fair-value table and later July 31 reported amounts.
- The August 26 exact outstanding share count.

### Existing assumptions or unresolved classifications

- Treating all $10,727 as excess cash.
- Using January 31 carrying-value debt for a September 23 valuation.
- Treating finance leases as debt-like without a fully reconciled lease-adjusted FCFF forecast.
- Excluding operating lease obligations from the bridge while their precise forecast expense treatment is aggregated.
- Making no NCI deduction even though the forecast is consolidated.
- Making no nonoperating-investment addition while broad `other_assets` mixes operating and nonoperating assets.
- Using FY2026 weighted-average diluted shares rather than a September 23 spot and diluted count.

## Evidence required before selecting a final bridge

1. A September 23 cash analysis identifying required operating cash, truly excess cash, transfer restrictions, restricted cash, taxes or friction on access, and NCI ownership.
2. September 23 market values for short- and long-term borrowings, with a definition consistent with the WACC capital weights.
3. A documented lease convention applied consistently to EBIT, FCFF, invested capital, WACC, and the bridge.
4. Market-value support for redeemable and nonredeemable NCI, with subsidiary cash and investment ownership reconciled.
5. A security-level schedule of nonoperating investments at September 23 and removal of any related assets, returns, and reinvestment from operating FCFF.
6. September 23 common shares outstanding plus a reproducible dilution calculation for options, restricted units, performance awards, and other potentially dilutive claims.

The existing bridge is arithmetically correct and its stated January 31 filing inputs are traceable. Its economic classifications and September 23 dating remain unresolved, so this review does **not** select or recommend a final enterprise-to-equity bridge.

## Enterprise-to-Equity Bridge Policy and Alternatives

### Governing policy

An FCFF DCF values the operating assets available to all capital providers. The bridge should therefore:

1. **add** assets not represented in operating FCFF or invested capital;
2. **subtract** financing claims and claims belonging to capital providers other than Walmart common shareholders; and
3. divide the resulting common equity value by a share base that captures the equity claims outstanding on the valuation date.

Each item should appear exactly once. An amount cannot be treated as an operating asset or liability in FCFF and invested capital and then be added or subtracted again in the bridge without a corresponding reclassification. Likewise, interest-bearing debt should be excluded from FCFF and subtracted once, while ordinary operating liabilities included in net operating capital should not be separately deducted from enterprise value.

This consistency requirement is especially important here. `project1_fcff.py` defines change in operating net working capital as changes in inventory plus broad `other_assets`, less changes in accounts payable and broad `other_liabilities`. The $79,007 opening `other_assets` balance includes receivables, prepaid assets, operating and finance lease right-of-use assets, goodwill, investments, and other long-term assets. The $64,197 opening `other_liabilities` balance includes operating lease obligations, accrued liabilities, taxes, deferred taxes, and other items, while separately excluding borrowings and finance leases. These aggregates are projected as percentages of revenue. They are not yet economically classified line by line.

### Policy by adjustment

| Adjustment | Direction from enterprise value | Policy rationale | Double-counting and model-consistency test | Current conclusion |
|---|---|---|---|---|
| Cash | **Add only excess, nonoperating cash** | Cash excluded from operating net working capital is normally a nonoperating asset. Cash required to fund operations is part of the operating business and is not freely distributable. | `project1_fcff.py` excludes cash from FCFF working capital and adds all $10,727. The $3.9 billion transfer-restricted portion is already inside that balance and must not be separately added. Deducting required cash and also lowering operating invested capital for the same amount would count the restriction twice. | Direction is add, but the excess amount at September 23 is **UNVERIFIED**. Adding all $10,727 is an assumption. |
| Borrowings | **Subtract** | Interest-bearing short- and long-term debt are claims senior to common equity. FCFF is before interest and debt service, so debt must be removed after enterprise value is calculated. | Subtract either carrying value or market value under a stated convention, not both. Do not add maturities to the balance-sheet debt lines because they describe the same obligations. Debt used in the bridge should also be consistent with debt used in WACC capital weights. | The $44,762 carrying-value subtraction is arithmetically complete but dated January 31. September 23 market value is **UNVERIFIED**. |
| Finance lease obligations | **Subtract under a financing convention; otherwise recast before deciding** | If finance leases fund operating assets and finance-lease interest is excluded from EBIT and FCFF, the obligation is debt-like and should be subtracted. | The leased asset's operating benefit must remain in enterprise value, while finance-lease interest and principal must not also be deducted as operating cash costs. The model subtracts $6,761, models finance-lease interest below operating income, and excludes finance leases from borrowings; however, the right-of-use asset is embedded in `other_assets`, amortization is not separately traceable, and the obligation is held constant. | A subtraction is the current policy, but full FCFF and invested-capital consistency is **UNRESOLVED**. |
| Operating lease obligations | **Do not subtract under the current operating-expense convention; subtract only after a full capitalization recast** | When operating lease expense remains in operating costs, the lease burden is already reflected in EBIT and FCFF. Under a capitalization convention, the liability becomes debt-like and is subtracted after rent is decomposed and the forecast is restated. | The $15,572 obligation is already contained in the opening `other_liabilities` aggregate, and the $14,750 right-of-use asset is in `other_assets`. Mechanically subtracting the liability while leaving lease expense and both aggregated balance-sheet lines in FCFF would count the lease burden more than once. | No separate subtraction is supported without a lease-adjusted FCFF, invested-capital, and WACC recast. |
| Noncontrolling interests | **Subtract** when enterprise value includes 100% of consolidated subsidiaries | Consolidated FCFF includes cash flows attributable to owners other than Walmart common shareholders. Their claim must be removed to reach Walmart common equity value. | Use a market-value claim consistent with the consolidated forecast. Do not subtract full NCI after already removing the minority owners' share of subsidiary FCFF. Cash and investments held in partly owned subsidiaries must be allocated consistently so NCI-controlled value is not deducted twice. | The bridge currently subtracts zero. January 31 book NCI of $6,563 and July 31 book NCI of $6,561 are verified facts, but neither is a verified September 23 market value. |
| Nonoperating investments | **Add** if their value and returns are excluded from operating enterprise value | Investments whose gains and losses are below operating income ordinarily sit outside FCFF and should be added to enterprise value. | Investments are embedded in the model's `other_assets` and their changes therefore affect FCFF. Before adding them, remove their balances and changes from operating invested capital and FCFF and exclude any related income. Allocate interests owned by NCI. Otherwise the investment can be counted in enterprise value and again in the bridge. | Direction is potentially add. The $5,675 January 31 and $4,867 July 31 recurring-fair-value totals are verified, but September 23 value, ownership, and complete scope are **UNVERIFIED**. |
| Diluted equity claims | **Generally reflected in the denominator, not added to or subtracted from enterprise value** | Common shares and share-based awards determine how common equity value is allocated. Options can be handled through treasury-stock dilution or through a separate option-value deduction with basic shares. Restricted or performance awards require probability and vesting analysis. | Do not use a diluted share count and also subtract the same awards' value from equity. Convertible or debt-like securities must be treated either as a financing claim or as converted shares under a consistent if-converted method, not both. | The model uses historical FY2026 diluted weighted-average shares. A September 23 spot diluted-equivalent count is **UNVERIFIED**. |

The verified filing facts in this table come from Walmart's [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) and [July 2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm). The policy conclusions are valuation judgments, not amounts reported by Walmart.

### Share-base comparison without automatic replacement

The original **8,022 million** denominator is Walmart's FY2026 weighted-average diluted share count: 7,983 million weighted-average basic shares plus 39 million dilutive shares under the treasury-stock method. It measures average claims during the year ended January 31, 2026.

The **7,933.746241 million** count is the exact common shares outstanding on August 26, 2026, reported on the cover of the Form 10-Q filed August 28. It is closer to the proposed September 23 valuation date, but it is a basic spot count and contains no valuation-date dilution adjustment. The 88.253759 million difference from 8,022 million reflects different dates, annual-average versus spot measurement, repurchases or issuances, and the absence versus inclusion of dilution. It is not evidence that one figure should mechanically replace the other.

For reference, the 7,969 million count in `walmart_project1_proforma.py` is the rounded January 31 statement-of-equity balance. It is another spot count, not a diluted denominator. A final September 23 denominator should begin with the best verified spot count and then incorporate award-specific dilution using September 23 prices, vesting terms, performance conditions, and proceeds.

### Illustrative sensitivity — share bases

The following table holds the current model equity value of **$265,178.253 million** constant. It isolates denominator effects and does not revise the bridge.

| Share basis | Shares (millions) | Illustrative value per share | Evidence and limitation |
|---|---:|---:|---|
| FY2026 weighted-average diluted | 8,022.000000 | $33.0564 | Verified historical diluted denominator; not a September 23 spot count. |
| January 31 shares outstanding | 7,969.000000 | $33.2762 | Verified rounded spot count; not diluted and dated nearly eight months before valuation. |
| August 26 shares outstanding | 7,933.746241 | $33.4241 | Verified exact pre-valuation-date spot count; not September 23 and not diluted. |
| August 26 outstanding plus **hypothetical** 24 million dilution | 7,957.746241 | $33.3233 | The 24 million equals the reported diluted impact for the three months ended July 31, but applying it to August 26 is a clearly labeled hypothetical, not a verified spot-dilution calculation. |

No row is selected as the final share basis.

### Illustrative sensitivity — claim and asset treatments

Each row below changes **one item at a time** from the current 7.00% WACC bridge. Enterprise value remains $305,974.253 million. The table shows both the existing 8,022 denominator and the August 26 basic spot count solely to separate bridge effects from denominator effects. Except where stated, the amounts are verified January 31 filing amounts applied as hypothetical valuation treatments; they are not verified September 23 bridge values.

| One-at-a-time treatment | Change from current equity value | Illustrative equity value | Per share using 8,022 | Per share using 7,933.746241 | Interpretation and limitation |
|---|---:|---:|---:|---:|---|
| Current model: add all cash; subtract carrying-value borrowings and finance leases | — | $265,178.253 | $33.0564 | $33.4241 | Existing arithmetic baseline; mixed with the August denominator only in the final column. |
| Add only cash above the model's **hypothetical $8,000 minimum cash** | $(8,000) | $257,178.253 | $32.0591 | $32.4157 | Uses a model assumption, not a verified required-cash amount. |
| Substitute January 31 debt fair-value proxy of $43,373 for $44,762 carrying value | +$1,389 | $266,567.253 | $33.2295 | $33.5992 | Uses verified January 31 fair-value evidence, not September 23 debt value. |
| Do not subtract finance leases | +$6,761 | $271,939.253 | $33.8992 | $34.2763 | Mechanical alternative only; would require treating finance leases as operating and recasting FCFF and invested capital. |
| Subtract operating lease obligations | $(15,572) | $249,606.253 | $31.1152 | $31.4613 | Deliberately mechanical sensitivity; inconsistent unless rent, right-of-use assets, liabilities, FCFF, and WACC are all recast. |
| Subtract January 31 combined book NCI as a **hypothetical market-value proxy** | $(6,563) | $258,615.253 | $32.2383 | $32.5969 | Book NCI is verified, but its use as market value is hypothetical. |
| Add January 31 recurring-fair-value investments | +$5,675 | $270,853.253 | $33.7638 | $34.1394 | Mechanical sensitivity only; requires removing investments from operating `other_assets` and FCFF first. |
| Combine January 31 debt fair-value proxy, book-NCI proxy, and investment addition | +$501 net | $265,679.253 | $33.1188 | $33.4872 | Illustrative bundle of mixed policy assumptions; excludes cash and lease changes and is not a final bridge. |

The rows are not all mutually compatible and should not be added together casually. In particular, the operating-lease and finance-lease alternatives require forecast recasts, while the investment addition requires reclassification of `other_assets`. The August 26 share column also combines a later basic share count with January 31 claims and therefore is a sensitivity, not a date-consistent valuation.

### Facts still required for a defensible September 23, 2026 bridge

1. **Cash:** September 23 cash or a defensible roll-forward from July 31; operating-cash needs by jurisdiction and subsidiary; the precise restricted-cash location; transfer costs; and ownership of cash subject to NCI approval.
2. **Borrowings:** instrument-level principal, accrued items included in carrying value, and observable market prices or yields on September 23; the selected debt definition must match the WACC weights.
3. **Finance leases:** a schedule connecting right-of-use asset amortization, interest, principal payments, new leases, and closing obligations to forecast EBIT, FCFF, and invested capital.
4. **Operating leases:** forecast rent expense and a decision to retain operating treatment or capitalize leases; if capitalized, a complete restatement of EBIT, NOPAT, reinvestment, invested capital, debt, and WACC.
5. **NCI:** subsidiary-level ownership, cash flows, cash, investments, redemption terms, and a supportable market value for both redeemable and nonredeemable interests at September 23.
6. **Nonoperating investments:** security-level holdings and September 23 values; tax leakage and liquidity restrictions; NCI ownership; and removal of related balances, returns, and changes from operating FCFF.
7. **Diluted equity claims:** exact September 23 common shares outstanding plus award-level options, restricted shares, performance units, vesting conditions, strike prices, settlement method, and treasury-stock or option-value calculations using the September 23 share price.
8. **Other broad balances:** disaggregation of `other_assets` and `other_liabilities` into operating, financing, and nonoperating components so ordinary operating liabilities remain in FCFF and no bridge claim is counted twice.

These alternatives are illustrative diagnostics only. They do **not** select a final bridge, a final share base, or a final value per share.
