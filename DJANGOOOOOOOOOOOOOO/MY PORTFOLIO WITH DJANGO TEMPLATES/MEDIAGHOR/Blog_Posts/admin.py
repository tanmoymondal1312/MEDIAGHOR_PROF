from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_for_blog_posts', 'created_at', 'updated_at')
    search_fields = ('title', 'post_content')
    list_filter = ('is_for_blog_posts', 'created_at')
