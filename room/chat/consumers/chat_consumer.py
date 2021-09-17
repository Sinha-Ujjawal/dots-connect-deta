import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        route_kwargs = self.scope["url_route"]["kwargs"]
        self.room_name = route_kwargs["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # join the room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, _close_code):
        # leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive_json(self, json_data):
        message = json_data["message"]

        # send message to the group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )

    def chat_message(self, event):
        message = event["message"]

        # send message to WebSocket
        self.send_json(content={"message": message})
