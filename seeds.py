from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AuthorGenre, Book, Genre, Customer, OrderItem
from datetime import datetime

# actual database URL
database_url = 'sqlite:///bookstore.db'

engine = create_engine(database_url)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Seed data for AuthorGenre
# Seed data for AuthorGenre
authors = [
    AuthorGenre(author_name='F. Scott Fitzgerald', birth_year=1900, nationality='American', genre_name='Fiction')
]

session.add_all(authors)
session.commit()

# Seed data for Genre
genres = [
    Genre(genre_name='Fiction')
]

session.add_all(genres)
session.commit()

authors = [
    AuthorGenre(author_name='Author 1', birth_year=1980, nationality='Nationality 1', genre_name='Genre 1'),
    AuthorGenre(author_name='Author 2', birth_year=1990, nationality='Nationality 2', genre_name='Genre 2')
]

session.add_all(authors)
session.commit()

# Seed data for Genre
genres = [
    Genre(genre_name='Genre 1'),
    Genre(genre_name='Genre 2')
]

session.add_all(genres)
session.commit()

# Seed data for Book
books = [
    Book(title='Book 1', author_id=1, genre_id=1, publication_year=2000, price=20.0),
    Book(title='Book 2', author_id=2, genre_id=2, publication_year=2010, price=215.0)
]

session.add_all(books)
session.commit()

# Seed data for Customer
customers = [
    Customer(customer_name='Customer 1', email='customer1@example.com', phone='123-456-7890'),
    Customer(customer_name='Customer 2', email='customer2@example.com', phone='987-654-3210')
]

session.add_all(customers)
session.commit()

# Seed data for OrderItem
order_items = [
    OrderItem(customer_id=1, book_id=1, order_date=datetime.now(), total_amount=20.0, quantity_in_stock=10),
    OrderItem(customer_id=2, book_id=2, order_date=datetime.now(), total_amount=25.0, quantity_in_stock=5)
]

session.add_all(order_items)
session.commit()

session.close()
