# Walmart Project 1 — Locked Changed-Input Record

## Test Identification
- Test name: Five-Year Revenue Growth Downside Test
- Date and time of prediction: October 12, 2026, 3:36 PM EDT
- Model and version: Walmart Project 1 V2 — Five-Year Three-Statement FCFF Model
- Baseline run/output reference: project1_fcff_v2.py; base-case valuation of $35.67 per diluted share using 7.00% WACC and 2.50% terminal growth.

## Human-Authored, AI-Off Prediction — Completed Before Running
- Input to change: Revenue Growth
- Original input and units: FY2027–FY2031 revenue growth rates of 4.3%, 4.2%, 4.0%, 3.8%, and 3.5%, respectively (annual percentage growth).
- Proposed new input and units: Decrease revenue growth by 1 percentage point each year.
- Expected output direction: Walmart's estimated value per share decreases.
- Why I expect that direction: Changes in projected cash flow can affect the present value of Walmart's future cash flows.
- Expected effect on the investment decision: I expect the lower valuation to strengthen the argument for keeping Walmart on the watchlist rather than investing at its current stock price.

## Precommit Evidence
- Saved prediction timestamp: October 12, 2026, 3:39 PM EDT
- Git commit or other immutable pre-run evidence: https://github.com/olianaozbaki-ctrl/WMT-Ticker---Research/commit/3314c717bd983030ec2011fa99e60c406cd74e56
- Confirmation that prediction was written before execution: The prediction-only record was uploaded to GitHub before the changed-input test was executed. The original commit preserves the prediction separately from the actual results.

## Actual Results — Completed After Running
- Test execution date and time: October 12, 2026, 3:50 PM EDT
- Actual input change: FY2027–FY2031 revenue growth decreased by 1 percentage point each year, from 4.3%, 4.2%, 4.0%, 3.8%, and 3.5% to 3.3%, 3.2%, 3.0%, 2.8%, and 2.5%.

- Actual output values and directions:
  - Original base valuation: $35.674421 per diluted share.
  - Changed-input valuation: $30.667082 per diluted share.
  - Change in valuation: -$5.007339 per diluted share (approximately -14.04%).
  - FY2027 FCFF change: -$468.710 million.
  - FY2028 FCFF change: -$845.958 million.
  - FY2029 FCFF change: -$1,257.139 million.
  - FY2030 FCFF change: -$1,699.209 million.
  - FY2031 FCFF change: -$2,162.975 million.

- Did the actual outcome match the prediction?: Yes. Walmart's estimated value per share decreased, matching my prediction. Annual FCFF also decreased across all five forecast years.

- Effect on the committee recommendation: The lower estimated intrinsic value supports maintaining the Watch–Defer recommendation rather than initiating a position at the comparison market price. The recommendation remains conditional because some model assumptions require further verification.

- Failure diagnosis or explanation of no change: No accounting or financing failures were reported. Both the base and changed-input cases passed the model's validation checks. The changed-input case maintained minimum cash of $8,626.0 million without requiring revolver borrowing. Lower revenue growth reduced forecast FCFF and the estimated value per share.

## Evidence and Reproducibility
- Files used:
  - walmart_project1_proforma_v2.py
  - project1_fcff_v2.py
  - walmart_project1_revenue_growth_changed_input.py
  - Walmart_Project1_Revenue_Growth_Changed_Input_Output.md
  - Walmart_Project1_Locked_Changed_Input_Record.md

- Test command: python3 walmart_project1_revenue_growth_changed_input.py
- Output log or screenshot: Walmart_Project1_Revenue_Growth_Changed_Input_Output.md and the VS Code execution screenshot.
- Remaining limitations: The valuation uses provisional WACC, terminal growth, and enterprise-to-equity bridge assumptions. Some operating-account classifications, share-count definitions, and source inputs still require final verification.