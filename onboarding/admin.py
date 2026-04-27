from django.contrib import admin
from .models import JobApplication, JobPosition


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'department', 'is_active', 'created_at']
    list_filter = ['is_active', 'department']
    search_fields = ['title', 'department']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'position', 'current_role', 'years_of_experience', 'status', 'extraction_successful', 'applied_at']
    list_filter = ['status', 'extraction_successful', 'position']
    search_fields = ['full_name', 'email', 'skills', 'current_role']
    readonly_fields = ['applied_at', 'raw_extracted_text', 'extraction_successful']
    fieldsets = (
        ('Application Info', {
            'fields': ('position', 'resume', 'status', 'applied_at')
        }),
        ('Extracted Personal Info', {
            'fields': ('full_name', 'email', 'phone', 'location', 'linkedin', 'github')
        }),
        ('Extracted Professional Info', {
            'fields': ('current_role', 'years_of_experience', 'skills', 'summary')
        }),
        ('Extracted Details', {
            'fields': ('education', 'work_experience'),
            'classes': ('collapse',)
        }),
        ('Extraction Meta', {
            'fields': ('extraction_successful', 'raw_extracted_text'),
            'classes': ('collapse',)
        }),
    )
