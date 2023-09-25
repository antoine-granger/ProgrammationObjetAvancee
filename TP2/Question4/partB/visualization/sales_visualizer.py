import matplotlib.pyplot as plt


class SalesVisualizer:
    def __init__(self, dataframe):
        """
        Initializes an instance of the class.

        :param dataframe: (pandas.DataFrame): The input dataframe.
        """
        self.dataframe = dataframe

    def plot_sales_trend(self):
        """
        Generates a plot of the sales trend for October 2023.
        """
        sales_trend = self.dataframe.groupby("Date").sum(numeric_only=True)["Sales"]
        sales_trend.plot(figsize=(12, 6))
        plt.title("Sales Trend for October 2023")
        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.grid(True)
        plt.show()

    def plot_sales_by_product(self):
        """
        Generates a plot of the sales trend for October 2023.
        """
        # Group by product and sum sales
        sales_by_product = self.dataframe.groupby("Product").sum(numeric_only=True)[
            "Sales"
        ]

        # Plotting
        sales_by_product.sort_values().plot(
            kind="barh", figsize=(10, 6), color="skyblue"
        )
        plt.title("Total Sales by Product for October 2023")
        plt.xlabel("Total Sales")
        plt.ylabel("Product")
        plt.grid(axis="x")
        plt.tight_layout()
        plt.show()

    def plot_sales_by_store(self):
        """
        Plots the total sales by store for October 2023.
        """
        # Group by store and sum sales
        sales_by_store = self.dataframe.groupby("Store").sum(numeric_only=True)["Sales"]

        # Plotting
        sales_by_store.sort_values().plot(
            kind="bar", figsize=(10, 6), color="lightgreen"
        )
        plt.title("Total Sales by Store for October 2023")
        plt.ylabel("Total Sales")
        plt.xlabel("Store")
        plt.xticks(rotation=45)
        plt.grid(axis="y")
        plt.tight_layout()
        plt.show()
