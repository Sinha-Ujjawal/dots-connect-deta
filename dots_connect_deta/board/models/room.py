import uuid
from django.db import models
from common.models import BaseModel
from dots_connect_deta.users.models import User


class Room(BaseModel):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="rooms",
        blank=True,
        null=True,
    )


class RoomUser(BaseModel):
    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
        related_name="room_users",
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    channel_name = models.CharField(max_length=255, help_text="Name of the channel")

    class Meta:
        unique_together = [("room", "channel_name")]
