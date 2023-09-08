import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AuthorGenre, Book, Genre, Customer, OrderItem
from datetime import datetime
from sqlalchemy.orm import joinedload

# Actual database URL
database_url = 'sqlite:///bookstore.db'

# Create a database engine and bind it to the Base metadata
engine = create_engine(database_url)
Base.metadata.bind = engine

# Create a session factory
DBSession = sessionmaker(bind=engine)

# Define the main CLI group
@click.group()
def cli():
    """Bookstore Management System CLI"""

# Command to list all books in the bookstore
@cli.command()
def list_books():
    """List all books in the bookstore"""
    session = DBSession()
    books = session.query(Book).all()
    session.close()
    for book in books:
        print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author_genre.author_name}, Genre: {book.genre.genre_name}")

# Command to list all customers in the bookstore
@cli.command()
def list_customers():
    """List all customers in the bookstore"""
    session = DBSession()
    customers = session.query(Customer).all()
    session.close()
    for customer in customers:
        print(f"Customer ID: {customer.customer_id}, Name: {customer.customer_name}, Email: {customer.email}, Phone: {customer.phone}")

# Command to add a new author to the bookstore
@cli.command()
@click.argument('author_name')
def add_author(author_name):
    """Add a new author to the bookstore"""
    session = DBSession()
    
    # Create a new AuthorGenre instance
    author = AuthorGenre(author_name=author_name)
    
    # Add the author to the session and commit the transaction
    session.add(author)
    session.commit()
    
    # Close the session and provide feedback
    session.close()
    click.echo(f"Author '{author_name}' added successfully!")

# Command to add a new genre to the bookstore
@cli.command()
@click.argument('genre_name')
def add_genre(genre_name):
    """Add a new genre to the bookstore"""
    session = DBSession()
    
    # Create a new Genre instance
    genre = Genre(genre_name=genre_name)
    
    # Add the genre to the session and commit the transaction
    session.add(genre)
    session.commit()
    
    # Close the session and provide feedback
    session.close()
    click.echo(f"Genre '{genre_name}' added successfully!")

# Command to list all customer orders with customer and book details
@cli.command()
def list_orders():
    """List all customer orders in the bookstore"""
    session = DBSession()
    
    # Query all order items and eagerly load associated customer and book data
    orders = session.query(OrderItem).options(joinedload(OrderItem.customer), joinedload(OrderItem.book)).all()
    
    # Close the session
    session.close()
    
    # Print order information
    for order in orders:
        print(f"Order ID: {order.order_id}, Customer ID: {order.customer.customer_id}, Book ID: {order.book.book_id}, Order Date: {order.order_date}, Total Amount: {order.total_amount}")

# Command to search books by title, author, or genre
@cli.command()
@click.option("--title", help="Search books by title.")
@click.option("--author", help="Search books by author name.")
@click.option("--genre", help="Search books by genre name.")
def search_books(title, author, genre):
    """Search books based on title, author, or genre."""
    session = DBSession()

    # Create a query that selects books and eagerly loads author and genre data
    query = session.query(Book).join(AuthorGenre).join(Genre)

    # Add filters based on provided options
    if title:
        query = query.filter(Book.title.like(f"%{title}%"))

    if author:
        query = query.filter(AuthorGenre.author_name.like(f"%{author}%"))

    if genre:
        query = query.filter(Genre.genre_name.like(f"%{genre}%"))

    # Execute the query and get the list of matching books
    books = query.all()

    # Close the session
    session.close()

    # Display the results or indicate no matching books found
    if not books:
        print("No matching books found.")
    else:
        print("Matching books:")
        for book in books:
            print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author_genre.author_name}, Genre: {book.genre.genre_name}")

@cli.command()
def list_books():
    """List all books in the bookstore"""
    session = DBSession()
    
    # Use joinedload to load the 'author' and 'genre' relationships in the same query
    books = session.query(Book).options(joinedload(Book.author), joinedload(Book.genre)).all()
    
    session.close()
    
    for book in books:
        # Now you can access the 'author' and 'genre' attributes without issues
        print(f"Book ID: {book.book_id}, Title: {book.title}, Author: {book.author.author_name}, Genre: {book.genre.genre_name}")

