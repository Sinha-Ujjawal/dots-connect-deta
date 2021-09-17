from typing import List, Optional
import uuid
from room.users.models import User
from .models import Room


def room_get_data(*, room: Room):
    return {"roomId": room.room_id, "name": room.name}


def room_get_by_id(*, room_id: uuid.UUID) -> Optional[Room]:
    try:
        return Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        return None


def room_get_rooms(*, user: User) -> List[Room]:
    return Room.objects.filter(host=user).all()
