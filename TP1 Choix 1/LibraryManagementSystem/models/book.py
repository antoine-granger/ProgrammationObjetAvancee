class Book:
    def __init__(self, isbn, title, author, year, price, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.quantity = quantity
        self.reviews = []

    """
    Returns a string representation of the Book object.
    Returns:
        str: The string representation of the Book object.
    """
    def __str__(self) -> str:
        return f"Book: {self.title} by {self.author} ({self.year}) - ${self.price:.2f}"

    # This method is violating the SRP
    # Because it is doing two things: adding a review and printing a message
    """
    Get the reviews of the book.
    Returns:
        The reviews of the book.
    """
    def add_review(self, review):
        self.reviews.append(review)
        print(f"Review added: {review.review_text} ({review.rating}/5)")

    def get_reviews(self):
        return self.reviews

    """
    Calculate the average rating of the book.
    Returns:
        float: The average rating of the book.
    """
    def get_average_rating(self):
        if len(self.reviews) == 0:
            return 0
        else:
            return sum([review[1] for review in self.reviews]) / len(self.reviews)

    """
    Returns the ISBN of the book.

    :return: The ISBN of the book.
    :rtype: str
    """
    def get_isbn(self):
        return self.isbn

    """
    Get the price of the book.

    Returns:
        The price of the book.
    """
    def get_price(self):
        return self.price
