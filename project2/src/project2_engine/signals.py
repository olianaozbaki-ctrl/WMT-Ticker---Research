"""Point-in-time DGS10 signal with explicit observation and availability dates."""

from __future__ import annotations

from datetime import date
import csv
from pathlib import Path


def load_dgs10_signal(path: str | Path, decision_date: str) -> dict[str, object]:
    decision = date.fromisoformat(decision_date)
    eligible = []
    with Path(path).open(newline="", encoding="utf-8") as source:
        for row in csv.DictReader(source):
            observation = date.fromisoformat(row["observation_date"])
            availability = date.fromisoformat(row["availability_date"])
            value = row["DGS10"]
            if not value or availability > decision or observation > decision:
                continue
            eligible.append((availability, observation, float(value)))
    if not eligible:
        return {
            "available": False,
            "decision_date": decision.isoformat(),
            "observation_date": None,
            "availability_date": None,
            "value_percent": None,
            "interpretation": "No eligible DGS10 observation; signal is unavailable.",
            "action": "No signal-driven portfolio change; retain base process and report unavailable.",
        }
    availability, observation, value = max(eligible)
    return {
        "available": True,
        "series_id": "DGS10",
        "source": "Board of Governors of the Federal Reserve System, H.15, via FRED/ALFRED",
        "source_url": "https://fred.stlouisfed.org/series/DGS10",
        "decision_date": decision.isoformat(),
        "observation_date": observation.isoformat(),
        "availability_date": availability.isoformat(),
        "value_percent": value,
        "units": "percent, not seasonally adjusted",
        "interpretation": "10-year Treasury constant-maturity yield; descriptive macro regime indicator, not a return forecast.",
        "action": "Modeling assumption: use as a review trigger only; do not alter weights automatically. Rerun rates-sensitive valuation and approved stresses when elevated or materially changed.",
    }
