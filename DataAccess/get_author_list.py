import sqlite3
from Entities.author import Author

def get_author_list():
    author_list=[]
    with sqlite3.connect('BookShop.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
          SELECT *
          FROM Author;
        """)
        data=cursor.fetchall()
        for row in data:
            author=Author(row[0],row[1],row[2])
            author_list.append(author)

        return author_list