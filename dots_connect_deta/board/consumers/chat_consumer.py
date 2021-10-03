from typing import List, Optional, Set
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import uuid
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase
from ..models import Room
from ..selectors import room_get_by_id


@dataclass
class ChannelData:
    game_ids: Set[uuid.UUID] = field(default_factory=set)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class GameIdResponse:
    game_id: str
    me: bool


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        route_kwargs = self.scope["url_route"]["kwargs"]

        self.room_id = route_kwargs["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        self.game_id = uuid.uuid4()

        self.room: Optional[Room] = await self.get_room_by_id()
        if self.room:  # existing room
            self.register_game_id()
            # join the group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
            await self.game_ids_broadcast_signal()
        else:
            await self.close()

    @database_sync_to_async
    def get_room_by_id(self) -> Optional[Room]:
        try:
            return room_get_by_id(room_id=self.scope["url_route"]["kwargs"]["room_id"])
        except Exception:
            return None

    def update_channel_data(self, channel_data: ChannelData):
        setattr(self.channel_layer, self.room_group_name, channel_data)

    def get_channel_data(self) -> ChannelData:
        channel_data = getattr(self.channel_layer, self.room_group_name, None)
        if channel_data is None:
            return ChannelData()
        else:
            return channel_data

    def register_game_id(self):
        channel_data = self.get_channel_data()
        channel_data.game_ids.add(self.game_id)
        self.update_channel_data(channel_data=channel_data)

    def unregister_game_id(self):
        channel_data = self.get_channel_data()
        channel_data.game_ids.discard(self.game_id)
        self.update_channel_data(channel_data=channel_data)

    def get_game_ids(self) -> List[GameIdResponse]:
        channel_data = self.get_channel_data()
        return [
            GameIdResponse(game_id=game_id.hex, me=game_id == self.game_id)
            for game_id in channel_data.game_ids
        ]

    async def disconnect(self, _close_code):
        self.unregister_game_id()
        # leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        await self.game_ids_broadcast_signal()

    async def receive_json(self, json_data):
        message = json_data["message"]

        # send message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "screem_handler",
                "message": message,
            },
        )

    async def screem_handler(self, event):
        message = event["message"]
        # send message to WebSocket
        await self.send_json(content={"message": message})

    async def game_ids_broadcast_signal(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_ids_broadcast_handler",
                "message": None,
            },
        )

    async def game_ids_broadcast_handler(self, _event):
        await self.send_json(
            content=[gameIdRes.to_dict() for gameIdRes in self.get_game_ids()]
        )
