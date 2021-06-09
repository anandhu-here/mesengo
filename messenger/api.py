from profiles.models import Profile
from django.core.checks import messages
from messenger.serializer import ConversationSerializer, MessagesCreateSerializer, MessagesSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from django.db.models import Q
import requests, json

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_api_conversations(request, *args, **kwargs):
    user = request.user
    conver = Conversation.objects.filter(Q(user_1=user)|Q(user_2=user))
    if conver.exists():
        serializer = ConversationSerializer(conver, many=True, context = {'request':request})
        return Response(serializer.data, status = 200)
    return Response({}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_api_messages(request, *args, **kwargs):
    user = request.user
    id_ = request.GET['id']
    profile_id = request.GET['profile_id']
    if id_ == 'null':
        return Response([], status=404)
    conversation = Conversation.objects.get(id=int(id_))
    messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
    serializer = MessagesSerializer(messages, many=True)
    return Response(serializer.data, status=200)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_api_messages(request, *args, **kwargs):
    user = request.user
    conver_id = request.data['conver_id']
    profile_id = request.data['profile_id']
    other_user = Profile.objects.get(id=int(profile_id)).user
    message = request.data['message']
    conver = Conversation.objects.filter((Q(user_1=user)|Q(user_2=user)) & (Q(user_1=other_user)|Q(user_2=other_user))).first()
    if conver:
        new_message_obj = Message.objects.create(
            conversation=conver,
            sender = user,
            reciever = other_user,
            message = message
        )
        serializer = MessagesSerializer(new_message_obj)
    else:
        new_conver = Conversation.objects.create(
            user_1=user,
            user_2 = other_user
        )
        new_message_obj = Message.objects.create(
            conversation=new_conver,
            sender = user,
            reciever = other_user,
            message = message
        )
        serializer = MessagesSerializer(new_message_obj)
    return Response(serializer.data, status=201)