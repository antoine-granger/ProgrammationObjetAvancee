from models.book import Book
from models.review import Review
from models.transaction import Transaction

class BookManager:
    def __init__(self):
        self.books = []
        self.transactions = []

    def add_book(self, isbn, title, author, year, price, quantity):
        book = Book(isbn, title, author, year, price, quantity)
        self.books.append(book)
        return book

    def add_review(self, isbn, review_text, rating):
        for book in self.books:
            if book.get_isbn() == isbn:
                review_instance = Review(book, review_text, rating)
                book.add_review(review_instance)
                return review_instance

    def add_transaction(self, book, buyer, date, status):
        transaction = Transaction(book, buyer, date, status)
        self.transactions.append(transaction)
        return transaction

    def get_books(self):
        return self.books

    def get_reviews(self):
        reviews = []
        for book in self.books:
            reviews.extend(book.get_reviews())
        return reviews

    def get_transactions(self):
        return self.transactions
