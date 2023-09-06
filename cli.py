import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AuthorGenre, Book, Genre, Customer, OrderItem
from datetime import datetime

# Replace 'your_database_url' with your actual database URL
database_url = 'sqlite:///bookstore.db'

engine = create_engine(database_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

@click.group()
def cli():
    """Bookstore Management System CLI"""

@cli.command()
def list_books():
    """List all books in the bookstore"""
    session = DBSession()
    books = session.query(Book).all()
    session.close()
    for book in books:
        print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author_genre.author_name}, Genre: {book.genre.genre_name}")

# @cli.command()
# @click.argument('title')
# @click.argument('author')
# @click.argument('genre')
# @click.argument('publication_year', type=int)
# @click.argument('price', type=float)
# def add_book(title, author, genre, publication_year, price):
#     """Add a new book to the bookstore"""
#     session = DBSession()
    
#     # Check if author and genre already exist in the database
#     author_genre = session.query(AuthorGenre).filter_by(author_name=author, genre_name=genre).first()
#     if author_genre is None:
#         author_genre = AuthorGenre(author_name=author, genre_name=genre)
#         session.add(author_genre)
#         session.commit()
    
#     book = Book(title=title, author_genre=author_genre, publication_year=publication_year, price=price)
#     session.add(book)
#     session.commit()
    
#     session.close()
#     print(f"Book '{title}' added successfully!")

# if __name__ == '__main__':
#     cli()
@cli.command()
@click.argument('title')
@click.argument('author')
@click.argument('genre')
@click.argument('publication_year', type=int)
@click.argument('price', type=float)
def add_book(title, author, genre, publication_year, price):
    """Add a new book to the bookstore"""
    session = DBSession()
    
    # Check if author and genre already exist in the database
    author_genre = session.query(AuthorGenre).filter_by(author_name=author, genre_name=genre).first()
    if author_genre is None:
        click.echo(f"Author '{author}' and Genre '{genre}' do not exist. Please add them first.")
        return
    
    # Use the author_id and genre_id from the author_genre object
    book = Book(title=title, author_id=author_genre.id, genre_id=author_genre.genre_id, publication_year=publication_year, price=price)
    session.add(book)
    session.commit()
    
    session.close()
    click.echo(f"Book '{title}' added successfully!")
