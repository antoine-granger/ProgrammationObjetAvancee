from datetime import datetime

from models.person import Person
from models.book import Book


class Transaction:
    def __init__(self, book: Book, buyer: Person, date: datetime, transaction_type):
        """
        Initializes a new instance of the class.
        
        :param book: Book: The book object associated with the transaction.
        :param buyer: Person: The person object representing the buyer.
        :param date: datetime: The date of the transaction.
        :param transaction_type: str: The type of transaction ("purchase" or "borrow").
        """
        self.book = book
        self.buyer = buyer
        self.date = date
        self.transaction_type = transaction_type  # "purchase" or "borrow"

    def __str__(self):
        """
        Returns a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """
        return f"Transaction: {self.book} by :{self.buyer.__str__()} \nDate:({self.date})"

    def update_status(self, transaction_type: str):
        """
        Updates the status of the object.

        :param transaction_type: str: The new status.

        :return: None
        """
        # Vérification de la validité du statut
        valid_statuses = ["purchase", "borrow", "returned"]
        if transaction_type not in valid_statuses:
            print("Invalid status")
            return
    
        self.transaction_type = transaction_type
