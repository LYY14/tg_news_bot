"""модуль парсинга яндекс новостей регион салехард"""


import requests
from bs4 import BeautifulSoup

from db_engine import get_all_data


URL = 'https://yandex.ru/news/region/salekhard'


def parse_news(url: str) -> list:
    """Получает url страницы, парсит её и спарсенные данные возвращает в виде списка словарей"""
    print('starting_parsing_news')
    request = requests.get(url)
    html = request.text
    soup = BeautifulSoup(html, 'lxml')
    news_cards = soup.find_all('article', class_='mg-card')
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


def get_current_news(parsed_news: list) -> list:
    """Получает список спарсенных новостей, сверяет их с тем, что есть в БД и возвращает только свежие новости"""
    db_data = get_all_data()
    result = []
    for parsed in parsed_news:
        is_not_in_db = True
        for db in db_data:
            if db['title'] == parsed['title']:
                is_not_in_db = False
        if is_not_in_db:
            result.append(parsed)
    return result


if __name__ == '__main__':
    print('news_parser.py')
    parsed_news = parse_news(URL)
    current_news = get_current_news(parsed_news)
    for news in current_news:
        print(news)
