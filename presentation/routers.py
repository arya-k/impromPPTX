from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/presentation/<presentation_id>/',
         consumers.PresentationConsumer),
]
