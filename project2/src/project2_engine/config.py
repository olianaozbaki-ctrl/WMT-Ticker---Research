"""Load and minimally validate the machine-readable Meridian mandate."""

import json
from pathlib import Path
from typing import Any, Mapping


REQUIRED_TOP_LEVEL_KEYS = {
    "mandate_name",
    "decision_context",
    "original_policy",
    "horizon_years",
    "objective",
    "reserve",
    "liquidity",
    "issuer_limit",
    "turnover",
    "restrictions",
    "risk",
    "costs",
    "benchmark",
    "allocation_ranges",
    "unresolved_decisions",
}


def validate_mandate_config(mandate: Mapping[str, Any]) -> None:
    """Raise ValueError when required mandate sections or units are invalid."""
    missing = REQUIRED_TOP_LEVEL_KEYS - set(mandate)
    if missing:
        raise ValueError(f"mandate configuration is missing: {sorted(missing)}")

    bounded_rates = {
        "reserve.minimum_weight": mandate["reserve"]["minimum_weight"],
        "liquidity.minimum_weight": mandate["liquidity"]["minimum_weight"],
        "issuer_limit.maximum_weight": mandate["issuer_limit"]["maximum_weight"],
        "turnover.maximum": mandate["turnover"]["maximum"],
    }
    for label, value in bounded_rates.items():
        if not isinstance(value, (int, float)) or not 0 <= value <= 1:
            raise ValueError(f"{label} must be a decimal rate between 0 and 1")

    if mandate["horizon_years"] <= 0:
        raise ValueError("horizon_years must be positive")
    if mandate["liquidity"]["maximum_business_days"] < 0:
        raise ValueError("maximum liquidity days cannot be negative")

    expected_policy_ids = {f"S{number}" for number in range(1, 11)}
    policy_ids = set(mandate["original_policy"]["statements"])
    if policy_ids != expected_policy_ids:
        raise ValueError("original_policy must preserve exactly S1 through S10")

    reserve = mandate["reserve"]
    calculated_reserve = (
        reserve["quarterly_distribution_usd_millions"]
        * reserve["quarters_to_cover"]
        / mandate["portfolio_size_usd_millions"]
    )
    if abs(calculated_reserve - reserve["minimum_weight"]) > 1e-12:
        raise ValueError(
            "reserve.minimum_weight must equal quarterly distribution times "
            "quarters to cover divided by portfolio size"
        )

    turnover = mandate["turnover"]
    hypothetical = turnover["illustrative_starting_allocation"]
    hypothetical_total = sum(hypothetical["weights"].values())
    if abs(hypothetical_total - 1.0) > 1e-12:
        raise ValueError("illustrative starting weights must sum to 100%")
    if not hypothetical["label"].lower().startswith("hypothetical"):
        raise ValueError("illustrative starting allocation must be labeled hypothetical")

    costs = mandate["costs"]
    sensitivity = costs["sensitivity_bps"]
    if costs["transaction_cost_bps"] not in sensitivity:
        raise ValueError("cost sensitivity must include the illustrative base cost")
    if any(value < 0 for value in sensitivity):
        raise ValueError("transaction-cost sensitivity values must be nonnegative")

    universe = {item["ticker"]: item for item in mandate["project_universe"]}
    if universe.get("BIL", {}).get("reserve_eligible") is not True:
        raise ValueError("BIL must be the designated reserve-eligible cash equivalent")
    if universe.get("IEF", {}).get("reserve_eligible") is not False:
        raise ValueError("IEF must not automatically count toward the reserve")


def load_mandate(path: Path | str) -> dict[str, Any]:
    """Read a JSON mandate after checking its required structure."""
    with Path(path).open(encoding="utf-8") as source:
        mandate = json.load(source)
    validate_mandate_config(mandate)
    return mandate
