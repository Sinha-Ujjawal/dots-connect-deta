from django.urls import path
from .views import CreateRoom, ListRooms, renderers

urlpatterns = [
    path("room", CreateRoom.as_view(), name="room_create"),
    path("rooms", ListRooms.as_view(), name="room_list"),
    path("", renderers.index, name="index"),
    path("<str:room_name>", renderers.room, name="room"),
]
