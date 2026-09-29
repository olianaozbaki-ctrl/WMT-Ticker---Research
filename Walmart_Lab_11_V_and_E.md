# Walmart Inc. (WMT) — Lab 11 Parts V and E

**Model:** [`walmart_proforma.py`](walmart_proforma.py)  
**Forecast period:** FY2027E–FY2031E  
**Financial statement units:** USD millions, except per-share amounts  
**Free-cash-flow measure:** Free cash flow to equity (FCFE)

## V — Check the Result

### 1. Base Before and After the Analysis

The original base run and the restored base run use separate fresh copies of `BASE_INPUTS`. The sensitivity cases do not mutate the stored base assumptions. The original and restored results are identical at full model precision and therefore match within the model's stated accounting tolerance of `1e-6`. They also match at the displayed precision of one decimal place for financial-statement amounts and two decimal places for value per share.

| Base input path, FY2027E–FY2031E | Original base | Restored base | Check |
|---|---|---|---|
| Revenue growth | 4.3%, 4.2%, 4.0%, 3.8%, 3.5% | 4.3%, 4.2%, 4.0%, 3.8%, 3.5% | Match |
| Cash SG&A as % of revenue | 18.800%, 18.825%, 18.850%, 18.837%, 18.849% | 18.800%, 18.825%, 18.850%, 18.837%, 18.849% | Match |

| Base result | Original base | Restored base | Difference | Check |
|---|---:|---:|---:|---|
| FY2031E operating profit | $36,385.5 | $36,385.5 | $0.0 | Match |
| FY2031E FCFE | $11,506.0 | $11,506.0 | $0.0 | Match |
| Value per share | $34.39 | $34.39 | $0.00 | Match |

At full model precision, both runs produced FY2031E operating profit of `36,385.47219121082`, FY2031E FCFE of `11,505.995734271237`, and value per share of `34.393862172257116`.

### 2. Lower or Higher Run

The higher revenue-growth case provides an isolation check. It changed only the independent input stored under `revenue_growth`:

| Forecast year | Base revenue growth | Higher revenue growth | Change |
|---|---:|---:|---:|
| FY2027E | 4.3% | 5.3% | +1.0 percentage point |
| FY2028E | 4.2% | 5.2% | +1.0 percentage point |
| FY2029E | 4.0% | 5.0% | +1.0 percentage point |
| FY2030E | 3.8% | 4.8% | +1.0 percentage point |
| FY2031E | 3.5% | 4.5% | +1.0 percentage point |

The model's input comparison identified `revenue_growth` as the only changed independent input. Gross margin, cash SG&A ratios, D&A, capital expenditures, tax rate, working-capital assumptions, debt assumptions, dividends, liquidity assumptions, valuation assumptions, share count, and opening balances remained at base. Revenue, gross profit, operating expenses, operating profit, taxes, working capital, cash, financing, FCFE, and valuation then recalculated through the linked model.

The SG&A cases use the existing `cash_sga_to_gross_profit` model input. The sensitivity routine translates the requested cash SG&A percentages of revenue into that existing variable while keeping gross margin and every other independent assumption at base.

### 3. Accounting Checks

The accounting and liquidity checks passed for all six usable sensitivity runs across all five forecast years.

| Driver | Case | Balance-sheet check | Minimum-cash check | Revolver-limit check | Overall status |
|---|---|---|---|---|---|
| Revenue growth | Lower | Passed | Passed | Passed | Valid |
| Revenue growth | Base | Passed | Passed | Passed | Valid |
| Revenue growth | Higher | Passed | Passed | Passed | Valid |
| SG&A as % of revenue | Lower | Passed | Passed | Passed | Valid |
| SG&A as % of revenue | Base | Passed | Passed | Passed | Valid |
| SG&A as % of revenue | Higher | Passed | Passed | Passed | Valid |

Every run had a displayed FY2031E balance-sheet gap of $0.0 million. The most borrowing-intensive case, higher SG&A as a percentage of revenue, ended FY2031E with $12,002.2 million drawn on the revolver, below the $15,000.0 million limit. No sensitivity run failed, so no run was excluded from the span calculations or valuation comparison.

