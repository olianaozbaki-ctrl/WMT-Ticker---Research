"""Check the Meridian Foundation candidate portfolios against its mandate."""


# Editable inputs ------------------------------------------------------------

HOLDINGS = {
    "Cash": {
        "issuer": "none",
        "redemption_days": 0,
        "reserve_eligible": True,
    },
    "Treasury bills": {
        "issuer": "U.S. Treasury",
        "redemption_days": 1,
        "reserve_eligible": True,
    },
    "Treasury 10-year note": {
        "issuer": "U.S. Treasury",
        "redemption_days": 1,
        "reserve_eligible": True,
    },
    "Global equity index fund": {
        "issuer": "diversified fund",
        "redemption_days": 2,
        "reserve_eligible": False,
    },
    "Investment-grade bond fund": {
        "issuer": "diversified fund",
        "redemption_days": 3,
        "reserve_eligible": False,
    },
    "Private real estate fund": {
        "issuer": "diversified fund",
        "redemption_days": 90,
        "reserve_eligible": False,
    },
    "Acme Corp bonds": {
        "issuer": "Acme Corp",
        "redemption_days": 4,
        "reserve_eligible": False,
    },
    "Acme Corp stock": {
        "issuer": "Acme Corp",
        "redemption_days": 1,
        "reserve_eligible": False,
    },
}

CANDIDATES = {
    "A": {
        "Cash": 2,
        "Treasury bills": 2,
        "Treasury 10-year note": 10,
        "Global equity index fund": 60,
        "Investment-grade bond fund": 26,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
    "B": {
        "Cash": 1,
        "Treasury bills": 0,
        "Treasury 10-year note": 0,
        "Global equity index fund": 55,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 15,
        "Acme Corp bonds": 5,
        "Acme Corp stock": 4,
    },
    "C": {
        "Cash": 1,
        "Treasury bills": 1,
        "Treasury 10-year note": 0,
        "Global equity index fund": 70,
        "Investment-grade bond fund": 20,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 8,
    },
    "D": {
        "Cash": 3,
        "Treasury bills": 0,
        "Treasury 10-year note": 97,
        "Global equity index fund": 0,
        "Investment-grade bond fund": 0,
        "Private real estate fund": 0,
        "Acme Corp bonds": 0,
        "Acme Corp stock": 0,
    },
}

RESERVE_SIZE_MILLIONS = 100
QUARTERLY_DISTRIBUTION_MILLIONS = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW_DAYS = 5
MINIMUM_LIQUID_SHARE_PERCENT = 90
ISSUER_LIMIT_PERCENT = 8
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


# Calculations ---------------------------------------------------------------

def status(passed):
    """Return the required display label for a Boolean result."""
    return "pass" if passed else "FAIL"


def reserve_minimum_percent():
    """Return the required payout reserve as a percent of the portfolio."""
    required_distributions = QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION_MILLIONS
    return required_distributions / RESERVE_SIZE_MILLIONS * 100


def reserve_eligible_weight(weights):
    return sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["reserve_eligible"]
    )


def liquid_weight(weights):
    return sum(
        weight
        for holding, weight in weights.items()
        if HOLDINGS[holding]["redemption_days"] <= LIQUIDITY_WINDOW_DAYS
    )


def largest_company_weight(weights):
    """Aggregate nonexempt holdings by issuer and return the largest weight."""
    company_weights = {}
    for holding, weight in weights.items():
        issuer = HOLDINGS[holding]["issuer"]
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] = company_weights.get(issuer, 0) + weight
    return max(company_weights.values(), default=0)


def check_candidate(name, weights, reserve_minimum):
    total_weight = sum(weights.values())
    lowest_weight = min(weights.values())
    reserve_weight = reserve_eligible_weight(weights)
    five_day_liquid_weight = liquid_weight(weights)
    company_weight = largest_company_weight(weights)

    checks = [
        ("Weights sum to 100", total_weight, total_weight == 100),
        ("Long-only (lowest weight)", lowest_weight, lowest_weight >= 0),
        (
            f"Reserve >= {reserve_minimum:.1f}%",
            reserve_weight,
            reserve_weight >= reserve_minimum,
        ),
        (
            f"Redeemable in {LIQUIDITY_WINDOW_DAYS} days "
            f">= {MINIMUM_LIQUID_SHARE_PERCENT:.1f}%",
            five_day_liquid_weight,
            five_day_liquid_weight >= MINIMUM_LIQUID_SHARE_PERCENT,
        ),
        (
            f"Largest single company <= {ISSUER_LIMIT_PERCENT:.1f}%",
            company_weight,
            company_weight <= ISSUER_LIMIT_PERCENT,
        ),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, measured_value, passed in checks:
        print(f"  {label}: {measured_value:.1f}% {status(passed)}")
        if not passed:
            failures += 1

    print("  Calendar-year loss: requires CIO clarification")
    if failures == 0:
        print("  Verdict: passes every checkable rule")
    else:
        print(f"  Verdict: fails {failures} rule(s)")


def main():
    reserve_minimum = reserve_minimum_percent()
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
