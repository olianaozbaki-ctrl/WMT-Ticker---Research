# FIN 43900 Project 2 — Complete Video Recording Scripts

These scripts are written for a clear, natural speaking pace. Practice once with a timer and pause only long enough for the cited screen evidence to be readable. The directions labeled **Show** are not spoken.

## Video 1 — System Evolution and Checked AI Output

**Target length:** about 2:40–2:55. **Maximum:** 3:00.

### 0:00–0:15 — Required opening

**Show:** Camera visible. Start with `docs/decision-memo.md` open at the title and recommendation.

**Say:**

“I used OpenAI Codex for development and documentation, and Google Gemini for an independent validation response. I checked their outputs, and I own the analysis and investment decision. This is an educational project, not investment advice.”

### 0:15–0:42 — Current decision and corrected boundary

**Show:** Highlight the HOLD recommendation, then scroll to “Evidence as of October 5, 2026.”

**Say:**

“My final recommendation is to hold funded deployment. Meridian should not adopt the process, allocate capital, rebalance, authorize a funded pilot, or approve an allocation range yet. The decision date is October fifth. Market data stop on September thirtieth, and the CPI input comes from the August release that was available on September eleventh.”

### 0:42–1:13 — Consequential system correction

**Show:** Open `docs/validation-and-ai-use.md` at “Corrected point-in-time CPI and decision-date market inputs.” Highlight the look-ahead correction and corrected portfolio bullet.

**Say:**

“An earlier run used September CPI, but that number was released on October fourteenth, after the decision date. I treated that as look-ahead bias and rejected the run. The corrected analysis uses August CPI, excludes October prices, and produces a 48 percent BIL and 52 percent VT portfolio. I preserved both the error and the correction in the validation record instead of hiding the failed result.”

### 1:13–2:05 — Checked Gemini output

**Show:** Open `docs/gemini-independent-validation.md` at the statement that a 1% grid step is about 73.9 basis points. Then open the matching row in `docs/gemini-validation-reconciliation.md`.

**Say:**

“For my checked AI output, Gemini said that a one-percent shift between BIL and VT changes expected return by about 73.9 basis points. I recalculated it. The return difference is 11.050235 percent minus 3.657409 percent. Multiplying that difference by a one-percent weight change gives 0.0739 percentage points, or about 7.39 basis points. Gemini’s figure was off by a factor of ten. I corrected that claim, while accepting the portfolio calculations Gemini independently reproduced. This shows why I treated the external response as evidence to test, not as an answer to copy.”

### 2:05–2:42 — Effect on judgment

**Show:** Return to the memo. Highlight the 5.51 basis-point margin and the 48% versus 80% BIL window result.

**Say:**

“These checks strengthened the HOLD decision. The modeled after-cost return exceeds the hurdle by only 5.51 basis points. Changing the estimation window moves BIL from 48 percent to 80 percent, a 32 percentage-point shift. That instability means the stress envelope is diagnostic only. It is not an allocation range that a committee should authorize.”

### 2:42–2:55 — Close

**Show:** Highlight the memo’s mandate-status rows for S6 through S9.

**Say:**

“Actual holdings, trading costs, position-sized liquidity, issuer treatment, and the S9 loss policy are still unresolved. Until those gates are documented, funded deployment remains on hold.”

## Video 2 — Technical Codebase and Reproducibility Walkthrough

**Target length:** about 4:20–4:45. **Maximum:** 5:00.

### 0:00–0:15 — Required opening

**Show:** Camera visible with the repository open.

**Say:**

“I used OpenAI Codex for development and documentation, and Google Gemini for independent validation. I tested their contributions, and I own the code, analysis, and decision. This is an educational project, not investment advice.”

### 0:15–0:43 — Reproduction path

**Show:** Open `README.md` at “Run from a clean checkout.” Slowly highlight the test, generator, and Streamlit commands.

**Say:**

