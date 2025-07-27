import sqlite3
from Entities.publisher import Publisher

def get_publisher_list():
    publisher_list = []
    with sqlite3.connect('BookShop.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
          SELECT *
          FROM Publisher;
        """)
        data = cursor.fetchall()
        for row in data:
            publisher = Publisher(row[0], row[1])
            publisher_list.append(publisher)

        return publisher_list