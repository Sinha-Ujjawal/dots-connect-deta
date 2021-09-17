from dots_connect_deta.users.models import User
from .models import Room


def room_create_room(*, name: str, user: User) -> Room:
    room = Room(name=name, host=user)
    room.save()
    return room
