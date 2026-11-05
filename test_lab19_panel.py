"""Offline tests for the FIN 43900 Lab 19 investor panel."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from lab19_panel import (
    audit_all_memos,
    build_memos,
    burry_checks,
    load_offline_costco,
    verdict,
    wood_checks,
)


class Lab19PanelTests(unittest.TestCase):
    @staticmethod
    def load_saved_nvda():
        return json.loads(
            Path("lab19_output/NVDA_panel_data.json").read_text(encoding="utf-8")
        )

    def test_costco_active_panel_results(self):
        analysis = load_offline_costco()
        self.assertEqual(
            analysis["panel_checks"]["Buffett"],
            {
                "roe_15_every_year": "pass",
                "positive_owner_earnings_every_year": "pass",
                "owner_earnings_growth": "pass",
            },
        )
        self.assertEqual(
            analysis["panel_checks"]["Wood"],
            {
                "innovation_exposure": "not known",
                "revenue_growth": "pass",
                "reported_rd_latest": "not known",
            },
        )
        self.assertEqual(
            analysis["panel_checks"]["Burry"],
            {
                "operating_cash_flow_covers_net_income": "pass",
                "liabilities_no_more_than_twice_equity": "pass",
            },
        )
        self.assertEqual(analysis["verdicts"]["Wood"], "not known")
        self.assertEqual(
            f"{analysis['rows'][-1]['current_ratio']['value']:.2f}", "1.06"
        )
        self.assertEqual(
            f"{analysis['rows'][-1]['liabilities_to_equity']['value']:.2f}",
            "1.49",
        )

    def test_wood_checks_are_computed_from_inputs(self):
        analysis = load_offline_costco()
        rows = copy.deepcopy(analysis["rows"])
        rows[-1]["revenue"]["value"] = rows[0]["revenue"]["value"] - 1
        rows[-1]["research_and_development"]["value"] = 100

        checks = wood_checks(rows, innovation_exposure=True)
        self.assertEqual(checks["innovation_exposure"], "pass")
        self.assertEqual(checks["revenue_growth"], "fail")
        self.assertEqual(checks["reported_rd_latest"], "pass")

        checks_without_external_research = wood_checks(rows)
        self.assertEqual(
            checks_without_external_research["innovation_exposure"], "not known"
        )

    def test_missing_values_remain_not_known(self):
        analysis = load_offline_costco()
        rows = copy.deepcopy(analysis["rows"])
        rows[-1]["revenue"]["value"] = None
        rows[1]["operating_cash_flow"]["value"] = None
        self.assertEqual(wood_checks(rows)["revenue_growth"], "not known")
        self.assertEqual(
            burry_checks(rows)["operating_cash_flow_covers_net_income"],
            "not known",
        )

    def test_unprinted_number_checker_covers_all_memos(self):
        analysis = load_offline_costco()
        memos = build_memos(analysis)
        self.assertEqual(
            audit_all_memos(memos, analysis),
            {"Buffett": [], "Wood": [], "Burry": []},
        )
        memos["Wood"] += " Unsupported test value: 999.9."
        self.assertEqual(
            audit_all_memos(memos, analysis)["Wood"], ["999.9"]
        )

    def test_generated_memo_spacing_and_titles(self):
        memos = build_memos(load_offline_costco())
        self.assertIn(
            "$3,501 million to $9,382 million", memos["Buffett"]
        )
        self.assertIn(
            "$15,817 million versus net income of $9,226 million",
            memos["Burry"],
        )
        self.assertIn(
            "# Cathie Wood-Inspired Investment Memo: COST", memos["Wood"]
        )
        for memo in memos.values():
            self.assertNotRegex(memo, r"\d[\d,]*(?:\.\d+)?\n(?:million|billion)")

    def test_nvda_active_panel_results(self):
        analysis = self.load_saved_nvda()
        self.assertEqual(
            list(analysis["panel_checks"]["Buffett"].values()),
            ["pass", "pass", "pass"],
        )
        self.assertEqual(
            list(analysis["panel_checks"]["Wood"].values()),
            ["not known", "pass", "pass"],
        )
        self.assertEqual(
            analysis["panel_checks"]["Burry"],
            {
                "operating_cash_flow_covers_net_income": "fail",
                "liabilities_no_more_than_twice_equity": "pass",
            },
        )

    def test_burry_memo_tracks_check_results(self):
        costco = load_offline_costco()
        costco_memo = build_memos(costco)["Burry"]
        self.assertIn("Both forensic checks pass.", costco_memo)
        self.assertNotIn("check fails", costco_memo)

        nvda = self.load_saved_nvda()
        nvda_memo = build_memos(nvda)["Burry"]
        self.assertIn("cash-flow coverage check fails", nvda_memo)
        self.assertIn("leverage check passes", nvda_memo)
        self.assertNotIn("Both forensic checks pass.", nvda_memo)

        leverage_failure = copy.deepcopy(costco)
        leverage_failure["rows"][-1]["liabilities_to_equity"]["value"] = 2.5
        leverage_failure["panel_checks"]["Burry"] = burry_checks(
            leverage_failure["rows"]
        )
        leverage_failure["verdicts"]["Burry"] = verdict(
            leverage_failure["panel_checks"]["Burry"], "Burry"
        )
        leverage_memo = build_memos(leverage_failure)["Burry"]
        self.assertIn("cash-flow coverage check passes", leverage_memo)
        self.assertIn("leverage check fails", leverage_memo)

        missing = copy.deepcopy(costco)
        missing["rows"][0]["operating_cash_flow"]["value"] = None
        missing["rows"][-1]["liabilities_to_equity"]["value"] = None
        missing["panel_checks"]["Burry"] = burry_checks(missing["rows"])
        missing["verdicts"]["Burry"] = verdict(
            missing["panel_checks"]["Burry"], "Burry"
        )
        missing_memo = build_memos(missing)["Burry"]
        self.assertIn("Both forensic checks are not known.", missing_memo)
        self.assertIn("**Verdict: not known**", missing_memo)


if __name__ == "__main__":
    unittest.main()
