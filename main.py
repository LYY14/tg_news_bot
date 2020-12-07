# -*- coding: utf-8 -*-

import sqlite3
import threading
from time import sleep

from telegram import Bot
from telegram.utils.request import Request

from bot_configs import API_TOKEN, ADMIN_ID
from db_engine import update_data, insert_data
from news_parser import get_current_news, parse_news


URL = 'https://yandex.ru/news/region/salekhard'


conn = sqlite3.connect('news_list.db')
cursor = conn.cursor()
# cursor.execute('''CREATE TABLE news (title text, url text, source text, status bool)''')
# conn.commit()


request = Request(connect_timeout=3)
bot = Bot(request=request, token=API_TOKEN)


def log_error(f):
    """Отлавливание ошибок"""
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error = f'ERROR {e} in '
            print(error)
            update = args[0]
            if update and hasattr(update, 'message'):
                bot.send_message(chat_id=ADMIN_ID, text=error)
            raise e
    return inner


@log_error
def post_new(post):
    insert_data(conn, cursor, post['title'], post['url'], post['source'])
    bot.send_message(chat_id=ADMIN_ID, text=generate_message_text(post), parse_mode='html')
    update_data(conn, cursor, post['url'])


def generate_message_text(post):
    return f'<a href="{post["url"]}">{post["title"]}</a>\n\n#{post["source"]}'


def update_channel_loop():
    while True:
        current_news = get_current_news(parse_news(URL))
        for post in current_news:
            post_new(post)
            sleep(2)
        sleep(900)


if __name__ == '__main__':
    print('main')
    update_channel_loop()
    conn.close()