# Adding the book
@cli.command()
@click.argument('book_title')
@click.argument('author_name')
@click.argument('genre_name')
@click.argument('publication_year', type=int)
@click.argument('price', type=float)
@click.argument('quantity_in_stock', type=int)
def add_book(book_title, author_name, genre_name, publication_year, price, quantity_in_stock):
    """Add a new book to the bookstore"""
    session = DBSession()
    
    # Check if author and genre already exist in the database or create them if not
    author = session.query(AuthorGenre).filter_by(author_name=author_name).first()
    genre = session.query(Genre).filter_by(genre_name=genre_name).first()
    
    if author is None:
        author = AuthorGenre(author_name=author_name)
        session.add(author)
    
    if genre is None:
        genre = Genre(genre_name=genre_name)
        session.add(genre)

    # Create a new book instance and add it to the session
    book = Book(
        title=book_title,
        author=author,
        genre=genre,
        publication_year=publication_year,
        price=price,
    )
    session.add(book)

    # Create an order item for the book and set its quantity in stock
    order_item = OrderItem(book=book, quantity_in_stock=quantity_in_stock)
    session.add(order_item)

    # Commit the changes and close the session
    session.commit()
    session.close()
    
    click.echo(f"Book '{book_title}' added successfully!")


@cli.command()
def list_inventory():
    """List the inventory of books in the bookstore"""
    session = DBSession()
    books = session.query(Book).all()
    session.close()
    for book in books:
        print(f"Book ID: {book.book_id}, Title: {book.title}, Quantity in Stock: {book.order_items[0].quantity_in_stock if book.order_items else 0}")

@cli.command()
@click.argument('customer_name')
@click.argument('email')
@click.argument('phone')
def add_customer(customer_name, email, phone):
    """Add a new customer to the bookstore"""
    session = DBSession()
    
    customer = Customer(customer_name=customer_name, email=email, phone=phone)
    session.add(customer)
    session.commit()
    
    session.close()
    click.echo(f"Customer '{customer_name}' added successfully!")

@cli.command()
@click.argument('book_title')
@click.argument('author_name')
@click.argument('genre_name')
@click.argument('publication_year', type=int)
@click.argument('price', type=float)
@click.argument('quantity_in_stock', type=int)
def add_book(book_title, author_name, genre_name, publication_year, price, quantity_in_stock):
    """Add a new book to the bookstore"""
    session = DBSession()
    
    # Check if author and genre already exist in the database
    author = session.query(AuthorGenre).filter_by(author_name=author_name).first()
    genre = session.query(Genre).filter_by(genre_name=genre_name).first()
    
    if author is None:
        author = AuthorGenre(author_name=author_name)
        session.add(author)
        session.commit()
    
    if genre is None:
        genre = Genre(genre_name=genre_name)
        session.add(genre)
        session.commit()
    
    book = Book(title=book_title, author_id=author.id, genre_id=genre.id, publication_year=publication_year, price=price, quantity_in_stock=quantity_in_stock)
    session.add(book)
    session.commit()
    
    session.close()
    click.echo(f"Book '{book_title}' added successfully!")

@cli.command()
@click.argument('customer_id', type=int)
@click.argument('email')
@click.argument('phone')
def update_customer(customer_id, email, phone):
    """Update customer information"""
    session = DBSession()
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    
    if customer:
        customer.email = email
        customer.phone = phone
        session.commit()
        session.close()
        click.echo(f"Customer information updated successfully!")
    else:
        session.close()
        click.echo(f"Customer with ID {customer_id} does not exist.")

