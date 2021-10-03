import uuid
from django.db import models
from common.models import BaseModel
from dots_connect_deta.users.models import User


class Room(BaseModel):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="rooms", blank=True, null=True
    )
