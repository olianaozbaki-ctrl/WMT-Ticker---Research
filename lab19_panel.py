#!/usr/bin/env python3
"""Three-investor SEC EDGAR panel for FIN 43900 Lab 19."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
BUFFETT_SCRIPTS = ROOT / ".codex" / "skills" / "warren-buffett-investing" / "scripts"
sys.path.insert(0, str(BUFFETT_SCRIPTS))

import sec_buffett  # noqa: E402


EXTRA_TAG_PRIORITIES = {
    "liabilities": ["Liabilities"],
    "assets_current": ["AssetsCurrent"],
    "liabilities_current": ["LiabilitiesCurrent"],
    "research_and_development": [
        "ResearchAndDevelopmentExpense",
        "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost",
    ],
}
EXTRA_FLOW_FIELDS = {"research_and_development"}

BUFFETT_CHECK_LABELS = sec_buffett.CHECK_LABELS
WOOD_CHECK_LABELS = {
    "innovation_exposure": "Disruptive-innovation exposure established",
    "revenue_growth": "Revenue grew from first to last year",
    "reported_rd_latest": "Latest reported R&D expense is positive",
}
BURRY_CHECK_LABELS = {
    "operating_cash_flow_covers_net_income": (
        "Operating cash flow at least net income every year"
    ),
    "liabilities_no_more_than_twice_equity": (
        "Latest liabilities no more than twice equity"
    ),
}

NUMBER_RE = re.compile(
    r"(?<![\w.-])(?:\d{4}-\d{2}-\d{2}|\$?-?\d[\d,]*(?:\.\d+)?%?)"
)


def select_extra_value(
    company_facts: dict[str, Any], field: str, fiscal_end: str
) -> dict[str, Any]:
    """Select one added SEC fact using Lab 18 period and priority rules."""
    flow = field in EXTRA_FLOW_FIELDS
    for tag in EXTRA_TAG_PRIORITIES[field]:
        matches = [
            fact
            for fact in sec_buffett.eligible_facts(company_facts, tag, flow=flow)
            if str(fact.get("end")) == fiscal_end
        ]
        chosen = sec_buffett.latest_filing(matches)
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


def ratio_value(
    numerator: float | int | None,
    denominator: float | int | None,
    tag: str,
) -> dict[str, Any]:
    """Calculate a ratio, preserving missing and nonpositive-denominator gaps."""
    if numerator is None or denominator is None or denominator <= 0:
        return {"value": None, "tag": None}
    return {"value": float(numerator) / float(denominator), "tag": tag}


def wood_checks(
    rows: list[dict[str, Any]], innovation_exposure: bool | None = None
) -> dict[str, str]:
    """Compute the course's transparent Wood-inspired operational checks."""
    checks = {key: "not known" for key in WOOD_CHECK_LABELS}
    if innovation_exposure is not None:
        checks["innovation_exposure"] = (
            "pass" if innovation_exposure else "fail"
        )
    if len(rows) != 5:
        return checks

    first_revenue = rows[0]["revenue"]["value"]
    latest_revenue = rows[-1]["revenue"]["value"]
    if first_revenue is not None and latest_revenue is not None:
        checks["revenue_growth"] = (
            "pass" if latest_revenue > first_revenue else "fail"
        )

    latest_rd = rows[-1]["research_and_development"]["value"]
    if latest_rd is not None:
        checks["reported_rd_latest"] = "pass" if latest_rd > 0 else "fail"
    return checks


def burry_checks(rows: list[dict[str, Any]]) -> dict[str, str]:
    """Compute the two Lab 19 Burry checks."""
    checks = {key: "not known" for key in BURRY_CHECK_LABELS}
    if len(rows) != 5:
        return checks

    cash_flow = [row["operating_cash_flow"]["value"] for row in rows]
    net_income = [row["net_income"]["value"] for row in rows]
    if all(value is not None for value in cash_flow + net_income):
        checks["operating_cash_flow_covers_net_income"] = (
            "pass"
            if all(cash >= income for cash, income in zip(cash_flow, net_income))
            else "fail"
        )

    latest_ratio = rows[-1]["liabilities_to_equity"]["value"]
    if latest_ratio is not None:
        checks["liabilities_no_more_than_twice_equity"] = (
            "pass" if latest_ratio <= 2.0 else "fail"
        )
    return checks


def verdict(checks: dict[str, str], investor: str) -> str:
    """Translate deterministic checks into a concise price-free verdict."""
    results = list(checks.values())
    if any(result == "not known" for result in results):
        return "not known"
    if investor == "Buffett":
        return "own the business" if all(r == "pass" for r in results) else "pass"
    if investor == "Wood":
        return "innovation screen passes" if all(r == "pass" for r in results) else "watch it"
    return "financial checks pass" if all(r == "pass" for r in results) else "forensic concern"


