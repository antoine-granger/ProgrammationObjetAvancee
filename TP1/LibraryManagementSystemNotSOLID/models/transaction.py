class Transaction:
    def __init__(self, book, buyer, date, status):
        """
        Initialize a Transaction object.
        :param book:
        :param buyer:
        :param date:
        :param status:
        """
        self.book = book
        self.buyer = buyer
        self.date = date
        self.status = status

    def process(self):
        """
        Updates the status of the transaction to "processed" and prints a message with the details of the transaction.
        
        Note: This implementation violates the Single Responsibility Principle (SRP).
        
        SRP Violation: The update_status method is responsible for updating the status of the transaction, but it is
        doing two things: updating the status and printing a message

        Returns:
            None
        """
        self.status = "processed"
        print(f"Transaction processed: {self.book} by {self.buyer} ({self.date})")
