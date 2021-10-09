from dots_connect_deta.users.models import User
from .models import Room, RoomUser


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
