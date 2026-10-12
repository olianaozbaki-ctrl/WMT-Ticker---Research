# Walmart Project 1 — Submission Checklist

**Inventory date:** October 12, 2026.  
**Scope:** folder artifacts and the public course submission architecture. This is not proof of Brightspace uploads, receipt timestamps, link access, or compliance with the student's specific Brightspace assignment page. Check that page before submission; the course identifies Brightspace as authoritative for dates, points and submission requirements.

Status key: **Present** = found locally; **Partial** = a draft or related evidence exists but does not yet satisfy the full item; **Missing / unverified** = no local evidence or not checkable from this folder.

## Research evolution and recommendation

- [x] **Edition A source file present:** `Walmart_Project_1_Edition_A.md`, with September 1, 2026 valuation date. Preserve unchanged.
- [ ] **Edition A checkpoint PDF and successful Brightspace receipt/attempt ID:** Missing/unverified. The local Edition A is Markdown; `Walmart_Week_1_Lab_Checkout.md` has a receipt placeholder, not a verified Project 1 Edition A receipt.
- [~] **Edition B / research-evolution brief:** `Walmart_Project1_Edition_B_Investment_Memo.md` exists as a draft. Add the required compact A-to-B change table (recommendation, data/source choice, assumption/model design, risks/limitations; what changed or did not, why, and evidence) and the closing “What changed from Edition A to Edition B, and why?” response. The memo is substantive but does not currently provide a clearly labeled comparison section.
- [~] **Committee decision memo:** Draft exists with provisional Watch–Defer, scenarios, range, evidence, risks, and triggers. Before finalization, add a named reference to the unified AI-use record and material checks; reconcile current date/bridge limitations as appropriate. No PDF export was found.
- [ ] **Research-Evolution.pdf containing unchanged Edition A and final Edition B (and any dated addendum if needed):** Missing.

## Code, README, output, and repository access

- [x] **Runnable model and analysis scripts:** V2/V3 models, scenario, reverse-DCF, comp, bridge-test, changed-input, and cold-run scripts are present. See [Evidence Manifest](Walmart_Project1_Evidence_Manifest.md).
- [x] **Current README draft:** `Walmart_Project1_README.md` covers decision/user, setup/run commands, file map, data sources, outputs and limitations.
- [x] **Visible executed output:** `Walmart_Project1_Cold_Run.log`, scenario/reverse/comp reports, and changed-input log are present. The cold-run log contains actual run output and process statuses.
- [~] **Dependency/environment file:** The scripts use Python standard library and local modules; no third-party dependencies were found/required for the recorded run. No `requirements.txt`, `pyproject.toml`, or explicit environment lock file was found. Add a minimal environment/version note or dependency file if required by Brightspace/course instructions.
- [ ] **GitHub repository URL and instructional-team access confirmation:** Missing/unverified. The inspected workspace is not a Git repository and has no configured remote. The course repository is not the student's project repository. Create/publish or configure the student's repository, then test grader access (including if private).
- [ ] **Repository structure required by the course package:** `docs/research-evolution.pdf`, `docs/decision-memo.pdf` (or decision deck), `docs/validation-and-ai-use.md`, and `docs/transcript-video-1.txt` through `docs/transcript-video-3.txt` were not found. Place equivalent final artifacts at required paths if using the course's prescribed package layout.

## Validation and AI-use evidence

- [x] **Locked Changed-Input Record:** `Walmart_Project1_Locked_Changed_Input_Record.md` is present; cold-run SHA-256 before/after matched. Retain it unchanged and confirm its timestamp/commit and Brightspace record meet course rules.
- [x] **Changed-input execution evidence:** `walmart_project1_revenue_growth_changed_input_test.py` and `Walmart_Project1_Revenue_Growth_Changed_Input_Test.log` are present. The cold run reports both V2 cases pass accounting/liquidity controls; changed case value $30.667082/share.
- [x] **Cold-run validation evidence:** `walmart_project1_cold_run.py`, `Walmart_Project1_Cold_Run.log`, and `Walmart_Project1_Reproducibility_Report.md` are present. Recorded suite passed arithmetic/model controls; source re-fetch, economic reasonableness, and valuation-date completeness are explicitly NOT RUN.
- [~] **Unified Validation-and-AI-Use record / named AI-tool disclosure:** Missing as a standalone local file. The locked record is not a substitute for the complete AI-use record. Create the working record with named tools and material use/checks, reconcile it to the memo and project artifacts, and include the frozen PDF required by Brightspace.
- [ ] **Validation-and-AI-Use.pdf frozen Brightspace copy:** Missing/unverified.
- [ ] **Validation-and-AI-Use working Markdown matching the PDF:** Missing/unverified.

## Three video evidence items and transcripts

The public course architecture specifies three separate, titled, accessible videos and three corrected plain-text transcripts. No video files, URLs, or transcript files were found locally.

