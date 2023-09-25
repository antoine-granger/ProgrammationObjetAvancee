class Review:
    def __init__(self, book, review_text, rating):
        """
        Initialize a Review instance.
        :param book:
        :param review_text:
        :param rating:
        """
        self.book = book
        self.review_text = review_text
        self.rating = rating

    def __str__(self) -> str:
        """
        Return a string representation of the object.
        
        :return: A string representation of the object.
        :rtype: str
        """
        return f"Review: {self.review_text} ({self.rating}/5)"

    def get_rating(self):
        """
        Get the rating of the object.
        
        Returns:
            The rating of the object.
        """
        return self.rating

    def get_book(self):
        """
        Get the value of the book attribute.
        
        Returns:
            The value of the book attribute.
        """
        return self.book

    def get_review_text(self):
        """
        Return the review text.
        
        Returns:
            str: The review text.
        """
        return self.review_text
