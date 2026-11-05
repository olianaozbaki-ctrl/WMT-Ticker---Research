
# Lab 19 – Legend Panel

## D – The Question

> When three investors' skills read the same 10-K facts, where do they agree, where do they split, and would you trust the panel?

For Costco, Buffett and Burry agree that the company's historical profitability, cash flow, and leverage meet their financial checks. Buffett passes all three checks, and Burry passes both. Wood passes the revenue-growth check, but the panel cannot determine disruptive-innovation exposure or reported R&D spending from the available SEC facts, so her overall verdict is **not known**. The difference shows that the same financial statements can support a business-quality screen without providing enough information for an innovation-focused screen.

I would trust the panel as a first-pass screening tool, but not as a final investment decision. The calculations and criteria are transparent, but the investors rely on the same SEC data, and the panel does not fully account for valuation, management, industry conditions, or future risks.

**Partner discussion:** Our discussion focused on why the investors reach different conclusions even when they use the same financial statements. Buffett and Burry both pass Costco, but Wood cannot reach a full verdict because the SEC numbers do not establish innovation exposure or R&D spending. We also discussed why missing data should stay `not known` instead of being treated as a failure.

## Build – The Panel

The active Lab 19 build retains the Lab 18 Buffett analysis and adds Cathie Wood-inspired and Michael Burry checks using five fiscal years of SEC 10-K facts.

- Buffett checks ROE, positive owner earnings, and owner-earnings growth.
- Wood checks documented disruptive-innovation exposure, first-to-last-year revenue growth, and positive latest reported R&D expense. These are **course interpretations**, not official ARK Invest rules.
- Burry checks whether operating cash flow was at least net income in every year and whether the latest liabilities-to-equity ratio was no greater than 2.0.
- Every check returns **pass**, **fail**, or **not known**. Missing information remains unknown rather than being estimated.
- `lab19_panel.py` calculates the checks and generates three independent memos. `lab19_panel_app.py` displays the investor-by-check table, separate verdicts, the three memos, and an unprinted-number check across all memos.

The previous Graham analysis is preserved in `lab19_archive/graham/`, but Graham is no longer part of the active panel after the in-class change.

## Validation – Active Costco Panel

The Costco results below are from the Streamlit panel using five fiscal years of SEC-derived financial facts. The saved analysis is located in `lab19_output/COST_panel_data.json`.

| Investor | Check | Result |
|---|---|---|
| Buffett | ROE of at least 15% every year | Pass |
| Buffett | Positive owner earnings every year | Pass |
| Buffett | Owner earnings increased | Pass |
| Wood | Disruptive-innovation exposure established | Not known |
| Wood | Revenue increased from first to last year | Pass |
| Wood | Latest reported R&D expense is positive | Not known |
| Burry | Operating cash flow at least net income every year | Pass |
| Burry | Latest liabilities no more than twice equity | Pass |

**Costco verdicts:** Buffett 3/3, **own the business**; Wood 1 pass and 2 not known, **not known**; Burry 2/2, **financial checks pass**. Costco's revenue rose from $226,954 million to $303,154 million, and its latest liabilities-to-equity ratio was 1.49. Innovation exposure was not established from the numeric SEC data, and reported R&D was not found in this panel's source data.

All three Costco memos passed the unprinted-number check. The Lab 18 and Lab 19 tests also passed, including the test showing that Wood's results depend on the input data rather than hardcoded Costco answers.

## Wood Operational Interpretation

The Wood checks use a transparent classroom interpretation of Cathie Wood's emphasis on disruptive innovation and long-term growth, not an official ARK Invest screening model. Revenue growth is a measurable sign of scaling, and reported R&D expense can provide limited evidence of investment in new products. However, neither alone establishes that a company is a disruptive innovator. The panel therefore leaves innovation exposure **not known** unless separate evidence supports it.

## Historical Graham Validation – Superseded

The original Graham version was completed before the professor replaced Graham with Wood. It is archived in `lab19_archive/graham/` and is not part of the active panel. With Graham's current-ratio threshold at 2.0, Costco scored Buffett 3/3, Graham 2/3, and Burry 2/2. Lowering the threshold to 1.0 changed Graham to 3/3 without changing the underlying numbers. Costco's latest current ratio was 1.06. These results are included only to document the earlier work.

## Your Company – NVIDIA (NVDA)

I analyzed NVIDIA using the Vanguard S&P 500 ETF (VOO) as the reference fund.

