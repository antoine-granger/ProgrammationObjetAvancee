class SalesReport:
    def __init__(self, book_manager):
        """
        Initialize a SalesReport object with a BookManager instance.
        """
        self.book_manager = book_manager

    def generate_report(self):
        """
        Generate a report based on the sales transactions.
        """
        transactions = self.book_manager.get_transactions()
        report = "Sales Report:\n"
        for transaction in transactions:
            report += f"- Buyer: {transaction.buyer}\n"
            report += f"  - Book: {transaction.book}\n"
            report += f"  - Date: {transaction.date}\n"
            report += f"  - Status: {transaction.status}\n"
        return report
