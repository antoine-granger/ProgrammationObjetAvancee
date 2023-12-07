from books_service import db


class AvailableIDs(db.Model):
    """
    A model representing an available ID.
    """
    __tablename__ = 'available_ids'

    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        """
        Serializes the object into a dictionary.

        :return: A dictionary containing the serialized object.
        :rtype: dict
        """
        return {'id': self.id}
