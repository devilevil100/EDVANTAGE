import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from users.models import User_profile, Tutor, Room, Message
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['disc'] == "yes":
            await self.close()
        else:
            message = text_data_json['message']
            userID = text_data_json['userID']
            # Send message to room group
            authorr = User.objects.get(id=userID)
            chatroom = Room.objects.get(name=self.room_name)
            newmsg = Message(author=authorr, content=message, room=chatroom)
            newmsg.save()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'userID': userID
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        userID = event['userID']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'userID': userID
        }))