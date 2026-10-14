#!/usr/bin/env python3
"""price_check.py - what does each product really earn per channel?

Reads products.csv and channels.csv, prints profit per unit after fees,
postage, materials, packaging and YOUR time. Read-only: it writes nothing
(unless you redirect the output yourself). No network access.

Usage:
  python price_check.py products.csv channels.csv --hourly 15 --cushion 10
"""
import argparse
import csv
import sys


def num(row, key, line):
    raw = (row.get(key) or "").strip().replace(",", ".")
    if raw == "":
        return 0.0
    try:
        return float(raw)
    except ValueError:
        sys.exit(f"Line {line}: '{key}' must be a number, got '{raw}'")


def read(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))
    except OSError as e:
        sys.exit(f"Cannot read {path}: {e}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("products")
    ap.add_argument("channels")
    ap.add_argument("--hourly", type=float, default=15.0, help="your hourly rate (default 15)")
    ap.add_argument("--cushion", type=float, default=10.0,
                    help="profit cushion in %% of price after paying yourself (default 10)")
    a = ap.parse_args()

    products = read(a.products)
    channels = read(a.channels)
    if not products or not channels:
        sys.exit("products.csv and channels.csv must each contain at least one row.")

    for i, p in enumerate(products, start=2):
        base = (num(p, "materials", i) + num(p, "packaging", i) + num(p, "other", i)
                + num(p, "minutes", i) / 60.0 * a.hourly)
        price, ship_in, postage = num(p, "price", i), num(p, "shipping_charged", i), num(p, "postage", i)
        print(f"\n{p.get('sku', '?')}  {p.get('name', '')}   price {price:.2f}   true cost {base:.2f} "
              f"(incl. {num(p, 'minutes', i):.0f} min of your time)")
        for j, c in enumerate(channels, start=2):
            ships = (c.get("ships") or "no").strip().lower() in ("yes", "y", "1", "true")
            revenue = price + (ship_in if ships else 0.0)
            fees = (num(c, "fixed_per_item", j)
                    + revenue * (num(c, "platform_pct", j) + num(c, "payment_pct", j)) / 100.0
                    + num(c, "payment_fixed", j))
            profit = revenue - fees - base - (postage if ships else 0.0)
            if profit < 0:
                verdict = "LOSES MONEY"
            elif profit < price * a.cushion / 100.0:
                verdict = "thin"
            else:
                verdict = "healthy"
            print(f"  {c.get('name', '?'):<24} fees {fees:7.2f}   profit/unit {profit:8.2f}   {verdict}")
    print("\nFees in channels.csv are examples - replace them with your own platform numbers.")


if __name__ == "__main__":
    main()
