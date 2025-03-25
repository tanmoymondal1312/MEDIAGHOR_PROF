from django.contrib import admin
from .models import CompanyService

@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_for_company_service', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('is_for_company_service', 'created_at')
