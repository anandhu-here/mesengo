from django.db.models.query_utils import Q
from messenger.models import Conversation
from django.db.models import fields
from rest_framework import serializers

from .models import Profile

class ProfileActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ['follow', 'unfollow', 'block', 'banish']:
            raise serializers.ValidationError('Invalid action')
        return value
        
class ProfileSearchSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'profile_picture')

    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    def get_profile_picture(self, obj):
        dp = obj.user.profile.profile_picture
        if dp:
            return dp.url
        else: return " " 

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    email = serializers.SerializerMethodField(read_only=True)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_followed = serializers.SerializerMethodField(read_only=True)
    conver_id_direct = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "id",
            "bio",
            "follower_count",
            "following_count",
            "is_following",
            "email",
            "profile_picture",
            "is_followed",
            "conver_id_direct"
        ]
    
    def get_is_following(self, obj):
        # request???
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_following_count(self, obj):
        return obj.user.following.count()
    
    def get_follower_count(self, obj):
        return obj.followers.count()

    def get_is_followed(self, obj):
        return self.context['request'].user in obj.followers.all()

    def get_conver_id_direct(self, obj):
        c_user = self.context['request'].user 
        conver = Conversation.objects.filter((Q(user_1=c_user)|Q(user_2=c_user)) & (Q(user_1=obj.user)|Q(user_2=obj.user)))
        if conver.exists():
            return conver.first().id
        return None
        