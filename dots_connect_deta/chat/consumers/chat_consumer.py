from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        route_kwargs = self.scope["url_route"]["kwargs"]
        self.room_name = route_kwargs["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # join the room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, _close_code):
        # leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive_json(self, json_data):
        message = json_data["message"]

        # send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    async def chat_message(self, event):
        message = event["message"]

        # send message to WebSocket
        await self.send_json(content={"message": message})
