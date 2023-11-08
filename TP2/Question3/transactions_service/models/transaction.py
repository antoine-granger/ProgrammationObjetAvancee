from transactions_service import db


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)  # Primary key to identify the transaction
    user = db.Column(db.ForeignKey('user.id'), nullable=False)  # User id
    book = db.Column(db.ForeignKey('book.id'), nullable=False)  # Book id
    category = db.Column(db.String(80), nullable=False)  # Category of transaction (borrow, return, buy, sell)
    value = db.Column(db.Integer, nullable=False)  # Value of transaction (in case of buying or selling)

    def serialize(self):
        """
        Serializes the object into a dictionary.

        :return: A dictionary containing the serialized object.
        :rtype: dict
        """
        return {
            'id': self.id,
            'user': self.user,
            'book': self.book,
            'category': self.category,
            'value': self.value
        }
