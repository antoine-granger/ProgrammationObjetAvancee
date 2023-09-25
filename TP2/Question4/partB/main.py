from analysis.sale_predictor import SalesPredictor
from analysis.sales_analyzer import SalesAnalyzer
from models.sales_dataframe_creator import SalesDataframeCreator
from utils.helpers import format_currency
from visualization.sales_visualizer import SalesVisualizer


def main():
    """
    Executes the main function of the program.

    This function creates a SalesDataframeCreator object to retrieve a dataframe
    containing sales data. Then, it creates a SalesAnalyzer object to analyze
    the sales data and print out the best selling products, best selling stores,
    best selling dates, total sales, and sales for the last 5 days.

    Next, it creates a SalesVisualizer object to visualize the sales data by
    plotting the sales trend, sales by product, and sales by store.

    Finally, it creates a SalesPredictor object to predict the sales for the
    next 5 days and prints out the predictions.
    """
    creator = SalesDataframeCreator()
    df = creator.get_dataframe()

    analyzer = SalesAnalyzer(df)
    print("Best Selling Products:\n", analyzer.best_selling_products())
    print("\nBest Selling Stores:\n", analyzer.best_selling_stores())
    print("\nBest Selling Dates:\n", analyzer.best_selling_dates())
    print("\nTotal Sales:\n", format_currency(analyzer.total_sales()))
    print("\nSales for last 5 days:\n", analyzer.get_sales_for_last_days(5))

    visualizer = SalesVisualizer(df)
    visualizer.plot_sales_trend()
    visualizer.plot_sales_by_product()
    visualizer.plot_sales_by_store()

    predictor = SalesPredictor(df)
    predictions_df = predictor.predict_sales(5)
    print("\nPredictions for next 5 days:\n", predictions_df)


if __name__ == "__main__":
    main()
