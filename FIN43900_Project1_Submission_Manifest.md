# FIN 43900 — Project 1 Submission Manifest

**Company:** Walmart Inc. (WMT)  
**Analyst role / decision user:** Equity research analyst advising a buy-side investment committee with no current position in Walmart.  
**Committee decision:** **Watch–Defer** — do not initiate a position at the reported September 23, 2026 closing price of $110.53, pending verification of the valuation assumptions and source inputs.  
**Valuation reference date:** September 23, 2026 (proposed).  
**GitHub repository:** https://github.com/olianaozbaki-ctrl/WMT-Ticker---Research  
**Repository visibility and access:** Public; no private-repository invitation is required. Links should remain accessible through grading and the appeal window.  
**Reproduction:** Run `python3 -B walmart_project1_cold_run.py` from the repository's project directory in a suitable Python environment.  
**Optional deployed application:** None; this project is a locally runnable Python financial model with documented output.

## Video links and durations

| Video | Title | Host / stable URL | Recorded duration | Course maximum |
|---|---|---|---|---|
| Video 1 | Research Evolution and AI-Output Check | YouTube (Unlisted) — https://youtu.be/dQL89fBIttM | 2:52 | 3:00 |
| Video 2 | Detailed Codebase Walkthrough | YouTube (Unlisted) — https://youtu.be/JHpVHoyCizE | 4:35 | 5:00 |
| Video 3 | Investment Committee Presentation | YouTube (Unlisted) — https://youtu.be/8zDtEbb0n_c | 4:26 | 5:00 |

The video links are submitted in video-number order and were confirmed accessible by the student. Each video's corrected transcript is separately provided as a plain-text attachment and in the repository.

## Required evidence index — 11 entries

