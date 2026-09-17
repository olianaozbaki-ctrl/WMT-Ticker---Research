# Lab 08 — Deal Evidence and Valuation Triangulation

## Company and Valuation Date

Company: Walmart Inc. (WMT)
Valuation Date: August 5, 2026

## Peer Policy

A reasonable peer for Walmart should have a similar large-scale retail business model, with significant sales from consumer goods through physical stores and e-commerce. I would qualify a peer if it has similar retail economics but meaningful differences in product mix, membership revenue, geographic exposure, or scale. I would exclude a company if its primary business model or sources of earnings are too different from Walmart for its P/E multiple to provide a meaningful comparison.

## Candidate Rejection Evidence

I would reject a candidate if its main source of earnings came from a business model that is substantially different from Walmart’s consumer retail operations, or if differences in product mix, membership structure, geographic exposure, or retail format made its P/E multiple not meaningfully comparable. I would also reject or leave a candidate unresolved if I could not verify annual reported diluted EPS that was public by August 5, 2026.

## Candidate Decisions

### Target Corporation (TGT) — Use

Target is a reasonable peer because it operates a large-scale retail business selling consumer products through physical stores and digital channels, which is similar to Walmart’s omnichannel retail model. Target is smaller, primarily U.S.-focused, and has a greater emphasis on discretionary merchandise, but these differences do not make the comparison unusable.

Primary source: [Target FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741926000016/tgt-20260131.htm)
Business-model locator: Item 1, Business — Our Strategy / Merchandise Categories
Latest annual reported diluted EPS: $8.13
Fiscal period: Fiscal year ended January 31, 2026
Publication date: March 11, 2026
EPS locator: Management’s Discussion and Analysis — Executive Overview & Financial Summary, page 28

### Costco Wholesale Corporation (COST) — Qualify

Costco is a reasonable but qualified peer because it is also a large-scale retailer selling consumer goods through physical locations and e-commerce. However, Costco’s paid membership warehouse model and limited, bulk-oriented merchandise assortment differ meaningfully from Walmart’s broader open-access supercenter and retail model.

Primary source: [Costco FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm)
Business-model locator: Item 1, Business — General / Warehouse Operations
Latest annual reported diluted EPS: $18.21
Fiscal period: 52 weeks ended August 31, 2025
Publication date: October 8, 2025
EPS locator: Consolidated Statements of Income, page 37

## P/E Inputs and Sources

