from typing import Optional
import uuid
from django.db.models.query import QuerySet
from django.db.models import Q
from dots_connect_deta.users.models import User
from .models import Room, RoomUser


def room_get_data(*, room: Room):
    return {
        "roomId": room.room_id.hex,
        "host": room.host_id,
    }


def room_get_by_id(*, room_id: uuid.UUID) -> Optional[Room]:
    try:
        return Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        return None


def room_get_rooms(*, user: User) -> QuerySet[Room]:
    if user.is_anonymous:
        user = None
    return Room.objects.filter(Q(host=user) | Q(host__isnull=True))


def room_user_get_data(*, room_user: RoomUser):
    return {
        "roomId": room_user.room_id.hex,
        "user": room_user.user_id,
        "channelName": room_user.channel_name,
    }


def room_get_joined_users(*, room: Room) -> QuerySet[RoomUser]:
    return RoomUser.objects.filter(room=room)
