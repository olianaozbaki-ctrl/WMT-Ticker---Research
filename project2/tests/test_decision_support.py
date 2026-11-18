import json
import unittest
from pathlib import Path

from project2_engine.decision_support import build_decision_support, evaluate_decision, render_decision_markdown


ROOT = Path(__file__).resolve().parents[1]


def sample_inputs():
    def scenario(name, weights, feasible=True):
        portfolio = {
            "portfolio": "Reoptimized minimum volatility",
            "weights": weights,
            "annual_expected_return": .08,
            "net_expected_return": .079,
            "annual_volatility": .08,
            "turnover_from_hypothetical_equal_weight": .50,
            "cost_rate": .0005,
            "optimizer_feasible": feasible,
            "mandate_verdicts": {"liquidity": "NOT_TESTABLE"},
        }
        return {
            "scenario": name,
            "feasible": feasible,
            "status": "PROVISIONAL_FEASIBLE" if feasible else "STOP_INFEASIBLE",
            "reason": "no feasible grid portfolio" if not feasible else "all modeled constraints passed",
            "weights": weights,
            "portfolio_comparisons": [portfolio],
        }

    stress = {
        "decision_date": "2026-10-05",
        "market_return_observations": 59,
        "scenarios": [
            scenario("baseline_full_window", {"BIL": .44, "IEF": 0, "LQD": 0, "VT": .56}),
            scenario("last_36_months", {"BIL": .78, "IEF": 0, "LQD": 0, "VT": .22}),
            scenario("turnover_cap_25pct_hypothetical", None, False),
        ],
    }
    phase = {
        "analysis_date": "2026-11-18",
        "stress_matrix": stress,
        "provisional_after_cost_hurdle": .07717,
        "optimization": {"full_mandate_feasible": False},
        "portfolios": [],
    }
    mandate = {
        "turnover": {
            "actual_starting_holdings_status": "unavailable",
            "maximum": .25,
            "illustrative_starting_allocation": {"label": "hypothetical equal weight"},
        },
        "project_universe": [{"liquidity_business_days": None}],
        "original_policy": {"statements": {"S6": "No single issuer can account for more than 8% of the portfolio."}},
        "risk": {"loss_rule_status": "unresolved_unverifiable_promise_not_a_hard_constraint"},
        "unresolved_decisions": [],
    }
    provenance = {
        "cpi_data": {
            "current_observation_date": "2026-09-01",
            "current_availability_date": "2026-10-14",
            "prior_year_observation_date": "2025-09-01",
            "prior_year_availability_date": "2025-10-24",
            "alfred_vintage_verified": False,
        }
    }
    return phase, mandate, provenance


class DecisionSupportTests(unittest.TestCase):
    def test_framework_returns_all_four_defined_outcomes(self):
        self.assertEqual(evaluate_decision(unmitigated_hard_failure=False, approval_ready=True, pilot_ready=True), "APPROVE")
        self.assertEqual(evaluate_decision(unmitigated_hard_failure=False, approval_ready=False, pilot_ready=True), "CONDITIONAL_PILOT")
        self.assertEqual(evaluate_decision(unmitigated_hard_failure=False, approval_ready=False, pilot_ready=False), "HOLD")
        self.assertEqual(evaluate_decision(unmitigated_hard_failure=True, approval_ready=True, pilot_ready=True), "REJECT")

    def test_cpi_after_decision_date_blocks_point_in_time_readiness(self):
        phase, mandate, provenance = sample_inputs()
        report = build_decision_support(phase, mandate, provenance)
        self.assertFalse(report["point_in_time_cpi"]["admissible_for_stress_decision"])
        self.assertEqual(report["point_in_time_cpi"]["status"], "STOP_LOOKAHEAD_OR_UNVERIFIED_VINTAGE")
        self.assertEqual(report["candidate_disposition_for_student_review"], "HOLD")
        self.assertFalse(report["hard_failure_observed"])
        self.assertEqual(report["hypothetical_turnover_stop"]["status"], "STOP_INFEASIBLE")
        self.assertFalse(report["hypothetical_turnover_stop"]["actual_meridian_holdings_inferred"])

    def test_range_is_envelope_not_authorization_and_shows_window_shift(self):
        phase, mandate, provenance = sample_inputs()
        report = build_decision_support(phase, mandate, provenance)
        self.assertEqual(report["window_sensitivity"]["bil_allocation_difference_percentage_points"], 34.0)
        self.assertEqual(report["modeled_feasible_stress_envelope"]["weights_by_ticker"]["BIL"], {"minimum": .44, "maximum": .78})
        self.assertEqual(report["modeled_feasible_stress_envelope"]["status"], "DIAGNOSTIC_ONLY_NOT_AN_AUTHORIZATION_RANGE")

    def test_report_includes_evidence_triggers_and_no_automatic_s9_breach(self):
        phase, mandate, provenance = sample_inputs()
        markdown = render_decision_markdown(build_decision_support(phase, mandate, provenance))
        self.assertIn("HOLD", markdown)
        self.assertIn("not admissible", markdown.lower())
        self.assertIn("Human-review alert only", markdown)
        self.assertIn("SEC ETF Rule 6c-11", markdown)
        self.assertIn("Hypothetical turnover-cap stop", markdown)
        self.assertIn("Reversal conditions", markdown)

    def test_generated_decision_artifacts_are_present_and_consistent(self):
        report_path = ROOT / "outputs" / "phase4a_decision_support.json"
        markdown_path = ROOT / "outputs" / "phase4a_decision_support.md"
        self.assertTrue(report_path.exists())
        self.assertTrue(markdown_path.exists())
        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["candidate_disposition_for_student_review"], "HOLD")
        self.assertIn("not an authorization range", markdown_path.read_text(encoding="utf-8").lower())
        phase2_markdown = (ROOT / "outputs" / "phase2_results.md").read_text(encoding="utf-8")
        self.assertIn("return-hurdle CPI valid for this decision date: **False**", phase2_markdown)
        self.assertNotIn("{result['stress_matrix']", phase2_markdown)


if __name__ == "__main__":
    unittest.main()
