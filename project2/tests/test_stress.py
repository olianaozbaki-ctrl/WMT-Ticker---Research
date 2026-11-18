import unittest
from pathlib import Path

from project2_engine.config import load_mandate
from project2_engine.data import estimate_from_monthly_prices, load_cpi_yoy
from project2_engine.phase2 import run_phase2
from project2_engine.calculations import portfolio_variance
from project2_engine.stress import _correlation_stress

ROOT=Path(__file__).resolve().parents[1]

class StressTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.result=run_phase2(ROOT)
    def test_matrix_covers_required_scenario_families(self):
        cats={r['category'] for r in self.result['stress_matrix']['scenarios']}
        self.assertTrue({'expected_return','window','cost','constraint','risk','signal'}<=cats)
        baseline=self.result['stress_matrix']['scenarios'][0]
        self.assertEqual({p['portfolio'] for p in baseline['portfolio_comparisons']},{'Equal weight','60/40 benchmark','Reoptimized minimum volatility'})
    def test_infeasibility_is_stop_not_relaxation(self):
        rows={r['scenario']:r for r in self.result['stress_matrix']['scenarios']}
        self.assertEqual(rows['turnover_cap_25pct_hypothetical']['status'],'STOP_INFEASIBLE')
        self.assertIsNone(rows['turnover_cap_25pct_hypothetical']['weights'])
    def test_signal_and_market_dates_share_decision_boundary(self):
        stress=self.result['stress_matrix']
        self.assertLessEqual(stress['market_data_as_of'],stress['decision_date'])
        self.assertEqual(stress['decision_date'],'2026-10-05')
        self.assertTrue(stress['signal_boundary_consistent'])
        self.assertLess(stress['market_return_observations'],60)

    def test_cpi_hurdle_lookahead_is_an_explicit_decision_stop(self):
        cpi=self.result['stress_matrix']['return_hurdle_cpi']
        self.assertEqual(cpi['current_availability_date'],'2026-10-14')
        self.assertFalse(cpi['point_in_time_valid_for_decision_date'])
        self.assertEqual(cpi['status'],'STOP_LOOKAHEAD_OR_UNVERIFIED_VINTAGE')
    def test_volatility_stress_is_valid_and_higher(self):
        rows={r['scenario']:r for r in self.result['stress_matrix']['scenarios']}
        self.assertTrue(rows['volatility_plus_25pct']['feasible'])
        self.assertGreater(rows['volatility_plus_25pct']['annual_volatility'],rows['baseline_full_window']['annual_volatility'])

    def test_correlation_stress_is_psd_and_preserves_covariance_validation(self):
        cov=self.result['stress_matrix']['scenarios']
        stressed=next(r for r in cov if r['scenario']=='correlations_psd_convex_blend_50pct')
        self.assertTrue(stressed['feasible'])
        # Validate a covariance submatrix from the exact stress calculation via the engine.
        from project2_engine.data import estimate_from_monthly_prices
        estimates=estimate_from_monthly_prices(ROOT/'data'/'prices_monthly.csv')
        matrix=_correlation_stress(estimates.annual_covariance)
        portfolio_variance({k:.25 for k in estimates.tickers},matrix)

    def test_invalid_covariance_is_still_rejected(self):
        invalid={'a':{'a':1.0,'b':2.0},'b':{'a':2.0,'b':1.0}}
        with self.assertRaisesRegex(ValueError,'positive semidefinite'):
            portfolio_variance({'a':.5,'b':.5},invalid)

if __name__=='__main__': unittest.main()
