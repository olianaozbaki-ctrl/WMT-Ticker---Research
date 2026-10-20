"""Calculate expected return, volatility, and reserves for simple portfolios."""

from math import sqrt


# Editable inputs ------------------------------------------------------------

SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {
        "expected_return": 0.050,
        "volatility": 0.060,
    },
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {
        "Treasury bills": 1.00,
        "Treasury 10-year note": 0.10,
        "Investment-grade bond fund": 0.05,
        "Global equity index fund": 0.00,
    },
    "Treasury 10-year note": {
        "Treasury bills": 0.10,
        "Treasury 10-year note": 1.00,
        "Investment-grade bond fund": 0.80,
        "Global equity index fund": -0.10,
    },
    "Investment-grade bond fund": {
        "Treasury bills": 0.05,
        "Treasury 10-year note": 0.80,
        "Investment-grade bond fund": 1.00,
        "Global equity index fund": 0.25,
    },
    "Global equity index fund": {
        "Treasury bills": 0.00,
        "Treasury 10-year note": -0.10,
        "Investment-grade bond fund": 0.25,
        "Global equity index fund": 1.00,
    },
}

OBJECTIVE_RETURN = 0.065
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


# Validation and calculations ------------------------------------------------

def validate_inputs(sleeves, correlations):
    """Raise ValueError when the correlation table is incomplete or invalid."""
    names = list(sleeves)

    if set(correlations) != set(names):
        raise ValueError("correlation table rows must match the sleeve names")

    for first in names:
        if set(correlations[first]) != set(names):
            raise ValueError(
                f"correlation table columns for {first!r} must match the sleeve names"
            )

        for second in names:
            correlation = correlations[first][second]
            if not -1.0 <= correlation <= 1.0:
                raise ValueError(
                    f"correlation for {first!r} and {second!r} must be between "
                    f"-1 and 1; received {correlation}"
                )
            if correlation != correlations[second][first]:
                raise ValueError(
                    f"correlation table is not symmetric for {first!r} and {second!r}"
                )


def build_covariance_matrix(sleeves, correlations):
    """Return covariance as correlation times both sleeves' volatilities."""
    return {
        first: {
            second: (
                correlations[first][second]
                * sleeves[first]["volatility"]
                * sleeves[second]["volatility"]
            )
            for second in sleeves
        }
        for first in sleeves
    }


def benchmark_weights(sleeves):
    """Return the 40% investment-grade bonds and 60% equity benchmark."""
    weights = {name: 0.0 for name in sleeves}
    weights["Investment-grade bond fund"] = 0.40
    weights["Global equity index fund"] = 0.60
    return weights


def equal_weights(sleeves):
    """Return equal weights for all sleeves."""
    weight = 1.0 / len(sleeves)
    return {name: weight for name in sleeves}


def inverse_volatility_weights(sleeves):
    """Return normalized weights proportional to inverse volatility."""
    inverse_volatilities = {
        name: 1.0 / values["volatility"] for name, values in sleeves.items()
    }
    total = sum(inverse_volatilities.values())
    return {name: value / total for name, value in inverse_volatilities.items()}


def expected_portfolio_return(weights, sleeves):
    """Return the weighted expected return."""
    return sum(
        weights[name] * sleeves[name]["expected_return"] for name in sleeves
    )


def portfolio_variance(weights, covariance_matrix):
    """Return portfolio variance, including every covariance term."""
    return sum(
        weights[first] * weights[second] * covariance_matrix[first][second]
        for first in weights
        for second in weights
    )


def portfolio_volatility(weights, covariance_matrix):
    """Return portfolio volatility as the square root of variance."""
    return sqrt(portfolio_variance(weights, covariance_matrix))


def reserve_eligible_weight(weights):
    """Return the combined weight of reserve-eligible sleeves."""
    return sum(weights[name] for name in RESERVE_ELIGIBLE)


def meets_objective(expected_return, objective_return=OBJECTIVE_RETURN):
    """Return whether expected return is at least the objective return."""
    return expected_return >= objective_return


def create_portfolios(sleeves):
    """Return the three requested simple portfolios."""
    return {
        "Benchmark": benchmark_weights(sleeves),
        "Equal weight": equal_weights(sleeves),
        "Inverse volatility": inverse_volatility_weights(sleeves),
    }


def print_portfolio(name, weights, sleeves, covariance_matrix):
    """Calculate and print all requested results for one portfolio."""
    portfolio_return = expected_portfolio_return(weights, sleeves)
    volatility = portfolio_volatility(weights, covariance_matrix)
    reserve_weight = reserve_eligible_weight(weights)

    print(f"\n{name}")
    print("  Weights:")
    for sleeve, weight in weights.items():
        print(f"    {sleeve}: {weight:.1%}")
    print(f"  Expected return: {portfolio_return:.2%}")
    print(f"  Volatility: {volatility:.2%}")
    print(f"  Reserve-eligible weight: {reserve_weight:.1%}")
    print(
        f"  Meets {OBJECTIVE_RETURN:.1%} objective: "
        f"{'yes' if meets_objective(portfolio_return) else 'no'}"
    )


def main():
    """Validate inputs, calculate the portfolios, and print their results."""
    try:
        validate_inputs(SLEEVES, CORRELATIONS)
        covariance_matrix = build_covariance_matrix(SLEEVES, CORRELATIONS)
        portfolios = create_portfolios(SLEEVES)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise SystemExit(f"Input error: {error}") from error

    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance_matrix)


if __name__ == "__main__":
    main()
