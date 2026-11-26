# Market scripts (2023–2024)

Small Python experiments with Indian market data, written while learning how prices, option chains and broker APIs work. Each folder stands on its own.

| Folder | Built | What it does |
|---|---|---|
| `stock-news-scraper/` | Jul 2023 | Prints Moneycontrol news snippets for one stock between two dates |
| `candlestick-chart/` | Nov 2023 | Draws a one-month candlestick chart (with volume) from an Investing.com NSE price export |
| `fyers-options/` | Jul 2024 | Fyers API v3: sign-in flow, a live price WebSocket, a live-prices-to-Google-Sheets logger, and open interest vs strike price charts |

The larger project from the same period, a Streamlit dashboard with an LSTM forecast, is in its own repository: `nse-stock-dashboard`.

> Learning code. Nothing here is investment advice.

## Setup

```bash
pip install -r requirements.txt
```

## stock-news-scraper

```bash
python stock-news-scraper/main.py reliance-industries 2023-07-15 2023-07-18
```

Moneycontrol has changed its pages since 2023, so this may print "No articles found".

## candlestick-chart

Download daily NSE prices from Investing.com (Historical Data, then Download), then:

```bash
python candlestick-chart/main.py nse-historical-data.csv --months 1
```

## fyers-options

You need a Fyers trading account and an app created on the Fyers API dashboard. Keys are read from environment variables, so copy `.env.example` to `.env` and fill it in. Never commit `.env` or the Google service-account file.

| Script | Step |
|---|---|
| `auth_code.py` | Prints the sign-in URL. After you sign in, copy the `auth_code` from the redirect into `FYERS_AUTH_CODE`. |
| `access_token.py` | Swaps the auth code for an access token. Put it in `FYERS_ACCESS_TOKEN`. It lasts one trading day. |
| `main.py` | Streams live NIFTY 50 and NIFTY BANK index updates over the WebSocket |
| `new_sheet.py`, `list_sheets.py`, `sample_sheet.py` | Create, list and test the Google Sheet (needs a Google service account) |
| `gsheet.py` | Subscribes to 27 large NSE stocks and writes each one's last price, previous close, high and low to the sheet, then exits |
| `oi.py` | Option chain from Fyers, plotted as call and put open interest by strike |
| `oi-nse.py` | The same chart from NSE data through `nsepy` |

### Status as of November 2026

- `oi-nse.py` no longer works: `nsepy` stopped working when NSE blocked scripted access. It's kept for reference.
- `oi.py` calls a Fyers quotes URL that may have changed since 2024. Check the current Fyers API docs for the option-chain endpoint if it returns an error.
- The rest follow the Fyers API v3 flow as of 2024.

## Changes in November 2026

- **Keys out of the code:** the Fyers keys and tokens now come from `.env` instead of being written in the scripts.
- **`gsheet.py` exits again:** it waited for HDFC Ltd, which stopped trading after the July 2023 merger with HDFC Bank, so it never received every symbol. HDFC Ltd is removed.
- **`oi.py` auth header:** now `app_id:access_token`, the format Fyers expects.
- **`candlestick-chart` no longer crashes:** it now sets a date index, uses the closing price and handles the volume column.
- **`stock-news-scraper`:** now takes the stock and dates as arguments and has a request timeout.
