# FIN 43900 Lab 12 — Walmart Presentation and Tesla Peer Review

**My company:** Walmart Inc. (WMT)  
**Learning partner's company:** Tesla, Inc. (TSLA)

## D — Main Question

**How did I get from choosing Walmart to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?**

I began with Walmart as a large, mature retailer with positive earnings, a clear business model, and enough reported history to build a supported forecast. I then moved from filing evidence to historical ratios, forecast assumptions, linked statements, cash flow, and several valuation methods. The methods produced different values, so I kept them separate rather than averaging them. My supported conclusion is **Watch-Defer**: Walmart is a strong business, but the saved market prices were above the values supported by my cash-flow models and peer median. The conclusion could change if Walmart produces stronger sustainable margins and cash flow, if better peer evidence changes the relative valuation, or if the market price falls enough to provide a margin of safety.

# R — Walmart Full Analysis Route

## Stop 1 — Selection and Initial View

### Why did I select Walmart, what makes it suitable to analyze, and what was my initial view?

I selected Walmart because it is a large, mature public company with positive earnings and a long history of reported financial data. Its business model is understandable: most revenue comes from retail sales through stores and e-commerce, with additional membership and other income.

Walmart was suitable for analysis because its filings provide enough history to develop forecast assumptions and compare it with other large retailers. My initial view was that Walmart was relatively stable because of its scale, established market position, and operating history. I expected its value to depend on steady growth, operating efficiency, and cash generation rather than extremely high growth.

## Stop 2 — Business Model and Evidence

### How does Walmart earn money, and what sources, periods, and units support the analysis?

Walmart earns money mainly by selling merchandise through stores, clubs, and e-commerce. It also receives membership and other income, including income connected with Sam's Club and Walmart's developing higher-margin businesses.

- **Historical period:** FY2024–FY2026
- **Fiscal year-end:** Approximately January 31
- **Primary source:** Walmart's Form 10-K filings
- **Financial-statement units:** USD millions unless stated otherwise
- **Valuation output:** USD per common share

Before forecasting, I checked that sources, reporting periods, definitions, and units were consistent. Key FY2026 evidence included $713,163 million of total revenue, $58,851 million of inventory, $10,727 million of cash, and $44,762 million of reported borrowings and long-term debt.

## Stop 3 — History to Pro Forma

### How did historical performance become forecast assumptions, and what are the company-specific drivers?

My process was:

**Historical results → historical ratios and trends → forecast assumptions → linked financial statements → FCFE → valuation**

The main historical ratios and forecast assumptions were:

| Driver | Historical evidence | FY2027E–FY2031E assumption |
|---|---|---|
| Revenue growth | Reported net-sales growth declined from 6.1% to 5.0% to 4.7%; FY2026 U.S. comparable sales grew 4.3% | 4.3%, 4.2%, 4.0%, 3.8%, 3.5% |
| Gross margin | Gross margin on net sales rose from 23.73% to 24.13% to 24.21% | 25.00% rising gradually to 25.30% on total revenue |
| Cash SG&A | FY2026 cash SG&A was approximately 75.2% of modeled gross contribution | 75.2% fading to 74.5% of gross profit |
| D&A | Historical D&A-to-year-end-PP&E averaged about 10.65% | 10.6% of opening PP&E |
| Capital spending | $20.606B, $23.783B, and $26.642B in FY2024–FY2026 | $26B, $28B, $29B, $30B, and $31B |
| Tax rate | 23.38%–25.53% over the historical period | 24.5% |
| Inventory days | 40.88, 40.25, and 40.12 days | 40.2 days |
| Accounts-payable days | 42.31, 41.84, and 42.99 days | 42.8 days |

Revenue growth matters because it changes sales, operating profit, working capital, cash flow, and valuation. SG&A matters because Walmart operates on thin margins and a small expense-ratio change applied to a very large revenue base can materially change profit and FCFE.

Accounts payable is a company-specific driver. Walmart's FY2026 accounts-payable days exceeded its inventory days, so supplier credit is a recurring source of operating financing. The pro forma forecasts inventory and accounts payable separately and carries both changes through cash flow.

The model links the income statement, balance sheet, and cash-flow statement. All six Lab 11 sensitivity runs passed the balance-sheet, minimum-cash, and revolver-limit checks across all five forecast years. Their displayed balance-sheet gaps were $0.0 million.

## Stop 4 — Valuation Methods and Differences

