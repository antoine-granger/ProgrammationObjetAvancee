from abc import ABC, abstractmethod
from typing import List


class ReportGenerator(ABC):
    """
    Define the interface of interest to clients.
    """

    @abstractmethod
    def generate_report(self, items: List) -> str:
        """
        Generates a report based on the provided list of items.
        Args:
            items (List): A list of objects representing the items to include in the report.
        Returns:
            str: A string representation of the generated report.
        """
        pass
