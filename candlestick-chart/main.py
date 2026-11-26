"""Candlestick chart of the last month from an Investing.com-style NSE price export.

    python main.py nse-historical-data.csv [--months 1]

The export is tab-separated with columns Date ("Nov 10, 2023"), Price, Open,
High, Low and, optionally, Vol. ("1.25M"). Price is the closing price.
"""
import argparse

import mplfinance as mpf
import pandas as pd


def parse_volume(v):
    if pd.isna(v) or v in ("-", ""):
        return float("nan")
    v = str(v).replace(",", "")
    mult = {"K": 1e3, "M": 1e6, "B": 1e9}.get(v[-1].upper(), 1)
    return float(v[:-1] if mult != 1 else v) * mult


def load(path, months=1):
    df = pd.read_csv(path, sep=None, engine="python", thousands=",")
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
    df = df.rename(columns={"Price": "Close", "Vol.": "Volume"}).set_index("Date").sort_index()
    if "Volume" in df:
        df["Volume"] = df["Volume"].map(parse_volume)
    cols = ["Open", "High", "Low", "Close"] + (["Volume"] if "Volume" in df and df["Volume"].notna().any() else [])
    df = df[cols].astype(float)
    return df[df.index >= df.index.max() - pd.DateOffset(months=months)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--months", type=int, default=1)
    a = ap.parse_args()
    data = load(a.csv, a.months)
    mpf.plot(data, type="candle", style="yahoo", volume="Volume" in data,
             title=f"Candlestick chart, last {a.months} month(s)")
