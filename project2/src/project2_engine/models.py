"""Typed records shared by the financial engine and mandate validator."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RuleStatus(str, Enum):
    """A rule is never silently treated as passing when evidence is unavailable."""

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_TESTABLE = "NOT_TESTABLE"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class AssetDefinition:
    """Mandate metadata needed to test an investable asset."""

    name: str
    issuer: Optional[str]
    liquidity_business_days: Optional[int]
    reserve_eligible: Optional[bool]


@dataclass(frozen=True)
class RuleResult:
    """One transparent mandate verdict with its evidence and feasibility role."""

    rule_id: str
    label: str
    status: RuleStatus
    measured_value: Optional[float]
    limit_value: Optional[float]
    units: str
    explanation: str
    required_for_feasibility: bool
