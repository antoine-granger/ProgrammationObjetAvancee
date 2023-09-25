class Book:
    def __init__(self, isbn, title, author, year, price, quantity):
        """
        Initialize a Book object.
        :param isbn:
        :param title:
        :param author:
        :param year:
        :param price:
        :param quantity:
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.quantity = quantity
        self.reviews = []

    def __str__(self) -> str:
        """
        Returns a string representation of the Book object.
        Returns:
            str: The string representation of the Book object.
        """
        return f"Book: {self.title} by {self.author} ({self.year}) - ${self.price:.2f}"

    def add_review(self, review):
        """
        Get the reviews of the book.

        Note: This implementation violates the Single Responsibility Principle (SRP).

        SRP Violation: The add_review method is responsible for adding a review to the book, but it is doing two things:
        adding a review and printing a message

        Returns:
            The reviews of the book.
        """
        self.reviews.append(review)
        print(f"Review added: {review.review_text} ({review.rating}/5)")

    def get_reviews(self):
        """
        Get the reviews.

        Returns:
            The reviews.
        """
        return self.reviews

    def get_average_rating(self):
        """
        Calculate the average rating of the book.

        Returns:
            float: The average rating of the book.
        """
        if len(self.reviews) == 0:
            return 0
        else:
            return sum([review[1] for review in self.reviews]) / len(self.reviews)

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

        Returns:
            The price of the book.
        """
        return self.price
