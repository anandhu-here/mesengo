from django.urls import path
from .api import (
    post_create_view,
    post_action_view,
    post_delete_view,
    post_detail_view,
    post_feed_view,
    post_list_view
)
urlpatterns = [
    path('api/posts/create', post_create_view, name='create'),
    path('api/posts/delete',post_delete_view, name='delete'),
    path('api/posts/detail', post_detail_view, name='detail'),
    path('api/posts/action',post_action_view, name='action'),
    path('api/posts/feed', post_feed_view, name='feed'),
    path('api/posts/posts', post_list_view, name='posts')
]
