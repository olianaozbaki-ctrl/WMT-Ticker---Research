# Walmart Project 1 — Independent Enterprise-to-Equity Bridge Validation

**Purpose:** Validate enterprise-to-equity bridge arithmetic independently of the Walmart model code. This evidence does not select a final bridge or verify the economic classification, source, or valuation-date suitability of any Walmart input.

**Validation script:** `walmart_project1_equity_bridge_validation.py`

**Existing files preserved:** The original model files and `Walmart_Project1_Locked_Changed_Input_Record.md` were not changed.

## Independent formula

All monetary amounts are USD millions.

```text
Equity value = Enterprise value
             + Cash
             − Debt
             − Finance leases
             − Noncontrolling interest

Value per diluted share = Equity value / Diluted shares
```

The validation script defines this formula itself and intentionally imports no Walmart pro-forma, FCFF, or scenario model.

## Synthetic known-answer test

| Input | Amount |
|---|---:|
| Enterprise value | $1,000 million |
| Cash | 100 million |
| Debt | (250) million |
| Finance leases | (50) million |
| Noncontrolling interest | $0 million |
| Diluted shares | 100 million |

Calculation:

```text
$1,000 + $100 − $250 − $50 − $0 = $800 million equity value
$800 / 100 million shares = $8.00 per share
```

| Test | Expected | Actual | Difference | Result |
|---|---:|---:|---:|---|
| Equity value | $800.000000M | $800.000000M | $0.000000M | **PASS** |
| Value per share | $8.000000 | $8.000000 | $0.000000 | **PASS** |

Both results are enforced with Python assertions using a `1e-9` tolerance.

## Walmart V2 reported-value reconciliation

The following calculation uses the supplied displayed values, not hidden adjustments or substituted amounts.

| Bridge item | Supplied amount | Treatment |
|---|---:|---|
| Enterprise value | $326,976.2M | Starting value |
| Cash | 10,727.0M | Added |
| Debt | (44,762.0)M | Subtracted |
| Finance leases | (6,761.0)M | Subtracted |
| Noncontrolling interest | $0.0M | No separate deduction in the supplied provisional bridge |
| Diluted shares | 8,022.0M | Per-share denominator |

Calculation:

```text
$326,976.2 + $10,727.0 − $44,762.0 − $6,761.0 − $0.0
= $286,180.2 million equity value

$286,180.2 / 8,022.0
= $35.674420344 per diluted share
= $35.67 per diluted share when rounded to cents
```

| Reconciliation | Implied expected value | Independently calculated | Arithmetic difference | Result |
|---|---:|---:|---:|---|
| Equity value | $286,180.200000M | $286,180.200000M | $0.000000M | **PASS** |
| Value per share, unrounded | — | $35.674420344 | — | Calculated |
| Value per share, displayed | $35.67 | $35.67 | $0.00 | **PASS** |

The unrounded calculated value is **$0.004420344 above** the displayed $35.67 figure. This is not an arithmetic failure: both values round to $35.67 at two decimal places. The supplied enterprise value is itself rounded to one decimal place, so this check should not be used to reconstruct more precision than the inputs contain.

## Execution output

Command:

```text
PYTHONDONTWRITEBYTECODE=1 python3 walmart_project1_equity_bridge_validation.py
```

Recorded output:

```text
WALMART PROJECT 1 -- INDEPENDENT EQUITY-BRIDGE VALIDATION
USD millions except per-share amounts
Model imports: none

Synthetic known-answer test
Formula: EV + cash - debt - finance leases - NCI
Equity value: $800.000000M | expected $800.000000M | difference $0.000000M
Value/share: $8.000000 | expected $8.000000 | difference $0.000000
Assertions: PASS

Walmart V2 supplied rounded-value reconciliation
$326,976.2M + $10,727.0M - $44,762.0M - $6,761.0M - $0.0M
Equity value: $286,180.200000M
Value/share: $35.674420344
Value/share rounded to cents: $35.67
Equity-value arithmetic difference: $0.000000M
Per-share difference from displayed $35.67: $+0.004420344 before rounding; $0.00 after rounding
Assertions: PASS
Failures: none
```

## Remaining limitations

This test verifies arithmetic only. It does not resolve the following valuation-policy and evidence questions:

1. **Enterprise-value precision:** $326,976.2 million is a displayed, rounded result. A calculation using the model's full-precision enterprise value can differ slightly below the displayed precision.
2. **Cash treatment:** the check assumes all $10,727 million is available to equity holders. It does not distinguish restricted, trapped, operational, or excess cash.
3. **Debt scope and date:** the $44,762 million measure is accepted as supplied. The test does not verify its valuation date, market value, or completeness relative to borrowings, supplier finance, derivatives, or other financing claims.
4. **Lease consistency:** finance leases are deducted because they are supplied as a separate claim. The test does not resolve operating-lease treatment or whether lease effects are fully consistent between enterprise value, FCFF, and the bridge.
5. **Noncontrolling interests:** zero is used only to reproduce the supplied provisional bridge, which has no separate NCI deduction. It does **not** establish that Walmart has no redeemable or nonredeemable NCI claim or that any such claim is immaterial.
6. **Other nonoperating assets and claims:** the bridge includes no separate adjustment for investments, unconsolidated interests, pension or other claims, or other nonoperating assets because no amounts were supplied for this test.
7. **Share denominator:** 8,022 million shares is accepted as supplied. The test does not determine whether historical weighted-average diluted shares, valuation-date shares outstanding, or a fully diluted treasury-stock-method count is the appropriate denominator.
8. **Source verification:** passing assertions prove formula implementation and arithmetic, not that the underlying amounts are independently sourced, consistently dated, or appropriate for a final September 23, 2026 valuation bridge.

Accordingly, the bridge arithmetic is validated, while the final economic bridge policy remains provisional.
