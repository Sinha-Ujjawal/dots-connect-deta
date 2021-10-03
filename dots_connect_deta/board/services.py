from dots_connect_deta.users.models import User
from .models import Room


def room_create_room(*, user: User) -> Room:
    if user.is_anonymous:
        user = None
    room = Room(host=user)
    room.save()
    return room
