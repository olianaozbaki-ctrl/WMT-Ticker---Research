"""Generate the visible Phase 2 output from the same engine used by the app."""

from __future__ import annotations

import json
from pathlib import Path

from project2_engine.config import load_mandate
from project2_engine.data import estimate_from_monthly_prices
from project2_engine.phase2 import TICKERS, run_phase2
from project2_engine.precision import compare_optimizer_precision


ROOT = Path(__file__).resolve().parents[1]


def percent(value: float) -> str:
    return f"{value:.2%}"


def main() -> None:
    result = run_phase2(ROOT)
    mandate = load_mandate(ROOT / "config" / "mandate.json")
    estimates = estimate_from_monthly_prices(ROOT / "data" / "prices_monthly.csv")
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

    lines = [
        "# Phase 2 Executed Results",
        "",
        "Generated directly by `python scripts/generate_phase2_results.py`; values were not manually transcribed.",
        "",
        f"- Analysis date: **{result['analysis_date']}**",
        f"- Source retrieval date: **{result['source_retrieval_date']}**",
        f"- Market-data as-of date: **{result['market_data_as_of']}**",
        f"- Price observations: **{result['price_observations']} monthly adjusted closes**",
        f"- Return observations: **{result['monthly_return_observations']} monthly simple returns**",
        f"- Provisional CPI year-over-year: **{percent(result['cpi_yoy'])}**",
        f"- Provisional after-cost hurdle: **{percent(result['provisional_after_cost_hurdle'])}**",
        f"- ALFRED vintage verified: **{result['cpi_vintage_verified']}**",
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
    (output_dir / "phase2_results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Generated {len(result['portfolios'])} portfolio results through "
        f"{result['market_data_as_of']}."
    )


if __name__ == "__main__":
    main()
