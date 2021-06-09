
from messenger.models import Conversation
from accounts.models import User
from .models import Profile
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProfileActionSerializer, ProfileSearchSerializer, PublicProfileSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination



def get_paginated_queryset_response(qs, size, request):
    paginator = PageNumberPagination()
    paginator.page_size = size
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = ProfileSearchSerializer(paginated_qs, many=True, context={"request": request})
    print(serializer.data, "ppp")
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_page(request, *args, **kwargs):
    id_ = int(request.GET['id'])
    profile = Profile.objects.get(id=id_)
    if profile:
        serializer = PublicProfileSerializer(profile, context={'request':request})
        print(serializer.data, "ll")
        return Response({"profile":serializer.data}, status=200)
    return Response({}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profiler_search_query(request, *args, **kwargs):
    query = request.GET['query']
    size = request.GET['size']
    if query:
        qs = Profile.objects.filter(Q(user__first_name__startswith=query) | Q(user__last_name__startswith=query))
        return get_paginated_queryset_response(qs,size, request)
    return Response({}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_action_api_view(request, *args, **kwargs):
    serializer = ProfileActionSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        profile_id = data.get("id")
        action = data.get('action')
        profile = Profile.objects.get(id=profile_id)
        if not profile:
            return Response({}, status=404)
        if action == 'follow':
            if request.user not in profile.followers.all():
                profile.followers.add(request.user)
                profile.save()
                serializer = PublicProfileSerializer(profile, context={'request':request})
                return Response(serializer.data, status = 201)
            else: 
                profile.followers.remove(request.user)
                profile.save()
                serializer = PublicProfileSerializer(profile, context={'request':request})
                return Response(serializer.data, status = 202)
        else:
            return Response({}, status=400)
    else:
        return Response({}, status=400)
    