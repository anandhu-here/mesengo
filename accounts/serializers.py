  
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model() 
# User Serializer
class UserSerializer(serializers.ModelSerializer):
  profile_picture = serializers.SerializerMethodField(read_only=True)
  user_profile_id = serializers.SerializerMethodField(read_only=True)
  class Meta:
    model = User
    fields = ('id', 'first_name','last_name', 'email', 'profile_picture','user_profile_id')
  def get_profile_picture(self, obj):
    dp = obj.profile.profile_picture
    if dp:
      return dp.url
    else: return " " 
  def get_user_profile_id(self, obj):
    return obj.profile.id

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'password', 'first_name', 'last_name')
    extra_kwargs = {'password': {'write_only': True}}
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()
  def validate(self, data):
    try:
      user = User.objects.get(email=data['email'])
      print(user.email)
    except User.DoesNotExist:
      raise serializers.ValidationError("Incorrect Credentials")
    user = authenticate(email=user.email, password=data['password'])
    print(user, data, "popo")
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")



