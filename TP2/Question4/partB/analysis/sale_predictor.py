import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


class SalesPredictor:
    def __init__(self, dataframe):
        """
        Initializes a new instance of the class.

        :param dataframe: pandas.DataFrame: The input dataframe.
        """
        self.dataframe = dataframe

    def predict_sales(self, future_days=5):
        """
        Predicts future sales based on historical data.

        :param future_days: int: The number of days to predict future sales for. Default is 5.

        :return: predictions_df : A DataFrame containing the future dates and the predicted sales for those dates.
        :rtype: pandas.DataFrame
        """
        # Prepare the data
        df = self.dataframe.groupby('Date').sum(numeric_only=True).reset_index()
        df['Day'] = df['Date'].dt.day

        # Variables independents and dependents
        x = df['Day'].values.reshape(-1, 1)  # Reshape pour avoir un array 2D
        y = df['Sales'].values

        # Creation and training of the model
        model = LinearRegression()
        model.fit(x, y)

        # Predict the future sales
        last_day = df['Day'].max()
        future_dates = np.array(range(last_day + 1, last_day + 1 + future_days)).reshape(-1, 1)
        predicted_sales = model.predict(future_dates)

        # Create the DataFrame to return
        future_dates_df = pd.date_range(start=df['Date'].max() + pd.DateOffset(1), periods=future_days)
        predictions_df = pd.DataFrame({
            'Date': future_dates_df,
            'Predicted Sales': [int(sale) for sale in predicted_sales]
        })

        return predictions_df
