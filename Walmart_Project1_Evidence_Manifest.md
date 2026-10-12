# Walmart Project 1 — Evidence Manifest

**Inventory checked:** project folder contents as listed at preparation time, October 12, 2026.  
**Purpose:** identify actual local evidence and its role, while separating stored calculations from primary-source verification. “Present” means a file was found in the folder; it does not mean submitted, published, source-verified, or approved.

## Core model and DCF

| Artifact | Status | Role / evidence boundary |
|---|---|---|
| [walmart_project1_proforma_v3.py](walmart_project1_proforma_v3.py) | Present | V3 five-year three-statement model. Internal articulation checks run; assumptions not independently validated. |
| [project1_fcff_v3.py](project1_fcff_v3.py) | Present | V3 FCFF and DCF layer; uses provisional WACC, terminal growth, bridge and denominator. |
| [Walmart_Project1_Model_V3_Changes.md](Walmart_Project1_Model_V3_Changes.md) | Present | V2-to-V3 change log and historical V2 comparison. |
| [Walmart_Project1_Operating_Base_Reconciliation.md](Walmart_Project1_Operating_Base_Reconciliation.md) | Present | FY2026 model opening-line reconciliation and unresolved differences. |
| [Walmart_Project1_Independent_Source_Check.md](Walmart_Project1_Independent_Source_Check.md) | Present | Source/definition findings; includes unresolved issues, not a full assurance opinion. |
| [Walmart_Project1_Model_Correction_Plan.md](Walmart_Project1_Model_Correction_Plan.md) | Present | Prioritized corrections. |
| [Walmart_Project1_Normalization_Review.md](Walmart_Project1_Normalization_Review.md) | Present | Normalization issues and initial model limitations. |
| [Walmart_Project1_Model_V2_Changes.md](Walmart_Project1_Model_V2_Changes.md) | Present | Earlier V2 change documentation. |
| [walmart_project1_proforma_v2.py](walmart_project1_proforma_v2.py), [project1_fcff_v2.py](project1_fcff_v2.py) | Present | Historical V2 models; retain as prior versions. |
| [walmart_project1_proforma.py](walmart_project1_proforma.py), [project1_fcff.py](project1_fcff.py) | Present | Earlier model files; not the current V3 engines. |

## WACC and enterprise-to-equity bridge

| Artifact | Status | Role / evidence boundary |
|---|---|---|
| [Walmart_Project1_WACC_Evidence.md](Walmart_Project1_WACC_Evidence.md) | Present | WACC input evidence, dates, assumptions and unresolved items; final rate is not selected. |
| [Walmart_Project1_Final_Valuation_Assumptions.md](Walmart_Project1_Final_Valuation_Assumptions.md) | Present | Current model values and recommendation/limitations for major valuation inputs. |
| [Walmart_Project1_Equity_Bridge_Review.md](Walmart_Project1_Equity_Bridge_Review.md) | Present | Filing fact vs assumption treatment of cash, debt, leases, NCI, investments, and shares. |
| [walmart_project1_equity_bridge_validation.py](walmart_project1_equity_bridge_validation.py) | Present | Independent arithmetic check; synthetic known answer plus supplied V2 figures. Does not import the Walmart model. |
| [Walmart_Project1_Equity_Bridge_Validation.md](Walmart_Project1_Equity_Bridge_Validation.md) | Present | Bridge test documentation/output. Arithmetic validation is not source validation. |
| [Walmart_Project1_WACC_Sensitivity.md](Walmart_Project1_WACC_Sensitivity.md) | Present | Earlier WACC sensitivity output. |
| [walmart_project1_wacc.py](walmart_project1_wacc.py), [walmart_project1_wacc_scenarios.py](walmart_project1_wacc_scenarios.py) | Present | WACC calculation and scenario scripts; underlying selections remain provisional. |

## Scenarios, reverse DCF, and comparable valuation

| Artifact | Status | Role / evidence boundary |
|---|---|---|
| [walmart_project1_v3_final_scenarios.py](walmart_project1_v3_final_scenarios.py) | Present | Runs causal Downside/Base/Upside scenarios through V3. |
| [Walmart_Project1_Final_Scenarios_and_Valuation_Range.md](Walmart_Project1_Final_Scenarios_and_Valuation_Range.md) | Present | Scenario drivers, annual outputs, controls and conditional range. |
| [walmart_project1_reverse_dcf_v3.py](walmart_project1_reverse_dcf_v3.py) | Present | Solves independent operating drivers to reproduce stored September 23 price input. |
| [Walmart_Project1_Reverse_DCF_Evidence.md](Walmart_Project1_Reverse_DCF_Evidence.md) | Present | Reverse-DCF values and limitations; equality is a model fit, not expectation verification. |
| [walmart_project1_comparables_v3.py](walmart_project1_comparables_v3.py) | Present | Target/Costco multiple calculations using stored dated inputs. |
| [Walmart_Project1_Comparable_Valuation_Triangulation.md](Walmart_Project1_Comparable_Valuation_Triangulation.md) | Present | Peer selection, definitions, calculations and comparability limitations. |
| [walmart_project1_v2_scenarios.py](walmart_project1_v2_scenarios.py), [Walmart_Project1_V2_Scenarios.md](Walmart_Project1_V2_Scenarios.md) | Present | Earlier V2 scenarios including severe downside failure record. |

## Independent tests, locked prediction, and cold-run evidence

