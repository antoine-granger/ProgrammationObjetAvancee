from books_service import db


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    author = db.Column(db.String(120), nullable=False)

    def serialize(self):
        """
        Serializes the object into a dictionary.

        :return: A dictionary containing the serialized object.
        :rtype: dict
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author
        }
