from datetime import datetime
from typing import Dict, Tuple, List, Optional

from models.book import Book
from models.review import Review
from models.transaction import Transaction
from models.person import Person


class LibraryManager:
    def __init__(self):
        """
        Initialize a BookManager object.
        """
        self.books: List[Book] = []  # Use a list to store the books
        self.reviews: Dict[Tuple[str, str], List[Review]] = {}  # Use a dictionnary to store the reviews by (author, title)
        self.transactions = []
        self.persons = []
        self.transactions = []

    def add_book(self, book: Book) -> None:
        """
        Adds a book to the list of books.

        :param book: Book: The book object to be added to the list.

        :return: None
        """
        self.books.append(book)

    def add_review(self, author,  title, review_text, rating=0):
        """
        Add a review to a book.

        :param author: str: Author of the book.
        :param review_text: str: Text of the review.
        :param rating: int: Rating given by the reviewer.
        :param title: str: Title of the book.

        :return: Review: The newly created review object.
        :rtype: Review
        """
        key = (author, title)
        review = Review(author, review_text, rating, title)
        if key in self.reviews:
            self.reviews[key].append(review)
        else:
            self.reviews[key] = [review]
        return review

    def add_transaction(self, book, buyer, date, status):
        """
        Add a transaction to the list of transactions.


        :param book: Book: The book object involved in the transaction.
        :param buyer: Buyer: The buyer object involved in the transaction.
        :param date: str: The date of the transaction.
        :param status: str: The status of the transaction.

        :return: The newly created transaction object.
        :rtype: Transaction
        """
        transaction = Transaction(book, buyer, date, status)
        self.transactions.append(transaction)
        return transaction

    def get_average_rating(self, author, title):
        reviews = self.get_reviews_by_title_and_author(author, title)
        if not reviews:
            return 0
        return sum(review.get_rating() for review in reviews) / len(reviews)

    def get_books(self):
        """
        Retrieves all the books.

        :return: A list of all the books.
        :rtype: List
        """
        return self.books

    def get_reviews(self):
        """
        Retrieves all the reviews from the object.

        :return: A list containing all the reviews.
        :rtype: List
        """
        reviews = [review for sublist in self.reviews.values() for review in sublist]
        return reviews

    def find_book(self, author: str, title: str) -> Optional[Book]:
        """
        Find and return a book with the given author and title.

        :param author: str: The author of the book.
        :param title: str: The title of the book.

        :return: The book with the given author and title, or None if no such book exists.
        :rtype: Optional[Book]
        """
        for book in self.books:
            if book.author == author and book.title == title:
                return book
        return None

    def get_reviews_by_title_and_author(self, author, title):
        """
        Retrieve all the reviews for a book with the given title and author.

        :param author: The author of the book.
        :param title: The title of the book.

        :return: A list of review objects for the book with the given title and author.
        :rtype: List
        """
        key = (author, title)
        return self.reviews.get(key, [])

    def get_transactions(self):
        """
        Get the transactions.

        :return: The list of transactions.
        :rtype: List
        """
        return self.transactions

    def is_book_available(self, author, title):
        """
        Check if a book is available for borrowing.

        :param author: str: The author of the book.
        :param title: str: The title of the book.

        :return: True if the book is available, False otherwise.
        :rtype: bool
        """
        # Browse book list
        for book in self.books:
            # Check if the book corresponds to the given author and title, and if it is available.
            if book.author == author and book.title == title and book.borrower is None:
                return True
        return False

    def remove_book(self, book: Book) -> None:
        """
        Removes a book from the inventory.

        :param book: Book: The book to be removed from the inventory.

        :return: None
        """
        if book in self.books:
            self.books.remove(book)
        else:
            print("Book not found in the inventory.")

    def create_person(self, name: str, age: int, email: str, address: str) -> Person:
        """
        Creates a new person and adds them to the list of people.

        :param name: The name of the person.
        :param age: The age of the person.
        :param email: The email address of the person.
        :param address: The home address of the person.

        :return: The created Person object.
        :rtype: Person
        """
        person = Person(address, age, email, name)
        self.persons.append(person)
        return person

    def get_person_by_email(self, email: str) -> Optional[Person]:
        """
        Finds and returns a person by their email address.

        :param email: The email address to search for.

        :return: Person: The Person object if found, otherwise None.
        :rtype: Optional[Person]
        """
        for person in self.persons:
            if person.email == email:
                return person
        return None

    def create_transaction(self, book: Book, borrower: Person, due_date: datetime, transaction_type: str) -> Transaction:
        """
        Creates a new transaction and adds it to the list of transactions.

        :param book: Book: The book being borrowed.
        :param borrower: Person: The person borrowing the book.
        :param due_date: datetime: The date the book is due to be returned.
        :param transaction_type: str: The type of transaction ("borrow" or "purchase").

        :return: Transaction: The created Transaction object.
        :rtype: Transaction
        """
        transaction = Transaction(book, borrower, due_date, transaction_type=transaction_type)
        self.transactions.append(transaction)
        return transaction

    def get_overdue_transactions(self) -> List[Transaction]:
        """
        Returns a list of overdue transactions.

        This function retrieves all transactions from the `self.transactions` list
        where the `due_date` is before the current date and the `status` is set to "borrowed".

        :return: A list of `Transaction` objects representing the overdue transactions.
        :rtype: List[Transaction]
        """
        today = datetime.now()
        return [
            transaction
            for transaction in self.transactions
            if transaction.date < today and transaction.transaction_type == "borrow"
        ]

    def get_transaction_by_book_and_borrower(self, author: str, title: str, borrower: Person) -> Optional[Transaction]:
        """
        Returns a transaction by book and borrower.

        :param author: str: The author of the book.
        :param title: str: The title of the book.
        :param borrower: Person: The borrower of the book.

        :return: The transaction object if found, None otherwise.
        :rtype: Optional[Transaction]
        """
        for transaction in self.transactions:
            if (
                transaction.book.author == author
                and transaction.book.title == title
                and transaction.buyer == borrower
                and transaction.transaction_type == "borrow"
            ):
                return transaction
        return None

    def get_transactions_by_person(self, person: Person) -> List[Transaction]:
        """
        Returns a list of transactions for a specific person.

        :param person: The person whose transactions are to be retrieved.

        :return: A list of Transaction objects.
        :rtype: List[Transaction]
        """
        return [transaction for transaction in self.transactions if transaction.borrower == person]

    @staticmethod
    def send_email(receiver_email, subject, body):
        """
        Sends an email to the specified receiver email address.

        :param receiver_email: str: The email address of the recipient.
        :param subject: str: The subject line of the email.
        :param body: str: The body content of the email.

        :return: None
        """
        print(f"Sending Email to {receiver_email}")
        print(f"Subject: {subject}")
        print(f"Message: {body}")
