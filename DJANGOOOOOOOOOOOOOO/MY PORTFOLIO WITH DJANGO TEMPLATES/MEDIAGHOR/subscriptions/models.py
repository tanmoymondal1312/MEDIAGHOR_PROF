from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SubscribeModel(models.Model):
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        help_text="Enter a valid email address for subscription"
    )
    subject = models.CharField(
        max_length=255,
        verbose_name="Subscription Subject",
        help_text="Brief description of what they're subscribing to"
    )
    subscriber_name = models.CharField(
        max_length=100,
        default='Not Provided',
        verbose_name="Subscriber Name",
        help_text="Name of the subscriber (optional)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Subscription",
        help_text="Whether this subscription is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.email} - {self.subject}"

    def clean(self):
        """Validate the model before saving"""
        if self.email:
            try:
                validate_email(self.email)
            except ValidationError:
                raise ValidationError({'email': 'Enter a valid email address.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
        
        
class Contact(models.Model):
    sender_name = models.CharField(max_length=20,blank=False)
    sender_mail = models.EmailField(blank=False)
    sender_phone = models.CharField(max_length=20,blank=True,null=True)
   
    title = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True,max_length=5000)
   