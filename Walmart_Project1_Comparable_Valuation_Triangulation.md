# Walmart Project 1 — Comparable Valuation and Triangulation (V3)

**Status:** Illustrative decision support only; not a final valuation or investment recommendation. No existing V2/V3 model or validation record was changed. Monetary amounts are USD millions except per-share values and multiples.

## Peer selection and method

The peer set retains Target (TGT) and Costco (COST), the same two comparators used by the existing `lab08_peer_pe_valuation.py`. Both are large U.S. omnichannel retailers with physical stores, digital sales, merchandise economics, and material consumer exposure. Target is the closer broadline/general-merchandise analogue. Costco is a qualified warehouse-membership retailer: its membership model, lower merchandise margins, scale, and valuation premium make it useful as an upper-bound reference, not a close operating match. The two companies do not constitute a statistically meaningful peer group; results are shown peer-by-peer, not treated as a robust median estimate.

The existing Lab 08 file is an August 5, 2026 historical P/E exercise (WMT $112.34, TGT $147.70, COST $941.99; annual diluted EPS $2.73, $8.13, and $18.21). Its historical outputs are preserved but not reused as the valuation-date multiples because the price date and earnings period differ from the September 23 / latest-TTM analysis below.

Kroger was not added. A grocery-led retailer would add relevant food retail exposure, but the existing project peer file does not contain it and a new peer requires consistent same-date price, shares, filing-period operating results, debt, cash, lease, and share-count treatment. No unsupported KR multiple is imputed.

The primary valuation multiple is **market EV / GAAP operating income (EBIT)**. For both peers, EV is calculated as same-date close × latest available reported shares + reported interest-bearing borrowing carrying amount − cash and cash equivalents − separately reported short-term investments. Lease liabilities are excluded from both peer EV numerators; lease-adjusted multiples are unavailable on a consistent basis. The corresponding P/E is same-date close / TTM GAAP diluted EPS, calculated by adding current interim EPS to the prior fiscal-year EPS and subtracting the comparable prior interim EPS. These are trailing—not forecast—multiples.

## Observations, dates, and source lineage

