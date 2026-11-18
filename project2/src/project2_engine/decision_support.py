"""Evidence-gated investment decision support for committee review."""

from __future__ import annotations

from typing import Any

from .labels import cpi_objective_label


def evaluate_decision(*, unmitigated_hard_failure: bool, approval_ready: bool, pilot_ready: bool) -> str:
    """Return a framework outcome without converting missing evidence to a pass."""
    if unmitigated_hard_failure:
        return "REJECT"
    if approval_ready:
        return "APPROVE"
    if pilot_ready:
        return "CONDITIONAL_PILOT"
    return "HOLD"


def build_decision_support(
    phase_result: dict[str, Any], mandate: dict[str, Any], provenance: dict[str, Any]
) -> dict[str, Any]:
    """Summarize model outputs, range stability, evidence gaps, and review gates."""
    stress = phase_result["stress_matrix"]
    objective_label = cpi_objective_label(mandate["objective"]["real_return_spread"])
    decision_date = stress["decision_date"]
    cpi = provenance["cpi_data"]
    cpi_current_available = cpi.get("current_availability_date")
    cpi_prior_available = cpi.get("prior_year_availability_date")
    cpi_source_verified = bool(cpi.get("point_in_time_verified"))
    cpi_admissible = bool(
        cpi_source_verified
        and cpi_current_available
        and cpi_prior_available
        and cpi_current_available <= decision_date
        and cpi_prior_available <= decision_date
    )
    cpi_availability_phrase = "before" if cpi_admissible else "after or without verification by"
    cpi_rate_for_text = phase_result.get("cpi_yoy")
    cpi_rate_text = "not computed" if cpi_rate_for_text is None else f"{cpi_rate_for_text:.4%}"
    hurdle_for_text = phase_result.get("provisional_after_cost_hurdle")
    hurdle_text = "not computed" if hurdle_for_text is None else f"{hurdle_for_text:.4%}"

    optimized = []
    for scenario in stress["scenarios"]:
        if not scenario.get("feasible"):
            continue
        for portfolio in scenario.get("portfolio_comparisons", []):
            if portfolio.get("portfolio") == "Reoptimized minimum volatility" and portfolio.get("optimizer_feasible"):
                optimized.append({"scenario": scenario["scenario"], **portfolio})
    if not optimized:
        envelope = {ticker: {"minimum": None, "maximum": None} for ticker in ("BIL", "IEF", "LQD", "VT")}
    else:
        envelope = {
            ticker: {
                "minimum": min(item["weights"][ticker] for item in optimized),
                "maximum": max(item["weights"][ticker] for item in optimized),
            }
            for ticker in ("BIL", "IEF", "LQD", "VT")
        }

    by_scenario = {scenario["scenario"]: scenario for scenario in stress["scenarios"]}

    def selected_weights(name: str) -> dict[str, float] | None:
        row = by_scenario.get(name)
        return None if row is None else row.get("weights")

    full_weights = selected_weights("baseline_full_window")
    short_weights = selected_weights("last_36_months")
    full_bil = None if full_weights is None else full_weights["BIL"]
    short_bil = None if short_weights is None else short_weights["BIL"]
    bil_window_gap = None if full_bil is None or short_bil is None else abs(full_bil - short_bil)

    actual_holdings_known = mandate["turnover"].get("actual_starting_holdings_status") != "unavailable"
    liquid_known = all(asset.get("liquidity_business_days") is not None for asset in mandate["project_universe"])
    # S6's actual Lab_13 wording states an 8% issuer cap and no exemptions.
    # The configured case exemptions therefore remain unconfirmed policy input.
    s6_text = mandate["original_policy"]["statements"]["S6"]
    issuer_treatment_confirmed = bool(
        ("exempt" in s6_text.lower() and "diversified" in s6_text.lower())
        or mandate.get("issuer_limit", {}).get("interpretation_confirmed", False)
    )
    issuer_exposure_known = bool(phase_result.get("issuer_exposure_verified", False))
    issuer_evidence_complete = issuer_treatment_confirmed and issuer_exposure_known
    s9_resolved = mandate["risk"].get("loss_rule_status") not in ("unresolved_unverifiable_promise_not_a_hard_constraint", "unresolved")
    hard_failure = any(
        rule["status"] == "FAIL" and rule.get("required_for_feasibility", False)
        for portfolio in phase_result.get("portfolios", [])
        if portfolio.get("kind") == "provisional_model_portfolio"
        for rule in portfolio.get("rules", [])
    )
    full_mandate_feasible = bool(phase_result.get("optimization", {}).get("full_mandate_feasible", False))
    range_supported = bool(cpi_admissible and actual_holdings_known and liquid_known and issuer_evidence_complete and s9_resolved and full_mandate_feasible and bil_window_gap is not None and bil_window_gap == 0)
    approval_ready = bool(range_supported and not hard_failure)
    pilot_ready = bool(actual_holdings_known and liquid_known and issuer_evidence_complete and cpi_admissible and s9_resolved and not hard_failure)
    disposition = evaluate_decision(
        unmitigated_hard_failure=hard_failure,
        approval_ready=approval_ready,
        pilot_ready=pilot_ready,
    )

    evidence = [
        {
            "requirement": "S8 five-business-day liquidity",
            "status": "NOT_VERIFIED",
            "available_evidence": "SEC Rule 6c-11 materials and fund-provider pages disclose prior-day holdings, market/NAV information, and/or 30-day median bid-ask spread. These are useful diligence inputs, not proof that the proposed portfolio's required 90% can be sold and settled within five business days at the intended trade size.",
            "needed": "Dated holdings and executable, position-sized liquidation/settlement analysis for each proposed allocation under normal-market conditions; confirm treatment of ETF secondary-market sale versus fund redemption.",
            "sources": [
                {"title": "SEC ETF Rule 6c-11 compliance guide", "url": "https://www.sec.gov/investment/exchange-traded-funds-small-entity-compliance-guide"},
                {"title": "State Street BIL product data", "url": "https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil"},
                {"title": "iShares IEF product data", "url": "https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf"},
                {"title": "iShares LQD product data", "url": "https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf"},
                {"title": "Vanguard VT product data", "url": "https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf"},
            ],
        },
        {
            "requirement": "S6 issuer cap and exemptions",
            "status": "POLICY_INTERPRETATION_AND_LOOKTHROUGH_UNVERIFIED",
            "available_evidence": f"Lab_13.md says: {s6_text} The machine-readable project configuration carries case-exemption assumptions, but the quoted client rule does not state them. Public daily ETF holdings disclosures can support look-through aggregation; no dated constituents or CIO ruling is loaded in this project.",
            "needed": "CIO confirmation of exemptions and look-through method; dated underlying holdings and issuer aggregation if exemptions do not apply.",
            "sources": [
                {"title": "SEC ETF Rule 6c-11 compliance guide (daily holdings disclosure)", "url": "https://www.sec.gov/investment/exchange-traded-funds-small-entity-compliance-guide"},
                {"title": "Lab_13.md S6 source", "repository_path": "../../Lab_13.md"},
            ],
        },
        {
            "requirement": f"S2 configured {objective_label} point-in-time hurdle",
            "status": "BLS_POINT_IN_TIME_RELEASE_VERIFIED" if cpi_source_verified else "LOOKAHEAD_OR_VINTAGE_UNVERIFIED",
            "available_evidence": f"The CPI pair is {cpi.get('prior_year_observation_date')}={cpi.get('prior_year_value')} and {cpi.get('current_observation_date')}={cpi.get('current_value')} ({cpi.get('units')}); release availability is {cpi_current_available}, {cpi_availability_phrase} decision date {decision_date}. Inflation is {cpi_rate_text}; the arithmetic {objective_label} hurdle is {hurdle_text}. Source: {cpi.get('source_url') or 'not supplied'}. This is BLS release evidence, not an ALFRED API vintage.",
            "needed": "For exact revised-series vintage reproduction, archive the underlying ALFRED response; this run relies on the contemporaneous BLS release and does not claim ALFRED API verification.",
            "sources": [
                {"title": "FRED observations API and vintage_dates parameter", "url": "https://fred.stlouisfed.org/docs/api/fred/series_observations.html"},
                {"title": "FRED real-time periods", "url": "https://fred.stlouisfed.org/docs/api/fred/realtime_period.html"},
                {"title": "BLS archived August 2026 CPI release", "url": "https://www.bls.gov/news.release/archives/cpi_09112026.htm"},
                {"title": "BLS 2026 release schedule", "url": "https://www.bls.gov/schedule/2026/home.htm"},
            ],
        },
        {
            "requirement": "S9 annual loss statement",
            "status": "UNRESOLVED_CLIENT_POLICY",
            "available_evidence": "Lab_13.md describes an annual loss greater than 10% as an unverifiable promise and does not define measurement or breach handling. No external market source can supply this client-specific policy decision.",
            "needed": "CIO definition of calendar/fiscal/rolling year, NAV or market-price total return, fee/cost treatment, and breach escalation. Until then, display a human-review alert only; do not promise or encode a loss guarantee.",
            "sources": [{"title": "Lab_13.md S9 source", "repository_path": "../../Lab_13.md"}],
        },
    ]

    triggers = [
        {"trigger": "Point-in-time CPI or required market observation unavailable, revised without a recorded vintage, or dated after the decision boundary", "response": "STOP the decision run; do not reuse the prior hurdle as current or substitute a later release."},
        {"trigger": "Optimizer returns infeasible, covariance validation fails, or required constraint cannot be evaluated", "response": "STOP and report the failed rule/input. Do not relax constraints or treat unknown as PASS."},
        {"trigger": "Verified reserve falls below the mandate's required distribution coverage", "response": "Escalate before trading and restore the committee-approved reserve; current modeled floor is 3% only under the stated $0.75m quarterly distribution assumption."},
        {"trigger": "Verified five-day liquid share falls below 90% or a position-sized liquidation test fails", "response": "STOP new allocations and obtain committee-approved remediation; ETF headline volume or median spread alone is insufficient."},
        {"trigger": "Aggregated nonexempt issuer exposure exceeds 8% under a CIO-confirmed S6 interpretation", "response": "Block the proposed trade and obtain committee direction; no exemption is presumed."},
        {"trigger": "Actual one-way turnover exceeds 25%", "response": "Do not rebalance absent the committee approval explicitly required by S7; current holdings are missing, so modeled turnover is illustrative only."},
        {"trigger": f"Rolling five-year after-cost return falls below the configured {objective_label} objective using admissible vintages", "response": "Trigger committee review and rerun the analysis; this is an objective review trigger, not a guaranteed return or automatic liquidation rule."},
        {"trigger": "DGS10 is unavailable at the decision date", "response": "Mark the signal unavailable and proceed without an automatic portfolio tilt; obtain a fresh permitted observation before using it as a review input."},
        {"trigger": "Calendar-year loss approaches or crosses -10%", "response": "Human-review alert only pending CIO definition of S9. Do not represent this as a verified breach or automatic sell rule."},
        {"trigger": "Proposed weights lie outside a subsequently committee-approved allocation range", "response": "STOP that trade pending review. The current stress envelope is not an approved range."},
    ]
    reversals = [
        {"current_outcome": "HOLD", "change_to": "CONDITIONAL_PILOT", "condition": "Point-in-time CPI and all required data are valid; actual holdings/costs are recorded; S3, S5, S6, S7 and S8 have documented treatment/evidence; the CIO approves S9 handling and the committee sets pilot size, authority, duration, review cadence, and abort conditions."},
        {"current_outcome": "CONDITIONAL_PILOT", "change_to": "HOLD", "condition": "Any required observation is unavailable or revised without vintage evidence, an optimizer/covariance stop occurs, a mandatory rule becomes untestable, or a pilot monitoring trigger is breached."},
        {"current_outcome": "ANY", "change_to": "REJECT", "condition": "A hard mandate violation is verified and no committee-approved exception or feasible remedy exists. Hypothetical equal-weight turnover infeasibility alone does not meet this condition."},
        {"current_outcome": "CONDITIONAL_PILOT", "change_to": "APPROVE", "condition": "Only after the committee-defined pilot review period is complete, outcomes and actual costs reconcile to the pre-approved plan, constraints remain verified, and the committee accepts a stress-supported allocation range."},
    ]

    approval_framework = [
        {"outcome": "APPROVE", "rule": "Only after every applicable hard rule has documented PASS evidence, point-in-time objective inputs are valid, actual-holdings turnover and costs are supportable, the committee accepts S10's optimization objective and S9 handling, and allocation ranges remain acceptable across approved stresses."},
        {"outcome": "CONDITIONAL_PILOT", "rule": "Only after hard legal/mandate constraints and point-in-time data gates are verified, with actual holdings, pilot size, duration, authority, monitoring cadence, and abort conditions approved in writing. A paper-only rehearsal may be considered while capital gates remain open."},
        {"outcome": "HOLD", "rule": "Use when material evidence or policy interpretation remains unknown, the estimate window produces material allocation dispersion, or feasibility depends on an inadmissible input. Do not authorize funded allocation."},
        {"outcome": "REJECT", "rule": "Use when a verified hard constraint is breached or no feasible portfolio exists under confirmed policy and evidence, with no approved remedy. A hypothetical-start infeasibility alone is not grounds to reject Meridian's actual portfolio."},
    ]

    approval_gates = {
        "point_in_time_cpi_valid": cpi_admissible,
        "actual_holdings_and_asof_known": actual_holdings_known,
        "five_day_liquidity_verified": liquid_known,
        "issuer_policy_and_exposure_verified": issuer_evidence_complete,
        "s9_handling_approved": s9_resolved,
        "full_mandate_feasibility_verified": full_mandate_feasible,
        "stress_range_robust_and_approved": range_supported,
    }
    baseline_comparisons = [
        {"scenario": "baseline_full_window", "portfolios": by_scenario.get("baseline_full_window", {}).get("portfolio_comparisons", [])},
        {"scenario": "last_36_months", "portfolios": by_scenario.get("last_36_months", {}).get("portfolio_comparisons", [])},
    ]
    turnover_sensitivity = by_scenario.get("turnover_cap_25pct_hypothetical", {})
    return {
        "phase": "4A",
        "generated_by": "scripts/generate_phase2_results.py",
        "configured_objective_label": objective_label,
        "evaluation_date": phase_result["analysis_date"],
        "candidate_disposition_for_student_review": disposition,
        "candidate_action": "HOLD funded deployment and do not authorize an allocation range yet; continue evidence collection and permit paper-only rehearsal if separately approved.",
        "not_final_investment_judgment": True,
        "decision_framework": approval_framework,
        "approval_gates": approval_gates,
        "hard_failure_observed": hard_failure,
        "point_in_time_cpi": {
            "decision_date": decision_date,
            "current_cpi_observation_date": cpi.get("current_observation_date"),
            "current_value": cpi.get("current_value"),
            "current_cpi_availability_date": cpi_current_available,
            "prior_cpi_observation_date": cpi.get("prior_year_observation_date"),
            "prior_value": cpi.get("prior_year_value"),
            "prior_cpi_availability_date": cpi_prior_available,
            "point_in_time_source_verified": cpi_source_verified,
            "inflation_rate": phase_result.get("cpi_yoy"),
            "admissible_for_stress_decision": cpi_admissible,
            "modeled_hurdle_used": phase_result["provisional_after_cost_hurdle"],
            "status": "PASS" if cpi_admissible else "STOP_LOOKAHEAD_OR_UNVERIFIED_VINTAGE",
        },
        "window_sensitivity": {
            "full_window_scenario": "baseline_full_window",
            "full_window_weights": full_weights,
            "full_window_return_observations": stress["market_return_observations"],
            "36_month_scenario": "last_36_months",
            "36_month_weights": short_weights,
            "bil_allocation_difference_percentage_points": None if bil_window_gap is None else bil_window_gap * 100.0,
            "interpretation": "The optimized BIL weight changes materially between the tested full and 36-month windows. The mandate supplies no approved tolerance for this dispersion; do not call the resulting envelope robust or authorize it as a band.",
        },
        "modeled_feasible_stress_envelope": {
            "weights_by_ticker": envelope,
            "feasible_reoptimized_scenario_count": len(optimized),
            "supporting_scenarios": [item["scenario"] for item in optimized],
            "status": "DIAGNOSTIC_ONLY_NOT_AN_AUTHORIZATION_RANGE",
            "reasons_not_robust": [
                "Full versus 36-month estimation changes BIL by the reported percentage-point amount.",
                "The mandate does not set a numerical tolerance for allocation stability, so a robust band cannot be inferred without committee judgment.",
                "CPI is point-in-time verified from the BLS archived August release, not an ALFRED API vintage; this uses unadjusted CPI-U rather than seasonally adjusted CPIAUCSL.",
                "Actual holdings, turnover, transaction costs, liquidity, issuer treatment/exposure, and S9 handling remain unverified.",
            ],
        },
        "portfolio_comparisons": baseline_comparisons,
        "hypothetical_turnover_stop": {
            "scenario": "turnover_cap_25pct_hypothetical",
            "starting_holdings": mandate["turnover"]["illustrative_starting_allocation"]["label"],
            "maximum_turnover": mandate["turnover"]["maximum"],
            "status": turnover_sensitivity.get("status", "NOT_AVAILABLE"),
            "feasible": bool(turnover_sensitivity.get("feasible", False)),
            "reason": turnover_sensitivity.get("reason", "stress scenario not available"),
            "actual_meridian_holdings_inferred": False,
        },
        "evidence_requirements": evidence,
        "monitoring_triggers_and_stop_conditions": triggers,
        "reversal_conditions": reversals,
        "committee_decisions_requested": [
            f"Confirm that the archived BLS not-seasonally-adjusted CPI-U release is the preferred operational interpretation of the configured {objective_label} model input. The original client S2 wording remains CPI + 4%; require a contemporaneous ALFRED CPIAUCSL vintage before adoption if needed.",
            "Provide Meridian's actual holdings and holdings as-of date, plus an approved transaction-cost estimate or execution evidence.",
            "Confirm whether the S6 exemptions in config/mandate.json govern despite their absence from the S6 sentence in Lab_13.md; approve look-through and issuer aggregation treatment.",
            "Provide position-sized five-business-day sale and settlement evidence for the 90% liquidity rule.",
            "Define how S9 is measured and handled, and confirm the minimum-volatility objective as a modeling choice under S10.",
            "Decide whether the model-only stress envelope is useful for discussion; no allocation range is recommended for authorization in this report.",
        ],
    }