def augment_buffett_analysis(
    buffett_analysis: dict[str, Any],
    company_facts: dict[str, Any],
    innovation_exposure: bool | None = None,
) -> dict[str, Any]:
    """Add Wood and Burry facts and checks to a Buffett analysis."""
    analysis = copy.deepcopy(buffett_analysis)
    for row in analysis["rows"]:
        fiscal_end = row["fiscal_year_end"]
        for field in EXTRA_TAG_PRIORITIES:
            row[field] = select_extra_value(company_facts, field, fiscal_end)
        row["current_ratio"] = ratio_value(
            row["assets_current"]["value"],
            row["liabilities_current"]["value"],
            "calculated: AssetsCurrent / LiabilitiesCurrent",
        )
        row["liabilities_to_equity"] = ratio_value(
            row["liabilities"]["value"],
            row["equity"]["value"],
            "calculated: Liabilities / StockholdersEquity",
        )

    panel_checks = {
        "Buffett": analysis["checks"],
        "Wood": wood_checks(analysis["rows"], innovation_exposure),
        "Burry": burry_checks(analysis["rows"]),
    }
    analysis["wood_framework_note"] = (
        "Course operational interpretation; not official ARK Invest rules"
    )
    analysis["panel_checks"] = panel_checks
    analysis["verdicts"] = {
        investor: verdict(checks, investor)
        for investor, checks in panel_checks.items()
    }
    analysis["source"] = "SEC EDGAR company facts; 10-K only"
    return analysis


def analyze_company_facts(
    ticker: str,
    cik: int,
    company_name: str,
    company_facts: dict[str, Any],
    innovation_exposure: bool | None = None,
) -> dict[str, Any]:
    """Run all three investors on one downloaded SEC company-facts document."""
    buffett = sec_buffett.analyze_company_facts(
        ticker, cik, company_name, company_facts
    )
    return augment_buffett_analysis(buffett, company_facts, innovation_exposure)


def fetch_panel_analysis(
    ticker: str, user_agent: str
) -> dict[str, Any]:
    """Retrieve SEC facts once, then run all three investor frameworks."""
    ticker = ticker.strip().upper()
    if not re.fullmatch(r"[A-Z0-9.-]{1,10}", ticker):
        raise ValueError("Enter a valid ticker containing letters, digits, dot, or hyphen.")
    tickers = sec_buffett.sec_json(sec_buffett.TICKERS_URL, user_agent)
    cik, company_name = sec_buffett.ticker_to_cik(ticker, tickers)
    company_facts = sec_buffett.sec_json(
        sec_buffett.FACTS_URL.format(cik=cik), user_agent
    )
    return analyze_company_facts(
        ticker,
        cik,
        company_name,
        company_facts,
    )


def load_offline_costco() -> dict[str, Any]:
    """Reproduce the known answer from saved SEC-derived Costco facts."""
    buffett_path = ROOT / "lab18_output" / "COST_buffett_data.json"
    balance_path = ROOT / "lab19_fixtures" / "COST_balance_facts.json"
    buffett = json.loads(buffett_path.read_text(encoding="utf-8"))
    balance_facts = json.loads(balance_path.read_text(encoding="utf-8"))
    return augment_buffett_analysis(buffett, balance_facts)


def money_millions(value: float | int | None) -> str:
    return sec_buffett.money_millions(value)


def ratio(value: float | None) -> str:
    return "not known" if value is None else f"{value:.2f}"


