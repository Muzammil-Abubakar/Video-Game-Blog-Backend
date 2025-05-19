from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.PostListAPIView.as_view(), name='post-list'),
    path('posts/', api_views.PostListAPIView.as_view(), name='api-posts'),
    path('posts/<slug:slug>/', api_views.PostDetailAPIView.as_view(), name='api-post-detail'),
    path('categories/', api_views.CategoryListAPIView.as_view(), name='api-categories'),
    path('comments/', api_views.CommentListAPIView.as_view(), name='api-comments'),
]
