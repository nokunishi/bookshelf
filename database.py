import sqlite3
from typing import List
from model import Book
from datetime import date


conn = sqlite3.connect('books.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS books (
              id INTEGER PRIMARY KEY,
              pos INTEGER,
              title varchar(255) NOT NULL, 
              author varchar(255),
              page INT,
              status INT,
              rating INT CHECK (Rating BETWEEN 0 and 10),
              started DATE,
              due DATE
              );''')
  
    
def insert_item(book: Book):
    # book already registerd
    c.execute('SELECT * FROM books WHERE title=:title AND author=:author', {"title": book.title, "author": book.author})
    if c.fetchone() is not None:
        raise InvalidBookException(book.title, book.author)
    
    # row number already taken
    c.execute('SELECT count(DISTINCT pos) FROM books')
    next_pos = c.fetchone()[0] + 1
    with conn:
        c.execute('SELECT * FROM books WHERE pos=:pos', {"pos": book.pos})
        if c.fetchone() is not None:
            book.pos = next_pos
        c.execute('INSERT INTO books(pos, title, author, page, status, rating, started, due) VALUES(?,?,?,?,?,?,?,?)', 
            (book.pos, book.title, book.author, book.page, book.status, book.rating, book.started, book.due))

def list_items() -> List[Book]:
    c.execute(f'SELECT * from books')
    books = []
    for rows in c.fetchall():
        _, pos, title, author, page, status, rating, started, due = rows
        books.append(Book(pos=pos, title=title, author=author, page=page, 
                          status=status, rating=rating, started=started, due=due))
    return books

def delete_item(pos):
    c.execute('SELECT title from books WHERE pos=:pos', {"pos": pos})
    title = c.fetchone()[0]
    with conn:
        c.execute("DELETE from books WHERE pos=:pos", {"pos": pos})
        for book in list_items():
            if book.pos > pos:
                c.execute('UPDATE books SET pos=:pos WHERE title =:title', {'pos': pos-1, 'title': book.title})
    return title

def delete_all():
    import os
    with conn:
        os.remove("books.db")
        

def update_item(pos: int, col:str, val):
    with conn:
        c.execute('SELECT title from books WHERE pos=:pos', {"pos": pos})
        if c.fetchone() is None:
            raise Exception
        if col == "author":
            c.execute('UPDATE books SET author=:author WHERE pos =:pos', {'pos': pos, 'author': val})
        elif col == "due":
            c.execute('UPDATE books SET due=:due WHERE pos =:pos', {'pos': pos, 'due': val})
        elif col == "page":
            c.execute('UPDATE books SET page=:page WHERE pos =:pos', {'pos': pos, 'page': val})
        elif col == "rating":
            c.execute('UPDATE books SET rating=:rating WHERE pos =:pos', {'pos': pos, 'rating': val})
        elif col == "started":
            c.execute('UPDATE books SET started=:started WHERE pos =:pos', {'pos': pos, 'started': val})
        elif col == "status":
            c.execute('UPDATE books SET status=:status WHERE pos =:pos', {'pos': pos, 'status': val})
        elif col == "title":
            c.execute('UPDATE books SET title=:title WHERE pos =:pos', {'pos': pos, 'title': val})

def set_due(pos: int, due: str):
    with conn:
        c.execute('SELECT started from books WHERE pos=:pos', {"pos": pos})
        try:
            started = c.fetchone()[0]
        except:
            pass
        
        # set appropriate year
        year = date.today().year
        due_ = [int(x) for x in due.split("-")]
        if started is not None:
            started = [int(x) for x in started.split("-")][1:]
            if due_ < started:
                due = date(year+1, due_[0], due_[1])
            else:
                due = date(year, due_[0], due_[1])

        c.execute('UPDATE books SET due=:due WHERE pos =:pos', {'pos': pos, 'due': due})

def complete_item(pos: int):
    with conn:
        c.execute('SELECT page from books WHERE pos=:pos', {"pos": pos})
        try:
            page = c.fetchone()[0]
        except:
            pass
        c.execute('UPDATE books SET status=:status WHERE pos =:pos', {'pos': pos, 'status': page})
        
        

class InvalidBookException(Exception):
    def __init__(self, title, author):
        self.title = title
        self.author = author

    