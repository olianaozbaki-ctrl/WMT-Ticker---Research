# Walmart Project 1 — Final Causal Scenarios and Conditional Valuation Range

**Valuation date:** September 23, 2026 (proposed)  
**Status:** Diagnostic analysis only; preserves the existing Watch–Defer stance pending source verification. No V2/V3 model, original lab, Edition A, or prior validation record was changed.  
**Units:** USD millions except per-share data, percentages, multiples, and days.

## Executive result

The V3 scenario runner produced three coherent cases using the unchanged V3 three-statement and FCFF engines. All three pass statement and DCF arithmetic controls under the model's existing $15,000 million revolver limit. Their model-only values are **$32.40 Downside, $36.78 Base, and $44.00 Upside per August 26 basic share**. These are not final September 23 diluted values.

For broader decision support, the prior DCF rate illustration extends the downside reference to **$31.19**, while the closer selected public peer, Target, indicates **$44.74–$49.24**. The resulting **conditional reference zone is $31–$49 per share**, not a statistically calculated fair-value range and not a single-point conclusion. Costco's much higher peer indication ($125.60–$134.84) and the $110.53 market close are shown separately rather than averaged into the zone.

## Scenario construction

The runner `walmart_project1_v3_final_scenarios.py` imports the unchanged `walmart_project1_proforma_v3.py` and `project1_fcff_v3.py`. It changes independent forecast inputs only. All cases retain 7.00% provisional WACC, 2.50% terminal growth, the same provisional enterprise-to-equity bridge, August 26 basic shares, cash-tax rate, debt rate, debt repayment, dividend policy, finance-lease additions/principal, minimum cash, and $15,000 million revolver limit. WACC, growth, bridge, and date limitations are detailed in [Final Valuation Assumptions](Walmart_Project1_Final_Valuation_Assumptions.md).

### Causal settings and assumptions

| Driver | Downside | Base | Upside |
|---|---|---|---|
| Business cause | Weaker consumer demand, competitive price pressure, slower digital/membership growth, less favorable supplier terms | Current V3 assumptions | Stronger digital/advertising and membership mix, resilient demand, productivity, better inventory/supplier execution |
| Annual net-sales and membership/other growth, FY27–FY31 | 3.8%, 3.7%, 3.5%, 3.3%, 3.0% (V3 less 0.50 percentage point each year) | 4.3%, 4.2%, 4.0%, 3.8%, 3.5% | 5.3%, 5.2%, 5.0%, 4.8%, 4.5% (V3 plus 1.00 percentage point each year) |
| Gross margin on net sales, FY27–FY31 | 24.90%, 25.00%, 25.10%, 25.15%, 25.20% (10 bp below V3) | 25.00%, 25.10%, 25.20%, 25.25%, 25.30% | 25.25%, 25.35%, 25.45%, 25.50%, 25.55% (25 bp above V3) |
| Cash opex / operating gross profit, FY27–FY31 | 75.4%, 75.2%, 75.0%, 74.8%, 74.7% (20 bp worse) | 75.2%, 75.0%, 74.8%, 74.6%, 74.5% | 74.7%, 74.5%, 74.3%, 74.1%, 74.0% (50 bp better) |
| Cash PP&E capex, FY27–FY31 | $26.0bn, $28.0bn, $29.0bn, $30.0bn, $31.0bn; maintain V3 program despite weaker demand | Same as V3 | $27.5bn, $29.5bn, $30.5bn, $31.5bn, $32.5bn; $1.5bn/year incremental growth/productivity investment |
| Inventory days | 41.12 (V3 +1 day) | 40.12 | 37.12 (V3 −3 days) |
| Accounts-payable days | 42.49 (V3 −0.5 day) | 42.99 | 44.99 (V3 +2 days) |
| Receivables / revenue | 1.6165% (V3 +5 bp) | 1.5665% | 1.4665% (V3 −10 bp) |
| Financing policy | Same debt repayment, dividends, lease financing and revolver terms as V3; financing need is allowed to emerge | Same as V3 | Same as V3; no discretionary distribution or debt schedule change to manufacture financing capacity |

