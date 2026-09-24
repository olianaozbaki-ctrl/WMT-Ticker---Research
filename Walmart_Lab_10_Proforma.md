# Walmart Inc. (WMT) — Five-Year Pro-Forma and FCFE Value

**Question:** What are five years of Walmart's statements worth, built from assumptions I can defend?  
**Historical base:** Fiscal year ended January 31, 2026  
**Forecast:** FY2027E–FY2031E  
**Units:** USD millions except per-share amounts  
**Model:** [`walmart_proforma.py`](walmart_proforma.py)  
**Purpose:** FIN 43900 learning exercise; not investment advice

## Answer

The base case values Walmart's equity at **$274.08 billion, or $34.39 per share**. The five explicit forecast years contribute $35.43 billion of present value and the terminal value contributes $238.65 billion, or **87.07%** of total modeled equity value. The result depends most heavily on the forecast margin, capital spending, working-capital ratios, and 6.85% cost of equity.

Walmart's last completed market close before this report was **$110.53 on September 23, 2026**. [Source: Stock Analysis, WMT historical prices](https://stockanalysis.com/stocks/wmt/history/). The model therefore says $34.39 while the market says $110.53, using 7,969 million fiscal-year-end shares in the model. The research question is: **what sustainable margin, capital-efficiency, or growth improvement would make the market price consistent with the cash Walmart can distribute?** This comparison is not an investment recommendation.

## Three-year filing history

Gross profit below follows Walmart's convention of net sales less cost of sales. Shareholders' equity excludes noncontrolling interests; the linked forecast uses total equity including noncontrolling interests so its consolidated balance sheet balances. See [`Walmart_History_and_Assumptions.md`](Walmart_History_and_Assumptions.md) for the fully sourced history and ratio schedules.

| Fiscal year ended January 31 | FY2024 | FY2025 | FY2026 | Filing source |
|---|---:|---:|---:|---|
| Total revenue | 648,125 | 680,985 | 713,163 | FY2026 10-K, Statements of Income, p. 52 |
| Gross profit (calculated) | 152,495 | 162,785 | 171,018 | Net sales less cost of sales; FY2026 10-K, Item 7 and p. 52 |
| Reported operating, selling, general and administrative expense | 130,971 | 139,884 | 147,943 | FY2026 10-K, p. 52 |
| Consolidated net income | 16,270 | 20,157 | 22,270 | FY2026 10-K, p. 52 |
| Inventory | 54,892 | 56,435 | 58,851 | FY2024: FY2025 10-K, Balance Sheets; FY2025–FY2026: FY2026 10-K, p. 54 |
| Property and equipment, net | 110,810 | 119,993 | 136,083 | FY2024: FY2025 10-K, Balance Sheets; FY2025–FY2026: FY2026 10-K, p. 54 |
| Walmart shareholders' equity | 83,861 | 91,013 | 99,617 | FY2024: FY2024 10-K; FY2025: FY2025 10-K; FY2026: FY2026 10-K, p. 54 |

Primary filings:

- [Walmart FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), filed March 13, 2026.
- [Walmart FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416925000021/wmt-20250131.htm), filed March 14, 2025.
- [Walmart FY2024 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416924000056/wmt-20240131.htm), filed March 15, 2024.

Manual checks completed against the filing: FY2026 total revenue of $713,163 million on the income statement and FY2026 inventory of $58,851 million on the balance sheet.

## Ratios earned from the filings

Reported SG&A includes depreciation and amortization. The model subtracts D&A from reported SG&A to create **cash SG&A**, then forecasts D&A separately; otherwise depreciation would be counted twice.

| Ratio | FY2024 | FY2025 | FY2026 | Calculation/source |
|---|---:|---:|---:|---|
| Reported net-sales growth | 6.1% | 5.0% | 4.7% | Walmart Item 7 consolidated results |
| Walmart U.S. comparable-sales growth | 5.5% | 4.8% | 4.3% | FY2026 10-K, Item 7, pp. 34 and 38–39 |
| Gross margin on net sales | 23.73% | 24.13% | 24.21% | Gross profit ÷ net sales |
| Reported SG&A ÷ gross profit | 85.89% | 85.93% | 86.51% | Reported SG&A ÷ gross profit |
| Inventory days | 40.88 | 40.25 | 40.12 | Inventory ÷ cost of sales × 365 |
| Accounts-payable days | 42.31 | 41.84 | 42.99 | Accounts payable ÷ cost of sales × 365 |
| D&A ÷ year-end PP&E | 10.70% | 10.81% | 10.44% | D&A from cash flows ÷ current-year net PP&E, following the video convention |
| Capital spending ÷ revenue | 3.18% | 3.49% | 3.74% | Property-and-equipment payments ÷ revenue |
| Effective tax rate | 25.53% | 23.38% | 24.43% | Tax expense ÷ pretax income |

The cash-flow inputs—D&A of $11,853 million, $12,973 million, and $14,203 million and capital spending of $20,606 million, $23,783 million, and $26,642 million—come from the [FY2026 10-K, Statements of Cash Flows, p. 56](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm).

## Company-specific line

**Accounts payable is Walmart's company-specific line.** A high-volume retailer sells much of its inventory before supplier invoices are due, so supplier credit partly finances inventory. Walmart's FY2026 accounts-payable days (42.99) exceeded its inventory days (40.12); omitting accounts payable would remove a recurring source of operating cash and understate FCFE. The model therefore forecasts inventory and accounts payable from cost of sales using separate day assumptions and carries both changes through cash flow.

## Forecast assumptions