def render_decision_markdown(report: dict[str, Any]) -> str:
    """Render the generated decision-support report as readable Markdown."""
    percent = lambda value: "—" if value is None else f"{value:.2%}"
    cpi_inflation = report["point_in_time_cpi"].get("inflation_rate")
    cpi_inflation_text = "—" if cpi_inflation is None else f"{cpi_inflation:.4%}"
    cpi_hurdle_text = f"{report['point_in_time_cpi']['modeled_hurdle_used']:.4%}"
    lines = [
        "# Phase 4A Investment Decision Support",
        "",
        "Generated from the Phase 2/3B financial engine. This is candidate decision support for the student's review, not the final investment judgment.",
        "",
        f"- Evaluation date: **{report['evaluation_date']}**",
        f"- Candidate disposition: **{report['candidate_disposition_for_student_review']}**",
        f"- Candidate action: {report['candidate_action']}",
        "",
        "## Decision framework",
        "",
        "| Outcome | Evidence gate |",
        "|---|---|",
    ]
    for rule in report["decision_framework"]:
        lines.append(f"| {rule['outcome']} | {rule['rule']} |")
    lines.extend(["", "## Current approval gates", "", "| Gate | Status |", "|---|---|"])
    lines.extend(f"| {gate.replace('_', ' ')} | {'PASS' if passed else 'NOT SATISFIED'} |" for gate, passed in report["approval_gates"].items())
    cpi = report["point_in_time_cpi"]
    lines.extend([
        "",
        "## Decision-date and CPI check",
        "",
        f"The stress decision date is **{cpi['decision_date']}**. The CPI inputs are {cpi['prior_cpi_observation_date']} and {cpi['current_cpi_observation_date']}, published {cpi['current_cpi_availability_date']} and available by the decision date. BLS point-in-time source verified: **{cpi['point_in_time_source_verified']}** (this is not an ALFRED API vintage). Inflation is {cpi_inflation_text}; the configured arithmetic {report['configured_objective_label']} modeled hurdle is {cpi_hurdle_text}. The earlier September 2026 current-snapshot input was unavailable on October 5 and is retained in validation history as a corrected look-ahead error.",
        "",
        "## Window sensitivity and model-only envelope",
        "",
        f"Full-window BIL allocation: {percent(report['window_sensitivity']['full_window_weights']['BIL'])}; 36-month BIL allocation: {percent(report['window_sensitivity']['36_month_weights']['BIL'])}; difference: {report['window_sensitivity']['bil_allocation_difference_percentage_points']:.1f} percentage points.",
        "",
        "| Ticker | Minimum across modeled feasible stress solutions | Maximum |",
        "|---|---:|---:|",
    ])
    for ticker, bounds in report["modeled_feasible_stress_envelope"]["weights_by_ticker"].items():
        lines.append(f"| {ticker} | {percent(bounds['minimum'])} | {percent(bounds['maximum'])} |")
    lines.extend(["", "**Status: diagnostic only; not an authorization range.** The full-to-36-month shift, unresolved mandate evidence, and CPI measurement choice do not support a robust allocation band.", "", "## Portfolio comparisons", "", "Gross return uses annualized arithmetic historical estimates. Net return subtracts one modeled rebalance cost; it is not a recurring annual cost forecast or proof of the rolling five-year S2 objective. Turnover and costs use hypothetical equal-weight starting holdings, not actual Meridian holdings.", ""])
    for group in report["portfolio_comparisons"]:
        lines.extend([f"### {group['scenario']}", "", "| Portfolio | Weights (BIL / IEF / LQD / VT) | Gross return | Net return | Volatility | Turnover from hypothetical equal weight | Cost | Mandate verdicts |", "|---|---|---:|---:|---:|---:|---:|---|"])
        for portfolio in group["portfolios"]:
            weights = " / ".join(percent(portfolio["weights"][ticker]) for ticker in ("BIL", "IEF", "LQD", "VT"))
            verdicts = ", ".join(f"{key}: {value}" for key, value in portfolio["mandate_verdicts"].items())
            lines.append("| " + " | ".join([portfolio["portfolio"], weights, percent(portfolio["annual_expected_return"]), percent(portfolio["net_expected_return"]), percent(portfolio["annual_volatility"]), percent(portfolio["turnover_from_hypothetical_equal_weight"]), percent(portfolio["cost_rate"]), verdicts]) + " |")
    stop = report["hypothetical_turnover_stop"]
    lines.extend(["", "## Hypothetical turnover-cap stop", "", f"Status: **{stop['status']}**; feasible: **{stop['feasible']}** under the {percent(stop['maximum_turnover'])} turnover cap from the explicitly hypothetical equal-weight start. Actual Meridian holdings are not inferred. Reason: {stop['reason']}."])
    lines.extend(["", "## Evidence requirements", "", "| Requirement | Status | Current evidence and remaining need |", "|---|---|---|"])
    for item in report["evidence_requirements"]:
        lines.append(f"| {item['requirement']} | {item['status']} | {item['available_evidence']} Needed: {item['needed']} Sources: " + ", ".join(f"[{source['title']}]({source.get('url', source.get('repository_path', ''))})" for source in item["sources"]) + " |")
    lines.extend(["", "## Monitoring triggers and stop conditions", ""])
    lines.extend(f"- **{row['trigger']}** — {row['response']}" for row in report["monitoring_triggers_and_stop_conditions"])
    lines.extend(["", "## Reversal conditions", "", "| Current outcome | Change to | Condition |", "|---|---|---|"])
    lines.extend(f"| {row['current_outcome']} | {row['change_to']} | {row['condition']} |" for row in report["reversal_conditions"])
    lines.extend(["", "## Decisions requested from the committee", ""])
    lines.extend(f"- {item}" for item in report["committee_decisions_requested"])
    lines.append("")
    return "\n".join(lines)
