import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AuthorGenre, Book, Genre, Customer, OrderItem
from datetime import datetime
from sqlalchemy.orm import joinedload


# Actual database URL
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

@cli.command()
def list_customers():
    """List all customers in the bookstore"""
    session = DBSession()
    customers = session.query(Customer).all()
    session.close()
    for customer in customers:
        print(f"Customer ID: {customer.customer_id}, Name: {customer.customer_name}, Email: {customer.email}, Phone: {customer.phone}")

# @cli.command()
# def list_orders():
#     """List all customer orders in the bookstore"""
#     session = DBSession()
#     orders = session.query(OrderItem).all()
#     session.close()
#     for order in orders:
#         print(f"Order ID: {order.order_id}, Customer ID: {order.customer.customer_id}, Book ID: {order.book.book_id}, Order Date: {order.order_date}, Total Amount: {order.total_amount}")

@cli.command()
def list_orders():
    """List all customer orders in the bookstore"""
    session = DBSession()
    orders = session.query(OrderItem).options(joinedload(OrderItem.customer), joinedload(OrderItem.book)).all()
    session.close()
    for order in orders:
        print(f"Order ID: {order.order_id}, Customer ID: {order.customer.customer_id}, Book ID: {order.book.book_id}, Order Date: {order.order_date}, Total Amount: {order.total_amount}")




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
    author_genre = session.query(AuthorGenre).filter_by(author_name=author_name, genre_name=genre_name).first()
    if author_genre is None:
        click.echo(f"Author '{author_name}' and Genre '{genre_name}' do not exist. Please add them first.")
        return
    
    # Use the author_id and genre_id from the author_genre object
    book = Book(title=book_title, author_id=author_genre.id, genre_id=author_genre.genre_id, publication_year=publication_year, price=price)
    order_item = OrderItem(customer_id=None, book=book, order_date=None, total_amount=0.0, quantity_in_stock=quantity_in_stock)
    session.add(order_item)
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

if __name__ == '__main__':
    cli()