| Input | Walmart | Target | Costco |
|---|---|---|---|
| Sep. 23, 2026 close | $110.53 | $156.26 | $904.70 |
| Price source | [StockAnalysis WMT history](https://stockanalysis.com/stocks/wmt/history/) | [StockAnalysis TGT history](https://stockanalysis.com/stocks/tgt/history/) | [StockAnalysis COST history](https://stockanalysis.com/stocks/cost/history/) |
| Latest reported spot shares used | 7,933.746241m, Aug. 26, 2026 | 454.296736m, Aug. 21, 2026 | 443.478804m, May 27, 2026 |
| Latest filing balance date | July 31, 2026 | Aug. 1, 2026 | May 10, 2026 |
| GAAP TTM operating income | $32,280m | $6,024m | $11,225m |
| TTM diluted EPS estimate | $2.76 | $9.64 | $19.88 |

Primary filing sources:

- Walmart [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm), fiscal year ended January 31, 2026, and [FY2027 Q2 Form 10-Q](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm), period ended July 31, 2026 and filed August 28, 2026. Consolidated income statements report FY2026 operating income of $29,825m, H1 FY2027 $16,876m, H1 FY2026 $14,421m; diluted EPS is $2.73, $1.46, and $1.43, respectively. Thus TTM operating income = 29,825 + 16,876 − 14,421 = **$32,280m** and approximate TTM diluted EPS = 2.73 + 1.46 − 1.43 = **$2.76**.
- Target [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/27419/000002741926000016/tgt-20260131.htm), fiscal year ended January 31, 2026, filed March 11, 2026; [Q2 FY2027 Form 10-Q](https://www.sec.gov/Archives/edgar/data/27419/000002741926000042/tgt-20260801.htm), period ended August 1, 2026 and filed August 28, 2026. The 10-Q cover reports 454,296,736 shares outstanding August 21. Target's TTM ROIC table reports GAAP operating income of $6,024m. The interim statement reports six-month diluted EPS $5.83 versus $4.32; the FY2026 10-K reports diluted EPS $8.13. Approximate TTM EPS = 8.13 + 5.83 − 4.32 = **$9.64**. Target's H1 FY2027 operating income includes a reported $994m tariff-refund benefit; no normalization is made.
- Costco [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm), fiscal year ended August 31, 2025, and [Q3 FY2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/909832/000090983226000051/cost-20260510.htm), period ended May 10, 2026 and filed June 3, 2026. The 10-Q cover reports 443,478,804 shares outstanding May 27. It reports 36-week operating income $7,884m versus $7,042m in the comparable 2025 period and diluted EPS $14.01 versus $12.34; the FY2025 10-K reports operating income $10,383m and diluted EPS $18.21. Therefore TTM operating income = 10,383 + 7,884 − 7,042 = **$11,225m**, and approximate TTM diluted EPS = 18.21 + 14.01 − 12.34 = **$19.88**. The Costco FY2026 10-K was filed after September 23 and is intentionally not used to avoid look-ahead.

Peer balance-sheet / debt inputs (filing units are $ millions):

- Target 10-Q balance sheet and debt/ROIC schedules: cash and cash equivalents $5,411 (including $4,337 short-term investments classified in cash equivalents); current and noncurrent borrowings $1,136 + $14,221 = $15,357. No separate investment subtraction is made, avoiding double counting the $4,337. Values are August 1, not September 23.
- Costco 10-Q: cash $18,946; short-term investments $1,050; long-term debt excluding current portion $5,670; short-term bank borrowing $96 (identified in the liquidity note as included in other current liabilities). Debt used is $5,766. Values are May 10, not September 23.
- Walmart V3 bridge is retained for EV-multiple conversion: cash $11,529, debt fair-value proxy $47,746, finance leases $6,832, nonoperating investments $0, NCI $0, and 7,933.746241m August 26 **basic** shares. These are July 31 / August 26 inputs rather than September 23 balances or diluted shares. They remain provisional as described in [Final Valuation Assumptions](Walmart_Project1_Final_Valuation_Assumptions.md).

The peer price dates are aligned to September 23; shares and balance-sheet values are the latest located pre-date filings, not same-day observations. The multiples are therefore valuation-date price snapshots built on lagged denominators and capital balances, not perfectly contemporaneous market EVs.

## Multiple calculations and implied Walmart values

Arithmetic in `walmart_project1_comparables_v3.py` uses share counts in millions and prices in USD/share. The market-cap and EV formulas are shown explicitly:

| Peer | Market cap | EV formula | EV | TTM EBIT | EV/EBIT | TTM diluted EPS | P/E |
|---|---:|---|---:|---:|---:|---:|---:|
| Target | $70,988.408 | 70,988.408 + 15,357 − 5,411 | $80,934.408 | $6,024 | **13.4353x** | $9.64 | **16.2095x** |
| Costco | $401,215.274 | 401,215.274 + 5,766 − 18,946 − 1,050 | $386,985.274 | $11,225 | **34.4753x** | $19.88 | **45.5080x** |

Applying EV/EBIT to Walmart TTM EBIT of $32,280m gives implied enterprise values of approximately $433,692m (Target multiple) and $1,112,863m (Costco multiple). Converting with the V3 bridge yields:

| Multiple reference | Walmart EV/EBIT implied value/share, V3 bridge | P/E implied value/share |
|---|---:|---:|
| Target | **$49.24** | **$44.74** |
| Costco | **$134.84** | **$125.60** |
| Two-peer observed range | **$49.24–$134.84** | **$44.74–$125.60** |
| Mechanical midpoint of two peer indications | $92.04 | $85.17 |

For EV/EBIT, Walmart equity value is calculated as implied EV + $11,529 cash − $47,746 debt proxy − $6,832 finance leases − $0 NCI + $0 investments; divided by 7,933.746241m August 26 basic shares. This preserves the V3 provisional bridge but is not perfectly lease-consistent with peer EV, which excludes leases. Omitting the separate Walmart finance-lease claim would increase the EV/EBIT indications by **$0.86/share** to approximately **$50.10–$135.70**. Neither conversion is selected as final. The P/E method is price-to-EPS and does not use this EV bridge.

The “midpoint” is only the arithmetic mean of two peer-implied values, not a statistically robust median. It should not be treated as a central estimate given the large differences in the businesses and multiples.

## Accounting, dating, and comparability limitations

1. **Peer choice / range width.** Target is the closer general-merchandise retailer but differs in scale and category mix. Costco's membership economics and very high multiple create a large upper endpoint. With two peers, there is no defensible outlier policy or robust distribution. No single peer multiple is selected.
2. **Period alignment.** Walmart and Target TTM metrics end July 31/August 1, 2026; Costco's end May 10, 2026. Costco is about 4.5 months before the valuation date. All are built from the latest reported annual period plus the latest interim period less the prior-year comparable interim period.
3. **TTM EPS construction.** TTM diluted EPS is the sum/subtraction of reported, rounded period EPS, not TTM net income divided by a single recomputed TTM diluted weighted-average share count. It is an approximation, affected by rounding, repurchases, and changing diluted-share denominators. TGT and Costco spot market caps use latest point-in-time shares, not diluted weighted-average shares; this is conventional for market capitalization but dates differ from the close.
4. **EBIT definition.** EV/EBIT uses reported GAAP operating income for all companies, excluding interest and other nonoperating income. Target's own ROIC table labels $6,088m as EBIT because it adds $64m net other income to $6,024m operating income; this analysis deliberately uses the comparable GAAP operating-income figure, not Target's broader ROIC numerator. Target's $994m tariff refund benefit remains in reported operating income and EPS; adjusted figures are not substituted.
5. **Leases.** EV numerators use reported interest-bearing borrowing carrying amounts and exclude operating and finance lease liabilities for every company because a complete, consistently defined lease-value series was not obtained. Reported EBIT is not lease-adjusted. Walmart V3 separately deducts its finance-lease claim from equity value and has finance-lease additions in FCFF; the mismatch with the peer EV convention creates the $0.86/share bridge sensitivity above and may also affect operating-income comparability. No lease-adjusted multiple is presented as verified.
6. **Debt and cash measures.** Walmart V3 uses a mixed carrying/fair-value debt proxy and July 31 balances, while peer EV uses carrying values from different dates. Costco short-term investments are deducted separately; Walmart and Target do not have a separately established comparable investment adjustment in this calculation. Any unrecognized cash restrictions, NCI ownership, or nonoperating assets can affect bridge comparability.
7. **Nonmeaningful inputs.** Both peers have positive TTM GAAP operating income and diluted EPS, so the calculated EV/EBIT and P/E are mathematically meaningful. They are not thereby economically comparable. A normalized EV/EBIT or lease-adjusted EV/EBITDA is **not available** from the validated input set; no EBITDA multiple is forced. A multiple would be nonmeaningful for a negative/near-zero denominator, but that condition does not apply to these two reported TTM denominators.

## Triangulation with V3 DCF and reverse DCF

| Method | Indication | What it says / key caveat |
|---|---:|---|
| V3 DCF, 7.00% WACC / 2.50% terminal growth | **$36.78/share** | Current diagnostic V3 base; 82.03% of EV is terminal value. Uses pre-date cash/debt/lease balances and August 26 basic shares. |
| V3 DCF, 7.6748% illustrative WACC / 2.50% terminal growth | **$31.19/share** | The evidence-file rate illustration, not a verified final WACC. Shows material rate sensitivity. |
| Reverse DCF at Sep. 23 close | **$110.53/share reproduced** | Requires either 15.48%–14.68% annual growth in both revenue streams (about 15.14% five-year revenue CAGR) or V3 cash-opex ratios lowered by 17.19 points to about 58.01%–57.31%. The solve is non-unique and both outcomes are aggressive relative to V3. |
| Target EV/EBIT / P/E | **$49.24 / $44.74** | Closest selected peer, but Target TTM operating income includes tariff-refund benefit; lease and date limitations remain. |
| Costco EV/EBIT / P/E | **$134.84 / $125.60** | Premium reference; business mix and multiple are materially different from Walmart. Not a base-case anchor. |

The DCF and Target indications cluster well below the observed market price; Costco is the exception and the reverse DCF shows the operating expectations needed to reach the price under V3's framework. This difference is not a mathematical contradiction: DCF discounts Walmart-specific projected FCFF, EV/EBIT transfers a peer operating multiple, P/E transfers an equity multiple, and reverse DCF solves model assumptions to match price. Their accounting perimeters, growth prospects, lease treatment, and risk assumptions differ.

### Conditional working reference band and triggers

As a **conditional screening band only**, the V3 base/rate illustration ($31.19–$36.78) and Target peer indications ($44.74–$49.24) support a broad **$31–$49 per-share reference zone** if: (a) V3 operating drivers remain directionally appropriate; (b) the 7.00%–7.6748% WACC cases remain useful sensitivities; (c) the V3 July/August bridge inputs are retained provisionally; and (d) Target is the primary selected peer while Costco is treated as an upper-bound context. This is not a statistically derived fair-value interval and does not resolve V3's provisional inputs. The $125–$135 Costco indications and $110.53 market price are disclosed outside that conditional core zone rather than averaged into it.

Potential review triggers—not buy/sell instructions:

- Reopen the DCF range when a source-backed WACC, September 23 share count, and September 23 cash/debt/lease/NCI bridge are established; these can move value independently of operations.
- Revisit the reverse-DCF gap if subsequent reported results support or falsify sustained net-sales/membership growth near 15% or an operating margin near 8.9%, after separating temporary items such as tariff refunds.
- Reconsider Costco as a more influential peer only if Walmart demonstrates durable membership, digital, and margin economics that make its business mix more comparable; otherwise retain it as a premium reference.
- Before any recommendation, set an explicit margin-of-safety rule and require source-verified value to exceed the contemplated purchase price by that rule. No margin-of-safety threshold was provided, so none is fabricated here.

## Arithmetic and run checks

The script independently reconstructs market capitalization, EV, EV/EBIT, P/E, each implied price, and the V3 imported DCF result. It flags nonpositive denominators, inconsistent market-price dates, fewer than two usable peers, or failing V3 controls. Run:

```text
python3 walmart_project1_comparables_v3.py
```

Run result: peer market-cap/EV/multiple arithmetic **PASS**; both EV/EBIT and P/E denominators positive; Sep. 23 price-date check **PASS**; imported V3 statement and DCF controls **PASS**. These checks validate calculation mechanics only, not completeness or comparability of source data.
