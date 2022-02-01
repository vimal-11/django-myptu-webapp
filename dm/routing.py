from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dm/(?P<room_id>\w+)/$', consumers.DmConsumer.as_asgi()),
]