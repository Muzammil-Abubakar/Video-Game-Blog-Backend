from django.contrib import admin
from .models import Post, Category, Comment, Tag, UserProfile


# Enhanced display for Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'views', 'like_count')
    list_filter = ('category', 'created_at', 'tags')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'

# Basic registration for others
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(UserProfile)
