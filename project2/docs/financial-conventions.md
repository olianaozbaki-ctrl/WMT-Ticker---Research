# Phase 1 Financial Conventions

This document resolves calculation conventions where the Meridian mandate is sufficiently clear and explicitly marks policy decisions that remain unresolved. Exact original S1-S10 language is stored separately under `original_policy` in `config/mandate.json`; the conventions below are Project 2 modeling assumptions, not rewritten client policy. It contains no final investment results.

## Decision and optimization

- Committee decision: reject, pilot, or adopt the constrained allocation process; if approved, authorize allocation ranges.
- Approved Project 2 modeling objective: minimize estimated annualized volatility subject to the return target and every applicable model-feasibility rule. Lab 13 did not originally specify an objective.
- A portfolio is model-feasible only when every rule marked as required for feasibility returns `PASS`. A missing input is never treated as a pass.
- The calendar-year loss statement remains `UNRESOLVED` because the CIO did not define its measurement or breach consequence.
- The optimizer must return “no feasible portfolio” rather than relax the objective or a hard constraint.

## Units and return measurement

- All weights and rates use decimals internally: `0.08` means 8%.
- Expected portfolio return is the weighted arithmetic annual expected return.
- Monthly historical arithmetic mean × 12 may be displayed as an estimate, not as a promised return.
- Volatility is annualized standard deviation. For monthly returns it is sample monthly standard deviation × square root of 12.
- Covariance and expected-return inputs must use the same annual units.
- The CPI + 4% expected-return check is only a feasibility proxy. It does not prove that realized compounded return will meet the mandate over rolling five-year periods.
- Later validation must separately measure rolling five-year compounded after-cost returns where enough point-in-time history exists.

## CPI and as-of boundary

- Selected series: CPI-U All Items, U.S. City Average, seasonally adjusted (`CPIAUCSL`).
- Inflation measure: year-over-year percentage change.
- As-of rule: use the ALFRED vintage available on the decision date. Retain observation and availability dates for both index levels used in the year-over-year calculation; both availability dates must be on or before the decision date.
- No CPI value or decision date is hardcoded in Phase 1.

## Costs and turnover

- One-way turnover equals `0.5 × Σ |target weight − current weight|`.
- Trading-cost rate equals `one-way turnover × cost basis points ÷ 10,000`.
- The base cost assumption is an explicitly illustrative 10 bps one-way cost, with 0/10/25 bps sensitivity. It is not an observed Meridian cost and must be labeled that way in every output.
- Historical adjusted-close returns may be treated as net of fund operating expenses only after confirming the data provider's adjustment definition.
- A one-rebalance cost deduction is not automatically an annual recurring-cost estimate. Later forecasts must state the assumed rebalancing frequency and expected annual turnover.

## Reserve eligibility and liquidity

- The reserve requirement is 3%: four quarterly distributions of $0.75 million divided by a $100 million portfolio.
- An asset counts toward the reserve only after the committee confirms it is cash or an eligible daily-liquid government security.
- BIL is the designated reserve-eligible cash equivalent for Project 2. IEF is a Treasury-bond holding and does not automatically count toward the reserve.
- Liquidity means market value reasonably saleable and settled within five business days under normal market conditions. Each fund requires dated evidence before it receives a liquidity value.
- Liquidity is not the same as principal stability or the ability to fund distributions without a loss.

## Issuer exposure

- Nonexempt securities from the same issuer are aggregated.
- The Lab 13 Meridian case explicitly exempts cash, the U.S. Treasury, and diversified funds.
- Phase 1 follows the case's fund-level exemption without look-through. Any later look-through analysis is supplemental unless the committee changes the rule.

## Risk and the -10% statement

- Optimization risk measure: annualized volatility.
- Monitored loss measure: calendar-year total return and declared one-year stress losses.
- Threshold: -10%.
- No automatic prohibition or breach response is created. The exact Lab 13 language remains an unverifiable promise.
- Unresolved decision: how the CIO would measure and handle the annual-loss statement. The system must report `UNRESOLVED`, exclude it from feasibility, and never claim compliance.

## Allocation ranges

No range is defined in Phase 1. A later phase should derive ranges from the set of portfolios that remain feasible across accepted estimate, window, cost, and constraint stresses. A cosmetic interval around one optimized point is not acceptable.
