# Walmart Project 1 — WACC Evidence Review

## Scope and valuation date

This review is limited to `Walmart_Lab_06_DCF_Valuation.md` and
`walmart_project1_wacc.py`. It does not treat repetition of the same assumption
across those two files as independent support.

- **Proposed final Project 1 valuation date:** September 23, 2026.
- **Original Edition A date:** September 1, 2026.
- **Historical Lab 06 valuation date:** September 10, 2026, using the September
  9, 2026 market close.
- **Financial-statement date:** Fiscal year ended January 31, 2026; the lab says
  Walmart's FY2026 Form 10-K was filed March 13, 2026.
- **Evidence status:** The Python file expressly says all WACC inputs are
  preliminary assumptions and not verified market facts. Except for limited
  filing-based support for the tax-rate approximation, the reviewed files do
  not contain independent evidence for the assumptions.

### Valuation-date reconciliation

September 23, 2026 is the proposed final Project 1 evidence date. September 1,
2026 is retained as the original Edition A date, and September 10, 2026 remains
the historical Lab 06 date rather than the final Project 1 date. This date
reconciliation documents the versions only; it does not revise any Python model
input or retroactively change the dates used in the original lab.

## WACC components and evidence status

| Component | Current assumed value | Existing source in the reviewed files | Documented as-of date | Does available evidence independently support it? |
|---|---:|---|---|---|
| Risk-free rate | 4.10% | The lab describes it as the 10-year Treasury rate; the Python file repeats the assumption. No Treasury observation, series, URL, quotation date, or retrieval date is supplied. | The WACC row says Sep. 2026, but no exact observation date is documented. | **UNVERIFIED — No.** Repetition in the Python file is not independent evidence. |
| Equity beta | 0.55 | The lab and Python file state the value. No data provider, beta methodology, estimation window, frequency, index, or observation date is supplied. | Not documented beyond the WACC row's general Sep. 2026 date. | **UNVERIFIED — No.** |
| Equity risk premium | 5.00% | The lab and Python file state the value. No published ERP source, methodology, geography, or publication date is supplied. | Not documented beyond the WACC row's general Sep. 2026 date. | **UNVERIFIED — No.** |
| Cost of equity (CAPM output) | 6.85% | Derived from 4.10% + 0.55 × 5.00%. | Same dates and limitations as its inputs. | **UNVERIFIED — No.** The arithmetic is reproducible, but all three economic inputs are not independently supported. |
| Pretax cost of debt | 4.50% | The lab calls it an approximate pretax debt rate; the Python file repeats the assumption. No bond yield, credit spread, interest-expense calculation, debt schedule calculation, or market quotation is supplied. | Not documented beyond the WACC row's general Sep. 2026 date. | **UNVERIFIED — No.** |
| Tax rate | 24.50% | The Python file assumes 24.5%. The lab separately reports a 24.43% effective tax rate and attributes it to Walmart's FY2026 Form 10-K when calculating after-tax interest. | FY ended Jan. 31, 2026. | **Limited support only.** The assumed 24.50% is a reasonable rounding of the lab's filing-attributed 24.43%, but the filing evidence was not reproduced in the reviewed files and no decision is documented that the historical effective rate is the appropriate marginal tax rate for WACC. Treat the WACC tax-rate choice as **UNVERIFIED**. |
| After-tax cost of debt | 3.3975% (about 3.40%) | Derived as 4.50% × (1 − 24.50%). | Same dates and limitations as pretax cost of debt and tax rate. | **UNVERIFIED — No.** The arithmetic is reproducible, but the pretax debt cost is unsupported and the tax-rate choice is not fully verified. |
| Market-value equity weight | 95.00% | The lab and Python file state the value. The lab gives a share price and diluted share count elsewhere, but it does not show a market-capitalization calculation used to derive this weight. | General WACC date Sep. 2026; underlying market-value measurement date is not documented. | **UNVERIFIED — No.** |
| Market-value debt weight | 5.00% | The lab and Python file state the value. The lab gives $44,762 million of balance-sheet debt as of Jan. 31, 2026, but it does not establish debt market value or reconcile that amount to the 5% weight. | General WACC date Sep. 2026; cited balance-sheet debt is as of Jan. 31, 2026. | **UNVERIFIED — No.** |
| Weight-sum check | 100.00% | 95.00% + 5.00%; enforced by an assertion in the Python file. | Not applicable. | **Yes, arithmetically only.** This does not validate either market-value weight. |
| Calculated WACC | 6.677375%, displayed as 6.6774% | Derived in the Python file from the assumptions above. | Same dates and limitations as the component inputs. | **UNVERIFIED as a market estimate.** The calculation is internally correct, but its inputs are not independently verified. |
| Provisional model WACC | 7.00% | The lab says the estimated range is about 6.7%–7.0% and models 7.00%; the Python constant is `PROVISIONAL_FCFF_WACC = 0.07`. | Sep. 2026 in the lab. | **UNVERIFIED — No.** It is a provisional modeling choice, not the direct output of the stated inputs. |

## Reconciliation of 6.6774% and 7.00%

The stated inputs produce:

\[
r_e = 4.10\% + 0.55(5.00\%) = 6.85\%
\]

\[
r_d(1-T) = 4.50\%(1-24.50\%) = 3.3975\%
\]

\[
WACC = 95.00\%(6.85\%) + 5.00\%(3.3975\%) = 6.677375\% \approx 6.6774\%
\]

The 7.00% model rate is therefore **0.322625 percentage points, or 32.2625 basis
points, above** the calculated rate. It is not ordinary rounding of 6.6774% to
two decimal places; that would be 6.68%. The lab presents 7.00% as the selected
rate within an approximate 6.7%–7.0% range, so the difference should be treated
as a provisional 32.26-basis-point modeling cushion or judgmental overlay.
Neither reviewed file documents a separate empirical source or explicit risk
adjustment that substantiates that overlay. Accordingly, both the calculated
market WACC and the 7.00% selected rate remain **UNVERIFIED** pending the evidence
listed below.

## Evidence still required

1. **Risk-free rate:** A dated observation from an authoritative Treasury or
   Federal Reserve source for the chosen maturity, preferably the 10-year U.S.
   Treasury yield on September 23, 2026 for the proposed final Project 1 date.
   The source, series, observation date, and convention must be recorded.
2. **Beta:** A dated beta from a named market-data source, or a reproducible beta
   calculation. A calculation must document the return frequency, lookback
   period, benchmark index, price-adjustment convention, regression result, and
   whether the beta is raw, adjusted, levered, or relevered.
3. **Equity risk premium:** A dated, published U.S. equity risk premium estimate
   from an identified source. The file must state whether it is historical or
   implied, which risk-free maturity it is paired with, and why that convention
   matches the CAPM calculation.
4. **Cost of debt:** Market yields as of the valuation date for Walmart's
   material outstanding debt, with issue weights and maturity details, or a
   documented synthetic-rating/credit-spread method. If an accounting proxy is
   used instead, reconcile interest expense to average interest-bearing debt and
   explain why that backward-looking rate is appropriate. Also document the tax
   rate used for the interest tax shield and why it is a marginal rate suitable
   for WACC.
5. **Market-value capital weights:** A valuation-date equity market value based
   on the appropriate shares outstanding and closing share price, plus the
   market value of interest-bearing debt (or a supported book-value proxy).
   Identify included and excluded claims—such as leases, short-term borrowings,
   preferred stock, and noncontrolling interests—and show the normalized
   calculations \(E/(D+E)\) and \(D/(D+E)\).

Until those items are obtained and retained, the component assumptions and both
WACC figures should not be represented as independently verified market facts.

## Equity Beta Verification

