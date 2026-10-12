# Walmart Project 1 — Cold-Run Reproducibility Report

**Run date:** October 12, 2026  
**Result:** The listed scripts ran in fresh Python subprocesses; all exited 0. Arithmetic/model checks reported PASS. This does not independently verify economic assumptions or source data.

## Commands and runtime

Harness command, run from the project directory:

```text
python3 -B walmart_project1_cold_run.py
```

The harness launched each item below as a separate process using the active Python interpreter (`/Library/Frameworks/Python.framework/Versions/3.12/bin/python3`):

```text
python3 -B walmart_project1_proforma_v3.py
python3 -B project1_fcff_v3.py
python3 -B walmart_project1_v3_final_scenarios.py
python3 -B walmart_project1_reverse_dcf_v3.py
python3 -B walmart_project1_comparables_v3.py
python3 -B walmart_project1_equity_bridge_validation.py
python3 -B walmart_project1_revenue_growth_changed_input_test.py
```

Runtime was Python **3.12.5** on macOS 15.7.4 arm64. Required dependencies are the Python standard library and the existing local project modules in this directory. No third-party packages, network calls, or data downloads were used. `-B` and `PYTHONDONTWRITEBYTECODE=1` prevented bytecode writes during subprocess runs.

The literal stdout, commands, exit codes, timestamps, runtime, and before/after SHA-256 values are preserved in [Walmart_Project1_Cold_Run.log](Walmart_Project1_Cold_Run.log). To repeat, run the harness command above from this directory.

## Results

| Check | Status | Cold-run result |
|---|---|---|
| V3 pro-forma balance-sheet articulation | **PASS** | All five years balance gap $0.000000M; cash-flow articulation $0.000000M. |
| V3 debt and finance-lease roll-forwards | **PASS** | Both reported roll-forward gaps $0.000000M. |
| V3 liquidity | **PASS** | Minimum cash $10,303.6M; maximum revolver $0.0M. |
| V3 base DCF | **PASS** | EV $334,855.6M; equity $291,806.6M; $36.780427/share using August 26 basic shares; terminal-value share 82.03%. WACC 7.00%, terminal growth 2.50%. |
| Downside scenario | **PASS** | $32.3958/share; feasible; minimum cash $8,000.0M; peak revolver $2,125.5M of $15,000M. Statement and DCF checks PASS. |
| Base scenario | **PASS** | $36.7804/share; feasible; no revolver draw. Statement and DCF checks PASS. |
| Upside scenario | **PASS** | $43.9999/share; feasible; no revolver draw. Statement and DCF checks PASS. |
| Scenario DCF boundary and bridge arithmetic | **PASS** | Each case satisfies WACC > terminal growth (7.00% > 2.50%) and reported bridge/per-share controls. |
| Synthetic known-answer equity bridge | **PASS** | $1,000M EV + $100M cash − $250M debt − $50M finance leases = $800M equity; 100M shares = $8.00/share; assertions passed. |
| Supplied V2 bridge arithmetic | **PASS** | Supplied rounded inputs calculate $286,180.2M equity and $35.674420/share, which rounds to $35.67. Difference from the displayed $35.67 is +$0.004420/share before rounding. This validates arithmetic only. |
| V2 changed-input isolation | **PASS** | Only revenue growth changed, down exactly 1.00 percentage point in each of FY2027–FY2031; base inputs were not mutated. Both cases passed accounting/liquidity controls. |
| V2 changed-input valuation | **PASS** | Base $35.674421/share; changed case $30.667082/share. Changed case is −$5.002918/share versus the rounded $35.67 baseline, or −$5.007338 versus the unrounded cold-run base. No accounting or financing failure. |
| Reverse-DCF solve | **PASS** | Reproduced the entered $110.53 September 23, 2026 price with either growth shift +11.18448276 points or expense-ratio reduction 17.19207532 points; internal statement and DCF checks PASS. |
| Comparable-company calculations | **PASS** | Arithmetic/validation PASS. Target: 13.4353x EV/EBIT and 16.2095x P/E; Walmart indications $49.24/$44.74. Costco: 34.4753x and 45.5080x; indications $134.84/$125.60. |
| Script process exits | **PASS** | All seven subprocess commands returned exit code 0. |
| Protected-file integrity | **PASS** | SHA-256 before/after matched for all 23 listed existing models, reports, Edition A, both existing Edition B artifacts, and Locked Changed-Input Record. Hashes are in the log. |
| Primary-source re-fetch / independent source verification | **NOT RUN** | The cold run did not access SEC, exchange, Treasury, Kroll, FRED, or peer source pages. Existing inputs were consumed as stored. |
| Economic reasonableness / forecast validation | **NOT RUN** | Internal controls do not prove the assumptions are economically likely or that model definitions match the filings. |
| Valuation-date completeness | **NOT RUN** | The V3 values still use July 31 bridge inputs and August 26 basic shares, not a verified September 23 debt/cash/lease bridge and diluted denominator. |

## Key calculations and discrepancies

The V3 base result reproduced the existing scenario report. Scenario outputs reproduced the listed downside/base/upside values. All scenario cases had zero displayed balance, cash-flow, debt-roll and finance-lease-roll gaps; these are computational checks under existing model rules.

Reverse DCF reproduced $110.53/share, but the two materially different solved operating paths demonstrate that the reverse problem is non-unique. This is a pass for solver arithmetic, not for the economic plausibility of either path.

The peer arithmetic reproduced the documented indications. Those results retain the known caveats: Target's TTM EBIT includes a $994M tariff-refund benefit; Costco periods end earlier; peers' share and balance dates lag; TTM EPS is assembled from rounded reported EPS; and peer EV excludes leases while Walmart's conversion separately deducts finance leases.

The V2 changed-input calculation produced $30.667082/share. The report's comparison against $35.67 is −$5.002918/share; comparing to the model's unrounded cold-run base is −$5.007338/share. This difference is a denominator/display precision distinction, not a failed test. The Locked Changed-Input Record was hash-identical before and after.

No numerical/model check failed in this run. The principal unresolved discrepancy is temporal/definition-based rather than arithmetic: the proposed September 23 valuation date does not match the July 31 bridge balances or August 26 basic-share denominator. WACC components, excess cash, market-value debt, finance-lease treatment, noncontrolling interests, nonoperating investments, and some operating working-capital classifications remain provisional or unverified as documented in prior evidence files.

## Interpretation and limitations

“PASS” means the script completed and its stated arithmetic or internal controls passed. It does not mean source observations were independently re-collected, accounting classifications were independently validated, assumptions were selected, or the valuation is investment-ready. The $32.40–$44.00 scenario range and $36.78 base are diagnostic outputs under provisional inputs. The reverse DCF is calibrated to a stored $110.53 observation, and peer multiples are arithmetic on stored inputs; neither is an independent conclusion about fair value.

The cold-run log is the raw evidence for this report. Existing model and evidence files were not edited by the harness; only the three requested new files were created by this task.
