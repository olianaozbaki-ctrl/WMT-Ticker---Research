"""Formatting helpers for configuration-derived reporting labels."""

from __future__ import annotations


def percentage_points(value: float) -> str:
    """Format a decimal spread as percentage points without needless zeros."""
    return f"{value * 100:.10f}".rstrip("0").rstrip(".") + "%"


def cpi_objective_label(real_return_spread: float) -> str:
    """Return the configured CPI-plus-spread label used in modeled outputs."""
    return f"CPI + {percentage_points(real_return_spread)}"
