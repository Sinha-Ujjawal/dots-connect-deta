from typing import Set
from django import dispatch
from asgiref.sync import async_to_sync
from .channel import CHANNEL_LAYER
from .models import Room

BROADCAST_JOINED_USERS = dispatch.Signal(providing_args=["rooms"])


@dispatch.receiver(BROADCAST_JOINED_USERS)
def handle_broadcast_joined_users_signal(rooms: Set[Room], **_kwargs):
    for room in rooms:
        async_to_sync(CHANNEL_LAYER.group_send)(
            f"chat_{room.room_id}",
            {
                "type": "broadcast_joined_users_infos_handler",
                "message": None,
            },
        )
