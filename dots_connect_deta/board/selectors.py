from typing import List, Optional
import uuid
from dots_connect_deta.users.models import User
from django.db.models import Q
from .models import Room


def room_get_data(*, room: Room):
    return {
        "roomId": room.room_id,
        "host": room.host.id if room.host else None,
    }


def room_get_by_id(*, room_id: uuid.UUID) -> Optional[Room]:
    try:
        return Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        return None


def room_get_rooms(*, user: User) -> List[Room]:
    if user.is_anonymous:
        user = None
    return Room.objects.filter(Q(host=user) | Q(host__isnull=True)).all()
