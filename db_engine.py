import sqlite3


conn = sqlite3.connect('news_list.db')
cursor = conn.cursor()



def get_all_data(cursor):
    cursor.execute('''SELECT * FROM news''')
    result = cursor.fetchall()
    return result


def insert_data(conn, cursor, title, url, source):
    cursor.execute(
        f'''INSERT INTO news VALUES ('{title}', '{url}', '{source}', FALSE )'''
    )
    conn.commit()


def update_data(conn, cursor, url):
    cursor.execute(f'''UPDATE news SET status=TRUE WHERE url="{url}"''')
    conn.commit()


def delete_data(conn, cursor, url):
    cursor.execute(f'''DELETE FROM news WHERE url="{url}"''')
    conn.commit()


if __name__ == '__main__':
    print('db_engine')
    insert_data(conn, cursor, 'title', 'url', 'source')
    rows = get_all_data(cursor)
    for row in rows:
        print(row)
    print("uhybjhbbkbj")
    update_data(conn, cursor, 'url')
    rows = get_all_data(cursor)
    for row in rows:
        print(row)
    print("uhybjhbbkbj")
    delete_data(conn, cursor, 'url')
    rows = get_all_data(cursor)
    for row in rows:
        print(row)
    print("uhybjhbbkbj")

