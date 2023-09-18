class Transaction:
    def __init__(self, book, buyer, date, status):
        self.book = book
        self.buyer = buyer
        self.date = date
        self.status = status

    # This method is violating the SRP
    # Because it is doing two things: adding a review and printing a message
    def process(self):
        self.status = "processed"
        print(f"Transaction processed: {self.book} by {self.buyer} ({self.date})")