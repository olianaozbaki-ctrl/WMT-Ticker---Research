# Meridian Foundation Investment Management Application

**AI use:** OpenAI Codex was used for Phase 1 software architecture, documentation, and test scaffolding. The analysis and investment decision remain the student's responsibility.

**Educational project only; not investment advice.**

## Phase 1 status

This directory contains the initial financial engine and mandate-validation framework for FIN 43900 Project 2. It does not contain a final portfolio, recommendation, cold-run record, or Locked Changed-Input Record.

The application is being designed to support this committee decision:

> Should the Meridian Foundation reject, pilot, or adopt the proposed constrained ETF allocation process and, if piloted or adopted, what allocation ranges should the committee authorize?

## Current structure

- `config/mandate.json` — machine-readable Meridian mandate and policy status.
- `src/project2_engine/` — reusable calculations, configuration loading, and rule-level mandate validation.
- `tests/` — deterministic known-answer tests using synthetic fixtures, not investment results.
- `docs/financial-conventions.md` — measurement conventions and unresolved CIO decisions.
- `docs/mandate-review.md` — line-by-line separation of original policy and Project 2 modeling assumptions.
- `docs/validation-and-ai-use.md` — working validation and AI-use record.
- `docs/decision-memo.md` — Phase 1 placeholder; no recommendation has been made.
- `data/` — reserved for traceable raw and processed data.
- `outputs/` — reserved for code-generated visible output.

## Setup and Phase 1 tests

From `project2/`:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m unittest discover -s tests -v
```

To open the Phase 1 application shell:

```bash
python -m streamlit run app.py
```

The app intentionally shows the mandate and unresolved decisions only. It does not present preliminary calculations as a final recommendation.

## Remaining unresolved controls

- Actual Meridian holdings and their as-of date; until supplied, equal weight is hypothetical and illustrative only.
- Observed or committee-approved trading-cost evidence to replace the illustrative 10 bps assumption.
- The analysis decision date and admissible CPIAUCSL observation/availability dates.
- Independent five-business-day liquidity evidence for all four ETFs.
- CIO measurement and handling of S9; it remains `UNRESOLVED`, not a hard prohibition.
- Confirmation that the official case's issuer exemptions govern despite their omission from the local `Lab_13.md` wording.

## Reproducibility boundary

All rates use decimal units internally: `0.065` means 6.5%, and `10` transaction-cost basis points means `0.001` per unit of turnover. No final data or output should be added manually; later phases will generate visible output from the same tested engine used by the app.
