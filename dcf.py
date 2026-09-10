import sys

# ==============================================================================
# SENSITIVITY AND REVERSE DCF INPUTS (Editable by hand)
# ==============================================================================
SENSITIVITY_WACCS = [0.06, 0.07, 0.08]
SENSITIVITY_TERMINAL_GROWTH_RATES = [0.02, 0.025, 0.03]
TARGET_SHARE_PRICE = 105.83                     # WMT close on September 9, 2026
REVERSE_SHIFT_LOWER = -0.05                     # -5 percentage points
REVERSE_SHIFT_UPPER = 0.25                      # +25 percentage points

# ==============================================================================
# INPUTS BLOCK (Editable by hand)
# ==============================================================================
FCFF_START = 17033.7                            # FY2026 FCFF in USD millions
GROWTH_RATES = [0.05, 0.045, 0.04, 0.035, 0.03]  # Growth rates for Years 1 to 5
WACC = 0.07                                     # Weighted Average Cost of Capital
G_TERMINAL = 0.025                              # Terminal growth rate
CASH = 10727.0                                  # Cash and equivalents, Jan. 31, 2026, USD millions
DEBT = 44762.0                                  # Borrowings and debt, Jan. 31, 2026, USD millions
SHARES = 8022.0                                 # FY2026 diluted weighted-average shares, millions

# ==============================================================================
# VALUATION COMPUTATION
# ==============================================================================

# Stop with a clear message if terminal growth >= WACC
if G_TERMINAL >= WACC:
    sys.exit(f"Error: Terminal growth ({G_TERMINAL:.4f}) must be strictly less than WACC ({WACC:.4f}).")

# 1. Forecast explicit FCFF for Years 1 to 5
fcff = []
cur_fcff = FCFF_START
for g in GROWTH_RATES:
    cur_fcff = cur_fcff * (1.0 + g)
    fcff.append(cur_fcff)

# 2. Present value of the five explicit FCFF (discounted at year-end)
pv_explicit = sum(cf / ((1.0 + WACC) ** (i + 1)) for i, cf in enumerate(fcff))

# 3. Gordon-growth terminal value at the end of Year 5: FCFF_6 / (WACC - g)
terminal_value = fcff[-1] * (1.0 + G_TERMINAL) / (WACC - G_TERMINAL)

# 4. Present value of terminal value discounted 5 years back to today
pv_terminal_value = terminal_value / ((1.0 + WACC) ** len(fcff))

# 5. Enterprise value = PV(explicit FCFF) + PV(terminal value)
enterprise_value = pv_explicit + pv_terminal_value

# 6. Equity value = Enterprise value + cash - debt
equity_value = enterprise_value + CASH - DEBT

# 7. Value per diluted share
value_per_share = equity_value / SHARES

# 8. Terminal value share of enterprise value
tv_share_ev = pv_terminal_value / enterprise_value

# ==============================================================================
# OUTPUT: TWELVE LABELLED LINES (To four decimals)
# ==============================================================================
for i, cf in enumerate(fcff):
    print(f"FCFF Year {i+1}: {cf:.4f}")
print(f"Present value of the five explicit FCFF: {pv_explicit:.4f}")
print(f"Terminal value at Year 5: {terminal_value:.4f}")
print(f"Present value of the terminal value: {pv_terminal_value:.4f}")
print(f"Enterprise value: {enterprise_value:.4f}")
print(f"Equity value: {equity_value:.4f}")
print(f"Value per diluted share: {value_per_share:.4f}")
print(f"Present value of the terminal value as a share of enterprise value: {tv_share_ev:.4f}")


def calculate_value_per_share(growth_rates, wacc, terminal_growth):
    """Return DCF value per diluted share for the supplied rate assumptions."""
    forecast_fcff = []
    current_fcff = FCFF_START
    for growth_rate in growth_rates:
        current_fcff *= 1.0 + growth_rate
        forecast_fcff.append(current_fcff)

    explicit_value = sum(
        cash_flow / ((1.0 + wacc) ** (year + 1))
        for year, cash_flow in enumerate(forecast_fcff)
    )
    terminal = (
        forecast_fcff[-1]
        * (1.0 + terminal_growth)
        / (wacc - terminal_growth)
    )
    terminal_present_value = terminal / ((1.0 + wacc) ** len(forecast_fcff))
    return (explicit_value + terminal_present_value + CASH - DEBT) / SHARES


