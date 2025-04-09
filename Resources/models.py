from django.db import models
from categories.models import LibraryCategory
from django.utils.text import slugify


class Library(models.Model):
    id = models.SlugField(primary_key=True, unique=True, editable=False, max_length=60)
    title = models.TextField(max_length=255)
    short_title = models.TextField(blank=True, null=True,max_length=50)
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


    def _generate_unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while Library.objects.filter(id=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.id and self.short_title:
            base_slug = slugify(self.short_title)
            self.id = self._generate_unique_slug(base_slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