### What valuation methods did I use, and why do they disagree?

I used peer P/E, an FCFF DCF with a reverse DCF, and a later three-statement FCFE valuation. I did **not** average them because they measure value differently and use different dates and assumptions.

### Comparable-company valuation

The repository's reproducible peer calculation produced:

| Company | P/E multiple |
|---|---:|
| Walmart | 41.150183× |
| Target | 18.167282× |
| Costco | 51.729270× |
| Peer median | 34.948276× |

Using Walmart's $2.73 diluted EPS:

| Peer result | Implied Walmart price (USD per common share) |
|---|---:|
| Low | $49.60 |
| Median | $95.41 |
| High | $141.22 |

The saved Walmart market price was **$112.34 per common share on August 5, 2026**. Target was used because its large-scale omnichannel retail model is reasonably similar. Costco was qualified because its paid-membership warehouse model, merchandise mix, and fiscal period differ from Walmart's. Removing Costco reduced the peer-median estimate from $95.41 to $49.60, showing how strongly peer selection affects the result.

### FCFF DCF and reverse DCF

| Item | Existing result |
|---|---:|
| Starting FCFF | $17,033.7 million |
| Explicit FCFF growth | 5.0%, 4.5%, 4.0%, 3.5%, 3.0% |
| WACC | 7.00% |
| Terminal growth | 2.50% |
| Enterprise value | $415,554.97 million |
| Less debt | $44,762 million |
| Plus cash | $10,727 million |
| Equity value | $381,519.97 million |
| Diluted shares | 8,022 million |
| DCF value | **$47.56 per diluted share** |
| Terminal-value share of enterprise value | 80.98% |

The September 9, 2026 market-price comparison was $105.83 per share. Holding WACC, terminal growth, cash, debt, and shares fixed, the reverse DCF required a **+18.18 percentage-point shift** to each annual FCFF growth assumption. The implied five-year FCFF growth path was **23.18%, 22.68%, 22.18%, 21.68%, and 21.18%**. That is much faster than Walmart's recent sales growth and shows what the market price required under this model.

### Three-statement FCFE valuation

The later linked pro forma used a **6.85% cost of equity** and **2.5% terminal growth**. It produced equity value of **$274.08 billion, or $34.39 per share**. The five explicit years contributed $35.43 billion of present value, while the terminal value contributed $238.65 billion, or **87.07%** of modeled equity value.

The DCF methods depend on future cash flows, discount rates, and terminal assumptions. Peer P/E depends on the market multiples and business comparability of Target and Costco. Because these methods answer different questions, I report each result separately.

## Stop 5 — Sensitivity and Main Drivers

### What did the sensitivity analysis show?

Each case changed one independent driver while holding the other independent assumptions at base.

### Revenue growth sensitivity

**Revenue growth → revenue → operating profit → working capital and cash flow → FCFE → value per share**

| Case | FY2027E–FY2031E revenue-growth inputs | FY2031E operating profit | FY2031E FCFE | Value per share |
|---|---|---:|---:|---:|
| Lower | 3.3%, 3.2%, 3.0%, 2.8%, 2.5% | $33,749.6M | $9,599.5M | $29.84 |
| Base | 4.3%, 4.2%, 4.0%, 3.8%, 3.5% | $36,385.5M | $11,506.0M | $34.39 |
| Higher | 5.3%, 5.2%, 5.0%, 4.8%, 4.5% | $39,124.7M | $13,422.1M | $38.97 |

The value-per-share span was **$9.13**.

### Cash SG&A as a percentage of revenue sensitivity

**SG&A percentage → cash operating expense → operating profit → taxes and cash flow → FCFE → value per share**

| Case | FY2027E–FY2031E cash SG&A/revenue inputs | FY2031E operating profit | FY2031E FCFE | Value per share |
|---|---|---:|---:|---:|
| Lower expense | 18.300%, 18.325%, 18.350%, 18.337%, 18.349% | $40,715.4M | $14,775.1M | $42.90 |
| Base | 18.800%, 18.825%, 18.850%, 18.837%, 18.849% | $36,385.5M | $11,506.0M | $34.39 |
| Higher expense | 19.300%, 19.325%, 19.350%, 19.337%, 19.349% | $32,055.5M | $7,828.2M | $24.92 |

The value-per-share span was **$17.98**. Therefore, SG&A as a percentage of revenue produced the larger valuation effect **over the tested ranges**. This happened because the expense percentage applies directly to Walmart's large revenue base and flows through operating profit, taxes, FCFE, and valuation.

