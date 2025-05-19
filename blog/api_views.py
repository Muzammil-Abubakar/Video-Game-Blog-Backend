from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post, Category, Comment, UserProfile
from .serializers import PostSerializer, CategorySerializer, CommentSerializer, UserProfileSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save(update_fields=['views'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__username'

class TogglePostLikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        return Response({
            "liked": liked,
            "like_count": post.likes.count()
        })
        
from rest_framework.generics import ListAPIView

class RelatedPostsAPIView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Post.objects.none()

        # Get all tags of the current post
        tags = post.tags.all()

        # Find other posts that share these tags, exclude current post
        return Post.objects.filter(tags__in=tags).exclude(id=post.id).distinct()