The revenue growth paths apply the same annual change to both revenue streams because V3 itself uses the same base growth for net sales and membership/other income. This shared-growth convention is an unverified simplifying assumption, not a Walmart forecast. Gross-margin and expense-ratio changes drive EBIT; working-capital days and receivables ratio drive defined operating NWC. No valuation output or price multiplier is directly manipulated.

V3's opening NWC uses FY2026 reported balances and historical ratios. Moving to the scenario ratios therefore creates a one-time FY2027 working-capital transition: downside uses $2,160 million; upside releases $9,022 million. The upside release is especially material and should be treated as a hypothesis about operational improvement, not recurring FCFF. The subsequent-year FCFF schedule reflects only further changes in the new scenario balances.

## Annual forecast results

### Downside

| FY | Revenue | EBIT | Capex | Change in operating NWC | FCFF | Ending cash | Ending debt | Ending finance leases | Ending revolver |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027 | $740,263.2 | $32,435.5 | $26,000 | $2,160.3 | $9,828.5 | $8,000.0 | $41,220 | $6,573 | $986.3 |
| 2028 | 767,652.9 | 33,528.6 | 28,000 | (416.4) | 12,444.8 | 8,000.0 | 37,983 | 6,385 | 1,927.0 |
| 2029 | 794,520.8 | 34,554.5 | 29,000 | (408.2) | 13,503.7 | 8,000.0 | 34,594 | 6,197 | 2,125.5 |
| 2030 | 820,740.0 | 35,507.4 | 30,000 | (399.6) | 14,479.4 | 8,000.0 | 32,451 | 6,009 | 241.1 |
| 2031 | 845,362.2 | 36,196.4 | 31,000 | (375.1) | 15,215.1 | 9,811.7 | 29,851 | 5,821 | 0.0 |

### Base

| FY | Revenue | EBIT | Capex | Change in operating NWC | FCFF | Ending cash | Ending debt | Ending finance leases | Ending revolver |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027 | $743,829.0 | $33,223.9 | $26,000 | (534.3) | $13,118.4 | $10,303.6 | $41,220 | $6,573 | $0.0 |
| 2028 | 775,069.8 | 34,592.0 | 28,000 | (583.1) | 13,414.3 | 10,369.6 | 37,983 | 6,385 | 0.0 |
| 2029 | 806,072.6 | 35,917.1 | 29,000 | (578.1) | 14,702.3 | 11,442.5 | 34,594 | 6,197 | 0.0 |
| 2030 | 836,703.4 | 37,190.8 | 30,000 | (573.9) | 15,924.7 | 14,852.4 | 32,451 | 6,009 | 0.0 |
| 2031 | 865,988.0 | 38,215.8 | 31,000 | (548.3) | 16,912.9 | 18,612.1 | 29,851 | 5,821 | 0.0 |

### Upside

| FY | Revenue | EBIT | Capex | Change in operating NWC | FCFF | Ending cash | Ending debt | Ending finance leases | Ending revolver |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027 | $750,960.6 | $35,114.4 | $27,500 | (9,022.0) | $21,533.4 | $18,718.7 | $41,220 | $6,573 | $0.0 |
| 2028 | 790,010.6 | 36,927.5 | 29,500 | (1,153.9) | 14,395.2 | 19,765.6 | 37,983 | 6,385 | 0.0 |
| 2029 | 829,511.1 | 38,770.7 | 30,500 | (1,165.7) | 16,223.5 | 22,359.7 | 34,594 | 6,197 | 0.0 |
| 2030 | 869,327.7 | 40,629.0 | 31,500 | (1,182.7) | 18,028.0 | 27,872.9 | 32,451 | 6,009 | 0.0 |
| 2031 | 908,447.4 | 42,291.5 | 32,500 | (1,161.0) | 19,609.2 | 34,328.8 | 29,851 | 5,821 | 0.0 |

## Valuation results

