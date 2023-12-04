from channels.generic.websocket import AsyncWebsocketConsumer
import json
from base.func import calculate_unread_messages
from asgiref.sync import sync_to_async
from base.models import Message

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"notification_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.send_data()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @sync_to_async
    def count_unread_messages(self):
        unread_count = calculate_unread_messages()
        return unread_count
    
    @sync_to_async
    def get_user_data(self):
        data = Message.objects.all()[Message.objects.count()-1]
        return data

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")
        
        if message_type == "unread_count":
            await self.send_data()

        elif message_type == "new_message":
            await self.send_updated_unread_count()

    async def send_data(self):
        unread_count = await self.count_unread_messages()
        context = {
            'unread_count' : unread_count,
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'send_preloaded_count',
                'count' : context,
            }
        )
    async def send_preloaded_count(self,event):
        await self.send(text_data=json.dumps({
            'type':'unread_count',
            'count':event['count'],
        }))

    async def send_updated_unread_count(self):
        unread_count = await self.count_unread_messages()
        data = await self.get_user_data()
        print(data.id)
        context = {
            'unread_count' : unread_count,
            'id' : str(data.id),
            'name' : data.name,
            'subject' : data.subject,
            'email':data.email,
            'body':data.body,
            'created_at' : data.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'update_unread_count',
                'count':context,
            },
        )

    async def update_unread_count(self,event):
        await self.send(text_data=json.dumps({
            'type':'new_message',
            'count':event['count'],
        }))