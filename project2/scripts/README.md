# Scripts

- `python scripts/fetch_market_data.py` rebuilds processed files from the committed raw snapshot.
- `python scripts/fetch_market_data.py --refresh` deliberately refreshes Yahoo/FRED source files and rewrites provenance.
- `PYTHONPATH=src python scripts/generate_phase2_results.py` executes the tested analysis and writes the visible JSON and Markdown results without depending on editable-install state.