# ==============================================================================
# OUTPUT: SENSITIVITY GRID
# ==============================================================================
print("\nSensitivity grid: value per diluted share")
row_label_width = 18
column_width = 12
header = f"{'Terminal growth':<{row_label_width}}" + "".join(
    f"WACC {wacc:.2%}".rjust(column_width) for wacc in SENSITIVITY_WACCS
)
print(header)
print("-" * len(header))
for terminal_growth in SENSITIVITY_TERMINAL_GROWTH_RATES:
    row = f"{terminal_growth:.2%}".ljust(row_label_width)
    for wacc in SENSITIVITY_WACCS:
        if terminal_growth >= wacc:
            cell = "INVALID"
        else:
            cell = f"{calculate_value_per_share(GROWTH_RATES, wacc, terminal_growth):.4f}"
        row += cell.rjust(column_width)
    print(row)


# ==============================================================================
# OUTPUT: REVERSE DCF
# ==============================================================================
print("\nReverse DCF")
print("Solved input: uniform shift added to all five explicit growth rates")
print(f"Target share price: {TARGET_SHARE_PRICE:.4f}")

held_fixed = (
    f"FCFF_START={FCFF_START:.4f}, WACC={WACC:.4%}, "
    f"G_TERMINAL={G_TERMINAL:.4%}, CASH={CASH:.4f}, DEBT={DEBT:.4f}, "
    f"SHARES={SHARES:.4f}, base GROWTH_RATES={GROWTH_RATES}"
)
print(f"Inputs held fixed: {held_fixed}")
print(
    f"Search bracket: {REVERSE_SHIFT_LOWER:+.4%} to "
    f"{REVERSE_SHIFT_UPPER:+.4%}"
)

lower_growth_rates = [growth + REVERSE_SHIFT_LOWER for growth in GROWTH_RATES]
upper_growth_rates = [growth + REVERSE_SHIFT_UPPER for growth in GROWTH_RATES]

if REVERSE_SHIFT_LOWER > REVERSE_SHIFT_UPPER:
    print("Solved shift: INVALID BRACKET")
    print("Reason: the lower bound must not exceed the upper bound.")
elif any(growth <= -1.0 for growth in lower_growth_rates + upper_growth_rates):
    print("Solved shift: INVALID BRACKET")
    print("Reason: the bracket pushes at least one annual growth rate to -100% or below.")
else:
    def reverse_dcf_difference(shift):
        shifted_growth_rates = [growth + shift for growth in GROWTH_RATES]
        return (
            calculate_value_per_share(shifted_growth_rates, WACC, G_TERMINAL)
            - TARGET_SHARE_PRICE
        )

    lower_difference = reverse_dcf_difference(REVERSE_SHIFT_LOWER)
    upper_difference = reverse_dcf_difference(REVERSE_SHIFT_UPPER)
    price_tolerance = 0.00000001

    if lower_difference * upper_difference > 0.0:
        print("Solved shift: NO SOLUTION IN BRACKET")
    elif abs(lower_difference) <= price_tolerance:
        print(f"Solved shift: {REVERSE_SHIFT_LOWER:+.6%}")
    elif abs(upper_difference) <= price_tolerance:
        print(f"Solved shift: {REVERSE_SHIFT_UPPER:+.6%}")
    else:
        lower = REVERSE_SHIFT_LOWER
        upper = REVERSE_SHIFT_UPPER
        for _ in range(100):
            midpoint = (lower + upper) / 2.0
            midpoint_difference = reverse_dcf_difference(midpoint)
            if abs(midpoint_difference) <= price_tolerance:
                break
            if lower_difference * midpoint_difference <= 0.0:
                upper = midpoint
            else:
                lower = midpoint
                lower_difference = midpoint_difference
        print(f"Solved shift: {midpoint:+.6%}")
