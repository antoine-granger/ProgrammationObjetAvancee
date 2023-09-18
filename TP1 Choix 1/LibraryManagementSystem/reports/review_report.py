class ReviewReport:
    def __init__(self, book_manager):
        """
        Initialize a ReviewReport object with a BookManager instance.
        """
        self.book_manager = book_manager

    def generate_report(self):
        """
        Generate a report based on the reviews of the books.

        Note: This implementation violates the Single Responsibility Principle (SRP)
        and the Open/Closed Principle (OCP).

        SRP Violation: The generate_report method is responsible for both generating
        the report and retrieving the list of books. This violates SRP as this class
        now has an additional responsibility of getting the list of books.

        OCP Violation: If we want to add new features or change the way reviews are
        retrieved or filtered, we would need to modify this class instead of extending
        or composing it. This violates OCP as the class is not closed for modification.
        """
        books = self.book_manager.get_books()
        reviews = self.book_manager.get_reviews()
        report = "Review Report:\n"
        for book in books:
            report += f"- Book: {book.title}\n"
            report += "  - Reviews:\n"
            for review in book.get_reviews():
                report += f"    - Review: {review.get_review_text()}\n"
                report += f"    - Rating: {review.get_rating()}/5\n"
        return report
