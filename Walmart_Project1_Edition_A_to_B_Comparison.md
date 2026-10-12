# Walmart Project 1 — Edition A to Edition B Comparison

**Status:** Evidence-based comparison draft for the student's review; it does not alter either edition or make the investment decision for the student.

## File identity and date note

The actual Edition A file in the project folder is [`Walmart_Project_1_Edition_A.md`](Walmart_Project_1_Edition_A.md), not `Walmart_Project1_Edition_A.md` as named in the request. Two separate Edition B-named artifacts are present:

- [`Walmart_Project_1_Edition_B.md`](Walmart_Project_1_Edition_B.md): an earlier long-form company research report with a March 13, 2026 information cutoff/call date.
- [`Walmart_Project1_Edition_B_Investment_Memo.md`](Walmart_Project1_Edition_B_Investment_Memo.md): a newer committee-memo draft with a proposed September 23, 2026 valuation date.

They are not the same document or date. The new committee memo explicitly preserves Edition A's September 1, 2026 date and the older report as historical work. It is therefore more accurate to compare Edition A to both files separately than to describe the older report as if it contained the newer V3 valuation.

## Concise before-and-after comparison

| Topic | Edition A — September 1, 2026 | Earlier research report — March 13, 2026 cutoff | Newer committee memo — proposed September 23, 2026 |
|---|---|---|---|
| Decision | Watch-defer: keep researching before deciding whether to initiate. | Watch-defer: operating performance merits research, but 10-K alone does not establish buy-worthiness. | Watch–Defer remains provisional. At stored $110.53 close, model/comparable references are far lower; defer initiation while source gaps remain. |
| Main evidence | FY2026 10-K facts: net sales $706.413B (+4.7%), operating income $29.825B, cash $10.727B, debt $44.762B, and FY diluted weighted-average shares 8.022B. | More detailed 10-K operating evidence: gross-profit rate 24.2% vs 24.1%, operating margin 4.2% vs 4.4%, U.S. comps +4.3%, and eCommerce contribution to comps. Debt and finance-lease lines are tabulated. | Adds FY2027 H1 data from the July 31 10-Q, five-year V3 forecast, DCF/scenarios, bridge, reverse DCF, Target/Costco comps, and cold-run checks. |
| Valuation | No completed forecast or valuation; lists growth, margins, capex, working capital, WACC, terminal growth, and bridge as open work. | No completed market-price valuation; calls for normalization, research into capital returns, and a market-price-based DCF/comps. | Reports V3 base $36.78 and scenario outputs $32.40/$36.78/$44.00 per August 26 basic share; conditional reference zone $31–$49; these are explicitly provisional/diagnostic. |
| Risks / unknowns | Growth sustainability, margins, reinvestment, and whether intrinsic value supports initiating. | Margin conversion, capital-program returns, digital/eCommerce economics, normalization, lease/NCI/investment treatment, and market-implied value. | Adds WACC, valuation-date shares/bridge, lease consistency, working-capital classification, terminal-value concentration, and reverse-DCF expectations as explicit limitations. |
| Research plan | Build history, forecast, FCFF/WACC/terminal value/bridge, and sensitivities. | Detailed six-step plan for operating history, bridge, business mix, normalization, scenarios/multiples, and falsification. | Specifies remaining sourcing/reconciliation tasks and quarterly monitoring triggers; it still does not claim the gaps are resolved. |

## What changed in the analysis

Edition A is a short pre-valuation baseline. It identified Walmart's FY2026 filing facts, set a Watch-defer starting thesis, and named the work still needed; it did not include a multi-year model or a market-price conclusion.

The earlier `Walmart_Project_1_Edition_B.md` expanded the operating narrative from the same FY2026 10-K. It added gross-profit and operating-margin comparisons, U.S. comparable-sales and eCommerce facts, a more explicit bridge inventory, and questions around normalization, capital investment, and nonoperating claims. It still stated that market-price valuation and forecast work remained to be done; its call date is March 13, 2026, not the proposed September 23 date.

The newer investment memo and linked support files add substantially more quantitative work:

- A V3 five-year three-statement/FCFF model with separate net sales and membership/other income, revised D&A and finance-lease mechanics, and internal articulation checks.
- A base DCF using 7.00% WACC and 2.50% terminal growth; an illustrative 7.6748% WACC case at about $31.19; no final WACC selection.
- Downside, Base, and Upside operating cases at $32.40, $36.78, and $44.00/share. Their internal balance-sheet, cash-flow, debt/lease-roll, liquidity, and DCF controls report PASS; those checks do not independently validate assumptions.
- A $110.53 September 23 market-price reference and reverse DCF paths that reproduce it under materially more demanding growth or efficiency assumptions.
- Target and Costco EV/EBIT and P/E comparisons, with Target indications around $44.74–$49.24/share and much higher Costco premium indications kept outside the central reference zone.
- A synthetic known-answer bridge test, V2 changed-input test, independent source/definition reviews, and a recorded Python cold run.

