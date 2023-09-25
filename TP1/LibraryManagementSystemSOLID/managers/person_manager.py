from typing import Optional

from models.person import Person


class PersonManager:
    def __init__(self):
        """
        Initializes a new instance of the PersonManager class.
        """
        self.people = []

    def create_person(self, name: str, age: int, email: str, address: str) -> Person:
        """
        Creates a new person and adds them to the list of people.

        :param name: The name of the person.
        :param age: The age of the person.
        :param email: The email address of the person.
        :param address: The home address of the person.

        :return: The created Person object.
        :rtype: Person
        """
        person = Person(address, age, email, name)
        self.people.append(person)
        return person

    def get_person_by_email(self, email: str) -> Optional[Person]:
        """
        Finds and returns a person by their email address.

        :param email: The email address to search for.

        :return: Person: The Person object if found, otherwise None.
        :rtype: Optional[Person]
        """
        for person in self.people:
            if person.email == email:
                return person
        return None
