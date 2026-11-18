"""Generate the visible Phase 2 output from the same engine used by the app."""

from __future__ import annotations

import json
from pathlib import Path

from project2_engine.config import load_mandate
from project2_engine.data import estimate_from_monthly_prices
from project2_engine.decision_support import render_decision_markdown
from project2_engine.labels import cpi_objective_label
from project2_engine.phase2 import TICKERS, run_phase2
from project2_engine.precision import compare_optimizer_precision


ROOT = Path(__file__).resolve().parents[1]


def percent(value: float) -> str:
    return f"{value:.2%}"


def main() -> None:
    result = run_phase2(ROOT)
    mandate = load_mandate(ROOT / "config" / "mandate.json")
    objective_label = cpi_objective_label(mandate["objective"]["real_return_spread"])
    estimates = estimate_from_monthly_prices(ROOT / "data" / "prices_monthly.csv", as_of_date="2026-10-05")
    result["optimizer_precision_validation"] = compare_optimizer_precision(
        estimates.annual_expected_returns,
        estimates.annual_covariance,
        minimum_return=result["provisional_after_cost_hurdle"],
        reserve_assets={"BIL"},
        minimum_reserve=mandate["reserve"]["minimum_weight"],
        illustrative_current_weights=mandate["turnover"][
            "illustrative_starting_allocation"
        ]["weights"],
        transaction_cost_bps=mandate["costs"]["transaction_cost_bps"],
    )
    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)
    (output_dir / "phase2_results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    decision = result["decision_support"]
    (output_dir / "phase4a_decision_support.json").write_text(
        json.dumps(decision, indent=2) + "\n", encoding="utf-8"
    )
    (output_dir / "phase4a_decision_support.md").write_text(
        render_decision_markdown(decision), encoding="utf-8"
    )

    lines = [
        "# Phase 2 Executed Results",
        "",
        "Generated directly by `PYTHONPATH=src python scripts/generate_phase2_results.py`; values were not manually transcribed.",
        "",
        f"- Analysis date: **{result['analysis_date']}**",
        f"- Source retrieval date: **{result['source_retrieval_date']}**",
        f"- Market-data as-of date: **{result['market_data_as_of']}**",
        f"- Price observations: **{result['price_observations']} monthly adjusted closes**",
        f"- Return observations: **{result['monthly_return_observations']} monthly simple returns**",
        f"- Point-in-time CPI-U year-over-year: **{result['cpi_yoy']:.4%}**",
        f"- {objective_label} after-cost hurdle: **{result['provisional_after_cost_hurdle']:.4%}**",
        f"- Point-in-time CPI source verified: **{result['cpi_point_in_time_source_verified']}** (BLS release; not ALFRED API vintage)",
        f"- CPI input pair: **{result['cpi_point_in_time_source']['prior_year_observation_date']} {result['cpi_point_in_time_source']['prior_year_value']} / {result['cpi_point_in_time_source']['current_observation_date']} {result['cpi_point_in_time_source']['current_value']}** ({result['cpi_point_in_time_source']['units']}); released {result['cpi_point_in_time_source']['availability_date']}",
        f"- DGS10 point-in-time signal: **{result['dgs10_signal']['value_percent']:.2f}%** (observation {result['dgs10_signal']['observation_date']}; available {result['dgs10_signal']['availability_date']}; decision {result['dgs10_signal']['decision_date']})",
        "",
        "## Portfolio comparison",
        "",
        "| Portfolio | " + " | ".join(TICKERS) + " | Expected return | Volatility | Reserve | Illustrative turnover | Illustrative cost | Verified mandate feasible |",
        "|---|" + "---:|" * 10,
    ]
    for portfolio in result["portfolios"]:
        cells = [
            portfolio["name"],
            *(percent(portfolio["weights"][ticker]) for ticker in TICKERS),
            percent(portfolio["annual_expected_return"]),
            percent(portfolio["annual_volatility"]),
            percent(portfolio["reserve_allocation"]),
            percent(portfolio["illustrative_turnover_from_equal_weight"]),
            percent(portfolio["illustrative_transaction_cost_rate"]),
            str(portfolio["verified_mandate_feasible"]),
        ]
        lines.append("| " + " | ".join(cells) + " |")

    lines.extend(["", "## Rule-level verdicts", ""])
    for portfolio in result["portfolios"]:
        lines.extend(
            [
                f"### {portfolio['name']}",
                "",
                "| Rule | Verdict | Measured | Limit | Explanation |",
                "|---|---|---:|---:|---|",
            ]
        )
        for rule in portfolio["rules"]:
            measured = "—" if rule["measured_value"] is None else f"{rule['measured_value']:.6f}"
            limit = "—" if rule["limit_value"] is None else f"{rule['limit_value']:.6f}"
            lines.append(
                f"| {rule['label']} | {rule['status']} | {measured} | {limit} | {rule['explanation']} |"
            )
        lines.append("")

    stop = result["optimization"]["hypothetical_turnover_cap_stop_condition"]
    lines.extend(
        [
            "## Feasibility boundary and stop condition",
            "",
            f"- Provisional optimizer feasible on supported model inputs: **{result['optimization']['provisional_feasible_on_supported_model_inputs']}**",
            f"- Full mandate feasible: **{result['optimization']['full_mandate_feasible']}**",
            f"- Starting holdings for turnover sensitivity: **{stop['starting_holdings']}**",
            f"- Feasible if the hypothetical start were subject to the {percent(stop['maximum_turnover'])} turnover cap: **{stop['feasible']}**",
            f"- Maximum net expected return under that hypothetical cap: **{percent(stop['maximum_net_expected_return'])}**",
            f"- Provisional return hurdle: **{percent(stop['return_hurdle'])}**",
            f"- Shortfall: **{percent(stop['return_shortfall'])}**",
            "",
            "Because actual Meridian holdings and their as-of date are unavailable, this is a hypothetical stop-condition test, not an actual turnover verdict. Actual turnover remains NOT_TESTABLE.",
            "",
            "## Optimizer precision validation",
            "",
        ]
    )
    precision = result["optimizer_precision_validation"]
    lines.append(precision["method"])
    lines.extend(
        [
            "",
            "| Method | BIL | IEF | LQD | VT | Net return | Volatility |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for label, key in (
        ("Production 1% grid", "production_grid"),
        ("Finer 0.5% grid", "finer_grid"),
        ("Continuous SLSQP", "continuous_slsqp"),
    ):
        values = precision[key]
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    *(percent(values["weights"][ticker]) for ticker in TICKERS),
                    percent(values["net_expected_return"]),
                    percent(values["annual_volatility"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            f"Maximum production-grid weight difference versus continuous: **{precision['maximum_weight_difference_percentage_points']:.4f} percentage points**.",
            f"Production-grid volatility gap versus continuous: **{precision['production_volatility_gap_percentage_points']:.4f} percentage points**.",
            f"Conclusion: **{precision['conclusion']}**",
            "",
        ]
    )

    lines.extend(["## Limitations", ""] + [f"- {item}" for item in result["limitations"]])
    lines.extend(["", "## DGS10 point-in-time signal", "", json.dumps(result["dgs10_signal"], indent=2)])
    cpi = result["stress_matrix"]["return_hurdle_cpi"]
    lines.extend(["", "## Phase 3B stress matrix", "", result["stress_matrix"]["assumptions"], "", f"Decision date: **{result['stress_matrix']['decision_date']}**; aligned market return data through **{result['stress_matrix']['market_data_as_of']}** ({result['stress_matrix']['market_return_observations']} monthly returns). Signal and market boundaries consistent: **{result['stress_matrix']['signal_boundary_consistent']}**.", "", f"**CPI gate:** point-in-time valid: **{cpi['point_in_time_valid_for_decision_date']}**; BLS observation pair {cpi['prior_observation_date']}={cpi['prior_year_value']} and {cpi['current_observation_date']}={cpi['current_value']} was available {cpi['current_availability_date']}. Inflation **{cpi['inflation_rate']:.4%}**; {objective_label} target **{result['provisional_after_cost_hurdle']:.4%}**. This is based on the archived BLS release, not an ALFRED API vintage.", "", "All scenarios use the hypothetical equal-weight starting allocation for turnover and cost; these are not actual Meridian holdings. Optimizer feasibility is provisional and does not imply full mandate compliance.", "", "| Scenario | Category | Window | Status | Weights | Gross return | Net return | Volatility | Turnover | Cost | Optimizer feasible | Mandate verdicts |", "|---|---|---|---|---|---:|---:|---:|---:|---:|---|---|"])
    for row in result["stress_matrix"]["scenarios"]:
        w = "STOP" if row["weights"] is None else ", ".join(f"{k} {v:.0%}" for k,v in row["weights"].items() if v)
        fmt=lambda x: "—" if x is None else percent(x)
        verdicts = ", ".join(f"{rule}: {status}" for rule,status in row["mandate_verdicts"].items()) or "Not available (infeasible stop)"
        lines.append(f"| {row['scenario']} | {row['category']} | {row['window']} | {row['status']} | {w} | {fmt(row['annual_expected_return'])} | {fmt(row['net_expected_return'])} | {fmt(row['annual_volatility'])} | {fmt(row['turnover'])} | {fmt(row['cost_rate'])} | {row['feasible']} | {verdicts} |")
    lines.extend(["", "### Baseline and reoptimized portfolio results by scenario", "", "Turnover and costs below are measured from the hypothetical equal-weight starting mix. Rule verdicts are independent evidence checks; optimizer feasibility does not imply full mandate compliance.", "", "| Scenario | Portfolio | Weights (BIL / IEF / LQD / VT) | Gross return | Net return | Volatility | Turnover | Cost | Optimizer feasible | Rule verdicts |", "|---|---|---|---:|---:|---:|---:|---:|---|---|"])
    for scenario in result["stress_matrix"]["scenarios"]:
        for item in scenario["portfolio_comparisons"]:
            weights = "STOP" if item["weights"] is None else " / ".join(percent(item["weights"][ticker]) for ticker in TICKERS)
            verdicts = ", ".join(f"{rule}: {status}" for rule,status in item["mandate_verdicts"].items()) or item.get("stop_reason", "—")
            lines.append("| " + " | ".join([scenario["scenario"], item["portfolio"], weights, fmt(item["annual_expected_return"]), fmt(item["net_expected_return"]), fmt(item["annual_volatility"]), fmt(item["turnover_from_hypothetical_equal_weight"]), fmt(item["cost_rate"]), str(item["optimizer_feasible"]), verdicts]) + " |")
    lines.extend([
        "",
        "## Phase 4A candidate decision support",
        "",
        f"Model-generated disposition: **{decision['candidate_disposition_for_student_review']}**. This aligns with the final written HOLD recommendation in `docs/decision-memo.md`; no allocation range is recommended for authorization. See [the complete generated decision-support report](phase4a_decision_support.md).",
    ])
    (output_dir / "phase2_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Generated {len(result['portfolios'])} portfolio results through "
        f"{result['market_data_as_of']} plus Phase 4A decision support."
    )


if __name__ == "__main__":
    main()
