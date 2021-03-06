from accounts.models import User
import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import TweetForm
from .models import Post
from .serializers import (
    PostActionSerializer,
    PostSerializer,
    PostCreateSerializer
)
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['POST']) # http method the client == POST
@parser_classes((MultiPartParser, ))
@permission_classes([IsAuthenticated]) # REST API course
def post_create_view(request, *args, **kwargs):
    print(request.data, "data")
    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def post_detail_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this post"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "post removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, repost
    '''
    print(request.data, "dtaa")
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            if request.user in obj.likes.all():
                obj.likes.remove(request.user)
                print(obj.likes.count(), "like")
            else:
                obj.likes.add(request.user)
                print(obj.likes.count(), "not like")
            serializer = PostSerializer(obj, context={"request": request})
            return Response(serializer.data, status=200)
        elif action == "repost":
            new_post = Post.objects.create(
                    user=request.user, 
                    parent=obj,
                    content=content,
                    )
            serializer = PostSerializer(new_post)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = PostSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_feed_view(request, *args, **kwargs):
    user = request.user
    qs = Post.objects.feed(user)
    return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_list_view(request, *args, **kwargs):
    qs = Post.objects.filter(user__profile__id=int(request.GET['id']))
    print(qs, "mayirrr")
    return get_paginated_queryset_response(qs, request)


