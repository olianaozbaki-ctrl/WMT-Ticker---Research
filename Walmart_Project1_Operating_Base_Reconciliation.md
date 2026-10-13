# Walmart Project 1 — Operating Base Reconciliation

**Status:** Reconciliation and diagnostic analysis only. No Python input, original lab, Edition A document, or existing valuation result has been changed.

**Reporting period:** Fiscal year ended January 31, 2026. **Units:** USD millions unless stated otherwise.

## Sources and definitions

- Walmart FY2026 Form 10-K, filed March 13, 2026: [primary filing](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) and [SEC filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/0000104169-26-000055-index.html).
- Local model files reviewed: `walmart_project1_proforma.py` and `project1_fcff.py`.
- Prior issue log reviewed: `Walmart_Project1_Normalization_Review.md`.

“Reported” means traced to the original Form 10-K. “Modeled” means an input, aggregation, or formula in the Python files. “Alternative” means an illustrative calculation only; no alternative is proposed for adoption unless expressly stated.

One implementation point is relevant: `project1_fcff.py` imports `walmart_proforma`, not `walmart_project1_proforma`. The two modules' `BASE_INPUTS` dictionaries currently compare equal, so the numbers below agree today, but the linkage is indirect and could diverge if only one module is updated.

## Summary reconciliation

| Item | FY2026 filing fact | Treatment in `walmart_project1_proforma.py` | Reconciliation result |
|---|---:|---|---|
| Total revenue | $713,163 | Opening revenue $713,163 | **Exact tie.** The amount is total revenue, consisting of $706,413 net sales and $6,750 membership and other income. |
| Operating income | $29,825 | No FY2026 opening operating-income field | **Not directly tied.** The model independently forecasts FY2027 operating income of $31,692.601 from revenue, margin, cash-SG&A, and depreciation assumptions. |
| Depreciation and amortization | $14,203 | No FY2026 opening expense; FY2027 depreciation is 10.6% of $136,083 opening net PP&E, or $14,424.798 | **Not like-for-like.** Filing D&A includes property and equipment, finance-lease assets, and intangible assets; the model applies one rate only to net PP&E. |
| Capital expenditures | $26,642 | No FY2026 opening cash-flow field; FY2027 forecast is $26,000 | **Forecast assumption, not a historical tie.** FY2027 is $642, or 2.41%, below FY2026 and lies within Walmart's disclosed FY2027 guidance of approximately $25–$27 billion. |
| Inventory | $58,851 | Opening inventory $58,851 | **Exact balance tie.** The 40.2-day forecast driver is an approximation, not the exact FY2026 implied days. |
| Accounts payable | $63,061 | Opening accounts payable $63,061 | **Exact balance tie.** The 42.8-day forecast driver is an approximation. The reported line includes $5,989 of supplier-financing-program obligations classified by Walmart as accounts payable and operating cash flow. |
| Other assets | $79,007 reconstructed from reported lines | Opening `other_assets` $79,007 | **Exact aggregate tie, but not an operating-asset tie.** The aggregate contains operating, investing, lease, financial, acquisition, and tax-related assets. |
| Other liabilities | $64,197 reconstructed from reported lines and mezzanine NCI | Opening `other_liabilities` $64,197 | **Exact aggregate tie, but not an operating-liability tie.** The aggregate contains operating accruals, taxes, leases, financial items, deferred taxes, and redeemable NCI. |

The exact balance-sheet ties demonstrate arithmetic completeness, not economic classification.

## Revenue and operating income

### Reported facts

The Form 10-K reports FY2026 net sales of **$706,413**, membership and other income of **$6,750**, total revenue of **$713,163**, gross profit of **$171,018**, operating expenses of **$147,943**, and operating income of **$29,825**. Source: [FY2026 Form 10-K, consolidated results](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm).

Reported cost of sales is therefore **$535,395** ($706,413 net sales less $171,018 gross profit). The filing defines gross profit using net sales, not total revenue.

### Model treatment and unresolved difference

The model correctly seeds total revenue at $713,163. It then applies its forecast gross-margin percentage to total modeled revenue and defines cost of sales as modeled revenue less gross profit. This combines net sales and membership and other income in a single revenue base, whereas Walmart's reported gross-profit definition uses net sales only.

The distinction is numerically visible in FY2026:

- reported gross profit / net sales = **24.2094%**;
- reported gross profit / total revenue = **23.9802%**; and
- model FY2027 gross-margin assumption = **25.0000%**, applied to total modeled revenue.

The model has no FY2026 operating-income input against which to validate the operating forecast. Its first forecast year is:

```text
FY2027 modeled revenue                                  $743,829.009
FY2027 modeled operating income                          31,692.601
Increase over reported FY2026 operating income            1,867.601
Implied growth                                             6.2619%
```

This increase is a modeled result, not a reconciliation difference that can be forced to zero. A fully reconciled operating model would forecast net sales and membership/other income separately or document why one blended margin is appropriate.

## Depreciation and capital expenditures

### Depreciation and amortization

The filing reports FY2026 depreciation and amortization of **$14,203**. Walmart states that the total includes property and equipment, property under finance leases, and intangible assets. Note 6 separately reports **$888** of finance-lease right-of-use asset amortization, but the filing does not provide all components needed to reproduce $14,203 from the model's single net-PP&E driver.

The model has no FY2026 D&A opening amount. It calculates FY2027 depreciation as:

```text
$136,083 opening net PP&E × 10.6% = $14,424.798
```

That forecast is **$221.798**, or **1.5616%**, above reported FY2026 D&A. The comparison is not like-for-like because reported D&A spans more asset classes and represents expense on assets held during FY2026, while the model applies a rate to one ending balance.

As a mechanical one-year sensitivity only, substituting $14,203 for $14,424.798 while leaving all other FY2027 model amounts unchanged would reduce D&A by $221.798, increase EBIT by the same amount, and reduce FY2027 FCFF by **$54.341** after the model's 24.5% tax rate because the lost D&A tax shield exceeds the offsetting EBIT/NOPAT increase. This is not a supported forecast change because later PP&E, amortization, and tax effects would also need to be rebuilt.

### Capital expenditures

The cash-flow statement reports **$26,642** of FY2026 payments for property and equipment. The model's FY2027 assumption is **$26,000**, $642 below FY2026. Replacing the forecast with the historical amount would mechanically lower FY2027 FCFF by **$642**, before any associated change to depreciation or later PP&E. This is not proposed: the existing $26,000 falls within management's FY2027 guidance of approximately $25–$27 billion.

## Inventory and accounts payable

The reported and modeled opening balances tie exactly. Using reported FY2026 cost of sales of $535,395 gives:

| Driver | Exact FY2026 implied days | Model assumption | Difference |
|---|---:|---:|---:|
| Inventory | 40.1211 | 40.2000 | +0.0789 day |
| Accounts payable | 42.9912 | 42.8000 | −0.1912 day |

Applied to the model's FY2027 cost of sales, the exact historical days would produce inventory of **$61,321.661** and accounts payable of **$65,708.404**, compared with modeled balances of $61,442.314 and $65,416.195. Holding everything else constant, exact historical days would improve FY2027 FCFF by **$412.862** through $120.653 less inventory and $292.209 more accounts payable.

This is a supported arithmetic sensitivity, not a proposed adjustment. The model's blended revenue/cost-of-sales definition and Walmart's changing business mix can justify forecast days different from the historical calculation.

Accounts payable also contains **$5,989** of supplier-financing-program obligations. Walmart reports these obligations as accounts payable and their cash flows as operating. The model treats the entire $63,061 as operating. Reclassifying any portion as financing would require a policy decision and corresponding changes to FCFF, debt, and the equity bridge; no reclassification is made here.

## Reconciliation of the $79,007 other-assets aggregate

The model's amount is the exact sum of every reported asset other than cash, inventory, and net property and equipment:

| Reported balance-sheet line | Amount | Preliminary economic content |
|---|---:|---|
| Receivables, net | $11,172 | Largely operating, but the filing says receivables also include amounts due from governments for income taxes and from real-estate transactions. |
| Prepaid expenses and other | 4,124 | Mixed and not sufficiently disaggregated in the filing for an operating-only classification. |
| Operating lease right-of-use assets | 14,750 | Lease asset; not ordinary working capital. |
| Finance lease right-of-use assets, net | 6,123 | Lease/financing-related asset; not ordinary working capital. |
| Goodwill | 28,735 | Acquisition-related long-term operating asset; not working capital and should not normally scale mechanically with annual revenue. |
| Other long-term assets | 14,103 | Mixed investing, tax, intangible, restricted/financial, and other balances. |
| **Model `other_assets`** | **$79,007** | **Arithmetic tie only.** |

