# Project 2 Video Recording Outlines

These are recording plans, not evidence that any video has been recorded. Replace every placeholder in the manifest only after recording, reviewing, uploading, and checking access.

Each video must open with two short statements: identify the AI tools used and state that the student owns the analysis and decision; then state that the project is educational and not investment advice. Use only model/version identifiers actually exposed by the interfaces.

## Video 1 — System evolution and checked AI output

**Maximum:** 3:00. **Purpose:** show how the system and the student's thinking changed and demonstrate one AI output that was independently checked. Do not turn this into a generic reflection.

### Recording sequence

1. **0:00–0:15 — Required opening statements**
   - Camera visible as required by the course.
   - State the AI-use/ownership announcement and educational disclaimer.
2. **0:15–0:45 — Show the current decision and what changed**
   - Open the top of `docs/decision-memo.md`.
   - Explain that the final process recommendation is HOLD funded deployment, not adoption or allocation.
   - State the corrected point-in-time boundary: October 5 decision date, September 30 market-data cutoff, and August CPI release available September 11.
3. **0:45–1:20 — Show one consequential system correction**
   - Open `docs/validation-and-ai-use.md` at “Corrected point-in-time CPI and decision-date market inputs.”
   - Explain that a prior September CPI input was released after the decision date and was rejected as look-ahead bias.
   - Show the corrected 48% BIL / 52% VT result and why the change is preserved in the audit trail.
4. **1:20–2:15 — Demonstrate one checked AI output**
   - Open `docs/gemini-independent-validation.md` at the grid-step statement, then `docs/gemini-validation-reconciliation.md` at the corresponding disposition.
   - Recompute: `0.01 × (0.11050235 − 0.03657409) ≈ 0.0007393`, or about 7.39 basis points.
   - Explain that Gemini's 73.9 bp statement was corrected by a factor of ten, while its reproduced portfolio arithmetic was accepted.
   - State clearly whether the AI output was accepted, qualified, corrected, or rejected.
5. **2:15–2:45 — Explain how judgment changed**
   - Show the 5.51 bp modeled hurdle margin and the 32 percentage-point BIL window shift in the memo or app.
   - Explain why those checks strengthen HOLD and prevent authorization of an allocation range.
6. **2:45–3:00 — Close**
   - State the remaining unknowns: actual holdings, transaction costs, liquidity, issuer treatment, and S9 policy.

### Evidence to capture in the final timestamp index

- AI/ownership and educational statements.
- System/thinking change.
- Exact AI output checked.
- Independent calculation and disposition.
- Effect on HOLD.

## Video 2 — Technical codebase and reproducibility walkthrough

**Maximum:** 5:00. **Purpose:** demonstrate technical ownership—architecture, data flow, financial logic, reproduction, validation, and a failure mode. Showing only the interface or reading the README is insufficient.

### Recording sequence

1. **0:00–0:15 — Required opening statements**
   - State the AI-use/ownership announcement and educational disclaimer.
2. **0:15–0:45 — Reproduction path**
   - Open `README.md` at “Run from a clean checkout.”
   - Explain the difference between the generator command and the Streamlit launch command.
   - Point to the four generated output paths.
3. **0:45–1:30 — Input and point-in-time flow**
   - Show `data/market_data_provenance.json`, `data/cpi_pit_2026-10-05.csv`, and `data/dgs10_pit.csv`.
   - Explain observation date versus availability date and why October 30 prices are excluded.
4. **1:30–2:30 — Financial engine**
   - Show `src/project2_engine/calculations.py` for expected return, covariance-based volatility, turnover, and cost.
   - Show `src/project2_engine/optimizer.py` for the exhaustive 1% long-only grid and explicit infeasible stop.
   - Show `src/project2_engine/mandate.py` for rule-level PASS/FAIL/NOT_TESTABLE/UNRESOLVED behavior.
