from datetime import datetime
from typing import List, Optional
from models.transaction import Transaction
from models.book import Book
from models.person import Person


class TransactionManager:
    def __init__(self):
        """
        Initializes a new instance of the class.
        """
        self.transactions = []

    def create_transaction(self, book: Book, borrower: Person, due_date: datetime, transaction_type: str) -> Transaction:
        """
        Creates a new transaction and adds it to the list of transactions.

        :param book: Book: The book being borrowed.
        :param borrower: Person: The person borrowing the book.
        :param due_date: datetime: The date the book is due to be returned.
        :param transaction_type: str: The type of transaction ("borrow" or "purchase").

        :return: Transaction: The created Transaction object.
        :rtype: Transaction
        """
        transaction = Transaction(book, borrower, due_date, transaction_type=transaction_type)
        self.transactions.append(transaction)
        return transaction

    def get_overdue_transactions(self) -> List[Transaction]:
        """
        Returns a list of overdue transactions.

        This function retrieves all transactions from the `self.transactions` list
        where the `due_date` is before the current date and the `status` is set to "borrowed".

        :return: A list of `Transaction` objects representing the overdue transactions.
        :rtype: List[Transaction]
        """
        today = datetime.now()
        return [
            transaction
            for transaction in self.transactions
            if transaction.date < today and transaction.transaction_type == "borrow"
        ]

    def get_transaction_by_book_and_borrower(self, author: str, title: str, borrower: Person) -> Optional[Transaction]:
        """
        Returns a transaction by book and borrower.

        :param author: str: The author of the book.
        :param title: str: The title of the book.
        :param borrower: Person: The borrower of the book.

        :return: The transaction object if found, None otherwise.
        :rtype: Optional[Transaction]
        """
        for transaction in self.transactions:
            if (
                transaction.book.author == author
                and transaction.book.title == title
                and transaction.buyer == borrower
                and transaction.transaction_type == "borrow"
            ):
                return transaction
        return None

    def get_transactions_by_person(self, person: Person) -> List[Transaction]:
        """
        Returns a list of transactions for a specific person.

        :param person: The person whose transactions are to be retrieved.

        :return: A list of Transaction objects.
        :rtype: List[Transaction]
        """
        return [transaction for transaction in self.transactions if transaction.borrower == person]