“A clean user installs the pinned requirements and the local package, runs the full test suite, generates the reports, and then starts Streamlit. The generator writes the Phase 2 JSON and Markdown plus the Phase 4A decision-support JSON and Markdown. The Streamlit command launches the interface; it does not silently regenerate those files.”

### 0:43–1:20 — Inputs and point-in-time controls

**Show:** Open `data/market_data_provenance.json`, then `data/cpi_pit_2026-10-05.csv`, then `data/dgs10_pit.csv`.

**Say:**

“The data layer records source, retrieval date, units, transformations, and missingness. The key control is the difference between an observation date and the date the observation became available. For the October fifth decision, ETF returns stop at September thirtieth. August CPI was released September eleventh, and the October second ten-year Treasury yield was available October fifth. The preserved October thirtieth prices are excluded because they were not available at the decision boundary.”

### 1:20–2:15 — Financial calculations and optimizer

**Show:** Open `src/project2_engine/calculations.py`. Point to expected return, portfolio variance or volatility, turnover, and transaction cost. Then open `src/project2_engine/optimizer.py` at the grid search and infeasible return.

**Say:**

“The calculation layer uses weighted annual arithmetic return, covariance-based annual volatility, one-way turnover equal to one-half the sum of absolute trades, and basis-point transaction costs. The optimizer searches every long-only portfolio on a one-percent grid. Weights must sum to one, BIL must meet the reserve floor, and the illustrative after-cost return must meet the hurdle. If the supplied constraints cannot all be satisfied, the optimizer returns an explicit infeasible stop. It never relaxes a rule to force an answer.”

### 2:15–2:48 — Mandate, stress, and decision logic

**Show:** Open `src/project2_engine/mandate.py` at the rule verdict logic, `src/project2_engine/stress.py` at the scenario construction, and `src/project2_engine/decision_support.py` at approval gates and reversal conditions.

**Say:**

“The mandate checker separates PASS, FAIL, NOT TESTABLE, and UNRESOLVED. Missing evidence never becomes a pass. The stress engine changes returns, estimation windows, costs, constraints, volatility, and correlations. Its correlation stress uses a positive-semidefinite convex blend so the covariance matrix remains valid. Decision support then combines model results with evidence gates, monitoring triggers, and reversal conditions.”

### 2:48–3:48 — Validation demonstration

**Show:** In a terminal, run `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`. While it runs, open `tests/test_data.py` at the CPI availability test and `tests/test_stress.py` at covariance validation. Finish on the terminal summary showing 60 tests passed.

**Say:**

“I am running all discovered tests. The data tests reject a CPI observation or vintage that was unavailable by the decision date and exclude future market prices. The stress tests require the correlation-stressed covariance to remain valid and deliberately confirm that a non-positive-semidefinite matrix is rejected. The full suite contains 60 tests, and all 60 pass. The Altair jsonschema messages are deprecation warnings, not failures.”

### 3:48–4:16 — Locked changed-input evidence

**Show:** Open `docs/locked-changed-input-record.md`, then the baseline and changed-input `SHA256SUMS` files under `outputs/locked-changed-input-test-1fd3c8b/`.

**Say:**

“The locked test increased the real-return spread from four to five percent after the prediction was committed. The portfolio shifted from 48 percent BIL and 52 percent VT to 35 percent BIL and 65 percent VT, but the decision stayed HOLD. I am showing the preserved checksums rather than rerunning or changing the locked evidence.”

### 4:16–4:43 — Output trace and failure mode

**Show:** Open `outputs/phase2_results.md` at the optimized portfolio, then `outputs/phase4a_decision_support.md` at the disposition and approval gates.

**Say:**

“The generated output reports 48 percent BIL, 52 percent VT, 7.4517 percent illustrative net expected return, and 7.8242 percent volatility. The decision report returns HOLD because full mandate evidence is incomplete. A concrete failure mode is missing actual holdings: without them, actual turnover and recurring costs cannot be tested. The system reports that limitation instead of claiming compliance.”

## Video 3 — Investment-Committee Presentation

**Target length:** about 4:15–4:40. **Maximum:** 5:00.

