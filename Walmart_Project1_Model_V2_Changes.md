# Walmart Project 1 — Model V2 Changes

**Status:** Diagnostic model revision only. V2 does not select a final forecast, FCFF, WACC, enterprise-to-equity bridge, or fair value. Original Python files, labs, Edition A, and existing valuation results remain unchanged.

**New executable files:** `walmart_project1_proforma_v2.py` and `project1_fcff_v2.py`.

**Primary filing source:** Walmart FY2026 Form 10-K, fiscal year ended January 31, 2026, filed March 13, 2026: [primary filing](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) and [SEC filing index](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/0000104169-26-000055-index.html).

## Objective and outcome

V2 replaces the original model's changes in aggregated `other_assets` and `other_liabilities` with changes in individually identified operating current accounts. All balance-sheet lines remain visible. Mixed and nonoperating balances excluded from operating NWC are held constant as explicit diagnostic assumptions, not used as balancing plugs.

The new files ran successfully. Opening assets and claims each reconcile to **$284,668 million**. All five projected balance sheets balance, all cash-flow articulation checks pass, and no revolver is required.

## Before-and-after operating NWC definition

| Topic | Original model | V2 diagnostic model |
|---|---|---|
| Formula | Change in inventory + change in all other assets − change in accounts payable − change in all other liabilities | Change in receivables + change in inventory − change in accounts payable − changes in four identified operating accruals |
| Other assets | One $79,007 aggregate projected as a percentage of revenue | Individually shows receivables, prepaid/other, lease assets, goodwill, and other long-term assets; only receivables enter operating NWC |
| Other liabilities | One $64,197 aggregate projected as a percentage of revenue | Individually shows supported operating accruals and excluded tax, lease, financial, NCI, and mixed balances |
| Long-term/nonoperating balances | Changes passed through FCFF as operating working capital | Excluded from operating NWC and held constant pending evidence |
| Historical working-capital drivers | 40.2 inventory days and 42.8 payable days | Exact FY2026 filing-implied 40.1211 inventory days and 42.9912 payable days |
| FCFF | EBIT × (1 − tax rate) + D&A − capex − aggregate change in NWC | EBIT − assumed cash operating tax + D&A − capex − change in defined operating NWC |

The original `project1_fcff.py` imports `walmart_proforma`, not `walmart_project1_proforma`. Their base inputs currently match, but v2 removes that indirect lineage by importing `walmart_project1_proforma_v2` directly.

## FY2026 opening reconciliation

### Assets

| Opening balance | Amount | Operating-NWC treatment |
|---|---:|---|
| Cash | $10,727 | Excluded; retained for balance-sheet cash articulation and provisional equity bridge |
| Receivables, net | 11,172 | Included provisionally; filing line is verified but contains some tax and real-estate receivables that cannot be separated |
| Inventory | 58,851 | Included |
| Prepaid expenses and other | 4,124 | Excluded because the filing does not provide an operating/nonoperating split |
| Property and equipment, net | 136,083 | Excluded from NWC; rolled through capex and D&A |
| Operating lease ROU assets | 14,750 | Excluded and held constant pending a lease roll-forward |
| Finance lease ROU assets | 6,123 | Excluded and held constant pending a lease roll-forward |
| Goodwill | 28,735 | Excluded and held constant |
| Other long-term assets | 14,103 | Excluded and held constant; contains investments, deferred-tax assets, intangibles, and other unresolved items |
| **Total assets** | **$284,668** | **Exact filing reconciliation** |

### Liabilities, NCI, and equity

| Opening balance | Amount | Operating-NWC treatment |
|---|---:|---|
| Accounts payable | $63,061 | Included; contains $5,989 supplier-finance obligations that Walmart classifies as AP and operating cash flow |
| Accrued wages and benefits | 7,878 | Included |
| Self-insurance | 5,525 | Included |
| Accrued non-income taxes | 4,110 | Included |
| Deferred gift-card revenue | 2,941 | Included |
| Other accrued liabilities | 10,733 | Excluded because it combines operating items with interest and is not separable from the filing |
| Accrued income taxes | 596 | Excluded from operating NWC; tax expense is assumed paid in cash in the forecast |
| Interest-bearing borrowings | 44,762 | Excluded from NWC; interest and scheduled repayments are modeled separately |
| Operating lease obligations | 15,572 | Excluded and held constant pending a lease roll-forward |
| Finance lease obligations | 6,761 | Excluded from NWC; interest is modeled separately and the provisional bridge subtracts the claim |
| Deferred income taxes and other | 16,549 | Excluded and held constant; contains tax, derivative, indemnity, and unresolved balances |
| Redeemable NCI | 293 | Excluded and held constant |
| Total shareholders' equity | 105,887 | Includes $6,270 nonredeemable NCI; forecast using consolidated net income, dividends, and buybacks |
| **Total claims and equity** | **$284,668** | **Exact filing reconciliation** |

