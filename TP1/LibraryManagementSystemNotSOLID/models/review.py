class Review:
    def __init__(self, author, review_text, rating, title):
        """
        Initialize a Review instance.

        :param author: str: Author of the review.
        :param review_text: str: Text of the review.
        :param rating: float: Rating given by the reviewer.
        :param title: str: Title of the review.
        """
        self.title = title
        self.author = author
        self.review_text = review_text
        self.rating = rating

    def __str__(self) -> str:
        """
        Return a string representation of the object.
    
        :return: A string representation of the object.
        :rtype: str
        """
        return f"Review for '{self.title}' by {self.author}: {self.review_text} ({self.rating}/5)"

    def get_rating(self):
        """
        Get the rating of the object.

        :return: The rating of the object.
        :rtype: int
        """
        return self.rating

    def get_review_text(self):
        """
        Return the review text.

        :return: The review text.
        :rtype: str
        """
        return self.review_text
