"""
ASGI config for DOTS-CONNECT-DETA.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import dots_connect_deta.chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings..base")

application = ProtocolTypeRouter(
    application_mapping={
        "http": get_asgi_application(),
        "websocket": URLRouter(dots_connect_deta.chat.routing.websocket_urlpatterns),
    }
)
