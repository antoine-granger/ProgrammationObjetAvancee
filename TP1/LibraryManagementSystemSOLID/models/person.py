class Person:
    def __init__(self, address, age, email, name):
        """
        Initializes a new instance of the class.

        :param address: str: The address of the person.
        :param age: int: The age of the person.
        :param email: str: The email address of the person.
        :param name: str: The name of the person.
        """
        self.name = name
        self.age = age
        self.email = email
        self.address = address

    def __str__(self):
        """
        Return a string representation of the object.

        :return: A string containing the name, age, email, and address of the object.
        :rtype: str
        """
        return (
            f"\n\tName: {self.name},"
            f"\n\tAge: {self.age},"
            f"\n\tEmail: {self.email},"
            f"\n\tAddress: {self.address}"
        )

    def send_email(self, message, subject):
        """
        Sends an email to the specified recipient.

        :param message: str: The content of the email.
        :param subject: str: The subject of the email.

        :return: None
        """
        print(f"Sending Email to {self.email}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