| Investor | Checks | Verdict |
|---|---|---|
| Buffett | 3/3 pass | Own the business |
| Cathie Wood | 2 pass, 1 not known | Not known |
| Michael Burry | 1 pass, 1 fail | Forensic concern |

Buffett's framework produced the strongest result. NVIDIA's ROE stayed above 15% in all five years, owner earnings were positive every year, and owner earnings increased from $8,132 million to $96,676 million. Wood's framework passed revenue growth and reported R&D checks. Revenue increased from $26,914 million to $215,938 million, and latest reported R&D was $18,497 million. However, innovation exposure remained **not known** because the numeric SEC facts did not establish it.

Burry identified a concern because operating cash flow did not equal or exceed net income in every year. NVIDIA still passed his leverage check, with a latest liabilities-to-equity ratio of 0.31. These results show how the investors can reach different conclusions using the same financial statements.

## Explain the Code

The `wood_checks` function starts by setting each result to `not known`. It only changes the innovation check when separate evidence is explicitly supplied. With five fiscal-year rows, it compares the first year's revenue with the last year's revenue and tests whether the most recent reported R&D expense is positive. If the necessary data are missing, the check remains **not known** instead of automatically passing or failing.

**Partner code discussion:** I explained that `wood_checks` starts with `not known` values and updates only the checks supported by available data. We discussed what happens when the latest R&D expense is missing: the R&D check stays `not known` instead of automatically passing or failing. We also reviewed how checking inputs before making comparisons prevents the code from treating missing information as a financial conclusion. For the role swap, we used the same approach to explain why the cash-flow coverage check can fail even if the latest year looks strong.

## Bull and Bear

**Bear case discussed for partner review:** Although NVIDIA has experienced significant growth, its operating cash flow did not meet or exceed net income in every year, causing it to fail one of Burry's checks. This raises questions about whether earnings are consistently supported by operating cash flow.

**My bull case:** NVIDIA maintained ROE above 15% and positive owner earnings across all five years, with owner earnings increasing from $8,132 million to $96,676 million. Revenue also rose from $26,914 million to $215,938 million, while the latest liabilities-to-equity ratio of 0.31 passed Burry's leverage check.

## Decision

**Only with a condition.** I would use the panel as an initial investment screen, but only after checking that its calculations reproduce correctly and following up with company-specific research and valuation. NVIDIA passes Buffett's checks and most of Wood's measurable checks, but Burry raises a cash-flow concern and Wood's innovation exposure remains unknown. Those differences are worth investigating before making an investment decision.

## A Panel of AI Agents

A panel of AI agents applies different investment frameworks to the same data. Buffett focuses on business quality and owner earnings, Wood emphasizes innovation and growth, and Burry tests cash-flow coverage and leverage. Their conclusions may differ because the checks emphasize different financial characteristics, even when the underlying 10-K facts are identical. The panel is useful for identifying areas that need more research, but shared data limitations can affect all three investors.

**Partner discussion:** We discussed how an AI-agent panel can disagree without using different underlying facts. The important distinction is that different rules produce different verdicts, while missing or incorrect SEC data can affect every investor in the panel. This reinforced why the panel should support further research rather than replace it.

## Reflection

The Costco and NVIDIA analyses helped me see why the same company can receive different results depending on what each investor prioritizes. For Costco, Buffett and Burry passed all their checks, while Wood could not reach a complete verdict because innovation exposure and reported R&D were not established. For NVIDIA, Buffett passed all three checks and Wood passed revenue growth and R&D, but her innovation result remained unknown. Burry raised a concern because operating cash flow did not cover net income in every year, even though NVIDIA passed the leverage check.

This makes the panel useful for identifying strengths, risks, and missing information, rather than automatically deciding whether to invest. I would want to review NVIDIA's cash-flow differences, confirm its innovation position using company-specific evidence, and consider valuation before relying on the results.

## Checkout

Launch the application from the project folder:

```bash
python -m streamlit run lab19_panel_app.py
```

The saved Costco data can be opened using **Load saved Costco validation**. A fresh SEC request requires contact information at runtime.

## References

- [Lab 19 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-11/lab-19-legend-panel.md)
- [FAskills financial-researcher plugin](https://github.com/CinderZhang/FAskills)
- [ARK Invest investment process](https://www.ark-invest.com/investment-process/)
- [ARK disruptive-innovation strategy](https://www.ark-invest.com/strategy/ark-disruptive-innovation)
- [ARK Invest FAQ](https://www.ark-invest.com/faq)
- [SEC EDGAR API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