- [ ] **Video 1 — research evolution and AI-output check:** Missing/unverified. Course architecture specifies maximum 3:00; show Edition A/B change, a consequential AI output, the check, and disposition.
- [ ] **Video 2 — codebase walkthrough:** Missing/unverified. Maximum 5:00; explain architecture/data flow/finance logic, reproduce output, demonstrate a high-risk validation and limitation.
- [ ] **Video 3 — investment committee presentation:** Missing/unverified. Maximum 5:00; lead with decision, valuation range, evidence, assumptions, risks/triggers, and committee ask. Project 1 architecture says live product demonstration is the main delivery.
- [ ] **Corrected plain-text transcripts:** Missing/unverified: `docs/transcript-video-1.txt`, `docs/transcript-video-2.txt`, `docs/transcript-video-3.txt`. Review financial terms, names, tickers, and numbers against recordings.
- [ ] **Video captions/access:** Missing/unverified. Confirm links are Unlisted/Public or approved Purdue-hosted equivalent (not Private), captions/transcripts are available, and links remain accessible through the grade-appeal window.
- [ ] **Timestamped evidence index:** Missing/unverified. Record required video moments, links/IDs, titles, duration, and timestamps in the final submission manifest.

## Brightspace final package

- [ ] **Check the actual Project 1 assignment page and detailed rubric in Brightspace.** No local rubric file was found. The course's public architecture points to `MAJOR-PROJECT-ANALYTIC-RUBRIC.md`, but that detailed rubric was not available in this inspected folder/public-repo check. Brightspace governs final deadlines, points, upload slots, naming rules, and exact requirements.
- [ ] **Final submission manifest:** Include student repository URL, three video URLs, optional deployed-output URL if any, timestamped video evidence index, and private-repository access confirmation if applicable.
- [ ] **Research-Evolution.pdf:** unchanged Edition A plus final Edition B (and dated addendum only if needed).
- [ ] **Decision-Memo.pdf or Decision-Deck.pdf:** final, concise committee artifact matching the recommendation and calculations.
- [ ] **Validation-and-AI-Use.pdf:** frozen record matching repository Markdown.
- [ ] **Three corrected transcript text files:** one per video.
- [ ] **Upload all required items to the correct Brightspace assignment and verify receipt.** Record receipt/attempt identifier and retain a copy; no final submission receipt is evidenced in this folder.

## Published rubric-evidence crosswalk

The public submission architecture names these six unchanged project criteria but points to a separate detailed rubric that was not available in the folder/repository review. This is an evidence-readiness crosswalk, not a grade prediction.

| Criterion named in course architecture | Current evidence status |
|---|---|
| Problem definition and decision usefulness | **Partial:** Edition A and an extensive provisional committee memo exist; final A-to-B change table, final PDFs, and Brightspace record are missing/unverified. |
| Data integrity and traceability | **Partial:** SEC/source evidence and limitations are documented, but valuation-date bridge/share/WACC issues remain and no final unified AI-use/validation record exists. |
| Financial soundness and judgment | **Partial:** three cases, reverse DCF, peers, bridge and risks are calculated; assumptions and several definitions remain provisional. |
| Technical execution and usability | **Partial:** reproducible Python harness and visible run output exist; no configured student GitHub repo/access confirmation was found. |
| Validation, sensitivity, and reproducibility | **Partial:** cold-run controls and changed-input test passed; external source verification and economic validation were NOT RUN. |
| Professional communication | **Partial:** README, manifest and memo drafts are present; videos, corrected transcripts, final PDFs and complete upload manifest are missing/unverified. |

## Before calling this package final

- [ ] Resolve or prominently retain the V3's provisional WACC, September 23 diluted share count, valuation-date cash/debt/finance-lease bridge, operating-lease/claim consistency, noncontrolling interests/nonoperating investments, and working-capital classifications.
- [ ] Keep the $31–$49 zone and $32.40/$36.78/$44.00 scenario outputs labeled conditional/diagnostic; do not call the model fully source-validated.
- [ ] Ensure every PDF, transcript, video claim, README result, and Brightspace attachment agrees with the final retained source record and execution log.
- [ ] Verify the GitHub repository and video links from a clean, grader-equivalent access context before submission.

## Source for submission architecture

The local workspace was searched for a rubric and submission instructions. The public [FIN 43900 major-project submission architecture](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/PROJECT-SUBMISSION-ARCHITECTURE.md) states the common project evidence package, video roles/durations, repository contents, and Brightspace attachment set. The public course [repository landing page](https://github.com/CinderZhang/FIN43900-Fall2026) says graded items, deadlines, and submissions are governed by Brightspace. The architecture itself identifies a separate detailed analytic rubric; confirm its current version on the Project 1 assignment page before relying on this checklist as exhaustive.