This result does not prove that SG&A is always Walmart's most important or most uncertain driver, or that either sensitivity case is likely. Sensitivity measures model impact, not probability. The ranking also depends on the selected ranges: revenue growth was changed by ±1.0 percentage point, while SG&A/revenue was changed by ±0.5 percentage point.

## Stop 6 — Conclusion and Next Evidence

### What conclusion does the analysis support, what could change it, and what comes next?

My supported conclusion is **Watch-Defer**. Walmart's operating performance supports continued research, but the saved market prices were above the FCFF DCF, FCFE value, and peer-median value. Even the highest Lab 11 sensitivity value, $42.90 per share, remained below the $110.53 market comparison used in the pro-forma analysis.

I would reconsider the conclusion if:

- Walmart's price moved closer to supported cash-flow value. The FCFF work identified below $55, or roughly $50–$55, as a possible entry area under those assumptions.
- Quarterly evidence showed sustainable consolidated operating-margin expansion beyond 5.5% and normalized FCFF above $28 billion.
- Advertising, marketplace, membership, e-commerce, and automation produced measurable margin and cash-flow improvements.
- Better-matched peers or updated earnings materially changed the peer range.
- Supported revisions to growth, margins, capital spending, or the discount rate materially changed the DCF.

Evidence that would weaken the case includes persistent SG&A pressure, continued high capital spending without better returns, weaker comparable sales, worse working-capital efficiency, or price investment that prevents margin improvement.

My next research priorities are SG&A and operating leverage, e-commerce profitability, returns on capital spending, membership and Sam's Club growth, and whether Target and Costco remain the best peers.

# V — Questions I Received as the Walmart Presenter

## Question 1 — Why did you choose Revenue Growth and SG&A % of Revenue?

I chose Revenue Growth because it directly changes Walmart's projected sales and then affects operating profit, working capital, FCFE, and value. I chose SG&A % of Revenue because Walmart has thin operating margins, so a small expense-rate change applied to a large revenue base can materially affect profitability and value.

## Question 2 — Why is the peer-implied price range so wide?

Target's P/E was 18.167282× while Costco's was 51.729270×. Applying these very different multiples to Walmart's EPS produced a $49.60–$141.22 implied range. Costco's membership model and market valuation make it a less direct peer. Removing Costco lowered the estimate to $49.60, so peer selection is a major limitation.

## Question 3 — Which assumption had the greatest effect?

SG&A as a percentage of revenue had the greater effect **over the tested ranges**. Its value-per-share span was $17.98, compared with $9.13 for Revenue Growth. Lower cash SG&A increased operating profit, after-tax earnings, FCFE, and value; higher cash SG&A did the opposite. This ranking depends on the tested ±0.5-point SG&A range and ±1.0-point growth range. It does not establish which variable is always most important or most uncertain.

# Tesla — My Review of My Partner's Analysis

## Tesla Selection and Evidence

My partner selected Tesla because it combines substantial risk with substantial growth opportunities. The automotive business struggled in FY2025, while energy grew, and Tesla continued investing in AI, autonomy, robotics, batteries, and other technologies. The main question was whether future growth, margins, and free cash flow could support Tesla's valuation.

| Metric | FY2025 result |
|---|---:|
| Revenue | $94.8B |
| Automotive revenue | $69.5B |
| Automotive share of revenue | 73.3% |
| Automotive revenue change | -10% |
| Energy revenue | $12.8B |
| Energy share of revenue | 13.5% |
| Energy revenue growth | +27% |
| Energy gross margin | 29.8% |
| Net income | $3.8B |
| Net margin | About 4.0% |
| Operating cash flow | $14.7B |
| Capital expenditures | $8.5B |
| Cash plus short-term investments | $44.1B |
| Debt | $8.2B |

The main evidence was the contrast between automotive and energy. Total revenue declined approximately 3% and automotive revenue declined 10%, while energy revenue grew 27% and earned a 29.8% gross margin.

## Tesla Pro Forma

My partner forecast Tesla from 2026 through 2030.

