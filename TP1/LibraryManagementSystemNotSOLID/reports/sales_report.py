from typing import List
from reports.report_generator import ReportGenerator
from models.transaction import Transaction


class SalesReportGenerator(ReportGenerator):
    """
    Implement the ReportGenerator interface and define a concrete product.
    """

    def generate_report(self, transactions: List[Transaction]) -> str:
        report = "Sales Report:\n"
        for transaction in transactions:
            report += f"  - Book: {transaction.book}\n"
            report += f"  - Date: {transaction.date}\n"
            report += f"  - Buyer: {transaction.buyer}\n"
            report += f"  - type of purchase: {transaction.transaction_type}\n\n"
        return report
