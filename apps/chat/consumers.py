import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import TokenError, AccessToken
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.chat.models import Message, Room

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            token = self.scope["query_string"].decode().split("=")[1]
        except IndexError:
            token = None

        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            user = await self.get_user(user_id)
            self.scope["user"] = user
        except (TokenError, User.DoesNotExist):
            pass

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.room = await self.get_or_create_room(self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

        # Retrieve and send message history
        messages = await self.get_message_history()
        for message in messages:
            await self.chat_message(message)

        if self.scope["session"].get("anonymous"):
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": "Joined the chat",
                    "username": ""
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            username = await self.get_username()

            await self.create_message(username, message)

            if text_data_json.get("anonymous"):
                self.scope["session"]["anonymous"] = True
                username = "AnonymousUser"

            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "message": message,
                    "username": username
                }
            )
        except json.JSONDecodeError as e:
            # Handle the JSONDecodeError here
            print("Error decoding JSON:", e)

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username
        }))

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_username(self):
        if self.scope["user"].is_authenticated:
            return self.scope["user"].username
        elif self.scope["session"].get("anonymous"):
            return "AnonymousUser"
        else:
            return "Guest"

    @database_sync_to_async
    def get_or_create_room(self, room_name):
        return Room.objects.get_or_create(room_name=room_name)[0]

    @database_sync_to_async
    def get_message_history(self):
        messages = Message.objects.filter(room=self.room).order_by('timestamp')
        return list(messages.values('message', 'username', 'timestamp'))

    @database_sync_to_async
    def create_message(self, username, message):
        return Message.objects.create(room=self.room, username=username, message=message)