| Assumption | 2026 | 2030 | Reason |
|---|---:|---:|---|
| Revenue growth | 15% | 8% | Renewed growth that slows as Tesla becomes larger |
| Revenue | $109.1B | $166.9B | Result of forecast growth |
| Gross margin | 18.0% | 21.5% | Improved mix, utilization, and efficiency |
| R&D / Revenue | 7.0% | 6.0% | Continued investment with some scale benefits |
| Capital expenditures | $20.5B | $12.0B | Heavy near-term investment that gradually decreases |
| Operating margin | 5.0% | 10.0% | Improved future profitability |
| Cost of equity | 10% | 10% | Required return for FCFE |
| Terminal growth | 3% | 3% | Sustainable long-term growth |
| Minimum cash | $10B | $10B | Minimum liquidity assumption |

Tesla's company-specific pathway was:

**Higher R&D → higher operating expenses → lower operating income → lower FCFE → lower modeled value per share**

This does not automatically make R&D bad. Successful R&D could create products, revenue, and future cash flow. The model's accounting check was **Assets − Liabilities − Equity = 0**.

## Tesla Valuation and Sensitivity

| Valuation method | Value per share (USD per common share) |
|---|---:|
| Qualified-peer P/E | $28.28 |
| DCF | $38.82 |
| Five-year FCFE pro forma | $31.14 |
| Saved market price | $356.09 |

Tesla used a 10% cost of equity and 3% terminal growth. GM was the qualified GAAP-EPS peer. The conventional values of approximately $28–$39 per share were far below the $356.09 saved market price. This does not mean Tesla's stock must fall to the modeled values. It means the conventional automotive and cash-flow assumptions did not explain the higher market valuation. Supporting that price would require additional economic value from energy, AI, autonomy, robotics, stronger growth, or other opportunities. Tesla's reverse DCF is **unresolved** because no actual partner result was provided.

| Driver | Sensitivity change | Value-per-share range | Change from $31.14 base |
|---|---:|---:|---:|
| Revenue Growth | ±3 percentage points | $27.32–$35.27 | -12.3% to +13.3% |
| R&D / Revenue | ±1 percentage point | $26.44–$35.84 | -15.1% to +15.1% |

Over these tested ranges, R&D produced the larger value-per-share effect. Revenue growth had a larger effect on operating income, but it also increased working-capital requirements, so not all additional operating earnings became FCFE. The ranking applies only to the selected ranges and is not a probability forecast.

# V — My Questions as the Tesla Reviewer

## Review Area 1 — Selection and Evidence

### Question 1 — Tesla's automotive revenue declined 10% while energy revenue grew 27%. Why did you assume 15% total revenue growth for 2026?

**Partner response:** The forecast assumes a return to growth through improved automotive performance and continued expansion in businesses such as energy. It is a forecast rather than a continuation of FY2025's decline, but it is an important assumption that future evidence must support.

### Question 2 — Which evidence changed your view of Tesla the most?

**Partner response:** The contrast between automotive and energy changed the analysis. Automotive remained the largest business but declined, while energy grew 27% and produced a 29.8% gross margin. This made energy more important to the valuation story.

## Review Area 2 — Model and Valuation

### Question 3 — Why are the modeled values of roughly $28–$39 so far below the $356.09 saved market price?

**Partner response:** The conventional methods mainly capture supportable current earnings and forecast cash flows. The market may include expectations for additional value from AI, autonomy, robotics, energy, or stronger growth that the conventional model does not fully capture.

### Question 4 — Why does peer P/E differ from the DCF and FCFE results?

**Partner response:** Peer P/E uses GM's earnings multiple, while DCF and FCFE value Tesla's forecast cash flows. GM is imperfect because Tesla has expected opportunities outside traditional automotive manufacturing. The methods answer different valuation questions.

## Review Area 3 — Sensitivity and Interpretation

### Question 5 — Does the sensitivity analysis prove that R&D is more important than Revenue Growth?

**Partner response:** No. R&D produced the larger value-per-share effect only over the ranges tested. Revenue Growth changed by ±3 percentage points and R&D / Revenue by ±1 percentage point. Different ranges could change the ranking.

### Question 6 — What evidence would be most likely to change your Tesla conclusion?

**Partner response:** Evidence that investments in AI, autonomy, robotics, energy, or other technology are producing meaningful revenue, stronger margins, operating cash flow, and FCFE would make the higher market valuation easier to explain.

# Tesla Evidence / Calculation Check

I checked the R&D sensitivity against the $31.14 base value:

- Lower case: ($26.44 ÷ $31.14) − 1 ≈ **-15.1%**
- Higher case: ($35.84 ÷ $31.14) − 1 ≈ **+15.1%**

