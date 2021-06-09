from messenger.models import Conversation, FileMessage, Message
from django.contrib import admin

# Register your models here.

admin.site.register((Conversation, Message, FileMessage,))