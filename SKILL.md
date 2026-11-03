---
name: warren-buffett-investing
description: Analyze a public company from its last five SEC 10-K fiscal years using Lab 18's deterministic Buffett checks, then write a short price-free investment memo. Use when asked for a Buffett-style business-quality review, owner earnings analysis, or the FIN 43900 Lab 18 workflow.
---

# Warren Buffett Investing

Use the bundled `scripts/sec_buffett.py` for every financial value and every
check. The model judges the business; it must not calculate, estimate, repair,
or silently replace financial data.

## Workflow

1. Ask for the SEC contact name and email if they are not already available in
   the current conversation or runtime. Never invent either value and never
   save personal contact information in the repository.
2. Set `SEC_EDGAR_NAME` and `SEC_EDGAR_EMAIL` only for the process that runs:

   ```bash
   SEC_EDGAR_NAME="<name>" SEC_EDGAR_EMAIL="<email>" \
     python .codex/skills/warren-buffett-investing/scripts/sec_buffett.py TICKER \
       --json-output lab18_output/TICKER_buffett_data.json
   ```

3. Read the script output. Treat `not found` and `not known` as results, not as
   invitations to estimate. If fewer than five fiscal years are available,
   disclose that limitation.
4. Write `lab18_output/TICKER_buffett_memo.md` as a short Buffett-style memo.
   Use only financial numbers printed by the script, including the exact
   displayed units. Do not use stock prices, market capitalization, valuation
   multiples, outside financial data, or model-generated arithmetic.
5. Give exactly one verdict: **own the business**, **watch it**, or **pass**.
   Explain what the three computed checks show, what remains unknown, and why
   the operating record supports the verdict. Judge business quality, not the
   price.
6. Run the memo-number validator after saving the memo:

   ```bash
   SEC_EDGAR_NAME="<name>" SEC_EDGAR_EMAIL="<email>" \
     python .codex/skills/warren-buffett-investing/scripts/sec_buffett.py TICKER \
       --validate-memo lab18_output/TICKER_buffett_memo.md
   ```

   Revise the memo if any unsupported number is flagged.

## Non-negotiable data rules

- SEC EDGAR company facts only; forms must be exactly `10-K`.
- Use the last five fiscal years, labelled by fiscal-year-end date.
- Revenue, net income, operating cash flow, and capital spending must cover a
  one-year period. When the same period occurs in several filings, the latest
  filing wins.
- Tag priority is fixed:
  - Revenue: `RevenueFromContractWithCustomerExcludingAssessedTax`, then
    `Revenues`.
  - Net income: `NetIncomeLoss`.
  - Operating cash flow: `NetCashProvidedByUsedInOperatingActivities`.
  - Capital spending: `PaymentsToAcquirePropertyPlantAndEquipment`, then
    `PaymentsToAcquireProductiveAssets`.
  - Equity: `StockholdersEquity`.
- ROE is net income divided by year-end equity.
- Owner earnings is operating cash flow minus capital spending.
- A missing value is `not found`. ROE is `not known` when equity is zero or
  below. A check with any missing input is `not known`.
- The three checks are computed only in Python: ROE at least 15% every year,
  positive owner earnings every year, and owner earnings growth from the first
  to last year.
