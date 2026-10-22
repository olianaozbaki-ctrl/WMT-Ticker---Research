"""Calculate expected return, volatility, and reserves for simple portfolios."""

import csv
from datetime import datetime
from io import StringIO
from math import sqrt
from statistics import mean, stdev


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


def _weight_combinations(asset_count, units_remaining, prefix=()):
    """Yield every nonnegative integer allocation summing to units_remaining."""
    if asset_count == 1:
        yield prefix + (units_remaining,)
        return

    for units in range(units_remaining + 1):
        yield from _weight_combinations(
            asset_count - 1,
            units_remaining - units,
            prefix + (units,),
        )


def search_lowest_risk_mix(
    sleeves,
    correlations,
    objective_return=OBJECTIVE_RETURN,
    reserve_minimum=0.03,
    reserve_eligible=RESERVE_ELIGIBLE,
    step_percent=5,
):
    """Return the least-volatile feasible long-only mix on a fixed grid.

    The result contains weights, expected return, volatility, and the
    reserve-eligible weight. Return ``None`` when the grid has no feasible mix.
    """
    if not sleeves:
        raise ValueError("at least one asset is required")
    if step_percent <= 0 or 100 % step_percent != 0:
        raise ValueError("step_percent must be a positive divisor of 100")
    if not 0 <= reserve_minimum <= 1:
        raise ValueError("reserve_minimum must be between 0 and 1")

    validate_inputs(sleeves, correlations)
    names = list(sleeves)
    unknown_reserve_assets = set(reserve_eligible) - set(names)
    if unknown_reserve_assets:
        raise ValueError(
            "reserve-eligible assets are not in sleeves: "
            + ", ".join(sorted(unknown_reserve_assets))
        )

    covariance_matrix = build_covariance_matrix(sleeves, correlations)
    total_units = 100 // step_percent
    best = None

    for units in _weight_combinations(len(names), total_units):
        weights = {
            name: unit / total_units for name, unit in zip(names, units)
        }
        portfolio_return = expected_portfolio_return(weights, sleeves)
        reserve_weight = sum(weights[name] for name in reserve_eligible)
        if portfolio_return + 1e-12 < objective_return:
            continue
        if reserve_weight + 1e-12 < reserve_minimum:
            continue

        volatility = portfolio_volatility(weights, covariance_matrix)
        if best is None or volatility < best["volatility"]:
            best = {
                "weights": weights,
                "expected_return": portfolio_return,
                "volatility": volatility,
                "reserve_eligible_weight": reserve_weight,
            }

    return best


def _parse_month(value):
    """Parse common ISO and U.S. date formats for order validation."""
    value = value.strip()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        pass

    for date_format in ("%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d", "%Y-%m"):
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            continue
    raise ValueError(f"unrecognized date {value!r}")


def _read_csv_text(csv_source):
    """Return text from a path, text/bytes stream, or raw bytes."""
    if isinstance(csv_source, (str, bytes)):
        if isinstance(csv_source, str):
            with open(csv_source, encoding="utf-8-sig", newline="") as source:
                return source.read()
        return csv_source.decode("utf-8-sig")

    csv_source.seek(0)
    content = csv_source.read()
    if isinstance(content, bytes):
        return content.decode("utf-8-sig")
    return content


def estimate_from_price_csv(csv_source, last_36_months=False):
    """Estimate annual inputs from monthly prices in an oldest-first CSV.

    The first column must contain dates and all later columns asset prices.
    Returns use adjacent prices. Expected returns are arithmetic monthly means
    times 12, volatilities are sample monthly standard deviations times sqrt(12),
    and correlations use the same selected monthly-return observations.
    """
    reader = csv.reader(StringIO(_read_csv_text(csv_source)))
    try:
        header = next(reader)
    except StopIteration as error:
        raise ValueError("the CSV is empty") from error

    if len(header) < 2:
        raise ValueError("the CSV needs a date column and at least one asset")
    asset_names = [name.strip() for name in header[1:]]
    if any(not name for name in asset_names) or len(set(asset_names)) != len(asset_names):
        raise ValueError("asset column names must be nonblank and unique")

    dates = []
    prices = {name: [] for name in asset_names}
    for row_number, row in enumerate(reader, start=2):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != len(header):
            raise ValueError(f"row {row_number} has {len(row)} columns; expected {len(header)}")
        dates.append(_parse_month(row[0]))
        for name, value in zip(asset_names, row[1:]):
            try:
                price = float(value)
            except ValueError as error:
                raise ValueError(
                    f"row {row_number}, {name}: price must be numeric"
                ) from error
            if price <= 0:
                raise ValueError(f"row {row_number}, {name}: price must be positive")
            prices[name].append(price)

    if len(dates) < 3:
        raise ValueError("at least three monthly price rows are required")
    if any(later <= earlier for earlier, later in zip(dates, dates[1:])):
        raise ValueError("dates must be strictly increasing (oldest first)")

    monthly_returns = {
        name: [later / earlier - 1 for earlier, later in zip(values, values[1:])]
        for name, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {
            name: values[-36:] for name, values in monthly_returns.items()
        }

    observation_count = len(next(iter(monthly_returns.values())))
    if observation_count < 2:
        raise ValueError("at least two monthly returns are required")

    monthly_means = {name: mean(values) for name, values in monthly_returns.items()}
    monthly_volatilities = {
        name: stdev(values) for name, values in monthly_returns.items()
    }
    sleeves = {
        name: {
            "expected_return": monthly_means[name] * 12,
            "volatility": monthly_volatilities[name] * sqrt(12),
        }
        for name in asset_names
    }

    correlations = {}
    for first in asset_names:
        correlations[first] = {}
        for second in asset_names:
            if first == second:
                correlation = 1.0
            elif monthly_volatilities[first] == 0 or monthly_volatilities[second] == 0:
                raise ValueError("correlations are undefined for an asset with zero volatility")
            else:
                covariance = sum(
                    (first_value - monthly_means[first])
                    * (second_value - monthly_means[second])
                    for first_value, second_value in zip(
                        monthly_returns[first], monthly_returns[second]
                    )
                ) / (observation_count - 1)
                correlation = covariance / (
                    monthly_volatilities[first] * monthly_volatilities[second]
                )
                correlation = max(-1.0, min(1.0, correlation))
            correlations[first][second] = correlation

    validate_inputs(sleeves, correlations)
    return sleeves, correlations


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
