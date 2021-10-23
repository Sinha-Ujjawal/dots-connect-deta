from datetime import timedelta
from asgiref.sync import async_to_sync
from typing import List, Optional
from django.utils import timezone
from django.conf import settings
from django.db.models.query_utils import Q
from dots_connect_deta.users.models import User
from .models import Room, RoomUser
from .channel import CHANNEL_LAYER
from .signal import BROADCAST_JOINED_USERS


def room_create_room(*, user: User) -> Room:
    if user.is_anonymous:
        user = None
    room = Room(host=user)
    room.save()
    return room


def room_join_user(*, room: Room, user: User, channel_name: str) -> RoomUser:
    if user.is_anonymous:
        user = None
    room_user = RoomUser(
        room=room,
        user=user,
        channel_name=channel_name,
    )
    room_user.save()
    return room_user


def room_leave_user(*, room_user: RoomUser) -> bool:
    room_user.delete()
    return True


def room_update_last_seen(*, room_user: RoomUser) -> bool:
    room_user.last_seen = timezone.now()
    room_user.save()
    return True


def prune_stale_users_from_room(age_in_seconds: Optional[int] = None):
    if age_in_seconds is None:
        age_in_seconds = getattr(settings, "CHANNELS_CONNECTION_MAX_AGE", 60)
    room_users: List[RoomUser] = RoomUser.objects.filter(
        Q(last_seen__lt=timezone.now() - timedelta(seconds=age_in_seconds))
    )
    rooms = set()
    for room_user in room_users:
        rooms.add(room_user.room)
        async_to_sync(CHANNEL_LAYER.group_discard)(
            f"chat_{room_user.room_id}",
            room_user.channel_name,
        )
        room_user.delete()
    BROADCAST_JOINED_USERS.send(
        prune_stale_users_from_room.__class__,
        rooms=rooms,
    )
