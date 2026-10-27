# Lab 16 – Provenance Gate

This lab applies a point-in-time filter to determine what data was knowable on a decision date. Publication dates matter because a value may describe an earlier month but still be unavailable to an investor until it is published.

## Row Funnel

The decision date is March 31, 2026. The four rules are applied in order.

| Rule | Treatment | Rows Removed |
|---:|---|---|
| 1 | Quarantine rows with no ticker | 11 |
| 2 | Remove exact duplicates | 7 |
| 3 | Remove rows published after March 31, 2026 | 3, 8, 10 |
| 4 | Replace an older vintage with the latest revision available by the decision date | 2 |
| Final panel | Keep the rows remaining after all four rules | 1, 4, 5, 6, 9, 12 |

## As-Of vs. Naive Signals

| Ticker | As-of signal | Naive signal |
|---|---:|---:|
| AAA | +1.98% (February 2026) | +5.83% (March 2026) |
| BBB | −1.02% (February 2026) | −5.15% (March 2026) |
| CCC | +0.91% (February 2026) | +1.82% (February 2026) |

The as-of signals use only values published by March 31. The naive signals ignore publication dates, so they include AAA's and BBB's April publications and CCC's later February revision.

## Revision Logic

Rule 4 groups rows by ticker and month and keeps the row with the latest publication date. For AAA in February, row 2 was published on March 10 and row 4 was published on March 25. The code removes row 2 and keeps row 4 because March 25 is later.

The `prior is None` condition means no row has been stored yet for that ticker-month pair. In that case, the current row becomes the first candidate. If a prior row exists, the code compares the two publication dates and replaces the prior row only when the current row was published later.

## Decision Date Test

The original decision date is March 31, 2026. I tested April 15, 2026 as a later decision date, when every publication in the table was available.

| Ticker | April 15 as-of signal | Naive signal |
|---|---:|---:|
| AAA | +5.83% (March 2026) | +5.83% (March 2026) |
| BBB | −5.15% (March 2026) | −5.15% (March 2026) |
| CCC | +1.82% (February 2026) | +1.82% (February 2026) |

The April 15 as-of signals match the naive signals for all three tickers because no publication occurs after that date. The decision date in `asof.py` was restored to March 31, 2026 after the test.

## Key Takeaways

I learned that look-ahead bias occurs when a historical analysis uses information that had not been published on the decision date. Tracking publication dates and revisions keeps the signal limited to what an investor could actually have known at the time.
