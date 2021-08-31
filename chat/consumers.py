import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.checks import messages
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_msgs(self, data):
        messages = Message.last_20_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_json(messages)
        }
        self.send_message(content)

    def new_msgs(self, data):
        author_from = data['from']
        #author_to = data['to']
        from_user = User.objects.filter(username=author_from)[0]
        #to_user = User.objects.filter(username=author_to)[0]
        message = Message.objects.create(
            author = from_user,
            msg_content = data['message']
        )
        content = {
            'command': 'new_msgs',
            'message': self.message_json(message)
        }
        return self.send_chat_message(content)



    def messages_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_json(message))
        return result

    def message_json(self, message):
        return{
            'author': message.author.username,
            'content': message.msg_content,
            'time': str(message.time)
        }

    commands = {
        'fetch_messages': fetch_msgs,
        'new_messages': new_msgs,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

        # Send message to room group
    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))     # Send message to WebSocket