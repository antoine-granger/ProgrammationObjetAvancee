class SalesAnalyzer:
    def __init__(self, dataframe):
        """
        Initializes an instance of the class.

        :param dataframe: (pandas.DataFrame): The input dataframe.
        """
        self.dataframe = dataframe

    def best_selling_products(self):
        """
        Calculate the best-selling products.

        :return: A series containing the total sales for each product, sorted in descending order.
        :rtype: pandas.Series
        """
        best_selling_products_series = (
            self.dataframe.groupby("Product")
            .sum(numeric_only=True)
            .sort_values(by="Sales", ascending=False)["Sales"]
        )

        best_selling_products_df = best_selling_products_series.reset_index()
        best_selling_products_df.columns = ["Date", "Sales"]

        return best_selling_products_df

    def best_selling_stores(self):
        """
        Returns a pandas Series object that contains the total sales for each store, sorted in descending order.

        :return: A pandas Series object with store IDs as the index and the corresponding total sales as the values.
        :rtype: pandas.Series
        """
        best_selling_stores_series = (
            self.dataframe.groupby("Store")
            .sum(numeric_only=True)
            .sort_values(by="Sales", ascending=False)["Sales"]
        )

        best_selling_stores_df = best_selling_stores_series.reset_index()
        best_selling_stores_df.columns = ["Date", "Sales"]

        return best_selling_stores_df

    def best_selling_dates(self):
        """
        Calculates the best-selling dates based on the given dataframe.

        :return: A pandas Series object representing the best-selling dates.
        :rtype: pandas.Series
        """
        best_selling_date_series = (
            self.dataframe.groupby("Date")
            .sum(numeric_only=True)
            .sort_values(by="Sales", ascending=False)["Sales"]
        )

        best_selling_date_df = best_selling_date_series.reset_index()
        best_selling_date_df.columns = ["Date", "Sales"]

        return best_selling_date_df

    def total_sales(self):
        """
        Calculate and return the total sales from the dataframe.

        :return: The total sales amount.
        :rtype: float
        """
        return self.dataframe["Sales"].sum()

    def get_sales_for_last_days(self, days=5):
        """
        Get the total sales for the last `days` days.

        :param days: The number of days to consider for the sales calculation. Default is 5.
        :type days: int, optional

        :return: A pandas Series object containing the sum of sales for the last `days` days.
        :rtype: pandas.Series
        """
        sales_for_last_days_series = (
            self.dataframe.groupby("Date")
            .sum(numeric_only=True)["Sales"]
            .sort_index(ascending=False)
            .head(days)
        )

        sales_for_last_days_df = sales_for_last_days_series.reset_index()
        sales_for_last_days_df.columns = ["Date", "Sales"]

        return sales_for_last_days_df
