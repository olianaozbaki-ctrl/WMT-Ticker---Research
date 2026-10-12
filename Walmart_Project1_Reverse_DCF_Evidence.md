# Walmart Project 1 — Reverse DCF Evidence (V3)

**Status:** Diagnostic, not a final valuation or investment recommendation. The analysis imports and reruns the unchanged V3 forecast and DCF modules. Dollar figures are USD millions unless otherwise noted.

## Market price and V3 reference case

The observed Walmart (WMT) closing price was **$110.53 on September 23, 2026**. The dated historical-price table reports the September 23 open/high/low/close as $110.22/$111.23/$109.49/$110.53. [StockAnalysis historical prices](https://stockanalysis.com/stocks/wmt/history/) independently agrees with the [FinanceCharts historical table](https://www.financecharts.com/stocks/WMT/summary/price). The price date matches the proposed Project 1 valuation date.

At V3's unchanged 7.00% WACC, 2.50% terminal growth, operating forecast, provisional bridge, and August 26 basic-share denominator, the model returns **$36.7804 per share**. That is $73.7496 below the September 23 close; the market price is about 3.004x the V3 output. The DCF is not a same-date diluted-share valuation: V3 uses July 31 bridge balances and August 26 basic shares, with no September 23 stub-period discounting.

## Reverse-solve method

`walmart_project1_reverse_dcf_v3.py` performs two separate one-driver bisection solves. All non-solved assumptions remain at V3 values. Each solved scenario reruns the V3 three-statement forecast, FCFF schedule, enterprise-to-equity bridge, and per-share calculation; neither script nor model is calibrated or overwritten.

| Solve | Single driver changed | Solved path | Repriced output | Checks |
|---|---|---|---|---|
| Revenue growth | Add the same 11.1845 percentage points to each year's net-sales growth and membership/other-income growth | FY2027–FY2031: **15.4845%, 15.3845%, 15.1845%, 14.9845%, 14.6845%** | $110.5300/share; EV $919,965.972; equity $876,916.972 | PASS |
| Operating efficiency | Reduce cash operating expense / operating gross profit by 17.1921 percentage points in each year | Ratios: **58.0079%, 57.8079%, 57.6079%, 57.4079%, 57.3079%** | $110.5300/share; EV $919,965.972; equity $876,916.972 | PASS |

The growth solution raises combined revenue from V3 opening revenue of $713,163 to $1,443,436.6 in FY2031, a roughly **15.14% five-year CAGR**. Its annual EBIT margins rise from 4.65% to 5.30%. Annual FCFF is $18,462.2, $23,749.3, $31,057.6, $39,438.5, and $48,753.4. The terminal value is **86.06%** of EV.

The efficiency solution leaves V3 revenue growth unchanged. Annual EBIT margins rise to approximately **8.9%**; annual FCFF is $37,941.0, $39,379.2, $41,809.4, $44,115.6, and $46,146.2. The terminal value is **81.46%** of EV.

Both solves reproduce the sourced price to within the $0.00000001 display precision. Each passes the existing V3 balance-sheet/cash-flow/revolver controls and the DCF bridge/rate checks. Passing is an arithmetic and model-control result, not evidence that the solved assumption is economically likely.

## Interpretation and limitations

The market price requires a much stronger operating path than V3's base case under the unchanged provisional discount rate, terminal growth, bridge, and share denominator. The reverse solve is not unique: either exceptionally high growth or a large operating-efficiency improvement can produce the same share price. Combinations of growth, margins, reinvestment, working capital, WACC, terminal growth, and bridge values could also do so; one price cannot identify them separately.

The growth case assumes growth stays unusually high across both net sales and membership/other income and does not introduce a fade beyond FY2031. The efficiency case assumes a 17.19-point reduction in the operating-expense ratio without identifying a source-backed operating program. Both retain V3's flat/forecast capital expenditure, cash-tax, working-capital, debt, lease, and distribution assumptions. Terminal value remains more than 80% of EV, so small changes in terminal economics or WACC can dominate the apparent fit.

The expectations would be challenged if future filings show sustained net-sales and membership growth materially below the implied path, operating margins that fail to expand toward the implied level, or materially higher capex/working-capital needs; they could be supported by sustained high growth, mix and productivity improvements, or digital/advertising profit contributions that exceed the base model. Those are monitoring tests, not claims that the market embeds one uniquely identifiable forecast.

## Reproducibility

Run from the project directory:

```text
python3 walmart_project1_reverse_dcf_v3.py
```

The run completed with: growth solve **PASS**; efficiency solve **PASS**; unchanged V3 statement controls **PASS**; DCF checks **PASS**. The companion script prints annual revenue, EBIT, EBIT margin, FCFF, cash, revolver, enterprise value, equity value, price, and terminal-value share.
