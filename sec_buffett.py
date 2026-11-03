#!/usr/bin/env python3
"""Deterministic SEC EDGAR calculations for FIN 43900 Lab 18."""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    import certifi
except ImportError:  # pragma: no cover - system trust store is the fallback
    certifi = None


TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
ANNUAL_MIN_DAYS = 330
ANNUAL_MAX_DAYS = 380  # includes 52- and 53-week fiscal years

TAG_PRIORITIES = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    ],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
    ],
    "equity": ["StockholdersEquity"],
}

FLOW_FIELDS = {
    "revenue",
    "net_income",
    "operating_cash_flow",
    "capital_spending",
}

FIELD_LABELS = {
    "revenue": "Revenue",
    "net_income": "Net income",
    "operating_cash_flow": "Operating cash flow",
    "capital_spending": "Capital spending",
    "equity": "Equity",
    "roe": "ROE",
    "owner_earnings": "Owner earnings",
}

CHECK_LABELS = {
    "roe_15_every_year": "ROE of at least 15% every year",
    "positive_owner_earnings_every_year": "Positive owner earnings every year",
    "owner_earnings_growth": "Growth in owner earnings from first to last year",
}


class EdgarError(RuntimeError):
    """Readable error for SEC retrieval or parsing failures."""


def make_user_agent(name: str, email: str) -> str:
    """Build a compliant, descriptive SEC User-Agent without storing it."""
    clean_name = " ".join(name.split())
    clean_email = email.strip()
    if not clean_name:
        raise ValueError("SEC contact name is required; do not invent one.")
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", clean_email):
        raise ValueError("A valid SEC contact email is required; do not invent one.")
    return f"{clean_name} {clean_email} FIN 43900 educational analysis"


def runtime_user_agent() -> str:
    """Read identity from the environment, or ask in an interactive terminal."""
    name = os.environ.get("SEC_EDGAR_NAME", "").strip()
    email = os.environ.get("SEC_EDGAR_EMAIL", "").strip()
    if (not name or not email) and sys.stdin.isatty():
        name = name or input("SEC contact name: ").strip()
        email = email or input("SEC contact email: ").strip()
    if not name or not email:
        raise ValueError(
            "Set SEC_EDGAR_NAME and SEC_EDGAR_EMAIL. Personal contact information "
            "is required at runtime and is not stored in this repository."
        )
    return make_user_agent(name, email)


