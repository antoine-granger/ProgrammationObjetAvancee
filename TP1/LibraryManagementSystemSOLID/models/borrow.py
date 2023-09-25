from datetime import datetime

from models.book import Book
from models.person import Person


class Borrow:
    def __init__(self, book: Book, borrower: Person, due_date: datetime):
        """
        Initializes a new instance of the BorrowedBook class.

        :param book: The book being borrowed.
        :param borrower: The person borrowing the book.
        :param due_date: The due date for returning the book.
        """
        self.book = book
        self.borrower = borrower
        self.borrowing_date = datetime.now()
        self.due_date = due_date

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: The string representation of the object.
        :rtype: str
        """
        return f"Borrow: {self.book} by {self.borrower} ({self.due_date})"