### 4. Change from Base

For the lower SG&A-as-a-percentage-of-revenue case, the reported change in FY2031E operating profit can be recomputed directly:

$$
\$40{,}715.4\text{ million} - \$36{,}385.5\text{ million}
= +\$4{,}329.9\text{ million}
$$

Using the unrounded model outputs:

$$
\$40{,}715.412182975255 - \$36{,}385.47219121082
= +\$4{,}329.939991764435
$$

The unrounded result rounds to **+$4,329.9 million**, so the reported change is correct at the model's displayed precision.

### Locked Prediction Reconciliation

My locked prediction was that SG&A as a percentage of revenue would have the larger effect on Walmart's forecast and value **over the ranges tested**. The prediction was supported.

| Output | Revenue-growth span | SG&A/revenue span | Larger span over the ranges tested |
|---|---:|---:|---|
| FY2031E operating profit | $5,375.1 million | $8,659.9 million | SG&A as % of revenue |
| FY2031E FCFE | $3,822.6 million | $6,946.9 million | SG&A as % of revenue |
| Value per share | $9.13 | $17.98 | SG&A as % of revenue |

Over the ranges tested, changing SG&A as a percentage of revenue produced the larger span in all three outputs. SG&A is applied to Walmart's large revenue base, so a change in the expense ratio produces a direct change in operating expense and operating profit. The resulting after-tax earnings and FCFE changes also flow into the valuation.

The result does **not** change my valuation conclusion. The highest value produced by either tested sensitivity was $42.90 per share, which remains below the $110.53 market-price comparison used in the existing Lab 10 analysis. The tested cases therefore do not close the gap between the model's intrinsic value and that comparison price.

The result **does change or sharpen my research priority**. Verifying whether Walmart can sustain the modeled cash SG&A ratio and operating leverage becomes the first research priority because that driver produced the largest forecast and valuation spans over the ranges tested. This is a research priority, not proof that SG&A is inherently the most important driver under every possible range.

### Partner Exchange 2 — Check Each Other's Evidence

- **Result I showed my partner:** Walmart's FY2031E operating profit under the lower SG&A-as-a-percentage-of-revenue case.
- **Base result:** $36,385.5 million.
- **Changed result:** $40,715.4 million.
- **Difference my partner recomputed:** +$4,329.9 million.
- **Did the other independent inputs stay at base?** Yes. Only the selected SG&A assumption changed; all other independent assumptions remained at base.
- **How I traced the result through the statements:** Lower cash SG&A reduced operating expense, which increased operating profit and after-tax earnings. The change then flowed through cash flow to FCFE and value per share.
- **Question or correction from my partner:** Did the lower SG&A case change only the SG&A assumption, or did revenue and gross profit change too?
- **My response:** Only the selected SG&A assumption changed. Revenue and gross profit remained at their base values, while linked operating profit, taxes, cash flow, FCFE, and valuation recalculated through the model.

### Check I Performed on My Partner's Model

- **Partner's company:** Tesla.
- **Driver/scenario I checked:** R&D sensitivity case.
- **Base result:** Exact Tesla numeric values were not retained in my notes.
- **Changed result:** Exact Tesla numeric values were not retained in my notes.
- **Recomputed difference:** Exact Tesla numeric values were not retained in my notes.
- **Whether the other inputs stayed at base:** Yes. Only the selected R&D assumption changed; the other independent assumptions remained at base.
- **Question or correction I gave:** Could the larger effect from R&D partly reflect the size of the R&D sensitivity range rather than R&D always being Tesla's most important driver?
- **Partner's response:** Yes. The result only shows that R&D had the larger effect over the specific ranges tested, and a different set of ranges could change the comparison.

## E — Find the Driver

For each driver and output, the span is calculated as:

$$
\text{Span} = \text{maximum valid output} - \text{minimum valid output}
$$

### Revenue Growth

