import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set a random seed for reproducibility
np.random.seed(42)

# Generator function to yield synthetic time series data point by point
def generate_stock_data(initial_price=100.0, volatility=0.02):
    current_price = initial_price

    while True:
        daily_return = np.random.normal(loc=0, scale=volatility)
        current_price *= (1 + daily_return)

        yield current_price

if __name__ == "__main__":
    stock_data_generator = generate_stock_data()

    # Collect data points for plotting
    prices = []

    for _ in range(600):
        prices.append(next(stock_data_generator))

    # Create a DataFrame for plotting
    stock_data = pd.DataFrame({'StockPrice': prices})

    # Plot the generated stock data
    plt.figure(figsize=(12, 6))
    plt.plot(stock_data.index, stock_data['StockPrice'], label='Stock Price')
    plt.title('Synthetic Stock Price Time Series Data')
    plt.ylabel('Stock Price')
    plt.legend()
    plt.show()