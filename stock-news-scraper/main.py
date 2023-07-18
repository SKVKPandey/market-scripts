import requests
from bs4 import BeautifulSoup

def scrape_stock_news(stock, start_date, end_date):
    base_url = 'https://www.moneycontrol.com/news/business/stocks'
    url = f"{base_url}/{stock}-Stocks-9.html?classic=true&sc_period={start_date}-{end_date}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('li', class_='clearfix')

    for article in articles:
        news_paragraph = article.find('p', class_='MT20')
        if news_paragraph:
            print(news_paragraph.get_text())
            print('-' * 50)

# Example usage
stock = 'reliance-industries'
start_date = '2023-07-15'
end_date = '2023-07-18'
scrape_stock_news(stock, start_date, end_date)

