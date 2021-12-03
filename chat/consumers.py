import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Rooms, Message

class ChatConsumer(AsyncWebsocketConsumer):   
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        '''if channel_obj is not None:
            #print(channel_obj, channel_obj.channel_name)
            #self.channel_name = channel_obj.channel_name
            pass
        else:
            self.channel_name = self.channel_name'''
            

        self.room_group_name = 'chat_%s' % self.room_name

        print('room_group_name', self.room_group_name)        
        print('channel_name', self.channel_name)        
        print('channel_layer', self.channel_layer)  
        print()      
        print(self.scope)
        print(self.scope['user'].username)
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
        print('text_data', text_data_json)
        message = text_data_json['message']

        # Find room object
        room = await  database_sync_to_async(Rooms.objects.get)(room = self.room_name)

        # Creat Message object
        chat = Message(
            msg_content = message,
            room = room,
            author= self.scope['user']
        )

        await  database_sync_to_async(chat.save)()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope['user'].username,
                
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('receive event', event)
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))