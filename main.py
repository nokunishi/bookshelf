import typer
from rich.console import Console
from rich.table import Table
from model import Book
from database import *


console = Console()
app = typer.Typer()

@app.command(short_help='add an item')
def add(title: str, author: str, page:int):
    title = " ".join(word.capitalize() for word in title.split(" "))
    author = " ".join(word.capitalize() for word in author.split(" "))

    try:
        insert_item(Book(title=title, author=author, page=page))
    except InvalidNameException as e:
        typer.echo(f'ERROR: "{e.title}" by {e.author} is already registered')
    else:
        show()


@app.command()
def delete(id: int):
    book = delete_item(id=id)
    typer.echo(f"deleting: {book}")


@app.command()
# author, title is linked to id: immutable
def update(id: int, val):
    try:
        if val.isdigit():
            update_item(id, 'rating', val)
        else:
            update_item(id, 'category', val)
    except:
        typer.echo(f"book with id {id} not found")
    else:
        show()

@app.command()
def progress(id: int, curr_page: int):
    update_item(id, 'status', curr_page)
    show()


@app.command()
def show():
    console.print("[bold magenta] Books To Read!! [/bold magenta]", "🐱")
    
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", min_width=6)
    table.add_column("Author", min_width=20)
    table.add_column("Title", min_width=12, justify="right")
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Status", min_width=20, justify="right")
    table.add_column("Rating", min_width=6, justify="right")

    def get_category_colour(category):
        # TODO: make it customizable
        COLOURS = {'Novel': 'red', 'Sci-Fi': 'blue' ,'Research': 'green'}
        if category in COLOURS:
            return COLOURS[category]
        return 'white'

    for book in list_items():
        c = get_category_colour(book.category)
        if book.status == book.page:
            is_done = 'Completed ✅' 
        elif book.status:
            is_done = f'On page 📖: {book.status} / {book.page}'
        else:
            is_done = 'Not started ❌'
        table.add_row(str(book.id), book.title, book.author, f'[{c}]{book.category}[/{c}]', is_done, str(book.rating))
        console.print(table)

if __name__ == "__main__":
    app()