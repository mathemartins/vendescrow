from channels.consumer import AsyncConsumer


class P2PTradeConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({'type': 'websocket.accept'})
        await self.send({'type': 'websocket.send', 'text': 'Hello World'})