Opening operating NWC is therefore:

```text
Receivables                                      $11,172
+ Inventory                                       58,851
− Accounts payable                               (63,061)
− Accrued wages and benefits                      (7,878)
− Self-insurance                                  (5,525)
− Accrued non-income taxes                        (4,110)
− Deferred gift-card revenue                      (2,941)
                                                 --------
Operating NWC                                   $(13,492)
```

This total is a defined diagnostic measure, not a Walmart-reported subtotal.

## Input lineage and assumptions

| Input | V2 value or method | Lineage | Classification |
|---|---|---|---|
| Revenue, cash, detailed opening balance sheet | FY2026 reported lines | FY2026 Form 10-K | Verified filing facts |
| Cost of sales used to derive days | $535,395 | $706,413 net sales − $171,018 gross profit | Verified arithmetic |
| Inventory days | 40.1211 | $58,851 / $535,395 × 365 | Verified arithmetic; future constancy is an assumption |
| Accounts-payable days | 42.9912 | $63,061 / $535,395 × 365 | Verified arithmetic; includes supplier financing and future constancy is an assumption |
| Receivables | $11,172 opening; constant percentage of revenue thereafter | Reported opening line | Forecast method is an assumption; full line is not purely operating |
| Four operating accruals | Reported opening balances; each held at its opening percentage of revenue | Note 4 | Forecast method is an assumption |
| Revenue growth, margins, cash-SG&A ratios, D&A rate, capex, debt repayment, dividends | Same schedules as the existing project pro forma | Existing model | Preserved provisional assumptions |
| Cash operating tax | 24.5% of positive EBIT for FCFF | Existing model tax assumption | Proxy, not a verified cash-tax forecast |
| Mixed/nonoperating balances | Held constant | Explicit v2 convention | Diagnostic assumption necessitated by missing forecasts; no plug |
| WACC and terminal growth | 7.00% and 2.50% | Existing FCFF model | Provisional assumptions |
| Equity bridge | +$10,727 cash − $44,762 borrowings − $6,761 finance leases | Existing FCFF model | Preserved provisionally; not selected as final |
| Share denominator | 8,022 FY2026 diluted weighted-average shares | Existing FCFF model and 10-K | Historical denominator, not final valuation-date dilution |

## Three-statement architecture

The v2 pro forma retains five annual income statements, balance sheets, and cash-flow articulations for FY2027–FY2031:

- Revenue, gross profit, cash SG&A, D&A, EBIT, interest, assumed tax, and net income form the income statement.
- Receivables, inventory, supported operating accruals, PP&E, debt, cash, revolver, excluded balances, and equity form the balance sheet.
- Net income + D&A − capex − change in operating NWC − debt repayment produces cash available before distributions; dividends, buybacks, and revolver activity then reconcile exactly to cash.
- PP&E rolls as opening PP&E + capex − D&A. Debt rolls through scheduled repayment. Equity rolls through consolidated net income less dividends and buybacks.
- Excluded balances do not move because no supported forecast was available. The model tests that they remain unchanged rather than allowing them to absorb a balance-sheet difference.

The v2 FCFF model independently calculates:

```text
FCFF = EBIT − assumed cash operating tax + D&A − capex − change in operating NWC
```

Interest and debt repayment do not enter FCFF. Cash, borrowings, and finance leases remain in the provisional enterprise-to-equity bridge.

## Diagnostic results

### V2 FCFF schedule

| Year | EBIT | Assumed cash operating tax | D&A | Capex | Change in operating NWC | FCFF |
|---:|---:|---:|---:|---:|---:|---:|
| 2027 | $31,692.6 | $7,764.7 | $14,424.8 | $26,000.0 | $(575.9) | $12,928.6 |
| 2028 | 32,983.9 | 8,081.0 | 15,651.8 | 28,000.0 | (584.8) | 13,139.3 |
| 2029 | 34,228.2 | 8,385.9 | 16,960.7 | 29,000.0 | (579.8) | 14,382.7 |
| 2030 | 35,425.1 | 8,679.2 | 18,236.8 | 30,000.0 | (575.5) | 15,558.4 |
| 2031 | 36,385.5 | 8,914.4 | 19,483.7 | 31,000.0 | (549.9) | 16,504.6 |

A negative change in operating NWC is a cash source. It occurs because the included operating current liabilities grow faster than receivables and inventory under the chosen drivers. This behavior is mechanical and requires economic validation; it is not assumed to be sustainable merely because the balance sheet balances.

### Original versus v2

