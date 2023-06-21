import json

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import TokenError, AccessToken

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Extract the JWT token from the query string
        try:
            token = self.scope["query_string"].decode().split("=")[1]
        except IndexError:
            token = None

        try:
            # Verify and decode the JWT token
            access_token = AccessToken(token)
            # Retrieve the user object from the access token
            user_id = access_token.payload.get('user_id')

            user = User.objects.get(id=user_id)
            self.scope["user"] = user

        except (TokenError, User.DoesNotExist):
            pass

        print(self.scope["user"])
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope["user"].username
        print(message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "username": username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))