| Output | Minimum | Maximum | Span calculation | Output span |
|---|---:|---:|---:|---:|
| FY2031E operating profit | $33,749.6 million | $39,124.7 million | $39,124.7 − $33,749.6 | **$5,375.1 million** |
| FY2031E FCFE | $9,599.5 million | $13,422.1 million | $13,422.1 − $9,599.5 | **$3,822.6 million** |
| Value per share | $29.84 | $38.97 | $38.97 − $29.84 | **$9.13** |

### SG&A as a Percentage of Revenue

| Output | Minimum | Maximum | Span calculation | Output span |
|---|---:|---:|---:|---:|
| FY2031E operating profit | $32,055.5 million | $40,715.4 million | $40,715.4 − $32,055.5 | **$8,659.9 million** |
| FY2031E FCFE | $7,828.2 million | $14,775.1 million | $14,775.1 − $7,828.2 | **$6,946.9 million** |
| Value per share | $24.92 | $42.90 | $42.90 − $24.92 | **$17.98** |

**Over these ranges**, SG&A as a percentage of revenue had the larger operating-profit span: $8,659.9 million compared with $5,375.1 million for revenue growth.

**Over these ranges**, SG&A as a percentage of revenue had the larger FCFE span: $6,946.9 million compared with $3,822.6 million for revenue growth.

**Over these ranges**, SG&A as a percentage of revenue had the larger value-per-share span: $17.98 compared with $9.13 for revenue growth.

These results do not establish that SG&A as a percentage of revenue is inherently more important. A larger output span can partly reflect the width and construction of the tested input range. Revenue growth was tested at base ±1.0 percentage point, while SG&A as a percentage of revenue was tested at base ±0.5 percentage points. A different set of ranges could produce a different comparison.

### Causal Explanation

The clearest causal link in the actual results is:

**Cash SG&A as a percentage of revenue**  
→ **cash operating expense**  
→ **operating profit**  
→ **taxes and after-tax cash flow**  
→ **FCFE**  
→ **value per share**

Revenue and gross profit remain unchanged across the three SG&A cases. FY2031E revenue stays at $865,988.0 million and gross profit stays at $219,095.0 million. The lower SG&A case reduces FY2031E cash SG&A to $158,895.8 million, compared with $163,225.7 million in the base case and $167,555.7 million in the higher case.

Consequently, FY2031E operating profit rises to $40,715.4 million in the lower-expense case and falls to $32,055.5 million in the higher-expense case. The lower-expense case pays more tax—$9,523.1 million compared with $7,268.8 million in the higher-expense case—but still produces greater after-tax earnings and cash flow. FY2031E FCFE therefore ranges from $7,828.2 million to $14,775.1 million, and value per share ranges from $24.92 to $42.90.

### Partner Exchange 3 — Explain and Compare

- **Main driver I explained to my partner:** Walmart's main driver was SG&A as a percentage of revenue over the ranges tested.
- **Causal link I explained:** A change in SG&A as a percentage of revenue changes operating expense, which changes operating profit, taxes and after-tax cash flow, FCFE, and value per share.
- **Question my partner asked about whether the ranking could reflect the chosen ranges:** Could the difference in our main drivers be partly due to the sensitivity ranges we each selected?
- **My answer:** Yes. The comparison only shows which driver produced the larger effect over the specific ranges tested in each model. Different ranges could change the ranking.
- **My partner's main driver:** Tesla's main driver was R&D, which had the larger effect than Revenue Growth over the ranges tested.
- **Why our companies may have different main drivers:** Walmart's main driver was SG&A as a percentage of revenue, while Tesla's was R&D. The difference may reflect the companies' different business models and cost structures.
- **My summary of my partner's conclusion:** R&D had the larger effect over the ranges tested because changes in R&D directly affect operating expenses and operating profit, which then flow through taxes, cash flow, and valuation.

The partner comparison should use each model's direction, percentage effects, and business mechanism rather than ranking the companies using raw dollar changes.

### Final Takeaway

Over the ranges tested, SG&A as a percentage of revenue produced the larger effect on Walmart's FY2031E operating profit, FY2031E FCFE, and value per share. The main limitation is that the comparison depends on the selected sensitivity ranges; it does not prove that SG&A is inherently the more important driver under different or normalized ranges.
