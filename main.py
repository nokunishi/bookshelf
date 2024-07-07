import typer
from typing_extensions import Annotated

from rich.console import Console
from rich.table import Table

from datetime import date

from model import Book
from database import *


console = Console()
app = typer.Typer()

@app.command(short_help='add an item')
def add(title: str, author: str, page:int):
    title = " ".join(word.capitalize() for word in title.split(" "))
    author = " ".join(word.capitalize() for word in author.split(" "))
    book = Book(title=title, author=author, page=page)

    try:
        insert_item(book)
    except InvalidBookException as e:
        typer.echo(f'ERROR: "{e.title}" by {e.author} is already registered')
    else:
        show()


@app.command()
def delete(pos: int):
    book = delete_item(pos=pos)
    typer.echo(f"deleting: {book}")

@app.command()
def deleteAll():
    delete_all()

@app.command()
def start(pos: int):
    update_item(pos, 'started', date.today())
    show()

@app.command()
def due(pos: int, due: str):
    set_due(pos, due)
    show()

@app.command()
def update(pos: int, col: str, val):
    try:
        if col == "title":
            update_item(pos, 'title', val)
        elif col == "author":
            update_item(pos, 'author', val)
        elif col == "page":
            update_item(pos, 'page', val)
        elif col == "rating":
            update_item(pos, 'rating', val)
        elif col == "status":
            update_item(pos, 'status', val)
    except:
        typer.echo(f"book with pos {pos} not found")
    else:
        show()


@app.command()
def complete(pos: int):
    complete_item(pos)
    show()

@app.command()
def reset(pos: int):
    update_item(pos, 'status', 0)
    show()

@app.command()
def show(wip :Annotated[bool, typer.Option(help="show only unfinished books")] = False,
         complete :Annotated[bool, typer.Option(help="show only unfinished books")] = False):
    table = create_table()
    for book in list_items():
        status_color, is_done = render_status(book)
        
        if wip and status_color == 'green':
            continue
        if complete and status_color != 'green':
            continue

        due_color = color_due(book)
        due = book.due if book.due is not None else ""
        rating = book.rating if str(book.rating) is not None else ""
        table.add_row(str(book.pos), book.title, book.author, f'[{status_color}]{is_done}[/{status_color}]', 
                      book.started, f'[{due_color}] {due}[/{due_color}]', rating)
    console.print(table)


def create_table():
    console.print("[bold magenta] Books To Read!! [/bold magenta]", "🐱")
    
    table = Table(show_header=True, header_style="bold blue", show_lines= True)
    table.add_column("#", min_width=3)
    table.add_column("Title", min_width=20, justify="right")
    table.add_column("Author", min_width=20, justify="right")
    table.add_column("Status", min_width=20, justify="right")
    table.add_column("Started", min_width=12, justify="right")
    table.add_column("Due", min_width=12, justify="right")
    table.add_column("Rating", min_width=6, justify="right")

    return table

def render_status(book):
    if book.status == book.page:
        is_done = f'{date.today()}: Done! ✅' 
        c = 'green'
    elif book.status:
        is_done = f'On page 📖: {book.status} / {book.page}'
        c = 'yellow'
    else:
        is_done = 'Not started ❌'
        c = 'white'
    return c, is_done

def color_due(book):
    if book.due is None:
        return 'white'
    
    due = [int(x) for x in book.due.split("-")]
    if date(*due) < date.today():
        return 'red'
    else:
        return 'white'
    


if __name__ == "__main__":
    app()