def sec_json(url: str, user_agent: str, timeout: int = 30) -> dict[str, Any]:
    """Download JSON from SEC EDGAR with its required identifying header."""
    request = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "application/json",
            "Accept-Encoding": "identity",
        },
    )
    ssl_context = (
        ssl.create_default_context(cafile=certifi.where())
        if certifi is not None
        else ssl.create_default_context()
    )
    try:
        with urlopen(request, timeout=timeout, context=ssl_context) as response:
            return json.load(response)
    except HTTPError as exc:
        raise EdgarError(f"SEC EDGAR returned HTTP {exc.code} for {url}") from exc
    except URLError as exc:
        raise EdgarError(f"Could not reach SEC EDGAR: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise EdgarError(f"SEC EDGAR did not return valid JSON for {url}") from exc


def ticker_to_cik(ticker: str, tickers: dict[str, Any]) -> tuple[int, str]:
    """Return CIK and SEC company title for a ticker."""
    wanted = ticker.strip().upper()
    for record in tickers.values():
        if str(record.get("ticker", "")).upper() == wanted:
            return int(record["cik_str"]), str(record.get("title", wanted))
    raise EdgarError(f"Ticker {wanted!r} was not found in the SEC ticker file.")


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def is_one_year_fact(fact: dict[str, Any]) -> bool:
    """Accept one-year duration facts, including 52- and 53-week fiscal years."""
    try:
        days = (parse_iso_date(fact["end"]) - parse_iso_date(fact["start"])).days
    except (KeyError, TypeError, ValueError):
        return False
    return ANNUAL_MIN_DAYS <= days <= ANNUAL_MAX_DAYS


def tag_facts(company_facts: dict[str, Any], tag: str) -> list[dict[str, Any]]:
    """Return USD facts for one us-gaap tag, or an empty list."""
    tag_data = company_facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
    units = tag_data.get("units", {})
    return list(units.get("USD", []))


def eligible_facts(
    company_facts: dict[str, Any], tag: str, *, flow: bool
) -> list[dict[str, Any]]:
    """Apply the Lab 18 form and annual-period filters."""
    eligible: list[dict[str, Any]] = []
    for index, fact in enumerate(tag_facts(company_facts, tag)):
        if fact.get("form") != "10-K" or "end" not in fact or "val" not in fact:
            continue
        if flow and not is_one_year_fact(fact):
            continue
        copy = dict(fact)
        copy["_source_index"] = index
        eligible.append(copy)
    return eligible


def latest_filing(facts: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Choose the latest filing when the same period appears more than once."""
    if not facts:
        return None
    return max(
        facts,
        key=lambda fact: (
            str(fact.get("filed", "")),
            str(fact.get("accn", "")),
            int(fact.get("_source_index", -1)),
        ),
    )


def fiscal_year_ends(company_facts: dict[str, Any]) -> list[str]:
    """Find the five latest annual fiscal-period ends from required flow tags."""
    ends: set[str] = set()
    for field in FLOW_FIELDS:
        for tag in TAG_PRIORITIES[field]:
            for fact in eligible_facts(company_facts, tag, flow=True):
                ends.add(str(fact["end"]))
    return sorted(ends)[-5:]


def select_value(
    company_facts: dict[str, Any], field: str, fiscal_end: str
) -> dict[str, Any]:
    """Apply tag priority, then latest-filing selection, for one fiscal year."""
    flow = field in FLOW_FIELDS
    for tag in TAG_PRIORITIES[field]:
        matches = [
            fact
            for fact in eligible_facts(company_facts, tag, flow=flow)
            if str(fact.get("end")) == fiscal_end
        ]
        chosen = latest_filing(matches)
        if chosen is not None:
            return {
                "value": chosen["val"],
                "tag": tag,
                "filed": chosen.get("filed"),
                "accession": chosen.get("accn"),
                "start": chosen.get("start"),
                "end": chosen.get("end"),
            }
    return {"value": None, "tag": None}


def calculated_value(value: float | int | None, tag: str | None) -> dict[str, Any]:
    return {"value": value, "tag": tag}


def build_year_row(company_facts: dict[str, Any], fiscal_end: str) -> dict[str, Any]:
    """Turn EDGAR facts into one fiscal-year row using only Lab 18 formulas."""
    row: dict[str, Any] = {"fiscal_year_end": fiscal_end}
    for field in TAG_PRIORITIES:
        row[field] = select_value(company_facts, field, fiscal_end)

    net_income = row["net_income"]["value"]
    equity = row["equity"]["value"]
    if net_income is None or equity is None or equity <= 0:
        row["roe"] = calculated_value(None, None)
    else:
        row["roe"] = calculated_value(
            float(net_income) / float(equity),
            f"calculated: {row['net_income']['tag']} / {row['equity']['tag']}",
        )

    cash_flow = row["operating_cash_flow"]["value"]
    capital_spending = row["capital_spending"]["value"]
    if cash_flow is None or capital_spending is None:
        row["owner_earnings"] = calculated_value(None, None)
    else:
        row["owner_earnings"] = calculated_value(
            cash_flow - capital_spending,
            "calculated: "
            f"{row['operating_cash_flow']['tag']} - {row['capital_spending']['tag']}",
        )
    return row


def buffett_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Compute the three required checks; missing inputs produce not known."""
    checks = {key: "not known" for key in CHECK_LABELS}
    if len(rows) != 5:
        return checks

    roes = [row["roe"]["value"] for row in rows]
    owners = [row["owner_earnings"]["value"] for row in rows]

    if all(value is not None for value in roes):
        checks["roe_15_every_year"] = (
            "pass" if all(value >= 0.15 for value in roes) else "fail"
        )
    if all(value is not None for value in owners):
        checks["positive_owner_earnings_every_year"] = (
            "pass" if all(value > 0 for value in owners) else "fail"
        )
        checks["owner_earnings_growth"] = (
            "pass" if owners[-1] > owners[0] else "fail"
        )
    return checks


def analyze_company_facts(
    ticker: str, cik: int, company_name: str, company_facts: dict[str, Any]
) -> dict[str, Any]:
    """Create the complete serializable analysis from downloaded facts."""
    ends = fiscal_year_ends(company_facts)
    rows = [build_year_row(company_facts, fiscal_end) for fiscal_end in ends]
    return {
        "ticker": ticker.upper(),
        "company_name": company_name,
        "cik": cik,
        "units": "USD; displayed financial statement values are USD millions",
        "rows": rows,
        "checks": buffett_checks(rows),
        "source": "SEC EDGAR company facts; 10-K only",
    }


def fetch_analysis(ticker: str, user_agent: str) -> dict[str, Any]:
    """Retrieve SEC ticker mapping and company facts, then calculate results."""
    ticker = ticker.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.-]{1,10}", ticker):
        raise ValueError("Enter a valid ticker containing letters, digits, dot, or hyphen.")
    tickers = sec_json(TICKERS_URL, user_agent)
    cik, company_name = ticker_to_cik(ticker, tickers)
    company_facts = sec_json(FACTS_URL.format(cik=cik), user_agent)
    return analyze_company_facts(ticker, cik, company_name, company_facts)


def money_millions(value: float | int | None) -> str:
    return "not found" if value is None else f"{value / 1_000_000:,.0f}"


def percent(value: float | None) -> str:
    return "not known" if value is None else f"{value * 100:.1f}%"


def display_tag(item: dict[str, Any]) -> str:
    return str(item.get("tag") or "not found")


def markdown_report(analysis: dict[str, Any]) -> str:
    """Render exactly what the model and student should use for the memo."""
    lines = [
        f"# Deterministic Buffett Data: {analysis['ticker']}",
        "",
        "Financial statement values are USD millions.",
        "",
        "| Fiscal year end | Revenue | Net income | Operating cash flow | "
        "Capital spending | Equity | ROE | Owner earnings |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in analysis["rows"]:
        lines.append(
            "| {date} | {revenue} | {net_income} | {cash_flow} | {capex} | "
            "{equity} | {roe} | {owner} |".format(
                date=row["fiscal_year_end"],
                revenue=money_millions(row["revenue"]["value"]),
                net_income=money_millions(row["net_income"]["value"]),
                cash_flow=money_millions(row["operating_cash_flow"]["value"]),
                capex=money_millions(row["capital_spending"]["value"]),
                equity=money_millions(row["equity"]["value"]),
                roe=percent(row["roe"]["value"]),
                owner=money_millions(row["owner_earnings"]["value"]),
            )
        )

    lines.extend(["", "## XBRL tags used", ""])
    for row in analysis["rows"]:
        lines.append(f"### {row['fiscal_year_end']}")
        for field in (
            "revenue",
            "net_income",
            "operating_cash_flow",
            "capital_spending",
            "equity",
            "roe",
            "owner_earnings",
        ):
            lines.append(f"- {FIELD_LABELS[field]}: `{display_tag(row[field])}`")
        lines.append("")

    lines.extend(["## Buffett checks", ""])
    for key, label in CHECK_LABELS.items():
        lines.append(f"- {label}: **{analysis['checks'][key]}**")
    return "\n".join(lines).rstrip() + "\n"


NUMBER_RE = re.compile(
    r"(?<![\w.-])(?:\d{4}-\d{2}-\d{2}|\$?-?\d[\d,]*(?:\.\d+)?%?)"
)


def number_key(token: str) -> tuple[Any, ...] | None:
    """Normalize number formatting while keeping percentages and dates distinct."""
    cleaned = token.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", cleaned):
        return "date", cleaned
    is_percent = cleaned.endswith("%")
    cleaned = cleaned.rstrip("%").lstrip("$").replace(",", "")
    try:
        return "number", Decimal(cleaned).normalize(), is_percent
    except InvalidOperation:
        return None


def printed_number_keys(analysis: dict[str, Any]) -> set[tuple[Any, ...]]:
    """Numbers present in the human-readable script report."""
    report = markdown_report(analysis)
    keys = {number_key(token) for token in NUMBER_RE.findall(report)}
    return {key for key in keys if key is not None}


def unsupported_memo_numbers(memo: str, analysis: dict[str, Any]) -> list[str]:
    """Flag every memo number absent from the deterministic printed report."""
    allowed = printed_number_keys(analysis)
    unsupported: list[str] = []
    for token in NUMBER_RE.findall(memo):
        if number_key(token) not in allowed and token not in unsupported:
            unsupported.append(token)
    return unsupported


def write_json(path: Path, analysis: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysis, indent=2) + "\n", encoding="utf-8")


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", help="SEC ticker symbol, for example COST")
    parser.add_argument("--json-output", type=Path, help="Optional analysis JSON path")
    parser.add_argument(
        "--validate-memo",
        type=Path,
        help="Optional Markdown memo whose numbers should be checked",
    )
    args = parser.parse_args()

    try:
        analysis = fetch_analysis(args.ticker, runtime_user_agent())
        print(markdown_report(analysis), end="")
        if args.json_output:
            write_json(args.json_output, analysis)
        if args.validate_memo:
            memo = args.validate_memo.read_text(encoding="utf-8")
            unsupported = unsupported_memo_numbers(memo, analysis)
            if unsupported:
                print("\nUnsupported memo numbers: " + ", ".join(unsupported))
                return 2
            print("\nMemo number validation: no unsupported numbers found")
        return 0
    except (EdgarError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(cli())
