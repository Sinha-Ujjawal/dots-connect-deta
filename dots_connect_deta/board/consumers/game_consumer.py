from typing import List, Optional
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from ..models import Room, RoomUser
from ..services import room_join_user, room_leave_user
from ..selectors import room_get_by_id, room_get_joined_users, room_user_get_data


class GameConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        route_kwargs = self.scope["url_route"]["kwargs"]

        self.room_id = route_kwargs["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        self.room: Optional[Room] = await self.get_room_by_id()

        if self.room:  # existing room
            self.room_user = await self.join_room()
            # join the group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
            await self.broadcast_joined_users_infos()
        else:
            await self.close()

    @database_sync_to_async
    def join_room(self) -> RoomUser:
        return room_join_user(
            room=self.room,
            user=self.scope["user"],
            channel_name=self.channel_name,
        )

    @database_sync_to_async
    def leave_room(self) -> bool:
        return room_leave_user(room_user=self.room_user)

    @database_sync_to_async
    def get_room_by_id(self) -> Optional[Room]:
        try:
            return room_get_by_id(room_id=self.scope["url_route"]["kwargs"]["room_id"])
        except Exception:
            return None

    @database_sync_to_async
    def get_joined_users(self) -> List[RoomUser]:
        return list(room_get_joined_users(room=self.room))

    async def disconnect(self, _close_code):
        # leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )
        if self.room:
            await self.leave_room()
            await self.broadcast_joined_users_infos()

    async def receive_json(self, json_data):
        message = json_data["message"]
        logging.info(f"Received: {message}")
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

    async def broadcast_joined_users_infos(self):
        logging.info("Broadcasting Joined Users")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "broadcast_joined_users_infos_handler",
                "message": None,
            },
        )

    async def broadcast_joined_users_infos_handler(self, _event):
        joined_users = await self.get_joined_users()
        await self.send_json(
            content=[
                {
                    **room_user_get_data(room_user=room_user),
                    "me": self.room_user == room_user,
                }
                for room_user in joined_users
            ]
        )
