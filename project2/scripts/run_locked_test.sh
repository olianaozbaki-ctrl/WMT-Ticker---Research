#!/bin/zsh

(
  set -euo pipefail

  PROJECT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
  EXPECTED_COMMIT='1fd3c8ba1895424dcea5a0c1eb76f4934f09f346'
  RUN_DIR='outputs/locked-changed-input-test-1fd3c8b'

  cd "$PROJECT_DIR"

  [[ "$(git rev-parse HEAD)" == "$EXPECTED_COMMIT" ]] || {
    echo "STOP: HEAD is not prediction commit $EXPECTED_COMMIT"
    exit 1
  }

  [[ -z "$(git status --porcelain -- . ':(exclude)scripts/run_locked_test.sh')" ]] || {
    echo "STOP: working tree is not clean"
    git status --short
    exit 1
  }

  [[ ! -e "$RUN_DIR" ]] || {
    echo "STOP: $RUN_DIR already exists; preserve or rename it before rerunning"
    exit 1
  }

  output_names=(
    phase2_results.json
    phase2_results.md
    phase4a_decision_support.json
    phase4a_decision_support.md
  )

  mkdir -p "$RUN_DIR/baseline" "$RUN_DIR/changed-input"
  cp config/mandate.json "$RUN_DIR/mandate.original.json"

  for output_name in "${output_names[@]}"; do
    cp "outputs/$output_name" "$RUN_DIR/baseline/$output_name"
  done

  (
    cd "$RUN_DIR/baseline"
    shasum -a 256 "${output_names[@]}" > SHA256SUMS
  )

  restore_originals() {
    cp "$RUN_DIR/mandate.original.json" config/mandate.json
    for output_name in "${output_names[@]}"; do
      cp "$RUN_DIR/baseline/$output_name" "outputs/$output_name"
    done
  }
  trap restore_originals EXIT HUP INT TERM

  python - <<'PY'
from pathlib import Path

path = Path("config/mandate.json")
original = path.read_text(encoding="utf-8")
old = '"real_return_spread": 0.04'
new = '"real_return_spread": 0.05'

if original.count(old) != 1:
    raise SystemExit(
        f"STOP: expected exactly one occurrence of {old!r}; "
        f"found {original.count(old)}"
    )

path.write_text(original.replace(old, new), encoding="utf-8")
PY

  python - <<'PY'
import json
from pathlib import Path

mandate = json.loads(Path("config/mandate.json").read_text(encoding="utf-8"))
assert mandate["objective"]["real_return_spread"] == 0.05
print("Verified reserved input: objective.real_return_spread = 0.05")
PY

  git diff -- config/mandate.json

  [[ "$(git diff --name-only)" == "project2/config/mandate.json" ]] || {
    echo "STOP: an unexpected tracked file changed before execution"
    git diff --name-only
    exit 1
  }

  cp config/mandate.json "$RUN_DIR/changed-input/mandate.json"

  PYTHONPATH=src python scripts/generate_phase2_results.py

  for output_name in "${output_names[@]}"; do
    cp "outputs/$output_name" "$RUN_DIR/changed-input/$output_name"
  done

  (
    cd "$RUN_DIR/changed-input"
    shasum -a 256 mandate.json "${output_names[@]}" > SHA256SUMS
  )

  restore_originals
  trap - EXIT HUP INT TERM

  python - <<'PY'
import json
from pathlib import Path

mandate = json.loads(Path("config/mandate.json").read_text(encoding="utf-8"))
assert mandate["objective"]["real_return_spread"] == 0.04
print("Verified restoration: objective.real_return_spread = 0.04")
PY

  for output_name in "${output_names[@]}"; do
    cmp -s "outputs/$output_name" "$RUN_DIR/baseline/$output_name"
  done

  git diff --exit-code -- \
    config/mandate.json \
    outputs/phase2_results.json \
    outputs/phase2_results.md \
    outputs/phase4a_decision_support.json \
    outputs/phase4a_decision_support.md \
    docs/locked-changed-input-record.md

  echo "Run complete."
  echo "Baseline copies:      $RUN_DIR/baseline/"
  echo "Changed-input copies: $RUN_DIR/changed-input/"
  echo "Tracked files have been restored."
  git status --short
)
