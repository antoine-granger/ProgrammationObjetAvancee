from typing import List

from managers.library_manager import LibraryManager
from models.book import Book
from reports.report_generator import ReportGenerator


class ReviewReportGenerator(ReportGenerator):
    """
    Implement the ReportGenerator interface and define a concrete product.
    """

    def __init__(self, library_manager: LibraryManager):
        """
        Initializes a new instance of the class.

        :param library_manager: BookManager: The book manager object.

        :return: None
        """
        self.book_manager = library_manager

    def generate_report(self, books: List[Book]) -> str:
        """
        Generates a report based on a list of books.

        :param books: List[Book]: A list of Book objects representing the books to be included in the report.

        :return: The generated report as a string.
        :rtype: str
        """
        report = "Review Report:\n"
        for book in books:
            report += f"- Book: {book.title}\n"
            report += f"  - Average rating: {self.book_manager.get_average_rating(book.author, book.title)}/5\n"
            report += "  - Reviews:\n"

            book_reviews = self.book_manager.reviews.get((book.author, book.title), [])
    
            for review in book_reviews:
                report += f"    - Review: {review.get_review_text()}\n"
                report += f"    - Rating: {review.get_rating()}/5\n"
    
        return report