The $14,103 other-long-term-assets line includes or overlaps the following disclosures:

- **$5,675** of equity and debt investments measured at recurring fair value, primarily classified in other long-term assets;
- **$1,891** of deferred-tax assets classified in other long-term assets;
- approximately **$4.3 billion** of indefinite-lived intangible assets; and
- other items not separately quantified in the filing, potentially including restricted cash, derivatives, other intangibles, and operating balances.

Because “primarily classified” and “approximately” are not exact allocation statements, these disclosures do not support forcing a residual classification. The operating portion of $79,007 is **UNRESOLVED**.

The model projects the entire aggregate at **11.0784% of revenue**. In FY2027 this raises `other_assets` from $79,007 to $82,404.301, a **$3,397.301 FCFF use**. This treats goodwill, lease assets, investments, deferred-tax assets, and other nonworking-capital items as if they all grow with revenue.

## Reconciliation of the $64,197 other-liabilities aggregate

The model's amount can be reproduced exactly as follows:

| Reported balance-sheet or mezzanine line | Amount | Preliminary economic content |
|---|---:|---|
| Accrued liabilities | $31,187 | Mixed operating, tax, and financial accruals. |
| Accrued income taxes | 596 | Tax liability; not ordinary supplier working capital. |
| Operating lease obligations due within one year | 1,631 | Lease obligation. |
| Long-term operating lease obligations | 13,941 | Lease obligation. |
| Deferred income taxes and other | 16,549 | Deferred tax, derivatives, indemnities, and other mixed liabilities. |
| Redeemable noncontrolling interest | 293 | Ownership claim presented outside liabilities and equity; not an operating liability. |
| **Model `other_liabilities`** | **$64,197** | **Arithmetic tie only.** |

The $31,187 accrued-liabilities line itself consists of $7,878 accrued wages and benefits, $5,525 self-insurance, $4,110 non-income taxes, $2,941 deferred gift-card revenue, and $10,733 other. Walmart states that “other” includes deferred membership revenue, interest, supply-chain, advertising, maintenance, and utilities. It therefore mixes operating and financing content.

The $16,549 deferred-income-taxes-and-other line includes financial and nonoperating items. Among the separately disclosed amounts are net deferred-tax liabilities, derivative liabilities primarily classified in this line, and approximately $0.7 billion of divestiture-related indemnification liabilities. These disclosures do not provide an exact operating/nonoperating split.

The model projects the whole $64,197 aggregate at **9.0017% of revenue**. FY2027 `other_liabilities` rises to $66,957.471, a **$2,760.471 FCFF source**. Combined with the other-assets change, the two broad aggregates create a net FY2027 working-capital use of:

```text
$3,397.301 other-assets increase
− 2,760.471 other-liabilities increase
=  $636.830 net FCFF use
```

Holding both aggregates flat would mechanically raise FY2027 FCFF by $636.830. That is a clearly labeled hypothetical, not a supported adjustment: genuine operating receivables, prepaids, accruals, and deferred revenue should normally change with the business. A defensible alternative requires line-by-line operating classification rather than setting both changes to zero.

## FY2026 normalization candidates

### Approximately $900 million higher general-liability claims expense

**Reported fact:** Management states that FY2026 operating-expense pressure was driven partly by approximately **$0.9 billion of higher self-insured general-liability claims expense in the U.S.**, influenced by rising claim-resolution costs across retail and related industries. The filing also reports a $5,525 self-insurance liability at year-end, but that reserve balance is not the same measure as the approximately $900 expense increase.

**Assessment:** The amount is included in operating expenses and therefore reduces reported operating income. The wording describes higher costs, not a correction or a discontinued activity. Rising industry claim costs may recur. The filing does not provide a normalized run rate or establish that the full $900 is nonrecurring.

**Proposed adjustment:** **None.** A full addback is shown only as an upper-bound scenario pending claim-frequency, severity, reserve-development, and multi-year expense evidence.

### Approximately $700 million PhonePe compensation charge

**Reported fact:** Walmart recorded a **$0.7 billion noncash charge** in Walmart International operating expenses after modifying certain PhonePe share-based compensation arrangements in contemplation of a possible IPO. The charge primarily related to previously unrecognized compensation expense. PhonePe employee option exercises reduced Walmart's ownership from approximately 84% to approximately 73%. The filing also reports approximately $3 billion of unrecognized compensation cost primarily associated with subsidiary plans subject to performance or IPO-related conditions.

