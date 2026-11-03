# FIN 43900 Lab 18 — Warren Buffett Skill

The reusable Codex skill is in
`.codex/skills/warren-buffett-investing/`. Its Python script retrieves SEC EDGAR
company facts, applies the lab's fixed XBRL rules, and computes all financial
values and checks. Personal SEC contact information is supplied at runtime and
is not stored in the repository.

## Run the SEC analysis

In a terminal, set your SEC identity for that shell and run the initial COST
test. Replace the placeholders with your own name and email:

```bash
export SEC_EDGAR_NAME="Your Name"
export SEC_EDGAR_EMAIL="your_email@example.edu"
python .codex/skills/warren-buffett-investing/scripts/sec_buffett.py COST \
  --json-output lab18_output/COST_buffett_data.json
```

Then ask Codex to use `$warren-buffett-investing` on COST. The skill writes the
model's short, price-free memo to `lab18_output/COST_buffett_memo.md` and checks
the memo for unsupported numbers.

## Run the Streamlit app

```bash
python -m pip install -r requirements_lab18.txt
streamlit run lab18_buffett_app.py
```

Enter the SEC contact in the collapsed section if the environment variables
are not set, keep COST as the initial ticker, and select **Analyze five fiscal
years**. The app does not save the SEC contact fields.

## Run offline tests

```bash
python -m unittest -v test_lab18_buffett.py
```

The offline tests cover XBRL priority, latest-filing selection, missing-input
checks, and the hand-entered `40.0%` memo-number probe. Live COST and JPM results
must still be tested against the Lab 18 validation table before claiming the
full validation passes.

## Decision

I would trust the Costco verdict because the company consistently maintained strong ROE and positive owner earnings over the five-year period. However, I would still consider other factors before making a final investment decision.
