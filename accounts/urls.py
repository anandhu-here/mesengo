from django.urls import path
from . import api, views

from knox import views as knox_views





urlpatterns = [
    path('api/auth/register', api.RegisterAPI.as_view()),
    path('api/auth/login', api.LoginAPI.as_view()),
    path('api/auth/user', api.UserAPI.as_view()),
    path('api/auth/validate_phone', api.VerifyPhoneWithOTPSent.as_view()),
    path('api/auth/validate_otp', api.VerifyOTPSent.as_view()),
    # path('api/auth/upload_selfie', ProfileImageUpload.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]