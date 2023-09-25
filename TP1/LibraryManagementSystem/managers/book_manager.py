from models.book import Book
from models.review import Review
from models.transaction import Transaction


class BookManager:
    def __init__(self):
        """
        Initialize a BookManager object.
        """
        self.books = []
        self.transactions = []

    def add_book(self, isbn, title, author, year, price, quantity):
        """
        Adds a book to the list of books.

        Parameters:
            isbn (str): The ISBN of the book.
            title (str): The title of the book.
            author (str): The author of the book.
            year (int): The year the book was published.
            price (float): The price of the book.
            quantity (int): The quantity of the book.

        Returns:
            Book: The newly added book object.
        """
        book = Book(isbn, title, author, year, price, quantity)
        self.books.append(book)
        return book

    def add_review(self, isbn, review_text, rating):
        """
        Adds a review for a book with a given ISBN.

        Parameters:
            isbn (str): The ISBN of the book.
            review_text (str): The text of the review.
            rating (int): The rating of the review.

        Returns:
            Review: The newly created Review instance.

        """
        for book in self.books:
            if book.get_isbn() == isbn:
                review_instance = Review(book, review_text, rating)
                book.add_review(review_instance)
                return review_instance

    def add_transaction(self, book, buyer, date, status):
        """
        Add a transaction to the list of transactions.

        Args:
            book (Book): The book object involved in the transaction.
            buyer (Buyer): The buyer object involved in the transaction.
            date (str): The date of the transaction.
            status (str): The status of the transaction.

        Returns:
            Transaction: The newly created transaction object.
        """
        transaction = Transaction(book, buyer, date, status)
        self.transactions.append(transaction)
        return transaction

    def get_books(self):
        """
        Get the list of books.

        Returns:
            list: The list of books.
        """
        return self.books

    def get_reviews(self):
        """
        Retrieves all the reviews from the books in the library.

        Returns:
            list: A list of review objects from the books in the library.
        """
        reviews = []
        for book in self.books:
            reviews.extend(book.get_reviews())
        return reviews

    def get_transactions(self):
        """
        Get the transactions.

        Returns:
            list: The list of transactions.
        """
        return self.transactions
