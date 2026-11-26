"""Print Moneycontrol news snippets for one stock between two dates (2023 experiment).

    python main.py reliance-industries 2023-07-15 2023-07-18

Moneycontrol has changed its pages since 2023, so this may return nothing today.
Keep requests slow and respect the site's terms.
"""
import argparse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.moneycontrol.com/news/business/stocks"


def scrape_stock_news(stock, start_date, end_date):
    url = f"{BASE_URL}/{stock}-Stocks-9.html?classic=true&sc_period={start_date}-{end_date}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")
    out = []
    for article in soup.find_all("li", class_="clearfix"):
        p = article.find("p", class_="MT20")
        if p:
            out.append(p.get_text(strip=True))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stock", help="Moneycontrol slug, e.g. reliance-industries")
    ap.add_argument("start", help="YYYY-MM-DD")
    ap.add_argument("end", help="YYYY-MM-DD")
    a = ap.parse_args()
    items = scrape_stock_news(a.stock, a.start, a.end)
    for text in items:
        print(text)
        print("-" * 50)
    if not items:
        print("No articles found (the page layout may have changed).")
