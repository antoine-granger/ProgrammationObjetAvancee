from typing import TypeVar, Generic

T = TypeVar("T")  # Declare type variable


class Box(Generic[T]):
    """
    Generic class to hold items of any type.
    """

    def __init__(self, item: T):
        self.item = item

    def get_item(self) -> T:
        """
        Returns the item contained in the box.
        """
        return self.item


# Create instances of Box with different types
int_box = Box(5)
str_box = Box("Hello")

int_box_item = int_box.get_item()
str_box_item = str_box.get_item()

print(f"int_box_item: {int_box_item}\nstr_box_item: {str_box_item}")
