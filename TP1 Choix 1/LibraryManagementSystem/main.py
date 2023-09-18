from managers.book_manager import BookManager
from reports.review_report import ReviewReport
from reports.sales_report import SalesReport


def main():
    # Création d'un gestionnaire de livres
    book_manager = BookManager()

    # Ajout de livres
    book1 = book_manager.add_book(isbn="978-0-441-01359-3", title="Dune", author="Frank Herbert",
                                  year=1965, price=10.99, quantity=10)
    book2 = book_manager.add_book(isbn="978-0-553-29335-7", title="Foundation", author="Isaac Asimov",
                                  year=1951, price=8.99, quantity=5)

    # Ajout de revues
    book_manager.add_review(isbn="978-0-441-01359-3", review_text="Great read!", rating=5)
    book_manager.add_review(isbn="978-0-553-29335-7", review_text="A bit slow in the middle, but overall good.",
                            rating=4)

    # Ajout de transactions
    book_manager.add_transaction(book=book1, buyer="Alice", date="2023-09-12", status="pending")
    book_manager.add_transaction(book=book2, buyer="Bob", date="2023-09-13", status="pending")

    # Générer les rapports
    sales_report = SalesReport(book_manager)
    review_report = ReviewReport(book_manager)

    print(sales_report.generate_report())
    print(review_report.generate_report())


if __name__ == "__main__":
    main()