All DCFs use 7.00% WACC and 2.50% terminal growth, and the same bridge: +$11,529 cash, −$47,746 debt proxy, −$6,832 finance leases, $0 NCI, $0 nonoperating investments, divided by 7,933.746241 million August 26 basic shares. The bridge and denominator are not valuation-date verified.

| Scenario | Enterprise value | Equity value | Per August 26 basic share | Change vs. Base | Terminal-value share | Liquidity status |
|---|---:|---:|---:|---:|---:|---|
| Downside | $300,069.4 | $257,020.4 | **$32.3958** | −$4.3846 | 82.35% | Feasible; peak revolver $2,125.5M, below $15,000M limit |
| Base | 334,855.6 | 291,806.6 | **$36.7804** | — | 82.03% | Feasible; no revolver draw |
| Upside | 392,133.3 | 349,084.3 | **$43.9999** | +$7.2195 | 81.21% | Feasible; no revolver draw |

The scenario values form a **$32.40–$44.00 model-only feasible range** at the V3 discount rate and bridge. All cases satisfy `WACC > terminal growth` (7.00% > 2.50%). This is not the complete conditional range because it excludes WACC uncertainty, peer multiples, and bridge/share-count uncertainty.

## Accounting, financing, and DCF validation

The script calls V3 statement and FCFF functions without editing their code. It reports all validation outcomes rather than forcing a plug.

| Control | Downside | Base | Upside |
|---|---|---|---|
| Balance-sheet articulation | PASS; max gap < $0.000001M | PASS; max gap < $0.000001M | PASS; max gap < $0.000001M |
| Cash-flow articulation | PASS; $0.000000M max gap | PASS; $0.000000M max gap | PASS; $0.000000M max gap |
| Borrowing roll-forward | PASS; $0.000000M max gap | PASS; $0.000000M max gap | PASS; $0.000000M max gap |
| Finance-lease roll-forward | PASS; $0.000000M max gap | PASS; $0.000000M max gap | PASS; $0.000000M max gap |
| Nonnegative / minimum cash | PASS; minimum $8,000.0M | PASS; minimum $10,303.6M | PASS; minimum $18,718.7M |
| Revolver capacity | PASS; max $2,125.5M / $15,000M | PASS; $0 / $15,000M | PASS; $0 / $15,000M |
| DCF horizon, rate, bridge, per-share arithmetic | PASS | PASS | PASS |

“PASS” means the forecast articulates under the V3 mechanics and the case stays within the model's financing limits. It does not verify the assumptions, date the bridge to September 23, or establish economic feasibility beyond the modeled five years.

## Comparison with reverse DCF and public comps

The method comparisons below summarize the prior [reverse DCF evidence](Walmart_Project1_Reverse_DCF_Evidence.md) and [comparable valuation / triangulation](Walmart_Project1_Comparable_Valuation_Triangulation.md).

| Evidence | Per-share indication | Interpretation relative to causal scenarios |
|---|---:|---|
| Causal V3 Downside / Base / Upside | $32.40 / $36.78 / $44.00 | All below the September 23 market close; upside remains below the reverse-DCF requirement. |
| V3 Base at 7.6748% illustrative WACC, 2.50% growth | $31.19 | Adds discount-rate sensitivity below the 7.00% Downside; WACC remains illustrative, not final. |
| Target EV/EBIT and P/E | $49.24 / $44.74 | Closest selected peer; its $994M TTM tariff-refund benefit and lagged shares/balances remain limitations. |
| Costco EV/EBIT and P/E | $134.84 / $125.60 | Premium upper reference; membership mix and multiple make it a weak central anchor. |
| Reverse DCF at September 23 close | $110.53 matched | Requires 15.48% to 14.68% growth in both revenue streams, about 15.14% five-year revenue CAGR, **or** cash-opex ratios reduced to about 58.01%–57.31%, producing about 8.9% EBIT margins. |

The reverse DCF is a price-fitting exercise, not another independent value estimate. It demonstrates how far market-implied operating expectations sit above the causal V3 scenarios. The peer methods transfer market multiples and therefore reflect peer selection, their own accounting conventions, and market sentiment; they do not share the V3 cash-flow forecast. The two methods also treat lease claims differently. The DCF is driven by modeled Walmart FCFF and provisional WACC/terminal growth, with over 81% of EV from terminal value in these scenarios.

