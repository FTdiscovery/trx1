"""
Scrapes articles from ALPACA API
"""
import unicodedata

from newsapi import NewsApiClient
from datetime import date, timedelta, datetime, time
from alpaca_trade_api import REST, Stream
from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime
import requests
from dateutil import rrule
import pyuser_agent
import json

def remove_unicode(string):
    return (string.replace("\u2013", "-")
            .replace("\u2014", "-")
            .replace("\u2015", "-")
            .replace("\u2017", "_")
            .replace("\u2018", "\'")
            .replace("\u2019", "\'")
            .replace("\u201a", ",")
            .replace("\u201b", "\'")
            .replace("\u201c", "\"")
            .replace("\u201d", "\"")
            .replace("\u201e", "\"")
            .replace("\u2026", "...")
            .replace("\u2032", "\'")
            .replace("\u2033", "\""))
import pandas as pd

API_SECRET = 'xYPcL5xOgWDDledWt40oenT9k5zgeGldv2Ewpd5d'
API_KEY = 'AKL379LS0BLM4SUDEOMQ'
BASE_URL = "https://paper-api.alpaca.markets"


def get_headers():
    return {'User-Agent': pyuser_agent.UA().random}


def scrape_articles_alpaca(relevant_tickers, start_date, end_date, summary_req):
    # if summary_req is 0, allow anything
    # if summary req is 1, allow only len(20) >
    # if summary req is -1, only allow no summary ones

    entire_article = []

    dates = [start_date] + list(rrule.rrule(rrule.WEEKLY, dtstart=start_date, until=end_date)) + [end_date]
    if dates[0] == dates[1]:
        dates.pop(0)

    news_urls = set()
    rest_client = REST(API_KEY, API_SECRET)

    for ticker in relevant_tickers:
        for i in range(len(dates)-1):
            print("Grabbing news on", ticker, "from", dates[i].strftime("%Y-%m-%d"), "to", dates[i+1].strftime("%Y-%m-%d"), end="|")
            try:
                news = rest_client.get_news(ticker, dates[i].strftime("%Y-%m-%d"), dates[i+1].strftime("%Y-%m-%d"))
                for elem in news:
                    article = {}
                    article['source'] = elem.source
                    article['link'] = elem.url
                    article['title'] = elem.headline
                    a = (datetime.strptime(str(elem.updated_at), '%Y-%m-%d %H:%M:%S+00:00') - timedelta(hours=5)).strftime(
                        "%Y-%m-%d %H:%M")
                    article['date'] = a
                    article['summary'] = remove_unicode(elem.summary.replace('\xa0', '\' ').replace('&#39;', '\''))
                    article['tickers'] = elem.symbols
                    article['sentiments'] = [0 for i in range(len(article['tickers']))]

                    # if len(article['summary']) < 10:
                    #     print('we are here')
                    #     soup = BeautifulSoup(
                    #         requests.get(article['link'], headers=get_headers(), timeout=10).content.decode('utf-8', 'ignore'),
                    #         'html.parser')
                    #     print(article['link'])
                    #     print(soup.p)

                    if article['link'] not in news_urls and len(article['tickers']) < 7:
                        if len(article['summary']) > 20 and summary_req == 1:
                            entire_article.append(article)
                            news_urls.add(article['link'])
                        elif len(article['summary']) < 5 and summary_req == -1:
                            entire_article.append(article)
                            news_urls.add(article['link'])
                        elif summary_req == 0:
                            entire_article.append(article)
                            news_urls.add(article['link'])

                print(ticker, len(entire_article))
                time.sleep(0.5)
            except:
                continue
    print("")

    print(entire_article)
    start_str = ','.join(relevant_tickers) + "," + dates[0].strftime("%Y-%m-%d")+','+'summary='+str(summary_req)
    file_name = f"data/alpaca/{start_str}.json"
    with open(file_name, "w") as f:
        json.dump(entire_article, f)

    return entire_article

# don't do fb!
tickers = ["AAPL", "AMZN", "MSFT", "SPY", "TSLA", "NVDA", "BRK-A", "NVDA", "F", "SNAP", "PLTR", "INTC", "BAC", "JPM", "GM", "F", "META", "TWTR", "NYT", "META"]
b = scrape_articles_alpaca(tickers, datetime(2022, 10, 26), datetime(2022, 10, 27), 1)
