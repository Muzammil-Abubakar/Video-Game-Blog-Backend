from rest_framework import serializers
from .models import Post, Category, Comment, Tag, UserProfile
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    tags = TagSerializer(many=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'content',
            'created_at', 'updated_at', 'category',
            'tags', 'views', 'like_count'
        ]

    def get_like_count(self, obj):
        return obj.likes.count()

class UserProfileSerializer(serializers.ModelSerializer):
    saved_posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'saved_posts']

