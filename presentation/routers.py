from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/presentation/<page_type>/',
         consumers.PresentationConsumer),
]
