from users_service import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    A model representing a user.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        """
        Creates a hashed password and stores it in the password_hash field.

        :param password: The user's password.
        :type password: str
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the hashed password against the given password.

        :param password: The password to check against the hashed password.
        :type password: str

        :return: True if the password matches, False otherwise.
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        """
        Serializes the object into a dictionary.

        :return: A dictionary containing the serialized object.
        :rtype: dict
        """
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }
