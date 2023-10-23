class Animal:
    """
    Base class for all animals.
    """

    def speak(self) -> str:
        """
        Returns the sound made by the animal.
        """
        return "Unknown sound"


class Dog(Animal):
    """
    Dog class inheriting from Animal.
    """

    def speak(self) -> str:
        """
        Returns the sound made by the dog.
        """
        return "Woof!"


class Cat(Animal):
    """
    Cat class inheriting from Animal.
    """

    def speak(self) -> str:
        """
        Returns the sound made by the cat.
        """
        return "Meow!"


# Test polymorphism
def animal_sound(animal: Animal) -> str:
    """
    Returns the sound of the given animal.
    """
    return animal.speak()


# Testing the classes
dog = Dog()
cat = Cat()

dog_response = dog.speak()
cat_response = cat.speak()
polymorphic_response = animal_sound(dog), animal_sound(cat)

print(f"dog: {dog_response}\ncat: {cat_response}\npolymorphic: {polymorphic_response}")
