#!/usr/bin/env python3
"""float_check.py - does the cash box match at the end of a market day?

expected cash = opening float + cash sales - cash paid out
Counted cash can be given as a total, or as a note/coin count like "20x1,10x2,0.5x4".
Read-only, prints to the screen, no network access.

Examples:
  python float_check.py --float 80 --cash-sales 312.50 --paid-out 5 --counted 385
  python float_check.py --float 80 --cash-sales 312.50 --counts "50x2,20x13,5x4,1x7,0.5x3"
"""
import argparse
import sys


def parse_counts(text):
    total = 0.0
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            value, qty = part.lower().split("x")
            total += float(value) * int(qty)
        except ValueError:
            sys.exit(f"Cannot read '{part}'. Use value x quantity, e.g. 20x3")
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--float", dest="opening", type=float, required=True, help="opening float")
    ap.add_argument("--cash-sales", type=float, required=True, help="total cash sales of the day")
    ap.add_argument("--paid-out", type=float, default=0.0, help="cash taken out for costs (default 0)")
    ap.add_argument("--counted", type=float, help="counted cash in the box (total)")
    ap.add_argument("--counts", help='counted by denomination, e.g. "20x3,5x4,0.5x6"')
    ap.add_argument("--tolerance", type=float, default=1.0, help="difference still considered fine (default 1.00)")
    a = ap.parse_args()

    if (a.counted is None) == (a.counts is None):
        sys.exit("Give exactly one of --counted or --counts.")
    counted = a.counted if a.counted is not None else parse_counts(a.counts)
    expected = a.opening + a.cash_sales - a.paid_out
    diff = counted - expected

    print(f"Opening float : {a.opening:10.2f}")
    print(f"+ Cash sales  : {a.cash_sales:10.2f}")
    print(f"- Paid out    : {a.paid_out:10.2f}")
    print(f"= Expected    : {expected:10.2f}")
    print(f"Counted       : {counted:10.2f}")
    print(f"Difference    : {diff:+10.2f}")
    if abs(diff) <= a.tolerance:
        print("OK - within tolerance.")
    elif diff < 0:
        print("Short. Recount, check for unrecorded payouts or change given wrongly.")
    else:
        print("Over. Recount, check for sales or float top-ups you did not note down.")
    print(f"Cash to take home (counted minus next float {a.opening:.2f}): {counted - a.opening:.2f}")


if __name__ == "__main__":
    main()
