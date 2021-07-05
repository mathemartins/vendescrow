import json

from channels.generic.websocket import AsyncWebsocketConsumer


class P2PTradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('p2p', self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('p2p', self.channel_name)

    async def send_new_data(self, event):
        print(event)
        new_data = event['text']
        await self.send(json.dumps(new_data))
