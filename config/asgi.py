"""
ASGI config for DOTS-CONNECT-DETA.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import dots_connect_deta.board.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings..base")

application = ProtocolTypeRouter(
    application_mapping={
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(dots_connect_deta.board.routing.websocket_urlpatterns)
        ),
    }
)
