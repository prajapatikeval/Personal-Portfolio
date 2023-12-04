from .models import Message

def calculate_unread_messages():
    unreadMessages = Message.objects.filter(is_read=False).count()
    return unreadMessages
