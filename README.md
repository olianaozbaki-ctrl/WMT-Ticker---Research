# Walmart (WMT) — Corporate Finance Project 1

**FIN 43900 | Purdue University**

## Project Overview

This project evaluates Walmart Inc. (NYSE: WMT) to determine whether an investment committee should initiate a position, place the company on watch, or decide not to invest.

The analysis incorporates financial statement research, a five-year financial forecast, discounted cash flow (DCF) valuation, comparable-company analysis, reverse DCF, scenario testing, and independent validation.

- **Company:** Walmart Inc. (WMT)
- **Proposed Valuation Date:** September 23, 2026
- **Current Recommendation:** Watch–Defer (provisional)
- **Forecast Period:** FY2027–FY2031

## Valuation Results

| Scenario | Estimated Value per Share |
|---|---:|
| Downside | $32.40 |
| Base | $36.78 |
| Upside | $44.00 |

The analysis also presents a conditional working reference zone of **$31–$49 per share**, compared with Walmart's reported closing price of **$110.53 on September 23, 2026**.

These estimates are provisional and depend on assumptions about revenue growth, operating margins, reinvestment, WACC, terminal growth, and the enterprise-to-equity bridge.

## Project Files

### Investment Research and Recommendation
- [Edition A](Walmart_Project_1_Edition_A.md)
- [Edition B Investment Committee Memo](Walmart_Project1_Edition_B_Investment_Memo.md)
- [Edition A to Edition B Comparison](Walmart_Project1_Edition_A_to_B_Comparison.md)

### Financial Models and Valuation
- [Five-Year Financial Model](walmart_project1_proforma_v3.py)
- [FCFF and DCF Valuation](project1_fcff_v3.py)
- [Scenario Analysis](Walmart_Project1_Final_Scenarios_and_Valuation_Range.md)
- [Reverse DCF](Walmart_Project1_Reverse_DCF_Evidence.md)
- [Comparable-Company Valuation](Walmart_Project1_Comparable_Valuation_Triangulation.md)
- [Valuation Assumptions](Walmart_Project1_Final_Valuation_Assumptions.md)

### Validation and Supporting Evidence
- [Independent Source Check](Walmart_Project1_Independent_Source_Check.md)
- [Equity Bridge Validation](Walmart_Project1_Equity_Bridge_Validation.md)
- [Locked Changed-Input Record](Walmart_Project1_Locked_Changed_Input_Record.md)
- [Cold-Run Reproducibility Report](Walmart_Project1_Reproducibility_Report.md)
- [Cold-Run Output Log](Walmart_Project1_Cold_Run.log)
- [AI-Use Record](Walmart_Project1_AI_Use_Record.md)
- [Evidence Manifest](Walmart_Project1_Evidence_Manifest.md)

## Reproducing the Analysis

The project uses Python 3.12 and standard-library dependencies.

To run the validation suite from the repository directory:

```bash
python3 -B walmart_project1_cold_run.py
```

The suite runs the financial model, scenario analysis, reverse DCF, comparables, and validation scripts. It reports whether calculations and internal model checks pass.

## Key Limitations

The model uses provisional valuation assumptions, including a 7.00% WACC, 2.50% terminal growth rate, July 31, 2026 bridge balances, and an August 26, 2026 basic share count. The valuation-date diluted share count and some financial classifications remain unresolved.

Passing computational checks does not independently verify financial source data or establish that forecast assumptions will occur.

## Additional Documentation

For a detailed overview of the model, methodology, and supporting files, see the [Full Project README](Walmart_Project1_README.md).

---

*Prepared for FIN 43900 as an academic research exercise. This material is not investment advice.*
