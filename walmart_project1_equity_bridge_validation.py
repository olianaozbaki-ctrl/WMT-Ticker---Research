"""Independent known-answer enterprise-to-equity bridge validation.

This script intentionally does not import the Walmart valuation models. It
checks the bridge arithmetic using a synthetic known answer and then applies
the same independently defined formula to the supplied rounded Walmart V2
values. USD millions except per-share amounts.
"""
from __future__ import annotations

from dataclasses import dataclass


TOLERANCE = 1e-9


@dataclass(frozen=True)
class BridgeInputs:
    enterprise_value: float
    cash: float
    debt: float
    finance_leases: float
    noncontrolling_interest: float
    diluted_shares: float


def calculate_bridge(inputs: BridgeInputs) -> tuple[float, float]:
    """Return equity value and value per diluted share."""
    if inputs.diluted_shares <= 0.0:
        raise ValueError("Diluted shares must be positive")
    equity_value = (
        inputs.enterprise_value
        + inputs.cash
        - inputs.debt
        - inputs.finance_leases
        - inputs.noncontrolling_interest
    )
    return equity_value, equity_value / inputs.diluted_shares


def known_answer_test() -> tuple[float, float]:
    synthetic = BridgeInputs(
        enterprise_value=1_000.0,
        cash=100.0,
        debt=250.0,
        finance_leases=50.0,
        noncontrolling_interest=0.0,
        diluted_shares=100.0,
    )
    equity_value, per_share = calculate_bridge(synthetic)
    assert abs(equity_value - 800.0) <= TOLERANCE, (
        f"Synthetic equity value failed: {equity_value}"
    )
    assert abs(per_share - 8.0) <= TOLERANCE, (
        f"Synthetic per-share value failed: {per_share}"
    )
    return equity_value, per_share


def walmart_reported_values_test() -> tuple[float, float]:
    # NCI is set to zero only to reproduce the supplied provisional V2 bridge,
    # which does not provide a separate NCI deduction. This is not verification
    # that Walmart has no NCI claim.
    walmart = BridgeInputs(
        enterprise_value=326_976.2,
        cash=10_727.0,
        debt=44_762.0,
        finance_leases=6_761.0,
        noncontrolling_interest=0.0,
        diluted_shares=8_022.0,
    )
    equity_value, per_share = calculate_bridge(walmart)
    expected_equity_from_displayed_values = 286_180.2
    expected_displayed_per_share = 35.67
    assert abs(equity_value - expected_equity_from_displayed_values) <= TOLERANCE
    assert round(per_share, 2) == expected_displayed_per_share
    return equity_value, per_share


def main() -> None:
    synthetic_equity, synthetic_per_share = known_answer_test()
    walmart_equity, walmart_per_share = walmart_reported_values_test()

    print("WALMART PROJECT 1 -- INDEPENDENT EQUITY-BRIDGE VALIDATION")
    print("USD millions except per-share amounts")
    print("Model imports: none")
    print("\nSynthetic known-answer test")
    print("Formula: EV + cash - debt - finance leases - NCI")
    print(f"Equity value: ${synthetic_equity:,.6f}M | expected $800.000000M | difference $0.000000M")
    print(f"Value/share: ${synthetic_per_share:.6f} | expected $8.000000 | difference $0.000000")
    print("Assertions: PASS")

    displayed_per_share = 35.67
    print("\nWalmart V2 supplied rounded-value reconciliation")
    print("$326,976.2M + $10,727.0M - $44,762.0M - $6,761.0M - $0.0M")
    print(f"Equity value: ${walmart_equity:,.6f}M")
    print(f"Value/share: ${walmart_per_share:.9f}")
    print(f"Value/share rounded to cents: ${walmart_per_share:.2f}")
    print("Equity-value arithmetic difference: $0.000000M")
    print(
        "Per-share difference from displayed $35.67: "
        f"${walmart_per_share - displayed_per_share:+.9f} before rounding; $0.00 after rounding"
    )
    print("Assertions: PASS")
    print("Failures: none")


if __name__ == "__main__":
    main()
