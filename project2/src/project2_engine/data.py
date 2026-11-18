"""Validated loaders and estimators for dated Phase 2 inputs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from math import isfinite
from pathlib import Path
from statistics import mean


@dataclass(frozen=True)
class MarketEstimates:
    tickers: tuple[str, ...]
    observation_dates: tuple[date, ...]
    monthly_returns: dict[str, tuple[float, ...]]
    annual_expected_returns: dict[str, float]
    annual_covariance: dict[str, dict[str, float]]


def load_monthly_prices(path: Path | str) -> tuple[tuple[date, ...], dict[str, tuple[float, ...]]]:
    """Load a complete, strictly increasing adjusted-price panel."""
    with Path(path).open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or reader.fieldnames[0] != "observation_date":
            raise ValueError("first CSV column must be observation_date")
        tickers = tuple(reader.fieldnames[1:])
        if not tickers or len(set(tickers)) != len(tickers):
            raise ValueError("price CSV must contain unique ticker columns")
        dates: list[date] = []
        values = {ticker: [] for ticker in tickers}
        for row_number, row in enumerate(reader, start=2):
            if any(row.get(name) in (None, "") for name in reader.fieldnames):
                raise ValueError(f"missing value in price CSV row {row_number}")
            observation = date.fromisoformat(row["observation_date"])
            if dates and observation <= dates[-1]:
                raise ValueError("observation dates must be unique and strictly increasing")
            dates.append(observation)
            for ticker in tickers:
                value = float(row[ticker])
                if not isfinite(value) or value <= 0:
                    raise ValueError(f"{ticker} price must be finite and positive")
                values[ticker].append(value)
    if len(dates) < 2:
        raise ValueError("at least two price observations are required")
    return tuple(dates), {name: tuple(series) for name, series in values.items()}


def estimate_from_monthly_prices(path: Path | str) -> MarketEstimates:
    """Estimate arithmetic annual returns and annual covariance from monthly prices."""
    dates, prices = load_monthly_prices(path)
    tickers = tuple(prices)
    returns = {
        ticker: tuple(
            prices[ticker][index] / prices[ticker][index - 1] - 1.0
            for index in range(1, len(dates))
        )
        for ticker in tickers
    }
    sample_size = len(dates) - 1
    if sample_size < 2:
        raise ValueError("at least two monthly returns are required for covariance")
    expected = {ticker: mean(returns[ticker]) * 12.0 for ticker in tickers}
    covariance: dict[str, dict[str, float]] = {}
    for first in tickers:
        covariance[first] = {}
        first_mean = mean(returns[first])
        for second in tickers:
            second_mean = mean(returns[second])
            monthly_covariance = sum(
                (left - first_mean) * (right - second_mean)
                for left, right in zip(returns[first], returns[second])
            ) / (sample_size - 1)
            covariance[first][second] = monthly_covariance * 12.0
    return MarketEstimates(tickers, dates, returns, expected, covariance)


def load_cpi_yoy(path: Path | str, current: str, prior: str) -> float:
    """Compute a decimal year-over-year change from two nonmissing CPI observations."""
    values: dict[str, float] = {}
    with Path(path).open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            if row["CPIAUCSL"]:
                values[row["observation_date"]] = float(row["CPIAUCSL"])
    if current not in values or prior not in values:
        raise ValueError("both requested CPI observations must be available")
    if values[current] <= 0 or values[prior] <= 0:
        raise ValueError("CPI levels must be positive")
    return values[current] / values[prior] - 1.0
