from django.core.checks import messages
from .models import Conversation, Message
from rest_framework import serializers




class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Conversation
        fields = ('user', 'timestamp', 'id')

    def get_user(self, obj):
        cur_user = self.context['request'].user
        
        if obj.user_1 == cur_user:
            dp = obj.user_2.profile.profile_picture
            if dp: dp=dp.url
            else: dp=""
            return {"name":obj.user_2.first_name, "profile_picture":dp, 'profile_id':obj.user_2.profile.id}
        dp = obj.user_1.profile.profile_picture
        if dp: dp=dp.url
        else: dp=""
        return {"name":obj.user_1.first_name, "profile_picture":dp, 'profile_id':obj.user_2.profile.id}


class MessagesSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)
    reciever = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Message
        fields = ('message', 'timestamp', 'id','sender', 'reciever')

    def get_sender(self, obj):
        return obj.sender.first_name
    def get_reciever(self, obj):
        return obj.reciever.first_name
    
    
class MessagesCreateSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)
    reciever = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Message
        fields = ('message', 'timestamp', 'id','sender', 'reciever')

    def get_sender(self, obj):
        return obj.sender.first_name
    def get_reciever(self, obj):
        return obj.reciever.first_name
    
    def validate_message(self, value):
        if(len(value)>500):
            raise serializers.ValidationError("This tweet is too long")
        return value
    
