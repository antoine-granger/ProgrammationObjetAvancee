from managers.book_manager import BookManager
from managers.library import Library
from managers.person_manager import PersonManager
from managers.transaction_manager import TransactionManager
from models.book import Book
from reports.review_report import ReviewReportGenerator
from reports.sales_report import SalesReportGenerator

from utils.email_sender import EmailSender

# Initialize manager classes
book_manager = BookManager()
person_manager = PersonManager()
transaction_manager = TransactionManager()
email_sender = EmailSender()
library = Library(book_manager, person_manager, transaction_manager, email_sender)

# Create some example books
Book1 = Book(author="Author1", isbn="ISBN1", price=10.0, title="Title1", year=2021)
Book2 = Book(author="Author2", isbn="ISBN2", price=15.0, title="Title2", year=2020)

# Add some example books
book_manager.add_book(Book1)
book_manager.add_book(Book2)

# Add some example persons (users)
Person1 = person_manager.create_person(age=30, address="Rue des lilas", email="person1@example.com", name="Person1")
Person2 = person_manager.create_person(age=18, address="Boulevard nicolas", email="person2@example.com", name="Person2")

# Add some example reviews
Review1 = book_manager.add_review(author="Author1", rating=4, title="Title1", review_text="Good book")
Review2 = book_manager.add_review(author="Author2", rating=3.5, title="Title2", review_text="Bad book !")
Review3 = book_manager.add_review(author="Author1", rating=5, title="Title1", review_text="Fantastic book !")

# Borrow and return books
print(f"###### Borrow ######")
borrow_result = library.borrow_book(borrower=Person1, author="Author1", title="Title1")
print(f"Borrow result :\n{borrow_result}")

# Send an email notification
library.notify_overdue_borrowers()

# Return a book
print(f"\n###### Return borrowed book ######\nReturn result: ")
return_result = library.return_book(borrower=Person1, author="Author1", title="Title1")

# Buy a book
print(f"\n###### Purchase book ######")
purchase_result = library.purchase_book(buyer=Person2, author="Author2", title="Title2")
print(f"Purchase result: \n{purchase_result}")

# Generate a review report
review_report_generator = ReviewReportGenerator(book_manager)
review_report = review_report_generator.generate_report(book_manager.books)
print(f"\n###### Review Report ######\n{review_report}")

# Generate a sales report
sales_report_generator = SalesReportGenerator()
sales_report = sales_report_generator.generate_report(transaction_manager.transactions)
print(f"\n###### Sales Report ######\n{sales_report}")