**Conclusion: UNVERIFIED as of the proposed September 23, 2026 Project 1
valuation date. Retain 0.55 as a provisional assumption.** The original
publications below were reviewed to confirm that they report the listed values
and dates. That confirms the transcription, not the underlying estimates: none
provides an exact September 23, 2026 beta with a complete, reproducible
methodology.

### Dated evidence

| Provider and source | Reported beta | Observation/report date | Measurement window | Benchmark index | Assessment |
|---|---:|---|---|---|---|
| [Trefis — Walmart (WMT) Price Behavior](https://www.trefis.com/data/companies/wmt) | **0.39** | **August 31, 2026** | **3 years** | SPY, the SPDR S&P 500 ETF Trust, appears as the equity benchmark in the surrounding price-behavior analysis, but the publication does not explicitly state that SPY is the benchmark for the ordinary beta. | Value and date confirmed as reported in the original publication and available before September 23. The estimate remains **UNVERIFIED** for the proposed valuation date. The page also reports a one-year beta of −0.07. |
| [The Henry Fund — Walmart report](https://henryfund.tippie.uiowa.edu/sites/henryfund.tippie.uiowa.edu/files/2026-04/WMT-S26.pdf) | **0.66** | **April 22, 2026** | Not disclosed | Not disclosed | Value and date confirmed as reported in the original publication and available before September 23. The estimate remains **UNVERIFIED** because the window, benchmark, and calculation method are not disclosed. |
| [The Henry Fund — earlier Walmart report](https://henryfund.tippie.uiowa.edu/sites/henryfund.tippie.uiowa.edu/files/2025-09/f24_WMT.pdf) | **0.57** | **October 1, 2024** | Described as the average of semiannual beta over a three-year range | Not disclosed | Value, date, and window description confirmed as reported in the original publication. The estimate remains **UNVERIFIED** for September 23, 2026 because it is older and lacks the benchmark and return-calculation details. |

### Comparison with the preliminary 0.55

- The provisional **0.55** is **0.16 above** Trefis's August 31, 2026
  three-year beta of 0.39, or approximately **41.0% higher** relative to 0.39.
- It is **0.11 below** the Henry Fund's April 22, 2026 figure of 0.66, or
  approximately **16.7% lower** relative to 0.66.
- It is **0.02 below** the older Henry Fund estimate of 0.57, or approximately
  **3.5% lower** relative to 0.57.

The dispersion from 0.39 to 0.66 demonstrates that beta depends materially on
the provider's window, return frequency, benchmark, and adjustment method. It
does not support silently replacing 0.55 with any one observed figure.

### Limitations and verification status

- The Trefis observation is dated 23 calendar days before the proposed final
  valuation date, not on September 23, 2026. The live page can update, although
  its beta table preserves an August 31, 2026 as-of label.
- Trefis identifies SPY in the surrounding price-behavior analysis and labels
  the beta windows, but it does not fully state the ordinary-beta formula,
  adjusted-price convention, minimum observations, or whether the reported
  ordinary beta is raw or adjusted. Its footnote expressly refers to daily
  benchmark returns for *upside and downside* betas; it does not expressly state
  the return frequency for the ordinary beta.
- The April 2026 Henry Fund report provides neither the measurement window nor
  the benchmark for its 0.66 figure. The October 2024 report supplies a
  three-year/semiannual description for 0.57 but omits the benchmark, data
  provider, price-adjustment convention, regression details, and raw-versus-
  adjusted status.
- Beta is not a company-reported accounting fact, and the reviewed provider
  estimates are not equivalent measurements. Checking the publications confirms
  what they report but does not independently validate their calculations. None
  independently verifies **0.55 specifically on September 23, 2026**.

Accordingly, **0.55 remains UNVERIFIED and provisional**. Final verification
requires a saved, dated provider output for September 23, 2026 or a reproducible
regression ending on that date that specifies adjusted WMT returns, the
benchmark series (for example, SPY or the S&P 500), return frequency, lookback
window, observation count, and raw or adjusted beta convention.

## Independently Verified Market Evidence — September 23, 2026

**Risk-free rate:** 5.11%

**Source:** U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates, September 23, 2026, 10-year maturity.

**URL:** https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&trk=public_post_comment-text&type=daily_treasury_yield_curve

**Previous assumption:** 4.10% (Lab 06)

**Evidence assessment:** The earlier 4.10% assumption is not the same as the observed September 23, 2026 10-year yield. The September 23 Treasury rate is the appropriate dated reference if September 23 is selected as the final valuation date.

**Model status:** Not yet updated. Beta, ERP, borrowing cost, and market-value weights still require verification.

## Remaining WACC Component Research — September 23, 2026

This section separates facts reported by Walmart from market observations and
analyst estimates. Monetary amounts are in **millions of U.S. dollars** unless
otherwise stated. The research cutoff and proposed valuation date are both
September 23, 2026. No model input is changed by this analysis.

### 1. Equity risk premium

#### Published recommendation

- **Value:** **5.00% U.S. ERP**.
- **Provider:** Kroll.
- **Publication date:** September 10, 2026.
- **Effective date:** September 2, 2026, until further notice.
- **Units and intended use:** Percentage premium for USD-denominated discount
  rates under CAPM.
- **Original source:** [Kroll, “Cost of Capital Recommendations Updated to Use
  Spot Risk-Free Rates”](https://edge.sitecorecloud.io/krollllc17bf0-kroll6fee-proda464-0e9b/media/cost-of-capital/kroll-cost-of-capital-recommendations-updated-to-use-spot-risk-free-rates-september-2026.pdf).
- **Evidence assessment:** The publication directly reports that Kroll
  reaffirmed a 5.0% U.S. ERP. This supports the numerical value of the Python
  file's preliminary 5.00% assumption as a published recommendation available
  by September 23. It does not prove that 5.00% is the uniquely correct ERP.
- **Important pairing limitation:** Kroll directs users to pair its 5.00% ERP
  with the **spot 20-year U.S. Treasury yield** as of the valuation date. The
  evidence memo currently records a 5.11% **10-year** Treasury yield. Combining
  the Kroll ERP with that 10-year yield is therefore methodologically different
  from Kroll's stated convention.

#### Market-implied cross-check

[Aswath Damodaran's NYU Stern monthly ERP workbook](https://pages.stern.nyu.edu/~adamodar/pc/implprem/ERPbymonth.xlsx)
reports **4.14%** for “ERP (T12m with sustainable payout)” at the **September 1,
2026** start-of-month observation. The same row reports 4.09% for the unadjusted
trailing-12-month cash-flow specification, illustrating that the result depends
on the cash-flow convention. The 4.14% value is a forward-looking implied ERP
derived from an S&P 500 cash-flow valuation, not a historical realized premium.
It is a useful dated cross-check, but it is not a September 23 observation and
is not interchangeable with Kroll's recommended ERP.

**ERP conclusion:** The preliminary **5.00%** is supported as a dated Kroll
recommendation in force on September 23, 2026. Selection of Kroll's convention,
including its required 20-year risk-free-rate pairing, remains an analytical
choice rather than a reported Walmart fact.

### 2. Pretax cost of debt

#### Walmart-reported borrowing facts

The following are company-reported facts, not cost-of-debt estimates:

| Reported fact | Value and unit | Reporting date | Source |
|---|---:|---|---|
| Short-term borrowings | $6,596 million; 4.0% weighted-average rate | January 31, 2026 | [Walmart FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) |
| Long-term debt, including current maturities | $38,166 million carrying value; $36,777 million fair value | January 31, 2026 | [Walmart FY2026 Form 10-K, Notes 5 and 7](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) |
| Fixed-rate long-term debt | $37,416 million; 4.1% weighted-average stated rate | January 31, 2026 | [Walmart FY2026 Form 10-K market-risk table](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) |
| Long-term credit ratings | S&P AA; Moody's Aa2; Fitch AA | January 31, 2026 | [Walmart FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) |
| Short-term borrowings | $10,479 million; carrying value approximates fair value because of short maturities | July 31, 2026 | [Walmart Form 10-Q filed August 28, 2026](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) |
| Long-term debt, including current maturities | $39,932 million carrying value; $37,267 million fair value | July 31, 2026 | [Walmart Form 10-Q filed August 28, 2026](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) |
| Long-term credit ratings | S&P AA; Moody's Aa2; Fitch AA | July 31, 2026 | [Walmart Form 10-Q](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) |

The 4.0% and 4.1% filing rates are historical weighted-average borrowing or
stated rates. They are not September 23 marginal yields and should not be
presented as the valuation-date pretax cost of debt.

#### Walmart issuance and valuation-date market-yield evidence

Walmart's [April 28, 2026 final pricing
terms](https://www.sec.gov/Archives/edgar/data/104169/000119312526183374/0001193125-26-183374-index.htm)
reported the following yields to maturity and Treasury spreads for its fixed-rate
senior unsecured notes:

| Maturity | Principal | Coupon | Issue YTM | Spread to benchmark Treasury |
|---|---:|---:|---:|---:|
| April 30, 2029 | $650 million | 4.000% | 4.027% | +20 bp |
| April 30, 2031 | $1,000 million | 4.150% | 4.198% | +25 bp |
| April 30, 2033 | $1,250 million | 4.450% | 4.462% | +33 bp |
| April 30, 2036 | $1,000 million | 4.750% | 4.758% | +43 bp |

Those are primary-market yields from April 2026, not September 23 secondary-
market yields. For a same-date market cross-check, the [ICE BofA AA U.S.
Corporate Index Effective Yield, FRED series
`BAMLC0A2CAAEY`](https://fred.stlouisfed.org/series/BAMLC0A2CAAEY), was
**5.66% on September 23, 2026**. Its units are percent, not seasonally adjusted,
daily close. Walmart's AA/Aa2/AA ratings make the AA index directionally
relevant, but the index is not a Walmart-specific yield and contains securities
with different maturities and structures.

Two transparent proxies result:

1. **5.54% spread-based proxy:** 5.11% September 23 ten-year Treasury yield +
   0.43% spread from Walmart's April 2036 issue. This assumes the April Walmart
   spread remained unchanged, which has not been established.
2. **5.66% rating-index proxy:** the September 23 AA corporate index effective
   yield. This is current to the valuation date but is not company-specific.

**Pretax cost-of-debt conclusion: UNVERIFIED.** Available evidence supports an
illustrative **5.54%–5.66%** range, rather than the preliminary 4.50%, but no
September 23 Walmart bond price or yield was located to verify a company-specific
marginal borrowing cost. Coupons, historical average rates, issuance yields, and
current index yields are different measures and must not be conflated.

### 3. Market-value capital weights

#### Equity market value estimate

- **September 23, 2026 WMT closing price:** **$110.53 per share**, reported by
  [StockAnalysis historical prices](https://stockanalysis.com/stocks/wmt/history/)
  and independently matched by [ChartExchange historical
  prices](https://chartexchange.com/symbol/nasdaq-wmt/historical/).
- **Share count:** **7,933,746,241 common shares outstanding as of August 26,
  2026**, reported in Walmart's [Form 10-Q filed August 28,
  2026](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm).
  This is an actual shares-outstanding snapshot, not the diluted weighted-average
  share count used for EPS.
- **Estimated equity market value:**

\[
E = \$110.53 \times 7{,}933.746241\text{ million shares}
  = \$876{,}916.9\text{ million}
\]

The price is from the valuation date, but the latest filed actual share count is
28 days earlier. Any issuance, vesting, or repurchase activity after August 26
is not captured; therefore the exact September 23 equity value is **UNVERIFIED**.

#### Explicit debt measure

For this estimate, **debt is defined as interest-bearing short-term borrowings
at carrying value plus the disclosed fair value of long-term debt, including
current maturities**, using the latest filing available before the valuation
date:

\[
D = \$10{,}479 + \$37{,}267 = \$47{,}746\text{ million}
\]

This measure uses July 31, 2026 values from the August 28 Form 10-Q. Short-term
carrying value is used because Walmart states that it approximates fair value;
long-term debt uses Walmart's Level 2 fair-value estimate. The definition
excludes operating lease obligations, finance lease obligations, accounts
payable, undrawn credit facilities, letters of credit, noncontrolling interests,
and netting of cash. At July 31, finance lease obligations were $880 million
current and $5,952 million long-term; including them would increase the debt
weight. The selected exclusions are conventions, not findings that those claims
have no financing character.

#### Estimated weights

\[
w_E = \frac{876{,}916.9}{876{,}916.9 + 47{,}746} = 94.8364\%
\]

\[
w_D = \frac{47{,}746}{876{,}916.9 + 47{,}746} = 5.1636\%
\]

These estimates are close to the preliminary 95% equity / 5% debt assumptions,
but they are **UNVERIFIED as exact September 23 market-value weights** because
the share count and debt fair value precede the valuation date and no September
23 fair value was reported for Walmart's entire debt portfolio.

### 4. Clearly labelled illustrative WACC — not a final selection

The following calculation shows how the researched evidence fits together. It
is **ILLUSTRATIVE ONLY** and is **not a selected final WACC**:

| Input | Illustrative value | Status |
|---|---:|---|
| Risk-free rate | 5.11% | September 23 ten-year Treasury evidence already recorded above; Kroll's ERP guidance instead specifies a 20-year Treasury pairing |
| Beta | 0.55 | **UNVERIFIED** provisional assumption |
| Equity risk premium | 5.00% | Kroll published recommendation in force on September 23 |
| Pretax cost of debt | 5.66% | **UNVERIFIED** AA-index proxy, not a Walmart-specific yield |
| Tax rate | 24.50% | **UNVERIFIED** provisional WACC assumption; approximately the filing-attributed historical effective rate |
| Equity weight | 94.8364% | Estimated using dated price and latest pre-valuation-date filed shares |
| Debt weight | 5.1636% | Estimated using latest pre-valuation-date short-term debt and long-term debt fair value |

\[
r_e = 5.11\% + 0.55(5.00\%) = 7.86\%
\]

\[
r_d(1-T) = 5.66\%(1-24.50\%) = 4.2733\%
\]

\[
\text{Illustrative WACC}
= 94.8364\%(7.86\%) + 5.1636\%(4.2733\%)
= \mathbf{7.6748\%}
\]

Using the 5.54% spread-based debt proxy instead would produce approximately
7.6701%, holding all other illustrative inputs constant. These figures are not
final because beta, the marginal Walmart debt yield, the tax-rate convention,
the exact valuation-date capital weights, and the risk-free-rate/ERP maturity
pairing remain unresolved. No Python or valuation-model input should be updated
from this illustration without an explicit final methodology decision.

## WACC Reconciliation and Decision

### Three rates being compared

| Rate | Recomputed value | Basis | Status |
|---|---:|---|---|
| Preliminary calculated WACC | **6.677375%**, displayed as **6.6774%** | 4.10% risk-free rate, 0.55 beta, 5.00% ERP, 4.50% pretax debt cost, 24.50% tax rate, and 95%/5% weights | Arithmetic verified; economic inputs were explicitly preliminary assumptions in `walmart_project1_wacc.py` |
| Existing model assumption | **7.00%** | Selected in the historical Lab 06/model as a provisional rate within an approximate 6.7%–7.0% range | Not generated by a separately documented component set; **UNVERIFIED** judgmental overlay |
| New illustrative WACC | **7.674797%**, displayed as **7.6748%** | 5.11% risk-free rate, 0.55 beta, 5.00% ERP, 5.66% pretax debt proxy, 24.50% tax rate, and 94.8364%/5.1636% estimated weights | Arithmetic verified; **illustrative only**, with incomplete and mixed-date inputs |

The preliminary calculation is:

\[
r_e = 4.10\% + 0.55(5.00\%) = 6.85\%
\]

\[
r_d(1-T) = 4.50\%(1-24.50\%) = 3.3975\%
\]

\[
WACC = 95.00\%(6.85\%) + 5.00\%(3.3975\%) = 6.677375\%
\]

The illustrative calculation is:

\[
r_e = 5.11\% + 0.55(5.00\%) = 7.86\%
\]

\[
r_d(1-T) = 5.66\%(1-24.50\%) = 4.2733\%
\]

\[
WACC = 94.8364\%(7.86\%) + 5.1636\%(4.2733\%)
= 7.674797\% \approx 7.6748\%
\]

### Component-by-component numerical bridge

The bridge below changes one component group at a time. Risk-free rate, beta,
ERP, and debt cost are changed before the weights; this ordering makes each
increment reproducible. A different ordering would reallocate a small interaction
effect but would not change the ending WACC.

| Step | Preliminary input | Illustrative input | Input change | Incremental WACC effect | Running WACC | Evidence classification |
|---|---:|---:|---:|---:|---:|---|
| Starting preliminary calculation | — | — | — | — | **6.677375%** | All market inputs are preliminary assumptions in the Python file. |
| Risk-free rate | 4.10% | 5.11% | +1.01 percentage points | **+0.959500 pp** | **7.636875%** | 4.10% is an unsupported preliminary assumption; 5.11% is the documented September 23 ten-year Treasury observation. Effect: 95% × 1.01%. |
| Beta | 0.55 | 0.55 | 0.00 | **0.000000 pp** | **7.636875%** | No numerical change. Beta remains **UNVERIFIED** and provisional. |
| Equity risk premium | 5.00% | 5.00% | 0.00 pp | **0.000000 pp** | **7.636875%** | No numerical change. Its status improves from an unsupported assumption to a documented Kroll recommendation, but the Kroll maturity-pairing convention is not followed in the illustration. |
| Pretax cost of debt | 4.50% | 5.66% | +1.16 pp pretax; +0.8758 pp after tax | **+0.043790 pp** | **7.680665%** | 4.50% is preliminary; 5.66% is an **UNVERIFIED** AA-index proxy. Effect: 5% × 1.16% × (1 − 24.5%). |
| Capital weights | 95.0000% equity / 5.0000% debt | 94.8364% equity / 5.1636% debt | −0.1636 pp equity / +0.1636 pp debt | **−0.005868 pp** | **7.674797%** | Estimated from the documented price, share count, and debt measure; not exact September 23 weights. Moving weight from the 7.86% equity cost to the 4.2733% after-tax debt cost slightly lowers WACC. |
| Tax rate | 24.50% | 24.50% | 0.00 pp | **0.000000 pp** | **7.674797%** | No numerical change; the WACC tax-rate convention remains **UNVERIFIED**. |

The bridge sums to **+0.997422 percentage points**:

\[
6.677375\% + 0.959500\% + 0.000000\% + 0.000000\%
+ 0.043790\% - 0.005868\% = 7.674797\%
\]

Thus, approximately 96% of the total increase on this ordered bridge comes from
the risk-free-rate update. Beta and ERP create no numerical bridge because their
values remain 0.55 and 5.00%, respectively. The ERP evidence status changed,
but the number did not.

### Reconciliation to the 7.00% model assumption

- **7.00% minus 6.677375% = 0.322625 percentage points = 32.2625 basis
  points.** The 7.00% rate is not normal rounding of 6.677375%; normal rounding
  to two decimal percentage points gives 6.68%.
- The Python file calculates `wacc - PROVISIONAL_FCFF_WACC`, so it reports the
  same gap as **−0.322625 percentage points (−32.2625 basis points)**. The sign
  differs only because the subtraction direction is calculated-minus-model.
- **7.674797% minus 7.00% = 0.674797 percentage points = 67.4797 basis
  points.** No component-by-component bridge to 7.00% is possible because the
  evidence file does not document a distinct risk-free rate, beta, ERP, debt
  cost, tax rate, and weight set that produces exactly 7.00%. It remains a
  provisional judgmental overlay.

### Sourced observations versus assumptions and estimates

| Item used in the illustrative WACC | Classification at September 23, 2026 |
|---|---|
| 5.11% ten-year Treasury yield | Sourced September 23 market observation documented in this evidence file |
| 0.55 beta | **UNVERIFIED assumption** retained provisionally; reported external estimates range from 0.39 to 0.66 and are not equivalent measurements |
| 5.00% ERP | Sourced Kroll recommendation published September 10 and effective September 2; not a Walmart fact or directly observed market price |
| 5.66% pretax debt cost | **UNVERIFIED estimate** using a same-date AA corporate index, not a Walmart-specific traded yield |
| 24.50% tax rate | **UNVERIFIED assumption** approximating a historical effective tax rate; suitability as a marginal interest tax-shield rate is unresolved |
| 94.8364% / 5.1636% weights | Estimates using a September 23 share price, August 26 share count, and July 31 debt fair-value data |

### Arithmetic and date-consistency findings

1. **No arithmetic error was found** in either 6.677375% or 7.674797%; their
   displayed values of 6.6774% and 7.6748% are correct four-decimal rounding.
2. **The 7.00% rate is not arithmetically derived** from the preliminary inputs.
   Its 32.2625-basis-point uplift is undocumented beyond being a provisional
   modeling choice.
3. **Risk-free-rate/ERP maturity inconsistency:** the illustration combines a
   ten-year Treasury yield with Kroll's 5.00% ERP, while Kroll specifies a spot
   20-year Treasury pairing. The illustrative cost of equity is therefore not a
   fully Kroll-consistent estimate.
4. **Mixed observation dates:** September 23 is used for the Treasury yield and
   share price; September 10 is the Kroll publication date; August 31 is the
   nearest Trefis beta date; August 26 is the filed share-count date; and July 31
   is the debt fair-value date. The resulting 7.6748% is not composed entirely
   of same-date observations.
5. **Historical-date mismatch:** the preliminary calculation and 7.00% model
   assumption belong to the earlier lab/model evidence, while 7.6748% is an
   illustration for the proposed September 23 Project 1 date. They are useful
   for reconciliation but are not contemporaneous estimates.
6. **Document-status inconsistency:** the opening scope says the review is
   limited to the lab and Python file, and the earlier “Evidence still required”
   list predates the appended external research. Those statements describe the
   initial review, not the expanded evidence now contained in this file.

### Evidence still required before selecting a final WACC

1. A selected beta methodology or a reproducible regression ending on or near
   September 23, including benchmark, return frequency, lookback window,
   adjusted-price convention, observation count, and raw-versus-adjusted status.
2. A consistent risk-free-rate/ERP framework: either obtain the September 23
   20-year Treasury required by the documented Kroll recommendation, or document
   and support an ERP intended to be paired with the selected ten-year rate.
3. Walmart-specific secondary-market bond yields as of September 23, preferably
   across representative maturities and weighted to the debt portfolio, or a
   fully documented synthetic spread method. The AA index and the carried-forward
   April issuance spread remain proxies.
4. A documented marginal tax rate appropriate for the interest tax shield,
   rather than relying only on an approximate historical effective rate.
5. A final capital-definition decision covering finance leases, operating
   leases, noncontrolling interests, cash netting, and other claims, plus the
   best available September 23 share count and debt market value.
6. A single valuation-date policy that explicitly addresses unavoidable stale
   filing data and prevents Edition A, Lab 06, and final Project 1 dates from
   being mixed without disclosure.

**Decision status: no final WACC selected.** The 6.6774% and 7.00% figures remain
historical preliminary/model references, and 7.6748% remains an illustration
pending the evidence and methodology decisions above.
