from django.contrib import admin
from .models import Library

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_for_libraries', 'created_at', 'updated_at')
    search_fields = ('title', 'library_link', 'description')
    list_filter = ('is_for_libraries', 'created_at')