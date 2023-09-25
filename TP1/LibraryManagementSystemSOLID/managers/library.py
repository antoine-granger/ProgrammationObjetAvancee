from datetime import datetime, timedelta
from typing import Optional

from managers.book_manager import BookManager
from managers.person_manager import PersonManager
from managers.transaction_manager import TransactionManager
from models.person import Person
from utils.email_sender import EmailSender


class Library:
    def __init__(self, book_manager: BookManager, person_manager: PersonManager, transaction_manager: TransactionManager, email_sender: EmailSender):
        """
        Initialize a Library object.
        """
        self.book_manager = book_manager
        self.person_manager = person_manager
        self.transaction_manager = transaction_manager
        self.email_sender = email_sender

    def borrow_book(self, borrower: Person, author: str, title: str):
        """
        Borrow a book for a given borrower.
        
        :param borrower: Person: The person who wants to borrow the book.
        :param author: str: The author of the book.
        :param title: str: The title of the book.
        
        :return: A string representing the transaction details if the book is successfully borrowed.
        :rtype: str
        
        Notes:
            - If the borrower is None, the function returns "Borrower not found."
            - If the book is not available, the function prints "Book is not available."
        """
        if borrower is None:
            return "Borrower not found."

        # Check if the book is available
        if self.book_manager.is_book_available(author, title):
            # Create a transaction of type "borrow"
            due_date = datetime.now() + timedelta(days=-14)  # To test book due date notification
            book = self.book_manager.find_book(author, title)
            transaction = self.transaction_manager.create_transaction(book, borrower, due_date, "borrow")

            # Update the book's borrower
            book.borrower = borrower
            self.book_manager.remove_book(book)
            return transaction.__str__()
        else:
            print("Book is not available.")

    def purchase_book(self, buyer: Person, author, title):
        """
        Purchase a book.

        :param buyer : Person: The person who is purchasing the book.
        :param author: str: The author of the book.
        :param title: str: The title of the book.

        :return: The transaction object representing the purchase of the book.
        :rtype: Transaction
        """
        # Check if the book is available
        if self.book_manager.is_book_available(author, title):
            # Create a transaction of type "purchase"
            book = self.book_manager.find_book(author, title)
            transaction = self.transaction_manager.create_transaction(book, buyer, datetime.now(), "purchased")

            # Remove the book from the inventory
            self.book_manager.remove_book(book)  # Ajoutez une méthode pour retirer un livre de l'inventaire
            return transaction
        else:
            print("Book is not available.")

    def return_book(self, borrower: Person, author: str, title: str):
        """
        Return a book that was borrowed by a borrower.

        :param borrower: Person: The borrower who borrowed the book.
        :param author: str: The author of the book.
        :param title: str: The title of the book.

        :return: None
        """
        # Find the transaction
        transaction = self.transaction_manager.get_transaction_by_book_and_borrower(
            author, title, borrower
        )
        if transaction is None or transaction.transaction_type != "borrow":
            print("The book has not been borrowed.")
            return

        # Mark the transaction as returned
        transaction.transaction_type = "returned"

        # Add the book to the list of books
        book = transaction.book
        self.book_manager.books.append(book)

        print(f"The book '{book.title}' with ISBN '{book.isbn}' has been returned.")

    def add_member(self, address, age, name, email):
        """
        Adds a new member to the system.
        
        :param address: str: The address of the member.
        :param age: int: The age of the member.
        :param name: str: The name of the member.
        :param email: str: The email of the member.
        
        :return: None
        """
        self.person_manager.create_person(address, age, email, name)

    def notify_overdue_borrowers(self):
        """
        Notifies borrowers who have overdue books.

        Retrieves the list of overdue transactions using the `transaction_manager` and
        prints the number of overdue transactions. For each overdue transaction,
        constructs a notification message and emails it to the borrower using the
        `email_sender`.

        :return: None
        """
        # Get the list of overdue transactions
        overdue_transactions = self.transaction_manager.get_overdue_transactions()
        print(f"There are {len(overdue_transactions)} overdue transactions.")
        for transaction in overdue_transactions:
            borrower = transaction.buyer
            book = transaction.book
    
            # Construct the notification message
            subject = "Overdue Book Return"
            message = (
                f"Dear {borrower.name},\n\n"
                f"You have borrowed the book '{book.title}' which was due on {transaction.date}. "
                "Please return it as soon as possible.\n\nKind regards,\nThe Library"
            )
    
            # Email the overdue recipient
            self.email_sender.send_email(borrower.email, subject, message)
