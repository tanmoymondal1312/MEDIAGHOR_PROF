from django.db import models

class CompanyService(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='company_services/', blank=True, null=True)
    description = models.TextField()
    is_for_company_service = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title