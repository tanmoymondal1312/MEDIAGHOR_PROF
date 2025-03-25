from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='blog_posts/', blank=True, null=True)
    post_content = models.TextField()
    full_post_content = models.TextField(blank=True, null=True)
    is_for_blog_posts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