def panel_markdown_report(analysis: dict[str, Any]) -> str:
    """Print every number that the three memos may use."""
    lines = [
        f"# Deterministic Investor Panel Data: {analysis['ticker']}",
        "",
        "Financial statement values are USD millions.",
        "Wood checks are a course operational interpretation, not official ARK rules.",
        "Burry liabilities-to-equity threshold: 2.0.",
        "",
        "| Fiscal year end | Revenue | Net income | Operating cash flow | "
        "Capital spending | Reported R&D | Equity | Owner earnings | ROE | "
        "Liabilities | Liabilities / equity |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in analysis["rows"]:
        lines.append(
            "| {date} | {revenue} | {net_income} | {cash_flow} | {capex} | "
            "{rd} | {equity} | {owner} | {roe} | {liabilities} | {leverage} |".format(
                date=row["fiscal_year_end"],
                revenue=money_millions(row["revenue"]["value"]),
                net_income=money_millions(row["net_income"]["value"]),
                cash_flow=money_millions(row["operating_cash_flow"]["value"]),
                capex=money_millions(row["capital_spending"]["value"]),
                rd=money_millions(row["research_and_development"]["value"]),
                equity=money_millions(row["equity"]["value"]),
                owner=money_millions(row["owner_earnings"]["value"]),
                roe=sec_buffett.percent(row["roe"]["value"]),
                liabilities=money_millions(row["liabilities"]["value"]),
                leverage=ratio(row["liabilities_to_equity"]["value"]),
            )
        )

    labels = {
        "Buffett": BUFFETT_CHECK_LABELS,
        "Wood": WOOD_CHECK_LABELS,
        "Burry": BURRY_CHECK_LABELS,
    }
    lines.extend(["", "## Panel checks", ""])
    for investor in ("Buffett", "Wood", "Burry"):
        lines.append(f"### {investor}")
        for key, label in labels[investor].items():
            lines.append(
                f"- {label}: **{analysis['panel_checks'][investor][key]}**"
            )
        lines.append(f"- Verdict: **{analysis['verdicts'][investor]}**")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_memos(analysis: dict[str, Any]) -> dict[str, str]:
    """Create three independent, price-free memos from printed values only."""
    ticker = analysis["ticker"]
    rows = analysis["rows"]
    first = rows[0]
    latest = rows[-1]
    wood_results = analysis["panel_checks"]["Wood"]
    burry_results = analysis["panel_checks"]["Burry"]

    innovation_text = {
        "pass": "Disruptive-innovation exposure was established outside the numeric filing data.",
        "fail": "Disruptive-innovation exposure was not established by the supplied evidence.",
        "not known": (
            "Disruptive-innovation exposure cannot be established from SEC "
            "company-facts numbers, so it remains not known."
        ),
    }[wood_results["innovation_exposure"]]

    revenue_result = wood_results["revenue_growth"]
    if revenue_result == "pass":
        revenue_text = (
            f"Revenue increased from ${money_millions(first['revenue']['value'])} "
            f"million to ${money_millions(latest['revenue']['value'])} million, "
            "so the operational revenue-scaling check passes."
        )
    elif revenue_result == "fail":
        revenue_text = (
            f"Revenue did not increase from ${money_millions(first['revenue']['value'])} "
            f"million to ${money_millions(latest['revenue']['value'])} million, "
            "so the operational revenue-scaling check fails."
        )
    else:
        revenue_text = "The first-to-last revenue-scaling check is not known."

    rd_result = wood_results["reported_rd_latest"]
    if rd_result == "pass":
        rd_text = (
            f"Latest reported R&D expense was "
            f"${money_millions(latest['research_and_development']['value'])} million, "
            "so the reported-R&D check passes."
        )
    elif rd_result == "fail":
        rd_text = (
            f"Latest reported R&D expense was "
            f"${money_millions(latest['research_and_development']['value'])} million, "
            "so the reported-R&D check fails."
        )
    else:
        rd_text = (
            "The latest reported R&D expense was not found, so the reported-R&D "
            "check is not known."
        )

    cash_flow_result = burry_results[
        "operating_cash_flow_covers_net_income"
    ]
    if cash_flow_result == "pass":
        cash_flow_text = (
            "Operating cash flow was at least net income in every reported year. "
            f"In the latest year, it was "
            f"${money_millions(latest['operating_cash_flow']['value'])} million "
            f"versus net income of ${money_millions(latest['net_income']['value'])} "
            "million."
        )
    elif cash_flow_result == "fail":
        cash_flow_text = (
            "Operating cash flow was not at least net income in every reported "
            "year. In the latest year, operating cash flow was "
            f"${money_millions(latest['operating_cash_flow']['value'])} million "
            f"versus net income of ${money_millions(latest['net_income']['value'])} "
            "million."
        )
    else:
        cash_flow_text = (
            "The cash-flow coverage check is not known because at least one "
            "required operating cash flow or net income value was not found."
        )

    leverage_result = burry_results[
        "liabilities_no_more_than_twice_equity"
    ]
    if leverage_result == "pass":
        leverage_text = (
            "The latest liabilities-to-equity ratio is "
            f"{ratio(latest['liabilities_to_equity']['value'])}, at or below the "
            "2.0 limit."
        )
    elif leverage_result == "fail":
        leverage_text = (
            "The latest liabilities-to-equity ratio is "
            f"{ratio(latest['liabilities_to_equity']['value'])}, above the 2.0 "
            "limit."
        )
    else:
        leverage_text = (
            "The latest liabilities-to-equity ratio was not available, so the "
            "leverage check is not known."
        )

    burry_summary = {
        ("pass", "pass"): "Both forensic checks pass.",
        ("pass", "fail"): (
            "The cash-flow coverage check passes, but the leverage check fails."
        ),
        ("fail", "pass"): (
            "The cash-flow coverage check fails, but the leverage check passes."
        ),
        ("fail", "fail"): "Both forensic checks fail.",
        ("pass", "not known"): (
            "The cash-flow coverage check passes, and the leverage check is not known."
        ),
        ("fail", "not known"): (
            "The cash-flow coverage check fails, and the leverage check is not known."
        ),
        ("not known", "pass"): (
            "The cash-flow coverage check is not known, and the leverage check passes."
        ),
        ("not known", "fail"): (
            "The cash-flow coverage check is not known, and the leverage check fails."
        ),
        ("not known", "not known"): "Both forensic checks are not known.",
    }[(cash_flow_result, leverage_result)]

    buffett = (
        f"# Buffett-Style Investment Memo: {ticker}\n\n"
        f"**Verdict: {analysis['verdicts']['Buffett']}**\n\n"
        "ROE was at least 15.0% in every reported year, and owner earnings "
        "were positive in every year. "
        f"Owner earnings increased from ${money_millions(first['owner_earnings']['value'])} "
        f"million to ${money_millions(latest['owner_earnings']['value'])} million.\n\n"
        "All Buffett checks pass. This is a business-quality judgment only "
        "and does not address the market price.\n"
    )

    wood = (
        f"# Cathie Wood-Inspired Investment Memo: {ticker}\n\n"
        f"**Verdict: {analysis['verdicts']['Wood']}**\n\n"
        f"{innovation_text}\n\n"
        f"{revenue_text}\n\n"
        f"{rd_text}\n\n"
        "This is a course operational interpretation, not an official ARK "
        "Invest screen. The missing innovation evidence requires "
        "company-specific research.\n"
    )

    burry = (
        f"# Michael Burry Investment Memo: {ticker}\n\n"
        f"**Verdict: {analysis['verdicts']['Burry']}**\n\n"
        f"{cash_flow_text} {leverage_text}\n\n"
        f"{burry_summary} These checks do not replace a full "
        "footnote review and do not address the market price.\n"
    )
    return {"Buffett": buffett, "Wood": wood, "Burry": burry}


def number_key(token: str) -> tuple[Any, ...] | None:
    """Normalize dates, percentages, currency, commas, and decimals."""
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
    report = panel_markdown_report(analysis)
    keys = {number_key(token) for token in NUMBER_RE.findall(report)}
    return {key for key in keys if key is not None}


def unsupported_memo_numbers(
    memo: str, analysis: dict[str, Any]
) -> list[str]:
    """Return memo numbers not present in the deterministic panel report."""
    allowed = printed_number_keys(analysis)
    unsupported: list[str] = []
    for token in NUMBER_RE.findall(memo):
        if number_key(token) not in allowed and token not in unsupported:
            unsupported.append(token)
    return unsupported


def audit_all_memos(
    memos: dict[str, str], analysis: dict[str, Any]
) -> dict[str, list[str]]:
    """Run one number audit across all three independent memos."""
    return {
        investor: unsupported_memo_numbers(memo, analysis)
        for investor, memo in memos.items()
    }


def write_json(path: Path, analysis: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(analysis, indent=2) + "\n", encoding="utf-8")


def write_memos(directory: Path, ticker: str, memos: dict[str, str]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    names = {"Buffett": "buffett", "Wood": "wood", "Burry": "burry"}
    for investor, memo in memos.items():
        path = directory / f"{ticker}_{names[investor]}_memo.md"
        path.write_text(memo.rstrip() + "\n", encoding="utf-8")


def cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ticker", nargs="?", default="COST")
    parser.add_argument("--offline-costco", action="store_true")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--memo-dir", type=Path)
    args = parser.parse_args()

    try:
        if args.offline_costco:
            if args.ticker.upper() != "COST":
                raise ValueError("--offline-costco can only be used with COST.")
            analysis = load_offline_costco()
        else:
            analysis = fetch_panel_analysis(
                args.ticker,
                sec_buffett.runtime_user_agent(),
            )

        memos = build_memos(analysis)
        audit = audit_all_memos(memos, analysis)
        print(panel_markdown_report(analysis), end="")
        if args.json_output:
            write_json(args.json_output, analysis)
        if args.memo_dir:
            write_memos(args.memo_dir, analysis["ticker"], memos)
        unsupported = {
            investor: numbers for investor, numbers in audit.items() if numbers
        }
        if unsupported:
            for investor, numbers in unsupported.items():
                print(f"{investor} unsupported memo numbers: {', '.join(numbers)}")
            return 2
        print("Memo number validation: all three memos passed")
        return 0
    except (OSError, ValueError, sec_buffett.EdgarError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(cli())