### Conditional valuation range

Use **$31–$49 per share as a conditional reference zone only**: the low end rounds the $31.19 V3 base at the illustrative 7.6748% WACC; the high end rounds the $49.24 Target EV/EBIT indication using the V3 bridge. It contains the causal V3 cases ($32.40–$44.00) and Target P/E/EV-EBIT indications ($44.74–$49.24), but it is not a statistical interval, does not reconcile method-specific accounting differences, and is not a final fair value. The September 23 close of $110.53 is well above this conditional zone; the Costco result and reverse-DCF solve explain the premium scenario rather than independently validating it.

## Watch–Defer recommendation: what would change it

The existing Watch–Defer posture remains the defensible conditional position at the observed price, rather than treating this range as a trade instruction. Reassessment would be warranted if:

- The market price moved into or below the conditional zone **and** a refreshed model using September 23 shares, cash, debt, finance leases, NCI, and a verified discount rate still supported the relevant value with an explicit margin of safety. No margin-of-safety percentage is invented here.
- Reported results and company disclosures supported the causal Base or Upside path—particularly growth by revenue stream, sustained gross-margin and opex improvements, and the inventory/payables efficiency required for the large FY2027 cash release.
- Conversely, growth/margins weakened or working-capital needs worsened enough to increase revolver use materially; approaching the $15bn cap would invalidate the modeled feasible downside and could warrant a more cautious view.
- Peer selection and lease/accounting definitions became more comparable, or Costco-like membership and margin economics became demonstrably more relevant to Walmart.

The $110.53 close requires markedly stronger modeled economics than the causal Upside case. A recommendation change would need evidence that resolves that gap, not simply the reverse-DCF equality.

## Highest-risk assumptions and unresolved limitations

The highest valuation risk is the **terminal-value/WACC combination**: terminal value represents 81.21%–82.35% of scenario EV, while 7.00% WACC and 2.50% terminal growth are provisional. A 7.6748% illustrative WACC reduces the V3 base from $36.78 to $31.19/share. The highest operating assumption risk is the Upside case's immediate working-capital efficiency shift, which releases $9.022bn in FY2027; it has no specific source-backed operational plan.

Other unresolved limits remain from the existing evidence files:

1. September 23 diluted shares are not established; V3 uses August 26 basic shares.
2. Cash, debt, and finance-lease bridge data are July 31 values, not September 23; excess cash, same-date debt market value, NCI value, and nonoperating investment treatment remain unresolved.
3. Separate source-backed growth forecasts for net sales and membership/other income are unavailable; V3 applies one growth path to both.
4. Cash tax, margin, operating-expense, capex, and forecast financing inputs remain assumptions rather than management guidance.
5. V3's finance-lease additions/principal use FY2026 historical amounts as flat forecast assumptions; operating leases are not forecast as a complete liability schedule.
6. Working capital uses individually selected V3 components, but supplier financing and some mixed accrued/prepaid accounts remain limitations.
7. The DCF uses annual fiscal periods without a September 23 stub-period convention; Costco TTM metrics end May 10 and the peer share/balance observations are from different dates.
8. TTM peer EPS is calculated from rounded reported annual/interim EPS, and the two-peer sample is small and heterogeneous.

## Files created and run results

Created in this task:

- `walmart_project1_v3_final_scenarios.py` — separate scenario runner; imports, does not modify, the V3 engines.
- `Walmart_Project1_Final_Scenarios_and_Valuation_Range.md` — scenario assumptions, results, validation, triangulation, and conditional decision range.

Run from the project folder with:

```text
python3 walmart_project1_v3_final_scenarios.py
```

Run outcome: Downside, Base, and Upside all **FEASIBLE**; balance-sheet, cash-flow, debt roll-forward, finance-lease roll-forward, minimum-cash, revolver, DCF rate, bridge, and per-share arithmetic checks all **PASS**. No existing models or validation records were changed.
