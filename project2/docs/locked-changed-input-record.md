# Locked Changed-Input Record

## Pre-Run Record

- Test-only changed input: `objective.real_return_spread`
- Baseline value: 0.04
- Proposed value: 0.05
- Units: Annual return above CPI, expressed as a decimal
- Baseline commit: `05853e3`
- Baseline output artifact: `outputs/phase2_results.md`
- Expected output direction: Lower probability of achieving the investment objective because the required annual return increases from 4% to 5% above inflation.
- Expected decision effect:Potential change in the recommended portfolio allocation toward investments with higher expected returns, depending on the application's constraints and decision rules.
- Prediction written at (local date, time, and time zone): November 17, 2026, 11:30 PM EST

## Post-Run Record

- Changed input actually used: `objective.real_return_spread` increased from 0.04 to 0.05.
- Run command and timestamp: `bash scripts/run_locked_test.sh` on November 17, 2026. Preserved file-system evidence bounds the completed run: baseline files were preserved at 11:58:43 PM EST, changed-input reports were generated at 11:58:58 PM EST, and changed-input checksum evidence was completed at 11:59:03 PM EST. The available evidence does not establish an exact command-start timestamp, so none is asserted.
- Pre-run prediction commit: `1fd3c8ba1895424dcea5a0c1eb76f4934f09f346` (`1fd3c8b`).
- Preserved after-run output artifacts: `outputs/locked-changed-input-test-1fd3c8b/changed-input/phase2_results.md` and `outputs/locked-changed-input-test-1fd3c8b/changed-input/phase4a_decision_support.md`; corresponding JSON files, the changed mandate, and SHA-256 manifest are preserved in the same directory. Baseline artifacts and their SHA-256 manifest are preserved in `outputs/locked-changed-input-test-1fd3c8b/baseline/`.
- Actual output direction: The required return increased from 7.3965% to 8.3965%. The optimized portfolio shifted from 48% BIL and 52% VT to 35% BIL and 65% VT. The after-cost expected return increased from 7.45% to 8.41%, while annualized volatility increased from 7.82% to 9.75%.
- Actual decision effect: Although the optimized portfolio allocation changed, the investment decision remained HOLD. Full mandate compliance was still unverified, and the portfolio remained infeasible under the hypothetical 25% turnover constraint.
- Reconciliation with prediction: The results partially supported my original prediction. As expected, the optimized portfolio shifted toward investments with higher expected returns. However, the overall investment decision remained unchanged. My prediction regarding a lower probability of achieving the investment objective could not be directly verified because the application does not calculate that probability.
- Failure diagnosis or explanation if the result did not change: The investment decision remained HOLD because increasing the required return did not resolve the existing limitations related to actual holdings, liquidity, issuer exposure, turnover, and S9. The higher return requirement also increased portfolio volatility and sensitivity to the historical estimation window.
- Additional validation finding: The generated reports retained the CPI + 4% label even though the numerical hurdle correctly increased to 8.3965%. This indicates a reporting-label issue rather than a failure of the numerical optimization. The reporting correction is covered by regression tests; the original locked-test artifacts remain unchanged as evidence of the issue.
