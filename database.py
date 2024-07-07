import sqlite3
from typing import List
from model import Book

conn = sqlite3.connect('books.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS books (
              id INTEGER PRIMARY KEY,
              title varchar(255) NOT NULL, 
              author varchar(255),
              category varchar(255),
              page INT,
              status INT,
              rating INT CHECK (Rating BETWEEN 0 and 10)
              );''')
  
    
def insert_item(book: Book):
    c.execute('SELECT * FROM books')

    with conn:
        try:
            c.execute('INSERT INTO books(id, title, author, category, page, status, rating) VALUES(?,?,?,?,?,?,?)', 
                  (book.id, book.title, book.author, book.category, 
                   book.page, book.status, book.rating))
        except sqlite3.IntegrityError:
            raise InvalidNameException(book.title, book.author)
        

def list_items() -> List[Book]:
    c.execute(f'SELECT * from books')
    books = []
    for rows in c.fetchall():
        id, title, author, category, page, status, rating = rows
        books.append(Book(id=id, title=title, author=author, category=category, 
                          page=page, status=status, rating=rating))
    return books

def delete_item(id):
    c.execute('SELECT title from books WHERE id=:id', {"id": id})
    title = c.fetchone()[0]
    with conn:
        c.execute("DELETE from books WHERE id=:id", {"id": id})
    return title


def update_item(id: int, col:str, val):
    with conn:
        c.execute('SELECT title from books WHERE id=:id', {"id": id})
        if c.fetchone() is None:
            raise Exception

        if col == "category":
            c.execute('UPDATE books SET category=:category WHERE id =:id', {'id': id, 'category': val})
        elif col == "rating":
            c.execute('UPDATE books SET rating=:rating WHERE id =:id', {'id': id, 'rating': val})
        elif col == "status":
            c.execute('UPDATE books SET status=:status WHERE id =:id', {'id': id, 'status': val})
"""       
def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_status = :date_status WHERE position = :position',
                  {'position': position, 'date_status': datetime.datetime.now().isoformat()}),

"""

class InvalidNameException(Exception):
    def __init__(self, title, author):
        self.title = title
        self.author = author

    