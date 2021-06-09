from rest_framework import generics, permissions, views, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
import random
from .models import PhoneOTP
from django.contrib.auth import get_user_model
from rest_framework import parsers
from  rest_framework.permissions import IsAuthenticated

User = get_user_model()

# Register API
class RegisterAPI(generics.GenericAPIView):
  serializer_class = RegisterSerializer
  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })

# Login API
class LoginAPI(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    _, token = AuthToken.objects.create(user)
    print(token, "token")
    return Response({
      "user": UserSerializer(user, context=self.get_serializer_context()).data,
      "token": token
    })

# Get User API
class UserAPI(generics.RetrieveAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
  )
  serializer_class = UserSerializer
  def get_object(self):
    return self.request.user




class VerifyPhoneWithOTPSent(views.APIView):
  def get_otp(self, phone):
    otp = random.randrange(00000,99999)
    print(otp)
    return otp

  def send_otp(self, otp):
    return True

  def post(self,request, *args, **kwargs):
    phone = request.data.get('phone')
    print(phone,"maireee")
    if phone:
      otp = self.get_otp(phone)
      if otp:
        old_phone_user = PhoneOTP.objects.filter(phone__iexact=phone)
        if old_phone_user.exists():
          old_phone_user=old_phone_user.first()
          count = old_phone_user.count
          old_phone_user.count = count+1
          old_phone_user.otp = str(otp)
          old_phone_user.save()
        else:
          count = 0
          print("motherfuckerssss")
          PhoneOTP.objects.create(phone=phone, otp=str(otp), count=count)
        send = self.send_otp(otp)
        if send:
          return Response({
            'status':'otp-created',
            'data': 'otp created and send successfully'
          })
        else:
          return Response({
            'status':'failed',
            'data':'otp send error'
          })


class VerifyOTPSent(views.APIView):
  def post(self, request, *args, **kwargs):
    otp = request.data.get('otp')
    phone = request.data.get('phone')
    if phone and otp:
      phone_user = PhoneOTP.objects.get(phone=phone)
      phone_user_otp = phone_user.otp
      if phone_user_otp == otp:

        return Response({
          'status':'otp-verified',
          "data":"Successfully validated otp"
        })
      else:
        return Response({
        'status':'failed',
          "data":"UnSuccessfully validated otp"
          })



# class ProfileImageUpload(views.APIView):
#   permission_classes = (IsAuthenticated,)
#   def put(self, request, *args, **kwargs):
#     user = self.request.user
#     profile = Profile.objects.get(user=user)
#     data = {'user':user, 'image':request.data.get('image')}
#     serializer = ProfileSerializer(profile)
#     if serializer:
#       return Response(serializer.data, status=201)
#     else:
#       return Response(serializer.errors, status=400) 