from django.urls import path
from .views import CreateRoom, ListRooms

urlpatterns = [
    path("room", CreateRoom.as_view(), name="room_create"),
    path("rooms", ListRooms.as_view(), name="room_list"),
]
