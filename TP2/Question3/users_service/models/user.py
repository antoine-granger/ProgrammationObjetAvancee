from users_service import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def serialize(self):
        """
        Serializes the object into a dictionary.

        :return: A dictionary containing the serialized object.
        :rtype: dict
        """
        return {
            'id': self.id,
            'username': self.title,
            'password': self.author,
            'role': self.role
        }
