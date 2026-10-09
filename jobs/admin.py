from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'company',
        'location',
        'salary',
        'job_type',
        'created_at'
    )

    list_filter = ('job_type', 'location')

    search_fields = ('title', 'company', 'location')

    ordering = ('-created_at',)