The calculation supports the partner's numerical claim that changing R&D / Revenue by ±1 percentage point produced approximately a -15.1% to +15.1% change in modeled value per share. I checked the supplied calculation, not an external Tesla source.

# E — Explain Back the Tesla Analysis

## Tesla Valuation Conclusion

My understanding is that Tesla's conventional valuation methods produced values far below the saved $356.09 market price. This does not mean the stock must fall to those modeled values. It means the assumptions in the conventional models did not capture enough future economic value to explain the market price. A higher supported value would require stronger economic performance or additional value from energy, AI, autonomy, robotics, or other opportunities.

## Tesla Main Driver

R&D / Revenue had the largest value-per-share effect over the tested Lab 11 ranges. Changing it by ±1 percentage point moved value from $26.44 to $35.84 around the $31.14 base. That ranking is range-dependent and does not mean R&D is always the most important or uncertain variable.

## Tesla Biggest Limitation

The largest limitation is uncertainty about Tesla's future growth and the value of investments outside traditional automotive manufacturing. Potential value from AI, autonomy, and robotics cannot be captured responsibly until it can be translated into supported revenue, margin, and cash-flow assumptions.

## Tesla Strength

One strength is the clear connection between a company-specific assumption and valuation. The analysis traces R&D through operating expense, operating income, FCFE, and value per share while acknowledging that successful R&D may create long-term value.

## Tesla Improvement

One specific improvement is to strengthen the evidence supporting 15% revenue growth in 2026. Because FY2025 total revenue declined and automotive revenue fell 10%, the forecast needs more support from deliveries, energy growth, new products, or other measurable revenue sources.

# Response to Feedback on My Walmart Analysis

## What I Will Keep

- The linked pro-forma structure and accounting checks
- Historical Walmart evidence as the basis for forecast assumptions
- Revenue Growth and SG&A % of Revenue as sensitivity drivers
- Multiple valuation methods reported separately rather than averaged

## What I Will Revise

- Explain why each sensitivity range was selected and state more clearly that different ranges could change the ranking.
- Make the business-model and fiscal-period differences between Target and Costco more explicit.
- Distinguish clearly among the August peer comparison, September FCFF DCF, and later FCFE model so their different dates and share bases are not mixed.

## What I Will Investigate

- Long-term Walmart revenue-growth expectations
- SG&A and operating-margin trends
- E-commerce profitability and advertising economics
- Membership and Sam's Club growth
- Returns from automation, fulfillment, and other capital spending
- Whether Target and Costco remain the best peers

## Did the Review Change My Walmart Conclusion?

The review did not materially change my **Watch-Defer** conclusion. It changed my research priority. The first priority is now evidence about whether Walmart can sustain operating leverage and its modeled cash SG&A ratio, because SG&A produced the largest valuation span over the tested ranges. I would also improve the support for the ranges and peer selection. I am not claiming that the model was repaired or newly rerun for this review.

# Reflection

The question that made me reconsider my work most was which assumption had the greatest effect on Walmart's valuation. It showed me the difference between saying a driver had the largest effect over my tested ranges and saying it is objectively the most important or uncertain driver.

Sensitivity analysis measures how a model responds to an assumption change; it does not measure the probability of that change. The peer review also reinforced why methods can disagree. Walmart's Target and Costco multiples produced a wide range, while Tesla's market price was dramatically different from its conventional values. In both cases, the important task is to explain the disagreement and limitations rather than force the methods into an average.

## Existing Analysis and Output

- Company history and assumptions: [Walmart_History_and_Assumptions.md](Walmart_History_and_Assumptions.md)
- FY2026 filing and operating evidence: [Walmart_FY2026_MDA.md](Walmart_FY2026_MDA.md)
- Initial company research decision: [Walmart_Project_1_Edition_B.md](Walmart_Project_1_Edition_B.md)
- Three-statement pro forma and FCFE valuation: [Walmart_Lab_10_Proforma.md](Walmart_Lab_10_Proforma.md)
- FCFF DCF, enterprise-to-equity bridge, and reverse DCF: [Walmart_Lab_06_DCF_Valuation.md](Walmart_Lab_06_DCF_Valuation.md)
- Peer P/E valuation and peer-removal check: [lab08_notes.md](lab08_notes.md)
- Lab 11 sensitivity analysis: [Walmart_Lab_11_V_and_E.md](Walmart_Lab_11_V_and_E.md)

No Tesla files were available in this repository, so no partner repository links are listed.
