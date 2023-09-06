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
    for book in books:
        # Accessing related objects, so the session should remain open
        author_name = book.author.author_name if book.author else "Unknown Author"
        genre_name = book.genre.genre_name if book.genre else "Unknown Genre"
        print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {author_name}, Genre: {genre_name}")
    
    session.close()

# Other commands...



# Command to add a new book to the bookstore
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
        session.close()
        return
    
    # Use the author_id and genre_id from the author_genre object
    book = Book(title=title, author_id=author_genre.id, genre_id=author_genre.genre_id, publication_year=publication_year, price=price)
    session.add(book)
    session.commit()  # Commit the changes to persist them in the database
    
    session.close()
    click.echo(f"Book '{title}' added successfully!")

# Command to list all authors
@cli.command()
def list_authors():
    """List all authors"""
    session = DBSession()
    authors = session.query(AuthorGenre).all()
    session.close()
    for author in authors:
        print(f"Author ID: {author.id}, Name: {author.author_name}, Birth Year: {author.birth_year}, Nationality: {author.nationality}")

# Command to add a new author
@cli.command()
@click.argument('name')
@click.argument('birth_year', type=int)
@click.argument('nationality')
@click.argument('genre')
def add_author(name, birth_year, nationality, genre):
    """Add a new author to the bookstore"""
    session = DBSession()
    
    # Check if the genre already exists in the database
    existing_genre = session.query(Genre).filter_by(genre_name=genre).first()
    if existing_genre is None:
        click.echo(f"Genre '{genre}' does not exist. Please add it first.")
        return
    
    author_genre = AuthorGenre(author_name=name, birth_year=birth_year, nationality=nationality, genre=genre)
    session.add(author_genre)
    session.commit()
    
    session.close()
    click.echo(f"Author '{name}' added successfully!")

# Command to list all genres
@cli.command()
def list_genres():
    """List all genres"""
    session = DBSession()
    genres = session.query(Genre).all()
    session.close()
    for genre in genres:
        print(f"Genre ID: {genre.id}, Genre Name: {genre.genre_name}")

# Command to add a new genre
@cli.command()
@click.argument('genre_name')
def add_genre(genre_name):
    """Add a new genre to the bookstore"""
    session = DBSession()
    
    genre = Genre(genre_name=genre_name)
    session.add(genre)
    session.commit()
    
    session.close()
    click.echo(f"Genre '{genre_name}' added successfully!")

# Command to list all customers
@cli.command()
def list_customers():
    """List all customers"""
    session = DBSession()
    customers = session.query(Customer).all()
    session.close()
    for customer in customers:
        print(f"Customer ID: {customer.customer_id}, Name: {customer.customer_name}, Email: {customer.email}, Phone: {customer.phone}")

# Command to add a new customer
@cli.command()
@click.argument('name')
@click.argument('email')
@click.argument('phone')
def add_customer(name, email, phone):
    """Add a new customer to the bookstore"""
    session = DBSession()
    
    customer = Customer(customer_name=name, email=email, phone=phone)
    session.add(customer)
    session.commit()
    
    session.close()
    click.echo(f"Customer '{name}' added successfully!")

# Command to add a new order item
@cli.command()
@click.argument('customer_id', type=int)
@click.argument('book_id', type=int)
@click.argument('total_amount', type=float)
@click.argument('quantity_in_stock', type=int)
def add_order_item(customer_id, book_id, total_amount, quantity_in_stock):
    """Add a new order item to the bookstore"""
    session = DBSession()
    
    # Check if the customer and book exist in the database
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    book = session.query(Book).filter_by(book_id=book_id).first()
    if customer is None or book is None:
        click.echo(f"Customer or book not found. Please check the IDs.")
        return
    
    order_date = datetime.now()
    order_item = OrderItem(customer=customer, book=book, order_date=order_date, total_amount=total_amount, quantity_in_stock=quantity_in_stock)
    session.add(order_item)
    session.commit()
    
    session.close()
    click.echo(f"Order item added successfully!")

if __name__ == '__main__':
    cli()
