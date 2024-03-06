# Python Websockets Benchmark
A simple benchmark application that compares Python Websockets and Tornado Websockets implementations.

For this benchmark a generator is implemented that simulates real time stock price data. Generated data is broadcasted in 10ms intervals to the clients. Clients process this data and send buy or sell order to the server. Response of order is returned to the client by server, then client calculates latency between request and response.

## Prerequisites

* Python 3.10
  * Tested with Python 3.10 on Linux
  * Python versions above 3.6 should work but not tested
* websockets
* tornado
* pandas
* matplotlib (optional)

You can use following command to install required packages
```bash
pip install websockets tornado pandas matplotlib
```

## How to

Open two terminal and run server in one terminal and then run client in other one. Then wait for a while for benchmark result. Both servers and both clients are compatible each other.
```
python3 server_websockets.py
python3 server_tornado.py
python3 client_webstockets.py
python3 client_tornado.py
```

## Results

All data is in milliseconds.

<table>
  <tr>
    <th>Server</th>
    <th>Client</th>
    <th>Avg</th>
    <th>Max</th>
    <th>Min</th>
    <th>Std Dev</th>
  </tr>
  <tr>
    <td>Websockets</td>
    <td>Websockets</td>
    <td>0.64</td>
    <td>1.03</td>
    <td>0.39</td>
    <td>0.12</td>
  </tr>
  <tr>
    <td>Websockets</td>
    <td>Tornado</td>
    <td>0.61</td>
    <td>1.11</td>
    <td>0.36</td>
    <td>0.13</td>
  </tr>
  <tr>
    <td>Tornado</td>
    <td>Tornado</td>
    <td>9.59</td>
    <td>59.37</td>
    <td>0.13</td>
    <td>18.97</td>
  </tr>
  <tr>
    <td>Tornado</td>
    <td>Websockets</td>
    <td>13.34</td>
    <td>50.16</td>
    <td>0.20</td>
    <td>21.68</td>
  </tr>
</table>

According to results tornado clients give a little bit better performance on average but this difference might be negligible.

Also tornado server caused very high peaks on response times, the way it processes tasks in event loop might be the cause of this problem.

### Websockets server to Websockets client
![Websockets server to Websockets client](/results/websockets_server_websockets_client.png)
### Websockets server to Tornado client
![Websockets server to Tornado client](/results/websockets_server_tornado_client.png)
### Tornado server to Tornado client
![Tornado server to Tornado client](/results/tornado_server_tornado_client.png)
### Tornado server to Websockets client
![Tornado server to Websockets client](/results/tornado_server_websockets_client.png)

## License

This application is licensed under the MIT License. See LICENSE file for more details