# Market Day Calm Lite

**Know what your product really earns and whether the cash box adds up – in two small offline scripts.**

Two standalone Python tools for solo makers who sell at markets and online:

- `price_check.py` – profit per unit for every product and sales channel, after fees, postage, materials, packaging **and your own time**. Verdict: healthy / thin / loses money.
- `float_check.py` – end-of-day cash box check: opening float + cash sales − payouts = expected, compared with what you counted (by total or by note and coin).

Both scripts only read the files you give them and print to the screen. They make no network connections and never change or delete files.

## Quick start

```bash
python price_check.py products.csv channels.csv --hourly 15 --cushion 10
python float_check.py --float 80 --cash-sales 312.50 --paid-out 5 --counts "50x2,20x13,5x4,1x7,0.5x3"
```

Edit `products.csv` and `channels.csv` (sample data included) with your own numbers. The fees in `channels.csv` are examples – use the current numbers from your own platform's fee pages. Set `ships` to `yes` for channels where you post the item (shipping charged and postage paid are then included).

Sample output of `price_check.py` (shortened):

```
SOAP-01  Oat soap bar   price 6.50   true cost 4.50 (incl. 12 min of your time)
  Market stall - cash      fees    0.00   profit/unit     2.00   healthy
```

## Requirements

- Python 3.8 or newer, standard library only.

## Notes

This is an organising tool, not professional advice for tax, accounting or legal questions. Results are only as good as the numbers you type in.

Created with AI assistance by an automated system.

## Full version

The lite version covers two calculations. The full **Market Day Calm** Excel workbook adds, honestly listed:

- a Sales Log (up to 500 lines) with fees, postage and profit calculated per sale, plus drop-downs
- a Market Days sheet with cash/card sales, stall fee, profit per stall hour and a "worth it?" verdict
- Stock sheet with "make more" alerts, weeks of cover and money tied up in slow stock
- an Overview of revenue, profit and channel comparison, and a Custom Quote sheet
- a ready-made cash count sheet, sample data and a blank copy, and a quick-start PDF

Details: https://kontor7-agent.github.io/p/market-day-calm-stall-stock-sales-float-tracker?s=github

## License

MIT – see `LICENSE`.
