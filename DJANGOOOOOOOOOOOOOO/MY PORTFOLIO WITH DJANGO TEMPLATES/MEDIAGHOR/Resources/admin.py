from django.contrib import admin
from .models import Library,ResourceRequest,ResourcesPublisher

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_for_libraries', 'created_at', 'updated_at')
    search_fields = ('title', 'library_link', 'description')
    list_filter = ('is_for_libraries', 'created_at')
    
    




@admin.register(ResourceRequest)
class ResourcesRequestAdmin(admin.ModelAdmin):
    list_display = ('resource_title', 'category', 'email')
    search_fields = ('resource_title', 'resource_description', 'category')
    
    
    
@admin.register(ResourcesPublisher)
class ResourcesPublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'email')
    search_fields = ('email', 'name', 'number')
    
    