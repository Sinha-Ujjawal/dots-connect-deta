from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/dots/(?P<room_id>[abcdef0-9-]+)/$", consumers.GameConsumer.as_asgi()),
]
