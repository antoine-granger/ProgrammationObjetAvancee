from transactions_service import db


class AvailableIDs(db.Model):
    __tablename__ = 'available_ids'

    id = db.Column(db.Integer, primary_key=True)

    def serialize(self):
        """
        Serializes the object into a dictionary.

        :return: A dictionary containing the serialized object.
        :rtype: dict
        """
        return {'id': self.id}
