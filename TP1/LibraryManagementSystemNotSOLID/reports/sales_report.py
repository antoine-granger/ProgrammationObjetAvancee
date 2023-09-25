class SalesReport:
    def __init__(self, book_manager):
        """
        Initialize a SalesReport object with a BookManager instance.
        :param book_manager:
        """
        self.book_manager = book_manager

    def generate_report(self):
        """
        Generates a sales report based on the transactions stored in the book manager.
        
        Returns:
            str: The sales report containing information about each transaction.
        """
        transactions = self.book_manager.get_transactions()
        report = "Sales Report:\n"
        for transaction in transactions:
            report += f"- Buyer: {transaction.buyer}\n"
            report += f"  - Book: {transaction.book}\n"
            report += f"  - Date: {transaction.date}\n"
            report += f"  - Status: {transaction.status}\n"
        return report
