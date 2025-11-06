from django.db import models
from django.utils.text import slugify


class CompanyService(models.Model):
    id = models.SlugField(primary_key=True, unique=True, editable=False, max_length=60)
    title = models.CharField(max_length=100)
    short_title = models.TextField(blank=True, null=True,max_length=50)
    image = models.ImageField(upload_to='company_services/', blank=True, null=True)
    description = models.TextField()
    explanation = models.TextField(blank=True, null=True,max_length=5000)
    is_for_company_service = models.BooleanField(default=True)
    priority = models.IntegerField(default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def _generate_unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while CompanyService.objects.filter(id=slug).exists():
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