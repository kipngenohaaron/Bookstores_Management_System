from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuthorGenre(Base):
    __tablename__ = 'author_genre'
    
    id = Column(Integer, primary_key=True)
    author_name = Column(String)
    birth_year = Column(Integer)
    nationality = Column(String)
    genre_name = Column(String)

    # Define a one-to-many relationship with books
    books = relationship('Book', back_populates='author')

class Book(Base):
    __tablename__ = 'book'
    
    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    
    # Define foreign key relationships for author and genre
    author_id = Column(Integer, ForeignKey('author_genre.id'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    
    publication_year = Column(Integer)
    price = Column(Float)

    # Define many-to-one relationship with author_genre for author and genre
    author = relationship('AuthorGenre', foreign_keys=[author_id], back_populates='books')
    genre = relationship('Genre', foreign_keys=[genre_id], back_populates='books')

    # Define one-to-many relationship with order_items
    order_items = relationship('OrderItem', back_populates='book')  # This line should be included

   
class Genre(Base):
    __tablename__ = 'genre'

    id = Column(Integer, primary_key=True)
    genre_name = Column(String)

    # Define a one-to-many relationship with books
    books = relationship('Book', back_populates='genre')

class Customer(Base):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    email = Column(String)
    phone = Column(String)

    # Define a one-to-many relationship with order_items
    order_items = relationship('OrderItem', back_populates='customer')

class OrderItem(Base):
    __tablename__ = 'order_item'
    
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    book_id = Column(Integer, ForeignKey('book.book_id'))
    order_date = Column(Date)
    total_amount = Column(Float)
    quantity_in_stock = Column(Integer)

    # Define many-to-one relationships with customer and book
    customer = relationship('Customer', back_populates='order_items')
    book = relationship('Book', back_populates='order_items')

    # Method to calculate the total order amount
    def calculate_total_amount(self):
        return self.total_amount
