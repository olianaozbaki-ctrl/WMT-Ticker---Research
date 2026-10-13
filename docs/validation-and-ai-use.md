# Walmart (WMT) | Project 1 Validation and AI-Use

**FIN 43900 | Purdue University | October 12, 2026**

This report explains how I checked my Walmart financial models, what the tests showed, and how I used AI throughout the project. My goal was to make sure the results could be repeated while also identifying the assumptions that still needed more research.

## 1. How I Checked My Financial Model

After building my five-year model and DCF, I used several tests to see whether the calculations worked as expected. I kept the test results and supporting code in my GitHub repository.

| Test | What I Checked | Recorded Result |
|---|---|---|
| Enterprise-to-Equity Bridge | A separate example with known inputs and an expected answer. | $800 million in equity value and $8.00 per share; PASS |
| Changed-Input Test (V2) | Lowered FY2027–FY2031 revenue growth by one percentage point each year. | Value decreased from $35.674421 to $30.667082 per share; PASS |
| Cold-Run Test | Ran seven Python scripts in fresh processes and checked protected files. | Seven successful script exits and 23 files unchanged; PASS |
| V3 Model and Scenarios | Checked modeled statements, financing, and DCF calculations. | Downside $32.40, base $36.78, upside $44.00; internal checks PASS |

## 2. Enterprise-to-Equity Bridge Test

I tested the bridge separately from my Walmart model. I started with $1,000 million in enterprise value, added $100 million in cash, and subtracted $250 million in debt and $50 million in finance leases. This gave me $800 million in equity value. Dividing by 100 million shares gave me $8.00 per share, which matched the expected answer.

This confirmed that the bridge formula worked in the separate test. It did not confirm that every cash, debt, lease, or share-count input used in my Walmart valuation was correct.

## 3. Changed-Input Test

For this test, I recorded a prediction before running the code. I expected the valuation to decrease if revenue growth decreased. I then reduced the five annual revenue-growth assumptions by one percentage point in my V2 model, without changing the other independent inputs. The result decreased from $35.674421 to $30.667082 per share.

This test showed that the model reacted in the expected direction and that the changed inputs were isolated. I completed this test using V2, so the $35.67 baseline is different from the final V3 base-case value of $36.78. The original locked record and test log are preserved in the repository.

## 4. Cold-Run and Reproducibility Results

On October 12, I ran `python3 -B walmart_project1_cold_run.py`. The script ran seven Python subprocesses, including the V3 financial model, DCF, scenarios, reverse DCF, comparable valuation, and two validation tests. Each process exited successfully. The log also showed matching before-and-after file hashes for 23 protected files.

I can use the same command again to check the model calculations. These results are helpful because someone reviewing my GitHub repository can repeat the tests. However, a successful run does not mean that every source value or forecast assumption has been independently verified.

## 5. Source Checks and Remaining Limitations

I also reviewed the financial inputs and definitions used in the model. Some reported balances matched the FY2026 filing, but the source review identified items that still needed attention, including how some receivables, supplier-finance obligations, and other working-capital accounts were classified.

My proposed September 23 valuation also uses July 31 balance-sheet amounts and an August 26 basic share count. I still need a consistent diluted share count and a more complete enterprise-to-equity review. The 7.00% WACC and 2.50% terminal growth assumption remain provisional, and around 82% of the base-case enterprise value comes from terminal value.

The upside case also includes approximately $9.022 billion of working-capital release in FY2027 without a separate operating plan supporting that improvement. These are reasons I would continue reviewing the model before treating the valuation as final.

## 6. How I Used AI

I used ChatGPT and Codex to help organize financial research, develop and review Python code, create tests, and draft parts of my supporting documentation. AI also helped with explaining results and preparing written materials for the project.

I ran the recorded tests and reviewed their results, but the test scripts and documentation were also developed with AI assistance. For the changed-input test, I recorded the prediction before running the test; AI helped refine the wording of the prediction beforehand. I have kept the locked record unchanged and documented this distinction in my AI-use record.

The final interpretation and investment recommendation are my responsibility. I kept my Watch–Defer recommendation because my modeled values were below the reported September 23 market price, while several assumptions still needed more verification.

## 7. What the Tests Showed Me

One of my biggest takeaways was that a model can run successfully without proving that every assumption is right. The bridge test, changed-input test, and cold run helped me check my calculations, but I still need to understand where the financial inputs come from and whether the assumptions make sense. That is why I kept the investment recommendation cautious.

---

## Locked Changed-Input Record | Supporting Evidence

*This is a post-test summary. The original prediction and GitHub commit remain unchanged.*

### Prediction and Input Change

Recorded prediction: October 12, 2026, 3:36 PM EDT; uploaded at about 3:39 PM; test execution reported at about 3:50 PM. The test used the V2 model.

The test decreased FY2027–FY2031 revenue-growth assumptions from **4.3%, 4.2%, 4.0%, 3.8%, 3.5%** to **3.3%, 3.2%, 3.0%, 2.8%, 2.5%**. The expected direction was a decrease in estimated share value, supporting Watch–Defer.

### Observed Results

| Metric | Original V2 | Changed V2 |
|---|---:|---:|
| Value per share | $35.674421 | $30.667082 |
| Change in value | — | −$5.007339 (about −14.04%) |
| Model checks | PASS | PASS |

The modeled FCFF declined in each forecast year. The result agreed with the predicted direction and did not trigger a reported accounting or financing failure.

### Evidence and Reproduction

The original prediction commit is [GitHub commit 3314c717](https://github.com/olianaozbaki-ctrl/WMT-Ticker---Research/commit/3314c717bd983030ec2011fa99e60c406cd74e56). The repository contains `Walmart_Project1_Locked_Changed_Input_Record.md`, `walmart_project1_revenue_growth_changed_input_test.py`, and `Walmart_Project1_Revenue_Growth_Changed_Input_Test.log`. The recorded cold-run command was `python3 -B walmart_project1_cold_run.py`. I have not independently verified which standalone command was used for the original 3:50 PM test; no historical command is claimed here.

### AI Assistance and Limitation

ChatGPT helped refine the wording of the pre-run prediction. This means the original record’s “AI-off” heading should not be taken as proof that no AI assisted with its wording. The prediction was recorded before the reported execution, but I am distinguishing timing from authorship rather than changing the original record. The test checks model responsiveness under its assumptions, not whether Walmart’s share value is accurate.
