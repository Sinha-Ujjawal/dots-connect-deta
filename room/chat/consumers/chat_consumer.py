import json
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, _close_code):
        pass

    def receive_json(self, json_data):
        message = json_data["message"]
        self.send_json(content={"message": message[::-1]})