### 0:00–0:18 — Live application and required opening

**Show:** Begin on the running Streamlit app at the title and “Mandate and candidate decision” section. Camera visible.

**Say:**

“I used OpenAI Codex for development and Google Gemini for independent validation. I checked their outputs, and I own the analysis and investment decision. This is an educational project, not investment advice.”

### 0:18–0:45 — Lead with the recommendation

**Show:** Keep the model-generated HOLD disposition and warning banner visible.

**Say:**

“My recommendation is HOLD funded deployment. Meridian should not adopt this process, allocate capital, rebalance, authorize a funded pilot, or approve an allocation range on the current evidence. A paper-only rehearsal may be considered only if the committee separately defines its scope.”

### 0:45–1:28 — Portfolio comparison

**Show:** Scroll through “Decision-date data and provenance” and “Portfolio comparison.” Keep the three rows and charts visible.

**Say:**

“The decision date is October fifth, 2026, using market data through September thirtieth and August CPI available September eleventh. Equal weight estimates a 3.0128 percent return and 7.5482 percent volatility. The 60/40 reference estimates 6.2591 percent return and 12.3335 percent volatility. The constrained model selects 48 percent BIL and 52 percent VT, with 7.5017 percent gross expected return, 7.4517 percent after one illustrative transition cost, and 7.8242 percent volatility.”

### 1:28–2:05 — What the point estimate does not prove

**Show:** Scroll to “Rule-by-rule mandate assessment” and “Verified full mandate compliance: NO.”

**Say:**

“The modeled net return clears the 7.3965 percent arithmetic CPI-plus-four proxy by only 5.51 basis points. It does not prove after-cost performance over rolling five-year periods. The cost is based on hypothetical equal-weight holdings, not Meridian’s actual portfolio. Model feasibility is therefore not full mandate compliance.”

### 2:05–2:48 — Sensitivity and range decision

**Show:** Scroll to “Stress-test scenario analysis,” the full-window versus 36-month comparison, and the model-only envelope.

**Say:**

“The strongest sensitivity is the estimation window. The full window selects 48 percent BIL, while the 36-month window selects 80 percent BIL. Across feasible modeled stresses, BIL ranges from 21 to 80 percent and VT from 20 to 79 percent. I am not recommending that as an allocation band. It is a diagnostic envelope, and the 32 percentage-point window shift shows that it is not stable enough for authorization.”

### 2:48–3:35 — Mandate gaps and stop condition

**Show:** Select the constrained portfolio in the rule assessment, then show “Modeled feasibility and evidence status” and “Hypothetical turnover-cap stop condition.”

**Say:**

“The unresolved gates are material. Actual holdings are missing, so S7 turnover is not testable. S6 requires a CIO decision on issuer exemptions and ETF look-through. S8 lacks a position-sized five-day liquidation and settlement study. S9 has no approved loss measurement or breach response. Under a hypothetical equal-weight start, the 25 percent turnover cap is infeasible, but that is a sensitivity stop, not a verdict on Meridian’s unknown holdings.”

### 3:35–4:12 — Monitoring and reversal conditions

**Show:** Scroll to “Investment decision framework,” then show approval gates, monitoring triggers, and reversal conditions.

**Say:**

“The process should stop if required data were unavailable at the decision boundary, covariance validation fails, optimization is infeasible, or a mandatory rule cannot be evaluated. HOLD could move to a conditional pilot only after actual holdings and costs are supplied, issuer and liquidity evidence are verified, S9 and the optimization objective are approved, and the committee defines pilot size, duration, monitoring cadence, and abort conditions. A verified hard breach with no remedy would change the decision to REJECT.”

### 4:12–4:37 — Committee ask and close

**Show:** Keep the decision framework and requested committee decisions visible.

**Say:**

“I am asking the committee to accept HOLD, decline funded deployment and an allocation range, and direct staff to obtain the missing holdings, cost, liquidity, issuer, CPI-convention, and S9 evidence. These are historical model estimates, not promised returns or security-specific trade recommendations.”