| # | Required evidence | Artifact and location / timestamp |
|---|---|---|
| 1 | **Edition A checkpoint** | [Research Evolution PDF](docs/FIN%2043900%20Project%201%20Research%20Evolution.pdf), pp. 4–5, includes retained Edition A text. **The contemporaneous Brightspace Edition A receipt has not been independently verified; the retained repository copy must not be represented as proof of the original checkpoint.** |
| 2 | **Edition B research evolution** | [Research Evolution PDF](docs/FIN%2043900%20Project%201%20Research%20Evolution.pdf), pp. 1–3, with Edition B change/evidence table and conclusion on p. 6. |
| 3 | **GitHub codebase and reproducible visible output** | [Repository](https://github.com/olianaozbaki-ctrl/WMT-Ticker---Research), root `README.md`, `walmart_project1_proforma_v3.py`, `project1_fcff_v3.py`, `walmart_project1_v3_final_scenarios.py`, `walmart_project1_cold_run.py`; `Walmart_Project1_Final_Scenarios_and_Valuation_Range.md`, `Walmart_Project1_Reproducibility_Report.md`, and `Walmart_Project1_Cold_Run.log` document displayed results and checks. |
| 4 | **Video 1 — research evolution and AI-output check** | https://youtu.be/dQL89fBIttM — Edition A and original decision approximately **0:10–0:40**; Edition B and valuation approximately **0:40–1:10**; AI assistance and the V2 model/check approximately **1:20–2:25**; Watch–Defer conclusion approximately **2:35–2:50**. |
| 5 | **Video 1 corrected transcript** | [docs/transcript-video-1.txt](docs/transcript-video-1.txt), also attached to Brightspace as `transcript-video-1.txt`. |
| 6 | **Video 2 — codebase, reproduction and validation** | https://youtu.be/JHpVHoyCizE — GitHub README/repository approximately **0:15–0:40**; forecast/DCF/scenario code approximately **0:40–2:30**; live terminal running `python3 -B walmart_project1_cold_run.py` approximately **2:40–3:10**; known-answer bridge-validation evidence approximately **3:20–3:55**; reproducibility limitations approximately **4:00–4:30**. |
| 7 | **Video 2 corrected transcript** | [docs/transcript-video-2.txt](docs/transcript-video-2.txt), also attached to Brightspace as `transcript-video-2.txt`. |
| 8 | **Investment committee decision memo** | [Decision Memo PDF](docs/FIN%2043900%20Project%201%20Decision%20Memo.pdf), pp. 1–7. Recommendation p. 1; financial forecasts and downside/base/upside valuations p. 2; equity bridge p. 3; WACC, reverse DCF p. 4; peer evidence and risks p. 5; monitoring and reversal conditions pp. 5–6. |
| 9 | **Video 3 — investment committee defense with live product demonstration** | https://youtu.be/8zDtEbb0n_c — Watch–Defer decision and valuation approximately **0:10–1:00**; scenario assumptions, live run and output approximately **1:15–2:35**; reverse DCF approximately **2:40–3:10**; uncertainty, triggers and committee decision approximately **3:15–4:20**. |
| 10 | **Video 3 corrected transcript** | [docs/transcript-video-3.txt](docs/transcript-video-3.txt), also attached to Brightspace as `transcript-video-3.txt`. |
| 11 | **Frozen validation and AI-use evidence** | [Validation and AI-Use PDF](docs/FIN%2043900%20Project%201%20Validation%20and%20AI%20Use.pdf), three pages, and [docs/validation-and-ai-use.md](docs/validation-and-ai-use.md) working text, supported by `Walmart_Project1_AI_Use_Record.md`, independent tests and recorded logs. Includes the known-answer bridge, changed-input test, reproducibility results, and material limitations. AI assistance in the locked prediction's wording is disclosed; no claim is made that the wording was wholly AI-off. |

**Optional row 12 — Deployed output:** Not applicable. The product is the reproducible Python analysis and its stored reports, not a separately hosted application.

## Investment result and evidence boundaries

- **V3 model outputs:** $32.40 downside; $36.78 base; $44.00 upside, per August 26, 2026 basic share, under a provisional 7.00% WACC and 2.50% terminal growth rate.
- **Market comparator:** Reported September 23, 2026 Walmart closing price of $110.53. The broader $31–$49 zone is an illustrative, conditional reference, not a fully verified fair-value interval.
- **V2 changed-input test:** One percentage point less annual revenue growth in FY2027–FY2031 lowered modeled value from $35.674421 to $30.667082 per share. This is a V2 test and is not the V3 base value of $36.78.
- **Known-answer bridge:** $1,000 million enterprise value + $100 million cash − $250 million debt − $50 million finance leases = $800 million equity value, or $8.00 per 100 million shares.
- **Reproducibility:** The recorded cold run completed seven Python subprocesses and reported 23 protected files unchanged. Passing internal checks does not independently verify financial inputs or the economic validity of forecasts.
- **Open limitations:** WACC calibration, July 31 balance-sheet figures compared with a September 23 valuation date, August 26 basic rather than point-in-time diluted shares, lease/debt/cash bridge treatment, and unsupported $9.022 billion FY2027 working-capital release in the upside case.

## Brightspace final attachment index

Attach the following **seven separate files**, rather than the MP4 recordings:

1. `FIN43900_Project1_Submission_Manifest.md` (this manifest; adapt the filename if Brightspace requires a particular prefix).
2. `Research-Evolution.pdf` (same six-page content as the repository Research Evolution PDF).
3. `Decision-Memo.pdf` (same seven-page content as the repository Decision Memo PDF).
4. `Validation-and-AI-Use.pdf` (same three-page frozen content as the repository validation PDF and corresponding Markdown working record).
5. `transcript-video-1.txt`.
6. `transcript-video-2.txt`.
7. `transcript-video-3.txt`.

**Before final submission:** Verify that the linked files resolve at the stated GitHub paths and match the Brightspace copies. If the repository PDFs have been renamed, update the three PDF hyperlinks above to use the new names. Confirm actual Brightspace instructions regarding filename prefix, the original Edition A receipt, and access. Evidence timestamps are short navigation ranges to visible segments, not frame-exact boundaries.
