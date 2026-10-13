# Walmart Project 1 WACC Sensitivity

> **Illustrative results only — this is not a final WACC selection or a final fair-value range.**

## Method

The scenario analysis uses the unchanged base-case five-year forecast inputs in `walmart_project1_proforma.py` and the FCFF and DCF calculations in `project1_fcff.py`. The new scenario script confirmed that the base-input dictionary and five annual FCFF amounts match the base case used by `project1_fcff.py`. One FCFF schedule was calculated and reused for all three WACC cases, so WACC is the only scenario variable.

- Terminal growth: **2.50%** in every case
- Forecast period: FY2027–FY2031
- Units: USD millions except value per diluted share
- Equity bridge held constant: enterprise value + $10,727 million cash − $44,762 million borrowings − $6,761 million finance leases
- Diluted shares held constant: 8,022 million

The common base-case FCFF forecast is:

| Fiscal year | FCFF ($ millions) |
|---:|---:|
| 2027 | 11,479.8 |
| 2028 | 12,067.2 |
| 2029 | 13,318.8 |
| 2030 | 14,506.9 |
| 2031 | 15,499.5 |

## Illustrative results

| WACC | Enterprise value ($ millions) | Equity value ($ millions) | Value per diluted share | Terminal-value share of enterprise value |
|---:|---:|---:|---:|---:|
| 6.6774% | 330,035.6 | 289,239.6 | $36.06 | 83.41% |
| 7.0000% | 305,974.3 | 265,178.3 | $33.06 | 82.27% |
| 7.6748% | 265,357.9 | 224,561.9 | $27.99 | 79.94% |

Enterprise value equals the present value of the five explicit-period FCFF amounts plus the present value of terminal value. Equity value uses the constant bridge above. Terminal-value share equals the present value of terminal value divided by enterprise value.

## Validation outcomes

| Check | Outcome |
|---|---|
| The same five-year base FCFF forecast is used in every case | **PASS** |
| WACC exceeds the 2.50% terminal-growth rate in every case | **PASS** — the minimum WACC is 6.6774% |
| Enterprise value decreases as WACC increases | **PASS** — $330,035.6 million → $305,974.3 million → $265,357.9 million |
| Equity value decreases as WACC increases | **PASS** — $289,239.6 million → $265,178.3 million → $224,561.9 million |
| Value per diluted share decreases as WACC increases | **PASS** — $36.06 → $33.06 → $27.99 |

These results isolate WACC sensitivity and remain illustrative. They do not establish a final WACC, fair value, or fair-value range.
