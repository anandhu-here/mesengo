from django.urls import path 
from .api import create_api_messages, get_api_conversations, get_api_messages
urlpatterns = [
    path('api/messenger/', get_api_conversations),
    path('api/messenger/chat', get_api_messages),
    path('api/messenger/create_message', create_api_messages)
]
