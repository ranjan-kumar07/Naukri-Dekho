from django.contrib import admin
from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'company',
        'location',
        'job_type',
        'vacancies',
        'application_deadline',
        'created_at'
    )

    search_fields = (
        'title',
        'company',
        'location'
    )

    list_filter = (
        'job_type',
        'created_at'
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'job',
        'status',
        'applied_at',
        'updated_at'
    )

    search_fields = (
        'user__username',
        'job__title'
    )

    list_filter = (
        'status',
        'applied_at'
    )