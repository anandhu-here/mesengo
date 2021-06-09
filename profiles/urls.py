from profiles.api import profile_action_api_view, profile_page, profiler_search_query
from django.urls import path


urlpatterns=[
    path('api/profile/', profile_page),
    path('api/profile/follow', profile_action_api_view),
    path('api/profile/search', profiler_search_query),
    path('api/profile/action', profile_action_api_view)
]