The calculations and evidence are documented in the [V3 model change log](Walmart_Project1_Model_V3_Changes.md), [final assumptions review](Walmart_Project1_Final_Valuation_Assumptions.md), [scenario analysis](Walmart_Project1_Final_Scenarios_and_Valuation_Range.md), [reverse DCF](Walmart_Project1_Reverse_DCF_Evidence.md), [comparable valuation](Walmart_Project1_Comparable_Valuation_Triangulation.md), [source check](Walmart_Project1_Independent_Source_Check.md), [bridge review](Walmart_Project1_Equity_Bridge_Review.md), [bridge arithmetic validation](Walmart_Project1_Equity_Bridge_Validation.md), and [cold-run report](Walmart_Project1_Reproducibility_Report.md).

## Assumptions and recommendation: evolution, not reversal

The recommendation has **not changed in label**: Edition A says watch-defer; the older report also says watch-defer; the newer memo recommends Watch–Defer provisionally. What changed is the support for the stance. The newer memo compares model values and peer indications with a September 23 close and concludes that the price requires substantially stronger operating outcomes than the causal V3 cases under the stored assumptions.

The newer analysis also makes the assumptions more visible. It uses 7.00% WACC and 2.50% terminal growth for V3 scenarios, with more than 81% of EV coming from terminal value. The conditional $31–$49 zone combines a rate sensitivity and Target peer reference; it is not a statistically derived fair-value interval and is not an automatic buy/sell threshold. The reverse DCF is a price-fitting exercise, not independent proof of market expectations.

The conclusion is therefore more quantitative but **not more certain**. The newer memo itself says the WACC, valuation-date share count, cash/debt/lease bridge, working-capital classification, and several other assumptions remain provisional. Internal checks pass under model rules, but primary-source re-fetch, economic reasonableness, and valuation-date completeness were not established by the cold run.

## What remains uncertain or unresolved

1. **Date alignment:** Edition A is September 1; the older research report is March 13; the proposed final analysis uses September 23. V3's bridge is July 31 and its shares are August 26, so price, claims, and denominator are not all September 23 observations.
2. **WACC:** 7.00% is a provisional model assumption. Risk-free/ERP maturity pairing, beta, Walmart-specific debt cost, tax rate, and market-value weights need source-supported resolution.
3. **Shares:** August 26 shares are basic, not diluted, and predate the proposed date. FY2026 diluted weighted-average shares are a period average, not a point-in-time valuation denominator.
4. **Cash, debt, and leases:** Cash is not proven excess; the debt amount is a mixed proxy; finance-lease and operating-lease treatment must be consistent with FCFF and bridge definitions.
5. **Other claims/assets:** NCI and nonoperating-investment adjustments are zero in V3 by assumption, not verified as immaterial.
6. **Working capital and forecast:** Some account classifications/supplier-finance treatment remain unresolved. The upside includes a one-time modeled FY2027 working-capital release of about $9.022B without a documented operating plan. Growth, margin, tax, capex, and finance-lease forecast assumptions remain estimates.
7. **Terminal value and comps:** Terminal value dominates DCF. The two-peer comp sample is small; Target TTM EBIT includes a tariff-refund benefit, periods differ, and lease/denominator conventions are not fully aligned.
8. **Submission evidence:** The newer memo is a draft; this folder's prior inventory found no unified AI-use record, final PDFs, three videos/transcripts, or Brightspace receipt. The separate [AI-use record](Walmart_Project1_AI_Use_Record.md) is now available as a draft but still needs student review and approval.

## Judgments requiring the student's own review

- Whether Watch–Defer is still the student's judgment after reviewing the evidence, and what evidence/price/expected-return condition would change it.
- Whether the $31–$49 conditional zone is useful for committee discussion despite its provisional WACC, bridge, share count, and peer limitations; what margin-of-safety rule to use.
- Whether the scenario assumptions and implied market expectations are economically plausible, especially the revenue-stream growth, margin improvement, and upside working-capital release.
- Which valuation conventions to select for cash, debt, leases, NCI, investments, diluted claims, terminal economics, and the WACC.
- Whether the source links and filing facts have been checked against the original publications, and whether the memo's claims are appropriately worded.
- Whether the AI-use record accurately reflects actual tool usage, and how to resolve the Locked Changed-Input Record's “Human-Authored, AI-Off” assertion. That assertion is present in the locked file, but this comparison does not independently prove it.
- Whether to submit the separate Edition B investment memo as the final Edition B document after adding a clear A-to-B change table and required AI-use reference, while preserving the original Edition A and older report.

## Bottom line

Edition A established a documented Watch-defer starting position and a research plan. The older March 13 report deepened the FY2026 operating case but still called for a valuation. The newer September 23 memo adds a full diagnostic modeling and triangulation package and gives a more evidence-based reason to defer at the stored market price. Its result remains conditional, not source-complete or final. The student's investment judgment and final submission review remain essential.
