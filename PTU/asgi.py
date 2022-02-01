"""
ASGI config for PTU project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path, re_path
import chat.routing
from dm.consumers import DmConsumer
from chat.consumers import ChatConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PTU.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
            #dm.routing.websocket_urlpatterns
        )
    ),
})

# application = ProtocolTypeRouter({
#     #"http": get_asgi_application(),
# 	'websocket': AllowedHostsOriginValidator(
# 		AuthMiddlewareStack(
# 			URLRouter([
# 					#path('', NotificationConsumer),
# 					path('dm/<room_id>/', DmConsumer),
# 					path('chat/<room_name>/', ChatConsumer),
# 			])
# 		)
# 	),
# })