@cli.command()
@click.argument('book_id', type=int)
@click.argument('book_title')
@click.argument('author_name')
@click.argument('genre_name')
@click.argument('publication_year', type=int)
@click.argument('price', type=float)
@click.argument('quantity_in_stock', type=int)
def update_book(book_id, book_title, author_name, genre_name, publication_year, price, quantity_in_stock):
    """Update book information"""
    session = DBSession()
    book = session.query(Book).filter_by(book_id=book_id).first()
    
    if book:
        author_genre = session.query(AuthorGenre).filter_by(author_name=author_name, genre_name=genre_name).first()
        if author_genre is None:
            click.echo(f"Author '{author_name}' and Genre '{genre_name}' do not exist. Please add them first.")
            return

        book.title = book_title
        book.author_id = author_genre.id
        book.genre_id = author_genre.genre_id
        book.publication_year = publication_year
        book.price = price

        order_item = session.query(OrderItem).filter_by(book_id=book_id).first()
        if order_item:
            order_item.quantity_in_stock = quantity_in_stock

        session.commit()
        session.close()
        click.echo(f"Book information updated successfully!")
    else:
        session.close()
        click.echo(f"Book with ID {book_id} does not exist.")

@cli.command()
@click.argument('customer_id', type=int)
def delete_customer(customer_id):
    """Delete a customer from the bookstore"""
    session = DBSession()
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    
    if customer:
        session.delete(customer)
        session.commit()
        session.close()
        click.echo(f"Customer with ID {customer_id} deleted successfully!")
    else:
        session.close()
        click.echo(f"Customer with ID {customer_id} does not exist.")
@cli.command()
@click.argument('customer_id', type=int)
@click.argument('book_id', type=int)
@click.argument('order_date')
@click.argument('total_amount', type=float)
@click.argument('quantity_in_stock', type=int)
def add_order_item(customer_id, book_id, order_date, total_amount, quantity_in_stock):
    """Add a new order item to the bookstore"""
    session = DBSession()

    # Check if the customer and book exist
    customer = session.query(Customer).filter_by(customer_id=customer_id).first()
    book = session.query(Book).filter_by(book_id=book_id).first()

    if customer is None:
        session.close()
        click.echo(f"Customer with ID {customer_id} does not exist.")
        return

    if book is None:
        session.close()
        click.echo(f"Book with ID {book_id} does not exist.")
        return

    # Convert the order date to a datetime object
    try:
        order_date = datetime.strptime(order_date, '%Y-%m-%d')
    except ValueError:
        session.close()
        click.echo("Invalid date format. Please use YYYY-MM-DD.")
        return

    order_item = OrderItem(
        customer_id=customer_id,
        book_id=book_id,
        order_date=order_date,
        total_amount=total_amount,
        quantity_in_stock=quantity_in_stock,
    )

    session.add(order_item)
    session.commit()
    session.close()

    click.echo("Order item added successfully!")


@cli.command()
@click.argument('book_id', type=int)
def delete_book(book_id):
    """Delete a book from the bookstore"""
    session = DBSession()
    book = session.query(Book).filter_by(book_id=book_id).first()
    
    if book:
        session.delete(book)
        session.commit()
        session.close()
        click.echo(f"Book with ID {book_id} deleted successfully!")
    else:
        session.close()
        click.echo(f"Book with ID {book_id} does not exist.")

@cli.command()
def list_orders():
    """List all customer orders in the bookstore"""
    session = DBSession()
    orders = session.query(OrderItem).all()
    if not orders:
        click.echo("No customer orders found.")
        session.close()
        return

    for order in orders:
        # Load the related customer and book objects within the same session
        order = session.merge(order, load=False)  # Merge the detached object
        customer = order.customer
        book = order.book

        print(f"Order ID: {order.order_id}")
        print(f"Customer ID: {customer.customer_id}")
        print(f"Book ID: {book.book_id}")
        print(f"Order Date: {order.order_date}")
        print(f"Total Amount: {order.total_amount}")
        print(f"Quantity in Stock: {order.quantity_in_stock}")
        print()

    session.close()


if __name__ == '__main__':
    cli()