| Company | Decision | Share Price | Price Date | Annual Reported Diluted EPS | Fiscal Year-End | Publication Date | Primary Source / Locator |
|---|---|---:|---|---:|---|---|---|
| Walmart Inc. (WMT) | Target | $112.34 | August 5, 2026 | $2.73 | January 31, 2026 | March 13, 2026 | EPS: [Walmart FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), Item 8, Note 2 — Net Income Per Common Share, page 63.<br>Price: [Walmart historical prices](https://stockanalysis.com/stocks/wmt/history/), August 5, 2026 → Close. |
| Target Corporation (TGT) | Use | $147.70 | August 5, 2026 | $8.13 | January 31, 2026 | March 11, 2026 | EPS: [Target FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741926000016/tgt-20260131.htm), Consolidated Statements of Operations.<br>Price: [Target historical prices](https://stockanalysis.com/stocks/tgt/history/), August 5, 2026 → Close. |
| Costco Wholesale Corporation (COST) | Qualify | $941.99 | August 5, 2026 | $18.21 | August 31, 2025 | October 8, 2025 | EPS: [Costco FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm), Consolidated Statements of Income.<br>Price: [Costco historical prices](https://finance.yahoo.com/quote/COST/history/), August 5, 2026 → Close. |

## Validation

### Manual P/E Check

Using Target as the manual check:

Target P/E = Share Price / Annual Reported Diluted EPS

Target P/E = $147.70 / $8.13 = 18.167282x

This matches the P/E calculated by lab08_peer_pe_valuation.py.

### Peer-Removal Check

Prediction: Removing Costco should lower Walmart's implied valuation because Costco has the higher P/E multiple.

Full-peer median-implied price: $95.41

Removing Costco leaves only Target and lowers the median-implied price to $49.60, a decrease of $45.81. This occurs because Costco's P/E of 51.729270x is substantially higher than Target's P/E of 18.167282x. With only Target remaining, $49.60 becomes a one-peer reference estimate rather than a valuation range.

## DCF Comparison

| Method | Walmart Result and Date | Main Assumption or Limitation |
|---|---|---|
| Week 3 DCF | $15.09–$55.33 per share, base case $31.76, August 5, 2026 | Depends heavily on forecast assumptions, WACC, and terminal growth. |
| Peer P/E | $49.60–$141.22 per share, median-implied price $95.41, August 5, 2026 | Depends on peer selection and the use of annual reported diluted EPS. |

The peer P/E median-implied price of $95.41 is substantially higher than the DCF base case of $31.76, although the two valuation ranges overlap between approximately $49.60 and $55.33. The methods differ because the DCF is based on Walmart's projected cash flows and discount-rate assumptions, while the peer P/E method reflects the market multiples assigned to Target and Costco.

## AI Criticism

### Criticism 1 — Range Interpretation
Decision: Accept

The criticism is valid because the lower end of the peer P/E range, $49.60, overlaps with the upper end of the DCF range, $55.33. Therefore, it is more precise to say that the peer P/E median-implied price of $95.41 is substantially higher than the DCF base case of $31.76, rather than saying that the entire P/E valuation is higher.

### Criticism 2 — Earnings Timing
Decision: Accept

The peer comparison consistently uses reported diluted EPS, but the fiscal periods are not identical. Walmart and Target use fiscal years ending January 31, 2026, while Costco uses the fiscal year ended August 31, 2025. I will keep this as a limitation because the earnings periods are not perfectly aligned.

### Criticism 3 — DCF Date / Reproducibility
Decision: Reject

My Week 3 Walmart DCF was explicitly valued as of August 5, 2026, with a low/base/high range of approximately $15.09 / $31.76 / $55.33 per share. Therefore, I will continue using the August 5 Week 3 DCF for this comparison rather than switching to an unsupported later DCF result.

## Final Call

### Peer Choices

I used Target as a peer because its large-scale omnichannel retail model is reasonably similar to Walmart's. I qualified Costco because it is also a large consumer retailer, but its membership-warehouse model, limited assortment, and different fiscal period make it a less direct comparison.

### What the P/E Comparison Adds

The peer P/E analysis provides a market-based comparison that complements the DCF. The DCF focuses on Walmart's projected cash flows and discount-rate assumptions, while the P/E analysis shows the valuation implied by the earnings multiples of Target and Costco.

### Why the Results Differ

The DCF base case of $31.76 is much lower than the peer P/E median-implied price of $95.41. The DCF is highly dependent on Walmart's projected cash flows, WACC, and terminal growth, while the peer P/E result is highly dependent on which peers are included and their reported earnings. The large change when Costco is removed shows that the peer result is especially sensitive to peer selection.

### Conditional Call

Watch-Defer.

Walmart's August 5, 2026 market price of $112.34 is above the DCF range of $15.09–$55.33 and above the peer P/E median-implied price of $95.41, although it remains within the broad peer P/E range of $49.60–$141.22.

I would not average the DCF and P/E methods or claim one combined fair-value range. I can defend the two method-specific ranges, but I would withhold a single overall valuation range because the methods rely on different assumptions and the peer result is very sensitive to peer selection.

### What Could Change My Decision

I would reconsider my Watch-Defer call if I found peers with closer business and fiscal-period comparability, if updated reported earnings materially changed the peer P/E range, or if reviewing the Week 3 DCF assumptions produced a materially different supported valuation.

### Response to the Skeptical Question

For this comparison, I am using the saved Week 3 DCF because it is explicitly dated August 5, 2026 and matches the comparison date used for the peer analysis. If I could not reproduce or support the underlying DCF assumptions from my saved Week 3 work, I would treat the DCF conclusion as lower-confidence rather than replace it with an unsupported later valuation.
