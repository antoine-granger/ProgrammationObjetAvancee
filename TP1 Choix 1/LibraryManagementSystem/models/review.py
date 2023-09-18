class Review:
    def __init__(self, book, review_text, rating):
        self.book = book
        self.review_text = review_text
        self.rating = rating

    def __str__(self) -> str:
        return f"Review: {self.review_text} ({self.rating}/5)"

    def get_rating(self):
        return self.rating

    def get_book(self):
        return self.book

    def get_review_text(self):
        return self.review_text