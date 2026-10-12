# Walmart Project 1 — V3 FCFF Valuation

## Project purpose

This project evaluates whether Walmart Inc. (WMT) merits further investment research for an equity research analyst presenting to an investment committee with no current position. The proposed valuation date is **September 23, 2026**. The current provisional stance is **Watch–Defer**: the stored market close of $110.53 is well above the project's conditional valuation references, but several inputs are not verified for the valuation date. This README documents analysis, not a final investment recommendation.

Edition A remains the historical September 1, 2026 baseline. The separate committee memo is [Walmart_Project1_Edition_B_Investment_Memo.md](Walmart_Project1_Edition_B_Investment_Memo.md). The pre-existing `Walmart_Project_1_Edition_B.md` is another historical artifact and has not been replaced.

## Model and reproducibility

The V3 operating model is `walmart_project1_proforma_v3.py`; `project1_fcff_v3.py` produces the five-year FCFF forecast and DCF. The model forecasts FY2027–FY2031. Python standard-library modules are sufficient; the local model modules are imported from this folder. No third-party package installation or live data download is required for the stored-input analysis.

From the project folder, run the complete clean-process validation suite:

```text
python3 -B walmart_project1_cold_run.py
```

The harness starts separate Python subprocesses (Python 3.12.5 was used for the recorded run), captures actual stdout and exit codes in `Walmart_Project1_Cold_Run.log`, and checks SHA-256 hashes of protected files. To run a single component, use:

```text
python3 -B walmart_project1_proforma_v3.py
python3 -B project1_fcff_v3.py
python3 -B walmart_project1_v3_final_scenarios.py
python3 -B walmart_project1_reverse_dcf_v3.py
python3 -B walmart_project1_comparables_v3.py
python3 -B walmart_project1_equity_bridge_validation.py
python3 -B walmart_project1_revenue_growth_changed_input_test.py
```

The recorded cold run reports process exits and internal arithmetic/model controls as PASS. The SHA-256 check reported 23 protected existing files unchanged. The tests do not independently fetch or verify filing inputs, forecast assumptions, market prices, or valuation-date completeness. See [the reproducibility report](Walmart_Project1_Reproducibility_Report.md) and [raw cold-run output](Walmart_Project1_Cold_Run.log).

## V3 base and scenario results

The provisional base DCF is **$36.78 per August 26 basic share** (EV $334,855.6M; equity value $291,806.6M), using 7.00% WACC and 2.50% terminal growth. Those discount-rate assumptions are not final. The model's cash/debt/finance-lease bridge is based on July 31 balances; its denominator is an August 26 basic count, not a September 23 diluted count.

| Scenario | Per-share output | EV ($M) | Equity ($M) | Status |
|---|---:|---:|---:|---|
| Downside | $32.40 | 300,069.4 | 257,020.4 | Feasible in modeled financing limits; peak revolver $2,125.5M |
| Base | $36.78 | 334,855.6 | 291,806.6 | Feasible; no revolver draw |
| Upside | $44.00 | 392,133.3 | 349,084.3 | Feasible; no revolver draw |

These diagnostic scenario outputs hold the same WACC, terminal growth, bridge, and shares constant. They are not a final fair-value range. The upside includes a modeled $9,022M FY2027 working-capital release that lacks an independently documented operating plan.

The conditional screening zone in the current analysis is **$31–$49 per share**, not a statistically derived interval. It combines a higher-WACC illustration with Target-based peer indications. Costco indications are much higher and are treated as premium context rather than a central anchor. A reverse DCF fits the reported $110.53 September 23 close only by assuming either a very high path of revenue growth or a large operating-efficiency step-up; those solved assumptions are not verified market expectations.

## Key limitations

- WACC: 7.00% is provisional. Risk-free rate/ERP maturity pairing, beta, company-specific cost of debt, tax rate, and market-value capital weights remain unresolved.
- Shares: V3 uses 7,933.746241M basic shares as of August 26. The FY2026 8,022M diluted weighted-average share figure is a period average, not a valuation-date share count.
- Bridge: V3 uses July 31 cash ($11,529M), debt proxy ($47,746M), and finance leases ($6,832M). Excess cash, September 23 debt value, finance/operating lease consistency, noncontrolling interests, and nonoperating investments remain unverified or assumed.
- Operating working capital: V3 classifies individual accounts more carefully than earlier versions, but supplier financing and some mixed accrued/prepaid/tax accounts remain unresolved. The upside working-capital release is especially uncertain.
- Terminal value represents about 82% of the V3 base EV; forecasts, terminal growth, and discount rate therefore materially affect value.
- Peer multiples use lagged peer shares/balances and differing periods/lease conventions; Target TTM EBIT includes a reported tariff-refund benefit. The sample is only Target and Costco.
- The proposed valuation date is not consistently represented across market price, shares, and bridge balances. No source re-fetch or economic reasonableness review was performed during the cold run.

## Repository map

See [Walmart_Project1_Evidence_Manifest.md](Walmart_Project1_Evidence_Manifest.md) for the verified file inventory and role-by-role map. The core items are:

- V3 model and DCF: `walmart_project1_proforma_v3.py`, `project1_fcff_v3.py`
- Scenarios: `walmart_project1_v3_final_scenarios.py`, `Walmart_Project1_Final_Scenarios_and_Valuation_Range.md`
- Reverse DCF: `walmart_project1_reverse_dcf_v3.py`, `Walmart_Project1_Reverse_DCF_Evidence.md`
- Peers: `walmart_project1_comparables_v3.py`, `Walmart_Project1_Comparable_Valuation_Triangulation.md`
- Validation: `walmart_project1_equity_bridge_validation.py`, `walmart_project1_revenue_growth_changed_input_test.py`, `walmart_project1_cold_run.py`
- Decision evidence: `Walmart_Project1_Edition_B_Investment_Memo.md`

The raw source records, additional analysis, limitations, and missing submission artifacts are tracked in the evidence manifest and [submission checklist](Walmart_Project1_Submission_Checklist.md).

## Data sources

Financial-statement facts are drawn from Walmart's [FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) (year ended January 31, 2026; filed March 13, 2026) and [FY2027 Q2 Form 10-Q](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) (period ended July 31, 2026; filed August 28, 2026). Peer filing links, market-data sources, and rate evidence are indexed in the memo and supporting reports. Observed source facts are distinguished from model estimates and assumptions in those files.

This workspace did not resolve to a local Git repository when inspected, and these files have not been pushed or published by this task. This README is prepared as a project-root README artifact for review and later repository placement; it does not assert that a student GitHub repository exists or is accessible to course staff.
