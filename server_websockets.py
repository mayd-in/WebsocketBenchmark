#!/usr/bin/env python

import asyncio
import websockets
import generator
import datetime
import json

class Server:
    def __init__(self) -> None:
        self.__connections = set()

    async def trading_handler(self, websocket):
        async for raw_message in websocket:
            # Assuming trading order is completed
            message = json.loads(raw_message)
            message["type"] = "response"
            message["result"] = "success"
            await websocket.send(json.dumps(message))

    async def broadcast(self) -> None:
        # Generate random stock data
        stock_data_generator = generator.generate_stock_data()
        for price in stock_data_generator:
            message = {
                "type": "broadcast",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "value": price
            }
            websockets.broadcast(self.__connections, json.dumps(message))
            # Sleep for a while to simulate price changes
            await asyncio.sleep(0.001)

    async def server(self, websocket) -> None:
        try:
            print("WebSocket opened")
            # Register user
            self.__connections.add(websocket)
            # Handle trading orders per client
            await self.trading_handler(websocket)
        finally:
            self.__connections.remove(websocket)
            print("WebSocket closed")

async def main():
    server = Server()
    async with websockets.serve(server.server, "localhost", 8765):
        await server.broadcast()  # run forever

if __name__ == "__main__":
    try:
        print("Websocket server started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server closed")