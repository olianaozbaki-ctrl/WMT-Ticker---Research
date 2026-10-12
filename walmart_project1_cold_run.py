"""Clean-process reproducibility harness for Walmart Project 1.

This additive harness runs existing scripts in isolated Python subprocesses,
captures their literal output, and records hashes for protected source files.
It does not import or alter the existing model modules in this process.
"""
from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOG_PATH = ROOT / "Walmart_Project1_Cold_Run.log"
PROTECTED_FILES = [
    "project1_fcff_v2.py",
    "project1_fcff_v3.py",
    "walmart_project1_proforma_v2.py",
    "walmart_project1_proforma_v3.py",
    "walmart_project1_v3_final_scenarios.py",
    "walmart_project1_reverse_dcf_v3.py",
    "walmart_project1_comparables_v3.py",
    "walmart_project1_equity_bridge_validation.py",
    "walmart_project1_revenue_growth_changed_input_test.py",
    "Walmart_Project_1_Edition_A.md",
    "Walmart_Project_1_Edition_B.md",
    "Walmart_Project1_Edition_B_Investment_Memo.md",
    "Walmart_Project1_Locked_Changed_Input_Record.md",
    "Walmart_Project1_Final_Valuation_Assumptions.md",
    "Walmart_Project1_WACC_Evidence.md",
    "Walmart_Project1_Equity_Bridge_Review.md",
    "Walmart_Project1_Final_Scenarios_and_Valuation_Range.md",
    "Walmart_Project1_Reverse_DCF_Evidence.md",
    "Walmart_Project1_Comparable_Valuation_Triangulation.md",
    "Walmart_Project1_Equity_Bridge_Validation.md",
    "Walmart_Project1_Independent_Source_Check.md",
    "Walmart_Project1_Model_Correction_Plan.md",
    "Walmart_Project1_Model_V3_Changes.md",
]
COMMANDS = [
    ("V3 pro-forma / balance-sheet and cash-flow controls", "walmart_project1_proforma_v3.py"),
    ("V3 FCFF base valuation / DCF controls", "project1_fcff_v3.py"),
    ("Final downside, base, upside scenario run", "walmart_project1_v3_final_scenarios.py"),
    ("Reverse DCF run", "walmart_project1_reverse_dcf_v3.py"),
    ("Comparable valuation run", "walmart_project1_comparables_v3.py"),
    ("Synthetic known-answer bridge and supplied V2 arithmetic", "walmart_project1_equity_bridge_validation.py"),
    ("Locked changed-input test (V2 one-point growth reduction)", "walmart_project1_revenue_growth_changed_input_test.py"),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot() -> dict[str, str]:
    return {
        name: sha256(ROOT / name)
        for name in PROTECTED_FILES
        if (ROOT / name).is_file()
    }


def run_one(title: str, filename: str) -> tuple[str, int, str]:
    command = [sys.executable, "-B", filename]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    block = [f"### {title}", f"Command: {' '.join(command)}", f"Exit code: {result.returncode}"]
    block.append(result.stdout.rstrip() if result.stdout.strip() else "[no stdout]")
    return "\n".join(block), result.returncode, result.stdout


def main() -> int:
    before = snapshot()
    sections = [
        "WALMART PROJECT 1 — COLD RUN LOG",
        f"Run timestamp (UTC): {datetime.now(timezone.utc).isoformat()}",
        f"Python: {platform.python_version()} ({sys.executable})",
        f"Platform: {platform.platform()}",
        "Dependency basis: Python standard library plus existing local V2/V3 project modules; no network access or third-party package installation.",
        "Harness command: python3 -B walmart_project1_cold_run.py",
        "Subprocess policy: each listed command ran in a fresh interpreter with bytecode writing disabled.",
        "",
    ]
    outcomes: list[tuple[str, int, str]] = []
    for title, filename in COMMANDS:
        outcome = run_one(title, filename)
        outcomes.append(outcome)
        sections.append(outcome[0])
        sections.append("")

    after = snapshot()
    changed = [name for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)]
    sections.extend(["### Protected-file integrity", "SHA-256 before/after:"])
    for name in sorted(set(before) | set(after)):
        sections.append(f"{name}: {before.get(name, 'MISSING')} -> {after.get(name, 'MISSING')}")
    if changed:
        sections.append("Integrity status: FAIL — changed or missing protected files: " + ", ".join(changed))
    else:
        sections.append(f"Integrity status: PASS — {len(before)} protected files unchanged.")

    failed_commands = [title for title, code, _ in outcomes if code != 0]
    sections.append("Command status: " + ("FAIL — " + ", ".join(failed_commands) if failed_commands else "PASS — all commands exited 0."))
    sections.append("Interpretation: process exit and model assertions test arithmetic/reproducibility only; they do not independently verify economic assumptions, filing transcription, data provenance, or valuation-date completeness.")
    log_text = "\n".join(sections).rstrip() + "\n"
    LOG_PATH.write_text(log_text, encoding="utf-8")
    print(log_text)
    return 1 if failed_commands or changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
