"""Regression tests for configuration-derived reporting labels."""

import unittest

from project2_engine.labels import cpi_objective_label, percentage_points


class ReportingLabelTests(unittest.TestCase):
    def test_common_spreads_are_formatted_without_hardcoding(self):
        self.assertEqual(cpi_objective_label(0.04), "CPI + 4%")
        self.assertEqual(cpi_objective_label(0.05), "CPI + 5%")
        self.assertEqual(percentage_points(0.045), "4.5%")


if __name__ == "__main__":
    unittest.main()
