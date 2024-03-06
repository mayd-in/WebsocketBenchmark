import tornado.web
import tornado.websocket
import asyncio
import json
import datetime
import strategy
import pandas as pd

SAMPLE_SIZE = 100
TIMESTAMPS = []
LATENCIES = []

def show_benchmark():
    df = pd.DataFrame({'Timestamp': TIMESTAMPS, 'Latency': LATENCIES})
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Calculate statistics
    std_deviation = df['Latency'].std()
    max_value = df['Latency'].max()
    min_value = df['Latency'].min()
    average_value = df['Latency'].mean()

    print("BENCHMARK RESULTS")
    print("Sample Size:", SAMPLE_SIZE)
    print("Average:", average_value)
    print("Maximum:", max_value)
    print("Minimum:", min_value)
    print("Standard Deviation:", std_deviation)

    try:
        import matplotlib.pyplot as plt
        # Plot the time series data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Timestamp'], df['Latency'], label='Time Series Data')
        plt.xlabel('Timestamp')
        plt.ylabel('Value')
        plt.title('Time Series Data Plot')
        
        # Annotate the plot with statistical measures
        plt.axhline(y=average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
        plt.axhline(y=max_value, color='g', linestyle='--', label=f'Max: {max_value:.2f}')
        plt.axhline(y=min_value, color='b', linestyle='--', label=f'Min: {min_value:.2f}')
        plt.axhline(y=std_deviation, color='purple', linestyle='--', label=f'Std Dev: {std_deviation:.2f}')

        plt.legend()
        plt.show()
    except:
        pass

async def main():
    ws_uri = "ws://localhost:8765/"
    trading_strategy = strategy.TradingStrategy()
    client = await tornado.websocket.websocket_connect(ws_uri)
    try:
        while True:
            message = await client.read_message()
            message = json.loads(message)
            if message["type"] == "broadcast":
                trading_strategy.feed_value(message["value"])
                result = trading_strategy.result()
                if result == strategy.Order.BUY:
                    order = {
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "type": "buy",
                        "value": message["value"]
                    }
                    await client.write_message(json.dumps(order))
                    print("Buy order")
                elif result == strategy.Order.SELL:
                    order = {
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "type": "sell",
                        "value": message["value"]
                    }
                    await client.write_message(json.dumps(order))
                    print("Sell order")
            elif message["type"] == "response":
                now = datetime.datetime.utcnow()
                timestamp = datetime.datetime.fromisoformat(message["timestamp"])
                difference = now  - timestamp
                latency = difference/datetime.timedelta(milliseconds=1)
                TIMESTAMPS.append(timestamp)
                LATENCIES.append(latency)
                print("Response latency:", latency, "milliseconds")
                if len(TIMESTAMPS) >= SAMPLE_SIZE:
                    break
            else:
                print("Bad message type")
    finally:
        client.close()
        show_benchmark()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Client closed")