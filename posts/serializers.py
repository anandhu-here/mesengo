from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Post

MAX_TWEET_LENGTH = 1000
TWEET_ACTION_OPTIONS = ["like", "unlike", "repost"]

class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets")
        return value


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['user', 'id', 'content', 'likes', 'timestamp', 'image']
    
    def get_likes(self, obj):
        return obj.likes.count()
    def get_user(self, obj):
        return obj.user.first_name
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long")
        return value

    # def get_user(self, obj):
    #     return obj.user.id


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    profile_picture = serializers.SerializerMethodField(read_only = True)
    post_profile_id = serializers.SerializerMethodField(read_only = True)
    parent = PostCreateSerializer(read_only=True)
    class Meta:
        model = Post
        fields = [
                'user', 
                'id', 
                'content',
                'likes',
                'is_repost',
                'profile_picture',
                'parent',
                'image',
                'is_liked',
                'post_profile_id',
                'timestamp']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_post_profile_id(self, obj):
        return obj.user.profile.id
    def get_user(self, obj):
        return str(obj.user.first_name) + " " + str(obj.user.last_name)
    def get_is_liked(self, obj):
        if self.context['request'].user in obj.likes.all():
            return True
        else: return False
    def get_profile_picture(self, obj):
        dp = obj.user.profile.profile_picture
        if dp:
            return dp.url
        else: return " " 