from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import socket


class PresentationConsumer(WebsocketConsumer):

    def connect(self):
        if not self.scope["user"].is_authenticated:
            return
        self.room_group_name = 'presentation_%s' % self.scope["user"].username
        self.page_type = self.scope['url_route']['kwargs']['page_type']
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
        data = event['message']
        if data['page_type'] == self.page_type:
            return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("localhost", 9999))
        s.sendall(json.dumps(data).encode())
        full_deets = []
        deets = s.recv(1024).decode().strip()
        while deets:
            full_deets.append(deets)
            deets = s.recv(1024).decode().strip()
        the_full_deets = ''.join(full_deets)
        self.send(json.dumps({'update': json.loads(the_full_deets)}))