5. **2:30–3:20 — Stress and decision flow**
   - Show `src/project2_engine/stress.py` for window, return, cost, constraint, volatility, and PSD-preserving correlation stresses.
   - Show `src/project2_engine/decision_support.py` for evidence gates, monitoring triggers, and reversal conditions.
6. **3:20–4:10 — Demonstrate validation**
   - Run `PYTHONPATH=src python -m unittest discover -s tests -p 'test*.py' -v`, or show the completed terminal result if recording time makes a live full run impractical.
   - Open one material test such as `tests/test_data.py` for the CPI decision boundary or `tests/test_stress.py` for covariance validation.
   - Do not rerun or alter the Locked Changed-Input artifacts; show their checksum evidence and explain the preserved before/after run.
7. **4:10–4:40 — Trace output**
   - Open `outputs/phase2_results.md` and `outputs/phase4a_decision_support.md`.
   - Trace 48% BIL / 52% VT and HOLD back to the engine rather than describing them as manually entered.
8. **4:40–5:00 — Failure mode and limitation**
   - Explain one concrete failure mode: missing actual holdings makes turnover and recurring cost untestable, or a post-decision CPI release must stop the run.
   - State that unknown evidence never becomes PASS.

### Evidence to capture in the final timestamp index

- Reproduction command and output paths.
- Data lineage and as-of filter.
- Core financial calculation/optimizer code.
- One test or preserved validation demonstration.
- One failure mode or unresolved risk.

## Video 3 — Buy-side investment-committee presentation

**Maximum:** 5:00. **Purpose:** defend the final investment-process recommendation. This video must open with the application running live and end with a clear committee ask.

### Recording sequence

1. **0:00–0:20 — Live app plus required statements**
   - Start on the running Streamlit application, not a static file.
   - State the AI-use/ownership announcement and educational disclaimer.
2. **0:20–0:50 — Lead with the decision**
   - Show the app's decision banner.
   - Say: HOLD funded deployment; do not adopt, allocate, rebalance, or authorize a funded pilot or allocation range on current evidence.
3. **0:50–1:35 — Mandate and portfolio comparison**
   - Show the mandate summary and three-portfolio comparison.
   - Give the key point estimate: 48% BIL / 52% VT, 7.5017% gross, 7.4517% illustrative after-cost expected return, and 7.8242% volatility.
   - Contrast equal weight and the 60/40 reference without calling the model portfolio fully compliant.
4. **1:35–2:25 — Strongest evidence and sensitivity**
   - Show the window comparison and stress envelope.
   - Explain the 48% to 80% BIL shift and the 5.51 bp modeled hurdle margin.
   - State that BIL 21–80% / VT 20–79% is diagnostic only, not an authorized range.
5. **2:25–3:25 — Mandate gaps and stop conditions**
   - Show rule verdicts/evidence gates.
   - Cover actual holdings and S7 turnover, S6 issuer interpretation/exposure, S8 position-sized liquidity, S9 loss-policy definition, and the rolling five-year S2 limitation.
   - Mention the hypothetical 25% turnover case as a sensitivity stop, not an actual Meridian verdict.
6. **3:25–4:15 — Monitoring and reversal conditions**
   - Show the monitoring-trigger section.
   - Explain what would preserve HOLD, cause REJECT, or permit reconsideration of a conditional pilot.
7. **4:15–4:50 — Committee ask**
   - Ask the committee to accept HOLD, decline funded deployment and an allocation range, and direct staff to obtain the missing evidence and policy rulings.
   - State the conditions required before reconsideration.
8. **4:50–5:00 — Close**
   - Reiterate that the output is historical decision support, not a promised return or security-specific trade recommendation.

### Evidence to capture in the final timestamp index

- Live app opening.
- Recommendation and non-authorized range.
- Key numbers and as-of date.
- Principal risks and failure conditions.
- Monitoring/reversal triggers.
- Explicit committee ask.
