from managers.library import Library
from models.book import Book
from reports.review_report import ReviewReportGenerator
from reports.sales_report import SalesReportGenerator

from utils.email_sender import EmailSender


def main():
    # Initialize manager classes
    library = Library()

    # Create some example books
    book1 = Book(author="Author1", isbn="ISBN1", price=10.0, title="Title1", year=2021)
    book2 = Book(author="Author2", isbn="ISBN2", price=15.0, title="Title2", year=2020)

    # Add some example books
    library.library_manager.add_book(book1)
    library.library_manager.add_book(book2)

    # Add some example persons (users)
    person1 = library.library_manager.create_person(age=30, address="Rue des lilas", email="person1@example.com", name="Person1")
    person2 = library.library_manager.create_person(age=18, address="Boulevard nicolas", email="person2@example.com", name="Person2")

    # Add some example reviews
    review1 = library.library_manager.add_review(author="Author1", rating=4, title="Title1", review_text="Good book")
    review2 = library.library_manager.add_review(author="Author2", rating=3.5, title="Title2", review_text="Bad book !")
    review3 = library.library_manager.add_review(author="Author1", rating=5, title="Title1", review_text="Fantastic book !")

    # Borrow and return books
    print(f"###### Borrow ######")
    borrow_result = library.borrow_book(borrower=person1, author="Author1", title="Title1")
    print(f"Borrow result :\n{borrow_result}")

    # Send an email notification
    library.notify_overdue_borrowers()

    # Return a book
    print(f"\n###### Return borrowed book ######\nReturn result: ")
    library.return_book(borrower=person1, author="Author1", title="Title1")

    # Buy a book
    print(f"\n###### Purchase book ######")
    purchase_result = library.purchase_book(buyer=person2, author="Author2", title="Title2")
    print(f"Purchase result: \n{purchase_result}")

    # Generate a review report
    review_report_generator = ReviewReportGenerator(library.library_manager)
    review_report = review_report_generator.generate_report(library.library_manager.books)
    print(f"\n###### Review Report ######\n{review_report}")

    # Generate a sales report
    sales_report_generator = SalesReportGenerator()
    sales_report = sales_report_generator.generate_report(library.library_manager.transactions)
    print(f"\n###### Sales Report ######\n{sales_report}")


if __name__ == "__main__":
    main()
