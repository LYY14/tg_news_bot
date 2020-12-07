"""модуль парсинга яндекс новостей регион салехард"""


import sqlite3

import requests
from bs4 import BeautifulSoup

from db_engine import get_all_data

conn = sqlite3.connect('news_list.db')
cursor = conn.cursor()


URL = 'https://yandex.ru/news/region/salekhard'


def parse_news(url):
    print('starting_parsing_news')
    request = requests.get(url)
    html = request.text
    soup = BeautifulSoup(html, 'lxml')
    news_cards = soup.find_all('article', class_='news-card')
    result = []
    for news_card in news_cards:
        news_header = news_card.find('a', class_='news-card__link')
        url = news_header.get('href')
        title = news_header.text
        source = news_card.find('span', class_='mg-card-source__source').find('a').text.replace(' ', '')\
            .replace('-', '').replace('.', '').replace('(', '').replace(')', '')
        result.append(
            {
                'url': url,
                'title': title,
                'source': source,
            }
        )
    return result


def get_current_news(parsed_news):
    db_data = get_all_data(cursor)
    result = []
    for parsed in parsed_news:
        flag = False
        for db in db_data:
            try:
                if db['url'] == parsed['url']:
                    flag = True
            except TypeError:
                if db[1] == parsed['url']:
                    flag = True
        if not flag:
            result.append(parsed)
    return result


if __name__ == '__main__':
    print('news_parser.py')
    parsed_news = parse_news(URL)
    current_news = get_current_news(parsed_news)
    for news in current_news:
        print(news)
    conn.close()
