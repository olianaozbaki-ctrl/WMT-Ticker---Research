import sys

# ==============================================================================
# INPUTS BLOCK (Editable by hand)
# ==============================================================================
FCFF_START = 100.0                              # Starting FCFF in USD millions
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]  # Growth rates for Years 1 to 5
WACC = 0.10                                     # Weighted Average Cost of Capital
G_TERMINAL = 0.03                               # Terminal growth rate
CASH = 50.0                                     # Non-operating cash in USD millions
DEBT = 300.0                                    # Debt in USD millions
SHARES = 50.0                                   # Diluted shares in millions

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
