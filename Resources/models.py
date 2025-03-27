from django.db import models
from categories.models import LibraryCategory

class Library(models.Model):
    title = models.TextField(max_length=255)
    short_title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    library_link = models.TextField(max_length=500)  # Changed from URLField to CharField
    how_to_use = models.TextField(blank=True, null=True)
    is_for_libraries = models.BooleanField(default=True)
    copy = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        LibraryCategory, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='libraries'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
