from django.contrib import admin
from django.core.mail import send_mail
from django.utils.html import format_html
from .models import SubscribeModel,Contact

@admin.register(SubscribeModel)
class SubscribeModelAdmin(admin.ModelAdmin):
    list_display = [
        'email', 
        'subscriber_name', 
        'subject', 
        'is_active', 
        'created_at', 
        'subscription_actions'
    ]
    
    list_filter = [
        'is_active', 
        'created_at', 
        'subject'
    ]
    
    search_fields = [
        'email', 
        'subscriber_name', 
        'subject'
    ]
    
    readonly_fields = [
        'created_at', 
        'updated_at'
    ]
    
    list_editable = ['is_active']
    
    list_per_page = 20
    
    actions = ['make_active', 'make_inactive', 'send_bulk_email']
    
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('subscriber_name', 'email', 'subject')
        }),
        ('Subscription Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def subscription_actions(self, obj):
        return format_html(
            '<a class="button" href="/admin/{}/{}/{}/change/">Edit</a>',
            obj._meta.app_label,
            obj._meta.model_name,
            obj.id
        )
    subscription_actions.short_description = 'Actions'

    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} subscriptions activated.')
    make_active.short_description = "Activate selected subscriptions"

    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} subscriptions deactivated.')
    make_inactive.short_description = "Deactivate selected subscriptions"

    def send_bulk_email(self, request, queryset):
        """Action to send email to selected subscribers"""
        active_subscribers = queryset.filter(is_active=True)
        
        if not active_subscribers:
            self.message_user(request, "No active subscribers selected.", level='warning')
            return
            
        # This is a basic implementation - customize as needed
        try:
            for subscriber in active_subscribers:
                send_mail(
                    subject=f"Update on: {subscriber.subject}",
                    message=f"Hello {subscriber.subscriber_name},\n\nThis is an update regarding your subscription.\n\nBest regards,\nThe Team",
                    from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
            
            self.message_user(
                request, 
                f"Emails sent to {active_subscribers.count()} subscribers successfully."
            )
        except Exception as e:
            self.message_user(
                request, 
                f"Error sending emails: {str(e)}", 
                level='error'
            )
    send_bulk_email.short_description = "Send email to selected active subscribers"
    
    


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('sender_name','title')
 