import tornado.ioloop
import tornado.web
import tornado.websocket
import generator
import datetime
import json

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        print("WebSocket opened")
        self.clients.add(self)

    def on_message(self, message):
        # Assuming trading order is completed
        message = json.loads(message)
        message["type"] = "response"
        message["result"] = "success"
        self.write_message(json.dumps(message))

    def on_close(self):
        print("WebSocket closed")
        self.clients.remove(self)

# Generate random stock data
stock_data_generator = generator.generate_stock_data()

class PeriodicMessageSender:
    def __init__(self, interval=1):
        self.interval = interval
        self.callback = tornado.ioloop.PeriodicCallback(self.send_messages, interval * 1)
        self.callback.start()

    def send_messages(self):
        price = next(stock_data_generator)
        for client in WebSocketHandler.clients:
            try:
                message = {
                    "type": "broadcast",
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "value": price
                }
                client.write_message(message)
            except Exception as e:
                print(f"Error sending message to client: {e}")

app = tornado.web.Application([(r'/', WebSocketHandler)])

if __name__ == '__main__':
    try:
        print("Tornado server started")
        app.listen(8765)
        periodic_sender = PeriodicMessageSender(interval=1)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Server closed")