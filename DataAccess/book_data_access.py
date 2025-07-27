import sqlite3
from Entities.Book import Book
from Entities.author import Author
from Entities.publisher import Publisher


def get_book_list(term=None):
    book_list=[]
    with sqlite3.connect('BookShop.db') as connection:
        cursor=connection.cursor()
        if not term:
            cursor.execute("""
                    Select    Book.*
                ,         Author.first_name
                ,         Author.last_name
                ,         Publisher.title    AS    PublisherTitle
                From      Book
                Inner     Join
                          Author
                ON        Book.author_id    =    Author.id
                Inner     Join
                          Publisher
                ON        Book.publisher_id =    Publisher.id                
                    """)
        else:
            cursor.execute(f"""
                            Select    Book.*
                            ,         Author.first_name
                            ,         Author.last_name
                            ,         Publisher.title    AS    PublisherTitle
                            From      Book
                            Inner     Join
                                      Author
                            ON        Book.author_id    =    Author.id
                            Inner     Join
                                      Publisher
                            ON        Book.publisher_id =    Publisher.id
                            Where     Book.title LIKE '%{term}%'""")
        data=cursor.fetchall()
        for row in data:
            author = Author(row[3],row[5],row[6])
            publisher =Publisher(row[4],row[7])
            book=Book(row[0],row[1],row[2],author,publisher)
            book_list.append(book)
    return book_list

def delete_book(book_id):
    with sqlite3.connect('BookShop.db') as connection:
        cursor=connection.cursor()
        cursor.execute(f"""
            DELETE FROM Book
            WHERE id = {book_id}
        """)
        connection.commit()

def insert_book(title,price,author_id,publisher_id):
    with sqlite3.connect('BookShop.db') as connection:
        cursor=connection.cursor()
        cursor.execute(f"""
            INSERT INTO Book (
                     title,
                     price,
                     author_id,
                     publisher_id
                 )
                 VALUES (
                     '{title}',
                     {price},
                     {author_id},
                     {publisher_id}
                 );
        """)
        connection.commit()

def get_book_by_id(book_id):
    with sqlite3.connect('BookShop.db') as connection:
        cursor=connection.cursor()
        cursor.execute(f"""
                Select    Book.*
            ,         Author.first_name
            ,         Author.last_name
            ,         Publisher.title    AS    PublisherTitle
            From      Book
            Inner     Join
                      Author
            ON        Book.author_id    =    Author.id
            Inner     Join
                      Publisher
            ON        Book.publisher_id =    Publisher.id         
            where Book.id={book_id}       
                """)
        row=cursor.fetchone()
        author = Author(row[3],row[5],row[6])
        publisher =Publisher(row[4],row[7])
        book=Book(row[0],row[1],row[2],author,publisher)

    return book

def update_book(book_id, new_title, new_price, new_author_id, new_publisher_id):
    with sqlite3.connect("BookShop.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        UPDATE Book
        SET title = '{new_title}',
            price = {new_price},
            author_id = {new_author_id},
            publisher_id = {new_publisher_id}
        WHERE id = {book_id}""")
        connection.commit()