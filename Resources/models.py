from django.db import models

class Library(models.Model):
    title = models.TextField(max_length=255)
    description = models.TextField(blank=True, null=True)
    library_link = models.TextField(max_length=500)  # Changed from URLField to CharField
    how_to_use = models.TextField(blank=True, null=True)
    is_for_libraries = models.BooleanField(default=True)
    coppy = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
