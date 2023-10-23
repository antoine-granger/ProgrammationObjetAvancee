import time

import numpy as np
import pandas as pd


class SalesDataframeCreator:
    """
    This class is responsible for creating a DataFrame containing
    fictitious sales data.
    """

    def __init__(self):
        """Initialize and create the DataFrame."""
        self._data = self._create_dataframe()

    def _create_dataframe(self):
        """
        Create a DataFrame with fictitious data representing sales.

        :return: DataFrame containing the fictitious data.
        :rtype: pd.DataFrame
        """
        # Settings
        np.random.seed(int(time.time()))
        dates = pd.date_range("2023-10-01", "2023-10-31")
        products = ["Computer", "Phone", "Chair", "Desk", "Headset"]

        # Create the DataFrame
        data = {
            "Date": np.random.choice(dates, 500),
            "Store": np.random.choice(["Store_A", "Store_B", "Store_C"], 500),
            "Product": np.random.choice(products, 500),
            "Sales": np.random.randint(1, 50, 500),
        }

        return pd.DataFrame(data)

    def get_dataframe(self):
        """
        Return the created DataFrame.

        :return: DataFrame containing the fictitious data.
        :rtype: pd.DataFrame
        """
        return self._data
