# Author: KIPNGENOH A.

# Bookstore Management System CLI

The Bookstores Management System is a Python-based command-line application for managing a bookstore's inventory, customers, and orders. This system allows you to perform various tasks, including adding and updating books, managing customers, and tracking orders. It is built using SQLAlchemy for database management and Click for creating a command-line interface.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [List Books](#list-books)
  - [List Customers](#list-customers)
  - [List Orders](#list-orders)
  - [Add Customer](#add-customer)
  - [Add Book](#add-book)
  - [Update Customer](#update-customer)
  - [Update Book](#update-book)
  - [Delete Customer](#delete-customer)
  - [Delete Book](#delete-book)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before using the Bookstore Management System CLI, ensure you have the following prerequisites installed:

- Python (3.6 or higher)
- SQLAlchemy (A Python SQL toolkit and Object-Relational Mapping library)
- SQLite (A lightweight and file-based relational database)

## Installation

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/kipngenohaaron/Bookstores_Management_System.git
   ```

2. Navigate to the project directory:

   ```shell
   cd bookstore-management-cli
   ```

3. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

4. Initialize the SQLite database by running the `seeds.py` script:

   ```shell
   python seeds.py
   ```

## Usage

The Bookstore Management System CLI provides several commands to manage your bookstore efficiently. You can use the following commands:

### List Books

List all books in the bookstore:

```shell
python cli.py list-books
```

### List Customers

List all customers in the bookstore:

```shell
python cli.py list-customers
```

### List Orders

List all customer orders in the bookstore:

```shell
python cli.py list-orders
```


### Add Customer

Add a new customer to the bookstore:

```shell
python cli.py add-customer "Customer Name" "customer@example.com" "123-456-7890"
```

### Add Book

Add a new book to the bookstore:

```shell
python cli.py add-book "Book Title" "Author Name" "Genre Name" PUBLICATION_YEAR PRICE QUANTITY_IN_STOCK
```

Replace `PUBLICATION_YEAR`, `PRICE`, and `QUANTITY_IN_STOCK` with the actual values.

### Update Customer

Update customer information:

```shell
python cli.py update-customer CUSTOMER_ID "new-email@example.com" "new-phone-number"
```

Replace `CUSTOMER_ID`, `new-email@example.com`, and `new-phone-number` with the actual values.

### Update Book

Update book information:

```shell
python cli.py update-book BOOK_ID "New Book Title" "New Author Name" "New Genre Name" NEW_PUBLICATION_YEAR NEW_PRICE NEW_QUANTITY_IN_STOCK
```

Replace `BOOK_ID`, `New Book Title`, `New Author Name`, `New Genre Name`, `NEW_PUBLICATION_YEAR`, `NEW_PRICE`, and `NEW_QUANTITY_IN_STOCK` with the actual values.

### Delete Customer

Delete a customer from the bookstore:

```shell
python cli.py delete-customer CUSTOMER_ID
```

Replace `CUSTOMER_ID` with the actual customer ID.

### Delete Book

Delete a book from the bookstore:

```shell
python cli.py delete-book BOOK_ID
```

Replace `BOOK_ID` with the actual book ID.

## Contact Information
Email: kipngenohaaron@gmail.com
Phone Number: 0724 279 400 / 0724 828 197

## dbdiagram
### Link: https://dbdiagram.io/d/64f6e09102bd1c4a5efa9d19

## Database

The application uses a SQLite database to store book, customer, and order data. The database file `bookstore.db` will be created in the project directory when you run the `create_database.py` script.


## Contributing

If you would like to contribute to this project or report issues, please open an issue or pull request on the GitHub repository: [bookstore-management-cli](hhttps://github.com/kipngenohaaron/Bookstores_Management_System.git).

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3. Commit your changes and push them to your fork: `git push origin feature/your-feature-name`.
4. Create a pull request describing your changes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Click](https://click.palletsprojects.com/en/7.x/)


