"""Peer P/E valuation using only Python's standard library."""

from decimal import Decimal, InvalidOperation


# =============================================================================
# INPUTS (edit by hand)
# Use None for missing values. Numeric strings may be used to preserve every
# entered decimal digit exactly.
# =============================================================================
TARGET = {
    "ticker": "WMT",
    "price": "112.34",
    "diluted_eps": "2.73",
}

PEERS = [
    {"ticker": "TGT", "price": "147.70", "diluted_eps": "8.13"},
    {"ticker": "COST", "price": "941.99", "diluted_eps": "18.21"},
]


NOT_MEANINGFUL = "not meaningful"


def to_decimal(value):
    """Convert an input to a finite Decimal, or return None if it is missing."""
    if value is None or isinstance(value, bool):
        return None
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None
    return number if number.is_finite() else None


def normalized_ticker(value):
    """Return a case-insensitive ticker key used for exclusion and deduping."""
    return str(value).strip().upper() if value is not None else ""


def median(values):
    """Return the exact median of a nonempty Decimal sequence."""
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / Decimal(2)


def deduplicated_peers(peers, target_key):
    """Keep the first occurrence of each peer and remove the target."""
    result = []
    seen = set()
    for position, peer in enumerate(peers, start=1):
        key = normalized_ticker(peer.get("ticker"))
        # Missing tickers receive distinct keys so unrelated rows are not merged.
        dedupe_key = key if key else f"__MISSING_TICKER_{position}"
        if (key and key == target_key) or dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        result.append(
            {
                "label": key or f"(missing ticker, row {position})",
                "price": to_decimal(peer.get("price")),
                "eps": to_decimal(peer.get("diluted_eps")),
            }
        )
    return result


def peer_multiple(peer):
    """Return price / diluted EPS, or None when either input is unusable."""
    price = peer["price"]
    eps = peer["eps"]
    if price is None or eps is None or price <= 0 or eps <= 0:
        return None
    return price / eps


def implied_price(multiple, target_eps):
    """Return an implied price without any intermediate rounding."""
    if target_eps is None or target_eps <= 0:
        return None
    return multiple * target_eps


def format_multiple(value):
    return NOT_MEANINGFUL if value is None else f"{value:.6f}"


def format_price(value):
    return NOT_MEANINGFUL if value is None else f"${value:.2f}"


def main():
    target_key = normalized_ticker(TARGET.get("ticker"))
    target_label = target_key or "(missing ticker)"
    target_price = to_decimal(TARGET.get("price"))
    target_eps = to_decimal(TARGET.get("diluted_eps"))
    peers = deduplicated_peers(PEERS, target_key)

    print(f"Target: {target_label}")
    print(
        "Target closing price: "
        + (format_price(target_price) if target_price is not None and target_price > 0 else NOT_MEANINGFUL)
    )
    print(
        "Target diluted EPS: "
        + (format_price(target_eps) if target_eps is not None and target_eps > 0 else NOT_MEANINGFUL)
    )
    print("\nPeer P/E multiples")

    valid = []
    for peer in peers:
        multiple = peer_multiple(peer)
        print(f"{peer['label']}: {format_multiple(multiple)}")
        if multiple is not None:
            valid.append((peer, multiple))

    multiples = [multiple for _, multiple in valid]
    if not multiples:
        print("\nPeer summary: no usable peers")
        print("Median P/E: not meaningful")
        print("Implied price: not meaningful")
        full_estimate = None
    else:
        median_multiple = median(multiples)
        full_estimate = implied_price(median_multiple, target_eps)
        print(f"\nMedian peer P/E: {format_multiple(median_multiple)}")

        if len(multiples) == 1:
            print("Peer valuation: one valid peer; reference estimate, no range")
            print(f"Reference implied price: {format_price(full_estimate)}")
        else:
            minimum_multiple = min(multiples)
            maximum_multiple = max(multiples)
            print(f"Minimum peer P/E: {format_multiple(minimum_multiple)}")
            print(f"Maximum peer P/E: {format_multiple(maximum_multiple)}")
            print(f"Minimum implied price: {format_price(implied_price(minimum_multiple, target_eps))}")
            print(f"Median implied price: {format_price(full_estimate)}")
            print(f"Maximum implied price: {format_price(implied_price(maximum_multiple, target_eps))}")

    print("\nPeer-removal analysis")
    if not peers:
        print("No peer removals to analyze.")
        return

    for removed_peer in peers:
        remaining_multiples = [
            peer_multiple(peer) for peer in peers if peer is not removed_peer
        ]
        remaining_multiples = [
            multiple for multiple in remaining_multiples if multiple is not None
        ]
        prefix = f"Remove {removed_peer['label']}: "
        if not remaining_multiples:
            print(prefix + "no estimate")
            continue

        remaining_estimate = implied_price(median(remaining_multiples), target_eps)
        if remaining_estimate is None or full_estimate is None:
            print(prefix + "remaining median-implied price not meaningful; dollar change not meaningful")
            continue

        # Both the estimate and change are calculated before display rounding.
        change = remaining_estimate - full_estimate
        print(
            prefix
            + f"remaining median-implied price {format_price(remaining_estimate)}; "
            + f"dollar change {change:+.2f}"
        )


if __name__ == "__main__":
    main()