| Artifact | Status | Role / evidence boundary |
|---|---|---|
| [Walmart_Project1_Locked_Changed_Input_Record.md](Walmart_Project1_Locked_Changed_Input_Record.md) | Present | Human-authored pre-run changed-input prediction record. Preserve unchanged. Its existence in the folder does not itself prove Brightspace timing or submission. |
| [walmart_project1_revenue_growth_changed_input_test.py](walmart_project1_revenue_growth_changed_input_test.py) | Present | V2 test changes only revenue growth by −1 percentage point/year and runs both cases. |
| [Walmart_Project1_Revenue_Growth_Changed_Input_Test.log](Walmart_Project1_Revenue_Growth_Changed_Input_Test.log) | Present | Separate changed-input run output. |
| [walmart_project1_cold_run.py](walmart_project1_cold_run.py) | Present | Reproduction harness; launches scripts in separate Python processes. |
| [Walmart_Project1_Cold_Run.log](Walmart_Project1_Cold_Run.log) | Present | Actual recorded stdout, process codes, Python version, and protected-file hashes. |
| [Walmart_Project1_Reproducibility_Report.md](Walmart_Project1_Reproducibility_Report.md) | Present | Summarizes PASS/NOT RUN checks and limitations. |

## Decision memo and research evolution

| Artifact | Status | Role / evidence boundary |
|---|---|---|
| [Walmart_Project1_Edition_B_Investment_Memo.md](Walmart_Project1_Edition_B_Investment_Memo.md) | Present | New committee memo draft; Watch–Defer is provisional. It still needs final A-to-B comparison, named AI-use-record reference, and PDF packaging per course submission architecture. |
| [Walmart_Project_1_Edition_A.md](Walmart_Project_1_Edition_A.md) | Present | Original September 1, 2026 baseline in Markdown. No local submission receipt or PDF was found. Preserve unchanged. |
| [Walmart_Project_1_Edition_B.md](Walmart_Project_1_Edition_B.md) | Present | Separate earlier Edition B artifact; preserve, do not treat as the new named memo. |
| [Walmart_Week_1_Lab_Checkout.md](Walmart_Week_1_Lab_Checkout.md) | Present | Lab checkout includes a receipt placeholder; not evidence of the Project 1 Edition A Brightspace submission. |
| [README_Project1_FCFF.md](README_Project1_FCFF.md) | Present | Older working-draft README with earlier results; retain as history, but use the new V3 README for current repository presentation. |

## Primary and external sources referenced by local evidence

The following are source URLs recorded in the local reports; source pages were **not** re-fetched by the cold run.

| Source | Relevant date / use |
|---|---|
| [Walmart FY2026 Form 10-K (SEC)](https://www.sec.gov/Archives/edgar/data/104169/000010416926000055/wmt-20260131.htm) | Fiscal year ended Jan. 31, 2026; filed Mar. 13, 2026. Primary filing facts. |
| [Walmart FY2027 Q2 Form 10-Q (SEC)](https://www.sec.gov/Archives/edgar/data/104169/000010416926000154/wmt-20260731.htm) | Period ended Jul. 31, 2026; filed Aug. 28, 2026. Latest quarterly filing used by peer/model evidence. |
| [Target FY2026 Form 10-K (SEC)](https://www.sec.gov/Archives/edgar/data/27419/000002741926000016/tgt-20260131.htm) and [Target FY2027 Q2 Form 10-Q (SEC)](https://www.sec.gov/Archives/edgar/data/27419/000002741926000042/tgt-20260801.htm) | Target peer filings; fiscal year ended Jan. 31 and quarter ended Aug. 1, 2026. |
| [Costco FY2025 Form 10-K (SEC)](https://www.sec.gov/Archives/edgar/data/909832/000090983225000101/cost-20250831.htm) and [Costco FY2026 Q3 Form 10-Q (SEC)](https://www.sec.gov/Archives/edgar/data/909832/000090983226000051/cost-20260510.htm) | Costco peer filings; latest pre-valuation-date quarter ended May 10, 2026. |
| [WMT historical prices](https://stockanalysis.com/stocks/wmt/history/), [TGT](https://stockanalysis.com/stocks/tgt/history/), [COST](https://stockanalysis.com/stocks/cost/history/) | Secondary historical market-price pages used for Sep. 23, 2026 close inputs. |
| [U.S. Treasury daily yield curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202609&type=daily_treasury_yield_curve) | Daily risk-free observations used in the WACC discussion. |
| [Kroll September 2026 ERP update](https://edge.sitecorecloud.io/krollllc17bf0-kroll6fee-proda464-0e9b/media/cost-of-capital/kroll-cost-of-capital-recommendations-updated-to-use-spot-risk-free-rates-september-2026.pdf) | Published Sep. 10, effective Sep. 2, 2026; ERP methodology discussed in WACC evidence. |
| [ICE BofA AA yield series (FRED)](https://fred.stlouisfed.org/series/BAMLC0A2CAAEY) | Broad market yield proxy used as a limitation-marked debt-cost reference. |

## Missing or unconfirmed submission evidence

No local video files, video transcripts, unified AI-use record, final PDF package, or Brightspace receipt/manifest were found in the project folder inventory. No course rubric file was found locally. The public course [submission architecture](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/PROJECT-SUBMISSION-ARCHITECTURE.md) describes the required evidence bundle and points to Brightspace as authoritative for the assignment page, dates, points, and upload-specific requirements. It references a separate `MAJOR-PROJECT-ANALYTIC-RUBRIC.md`, but that detailed rubric was not available in the inspected project folder or verified in the public repo during this review. Confirm it in Brightspace. No student Git remote/repository was configured in this workspace, so repository publication/access is unverified.