**Assessment:** The modification charge is more specifically identified and noncash, but an addback is not costless. Share-based compensation is an economic cost that can appear through dilution or reduced parent ownership. Additional conditional expense may arise, and the model does not separately forecast PhonePe compensation or NCI dilution.

**Proposed adjustment:** **None.** A full $700 EBIT addback is an illustrative scenario only and would require a corresponding ownership/dilution treatment.

### $2.075 billion net other gain

**Reported fact:** The consolidated income statement reports **$2,075 of net other gains** below operating income. The cash-flow statement separately identifies **$2,016 of net investment gains**, and Note 7 says fair-value changes in investments were the primary driver.

**Assessment:** `project1_fcff.py` begins with modeled operating income. The $2,075 gain is already outside EBIT and therefore outside operating NOPAT and FCFF. Subtracting it from EBIT would create a false normalization; adding it to FCFF would also be incorrect. Investment value, if nonoperating, belongs in a separately reconciled enterprise-to-equity bridge after removing investment balances from operating assets.

**Proposed adjustment:** **Zero to operating income and FCFF.** For an earnings-only illustration, removing the gain would reduce reported pretax income by $2,075, but that is not an FCFF adjustment.

## Numerical normalization scenarios

The following scenarios start from reported FY2026 operating income of $29,825 and use the model's 24.5% tax rate solely to show mechanical NOPAT effects. The filing's reported effective tax rate and the tax consequences of each item may differ. No scenario changes the saved forecast or valuation.

| Illustrative FY2026 basis | Operating income | Change from reported EBIT | Mechanical NOPAT at 24.5% | NOPAT change | Status |
|---|---:|---:|---:|---:|---|
| Reported | $29,825 | — | $22,517.875 | — | Verified starting point |
| Add back full claims increase | 30,725 | +$900 | 23,197.375 | +$679.500 | Hypothetical upper bound; recurrence unresolved |
| Add back full PhonePe modification charge | 30,525 | +700 | 23,046.375 | +528.500 | Hypothetical; must address dilution/NCI ownership |
| Add back both operating items | 31,425 | +1,600 | 23,725.875 | +1,208.000 | Hypothetical combination; not selected |
| Remove $2,075 other gain from EBIT/FCFF | 29,825 | $0 | 22,517.875 | $0 | Correct FCFF treatment because gain is already below EBIT |

If the $2,075 gain were removed from reported pretax earnings rather than FCFF, the mechanical after-tax earnings effect at 24.5% would be **$(1,566.625)**. This calculation is included only to distinguish earnings normalization from operating FCFF normalization.

## Unresolved reconciliation items

1. The model does not carry reported FY2026 operating income or D&A as explicit opening fields, so there is no direct historical-to-forecast bridge for EBIT or depreciation.
2. Total revenue is blended into one gross-margin calculation even though the filing defines gross profit using net sales and reports membership and other income separately.
3. Reported D&A covers PP&E, finance-lease assets, and intangibles, while modeled depreciation uses only an ending net-PP&E base.
4. The operating portion of receivables, prepaid assets, other long-term assets, accrued liabilities, and deferred-income-taxes-and-other is not fully disclosed.
5. Investments, goodwill, lease right-of-use assets, deferred-tax assets, operating lease liabilities, financial derivatives or interest accruals, indemnities, and redeemable NCI are embedded in balances treated by FCFF as operating working capital.
6. Accounts payable contains supplier-financing-program obligations; their reported operating classification is clear, but the final valuation classification has not been tested.
7. The recurring portion of the higher claims expense is unknown, and the PhonePe charge cannot be separated from ownership dilution and potential future subsidiary compensation using available facts.
8. The original filing does not provide enough disaggregation to force $79,007 and $64,197 into clean operating-only totals. No plug or residual classification has been invented.
9. `project1_fcff.py` currently depends on `walmart_proforma`, creating a maintenance risk even though its base inputs match `walmart_project1_proforma.py` today.

The reported base amounts and aggregate arithmetic reconcile. The economic operating base does not yet reconcile because the model intentionally combines operating, investing, lease, tax, financial, and ownership items. No normalization or model change is selected in this review.
