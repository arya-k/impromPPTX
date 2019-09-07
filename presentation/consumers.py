from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class PresentationConsumer(WebsocketConsumer):
    def connect(self):
        if not self.scope["user"].is_authenticated:
            return
        self.room_group_name = 'presentation_%s' % self.scope["user"].username
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'handle_message',
                'message': json.loads(text_data),
            }
        )

    def handle_message(self, event):
        self.send(json.dumps(event['message']))
