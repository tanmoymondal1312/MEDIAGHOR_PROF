from django.db import models
from categories.models import LibraryCategory
from django.utils.text import slugify
from django.utils import timezone






class ResourcesPublisher(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=100, default="admin@gmail.com", blank=True)
    number = models.CharField(max_length=20, default="01736008374", blank=True)  # ✅ use CharField for phone
    def __str__(self):
        return self.name


class Library(models.Model):
    id = models.SlugField(primary_key=True, unique=True, editable=False, max_length=60)
    title = models.TextField(max_length=255)
    short_title = models.TextField(blank=True, null=True,max_length=50)
    description = models.TextField(blank=True, null=True)
    library_link = models.TextField(max_length=500)  # Changed from URLField to CharField
    how_to_use = models.TextField(blank=True, null=True)
    is_for_libraries = models.BooleanField(default=True)
    copy = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)
    publisher = models.ForeignKey(ResourcesPublisher,blank=True,null=True, on_delete=models.CASCADE)  # ✅ Added this line


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




class ResourceRequest(models.Model):
    """
    Model to store resource requests from users
    """
    URGENCY_CHOICES = [
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    resource_title = models.CharField(max_length=300)
    category = models.ForeignKey(LibraryCategory, on_delete=models.CASCADE)
    resource_description = models.TextField()
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.resource_title} - {self.full_name}"