| Assumption | Base-case value | Label | Reason |
|---|---:|---|---|
| Revenue growth, FY2027E–FY2031E | 4.3%, 4.2%, 4.0%, 3.8%, 3.5% | Judgment | Starts at FY2026 Walmart U.S. comparable growth and fades below Walmart's recent 4.7% consolidated growth as scale increases. |
| Gross margin on total revenue | 25.00% → 25.30% | Judgment | FY2026 was 24.93%; only 30 bps of expansion is assumed over five years for higher-margin businesses and disciplined inventory. |
| Cash SG&A ÷ gross profit | 75.2% → 74.5% | Judgment | Holds near the 75.2% FY2026 ratio, then assumes modest operating leverage rather than a sharp cost reduction. |
| D&A ÷ opening PP&E | 10.6% | History | The video's D&A ÷ year-end PP&E measure averaged about 10.65% over FY2024–FY2026; 10.6% is then applied consistently to forecast opening PP&E. |
| Capital spending | $26.0B, $28.0B, $29.0B, $30.0B, $31.0B | Guidance / judgment | FY2027 begins at the midpoint of management's $25B–$27B outlook; later years rise with Walmart's asset base. |
| Effective tax rate | 24.5% | Judgment | Near FY2026's 24.43% and inside the recent 23.38%–25.53% range. |
| Inventory days | 40.2 | History | Near the FY2025–FY2026 results and slightly below the three-year average. |
| Accounts-payable days | 42.8 | History | Near the 42.38-day three-year average; preserves retailer supplier financing without assuming further extension. |
| Other assets ÷ revenue | 11.08% | History | Holds the FY2026 aggregated ratio constant. |
| Other liabilities ÷ revenue | 9.00% | History | Holds the FY2026 aggregated ratio constant. |
| Scheduled debt repayment | $3.542B, $3.237B, $3.389B, $2.143B, $2.600B | Guidance | Matches the annual principal maturities in FY2026 10-K Note 5, pp. 65–67. |
| Debt / finance-lease interest rates | 4.5% / 5.7% | History / judgment | Anchored to FY2026 reported interest expense and finance-lease interest; held flat for transparency. |
| Dividends | $8.0B in FY2027, then +3% yearly | Guidance / judgment | FY2026 cash dividends were $7.507B and the FY2027 per-share dividend increased from $0.94 to $0.99. Later growth is deliberately slower. |
| Share repurchases | $0 | Judgment | Repurchases are discretionary. The base case suspends them because FCFE first funds dividends and scheduled debt maturities; resumption is a review trigger. |
| Minimum cash / revolver limit | $8.0B / $15.0B | Judgment / history | The cash floor is below FY2026 cash of $10.727B; the revolver limit matches disclosed undrawn committed U.S. credit lines. |
| Cost of equity / terminal growth | 6.85% / 2.5% | Judgment | Cost of equity retains the prior DCF's 4.1% risk-free rate, 0.55 beta, and 5.0% equity-risk premium. Terminal growth is below the discount rate and approximates long-run nominal growth. |
| Shares outstanding | 7,969 million | Fact | FY2026 year-end common shares outstanding, used so equity value and the market comparison are on the same count. |

The [FY2026 10-K MD&A, pp. 34–39](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) supports the comparable-sales, margin, capital-spending, dividend, liquidity, and operating explanations. Debt and lease inputs come from Notes 5–6, pp. 65–69.

## Five-year output

| Line | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---:|---:|---:|---:|---:|
| Revenue | 743,829.0 | 775,069.8 | 806,072.6 | 836,703.4 | 865,988.0 |
| Operating income | 31,692.6 | 32,983.9 | 34,228.2 | 35,425.1 | 36,385.5 |
| Net income | 22,116.2 | 23,211.4 | 24,251.5 | 25,264.7 | 26,077.5 |
| Free cash flow to equity | 6,126.0 | 7,138.8 | 8,339.0 | 10,882.7 | 11,506.0 |
| Ending cash | 8,853.0 | 8,000.0 | 8,000.0 | 9,744.5 | 12,246.4 |
| Assets − liabilities − equity | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

The model draws $248.2 million of the revolver in FY2028 and another $148.2 million in FY2029 to maintain the $8.0 billion cash floor, then repays the full $396.4 million in FY2030. This occurs because forecast FCFE initially falls short of dividends after scheduled debt maturities; no revolver balance remains in FY2030 or FY2031.

## Validation

Run:

```text
python3 walmart_proforma.py
```

The script prints all three statements, checks the balance sheet and cash floor, and calls `assert_balanced` before valuation. A deliberate failure test is also available:

```text
python3 walmart_proforma.py --break-check
```

That test replaces computed FY2027 cash with opening cash and the model refuses to value the company:

```text
ValueError: FY2027E balance-sheet gap: 1873.986157
```

Cash is computed last because it is the consequence of earnings, investment, working capital, financing, and shareholder distributions. Typing cash independently can conceal a broken link; the balance check exposes the error before valuation.

## Fresh-eyes review

**Partner attack on my Walmart model:** Why are you assuming Walmart's gross margin will increase from 25.00% to 25.30% over the forecast period when FY2026 gross margin was lower, and what would make you change that assumption?

**My answer:** I assumed gradual margin improvement because Walmart's higher-margin businesses, including membership and other income, could improve the overall mix over time. I would lower the assumption if future results show gross margin remaining near its historical level or declining because of pricing, merchandise mix, or cost pressure.

**My attack on my partner's Tesla model:** Why are you assuming Tesla can maintain the revenue growth rate used in your forecast over all five years, and what specific change in Tesla's performance would make you lower that assumption?
