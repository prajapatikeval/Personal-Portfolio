from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # re_path("ws/notification/", consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/notification/(?P<room_name>\w+)/$", consumers.NotificationConsumer.as_asgi()),
]