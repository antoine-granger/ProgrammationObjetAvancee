class Book:
    def __init__(self, author, isbn, price, title, year):
        """
        Initialize a Book object.

        :param isbn:
        :param title:
        :param author:
        :param year:
        :param price:
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.state = "New"
        self.borrower = None
        self.borrow_duration = None

    def __str__(self) -> str:
        """
        Returns a string representation of the Book object.

        :return: The string representation of the Book object.
        :rtype: str
        """
        return f"Book: {self.title} by {self.author} ({self.year}) - ${self.price:.2f}"

    def get_isbn(self):
        """
        Returns the ISBN of the book.

        :return: The ISBN of the book.
        :rtype: str
        """
        return self.isbn

    def get_price(self):
        """
        Get the price of the book.

        :return: The price of the book.
        :rtype: float
        """
        return self.price