| Year | Original change in NWC | V2 change in operating NWC | Original FCFF | V2 FCFF | FCFF change |
|---:|---:|---:|---:|---:|---:|
| 2027 | $872.9 | $(575.9) | $11,479.8 | $12,928.6 | +$1,448.8 |
| 2028 | 487.4 | (584.8) | 12,067.2 | 13,139.3 | +1,072.1 |
| 2029 | 484.2 | (579.8) | 13,318.8 | 14,382.7 | +1,063.9 |
| 2030 | 475.9 | (575.5) | 14,506.9 | 15,558.4 | +1,051.4 |
| 2031 | 455.3 | (549.9) | 15,499.5 | 16,504.6 | +1,005.2 |

At the preserved 7.00% WACC, 2.50% terminal growth, and original bridge:

| Diagnostic output | Original model | V2 | Change |
|---|---:|---:|---:|
| Enterprise value | $305,974.3 | $326,976.2 | +$21,001.9 |
| Equity value | 265,178.3 | 286,180.2 | +21,001.9 |
| Value per FY2026 diluted share | $33.06 | $35.67 | +$2.62 |
| Terminal-value share | 82.27% | 81.98% | −0.29 percentage point |

These differences are diagnostic consequences of the revised working-capital definition and exact historical day calculations. They are not revised valuation conclusions.

## Test results

Commands run:

```text
python3 walmart_project1_proforma_v2.py
python3 project1_fcff_v2.py
```

| Test | Result |
|---|---|
| FY2026 opening assets reconcile to $284,668 | **PASS** |
| FY2026 opening claims and equity reconcile to $284,668 | **PASS** |
| Opening defined operating NWC reconciles to $(13,492) | **PASS** |
| Five annual balance sheets balance | **PASS** — maximum absolute gap below $0.000001 million |
| Five annual cash-flow statements articulate to balance-sheet cash | **PASS** |
| Excluded balances remain unchanged absent evidence | **PASS** |
| Minimum cash and revolver limit | **PASS** — minimum cash $10,272.8; maximum revolver $0.0 |
| Five-year FCFF horizon and enterprise-to-equity arithmetic | **PASS** |
| WACC exceeds terminal growth | **PASS** |
| Injected $1 cash-flow error is detected | **PASS** — model raised `FY2027 cash-flow articulation gap 1.000000` |
| Injected unsupported goodwill change is detected | **PASS** — model raised an excluded-balance error |
| WACC equal to terminal growth is rejected | **PASS** — model raised the DCF boundary error |

No execution failures were suppressed.

## Unsupported classifications and unresolved items

1. **Receivables:** the filing line includes customer and supplier balances but also tax and real-estate receivables. V2 provisionally includes the whole line because the operating portion is not disclosed.
2. **Prepaids and other current assets:** excluded in full because no supported split is available; some portion is likely operating.
3. **Other accrued liabilities:** excluded in full because the $10,733 line mixes deferred membership revenue and operating accruals with interest; some portion is likely operating.
4. **Supplier financing:** $5,989 remains in accounts payable and operating NWC consistent with Walmart's presentation, but a valuation-specific financing assessment remains open.
5. **Self-insurance:** modeled as an operating accrual growing with revenue. Claims frequency, severity, reserve development, and the FY2026 expense increase may not scale with revenue.
6. **Leases:** lease assets and obligations are held constant while rent, finance-lease interest, and D&A remain embedded or approximated in forecast lines. A complete lease roll-forward is still required.
7. **Other long-term assets:** investments, deferred-tax assets, intangibles, restricted or financial assets, and operating assets remain aggregated and excluded. V2 does not invent a residual split.
8. **Deferred income taxes and other:** tax, derivatives, indemnities, and other balances remain aggregated and excluded. V2 assumes cash tax equals modeled tax expense and does not forecast deferred taxes.
9. **NCI:** redeemable NCI is held constant and nonredeemable NCI remains inside total equity. Subsidiary earnings, distributions, ownership changes, and market value are not separately forecast.
10. **Excluded-balance constancy:** holding mixed/nonoperating balances flat is transparent and balance-preserving but not an economic forecast. Acquisitions, investments, lease additions, tax movements, FX, impairments, and dispositions could change them.
11. **Revenue and margin:** the model continues to apply gross margin to total revenue although Walmart defines reported gross profit from net sales. Membership and other income remain blended.
12. **Cash tax rate:** 24.5% is a provisional proxy, not a forecast derived from jurisdictional cash taxes, NOLs, credits, deferred taxes, or discrete items.
13. **Bridge and WACC:** the January 31 cash, debt, finance leases, historical share denominator, 7.00% WACC, and 2.50% growth rate are preserved only for comparability. They are not finalized for September 23, 2026.

V2 improves classification transparency and accounting controls, but its output remains **diagnostic, not final**.
